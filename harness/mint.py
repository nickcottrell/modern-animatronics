"""
mint -- reconstruct the essay from coords/.

For every sentence: KEY passes through as its verbatim slice; STEERED is built
from its coordinates and sent through the provenance gate (jeff_bridge). Each
section is rebuilt by replacing only its STEERED spans inside the section raw,
back to front so earlier offsets stay valid. Untouched bytes -- separators,
blank lines, every KEY sentence, all whitespace -- survive exactly.

With no sentence promoted to STEERED, the output is the locked essay byte for
byte. That is the floor the whole instrument stands on: an all-KEY mint is a
no-op, and verify proves it.

Run:  python -m harness.mint            (writes generations/essay.minted.md)
      python -m harness.mint --plan     (writes the STEERED prompt plan only)
"""

import json
import sys
from pathlib import Path

from . import record
from . import prompt as prompt_mod
from . import jeff_bridge


def rebuild_section(section, rendered):
    """Apply STEERED renders to a section raw. rendered maps (index,i)->text."""
    raw = section["raw"]
    edits = []
    for i, sent in enumerate(section["sentences"]):
        if sent["tier"] == record.STEERED:
            key = (section["index"], i)
            if key in rendered:
                edits.append((sent["start"], sent["end"], rendered[key]))
    for start, end, text in sorted(edits, reverse=True):
        raw = raw[:start] + text + raw[end:]
    return raw


def build_plan(repo_root):
    """Every STEERED sentence with its deterministic (system, prompt)."""
    _index, sections = record.load_doc(repo_root)
    voice = record.load_voice(repo_root)
    plan = []
    for section in sections:
        for i, sent in enumerate(section["sentences"]):
            if sent["tier"] == record.STEERED:
                system, prompt = prompt_mod.build_prompt(sent, voice)
                plan.append({
                    "section": section["index"],
                    "sentence": i,
                    "target": sent["text"],
                    "system": system,
                    "prompt": prompt,
                })
    return plan


def mint(repo_root, write=True):
    out, records = mint_detailed(repo_root, write=write)
    return out, len(records)


def mint_detailed(repo_root, write=True, pins=None):
    """Mint, and return (out, per_sentence_records).

    Each STEERED sentence yields a record of exactly what the model was asked and
    what it returned -- the raw material the custody receipt binds. KEY sentences
    produce no record because the model never sees them.

    pins may be supplied to override the on-disk pins (e.g. to mint the same
    locked dataset through a different gated model). Defaults to pins.json.
    """
    from . import custody

    _index, sections = record.load_doc(repo_root)
    voice = record.load_voice(repo_root)
    pins = pins or jeff_bridge.load_pins(repo_root)

    rendered = {}
    records = []
    for section in sections:
        for i, sent in enumerate(section["sentences"]):
            if sent["tier"] != record.STEERED:
                continue
            system, prompt = prompt_mod.build_prompt(sent, voice)
            text, receipt = jeff_bridge.mint_one(pins, system, prompt)
            rendered[(section["index"], i)] = text
            verification = receipt.get("verification", {})
            records.append({
                "section": section["index"],
                "sentence": i,
                "ground": sent.get("ground", ""),
                "prompt_sha256": custody.sha256_bytes(system + "\n" + prompt),
                "text": text,
                "text_sha256": custody.sha256_bytes(text),
                "byline": receipt.get("byline"),
                "human_anchor": verification.get("human_anchor"),
                "gguf_ok": verification.get("gguf_ok"),
            })

    out = "".join(rebuild_section(section, rendered) for section in sections)

    if write:
        dest = Path(repo_root) / "generations" / "essay.minted.md"
        dest.write_text(out)
    return out, records


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    if "--plan" in sys.argv:
        plan = build_plan(root)
        dest = Path(root) / "generations" / "mint-plan.json"
        dest.write_text(json.dumps(plan, indent=2) + "\n")
        print("wrote %d STEERED prompts -> generations/mint-plan.json" % len(plan), file=sys.stderr)
    else:
        out, steered = mint(root)
        print("minted essay (%d STEERED sentences) -> generations/essay.minted.md" % steered, file=sys.stderr)
