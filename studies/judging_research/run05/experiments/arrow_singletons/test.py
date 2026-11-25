"""Run 05, arrow_singletons (the night's 8th test, written AFTER SEEING RESULTS): across songs by artists with exactly one song
among the 13,198, does chord motion that runs one way round (a Markov chain far from detailed balance) go with a higher chance
that a performer set sharing no name with the original artist released the song?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 2bfd4ca before any outcome was joined).
Measure A: arrow_of_time's `changes` and `clip_vals`, copied unchanged from ../arrow_of_time/test.py (rule 1f6c36d):
chord pitch-class sets in onset order, consecutive equal sets collapsed; clips with K < 6 changes have no value;
A = 1 - sum min(n_ij, n_ji) / sum n_ij; song A = mean over clips with a value, weighted by K.
Rows: common.load_rows()["allsongs"] whose artist has exactly one song (3,610); halves = md5(artist) mod 2.
Model rows: songs with A and all 17 data-pack measures finite; y_foreign NaN dropped after the join.
Model: cross-song OLS of y_foreign on z(A), z of the 17 data-pack measures (common.FE, incl. ch_rep and ch_ic_mean),
ln_chg, run 04's control block and an intercept; HC1 SE (= CR1 by artist, one song per artist). Same model in each half.
Sign check: statsmodels Logit on y_foreign/100 with the same columns (bfgs, maxiter 2000, then Newton if needed);
converged when max|score|/nobs < 1e-5.
PASS (a lead only): beta > 0, p < .00625 (.05/8, two-sided), beta > 0 in both halves, converged logit coefficient > 0.
OPPOSITE SIGN (beta < 0, p < .00625): killed, reported as a new hypothesis.  KILL: beta < +0.2 pp per SD.  Else UNSETTLED.
Order (as the rule says): 1 unit values; 2 singleton rows and A; 3 gate (stop if it fails); 4 notes-side power;
5 load_outcomes; 6 counts; 7 HC1 SE and power; 8 beta, p, 95% range, halves, logit, verdict; 9 reported items; 10 result.json.

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
python3 test.py -> result.json in this folder.
Env (code checks only): GATE_ONLY=1 stops before the outcome; FAKE_Y=<dir> uses a random outcome (no outcome file read) and writes there.
"""
import os, sys, json, time, hashlib, re, warnings, collections
import numpy as np
from scipy.stats import norm as NRM

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

ALPHA = 0.05 / 8; ZC = float(NRM.isf(ALPHA / 2))   # two-sided, 2.734
PRED, KILL = 0.6, 0.2
OUTDIR = os.environ.get("FAKE_Y") or HERE
OUT = dict(rule="PREDICTION.md in this folder, commit 2bfd4ca (written after seeing tonight's seven results)",
           test="arrow_singletons (A on songs by single-song artists, cross-song OLS, HC1)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           prediction_pp_per_sd=PRED, kill_below=KILL, threshold_p=ALPHA, threshold_z=round(ZC, 4),
           fake_outcome=bool(os.environ.get("FAKE_Y")),
           status_note="After-seeing-results test: a pass is a lead needing confirmation on songs not yet used, never a finding.")
r4 = C.r4

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1,
              default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)

# ---------------------------------------------------------------- the measure (copied unchanged from ../arrow_of_time/test.py)
def changes(harmony):
    seq = [C.chord_pcs(h) for h in sorted(harmony or [], key=lambda h: h["onset"])]   # Python's stable sort
    return [s for i, s in enumerate(seq) if i == 0 or s != seq[i - 1]]

def clip_vals(harmony):
    """(K, A, G2) for one clip; A and G2 are nan when K < 6."""
    s = changes(harmony); K = max(len(s) - 1, 0)
    if K < 6: return K, np.nan, np.nan
    n = {}
    for x, y in zip(s, s[1:]): n[(x, y)] = n.get((x, y), 0) + 1
    A = 1.0 - sum(min(v, n.get((y, x), 0)) for (x, y), v in n.items()) / sum(n.values())
    G2 = sum(s[t + 2] == s[t] for t in range(K - 1)) / K
    return K, A, G2

