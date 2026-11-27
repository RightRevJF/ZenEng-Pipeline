"""Run 08, cover_timeline (R08-L2 merged with R08-G3; card 2): frozen by the chair. Rules: PREDICTION.md in this folder.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common as C, models08 as M8, power_run08 as PW

ALPHA = 0.05 / 5     # K = 5 (PREDICTION.md)
COUNTED = True
FROZEN_POWER = 0.25   # middle scenario (PREDICTION.md)
PRED = 1.10
GAMMA = [("TRAV5", ["TRAVL1", "ch_rep", "V", "ln_chg", "ln_bars"]), ("econ", ["w_chr", "ch_rep", "V", "ln_chg", "ln_bars"]),
         ("T_rep", ["ch_rep", "V", "ln_chg", "ln_bars"]), ("IIV", ["w_chr", "ch_rep", "V", "ln_chg", "ln_bars"]), ("ch_rep", [])]

def bins5(t0): return [str(min(max(t, 1900), 2020) // 5 * 5) for t in t0]

def fit(rows, kcol, lcol):
    L = np.array([r[lcol] for r in rows], float); K = np.array([r[kcol] for r in rows], float)
    X = np.column_stack([np.log(K + 1.0), C.dummies(bins5([r["t0"] for r in rows]))]); g = np.array([r["composer"] for r in rows])
    b, se, N, G, it = M8.poisson_fe(L, X, g)
    return dict(beta=float(b[0]), se=float(se[0]), p_vs_1=M8.p_two(b[0], se[0], 1.0), N=N, G=G, iterations=it,
                range95=[float(b[0] - 1.96 * se[0]), float(b[0] + 1.96 * se[0])]), X, g, L

def main():
    t0 = time.time(); info, S = C.load_design(); MS = json.load(open(os.path.join(C.DL, "choco", "measures_run08.json")))
    for s in S: s.update(MS["songs"][s["clique"]])
    print(f"[cover_timeline] prediction beta = {PRED}; alpha {ALPHA}; status {'COUNTED' if COUNTED else 'ESTIMATE'}; design songs {len(S)}")
    # ---- power before the outcome (fake urn on the design, the frozen scenarios)
    pw = {sc: PW.timeline_sim(S, 1.10, *v, draws=100)["power_at_K"] for sc, v in PW.SCEN.items()}
    print("POWER (fake urn, before the outcome):", json.dumps(pw), "| frozen:", FROZEN_POWER, flush=True)
    # ---- the outcome (guarded)
    C.load_outcomes(S, HERE); C.load_timelines(S, HERE)
    rows = []
    for s in S:
        if s.get("first_year") is None or not s["years"]: continue
        r = dict(s); r["t0"] = s["first_year"]; r.update(M8.timeline_counts(s["years"], s["first_year"])); rows.append(r)
    prim = [r for r in rows if 1950 <= r["t0"] <= 1994]; ally = [r for r in rows if r["t0"] <= 1994]
    sec = [r for r in rows if 1950 <= r["t0"] <= 1989]
    # power on the real K10 (fake L under beta = 1.10, Poisson-gamma shape 1, scaled to the real mean of L): printed before beta
    rng = np.random.default_rng(9); K = np.array([r["K10"] for r in prim], float); gg = np.array([r["composer"] for r in prim])
    Xp = np.column_stack([np.log(K + 1.0), C.dummies(bins5([r["t0"] for r in prim]))]); mL = float(np.mean([r["L"] for r in prim])); hits = 0
    for d in range(100):
        lam = (K + 1.0) ** 1.10; lam *= mL / lam.mean(); Lf = rng.poisson(rng.gamma(1.0, lam))
        b, se, *_ = M8.poisson_fe(Lf, Xp, gg); hits += (M8.p_two(b[0], se[0], 1.0) < ALPHA) and b[0] > 1
    print(f"POWER on the real K10 (fake L, reported only): {hits / 100:.2f}; primary songs {len(prim)}; mean K10 "
          f"{np.mean(K):.2f}; mean L {mL:.2f}", flush=True)
    main_, X, g, L = fit(prim, "K10", "L")
    hv = np.array([C.halves(r["composer"]) for r in prim]); halves = []
    for h in (0, 1):
        b, se, N, G, it = M8.poisson_fe(L[hv == h], X[hv == h], g[hv == h]); halves.append(dict(beta=float(b[0]), se=float(se[0]), N=N, G=G))
    second, *_ = fit(sec, "K15", "L15")
    passed = bool(COUNTED and main_["p_vs_1"] < ALPHA and main_["beta"] > 1 and all(h["beta"] > 1 for h in halves) and second["beta"] > 1)
    inside = main_["range95"][0] <= PRED <= main_["range95"][1]; neutral_inside = main_["range95"][0] <= 1.0 <= main_["range95"][1]
    if not COUNTED: verdict = "estimate (under the power floor): passes nothing, kills nothing"
    elif passed: verdict = "PASS (beta > 1: late covers grow faster than early covers; heterogeneous fitness)"
    elif not inside: verdict = "KILLED (1.10 lies outside the 95% range)"
    else: verdict = "unsettled (no pass; 1.10 lies inside the 95% range)"
    out = dict(prediction=PRED, alpha=ALPHA, counted=COUNTED, frozen_power=FROZEN_POWER, power_rerun=pw, real_K10_power=hits / 100,
               primary=main_, halves=halves, second=second, verdict=verdict, neutral_1_inside_95=neutral_inside,
               n_primary=len(prim), n_all_years=len(ally), mean_K10=float(np.mean(K)), mean_L=mL)
    # ---- reported, deciding nothing
    out["all_years"] = fit(ally, "K10", "L")[0]
    out["by_t0"] = {}
    for lo, hi in ((1900, 1949), (1950, 1969), (1970, 1994)):
        sub = [r for r in rows if lo <= r["t0"] <= hi]
        if len(sub) > 100: out["by_t0"][f"{lo}-{hi}"] = fit(sub, "K10", "L")[0]
    coh = np.array(bins5([r["t0"] for r in prim]))
    out["urn_ceiling"] = M8.urn_ceiling([r["K10"] for r in prim], [r["L"] for r in prim], coh, c0=1.0, reps=200)
    out["gamma"] = {}
    for m, ex in GAMMA:
        sub = [r for r in prim if all(r.get(c) is not None for c in [m] + ex)]
        Ls = np.array([r["L"] for r in sub], float); Ks = np.array([r["K10"] for r in sub], float)
        Xg = np.column_stack([np.log(Ks + 1.0), C.zs([r[m] for r in sub])] + [C.zs([r[e] for r in sub]) for e in ex] +
                             [C.dummies(bins5([r["t0"] for r in sub])), C.dummies([r["genre"] for r in sub])])
        b, se, N, G, it = M8.poisson_fe(Ls, Xg, np.array([r["composer"] for r in sub]))
        out["gamma"][m] = dict(beta=float(b[0]), gamma=float(b[1]), se_gamma=float(se[1]), p_gamma=M8.p_two(b[1], se[1]), N=N, G=G)
    json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
    print(json.dumps(out, indent=1)); print("done", round(time.time() - t0), "s")

if __name__ == "__main__":
    main()
