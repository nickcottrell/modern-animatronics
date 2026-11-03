"""
prompt -- build the deterministic prompt for one STEERED sentence.

build_prompt is a pure function: the same record and voice card always produce
the same prompt string. That purity is half of determinism; the pinned decode
regime (temperature 0, seed 0) is the other half. Together they make a STEERED
sentence reproducible, which is what lets Nick judge a render instead of
chasing a moving target.

The prompt never contains the locked verbatim. A STEERED sentence is rebuilt
from its coordinates alone -- that is the measurement: how much of the meaning
lives in the structure (ground + axes + knobs) versus the original phrasing.
"""

from . import record


def _axis_phrase(value, neg, pos):
    if value is None:
        return None
    magnitude = abs(value)
    if magnitude < 0.15:
        return "balanced between %s and %s" % (neg, pos)
    pole = neg if value < 0 else pos
    if magnitude < 0.4:
        strength = "slightly "
    elif magnitude < 0.75:
        strength = ""
    else:
        strength = "strongly "
    return "%s%s" % (strength, pole)


def _knob_phrase(knob, value):
    if value is None:
        return None
    if value < 0.33:
        level = "low"
    elif value < 0.66:
        level = "moderate"
    else:
        level = "high"
    return "%s: %s" % (knob, level)


def coordinate_lines(rec):
    """The human-readable coordinate block for one sentence, order-stable."""
    lines = []
    ground = rec.get("ground") or ""
    if ground.strip():
        lines.append("Fact to carry: %s" % ground.strip())

    vrgb = rec.get("vrgb") or {}
    axis_bits = []
    for name, neg, pos in record.VRGB_AXES:
        phrase = _axis_phrase(vrgb.get(name), neg, pos)
        if phrase is not None:
            axis_bits.append(phrase)
    if axis_bits:
        lines.append("Position: " + "; ".join(axis_bits))

    calib = rec.get("calibration") or {}
    knob_bits = []
    for knob in record.CALIBRATION_KNOBS:
        phrase = _knob_phrase(knob, calib.get(knob))
        if phrase is not None:
            knob_bits.append(phrase)
    if knob_bits:
        lines.append("Calibration: " + "; ".join(knob_bits))

    return lines


def build_prompt(rec, voice):
    """Return (system, prompt) for a STEERED sentence. Deterministic."""
    stance = (voice or {}).get("stance", "")
    forbid = (voice or {}).get("forbid") or []

    system_parts = []
    if stance:
        system_parts.append(stance)
    if forbid:
        system_parts.append("Never use: " + ", ".join(forbid) + ".")
    system = " ".join(system_parts)

    body = coordinate_lines(rec)
    body.append("Write exactly one sentence at these coordinates. Output only the sentence.")
    prompt = "\n".join(body)
    return system, prompt
