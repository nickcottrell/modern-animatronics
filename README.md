# Modern Animatronics

An essay about coordinating independently operating parts. It starts with a Halloween pirate attraction on a front porch in Ladera Ranch and traces the same question back through Audio-Animatronics, Shannon, Wiener, Mandelbrot, and a cooler full of melting ice.

The bird has its own sound system. It knows nothing about the fog machine. The fog machine knows nothing about the soundtrack. A dad stands between them, maintaining a reasonably current understanding of a pirate attraction. That is the essay.

## Status

Draft. Private until release.

## What's here

- `drafts/modern-animatronics.md` — the essay, consolidated from working fragments.

## The harness

The essay is about coordinating independent parts. It is minted by a harness
that does exactly that, through a provenance gate, deterministically. The rig
proves the thesis by existing.

### How it works

The **sentence** is the unit. Every sentence is one of two tiers:

- **KEY** — locked. Used verbatim. The jokes, quotes, and thesis lines never move.
- **STEERED** — rebuilt from coordinates alone (never its own text), then judged
  against the locked line. Accept the render, or promote it back to KEY.

Each STEERED sentence carries three coordinate layers:

- **L0 ground** — the one fact it must carry.
- **L1 VRGB** — the three axes the essay itself names: concrete/abstract,
  individual/collective, past/future.
- **L2 calibration** — speculation / tone / density knobs.

A doc-level voice card supplies the stance. The compression ratio per section
(prose bytes over coordinate bytes) is the readout: how much meaning lives in
structure versus phrasing. That ratio is the *coherence over time* the essay
describes — the instrument measures the thing it is about.

### Determinism and the moat

Minting goes through `model_host.run` (the same entry point as the Jeff
`engine_run` MCP tool), decode pinned to temperature 0, seed 0. Same
coordinates in, same sentence out, every time. The model —
`engine/qwen2.5-14b-touchstone` — is only runnable while the `sd:touchstone` SD
card is physically seated. Pull the card and the mint returns a provenance
reject. The essay can only be built with the key in the slot.

### Layout

- `source/essay.locked.md` — the locked baseline; concatenating it is the floor.
- `coords/` — `_doc.json` index, `_voice.json` stance card, one `NN.json` per section.
- `harness/encode.py` — split the locked essay into the coords skeleton (all KEY).
- `harness/prompt.py` — build the deterministic prompt for one STEERED sentence.
- `harness/jeff_bridge.py` — mint one sentence through the provenance gate.
- `harness/mint.py` — reconstruct the essay from coords into `generations/`.
- `harness/verify.py` — floor check (all-KEY mint is byte-identical) + the readout.
- `harness/pins.json` — model ref, decode regime, and the determinism receipt.

### Run

    python -m harness.encode    # locked essay -> coords/ skeleton (all KEY)
    python -m harness.verify    # prove the floor, read the instrument
    python -m harness.mint      # coords/ -> generations/essay.minted.md

Held on purpose while the prose settles. The rig goes around it.
