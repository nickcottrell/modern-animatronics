"""
bundle -- fold a minted draft and its whole chain of custody into ONE file that
proves it is not forged, gated by the keepalive dead-man's switch.

A mint (mints/NN/) is already signed and tamper-evident, but it is scattered
across files and it trusts whatever keeper key happens to be on the host that
reads it. A bundle collapses the lot into a single self-contained artifact:

  - the draft text itself (readable, in the clear)
  - the mint's signed receipt + its chain line, verbatim
  - the entire coords dataset, byte-for-byte (base64), so dataset_root is
    re-derivable from inside the file with nothing external
  - the keeper PUBLIC key (PEM), so the file verifies against itself -- the only
    thing a reader must supply is trust in the keeper fingerprint
  - a keepalive attestation: the bundle will ONLY seal while the owner's
    dead-man's switch is live, and the switch's validity + deadline are bound
    UNDER the outer signature. Fail-closed: switch invalid -> no seal.

Then the whole body is sealed with the keeper's Ed25519 key. Two signatures end
up inside one file: the inner mint seal (when the draft was made) and the outer
bundle seal (when the owner, present, packaged it). Neither can be altered
without the private key, and the draft/dataset cannot be swapped without a hash
breaking.

  python -m harness.bundle              # seal mint 01 -> <sha>.macp.json (+ desktop)
  python -m harness.bundle --dir NN-... # seal a specific mint dir
  python -m harness.bundle --verify FILE # re-derive everything, check both seals
"""

import base64
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import custody
from . import jeff_bridge

SCHEMA = "modern-animatronics/bundle/1"


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# keepalive -- the extra auth guard. Live, authoritative, fail-closed.
# ---------------------------------------------------------------------------

