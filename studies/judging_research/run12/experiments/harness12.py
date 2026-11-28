"""Run 12 test harness (frozen with the predictions before any outcome is joined).
    python3 harness12.py power <folder>   -> power.json (fake outcomes on the real rows; NO outcome is read)
    python3 harness12.py run <folder>     -> result.json (refuses unless <folder>/PREDICTION.md, <folder>/spec.json, common12.py and
                                             harness12.py are committed, unmodified and pushed to origin/judging-research)
    python3 harness12.py dry <folder>     -> dry_result.json in the scratch dir given by $DRY_DIR: the run code on a SYNTHETIC outcome
                                             (random numbers; no outcome read), to prove the code runs.
spec.json "kind":
  v1        : Hooktheory rows with FIT. D = z(FIT) - z(log(1+N)) (z over the test rows), OLS of D (not re-standardised) on z(x),
              artist FE, run 04's controls, exact first-year dummies. Kill = range AND wrong side (Jason's words). No second model
              (D is continuous). Readings: beta on z(FIT) and on z(log1p N) separately (same rows and design).
  windows   : Hooktheory rows with FIT and t0 <= 2005. Per window w (E: ages 0-3, L: ages 8+), FE Poisson (artist) of N_w on z(x),
              run 04's controls and five-year first-year dummies, offset log X_w (fit.json's exposure). Delta = b_L - b_E, SE by
              paired artist bootstrap (500, seed 12) (analytic joint sandwich printed beside). Estimate.
  lakh      : Lakh within-artist songs; OLS of z(y_foreign) on z(x) (+ frozen extras), artist FE, run 07's controls + 5-year year
              bins + (if skeptic) LNEV, NPB, ACT, NFILES; conditional logit for sign; halves md5(artist) mod 2.
  fifths    : as lakh with x = E5_L and REST_L, TOP_L held; plus the Geometer's Wald test on the raw scale (b_E5 vs b_REST).
  hook      : Hooktheory rows; OLS of z(y_foreign) on z(x) + extras, artist FE, run 04's controls (common11's model).
  canal     : notes-side pilot (no outcome): `run` computes it.
"""
import os, sys, json, math, copy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy import stats
from scipy.special import digamma
import common12 as C

ALPHAS = [0.05 / k for k in range(1, 8)]
DRY = os.environ.get("DRY_DIR")


def spec_of(folder): return json.load(open(os.path.join(folder, "spec.json")))


# ---------------------------------------------------------------- controls by kind
def ctrl_v1(R): return C.hook_controls(R, (), year="exact")
def ctrl_win(R): return C.hook_controls(R, (), year="five")
def ctrl_lakh(extra, skeptic=True): return lambda R: C.lakh_controls(R, extra, skeptic)
def ctrl_hook(extra): return lambda R: C.hook_controls(R, extra, year=None)


# ---------------------------------------------------------------- the FIT simulations (power only; no outcome)
def _calib(R, rng):
    sh = C.shares(); mean = sh["hook_matched_rows"] / len(R)
    sel = C.calibrate_selection([r["artist"] for r in R], mean, sh["hook_matched_any (y)"][0], rng)
    target = sh["logcov_within_share_among_matched"][0]; best = None
    for rho in np.linspace(0.0, 0.9, 19):
        ws, wf = [], []
        for _ in range(2):
            M = C.within_artist(C.sim_matched(R, rng, sel["tau"], mean, rho))
            for r in M:
                E = C.exp_cached(r["t0"], 0, None); r["N"] = float(rng.poisson(r["eta"] * E)); r["lN"] = math.log1p(r["N"])
                r["FIT"] = float(digamma(C.fit_summary()["r"] + r["N"]) - math.log(C.fit_summary()["r"] + E))
            gg = _codes(M); ws.append(C._within_share([r["lN"] for r in M], gg)); wf.append(C._within_share([r["FIT"] for r in M], gg))
        d = abs(np.mean(ws) - target)
        if best is None or d < best[0]: best = (d, float(rho), float(np.mean(ws)), float(np.mean(wf)))
    return dict(mean=mean, tau=sel["tau"], selection_within_achieved=sel["within_achieved"], rho_artist_eta=best[1],
                logcov_within_achieved=best[2], FIT_within_achieved=best[3], logcov_within_target=target,
                FIT_within_target=sh["FIT_within_share_among_matched"][0])


