"""Run 10, Inventor: three melody measures (notes side only; no outcome is touched here).

measure(t) -> dict with
  ARCH_PE : normalised persistent entropy of the contour's sublevel+superlevel H0 barcode (pitch as a function of note
            order, repeated pitches merged). Low = a few big arches carry the shape; high = many equal bumps.
  ARCH_TOP: share of total persistence held by the single longest finite bar (companion reading, not the test).
  LOCK    : beat-locking of contour turning points = P(on a beat | turning point) - P(on a beat | any note-run start).
  GAP     : spectral gap g = lambda_2 of the normalised Laplacian of the cyclic, symmetrised pitch-transition graph
            (octave-distinct MIDI pitches, counts, self-loops kept, last->first closes the loop). S = 1 + g/pi.
  GAP_PC  : same on pitch classes (12 nodes max).
  FIED_REG: |Spearman| between the Fiedler vector and pitch height (descriptive: is the Cheeger cut a register cut?).
No fitted settings. Uses only mel = {pitch, dur, bar, beatpos}.
Test readings proposed in run10/round1_inventor.md: ARCH_PE (pred -0.03), LOCK (pred +0.03), GAP (pred -0.03, with range,
n_pitch, ln_notes as frozen extra controls). ARCH_TOP, GAP_PC, FIED_REG are descriptive only.
Checks: checks.py (stability, renaming on a random 3,000 of split A, seed 10), gapn.py, gapres.py. No outcome opened.
"""
import math
import numpy as np


def _runs(p, bp):
    """merge consecutive equal pitches; keep the first note's beat position."""
    P, B = [], []
    for x, b in zip(p, bp):
        if P and P[-1] == x:
            continue
        P.append(x); B.append(b)
    return P, B


def _sublevel_bars(v):
    """finite H0 bars of the sublevel filtration of a function on a path graph (union-find, elder rule)."""
    n = len(v)
    order = sorted(range(n), key=lambda i: (v[i], i))
    parent = [-1] * n          # -1 = not yet added
    birth = [0.0] * n

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    bars = []
    for i in order:
        parent[i] = i; birth[i] = v[i]
        for j in (i - 1, i + 1):
            if 0 <= j < n and parent[j] != -1:
                ri, rj = find(i), find(j)
                if ri == rj:
                    continue
                # elder rule: the root with the later (higher) birth dies
                young, old = (ri, rj) if birth[ri] > birth[rj] else (rj, ri)
                if birth[young] == birth[old] and young < old:
                    young, old = old, young
                L = v[i] - birth[young]
                if L > 0:
                    bars.append(L)
                parent[young] = old
    return bars


def contour_bars(p):
    v = [float(x) for x in p]
    return _sublevel_bars(v) + _sublevel_bars([-x for x in v])


def _pent(bars):
    L = np.asarray(bars, float)
    if len(L) < 2:
        return None
    q = L / L.sum()
    return float(-(q * np.log(q)).sum() / math.log(len(L)))


def _gap(nodes_seq):
    labs = sorted(set(nodes_seq))
    k = len(labs)
    if k < 3:
        return None, None, labs
    ix = {x: i for i, x in enumerate(labs)}
    C = np.zeros((k, k))
    s = [ix[x] for x in nodes_seq]
    for a, b in zip(s, s[1:] + s[:1]):          # cyclic: the tune goes round
        C[a, b] += 1
    W = C + C.T
    d = W.sum(1)
    Dm = 1.0 / np.sqrt(d)
    Lap = np.eye(k) - (Dm[:, None] * W * Dm[None, :])
    w, V = np.linalg.eigh(Lap)
    fied = V[:, 1] * Dm                          # random-walk Fiedler vector
    return float(w[1]), fied, labs


def measure(t):
    m = t["mel"]
    p = [int(x) for x in m["pitch"]]
    bp = [float(x) for x in m["beatpos"]]
    if len(p) < 16:
        return None
    P, B = _runs(p, bp)
    if len(P) < 8:
        return None
    out = {}
    # 1. contour architecture (sublevel persistence of the melody as a function)
    bars = contour_bars(P)
    pe = _pent(bars)
    out["ARCH_PE"] = pe if pe is not None else float("nan")
    out["ARCH_TOP"] = float(max(bars) / sum(bars)) if bars else float("nan")
    # 2. beat-locked turning points
    onb = np.array([abs(b - round(b)) < 1e-6 for b in B], float)
    tp = [i for i in range(1, len(P) - 1)
          if (P[i] > P[i - 1] and P[i] > P[i + 1]) or (P[i] < P[i - 1] and P[i] < P[i + 1])]
    out["LOCK"] = float(onb[tp].mean() - onb.mean()) if len(tp) >= 4 else float("nan")
    # 3. two rooms and a doorway: spectral gap of the cyclic pitch-transition graph
    g, fied, labs = _gap(p)
    out["GAP"] = g if g is not None else float("nan")
    out["S"] = 1 + out["GAP"] / math.pi
    if fied is not None:
        from scipy.stats import spearmanr
        r = spearmanr(fied, labs).correlation
        out["FIED_REG"] = float(abs(r)) if np.isfinite(r) else float("nan")
    else:
        out["FIED_REG"] = float("nan")
    gpc, _, _ = _gap([x % 12 for x in p])
    out["GAP_PC"] = gpc if gpc is not None else float("nan")
    return out
