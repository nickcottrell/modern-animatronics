"""
verify -- two honest checks, no crypto.

1. floor: rebuild the essay with every STEERED sentence as its locked slice
   (all-KEY) and byte-compare to source/essay.locked.md. If this fails, the
   coordinate split lost information and nothing downstream can be trusted.

2. --rerun: generate the STEERED sentences again and show how close the new
   output is to the recorded run in generations/provenance.json. The claim is
   closeness, not identity. A genuine re-run lands in the same voice; that is
   the proof the generation is real and not pasted in.

Run:
  python -m harness.verify
  python -m harness.verify --rerun
"""

import difflib
import hashlib
import json
import sys
from pathlib import Path

from . import record


def floor_check(repo_root):
    repo_root = Path(repo_root)
    index, sections = record.load_doc(repo_root)
    rebuilt = "".join(s["raw"] for s in sections)
    source = (repo_root / "source" / "essay.locked.md").read_text()
    sha = hashlib.sha256(source.encode()).hexdigest()
    ok = hashlib.sha256(rebuilt.encode()).hexdigest() == sha == index["sha256"]
    return ok, sha


def rerun(repo_root):
    """Re-generate and compare to the recorded provenance, sentence by sentence."""
    from . import mint as mint_mod
    from . import jeff_bridge
    repo_root = Path(repo_root)
    prov_path = repo_root / "generations" / "provenance.json"
    if not prov_path.exists():
        print("no generations/provenance.json yet; run harness.mint first")
        return
    recorded = json.loads(prov_path.read_text())
    pins = {**jeff_bridge.load_pins(repo_root),
            "model_ref": recorded["model"], "decode": recorded["decode"]}
    _draft, fresh = mint_mod.mint(repo_root, pins=pins, write=False)
    print("rerun closeness (recorded vs fresh, same model %s + decode):" % recorded["model"])
    for r, f in zip(recorded["generated"], fresh["generated"]):
        ratio = difflib.SequenceMatcher(None, r["output"], f["output"]).ratio()
        verdict = "identical" if r["output"] == f["output"] else "%.0f%% similar" % (ratio * 100)
        print("  s%d.%d  %s" % (r["section"], r["sentence"], verdict))
        if r["output"] != f["output"]:
            print("    recorded: %s" % r["output"])
            print("    fresh:    %s" % f["output"])


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    ok, sha = floor_check(root)
    if ok:
        print("floor OK -- all-KEY rebuild is byte-identical to the locked essay")
        print("  sha256 %s" % sha)
    else:
        print("floor FAIL -- reconstruction drifted from the locked essay", file=sys.stderr)
        sys.exit(1)
    if "--rerun" in sys.argv:
        rerun(root)