def _codes(M):
    codes = {a: i for i, a in enumerate(sorted(set(r["artist"] for r in M)))}; return np.array([codes[r["artist"]] for r in M])


def _world(R, rng, cal, era, P):
    M = C.within_artist(C.sim_matched(R, rng, cal["tau"], cal["mean"], cal["rho_artist_eta"], era=era))
    for r in M:
        E = C.exp_cached(r["t0"], 0, None); r["N"] = float(rng.poisson(r["eta"] * E)); r["lN"] = math.log1p(r["N"])
        r["FIT"] = float(digamma(P["r"] + r["N"]) - math.log(P["r"] + E))
    return M


def power_v1(spec, draws=300):
    R = C.hook_design([spec["measure"]]); rng = np.random.default_rng(C.SEED); P = C.fit_summary(); cal = _calib(R, rng); out = {}
    for era in ("artist", "recent"):
        hits = {a: 0 for a in ALPHAS}; ses = []; kz = 0; sdD = []; ns = []
        for _ in range(draws):
            M = _world(R, rng, cal, era, P); x = C._z([r[spec["measure"]] for r in M])
            D = C._z([r["FIT"] for r in M]) - C._z([r["lN"] for r in M]); sdD.append(float(D.std()))
            for r, d, xi in zip(M, D, x): r["Dtrue"] = d + spec["pred"] * xi; r["Dzero"] = d
            f = C.fe_fit(M, [spec["measure"]], "Dtrue", ctrl_v1, zy=False); ses.append(f["se"]); ns.append(f["n"])
            for a in ALPHAS: hits[a] += (f["p"] < a and np.sign(f["beta"]) == np.sign(spec["pred"]))
            f0 = C.fe_fit(M, [spec["measure"]], "Dzero", ctrl_v1, zy=False)
            kz += (not (f0["lo"] <= spec["pred"] <= f0["hi"])) and np.sign(f0["beta"]) != np.sign(spec["pred"])
        out[era] = dict(power={str(round(a, 6)): hits[a] / draws for a in ALPHAS}, median_fake_se=float(np.median(ses)),
                        kill_if_zero=kz / draws, median_sd_D=float(np.median(sdD)), median_n=float(np.median(ns)))
    pw = {k: min(out["artist"]["power"][k], out["recent"]["power"][k]) for k in out["artist"]["power"]}
    return dict(power=pw, scenarios=out, calibration=cal, draws=draws, seed=C.SEED, n_rows_all=len(R),
                note=("Model-based fake outcomes (fit.json's r, A, g, h): which songs are matched (artist-clustered probit tuned to "
                      "2,091 matched rows and the within-artist share 0.38 of y), first years (fake: an artist era 1960-2012 plus 0-8 "
                      "years, or 1985-2012 plus 0-3 = 'recent'), fitness eta ~ Gamma(r, r) with artist correlation tuned to the "
                      "within-artist share 0.427 of log covers, N ~ Poisson(eta E(t0)), FIT = digamma(r + N) - log(r + E). The fake "
                      "D carries the predicted -0.01 z(x) on top of the model's own D. power = the lower of the two scenarios."))


