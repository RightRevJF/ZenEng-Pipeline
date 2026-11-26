"""Run 06, fresh_arrow: within an artist's own songs, does the arrow of time A (run 05's detailed-balance asymmetry of chord
changes) go with a higher chance that another performer released the song, on FRESH songs whose outcome had never been joined?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 08b5167 before any outcome was joined); the shared fresh
rules are ../fresh_repetition/PREDICTION.md; the code is ../common.py (frozen) and run05/experiments/common.py (C5).
Measure A (common.A_clip): chord pitch-class sets in onset order, consecutive equal sets collapsed to s_0..s_K; K < 6: no value;
A = 1 - sum min(n_ij, n_ji) / sum n_ij. Song A = K-weighted mean over clips with a value (common.k_weighted).
Model: LPM of y_foreign on z_fresh(A), z_seen(A), z(ch_rep), battery controls (run 04's block, ln_chg, V, has_mel, fresh),
artist fixed effect, CR1 by artist; seen + fresh battery rows with a value of A. Tested slope: z_fresh.
PASS: beta > 0, two-sided p < .05/6, beta > 0 in both artist halves, conditional logit > 0 and converged.
KILL: beta <= 0. OPPOSITE SIGN (beta < 0, p < .00833): killed, joins arrow_singletons. Else UNSETTLED.
Order (PREDICTION.md): 1 unit values, seen reproduction; 2 rows and columns; 3 gate (stop if it fails); 4 notes-side power;
5 validate_match; 6 load_battery_outcomes; 7 counts; 8 clustered SE and power; 9 beta, halves, logit, verdict; 10 reported; 11 result.json.

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
Env (code checks only): FAKE_Y=<dir> uses a random outcome (no outcome file is read) and writes result.json there.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, re
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C
C5 = C.C5

ALPHA = C.ALPHA; PRED = 0.6
FAKE = os.environ.get("FAKE_Y")
OUTDIR = FAKE or HERE
r4 = C.r4
OUT = dict(rule="PREDICTION.md in this folder (commit 08b5167); shared rules ../fresh_repetition/PREDICTION.md; code ../common.py",
           test="fresh_arrow (arrow of time A on fresh songs, within artist)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           prediction_pp_per_sd=PRED, kill="beta <= 0", threshold_p=round(ALPHA, 6), fake_outcome=bool(FAKE), deviations=[])

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1,
              default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)

def G2_clip(a):
    """run 05's back-and-forth share (arrow_of_time/test.py): share of t < K-1 with s_{t+2} == s_t, over K; nan if K < 6."""
    s = [S for S, _ in C.chord_runs(a)]; K = len(s) - 1
    if K < 6: return np.nan
    return sum(s[t + 2] == s[t] for t in range(K - 1)) / K

# ---------------------------------------------------------------- 1. unit values (must reproduce)
CHD = {"I": (0, [4, 3]), "IV": (5, [4, 3]), "V": (7, [4, 3]), "vi": (9, [3, 4])}
def prog(names, reps):
    seq = names * reps
    return dict(harmony=[dict(onset=float(i), offset=float(i + 1), root_pitch_class=CHD[c][0], root_position_intervals=CHD[c][1])
                         for i, c in enumerate(seq)])
UNIT = [("I-V-vi-IV x4", ["I", "V", "vi", "IV"], 4, 1.0000, 0.0000), ("I-IV x8", ["I", "IV"], 8, 0.0667, 0.9333),
        ("I-V-I-IV x4", ["I", "V", "I", "IV"], 4, 0.0667, 0.4667)]
OUT["unit_values"] = []
for name, nm, reps, a0, g0 in UNIT:
    a = prog(nm, reps); A = C.A_clip(a); G = G2_clip(a); K = C.K_of(a)
    ok = round(A, 4) == a0 and round(G, 4) == g0
    print(f"unit {name}: K {K}, A {A:.4f} [{a0:.4f}], G2 {G:.4f} [{g0:.4f}] -> {'ok' if ok else 'MISMATCH'}", flush=True)
    OUT["unit_values"].append(dict(progression=name, K=K, A=r4(A), G2=r4(G), reproduced=ok))
    assert ok, "unit values not reproduced: stopping before anything else is read"

