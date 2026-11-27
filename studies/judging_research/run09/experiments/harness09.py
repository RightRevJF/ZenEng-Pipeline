"""Run 09 test harness, frozen by the chair before any outcome is joined. Each test folder's test.py calls one function here.

The outcome is read ONLY through common09.load_outcomes (unseen songs) or, for the two seen-song leads, from
studies/judging_research/data/choco_songs_discogs_run08.json AFTER common09.guard(folder) has passed. Power is printed BEFORE any
outcome is read.

THE FROZEN MODEL (the iiv_singletons model of run 08 first_principles section 5, with the chair's timebase rule):
  y_cov = log(1 + n_artist_sets) standardised over the analysed songs;
  plain OLS with intercept, HC1 robust SEs (posthoc08.ols_hc1), across composers (most composer keys have one song);
  columns: z(measure), z(each extra column), genre dummies (the design's partition-based coarse genre), first-year decade dummies
  (common.decade_bins: 10-year bins, unknown its own bin). A column that is constant on the analysed rows is dropped before z-scoring.
  STD = the iiv_singletons columns w_chr, ch_rep, V, ln_chg, ln_bars, plus no_bars (the timebase rule: ln_bars is missing on
  seconds-timed charts; a song with no bar-timed chart gets ln_bars = the mean over the analysed songs that have one, and no_bars = 1).
  Halves: common09.halves(composer key); y re-standardised within each half; same columns.
  Second model: posthoc08.poisson_plain on n_sets with the same columns (Poisson pseudo-likelihood, HC0).
  Verdict: common09.verdict with the frozen power (counted tests) or 0 (estimates and leads, which pass nothing and kill nothing).
POWER (before the outcome): posthoc08.fake_power_ols style: y = beta * z(measure) + N(0, 1 - beta^2) on the real rows, OLS HC1 on the
  frozen columns without the decade dummies (first_year comes with the outcome), 300 draws, seed 11; power = share of draws with
  p < alpha and the predicted sign. Also: the share of draws in which the range kill fires when the prediction is true (kill_if_true)
  and when the effect is zero (kill_if_zero), and the median fake SE.
"""
import sys, os, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from scipy import stats
import common09 as C9
C8 = C9.C8
sys.path.insert(0, os.path.join(C9.REPO, "studies/judging_research/run08/experiments"))
import posthoc08 as P8

MEAS_JSON = os.path.join(C9.DL, "choco", "measures_run09.json")
RUN08_DATA = os.path.join(C9.REPO, "studies/judging_research/data/choco_songs_discogs_run08.json")
STD = ["w_chr", "ch_rep", "V", "ln_chg", "ln_bars", "no_bars"]
SEED = 11

_MS = None
def measures():
    global _MS
    if _MS is None: _MS = json.load(open(MEAS_JSON))
    return _MS

# ---------------------------------------------------------------- rows (notes only)
def design_rows(cols, keep=None, source="all"):
    """the unseen design songs with every column defined. source 'all': song means over all charts; 'rbb': over the song's
    real-book and BiaB charts only (keys *_rbb; songs with at least one such measured chart). keep(s) filters on design fields."""
    info, S = C9.load_design(); MS = measures()["songs"]; R = []
    for s in S:
        if keep is not None and not keep(s): continue
        m = MS[s["clique"]]; r = dict(s)
        if source == "rbb":
            if not m["n_rbb_measured"]: continue
            for c in cols:
                r[c] = 0 if c == "no_bars" else m.get(c + "_rbb", m.get(c))
        else:
            for c in cols: r[c] = m.get(c)
        if all(r.get(c) is not None or c == "ln_bars" for c in cols): R.append(r)
    if "ln_bars" in cols:
        have = [r["ln_bars"] for r in R if r["ln_bars"] is not None]; mu = float(np.mean(have)) if have else 0.0
        for r in R:
            if r["ln_bars"] is None: r["ln_bars"] = mu
    return R

def seen_rows(cols, keep=None):
    """run 08 songs (seen in run 08) from measures_run09.json 'seen08' (notes side; clique and chart ids only were read)."""
    SE = measures()["seen08"]; R = []
    for cid, m in SE.items():
        r = dict(m); r["clique"] = cid; r["genre"] = m["genre8"]
        if keep is not None and not keep(r): continue
        if all(r.get(c) is not None for c in cols): R.append(r)
    return R

