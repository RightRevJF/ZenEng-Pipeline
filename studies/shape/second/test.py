import pickle, re, collections, hashlib, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
x = pickle.load(open("fresh.pkl", "rb"))
W = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 4: w = W[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
byT = collections.defaultdict(list)
for k, w in W.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: byT[t].append(k)
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx")[["Performer", "Song", "spotify_track_popularity"]].dropna(); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm)
pop = S.groupby(["t", "a"]).spotify_track_popularity.max().to_dict()
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int); B["pop"] = [pop.get((t, a)) for t, a in zip(B.t, B.a)]; PY = B.dropna(subset=["pop"])
x["pop"] = [pop.get((t, a)) for t, a in zip(x.title, x.artist)]; x = x.dropna(subset=["pop"]).copy()
x["love"] = [float((PY[(PY.year - y).abs() <= 3]["pop"].values < p).mean()) for p, y in zip(x["pop"], x.year)]
x["cov0"] = [max((W[k]["n"] for k in byT.get(t, []) if any(a in p or (len(p) >= 4 and p in a) for p in W[k]["perf"])), default=0) for t, a in zip(x.title, x.artist)]
yr = x.year.values; x["cover_rank"] = [float((x.cov0.values[np.abs(yr - y) <= 5] < c).mean() + .5 * (x.cov0.values[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, x.cov0)]
x["G"] = (x.love + x.cover_rank) / 2; x["half"] = [int(hashlib.md5(t.encode()).hexdigest(), 16) % 2 for t in x.title]; pickle.dump(x, open("fresh_graded.pkl", "wb"))
def partial(d, m, y, peak=False):
    d = d.dropna(subset=[m, y]); C = np.c_[tuple([np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([rankdata(d.peak)] if peak else []))]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(d[m])), res(rankdata(d[y]))); return round(float(r), 3), round(float(p), 4), len(d)
print("songs", len(x), "covered", int((x.cov0 > 0).sum()), "halves", x.half.value_counts().to_dict(), "| G vs peak", partial(x, "peak", "G")); out = {}
for m, s in dict(M7=1, M7r=1, M3=1, M4=-1).items():
    a, b, p = partial(x[x.half == 0], m, "G"), partial(x[x.half == 1], m, "G"), partial(x, m, "G"); ok = all(np.sign(v[0]) == s for v in (a, b, p)) and a[1] < .05 and b[1] < .05 and p[1] < .0125
    out[m] = dict(pred=s, A=a, B=b, pooled=p, with_peak=partial(x, m, "G", True), strict=partial(x[x.loose == 0], m, "G"), love=partial(x, m, "love"), covers=partial(x, m, "cover_rank"), verdict="PASS" if ok else "fail"); print(m, out[m])
print("M7 z median", round(x.M7.median(), 2), "share above 2:", round((x.M7 > 2).mean(), 3)); json.dump(out, open("fresh_results.json", "w"), indent=1)