# ---------------------------------------------------------------- seen reproduction and rows
B = C.battery(); seen9, rows, seen_all, fresh_all = B["seen_rows"], B["rows"], B["seen_all"], B["fresh_rows"]
C.add_measures(seen_all + fresh_all, which=("A", "V", "ln_chg"))
for r in seen_all + fresh_all: r["G2"], r["G2_c12"] = C.k_weighted(r, G2_clip)
Av9 = np.array([r["A"] for r in seen9], float); h9 = np.isfinite(Av9); q = np.percentile(Av9[h9], [10, 50, 90])
muA, sdA = C.seen_sd(seen9, "A"); murep, sdrep = C.seen_sd(seen9, "ch_rep")
print(f"seen within-artist rows {len(seen9)} [9,588]; with A {int(h9.sum())} [8,774]; 10/50/90th pct {q[0]:.3f} / {q[1]:.3f} / {q[2]:.3f} "
      f"[0.333 / 0.833 / 1.000]; mean {muA:.4f} [0.7589], SD {sdA:.4f} [0.2673]; ch_rep mean {murep:.4f} [0.2933] SD {sdrep:.4f} [0.2295]", flush=True)
nb = len(rows); nbf = sum(r["fresh"] for r in rows)
R = [r for r in rows if np.isfinite(r["A"])]; RF_ = [r for r in R if r["fresh"]]
cnt_rows = dict(battery_rows=nb, battery_fresh=nbf, battery_artists=len(set(r["artist"] for r in rows)),
                rows_with_A=len(R), seen_with_A=len(R) - len(RF_), fresh_with_A=len(RF_),
                fresh_artists=len(set(r["artist"] for r in RF_)), artists=len(set(r["artist"] for r in R)),
                fresh_rows_all=len(fresh_all))
print(f"fresh rows {len(fresh_all)} [1,825]; battery {nb} [5,768] with {nbf} fresh [1,295], {cnt_rows['battery_artists']} artists [601]; "
      f"with A: {len(R)} [4,920] = {len(R) - len(RF_)} seen [4,032] + {len(RF_)} fresh [888]; fresh by {cnt_rows['fresh_artists']} artists [448], "
      f"{cnt_rows['artists']} artists in all [590]", flush=True)
expect = dict(seen_with_A=8774, rows=9588, battery_rows=5768, battery_fresh=1295, battery_artists=601, fresh_rows_all=1825,
              rows_with_A=4920, seen_with_A_b=4032, fresh_with_A=888, fresh_artists=448, artists=590)
got = dict(seen_with_A=int(h9.sum()), rows=len(seen9), battery_rows=nb, battery_fresh=nbf, battery_artists=cnt_rows["battery_artists"],
           fresh_rows_all=len(fresh_all), rows_with_A=len(R), seen_with_A_b=len(R) - len(RF_), fresh_with_A=len(RF_),
           fresh_artists=cnt_rows["fresh_artists"], artists=cnt_rows["artists"])
repro = (got == expect and [round(x, 3) for x in q] == [0.333, 0.833, 1.0] and round(muA, 4) == 0.7589 and round(sdA, 4) == 0.2673
         and round(murep, 4) == 0.2933 and round(sdrep, 4) == 0.2295)
fz = [r["A_c12"] for r in fresh_all if r.get("A_c12")]
from scipy.stats import spearmanr
st_f = float(spearmanr([p[0] for p in fz], [p[1] for p in fz])[0])
nf_ch = float(np.mean([r["n_ch"] for r in RF_])); ns_ch = float(np.mean([r["n_ch"] for r in R if not r["fresh"]]))
print(f"mean pack chord tokens, all rows: fresh {np.mean([r['n_ch'] for r in fresh_all]):.1f} [10.6], seen {np.mean([r['n_ch'] for r in seen_all]):.1f} [14.4]", flush=True)
print(f"fresh clip 1 vs clip 2 (all fresh rows): {st_f:.3f} on {len(fz)} pairs [0.244 on 253]; mean pack chord tokens in the model rows: "
      f"fresh {nf_ch:.1f}, seen {ns_ch:.1f} (all-row figures in PREDICTION.md: 10.6 / 14.4)", flush=True)