# ---------------------------------------------------------------- 1. unit values (must reproduce)
CH = {"I": (0, [4, 3]), "IV": (5, [4, 3]), "V": (7, [4, 3]), "vi": (9, [3, 4])}   # tonic C
def prog(names, reps):
    seq = names * reps
    return [dict(onset=float(i), offset=float(i + 1), root_pitch_class=CH[c][0], root_position_intervals=CH[c][1]) for i, c in enumerate(seq)]
UNIT = [("I-V-vi-IV x4", ["I", "V", "vi", "IV"], 4, 15, 1.0000, 0.0000),
        ("I-IV x8", ["I", "IV"], 8, 15, 0.0667, 0.9333),
        ("I-V-I-IV x4", ["I", "V", "I", "IV"], 4, 15, 0.0667, 0.4667)]
OUT["unit_values"] = []
for name, nm, reps, k0, a0, g0 in UNIT:
    K, A, G2 = clip_vals(prog(nm, reps))
    ok = K == k0 and round(A, 4) == a0 and round(G2, 4) == g0
    print(f"unit {name}: changes {K} [{k0}], A {A:.4f} [{a0:.4f}], G2 {G2:.4f} [{g0:.4f}] -> {'ok' if ok else 'MISMATCH'}", flush=True)
    OUT["unit_values"].append(dict(progression=name, changes=K, A=r4(A), G2=r4(G2), reproduced=ok))
    assert ok, "unit values not reproduced: stopping before anything else is read"

# ---------------------------------------------------------------- 2. singleton rows and A from the notes
D = C.load_rows(); allsongs = D["allsongs"]
nart = collections.Counter(r["artist"] for r in allsongs)
rows = [r for r in allsongs if nart[r["artist"]] == 1]; n = len(rows)
r05 = set(r["artist"] for r in D["rows"])
assert not any(r["artist"] in r05 for r in rows)
for r in rows: r["half"] = int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
HV = np.array([r["half"] for r in rows])
print(f"singleton rows: {n} songs [3,610], {len(set(r['artist'] for r in rows))} artists [3,610], of {len(allsongs)} songs; "
      f"halves {int((HV == 0).sum())} / {int((HV == 1).sum())} songs [1,852 / 1,758]; none in run 04's / tonight's rows", flush=True)
R = C.raw_clips(); missing = 0
for r in rows:
    vals = []
    for c in r["clips"]:
        a = R.get(c["k"])
        if a is None: missing += 1; vals.append((0, np.nan, np.nan)); continue
        vals.append(clip_vals(a.get("harmony")))
    K = np.array([v[0] for v in vals], float); A = np.array([v[1] for v in vals]); G = np.array([v[2] for v in vals])
    ok = np.isfinite(A)
    r["A"] = float(np.average(A[ok], weights=K[ok])) if ok.any() else np.nan
    r["G2"] = float(np.average(G[ok], weights=K[ok])) if ok.any() else np.nan
    r["A_c12"] = (A[0], A[1]) if len(A) >= 2 and np.isfinite(A[:2]).all() else None
    r["Ktot"] = float(K.sum()); r["ln_chg"] = float(np.log(max(K.sum(), 1.0)))
Av = np.array([r["A"] for r in rows]); has = np.isfinite(Av)
q = np.percentile(Av[has], [10, 50, 90])
lnchg = np.array([r["ln_chg"] for r in rows])
rhoAR = C.sp(Av, [r["ch_rep"] for r in rows]); rhoAG = C.sp(Av, [r["G2"] for r in rows])
print(f"raw clips missing: {missing}; songs with A {int(has.sum())} [3,229] of {n}; 10/50/90th pct {q[0]:.3f} / {q[1]:.3f} / {q[2]:.3f} "
      f"[0.333 / 0.864 / 1.000]; share exactly 1 (of songs with A): {np.mean(Av[has] == 1):.3f} [0.413]; "
      f"rho(A, ch_rep) {rhoAR[0]:+.3f} [+0.04]; rho(A, G2) {rhoAG[0]:+.3f}", flush=True)
