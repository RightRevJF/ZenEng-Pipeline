"""Run 10's deductions, re-built on Hooktheory clip melodies (the recipes of run10/experiments/measures/measures_inventor.py;
no TheSession data is read). GAP: lambda_2 of the normalised Laplacian of the cyclic, symmetrised octave-distinct pitch-transition
graph (counts, self-loops kept). S = 1 + GAP/pi. LOCK: P(on a beat | contour turning point) - P(on a beat | any note-run start)."""
import math, numpy as np
KEYS = ["GAP", "S", "LOCK"]

def _gap(seq):
    labs = sorted(set(seq)); k = len(labs)
    if k < 3: return None
    ix = {x: i for i, x in enumerate(labs)}; C = np.zeros((k, k)); s = [ix[x] for x in seq]
    for a, b in zip(s, s[1:] + s[:1]): C[a, b] += 1
    W = C + C.T; d = W.sum(1); Dm = 1.0 / np.sqrt(d)
    return float(np.linalg.eigvalsh(np.eye(k) - Dm[:, None] * W * Dm[None, :])[1])

def clip_measure(mel, a):
    p = mel["pitch"]; bp = mel["beatpos"]
    g = _gap(p)
    P, B = [], []
    for x, b in zip(p, bp):
        if P and P[-1] == x: continue
        P.append(x); B.append(b)
    onb = np.array([abs(b - round(b)) < 1e-6 for b in B], float)
    tp = [i for i in range(1, len(P) - 1) if (P[i] > P[i-1] and P[i] > P[i+1]) or (P[i] < P[i-1] and P[i] < P[i+1])]
    return dict(GAP=g, S=None if g is None else 1 + g / math.pi,
                LOCK=float(onb[tp].mean() - onb.mean()) if len(tp) >= 4 else None)