OUT["reproduction"] = dict(got=got, expected=expect, seen_pct_10_50_90=[r4(x) for x in q], seen_mean_A=r4(muA), seen_sd_A=r4(sdA),
                           seen_mean_ch_rep=r4(murep), seen_sd_ch_rep=r4(sdrep), fresh_clip12=r4(st_f), fresh_clip12_pairs=len(fz),
                           mean_n_ch_model_rows=dict(fresh=r4(nf_ch), seen=r4(ns_ch)), reproduced=bool(repro))
print(f"REPRODUCTION: {'ok' if repro else 'MISMATCH'}", flush=True)
if not repro: finish("stopped (counts or unit values did not reproduce; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- 2. columns
zrep = lambda Rb: {"z_ch_rep": (np.array([r["ch_rep"] for r in Rb], float) - murep) / sdrep}
NAMES, X, (mu_, sd_) = C.fresh_design(R, "A", seen9, zrep(R))
art = np.array([r["artist"] for r in R]); HV = np.array([r["half"] for r in R]); FR = np.array([r["fresh"] for r in R], float)
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)
OUT["columns"] = NAMES

# ---------------------------------------------------------------- 3. gate (run 05's, on the seen rows)
gt = C.gate(seen9, "A", extra={"ln_chg": [r["ln_chg"] for r in seen9]})
print(f"GATE stability ({gt['clip_pairs']} pairs [3,294]): {gt['clip_to_clip']} [0.302], needs >= 0.20; largest overlap {gt['overlap_largest']} "
      f"[ln_chg -0.154], needs |rho| <= 0.7 (ch_rep {gt['overlap_all'].get('ch_rep')})", flush=True)
