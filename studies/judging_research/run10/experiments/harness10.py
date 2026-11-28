"""Run 10 test harness (frozen with the predictions). Each test folder holds spec.json and calls:
    python3 harness10.py power <folder>   -> power.json (fake outcomes on the real rows; no outcome read)
    python3 harness10.py run <folder>     -> result.json (refuses unless <folder>/PREDICTION.md is committed and pushed)
spec.json: {"measure": key in measures_run10.json, "pred": signed beta (SD of z(y_cov) per SD), "extra": [frozen extra controls],
            "alpha": .05/K or null (estimates), "counted": bool, "split": "A" (or "C" for a confirmation),
            "readings": [{"name":..., "kind": "subset"|"extra"|"love", ...}] (uncounted)}
Model, halves, second model, power and verdict: common10.py (docstring). The love reading (y_love on tunes with >= 10 tunebooks)
is reported beside the main test with its own predicted sign and decides nothing.
"""
import sys, os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import common10 as C

CACHE = "/home/claude/dl/thesession/measures_run10.json"

def design(spec, split=None):
    split = split or spec.get("split", "A")
    M = json.load(open(CACHE)); T = C.tunes(); R = []
    need = [spec["measure"]] + list(spec.get("extra", []))
    for tid, t in T.items():
        if t["split"] != split: continue
        m = M.get(str(tid))
        if m is None: continue
        r = {k: t[k] for k in ("tune_id", "type", "meter", "mode", "year", "composer", "half")}
        r.update(m)
        if all(r.get(c) is not None and np.isfinite(r[c]) for c in need): R.append(r)
    return R

def do_power(folder):
    spec = json.load(open(os.path.join(folder, "spec.json"))); R = design(spec)
    alpha = spec["alpha"] if spec.get("alpha") else 0.05
    pw = C.power(R, spec["measure"], spec["pred"], alpha, extra=spec.get("extra", []))
    pw["alpha_used"] = alpha
    json.dump(pw, open(os.path.join(folder, "power.json"), "w"), indent=1)
    print(json.dumps(pw))

def do_run(folder):
    spec = json.load(open(os.path.join(folder, "spec.json"))); split = spec.get("split", "A")
    pw = json.load(open(os.path.join(folder, "power.json")))
    print("power (frozen, before the outcome):", json.dumps(pw), flush=True)
    R = design(spec)
    O = C.load_outcomes(folder, splits=(split,))
    for r in R:
        o = O[r["tune_id"]]; r["n_art"] = o["n_art"]; r["y_cov"] = o["y_cov_raw"]
        r["y_love"] = math.log(o["tunebooks"]) if o["tunebooks"] else None
    x, ex, alpha = spec["measure"], spec.get("extra", []), (spec.get("alpha") or 0.05)
    main = C.fit(R, x, "y_cov", ex); hv = C.halves(R, x, "y_cov", ex); po = C.poisson_sign(R, x, "n_art", ex)
    pwr = pw["power"] if spec.get("counted") else 0.0
    vd = C.verdict(main, spec["pred"], alpha, pwr, hv, po)
    res = dict(spec=spec, power=pw, main=main, halves=hv, poisson=po, verdict=vd, n=len(R),
               mean_artists=float(np.mean([r["n_art"] for r in R])), share_recorded=float(np.mean([r["n_art"] > 0 for r in R])))
    RL = [r for r in R if r["y_love"] is not None]
    if len(RL) > 200:
        res["love"] = dict(main=C.fit(RL, x, "y_love", ex), halves=C.halves(RL, x, "y_love", ex),
                           pred_sign=spec.get("love_sign", int(np.sign(spec["pred"]))), n=len(RL))
    res["readings"] = {}
    for rd in spec.get("readings", []):
        try:
            if rd["kind"] == "subset":
                S = [r for r in R if r.get(rd["key"]) == rd["value"] or (rd.get("in") and r.get(rd["key"]) in rd["in"])]
                res["readings"][rd["name"]] = dict(C.fit(S, x, "y_cov", ex), n=len(S))
            elif rd["kind"] == "extra":
                S = [r for r in R if all(r.get(c) is not None and np.isfinite(r[c]) for c in rd["extra"])]
                res["readings"][rd["name"]] = C.fit(S, x, "y_cov", list(ex) + list(rd["extra"]))
            elif rd["kind"] == "measure":
                S = [r for r in R if r.get(rd["measure"]) is not None and np.isfinite(r[rd["measure"]])]
                res["readings"][rd["name"]] = C.fit(S, rd["measure"], "y_cov", rd.get("extra", ex))
        except Exception as e:
            res["readings"][rd["name"]] = {"error": str(e)}
    json.dump(res, open(os.path.join(folder, "result.json"), "w"), indent=1, default=float)
    print(json.dumps({"main": main, "verdict": vd, "halves": [h["beta"] for h in hv], "poisson": po.get("beta")}, default=float))

if __name__ == "__main__":
    mode, folder = sys.argv[1], os.path.abspath(sys.argv[2])
    {"power": do_power, "run": do_run}[mode](folder)
