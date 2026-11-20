import sys, os, json, pickle, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v30"); S = Bd.S
from sklearn.cluster import MiniBatchKMeans; from sklearn.neural_network import MLPRegressor; from sklearn.linear_model import RidgeCV; from sklearn.preprocessing import StandardScaler; from sklearn.model_selection import KFold
from scipy.stats import rankdata, pearsonr
rng = np.random.default_rng(0); W = 8
def pts(t, p, tr=None):
    P = S.path(list(zip(t, p)))[:, [0, 1, 2, 5]]
    if tr is not None: P = np.c_[P, [(.0, .4, 1.)[x] if x is not None else .5 for x in tr]]
    return P
def wins(P): return np.lib.stride_tricks.sliding_window_view(P, W, axis=0).reshape(len(P) - W + 1, -1) if len(P) >= W else np.zeros((0, P.shape[1] * W))
# ---- songs
G = pickle.load(open("/home/claude/zeneng/corpus/v23/graded.pkl", "rb")); byid = {(s["src"], s["id"]): s for s in G}
s1 = pickle.load(open("/home/claude/zeneng/corpus/v25/shapes.pkl", "rb")); s2 = pickle.load(open("/home/claude/zeneng/corpus/v26/fresh_graded.pkl", "rb"))
def w_clips(clips): return np.vstack([wins(pts([n[0] for n in c], [n[1] for n in c])) for c in clips if len(c) >= W])
X1 = [w_clips(byid[(r.src, r.id)]["clips"]) for r in s1.itertuples()]
X2 = []; X2w = []
for r in s2.itertuples():
    t, p, tr, lines = Bd.read(Bd.D + "syllable_level_npy_39/" + r.file); X2.append(wins(pts(t, p))); X2w.append(wins(pts(t, p, tr)))
used = set(s1.title) | set(s2.title)
pool = [w_clips(s["clips"]) for s in G if s["src"] == "HT" and s["title"] not in used and sum(len(c) for c in s["clips"]) >= 24]; pool = np.vstack(pool); pool = pool[rng.choice(len(pool), min(len(pool), 150000), replace=False)]
files = [f for f in sorted(os.listdir(Bd.D + "syllable_level_npy_39")) if f not in set(s2.file)]; files = [files[i] for i in rng.choice(len(files), 1500, replace=False)]; poolw = []
for f in files:
    try:
        t, p, tr, lines = Bd.read(Bd.D + "syllable_level_npy_39/" + f)
        if len(p) >= 40 and len(set(p.tolist())) >= 4: poolw.append(wins(pts(t, p, tr)))
    except Exception: pass
poolw = np.vstack(poolw); poolw = poolw[rng.choice(len(poolw), min(len(poolw), 150000), replace=False)]; print("unlabelled windows", len(pool), len(poolw), flush=True)
# ---- spaces, learned without grades
def codebook(P, K=64, seed=0):
    km = MiniBatchKMeans(K, random_state=seed, n_init=3, batch_size=4096).fit(P); return lambda X: np.sqrt(np.bincount(km.predict(X), minlength=K) / len(X))
def autoenc(P):
    sc = StandardScaler().fit(P); Z = sc.transform(P); ae = MLPRegressor(hidden_layer_sizes=(64, 16, 64), activation="tanh", max_iter=60, random_state=0, early_stopping=True).fit(Z, Z)
    def code(X):
        h = sc.transform(X)
        for i in range(2): h = np.tanh(h @ ae.coefs_[i] + ae.intercepts_[i])
        return np.r_[h.mean(0), h.std(0), np.linalg.norm(np.diff(h, axis=0), axis=1).mean()]
    return code

def reader(Xa, ya, Xb):
    sc = StandardScaler().fit(Xa); return RidgeCV(alphas=np.logspace(0, 4, 13)).fit(sc.transform(Xa), ya).predict(sc.transform(Xb))
def partial(d, pred, g, src=False, peak=False):
    C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] if src else []) + ([rankdata(d.peak.fillna(d.peak.median()))] if peak else []); C = np.c_[tuple(C)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(pred)), res(rankdata(d[g]))); return round(float(r), 3), round(float(p), 4)

