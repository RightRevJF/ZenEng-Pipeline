"""Run 06, fresh_repetition: on Hooktheory songs whose outcome nobody has looked at (the 'fresh' songs, not in the data pack), within
an artist's own songs, do songs whose chords repeat more (ch_rep) more often have a performer set that shares no name with the
original artist (y_foreign)?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 08b5167 before any outcome was joined). It also freezes the
rules shared by the five fresh tests; the code is ../common.py (frozen).
Model: LPM with artist fixed effects (demeaned, CR1 by artist) on seen + fresh rows together; tested column z_fresh = z(ch_rep) x fresh,
beside z_seen = z(ch_rep) x (1 - fresh); z over the 9,588 within-artist seen rows; controls common.battery_controls.
PASS: beta > 0, two-sided p < .05/6 = .00833, beta > 0 in both artist halves, conditional logit coef > 0 and converged.
KILL: beta <= 0.  OPPOSITE SIGN (beta < 0, p < .00833): killed, reported as a new hypothesis.  Else UNSETTLED.
Order: 1 reproduction; 2 columns; 3 notes-side power; 4 validate_match; 5 load_battery_outcomes; 6 counts; 7 clustered SE and power;
8 beta, halves, conditional logit, verdict; 9 reported items; 10 result.json.

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
Env: NOTES_ONLY=1 stops before the outcome (code check).  python3 test.py -> result.json in this folder.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, collections
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C
import power_fake as PF          # notes_bound only (its __main__ does not run on import)
C5 = C.C5; r4 = C.r4

ALPHA = C.ALPHA; PRED = 1.0
OUT = dict(rule="PREDICTION.md in this folder, commit 08b5167", test="fresh_repetition (ch_rep on fresh songs, battery primary)",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           prediction_pp_per_sd=PRED, kill="beta <= 0", threshold_p=round(ALPHA, 6))

def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)

# ---------------------------------------------------------------- 1. reproduction checks (notes only)
# memory only (the machine is shared): the fresh list is built once and reused, not reloaded from the 20 MB raw file a second time
_FS = []
_fresh_songs_orig = C.fresh_songs
def _fresh_songs_once(verbose=True):
    if not _FS: _FS.append(_fresh_songs_orig(verbose))
    return _FS[0]
C.fresh_songs = _fresh_songs_once
import gc
B = C.battery(); gc.collect(); rows = B["rows"]; seen_all = B["seen_all"]; fr_all = B["fresh_rows"]
R = C.raw_clips()
pack_clips = [c for r in seen_all for c in r["clips"]]
d_rep = 0.0; bad = collections.Counter()
for c in pack_clips:
    a = R[c["k"]]; mel, ch = C.pack_tokens(a)
    d_rep = max(d_rep, abs(C.repetition(ch, 3) - c["ch_rep"]))
    bad["n_ch"] += len(ch) != c["n_ch"]; bad["n_mel"] += len(mel) != c["n_mel"]; bad["beats"] += a.get("num_beats") != c["beats"]
print(f"REPRODUCTION on {len(pack_clips)} pack clips [21,998]: ch_rep max |diff| {d_rep:.3g} [0]; mismatches {dict(bad)} [all 0]", flush=True)
fs = C.fresh_songs(verbose=False)
nf_songs, nf_clips = len(fs), sum(len(f["clip_ids"]) for f in fs); nf_vid = sum(1 for f in fs if f["vids"])
fresh_b = [r for r in rows if r["fresh"]]; seen_b = [r for r in rows if not r["fresh"]]
arts_seen = {r["artist"] for r in seen_b}; nfa = collections.Counter(r["artist"] for r in fresh_b)
cnt_notes = dict(pack_clips=len(pack_clips), ch_rep_max_abs_diff=d_rep, mismatches=dict(bad),
                 fresh_songs=nf_songs, fresh_clips=nf_clips, fresh_songs_with_vid=nf_vid, fresh_rows=len(fr_all), fresh_drops=B["fresh_drops"],
                 fresh_rows_mixing_melody_and_no_melody_clips=sum(1 for r in fr_all if any(c["n_mel"] > 0 for c in r["clips"]) and any(c["n_mel"] == 0 for c in r["clips"])),
                 battery_rows=len(rows), battery_seen=len(seen_b), battery_fresh=len(fresh_b), battery_artists=len({r["artist"] for r in rows}),
                 battery_fresh_with_vid=sum(1 for r in fresh_b if r["vids"]), battery_fresh_without_vid=sum(1 for r in fresh_b if not r["vids"]),
                 fresh_rows_by_artists_with_seen=sum(1 for r in fresh_b if r["artist"] in arts_seen),
                 artists_with_fresh_and_seen=len({r["artist"] for r in fresh_b if r["artist"] in arts_seen}),
                 fresh_rows_by_artists_2p_fresh=sum(1 for r in fresh_b if nfa[r["artist"]] >= 2), artists_2p_fresh=sum(1 for a in nfa if nfa[a] >= 2))
want = dict(fresh_songs=1946, fresh_clips=2570, fresh_songs_with_vid=1765, fresh_rows=1825, battery_rows=5768, battery_seen=4473, battery_fresh=1295,
            battery_artists=601, battery_fresh_with_vid=1210, battery_fresh_without_vid=85, fresh_rows_by_artists_with_seen=1160,
            artists_with_fresh_and_seen=550, fresh_rows_by_artists_2p_fresh=932, artists_2p_fresh=238, fresh_rows_mixing_melody_and_no_melody_clips=32)
ok_counts = {k: cnt_notes[k] == v for k, v in want.items()}
ok_counts["drops"] = B["fresh_drops"] == {"no clip with harmony": 120, "same normalised artist and title as a seen song": 1}
for k, v in want.items(): print(f"  {k}: {cnt_notes[k]} [{v}] {'ok' if ok_counts[k] else 'MISMATCH'}", flush=True)
print(f"  fresh drops {B['fresh_drops']} [120 no harmony, 1 duplicate] {'ok' if ok_counts['drops'] else 'MISMATCH'}", flush=True)
seen9_vids = {r["vid"] for r in B["seen_rows"]}; seen9 = [r for r in seen_all if r["vid"] in seen9_vids]
mu, sd = C.seen_sd(seen9, "ch_rep")
fm_b = float(np.mean([r["ch_rep"] for r in fresh_b])); fm_all = float(np.mean([r["ch_rep"] for r in fr_all]))
print(f"  ch_rep over the {len(seen9)} seen within-artist rows [9,588]: mean {mu:.4f} [0.2933], SD {sd:.4f} [0.2295]; "
      f"fresh mean {fm_b:.4f} (battery's {len(fresh_b)}), {fm_all:.4f} (all {len(fr_all)}) [0.247]", flush=True)
ok_counts["seen9"] = len(seen9) == 9588; ok_counts["mean_sd"] = round(mu, 4) == 0.2933 and round(sd, 4) == 0.2295
ok_counts["fresh_mean"] = round(fm_b, 3) == 0.247 or round(fm_all, 3) == 0.247
ok_counts["pack_exact"] = d_rep == 0 and sum(bad.values()) == 0
cnt_notes.update(seen9=len(seen9), ch_rep_seen_mean=r4(mu), ch_rep_seen_sd=r4(sd), ch_rep_fresh_mean_battery=r4(fm_b), ch_rep_fresh_mean_all=r4(fm_all))
OUT["reproduction"] = dict(values=cnt_notes, checks=ok_counts, all_reproduced=all(ok_counts.values()))
if not all(ok_counts.values()):
    print("REPRODUCTION FAILED:", {k: v for k, v in ok_counts.items() if not v}, flush=True); finish("stopped (reproduction failed; no outcome joined)"); sys.exit(0)

# ---- the gate as the rule states it: ch_rep is the pack's own measure, no gate; stability and overlaps are reported (deciding nothing)
def c12(rs):
    pr = [(r["clips"][0]["ch_rep"], r["clips"][1]["ch_rep"]) for r in rs if len(r["clips"]) >= 2]
    return C.sp([p[0] for p in pr], [p[1] for p in pr])
st_f_all, st_f_b, st_s = c12(fr_all), c12(fresh_b), c12(seen9)
C.add_measures(rows, which=("V", "ln_chg"))
x9 = [r["ch_rep"] for r in seen9]
ov = {f: r4(C.sp(x9, [r[f] for r in seen9])[0]) for f in C.FE if f != "ch_rep"}
ov.update(n_ch=r4(C.sp(x9, [r["n_ch"] for r in seen9])[0]), beats=r4(C.sp(x9, [r["beats"] for r in seen9])[0]),
          clips_per_song=r4(C.sp(x9, [r["nclips"] for r in seen9])[0]))
xb = [r["ch_rep"] for r in rows]
ov_b = dict(V=r4(C.sp(xb, [r["V"] for r in rows])[0]), ln_chg=r4(C.sp(xb, [r["ln_chg"] for r in rows])[0]), has_mel=r4(C.sp(xb, [r["has_mel"] for r in rows])[0]),
            fresh=r4(C.sp(xb, [r["fresh"] for r in rows])[0]))
top = max(ov, key=lambda k: abs(ov[k]) if ov[k] is not None else -1)
print(f"GATE (none applies: ch_rep is the pack's own measure; reported): clip 1 vs 2, fresh {st_f_all[0]:.3f} on {st_f_all[1]} pairs (all fresh rows), "
      f"{st_f_b[0]:.3f} on {st_f_b[1]} (battery fresh) [0.395 on 432]; seen {st_s[0]:.3f} on {st_s[1]}; largest overlap with another pack measure "
      f"{top} {ov[top]:+.3f}; on the battery rows: {ov_b}", flush=True)
OUT["gate_reported"] = dict(note="PREDICTION.md: ch_rep is the pack's own measure and needs no gate; stability reported",
                            fresh_clip12_all=[r4(st_f_all[0]), st_f_all[1]], fresh_clip12_battery=[r4(st_f_b[0]), st_f_b[1]],
                            seen_clip12=[r4(st_s[0]), st_s[1]], overlap_seen9=ov, overlap_largest=[top, ov[top]], overlap_battery_rows=ov_b)

# ---------------------------------------------------------------- 2. columns
NAMES, X, (mu_, sd_) = C.fresh_design(rows, "ch_rep", seen9)
art = np.array([r["artist"] for r in rows]); HV = np.array([r["half"] for r in rows]); FR = np.array([r["fresh"] for r in rows], float)
print(f"columns ({len(NAMES)}): {NAMES}; z scale mean {mu_:.4f}, SD {sd_:.4f}", flush=True)
assert NAMES[0] == "z_fresh" and np.isfinite(X).all()

# ---------------------------------------------------------------- 3. notes-side power
se_b = PF.notes_bound(X, list(art))
pw_n, pw_n05 = C.power(PRED, se_b, ALPHA), C.power(PRED, se_b, 0.05)
print(f"NOTES-SIDE POWER: SE bound {se_b:.3f} pp [1.66]; power at +1.0, p < .00833: {pw_n:.3f}; at p < .05: {pw_n05:.3f}. "
      f"Fake-outcome power (power_fake.json): calibrated SE 1.21, pass rate 0.034, power .035 / .13", flush=True)
OUT["notes_side_power"] = dict(se_bound_pp=r4(se_b), power_p00833=r4(pw_n), power_p05=r4(pw_n05),
                               fake_outcome=json.load(open(os.path.join(C.HERE, "power_fake.json")))["fresh_repetition"])
if os.environ.get("NOTES_ONLY"): print("NOTES_ONLY: stopping before the outcome", flush=True); sys.exit(0)

# ---------------------------------------------------------------- 4. validation, 5. outcomes
V = C.validate_match(HERE)
print("MATCH VALIDATION (cached):", json.dumps({k: V[k] for k in V if not isinstance(V[k], list)}), flush=True)
OUT["validation"] = {k: V[k] for k in V if not isinstance(V[k], list)}
if not V["passed"]: finish("stopped (validation failed)"); sys.exit(0)
LO = C.load_battery_outcomes(rows, HERE)
print(f"\nOUTCOME joined: {json.dumps(LO)}", flush=True)
OUT["outcome_join"] = LO
yf = np.array([r["y_foreign"] for r in rows], float); yy = np.array([r["y"] for r in rows], float)
S = np.isfinite(yf)

# ---------------------------------------------------------------- 6. counts
cnt = dict(N=int(S.sum()), artists=len(set(art[S])), fresh_N=int((S & (FR == 1)).sum()), seen_N=int((S & (FR == 0)).sum()),
           y_foreign_100_fresh=int((yf[S & (FR == 1)] > 0).sum()), y_foreign_100_seen=int((yf[S & (FR == 0)] > 0).sum()),
           y_100_fresh=int((yy[FR == 1] > 0).sum()), y_100_seen=int((yy[FR == 0] > 0).sum()),
           dropped_nan_fresh=int((~S & (FR == 1)).sum()), dropped_nan_seen=int((~S & (FR == 0)).sum()),
           drop_reasons=dict(collections.Counter(r.get("drop_reason") for r, s in zip(rows, S) if not s)))
cnt["share_y_foreign_fresh"] = r4(cnt["y_foreign_100_fresh"] / max(cnt["fresh_N"], 1)); cnt["share_y_foreign_seen"] = r4(cnt["y_foreign_100_seen"] / max(cnt["seen_N"], 1))
print(f"COUNTS: {json.dumps(cnt)}", flush=True)
OUT["counts"] = cnt

# ---------------------------------------------------------------- 7. clustered SE and power, before the estimate
M = C.lpm(X[S], yf[S], art[S]); se = M["se"][0]
pw, pw05 = C.power(PRED, se, ALPHA), C.power(PRED, se, 0.05)
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_b:.3f}; fake calibrated 1.21]; power at +1.0, p < .00833: {pw:.3f}; at p < .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_p00833=r4(pw), power_p05=r4(pw05))

# ---------------------------------------------------------------- 8. estimate, halves, conditional logit, verdict
b, p = M["b"][0], M["p"][0]
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"], all_columns={nm: C.summ(M, i) for i, nm in enumerate(NAMES)})
print(f"PRIMARY LPM z_fresh: beta {b:+.4f} pp per SD (predicted +1.0), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print(f"  z_seen {M['b'][1]:+.4f} (SE {M['se'][1]:.4f}); fresh main effect {M['b'][NAMES.index('fresh')]:+.3f} (SE {M['se'][NAMES.index('fresh')]:.3f})", flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = S & (HV == h); HM[h] = C.lpm(X[s], yf[s], art[s])
    d = dict(half=h, songs=HM[h]["N"], fresh_songs=int((s & (FR == 1)).sum()), artists=HM[h]["G"], y_foreign_100_fresh=int((yf[s & (FR == 1)] > 0).sum()), **C.summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {d['songs']} songs ({d['fresh_songs']} fresh), {d['artists']} artists, fresh y_foreign=100 {d['y_foreign_100_fresh']}; "
          f"beta {d['beta']:+.4f} (SE {d['se']:.4f}, p {d['p']:.3g})", flush=True)

yb = (yf[S] > 0).astype(float); gS = art[S]
codes = {a: i for i, a in enumerate(sorted(set(gS)))}; gi = np.array([codes[a] for a in gS]); cS = np.bincount(gi)
ga = np.bincount(gi, weights=yb); keep_g = (ga > 0) & (ga < cS); keep = keep_g[gi]
Xk = X[S][keep]; sK = np.zeros((len(codes), X.shape[1])); np.add.at(sK, gi[keep], Xk); Xkd = Xk - (sK / np.maximum(cS, 1)[:, None])[gi[keep]]
novar = [NAMES[j] for j in range(X.shape[1]) if np.all(np.abs(Xkd[:, j]) < 1e-12)]
t1 = time.time(); cl = dict(columns_without_within_variation_in_kept_sample=novar,
                            kept_fresh_songs=int(keep[(FR[S] == 1)].sum()), kept_fresh_nonzero_z=int((keep & (FR[S] == 1)).sum()))
try:
    params, bse, pv, conv, ks, kg = C.cond_logit(X[S], yb, gS); cl["columns"] = "all columns as written"
except Exception as e:
    print(f"  statsmodels ConditionalLogit on all columns failed: {e!r}; refitting without the columns that have no within-artist variation "
          f"in the kept sample (they are not identified there): {novar}", flush=True)
    cl["error_all_columns"] = repr(e)
    use = [j for j in range(X.shape[1]) if NAMES[j] not in novar]
    pp_, bb_, pv_, conv, ks, kg = C.cond_logit(X[S][:, use], yb, gS)
    params = np.full(X.shape[1], np.nan); bse = params.copy(); pv = params.copy(); params[use], bse[use], pv[use] = pp_, bb_, pv_
    cl["columns"] = "without columns lacking within-artist variation in the kept sample"
cl.update(coef=r4(params[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=bool(conv), convergence_test="max|score|/nobs < 1e-5 (common.cond_logit)",
          kept_songs=ks, kept_artists=kg, dropped_songs=int(S.sum() - ks), dropped_artists=int(len(codes) - kg), seconds=round(time.time() - t1),
          all_columns={nm: [r4(a_), r4(b_)] for nm, a_, b_ in zip(NAMES, params, bse)})
print(f"CONDITIONAL LOGIT: drops {cl['dropped_artists']} artists, {cl['dropped_songs']} songs (all 0 or all 1); keeps {kg} artists, {ks} songs "
      f"({cl['kept_fresh_songs']} fresh); z_fresh coef {params[0]:+.4f} log-odds per SD (SE {bse[0]:.4f}, p {pv[0]:.4g}); converged: {conv}; "
      f"no within variation there: {novar}", flush=True)
OUT["conditional_logit"] = cl

hb = [HM[h]["b"][0] for h in (0, 1)]; cb = params[0]
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and cb > 0: v = "pass"
elif b < 0 and p < ALPHA: v = "opposite sign (beta < 0, p < .00833): killed; reported as a new hypothesis, not a pass"
elif b <= 0: v = "kill (beta <= 0)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00833")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb > 0: why.append("conditional logit sign disagrees")
    v = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the written rule): {v}", flush=True)

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
dn["z_seen_coefficient"] = C.summ(M, 1)
m = C.lpm(X, yy, art); dn["beta_on_y_in_DiscogsVI_at_all"] = dict(**C.summ(m, 0), N=m["N"], z_seen=C.summ(m, 1))
EL = np.array([C.early_late(r) for r in rows], float)
for j, nm in enumerate(("y_early_within_5y", "y_late_after_10y")):
    yv = EL[:, j]; s = np.isfinite(yv); m = C.lpm(X[s], yv[s], art[s])
    dn[nm] = dict(**C.summ(m, 0), N=m["N"], fresh_100=int((yv[s & (FR == 1)] > 0).sum()), seen_100=int((yv[s & (FR == 0)] > 0).sum()))
cs = np.array([bool(r.get("clique_seen")) for r in rows])
s = S & ~((FR == 1) & cs); m = C.lpm(X[s], yf[s], art[s])
dn["without_fresh_rows_whose_clique_is_seen__common_flag"] = dict(**C.summ(m, 0), N=m["N"], fresh_dropped=int((S & (FR == 1) & cs).sum()),
    note="common.load_battery_outcomes builds its 'seen cliques' from every key of the pack's covers file, which also holds fresh videos "
         "(fresh_vid_in_pack_covers_file), so this flag marks a fresh song whose own video is in that file; see the corrected form below")
# Deviation (reported item only): 'clique also matched by a seen song' rebuilt from the 13,198 seen songs' video ids only
CVp = json.loads(C5.GIT("hooktheory_covers_discogs.json")); seen_vids = {r["vid"] for r in seen_all}
seen_cq2 = {str(CVp[v_]["clique"]) for v_ in seen_vids if v_ in CVp}
cs2 = np.array([bool(r["fresh"]) and r.get("clique") is not None and r["clique"] in seen_cq2 for r in rows])
s = S & ~cs2; m = C.lpm(X[s], yf[s], art[s])
dn["without_fresh_rows_whose_clique_is_seen"] = dict(**C.summ(m, 0), N=m["N"], fresh_dropped=int((S & cs2).sum()),
    fresh_y_foreign_100_dropped=int((yf[S & cs2] > 0).sum()), seen_cliques=len(seen_cq2))
del CVp
hv = np.array([bool(r["vids"]) for r in rows])
s = S & ~((FR == 1) & ~hv); m = C.lpm(X[s], yf[s], art[s]); dn["fresh_rows_with_video_id_only"] = dict(**C.summ(m, 0), N=m["N"], fresh_dropped=int((S & (FR == 1) & ~hv).sum()))
KT = lambda st: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in st)
yk = yf.copy(); nchg = 0; nkt = 0
for i, r in enumerate(rows):
    if not np.isfinite(yf[i]) or not r.get("versions"): continue
    names = [e[0] for e in r["versions"]]; a = C.nrm(r["artist"]); nkt += int(any(KT(st) for st in names))
    own = [st for st in names if any(C.nrm(nm) == a for nm in st)]; O = {C.nrm(nm) for st in own for nm in st}
    new = 100.0 if [st for st in names if len(st) > 0 and not KT(st) and not any(C.nrm(nm) in O for nm in st)] else 0.0
    nchg += int(new != yf[i]); yk[i] = new
m = C.lpm(X[S], yk[S], art[S])
dn["y_foreign_without_karaoke_tribute_sets"] = dict(**C.summ(m, 0), songs_changed=nchg, songs_with_any_karaoke_or_tribute_set=nkt, fresh_100=int((yk[S & (FR == 1)] > 0).sum()))
nf = collections.Counter(r["artist"] for r in rows if r["fresh"])
sf = S & (FR == 1) & np.array([nf[r["artist"]] >= 2 for r in rows])
use = [j for j, nm in enumerate(NAMES) if nm not in ("z_seen", "fresh")]
m = C.lpm(X[sf][:, use], yf[sf], art[sf])
dn["fresh_only_within_artist"] = dict(**C.summ(m, 0), N=m["N"], artists=m["G"], y_foreign_100=int((yf[sf] > 0).sum()))
use = [j for j, nm in enumerate(NAMES) if nm != "has_mel"]
m = C.lpm(X[S][:, use], yf[S], art[S]); dn["without_has_mel"] = dict(**C.summ(m, 0), N=m["N"])
dn["fresh_counts"] = dict(y_100=cnt["y_100_fresh"], y_foreign_100=cnt["y_foreign_100_fresh"], y_foreign_nan=cnt["dropped_nan_fresh"])
dn["printed_match_checks"] = dict(fresh_with_vid=LO["fresh_with_vid"], fresh_vid_in_pack_covers_file=LO["fresh_vid_in_pack_covers_file"],
                                  fresh_slug_vs_vid_agree=LO["fresh_slug_vs_vid_agree"])
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k_, v_ in dn.items(): print(f"  {k_}: {json.dumps(v_)}", flush=True)
OUT["reported_deciding_nothing"] = dn

# ---------------------------------------------------------------- 10. result.json
finish(v)