def _keepalive_state(repo_root, pins):
    """(valid, detail) from maestro's core/keepalive.py -- the same dead-man's
    switch every core gate uses. Authoritative (PIN slot / subdomain), not the
    cached mirror flag. Any doubt resolves to invalid."""
    import importlib.util
    root = _maestro_root(pins)
    path = root / "core" / "keepalive.py"
    spec = importlib.util.spec_from_file_location("maestro_keepalive", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.keepalive_state()


def _maestro_root(pins):
    import os
    root = os.environ.get("MAESTRO_ROOT") or (pins or {}).get("maestro_root") or "~/maestro"
    return Path(root).expanduser()


# ---------------------------------------------------------------------------
# keeper public key -- embedded so the file verifies against itself
# ---------------------------------------------------------------------------

def _keeper_pubkey_pem(repo_root, pins):
    """The keeper PUBLIC key as PEM text + its fingerprint, read straight off
    disk so the bundle can carry it. Public only -- no secret leaves here."""
    root = _maestro_root(pins)
    pub = root / ".claude" / "keys" / "human.pub"
    pem = pub.read_text()
    fp = _fingerprint_from_pem(pem)
    return pem, fp


def _fingerprint_from_pem(pem_text):
    """Re-derive the keeper fingerprint from a PEM the same way signing.py does:
    sha256 over the raw public-key bytes, first 16 hex. Lets a verifier confirm
    the embedded key IS the keeper's, from the file alone."""
    import hashlib
    from cryptography.hazmat.primitives import serialization
    pub = serialization.load_pem_public_key(pem_text.encode("utf-8"))
    raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return hashlib.sha256(raw).hexdigest()[:16]


def _verify_with_pem(pem_text, data, signature_b64):
    """Verify an Ed25519 signature using ONLY the embedded PEM -- self-contained,
    does not touch the host keystore."""
    from cryptography.hazmat.primitives import serialization
    if isinstance(data, str):
        data = data.encode("utf-8")
    pub = serialization.load_pem_public_key(pem_text.encode("utf-8"))
    try:
        pub.verify(base64.b64decode(signature_b64), data)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# seal
# ---------------------------------------------------------------------------

def seal(repo_root, mint_dir=None, now=None):
    repo_root = Path(repo_root)
    pins = jeff_bridge.load_pins(repo_root)
    now = now or utc_now()

    # 1. the auth guard, first and fail-closed.
    valid, ka = _keepalive_state(repo_root, pins)
    if not valid:
        raise SystemExit(
            "keepalive is NOT live (%s) -- refusing to seal. The bundle guard "
            "requires the owner present. Arm the PIN in the TUI and retry." % ka
        )

    # 2. resolve the mint.
    chain = custody.load_chain(repo_root)
    if not chain:
        raise SystemExit("no mints to bundle -- run harness.draft first")
    link = chain[-1] if mint_dir is None else next(
        (l for l in chain if l["dir"] == mint_dir), None)
    if link is None:
        raise SystemExit("no chain link for mint dir %r" % mint_dir)
    mdir = repo_root / "mints" / link["dir"]
    receipt = json.loads((mdir / "receipt.json").read_text())
    draft_text = (mdir / "draft.md").read_text()

    # 3. the inner receipt must verify before we wrap it.
    ok, problems = custody.verify_receipt(receipt, repo_root, pins)
    if not ok:
        raise SystemExit("inner receipt does not verify: %s" % "; ".join(problems))
    if custody.sha256_bytes(draft_text) != receipt["body"]["output"]["sha256"]:
        raise SystemExit("draft.md does not match its receipt output sha")

    # 4. the dataset, byte-for-byte, so dataset_root is re-derivable in-file.
    coords = repo_root / "coords"
    coords_b64 = {}
    for p in sorted(coords.glob("*.json")):
        coords_b64["coords/%s" % p.name] = base64.b64encode(p.read_bytes()).decode("ascii")
    dataset_root = _dataset_root_from_b64(coords_b64)
    if dataset_root != receipt["body"]["dataset"]["dataset_root"]:
        raise SystemExit("coords on disk no longer match the mint's dataset_root")

    pem, fp = _keeper_pubkey_pem(repo_root, pins)

    body = {
        "schema": SCHEMA,
        "sealed_at": now,
        "draft": {
            "text": draft_text,
            "sha256": custody.sha256_bytes(draft_text),
            "bytes": len(draft_text.encode("utf-8")),
        },
        "mint": {
            "dir": link["dir"],
            "receipt": receipt,
            "chain_link": link,
        },
        "dataset": {
            "dataset_root": dataset_root,
            "source": receipt["body"]["dataset"]["source"],
            "coords_b64": coords_b64,
        },
        "keepalive": {
            "required": True,
            "state": "valid",
            "mode": ka.get("mode"),
            "until": ka.get("until"),
            "checked_at": now,
            "source": "maestro core/keepalive.py keepalive_state()",
        },
        "keeper": {
            "algo": "ed25519",
            "fingerprint": fp,
            "public_key_pem": pem,
        },
    }

    signing = custody._load_signing(repo_root, pins)
    if not signing.has_keypair():
        raise SystemExit("no keeper key on this host -- cannot seal the bundle")
    signature = signing.sign_bytes(custody.canonical(body))

    envelope = {
        "body": body,
        "body_sha256": custody.sha256_obj(body),
        "signer": fp,
        "signature": signature,
    }
    envelope["bundle_sha256"] = custody.sha256_obj(
        {k: v for k, v in envelope.items() if k != "bundle_sha256"})
    return envelope


def _dataset_root_from_b64(coords_b64):
    """Re-derive dataset_root from the embedded coords: sha256 each file's raw
    bytes, then sha256 over the sorted {path: sha} map -- identical to
    custody.dataset_manifest, but sourced from inside the bundle."""
    files = {rel: custody.sha256_bytes(base64.b64decode(b64))
             for rel, b64 in coords_b64.items()}
    return custody.sha256_obj(files)


# ---------------------------------------------------------------------------
# verify -- entirely from the file; the only external input is trust in the fp
# ---------------------------------------------------------------------------

def verify(path):
    env = json.loads(Path(path).read_text())
    body = env["body"]
    problems = []

    # self-consistency of the outer envelope
    if custody.sha256_obj(body) != env.get("body_sha256"):
        problems.append("body_sha256 does not match the body")
    unsealed = {k: v for k, v in env.items() if k != "bundle_sha256"}
    if custody.sha256_obj(unsealed) != env.get("bundle_sha256"):
        problems.append("bundle_sha256 does not match the envelope")

    # the embedded key really is the keeper's, and it signed this bundle
    pem = body["keeper"]["public_key_pem"]
    derived_fp = _fingerprint_from_pem(pem)
    if derived_fp != body["keeper"]["fingerprint"]:
        problems.append("embedded pubkey fingerprint != claimed keeper fingerprint")
    if derived_fp != env.get("signer"):
        problems.append("signer != embedded keeper fingerprint")
    if not _verify_with_pem(pem, custody.canonical(body), env.get("signature")):
        problems.append("OUTER bundle signature does not verify against embedded keeper key")

    # the draft bytes are the ones that were sealed
    if custody.sha256_bytes(body["draft"]["text"]) != body["draft"]["sha256"]:
        problems.append("draft text does not match its sha256")

    # the dataset re-derives, and agrees with the inner receipt
    recomputed_root = _dataset_root_from_b64(body["dataset"]["coords_b64"])
    if recomputed_root != body["dataset"]["dataset_root"]:
        problems.append("coords do not re-derive the bundle dataset_root")

    receipt = body["mint"]["receipt"]
    rbody = receipt["body"]
    if recomputed_root != rbody["dataset"]["dataset_root"]:
        problems.append("dataset_root disagrees with the inner mint receipt")
    if body["draft"]["sha256"] != rbody["output"]["sha256"]:
        problems.append("draft sha != inner mint receipt output sha")

    # the inner mint seal, verified from the same embedded key
    if custody.sha256_obj(rbody) != receipt.get("body_sha256"):
        problems.append("inner receipt body_sha256 broken")
    inner_unsealed = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    if custody.sha256_obj(inner_unsealed) != receipt.get("receipt_sha256"):
        problems.append("inner receipt_sha256 broken")
    if not _verify_with_pem(pem, custody.canonical(rbody), receipt.get("signature")):
        problems.append("INNER mint signature does not verify against embedded keeper key")

    # the keepalive guard was satisfied at seal time (bound under the signature)
    ka = body.get("keepalive", {})
    if not (ka.get("required") and ka.get("state") == "valid"):
        problems.append("keepalive guard was not satisfied at seal time")

    return (not problems), problems, body


def _report(path, ok, problems, body):
    out = sys.stderr
    print("bundle: %s" % path, file=out)
    if ok:
        ka = body["keepalive"]
        print("  VERIFIED -- not forged.", file=out)
        print("  keeper        %s (embedded pubkey, self-checked)" % body["keeper"]["fingerprint"], file=out)
        print("  outer seal    OK   (owner present + packaged)", file=out)
        print("  inner seal    OK   (mint %s)" % body["mint"]["dir"], file=out)
        print("  draft         %s  (%d bytes)" % (body["draft"]["sha256"][:16], body["draft"]["bytes"]), file=out)
        print("  dataset_root  %s  (re-derived in-file)" % body["dataset"]["dataset_root"][:16], file=out)
        print("  model         %s" % body["mint"]["receipt"]["body"]["model"]["model_ref"], file=out)
        print("  keepalive     live at seal %s, valid until %s" % (ka["checked_at"], ka["until"]), file=out)
        print("  sealed_at     %s" % body["sealed_at"], file=out)
    else:
        print("  FORGED or CORRUPT -- do not trust:", file=out)
        for p in problems:
            print("    - %s" % p, file=out)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    if "--verify" in sys.argv:
        target = sys.argv[sys.argv.index("--verify") + 1]
        ok, problems, body = verify(target)
        _report(target, ok, problems, body)
        sys.exit(0 if ok else 1)

    mint_dir = None
    if "--dir" in sys.argv:
        mint_dir = sys.argv[sys.argv.index("--dir") + 1]
    envelope = seal(root, mint_dir=mint_dir)

    short = envelope["bundle_sha256"][:12]
    name = "modern-animatronics-%s.macp.json" % short
    out_repo = root / "mints" / name
    out_repo.write_text(custody.json_pretty(envelope))

    desktop = Path.home() / "Desktop" / name
    try:
        desktop.write_text(custody.json_pretty(envelope))
        desk_note = " + ~/Desktop/%s" % name
    except OSError:
        desk_note = ""

    print("sealed bundle -> mints/%s%s" % (name, desk_note), file=sys.stderr)
    print("  bundle_sha256 %s" % envelope["bundle_sha256"], file=sys.stderr)
    print("  signer        %s" % envelope["signer"], file=sys.stderr)
    print("  verify: python3 -m harness.bundle --verify mints/%s" % name, file=sys.stderr)
