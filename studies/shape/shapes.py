import pickle, sys, hashlib, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import spearmanr, rankdata
from scipy.spatial.distance import pdist
from ripser import ripser
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); Y = pickle.load(open("yardstick.pkl", "rb"))
MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88]); MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
def tonic(ns):
    t = np.array([n[0] for n in ns]); p = np.array([n[1] for n in ns]); d = np.clip(np.diff(t, append=t[-1] + 1), .25, 4); h = np.bincount(p % 12, d, 12)
    return max(((np.corrcoef(np.roll(P, k), h)[0, 1], k) for P in (MAJ, MIN) for k in range(12)))[1]
def path(ns):
    t = np.array([n[0] for n in ns], float); p = np.array([n[1] for n in ns], float); k = tonic(ns); a = 2 * np.pi * (((p - k) * 7) % 12) / 12; b = 2 * np.pi * (t % 4) / 4
    d = np.log2(np.clip(np.diff(t, append=t[-1] + 1), .125, 8))
    return np.c_[np.cos(a), np.sin(a), (p - np.median(p)) / 12 * 2, np.cos(b), np.sin(b), d / 2]
def windows(clips, w=8):
    return np.vstack([np.lib.stride_tricks.sliding_window_view(P, w, axis=0).reshape(len(P) - w + 1, -1) for P in clips if len(P) >= w])
R = 2.0   # fixed radius, set below from the pooled distances of a sample, before any grade is read
def measures(clips):
    Ps = [path(c) for c in clips if len(c) >= 8]; Wd = windows(Ps)
    if len(Wd) > 400: Wd_s = Wd[np.linspace(0, len(Wd) - 1, 400).astype(int)]
    else: Wd_s = Wd
    D = pdist(Wd_s); near = D < R; m1 = near.mean(); m2 = (D[near] > 1e-9).mean() if near.any() else np.nan
    ang = []
    for P in Ps:
        v = np.diff(P, axis=0); n = np.linalg.norm(v, axis=1); ok = (n[:-1] > 0) & (n[1:] > 0); c = (v[:-1] * v[1:]).sum(1)[ok] / (n[:-1] * n[1:])[ok]; ang += list(np.arccos(np.clip(c, -1, 1)))
    m3 = np.mean(ang); lags = [1, 2, 4, 8, 16]; msd = []
    for L in lags:
        s = [((P[L:] - P[:-L]) ** 2).sum(1) for P in Ps if len(P) > L + 4]; msd.append(np.mean(np.concatenate(s)) if s else np.nan)
    m4 = np.polyfit(np.log(lags), np.log(msd), 1)[0] / 2 if np.all(np.isfinite(msd)) else np.nan
    ev = np.linalg.eigvalsh(np.cov(Wd.T)); ev = ev[ev > 0]; m5 = ev.sum() ** 2 / (ev ** 2).sum()
    X = Wd_s[np.linspace(0, len(Wd_s) - 1, min(len(Wd_s), 200)).astype(int)]; X = np.unique(X, axis=0)
    h1 = ripser(X, maxdim=1)["dgms"][1]; m6 = (h1[:, 1] - h1[:, 0]).sum() / pdist(X).max() if len(h1) else 0.0
    return dict(M1=m1, M2=m2, M3=m3, M4=m4, M5=m5, M6=m6)
if __name__ == "__main__":
    x = Y[(Y.year <= 2005) & Y.love.notna() & (Y.notes >= 48)]; x = x.assign(p=x.src.map({"CB": 0, "RS": 1, "BM": 2, "HT": 3})).sort_values("p", kind="mergesort").drop_duplicates("title").copy()
    x["cov0"] = x.covers.fillna(0); yr = x.year.values; x["cover_rank"] = [float((x.cov0.values[np.abs(yr - y) <= 5] < c).mean() + .5 * (x.cov0.values[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, x.cov0)]
    x["G"] = (x.love + x.cover_rank) / 2; byid = {(s["src"], s["id"]): s for s in G}
    rng = np.random.default_rng(0); samp = [byid[(r.src, r.id)]["clips"] for r in x.sample(150, random_state=0).itertuples()]
    pool = np.concatenate([pdist(windows([path(c) for c in cl if len(c) >= 8])[::3]) for cl in samp]); R = float(np.percentile(pool, 10)); print("radius", R)
    rows = []
    for r in x.itertuples():
        try: rows.append(dict(src=r.src, id=r.id, **measures(byid[(r.src, r.id)]["clips"])))
        except Exception as e: print("skip", r.id, e)
    x = x.merge(pd.DataFrame(rows), on=["src", "id"]); x["half"] = [int(hashlib.md5(t.encode()).hexdigest(), 16) % 2 for t in x.title]; pickle.dump(x, open("shapes.pkl", "wb")); print(len(x), x.half.value_counts().to_dict())
