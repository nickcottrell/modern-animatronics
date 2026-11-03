"""
custody -- chain of custody for a minted draft.

A mint binds four things: a dataset (the locked values the model was given), a
model (which weights, gated how), a time, and the draft that came out. This
module turns that binding into a receipt, chains each receipt to the one before
it, and signs the chain with the keeper's Ed25519 key.

Two independent tamper layers come out of that:

  tamper-evident  -- every receipt carries sha256 of its inputs, of the draft,
                     and of the previous receipt. Change one byte anywhere and a
                     recomputed hash stops matching. Anyone can detect it; no key
                     required. git's own commit DAG is a second evidence layer.
  tamper-proof    -- the receipt is signed with the human private key. A forged
                     receipt for altered content cannot be produced without that
                     key. As close to proof as crypto reaches.

The dataset is the coords/ tree: the KEY verbatim, each STEERED sentence's
ground fact and axes, and the voice card. We hash every coord file and fold them
into one dataset_root. That root IS "the particular dataset" in the receipt.

Signing is borrowed from maestro's keeper (cue-mem/lib/signing.py), resolved the
same lazy way jeff_bridge resolves model_host, so this repo stays self-contained
and the pure core still runs with no maestro checkout present.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

SCHEMA = "modern-animatronics/custody/1"


def canonical(obj):
    """Deterministic JSON bytes: sorted keys, no incidental whitespace."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def sha256_obj(obj):
    return sha256_bytes(canonical(obj))


def json_pretty(obj):
    """Readable JSON for on-disk receipts. Signatures cover canonical(), not this."""
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


# ---------------------------------------------------------------------------
# dataset -- the locked values the model was handed
# ---------------------------------------------------------------------------

def dataset_manifest(repo_root):
    """Hash every coord input and fold them into one dataset_root.

    files   -- {relative path: sha256} for _doc.json, _voice.json, every NN.json
    source  -- the locked essay sha the coords index already commits to
    dataset_root -- sha256 over the sorted (path, sha) pairs; the single fingerprint
    """
    repo_root = Path(repo_root)
    coords = repo_root / "coords"
    files = {}
    for path in sorted(coords.glob("*.json")):
        rel = "coords/%s" % path.name
        files[rel] = sha256_bytes(path.read_bytes())

    index = json.loads((coords / "_doc.json").read_text())
    return {
        "files": files,
        "source": {"path": index["source"], "sha256": index["sha256"]},
        "dataset_root": sha256_obj(files),
    }


# ---------------------------------------------------------------------------
# receipt -- the signed binding of dataset + model + time -> draft
# ---------------------------------------------------------------------------

def build_receipt(dataset, model, output, per_sentence, minted_at, prev_sha):
    """The unsigned receipt body. Everything that gets signed lives in here."""
    return {
        "schema": SCHEMA,
        "minted_at": minted_at,
        "prev": prev_sha,
        "dataset": dataset,
        "model": model,
        "output": output,
        "per_sentence": per_sentence,
    }


