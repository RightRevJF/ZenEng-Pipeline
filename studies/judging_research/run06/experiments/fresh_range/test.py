"""Run 06, fresh_range (idea R05-L2, melody range capped at three octaves, on fresh songs): within an artist's own songs, does a
narrower melody range go with more uptake by another artist (y_foreign), on Hooktheory songs whose outcome had never been seen?
The rule is PREDICTION.md in this folder plus the shared rules in ../fresh_repetition/PREDICTION.md and ../common.py, frozen and
pushed in commit 08b5167 (branch judging-research) before any outcome was joined.
Prediction: beta(z_fresh) on y_foreign = -0.7 pp per SD (SD 5.45 semitones). Pass: beta < 0, two-sided p < .05/6 = .00833, beta < 0
in both artist halves, conditional logit < 0 and converged. Kill: beta >= 0. Opposite sign (beta > 0, p < .00833): killed, reported
as a new hypothesis. Unsettled: anything else.
Order, as the rule says: 1. unit values; 2. seen reproduction and the cap's counts; 3. run 05's gate (stop if it fails); 4. notes-side
power; 5. common.validate_match; 6. common.load_battery_outcomes; 7. counts; 8. clustered SE and power; 9. beta, halves, logit,
verdict; 10. reported items; 11. result.json.
Code check: FAKE_Y=<dir> python3 test.py runs everything on a random fake outcome (no outcome file read) and writes result.json in <dir>.
BLAS threads limited to 1 (other experiments share the machine's 2 cores).
Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
HOOKTHEORY_RAW=/home/claude/dl/hooktheory/Hooktheory.json.gz python3 test.py -> result.json in this folder"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "1")
import sys, json, time
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C
from common import r4, nrm

ALPHA = C.ALPHA; ZC = 2.638
PRED = -0.7; MEAS = "L2c"
FAKE = os.environ.get("FAKE_Y")
OUTDIR = FAKE if FAKE else HERE
OUT = dict(rule="PREDICTION.md in this folder + ../fresh_repetition/PREDICTION.md + ../common.py, commit 08b5167 (branch judging-research)",
           test="fresh_range (R05-L2, folded melody range capped at 36 semitones, fresh songs)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)", fake_outcome=bool(FAKE),
           prediction_pp_per_sd=PRED, kill_rule="beta >= 0", threshold_p=ALPHA, tests_tonight=C.N_TESTS)

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True)

# ---------------------------------------------------------------- 1. unit values
def fake_clip(pitches):
    return {"melody": [{"onset": float(k), "offset": float(k + 1), "octave": p // 12, "pitch_class": p % 12} for k, p in enumerate(pitches)]}
UNITS = [([0, 4, 7, 12], 12), ([0, 4, 19, 12], 7), ([0, 2, 4, 5, 7, 9, 11, 12, 14, 16], 16)]
uv = []
for ps, want in UNITS:
    got = C.L2_clip(fake_clip(ps)); uv.append(dict(pitches=ps, want=want, got=got, ok=got == want))
    print(f"UNIT {ps}: {got} [{want}] {'ok' if got == want else 'MISMATCH'}", flush=True)
uv.append(dict(pitches=[0, 4, 7], want="nan (fewer than 4 notes)", got=str(C.L2_clip(fake_clip([0, 4, 7])))))
OUT["unit_values"] = uv
if not all(u["ok"] for u in uv[:3]):
    finish("stopped (unit values not reproduced)"); sys.exit(0)

# ---------------------------------------------------------------- 2. rows, L2, reproduction, the cap
B = C.battery(); rows_all, seen9, seen_all, fr = B["rows"], B["seen_rows"], B["seen_all"], B["fresh_rows"]
nb_f = sum(r["fresh"] for r in rows_all)
REPRO = dict(fresh_rows=[len(fr), 1825], battery_rows=[len(rows_all), 5768], battery_fresh=[nb_f, 1295],
             battery_artists=[len(set(r["artist"] for r in rows_all)), 601], seen_within_artist_rows=[len(seen9), 9588])
C.add_measures(seen_all + fr, which=("V", "ln_chg", "L2"))
C.song_measure(seen_all + fr, lambda a, c=None: C.L2_clip(a, fold=False), "L2u")      # unfolded range, reported only
for r in seen_all + fr: r["L2uc"] = r["L2u"] if np.isfinite(r["L2u"]) and r["L2u"] <= C.L2_CAP else np.nan

v9 = np.array([r["L2"] for r in seen9], float); v9c = np.array([r["L2c"] for r in seen9], float)
pct = np.nanpercentile(v9, [10, 50, 90]).round(3).tolist()
mu, sd = C.seen_sd(seen9, "L2c"); mu_u, sd_u = C.seen_sd(seen9, "L2")
bf = [r for r in rows_all if r["fresh"]]
bf_L2 = sum(np.isfinite(r["L2"]) for r in bf); bf_cap = sum(np.isfinite(r["L2"]) and not np.isfinite(r["L2c"]) for r in bf)
rows = [r for r in rows_all if np.isfinite(r["L2c"])]
nf = sum(r["fresh"] for r in rows)
REPRO.update(seen_with_value=[int(np.isfinite(v9).sum()), 9588], pct_10_50_90=[pct, [7, 11, 21]],
             seen_capped=[int((np.isfinite(v9) & ~np.isfinite(v9c)).sum()), 285], fresh_battery_with_melody=[int(bf_L2), 413],
             fresh_capped=[int(bf_cap), 9], z_mean=[r4(mu), 11.87], z_sd=[r4(sd), 5.45],
             rows=[len(rows), 4746], rows_seen=[len(rows) - nf, 4342], rows_fresh=[nf, 404], artists=[len(set(r["artist"] for r in rows)), 563],
             fresh_artists=[len(set(r["artist"] for r in rows if r["fresh"])), 260],
             # PREDICTION.md says "on the 9,588 seen rows the maximum is 1,030": 1,030 is the maximum over all 13,198 seen songs
             # (song value and clip value alike); over the 9,588 rows the song maximum is 674.08 (printed beside it). Descriptive only.
             seen_max_L2=[r4(np.nanmax([r["L2"] for r in seen_all])), 1030],
             uncapped_sd=[r4(sd_u), 17.5])
ok_all = True
for k, (got, want) in REPRO.items():
    if k in ("z_mean", "z_sd", "uncapped_sd"): ok = abs(got - want) < 0.006 if k != "uncapped_sd" else abs(got - want) < 0.05
    elif k == "seen_max_L2": ok = abs(got - want) < 0.5
    else: ok = got == want
    ok_all &= bool(ok)
    print(f"REPRO {k}: {got} [{want}] {'ok' if ok else 'MISMATCH'}", flush=True)
print(f"  (song maximum of L2 over the 9,588 within-artist rows: {np.nanmax(v9):.2f}; fresh battery maximum {np.nanmax([r['L2'] for r in bf]):.2f})", flush=True)
OUT["reproduction"] = dict(checks=REPRO, all_reproduced=ok_all, seen9_song_max_L2=r4(np.nanmax(v9)), fresh_battery_max_L2=r4(np.nanmax([r["L2"] for r in bf])))
if not ok_all:
    finish("stopped (counts not reproduced; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- 3. run 05's gate on the seen rows (notes only)
G = C.gate(seen9, "L2")
top5 = sorted(G["overlap_all"].items(), key=lambda kv: -abs(kv[1] or 0))[:5]
print(f"GATE 1, clip 1 vs clip 2 (seen): {G['clip_to_clip']} on {G['clip_pairs']} pairs [0.290 on 4,271]; needs >= 0.20", flush=True)
print(f"GATE 2, largest |Spearman|: {G['overlap_largest']} [mel_ic_mean +0.555]; ch_rep {G['overlap_all']['ch_rep']}; needs <= 0.7; top 5 {top5}", flush=True)
print(f"GATE: {'PASSED' if G['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = G
# reported, deciding nothing: the gate on the capped form, with V and ln_chg added to the overlap list; fresh clip agreement
Gc = C.gate(seen9, "L2", extra=dict(V=[r["V"] for r in seen9], ln_chg=[r["ln_chg"] for r in seen9]))
c9 = [r for r in seen9 if np.isfinite(r["L2c"])]
pr_c = [r["L2_c12"] for r in c9 if r.get("L2_c12") and max(r["L2_c12"]) <= C.L2_CAP]
from scipy.stats import spearmanr
stab_cap = float(spearmanr([p[0] for p in pr_c], [p[1] for p in pr_c])[0])
fp = [r["L2_c12"] for r in bf if r.get("L2_c12")]
stab_fresh = (float(spearmanr([p[0] for p in fp], [p[1] for p in fp])[0]), len(fp))
fa = [r["L2_c12"] for r in fr if r.get("L2_c12")]
stab_fresh_all = (float(spearmanr([p[0] for p in fa], [p[1] for p in fa])[0]), len(fa))
OUT["gate_reported"] = dict(overlap_with_V_ln_chg=dict(V=Gc["overlap_all"]["V"], ln_chg=Gc["overlap_all"]["ln_chg"]),
                            seen_clip_agreement_capped_rows_both_clips_le_36=[r4(stab_cap), len(pr_c)],
                            fresh_battery_clip_agreement=[r4(stab_fresh[0]), stab_fresh[1]],
                            all_1825_fresh_rows_clip_agreement=[r4(stab_fresh_all[0]), stab_fresh_all[1]], chair_fresh="0.396 on 52")
print(f"  reported: overlap V {Gc['overlap_all']['V']}, ln_chg {Gc['overlap_all']['ln_chg']}; seen clip agreement on capped rows "
      f"{stab_cap:.3f} ({len(pr_c)} pairs); fresh clip agreement, battery {stab_fresh[0]:.3f} ({stab_fresh[1]} pairs), all fresh rows "
      f"{stab_fresh_all[0]:.3f} ({stab_fresh_all[1]} pairs) [0.396 on 52]", flush=True)
if not G["passed"]:
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- columns
z9 = lambda Rb, nm: (np.array([r[nm] for r in Rb], float) - C.seen_sd(seen9, nm)[0]) / C.seen_sd(seen9, nm)[1]
def design(Rb, meas=MEAS):
    return C.fresh_design(Rb, meas, seen9, {"z_ch_rep": z9(Rb, "ch_rep")})
NAMES, X, (mu_, sd_) = design(rows)
print(f"columns ({len(NAMES)}): {NAMES}; z scale mean {mu_:.4f}, SD {sd_:.4f}", flush=True)
OUT["columns"] = NAMES; OUT["z_scale"] = dict(mean=r4(mu_), sd=r4(sd_))

# ---------------------------------------------------------------- 4. notes-side power (no outcome)
def demean(M, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); cnt = np.bincount(gg)
    M2 = np.asarray(M, float).reshape(len(g), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / cnt[:, None])[gg]
art0 = [r["artist"] for r in rows]
Xd = demean(X, art0); o = Xd[:, 1:]; o = o[:, np.abs(o).sum(0) > 1e-12]
xt = Xd[:, 0] - o @ np.linalg.lstsq(o, Xd[:, 0], rcond=None)[0]
se_ns = float(np.sqrt(0.22 * 0.78 / (xt @ xt)) * 100)
PF = json.load(open(os.path.join(C.HERE, "power_fake.json")))["fresh_range"]
pw_ns = dict(se_bound_pp=r4(se_ns), power_at_pred_threshold=r4(C.power(PRED, se_ns, ALPHA)), power_at_pred_p05=r4(C.power(PRED, se_ns, 0.05)),
             fake_outcome_power=dict(se_calibrated=PF["calibrated"]["zero"]["se_median"], se_homogeneous=PF["homogeneous"]["zero"]["se_median"],
                                     pass_rate_if_true_calibrated=PF["calibrated"]["true"]["pass_rate"],
                                     kill_fires_if_true=PF["calibrated"]["true"]["kill_rate"], kill_fires_if_zero=PF["calibrated"]["zero"]["kill_rate"],
                                     power_threshold_calibrated=PF["power_at_threshold_calibrated"], power_05_calibrated=PF["power_at_05_calibrated"]))
print(f"NOTES-SIDE POWER: SE bound {se_ns:.3f} pp [2.47]; power at -0.7, p < .00833: {pw_ns['power_at_pred_threshold']}; at .05: {pw_ns['power_at_pred_p05']}", flush=True)
print(f"  fake-outcome power (../power_fake.json): {json.dumps(pw_ns['fake_outcome_power'])}", flush=True)
OUT["notes_side_power"] = pw_ns

# ---------------------------------------------------------------- 5-6. validation, then the outcome
if FAKE:   # random outcome; no outcome file read
    rs = np.random.default_rng(6)
    for r in rows_all:
        r.update(y=0.0, y_foreign=0.0, versions=None, first_year=None, clique=None, clique_seen=False, drop_reason=None)
        if rs.random() < 0.2:
            r["y"] = 100.0; r["first_year"] = int(rs.integers(1960, 2020)); r["clique"] = str(rs.integers(1, 9)); r["clique_seen"] = bool(r["fresh"] and rs.random() < 0.1)
            sets = [[r["artist"]]] + ([["Karaoke Kings"]] if rs.random() < 0.2 else []) + ([["Other Band"]] if rs.random() < 0.7 else [])
            r["versions"] = [[s, int(rs.integers(1960, 2024)), [1]] for s in sets]
            r["y_foreign"] = np.nan if rs.random() < 0.03 else (100.0 if len(sets) > 1 else 0.0)
    LO = dict(fake=True); VAL = dict(fake=True)
else:
    VAL = C.validate_match(HERE)
    print("MATCH VALIDATION (cached in ../match_validation.json):", json.dumps({k: VAL[k] for k in VAL if not isinstance(VAL[k], list)}), flush=True)
    if not VAL["passed"]:
        OUT["validation"] = VAL; finish("stopped (validation failed)"); sys.exit(0)
    LO = C.load_battery_outcomes(rows_all, HERE)
OUT["validation"] = {k: VAL[k] for k in VAL if not isinstance(VAL[k], list)}
OUT["outcome_load"] = LO
print("OUTCOME LOAD:", json.dumps(LO, default=str), flush=True)

# karaoke / tribute variant (reported): own sets as in the primary outcome; foreign sets naming karaoke or tribute removed
KT = lambda s: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)
def ykt_of(r):
    if not np.isfinite(r["y_foreign"]): return np.nan
    if r["y_foreign"] <= 0: return 0.0
    sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
    own = [s for s in sets if any(nrm(nm) == a for nm in s)]; O = {nrm(nm) for s in own for nm in s}
    return 100.0 if [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s) and not KT(s)] else 0.0
for r in rows_all: r["ykt"] = ykt_of(r); r["y_early"], r["y_late"] = C.early_late(r)

# ---------------------------------------------------------------- 7. counts (rows with y_foreign NaN dropped from every model)
yf_all = np.array([r["y_foreign"] for r in rows], float); keep = np.isfinite(yf_all)
R = [r for r, k in zip(rows, keep) if k]; X = X[keep]
art = np.array([r["artist"] for r in R]); HV = np.array([r["half"] for r in R]); FR = np.array([r["fresh"] for r in R], bool)
yf = yf_all[keep]; y = np.array([r["y"] for r in R], float)
Gn = len(set(art))
CNT = dict(dropped_y_foreign_nan=int((~keep).sum()), dropped_fresh=int(sum(1 for r, k in zip(rows, keep) if not k and r["fresh"])),
           N=len(yf), artists=Gn, fresh_rows=int(FR.sum()), seen_rows=int((~FR).sum()),
           fresh_y1=int((y[FR] > 0).sum()), fresh_y_foreign1=int((yf[FR] > 0).sum()), fresh_share_y_foreign1=r4((yf[FR] > 0).mean()),
           seen_y1=int((y[~FR] > 0).sum()), seen_y_foreign1=int((yf[~FR] > 0).sum()), seen_share_y_foreign1=r4((yf[~FR] > 0).mean()),
           fresh_artists=len(set(art[FR])))
print(f"\nCOUNTS: {json.dumps(CNT)}", flush=True)
OUT["counts"] = CNT

# ---------------------------------------------------------------- 8. clustered SE and power, before the estimate
M = C.lpm(X, yf, art); se = float(M["se"][0])
pw = dict(clustered_se=r4(se), power_at_pred_threshold=r4(C.power(PRED, se, ALPHA)), power_at_pred_p05=r4(C.power(PRED, se, 0.05)))
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_ns:.3f}; fake calibrated 1.78]; power at -0.7, p < .00833: {pw['power_at_pred_threshold']}; "
      f"at p < .05: {pw['power_at_pred_p05']}", flush=True)
OUT["power"] = pw
try:
    import statsmodels.api as sm
    Xw = demean(X, art); yw = demean(yf, art).ravel(); kc = np.abs(Xw).sum(0) > 1e-12
    codes = {a: i for i, a in enumerate(sorted(set(art)))}; gg = np.array([codes[a] for a in art])
    smf = sm.OLS(yw, Xw[:, kc]).fit(cov_type="cluster", cov_kwds={"groups": gg, "df_correction": True})
    OUT["statsmodels_crosscheck_lpm"] = dict(beta_diff=float(abs(smf.params[0] - M["b"][0])), se_diff=float(abs(smf.bse[0] - M["se"][0])))
except Exception as e:
    OUT["statsmodels_crosscheck_lpm"] = dict(error=repr(e))
print(f"  (CR1 vs statsmodels cluster SE: {OUT['statsmodels_crosscheck_lpm']})", flush=True)

# ---------------------------------------------------------------- 9. beta, halves, conditional logit, verdict
b, p = float(M["b"][0]), float(M["p"][0])
dropped_cols = [NAMES[j] for j in range(len(NAMES)) if not np.isfinite(M["b"][j])]
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"], columns_without_within_artist_variation=dropped_cols,
                      others={nm: C.summ(M, j) for j, nm in enumerate(NAMES[:3]) if j > 0})
print(f"PRIMARY LPM: beta(z_fresh L2c) {b:+.4f} pp per SD (predicted -0.7), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to "
      f"{b + 1.96 * se:+.4f}; N {M['N']}, artists {M['G']}, K {M['K']}; dropped columns {dropped_cols}", flush=True)
print("  others: " + "; ".join(f"{k} {vv['beta']:+.3f} (SE {vv['se']:.3f}, p {vv['p']:.3g})" for k, vv in OUT["primary"]["others"].items()), flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = HV == h; HM[h] = C.lpm(X[s], yf[s], art[s])
    OUT["halves"].append(dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], fresh_rows=int(FR[s].sum()), fresh_y_foreign1=int((yf[s & FR] > 0).sum()), **C.summ(HM[h], 0)))
    print(f"HALF {h}: {HM[h]['N']} songs ({int(FR[s].sum())} fresh), {HM[h]['G']} artists; beta {HM[h]['b'][0]:+.4f} "
          f"(SE {HM[h]['se'][0]:.4f}, p {HM[h]['p'][0]:.3g})", flush=True)

def clogit(Xc, yy, g, names):
    """C5.cond_logit on the columns that vary within the artists it keeps (a column constant within every kept artist, such as
    has_mel here, is not identified in a conditional logit; the LPM drops the same columns). Column 0 is always kept."""
    yb = (yy > 0).astype(int); codes = {a: i for i, a in enumerate(sorted(set(g)))}; gi = np.array([codes[a] for a in g]); cnt = np.bincount(gi)
    ga = np.bincount(gi, weights=yb); kg = ((ga > 0) & (ga < cnt))[gi]
    Xk = demean(Xc[kg], list(np.asarray(g)[kg])); vc = np.where(np.abs(Xk).sum(0) > 1e-12)[0]; assert vc[0] == 0
    pa, bs, pv, conv, ks, kgn = C.cond_logit(Xc[:, vc], yb.astype(float), list(g))
    return dict(coef=r4(pa[0]), se=r4(bs[0]), p=float(f"{pv[0]:.4g}"), converged=conv, kept_songs=ks, kept_artists=kgn,
                dropped_songs=int(len(yb) - ks), dropped_artists=int(len(codes) - kgn), columns_dropped=[names[j] for j in range(len(names)) if j not in set(vc)],
                convergence_test="max|score|/nobs < 1e-5 (BFGS, then Newton)")
CL = clogit(X, yf, art, NAMES); OUT["conditional_logit"] = CL
print(f"CONDITIONAL LOGIT: keeps {CL['kept_songs']} songs, {CL['kept_artists']} artists (drops {CL['dropped_songs']} songs, "
      f"{CL['dropped_artists']} artists, all 0 or all 1; columns dropped {CL['columns_dropped']}); z_fresh coef {CL['coef']:+.4f} log-odds per SD, "
      f"SE {CL['se']:.4f}, p {CL['p']:.4g}; converged {CL['converged']}", flush=True)

hb = [float(HM[h]["b"][0]) for h in (0, 1)]; cb = CL["coef"]; conv = CL["converged"]
if b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0 and conv and cb < 0: verdict = "pass"
elif b > 0 and p < ALPHA: verdict = "opposite sign (beta > 0, p < .00833): killed; reported as a new hypothesis (wide-range showpieces are what others take up), not a pass"
elif b >= 0: verdict = "kill (beta >= 0)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00833")
    if not (hb[0] < 0 and hb[1] < 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb < 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"
print(f"\nVERDICT (by the frozen rule): {verdict}", flush=True)

# ---------------------------------------------------------------- 10. reported, deciding nothing
dn = {}
def fit_on(Rb, meas, yname, label, extra_note=None):
    Rb = [r for r in Rb if np.isfinite(r[meas]) and np.isfinite(r[yname])]
    nm, Xr, (m_, s_) = design(Rb, meas); yy = np.array([r[yname] for r in Rb], float); g = np.array([r["artist"] for r in Rb])
    m = C.lpm(Xr, yy, g); F = np.array([r["fresh"] for r in Rb], bool)
    d = dict(**C.summ(m, 0), N=m["N"], artists=m["G"], fresh_rows=int(F.sum()), fresh_outcome1=int((yy[F] > 0).sum()), z_mean=r4(m_), z_sd=r4(s_))
    if extra_note: d["note"] = extra_note
    dn[label] = d; return d
fit_on(rows_all, "L2", "y_foreign", "run05_form_uncapped_run05_z_scale",
       "L2 uncapped in place of L2c, z on run 05's scale (seen mean/SD of uncapped L2); mel_ic_mean left out (shared rule); SE unreliable (artefact rows carry the slope)")
fit_on(rows_all, "L2uc", "y_foreign", "unfolded_range_capped_in_place_of_L2c", "unfolded range, same 36-semitone cap, z over the seen rows at or under it")
dn["z_seen_coefficient"] = C.summ(M, 1)
fit_on(rows, MEAS, "y", "beta_on_y")
fit_on(rows, MEAS, "y_early", "W01_J6a_early_uptake", "foreign set dated <= first year + 5")
fit_on(rows, MEAS, "y_late", "W01_J6a_late_uptake", "foreign set dated > first year + 10")
fit_on(rows, MEAS, "ykt", "y_foreign_karaoke_tribute_removed")
fit_on([r for r in rows if not (r["fresh"] and r.get("clique_seen"))], MEAS, "y_foreign", "clique_collision_dropped",
       "fresh rows whose clique is also matched by a seen song dropped")
fit_on([r for r in rows if not r["fresh"] or r["vids"]], MEAS, "y_foreign", "fresh_with_video_id_only", "shared reported item (fresh_repetition)")
# fresh-only within-artist model: fresh rows with L2c by artists with two or more such rows; columns less z_seen and fresh
fo = [r for r in R if r["fresh"]]; cf = C.collections.Counter(r["artist"] for r in fo); fo = [r for r in fo if cf[r["artist"]] >= 2]
nm, Xf, _ = design(fo); kc = [j for j, n_ in enumerate(nm) if n_ not in ("z_seen", "fresh")]
mf = C.lpm(Xf[:, kc], np.array([r["y_foreign"] for r in fo], float), np.array([r["artist"] for r in fo]))
dn["fresh_only_within_artist"] = dict(**C.summ(mf, 0), N=mf["N"], artists=mf["G"], y_foreign1=int(sum(r["y_foreign"] > 0 for r in fo)))
dn["fresh_counts"] = dict(fresh_y1=CNT["fresh_y1"], fresh_y_foreign1=CNT["fresh_y_foreign1"],
                          fresh_clique_seen=int(sum(bool(r.get("clique_seen")) for r in R if r["fresh"])))
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k, vv in dn.items(): print(f"  {k}: {json.dumps(vv)}", flush=True)
OUT["reported_deciding_nothing"] = dn
finish(verdict)
