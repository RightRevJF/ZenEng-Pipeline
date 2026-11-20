"""Helpers for the greatness arena. Import with: import sys; sys.path.insert(0, '/home/claude/arena'); import arena"""
import pickle, numpy as np, pandas as pd
from scipy.stats import rankdata, pearsonr
A = "/home/claude/arena/"
def tunes(): return pickle.load(open(A + "tunes_open.pkl", "rb"))          # list of dicts, see README
def sound(): return pd.read_pickle(A + "sound_open.pkl")                    # one row per recording, 127 sound numbers + G
def hot100(): return pd.read_pickle(A + "hot100_open.pkl")                  # every Hot 100 song <= 2005: title, artist, Spotify readings, G
def partial(values, target, controls):
    """partial Spearman of values with target holding the control columns (lists/arrays). returns (rho, p, n)"""
    v = np.asarray(values, float); y = np.asarray(target, float); C = [np.asarray(c, float) for c in controls]; ok = np.isfinite(v) & np.isfinite(y)
    for c in C: ok &= np.isfinite(c)
    X = np.c_[tuple([np.ones(ok.sum())] + [rankdata(c[ok]) for c in C])]; res = lambda u: u - X @ np.linalg.lstsq(X, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v[ok])), res(rankdata(y[ok]))); return float(r), float(p), int(ok.sum())
def score_tunes(fn, songs=None, target="G_rank"):
    """fn(song dict) -> float. Scores per set (1, 2, 3), holding year and note count. Use this to explore on the OPEN half."""
    songs = songs or tunes(); out = {}
    for st in (1, 2, 3):
        S = [s for s in songs if s["set"] == st]; v = []
        for s in S:
            try: v.append(float(fn(s)))
            except Exception: v.append(np.nan)
        out[st] = partial(v, [s[target] for s in S], [[s["year"] for s in S], [sum(len(c) for c in s["clips"]) for s in S]])
    return out