print(f"GATE: {'PASSED' if gt['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = gt; OUT["gate"]["fresh_clip12_reported"] = r4(st_f)
if not gt["passed"]: finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- 4. notes-side power
def notes_bound(Xm, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); c = np.bincount(gg)
    s = np.zeros((len(codes), Xm.shape[1])); np.add.at(s, gg, Xm); Xw = Xm - (s / c[:, None])[gg]
    x = Xw[:, 0]; o = Xw[:, 1:]; o = o[:, np.abs(o).sum(0) > 1e-12]
    xt = x - o @ np.linalg.lstsq(o, x, rcond=None)[0]; return float(np.sqrt(0.22 * 0.78) * 100 / np.sqrt(xt @ xt))
seb = notes_bound(X, art)
PF = json.load(open(os.path.join(os.path.dirname(HERE), "power_fake.json")))["fresh_arrow"]
OUT["notes_side_power"] = dict(se_bound_pp=r4(seb), power_at_threshold=r4(C.power(PRED, seb, ALPHA)), power_at_05=r4(C.power(PRED, seb, 0.05)),
                               fake_outcome_power=PF)
print(f"NOTES-SIDE POWER: SE bound {seb:.3f} pp [1.44]; power at +0.6, p < .00833: {C.power(PRED, seb, ALPHA):.3f}; at .05: {C.power(PRED, seb, 0.05):.3f}; "
      f"fake-outcome SE calibrated {PF['calibrated']['zero']['se_median']} / homogeneous {PF['homogeneous']['zero']['se_median']}, "
      f"pass rate if true {PF['calibrated']['true']['pass_rate']} / {PF['homogeneous']['true']['pass_rate']}", flush=True)

# ---------------------------------------------------------------- 5-6. validation and the outcome
if FAKE:   # code check: random outcome, no outcome file read
    rs = np.random.default_rng(11)
    for r in rows:
        y = 100.0 * (rs.random() < 0.2); r.update(y=y, y_foreign=0.0, versions=None, first_year=None, clique_seen=False)
        if y:
            fy = int(rs.integers(1960, 2015)); own = [[r["artist"]], fy, 1]
            r["versions"] = [own] + [[["x%d" % i] if rs.random() < 0.8 else ["karaoke band"], fy + int(rs.integers(0, 20)), 1] for i in range(int(rs.integers(0, 3)))]
            r["first_year"] = fy; r["clique_seen"] = bool(rs.random() < 0.05)
            r["y_foreign"], _ = C.y_foreign_of(r["artist"], r["versions"])
            if rs.random() < 0.03: r["y_foreign"] = np.nan
    LO = dict(fake=True)
else:
    LO = C.load_battery_outcomes(rows, HERE)
OUT["outcome_join"] = LO
print(f"\nOUTCOME joined: {json.dumps(LO, default=str)}", flush=True)
yf = np.array([r["y_foreign"] for r in R], float); yy = np.array([r["y"] for r in R], float)
S = np.isfinite(yf)

# ---------------------------------------------------------------- 7. counts
cnt = dict(N=int(S.sum()), artists=len(set(art[S])), fresh_N=int((S & (FR == 1)).sum()), seen_N=int((S & (FR == 0)).sum()),
           fresh_artists=len(set(art[S & (FR == 1)])),
           fresh_y_100=int((yy[FR == 1] > 0).sum()), fresh_y_foreign_100=int((yf[S & (FR == 1)] > 0).sum()),
           seen_y_100=int((yy[FR == 0] > 0).sum()), seen_y_foreign_100=int((yf[S & (FR == 0)] > 0).sum()),
           dropped_y_foreign_nan=dict(fresh=int((~S & (FR == 1)).sum()), seen=int((~S & (FR == 0)).sum())))
cnt["fresh_share_y_foreign"] = r4(cnt["fresh_y_foreign_100"] / max(cnt["fresh_N"], 1)); cnt["seen_share_y_foreign"] = r4(cnt["seen_y_foreign_100"] / max(cnt["seen_N"], 1))
print(f"COUNTS: {json.dumps(cnt)}", flush=True)
OUT["counts"] = cnt

# ---------------------------------------------------------------- 8. clustered SE and power, before the estimate
M = C.lpm(X[S], yf[S], art[S]); se = M["se"][0]
pw, pw05 = C.power(PRED, se, ALPHA), C.power(PRED, se, 0.05)
print(f"POWER: clustered SE {se:.4f} pp [fake-outcome 1.06 calibrated / 1.43 homogeneous; notes bound {seb:.3f}]; "
      f"power at +0.6, p < .00833: {pw:.3f}; at p < .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_at_threshold=r4(pw), power_at_05=r4(pw05))

# ---------------------------------------------------------------- 9. estimate, halves, conditional logit, verdict
b, p = M["b"][0], M["p"][0]
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"], all_columns={nm: C.summ(M, i) for i, nm in enumerate(NAMES)})
print(f"PRIMARY LPM z_fresh(A): beta {b:+.4f} pp per SD (predicted +0.6), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print(f"  z_seen(A) {M['b'][1]:+.3f} (SE {M['se'][1]:.3f}); z(ch_rep) {M['b'][2]:+.3f} (SE {M['se'][2]:.3f})", flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = S & (HV == h); HM[h] = C.lpm(X[s], yf[s], art[s])
    d = dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], fresh_songs=int((s & (FR == 1)).sum()),
             fresh_y_foreign_100=int((yf[s & (FR == 1)] > 0).sum()), **C.summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {d['songs']} songs ({d['fresh_songs']} fresh, {d['fresh_y_foreign_100']} fresh y_foreign=100), {d['artists']} artists; "
          f"beta {d['beta']:+.4f} (SE {d['se']:.4f}, p {d['p']:.3g})", flush=True)

def cl_exact(Xk, yk, gk):
    """run 05's fallback (arrow_of_time/test.py), unchanged: exact conditional logit likelihood by the subset recursion,
    scipy BFGS then Newton. Returns params, se, max|score|, info."""
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

yb = (yf[S] > 0).astype(float); t1 = time.time()
gS = art[S]; codes = {a: i for i, a in enumerate(sorted(set(gS)))}; gi = np.array([codes[a] for a in gS]); cntS = np.bincount(gi)
ga = np.bincount(gi, weights=yb); keep_g = (ga > 0) & (ga < cntS); keep = keep_g[gi]; ks, kg = int(keep.sum()), int(keep_g.sum())
Xk = X[S][keep]; sK = np.zeros((len(codes), X.shape[1])); np.add.at(sK, gi[keep], Xk); Xkd = Xk - (sK / np.maximum(cntS, 1)[:, None])[gi[keep]]
novar = [NAMES[j] for j in range(X.shape[1]) if np.all(np.abs(Xkd[:, j]) < 1e-12)]
cl = dict(columns_without_within_variation=novar, kept_fresh_songs=int((FR[S][keep] == 1).sum()))
print(f"CONDITIONAL LOGIT sample: {kg} artists, {ks} songs ({cl['kept_fresh_songs']} fresh); columns with no within-artist variation: {novar}", flush=True)
try:
    params, bse, pv, conv, _, _ = C.cond_logit(X[S], yb, art[S]); how = "statsmodels ConditionalLogit (run05 common.cond_logit)"
    if not np.isfinite(bse[0]): raise ValueError("non-finite SE for z_fresh")
except Exception as e:
    print(f"  statsmodels ConditionalLogit failed: {e!r}; using run 05's exact conditional likelihood (deviation, documented)", flush=True)
    cl["statsmodels_error"] = repr(e)
    OUT["deviations"].append(f"statsmodels ConditionalLogit failed ({e!r}); the conditional logit was fitted with run 05's exact-likelihood fallback "
                             "(arrow_of_time/test.py cl_exact), on the same sample, without columns that have no within-artist variation there")
    use = [j for j in range(X.shape[1]) if NAMES[j] not in novar]
    bb, ss_, gmax, info = cl_exact(Xk[:, use], yb[keep], gi[keep])
    params = np.full(X.shape[1], np.nan); bse = np.full(X.shape[1], np.nan); params[use] = bb; bse[use] = ss_
    from scipy.stats import norm as _N
    pv = 2 * _N.sf(np.abs(params / bse)); conv = bool(gmax / info["nobs"] < 1e-5)
    how = "exact conditional likelihood (subset recursion), scipy BFGS then Newton"; cl.update(max_abs_score=gmax, **info)
cl.update(coef=r4(params[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=bool(conv), optimiser=how, kept_songs=ks, kept_artists=kg,
          dropped_songs=int(S.sum() - ks), dropped_artists=int(len(codes) - kg), seconds=round(time.time() - t1),
          all_columns={nm: [r4(a_), r4(b_)] for nm, a_, b_ in zip(NAMES, params, bse)})
print(f"CONDITIONAL LOGIT: drops {cl['dropped_artists']} artists, {cl['dropped_songs']} songs (all 0 or all 1); z_fresh coef {params[0]:+.4f} "
      f"(SE {bse[0]:.4f}, p {pv[0]:.4g}); converged: {conv}", flush=True)
OUT["conditional_logit"] = cl

hb = [HM[h]["b"][0] for h in (0, 1)]; cb = params[0]
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and cb > 0: v = "pass"
elif b < 0 and p < ALPHA: v = "opposite sign (beta < 0, p < .00833): killed; joins arrow_singletons as evidence that vamps are what others take up"
elif b <= 0: v = "kill (beta <= 0)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00833")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb > 0: why.append("conditional logit sign disagrees")
    v = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the written rule): {v}", flush=True)

# ---------------------------------------------------------------- 10. reported, deciding nothing
dn = {}
def fit(Rb, Xb, yv, nm="z_fresh"):
    s = np.isfinite(yv); m = C.lpm(Xb[s], yv[s], np.array([r["artist"] for r in Rb])[s]); return m
def col(m, names, nm): i = names.index(nm); return C.summ(m, i)
dn["z_seen_A"] = col(M, NAMES, "z_seen")
# G2 in place of A
RG = [r for r in rows if np.isfinite(r["G2"])]
NG, XG, scG = C.fresh_design(RG, "G2", seen9, zrep(RG)); yG = np.array([r["y_foreign"] for r in RG], float)
m = fit(RG, XG, yG); dn["G2_in_place_of_A"] = dict(z_fresh=col(m, NG, "z_fresh"), z_seen=col(m, NG, "z_seen"), N=m["N"], seen_mean_sd=[r4(x) for x in scG],
                                                    rho_A_G2_fresh_model_rows=r4(C.sp([r["A"] for r in RF_], [r["G2"] for r in RF_])[0]))
# beta on y
m = fit(R, X, yy); dn["A_on_y"] = dict(z_fresh=col(m, NAMES, "z_fresh"), z_seen=col(m, NAMES, "z_seen"), N=m["N"])
# W01-J6a early and late uptake
EL = np.array([C.early_late(r) for r in R], float)
for j, nm in enumerate(("y_early", "y_late")):
    m = fit(R, X, EL[:, j]); dn[f"W01_J6a_{nm}"] = dict(z_fresh=col(m, NAMES, "z_fresh"), z_seen=col(m, NAMES, "z_seen"), N=m["N"],
                                                          fresh_100=int(np.nansum(EL[FR == 1, j] > 0)))
# karaoke / tribute sets removed (run 05's rule)
kw = ("karaoke", "tribute"); nrm = C.nrm; yk = yf.copy(); nsw = 0; nkt = 0
for i, r in enumerate(R):
    if not np.isfinite(yf[i]) or not r.get("versions"): continue
    sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
    nkt += int(any(k in nm_.lower() for s_ in sets for nm_ in s_ for k in kw))
    own = [s_ for s_ in sets if any(nrm(nm_) == a for nm_ in s_)]; O = {nrm(nm_) for s_ in own for nm_ in s_}
    ks_ = [s_ for s_ in sets if not any(k in nm_.lower() for nm_ in s_ for k in kw)]
    new = 100.0 if [s_ for s_ in ks_ if len(s_) > 0 and not any(nrm(nm_) in O for nm_ in s_)] else 0.0
    nsw += int(new != yf[i]); yk[i] = new
m = fit(R, X, yk); dn["y_foreign_without_karaoke_tribute"] = dict(z_fresh=col(m, NAMES, "z_fresh"), N=m["N"], songs_switched=nsw, songs_with_such_set=nkt)
# fresh rows whose clique is also a seen song's dropped
keep_cs = np.array([not (r["fresh"] and r.get("clique_seen")) for r in R])
m = C.lpm(X[S & keep_cs], yf[S & keep_cs], art[S & keep_cs])
dn["drop_fresh_clique_seen"] = dict(z_fresh=C.summ(m, 0), N=m["N"], dropped=int((~keep_cs).sum()))
# fresh rows with a video id only
keep_v = np.array([bool(r["vids"]) or not r["fresh"] for r in R])
m = C.lpm(X[S & keep_v], yf[S & keep_v], art[S & keep_v]); dn["fresh_with_video_id_only"] = dict(z_fresh=C.summ(m, 0), N=m["N"], dropped=int((~keep_v).sum()))
# fresh-only within-artist model
import collections
fa = collections.Counter(r["artist"] for i, r in enumerate(R) if r["fresh"] and S[i])
sel = np.array([bool(r["fresh"]) and S[i] and fa[r["artist"]] >= 2 for i, r in enumerate(R)])
use = [j for j, nm in enumerate(NAMES) if nm not in ("z_seen", "fresh")]
m = C.lpm(X[sel][:, use], yf[sel], art[sel])
dn["fresh_only_within_artist"] = dict(z_A=C.summ(m, 0), N=m["N"], artists=m["G"], y_foreign_100=int((yf[sel] > 0).sum()))
# without z(ch_rep); without has_mel
for drop_ in ("z_ch_rep", "has_mel"):
    use = [j for j, nm in enumerate(NAMES) if nm != drop_]
    m = C.lpm(X[S][:, use], yf[S], art[S]); dn[f"without_{drop_}"] = dict(z_fresh=C.summ(m, 0), N=m["N"])
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k_, v_ in dn.items(): print(f"  {k_}: {json.dumps(v_, default=str)}", flush=True)
OUT["reported_deciding_nothing"] = dn

# ---------------------------------------------------------------- 11. result.json
finish(v)
