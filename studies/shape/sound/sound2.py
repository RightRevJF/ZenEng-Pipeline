import json, re, glob, os, hashlib, collections, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
root = "/home/claude/corpus/mcgill/"; rows = []
for f in glob.glob(root + "billboard-2.0-acousticbrainz/*/acousticbrainz.json"):
    sid = f.split("/")[-2]; m = {}
    try:
        for line in open(root + f"billboard-2.0-salami_chords/{sid}/salami_chords.txt", errors="ignore").read().splitlines()[:6]:
            mm = re.match(r"# (\w+): (.*)", line)
            if mm: m[mm.group(1)] = mm.group(2).strip()
    except Exception: continue
    d = json.load(open(f)); r = dict(sid=sid, t=norm(m.get("title")), a=norm(m.get("artist")))
    for sec in ("lowlevel", "rhythm", "tonal"):
        for k, v in d[sec].items():
            if isinstance(v, (int, float)): r[f"{k}"] = float(v)
            elif isinstance(v, dict) and "mean" in v:
                if isinstance(v["mean"], (int, float)): r[f"{k}.mean"] = float(v["mean"]); r[f"{k}.var"] = float(np.log(v["var"] + 1e-12)) if isinstance(v.get("var"), (int, float)) else np.nan
                elif k in ("mfcc", "spectral_contrast_coeffs", "spectral_contrast_valleys"):
                    for i, x in enumerate(v["mean"]): r[f"{k}{i}"] = float(x)
            elif k in ("key_scale", "chords_scale"): r[k + "_minor"] = float(v == "minor")
    rows.append(r)
D = pd.DataFrame(rows).drop(columns=["beats_count"], errors="ignore")
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity"]); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); pop = S.groupby(["t", "a"]).spotify_track_popularity.max().to_dict()
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int); B["pop"] = [pop.get(k) for k in zip(B.t, B.a)]; PY = B.dropna(subset=["pop"])
d = D.merge(B.sort_values("peak").drop_duplicates(["t", "a"])[["t", "a", "year", "peak", "pop"]], on=["t", "a"]).dropna(subset=["pop"]).drop_duplicates(["t", "a"]).reset_index(drop=True)
d["love"] = [float((PY[(PY.year - y).abs() <= 3]["pop"].values < p).mean()) for p, y in zip(d["pop"], d.year)]
W = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 4: w = W[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
byT = collections.defaultdict(list)
for k, w in W.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: byT[t].append(k)
d["cov0"] = [max((W[k]["n"] for k in byT.get(t, []) if any(a in q or (len(q) >= 4 and q in a) for q in W[k]["perf"])), default=0) for t, a in zip(d.t, d.a)]; yr = d.year.values; cv = d.cov0.values
d["cover_rank"] = [float((cv[np.abs(yr - y) <= 5] < c).mean() + .5 * (cv[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, cv)]; d["G"] = (d.love + d.cover_rank) / 2; d["h"] = [int(hashlib.md5(a.encode()).hexdigest(), 16) % 2 for a in d.a]
F = [c for c in D.columns if c not in ("sid", "t", "a") and d[c].notna().mean() > .95 and d[c].std() > 0]; X = d[F].fillna(d[F].median()).values
def part(x, v, g):
    C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.peak)]; res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[g]))); return round(float(r), 3), round(float(p), 4)
print("songs", len(d), "features", len(F), "halves", d.h.value_counts().to_dict(), "covered", int((d.cov0 > 0).sum())); pr = np.zeros(len(d))
for hh in (0, 1):
    a, b = (d.h != hh).values, (d.h == hh).values; sc = StandardScaler().fit(X[a]); pr[b] = RidgeCV(alphas=np.logspace(0, 5, 16)).fit(sc.transform(X[a]), d.G.values[a]).predict(sc.transform(X[b]))
out = {"A1 all sound numbers, out of fold": dict(G=part(d, pr, "G"), half0=part(d[d.h == 0], pr[(d.h == 0).values], "G"), half1=part(d[d.h == 1], pr[(d.h == 1).values], "G"), love=part(d, pr, "love"), covers=part(d, pr, "cover_rank")), "A2 danceability": dict(G=part(d, d.danceability.values, "G"), love=part(d, d.danceability.values, "love"), covers=part(d, d.danceability.values, "cover_rank"))}
for k, v in out.items(): print(k, v)
L = []
for c in F:
    a, b, p = part(d[d.h == 0], d[c][d.h == 0].values, "G"), part(d[d.h == 1], d[c][d.h == 1].values, "G"), part(d, d[c].values, "G")
    if np.sign(a[0]) == np.sign(b[0]): L.append((c, a[0], b[0], p[0], p[1]))
L.sort(key=lambda x: -abs(x[3])); print("leads (same sign in both halves), strongest first; chance alone at p<.01 would give about", round(len(F) * .01, 1))
for x in L[:14]: print("  ", x)
out["leads"] = L[:14]; json.dump(out, open("sound2_results.json", "w"), indent=1); d.to_pickle("sound2.pkl")
