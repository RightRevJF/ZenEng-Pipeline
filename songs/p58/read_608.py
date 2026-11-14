"""read_608.py: 608, the judge's baselines (printed once here: the judge was not refitted). L2 logistic, C = 0.3, on the judge's 39 measures.
- kept against kept, songs split four ways: fit on quarters 1 and 3 (labels A, B), test on 2 and 4; twenty random splits.
- engine against kept on density alone (notes a bar, empty bars), on the 39 measures, and on the 37 others with notes a bar (and its square)
  and empty bars regressed out on kept windows. The engine side is one song (48), so its builds are split in half (train, test); the kept
  side is split by piece. Twenty splits. Windows: the first eight bars of the first verse and chorus.
Usage: python3 read_608.py RUN.pkl [...]  ->  read/read_608.json"""
import sys, io, contextlib, json, pickle, random
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
sys.argv, ARGS = ["x", "10", "main"], sys.argv[1:]; sys.path.insert(0, "/home/claude/p58")
with contextlib.redirect_stdout(io.StringIO()): import melody_l1_p58 as E
J = E.RJ; MS = J["measures"]; FL = np.array(J["fill_missing_with"])
KW = json.load(open("/home/claude/p58/tables/zeneng_v132_kept_windows.json"))["windows"]
def xk(w): return np.array([FL[k] if (w.get(m) is None or not np.isfinite(w.get(m))) else w[m] for k, m in enumerate(MS)], float)
XK = np.array([xk(w) for w in KW]); PK = np.array([w["piece"] for w in KW])
def xe(N):
    f = E.feats(N, E.mton()) or {}; c = E.cand(sorted(N)) or {}
    return np.array([fl if (v is None or not np.isfinite(v)) else v for v, fl in ((f.get(m) if m in f else c.get(m), fl) for m, fl in zip(MS, FL))], float)
def auc(Xtr, ytr, Xte, yte):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-9
    m = LogisticRegression(C=0.3, max_iter=2000, class_weight="balanced").fit((Xtr - mu) / sd, ytr)
    return roc_auc_score(yte, m.predict_proba((Xte - mu) / sd)[:, 1])
ID = {m: k for k, m in enumerate(MS)}; DEN = [ID["notes_per_bar"], ID["empty_bars"]]; OTH = [k for k in range(len(MS)) if k not in DEN]
def dens(X): return np.column_stack([X[:, ID["notes_per_bar"]], X[:, ID["notes_per_bar"]] ** 2, X[:, ID["empty_bars"]], np.ones(len(X))])
B_ = np.linalg.lstsq(dens(XK), XK[:, OTH], rcond=None)[0]
def resid(X): return X[:, OTH] - dens(X) @ B_
out = {}
rng = random.Random(608); pieces = sorted(set(PK))
kk = []
for _ in range(20):
    pc = pieces[:]; rng.shuffle(pc); q = {p: i % 4 for i, p in enumerate(pc)}; g = np.array([q[p] for p in PK])
    tr, te = np.isin(g, (0, 2)), np.isin(g, (1, 3))
    kk.append(auc(XK[tr], (g[tr] == 2).astype(int), XK[te], (g[te] == 3).astype(int)))
out["kept against kept, songs split four ways (mean, sd)"] = [round(float(np.mean(kk)), 3), round(float(np.std(kk)), 3)]
for path in ARGS:
    D = pickle.load(open(path, "rb")); XE = []
    for b in D["all"]:
        ns = [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
        for s_ in ("Verse 1", "Chorus 1"):
            N_ = E.win_N(ns, E.BAR0[s_])
            if N_: XE.append(xe(N_))
    XE = np.array(XE); res = {"density alone": [], "the 39 measures": [], "the 37 others, density regressed out": []}
    for _ in range(20):
        pc = pieces[:]; rng.shuffle(pc); half = set(pc[: len(pc) // 2]); ktr = np.array([p in half for p in PK]); idx = list(range(len(XE))); rng.shuffle(idx)
        etr, ete = np.zeros(len(XE), bool), np.zeros(len(XE), bool); etr[idx[: len(idx) // 2]] = True; ete[idx[len(idx) // 2:]] = True
        for lab, f in (("density alone", lambda X: X[:, DEN]), ("the 39 measures", lambda X: X), ("the 37 others, density regressed out", resid)):
            Xtr = np.vstack([f(XK[ktr]), f(XE[etr])]); ytr = np.r_[np.zeros(ktr.sum()), np.ones(etr.sum())]
            Xte = np.vstack([f(XK[~ktr]), f(XE[ete])]); yte = np.r_[np.zeros((~ktr).sum()), np.ones(ete.sum())]
            res[lab].append(auc(Xtr, ytr, Xte, yte))
    out[path.split("/")[-1]] = {k: [round(float(np.mean(v)), 3), round(float(np.std(v)), 3)] for k, v in res.items()}
json.dump(out, open("/home/claude/p58/read/read_608.json", "w"), indent=1)
print(json.dumps(out, indent=1))
