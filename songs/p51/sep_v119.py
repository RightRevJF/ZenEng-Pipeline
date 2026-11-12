"""396/397: separability by family. 364's fresh judge (L2 logistic, C = 1, balanced, z-scored) fitted on kept windows against a run's
builds and tested on held-out true kept songs (369) and held-out builds (AUC), for each family of the 46 content measures apart:
pitch (24), rhythm (13), harmony (6), form (3), with all 46, all but the outside-scale share, and pitch without it.
Within a song: half the builds held out; across songs: fitted on one song's builds, tested on another's (mean of the pairs).
Also each measure's separation alone (AUC, builds pooled, every kept window). The first 400 complete builds of each main run.
Printed beside Window 139's figures (zeneng_v119_families.json) and the yardstick (0.57, 0.63).
Usage: python3 sep_v119.py OUT name=prefix [name=prefix ...]"""
import sys, pickle, json
import numpy as np
sys.path[:0] = ["/home/claude/p40"]
import judges as J
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
OUT = sys.argv[1]; PRE = dict(a.split("=", 1) for a in sys.argv[2:])
H = "/home/claude/p51/tables"
KW = json.load(open(f"{H}/zeneng_v105_kept_windows.json")) if False else json.load(open("/home/claude/p40/tables/zeneng_v105_kept_windows.json"))
SM = json.load(open(f"{H}/zeneng_v117_kept_songs_and_modes.json")); FAM = json.load(open(f"{H}/zeneng_v119_families.json"))
assert SM["row order checked against the v105 file"] and len(SM["song"]) == len(KW["rows"])
KRW = [dict(zip(KW["measures"], [np.nan if x is None else x for x in r])) for r in KW["rows"]]
MS = J.CJ["measures"]
F = {"pitch": MS[:24], "rhythm": MS[24:37], "form": MS[37:40], "harmony": MS[40:46]}
assert [len(F[k]) for k in ("pitch", "rhythm", "form", "harmony")] == [24, 13, 3, 6]
assert set(F["rhythm"]) == set(FAM["measures alone"]["the same with one measure left out"])
F["all"] = MS; F["all but outside_scale"] = [m for m in MS if m != "outside_scale"]; F["pitch but outside_scale"] = [m for m in F["pitch"] if m != "outside_scale"]
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
res = dict(kept_songs=NG, kept_windows=len(KX), grouping="true songs (369)", builds_read={s: n for s, (_, n) in B.items()},
           yardstick=dict(first_decade_against_last=0.57, sixties_against_seventies=0.63), window139={}, family={})
for fam, ms in F.items():
    ix = [MS.index(m) for m in ms]; r = dict(within={}, across={})
    for s, (X, n) in B.items():
        bh = np.repeat(np.arange(len(X) // 2 + 1) % 2 == 0, 2)[:len(X)]
        a = [fit_auc(KX[KH[h]][:, ix], X[bh if h == 0 else ~bh][:, ix], KX[KH[1 - h]][:, ix], X[~bh if h == 0 else bh][:, ix]) for h in (0, 1)]
        r["within"][s] = round(float(np.mean(a)), 3)
    for s in B:
        for t in B:
            if s == t: continue
            a = [fit_auc(KX[KH[h]][:, ix], B[s][0][:, ix], KX[KH[1 - h]][:, ix], B[t][0][:, ix]) for h in (0, 1)]
            r["across"][f"{s} -> {t}"] = round(float(np.mean(a)), 3)
    r["across_mean"] = round(float(np.mean(list(r["across"].values()))), 3) if r["across"] else None
    t3 = [k for k in r["across"] if all(x in ("40", "42", "43") for x in k.split(" -> "))]
    r["across_mean_40_42_43"] = round(float(np.mean([r["across"][k] for k in t3])), 3) if len(t3) == 6 else None
    res["family"][fam] = r
    w = FAM["by family (397)"].get(fam)
    if w: res["window139"][fam] = dict(v116=w["v116"]["across songs, mean of six"], v118=w["v118"]["across songs, mean of six"])
Ball = np.vstack([x for x, _ in B.values()]); alone = []
for j, m in enumerate(MS):
    yt = np.r_[np.ones(len(KX)), np.zeros(len(Ball))]; a = roc_auc_score(yt, np.r_[KX[:, j], Ball[:, j]])
    alone.append(dict(measure=m, family=next(k for k in ("pitch", "rhythm", "form", "harmony") if m in F[k]), auc=round(float(a), 3),
                      strength=round(abs(float(a) - 0.5), 3), kept_mean=round(float(KX[:, j].mean()), 3), builds_mean=round(float(Ball[:, j].mean()), 3)))
res["measures_alone_top10"] = sorted(alone, key=lambda x: -x["strength"])[:10]; res["measures_alone"] = alone
json.dump(res, open(OUT, "w"), indent=1)
print({f: (r["across_mean_40_42_43"], r["across_mean"], r["within"]) for f, r in res["family"].items()})
