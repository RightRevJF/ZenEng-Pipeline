"""364 with 369 and 374: separability. A judge fitted fresh (340's: L2 logistic, C = 1, balanced, the 46 content measures z-scored) on kept
windows against a run's builds, tested on held-out kept songs and held-out builds (AUC). Kept windows are split by their true songs
(zeneng_v117_kept_songs_and_modes.json, 369). Within a song: half the builds held out; across songs: fitted on one song's builds, tested on
another's. The first 400 complete builds of each main run. Printed beside the yardstick (374): kept 1958-1969 against 1980-1991 0.57, the
1960s against the 1970s 0.63.
Usage: python3 sep_v118.py OUT name=prefix [name=prefix ...]"""
import sys, pickle, json
import numpy as np
sys.path[:0] = ["/home/claude/p40"]
import judges as J
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
OUT = sys.argv[1]; PRE = dict(a.split("=", 1) for a in sys.argv[2:])
KW = json.load(open("/home/claude/p40/tables/zeneng_v105_kept_windows.json"))
SM = json.load(open("/home/claude/p50/tables/zeneng_v117_kept_songs_and_modes.json"))
assert SM["row order checked against the v105 file"] and len(SM["song"]) == len(KW["rows"])
KRW = [dict(zip(KW["measures"], [np.nan if x is None else x for x in r])) for r in KW["rows"]]
MS = J.CJ["measures"]
names = sorted(set(SM["song"])); grp = np.array([names.index(s) for s in SM["song"]]); NG = len(names)
KX = np.array([[r.get(m, np.nan) for m in MS] for r in KRW], float)
def bx(prefix):
    D = pickle.load(open(f"{prefix}_main.pkl", "rb")); Al = [b for b in D["all"] if b["read"]["v"] and b["read"]["c"]][:400]
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
res = dict(kept_songs=NG, kept_windows=len(KX), grouping="true songs (369)", builds_read={s: n for s, (_, n) in B.items()}, within={}, across={},
           yardstick=dict(first_decade_against_last=0.57, sixties_against_seventies=0.63, source="zeneng_v117_yardstick.json (374)"))
for s, (X, n) in B.items():
    bh = np.repeat(np.arange(len(X) // 2 + 1) % 2 == 0, 2)[:len(X)]                     # a build's two windows stay together
    a = [fit_auc(KX[KH[h]], X[bh if h == 0 else ~bh], KX[KH[1 - h]], X[~bh if h == 0 else bh]) for h in (0, 1)]
    res["within"][s] = round(float(np.mean(a)), 3)
for s in B:
    for t in B:
        if s == t: continue
        a = [fit_auc(KX[KH[h]], B[s][0], KX[KH[1 - h]], B[t][0]) for h in (0, 1)]
        res["across"][f"{s} -> {t}"] = round(float(np.mean(a)), 3)
res["across_mean"] = round(float(np.mean(list(res["across"].values()))), 3) if res["across"] else None
json.dump(res, open(OUT, "w"), indent=1); print(json.dumps(res))