OUT["notes"] = dict(singleton_songs=n, singleton_artists=len(set(r["artist"] for r in rows)), half_songs=[int((HV == 0).sum()), int((HV == 1).sum())],
                    raw_clips_missing=missing, songs_with_A=int(has.sum()), pct_10_50_90=[r4(x) for x in q],
                    share_A_eq_1=r4(np.mean(Av[has] == 1)), rho_A_ch_rep=r4(rhoAR[0]), rho_A_G2=r4(rhoAG[0]))

# ---------------------------------------------------------------- 3. gate (notes only)
gt = C.gate(rows, "A", extra={"ln_chg": list(lnchg)})
print(f"GATE stability (clip 1 vs clip 2, {gt['clip_pairs']} pairs [896]): {gt['clip_to_clip']} [0.339], needs >= 0.20; "
      f"largest overlap {gt['overlap_largest']} [ln_chg -0.187], needs |rho| <= 0.7", flush=True)
print("  overlap all: " + json.dumps(gt["overlap_all"]), flush=True)
print(f"GATE: {'PASSED' if gt['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = gt
if not gt["passed"]:
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- columns (model rows)
fe_ok = np.array([all(np.isfinite(r[f]) for f in C.FE) for r in rows])
MR = has & fe_ok; mi = np.nonzero(MR)[0]; mrows = [rows[i] for i in mi]; nm_ = len(mi)
print(f"model rows (A and all 17 measures finite): {nm_} [3,223]; songs with A but a measure missing: {int((has & ~fe_ok).sum())}", flush=True)
CN, CX = C.controls(mrows)
def zcol(v): return C.zs(np.asarray(v, float))   # population SD, over the model rows
zA = zcol(Av[mi]); zG2 = zcol([rows[i]["G2"] for i in mi])
ZF = {f: zcol([r[f] for r in mrows]) for f in C.FE}
def design(meas, measname="z_A", others=True):
    cols = collections.OrderedDict([(measname, meas)])
    for f in C.FE:
        if others or f in ("ch_rep", "ch_ic_mean"): cols["z_" + f] = ZF[f]
    cols["ln_chg"] = lnchg[mi]
    for j, c in enumerate(CN): cols[c] = CX[:, j]
    cols["intercept"] = np.ones(nm_)
    names = list(cols); X = np.column_stack(list(cols.values()))
    return names, X
NAMES0, X0 = design(zA)
keepc = [j for j, c in enumerate(NAMES0) if c == "intercept" or np.ptp(X0[:, j]) > 0]
dropped_cols = [c for j, c in enumerate(NAMES0) if j not in keepc]
print(f"columns ({len(NAMES0)}): {NAMES0}", flush=True)
print(f"columns dropped for no variation in the model rows: {dropped_cols}", flush=True)
# No model row has fewer than 5 chords (A needs 6+ changes), so if run 04's chord-count bins 1..9 cover every row they add up to
# the intercept (run 04 never met this: its artist fixed effect absorbed the intercept). The lowest bin then becomes the
# reference. This is found from the notes before any outcome is read and changes no estimate or SE of z(A) (the fitted space is
# the same); it only makes the design full rank for HC1's N/(N-K) and for the logit.
_bins = [j for j, c in enumerate(NAMES0) if c.startswith("nch_bin") and c not in dropped_cols]
collinear_ref = None
if _bins and np.all(X0[:, _bins].sum(1) == 1):
    collinear_ref = NAMES0[_bins[0]]; dropped_cols.append(collinear_ref)
    print(f"chord-count bins cover every model row and add up to the intercept: {collinear_ref} becomes the reference (dropped)", flush=True)
OUT["columns"] = dict(all=NAMES0, dropped_no_variation=[c for c in dropped_cols if c != collinear_ref],
                      dropped_as_reference_for_collinearity=collinear_ref)
def prune(names, X):
    k = [j for j, c in enumerate(names) if c not in dropped_cols]
    return [names[j] for j in k], X[:, k]
NAMES, X = prune(NAMES0, X0)
rk = np.linalg.matrix_rank(X)
print(f"design: {X.shape[0]} x {X.shape[1]}, rank {rk}", flush=True)
OUT["columns"]["used"] = NAMES; OUT["columns"]["rank"] = int(rk)
assert rk == X.shape[1], "design is not full rank"
assert NAMES[0] == "z_A"
iREP = NAMES.index("z_ch_rep")

def ols_hc1(Xm, yv):
    """OLS with HC1 SE: V = N/(N-K) (X'X)^-1 X' diag(u^2) X (X'X)^-1. Columns with no variation in this sample
    (other than the intercept) are dropped and reported as nan."""
    k = [j for j in range(Xm.shape[1]) if np.ptp(Xm[:, j]) > 0 or np.all(Xm[:, j] == 1)]
    Xk = Xm[:, k]; Nn = Xk.shape[0]; Kk = int(np.linalg.matrix_rank(Xk))   # K = rank (equals the column count when full rank)
    XtXi = np.linalg.pinv(Xk.T @ Xk); b2 = XtXi @ Xk.T @ yv; u = yv - Xk @ b2
    V = Nn / (Nn - Kk) * XtXi @ ((Xk * (u ** 2)[:, None]).T @ Xk) @ XtXi
    b = np.full(Xm.shape[1], np.nan); se = np.full(Xm.shape[1], np.nan); b[k] = b2; se[k] = np.sqrt(np.diag(V))
    return dict(b=b, se=se, p=2 * NRM.sf(np.abs(b / se)), N=Nn, G=Nn, K=Kk, rank=int(np.linalg.matrix_rank(Xk)))

# ---------------------------------------------------------------- 4. notes-side power
def resid_ss(Xm):
    x = Xm[:, 0]; o = Xm[:, 1:]; xt = x - o @ np.linalg.lstsq(o, x, rcond=None)[0]; return float(xt @ xt)
ss = resid_ss(X); se_b = np.sqrt(0.22 * 0.78) * 100 / np.sqrt(ss)
pw_n = C.power(PRED, se_b, ALPHA); pw_n05 = C.power(PRED, se_b, 0.05)
kt_n, k0_n = NRM.cdf((KILL - PRED) / se_b), NRM.cdf(KILL / se_b)
print(f"NOTES-SIDE POWER: residual share {ss / nm_:.3f} [0.921] on {nm_} songs; SE bound {se_b:.3f} pp [0.76]; "
      f"power at +0.6, p < .00625: {pw_n:.3f} [0.03]; at p < .05: {pw_n05:.3f} [0.12]; kill fires {kt_n:.0%} if +0.6 true [30%], "
      f"{k0_n:.0%} if zero [60%]", flush=True)
OUT["notes_side_power"] = dict(residual_share=r4(ss / nm_), songs=nm_, se_bound_pp=r4(se_b), power_p00625=r4(pw_n), power_p05=r4(pw_n05),
                               kill_fires_if_pred_true=r4(kt_n), kill_fires_if_zero=r4(k0_n))
if os.environ.get("GATE_ONLY"): print("GATE_ONLY: stopping before the outcome", flush=True); sys.exit(0)

# ---------------------------------------------------------------- 5. outcome
if os.environ.get("FAKE_Y"):   # code check: random outcome, no outcome file read
    rs = np.random.default_rng(7)
    for r in rows:
        r.update(y=100.0 * (rs.random() < 0.15), versions=None)
        r["y_foreign"] = (np.nan if rs.random() < 0.03 else 100.0 * (rs.random() < 0.5)) if r["y"] else 0.0
        if r["y"]: r["versions"] = [[["x"]], [["karaoke y"]]]
    LO = dict(fake=True)
else:
    LO = C.load_outcomes(rows, HERE)
print(f"\nOUTCOME joined: {json.dumps(LO)}", flush=True)
yf_all = np.array([r["y_foreign"] for r in rows], float); yy_all = np.array([r["y"] for r in rows], float)
yfm = yf_all[mi]; yym = yy_all[mi]; S = np.isfinite(yfm)   # S indexes model rows

# ---------------------------------------------------------------- 6. counts
cnt = dict(N=int(S.sum()), y_foreign_100=int((yfm[S] > 0).sum()), share_y_foreign=r4((yfm[S] > 0).mean()),
           y_100_in_model_rows=int((yym > 0).sum()), singleton_songs=n, dropped_no_A=int((~has).sum()),
           dropped_measure_missing=int((has & ~fe_ok).sum()), dropped_y_foreign_nan=int((~S).sum()),
           drop_reasons=dict(collections.Counter(rows[i].get("drop_reason") for i in mi if not np.isfinite(rows[i]["y_foreign"]))),
           half_N=[int((S & (HV[mi] == h)).sum()) for h in (0, 1)])
print(f"COUNTS: N {cnt['N']}, y_foreign = 100: {cnt['y_foreign_100']} ({cnt['share_y_foreign']}); in Discogs-VI at all (y = 100) among model rows: "
      f"{cnt['y_100_in_model_rows']}; dropped: no A {cnt['dropped_no_A']}, a measure missing {cnt['dropped_measure_missing']}, "
      f"y_foreign NaN {cnt['dropped_y_foreign_nan']} {cnt['drop_reasons']}; halves N {cnt['half_N']}", flush=True)
OUT["counts"] = cnt

# ---------------------------------------------------------------- 7. HC1 SE and power, before the estimate
M = ols_hc1(X[S], yfm[S])
se = M["se"][0]; pw = C.power(PRED, se, ALPHA); pw05 = C.power(PRED, se, 0.05)
print(f"POWER: HC1 SE {se:.4f} pp [notes bound {se_b:.3f}]; power at +0.6, p < .00625: {pw:.3f}; at p < .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_p00625=r4(pw), power_p05=r4(pw05),
                    kill_fires_if_pred_true=r4(NRM.cdf((KILL - PRED) / se)), kill_fires_if_zero=r4(NRM.cdf(KILL / se)))

# ---------------------------------------------------------------- 8. estimate, halves, logit, verdict
b, p = M["b"][0], M["p"][0]
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], K=M["K"], rank=M["rank"],
                      all_columns={c: C.summ(M, i) for i, c in enumerate(NAMES)})
