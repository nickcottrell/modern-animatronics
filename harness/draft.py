"""
draft -- mint a versioned, signed draft with a chain-of-custody receipt.

This is the command Nick runs to produce a draft that goes into version history.
It does four things, in order:

  1. mint the essay through the provenance gate (mint_detailed). Every STEERED
     sentence is generated live by the pinned model; the card must be seated or
     the gate rejects and nothing is written.
  2. fingerprint the dataset (the coords tree) and record which model ran, under
     what decode regime, with which human anchor, at what time.
  3. bind all of it into a receipt, chain it to the previous receipt, and sign it
     with the keeper's Ed25519 key.
  4. write mints/<seq>/draft.md + mints/<seq>/receipt.json and append one line to
     mints/CHAIN.jsonl. Committing that directory is the versioned draft.

A second mint repeats the whole thing at the next seq, pointing prev at this
receipt. The chain grows; verify (python -m harness.verify --chain) re-walks it.

Run:  python -m harness.draft            (mint + sign + write a versioned draft)
      python -m harness.draft --commit   (also: git add + commit the new mint)
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import custody
from . import jeff_bridge
from . import mint as mint_mod


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def mint_versioned(repo_root, now=None, commit=False, model_ref=None, decode=None):
    repo_root = Path(repo_root)
    pins = jeff_bridge.load_pins(repo_root)
    if model_ref:
        pins = {**pins, "model_ref": model_ref}   # same locked dataset, different gated brain
    if decode:
        pins = {**pins, "decode": {**pins.get("decode", {}), **decode}}   # per-take seed/temp, recorded in the receipt
    now = now or utc_now()

    out, records = mint_mod.mint_detailed(repo_root, write=False, pins=pins)
    if not records:
        raise SystemExit(
            "no STEERED sentences -- an all-KEY mint never calls the model, so a "
            "custody receipt would name no model. Promote at least one sentence to "
            "STEERED (with a ground fact) before minting a versioned draft."
        )

    dataset = custody.dataset_manifest(repo_root)
    decode = pins.get("decode", {})
    model = {
        "model_ref": pins["model_ref"],
        "card": pins.get("gate", {}).get("card"),
        "decode": {"temperature": decode.get("temperature", 0.0), "seed": decode.get("seed", 0)},
        "human_anchor": records[0].get("human_anchor"),
        "gguf_ok": all(r.get("gguf_ok") for r in records),
    }
    output = {
        "sha256": custody.sha256_bytes(out),
        "bytes": len(out.encode("utf-8")),
        "steered": len(records),
    }

    body = custody.build_receipt(
        dataset=dataset,
        model=model,
        output=output,
        per_sentence=records,
        minted_at=now,
        prev_sha=custody.last_receipt_sha(repo_root),
    )
    envelope = custody.sign_receipt(body, repo_root, pins)

    seq = custody.next_seq(repo_root)
    short = envelope["receipt_sha256"][:12]
    name = "%02d-%s" % (seq, short)
    mint_dir = repo_root / "mints" / name
    mint_dir.mkdir(parents=True, exist_ok=True)
    (mint_dir / "draft.md").write_text(out)
    (mint_dir / "receipt.json").write_text(custody.json_pretty(envelope))

    custody.append_to_chain(repo_root, {
        "seq": seq,
        "dir": name,
        "minted_at": now,
        "prev": body["prev"],
        "receipt_sha256": envelope["receipt_sha256"],
        "draft_sha256": output["sha256"],
        "signed": bool(envelope.get("signature")),
    })

    if commit:
        _git_commit(repo_root, name, seq, envelope)

    return seq, name, envelope


def _git_commit(repo_root, name, seq, envelope):
    rel = "mints/%s" % name
    subprocess.run(["git", "-C", str(repo_root), "add", rel, "mints/CHAIN.jsonl"], check=True)
    signed = "signed" if envelope.get("signature") else "unsigned"
    msg = "mint %02d: versioned draft (%s)\n\nreceipt %s\n\nclaude wuz here" % (
        seq, signed, envelope["receipt_sha256"][:12])
    subprocess.run(["git", "-C", str(repo_root), "commit", "-m", msg], check=True)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    commit = "--commit" in sys.argv
    model_ref = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else None
    decode = {}
    if "--seed" in sys.argv:
        decode["seed"] = int(sys.argv[sys.argv.index("--seed") + 1])
    if "--temp" in sys.argv:
        decode["temperature"] = float(sys.argv[sys.argv.index("--temp") + 1])
    seq, name, envelope = mint_versioned(root, commit=commit, model_ref=model_ref, decode=decode or None)
    signed = "signed" if envelope.get("signature") else "UNSIGNED (no keeper key on host)"
    print("minted versioned draft -> mints/%s/" % name, file=sys.stderr)
    print("  receipt %s [%s]" % (envelope["receipt_sha256"], signed), file=sys.stderr)
    if not commit:
        print("  (not committed -- run with --commit to put it in version history)", file=sys.stderr)
