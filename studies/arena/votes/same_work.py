import re, collections, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, binomtest, spearmanr
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
F = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "spotify_track_duration_ms"]
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity"]); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); S = S.sort_values("spotify_track_popularity", ascending=False).drop_duplicates(["t", "a"])
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int); d = B.sort_values("peak").drop_duplicates(["t", "a"]).merge(S[["t", "a", "spotify_track_popularity"] + F], on=["t", "a"]).sort_values("year").reset_index(drop=True)
yr = d.year.values; pp = d.spotify_track_popularity.values; d["love"] = [float((pp[np.abs(yr - y) <= 3] < p).mean()) for y, p in zip(yr, pp)]
C = np.c_[np.ones(len(d)), rankdata(d.year), rankdata(d.peak)]; d["lr"] = rankdata(d.love) - C @ np.linalg.lstsq(C, rankdata(d.love), rcond=None)[0]; d["lr"] /= d.lr.std()
am = d.groupby("a").lr.agg(["sum", "count"]); d["art"] = [(am.loc[a, "sum"] - v) / (am.loc[a, "count"] - 1) if am.loc[a, "count"] > 1 else np.nan for a, v in zip(d.a, d.lr)]
Z = d[F].copy(); u = np.zeros(len(d))
for i in range(len(d)):
    pass
# unlike its years: mean |z| of Spotify's readings against hits within two years (as the locked candidate)
X = d[F].values.astype(float); un = np.full(len(d), np.nan)
for y in np.unique(yr):
    m = np.abs(yr - y) <= 2; mu, sd = np.nanmean(X[m], 0), np.nanstd(X[m], 0) + 1e-9; k = yr == y; un[k] = np.nanmean(np.abs((X[k] - mu) / sd), 1)
d["unlike"] = un
W = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 4: w = W[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
byT = collections.defaultdict(list)
for k, w in W.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: byT[t].append(k)
def work(t, a):
    c = [k for k in byT.get(t, []) if len(a) >= 3 and any(a == q or (len(q) >= 5 and (a in q or q in a)) for q in W[k]["perf"])]; return max(c, key=lambda k: W[k]["n"]) if c else None
d["work"] = [work(t, a) for t, a in zip(d.t, d.a)]
def icc(x, g):
    x = np.asarray(x, float); g = pd.Categorical(g).codes; n = np.bincount(g); a = len(n); N = len(x); mean = np.bincount(g, x) / n; msb = (n * (mean - x.mean()) ** 2).sum() / (a - 1); msw = ((x - mean[g]) ** 2).sum() / (N - a); k0 = (N - (n ** 2).sum() / N) / (a - 1); return float((msb - msw) / (msb + (k0 - 1) * msw))
def report(sub, col, label, rng=np.random.default_rng(0)):
    sub = sub.dropna(subset=[col]); k = sub.groupby("grp")[col].transform("size"); sub = sub[k >= 2]; v = icc(sub[col], sub.grp); gs = sub.grp.unique(); idx = {g: np.where(sub.grp.values == g)[0] for g in gs}; boot = []
    for _ in range(1000):
        pick = rng.choice(gs, len(gs)); ii = np.concatenate([idx[g] for g in pick]); gg = np.concatenate([[j] * len(idx[g]) for j, g in enumerate(pick)]); boot.append(icc(sub[col].values[ii], gg))
    null = [icc(sub[col].values, rng.permutation(sub.grp.values)) for _ in range(1000)]
    print(f"{label:58} works {len(gs):4d} recordings {len(sub):4d}  ICC {v:+.3f}  95% [{np.percentile(boot, 2.5):+.3f}, {np.percentile(boot, 97.5):+.3f}]  shuffle 95th {np.percentile(null, 95):+.3f}  ceiling for a page reader {np.sqrt(max(v, 0)):.2f}"); return v
x = d[d.work.notna()].copy(); x["grp"] = x.work; x = x[x.groupby("grp").a.transform("nunique") >= 2]; out = {}
out["love"] = report(x, "lr", "Q1 love, same work, different performers")
C2 = np.c_[np.ones(len(x)), x.art.fillna(0).values, x.art.isna().values.astype(float)]; x["lr2"] = x.lr.values - C2 @ np.linalg.lstsq(C2, x.lr.values, rcond=None)[0]; out["love_artist_held"] = report(x, "lr2", "   with the performer's own standing held")
x60 = x[x.groupby("grp").year.transform("max") - x.groupby("grp").year.transform("min") <= 3]; out["love_same_years"] = report(x60, "lr", "   versions within three years of each other only") if x60.grp.nunique() > 20 else None
y = d[d.work.isna()].copy(); y["grp"] = y.t; y = y[y.groupby("grp").a.transform("nunique") >= 2]; out["title_only"] = report(y, "lr", "control: same title, not a known shared work")
z = d.copy(); z["grp"] = z.a; out["artist"] = report(z, "lr", "for scale: same performer, different songs")
# Q2: within a work, pairs
print("\nQ2 within a work: does the version with MORE of the reading have more love now? (all pairs)")
for col, pred in (("unlike", "+"), ("valence", "-"), ("danceability", "-"), ("acousticness", "?"), ("energy", "?"), ("year", "?"), ("peak", "?")):
    win = tot = 0; dl = []; dv = []
    for g, s in x.groupby("grp"):
        s = s.dropna(subset=[col]).sort_values("year"); r = s[[col, "lr"]].values
        for i in range(len(r)):
            for j in range(i + 1, len(r)):
                if r[i][0] != r[j][0] and r[i][1] != r[j][1]: tot += 1; win += (r[i][0] > r[j][0]) == (r[i][1] > r[j][1]); dv.append(r[i][0] - r[j][0]); dl.append(r[i][1] - r[j][1])
    bt = binomtest(win, tot); out["pair_" + col] = (win / tot, tot, bt.pvalue); print(f"   {col:14} predicted {pred}  agree {win / tot:.3f} of {tot} pairs  p {bt.pvalue:.4f}  rho of differences {spearmanr(dv, dl)[0]:+.3f}")
json.dump({k: v for k, v in out.items()}, open("same_work_results.json", "w"), indent=1, default=float); x.to_pickle("same_work.pkl")
