"""Run 11 test harness (frozen with the predictions). Each test folder holds spec.json and is run as:
    python3 harness11.py power <folder>   -> power.json (fake outcomes on the real rows; no outcome read)
    python3 harness11.py run <folder>     -> result.json (refuses unless <folder>/PREDICTION.md and common11.py are pushed)
spec.json: {"measure": cache key, "pred": signed beta (SD of z(y_foreign) per SD of the measure, within artist),
            "extra": [frozen extra controls, cache keys or pack measures], "alpha": .05/K, "counted": bool,
            "readings": [{"name", "kind": "extra"|"measure"|"intensive", ...}] (uncounted; decide nothing)}
Model, halves, second model (conditional logit, sign only), power and verdict: common11.py.
Reading kinds: extra = the measure with more frozen extras; measure = another cache key with the spec's extras;
intensive = among songs in Discogs-VI (y = 100), z(log(1 + covers)) on z(x), artist FE, extras + first_year (linear)."""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import common11 as C

def _need(spec):
    return [c for c in spec.get("extra", [])] + [c for rd in spec.get("readings", []) for c in rd.get("extra", []) if rd["kind"] == "extra"]

def design(spec):
    return C.design(spec["measure"], spec.get("extra", []))

def do_power(folder):
    spec = json.load(open(os.path.join(folder, "spec.json"))); R = design(spec)
    alpha = spec.get("alpha") or 0.05
    pw = C.power(R, spec["measure"], spec["pred"], alpha, extra=spec.get("extra", []))
    pw["alpha_used"] = alpha
    json.dump(pw, open(os.path.join(folder, "power.json"), "w"), indent=1); print(json.dumps(pw))

def do_run(folder):
    spec = json.load(open(os.path.join(folder, "spec.json")))
    pw = json.load(open(os.path.join(folder, "power.json")))
    print("power (frozen, before the outcome):", json.dumps(pw), flush=True)
    R = design(spec); info = C.load_outcomes(R, folder)
    x, ex, alpha = spec["measure"], spec.get("extra", []), (spec.get("alpha") or 0.05)
    main = C.fit(R, x, "y_foreign", ex); hv = C.halves(R, x, "y_foreign", ex); sec = C.second(R, x, "y_foreign", ex)
    pwr = pw["power"] if spec.get("counted") else 0.0
    vd = C.verdict(main, spec["pred"], alpha, pwr, hv, sec)
    Rv = [r for r in R if np.isfinite(r["y_foreign"])]
    res = dict(spec=spec, power=pw, outcome_info=info, main=main, halves=hv, second=sec, verdict=vd, n=len(Rv),
               share_taken_up=float(np.mean([r["y_foreign"] > 0 for r in Rv])), readings={})
    for rd in spec.get("readings", []):
        try:
            if rd["kind"] == "extra":
                S = [r for r in R if all(r.get(c) is not None and np.isfinite(r[c]) for c in rd["extra"])]
                res["readings"][rd["name"]] = C.fit(S, x, "y_foreign", list(ex) + list(rd["extra"]))
            elif rd["kind"] == "measure":
                S = [r for r in C.design(rd["measure"], rd.get("extra", ex))]
                C.load_outcomes(S, folder)
                res["readings"][rd["name"]] = C.fit(S, rd["measure"], "y_foreign", rd.get("extra", ex))
            elif rd["kind"] == "intensive":
                S = [r for r in R if r["y"] > 0 and r.get("lcov") is not None and r.get("first_year")]
                for r in S: r["fy"] = float(r["first_year"])
                res["readings"][rd["name"]] = C.fit(S, x, "lcov", list(ex) + ["fy"])
            res["readings"][rd["name"]]["pred_sign"] = rd.get("pred_sign")
        except Exception as e:
            res["readings"][rd["name"]] = {"error": str(e)}
    json.dump(res, open(os.path.join(folder, "result.json"), "w"), indent=1, default=float)
    print(json.dumps({"main": main, "verdict": vd, "halves": [h["beta"] for h in hv], "second": sec.get("beta")}, default=float))

if __name__ == "__main__":
    mode, folder = sys.argv[1], os.path.abspath(sys.argv[2])
    {"power": do_power, "run": do_run}[mode](folder)
