import sys, os, json, pickle, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v29"); S = Bd.S
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
f = reader(A, s1.G.values, B); b = reader(B, s2.G.values, A)
print("1. plain            fwd", part(s2, f, "G"), "rev", part(s1, b, "G", src=True))
print("   + genre families fwd", part(s2, f, "G", G2), "rev", part(s1, b, "G", G1, True))
print("   + genre + decade fwd", part(s2, f, "G", np.c_[G2, dec(s2)]), "rev", part(s1, b, "G", np.c_[G1, dec(s1)], True))
# 2. what the two readers weight, region by region
def coef(X, d, src):
    sc = StandardScaler().fit(X); C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] if src else []); C = np.c_[tuple(C)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; y = res(rankdata(d.G))
    return np.array([pearsonr(res(rankdata(X[:, k])), y)[0] for k in range(X.shape[1])])
c1, c2 = coef(A, s1, True), coef(B, s2, False); print("2. region-by-region lean toward G, set 1 against set 2: r =", round(float(np.corrcoef(c1, c2)[0, 1]), 3), "p", round(float(pearsonr(c1, c2)[1]), 4))
# 3. what the regions are
Cn = km.cluster_centers_.reshape(K, 8, 4); deg = (np.round(np.arctan2(Cn[:, :, 1], Cn[:, :, 0]) / (2 * np.pi) * 12) % 12 * 7) % 12; ht = Cn[:, :, 2] * 6; ioi = 2 ** (Cn[:, :, 3] * 2)
D = pd.DataFrame(dict(region=range(K), lean1=c1, lean2=c2, use=A.mean(0) ** 2, beats_per_note=ioi[:, :7].mean(1), longest=ioi.max(1), uneven=np.log2(ioi[:, :7]).std(1), span=ht.max(1) - ht.min(1), step=np.abs(np.diff(ht, axis=1)).mean(1), rise=ht[:, -1] - ht[:, 0], same_note=(np.abs(np.diff(ht, axis=1)) < .5).mean(1), on_tonic_chord=np.isin(deg, [0, 4, 7]).mean(1), off_scale=np.isin(deg, [1, 3, 6, 8, 10]).mean(1)))
D["lean"] = (D.lean1 + D.lean2) / 2; print("3. what regions that lean great look like (correlation of a region's lean with its traits, 64 regions)")
for c in ("beats_per_note", "longest", "uneven", "span", "step", "rise", "same_note", "on_tonic_chord", "off_scale"):
    print(f"   {c:15} set1 {np.corrcoef(D.lean1, D[c])[0,1]:+.2f}  set2 {np.corrcoef(D.lean2, D[c])[0,1]:+.2f}")
pd.set_option("display.width", 250); print(D.sort_values("lean").round(2).iloc[list(range(5)) + list(range(K - 5, K))][["region", "lean1", "lean2", "use", "beats_per_note", "longest", "uneven", "span", "step", "same_note", "off_scale"]].to_string())
# 4. the same traits read straight off each song (after the fact)
def traits(X):
    X = X.reshape(len(X), 8, 4); h = X[:, :, 2] * 6; l = X[:, :, 3] * 2; st = np.abs(np.diff(h, axis=1))
    return dict(beats_per_note=float((2 ** l[:, 0]).mean()), log_pace=float(l[:, 0].mean()), uneven=float(l[:, :7].std(1).mean()), span=float((h.max(1) - h.min(1)).mean()), step=float(st.mean()), same_note=float((st < .5).mean()), leaps=float((st > 2.5).mean()), long_notes=float((l[:, 0] >= 1).mean()))
T1 = pd.DataFrame([traits(x) for x in X1]); T2 = pd.DataFrame([traits(x) for x in X2]); print("4. plain traits against G (partial rho): set 1, set 2")
for c in T1.columns: print(f"   {c:15} {part(s1, T1[c].values, 'G', src=True)}  {part(s2, T2[c].values, 'G')}   love {part(s1, T1[c].values, 'love', src=True)[0]:+.3f}/{part(s2, T2[c].values, 'love')[0]:+.3f}  covers {part(s1, T1[c].values, 'cover_rank', src=True)[0]:+.3f}/{part(s2, T2[c].values, 'cover_rank')[0]:+.3f}")
T1.to_pickle("traits1.pkl"); T2.to_pickle("traits2.pkl"); D.to_csv("regions.csv", index=False)
