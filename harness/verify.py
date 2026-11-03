"""
verify -- prove the mint is honest, and read the instrument.

Two jobs:

1. Floor check (no model needed). Rebuild the essay treating every STEERED
   sentence as its verbatim slice -- i.e. an all-KEY reconstruction -- and
   byte-compare against source/essay.locked.md. If this fails, encode lost
   information and nothing downstream can be trusted.

2. Readout. For each section, the compression ratio is the bytes of settled
   prose over the bytes of coordinate it was reconstructed from (ground + axes
   + knobs for every STEERED sentence). High ratio means the meaning lives in
   structure; low ratio means it lives in the phrasing. That ratio IS the
   "coherence over time" reading the essay is about -- the instrument measuring
   the thing it describes.

Run:  python -m harness.verify
"""

import hashlib
import sys
from pathlib import Path

from . import record
from . import prompt as prompt_mod


def reconstruct_verbatim(sections):
    """All-KEY reconstruction: every sentence as its slice. Should equal source."""
    return "".join(section["raw"] for section in sections)


def coordinate_bytes(sent, voice):
    """Bytes of coordinate a STEERED sentence is rebuilt from."""
    system, prompt = prompt_mod.build_prompt(sent, voice)
    return len(system.encode()) + len(prompt.encode())


def floor_check(repo_root):
    repo_root = Path(repo_root)
    index, sections = record.load_doc(repo_root)
    rebuilt = reconstruct_verbatim(sections)
    source = (repo_root / "source" / "essay.locked.md").read_text()

    rebuilt_sha = hashlib.sha256(rebuilt.encode()).hexdigest()
    source_sha = hashlib.sha256(source.encode()).hexdigest()
    return {
        "ok": rebuilt_sha == source_sha == index["sha256"],
        "rebuilt_sha": rebuilt_sha,
        "source_sha": source_sha,
        "index_sha": index["sha256"],
    }


def readout(repo_root):
    _index, sections = record.load_doc(repo_root)
    voice = record.load_voice(repo_root)
    rows = []
    for section in sections:
        prose = 0
        coord = 0
        steered = 0
        for sent in section["sentences"]:
            if sent["tier"] == record.STEERED:
                steered += 1
                prose += len(sent["text"].encode())
                coord += coordinate_bytes(sent, voice)
        ratio = (prose / coord) if coord else None
        rows.append({
            "section": section["index"],
            "steered": steered,
            "prose_bytes": prose,
            "coord_bytes": coord,
            "ratio": ratio,
        })
    return rows


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent

    if "--chain" in sys.argv:
        from . import custody
        from . import jeff_bridge
        pins = jeff_bridge.load_pins(root)
        ok, report = custody.walk_chain(root, pins)
        for line in report:
            print(line)
        if not ok:
            sys.exit(1)
        sys.exit(0)

    floor = floor_check(root)
    if floor["ok"]:
        print("floor OK -- all-KEY reconstruction is byte-identical to the locked essay")
        print("  sha256 %s" % floor["source_sha"])
    else:
        print("floor FAIL -- reconstruction drifted from the locked essay", file=sys.stderr)
        print("  rebuilt %s" % floor["rebuilt_sha"], file=sys.stderr)
        print("  source  %s" % floor["source_sha"], file=sys.stderr)
        sys.exit(1)

    rows = readout(root)
    steered_total = sum(r["steered"] for r in rows)
    if steered_total == 0:
        print("readout -- 0 STEERED sentences yet; the essay is fully locked (all KEY).")
    else:
        print("readout -- compression ratio per section (prose bytes / coord bytes):")
        for r in rows:
            if r["steered"]:
                print("  section %02d  %2d steered  %.2fx" % (r["section"], r["steered"], r["ratio"]))
