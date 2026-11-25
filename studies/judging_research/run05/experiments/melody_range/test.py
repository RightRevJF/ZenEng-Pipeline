"""Run 05, melody_range (idea L2, the Listener; folded form): within an artist's own songs, does a narrower melody range go with
more uptake by another artist (y_foreign)?
The rule is PREDICTION.md in this folder, frozen and pushed in commit 1f6c36d (branch judging-research) before any outcome was joined.
Prediction: beta(L2) on y_foreign = -0.7 pp per SD. Pass: beta < 0, p < .05/7 = .00714 two-sided, beta < 0 in both artist halves,
conditional logit < 0 and converged. Kill: beta > -0.2. Opposite sign (beta > 0, p < .00714): killed, reported as a new hypothesis.
Unsettled: anything else.
Order, as the rule says: 1. unit values; 2. rows and L2; 3. gate (stop if it fails, no outcome joined); 4. notes-side power;
5. common.load_outcomes; 6. counts; 7. clustered SE and power; 8. beta, halves, conditional logit, verdict; 9. reported items;
10. result.json.
Single process; BLAS threads limited to 1 (other experiments share the machine's 2 cores).
Code check: FAKE_Y=<dir> python3 test.py runs everything on a random fake outcome (no outcome file read) and writes result.json in <dir>.
Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
python3 test.py -> result.json in this folder"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "1")
import sys, json, time, re
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C
from common import r4, zs

NTEST = 7; ALPHA = 0.05 / NTEST; ZC = 2.690
PRED, KILL = -0.7, -0.2
FAKE = os.environ.get("FAKE_Y")
OUTDIR = FAKE if FAKE else HERE
OUT = dict(rule="PREDICTION.md in this folder, commit 1f6c36d (branch judging-research)", test="melody_range (L2, folded melody range)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)", fake_outcome=bool(FAKE),
           prediction_pp_per_sd=PRED, kill_line=KILL, threshold_p=ALPHA, tests_tonight=NTEST)

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    os.makedirs(OUTDIR, exist_ok=True)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True)

# ---------------------------------------------------------------- the measure (frozen)
def note_range(a, fold=True):
    p = sorted(C.melody_midi(a))
    if len(p) < 4: return np.nan
    q = [p[0][2]]
    for k in range(1, len(p)):
        i = p[k][2] - p[k - 1][2]
        if fold:
            while abs(i) > 12: i -= 12 * int(np.sign(i))
        q.append(q[-1] + i)
    q = np.array(q, float); w = np.array([x[1] - x[0] for x in p], float)
    o = np.argsort(q, kind="stable"); cw = np.cumsum(w[o]) / w.sum()
    return float(q[o][np.searchsorted(cw, 0.95)] - q[o][np.searchsorted(cw, 0.05)])
L2 = lambda a, c=None: note_range(a, True)
L2_unfolded = lambda a, c=None: note_range(a, False)

# ---------------------------------------------------------------- 1. unit values
def fake_clip(pitches):
    return {"melody": [{"onset": float(k), "offset": float(k + 1), "octave": p // 12, "pitch_class": p % 12} for k, p in enumerate(pitches)]}
UNITS = [([0, 4, 7, 12], 12), ([0, 4, 19, 12], 7), ([0, 2, 4, 5, 7, 9, 11, 12, 14, 16], 16)]
uv = []
for ps, want in UNITS:
    got = L2(fake_clip(ps)); uv.append(dict(pitches=ps, want=want, got=got, ok=got == want))
    print(f"UNIT {ps}: {got} [{want}] {'ok' if got == want else 'MISMATCH'}", flush=True)
uv.append(dict(pitches=[0, 4, 7], want="nan (fewer than 4 notes)", got=str(L2(fake_clip([0, 4, 7])))))
OUT["unit_values"] = uv
assert all(u["ok"] for u in uv[:3]), "unit values not reproduced"

# ---------------------------------------------------------------- 2. rows and L2
D = C.load_rows(); rows = D["rows"]; n = len(rows)
miss = C.song_measure(rows, L2, "L2"); C.song_measure(rows, L2_unfolded, "L2u")
v = np.array([r["L2"] for r in rows], float); vu = np.array([r["L2u"] for r in rows], float)
pct = np.nanpercentile(v, [10, 50, 90]).round(3).tolist()
rho_fu = C.sp(v, vu)
print(f"L2: songs with a value {int(np.isfinite(v).sum())} [9,588]; clips missing from the raw file {miss}; "
      f"10/50/90th percentiles {pct} [7 / 11 / 21]; folded vs unfolded Spearman {rho_fu[0]:+.3f} [+0.94]", flush=True)
OUT["measure"] = dict(songs=n, songs_with_value=int(np.isfinite(v).sum()), clips_missing_raw=miss, pct_10_50_90=pct,
                      mean=r4(np.nanmean(v)), sd=r4(np.nanstd(v)), folded_vs_unfolded_spearman=r4(rho_fu[0]),
                      unfolded_pct_10_50_90=np.nanpercentile(vu, [10, 50, 90]).round(3).tolist())

# ---------------------------------------------------------------- 3. gate (notes only)
G = C.gate(rows, "L2")
top5 = sorted(G["overlap_all"].items(), key=lambda kv: -abs(kv[1] or 0))[:5]
print(f"GATE 1, clip 1 vs clip 2: {G['clip_to_clip']} on {G['clip_pairs']} pairs [0.290 on 4,271]; needs >= 0.20", flush=True)
print(f"GATE 2, largest |Spearman|: {G['overlap_largest']} [mel_ic_mean +0.555]; needs <= 0.7; top 5 {top5}", flush=True)
print(f"GATE: {'PASSED' if G['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = G
if not G["passed"]:
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# ---------------------------------------------------------------- columns
art = np.array([r["artist"] for r in rows]); HV = np.array([r["half"] for r in rows])
CN, CX = C.controls(rows)
Z = dict(z_L2=zs(v), z_mel_ic_mean=zs([r["mel_ic_mean"] for r in rows]), z_ch_rep=zs([r["ch_rep"] for r in rows]),
         z_ch_ic_mean=zs([r["ch_ic_mean"] for r in rows]), z_L2u=zs(vu))
def design(first="z_L2", mel=True, extra=None):
    names = [first] + (["z_mel_ic_mean"] if mel else []) + ["z_ch_rep", "z_ch_ic_mean"]
    cols = [Z[k] for k in names]
    if extra:
        for k, x in extra.items(): names.append(k); cols.append(np.asarray(x, float))
    return names + CN, np.column_stack(cols + [CX])
NAMES, X = design()
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)
OUT["columns"] = NAMES

# ---------------------------------------------------------------- 4. notes-side power (no outcome)
def demean(M, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); cnt = np.bincount(gg)
    M2 = np.asarray(M, float).reshape(len(g), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / cnt[:, None])[gg]
Xd = demean(X, art); o = Xd[:, 1:]; keepc = np.abs(o).sum(0) > 1e-12; o = o[:, keepc]
xt = Xd[:, 0] - o @ np.linalg.lstsq(o, Xd[:, 0], rcond=None)[0]
se_ns = float(np.sqrt(0.22 * 0.78 / (xt @ xt)) * 100)
pw_ns = dict(residual_share=r4(xt @ xt / n), se_bound_pp=r4(se_ns), power_at_pred_p00714=r4(C.power(PRED, se_ns, ALPHA)),
             power_at_pred_p05=r4(C.power(PRED, se_ns, 0.05)))
print(f"NOTES-SIDE POWER: residual share {pw_ns['residual_share']} [0.748]; SE bound {se_ns:.3f} pp [0.49]; power at -0.7, p < .00714: "
      f"{pw_ns['power_at_pred_p00714']} [0.10]; at p < .05: {pw_ns['power_at_pred_p05']} [0.30]", flush=True)
OUT["notes_side_power"] = pw_ns

# ---------------------------------------------------------------- 5. outcome
nrm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
if FAKE:   # random outcome, no outcome file read
    rs = np.random.default_rng(5)
    for r in rows:
        r["y"] = 100.0 if rs.random() < 0.23 else 0.0; r["drop_reason"] = None; r["versions"] = None
        r["y_foreign"] = (np.nan if rs.random() < 0.04 else (100.0 if rs.random() < 0.6 else 0.0)) if r["y"] > 0 else 0.0
        r["covers"] = int(rs.integers(1, 30)) if r["y"] > 0 else None; r["lcov"] = float(np.log1p(r["covers"])) if r["covers"] else None
        r["first_year"] = int(rs.integers(1960, 2020)) if r["y"] > 0 and rs.random() < 0.9 else None
        if r["y"] > 0 and np.isfinite(r["y_foreign"]):
            sets = [[r["artist"]]] + ([["Karaoke Kings"]] if rs.random() < 0.2 else []) + ([["Other Band"]] if r["y_foreign"] > 0 and rs.random() < 0.8 else [])
            if r["y_foreign"] > 0 and len(sets) == 1: sets.append(["Other Band"])
            r["versions"] = [[s, 2000, [1]] for s in sets]
    LO = dict(md5=["fake", "fake"], drops=int(sum(1 for r in rows if not np.isfinite(r["y_foreign"]))))
else:
    LO = C.load_outcomes(rows, HERE)
OUT["outcome_files"] = LO
yf_all = np.array([r["y_foreign"] for r in rows], float); keep = np.isfinite(yf_all)
# karaoke / tribute variant (reported): own sets and O as in the primary outcome; foreign sets naming karaoke or tribute removed
KT = lambda s: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)
ykt_all = np.zeros(n)
for i_, r in enumerate(rows):
    if not keep[i_] or not r["y_foreign"] or r["y_foreign"] <= 0: continue
    sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
    own = [s for s in sets if any(nrm(nm) == a for nm in s)]; O = {nrm(nm) for s in own for nm in s}
    foreign = [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)]
    ykt_all[i_] = 100.0 if [s for s in foreign if not KT(s)] else 0.0

# ---------------------------------------------------------------- 6. counts (songs with y_foreign = NaN dropped from every model)
X, art, HV = X[keep], art[keep], HV[keep]
yf = yf_all[keep]; y = np.array([r["y"] for r in rows], float)[keep]; ykt = ykt_all[keep]; R = [r for r, k in zip(rows, keep) if k]
Gn = len(set(art))
print(f"\nOUTCOME: md5 {LO['md5']}; dropped (y_foreign NaN) {int((~keep).sum())}; N {len(yf)} songs, {Gn} artists; "
      f"y_foreign = 1: {int((yf > 0).sum())} ({(yf > 0).mean():.4f}); y = 1: {int((y > 0).sum())}", flush=True)
OUT["counts"] = dict(dropped_y_foreign_nan=int((~keep).sum()), N=len(yf), artists=Gn, y_foreign1=int((yf > 0).sum()),
                     share_y_foreign1=r4((yf > 0).mean()), y1=int((y > 0).sum()), y_foreign_karaoke_tribute_removed1=int((ykt > 0).sum()))

# ---------------------------------------------------------------- 7. clustered SE and power, before the estimate
M = C.lpm(X, yf, art)
se = float(M["se"][0])
pw = dict(clustered_se=r4(se), power_at_pred_p00714=r4(C.power(PRED, se, ALPHA)), power_at_pred_p05=r4(C.power(PRED, se, 0.05)))
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_ns:.3f}]; power at -0.7, p < .00714: {pw['power_at_pred_p00714']}; "
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

# ---------------------------------------------------------------- 8. beta, halves, conditional logit, verdict
b, p = float(M["b"][0]), float(M["p"][0])
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"],
                      others={nm: C.summ(M, j) for j, nm in enumerate(NAMES[:4]) if j > 0})
print(f"PRIMARY LPM: beta(L2) {b:+.4f} pp per SD (predicted -0.7), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print("  other measures: " + "; ".join(f"{k} {vv['beta']:+.3f} (SE {vv['se']:.3f}, p {vv['p']:.3g})" for k, vv in OUT["primary"]["others"].items()), flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = HV == h; HM[h] = C.lpm(X[s], yf[s], art[s])
    OUT["halves"].append(dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], y_foreign1=int((yf[s] > 0).sum()), **C.summ(HM[h], 0)))
    print(f"HALF {h}: {HM[h]['N']} songs, {HM[h]['G']} artists, y_foreign=1 {int((yf[s] > 0).sum())}; beta {HM[h]['b'][0]:+.4f} "
          f"(SE {HM[h]['se'][0]:.4f}, p {HM[h]['p'][0]:.3g})", flush=True)
yb = (yf > 0).astype(int)
params, bse, pv, conv, ks, kg = C.cond_logit(X, yb, list(art))
OUT["conditional_logit"] = dict(coef=r4(params[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=conv, kept_songs=ks, kept_artists=kg,
                                dropped_songs=int(len(yb) - ks), dropped_artists=int(Gn - kg), convergence_test="max|score|/nobs < 1e-5 (BFGS, then Newton)",
                                others={nm: [r4(params[j]), r4(bse[j])] for j, nm in enumerate(NAMES[:4]) if j > 0})
print(f"CONDITIONAL LOGIT: keeps {ks} songs, {kg} artists (drops {len(yb) - ks} songs, {Gn - kg} artists, all 0 or all 1); "
      f"L2 coef {params[0]:+.4f} log-odds per SD, SE {bse[0]:.4f}, p {pv[0]:.4g}; converged {conv}", flush=True)

hb = [float(HM[h]["b"][0]) for h in (0, 1)]; cb = float(params[0])
if b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0 and conv and cb < 0: verdict = "pass"
elif b > 0 and p < ALPHA: verdict = "opposite sign (beta > 0, p < .00714): killed; reported as a new hypothesis (wide-range showpieces are what others take up), not a pass"
elif b > KILL: verdict = "kill (beta > -0.2 pp)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00714")
    if not (hb[0] < 0 and hb[1] < 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb < 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
nm_, Xu = design(first="z_L2u"); Xu = Xu[keep]; m = C.lpm(Xu, yf, art); dn["unfolded_range_in_place_of_L2"] = C.summ(m, 0)
nm_, Xn = design(mel=False); Xn = Xn[keep]; m = C.lpm(Xn, yf, art); dn["without_mel_ic_mean"] = C.summ(m, 0)
m = C.lpm(X, y, art); dn["L2_on_y"] = dict(y1=int((y > 0).sum()), **C.summ(m, 0))
lc = np.array([r["lcov"] if r["lcov"] is not None else np.nan for r in R], float)
fy = np.array([r["first_year"] if r["first_year"] is not None else np.nan for r in R], float)
si = (y > 0) & np.isfinite(lc) & np.isfinite(fy)
Xi = np.column_stack([X[si][:, :4], fy[si], X[si][:, 4:]])
m = C.lpm(Xi, zs(lc[si]), art[si])
dn["intensive_margin"] = dict(songs=int(si.sum()), artists=len(set(art[si])), outcome="z(log(1+covers)) over these songs (population SD)",
                              listener_prediction_sd_per_sd=-0.02, **C.summ(m, 0))
m = C.lpm(X, ykt, art); dn["y_foreign_karaoke_tribute_removed"] = dict(count1=int((ykt > 0).sum()), **C.summ(m, 0))
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k, vv in dn.items(): print(f"  {k}: {json.dumps(vv)}", flush=True)
OUT["reported_deciding_nothing"] = dn

# ---------------------------------------------------------------- diagnostic, ADDED AFTER the first run's result, deciding nothing:
# why beta on y (about 0) differs from beta on y_foreign, when the two outcomes differ on only the y_self songs.
diag = {}
m = C.lpm(X, y - yf, art); diag["L2_on_y_self"] = dict(y_self1=int(((y - yf) > 0).sum()), **C.summ(m, 0))
codes = {a: i for i, a in enumerate(sorted(set(art)))}; gg = np.array([codes[a] for a in art]); cnt = np.bincount(gg); inv = {i: a for a, i in codes.items()}
Xw = demean(X, art); Xw = Xw[:, np.abs(Xw).sum(0) > 1e-12]; XtXi = np.linalg.pinv(Xw.T @ Xw)
for nm, yy in (("y_foreign", yf), ("y", y)):
    yw = demean(yy, art).ravel(); u = yw - Xw @ (XtXi @ Xw.T @ yw)
    sc = np.zeros((len(codes), Xw.shape[1])); np.add.at(sc, gg, Xw * u[:, None]); infl = (sc @ XtXi[:, 0]) ** 2
    top = np.argsort(-infl)[:3]
    diag[f"clustered_variance_share_top3_artists_{nm}"] = [[inv[i], int(cnt[i]), r4(infl[i] / infl.sum())] for i in top]
print("\nDIAGNOSTIC (added after the result, deciding nothing):", flush=True)
for k, vv in diag.items(): print(f"  {k}: {json.dumps(vv)}", flush=True)
OUT["diagnostic_added_after_result"] = diag
finish(verdict)
