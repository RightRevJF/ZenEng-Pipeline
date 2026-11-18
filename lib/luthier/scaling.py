"""Luthier, fix 867: the same order at every scale. Detrended fluctuation analysis (first order) of a song's pitch series (one value a note) and of its onsets on
a sixteenth-note grid; scales from 4 to a quarter of the series. Kept pop songs: pitch alpha 0.79 / 0.90 / 1.00 (shuffled 0.53); onsets 0.61 / 0.66 / 0.72 (shuffled 0.51).
Needs 64 values or more."""
import numpy as np
def dfa(x, order=1, smin=4, nscales=14):
    x = np.asarray(x, float); n = len(x)
    if n < 64 or np.std(x) == 0: return None
    y = np.cumsum(x - x.mean()); smax = n // 4; S = np.unique(np.round(np.logspace(np.log10(smin), np.log10(smax), nscales)).astype(int)); F = []
    for s in S:
        m = n // s; segs = np.concatenate([y[:m * s].reshape(m, s), y[n - m * s:].reshape(m, s)]); t = np.arange(s); f2 = []
        for seg in segs: c = np.polyfit(t, seg, order); f2.append(np.mean((seg - np.polyval(c, t)) ** 2))
        F.append(np.sqrt(np.mean(f2)))
    S = S.astype(float); F = np.array(F); ok = F > 0
    if ok.sum() < 5: return None
    ls, lf = np.log(S[ok]), np.log(F[ok]); a = np.polyfit(ls, lf, 1)[0]; half = len(ls) // 2
    return dict(alpha=float(a), short=float(np.polyfit(ls[:half + 1], lf[:half + 1], 1)[0]), long=float(np.polyfit(ls[half:], lf[half:], 1)[0]), n=n)
def series(notes):
    """notes: [(onset twelfths, pitch, ...)]"""
    t = np.array([x[0] for x in notes]); p = np.array([x[1] for x in notes], float); ioi = np.diff(t).astype(float); ioi = np.minimum(ioi, 96)
    g0 = t.min() // 3; grid = np.zeros(int(t.max() // 3 - g0 + 1)); grid[(t // 3 - g0).astype(int)] = 1
    return {"pitch": p, "time between onsets": ioi, "onsets on the grid": grid}
