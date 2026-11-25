"""Run 05, arrow_of_time: within an artist's own songs, do chord changes that run one way round (a Markov chain far from
detailed balance) go with a higher chance that a performer set sharing no name with the original artist released the song?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 1f6c36d before any outcome was joined).
Measure A, per clip: chord pitch-class sets in onset order (stable sort), consecutive equal sets collapsed to s_0..s_K;
clips with K < 6 have no value; n_ij = count of moves i -> j (no wrap); A = 1 - sum_ij min(n_ij, n_ji) / sum_ij n_ij.
Song A = mean over clips with a value, weighted by K. G2 (back-and-forth share) is printed, deciding nothing.
Model: LPM of y_foreign on z(A), z(ch_rep), z(ch_ic_mean), ln_chg and run 04's control block, artist fixed effect, CR1 by artist.
PASS: beta > 0, p < .00714 (.05/7, two-sided), beta > 0 in both artist halves, conditional-logit coefficient > 0 with convergence.
KILL: beta < +0.2 pp per SD.  OPPOSITE SIGN (beta < 0, p < .00714): killed, reported as a new hypothesis.  Else UNSETTLED.
Order (as the rule says): 1 unit values; 2 rows and A from the notes; 3 gate (stop if it fails); 4 notes-side power;
5 load_outcomes; 6 counts; 7 clustered SE and power; 8 beta, halves, conditional logit, verdict; 9 reported items; 10 result.json.

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
Runs in one process (BLAS threads pinned to 1).  python3 test.py -> result.json in this folder.
Env (code checks only): GATE_ONLY=1 stops before the outcome; FAKE_Y=<dir> uses a random outcome (no outcome file read) and writes there.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

ALPHA = 0.05 / 7; ZC = 2.690   # two-sided
PRED, KILL = 0.6, 0.2
OUTDIR = os.environ.get("FAKE_Y") or HERE
OUT = dict(rule="PREDICTION.md in this folder, commit 1f6c36d", test="arrow_of_time (A, detailed-balance asymmetry of chord changes)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           prediction_pp_per_sd=PRED, kill_below=KILL, threshold_p=round(ALPHA, 6), fake_outcome=bool(os.environ.get("FAKE_Y")))
r4 = C.r4

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1,
              default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)

# ---------------------------------------------------------------- the measure
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

# ---------------------------------------------------------------- 2. rows and A from the notes
D = C.load_rows(); rows = D["rows"]; n = len(rows)
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
    r["A_plain"] = float(np.mean(A[ok])) if ok.any() else np.nan
    r["G2"] = float(np.average(G[ok], weights=K[ok])) if ok.any() else np.nan
    r["A_c12"] = (A[0], A[1]) if len(A) >= 2 and np.isfinite(A[:2]).all() else None
    r["Ktot"] = float(K.sum()); r["ln_chg"] = float(np.log(max(K.sum(), 1.0)))
Av = np.array([r["A"] for r in rows]); has = np.isfinite(Av)
q = np.percentile(Av[has], [10, 50, 90])
print(f"raw clips missing from the full file: {missing}; songs with A {int(has.sum())} [8,774] of {n}; "
      f"10/50/90th pct {q[0]:.3f} / {q[1]:.3f} / {q[2]:.3f} [0.333 / 0.833 / 1.000]; share exactly 1: {np.mean(Av[has] == 1):.3f} [0.33]", flush=True)
lnchg = np.array([r["ln_chg"] for r in rows])
rhoAG = C.sp(Av, [r["G2"] for r in rows]); rhoAL = C.sp(Av, lnchg)
print(f"rho(A, G2) {rhoAG[0]:+.4f} on {rhoAG[1]} songs [-0.96]; rho(A, ln_chg) {rhoAL[0]:+.4f} [-0.15]", flush=True)
OUT["notes"] = dict(rows=n, raw_clips_missing=missing, songs_with_A=int(has.sum()), pct_10_50_90=[r4(x) for x in q],
                    share_A_eq_1=r4(np.mean(Av[has] == 1)), rho_A_G2=r4(rhoAG[0]), rho_A_ln_chg=r4(rhoAL[0]))

# ---------------------------------------------------------------- 3. gate (notes only)
gt = C.gate(rows, "A", extra={"ln_chg": list(lnchg)})
print(f"GATE stability (clip 1 vs clip 2, {gt['clip_pairs']} pairs [3,294]): {gt['clip_to_clip']} [0.302], needs >= 0.20; "
      f"largest overlap {gt['overlap_largest']} [ch_ic_mean +0.152; ln_chg -0.154], needs |rho| <= 0.7", flush=True)
print("  overlap all: " + json.dumps(gt["overlap_all"]), flush=True)
print(f"GATE: {'PASSED' if gt['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = gt
if not gt["passed"]:
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- columns
CN, CX = C.controls(rows)
zA = np.full(n, np.nan); zA[has] = C.zs(Av[has])                      # over songs with a value, population SD
zrep = C.zs([r["ch_rep"] for r in rows]); zic = C.zs([r["ch_ic_mean"] for r in rows])   # over the 9,588 rows
def design(meas, ln=True):
    cols = {"z_A": meas, "z_ch_rep": zrep, "z_ch_ic_mean": zic}
    if ln: cols["ln_chg"] = lnchg
    names = list(cols) + CN
    return names, np.column_stack(list(cols.values()) + [CX])
NAMES, X = design(zA)
art = np.array([r["artist"] for r in rows]); HV = np.array([r["half"] for r in rows])
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)

def resid_share(Xs, gs):
    """sum of squares of column 0's residual after the artist fixed effect and every other column, and N"""
    codes = {a: i for i, a in enumerate(sorted(set(gs)))}; gg = np.array([codes[a] for a in gs]); cnt = np.bincount(gg)
    s = np.zeros((len(codes), Xs.shape[1])); np.add.at(s, gg, Xs); Xd = Xs - (s / cnt[:, None])[gg]
    o = Xd[:, 1:]; x = Xd[:, 0]; xt = x - o @ np.linalg.lstsq(o, x, rcond=None)[0]
    return float(xt @ xt), len(Xs)