def _load_signing(repo_root, pins):
    # Load the keeper signing module by PATH under a unique name. A bare
    # `import signing` is unsafe here: other maestro modules (leases, cuesync)
    # register their own `signing` in sys.modules and we would get whichever
    # loaded first -- a module with no verify_bytes. Resolve the exact file.
    import importlib.util
    root = os.environ.get("MAESTRO_ROOT") or (pins or {}).get("maestro_root") or "~/maestro"
    path = Path(root).expanduser() / "cue-mem" / "lib" / "signing.py"
    mod = sys.modules.get("maestro_keeper_signing")
    if mod is None:
        spec = importlib.util.spec_from_file_location("maestro_keeper_signing", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sys.modules["maestro_keeper_signing"] = mod
    return mod


def sign_receipt(body, repo_root, pins=None):
    """Wrap a receipt body in a signed envelope.

    The signature covers the canonical body. receipt_sha is the fingerprint of the
    whole signed envelope -- that is the value the NEXT receipt points at via prev.
    If no key is on this host the envelope is still written, unsigned, so the chain
    stays intact and honest about what it is (evident, not proof).
    """
    signing = _load_signing(repo_root, pins)
    body_sha = sha256_obj(body)
    signature = None
    signer = None
    if signing.has_keypair():
        signature = signing.sign_bytes(canonical(body))
        signer = signing.get_public_key_fingerprint()

    envelope = {
        "body": body,
        "body_sha256": body_sha,
        "signer": signer,
        "signature": signature,
    }
    envelope["receipt_sha256"] = sha256_obj(envelope_unsealed(envelope))
    return envelope


def envelope_unsealed(envelope):
    """The envelope minus its own self-referential receipt_sha256, for hashing."""
    return {k: v for k, v in envelope.items() if k != "receipt_sha256"}


def verify_receipt(envelope, repo_root, pins=None):
    """Re-derive every hash and check the signature. Returns (ok, [problems])."""
    problems = []

    if sha256_obj(envelope["body"]) != envelope.get("body_sha256"):
        problems.append("body_sha256 does not match the body")

    if sha256_obj(envelope_unsealed(envelope)) != envelope.get("receipt_sha256"):
        problems.append("receipt_sha256 does not match the envelope")

    sig = envelope.get("signature")
    if sig:
        signing = _load_signing(repo_root, pins)
        if not signing.verify_bytes(canonical(envelope["body"]), sig):
            problems.append("signature does not verify against the keeper public key")
    else:
        problems.append("unsigned (tamper-evident only, not signed)")

    return (not problems, problems)


# ---------------------------------------------------------------------------
# ledger -- the append-only chain of receipts, one line per mint
# ---------------------------------------------------------------------------

def chain_path(repo_root):
    return Path(repo_root) / "mints" / "CHAIN.jsonl"


def load_chain(repo_root):
    path = chain_path(repo_root)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def last_receipt_sha(repo_root):
    chain = load_chain(repo_root)
    return chain[-1]["receipt_sha256"] if chain else None


def next_seq(repo_root):
    return len(load_chain(repo_root)) + 1


def append_to_chain(repo_root, link):
    path = chain_path(repo_root)
    path.parent.mkdir(exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(link, sort_keys=True) + "\n")


def walk_chain(repo_root, pins=None):
    """Re-verify the whole chain end to end. Returns (ok, [report lines])."""
    chain = load_chain(repo_root)
    report = []
    ok = True
    prev_sha = None
    for link in chain:
        seq = link["seq"]
        receipt_path = Path(repo_root) / "mints" / link["dir"] / "receipt.json"
        if not receipt_path.exists():
            report.append("mint %02d: receipt missing on disk" % seq)
            ok = False
            continue
        envelope = json.loads(receipt_path.read_text())

        r_ok, problems = verify_receipt(envelope, repo_root, pins)

        if envelope["body"].get("prev") != prev_sha:
            problems.append("prev pointer broken (chain reordered or spliced)")
            r_ok = False

        if envelope.get("receipt_sha256") != link.get("receipt_sha256"):
            problems.append("ledger receipt_sha256 disagrees with the receipt file")
            r_ok = False

        draft_path = Path(repo_root) / "mints" / link["dir"] / "draft.md"
        if draft_path.exists():
            if sha256_bytes(draft_path.read_bytes()) != envelope["body"]["output"]["sha256"]:
                problems.append("draft.md no longer matches its receipt output sha")
                r_ok = False
        else:
            problems.append("draft.md missing on disk")
            r_ok = False

        tag = "OK" if r_ok else "FAIL"
        note = "" if r_ok else "  -- " + "; ".join(problems)
        signed = "signed" if envelope.get("signature") else "UNSIGNED"
        report.append("mint %02d [%s] %s%s" % (seq, signed, tag, note))
        ok = ok and r_ok
        prev_sha = envelope.get("receipt_sha256")

    if not chain:
        report.append("no mints yet")
    return ok, report