print(f"PRIMARY OLS (HC1) z(A): beta {b:+.4f} pp per SD (predicted +0.6), SE {se:.4f}, p {p:.4g}, "
      f"95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; N {M['N']}, K {M['K']}", flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = S & (HV[mi] == h); HM[h] = ols_hc1(X[s], yfm[s])
    d = dict(half=h, songs=HM[h]["N"], y_foreign_100=int((yfm[s] > 0).sum()), K=HM[h]["K"], **C.summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {d['songs']} songs, y_foreign=100 {d['y_foreign_100']}, K {d['K']}; beta {d['beta']:+.4f} (SE {d['se']:.4f}, p {d['p']:.3g})", flush=True)

def logit(Xm, yb):
    import statsmodels.api as sm
    k = [j for j in range(Xm.shape[1]) if np.ptp(Xm[:, j]) > 0 or np.all(Xm[:, j] == 1)]
    info = dict(columns_used=len(k))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mod = sm.Logit(yb, Xm[:, k])
        fit = mod.fit(method="bfgs", maxiter=2000, disp=False)
        g = float(np.max(np.abs(mod.score(fit.params)))); conv = g / len(yb) < 1e-5; info["newton_used"] = False
        if not conv:
            fit = mod.fit(start_params=fit.params, method="newton", maxiter=100, disp=False)
            g = float(np.max(np.abs(mod.score(fit.params)))); conv = g / len(yb) < 1e-5; info["newton_used"] = True
    params = np.full(Xm.shape[1], np.nan); bse = params.copy(); pv = params.copy()
    params[k] = fit.params; bse[k] = fit.bse; pv[k] = fit.pvalues
    info.update(max_abs_score=g, nobs=int(len(yb)), converged=bool(conv), llf=float(fit.llf))
    return params, bse, pv, info

yb = (yfm[S] > 0).astype(float)
try:
    lp, lse, lpv, linfo = logit(X[S], yb)
except Exception as e:
    lp = np.full(X.shape[1], np.nan); lse = lp.copy(); lpv = lp.copy(); linfo = dict(error=repr(e), converged=False)
    print(f"LOGIT failed: {e!r}", flush=True)
big = [(c, r4(a_)) for c, a_ in zip(NAMES, lp) if np.isfinite(a_) and abs(a_) > 5]
lg = dict(coef=r4(lp[0]), se=r4(lse[0]), p=float(f"{lpv[0]:.4g}") if np.isfinite(lpv[0]) else None, convergence_test="max|score|/nobs < 1e-5",
          columns_abs_coef_over_5=big, all_columns={c: [r4(a_), r4(b_)] for c, a_, b_ in zip(NAMES, lp, lse)}, **linfo)
OUT["logit"] = lg
print(f"LOGIT (sign check): z(A) coef {lp[0]:+.4f} log-odds per SD (SE {lse[0]:.4f}, p {lpv[0]:.4g}); converged: {linfo.get('converged')} "
      f"(max|score| {linfo.get('max_abs_score', float('nan')):.3g}, nobs {linfo.get('nobs')}, Newton used {linfo.get('newton_used')})", flush=True)
if big: print(f"  columns with |coef| > 5: {big}", flush=True)
conv = bool(linfo.get("converged")); cb = lp[0]

hb = [HM[h]["b"][0] for h in (0, 1)]
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and cb > 0:
    v = "pass (a lead only, needing confirmation on songs not yet used; never a finding)"
elif b < 0 and p < ALPHA: v = "opposite sign (beta < 0, p < .00625): killed; reported as a new hypothesis, not a pass"
elif b < KILL: v = "kill (beta < +0.2 pp per SD)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00625")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("logit did not converge")
    elif not cb > 0: why.append("logit sign disagrees")
    v = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the written rule): {v}", flush=True)

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
dn["ch_rep_in_primary_model"] = C.summ(M, iREP)
nm2, X2 = prune(*design(zA, others=False)); m = ols_hc1(X2[S], yfm[S])
dn["without_the_15_other_measures"] = dict(**C.summ(m, 0), ch_rep=C.summ(m, nm2.index("z_ch_rep")), K=m["K"])
m = ols_hc1(X, yym); dn["A_on_y_in_DiscogsVI_at_all"] = dict(**C.summ(m, 0), N=m["N"], y_100=int((yym > 0).sum()),
                                                            note="all model rows (y is defined for every row)")
