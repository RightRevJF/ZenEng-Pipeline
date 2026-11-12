"""422 (amends 364, 374, 397): separation read on the 30 measures the two kept collections agree on (zeneng_v120_second_collection.json),
against the kept windows of both collections pooled: CoCoPops (314 windows, 170 true songs, 369) and BiMMuDa 1958-1991
(zeneng_v120_bimmuda_windows.json, 231 windows). 364's fresh judge (L2 logistic, C = 1, balanced, z-scored), tested on held-out kept songs
(both collections split by song) and held-out builds (AUC). Within a song: half the builds held out; across songs: fitted on one song's
builds, tested on another's. Families within the 30: pitch (23), rhythm (4), form (3). The six harmony measures are read on CoCoPops alone
and printed apart (422). Printed beside the collections' own separation from each other, 0.56, and beside 0.75 (Window 140).
The first 400 complete builds of each main run.
Usage: python3 sep_v120.py OUT name=prefix [name=prefix ...]"""
import sys, pickle, json
import numpy as np
sys.path[:0] = ["/home/claude/p40"]
import judges as J
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
OUT = sys.argv[1]; PRE = dict(a.split("=", 1) for a in sys.argv[2:])
T = "/home/claude/p51/tables"
KW = json.load(open("/home/claude/p40/tables/zeneng_v105_kept_windows.json"))
SM = json.load(open(f"{T}/zeneng_v117_kept_songs_and_modes.json")); SC = json.load(open(f"{T}/zeneng_v120_second_collection.json"))
BW = json.load(open(f"{T}/zeneng_v120_bimmuda_windows.json"))
A30 = SC["the 30 agreed measures (420, 422)"]; assert len(A30) == 30 and BW["measures"] == A30
MS = J.CJ["measures"]; HARM = MS[40:46]
FAM = {"agreed 30": A30, "pitch (agreed)": [m for m in A30 if m in MS[:24]], "rhythm (agreed)": [m for m in A30 if m in MS[24:37]], "form": MS[37:40]}
assert [len(FAM[k]) for k in ("pitch (agreed)", "rhythm (agreed)", "form")] == [23, 4, 3]
KRW = [dict(zip(KW["measures"], [np.nan if x is None else x for x in r])) for r in KW["rows"]]
C_X = np.array([[r.get(m, np.nan) for m in A30] for r in KRW], float)
B_X = np.array([[np.nan if x is None else x for x in r] for r in BW["rows"]], float)
C_H = np.array([[r.get(m, np.nan) for m in HARM] for r in KRW], float)
cs = sorted(set(SM["song"])); bs = sorted(set(BW["song"]))
grp = np.r_[[cs.index(s) for s in SM["song"]], [len(cs) + bs.index(s) for s in BW["song"]]]; NG = len(cs) + len(bs)
KX = np.vstack([C_X, B_X]); src = np.r_[np.zeros(len(C_X)), np.ones(len(B_X))]
colm = np.nanmean(KX, 0); KX = np.where(np.isfinite(KX), KX, colm)
hcol = np.nanmean(C_H, 0); C_H = np.where(np.isfinite(C_H), C_H, hcol)
def bx(prefix):
    D = pickle.load(open(f"{prefix}_main.pkl", "rb")); Al = [b for b in D["all"] if b["read"]["v"] and b["read"]["c"]][:400]
    F = [f for b in Al for w in ("v", "c") if (f := b["read"][w])]
    a = np.array([[f.get(m, np.nan) if f.get(m) is not None else np.nan for m in A30] for f in F], float)
    h = np.array([[f.get(m, np.nan) if f.get(m) is not None else np.nan for m in HARM] for f in F], float)
    return np.where(np.isfinite(a), a, colm), np.where(np.isfinite(h), h, hcol), len(Al)