import re, collections
norm = lambda s: re.sub(r"[^a-z0-9]", "", re.sub(r"\(.*?\)|feat.*$|featuring.*$", "", str(s).lower().replace("&", "and")))
SP = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx")[["Performer", "Song", "spotify_genre"]].dropna(); SP["t"] = SP.Song.map(norm); SP["a"] = SP.Performer.map(norm); byT = collections.defaultdict(list)
for r in SP.itertuples(): byT[r.t].append(r)
FAM = dict(rock=r"rock|metal|punk|grunge", soul=r"soul|motown|r&b|funk|disco|quiet storm", country=r"country|nashville", hiphop=r"hip hop|rap", folk=r"folk|singer-songwriter", standards=r"adult standards|easy listening|lounge|vocal jazz|brill", dance=r"dance|new wave|synth|europop")
def fam(d):
    out = []
    for r in d.itertuples():
        h = [x for x in byT.get(r.title, []) if r.artist and (r.artist in x.a or x.a in r.artist)]; g = " ".join(str(x.spotify_genre) for x in h); out.append([float(bool(re.search(p, g))) for p in FAM.values()])
    return np.array(out)
G1, G2 = fam(s1), fam(s2); print("genre known", (G1.sum(1) > 0).mean().round(2), (G2.sum(1) > 0).mean().round(2))
def part(d, pred, g, extra=None, src=False):
    C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] if src else []); C = np.c_[tuple(C)]
    if extra is not None: C = np.c_[C, extra]
    res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(pred)), res(rankdata(d[g]))); return round(float(r), 3), round(float(p), 4)
