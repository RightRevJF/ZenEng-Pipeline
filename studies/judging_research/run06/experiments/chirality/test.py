"""Run 06, chirality: within an artist's own songs, do songs whose chord roots turn clockwise round the circle of fifths (negative
signed area, CH < 0) go with a higher chance that a performer set sharing no name with the original artist released the song?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 08b5167 before any outcome was joined).
Measure CH, per clip (common.CH_clip): harmony events by onset (stable sort) -> chord pitch-class sets, consecutive equal sets
collapsed to runs s_0..s_K (root = first event's root_pitch_class); K < 6 no value; theta = 2 pi ((7 root) mod 12) / 12;
CH = (1/K) sum_{t<K} 1/2 sin(theta_{t+1} - theta_t) (open walk). Song CH = K-weighted mean over clips with a value.
Model: LPM of y_foreign on z(CH), z(A), z(ch_rep), z(ch_ic_mean), V, ln_chg and run 04's control block, artist fixed effect, CR1.
PASS: beta < 0, p < .00833 (.05/6, two-sided), beta < 0 in both artist halves, conditional logit < 0 and converged.
OPPOSITE SIGN (beta > 0, p < .00833): killed, reported as a new hypothesis.  KILL: beta > -0.2 pp per SD.  Else UNSETTLED.
Order: 1 unit values; 2 rows and CH, A, V, ln_chg; percentiles; 3 gate (stop if it fails); 4 notes-side power; 5 common.guard, then
load_outcomes; 6 counts; 7 clustered SE and power; 8 beta, halves, conditional logit, verdict; 9 reported items (fresh last);
10 result.json.

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
Run: HOOKTHEORY_RAW=... python3 test.py (BLAS threads pinned to 1).  GATE_ONLY=1 stops before the outcome (code check).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, re
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C          # run 06's frozen shared code
C5 = C.C5                   # run 05's shared code (the same module instance common uses, so the raw file is loaded once)

ALPHA = C.ALPHA; ZC = 2.638
PRED, KILL = -0.6, -0.2
OUT = dict(rule="PREDICTION.md in this folder, commit 08b5167", test="chirality (CH, signed area of the chord-root walk on the circle of fifths)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           prediction_pp_per_sd=PRED, kill_above=KILL, threshold_p=round(ALPHA, 6), deviations=[])
r4 = C.r4

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)

def check(label, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {label}: {got} [{want}] -> {'ok' if ok else 'MISMATCH'}", flush=True)
    return ok

# ---------------------------------------------------------------- 1. unit values (must reproduce)
CHD = {"I": (0, [4, 3]), "ii": (2, [3, 4]), "IV": (5, [4, 3]), "V": (7, [4, 3]), "vi": (9, [3, 4])}   # tonic C, one chord per beat
def prog(names, reps):
    return dict(harmony=[dict(onset=float(i), offset=float(i + 1), root_pitch_class=CHD[c][0], root_position_intervals=CHD[c][1])
                         for i, c in enumerate(names * reps)])
UNIT = [("I-V-vi-IV x4", ["I", "V", "vi", "IV"], 4, 15, 0.1167, 0.1333, 1.0000),
        ("I-IV-vi-V x4", ["I", "IV", "vi", "V"], 4, 15, -0.1167, -0.1333, 1.0000),
        ("I-vi-ii-V x4", ["I", "vi", "ii", "V"], 4, 15, -0.0500, -0.0667, 1.0000),
        ("ii-V-I x5", ["ii", "V", "I"], 5, 14, -0.0549, -0.0239, 1.0000),
        ("I-IV x8", ["I", "IV"], 8, 15, -0.0167, 0.0000, 0.0667),
        ("I-V x8", ["I", "V"], 8, 15, 0.0167, 0.0000, 0.0667),
        ("I-V x2", ["I", "V"], 2, 3, None, None, None)]
OUT["unit_values"] = []
for name, nm, reps, k0, ch0, cw0, a0 in UNIT:
    a = prog(nm, reps); K = C.K_of(a); ch = C.CH_clip(a); cw = C.CH_clip(a, wrap=True); A = C.A_clip(a)
    if ch0 is None: ok = K == k0 and np.isnan(ch) and np.isnan(cw) and np.isnan(A)
    else: ok = K == k0 and round(ch, 4) == ch0 and round(cw, 4) == cw0 and round(A, 4) == a0
    print(f"unit {name}: K {K} [{k0}], CH {ch:+.4f} [{ch0}], CH wrapped {cw:+.4f} [{cw0}], A {A:.4f} [{a0}] -> {'ok' if ok else 'MISMATCH'}", flush=True)
    OUT["unit_values"].append(dict(progression=name, K=K, CH=r4(ch), CH_wrap=r4(cw), A=r4(A), reproduced=ok))
    assert ok, "unit values not reproduced: stopping before anything else is read"

# ---------------------------------------------------------------- 2. rows and CH, A, V, ln_chg from the notes
D = C5.load_rows(); rows = D["rows"]; n = len(rows)
C.add_measures(rows, which=("CH", "A", "V", "ln_chg"))
CHv = np.array([r["CH"] for r in rows], float); has = np.isfinite(CHv)
Av = np.array([r["A"] for r in rows], float); CWv = np.array([r["CH_wrap"] for r in rows], float)
Vv = np.array([r["V"] for r in rows], float); lnchg = np.array([r["ln_chg"] for r in rows], float)
art = np.array([r["artist"] for r in rows]); HV = np.array([r["half"] for r in rows])
q = np.percentile(CHv[has], [10, 50, 90]); arts_has = sorted(set(art[has]))
hh = [sum(1 for a_ in arts_has if C.half_of(a_) == h) for h in (0, 1)]
rho_ow = C5.sp(CHv, CWv)
print("REPRODUCTION (notes only):", flush=True)
okc = [check("songs with CH", int(has.sum()), 8774, 0), check("artists", len(arts_has), 1727, 0),
       check("artists half 0", hh[0], 878, 0), check("artists half 1", hh[1], 849, 0),
       check("10th pct", round(q[0], 3), -0.083, 0.0005), check("50th pct", round(q[1], 3), 0.005, 0.0005), check("90th pct", round(q[2], 3), 0.104, 0.0005),
       check("mean", round(CHv[has].mean(), 4), 0.0078, 0.00005), check("SD (population)", round(CHv[has].std(), 4), 0.0771, 0.00005),
       check("share above 0", round(np.mean(CHv[has] > 0), 2), 0.53, 0.005), check("share exactly 0", round(np.mean(CHv[has] == 0), 2), 0.02, 0.005),
       check("rho open vs wrapped", round(rho_ow[0], 3), 0.918, 0.0005),
       check("A finite wherever CH is", int((has & ~np.isfinite(Av)).sum()), 0, 0)]
# within artist, V, ln K, A and ch_rep explain R^2 0.009 of CH (the Inventor's check)
def demean(M, g):
    codes = {a_: i for i, a_ in enumerate(sorted(set(g)))}; gg = np.array([codes[a_] for a_ in g]); c_ = np.bincount(gg)
    M = np.asarray(M, float).reshape(len(g), -1); s = np.zeros((len(codes), M.shape[1])); np.add.at(s, gg, M); return M - (s / c_[:, None])[gg]
Wd = demean(np.column_stack([CHv[has], Vv[has], lnchg[has], Av[has], [r["ch_rep"] for r, h_ in zip(rows, has) if h_]]), art[has])
yv = Wd[:, 0]; fit_ = Wd[:, 1:] @ np.linalg.lstsq(Wd[:, 1:], yv, rcond=None)[0]; R2w = 1 - ((yv - fit_) ** 2).sum() / (yv ** 2).sum()
okc.append(check("within-artist R^2 of CH on V, ln K, A, ch_rep", round(R2w, 3), 0.009, 0.0005))
OUT["notes"] = dict(rows=n, songs_with_CH=int(has.sum()), artists=len(arts_has), artists_per_half=hh, pct_10_50_90=[r4(x) for x in q],
                    mean=r4(CHv[has].mean()), sd=r4(CHv[has].std()), share_above_0=r4(np.mean(CHv[has] > 0)), share_eq_0=r4(np.mean(CHv[has] == 0)),
                    rho_open_wrapped=r4(rho_ow[0]), within_artist_R2_by_size_A_rep=r4(R2w), reproduced=all(okc))
assert all(okc), "notes counts not reproduced: stopping before the gate"

# ---------------------------------------------------------------- 3. gate (notes only)
gt = C.gate(rows, "CH", extra={"ln_chg": list(lnchg), "V": list(Vv), "A": list(Av)})
print(f"GATE stability (clip 1 vs clip 2, {gt['clip_pairs']} pairs [3,294]): {gt['clip_to_clip']} [0.252], needs >= 0.20; "
      f"largest overlap {gt['overlap_largest']} [ch_ic_mean -0.141], needs |rho| <= 0.7", flush=True)
print("  overlap all: " + json.dumps(gt["overlap_all"]), flush=True)
print(f"  correlation with ch_rep: {gt['overlap_all']['ch_rep']} [+0.07]; A {gt['overlap_all']['A']} [+0.07]; V {gt['overlap_all']['V']} [-0.12]; "
      f"ln_chg {gt['overlap_all']['ln_chg']} [-0.03]", flush=True)
print(f"GATE: {'PASSED' if gt['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = gt
if not gt["passed"]:
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- columns (on the songs with a value)
R9 = [r for r in rows if np.isfinite(r["CH"])]; idx9 = np.nonzero(has)[0]
def zseen(nm, Rb): mu, sd = C.seen_sd(rows, nm); return (np.array([r[nm] for r in Rb], float) - mu) / sd   # seen scale over the 9,588 rows
CN, CX = C5.controls(R9)
zCH = C5.zs(CHv[has])                                        # over the songs with a value, population SD
zA, zrep, zic = zseen("A", R9), zseen("ch_rep", R9), zseen("ch_ic_mean", R9)
V9, ln9 = Vv[has], lnchg[has]
def design(meas, withAV=True, withIC=True):
    cols = {"z_CH": meas}
    if withAV: cols["z_A"] = zA
    cols["z_ch_rep"] = zrep
    if withIC: cols["z_ch_ic_mean"] = zic
    if withAV: cols["V"] = V9
    cols["ln_chg"] = ln9
    names = list(cols) + CN
    return names, np.column_stack(list(cols.values()) + [CX])
NAMES, X = design(zCH)
art9 = art[has]; HV9 = HV[has]
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)

# ---------------------------------------------------------------- 4. notes-side power
nb = C5.power(PRED, 0.514, ALPHA)
Xw = demean(X, art9); x0 = Xw[:, 0]; o = Xw[:, 1:]; o = o[:, np.abs(o).sum(0) > 1e-12]
xt = x0 - o @ np.linalg.lstsq(o, x0, rcond=None)[0]; se_b = float(np.sqrt(0.22 * 0.78) * 100 / np.sqrt(xt @ xt))
PF = json.load(open(os.path.join(os.path.dirname(HERE), "power_fake.json")))["chirality"]
pw_n = C5.power(PRED, se_b, ALPHA); pw_n05 = C5.power(PRED, se_b, 0.05)
print(f"NOTES-SIDE POWER: SE bound {se_b:.3f} pp [0.514] on {len(R9)} songs; power at -0.6, p < .00833: {pw_n:.3f}; at p < .05: {pw_n05:.3f}", flush=True)
print(f"  fake-outcome power (../power_fake.json): calibrated SE {PF['calibrated']['zero']['se_median']} pp, pass rate if true "
      f"{PF['calibrated']['true']['pass_rate']}, power at .00833 {PF['power_at_threshold_calibrated']}, at .05 {PF['power_at_05_calibrated']}; "
      f"kill fires if true {PF['calibrated']['true']['kill_rate']}, if 0 {PF['calibrated']['zero']['kill_rate']}; homogeneous SE "
      f"{PF['homogeneous']['zero']['se_median']}, pass rate if true {PF['homogeneous']['true']['pass_rate']}", flush=True)
print("  run 03's proposed 0.5 power floor (Jason's undecided proposal): below it; printed, not blocking", flush=True)
OUT["notes_side_power"] = dict(se_bound_pp=r4(se_b), power_p00833=r4(pw_n), power_p05=r4(pw_n05), fake_outcome_power=PF)
if os.environ.get("GATE_ONLY"): print("GATE_ONLY: stopping before the outcome", flush=True); sys.exit(0)

# ---------------------------------------------------------------- 5. outcome (guarded)
C.guard(HERE)
LO = C5.load_outcomes(rows, HERE)
yf_all = np.array([r["y_foreign"] for r in rows], float); yy_all = np.array([r["y"] for r in rows], float)
yf, yy = yf_all[has], yy_all[has]
S = np.isfinite(yf)
print(f"\nOUTCOME joined: {json.dumps(LO)}", flush=True)

# ---------------------------------------------------------------- 6. counts
cnt = dict(N=int(S.sum()), artists=len(set(art9[S])), y_foreign_100=int((yf[S] > 0).sum()), share_y_foreign=r4((yf[S] > 0).mean()),
           y_100_among_songs_with_CH=int((yy > 0).sum()), dropped_no_CH=int((~has).sum()), dropped_y_foreign_nan_among_songs_with_CH=int((~S).sum()),
           y_foreign_nan_all_rows=int((~np.isfinite(yf_all)).sum()),
           singleton_artists_after_drops=int(sum(1 for a_, c_ in zip(*np.unique(art9[S], return_counts=True)) if c_ == 1)))
print(f"COUNTS: N {cnt['N']}, artists {cnt['artists']}, y_foreign = 100: {cnt['y_foreign_100']} ({cnt['share_y_foreign']}); y = 100: "
      f"{cnt['y_100_among_songs_with_CH']}; dropped: no CH {cnt['dropped_no_CH']}, y_foreign NaN {cnt['dropped_y_foreign_nan_among_songs_with_CH']} "
      f"[NaN in all rows: {cnt['y_foreign_nan_all_rows']}]; artists left with one song: {cnt['singleton_artists_after_drops']}", flush=True)
OUT["counts"] = cnt

# ---------------------------------------------------------------- 7. clustered SE and power, before the estimate
M = C5.lpm(X[S], yf[S], art9[S])
se = M["se"][0]; pw = C5.power(PRED, se, ALPHA); pw05 = C5.power(PRED, se, 0.05)
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_b:.3f}; fake calibrated 0.38]; power at -0.6, p < .00833: {pw:.3f}; at p < .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_p00833=r4(pw), power_p05=r4(pw05))

# ---------------------------------------------------------------- 8. estimate, halves, conditional logit, verdict
b, p = M["b"][0], M["p"][0]
OUT["primary"] = dict(**C5.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"], all_columns={nm: C5.summ(M, i) for i, nm in enumerate(NAMES)})
print(f"PRIMARY LPM z(CH): beta {b:+.4f} pp per SD (predicted -0.6), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print("  other columns: " + ", ".join(f"{nm} {M['b'][i]:+.3f} (SE {M['se'][i]:.3f})" for i, nm in enumerate(NAMES[1:6], 1)), flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = S & (HV9 == h); HM[h] = C5.lpm(X[s], yf[s], art9[s])
    d = dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], y_foreign_100=int((yf[s] > 0).sum()), **C5.summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {d['songs']} songs, {d['artists']} artists, y_foreign=100 {d['y_foreign_100']}; beta {d['beta']:+.4f} (SE {d['se']:.4f}, p {d['p']:.3g})", flush=True)

yb = (yf[S] > 0).astype(float); t1 = time.time()
gS = art9[S]; codes = {a_: i for i, a_ in enumerate(sorted(set(gS)))}; gi = np.array([codes[a_] for a_ in gS]); cntS = np.bincount(gi)
ga = np.bincount(gi, weights=yb); keep_g = (ga > 0) & (ga < cntS); keep = keep_g[gi]
Xkd = demean(X[S][keep], gS[keep]); novar = [NAMES[j] for j in range(X.shape[1]) if np.all(np.abs(Xkd[:, j]) < 1e-12)]
print(f"CONDITIONAL LOGIT sample: keeps {int(keep_g.sum())} artists, {int(keep.sum())} songs; columns with no within-artist variation there: {novar}", flush=True)
cl = dict(columns_without_within_variation=novar)
use = [j for j in range(X.shape[1]) if NAMES[j] not in novar]
if novar:
    OUT["deviations"].append(f"conditional logit: columns with no within-artist variation in its sample dropped ({novar}); they carry no information in a conditional likelihood")
def cl_exact(Xk, yk, gk):
    """Exact conditional (fixed-effect) logit likelihood by the subset recursion (elementary symmetric sums), copied unchanged from
    run05/experiments/arrow_of_time/test.py (run 04's cross-check). scipy BFGS, then Newton. Returns params, se, max|score|, info."""
    from scipy.optimize import minimize
    grp = [np.nonzero(gk == a)[0] for a in np.unique(gk)]; P = Xk.shape[1]
    def fgh(b, hess=True):
        ll = 0.0; gr = np.zeros(P); H = np.zeros((P, P))
        for ix in grp:
            x = Xk[ix]; k = int(yk[ix].sum()); eta = x @ b; c = eta.max(); w = np.exp(eta - c)
            E = np.zeros(k + 1); E[0] = 1; Dd = np.zeros((k + 1, P)); Hh = np.zeros((k + 1, P, P)) if hess else None
            for t in range(len(ix)):
                xt = x[t]; wt = w[t]
                if hess:
                    Hh[1:] = Hh[1:] + wt * (Hh[:-1] + np.outer(xt, xt)[None] * E[:-1, None, None] + xt[None, :, None] * Dd[:-1, None, :]
                                            + Dd[:-1, :, None] * xt[None, None, :])
                Dd[1:] = Dd[1:] + wt * (Dd[:-1] + E[:-1, None] * xt[None])
                E[1:] = E[1:] + wt * E[:-1]
            e = E[k]; m_ = Dd[k] / e
            ll += yk[ix] @ eta - (np.log(e) + k * c); gr += yk[ix] @ x - m_
            if hess: H -= Hh[k] / e - np.outer(m_, m_)
        return ll, gr, H
    nob = len(yk)
    res = minimize(lambda b: -fgh(b, False)[0] / nob, np.zeros(P), jac=lambda b: -fgh(b, False)[1] / nob, method="BFGS",
                   options=dict(gtol=1e-7, maxiter=2000))
    b = res.x; it = 0
    for it in range(1, 101):
        ll, gr, H = fgh(b); step = np.linalg.pinv(H) @ gr; lam = 1.0
        while lam > 1e-8:
            nb_ = b - lam * step
            if fgh(nb_, False)[0] >= ll - 1e-12: break
            lam /= 2
        b = nb_
        if np.max(np.abs(lam * step)) < 1e-9: break
    ll, gr, H = fgh(b)
    se_ = np.sqrt(np.abs(np.diag(np.linalg.pinv(-H))))
    return b, se_, float(np.max(np.abs(gr))), dict(bfgs_success=bool(res.success), bfgs_message=str(res.message), newton_steps=it, llf=float(ll), nobs=nob)

Gs = len(set(gS)); ks, kg = int(keep.sum()), int(keep_g.sum())
P_ = np.full(X.shape[1], np.nan); B_ = P_.copy(); PV_ = P_.copy()
try:
    params, bse, pv, conv, ks, kg = C5.cond_logit(X[S][:, use], yb, gS); how = "statsmodels ConditionalLogit (run05 common.cond_logit)"
    P_[use] = params; B_[use] = bse; PV_[use] = pv
except Exception as e:
    print(f"  statsmodels ConditionalLogit failed: {e!r}; using the exact conditional likelihood with scipy (BFGS, then Newton), "
          f"run 05's fallback on this same sample", flush=True)
    cl["statsmodels_error"] = repr(e)
    OUT["deviations"].append("statsmodels ConditionalLogit (run05 common.cond_logit) raised " + repr(e) + " while forming the covariance "
                             "(nuisance columns with no finite estimate, as in run 05 on the same 3,186-song sample); the coefficient was taken "
                             "from the exact conditional likelihood (subset recursion, copied unchanged from run05 arrow_of_time/test.py), with a "
                             "statsmodels cross-check dropping the non-finite columns. Code fix only; no rule changed.")
    gk_codes = np.array([codes[a_] for a_ in gS[keep]])
    bb, ss_, gmax, info = cl_exact(X[S][keep][:, use], yb[keep], gk_codes)
    P_[use] = bb; B_[use] = ss_
    from scipy.stats import norm as _N
    PV_ = 2 * _N.sf(np.abs(P_ / B_)); conv = bool(gmax / info["nobs"] < 1e-5)
    how = "exact conditional likelihood (subset recursion), scipy BFGS then Newton"; cl.update(max_abs_score=gmax, **info)
cl.update(coef=r4(P_[0]), se=r4(B_[0]), p=float(f"{PV_[0]:.4g}"), converged=conv, optimiser=how,
          convergence_test="max|score|/nobs < 1e-5", kept_songs=ks, kept_artists=kg, dropped_songs=int(S.sum() - ks), dropped_artists=int(Gs - kg),
          seconds=round(time.time() - t1), all_columns={nm: [r4(a_), r4(b_)] for nm, a_, b_ in zip(NAMES, P_, B_)})
big = [(nm, r4(a_)) for nm, a_ in zip(NAMES, P_) if np.isfinite(a_) and abs(a_) > 5]
cl["columns_abs_coef_over_5"] = big
print(f"CONDITIONAL LOGIT: drops {cl['dropped_artists']} artists and {cl['dropped_songs']} songs (all 0 or all 1); keeps {kg} artists, {ks} songs; "
      f"z(CH) coef {P_[0]:+.4f} log-odds per SD (SE {B_[0]:.4f}, p {PV_[0]:.4g}); converged: {conv}; {cl['seconds']} s", flush=True)
if big:
    print(f"  columns with |coef| > 5: {big}", flush=True)
    try:   # cross-check, deciding nothing: statsmodels on the same sample without the columns that have no finite estimate
        use2 = [j for j in use if NAMES[j] not in [b_[0] for b_ in big]]
        p2, b2, pv2, cv2, _, _ = C5.cond_logit(X[S][:, use2], yb, gS)
        cl["crosscheck_without_nonfinite_columns"] = dict(dropped=[b_[0] for b_ in big], coef=r4(p2[0]), se=r4(b2[0]), p=float(f"{pv2[0]:.4g}"), converged=cv2)
        print(f"  cross-check (statsmodels, without {[b_[0] for b_ in big]}): z(CH) coef {p2[0]:+.4f} (SE {b2[0]:.4f}, p {pv2[0]:.4g}), converged {cv2}", flush=True)
    except Exception as e:
        cl["crosscheck_without_nonfinite_columns"] = dict(error=repr(e)); print(f"  cross-check failed: {e!r}", flush=True)
OUT["conditional_logit"] = cl

hb = [HM[h]["b"][0] for h in (0, 1)]; cb = P_[0]
if b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0 and conv and cb < 0: v = "pass"
elif b > 0 and p < ALPHA: v = "opposite sign (beta > 0, p < .00833): killed; reported as a new hypothesis ('counterclockwise loops such as I-V-vi-IV are what others take up'), not a pass"
elif b > KILL: v = "kill (beta > -0.2 pp per SD)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00833")
    if not (hb[0] < 0 and hb[1] < 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb < 0: why.append("conditional logit sign disagrees")
    v = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the written rule): {v}", flush=True)
