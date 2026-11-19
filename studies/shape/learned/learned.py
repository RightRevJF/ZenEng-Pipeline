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
def codebook(P, K=64):
    km = MiniBatchKMeans(K, random_state=0, n_init=3, batch_size=4096).fit(P); return lambda X: np.sqrt(np.bincount(km.predict(X), minlength=K) / len(X))
def autoenc(P):
    sc = StandardScaler().fit(P); Z = sc.transform(P); ae = MLPRegressor(hidden_layer_sizes=(64, 16, 64), activation="tanh", max_iter=60, random_state=0, early_stopping=True).fit(Z, Z)
    def code(X):
        h = sc.transform(X)
        for i in range(2): h = np.tanh(h @ ae.coefs_[i] + ae.intercepts_[i])
        return np.r_[h.mean(0), h.std(0), np.linalg.norm(np.diff(h, axis=0), axis=1).mean()]
    return code
L1 = codebook(pool); L2 = autoenc(pool); mixw = np.vstack([poolw]); L3 = codebook(poolw); L3n = codebook(poolw[:, [j for j in range(poolw.shape[1]) if j % 5 != 4]]); print("spaces learned", flush=True)
F = dict(L1=(np.array([L1(x) for x in X1]), np.array([L1(x) for x in X2])), L2=(np.array([L2(x) for x in X1]), np.array([L2(x) for x in X2])))
F3 = np.array([L3(x) for x in X2w]); F3n = np.array([L3n(x[:, [j for j in range(x.shape[1]) if j % 5 != 4]]) for x in X2w])
# ---- readers
def reader(Xa, ya, Xb):
    sc = StandardScaler().fit(Xa); return RidgeCV(alphas=np.logspace(0, 4, 13)).fit(sc.transform(Xa), ya).predict(sc.transform(Xb))
def partial(d, pred, g, src=False):
    C = [np.ones(len(d)), rankdata(d.year), rankdata(d.notes)] + ([(d.src == s).astype(float).values for s in ("CB", "RS", "BM")] if src else []); C = np.c_[tuple(C)]; res = lambda v: v - C @ np.linalg.lstsq(C, v, rcond=None)[0]; r, p = pearsonr(res(rankdata(pred)), res(rankdata(d[g]))); return round(float(r), 3), round(float(p), 4), len(d)
out = {}
for k, (A, B) in F.items():
    f = reader(A, s1.G.values, B); b = reader(B, s2.G.values, A)
    out[k] = dict(set1_to_set2=partial(s2, f, "G"), set2_to_set1=partial(s1, b, "G", True), love=partial(s2, f, "love"), covers=partial(s2, f, "cover_rank")); print(k, out[k], flush=True)
def oof(X, y):
    pr = np.zeros(len(y))
    for a, b in KFold(5, shuffle=True, random_state=0).split(X): pr[b] = reader(X[a], y[a], X[b])
    return pr
p3, p3n = oof(F3, s2.G.values), oof(F3n, s2.G.values)
out["L3"] = dict(words_in=partial(s2, p3, "G"), notes_only_twin=partial(s2, p3n, "G"), love=partial(s2, p3, "love"), covers=partial(s2, p3, "cover_rank")); print("L3", out["L3"])
# within-set-1 out-of-fold, for reference
out["within_set1"] = {k: partial(s1, oof(F[k][0], s1.G.values), "G", True) for k in F}; print("within set 1", out["within_set1"]); json.dump(out, open("learned_results.json", "w"), indent=1)
