"""
anchor -- sign the essay's before and after, so the polish pass is provable by
signature, not only by the commit DAG.

The design says: lock a signed baseline anchor first, then edit in public commit
history. This module makes that literal. An anchor binds three things and signs
them with the keeper's Ed25519 key:

  essay_sha256  -- sha of source/essay.locked.md at that point
  commit        -- the git commit where that essay is current
  label         -- "baseline" (pre-polish) or "final" (post-polish)

Two anchors go into harness/pins.json: baseline_anchor and final_anchor. Between
them sits the commit trail. Anyone can then prove, from the repo alone, that the
published essay is the exact one the keeper signed off on, and that the baseline
it departed from was signed too. The git history shows the path; the anchors
sign the endpoints.

  python -m harness.anchor --seal    # sign baseline + final into pins.json
  python -m harness.anchor --verify  # re-check both signatures + the live essay
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import custody
from . import jeff_bridge


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _git(repo_root, *args):
    return subprocess.run(["git", "-C", str(repo_root), *args],
                          capture_output=True, text=True, check=True).stdout.strip()


def essay_sha_at(repo_root, ref):
    """sha256 of source/essay.locked.md as it stood at a commit ref. Hash the RAW
    blob bytes (no strip) so it matches the file's own sha, not a trimmed copy."""
    out = subprocess.run(
        ["git", "-C", str(repo_root), "show", "%s:source/essay.locked.md" % ref],
        capture_output=True, check=True)
    return custody.sha256_bytes(out.stdout)


def build_anchor(label, essay_sha, commit, now):
    return {
        "label": label,
        "essay_sha256": essay_sha,
        "commit": commit,
        "signed_at": now,
    }


def sign_anchor(body, repo_root, pins):
    signing = custody._load_signing(repo_root, pins)
    if not signing.has_keypair():
        raise SystemExit("no keeper key on this host -- cannot sign the anchor")
    return {
        "body": body,
        "signer": signing.get_public_key_fingerprint(),
        "signature": signing.sign_bytes(custody.canonical(body)),
    }


def verify_anchor(envelope, repo_root, pins):
    problems = []
    signing = custody._load_signing(repo_root, pins)
    if not signing.verify_bytes(custody.canonical(envelope["body"]), envelope.get("signature")):
        problems.append("signature does not verify against the keeper key")
    return (not problems), problems


def seal(repo_root, baseline_ref, final_ref):
    repo_root = Path(repo_root)
    pins_path = repo_root / "harness" / "pins.json"
    pins = jeff_bridge.load_pins(repo_root)
    now = utc_now()

    baseline = sign_anchor(build_anchor(
        "baseline", essay_sha_at(repo_root, baseline_ref),
        _git(repo_root, "rev-parse", baseline_ref), now), repo_root, pins)
    final = sign_anchor(build_anchor(
        "final", essay_sha_at(repo_root, final_ref),
        _git(repo_root, "rev-parse", final_ref), now), repo_root, pins)

    pins["baseline_anchor"] = baseline
    pins["final_anchor"] = final
    pins_path.write_text(custody.json_pretty(pins))
    return baseline, final


def verify(repo_root):
    repo_root = Path(repo_root)
    pins = jeff_bridge.load_pins(repo_root)
    report = []
    ok = True
    for key in ("baseline_anchor", "final_anchor"):
        env = pins.get(key)
        if not env:
            report.append("%s: MISSING" % key)
            ok = False
            continue
        a_ok, problems = verify_anchor(env, repo_root, pins)
        b = env["body"]
        # the essay at the anchored commit must still hash to what was signed
        if essay_sha_at(repo_root, b["commit"]) != b["essay_sha256"]:
            problems.append("essay at %s no longer matches the signed sha" % b["commit"][:9])
            a_ok = False
        tag = "OK" if a_ok else "FAIL"
        note = "" if a_ok else "  -- " + "; ".join(problems)
        report.append("%-15s [%s] %s @ %s%s" % (b["label"], tag, b["essay_sha256"][:16], b["commit"][:9], note))
        ok = ok and a_ok
    # the live essay should match the final anchor
    final = pins.get("final_anchor")
    if final:
        live = custody.sha256_bytes((repo_root / "source" / "essay.locked.md").read_text())
        if live == final["body"]["essay_sha256"]:
            report.append("live essay matches the final anchor")
        else:
            report.append("live essay DRIFTED from the final anchor")
            ok = False
    return ok, report


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    if "--verify" in sys.argv:
        ok, report = verify(root)
        for line in report:
            print(line, file=sys.stderr)
        sys.exit(0 if ok else 1)

    baseline_ref = sys.argv[sys.argv.index("--baseline") + 1] if "--baseline" in sys.argv else "HEAD"
    final_ref = sys.argv[sys.argv.index("--final") + 1] if "--final" in sys.argv else "HEAD"
    baseline, final = seal(root, baseline_ref, final_ref)
    print("sealed anchors into harness/pins.json", file=sys.stderr)
    print("  baseline %s @ %s" % (baseline["body"]["essay_sha256"][:16], baseline["body"]["commit"][:9]), file=sys.stderr)
    print("  final    %s @ %s" % (final["body"]["essay_sha256"][:16], final["body"]["commit"][:9]), file=sys.stderr)
    print("  signer   %s" % final["signer"], file=sys.stderr)
