"""Run 06, fresh_diatonic: R04-G1 diatonicity D5 = |a5| / a0 on fresh songs, holding the fifths path FP and the non-triad share NT.

Rule: PREDICTION.md in this folder (with ../fresh_repetition/PREDICTION.md for the shared fresh rules and ../common.py), frozen and
committed in 08b5167 (branch judging-research) before any outcome was joined.
  Prediction: beta(z_fresh) on y_foreign = +0.5 pp per SD of D5, holding z(FP), z(NT), z(ch_rep) and the shared controls.
  Pass: beta > 0, two-sided p < .05/6, beta > 0 in both artist halves, conditional logit > 0 and converged.
  Kill: beta <= 0. Opposite sign (beta < 0, p < .00833): killed; reported as a new hypothesis. Unsettled: anything else.

Order (PREDICTION.md): 1. unit values; 2. seen reproduction (D5 for 9,588; FP percentiles); 3. gate (stop if it fails);
4. notes-side power (bound 1.54 pp); 5. common.validate_match; 6. common.load_battery_outcomes; 7. counts; 8. clustered SE, power;
9. beta, halves, logit, verdict; 10. reported; 11. result.json.
Code check on a fake random outcome (no outcome file is read): FAKE_Y=/some/dir python3 test.py (writes result.json there).
HOOKTHEORY_RAW=/home/claude/dl/hooktheory/Hooktheory.json.gz python3 .../fresh_diatonic/test.py -> result.json in this folder.

Data credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
             Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, re, collections
import numpy as np
from scipy.stats import spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C
import power_fake as PF          # only its notes_bound(); nothing else runs on import

ALPHA = C.ALPHA; PRED = 0.5
FAKE = os.environ.get("FAKE_Y"); OUTDIR = FAKE if FAKE else HERE
r4 = C.r4
OUT = dict(rule="PREDICTION.md in this folder, commit 08b5167 (shared rules ../fresh_repetition/PREDICTION.md, ../common.py)",
           test="fresh_diatonic (R04-G1 diatonicity D5 on fresh songs, holding FP and NT)", alpha=round(ALPHA, 5), z_crit=2.638,
           prediction_pp_per_sd=PRED, kill_line="beta <= 0", fake_outcome=bool(FAKE),
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)")
def T(): return f"[{time.time() - T0:.0f}s]"
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- 1. unit values (one beat per chord, tonic C)
def fake_clip(chords):
    return dict(keys=[dict(tonic_pitch_class=0, beat=0)],
                harmony=[dict(root_pitch_class=r, root_position_intervals=iv, onset=i, offset=i + 1) for i, (r, iv) in enumerate(chords)])
MAJ, MIN, DOM7 = [4, 3], [3, 4], [4, 3, 3]
UNIT = [("C triad alone", C.D5_clip, [(0, MAJ)], 0.6440), ("C, F, G triads", C.D5_clip, [(0, MAJ), (5, MAJ), (7, MAJ)], 0.5864),
        ("C and Ab triads", C.D5_clip, [(0, MAJ), (8, MAJ)], 0.3220), ("NT of I, V7, vi, IV", C.NT_clip, [(0, MAJ), (7, DOM7), (9, MIN), (5, MAJ)], 0.2500)]
unit = {}
for nm, fn, ch, want in UNIT:
    got = fn(fake_clip(ch)); unit[nm] = dict(want=want, got=r4(got))
    print(f"unit {nm}: {got:.4f} (want {want:.4f})", flush=True); assert abs(got - want) < 5e-5, (nm, got, want)
OUT["unit_values"] = unit

# ---------------------------------------------------------------- 2. rows and seen reproduction (notes only)
B = C.battery(); rows_all = B["rows"]
seen9_vids = {r["vid"] for r in B["seen_rows"]}; seen9 = [r for r in B["seen_all"] if r["vid"] in seen9_vids]
C.add_measures(B["seen_all"] + B["fresh_rows"], which=("V", "ln_chg", "D5", "NT", "FP"))
nf_b = sum(r["fresh"] for r in rows_all)
counts_shared = dict(fresh_rows_built=len(B["fresh_rows"]), battery_rows=len(rows_all), battery_seen=len(rows_all) - nf_b, battery_fresh=nf_b,
                     battery_artists=len(set(r["artist"] for r in rows_all)), fresh_drops=B["fresh_drops"])
print(f"{T()} shared counts: {counts_shared} [1,825 / 5,768 / 4,473 / 1,295 / 601]", flush=True)
assert (len(B["fresh_rows"]), len(rows_all), nf_b, counts_shared["battery_artists"]) == (1825, 5768, 1295, 601), counts_shared

d5s = np.array([r["D5"] for r in seen9]); fps = np.array([r["FP"] for r in seen9]); nts = np.array([r["NT"] for r in seen9])
muD, sdD = C.seen_sd(seen9, "D5"); muF, sdF = C.seen_sd(seen9, "FP"); muN, sdN = C.seen_sd(seen9, "NT"); muR, sdR = C.seen_sd(seen9, "ch_rep")
pct = np.nanpercentile(fps, (10, 50, 90)); rho_df = C.sp(d5s, fps); rho_dn = C.sp(d5s, nts)
GN = C.gate(seen9, "NT")
seen_rep = dict(seen_rows=len(seen9), D5_finite=int(np.isfinite(d5s).sum()), D5_mean=r4(muD), D5_sd=r4(sdD),
                FP_finite=int(np.isfinite(fps).sum()), FP_p10_p50_p90=[r4(x) for x in pct], FP_mean=r4(muF), FP_sd=r4(sdF),
                NT_finite=int(np.isfinite(nts).sum()), NT_mean=r4(muN), NT_sd=r4(sdN), ch_rep_mean=r4(muR), ch_rep_sd=r4(sdR),
                rho_D5_FP=r4(rho_df[0]), rho_D5_NT=r4(rho_dn[0]), NT_largest_pack_overlap=GN["overlap_largest"])
print(f"{T()} SEEN: {json.dumps(seen_rep)}", flush=True)
print("  [chair: D5 9,588, mean 0.5253, SD 0.0948; FP 0.449 / 0.714 / 1.197, mean 0.7822, SD 0.3329; NT mean 0.281, SD 0.3074; "
      "rho(D5, FP) -0.731; rho(D5, NT) -0.215; NT largest overlap ch_ic_mean +0.69]", flush=True)
chk = [(seen_rep["D5_finite"], 9588, 0), (muD, 0.5253, 5e-5), (sdD, 0.0948, 5e-5), (pct[0], 0.449, 5e-4), (pct[1], 0.714, 5e-4), (pct[2], 1.197, 5e-4),
       (muF, 0.7822, 5e-5), (sdF, 0.3329, 5e-5), (muN, 0.281, 5e-4), (sdN, 0.3074, 5e-5), (rho_df[0], -0.731, 5e-4), (rho_dn[0], -0.215, 5e-4),
       (GN["overlap_largest"][1], 0.69, 5e-3)]
bad = [c for c in chk if abs(c[0] - c[1]) > c[2]]
assert not bad and GN["overlap_largest"][0] == "ch_ic_mean", ("seen reproduction failed", bad, GN["overlap_largest"])
OUT["seen_reproduction"] = seen_rep; OUT["shared_counts"] = counts_shared

Rb = [r for r in rows_all if all(np.isfinite(r[k]) for k in ("D5", "FP", "NT"))]
fR = [r for r in Rb if r["fresh"]]
cnt = dict(rows=len(Rb), seen=len(Rb) - len(fR), fresh=len(fR), artists=len(set(r["artist"] for r in Rb)), fresh_artists=len(set(r["artist"] for r in fR)),
           fresh_rows_without_FP=sum(1 for r in rows_all if r["fresh"] and not np.isfinite(r["FP"])),
           battery_rows_dropped=len(rows_all) - len(Rb))
fp12 = [r["D5_c12"] for r in rows_all if r["fresh"] and r.get("D5_c12")]
fp12b = [r["D5_c12"] for r in fR if r.get("D5_c12")]
fp12a = [r["D5_c12"] for r in B["fresh_rows"] if r.get("D5_c12")]
cnt["fresh_clip12_raw_D5"] = dict(all_fresh_rows=[r4(spearmanr([p[0] for p in fp12a], [p[1] for p in fp12a])[0]), len(fp12a)], battery_fresh=[r4(spearmanr([p[0] for p in fp12], [p[1] for p in fp12])[0]), len(fp12)],
                                  model_fresh=[r4(spearmanr([p[0] for p in fp12b], [p[1] for p in fp12b])[0]), len(fp12b)])
print(f"{T()} ROWS: {json.dumps(cnt)} [chair 5,707 = 4,472 seen + 1,235 fresh, fresh by 585 artists; 60 fresh without FP; fresh clip 1 vs 2: 0.395 on 432]", flush=True)
assert (cnt["rows"], cnt["seen"], cnt["fresh"], cnt["fresh_artists"]) == (5707, 4472, 1235, 585), cnt
OUT["rows"] = cnt

# ---------------------------------------------------------------- 3. GATE (seen rows, notes only)
R = C.raw_clips(); P1, P2 = [], []
for r in seen9:
    if len(r["clips"]) < 2: continue
    v = []
    for c in r["clips"][:2]:
        a = R[c["k"]]; v.append((C.D5_clip(a), C.FP_song([a]), C.NT_clip(a)))
    if np.isfinite(v[0]).all() and np.isfinite(v[1]).all(): P1.append(v[0]); P2.append(v[1])
P1, P2 = np.array(P1), np.array(P2); npairs = len(P1)
S = np.vstack([P1, P2]); Xg = np.column_stack([np.ones(len(S)), S[:, 1], S[:, 2]])
bg = np.linalg.lstsq(Xg, S[:, 0], rcond=None)[0]; e = S[:, 0] - Xg @ bg
r2 = 1 - (e @ e) / ((S[:, 0] - S[:, 0].mean()) @ (S[:, 0] - S[:, 0].mean()))
st_res = float(spearmanr(e[:npairs], e[npairs:])[0]); st_raw = float(spearmanr(P1[:, 0], P2[:, 0])[0])
GD = C.gate(seen9, "D5")
ov = GD["overlap_largest"]; g1 = st_res >= 0.20; g2 = abs(ov[1]) <= 0.70
print(f"{T()} GATE 1, residual clip 1 vs clip 2 (D5 on const, FP, NT; stacked): Spearman {st_res:.4f} on {npairs} pairs (needs >= 0.20) "
      f"[chair 0.342 on 4,268]; raw {st_raw:.4f} [0.503]; R2 {r2:.3f} [0.55]", flush=True)
print(f"GATE 2, overlap: largest {ov} (needs |rho| <= 0.7) [chair ch_ic_mean -0.423]; all {json.dumps(GD['overlap_all'])}", flush=True)
gate = dict(residual_clip_to_clip=r4(st_res), pairs=npairs, raw_clip_to_clip=r4(st_raw), r2_FP_NT=r4(r2), ols_coefs_const_FP_NT=[r4(x) for x in bg],
            overlap_largest=ov, overlap_all=GD["overlap_all"], stab_threshold=0.20, overlap_threshold=0.70, passed=bool(g1 and g2))
print(f"GATE: {'PASSED' if gate['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = gate
if not gate["passed"]:
    OUT["outcome_joined"] = False; finish("stopped (gate failed before any outcome was read)")
assert npairs == 4268 and abs(st_res - 0.342) < 5e-4, ("gate figures do not reproduce", npairs, st_res)

# ---------------------------------------------------------------- design
z = lambda Rr, nm, mu, sd: (np.array([r[nm] for r in Rr], float) - mu) / sd
extra = {"z_ch_rep": z(Rb, "ch_rep", muR, sdR), "z_FP": z(Rb, "FP", muF, sdF), "z_NT": z(Rb, "NT", muN, sdN)}
NAMES, X, (mu, sd) = C.fresh_design(Rb, "D5", seen9, extra)
assert NAMES[:5] == ["z_fresh", "z_seen", "z_ch_rep", "z_FP", "z_NT"] and abs(mu - muD) < 1e-12
art = np.array([r["artist"] for r in Rb]); half = np.array([r["half"] for r in Rb]); isf = np.array([r["fresh"] for r in Rb], bool)
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)
OUT["columns"] = NAMES; OUT["z_scale"] = dict(D5=[r4(muD), r4(sdD)], FP=[r4(muF), r4(sdF)], NT=[r4(muN), r4(sdN)], ch_rep=[r4(muR), r4(sdR)])

# ---------------------------------------------------------------- 4. notes-side power
seb = PF.notes_bound(X, list(art))
print(f"{T()} NOTES-SIDE POWER: SE bound {seb:.3f} pp [1.54]; power at +0.5, p < .00833: {C.power(PRED, seb, ALPHA):.3f}; at .05: {C.power(PRED, seb, 0.05):.3f}", flush=True)
PFJ = json.load(open(os.path.join(os.path.dirname(HERE), "power_fake.json")))["fresh_diatonic"]
OUT["notes_side_power"] = dict(se_bound_pp=r4(seb), power_p00833=r4(C.power(PRED, seb, ALPHA)), power_p05=r4(C.power(PRED, seb, 0.05)),
                               fake_outcome_power_file=dict(calibrated=PFJ["calibrated"], homogeneous=PFJ["homogeneous"]))

# ---------------------------------------------------------------- 5-6. validation and outcome
if FAKE:
    rs = np.random.default_rng(11)
    for r in rows_all:
        yy = rs.random() < 0.22
        r.update(y=100.0 if yy else 0.0, y_foreign=(np.nan if rs.random() < 0.03 else (100.0 if rs.random() < 0.8 else 0.0)) if yy else 0.0,
                 versions=[[["Fake Artist"], 2001, [1]], [["Karaoke Kings"], 2003, [1]], [[r["artist"]], 1999, [1]]] if yy else None,
                 first_year=1999 if yy else None, clique_seen=bool(yy and rs.random() < 0.1))
    VAL = dict(passed="fake"); LB = dict(fake=True)
else:
    VAL = C.validate_match(HERE)
    print(f"{T()} MATCH VALIDATION (cached file): " + json.dumps({k: VAL[k] for k in VAL if not isinstance(VAL[k], list)}), flush=True)
    if not VAL["passed"]:
        OUT["validation"] = VAL; OUT["outcome_joined"] = False; finish("stopped (validation failed)")
    LB = C.load_battery_outcomes(rows_all, HERE)
OUT["validation"] = {k: VAL[k] for k in VAL if not isinstance(VAL[k], list)}
OUT["load_battery_outcomes"] = {k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items()}) for k, v in LB.items()}
print(f"{T()} OUTCOME LOADER: {json.dumps(LB, default=str)}", flush=True)

yf = np.array([r["y_foreign"] for r in Rb], float); yv = np.array([r["y"] for r in Rb], float); keep = np.isfinite(yf)

# ---------------------------------------------------------------- 7. counts
oc = dict(N=int(keep.sum()), artists=len(set(art[keep])), y_foreign_dropped_nan=int((~keep).sum()),
          dropped_fresh=int((~keep & isf).sum()), dropped_seen=int((~keep & ~isf).sum()),
          fresh_N=int((keep & isf).sum()), seen_N=int((keep & ~isf).sum()),
          fresh_y1=int((yv[isf] > 0).sum()), seen_y1=int((yv[~isf] > 0).sum()),
          fresh_y_foreign1=int((yf[keep & isf] > 0).sum()), seen_y_foreign1=int((yf[keep & ~isf] > 0).sum()),
          fresh_share_y_foreign1=r4((yf[keep & isf] > 0).mean()), seen_share_y_foreign1=r4((yf[keep & ~isf] > 0).mean()))
print(f"{T()} COUNTS: {json.dumps(oc)}", flush=True)
OUT["counts"] = oc
Xk, yk, ak, hk = X[keep], yf[keep], art[keep], half[keep]

# ---------------------------------------------------------------- 8. clustered SE and power (before beta)
M = C.lpm(Xk, yk, ak); se = float(M["se"][0])
pw, pw05 = C.power(PRED, se, ALPHA), C.power(PRED, se, 0.05)
print(f"POWER: clustered SE {se:.4f} pp [fake-outcome median 1.12 calibrated / 1.50 homogeneous; bound {seb:.3f}]; power at +0.5, p < .00833: {pw:.3f}; at .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_p00833=r4(pw), power_p05=r4(pw05))

# ---------------------------------------------------------------- 9. beta, halves, logit, verdict
b, p = float(M["b"][0]), float(M["p"][0])
print(f"PRIMARY LPM: beta(z_fresh) {b:+.4f} pp per SD (predicted +0.5), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
OUT["primary"] = dict(z_fresh=C.summ(M, 0), **{NAMES[j]: C.summ(M, j) for j in range(1, 5)}, fresh_main=C.summ(M, NAMES.index("fresh")),
                      N=M["N"], artists=M["G"], K=M["K"])
for j in range(1, 5): print(f"  {NAMES[j]} {M['b'][j]:+.4f} (SE {M['se'][j]:.4f}, p {M['p'][j]:.3g})", flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = hk == h; HM[h] = C.lpm(Xk[s], yk[s], ak[s])
    OUT["halves"].append(dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], fresh_songs=int((s & isf[keep]).sum()),
                              fresh_y_foreign1=int((yk[s & isf[keep]] > 0).sum()), z_fresh=C.summ(HM[h], 0)))
    print(f"HALF {h}: {HM[h]['N']} songs ({int((s & isf[keep]).sum())} fresh), {HM[h]['G']} artists; beta {HM[h]['b'][0]:+.4f} "
          f"(SE {HM[h]['se'][0]:.4f}, p {HM[h]['p'][0]:.3g})", flush=True)
hb = [float(HM[h]["b"][0]) for h in (0, 1)]

ybk = (yk > 0).astype(float)
try:
    prm, bse, pv, conv, ks, kgn = C.cond_logit(Xk, ybk, list(ak))
    cl = dict(coef=r4(prm[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=bool(conv), kept_songs=ks, kept_artists=kgn,
              dropped_songs=int(len(ak) - ks), dropped_artists=int(len(set(ak)) - kgn), convergence_test="max|score|/nobs < 1e-5 (BFGS, then Newton)",
              z_seen=r4(prm[1]), z_ch_rep=r4(prm[2]), z_FP=r4(prm[3]), z_NT=r4(prm[4]),
              large_nuisance_coefs={NAMES[j]: r4(prm[j]) for j in range(len(NAMES)) if abs(prm[j]) > 5})
except Exception as ex:
    prm = None; conv = False; cl = dict(error=repr(ex), converged=False)
print(f"CONDITIONAL LOGIT: {json.dumps(cl)}", flush=True)
OUT["conditional_logit"] = cl
cb = float(prm[0]) if prm is not None else np.nan

if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and cb > 0: verdict = "pass"
elif b < 0 and p < ALPHA: verdict = "opposite sign (beta < 0, p < .00833): killed; R04-G1 closed; reported as a new hypothesis, not a pass"
elif b <= 0: verdict = "kill (beta <= 0); R04-G1 closed"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00833")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb > 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the rule): {verdict}", flush=True)

# ---------------------------------------------------------------- 10. reported, deciding nothing
dn = {}
def drop_cols(Xm, names, out):
    ix = [j for j, n in enumerate(names) if n not in out]; return Xm[:, ix], [names[j] for j in ix]
# D5 without FP and NT (run 05's printed form; ch_ic_mean is left out by the shared rule), same rows
Xa, na = drop_cols(X, NAMES, ("z_FP", "z_NT")); assert na[0] == "z_fresh"
dn["D5_without_FP_and_NT"] = dict(songs=int(keep.sum()), **C.summ(C.lpm(Xa[keep], yf[keep], art[keep]), 0))
dn["z_seen"] = dict(**C.summ(M, 1), note="seen-song reading, already spent")
oky = np.isfinite(yv)
dn["beta_on_y"] = dict(songs=int(oky.sum()), **C.summ(C.lpm(X[oky], yv[oky], art[oky]), 0))
el = np.array([C.early_late(r) for r in Rb], float)
for j, nm in enumerate(("y_early", "y_late")):
    ok = np.isfinite(el[:, j])
    dn[nm] = dict(songs=int(ok.sum()), count1=int((el[ok, j] > 0).sum()), fresh_count1=int((el[ok & isf, j] > 0).sum()), **C.summ(C.lpm(X[ok], el[ok, j], art[ok]), 0))
KT = lambda s: any(("karaoke" in (nm or "").lower()) or ("tribute" in (nm or "").lower()) for nm in s)
ykt = np.full(len(Rb), np.nan)
for i, r in enumerate(Rb):
    if not np.isfinite(r["y_foreign"]): continue
    if r["y"] <= 0 or not r.get("versions"): ykt[i] = 0.0 if r["y"] <= 0 else np.nan; continue
    sets = [e_[0] for e_ in r["versions"]]; a = C.nrm(r["artist"])
    own = [s_ for s_ in sets if any(C.nrm(nm) == a for nm in s_)]; O = {C.nrm(nm) for s_ in own for nm in s_}
    foreign = [s_ for s_ in sets if len(s_) > 0 and not any(C.nrm(nm) in O for nm in s_)]
    ykt[i] = 100.0 if [s_ for s_ in foreign if not KT(s_)] else 0.0
okk = np.isfinite(ykt)
dn["y_foreign_without_karaoke_tribute"] = dict(songs=int(okk.sum()), count1=int((ykt[okk] > 0).sum()), changed_vs_primary=int((ykt[okk] != yf[okk]).sum()),
                                               fresh_changed=int((ykt[okk & isf] != yf[okk & isf]).sum()), **C.summ(C.lpm(X[okk], ykt[okk], art[okk]), 0))
cs = np.array([bool(r.get("clique_seen")) for r in Rb]); okc = keep & ~(isf & cs)
dn["clique_collision_dropped"] = dict(fresh_rows_dropped=int((keep & isf & cs).sum()), songs=int(okc.sum()), **C.summ(C.lpm(X[okc], yf[okc], art[okc]), 0))
hv = np.array([bool(r.get("vids")) for r in Rb]); okv = keep & ~(isf & ~hv)
dn["fresh_with_video_id_only"] = dict(fresh_rows_dropped=int((keep & isf & ~hv).sum()), songs=int(okv.sum()), **C.summ(C.lpm(X[okv], yf[okv], art[okv]), 0))
Xh, nh = drop_cols(X, NAMES, ("has_mel",))
dn["without_has_mel"] = C.summ(C.lpm(Xh[keep], yf[keep], art[keep]), 0)
nfa = collections.Counter(r["artist"] for r in fR); fo = keep & isf & np.array([nfa[r["artist"]] >= 2 for r in Rb])
Xf, nfo = drop_cols(X, NAMES, ("z_seen", "fresh")); assert nfo[0] == "z_fresh"
mf = C.lpm(Xf[fo], yf[fo], art[fo])
dn["fresh_only_within_artist"] = dict(songs=mf["N"], artists=mf["G"], artists_with_2plus_fresh_rows_in_model_rows=sum(1 for v in nfa.values() if v >= 2),
                                      y_foreign1=int((yf[fo] > 0).sum()), **C.summ(mf, 0))
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k, v in dn.items(): print(f"  {k}: {json.dumps(v)}", flush=True)
OUT["reported_deciding_nothing"] = dn
OUT["outcome_joined"] = not FAKE
finish(verdict)
