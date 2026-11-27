"""Run 09 chair: fake-outcome power for every candidate test, before any outcome (harness09.fake_power logic; one set of 300 draws per
candidate, evaluated at alpha = .05/K for K = 1..8). Notes only. Writes power_run09.json.  python3 -I power_run09.py  (about 2 minutes)"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import harness09 as H
P8 = H.P8
STD = H.STD
NJ = lambda s: s["genre"] != "jazz"
CANDS = [  # name, rows, cols, beta, coefficient position
    ("iiv_confirm09 (IIV, all unseen)", lambda: H.design_rows(["IIV"] + STD), ["IIV"] + STD, 0.05, 0),
    ("tr_resolve (TR)", lambda: H.design_rows(["TR"] + STD), ["TR"] + STD, 0.035, 0),
    ("reading: IIV non-jazz genres", lambda: H.design_rows(["IIV"] + STD, keep=NJ), ["IIV"] + STD, 0.04, 0),
    ("reading: IIV on RB/BiaB charts only", lambda: H.design_rows(["IIV"] + STD, source="rbb"), ["IIV"] + STD, 0.035, 0),
    ("reading: DRES per bar", lambda: H.design_rows(["DRES"] + STD), ["DRES"] + STD, 0.035, 0),
    ("tq_tension (TQ | IIV)", lambda: H.design_rows(["TQ", "IIV"] + STD), ["TQ", "IIV"] + STD, 0.01, 0),
    ("irr_skeleton (IRR)", lambda: H.design_rows(["IRR"] + STD), ["IRR"] + STD, 0.02, 0),
    ("vr4c_momentum (VR4c | IIV)", lambda: H.design_rows(["VR4c", "IIV"] + STD), ["VR4c", "IIV"] + STD, 0.02, 0),
    ("typ_typical (TYP)", lambda: H.design_rows(["TYP"] + STD), ["TYP"] + STD, -0.02, 0),
    ("CARC (waits)", lambda: H.design_rows(["CARC"] + STD), ["CARC"] + STD, 0.02, 0),
    ("TE (waits)", lambda: H.design_rows(["TE"] + STD), ["TE"] + STD, 0.02, 0),
    ("seen lead gap_writer08: b_up", H.gap_rows, ["IIV_up", "GAP"] + H.GAP_CTRL + ["ln_n_ireal"], 0.045, 0),
    ("seen lead gap_writer08: b_gap", H.gap_rows, ["IIV_up", "GAP"] + H.GAP_CTRL + ["ln_n_ireal"], 0.03, 1),
    ("seen lead iiv_dres08: b_IIV | DRES", H.dres_rows, ["IIV", "DRES"] + H.SEEN_STD, 0.035, 0),
    ("seen lead iiv_dres08: b_DRES | IIV", H.dres_rows, ["IIV", "DRES"] + H.SEEN_STD, 0.04, 1),
]
out = {}
for name, rows, cols, beta, j in CANDS:
    R = rows(); X = H.Xmat(R, cols, decade=False); z = X[:, j]; rng = np.random.default_rng(H.SEED)
    bs, ps, ses, kz = [], [], [], 0
    for d in range(300):
        e = rng.normal(0, 1, len(z)); y = beta * z + math.sqrt(1 - beta ** 2) * e
        b, se, p, n = P8.ols_hc1(y, X); bs.append(b[j]); ps.append(p[j]); ses.append(se[j])
        b0, se0, p0, n0 = P8.ols_hc1(e, X); kz += abs(beta - b0[j]) > 1.96 * se0[j]
    bs, ps, ses = map(np.array, (bs, ps, ses))
    good = np.sign(bs) == np.sign(beta)
    out[name] = dict(N=len(R), beta=beta, se_fake=round(float(np.median(ses)), 4),
                     power_at_K={K: round(float(np.mean((ps < 0.05 / K) & good)), 3) for K in range(1, 9)},
                     kill_if_true=round(float(np.mean(np.abs(beta - bs) > 1.96 * ses)), 3), kill_if_zero=round(kz / 300, 3))
    print(name, json.dumps(out[name]), flush=True)
json.dump(dict(note="fake-outcome power on the real rows and frozen columns (no decade dummies: first_year comes with the outcome); "
                    "300 draws, seed 11; power = share with p < .05/K and the predicted sign", candidates=out),
          open(os.path.join(HERE, "power_run09.json"), "w"), indent=1)