nmG, XG = prune(*design(zG2, "z_G2")); m = ols_hc1(XG[S], yfm[S]); dn["G2_in_place_of_A"] = dict(**C.summ(m, 0), rho_A_G2=r4(rhoAG[0]))
kw = ("karaoke", "tribute")
nrm = lambda s_: re.sub(r"[^a-z0-9]", "", s_.lower().replace("&", "and"))
yk = yfm.copy(); nchg_k = 0; nkt = 0
for t, i in enumerate(mi):
    r = rows[i]
    if not np.isfinite(yfm[t]) or r.get("versions") is None: continue
    sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
    nkt += int(any(k in nm.lower() for s_ in sets for nm in s_ for k in kw))
    own = [s_ for s_ in sets if any(nrm(nm) == a for nm in s_)]
    O = {nrm(nm) for s_ in own for nm in s_}
    keep_sets = [s_ for s_ in sets if not any(k in nm.lower() for nm in s_ for k in kw)]
    new = 100.0 if [s_ for s_ in keep_sets if len(s_) > 0 and not any(nrm(nm) in O for nm in s_)] else 0.0
    nchg_k += int(new != yfm[t]); yk[t] = new
m = ols_hc1(X[S], yk[S])
dn["y_foreign_without_karaoke_tribute_sets"] = dict(**C.summ(m, 0), songs_switched_to_0=nchg_k, songs_with_any_karaoke_or_tribute_set=nkt,
                                                    y_foreign_100=int((yk[S] > 0).sum()))
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k_, v_ in dn.items(): print(f"  {k_}: {json.dumps(v_)}", flush=True)
OUT["reported_deciding_nothing"] = dn

# ---------------------------------------------------------------- 10. result.json
finish(v)