# ---------------------------------------------------------------- 4. notes-side power
ss, nn = resid_share(X[has], art[has])
se_b = np.sqrt(0.22 * 0.78) * 100 / np.sqrt(ss)
pw_n = C.power(PRED, se_b, ALPHA); pw_n05 = C.power(PRED, se_b, 0.05)
print(f"NOTES-SIDE POWER: residual share {ss / nn:.3f} [0.667] on {nn} songs; SE bound {se_b:.3f} pp [0.54]; "
      f"power at +0.6, p < .00714: {pw_n:.3f} [0.06]; at p < .05: {pw_n05:.3f} [0.20]", flush=True)
OUT["notes_side_power"] = dict(residual_share=r4(ss / nn), songs=nn, se_bound_pp=r4(se_b), power_p00714=r4(pw_n), power_p05=r4(pw_n05))
if os.environ.get("GATE_ONLY"): print("GATE_ONLY: stopping before the outcome", flush=True); sys.exit(0)

# ---------------------------------------------------------------- 5. outcome
if os.environ.get("FAKE_Y"):   # code check: random outcome, no outcome file read
    rs = np.random.default_rng(7)
    for r in rows:
        r.update(y=100.0 * (rs.random() < 0.23), covers=None, lcov=None, first_year=None, versions=None)
        r["y_foreign"] = (np.nan if rs.random() < 0.03 else 100.0 * (rs.random() < 0.4)) if r["y"] else 0.0
        if r["y"]: r.update(covers=int(rs.integers(1, 20)), first_year=int(rs.integers(1960, 2020)), versions=[[["x"]], [["karaoke y"]]])
        r["lcov"] = float(np.log1p(r["covers"])) if r["covers"] else None
    LO = dict(fake=True)
