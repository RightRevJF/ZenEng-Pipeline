"""luthier_read.py: Luthier v1's readings of a melody (605, 606, 607), as luthier_v1_structure.json defines them.
- bar rhythms: a sung bar's rhythm is the tuple of its onset positions in twelfths of a beat (0-47); bars by bar number; a bar's section is
  the section of most of its onsets, trailing numbers removed ('Verse 1' and 'Verse 2' are 'Verse').
- recurrence(k): within a section, the share of pairs of sung bars k apart whose rhythms are exactly the same (and Jaccard 0.6 or more).
- coupling gain: pseudo-log-likelihood, bits a bar, of the kept couplings J (k = 1, 2, 4, 8, 16) over none, q = the song's own shares.
- bits saved: the melody's first half (by notes) mixed into the corpus model (the kept mean palette) at share w, tested on its second half,
  per gap (nine classes) and per interval (-7..+7, clipped)."""
import json, math, collections
import numpy as np
T = json.load(open("/home/claude/p59/tables/luthier_v1_structure.json"))
J = dict(zip((1, 2, 4, 8, 16), T["605: the bar model. x_b = the rhythm of sung bar b; P(x_b = v | the rest) is proportional to q(v) exp(sum over k of J_k [d(v, x_{b-k}) + d(v, x_{b+k})]), q = the song's own shares of its bar rhythms, d = 1 if equal. J for k = 1, 2, 4, 8, 16"]))
MEANPAL = T["606: the kept mean palette (gaps; intervals)"]
BAR = 48
def gclass(g):
    return 0 if g <= 3 else 1 if g == 4 else 2 if g <= 6 else 3 if g <= 9 else 4 if g <= 12 else 5 if g <= 18 else 6 if g <= 24 else 7 if g <= 48 else 8
def sec_label(s): return s.rstrip("0123456789 ").strip()
def bars(notes):
    """{bar: (rhythm tuple, section label)} for sung bars; notes: dicts with on, sec."""
    by = collections.defaultdict(list)
    for n in notes: by[n["on"] // BAR].append(n)
    out = {}
    for b, ns in by.items():
        lab = collections.Counter(sec_label(n["sec"]) for n in ns).most_common(1)[0][0]
        out[b] = (tuple(sorted({n["on"] % BAR for n in ns})), lab)
    return out
def recurrence(notes, ks=(1, 2, 4, 8, 16)):
    B = bars(notes); out = {}
    for k in ks:
        same = jac = n = 0
        for b, (r, lab) in B.items():
            if b + k in B and B[b + k][1] == lab:
                r2 = B[b + k][0]; n += 1; same += (r == r2)
                jac += (len(set(r) & set(r2)) / max(1, len(set(r) | set(r2))) >= 0.6)
        out[k] = (same / n if n else None, jac / n if n else None, n)
    return out
def coupling_gain(notes):
    B = bars(notes); seq = sorted(B); xs = {b: B[b][0] for b in seq}
    cnt = collections.Counter(xs.values()); N = len(seq); q = {v: c / N for v, c in cnt.items()}; vals = list(q)
    g = []
    for b in seq:
        e = {v: sum(J[k] * ((xs.get(b - k) == v) + (xs.get(b + k) == v)) for k in J) for v in vals}
        z = sum(q[v] * math.exp(e[v]) for v in vals)
        g.append(math.log2(math.exp(e[xs[b]]) / z))                                     # log2 P_J(x_b) - log2 q(x_b)
    return float(np.mean(g)) if g else None
def sequences(notes):
    ns = sorted(notes, key=lambda n: n["on"])
    gaps = [gclass(b["on"] - a["on"]) for a, b in zip(ns, ns[1:])]
    ivs = [max(-7, min(7, b["p"] - a["p"])) + 7 for a, b in zip(ns, ns[1:])]
    return gaps, ivs
def bits_saved(seq, corpus, w):
    h = len(seq) // 2; a, b = seq[:h], seq[h:]
    if not a or not b: return None
    own = np.bincount(a, minlength=len(corpus)) / len(a); cp = np.array(corpus, float); cp = cp / cp.sum()
    mix = w * own + (1 - w) * cp
    base = -np.mean([math.log2(max(1e-12, cp[x])) for x in b]); mixed = -np.mean([math.log2(max(1e-12, mix[x])) for x in b])
    return base, base - mixed
W_GRID = (0.1, 0.3, 0.5, 0.7, 0.85, 0.9)
def saved_both(notes):
    g, iv = sequences(notes)
    return {w: (bits_saved(g, MEANPAL[0], w), bits_saved(iv, MEANPAL[1], w)) for w in W_GRID}
