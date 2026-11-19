import sys, os, json, pickle, hashlib, warnings, numpy as np, pandas as pd; warnings.filterwarnings("ignore")
sys.path[:0] = ["/home/claude/zeneng/corpus/v26", "/home/claude/zeneng/corpus/v25"]
os.chdir("/home/claude/zeneng/corpus/v26"); import build as Bd; os.chdir("/home/claude/zeneng/corpus/v28"); S = Bd.S
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
out = []
for K in (32, 64, 128):
    for seed in range(1, 6):
        L = codebook(pool, K, seed); A = np.array([L(x) for x in X1]); B = np.array([L(x) for x in X2]); f = reader(A, s1.G.values, B); b = reader(B, s2.G.values, A)
        row = dict(K=K, seed=seed, fwd=partial(s2, f, "G"), fwd_peak=partial(s2, f, "G", peak=True), rev=partial(s1, b, "G", True), rev_peak=partial(s1, b, "G", True, True), strict=partial(s2[s2.loose == 0], f[(s2.loose == 0).values], "G")); out.append(row); print(row, flush=True)
    if K == 64:
        perm = []
        for i in range(200):
            y = rng.permutation(s1.G.values); perm.append(partial(s2, reader(A, y, B), "G")[0])
        print("shuffled grades in set 1: mean", round(float(np.mean(perm)), 3), "95th", round(float(np.percentile(perm, 95)), 3), "99th", round(float(np.percentile(perm, 99)), 3), flush=True)
print("fwd median", np.median([r["fwd"][0] for r in out]), "share > 0", np.mean([r["fwd"][0] > 0 for r in out]), "| rev median", np.median([r["rev"][0] for r in out]), "share > 0", np.mean([r["rev"][0] > 0 for r in out]))
json.dump(out, open("robust_results.json", "w"), indent=1)