else:
    LO = C.load_outcomes(rows, HERE)
yf = np.array([r["y_foreign"] for r in rows], float); yy = np.array([r["y"] for r in rows], float)
S = has & np.isfinite(yf)
print(f"\nOUTCOME joined: {json.dumps(LO)}", flush=True)

# ---------------------------------------------------------------- 6. counts
n_noA = int((~has).sum()); n_nan = int((has & ~np.isfinite(yf)).sum()); n_nan_all = int((~np.isfinite(yf)).sum())
cnt = dict(N=int(S.sum()), artists=len(set(art[S])), y_foreign_100=int((yf[S] > 0).sum()), share_y_foreign=r4((yf[S] > 0).mean()),
           dropped_no_A=n_noA, dropped_y_foreign_nan_among_songs_with_A=n_nan, y_foreign_nan_all_rows=n_nan_all,
           singleton_artists_after_drops=int(sum(1 for a in set(art[S]) if (art[S] == a).sum() == 1)))
print(f"COUNTS: N {cnt['N']}, artists {cnt['artists']}, y_foreign = 100: {cnt['y_foreign_100']} ({cnt['share_y_foreign']}); "
      f"dropped: no A {n_noA}, y_foreign NaN (among songs with A) {n_nan} [NaN in all rows: {n_nan_all}]; "
      f"artists left with one song (add nothing): {cnt['singleton_artists_after_drops']}", flush=True)
OUT["counts"] = cnt

# ---------------------------------------------------------------- 7. clustered SE and power, before the estimate
M = C.lpm(X[S], yf[S], art[S])
se = M["se"][0]; pw = C.power(PRED, se, ALPHA); pw05 = C.power(PRED, se, 0.05)
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_b:.3f}]; power at +0.6, p < .00714: {pw:.3f}; at p < .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_p00714=r4(pw), power_p05=r4(pw05))

# ---------------------------------------------------------------- 8. estimate, halves, conditional logit, verdict
b, p = M["b"][0], M["p"][0]
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"],
                      all_columns={nm: C.summ(M, i) for i, nm in enumerate(NAMES)})
print(f"PRIMARY LPM z(A): beta {b:+.4f} pp per SD (predicted +0.6), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print(f"  other tested-nothing columns: ch_rep {M['b'][1]:+.3f} (SE {M['se'][1]:.3f}), ch_ic_mean {M['b'][2]:+.3f} (SE {M['se'][2]:.3f}), "
      f"ln_chg {M['b'][3]:+.3f} (SE {M['se'][3]:.3f})", flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = S & (HV == h); HM[h] = C.lpm(X[s], yf[s], art[s])
    d = dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], y_foreign_100=int((yf[s] > 0).sum()), **C.summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {d['songs']} songs, {d['artists']} artists, y_foreign=100 {d['y_foreign_100']}; beta {d['beta']:+.4f} (SE {d['se']:.4f}, p {d['p']:.3g})", flush=True)

def cl_exact(Xk, yk, gk):
    """Exact conditional (fixed-effect) logit likelihood by the subset recursion (elementary symmetric sums), as in run 04's
    cross-check. Maximised with scipy BFGS, then Newton (pseudo-inverse step, step halving). Returns params, se, max|score|, info."""
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
            nb = b - lam * step
            if fgh(nb, False)[0] >= ll - 1e-12: break
            lam /= 2
        b = nb
        if np.max(np.abs(lam * step)) < 1e-9: break
    ll, gr, H = fgh(b)
    se_ = np.sqrt(np.abs(np.diag(np.linalg.pinv(-H))))
    return b, se_, float(np.max(np.abs(gr))), dict(bfgs_success=bool(res.success), bfgs_message=str(res.message), newton_steps=it, llf=float(ll), nobs=nob)