def power_windows(spec, draws=300):
    R = C.hook_design(spec["measures"]); rng = np.random.default_rng(C.SEED); P = C.fit_summary(); cal = _calib(R, rng); out = {}
    for m in spec["measures"]:
        pred = spec["pred"][m]
        if pred == 0: out[m] = dict(power=None, note="prediction Delta = 0: no directional pass is possible; an estimate"); continue
        bE = spec["sim_beta_E"]; bL = bE + pred; hits = {a: 0 for a in ALPHAS}; ses = []; ns = []
        for _ in range(draws):
            M = [r for r in _world(R, rng, cal, "artist", P) if r["t0"] <= 2005]; M = C.within_artist(M)
            x = C._z([r[m] for r in M])
            for r, xi in zip(M, x):
                r["X_E"] = C.exp_cached(r["t0"], 0, 3); r["X_L"] = C.exp_cached(r["t0"], C.LATE_FROM, None)
                r["N_E"] = float(rng.poisson(r["eta"] * math.exp(bE * xi) * r["X_E"])); r["N_L"] = float(rng.poisson(r["eta"] * math.exp(bL * xi) * r["X_L"]))
            d = windows_fit(M, m, analytic_only=True); ses.append(d["se_analytic"]); ns.append(d["n"])
            for a in ALPHAS: hits[a] += (d["p_analytic"] < a and np.sign(d["delta"]) == np.sign(pred))
        out[m] = dict(power={str(round(a, 6)): hits[a] / draws for a in ALPHAS}, median_se_delta=float(np.median(ses)),
                      median_n=float(np.median(ns)), sim_beta_E=bE, sim_beta_L=bL)
    return dict(per_measure=out, calibration=cal, draws=draws, seed=C.SEED,
                note="model-based fake counts as power_v1 ('artist' era scenario), t0 <= 2005; Delta SE by the analytic joint sandwich")


def windows_fit(M, m, analytic_only=False, boot=0, seed=C.SEED, ctrl=ctrl_win):
    """per window FE Poisson of N_w on [z(x), controls], offset log X_w; Delta = b_L - b_E."""
    g = [r["artist"] for r in M]; x = C._z([r[m] for r in M]); Cm = ctrl(M)
    X = np.column_stack([x, Cm])
    res = {}
    for w in ("E", "L"):
        res[w] = C.pois_fe([r["N_" + w] for r in M], X, np.log([r["X_" + w] for r in M]), g)
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; G = len(codes)
    def full(o):
        S = np.zeros((G, o["S"].shape[1])); S[o["groups_kept"]] = o["S"]; return S
    SE_, SL = full(res["E"]), full(res["L"])
    cov = (G / (G - 1)) * (res["L"]["Hi"] @ SL.T @ SE_ @ res["E"]["Hi"])[0, 0]
    bE, bL = float(res["E"]["b"][0]), float(res["L"]["b"][0]); vE, vL = float(res["E"]["V"][0, 0]), float(res["L"]["V"][0, 0])
    delta = bL - bE; se_a = math.sqrt(max(vL + vE - 2 * cov, 1e-12))
    out = dict(delta=delta, se_analytic=se_a, p_analytic=float(2 * stats.norm.sf(abs(delta / se_a))), n=len(M), artists=G,
               beta_E=bE, se_E=math.sqrt(vE), beta_L=bL, se_L=math.sqrt(vL), groups_E=res["E"]["G"], groups_L=res["L"]["G"],
               covers_E=float(sum(r["N_E"] for r in M)), covers_L=float(sum(r["N_L"] for r in M)))
    if analytic_only or not boot: return out
    rng = np.random.default_rng(seed); arts = sorted(codes); idx = {a: [i for i, r in enumerate(M) if r["artist"] == a] for a in arts}; ds = []
    for b in range(boot):
        pick = rng.integers(0, len(arts), len(arts)); B = []
        for j, k in enumerate(pick):
            for i in idx[arts[k]]: q = dict(M[i]); q["artist"] = f"{arts[k]}#{j}"; B.append(q)
        try:
            xb = C._z([r[m] for r in B]); Xb = np.column_stack([xb, ctrl(B)])
            gb = [r["artist"] for r in B]
            eE = C.pois_fe([r["N_E"] for r in B], Xb, np.log([r["X_E"] for r in B]), gb)["b"][0]
            eL = C.pois_fe([r["N_L"] for r in B], Xb, np.log([r["X_L"] for r in B]), gb)["b"][0]
            ds.append(float(eL - eE))
        except Exception:
            continue
    sb = float(np.std(ds, ddof=1)); out.update(se_boot=sb, p_boot=float(2 * stats.norm.sf(abs(delta / sb))), boot_reps=len(ds),
                                               lo=delta - 1.96 * sb, hi=delta + 1.96 * sb, boot_seed=seed)
    return out


