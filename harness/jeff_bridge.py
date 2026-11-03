"""
jeff_bridge -- mint one sentence through the provenance gate.

The mint does NOT talk to ollama directly. It calls maestro's model_host.run,
the same entry point the jeff MCP engine_run tool uses, with the decode regime
pinned from pins.json. model_host.run re-checks the full gate on every call --
the sd:touchstone card must be seated, the provenance chain must terminate at a
human-signed token, the signature must verify, and the weight hash must match.
A missing card returns a PROVENANCE REJECT and no text is produced.

That is the point of the whole essay: it can only be minted while the physical
card is in the slot. The moat is real and it rides this call.

model_host lives in the maestro repo, resolved from pins.maestro_root (default
~/maestro) so this repo stays self-contained. The import is lazy, so the pure
core (encode, prompt, verify) runs with no maestro checkout present.
"""

import json
import os
import sys
from pathlib import Path


class MintError(RuntimeError):
    pass


def _maestro_root(pins):
    root = os.environ.get("MAESTRO_ROOT") or pins.get("maestro_root") or "~/maestro"
    return Path(root).expanduser()


def _load_model_host(pins):
    root = _maestro_root(pins)
    lib = root / "cue-mem" / "lib"
    if not lib.exists():
        raise MintError("maestro model_host not found at %s (set MAESTRO_ROOT)" % lib)
    # CUE_MEM_HOME pins the token store to maestro's .claude; without it storage
    # walks up from cwd and reads an empty store, so the model-link token (and
    # thus the whole provenance chain) is invisible. Same pin the MCP path uses.
    os.environ["CUE_MEM_HOME"] = str(root)
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        import model_host  # noqa: E402  (resolved at runtime from maestro)
    except Exception as exc:
        raise MintError("could not import model_host: %s" % exc)
    # Pick up freshly-mounted cards, exactly as engine_list does before a run.
    try:
        model_host.sync_mounted_cards()
    except Exception:
        pass
    return model_host


def load_pins(repo_root):
    return json.loads((Path(repo_root) / "harness" / "pins.json").read_text())


def mint_one(pins, system, prompt, max_tokens=128):
    """Return the model's text for one sentence, or raise MintError.

    Honors the pinned decode regime. Raises on PROVENANCE REJECT so a missing
    card fails the mint loudly rather than silently degrading.
    """
    model_host = _load_model_host(pins)
    decode = pins.get("decode", {})
    receipt = model_host.run(
        pins["model_ref"],
        prompt,
        system=system,
        max_tokens=max_tokens,
        temperature=decode.get("temperature", 0.0),
        seed=decode.get("seed", 0),
    )
    if not receipt.get("ok"):
        raise MintError(receipt.get("reason", "model not runnable"))
    text = receipt.get("text")
    if not text:
        raise MintError("empty generation: %s" % receipt.get("reason", "?"))
    return text.strip(), receipt
