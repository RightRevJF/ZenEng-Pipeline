"""364: separability. A judge fitted fresh (340's: L2 logistic, C = 1, balanced, the 46 content measures z-scored) on kept windows against
a run's builds, tested on held-out kept songs and held-out builds (AUC). Within a song: half the builds held out; across songs: fitted on
one song's builds, tested on another's. The first 400 complete builds of each main run. Kept windows are split by song: the kept-window
table carries no song, so a song is read as a run of adjacent windows with the same year (Q1 A, v116; an inference, labelled).
Usage: python3 sep_v116.py OUT PREFIX40 PREFIX42 PREFIX43"""
import sys, pickle, json
import numpy as np
sys.path[:0] = ["/home/claude/p40"]
import judges as J
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
OUT = sys.argv[1]; PRE = dict(zip(("40", "42", "43"), sys.argv[2:5]))
KW = json.load(open("/home/claude/p40/tables/zeneng_v105_kept_windows.json"))
KRW = [dict(zip(KW["measures"], [np.nan if x is None else x for x in r])) for r in KW["rows"]]
MS = J.CJ["measures"]
grp, g = [], -1                                                                       # adjacent windows of one year: one song
for k, y in enumerate(KW["year"]):
    if k == 0 or y != KW["year"][k - 1] or (KW["section"][k] == "verse" and KW["section"][k - 1] == "chorus"): g += 1
    grp.append(g)
grp = np.array(grp); NG = grp.max() + 1
KX = np.array([[r.get(m, np.nan) for m in MS] for r in KRW], float)
def bx(prefix):
    D = pickle.load(open(f"{prefix}_main.pkl", "rb")); Al = D["all"][:400]
    return np.array([[f.get(m, np.nan) if f.get(m) is not None else np.nan for m in MS] for b in Al for w in ("v", "c") if (f := b["read"][w])], float), len(Al)
B = {s: bx(p) for s, p in PRE.items()}
colm = np.nanmean(KX, 0)
def fill(X): return np.where(np.isfinite(X), X, colm)
KX = fill(KX); B = {s: (fill(x), n) for s, (x, n) in B.items()}
rs = np.random.RandomState(20261116); perm = rs.permutation(NG); half = [set(perm[: NG // 2]), set(perm[NG // 2:])]
KH = [np.array([gg in half[h] for gg in grp]) for h in (0, 1)]
def fit_auc(Ktr, Btr, Kte, Bte):
    X = np.vstack([Ktr, Btr]); mu, sd = X.mean(0), X.std(0) + 1e-9; y = np.r_[np.ones(len(Ktr)), np.zeros(len(Btr))]
    lr = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced").fit((X - mu) / sd, y)
    Xt = np.vstack([Kte, Bte]); yt = np.r_[np.ones(len(Kte)), np.zeros(len(Bte))]
    return float(roc_auc_score(yt, lr.decision_function((Xt - mu) / sd)))
res = dict(kept_songs_read=int(NG), kept_windows=len(KX), builds_read={s: n for s, (_, n) in B.items()}, within={}, across={})
for s, (X, n) in B.items():
    bh = np.arange(len(X)) % 2 == 0                                                    # a build's two windows stay together (v, c adjacent)
    bh = np.repeat(np.arange(len(X) // 2 + 1) % 2 == 0, 2)[:len(X)]
    a = [fit_auc(KX[KH[h]], X[bh if h == 0 else ~bh], KX[KH[1 - h]], X[~bh if h == 0 else bh]) for h in (0, 1)]
    res["within"][s] = round(float(np.mean(a)), 3)
for s in B:
    for t in B:
        if s == t: continue
        a = [fit_auc(KX[KH[h]], B[s][0], KX[KH[1 - h]], B[t][0]) for h in (0, 1)]
        res["across"][f"{s} -> {t}"] = round(float(np.mean(a)), 3)
res["across_mean"] = round(float(np.mean(list(res["across"].values()))), 3)
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res))