# ---------------------------------------------------------------- matrices and models
def Xmat(R, cols, decade=True):
    Z = []
    for c in cols:
        v = np.array([s[c] for s in R], float)
        if v.std() > 1e-12: Z.append((v - v.mean()) / v.std())
        elif c == cols[0]: raise ValueError("the measure is constant on the analysed rows")
    D = [C8.dummies([s["genre"] for s in R])]
    if decade: D.append(C8.dummies(C8.decade_bins(R)))
    return np.column_stack(Z + [d for d in D if d.size])

def ols_cr1(y, X, g):
    """plain OLS, CR1 SEs clustered by g (a reading only)."""
    X1 = np.column_stack([np.ones(len(y)), X]); XtX = np.linalg.pinv(X1.T @ X1); b = XtX @ X1.T @ y; e = y - X1 @ b
    n, k = X1.shape; G = len(set(g)); meat = np.zeros((k, k))
    for u in set(g):
        i = np.array([x == u for x in g]); s = X1[i].T @ e[i]; meat += np.outer(s, s)
    V = XtX @ meat @ XtX * (G / (G - 1)) * ((n - 1) / (n - k)); se = np.sqrt(np.diag(V))
    p = 2 * stats.t.sf(np.abs(b / se), G - 1)
    return b[1:], se[1:], p[1:], n, G

def fake_power(R, cols, beta, alpha, draws=300, seed=SEED, coef=0):
    rng = np.random.default_rng(seed); X = Xmat(R, cols, decade=False); z = X[:, coef]
    hits = kt = kz = 0; ses = []
    for d in range(draws):
        e = rng.normal(0, 1, len(z))
        y = beta * z + math.sqrt(1 - beta ** 2) * e; b, se, p, n = P8.ols_hc1(y, X)
        hits += (p[coef] < alpha) and np.sign(b[coef]) == np.sign(beta); kt += abs(beta - b[coef]) > 1.96 * se[coef]; ses.append(se[coef])
        b0, se0, p0, n0 = P8.ols_hc1(e, X); kz += abs(beta - b0[coef]) > 1.96 * se0[coef]
    return dict(power=hits / draws, kill_if_true=kt / draws, kill_if_zero=kz / draws, se_fake=round(float(np.median(ses)), 4),
                N=len(R), beta=beta, alpha=alpha, draws=draws)

def ystd(R):
    v = np.array([s["ln_sets"] for s in R]); return (v - v.mean()) / v.std()

def fit_all(R, cols, coefs=(0,)):
    """main OLS HC1, halves, Poisson second model, CR1 reading, for the listed coefficient positions."""
    y = ystd(R); X = Xmat(R, cols); b, se, p, n = P8.ols_hc1(y, X)
    out = {}
    hv = np.array([C9.halves(s["composer"]) for s in R]); hb = []
    for h in (0, 1):
        i = hv == h; RR = [s for s, k in zip(R, i) if k]
        bh, sh, ph, nh = P8.ols_hc1(ystd(RR), Xmat(RR, cols)); hb.append((bh, sh, nh))
    bc, sc, pc, nc, gc = ols_cr1(y, X, [s["composer"] for s in R])
    nsets = np.array([s["n_sets"] for s in R], float)
    for j in coefs:
        order = [j] + [k for k in range(X.shape[1]) if k != j]
        pb, pse, pp = P8.poisson_plain(nsets, X[:, order])
        out[cols[j]] = dict(b=float(b[j]), se=float(se[j]), p=float(p[j]), N=int(n),
                            range95=[float(b[j] - 1.96 * se[j]), float(b[j] + 1.96 * se[j])],
                            halves=[dict(b=float(x[0][j]), se=float(x[1][j]), N=int(x[2])) for x in hb],
                            second=dict(model="Poisson QMLE on n_sets, intercept, same columns, HC0 (posthoc08.poisson_plain)",
                                        b=pb, se=pse, p=pp),
                            cluster_composer=dict(b=float(bc[j]), se=float(sc[j]), p=float(pc[j]), G=int(gc)))
    return out