OUT["verdict_rule_inputs"] = dict(beta=r4(b), p=float(f"{p:.4g}"), halves=[r4(x) for x in hb], logit=r4(cb), logit_converged=conv)

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
zW = C5.zs(CWv[has]); _, XW = design(zW); m = C5.lpm(XW[S], yf[S], art9[S]); dn["wrapped_CH_in_place_of_CH"] = C5.summ(m, 0)
zAb = C5.zs(np.abs(CHv[has])); _, XB = design(zAb); m = C5.lpm(XB[S], yf[S], art9[S]); dn["abs_CH_in_place_of_CH"] = C5.summ(m, 0)
_, X1 = design(zCH, withAV=False); m = C5.lpm(X1[S], yf[S], art9[S]); dn["without_zA_and_V"] = C5.summ(m, 0)
_, X2 = design(zCH, withIC=False); m = C5.lpm(X2[S], yf[S], art9[S]); dn["without_z_ch_ic_mean"] = C5.summ(m, 0)
m = C5.lpm(X, yy, art9); dn["CH_on_y_in_DiscogsVI_at_all"] = dict(**C5.summ(m, 0), N=m["N"], note="all songs with CH (y is defined for every row)")
R9o = [rows[i] for i in idx9]
lc = np.array([np.nan if r["lcov"] is None else r["lcov"] for r in R9o], float)
fy = np.array([np.nan if r["first_year"] is None else r["first_year"] for r in R9o], float)
Si = (yy > 0) & np.isfinite(lc) & np.isfinite(fy)
zl = np.full(len(R9o), np.nan); zl[Si] = C5.zs(lc[Si])
m = C5.lpm(np.column_stack([X[Si], fy[Si]]), zl[Si], art9[Si])
dn["intensive_margin_zlog1p_covers"] = dict(**C5.summ(m, 0), N=m["N"], artists=m["G"],
    note="SD of log(1+covers) per SD of CH; outcome standardised over this sample; first_year linear added")
