# Modern Animatronics

An essay about coordinating independently operating parts. It starts with a Halloween pirate attraction on a front porch in Ladera Ranch and traces the same question back through Audio-Animatronics, Shannon, Wiener, Mandelbrot, and a cooler full of melting ice.

The bird has its own sound system. It knows nothing about the fog machine. The fog machine knows nothing about the soundtrack. A dad stands between them, maintaining a reasonably current understanding of a pirate attraction. That is the essay.

This repository is the other half of the essay: the machine that printed it. The essay argues that coherent output can come from independent parts held together by a human in the loop. The essay was produced that way, on purpose, through a provenance gate, with every editorial decision left in public commit history. The rig proves the thesis by existing. What follows is how to run it yourself.

## How the harness works

The **sentence** is the unit. Every sentence is one of two tiers:

- **KEY**: locked. Used verbatim. The jokes, quotes, and thesis lines never move.
- **STEERED**: rebuilt from coordinates alone, never from its own text, then judged against the locked line. You accept the render or promote it back to KEY.

Each STEERED sentence carries three coordinate layers:

- **L0 ground**: the one fact it must carry.
- **L1 VRGB**: the three axes the essay itself names, concrete/abstract, individual/collective, past/future.
- **L2 calibration**: speculation, tone, and density knobs.

A doc-level voice card supplies the stance. The compression ratio per section, prose bytes over coordinate bytes, is the readout: how much meaning lives in structure versus phrasing. That ratio is the *coherence over time* the essay describes. The instrument measures the thing it is about.

## Determinism and the moat

Minting goes through `model_host.run`, the same entry point as the Jeff `engine_run` MCP tool, with decode pinned. At temperature 0 the decode is greedy: same coordinates in, same sentence out, byte for byte, every time. The model is only runnable while its `sd:touchstone` SD card is physically seated. Pull the card and the mint returns a provenance reject. The essay can only be built with the key in the slot.

## Reproduce your own draft

You supply the locked prose. The harness renders only what you open to it, records exactly what it did, and lets you keep or discard each render.

**1. Encode.** Split your locked essay into the coordinate skeleton. Every sentence starts KEY.

    python -m harness.encode

**2. Tier a sentence.** In `coords/NN.json`, set a sentence `tier` to `STEERED`, give it a one-line `ground` fact, and set any `vrgb` / `calibration` values. That is the only thing the model will be told. It never sees your original words.

**3. Mint candidates.** Each versioned mint produces `mints/NN/` with the draft and a signed receipt, chained to the one before it.

    python -m harness.draft --model engine/qwen2.5-14b-touchstone

Greedy mints are deterministic, so three greedy runs are identical. To get a *pool* of candidates that are each still reproducible, lift the temperature and vary the seed. Every `(temperature, seed)` pair is recorded in the receipt and regenerates byte for byte:

    python -m harness.draft --model engine/qwen2.5-14b-touchstone --temp 0.7 --seed 1
    python -m harness.draft --model engine/qwen2.5-14b-touchstone --temp 0.7 --seed 2

**4. Judge.** Read the candidates. Pick the winner, or keep your locked original.

**5. Promote.** Write the winning render into `source/essay.locked.md` and re-encode. The sentence is KEY again, locked to the words you chose.

    python -m harness.encode && python -m harness.verify

**6. Polish in public.** Make each improvement its own commit, so the before and after are addressable by commit hash. The "notes on final edits" the essay promises are the git log.

**7. Anchor.** Sign the endpoints. The commit DAG shows the path between them.

    python -m harness.anchor --baseline <first-commit> --final HEAD

**8. Verify.** Any of these can be run by anyone, from the repo alone.

    python -m harness.verify --chain      # every mint receipt re-checks and chains
    python -m harness.anchor --verify     # both signed endpoints still hold
    python -m harness.bundle --verify FILE # a sealed single-file draft is not forged

## What the two models showed

The same locked fact, *the cooler holds ice, and the ice chills the fog before it reaches the treasure chest*, was minted three times each through a smart model (`qwen2.5-14b`) and a dumb one (`llama3.2-3b`), at temperature 0.7 with seeds 1, 2, 3. Full reviews are in `notes/candidate-reviews.md`. The short version:

- The **smart** model varied the *wording* and held the *fact*. Every take kept cooler, ice, fog, and chest in the right causal order. Its worst failure was subtle: one fluent sentence that cooled the fog *generator* instead of the fog, a false claim wearing good prose.
- The **dumb** model varied the *subject* and held the *register*. Two of three takes abandoned the fact entirely and confabulated a different prop (an LED array, a skeleton), and every take fabricated a measured specific (`2.5 liters per minute`, `3.75 psi`, `80% brightness`) that nothing supplied. The dry, operational voice stayed intact the whole time.

That is the finding, and it is the essay's thesis in miniature. For the capable part, **meaning is stable while the surface moves**. For the weak part, **the surface is stable while the meaning drifts off**. Style alone would wave the dumb drafts through; grounding has to be checked separately from voice, which is exactly the job of the human in the loop.

## Provenance: how you know a draft is real

Three independent layers, strongest last:

- **Chained receipts.** Each mint hashes its dataset, its model, its decode regime, and its output, signs the lot with an Ed25519 keeper key, and points at the previous receipt. Change one byte and a hash stops matching.
- **A sealed bundle.** `harness/bundle.py` folds a draft, its receipt, the full coordinate dataset, and the keeper public key into one self-verifying file, gated at seal time by a keepalive dead-man's switch so it can only be packaged while the owner is present. It verifies against itself.
- **Signed anchors plus the commit DAG.** The baseline and final essay are each signed; the public commit history is the path between them. The edits are not described after the fact, they *are* the record.

## Layout

- `source/essay.locked.md`: the locked baseline. Concatenating it is the floor.
- `coords/`: `_doc.json` index, `_voice.json` stance card, one `NN.json` per section.
- `harness/encode.py`: split the locked essay into the coords skeleton (all KEY).
- `harness/prompt.py`: build the deterministic prompt for one STEERED sentence.
- `harness/jeff_bridge.py`: mint one sentence through the provenance gate.
- `harness/mint.py`: reconstruct the essay from coords.
- `harness/draft.py`: a versioned, signed, chained mint (with `--model` / `--temp` / `--seed`).
- `harness/custody.py`: hash, sign, chain, and verify receipts.
- `harness/bundle.py`: seal or verify a single self-contained draft file.
- `harness/anchor.py`: sign and verify the baseline and final essay.
- `harness/verify.py`: floor check (all-KEY mint is byte-identical) plus the readout.
- `harness/pins.json`: model ref, decode regime, determinism receipt, signed anchors.
- `mints/`: every versioned draft and its receipt, with `CHAIN.jsonl`.
- `notes/`: the editorial record, including the candidate reviews.

Held on purpose while the prose settles. The rig goes around it.