def jd(x):
    return json.dumps(x, default=lambda o: float(o) if isinstance(o, (np.floating, float)) else int(o) if isinstance(o, np.integer) else str(o))

# ---------------------------------------------------------------- unseen y_cov tests
def run_unseen(folder, meas, extra, pred, alpha, K, counted, frozen_power, readings=(), estimate_reason=None, keep=None):
    """readings: list of dicts(label, meas, extra, pred or None, keep or None, source 'all'/'rbb', coef_names optional);
    each is reported, deciding nothing (an estimate), with its own power printed before the outcome when it has a prediction."""
    t0 = time.time(); cols = [meas] + list(extra)
    R = design_rows(cols, keep=keep)
    name = os.path.basename(folder)
    print(f"[{name}] measure {meas}; extra {list(extra)}; prediction {pred:+.3f} SD per SD; K {K}; alpha {alpha:.5f}; "
          f"status frozen as {'COUNTED' if counted else 'ESTIMATE'}; songs {len(R)}", flush=True)
    pw = fake_power(R, cols, pred, alpha)
    print("POWER (fake outcomes on the real rows, before the outcome is joined):", jd(pw), "| frozen in PREDICTION.md:", frozen_power, flush=True)
    RD = []
    for rd in readings:
        rc = [rd["meas"]] + list(rd["extra"]); RR = design_rows(rc, keep=rd.get("keep"), source=rd.get("source", "all"))
        rpw = fake_power(RR, rc, rd["pred"], alpha) if rd.get("pred") is not None and len(RR) >= 50 else None
        print(f"  reading {rd['label']}: songs {len(RR)}; prediction {rd.get('pred')}; power {jd(rpw) if rpw else '-'}", flush=True)
        RD.append((rd, rc, RR, rpw))
    # ---- the outcome (guarded): loaded onto every design song once; y re-standardised per analysis
    info, S = C9.load_design(); C9.load_outcomes(S, folder); O = {s["clique"]: s for s in S}
    def attach(rows):
        for r in rows:
            o = O[r["clique"]]; r.update(n_sets=o["n_sets"], covers=o["covers"], first_year=o["first_year"], ln_sets=o["ln_sets"])
    attach(R)
    res = fit_all(R, cols)[meas]
    v = C9.verdict(res["b"], res["se"], res["p"], pred, alpha, [h["b"] for h in res["halves"]], res["second"]["b"],
                   frozen_power if counted else 0.0)
    if not counted: v["verdict"] = "estimate (" + (estimate_reason or "under the power floor") + "): passes nothing, kills nothing"
    out = dict(folder=name, measure=meas, extra=list(extra), prediction=pred, K=K, alpha=alpha, counted=counted,
               frozen_power=frozen_power, power_rerun=pw, main=res, verdict=v, readings={},
               n_sets_median=float(np.median([s["n_sets"] for s in R])), covers_mean=float(np.mean([s["covers"] for s in R])))
    for rd, rc, RR, rpw in RD:
        if len(RR) < 50: out["readings"][rd["label"]] = dict(skipped="fewer than 50 songs", N=len(RR)); continue
        attach(RR); r = fit_all(RR, rc)[rd["meas"]]
        r.update(prediction=rd.get("pred"), power=rpw, note=rd.get("note", ""))
        if rd.get("pred") is not None:
            r["prediction_inside_95"] = bool(abs(rd["pred"] - r["b"]) <= 1.96 * r["se"])
        out["readings"][rd["label"]] = r
    json.dump(out, open(os.path.join(folder, "result.json"), "w"), indent=1, default=float)
    print(jd(dict(main=res, verdict=v)))
    print("readings:", jd(out["readings"])); print("done", round(time.time() - t0), "s")
    return out

# ---------------------------------------------------------------- seen-song leads (run 08 songs; outcomes already seen in run 08)
def load_seen_outcomes(R, folder):
    """AFTER common09.guard(folder): read n_artist_sets, first_year and composer for the run 08 songs from the run 08 data file."""
    C9.guard(folder)
    D = {v["clique"]: v for v in json.load(open(RUN08_DATA))["songs"]}
    for r in R:
        d = D[r["clique"]]; r["n_sets"] = d["n_artist_sets"]; r["covers"] = d["n_artist_sets"] - 1; r["first_year"] = d["first_year"]
        r["ln_sets"] = math.log(1 + d["n_artist_sets"]); r["composer"] = d["composer"]; r["within"] = d["within"]
    return R

