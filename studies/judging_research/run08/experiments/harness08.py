"""Run 08 test harness, frozen by the chair before any outcome is joined. Each test folder's test.py calls one function here.
The outcome is read ONLY through common.load_outcomes / common.load_timelines, which refuse unless the folder's PREDICTION.md and
common.py are committed, unmodified and pushed. Power is printed BEFORE any outcome is loaded.

run_ycov      a y_cov test: within-composer OLS (common.ols_fe, CR1 by composer) of y_cov on z(measure), z(frozen extra columns),
              genre dummies and first-year decade dummies (common.design_matrix); the two composer halves (common.halves); the
              second model = models08.poisson_fe on n_sets with the same columns; common.verdict with the frozen status.
"""
import sys, os, json, math, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import common as C, models08 as M8

def design_songs(cols):
    info, S = C.load_design(); MS = json.load(open(os.path.join(C.DL, "choco", "measures_run08.json")))
    for s in S: s.update(MS["songs"][s["clique"]])
    return [s for s in S if all(s.get(c) is not None for c in cols)], MS

def fit_ycov(R, meas, extra):
    y = np.array([s["y_cov"] for s in R]); X = C.design_matrix(R, meas, extra); g = np.array([s["composer"] for s in R])
    b, se, p, N, G = C.ols_fe(y, X, g)
    return dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(N), G=int(G)), X, g

def run_ycov(folder, meas, extra, pred, alpha, frozen_power, counted, readings=(), draws=300, estimate_reason=None):
    t0 = time.time(); cols = [meas] + list(extra)
    R, MS = design_songs(cols)
    print(f"[{os.path.basename(folder)}] measure {meas}; extra {list(extra)}; prediction {pred:+.3f} SD per SD; alpha {alpha:.5f}; "
          f"status frozen as {'COUNTED' if counted else 'ESTIMATE'}; songs {len(R)}", flush=True)
    # ---- power, before the outcome (fake outcomes on these rows and columns)
    pw = {str(cs): C.fake_power(R, meas, extra, pred, alpha, sign=np.sign(pred), draws=draws, comp_share=cs) for cs in (0.3, 0.5)}
    print("POWER (fake outcomes, before the outcome is joined):", json.dumps({k: {kk: (float(v) if isinstance(v, (float, np.floating)) else v)
          for kk, v in d.items()} for k, d in pw.items()}), "| frozen in PREDICTION.md:", frozen_power, flush=True)
    # ---- the outcome (guarded)
    C.load_outcomes(R, folder)
    main, X, g = fit_ycov(R, meas, extra)
    hv = np.array([C.halves(s["composer"]) for s in R]); halves = []
    for h in (0, 1):
        i = hv == h; b, se, p, N, G = C.ols_fe(np.array([s["y_cov"] for s in R])[i], X[i], g[i])
        halves.append(dict(b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(N), G=int(G)))
    pb, pse, pN, pG, pit = M8.poisson_fe(np.array([s["n_sets"] for s in R], float), X, g)
    second = dict(model="Poisson QMLE on n_sets, composer FE, same columns", b=float(pb[0]), se=float(pse[0]),
                  p=M8.p_two(pb[0], pse[0]), N=pN, G=pG, iterations=pit)
    v = C.verdict(main["b"], main["se"], main["p"], pred, alpha, [h["b"] for h in halves], second["b"],
                  frozen_power if counted else 0.0)
    if not counted and estimate_reason: v["verdict"] = "estimate (" + estimate_reason + "): passes nothing, kills nothing"
    out = dict(folder=os.path.basename(folder), measure=meas, extra=list(extra), prediction=pred, alpha=alpha, counted=counted,
               frozen_power=frozen_power, power_rerun={k: {kk: (float(v2) if isinstance(v2, (float, np.floating)) else v2) for kk, v2 in d.items()}
                                                       for k, d in pw.items()},
               main=main, halves=halves, second=second, verdict=v, range95=[main["b"] - 1.96 * main["se"], main["b"] + 1.96 * main["se"]],
               n_sets_median=float(np.median([s["n_sets"] for s in R])), readings={})
    # ---- reported readings, deciding nothing
    for lab, rm, rex, mask in readings:
        RR = [s for s in R if all(s.get(c) is not None for c in [rm] + list(rex)) and (mask is None or mask(s))]
        if len(RR) < 50: continue
        m = np.array([s["ln_sets"] for s in RR]); yv = (m - m.mean()) / m.std()
        for s, yy in zip(RR, yv): s["_y"] = yy
        Xr = C.design_matrix(RR, rm, rex); gr = np.array([s["composer"] for s in RR])
        b, se, p, N, G = C.ols_fe(np.array([s["_y"] for s in RR]), Xr, gr)
        out["readings"][lab] = dict(measure=rm, extra=list(rex), b=float(b[0]), se=float(se[0]), p=float(p[0]), N=int(N), G=int(G))
    json.dump(out, open(os.path.join(folder, "result.json"), "w"), indent=1)
    print(json.dumps(dict(main=main, halves=halves, second=second, verdict=v), indent=1))
    print("readings:", json.dumps(out["readings"], indent=1)); print("done", round(time.time() - t0), "s")
    return out

# masks for the shared readings
def writer_only(s): return s["match"] == "writer"
def t0_1950(s): return s.get("first_year") is not None and s["first_year"] >= 1950