dec = lambda d: np.array([[float(y // 10 == k) for k in range(195, 200)] for y in d.year])

K = 64; km = MiniBatchKMeans(K, random_state=0, n_init=3, batch_size=4096).fit(pool); H = lambda X: np.sqrt(np.bincount(km.predict(X), minlength=K) / len(X)); A = np.array([H(x) for x in X1]); B = np.array([H(x) for x in X2])
# ---- third set
Bb = pd.read_csv("/home/claude/zeneng/corpus/billboard_songs.csv"); Bb["t"] = Bb.title.map(norm); Bb["a"] = Bb.performer.map(norm); bbk = {(norm(r.performer), r.first): r for r in Bb.itertuples()}
S3 = pd.read_excel("/home/claude/corpus/try2/tidytuesday/data/2021/2021-09-14/Hot 100 Audio Features.xlsx")[["Performer", "Song", "spotify_track_popularity"]].dropna(); S3["t"] = S3.Song.map(norm); S3["a"] = S3.Performer.map(norm); pop = S3.groupby(["t", "a"]).spotify_track_popularity.max().to_dict()
PY = Bb.assign(year=Bb["first"].str[:4].astype(int), pop=[pop.get((t, a)) for t, a in zip(Bb.t, Bb.a)]).dropna(subset=["pop"])
Wk = collections.defaultdict(lambda: dict(n=0, perf=set(), titles=collections.Counter()))
for ln in open("/tmp/claude-0/shs/list", encoding="utf8", errors="ignore"):
    p = ln.rstrip("\n").split("\t")
    if len(p) >= 4: w = Wk[p[0]]; w["n"] += 1; w["perf"].add(norm(p[3])); w["titles"][norm(p[2])] += 1
shsT = collections.defaultdict(list)
for k, w in Wk.items():
    for t, c in w["titles"].items():
        if c >= 2 or c == w["n"]: shsT[t].append(k)
used = set(s1.title) | set(s2.title); rows = {}; X3 = {}
for ln in open("/home/claude/corpus/parsed_lakh.jsonl"):
    r = json.loads(ln)
    if not r.get("bb"): continue
    t = norm(r["title"]); a = norm(r["bb"]["performer"]); year = int(r["bb"]["first"][:4])
    if year > 2005 or t in used or (t, a) not in pop: continue
    ns = sorted({(float(n["off"]), int(n["p"])) for s in r["melody"]["sections"] for n in s["notes"] if "off" in n})
    if len(ns) < 48 or len({p for _, p in ns}) < 4: continue
    if (t, a) in rows and rows[(t, a)]["track_score"] >= r["track_score"]: continue
    rows[(t, a)] = dict(id=r["id"], title=t, artist=a, year=year, peak=r["bb"]["peak"], notes=len(ns), track_score=r["track_score"], pop=pop[(t, a)]); X3[(t, a)] = wins(pts([n[0] for n in ns], [n[1] for n in ns]))
s3 = pd.DataFrame(rows.values()); X3 = [X3[(t, a)] for t, a in zip(s3.title, s3.artist)]
s3["love"] = [float((PY[(PY.year - y).abs() <= 3]["pop"].values < p).mean()) for p, y in zip(s3["pop"], s3.year)]
s3["cov0"] = [max((Wk[k]["n"] for k in shsT.get(t, []) if any(a in p or (len(p) >= 4 and p in a) for p in Wk[k]["perf"])), default=0) for t, a in zip(s3.title, s3.artist)]
yr = s3.year.values; s3["cover_rank"] = [float((s3.cov0.values[np.abs(yr - y) <= 5] < c).mean() + .5 * (s3.cov0.values[np.abs(yr - y) <= 5] == c).mean()) for y, c in zip(yr, s3.cov0)]; s3["G"] = (s3.love + s3.cover_rank) / 2
C3 = np.array([H(x) for x in X3]); G3 = fam(s3); s3.to_pickle("set3.pkl"); np.save("set3_hist.npy", C3); print("third set:", len(s3), "songs; covered", int((s3.cov0 > 0).sum()), "; genre known", (G3.sum(1) > 0).mean().round(2), flush=True)
both = reader(np.r_[A, B], np.r_[s1.G.values, s2.G.values], C3); r1 = reader(A, s1.G.values, C3); r2 = reader(B, s2.G.values, C3); out = {}
out["T frozen reader (sets 1+2)"] = part(s3, both, "G"); out["reader of set 1 alone"] = part(s3, r1, "G"); out["reader of set 2 alone"] = part(s3, r2, "G")
out["genre and decade held"] = part(s3, both, "G", np.c_[G3, dec(s3)]); out["chart peak held too"] = part(s3, both, "G", np.c_[G3, dec(s3), rankdata(s3.peak)])
hi = (s3.track_score >= s3.track_score.median()).values; out["best-scored voice tracks"] = part(s3[hi], both[hi], "G") + (int(hi.sum()),); out["worse-scored voice tracks"] = part(s3[~hi], both[~hi], "G")
out["love"] = part(s3, both, "love"); out["covers"] = part(s3, both, "cover_rank")
def coef(X, d, src):
    C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] if src else []); C = np.c_[tuple(C)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; y = res(rankdata(d.G)); return np.array([pearsonr(res(rankdata(X[:, k])), y)[0] for k in range(X.shape[1])])
c1, c2, c3 = coef(A, s1, True), coef(B, s2, False), coef(C3, s3, False); out["region leans: set 3 vs set 1"] = tuple(round(float(v), 4) for v in pearsonr(c3, c1)); out["region leans: set 3 vs set 2"] = tuple(round(float(v), 4) for v in pearsonr(c3, c2)); out["region leans: set 1 vs set 2"] = tuple(round(float(v), 4) for v in pearsonr(c1, c2))
perm = [part(s3, reader(np.r_[A, B], rng.permutation(np.r_[s1.G.values, s2.G.values]), C3), "G")[0] for _ in range(200)]; out["shuffled grades: 95th, 99th"] = (round(float(np.percentile(perm, 95)), 3), round(float(np.percentile(perm, 99)), 3))
for k, v in out.items(): print(f"{k:32} {v}")
json.dump({k: list(v) for k, v in out.items()}, open("third_results.json", "w"), indent=1); np.save("leans.npy", np.c_[c1, c2, c3])
