# Modern Animatronics

An essay about coordinating independently operating parts. It starts with a Halloween pirate attraction on a front porch in Ladera Ranch and traces the same question back through Audio-Animatronics, Shannon, Wiener, Mandelbrot, and a cooler full of melting ice.

The bird has its own sound system. It knows nothing about the fog machine. The fog machine knows nothing about the soundtrack. A dad stands between them, maintaining a reasonably current understanding of a pirate attraction. That is the essay.

This repository is the other half of the essay: the machine that printed it. The essay argues that coherent output can come from independent parts held together by a human in the loop. The essay was produced that way, on purpose, through a provenance gate, with every editorial decision left in public commit history. The rig proves the thesis by existing. What follows is how to run it yourself.

## How the harness works

The **sentence** is the unit. Every sentence is one of two tiers:

- **KEY**: locked. Used verbatim. The jokes, quotes, and thesis lines never move.
- **STEERED**: generated from its coordinates, never from its own text, then judged against the locked line. You accept the render, promote it back to KEY, or keep it STEERED so the published line stays provably generated.

Each STEERED sentence carries three coordinate layers:

- **L0 ground**: the one fact it must carry.
- **L1 VRGB**: the three axes the essay itself names, concrete/abstract, individual/collective, past/future.
- **L2 calibration**: speculation, tone, and density knobs.

A doc-level voice card supplies the stance. The compression ratio per section, prose bytes over coordinate bytes, is the readout: how much meaning lives in structure versus phrasing. That ratio is the *coherence over time* the essay describes. The instrument measures the thing it is about.

A STEERED sentence is generated one of two ways. By default it is built from its coordinates in a vacuum. Opt a sentence into the **wider locked net** (`grounding: section`) and it is instead generated to fill a gap in its own locked paragraph, hearing the surrounding voice while its own words stay hidden. Which mode you pick is itself a declaration of intent; the case for that is below.

## Determinism and the moat

Minting goes through `model_host.run`, the same entry point as the Jeff `engine_run` MCP tool, with decode pinned. At temperature 0 the decode is greedy: same coordinates in, same sentence out, byte for byte, every time. The model is only runnable while its `sd:touchstone` SD card is physically seated. Pull the card and the mint returns a provenance reject. The essay can only be built with the key in the slot.

## Reproduce your own draft

You supply the locked prose. The harness renders only what you open to it, records exactly what it did, and lets you keep or discard each render.

**1. Encode.** Split your locked essay into the coordinate skeleton. Every sentence starts KEY.

    python -m harness.encode

**2. Tier a sentence.** In `coords/NN.json`, set a sentence `tier` to `STEERED`, give it a one-line `ground` fact, and set any `vrgb` / `calibration` values. That is the only thing the model will be told. It never sees your original words. For a line that has to match the surrounding voice, also set `grounding` to `section`: the model then fills a gap in its own locked paragraph instead of generating from the fact in a vacuum.

**3. Mint candidates.** Each versioned mint produces `mints/NN/` with the draft and a signed receipt, chained to the one before it.

    python -m harness.draft --model engine/qwen2.5-14b-touchstone

Greedy mints are deterministic, so three greedy runs are identical. To get a *pool* of candidates that are each still reproducible, lift the temperature and vary the seed. Every `(temperature, seed)` pair is recorded in the receipt and regenerates byte for byte:

    python -m harness.draft --model engine/qwen2.5-14b-touchstone --temp 0.7 --seed 1
    python -m harness.draft --model engine/qwen2.5-14b-touchstone --temp 0.7 --seed 2

**4. Judge.** Read the candidates. Pick the winner, or keep your locked original.

**5. Promote, or keep it generated.** Write the winning render into `source/essay.locked.md` and re-encode, and the sentence is KEY again, locked to the words you chose. Or leave it STEERED and grounded: the mint renders it every time, so the published line stays provably generated rather than typed.

    python -m harness.encode && python -m harness.verify

**6. Polish in public.** Make each improvement its own commit, so the before and after are addressable by commit hash. The "notes on final edits" the essay promises are the git log.

**7. Anchor.** Sign the endpoints. The commit DAG shows the path between them.

    python -m harness.anchor --baseline <first-commit> --final HEAD