# ---------------------------------------------------------------- designs
def lakh_cols(spec): return [spec["measure"]] + list(spec.get("extra", [])) + C.LAKH_BASE + C.LAKH_SKEPTIC


def design(spec):
    k = spec["kind"]
    if k == "lakh" or k == "fifths": return C.lakh_design(lakh_cols(spec))
    if k == "hook": return C.hook_design([spec["measure"]] + list(spec.get("extra", [])))
    raise ValueError(k)


def do_power(folder):
    spec = spec_of(folder); k = spec["kind"]
    if k == "v1": pw = power_v1(spec)
    elif k == "windows": pw = power_windows(spec)
    elif k in ("lakh", "fifths"):
        R = design(spec); w = C.shares()["lakh_y_foreign"][0]
        pw = C.power_ols(R, [spec["measure"]], spec["pred"], ALPHAS, ctrl_lakh(spec.get("extra", [])), w)
    elif k == "hook":
        R = design(spec); w = C.shares()["hook_matched_any (y)"][0]
        pw = C.power_ols(R, [spec["measure"]], spec["pred"], ALPHAS, ctrl_hook(spec.get("extra", [])), w)
        pw["no_artist_share"] = C.power_ols(R, [spec["measure"]], spec["pred"], ALPHAS, ctrl_hook(spec.get("extra", [])), 1.0)["power"]
        pw["note"] = "within-artist share 0.38 = y's (outcome_side_shares.json); y_foreign's own share is not in that file"
    elif k == "canal": pw = dict(power=None, note="notes-side pilot; no outcome")
    pw["alpha_frozen"] = spec.get("alpha"); pw["alphas_key"] = {f"K={i+1}": str(round(a, 6)) for i, a in enumerate(ALPHAS)}
    json.dump(pw, open(os.path.join(folder, "power.json"), "w"), indent=1, default=float)
    print(json.dumps({kk: pw[kk] for kk in pw if kk in ("power", "per_measure", "median_fake_se", "n", "artists")}, default=float))


# ---------------------------------------------------------------- runs
def _synthetic(R, kind, rng):
    for r in R:
        r["y_foreign"] = float(rng.random() < 0.3) * 100; r["y"] = 100.0
    if kind in ("v1", "windows"):
        for r in R:
            r["t0"] = int(rng.integers(1960, 2015)); r["N"] = float(rng.poisson(5)); r["lN"] = math.log1p(r["N"])
            r["FIT"] = float(digamma(0.66 + r["N"]) - math.log(0.66 + 5)); r["N_E"] = float(rng.poisson(1)); r["N_L"] = float(rng.poisson(3))
            r["X_E"] = 3.0; r["X_L"] = 10.0


