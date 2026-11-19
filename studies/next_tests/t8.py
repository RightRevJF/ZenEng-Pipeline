import json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
src = open("/home/claude/zeneng/corpus/v34/sound.py").read().split("def part")[0].replace('d = d[d.year <= 2005].reset_index(drop=True); yr = d.year.values; cv = d.cov0.values', 'ALL = d.copy(); d = d[d.year <= 2005].reset_index(drop=True); yr = d.year.values; cv = d.cov0.values'); exec(src)
R = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "spotify_track_duration_ms"]; X = ALL[R].values.astype(float); ya = ALL.year.values; Xd = d[R].values.astype(float); un = np.full(len(d), np.nan); fu = np.full(len(d), np.nan); pa = np.full(len(d), np.nan)
for y in np.unique(d.year):
    k = d.year.values == y; m = np.abs(ya - y) <= 2; mu, sd = X[m].mean(0), X[m].std(0) + 1e-9; own = np.abs((Xd[k] - mu) / sd).mean(1); un[k] = own
    for arr, lo, hi in ((fu, 10, 20), (pa, -20, -10)):
        m2 = (ya >= y + lo) & (ya <= y + hi)
        if m2.sum() >= 300: mu2, sd2 = X[m2].mean(0), X[m2].std(0) + 1e-9; arr[k] = own - np.abs((Xd[k] - mu2) / sd2).mean(1)
d["unlike"] = un; d["future"] = fu; d["past"] = pa
def part(x, c, tg, hold):
    x = x.dropna(subset=[c]); C = np.c_[tuple([np.ones(len(x)), rankdata(x.year), rankdata(x.peak)] + [rankdata(x[h]) for h in hold])]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(x[c])), res(rankdata(x[tg]))); return round(float(r), 3), float(p), len(x)
H = ["tempo", "energy", "loudness", "acousticness"]; out = {}
out["valence alone"] = part(d, "valence", "G", []); out["unlike alone"] = part(d, "unlike", "G", []); out["valence | unlike + tempo, energy, loudness, acousticness"] = part(d, "valence", "G", H + ["unlike"]); out["unlike | valence + the same"] = part(d, "unlike", "G", H + ["valence"])
out["sounded like the future (10-20 years on)"] = part(d, "future", "G", []); out["   with unlike and valence held"] = part(d, "future", "G", ["unlike", "valence"]); out["sounded like the past (10-20 years before)"] = part(d, "past", "G", []); out["   with unlike and valence held "] = part(d, "past", "G", ["unlike", "valence"])
for k, v in out.items(): print(f"{k:58} {v[0]:+.3f}  (p {v[1]:.1g}, n {v[2]})")
for tg in ("love", "cover_rank"): print(f"   future against {tg}: {part(d, 'future', tg, ['unlike', 'valence'])[0]:+.3f}   past against {tg}: {part(d, 'past', tg, ['unlike', 'valence'])[0]:+.3f}")
x = d.dropna(subset=["unlike"]); q = pd.qcut(x.unlike, 10, labels=False); print("mean G by tenth of unlikeness:", x.groupby(q).G.mean().round(3).tolist()); json.dump({k: list(v) for k, v in out.items()}, open("t8_results.json", "w"), indent=1)
