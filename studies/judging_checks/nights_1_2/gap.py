"""Checks on the judging research, A: the spectral gap g rebuilt from the chair's written rules, and its split-half stability. See PREDICTION.md.
python3 studies/judging_checks/nights_1_2/gap.py -> gap.json. No outcome is read: peak and date are deleted on load."""
import os, json, math, hashlib, numpy as np
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
B = json.load(open(os.path.join(ROOT, "studies", "harmony", "billboard_sections.json")))
for s in B: s.pop("peak", None); s.pop("date", None)
def tokens(sec): return [r + ("7" if v else "") for b in sec["bars"] for r, v in zip(b["rn"], b["sev"]) if r is not None]
def merge(seq):
    out = []
    for x in seq:
        if not out or out[-1] != x: out.append(x)
    return out
def rep3(seq):
    seen = set(); rep = tot = 0
    for i in range(len(seq) - 2):
        g = tuple(seq[i:i + 3]); tot += 1; rep += g in seen; seen.add(g)
    return rep / tot if tot else None
def graph(seq):
    seq = list(seq)
    if seq[0] == seq[-1] and len(seq) > 1: seq = seq[:-1]                 # the song as a cycle: the last chord moves to the first (merged if the same)
    names = sorted(set(seq)); ix = {n: i for i, n in enumerate(names)}; n = len(names)
    if n < 2 or len(seq) < 4: return None
    M = np.zeros((n, n))
    for a, b in zip(seq, seq[1:] + seq[:1]):
        if a != b: M[ix[a], ix[b]] += 1
    if (M.sum(1) == 0).any(): return None
    return M
def gap(seq):
    M = graph(seq)
    if M is None: return None
    P = M / M.sum(1, keepdims=True); ev = sorted(np.abs(np.linalg.eigvals(P)), reverse=True); return float(1 - ev[1])
def branch(seq):
    M = graph(seq)
    if M is None or len(M) < 3: return None
    P = M / M.sum(1, keepdims=True); n = len(M); return float(np.mean([-(p[p > 0] * np.log2(p[p > 0])).sum() / math.log2(n - 1) for p in P]))
rows = []
for s in B:
    whole = merge([t for sec in s["sections"] for t in tokens(sec)]); g = gap(whole) if len(whole) >= 4 else None
    if g is None: continue
    seen = set(); num = den = 0.0
    for sec in s["sections"]:
        if sec["letter"] in seen: continue
        seen.add(sec["letter"]); m = merge(tokens(sec))
        if len(m) >= 4: num += rep3(m) * len(sec["bars"]); den += len(sec["bars"])
    h = len(whole) // 2; a, b = whole[:h], whole[h:]
    rows.append(dict(id=s["id"], artist=s["artist"], g=g, rep=num / den if den else None, distinct=len(set(whole)), length=len(whole), E=branch(whole),
                     g1=gap(a) if len(a) >= 4 else None, g2=gap(b) if len(b) >= 4 else None, d1=len(set(a)), d2=len(set(b)), r1=rep3(a), r2=rep3(b)))
def sp(x, y):
    k = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]; r, p = spearmanr([a for a, _ in k], [b for _, b in k]); return dict(rho=round(float(r), 3), n=len(k))
col = lambda c: [r[c] for r in rows]; G = np.array(col("g"))
out = dict(songs_read=len(B), songs_kept=len(rows),
           reproduction=dict(chair=dict(songs_kept=721, g_with_repetition=-0.26, g_with_distinct_chords=0.02, g_with_E=0.47, median_g=0.19, middle_half=[0.09, 0.30], share_under_0_01=0.087),
                             here=dict(songs_kept=len(rows), g_with_repetition=sp(col("g"), col("rep")), g_with_distinct_chords=sp(col("g"), col("distinct")), g_with_E=sp(col("g"), col("E")), g_with_length=sp(col("g"), col("length")),
                                       median_g=round(float(np.median(G)), 3), middle_half=[round(float(x), 3) for x in np.percentile(G, (25, 75))], share_under_0_01=round(float(np.mean(G < 0.01)), 3))),
           split_half=dict(g=sp(col("g1"), col("g2")), distinct_chords=sp(col("d1"), col("d2")), repetition_3grams=sp(col("r1"), col("r2")),
                           g_by_distinct_chords={k: sp([r["g1"] for r in rows if lo <= r["distinct"] <= hi], [r["g2"] for r in rows if lo <= r["distinct"] <= hi]) for k, (lo, hi) in (("2 to 5", (2, 5)), ("6 to 9", (6, 9)), ("10 or more", (10, 999)))}))
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, "gap.json"), "w"), indent=1)