**8. Verify.** Any of these can be run by anyone, from the repo alone.

    python -m harness.verify --chain      # every mint receipt re-checks and chains
    python -m harness.anchor --verify     # both signed endpoints still hold
    python -m harness.bundle --verify FILE # a sealed single-file draft is not forged

## Steering to the capability envelope

A model is not a writer you correct line by line. It is an instrument with a capability envelope, and the work is declaring intent precisely enough that the instrument lands the effect you want. Different models have different envelopes, so you steer each one differently. There is room for every idea in the pool; the skill is matching the idea to the instrument that can carry it.

The same locked fact, *the cooler holds ice, and the ice chills the fog before it reaches the chest*, was minted three times each through a smart model (`qwen2.5-14b`) and a dumb one (`llama3.2-3b`). Full reviews are in `notes/candidate-reviews.md`. The short version:

- The **smart** model varied the *wording* and held the *fact*. Its worst miss was subtle: one fluent sentence that cooled the fog *generator* instead of the fog, a false claim wearing good prose.
- The **dumb** model varied the *subject* and held the *register*. Two of three takes abandoned the fact and confabulated a different prop, and every take invented a measured specific (`3.75 psi`, `80% brightness`) that nothing supplied. The dry voice never broke.

For the capable part, meaning is stable while the surface moves. For the weak part, the surface is stable while the meaning drifts off. So you steer to the envelope: the weak model is useful where register is the whole job and the fact is trivial; the capable model is where meaning has to survive rephrasing. And because voice alone would wave the dumb drafts through, grounding is checked separately from voice. That separation is the job of the human in the loop.

### The wider locked net

The effect you want is not always reachable by turning up the obvious dials. The first attempt to tighten a line tuned its *meaning* coordinates: rephrasing the ground fact, dropping the temperature, forbidding the words the model kept reaching for. It got worse. The model technicalized every time ("fog machine reservoir", "pump chamber") because it was generating in a vacuum, with no sense of the voice the sentence had to live in.

The fix was to widen the net: hand the model the sentence's own locked paragraph with the target gapped, and let it fill the hole in the surrounding voice. The target's own words are never shown, so the measurement still holds, but now the model can hear the room. The drift collapsed in one step:

    coordinates only:   The cooler maintains a steady temperature for the ice, which cools the fog fluid before it enters the fog machine reservoir.
    wider locked net:   The cooler contains ice that chills the fog before it enters the chest.

Same fact, same model, same decode. The only thing that changed was how much intent was declared. Intent is not just the fact a sentence must carry. It is the fact, plus the voice it sits inside, plus what it must not reach for, plus which instrument renders it and how far you let it breathe. Declare all of it and a capable model lands the line. The words are the model's; the intent is yours.

The net is a per-sentence choice (`"grounding": "section"`), not a global one, so the vacuum and the wider net both stay on the table: a line you want invented from nothing uses the bare coordinates, a line that has to belong uses the net.

## Writing is declaring intent

That is the whole claim behind this repository. Writing is not typing words. It is declaring intent, and that is all it is. Typing is just the lowest-bandwidth way to declare it, one word at a time, with the intent left implicit inside the choices. This harness makes the intent explicit and hands the typing to an instrument you have scoped to the effect. You do not write the sentence. You declare it precisely enough that it can come out right, pick the instrument whose envelope fits, and judge whether it did.

## Provenance: how you know a draft is real

Three independent layers, strongest last:

- **Chained receipts.** Each mint hashes its dataset, its model, its decode regime, and its output, signs the lot with an Ed25519 keeper key, and points at the previous receipt. Change one byte and a hash stops matching.
- **A sealed bundle.** `harness/bundle.py` folds a draft, its receipt, the full coordinate dataset, and the keeper public key into one self-verifying file, gated at seal time by a keepalive dead-man's switch so it can only be packaged while the owner is present. It verifies against itself.
- **Signed anchors plus the commit DAG.** The baseline and final essay are each signed; the public commit history is the path between them. The edits are not described after the fact, they *are* the record.

## Layout

- `source/essay.locked.md`: the locked baseline. Concatenating it is the floor.
- `coords/`: `_doc.json` index, `_voice.json` stance card, one `NN.json` per section.
- `harness/encode.py`: split the locked essay into the coords skeleton (all KEY).
- `harness/prompt.py`: build the deterministic prompt for one STEERED sentence (bare coordinates, or the wider locked net).
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