def do_run(folder, dry=False):
    spec = spec_of(folder); k = spec["kind"]
    pw = json.load(open(os.path.join(folder, "power.json")))
    print("power (frozen, before the outcome):", json.dumps(pw.get("power", pw.get("per_measure")), default=float), flush=True)
    rng = np.random.default_rng(0)
    if k == "canal": return run_canal(folder, spec)
    res = dict(spec=spec, power=pw, readings={}, dry_run_synthetic_outcome=bool(dry))
    alpha = spec.get("alpha") or 0.05
    if k in ("v1", "windows"):
        R = C.hook_design([spec["measure"]] if k == "v1" else spec["measures"])
        if dry: _synthetic(R, k, rng); res["outcome_info"] = "SYNTHETIC"
        else: res["outcome_info"] = C.load_hook(R, folder)
        T = [r for r in R if np.isfinite(r.get("FIT", np.nan))]
    if k == "v1":
        T = C.within_artist(T); m = spec["measure"]
        D = C._z([r["FIT"] for r in T]) - C._z([r["lN"] for r in T])
        for r, d in zip(T, D): r["D"] = float(d)
        main = C.fe_fit(T, [m], "D", ctrl_v1, zy=False); hv = C.halves_fit(T, [m], "D", ctrl_v1, zy=False)
        vd = C.verdict(main, spec["pred"], alpha, spec["counted"] and pw["power"][str(round(alpha, 6))] >= 0.2, hv, None,
                       second_applies=False, kill="range_and_wrong_side")
        res.update(main=main, halves=hv, verdict=vd, n=len(T), sd_D=float(np.std(D)))
        res["readings"]["beta_on_zFIT"] = C.fe_fit(T, [m], "FIT", ctrl_v1)
        res["readings"]["beta_on_zlog1pN"] = C.fe_fit(T, [m], "lN", ctrl_v1)
        res["readings"]["share_zero_covers"] = float(np.mean([r["N"] == 0 for r in T]))
        res["readings"]["corr_FIT_log1pN_on_rows"] = float(np.corrcoef([r["FIT"] for r in T], [r["lN"] for r in T])[0, 1])
        for rd in spec.get("readings", []):
            if rd["kind"] == "five_year_bins":
                res["readings"][rd["name"]] = C.fe_fit(T, [m], "D", ctrl_win, zy=False)
    elif k == "windows":
        T = C.within_artist([r for r in T if r["t0"] is not None and r["t0"] <= 2005 and np.isfinite(r.get("N_E", np.nan))])
        res["n"] = len(T); res["per_measure"] = {}
        for m in spec["measures"]:
            d = windows_fit(T, m, boot=spec["boot"], seed=C.SEED); pred = spec["pred"][m]
            d["prediction"] = pred; d["prediction_by"] = spec["pred_by"][m]
            d["prediction_outside_range"] = bool(not (d["lo"] <= pred <= d["hi"])); d["verdict"] = "estimate"
            S70 = C.within_artist([r for r in T if r["t0"] >= 1970]); d["reading_1970_plus"] = windows_fit(S70, m, analytic_only=True)
            lnE = np.log(C.fit_summary()["r"] + np.array([r["N_E"] for r in T]))
            oL = C.pois_fe([r["N_L"] for r in T], np.column_stack([C._z([r[m] for r in T]), lnE, ctrl_win(T)]), np.log([r["X_L"] for r in T]), [r["artist"] for r in T])
            d["reading_beta_L_with_log_r_plus_NE_held"] = dict(beta=float(oL["b"][0]), se=float(math.sqrt(oL["V"][0, 0])))
            inv = spec.get("inventor_beta_L", {}).get(m)
            if inv is not None:
                d["reading_inventor_beta_L"] = dict(pred=inv, outside_range=bool(not (d["beta_L"] - 1.96 * d["se_L"] <= inv <= d["beta_L"] + 1.96 * d["se_L"])))
            d["reading_delta_zero_outside_range"] = bool(not (d["lo"] <= 0 <= d["hi"]))
            res["per_measure"][m] = d
    elif k in ("lakh", "fifths"):
        R = design(spec)
        if dry: _synthetic(R, k, rng); res["outcome_info"] = "SYNTHETIC"
        else: res["outcome_info"] = C.load_lakh(R, folder)
        m, ex = spec["measure"], spec.get("extra", [])
        xc = [m] + list(ex); ct = ctrl_lakh([])   # extras enter as x columns after the measure (z-scored), same model
        main = C.fe_fit(R, xc, "y_foreign", ct); hv = C.halves_fit(R, xc, "y_foreign", ct); sec = C.second_logit(R, xc, "y_foreign", ct)
        counted = spec["counted"] and pw["power"][str(round(alpha, 6))] >= 0.2
        vd = C.verdict(main, spec["pred"], alpha, counted, hv, sec)
        Rv = [r for r in R if np.isfinite(r["y_foreign"])]
        res.update(main=main, halves=hv, second=sec, verdict=vd, n=len(Rv), share_taken_up=float(np.mean([r["y_foreign"] > 0 for r in Rv])))
        if k == "fifths":
            b, V, n = C.fe_fit_raw(R, ["E5_L", "REST_L"] + [e for e in ex if e != "REST_L"], "y_foreign", ct)
            dlt = float(b[0] - b[1]); sd = float(math.sqrt(V[0, 0] + V[1, 1] - 2 * V[0, 1]))
            res["wald_raw"] = dict(b_E5=float(b[0]), b_REST=float(b[1]), diff=dlt, se_diff=sd, p_two_sided=float(2 * stats.norm.sf(abs(dlt / sd))),
                                   diff_significantly_below_zero=bool(dlt + 1.96 * sd < 0), n=n)
            if vd["verdict"] == "passed" and not dlt > 0: res["verdict"]["verdict"] = "unsettled"; res["verdict"]["note"] = "b_E5 <= b_REST"
            if vd["counted"] and dlt + 1.96 * sd < 0: res["verdict"]["verdict"] = "killed"; res["verdict"]["note"] = "b_E5 < b_REST beyond 1.96 SE"
        for rd in spec.get("readings", []):
            try:
                if rd["kind"] == "lakh":
                    cols = [rd["measure"]] + list(rd.get("extra", []))
                    S = [r for r in R if all(np.isfinite(r.get(c, np.nan)) for c in cols + C.LAKH_BASE + (C.LAKH_SKEPTIC if rd.get("skeptic", True) else []))]
                    out = C.fe_fit(S, cols, "y_foreign", ctrl_lakh([], rd.get("skeptic", True)))
                    out.pop("cov", None); out["pred_sign"] = rd.get("pred_sign"); res["readings"][rd["name"]] = out
                elif rd["kind"] == "shrink":
                    S = [r for r in R if all(np.isfinite(r.get(c, np.nan)) for c in [rd["measure"], rd["held"]] + rd.get("extra", []))]
                    a = C.fe_fit(S, [rd["measure"]] + rd.get("extra", []), "y_foreign", ctrl_lakh([]))
                    b2 = C.fe_fit(S, [rd["measure"]] + rd.get("extra", []) + [rd["held"]], "y_foreign", ctrl_lakh([]))
                    res["readings"][rd["name"]] = dict(beta_without=a["beta"], se_without=a["se"], p_without=a["p"], beta_with=b2["beta"],
                                                       se_with=b2["se"], shrink=(1 - b2["beta"] / a["beta"]) if a["beta"] != 0 else None,
                                                       counts=bool(a["p"] < 0.05), rule=rd.get("rule"))
                elif rd["kind"] == "hook":
                    H = C.hook_design([rd["measure"]] + rd.get("extra", []))
                    if dry: _synthetic(H, "hook", rng)
                    else: C.load_hook(H, folder)
                    o = C.fe_fit(H, [rd["measure"]] + rd.get("extra", []), "y_foreign", ctrl_hook([])); o.pop("cov", None)
                    o["pred_sign"] = rd.get("pred_sign"); res["readings"][rd["name"]] = o
            except Exception as e:
                res["readings"][rd["name"]] = {"error": str(e)}
    elif k == "hook":
        R = design(spec)
        if dry: _synthetic(R, k, rng); res["outcome_info"] = "SYNTHETIC"
        else: res["outcome_info"] = C.load_hook(R, folder)
        m, ex = spec["measure"], spec.get("extra", []); xc = [m] + list(ex); ct = ctrl_hook([])
        main = C.fe_fit(R, xc, "y_foreign", ct); hv = C.halves_fit(R, xc, "y_foreign", ct); sec = C.second_logit(R, xc, "y_foreign", ct)
        counted = spec["counted"] and pw["power"][str(round(alpha, 6))] >= 0.2
        res.update(main=main, halves=hv, second=sec, verdict=C.verdict(main, spec["pred"], alpha, counted, hv, sec), n=len(R))
        for rd in spec.get("readings", []):
            try:
                cols = [rd["measure"]] + list(rd.get("extra", [])); S = [r for r in R if all(np.isfinite(r.get(c, np.nan)) for c in cols)]
                o = C.fe_fit(S, cols, "y_foreign", ct); o.pop("cov", None); o["pred_sign"] = rd.get("pred_sign"); res["readings"][rd["name"]] = o
            except Exception as e:
                res["readings"][rd["name"]] = {"error": str(e)}
    for kk in ("main",):
        if kk in res: res[kk].pop("cov", None)
    for h in res.get("halves", []): h.pop("cov", None)
    out_path = os.path.join(DRY if dry else folder, ("dry_" + os.path.basename(folder) + ".json") if dry else "result.json")
    json.dump(res, open(out_path, "w"), indent=1, default=float)
    show = {kk: res.get(kk) for kk in ("main", "verdict", "wald_raw")}
    if "per_measure" in res: show["per_measure"] = {m: {q: res["per_measure"][m][q] for q in ("delta", "se_boot", "beta_E", "beta_L", "prediction_outside_range")} for m in res["per_measure"]}
    print(json.dumps(show, default=float)); print("wrote", out_path)


