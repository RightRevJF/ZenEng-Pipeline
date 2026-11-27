"""Run 08, heritability (R08-I2; card 2): frozen by the chair. Rules: PREDICTION.md in this folder.
Run once, after the predictions commit is pushed:  python3 -I test.py   (from this folder)"""
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import numpy as np
import common as C, models08 as M8, power_run08 as PW

ALPHA = 0.05 / 5     # K = 5 (PREDICTION.md)
COUNTED = True
FROZEN_POWER = 0.65   # pseudo-decade cells (PREDICTION.md)
PRED = 0.06
NPERM = 10000

def main():
    t0 = time.time(); info, S = C.load_design(); MS = json.load(open(os.path.join(C.DL, "choco", "measures_run08.json")))
    NB = MS["neighbours"]
    print(f"[heritability] prediction rho_nb = +{PRED}; alpha {ALPHA}; status {'COUNTED' if COUNTED else 'ESTIMATE'}")
    pw = PW.heritability_sim(S, MS, 0.3, draws=50, pseudo_decade=True)
    print("POWER (fake outcomes, before the outcome):", json.dumps(pw["power_at_K"]), "| frozen:", FROZEN_POWER, flush=True)
    # ---- the outcome (guarded)
    R = [s for s in S if NB.get(s["clique"])]
    C.load_outcomes(R, HERE)
    order = [s["clique"] for s in R]
    A10, has = M8.nb_matrix(order, NB, 10); A5, has5 = M8.nb_matrix(order, NB, 5)
    comp = np.array([s["composer"] for s in R])
    D = np.column_stack([C.dummies([s["genre"] for s in R]), C.dummies([str(b) for b in
                         [("u" if s.get("first_year") is None else min(max(s["first_year"], 1900), 2020) // 5 * 5) for s in R]])])
    yw = C.within(np.array([s["y_cov"] for s in R])[:, None], comp)[:, 0]; Dw = C.within(D, comp)
    b, *_ = np.linalg.lstsq(Dw, yw, rcond=None); r = yw - Dw @ b
    cells = np.array([f'{s["composer"]}|{s["genre"]}|{d}' for s, d in zip(R, C.decade_bins(R))])
    hv = np.array([C.halves(c) for c in comp])
    specs = [(A10, has, None), (A10, has, hv == 0), (A10, has, hv == 1), (A5, has5, None)]
    T = M8.excess_test(r, specs, cells, NPERM, seed=2026)
    main_, halves, second = T[0], [T[1]["excess"], T[2]["excess"]], T[3]["excess"]
    v = C.verdict(main_["excess"], main_["null_sd"], main_["p"], PRED, ALPHA, halves, second, FROZEN_POWER if COUNTED else 0.0)
    out = dict(prediction=PRED, alpha=ALPHA, counted=COUNTED, frozen_power=FROZEN_POWER, power_rerun=pw["power_at_K"], main=main_,
               range95=[main_["excess"] - 1.96 * main_["null_sd"], main_["excess"] + 1.96 * main_["null_sd"]],
               halves=T[1:3], second_K5=T[3], verdict=v, N=int(has.sum()), nperm=NPERM)
    # ---- reported, deciding nothing
    m = np.array([s.get("first_year") is not None and s["first_year"] >= 1950 for s in R])
    out["t0_1950"] = M8.excess_test(r, [(A10, has, m)], cells, 2000, seed=7)[0]
    out["cells_genre_decade_only"] = M8.excess_test(r, [(A10, has, None)], np.array([f'{s["genre"]}|{d}' for s, d in zip(R, C.decade_bins(R))]), 2000, seed=7)[0]
    json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1)
    print(json.dumps(out, indent=1)); print("done", round(time.time() - t0), "s")

if __name__ == "__main__":
    main()