yb = (yf[S] > 0).astype(float)
t1 = time.time(); Gs = len(set(art[S]))
gS = art[S]; codes = {a: i for i, a in enumerate(sorted(set(gS)))}; gi = np.array([codes[a] for a in gS]); cntS = np.bincount(gi)
ga = np.bincount(gi, weights=yb); keep_g = (ga > 0) & (ga < cntS); keep = keep_g[gi]
ks, kg = int(keep.sum()), int(keep_g.sum())
Xk = X[S][keep]; sK = np.zeros((len(codes), X.shape[1])); np.add.at(sK, gi[keep], Xk)
Xkd = Xk - (sK / np.maximum(cntS, 1)[:, None])[gi[keep]]
novar = [NAMES[j] for j in range(X.shape[1]) if np.all(np.abs(Xkd[:, j]) < 1e-12)]
print(f"CONDITIONAL LOGIT sample: keeps {kg} artists, {ks} songs; columns with no within-artist variation there: {novar}", flush=True)
cl = dict(columns_without_within_variation=novar)
try:
    params, bse, pv, conv, ks2, kg2 = C.cond_logit(X[S], yb, art[S]); how = "statsmodels ConditionalLogit (common.cond_logit)"
except Exception as e:
    print(f"  statsmodels ConditionalLogit failed: {e!r}; using the exact conditional likelihood with scipy (BFGS, then Newton), as the rule allows", flush=True)
    cl["statsmodels_error"] = repr(e)
    use = [j for j in range(X.shape[1]) if NAMES[j] not in novar]
    bb, ss_, gmax, info = cl_exact(Xk[:, use], yb[keep], gi[keep])
    params = np.full(X.shape[1], np.nan); bse = np.full(X.shape[1], np.nan); params[use] = bb; bse[use] = ss_
    from scipy.stats import norm as _N
    pv = 2 * _N.sf(np.abs(params / bse)); conv = bool(gmax / info["nobs"] < 1e-5)
    how = "exact conditional likelihood (subset recursion), scipy BFGS then Newton"; cl.update(max_abs_score=gmax, **info)
cl.update(coef=r4(params[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=conv, optimiser=how,
          convergence_test="max|score|/nobs < 1e-5", kept_songs=ks, kept_artists=kg, dropped_songs=int(S.sum() - ks),
          dropped_artists=int(Gs - kg), seconds=round(time.time() - t1),
          all_columns={nm: [r4(a_), r4(b_)] for nm, a_, b_ in zip(NAMES, params, bse)})
print(f"CONDITIONAL LOGIT: drops {cl['dropped_artists']} artists and {cl['dropped_songs']} songs (all 0 or all 1); keeps {kg} artists, {ks} songs; "
      f"z(A) coef {params[0]:+.4f} log-odds per SD (SE {bse[0]:.4f}, p {pv[0]:.4g}); converged: {conv}", flush=True)
big = [(nm, r4(a_)) for nm, a_ in zip(NAMES, params) if abs(a_) > 5]
if big: print(f"  columns with |coef| > 5 (no finite estimate likely): {big}", flush=True)
cl["columns_abs_coef_over_5"] = big
if big:   # cross-check, deciding nothing: statsmodels on the same sample without the columns that have no finite estimate
    try:
        use2 = [j for j in range(X.shape[1]) if NAMES[j] not in [b_[0] for b_ in big] + novar]
        p2, b2, pv2, cv2, _, _ = C.cond_logit(X[S][:, use2], yb, art[S])
        cl["crosscheck_without_nonfinite_columns"] = dict(dropped=[b_[0] for b_ in big], coef=r4(p2[0]), se=r4(b2[0]), p=float(f"{pv2[0]:.4g}"), converged=cv2)
        print(f"  cross-check (statsmodels, without {[b_[0] for b_ in big]}): z(A) coef {p2[0]:+.4f} (SE {b2[0]:.4f}, p {pv2[0]:.4g}), converged {cv2}", flush=True)
    except Exception as e:
        cl["crosscheck_without_nonfinite_columns"] = dict(error=repr(e)); print(f"  cross-check failed: {e!r}", flush=True)
OUT["conditional_logit"] = cl

hb = [HM[h]["b"][0] for h in (0, 1)]; cb = params[0]
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and cb > 0: v = "pass"
elif b < 0 and p < ALPHA: v = "opposite sign (beta < 0, p < .00714): killed; reported as a new hypothesis ('reversible vamps are what others take up'), not a pass"
elif b < KILL: v = "kill (beta < +0.2 pp per SD)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00714")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb > 0: why.append("conditional logit sign disagrees")
    v = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the written rule): {v}", flush=True)

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
zG = np.full(n, np.nan); zG[has] = C.zs(np.array([r["G2"] for r in rows])[has])
_, XG = design(zG); m = C.lpm(XG[S], yf[S], art[S]); dn["G2_in_place_of_A"] = C.summ(m, 0); dn["rho_A_G2"] = r4(rhoAG[0])
Sy = has; m = C.lpm(X[Sy], yy[Sy], art[Sy])
dn["A_on_y_in_DiscogsVI_at_all"] = dict(**C.summ(m, 0), N=m["N"], note="all songs with A (y is defined for every row)")
lc = np.array([np.nan if r["lcov"] is None else r["lcov"] for r in rows], float)
fy = np.array([np.nan if r["first_year"] is None else r["first_year"] for r in rows], float)
Si = has & (yy > 0) & np.isfinite(lc) & np.isfinite(fy)
zl = np.full(n, np.nan); zl[Si] = C.zs(lc[Si])
m = C.lpm(np.column_stack([X[Si], fy[Si]]), zl[Si], art[Si])
dn["intensive_margin_zlog1p_covers"] = dict(**C.summ(m, 0), N=m["N"], artists=m["G"],
    note="SD of log(1+covers) per SD of A; outcome standardised over this sample, z(A) as in the primary; first_year linear added")
