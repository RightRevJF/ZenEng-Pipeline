"""Run 08 iiv_singletons (after seeing results). Rules in PREDICTION.md. Run once: python3 -I test.py"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np, common as C, models08 as M8, posthoc08 as P
K = 6; ALPHA = 0.05 / K; PRED = 0.07
R = P.singleton_rows(); print("songs", len(R), flush=True)
pw = P.fake_power_ols(R, "IIV", P.EXTRA, PRED, 0.05 / 7); print("POWER (before the outcome):", pw, flush=True)
C.load_outcomes(R, HERE)
y = np.array([s["y_cov"] for s in R]); X = P.Xmat(R, "IIV", P.EXTRA)
b, se, p, n = P.ols_hc1(y, X); main = dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(n))
hv = np.array([C.halves(s["composer"]) for s in R]); halves = []
for h in (0, 1):
    i = hv == h; yy = (np.array([s["ln_sets"] for s in R])[i]); yy = (yy - yy.mean()) / yy.std()
    bh, sh, ph, nh = P.ols_hc1(yy, P.Xmat([s for s, k in zip(R, i) if k], "IIV", P.EXTRA)); halves.append(dict(b=float(bh[0]), se=float(sh[0]), N=int(nh)))
pb, pse, pN, pG, pit = M8.poisson_fe(np.array([s["n_sets"] for s in R], float), X, np.zeros(len(R)))
second = dict(model="Poisson QMLE on n_sets, one group, same columns", b=float(pb[0]), se=float(pse[0]), p=M8.p_two(pb[0], pse[0]))
v = C.verdict(main["b"], main["se"], main["p"], PRED, ALPHA, [h["b"] for h in halves], second["b"], pw["power"])
out = dict(test="iiv_singletons", after_seeing_results=True, prediction=PRED, alpha=ALPHA, power=pw, main=main, halves=halves, second=second,
           verdict=v, range95=[main["b"] - 1.96 * main["se"], main["b"] + 1.96 * main["se"]])
# reported, deciding nothing: without genre dummies; jazz genres (swing, ballad) vs the rest
b2, s2, p2, n2 = P.ols_hc1(y, P.Xmat(R, "IIV", P.EXTRA, fe_genre=False)); out["no_genre"] = dict(b=float(b2[0]), se=float(s2[0]), N=int(n2))
for lab, keep in (("jazz_genres", lambda s: s["genre"] in ("swing", "ballad")), ("other_genres", lambda s: s["genre"] not in ("swing", "ballad"))):
    RR = [s for s in R if keep(s)]; yy = np.array([s["ln_sets"] for s in RR]); yy = (yy - yy.mean()) / yy.std()
    bb, ss, pp, nn = P.ols_hc1(yy, P.Xmat(RR, "IIV", P.EXTRA)); out[lab] = dict(b=float(bb[0]), se=float(ss[0]), N=int(nn))
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1); print(json.dumps(out, indent=1))
