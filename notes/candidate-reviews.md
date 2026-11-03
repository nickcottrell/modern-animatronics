# Candidate reviews, section 2 sentence 14

One STEERED sentence, six takes. Three from the smart model (qwen2.5-14b),
three from the dumb model (llama3.2-3b), each at temperature 0.7 with a fixed
seed so the take is reproducible from its receipt.

**Ground fact (the locked input):** the cooler holds ice, and the ice chills the
fog before it reaches the treasure chest.

**Locked original (Nick's KEY line):** "The cooler holds ice, which chills the
fog before it reaches the chest."

**Scoring axes.** Fidelity: does the sentence carry the ground fact and nothing
the fact did not assert. Voice: dry, understated, present-tense, operational,
concrete nouns, one idea. Discipline: sparse (density 0.2), no invented
specifics, no forbidden moves. Each axis is 0 to 5.

---

## Smart model (qwen2.5-14b)

### [03] seed 1 - Fidelity 4 / Voice 3 / Discipline 2
"A portable cooler next to a fog machine contains ice that cools the fog prior
to its release into a nearby treasure chest."

The fact survives: cooler, ice, fog, chest, in the right causal order. But the
sentence over-builds. It stakes three spatial claims the fact never made ("next
to a fog machine," "nearby treasure chest," and the fog being "released into"
the chest), and that last one is a small distortion: the fog *reaches* the
chest, it is not released *into* it. "prior to its release" is procurement
language where the voice wants a plain verb. Two ideas braided into one line,
against the one-idea rule and the 0.2 density target. Competent, but padded and
slightly off-mechanism.

### [04] seed 2 - Fidelity 5 / Voice 5 / Discipline 5  — WINNER
"The cooler maintains ice to chill the fog flowing towards the treasure chest."

The fact, clean, in one idea, in the operational register the voice card asks
for. "maintains ice" is the sentence's one real choice and it is a good one: it
reads like a status line from someone running the attraction, which is exactly
the stance. Nothing is invented, nothing is over-specified, the causal chain is
intact. The only nits are cosmetic: "maintains" is a hair less plain than the
locked "holds," and "towards" carries a British spelling the rest of the essay
may not. Both are one-word fixes for the polish pass. This is the take to
promote.

### [05] seed 3 - Fidelity 2 / Voice 4 / Discipline 4
"The cooler containing ice cools the fog generator positioned near the treasure
chest."

Reads well and sounds operational, which makes its error easy to miss: it cools
the wrong thing. The ice chills the *fog*; this sentence has the cooler cooling
the *fog generator*. That inverts the mechanism the whole gag depends on (cold
fog sinks and pools, which is why it is cooled at all). "positioned near" is
again more spatial precision than the fact licensed. A fluent sentence that
quietly says something untrue. The most instructive smart-model failure, because
the prose quality camouflages the fault.

---

## Dumb model (llama3.2-3b)

### [06] seed 1 - Fidelity 0 / Voice 3 / Discipline 1
"A LED light embedded in a foam block casts a 270-degree beam onto the ground
beneath the plastic spiders, which remain stationary despite slight wind
fluctuations."

There is no cooler, no ice, no fog, no chest. The model abandoned the fact and
confabulated a different prop from a different corner of the scene. It also
fabricates a measured specific ("270-degree beam") that nothing asked for. The
cruel part is that the voice is roughly right: it is dry, concrete, and
operational. A stylistically plausible sentence about entirely the wrong thing.
This is the dangerous failure mode, because voice alone would pass it.

### [07] seed 2 - Fidelity 1 / Voice 2 / Discipline 0
"The pump attached to the fog machine is set to 3.75 psi, creating a steady flow
of mist that will condense on the glass surface of the treasure chest."

Partial contact with the fact: fog, mist, and the chest are still in frame. But
it invents a pump, a fabricated pressure ("3.75 psi"), and a material the chest
never had ("glass surface"), then distorts the mechanism, the fog is supposed to
chill and reach the chest, not condense on glass. Three fabricated specifics in
one sentence. False precision is the model's tell: it reaches for a number to
sound authoritative and manufactures one.

### [08] seed 3 - Fidelity 0 / Voice 3 / Discipline 1
"The LED lights on the skeleton's face are set to 80% brightness, simulating a
mild glow in the dark environment."

Total topic collapse again, now a skeleton. No cooler, ice, fog, or chest. Same
signature as seed 1: a fluent, dry, operational sentence about a prop the fact
never mentioned, decorated with a fabricated setting ("80% brightness").
Consistent with the model's behavior across seeds, it does not phrase the fact,
it replaces it.

---

## The pattern

The smart model's three takes vary in *wording* while holding the *fact*; its
worst failure (05) is a subtle mechanism error inside otherwise faithful prose.
The dumb model's three takes vary in *subject*: two of three abandon the ground
fact entirely and confabulate a different prop, and all three fabricate measured
specifics that were never supplied.

The instrument is measuring coherence over time. For the smart model, meaning is
stable across takes and only the surface moves. For the dumb model, the surface
is stable (same dry register every time) while the meaning drifts off the fact
completely. That inversion, stable meaning under moving words versus stable words
under moving meaning, is the finding the essay is about, produced by the harness
the essay describes.
