"""Run 09, late_momentum08 (AFTER SEEING RESULTS; seen songs; a lead): late_window08 plus recent momentum. Rules in PREDICTION.md. Run once:  python3 -I test.py"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common09 as C9
import harness09 as H
P8 = H.P8; C8 = H.C8
JAZZ8 = {"swing", "ballad", "latin", "blues", "waltz"}

R = H.dres_rows()
COLS0 = ["IIV"] + H.SEEN_STD
print(f"[late_momentum08] seen songs {len(R)}; prediction +0.03 on y_new = log(1 + artist sets first dated 2023-2024)", flush=True)
pw = H.fake_power(R, COLS0, 0.03, 0.05)
print("POWER at .05 (fake outcomes, without the n_prior column):", H.jd(pw), flush=True)

H.load_seen_outcomes(R, HERE)                     # the guard runs here
need = {r["clique"] for r in R}; T = {}
with open(os.path.join(C9.SHAPE, "discogs_versions.jsonl")) as f:
    for line in f:
        d = json.loads(line)
        if d["id"] in need: T[d["id"]] = [y for _, y, _ in d["sets"] if y is not None]
for r in R:
    ys = T.get(r["clique"], [])
    r["n_new"] = sum(1 for y in ys if y >= 2023); r["n_prior"] = sum(1 for y in ys if y <= 2022); r["ln_recent"] = math.log(1 + sum(1 for y in ys if 2018 <= y <= 2022))
    r["ln_prior"] = math.log(1 + r["n_prior"]); r["ln_new"] = math.log(1 + r["n_new"])

def ystd(RR):
    v = np.array([s["ln_new"] for s in RR]); return (v - v.mean()) / v.std()

def fit(RR, cols):
    y = ystd(RR); X = H.Xmat(RR, cols); b, se, p, n = P8.ols_hc1(y, X)
    hv = np.array([C9.halves(s["composer"]) for s in RR]); hb = []
    for h in (0, 1):
        sub = [s for s, k in zip(RR, hv == h) if k]; bh, sh, ph, nh = P8.ols_hc1(ystd(sub), H.Xmat(sub, cols)); hb.append(dict(b=float(bh[0]), se=float(sh[0]), N=int(nh)))
    pb, pse, pp = P8.poisson_plain(np.array([s["n_new"] for s in RR], float), X)
    return dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(n), range95=[float(b[0] - 1.96 * se[0]), float(b[0] + 1.96 * se[0])],
                halves=hb, second=dict(model="Poisson QMLE on n_new (posthoc08.poisson_plain)", b=pb, se=pse, p=pp))

COLS = ["IIV", "ln_prior", "ln_recent"] + H.SEEN_STD
main = fit(R, COLS)
sup = main["p"] < 0.05 and main["b"] > 0 and all(h["b"] > 0 for h in main["halves"]) and main["second"]["b"] > 0
notsup = abs(0.03 - main["b"]) > 1.96 * main["se"]
verdict = "lead supported" if sup else "lead not supported (+0.03 outside the 95% range)" if notsup else "unsettled"
rd = {}
rd["without_prior"] = fit(R, COLS0)
yy = ystd(R); XX = H.Xmat(R, COLS); bb, ss, pp_, nn = P8.ols_hc1(yy, XX); rd["recent_momentum_coef"] = dict(b=float(bb[2]), se=float(ss[2]), p=float(pp_[2]))
W = [r for r in R if r["within"]]; y = ystd(W); X = H.Xmat(W, COLS); g = np.array([r["composer"] for r in W])
b, se, p, N, G = C8.ols_fe(y, X, g); rd["within_composer"] = dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(N), G=int(G))
NJ = [r for r in R if r["genre"] not in JAZZ8]; rd["non_jazz"] = fit(NJ, COLS)
share = float(np.mean([r["n_new"] > 0 for r in R]))
out = dict(folder="late_momentum08", after_seeing_results=True, seen_songs=True, lead=True, prediction=0.03, power_at_05_without_prior=pw,
           main=main, verdict=verdict, readings=rd, share_with_new_sets=share,
           n_new_total=int(sum(r["n_new"] for r in R)), n_prior_median=float(np.median([r["n_prior"] for r in R])))
json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=float)
print(H.jd(out))
