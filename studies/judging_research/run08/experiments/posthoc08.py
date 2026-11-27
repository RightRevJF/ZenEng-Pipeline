"""Run 08 after-seeing-results tests (written after iiv_chunk and heritability passed; frozen before their own outcomes are joined).
iiv_singletons: IIV on the 2,733 matched ChoCo songs whose composer has only one song (never joined to an outcome).
iiv_source:     IIV read from Wikifonia lead sheets only, on design songs that have both an iReal and a Wikifonia chart (seen songs)."""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import stats
import common as C, models08 as M8, measures as MS

EXTRA = ["w_chr", "ch_rep", "V", "ln_chg", "ln_bars"]

def ols_hc1(y, X):
    """plain OLS with intercept, HC1 robust SEs. Returns b, se, p for the columns of X (intercept dropped)."""
    X1 = np.column_stack([np.ones(len(y)), X]); keep = np.r_[True, X.std(0) > 1e-12]; X1 = X1[:, keep]
    XtX = np.linalg.pinv(X1.T @ X1); b = XtX @ X1.T @ y; e = y - X1 @ b; n, k = X1.shape
    V = XtX @ (X1.T * e ** 2) @ X1 @ XtX * n / (n - k); se = np.sqrt(np.diag(V)); p = 2 * stats.t.sf(np.abs(b / se), n - k)
    return b[1:], se[1:], p[1:], n

def singleton_rows():
    info, S = C.load_design(within=False); cb = C.charts_by_id(); R = []
    for s in S:
        if s["within"]: continue
        rows = [MS.chart_row(cb[k])[0] for k in s["charts"]]; rows = [r for r in rows if r is not None]
        if not rows: continue
        for m in ["IIV"] + EXTRA:
            v = [r[m] for r in rows if np.isfinite(r[m])]; s[m] = float(np.mean(v)) if v else None
        if all(s.get(m) is not None for m in ["IIV"] + EXTRA): R.append(s)
    return R

def source_rows():
    info, S = C.load_design(); M = json.load(open(os.path.join(C.DL, "choco", "measures_run08.json"))); cb = C.charts_by_id(); R = []
    for s in S:
        if "wikifonia" not in s["parts"] or not any(p.startswith("ireal") for p in s["parts"]): continue
        wk = [M["charts"][k] for k in s["charts"] if k in M["charts"] and cb[k]["part"] == "wikifonia"]
        ir = [M["charts"][k] for k in s["charts"] if k in M["charts"] and cb[k]["part"] != "wikifonia"]
        if not wk or not ir: continue
        for m in ["IIV"] + EXTRA:
            s[m] = float(np.mean([r[m] for r in wk])); s[m + "_ireal"] = float(np.mean([r[m] for r in ir]))
        s["genre"] = "wikifonia_and_ireal"   # one bin: every song here has both sources
        R.append(s)
    return R

def Xmat(R, meas, extra, fe_genre=True):
    cols = [C.zs([s[meas] for s in R])] + [C.zs([s[e] for s in R]) for e in extra]
    D = [C.dummies(C.decade_bins(R))]
    if fe_genre: D.insert(0, C.dummies([s["genre"] for s in R]))
    return np.column_stack(cols + [d for d in D if d.size])

def fake_power_ols(R, meas, extra, beta, alpha, draws=300, seed=11, composer_fe=False):
    rng = np.random.default_rng(seed)
    X = np.column_stack([C.zs([s[meas] for s in R])] + [C.zs([s[e] for s in R]) for e in extra] +
                        ([C.dummies([s["genre"] for s in R])] if not composer_fe else []))
    z = X[:, 0]; g = np.array([s["composer"] for s in R]); hits = 0; ses = []
    for d in range(draws):
        if composer_fe:
            ug, inv = np.unique(g, return_inverse=True); u = rng.normal(0, math.sqrt(0.3), len(ug))[inv]
            y = u + beta * z + rng.normal(0, math.sqrt(0.7 - beta ** 2), len(z)); b, se, p, N, G = C.ols_fe(y, X, g)
        else:
            y = beta * z + rng.normal(0, math.sqrt(1 - beta ** 2), len(z)); b, se, p, N = ols_hc1(y, X)
        hits += (p[0] < alpha) and b[0] > 0; ses.append(se[0])
    return dict(power=hits / draws, se_fake=float(np.median(ses)), N=len(R), draws=draws)
