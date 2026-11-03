"""
record -- the data model for the deterministic mint.

A section is a contiguous slice of the locked essay. Concatenating every
section's raw text, in order, reproduces source/essay.locked.md byte for byte.
Within a section, sentences are addressable by (start, end) offsets relative to
that section's raw. Everything between sentence spans (whitespace, the ***
separators, emphasis lines) is untouched structure that always survives verbatim.

Each sentence carries a tier:
  KEY     -- locked. Reconstruction uses the verbatim slice. Never rendered.
  STEERED -- rendered from its coordinates by the model, judged against the slice.

The coordinate layers on a sentence (filled in by Nick, empty at encode time):
  ground      L0  one short anchored fact the sentence must carry
  vrgb        L1  the three axes the essay itself names
  calibration L2  speculation / tone / density knobs

The source of truth on disk is coords/_doc.json (the index) plus one
coords/NN.json per section. This module only reads and writes that shape; it
holds no model and no I/O beyond json.
"""

import json
from pathlib import Path

KEY = "KEY"
STEERED = "STEERED"
TIERS = (KEY, STEERED)

# L1 -- the three axes the essay names in the VRGB section. Each is a float in
# [-1.0, 1.0]; negative leans to the first pole, positive to the second, 0.0 is
# neutral. None means "not yet encoded".
VRGB_AXES = (
    ("concrete_abstract", "concrete", "abstract"),
    ("individual_collective", "individual", "collective"),
    ("past_future", "past", "future"),
)

# L2 -- calibration knobs, each a float in [0.0, 1.0] or None if unset.
CALIBRATION_KNOBS = ("speculation", "tone", "density")


def empty_vrgb():
    return {name: None for name, _neg, _pos in VRGB_AXES}


def empty_calibration():
    return {knob: None for knob in CALIBRATION_KNOBS}


def new_sentence(start, end, text):
    """A sentence record defaulted to KEY with empty coordinate layers."""
    return {
        "start": start,
        "end": end,
        "text": text,
        "tier": KEY,
        "ground": "",
        "vrgb": empty_vrgb(),
        "calibration": empty_calibration(),
    }


def load_doc(repo_root):
    """Return (index_dict, [section_dict, ...]) read from coords/."""
    coords = Path(repo_root) / "coords"
    index = json.loads((coords / "_doc.json").read_text())
    sections = [json.loads((coords / name).read_text()) for name in index["sections"]]
    return index, sections


def load_voice(repo_root):
    path = Path(repo_root) / "coords" / "_voice.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def section_filename(index):
    return "%02d.json" % index