kw = ("karaoke", "tribute")
nrm = lambda s_: __import__("re").sub(r"[^a-z0-9]", "", s_.lower().replace("&", "and"))
yk = yf.copy(); nchg_k = 0; nkt = 0
for i, r in enumerate(rows):
    if not np.isfinite(yf[i]) or r.get("versions") is None: continue
    sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
    nkt += int(S[i] and any(k in nm.lower() for s_ in sets for nm in s_ for k in kw))
    own = [s_ for s_ in sets if any(nrm(nm) == a for nm in s_)]
    O = {nrm(nm) for s_ in own for nm in s_}
    keep_sets = [s_ for s_ in sets if not any(k in nm.lower() for nm in s_ for k in kw)]
    new = 100.0 if [s_ for s_ in keep_sets if len(s_) > 0 and not any(nrm(nm) in O for nm in s_)] else 0.0
    nchg_k += int(new != yf[i]); yk[i] = new
m = C.lpm(X[S], yk[S], art[S])
dn["y_foreign_without_karaoke_tribute_sets"] = dict(**C.summ(m, 0), songs_switched_to_0=nchg_k, songs_with_any_karaoke_or_tribute_set=nkt, y_foreign_100=int((yk[S] > 0).sum()))
_, X0 = design(zA, ln=False); m = C.lpm(X0[S], yf[S], art[S]); dn["without_ln_chg"] = C.summ(m, 0)
Ap = np.array([r["A_plain"] for r in rows]); zAp = np.full(n, np.nan); zAp[has] = C.zs(Ap[has])
_, XP = design(zAp); m = C.lpm(XP[S], yf[S], art[S]); dn["unweighted_song_A"] = C.summ(m, 0)
dn["songs_artists_per_half"] = [dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"]) for h in (0, 1)]
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k_, v_ in dn.items(): print(f"  {k_}: {json.dumps(v_)}", flush=True)
OUT["reported_deciding_nothing"] = dn

# ---------------------------------------------------------------- 10. result.json
finish(v)
