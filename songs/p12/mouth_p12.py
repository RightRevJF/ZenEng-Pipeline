"""Song 12, Wood and Cloth (second edition): the mouth test, every line, as song 61's (Luthier v7 Principle 4: weak endings,
density and friction, word-boundary clusters, the held vowel, rare words), with the hymn's own tests added because one tune
carries five stanzas (749.11-749.13, Module 11.19):
  the 87 87 template: exact syllable counts 8 7 8 7;
  trochaic strong positions 1 3 5 7 in every line: a stressed syllable of a content word placed on a weak position, or an
  unstressed syllable on a strong one, is reported (monosyllabic function words are free either way);
  the line-end hold: an 8-syllable line holds its 7th syllable into a weak 8th; a 7-syllable line holds its 7th; the held
  vowel is read there;
  the shared tune: for each position, whether all five stanzas agree on stress (the column test).
Tempo provisional: q = 100 in 3/4, a line across four bars (twelve beats, about eleven sung), until the new tune is drawn."""
import re, sys
sys.path[:0] = ["/home/claude/carol", "/home/claude/zeneng-pipeline/songs/p71"]
import mouth_p71 as M
from lyricsearch import words, syllables, FUNCTION, phones
M.QBPM, M.BEATS = 100, 11.0
def stress_row(line):
    """per syllable: 1 stressed content, 0 unstressed, f free (monosyllabic function word)"""
    out = []
    for w in words(line):
        ps = [p for p in phones(w).split() if p[-1].isdigit()]
        if len(ps) == 1:
            out.append("f" if w in FUNCTION else "1")
        else:
            out += ["1" if p[-1] == "1" else "0" for p in ps]
    return out
stanzas = []; cur = None
for raw in open("lyric_locked.md"):
    l = raw.strip()
    if l.startswith("## "): cur = []; stanzas.append((l[3:], cur)); continue
    if l and not l.startswith("#"): cur.append(l)
print("== the mouth test, every line (q = 100, 3/4, a line across about 11 beats)")
for name, ls in stanzas:
    prev = []
    for i, l in enumerate(ls):
        n, sps, fr, fl = M.read(l, tuple(prev)); prev.append(l)
        want = [8, 7, 8, 7][i]; row = stress_row(l)
        if n != want: fl.append(f"syllables {n}, the metre wants {want}")
        for k, s in enumerate(row):
            strong = k % 2 == 0
            if strong and s == "0": fl.append(f"unstressed syllable on strong position {k+1}")
            if not strong and s == "1" and not (k + 1 == 8): fl.append(f"stressed syllable on weak position {k+1}")
        syl = syllables(l); hold = syl[6] if len(syl) >= 7 else syl[-1]; v = re.sub(r"\d", "", hold[1])
        if hold[1] in M.REDUCED: fl.append(f"held syllable reduced ({hold[0]})")
        elif v in M.CLOSE: fl.append(f"held vowel close ({v} in '{hold[0]}')")
        print(f"{name:9} L{i+1} {n:2d} syl {sps:4.2f}/s fr {fr:5.2f} | {''.join(row):8} | {l}" + ("   <- " + "; ".join(fl) if fl else ""))
print("\n== the column test (one tune, five stanzas): stress by position, 1 stressed, 0 unstressed, f free")
for i in range(4):
    rows = [stress_row(ls[i]) for _, ls in stanzas]
    cols = ["".join(r[k] if k < len(r) else "-" for r in rows) for k in range(max(map(len, rows)))]
    bad = [f"pos {k+1} ({'strong' if k % 2 == 0 else 'weak'}): {c}" for k, c in enumerate(cols) if ("0" in c and k % 2 == 0) or ("1" in c and k % 2 == 1 and k != 7)]
    print(f"line {i+1}: " + " ".join(cols) + ("   <- " + "; ".join(bad) if bad else "   clean"))