def run_canal(folder, spec):
    """notes-side pilot: CANAL = 1 - min over 12 rotations of JSD (bits) between the kept files' pitch-class profiles (tracks 1, 2, 4)."""
    M = json.load(open(C.LAKH12))["songs"]; rows = []
    for key, v in sorted(M.items()):
        fs = v["files"]
        if len(fs) < 2: continue
        a, b = fs[0], fs[1]; js = C_jsd(a["PROF"], b["PROF"]); rot = int(np.argmin(js))
        d = dict(key=key, CANAL=1 - float(min(js)), rot=rot, PCE=(a["PCE_ALL"] + b["PCE_ALL"]) / 2)
        for k in spec["delta_keys"]:
            d["d_" + k] = abs(a[k] - b[k]) if a.get(k) is not None and b.get(k) is not None else np.nan
        rows.append(d)
    c = np.array([r["CANAL"] for r in rows]); out = dict(pairs=len(rows), CANAL_q10_50_90=[float(x) for x in np.percentile(c, [10, 50, 90])],
                                                         same_key_share=float(np.mean([r["rot"] == 0 for r in rows])))
    out["rho_CANAL_meanPCE"] = float(stats.spearmanr(c, [r["PCE"] for r in rows]).correlation)
    out["rho_CANAL_vs_minus_absdiff"] = {}
    for k in spec["delta_keys"]:
        v = np.array([r["d_" + k] for r in rows]); ok = np.isfinite(v)
        out["rho_CANAL_vs_minus_absdiff"][k] = dict(rho=float(stats.spearmanr(c[ok], -v[ok]).correlation), n=int(ok.sum()))
    rr = out["rho_CANAL_vs_minus_absdiff"]
    out["predictions_checked"] = {
        "P1_H1_and_REP_L_above_0.20": bool(rr["H1"]["rho"] > 0.20 and rr["REP_L"]["rho"] > 0.20),
        "P2_PI3c_positive_and_below_both_P1": bool(0 < rr["PI3c"]["rho"] < min(rr["H1"]["rho"], rr["REP_L"]["rho"])),
        "P3_ROUGH_X_abs_below_0.15": bool(abs(rr["ROUGH_X"]["rho"]) < 0.15),
        "P4_abs_rho_with_mean_PCE_below_0.30": bool(abs(out["rho_CANAL_meanPCE"]) < 0.30)}
    json.dump(out, open(os.path.join(folder, "result.json"), "w"), indent=1); print(json.dumps(out, indent=1))


def C_jsd(p, q):
    p, q = np.asarray(p, float), np.asarray(q, float)
    def H(v): v = v[v > 0]; return float(-(v * np.log2(v)).sum())
    return [H((p + np.roll(q, k)) / 2) - (H(p) + H(np.roll(q, k))) / 2 for k in range(12)]


if __name__ == "__main__":
    mode, folder = sys.argv[1], os.path.abspath(sys.argv[2])
    if mode == "power": do_power(folder)
    elif mode == "run": do_run(folder)
    elif mode == "dry":
        assert DRY, "set DRY_DIR to a scratch directory"; do_run(folder, dry=True)
