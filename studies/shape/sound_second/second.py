import pickle, re, collections, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy.stats import rankdata, pearsonr
from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
M = pd.read_pickle("/home/claude/zeneng/corpus/v36/sound2_meta.pkl"); GM = np.load("/home/claude/zeneng/corpus/v36/genre.npy")
R = pd.DataFrame(pickle.load(open("pulled.pkl", "rb"))).merge(pd.read_csv("/tmp/claude-0/hsp/msd_bb_matches.csv")[["msd_id", "artist", "title"]], on="msd_id"); R["t"] = R.title.map(norm); R["a"] = R.artist.map(norm)
S = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx").dropna(subset=["spotify_track_popularity"]); S["t"] = S.Song.map(norm); S["a"] = S.Performer.map(norm); pop = S.groupby(["t", "a"]).spotify_track_popularity.max().to_dict(); gen = S.dropna(subset=["spotify_genre"]).groupby(["t", "a"]).spotify_genre.first().to_dict()
B = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); B["t"] = B.title.map(norm); B["a"] = B.performer.map(norm); B["year"] = B["first"].str[:4].astype(int); B["pop"] = [pop.get(k) for k in zip(B.t, B.a)]; PY = B.dropna(subset=["pop"])
d = R.merge(B.sort_values("peak").drop_duplicates(["t", "a"])[["t", "a", "year", "peak", "pop"]], on=["t", "a"]).dropna(subset=["pop"]); d = d[(d.year <= 2005) & ~d.t.isin(set(M.t))].drop_duplicates(["t", "a"]).reset_index(drop=True)
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
d["cover_rank"] = [float((cv[np.abs(yr - y) <= 5] < c).mean() + .5 * (cv[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, cv)]; d["G"] = (d.love + d.cover_rank) / 2
FAM = dict(rock=r"rock|metal|punk|grunge", soul=r"soul|motown|r&b|funk|disco|quiet storm", country=r"country|nashville", hiphop=r"hip hop|rap", folk=r"folk|singer-songwriter", standards=r"adult standards|easy listening|lounge|vocal jazz|brill", dance=r"dance|new wave|synth|europop")
Gd = np.c_[np.array([[float(bool(re.search(p, str(gen.get((t, a), ""))))) for p in FAM.values()] for t, a in zip(d.t, d.a)]), np.array([[float(y // 10 == k) for k in (196, 197, 198, 199, 200)] for y in d.year])]
skip = {"sid", "t", "a", "year", "peak", "pop", "love", "cov0", "cover_rank", "G", "h", "fyear", "bitrate", "gain", "lossless", "codec", "length", "lag"}
F = [c for c in M.columns if c not in skip and c in d.columns and M[c].dtype != object and M[c].notna().mean() > .95 and d[c].notna().mean() > .95 and M[c].std() > 0 and d[c].std() > 0]
z = lambda x: StandardScaler().fit_transform(x[F].fillna(x[F].median()).values); pr = RidgeCV(alphas=np.logspace(0, 5, 16)).fit(z(M), M.G.values).predict(z(d))
def part(x, v, g, extra=None):
    C = np.c_[np.ones(len(x)), rankdata(x.year), rankdata(x.peak)]
    if extra is not None: C = np.c_[C, extra]
    res = lambda u: u - C @ np.linalg.lstsq(C, u, rcond=None)[0]; r, p = pearsonr(res(rankdata(v)), res(rankdata(x[g]))); return round(float(r), 3), round(float(p), 5)
print("second store: songs", len(d), "| covered", int((d.cov0 > 0).sum()), "| features shared", len(F), "| years", int(d.year.min()), "-", int(d.year.max())); out = {}
out["F1 frozen reader"] = dict(G=part(d, pr, "G"), genre_decade_held=part(d, pr, "G", Gd), love=part(d, pr, "love"), covers=part(d, pr, "cover_rank"), to_1991_only=part(d[d.year <= 1991], pr[(d.year <= 1991).values], "G")); print("F1", out["F1 frozen reader"])
for m, s in (("spectral_energyband_low.mean", 1), ("barkbands_skewness.mean", 1), ("barkbands_kurtosis.mean", 1), ("spectral_energy.var", 1), ("beats_loudness.var", 1), ("silence_rate_30dB.mean", -1)):
    a = part(d, d[m].values, "G"); ok = np.sign(a[0]) == s and a[1] < .0083; out[m] = dict(pred=s, G=a, genre_decade_held=part(d, d[m].values, "G", Gd), love=part(d, d[m].values, "love"), covers=part(d, d[m].values, "cover_rank"), mcgill=part(M, M[m].values, "G"), mcgill_genre_decade_held=part(M, M[m].values, "G", GM), verdict="PASS" if ok else "fail"); print(f"{m:30}", out[m])
json.dump(out, open("second_results.json", "w"), indent=1); d.to_pickle("second.pkl")
