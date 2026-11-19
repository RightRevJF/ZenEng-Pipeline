"""Luthier v22, way 3 (Module 27.103; fixes 879-884): the marriage of tune and words.

A sung syllable has a WEIGHT the engine can read without ears: 0 for a one-syllable function word (the, of, and, my), 1 for the weak syllable of a longer word,
2 for a stressed syllable. A note has a SALIENCE: its length, its place in the bar, its height within its line. Kept songs give the weightier syllable the more
salient note: the rank correlation of the two over a song (the FIT) stands at 0.20 / 0.29 / 0.38 by quartile over 159 kept songs (0.202, 0.291, 0.384; 10th percentile 0.092), and beats the same
song with each line's words dealt again over its notes in 89 songs in 100 (the first measure, which also weighed a word's rarity, gave 0.18 / 0.28 / 0.37 and 87; 898, 749.72). The engine's builds stood at 0.09 to 0.16. tables/kept_word_weight.json holds what the kept songs do:
where in the bar each weight is sung, which way the tune steps between two weights, and the kept songs' own fits.
    tier(sy)           the weights of a line's syllables, from the engine's own (text, stressed) pairs
    place(t, bar)      0 bar start, 1 half bar, 2 another beat, 3 an off-beat eighth, 4 finer
    fit(notes, bar)    the fit of a build or a song: notes carry on, dur, p (or midi), text, stress, sec, line
Nothing here says a song is great: the fit does not rank kept songs by their chart record (0.03 with weeks, 0.00 with peak). It is a gate, not a pick (858)."""
import json, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TABLE = os.path.join(HERE, "..", "..", "tables", "kept_word_weight.json")
WEIGHT = (0.0, 0.4, 1.0)
def tier(sy):
    out = []
    for k, x in enumerate(sy):
        if x[1]: out.append(2)
        elif (k > 0 and sy[k - 1][0] == x[0]) or (k + 1 < len(sy) and sy[k + 1][0] == x[0]): out.append(1)
        else: out.append(0)
    return out
def place(t, bar=48, beat=12):
    p = t % bar; return 0 if p == 0 else 1 if (bar % 2 == 0 and p == bar // 2) else 2 if p % beat == 0 else 3 if p % (beat // 2) == 0 else 4
PLACE_VALUE = (3.0, 2.0, 1.0, 0.3, 0.0)
def _rank(v):
    v = np.asarray(v, float); o = np.argsort(v, kind="mergesort"); r = np.empty(len(v)); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[o[j + 1]] == v[o[i]]: j += 1
        r[o[i:j + 1]] = (i + j) / 2.0; i = j + 1
    return r
def spearman(a, b):
    ra, rb = _rank(a), _rank(b)
    if ra.std() == 0 or rb.std() == 0: return 0.0
    return float(np.corrcoef(ra, rb)[0, 1])
def salience(t, dur, p, lines, bar=48, beat=12):
    z = lambda v: (v - v.mean()) / (v.std() + 1e-9); t = np.asarray(t); d = np.log(np.maximum(3, np.asarray(dur, float))); m = np.array([PLACE_VALUE[place(x, bar, beat)] for x in t]); p = np.asarray(p, float); h = np.zeros(len(p)); lines = np.asarray(lines)
    for l in set(lines.tolist()):
        k = lines == l; h[k] = p[k] - p[k].mean()
    return dict(length=z(d), place=z(m), height=z(h), all=(z(d) + z(m) + z(h)) / 3)
def sung_lines(t, gap=24):
    out = []; l = 0
    for i in range(len(t)):
        if i and t[i] - t[i - 1] >= gap: l += 1
        out.append(l)
    return out
def fit(notes, bar=48, beat=12, parts=False):
    """notes in time order, each with on, dur, p or midi, text, stress, sec, line. The weights are read line by line from (text, stress)."""
    tr = []; i = 0
    while i < len(notes):
        j = i
        while j < len(notes) and (notes[j]["sec"], notes[j]["line"]) == (notes[i]["sec"], notes[i]["line"]): j += 1
        tr += tier([(n["text"], n["stress"]) for n in notes[i:j]]); i = j
    t = [n["on"] for n in notes]; S = salience(t, [n["dur"] for n in notes], [n.get("p", n.get("midi")) for n in notes], sung_lines(t), bar, beat); w = [WEIGHT[x] for x in tr]
    return {k: spearman(w, S[k]) for k in S} if parts else spearman(w, S["all"])
def table(): return json.load(open(TABLE))