GAP_CTRL = ["w_chr_up", "ch_rep_up", "V_up", "ln_chg_up", "ln_bars_up", "w_chr_ireal", "ch_rep_ireal", "V_ireal", "ln_chg_ireal", "ln_bars_ireal"]
def gap_rows():
    """the GAP lead's rows: run 08 songs with at least one measured iReal Pro chart and at least one matched upstream (real-book or
    BiaB) chart. IIV_up = mean IIV over the upstream charts; GAP = IIV_ireal - IIV_up; ln_n_ireal = log(number of the song's
    measured iReal charts)."""
    R = seen_rows(["IIV_up", "IIV_ireal"] + GAP_CTRL, keep=lambda r: r["n_up"] > 0 and r["n_ireal"] > 0)
    for r in R: r["GAP"] = r["IIV_ireal"] - r["IIV_up"]; r["ln_n_ireal"] = math.log(r["n_ireal"])
    return R
SEEN_STD = ["w_chr", "ch_rep", "V", "ln_chg", "ln_bars"]
def dres_rows():
    """the IIV-holding-DRES lead's rows: run 08 songs with IIV, DRES and the five iiv_singletons columns (all charts, run 08's song value)."""
    return seen_rows(["IIV", "DRES"] + SEEN_STD)

def run_seen(folder, rows_fn, cols, preds, readings=(), classify=None, within_reading=False, power_betas=None):
    """a seen-song LEAD (re-spends run 08's outcomes; never in K; passes nothing and kills nothing).
    preds: {column name: predicted coefficient} for the coefficients reported; power for each (or at power_betas, when a
    prediction is 0) printed before the outcome.
    readings: list of dicts(label, cols, report: [column names]), deciding nothing.
    classify(main, readings) -> dict of frozen labels computed from the main estimates and the readings."""
    t0 = time.time(); R = rows_fn(); name = os.path.basename(folder)
    print(f"[{name}] SEEN-SONG LEAD (run 08 songs, outcomes opened in run 08; not in K); columns {cols}; predictions {preds}; "
          f"songs {len(R)}", flush=True)
    pw = {c: fake_power(R, cols, b, 0.05, coef=cols.index(c)) for c, b in (power_betas or preds).items() if b != 0}
    print("POWER at .05 (fake outcomes on the real rows, before the outcome is read):", jd(pw), flush=True)
    load_seen_outcomes(R, folder)
    idx = [cols.index(c) for c in preds]
    res = fit_all(R, cols, coefs=idx)
    for c, b in preds.items():
        res[c]["prediction"] = b; res[c]["prediction_inside_95"] = bool(abs(b - res[c]["b"]) <= 1.96 * res[c]["se"])
    out = dict(folder=name, lead=True, seen_songs=True, columns=cols, predictions=preds, power_at_05=pw, main=res,
               verdict="lead on seen songs (re-spends run 08's outcomes; not in K): passes nothing, kills nothing",
               labels={}, readings={},
               n_sets_median=float(np.median([s["n_sets"] for s in R])))
    for rd in readings:
        RR = [r for r in R if rd.get("keep") is None or rd["keep"](r)]
        r = fit_all(RR, rd["cols"], coefs=[rd["cols"].index(c) for c in rd["report"]])
        out["readings"][rd["label"]] = r
    if within_reading:
        RR = [r for r in R if r["within"]]; y = ystd(RR); X = Xmat(RR, cols); g = np.array([r["composer"] for r in RR])
        b, se, p, N, G = C8.ols_fe(y, X, g)
        out["readings"]["within_composer_run08_model"] = {c: dict(b=float(b[cols.index(c)]), se=float(se[cols.index(c)]),
                                                                   p=float(p[cols.index(c)]), N=int(N), G=int(G)) for c in preds}
    if classify: out["labels"] = classify(res, out["readings"])
    json.dump(out, open(os.path.join(folder, "result.json"), "w"), indent=1, default=float)
    print(jd(dict(main=res, labels=out["labels"]))); print("readings:", jd(out["readings"])); print("done", round(time.time() - t0), "s")
    return out