kw = ("karaoke", "tribute"); nrm = C.nrm
yk = yf.copy(); nchg_k = 0; nkt = 0
for i, r in enumerate(R9o):
    if not np.isfinite(yf[i]) or r.get("versions") is None: continue
    sets = [e[0] for e in r["versions"]]; a_ = nrm(r["artist"])
    nkt += int(any(k in nm.lower() for s_ in sets for nm in s_ for k in kw))
    own = [s_ for s_ in sets if any(nrm(nm) == a_ for nm in s_)]
    O = {nrm(nm) for s_ in own for nm in s_}
    keep_sets = [s_ for s_ in sets if not any(k in nm.lower() for nm in s_ for k in kw)]
    new = 100.0 if [s_ for s_ in keep_sets if len(s_) > 0 and not any(nrm(nm) in O for nm in s_)] else 0.0
    nchg_k += int(new != yf[i]); yk[i] = new
m = C5.lpm(X[S], yk[S], art9[S])
dn["y_foreign_without_karaoke_tribute_sets"] = dict(**C5.summ(m, 0), songs_switched_to_0=nchg_k, songs_with_any_karaoke_or_tribute_set=nkt,
                                                     y_foreign_100=int((yk[S] > 0).sum()))
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k_, v_ in dn.items(): print(f"  {k_}: {json.dumps(v_)}", flush=True)