B = {s: bx(p) for s, p in PRE.items()}
rs = np.random.RandomState(20261116); perm = rs.permutation(NG); half = [set(perm[: NG // 2]), set(perm[NG // 2:])]
KH = [np.array([g in half[h] for g in grp]) for h in (0, 1)]
cgrp = np.array([cs.index(s) for s in SM["song"]]); cperm = rs.permutation(len(cs)); chalf = [set(cperm[: len(cs) // 2]), set(cperm[len(cs) // 2:])]
CKH = [np.array([g in chalf[h] for g in cgrp]) for h in (0, 1)]
def fit_auc(Ktr, Btr, Kte, Bte):
    X = np.vstack([Ktr, Btr]); mu, sd = X.mean(0), X.std(0) + 1e-9; y = np.r_[np.ones(len(Ktr)), np.zeros(len(Btr))]
    lr = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced").fit((X - mu) / sd, y)
    Xt = np.vstack([Kte, Bte]); yt = np.r_[np.ones(len(Kte)), np.zeros(len(Bte))]
    return float(roc_auc_score(yt, lr.decision_function((Xt - mu) / sd)))
def read(KXf, KHf, Bget):
    out = dict(within={}, across={})
    for s in B:
        X = Bget(s); bh = np.repeat(np.arange(len(X) // 2 + 1) % 2 == 0, 2)[:len(X)]
        out["within"][s] = round(float(np.mean([fit_auc(KXf[KHf[h]], X[bh if h == 0 else ~bh], KXf[KHf[1 - h]], X[~bh if h == 0 else bh]) for h in (0, 1)])), 3)
    for s in B:
        for t in B:
            if s != t: out["across"][f"{s} -> {t}"] = round(float(np.mean([fit_auc(KXf[KHf[h]], Bget(s), KXf[KHf[1 - h]], Bget(t)) for h in (0, 1)])), 3)
    out["across_mean"] = round(float(np.mean(list(out["across"].values()))), 3) if out["across"] else None
    t3 = [k for k in out["across"] if all(x in ("40", "42", "43") for x in k.split(" -> "))]
    out["across_mean_40_42_43"] = round(float(np.mean([out["across"][k] for k in t3])), 3) if len(t3) == 6 else None
    return out
res = dict(kept=dict(cocopops_windows=len(C_X), bimmuda_windows=len(B_X), songs=NG), agreed=A30, beside=dict(collections_against_each_other=0.56, window140_builds_pooled=0.75),
           window140=SC["separation (422)"], builds_read={s: n for s, (_, _, n) in B.items()}, family={})
for fam, ms in FAM.items():
    ix = [A30.index(m) for m in ms]
    res["family"][fam] = read(KX[:, ix], KH, lambda s, ix=ix: B[s][0][:, ix])
res["family"]["harmony (CoCoPops alone, apart)"] = read(C_H, CKH, lambda s: B[s][1])
# the collections against each other on the agreed 30 (a check of the pooled rows: Window 140 reads 0.555)
yc = src; a_ = []
for h in (0, 1):
    tr, te = KH[h], KH[1 - h]
    X = KX[tr]; mu, sd = X.mean(0), X.std(0) + 1e-9
    lr = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced").fit((X - mu) / sd, yc[tr]); a_.append(roc_auc_score(yc[te], lr.decision_function((KX[te] - mu) / sd)))
res["collections_against_each_other"] = round(float(np.mean(a_)), 3)
# costs (340 on the agreed 30): a judge fitted on both collections pooled against all these builds; points from the kept mean
Ball = np.vstack([B[s][0] for s in B]); XX = np.vstack([KX, Ball]); mu, sd = XX.mean(0), XX.std(0) + 1e-9
lr = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced").fit((XX - mu) / sd, np.r_[np.ones(len(KX)), np.zeros(len(Ball))])
cost = lr.coef_[0] * (KX.mean(0) - Ball.mean(0)) / sd
order = np.argsort(-cost)
res["costs_agreed_30"] = dict(gap=round(float(cost.sum()), 2), eight=[(A30[j], round(float(cost[j]), 2), round(float(KX[:, j].mean()), 3), round(float(Ball[:, j].mean()), 3)) for j in order[:8]])
json.dump(res, open(OUT, "w"), indent=1)
print("collections", res["collections_against_each_other"], {f: (r["across_mean"], r["within"]) for f, r in res["family"].items()}, res["costs_agreed_30"]["eight"][:4])
