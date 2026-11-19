"""Helpers for the gate-strengthening round. import sys; sys.path.insert(0, '/home/claude/arena2'); import arena2"""
import pickle, hashlib, numpy as np, pandas as pd
from scipy.stats import rankdata, pearsonr
A = "/home/claude/arena2/"; A1 = "/home/claude/arena/"
def session(): return pickle.load(open(A + "session_open.pkl", "rb"))     # list of dicts (see README)
def hymns(): return pd.read_pickle(A + "hymn_open.pkl")
def gate(): return pickle.load(open(A + "gate_open.pkl", "rb"))
def sound(): return pd.read_pickle(A1 + "sound_open.pkl")
def hot100(): return pd.read_pickle(A1 + "hot100_open.pkl")
def _res(C, u): return u - C @ np.linalg.lstsq(C, u, rcond=None)[0]
def score_session(values, tunes):
    """partial rank correlation of values with Gs holding tune type, mode family, length and submission order (tune_id)."""
    d = pd.DataFrame(dict(v=np.asarray(values, float), Gs=[t["Gs"] for t in tunes], n=[t["n"] for t in tunes], tid=[t["tune_id"] for t in tunes], ty=[t["type"] for t in tunes], md=[t["mode_family"] for t in tunes])); d["v"] = d.v.fillna(d.v.median())
    C = np.c_[np.ones(len(d)), pd.get_dummies(d.ty).values[:, 1:].astype(float), pd.get_dummies(d.md).values[:, 1:].astype(float), rankdata(d.n), rankdata(d.tid)]; r, p = pearsonr(_res(C, rankdata(d.v)), _res(C, rankdata(d.Gs))); return float(r), float(p), len(d)
def score_hymns(values, H):
    """partial rank correlation with log hymnal count holding metre class, major/minor and incipit length."""
    v = pd.Series(np.asarray(values, float)).fillna(np.nanmedian(values)).values; C = np.c_[np.ones(len(H)), pd.get_dummies(H.meter).values[:, 1:].astype(float), H.minor.values.astype(float), rankdata(H.length)]; r, p = pearsonr(_res(C, rankdata(v)), _res(C, rankdata(H.y))); return float(r), float(p), len(H)
def score_gate(values, songs, source):
    """within-artist partial correlation of values with 'charted' (artist and note count held), one source ('lakh' or 'hooktheory')."""
    m = pd.DataFrame(dict(v=np.asarray(values, float), artist=[s["artist"] for s in songs], charted=[float(s["charted"]) for s in songs], n=[len(s["notes"]) for s in songs], src=[s["source"] for s in songs])); m = m[m.src == source]; m["v"] = m.v.fillna(m.v.median()); g = m.groupby("artist").charted; m = m[(g.transform("min") == 0) & (g.transform("max") == 1)]
    a = pd.Categorical(m.artist).codes; X = np.c_[rankdata(m.v), m.charted.values, rankdata(m.n)]; X = X - pd.DataFrame(X).groupby(a).transform("mean").values; x, y = _res(X[:, 2:], X[:, 0]), _res(X[:, 2:], X[:, 1]); return float(np.corrcoef(x, y)[0, 1]), len(m), int(m.artist.nunique())
def score_sound(values, D, target="G"):
    """per store partial rank correlation with the yardstick, year and chart peak held. D = sound() or hot100() (hot100 has one 'store')."""
    D = D.copy(); D["v"] = np.asarray(values, float); D["v"] = D.v.fillna(D.v.median()); out = {}
    for st in (D.store.unique() if "store" in D else ["hot100"]):
        x = D[D.store == st] if "store" in D else D; C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.peak)]; r, p = pearsonr(_res(C, rankdata(x.v)), _res(C, rankdata(x[target]))); out[st] = (float(r), float(p), len(x))
    return out
