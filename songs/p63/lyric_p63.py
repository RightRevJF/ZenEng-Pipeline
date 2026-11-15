"""Sung to Sleep (song 53): the locked lyric, syllabified for singing. Common Meter (8.6.8.6), iambic: every line opens on a pickup
syllable except the refrain's 'Hush now' lines, which open on the downbeat. A syllable list per line; '-' joins a word's syllables."""
TITLE = "Sung to Sleep"
VERSES = [
    ["Be- fore the hills, be- fore the sea", "be- fore the first of days", "there was a Song, and at its sound", "the stars be- gan to blaze"],
    ["That Song came down and had to learn", "to breathe the win- ter air", "the voice that called the light to be", "now cried for Ma- ry there"],
    ["She hummed the tune her moth- er hummed", "and rocked him in the hay", "and he who taught the stars to sing", "was sung to sleep that way"],
    ["And he will sing a- gain one day", "when all the night is done", "and o- ver us, with joy, the Song", "will sing us, ev- ery one"],
]
REFRAIN = ["Hush now, the Song of God is small", "hush now, the stars are near", "the One who sang the world a- wake", "is sleep- ing, sleep- ing here"]
def syls(line):
    """'Be- fore the' -> [('Be', True), ('fore', False), ('the', False)]: (text, joins the next syllable)"""
    out = []
    for w in line.split():
        out.append((w[:-1], True) if w.endswith("-") else (w, False))
    return out
SHAPE = [8, 6, 8, 6]
for v in VERSES + [REFRAIN]:
    assert [len(syls(l)) for l in v] == SHAPE, [len(syls(l)) for l in v]
