"""
encode -- split source/essay.locked.md into the coords/ skeleton.

The essay is cut at every line that is exactly "***". Each cut begins a new
section slice, so concatenating every slice reproduces the file exactly (the
separator lives at the head of the section that follows it). The head matter
before the first separator is section 00.

Within each slice, sentences are found by a deliberately plain splitter: a run
of non-newline text ending in terminal punctuation followed by whitespace or
end of line. Anything the splitter does not claim -- titles, emphasis lines,
the separators, blank lines -- is preserved untouched. Reconstruction never
depends on the splitter being clever, only on span replacement being exact.

Every sentence starts life KEY. Settling the prose first and opening sentences
to STEERED later is the whole posture: the rig goes around the prose.

Run:  python -m harness.encode          (from the repo root)
"""

import json
import re
import sys
from pathlib import Path

from . import record

SENTENCE = re.compile(r"\S.*?[.?!]+(?=\s|$)")
SEPARATOR = re.compile(r"^\*\*\*$", re.MULTILINE)


def split_sections(text):
    """Return a list of (start, raw) slices whose raws concatenate to text."""
    cuts = [m.start() for m in SEPARATOR.finditer(text)]
    bounds = [0] + cuts + [len(text)]
    # Drop a zero-length leading slice if the file somehow opens on a separator.
    slices = []
    for i in range(len(bounds) - 1):
        start, end = bounds[i], bounds[i + 1]
        if end > start:
            slices.append((start, text[start:end]))
    return slices


def find_sentences(raw):
    out = []
    for m in SENTENCE.finditer(raw):
        out.append(record.new_sentence(m.start(), m.end(), m.group()))
    return out


def encode(repo_root):
    repo_root = Path(repo_root)
    source = repo_root / "source" / "essay.locked.md"
    text = source.read_text()

    coords = repo_root / "coords"
    coords.mkdir(exist_ok=True)

    section_files = []
    for index, (start, raw) in enumerate(split_sections(text)):
        sentences = find_sentences(raw)
        section = {
            "index": index,
            "doc_offset": start,
            "raw": raw,
            "sentences": sentences,
        }
        name = record.section_filename(index)
        (coords / name).write_text(json.dumps(section, indent=2) + "\n")
        section_files.append(name)

    import hashlib
    sha = hashlib.sha256(text.encode()).hexdigest()
    index_doc = {
        "source": "source/essay.locked.md",
        "sha256": sha,
        "sections": section_files,
    }
    (coords / "_doc.json").write_text(json.dumps(index_doc, indent=2) + "\n")

    voice = coords / "_voice.json"
    if not voice.exists():
        voice.write_text(json.dumps(DEFAULT_VOICE, indent=2) + "\n")

    total = 0
    for name in section_files:
        sec = json.loads((coords / name).read_text())
        total += len(sec["sentences"])
    return len(section_files), total


# Doc-level stance. Loaded once and prepended to every STEERED prompt. This is
# the essay's register, written as instruction, not computed at runtime.
DEFAULT_VOICE = {
    "name": "ladera-ranch-operator",
    "stance": (
        "Dry, understated, present-tense. A software person narrating a Halloween "
        "porch attraction as if filing a calm operational report. Concrete nouns "
        "over abstractions. The joke is in the deadpan, never announced. One idea "
        "per sentence. No exclamation, no hype, no summary of what was just said."
    ),
    "forbid": ["em dash", "exclamation point", "rhetorical questions stacked", "hype adjectives"],
}


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    n_sections, n_sentences = encode(root)
    print("encoded %d sections, %d sentences -> coords/" % (n_sections, n_sentences), file=sys.stderr)