# ---- CH on the fresh songs (reported only; sign frozen negative; only after the validation passes)
print("\nCH ON THE FRESH SONGS (reported only; frozen sign negative; decides nothing):", flush=True)
try:
    B = C.battery(); brows = B["rows"]
    C.add_measures(brows, which=("CH", "A", "V", "ln_chg"))
    Rb = [r for r in brows if np.isfinite(r["CH"]) and np.isfinite(r["A"])]
    fr_n = sum(r["fresh"] for r in Rb)
    print(f"  fresh-design rows with CH: {len(Rb)} ({fr_n} fresh) by {len(set(r['artist'] for r in Rb))} artists [888 fresh, 448 artists per chair's note]", flush=True)
    LB = C.load_battery_outcomes(Rb, HERE)    # guard(fresh=True) + validate_match (cached, passed) inside
    print(f"  validation passed: {LB['validation_passed']}; fresh outcome summary: " + json.dumps({k: LB[k] for k in LB if k != "seen"}), flush=True)
    seen_mu, seen_sdv = C.seen_sd(rows, "CH")
    extra = {"z_A": zseen("A", Rb), "z_ch_rep": zseen("ch_rep", Rb)}
    FN, FX, (mu_, sd_) = C.fresh_design(Rb, "CH", rows, extra)
    fy_ = np.array([r["y_foreign"] for r in Rb], float); Sf = np.isfinite(fy_)
    fa = np.array([r["artist"] for r in Rb]); fh = np.array([r["half"] for r in Rb]); ff = np.array([r["fresh"] for r in Rb])
    mf = C5.lpm(FX[Sf], fy_[Sf], fa[Sf])
    fres = dict(rows=int(Sf.sum()), fresh_rows=int(ff[Sf].sum()), artists=len(set(fa[Sf])), z_scale=[r4(mu_), r4(sd_)],
                fresh_y_foreign_100=int((fy_[Sf & (ff == 1)] > 0).sum()), seen_y_foreign_100=int((fy_[Sf & (ff == 0)] > 0).sum()),
                fresh_nan_dropped=int((~Sf & (ff == 1)).sum()), z_fresh=C5.summ(mf, 0), z_seen=C5.summ(mf, 1),
                power_at_minus06_p00833=r4(C5.power(PRED, mf["se"][0], ALPHA)), columns=FN, outcome_summary={k: LB[k] for k in LB if k != "seen"})
    fres["halves"] = []
    for h in (0, 1):
        s = Sf & (fh == h); mh = C5.lpm(FX[s], fy_[s], fa[s]); fres["halves"].append(dict(half=h, songs=mh["N"], **C5.summ(mh, 0)))
    try:
        ybf = (fy_[Sf] > 0).astype(float); Xd = demean(FX[Sf], fa[Sf])
        g_ = fa[Sf]; cd = {a_: i for i, a_ in enumerate(sorted(set(g_)))}; gi_ = np.array([cd[a_] for a_ in g_]); ct_ = np.bincount(gi_)
        ga_ = np.bincount(gi_, weights=ybf); kk = ((ga_ > 0) & (ga_ < ct_))[gi_]
        Xkd2 = demean(FX[Sf][kk], g_[kk]); use2 = [j for j in range(FX.shape[1]) if not np.all(np.abs(Xkd2[:, j]) < 1e-12)]
        pp_, bb_, pv_, cv_, ks_, kg_ = C5.cond_logit(FX[Sf][:, use2], ybf, g_)
        fres["conditional_logit"] = dict(coef=r4(pp_[0]), se=r4(bb_[0]), p=float(f"{pv_[0]:.4g}"), converged=cv_, kept_songs=ks_, kept_artists=kg_,
                                         dropped_columns=[FN[j] for j in range(FX.shape[1]) if j not in use2])
    except Exception as e:
        fres["conditional_logit"] = dict(error=repr(e))
    print(f"  z_fresh(CH): beta {fres['z_fresh']['beta']} (SE {fres['z_fresh']['se']}, p {fres['z_fresh']['p']}); halves "
          f"{[x['beta'] for x in fres['halves']]}; logit {fres['conditional_logit']}; z_seen {fres['z_seen']['beta']} (SE {fres['z_seen']['se']})", flush=True)
    print(f"  rows {fres['rows']} ({fres['fresh_rows']} fresh), fresh y_foreign=100 {fres['fresh_y_foreign_100']}; power at -0.6, p < .00833: {fres['power_at_minus06_p00833']}", flush=True)
    dn["CH_on_fresh_songs"] = fres
except SystemExit as e:
    dn["CH_on_fresh_songs"] = dict(stopped=str(e)); print(f"  stopped: {e}", flush=True)
OUT["reported_deciding_nothing"] = dn

# ---------------------------------------------------------------- 10. result.json
finish(v)
