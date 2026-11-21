"""Wood and Cloth (second edition): the locked lyric as data. Five stanzas of 87 87, trochaic; every line starts on a downbeat."""
import re, sys
sys.path[:0] = ["/home/claude/carol"]
from lyricsearch import syllables as _syl
TITLE = "Wood and Cloth"; EDITION = " (third edition)"
SHAPE = [8, 7, 8, 7]
STANZAS = []
for raw in open("/home/claude/zeneng-pipeline/songs/p12/lyric_locked.md"):
    l = raw.strip()
    if l.startswith("## "): STANZAS.append([]); continue
    if l and not l.startswith("#"): STANZAS[-1].append(l)
assert len(STANZAS) == 5 and all(len(s) == 4 for s in STANZAS)
HYPH = {}   # printed hyphenation, from the spelling
def syls(line):
    """printed syllables of a line: [(text, word_index)], hyphenated by spelling; counts checked against SHAPE"""
    out = []
    for wi, w in enumerate(line.split()):
        core = w.strip(",;:.")
        parts = SPLIT.get(core.lower())
        if parts is None: parts = [core]
        # keep the original case on the first part and the trailing punctuation on the last
        if core[:1].isupper(): parts = [parts[0][:1].upper() + parts[0][1:]] + parts[1:]
        tail = w[len(core):]
        for k, p in enumerate(parts):
            out.append((p + ("" if k < len(parts) - 1 else tail), wi, k < len(parts) - 1))
    return out
SPLIT = {"oxen": ["ox", "en"], "maker": ["Ma", "ker"], "enough": ["e", "nough"], "dying": ["dy", "ing"], "either": ["ei", "ther"],
         "mary": ["Ma", "ry"], "linen": ["lin", "en"], "against": ["a", "gainst"], "winter": ["win", "ter"], "joseph": ["Jo", "seph"],
         "before": ["be", "fore"], "carry": ["car", "ry"], "borrowed": ["bor", "rowed"], "garden": ["gar", "den"],
         "strangers": ["stran", "gers"], "judah": ["Ju", "dah"], "beneath": ["be", "neath"], "pilate": ["Pi", "late"],
         "above": ["a", "bove"], "lying": ["ly", "ing"], "manger": ["man", "ger"], "sleeping": ["sleep", "ing"], "behind": ["be", "hind"]}
for s in STANZAS:
    for i, l in enumerate(s):
        assert len(syls(l)) == SHAPE[i], (l, syls(l))
