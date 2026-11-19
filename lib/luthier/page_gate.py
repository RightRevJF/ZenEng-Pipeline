"""922, 923 (Window 188): the page gate. What a tune's written notes say about whether it is the kind of tune that gets kept:
a next note easy to foresee, few different pitches, the home note, five or six notes of the scale, few leaps, its own short figures sung again.
Found on 23,205 session tunes and 10,360 hymn tunes and inside artists' own work (studies/session_lab, hymn_lab, gate, gates_strengthened);
here it is read against the kept 4/4 pop tunes (tables/kept_page_gate.json, made by make_kept_page_gate.py), as a floor and not as an aim."""
import os, json, math, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); TABLE = os.path.join(HERE, "..", "..", "tables", "kept_page_gate.json")
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
PLAIN = dict(surprise=-1, six_note_share=1, five_note_share=1, time_on_tonic=1, different_pitches=-1, different_intervals=-1, leaps=-1, range=-1, repeated_notes=1, repeated_figures=1)   # which way is plain
K = 3                                                                                         # the notes before, by their intervals, that the next interval is foreseen from
def ivs(p): return [max(-12, min(12, int(p[i] - p[i - 1]))) for i in range(1, len(p))]
def _ent(v):
    c = np.array(list(collections.Counter(v).values()), float); q = c / c.sum(); return float(-(q * np.log2(q)).sum())
def counts(seqs):
    """interval counts for contexts of 0 to K intervals: c[k][context + (next,)] and n[k][context]"""
    c = [collections.Counter() for _ in range(K + 1)]; n = [collections.Counter() for _ in range(K + 1)]
    for s in seqs:
        for i in range(len(s)):
            for k in range(K + 1):
                if i - k >= 0: c[k][tuple(s[i - k:i + 1])] += 1; n[k][tuple(s[i - k:i])] += 1
    return c, n
def surprise(s, C, minus=None):
    """mean bits per interval under the kept tunes' counts, shorter contexts backing the longer; minus = a tune's own counts, taken out when it is one of the kept"""
    c, n = C; out = []
    for i in range(len(s)):
        p = 1.0 / 25
        for k in range(K + 1):
            if i - k < 0: break
            a = c[k][tuple(s[i - k:i + 1])]; b = n[k][tuple(s[i - k:i])]
            if minus: a -= minus[0][k][tuple(s[i - k:i + 1])]; b -= minus[1][k][tuple(s[i - k:i])]
            p = (a + 2.0 * p) / (b + 2.0)
        out.append(-math.log2(max(p, 1e-9)))
    return float(np.mean(out)) if out else float("nan")
def figures_again(p, k=4):
    """the share of a tune's four-interval figures that it has already sung"""
    s = ivs(p); g = [tuple(s[i:i + k]) for i in range(len(s) - k + 1)]; return 1 - len(set(g)) / max(len(g), 1)
def parts(p, d):
    """p: pitches in order; d: each note's time to the next, in beats"""
    p = np.asarray(p, float); d = np.clip(np.asarray(d, float), .0625, 8); h = np.bincount(p.astype(int) % 12, d, 12); cm = [np.corrcoef(np.roll(MAJ, k), h)[0, 1] for k in range(12)]; cn = [np.corrcoef(np.roll(MIN, k), h)[0, 1] for k in range(12)]
    minor = max(cn) > max(cm); ton = int(np.argmax(cn if minor else cm)); pc = (p.astype(int) - ton) % 12; a = np.abs(np.diff(p)); six = [0, 3, 5, 7, 8, 10] if minor else [0, 2, 4, 5, 7, 9]; five = [0, 3, 5, 7, 10] if minor else [0, 2, 4, 7, 9]
    return dict(six_note_share=float(np.isin(pc, six).mean()), five_note_share=float(np.isin(pc, five).mean()), time_on_tonic=float((pc == 0).mean()), different_pitches=_ent(p), different_intervals=_ent(np.diff(p)), leaps=float((a > 4).mean()), range=float(p.max() - p.min()), repeated_notes=float((a == 0).mean()), repeated_figures=figures_again(p))
_T = None
def table():
    global _T
    if _T is None:
        T = json.load(open(TABLE)); c = [collections.Counter({tuple(int(x) for x in k.split(",")) if k else (): v for k, v in t.items()}) for t in T["interval_counts"]]; n = [collections.Counter() for _ in range(K + 1)]
        for k in range(K + 1):
            for key, v in c[k].items(): n[k][key[:-1]] += v
        T["_C"] = (c, n); _T = T
    return _T
def read(p, d, T=None):
    """every part of the gate for one tune, and the plainness they add up to (each part against the kept tunes' mean and spread, turned the plain way)"""
    T = T or table(); r = parts(p, d); r["surprise"] = surprise(ivs([int(x) for x in p]), T["_C"]); r["plainness"] = float(np.mean([PLAIN[c] * (r[c] - T["mean"][c]) / T["sd"][c] for c in PLAIN])); return r
def place(v, part, T=None):
    """the share of kept tunes a value is plainer than, 0 to 100"""
    T = T or table(); k = np.asarray(T["kept_values"][part]); s = float((k < v).mean() * 100); return s if PLAIN.get(part, 1) > 0 else 100 - s
