"""Where does the signal live? Spotify's own readings of the recording (not the notes) against G, every Hot 100 song of 2005 or earlier with love known. After the fact; halves by title hash."""
import re, collections, hashlib, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
F = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "spotify_track_duration_ms", "mode"]
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity"] + F); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); S = S.sort_values("spotify_track_popularity", ascending=False).drop_duplicates(["t", "a"])
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int); d = B.merge(S, on=["t", "a"]).drop_duplicates(["t", "a"]); d = d.sort_values("year").reset_index(drop=True)
yr = d.year.values; pp = d.spotify_track_popularity.values; d["love"] = [float((pp[np.abs(yr - y) <= 3] < p).mean()) for y, p in zip(yr, pp)]
W = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 4: w = W[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
byT = collections.defaultdict(list)
for k, w in W.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: byT[t].append(k)
d["cov0"] = [max((W[k]["n"] for k in byT.get(t, []) if any(a in q or (len(q) >= 4 and q in a) for q in W[k]["perf"])), default=0) for t, a in zip(d.t, d.a)]; d = d[d.year <= 2005].reset_index(drop=True); yr = d.year.values; cv = d.cov0.values
d["cover_rank"] = [float((cv[np.abs(yr - y) <= 5] < c).mean() + .5 * (cv[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, cv)]; d["G"] = (d.love + d.cover_rank) / 2; d["half"] = [int(hashlib.md5(t.encode()).hexdigest(), 16) % 2 for t in d.t]
def part(x, m, g):
    C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.peak)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(x[m])), res(rankdata(x[g]))); return round(float(r), 3)
print("songs", len(d), "covered", int((d.cov0 > 0).sum())); out = {}
for m in F: out[m] = dict(A=part(d[d.half == 0], m, "G"), B=part(d[d.half == 1], m, "G"), all=part(d, m, "G"), love=part(d, m, "love"), covers=part(d, m, "cover_rank")); print(f"{m:28}", out[m])
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
a, b = d[d.half == 0], d[d.half == 1]; sc = StandardScaler().fit(a[F]); pr = RidgeCV().fit(sc.transform(a[F]), a.G).predict(sc.transform(b[F])); b = b.assign(pr=pr); print("all eleven together, fitted on half A, judged on half B:", part(b, "pr", "G"), "love", part(b, "pr", "love"), "covers", part(b, "pr", "cover_rank")); json.dump(out, open("sound_results.json", "w"), indent=1)
