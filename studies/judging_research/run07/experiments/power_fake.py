"""Run 07 chair: fake-outcome power for the eight counted tests (C.fake_power; fake outcomes only, no outcome read).
Usage: python3 -I power_fake.py power_fake.json  (about 1.5 minutes)"""
import sys, json, time
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/judging_research/run07/experiments")
import numpy as np, common as C
from scipy.stats import norm
S = C.add_shapes(C.lakh_songs())
N = 8; ALPHA = 0.05 / N
T = [("lakh_repetition", "ch_rep", (), 1.0, 1), ("tree_h4m", "H4m", ("cv_w", "ch_rep"), -0.5, -1), ("spectral_gap", "g", ("ch_rep",), -0.3, -1),
     ("lakh_chirality", "CH", ("A", "ch_rep"), -0.6, -1), ("lakh_arrow", "A", (), 0.6, 1), ("loop_period", "lnP", ("ln_tempo",), 0.6, 1),
     ("burstiness", "B", (), 0.3, 1), ("triad_fidelity", "F", (), 0.5, 1)]
KILL = dict(lakh_chirality=-0.2)
out = dict(note="C.fake_power on the 5,901 within-artist Lakh songs: artist baselines Beta(0.25, 1.0) (base 0.20, precision 1.25, run 06's calibration), "
                "y ~ Bernoulli(baseline + beta/100 * z); pass = two-sided p < alpha, predicted sign, same sign in both artist halves (no logit). "
                "300 draws under the prediction, 150 under zero, seed 7. Kill-fire rates are normal approximations from the mean SE.",
           n_counted=N, alpha=ALPHA, tests={})
for name, m, ex, b, sg in T:
    t0 = time.time()
    names, X = C.design(S, m, ex); rows = int(np.isfinite(X).all(1).sum())
    g = np.array([s["artist_key"] for s in S])[np.isfinite(X).all(1)]
    pa = C.fake_power(S, m, ex, b, ALPHA, sg, draws=300)
    p05 = C.fake_power(S, m, ex, b, 0.05, sg, draws=300)
    se = pa["se"]; k = KILL.get(name, 0.0)
    if sg > 0: kt, k0 = norm.cdf((k - b) / se), norm.cdf((k - 0) / se)
    else: kt, k0 = 1 - norm.cdf((k - b) / se), 1 - norm.cdf((k - 0) / se)
    r = dict(measure=m, extra=list(ex), prediction=b, sign=sg, rows=rows, artists=int(len(set(g))), at_alpha=pa, at_05=p05, se=round(se, 3),
             kill_line=k, kill_fires_if_true=round(float(kt), 3), kill_fires_if_zero=round(float(k0), 3), columns=names[:len(ex) + 4])
    if name == "lakh_repetition":
        r["at_alpha_if_0.4"] = C.fake_power(S, m, ex, 0.4, ALPHA, sg, draws=300)
        r["at_05_if_0.4"] = C.fake_power(S, m, ex, 0.4, 0.05, sg, draws=300)
    out["tests"][name] = r
    print(name, json.dumps(r, default=float), round(time.time() - t0), flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=1, default=float)
