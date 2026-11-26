"""Run 06, fresh_tonic: tonic resistance H (R03-I2) on fresh Hooktheory songs whose outcome has never been seen.

The rule is PREDICTION.md in this folder (frozen and pushed in commit 08b5167, branch judging-research, before any outcome was
joined); shared rules are ../fresh_repetition/PREDICTION.md and ../common.py. The measure is common.H_song (run 05's tonic resistance,
run05/experiments/tonic_resistance/PREDICTION.md); the gate is run 05's, re-run on the seen rows.

Order (printed as it goes; PREDICTION.md's order):
  1. unit tests; 2. seen reproduction (9,009 with H; percentiles; mean, SD) and the shared battery counts; 3. gate on the seen rows
  (stop if it fails; fresh agreement reported); 4. notes-side power (bound 1.20 pp); 5. common.validate_match (cached);
  6. common.load_battery_outcomes; 7. counts; 8. clustered SE and power; 9. beta, halves, conditional logit, verdict;
  10. reported items; 11. result.json.
`--notes-only` stops before step 5 and writes nothing.
Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, collections, re
import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C
C5 = C.C5
NOTES_ONLY = "--notes-only" in sys.argv
ALPHA = C.ALPHA; ZC = float(N.isf(ALPHA / 2))
PRED = -0.6
r4 = C.r4
OUT = dict(rule="PREDICTION.md in this folder, commit 08b5167 (branch judging-research); shared rules ../fresh_repetition/PREDICTION.md, ../common.py",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           threshold_p=ALPHA, threshold_z=round(ZC, 3), prediction_pp_per_sd=PRED, kill="beta >= 0")
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    if NOTES_ONLY: print("NOTES-ONLY run: nothing written; would continue to the outcome. verdict so far:", verdict, flush=True); sys.exit(0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True); sys.exit(0)
def check(name, got, want, tol=0):
    ok = (got == want) if tol == 0 else abs(got - want) <= tol
    print(f"  check {name}: got {got} [frozen {want}] -> {'ok' if ok else 'DOES NOT REPRODUCE'}", flush=True)
    if not ok:
        OUT.setdefault("reproduction_failures", []).append([name, got, want]); finish(f"stopped (reproduction failed: {name})")
    return ok

# ---------------------------------------------------------------- 1. unit tests
def H_core(W, t):
    om = C._resist(W); pi = W.sum(1) / W.sum(); return float(pi @ om[:, t] / (pi @ om @ pi))
def cyc(n): W = np.zeros((n, n)); [W.__setitem__((i, (i + 1) % n), 1) for i in range(n)]; return W + W.T
star = np.zeros((4, 4)); star[0, 1:] = 1; star = star + star.T
unit = {}
for name, got, want in (("5-cycle", H_core(cyc(5), 0), 1.0), ("star, T at the hub", H_core(star, 0), 0.6), ("star, T on a leaf", H_core(star, 1), 1.4),
                        ("5-cycle via one token clip [0,18,27,36,45]", C.H_song([[0, 18, 27, 36, 45]])[0], 1.0),
                        ("star via tokens [[0,18],[0,27],[0,45]]", C.H_song([[0, 18], [0, 27], [0, 45]])[0], 0.6),
                        ("star via tokens [[18,0],[18,27],[18,45]]", C.H_song([[18, 0], [18, 27], [18, 45]])[0], 1.4)):
    unit[name] = dict(want=want, got=r4(got), ok=abs(got - want) < 1e-9)
    print(f"unit test H, {name}: want {want}, got {got:.10f}", flush=True)
OUT["unit_tests"] = unit
if not all(u["ok"] for u in unit.values()): finish("stopped (unit tests failed)")

# ---------------------------------------------------------------- 2. rows, measures, reproduction
B = C.battery(); rows = B["rows"]; seen_all, fresh_all = B["seen_all"], B["fresh_rows"]
v9 = {r["vid"] for r in B["seen_rows"]}; seen9 = [r for r in seen_all if r["vid"] in v9]
C.add_measures(seen_all + fresh_all, which=("A", "V", "ln_chg", "H"))
R = C.raw_clips()
def tpiece(seqs):
    """size of home's connected piece, by H_song's own rules (for the reported 'home piece not the whole graph' item)"""
    names = sorted(set(t for s in seqs for t in s)); ix = {t: i for i, t in enumerate(names)}; M = np.zeros((len(names), len(names)))
    for s in seqs:
        for x, y in zip(s, s[1:]): M[ix[x], ix[y]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[ix[s[-1]], ix[s[0]]] += 1
    Cm = M + M.T; np.fill_diagonal(Cm, 0); cand = [i for i, t in enumerate(names) if t // 9 == 0]
    if len(names) < 3 or not cand: return None
    rs = Cm.sum(1); T = min(cand, key=lambda i: (-rs[i], names[i])); _, lab = connected_components(Cm > 0, directed=False)
    return int((lab == lab[T]).sum())
for r in seen_all + fresh_all:
    r["seqs"] = [C.tokens_rel(R[c["k"]]) for c in r["clips"]]
    r["tpiece"] = tpiece(r["seqs"]) if np.isfinite(r["H"]) else None
print("REPRODUCTION (notes only):", flush=True)
fr_b = [r for r in rows if r["fresh"]]
check("fresh rows", len(fresh_all), 1825); check("battery rows", len(rows), 5768); check("battery fresh rows", len(fr_b), 1295)
check("battery artists", len(set(r["artist"] for r in rows)), 601); check("seen within-artist rows", len(seen9), 9588)
s9 = [r for r in seen9 if np.isfinite(r["H"])]; hv = np.array([r["H"] for r in s9])
check("seen rows with H", len(s9), 9009)
pct = np.percentile(hv, (10, 50, 90))
for q, g, w in zip((10, 50, 90), pct, (0.624, 0.818, 1.143)): check(f"seen H {q}th percentile", round(float(g), 3), w, 0.0005)
mu, sd = C.seen_sd(seen9, "H"); check("seen mean H", round(mu, 3), 0.870, 0.0005); check("seen SD H (z scale)", round(sd, 4), 0.2583, 0.00005)
RB = [r for r in rows if np.isfinite(r["H"])]; fRB = [r for r in RB if r["fresh"]]
check("battery rows with H", len(RB), 5144); check("seen battery rows with H", len(RB) - len(fRB), 4147); check("fresh battery rows with H", len(fRB), 997)
check("artists of fresh rows with H", len(set(r["artist"] for r in fRB)), 527); check("fresh battery rows without H", len(fr_b) - len(fRB), 298)
fz = (np.array([r["H"] for r in fRB]) - mu) / sd
fza = (np.array([r["H"] for r in fresh_all if np.isfinite(r["H"])]) - mu) / sd
print(f"  fresh H (battery rows): mean {np.mean([r['H'] for r in fRB]):.3f}, z range {fz.min():+.2f} to {fz.max():+.2f}; all fresh rows with H: z max {fza.max():+.2f} [frozen text: z up to 13.5]", flush=True)
OUT["reproduction"] = dict(fresh_rows=len(fresh_all), battery_rows=len(rows), battery_fresh=len(fr_b), battery_artists=len(set(r["artist"] for r in rows)),
                           seen9=len(seen9), seen_with_H=len(s9), seen_pct_10_50_90=[r4(x) for x in pct], seen_mean=r4(mu), seen_sd=r4(sd),
                           rows_with_H=len(RB), seen_rows_with_H=len(RB) - len(fRB), fresh_rows_with_H=len(fRB), fresh_artists_with_H=len(set(r["artist"] for r in fRB)),
                           fresh_battery_without_H=len(fr_b) - len(fRB), fresh_z_min=r4(fz.min()), fresh_z_max=r4(fz.max()), all_reproduced=True)

# ---------------------------------------------------------------- 3. GATE on the seen rows (run 05's, exactly), fresh reported
def dums(nd): nd = np.asarray(nd); return [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)]
def ols_resid(y, X): return y - X @ np.linalg.lstsq(X, y, rcond=None)[0]
def clip_gate(songs):
    pairs = []
    for r in songs:
        if r["nclips"] < 2: continue
        a, b = C.H_song([r["seqs"][0]]), C.H_song([r["seqs"][1]])
        if not (np.isfinite(a[0]) and np.isfinite(b[0])): continue
        pairs.append((a, b))
    P = len(pairs); hs = np.array([a[0] for a, _ in pairs] + [b[0] for _, b in pairs])
    Xc = np.column_stack([np.ones(2 * P)] + dums([a[1] for a, _ in pairs] + [b[1] for _, b in pairs]) + [np.array([a[2] for a, _ in pairs] + [b[2] for _, b in pairs], float)])
    res = ols_resid(hs, Xc)
    return float(spearmanr(res[:P], res[P:])[0]), float(spearmanr(hs[:P], hs[P:])[0]), P
rho_cc, rho_raw, P = clip_gate(s9); g1 = rho_cc >= 0.20
print(f"GATE 1 (seen), clip-to-clip residualised: {rho_cc:.4f} on {P} pairs (needs >= 0.20) [chair 0.203, 3,512]; raw {rho_raw:.4f} [0.259] -> {'pass' if g1 else 'FAIL'}", flush=True)
check("gate pairs", P, 3512); check("gate rho", round(rho_cc, 3), 0.203, 0.0005)
Xs = np.column_stack([np.ones(len(s9))] + dums([r["n_tok"] for r in s9]) + [np.array([r["links"] for r in s9], float), np.log([r["nclips"] for r in s9])])
Hres = ols_resid(hv, Xs); R2 = float(1 - (Hres ** 2).sum() / ((hv - hv.mean()) ** 2).sum())
cands = {f: [r[f] for r in s9] for f in C.FE}
cands.update(n_ch=[r["n_ch"] for r in s9], beats=[r["beats"] for r in s9], clips_per_song=[r["nclips"] for r in s9],
             distinct_chords=[r["n_tok"] for r in s9], links=[r["links"] for r in s9])
cor = {k: C.sp(Hres, v) for k, v in cands.items()}; top = max(cor, key=lambda k: abs(cor[k][0]))
g2 = abs(cor[top][0]) <= 0.7 and R2 <= 0.8
print("GATE 2 (seen), Spearman of H_res with:", json.dumps({k: r4(v[0]) for k, v in cor.items()}), flush=True)
print(f"  largest |rho| {top} {cor[top][0]:+.4f} (<= 0.7) [chair beats 0.081]; ch_rep {cor['ch_rep'][0]:+.4f}; R2 on the size block {R2:.4f} (<= 0.8) [0.156] -> {'pass' if g2 else 'FAIL'}", flush=True)
# fresh agreement, reported (not gated): fresh rows (all 1,825) and battery fresh rows
fg_all = clip_gate([r for r in fresh_all if np.isfinite(r["H"])]); fg_b = clip_gate(fRB)
print(f"  fresh clip-to-clip (reported, not gated): all fresh rows {fg_all[0]:.4f} on {fg_all[2]} pairs (raw {fg_all[1]:.4f}); battery fresh rows {fg_b[0]:.4f} on {fg_b[2]} pairs (raw {fg_b[1]:.4f}) [chair 0.182 on 243, raw 0.213]", flush=True)
OUT["gate"] = dict(seen=dict(clip_to_clip_residualised=r4(rho_cc), rho_unrounded=rho_cc, pairs=P, raw=r4(rho_raw), threshold=0.20, passed=bool(g1),
                             overlap_spearman_H_res={k: r4(v[0]) for k, v in cor.items()}, largest_abs=[top, r4(cor[top][0])], r2_size_block=r4(R2), overlap_passed=bool(g2),
                             chair=dict(rho=0.203, pairs=3512, raw=0.259, largest=["beats", 0.081], r2=0.156)),
                   fresh_reported=dict(all_fresh_rows=dict(rho=r4(fg_all[0]), raw=r4(fg_all[1]), pairs=fg_all[2]),
                                       battery_fresh_rows=dict(rho=r4(fg_b[0]), raw=r4(fg_b[1]), pairs=fg_b[2]), chair=dict(rho=0.182, raw=0.213, pairs=243)),
                   passed=bool(g1 and g2))
print(f"GATE: {'PASSED' if g1 and g2 else 'FAILED'}", flush=True)
if not (g1 and g2): finish("stopped (gate failed; no outcome joined)")

# ---------------------------------------------------------------- columns and 4. notes-side power
zc = lambda Rb, nm: (np.array([r[nm] for r in Rb], float) - C.seen_sd(seen9, nm)[0]) / C.seen_sd(seen9, nm)[1]
def extra(Rb):
    e = {"z_ch_rep": zc(Rb, "ch_rep")}; nd = np.array([r["n_tok"] for r in Rb])
    e.update({f"ntok{k}": (nd == k).astype(float) for k in range(4, 12)}); e["ntok12p"] = (nd >= 12).astype(float)
    e["links"] = np.array([r["links"] for r in Rb], float); return e
def design(Rb, drop=()):
    names, X, _ = C.fresh_design(Rb, "H", seen9, extra(Rb))
    keep = [i for i, n in enumerate(names) if n not in drop]
    return [names[i] for i in keep], X[:, keep]
def demean(M, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); c_ = np.bincount(gg)
    M2 = np.asarray(M, float).reshape(len(M), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / c_[:, None])[gg]
names0, X0 = design(RB); Xw = demean(X0, [r["artist"] for r in RB]); o = Xw[:, 1:]; o = o[:, np.abs(o).sum(0) > 1e-12]
xt = Xw[:, 0] - o @ np.linalg.lstsq(o, Xw[:, 0], rcond=None)[0]; se_bound = float(np.sqrt(0.22 * 0.78) * 100 / np.sqrt(xt @ xt))
PF = json.load(open(os.path.join(os.path.dirname(HERE), "power_fake.json")))["fresh_tonic"]
print(f"NOTES-SIDE POWER: columns {names0}", flush=True)
print(f"  SE bound {se_bound:.3f} pp [frozen 1.20]; power at {PRED} and p < .00833: {C.power(PRED, se_bound, ALPHA):.3f}; at .05: {C.power(PRED, se_bound, 0.05):.3f}", flush=True)
print(f"  fake-outcome power (../power_fake.json): calibrated SE {PF['calibrated']['zero']['se_median']}, pass rate if true {PF['calibrated']['true']['pass_rate']}; "
      f"homogeneous SE {PF['homogeneous']['zero']['se_median']}, pass rate {PF['homogeneous']['true']['pass_rate']}", flush=True)
check("notes-side SE bound", round(se_bound, 2), 1.20, 0.005)
OUT["notes_side_power"] = dict(se_bound_pp=r4(se_bound), power_at_alpha=r4(C.power(PRED, se_bound, ALPHA)), power_at_05=r4(C.power(PRED, se_bound, 0.05)),
                               columns=names0, fake_outcome_power=PF)
if NOTES_ONLY: finish("notes side complete")

# ---------------------------------------------------------------- 5-6. validation (cached) and outcome
v = C.validate_match(HERE)
print(f"MATCH VALIDATION (cached ../match_validation.json): passed {v['passed']}; key Jaccard {v['key_jaccard']}, cliques {v['clique_agree']}, "
      f"version sets {v['version_sets_agree']}, seen y_foreign {v['seen_y_foreign_agree']}", flush=True)
OUT["validation"] = {k: v[k] for k in v if not isinstance(v[k], list)}
if not v["passed"]: finish("stopped (validation failed)")
osum = C.load_battery_outcomes(rows, HERE)
print("OUTCOME joined:", json.dumps(osum, default=str), flush=True)
OUT["outcome_summary"] = osum
KT = lambda s: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)
nrm = C.nrm
for r in rows:
    r["y_kt"] = r["y_foreign"]
    if r.get("versions") and np.isfinite(r["y_foreign"]):
        sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"]); own = [s for s in sets if any(nrm(nm) == a for nm in s)]
        O = {nrm(nm) for s in own for nm in s}; foreign = [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)]
        r["y_kt"] = 100.0 if [s for s in foreign if not KT(s)] else 0.0
    r["y_early"], r["y_late"] = C.early_late(r)

# ---------------------------------------------------------------- 7. counts
S = [r for r in RB if np.isfinite(r["y_foreign"])]; art = [r["artist"] for r in S]; yf = np.array([r["y_foreign"] for r in S])
fS = [r for r in S if r["fresh"]]; sS = [r for r in S if not r["fresh"]]
cnt = dict(N=len(S), artists=len(set(art)), fresh=len(fS), seen=len(sS), fresh_artists=len(set(r["artist"] for r in fS)),
           fresh_y1=int(sum(r["y"] > 0 for r in fS)), fresh_y_foreign1=int(sum(r["y_foreign"] > 0 for r in fS)),
           seen_y_foreign1=int(sum(r["y_foreign"] > 0 for r in sS)), fresh_y_foreign_rate_pct=r4(np.mean([r["y_foreign"] for r in fS])),
           seen_y_foreign_rate_pct=r4(np.mean([r["y_foreign"] for r in sS])),
           dropped_nan_fresh=sum(1 for r in fRB if not np.isfinite(r["y_foreign"])), dropped_nan_seen=sum(1 for r in RB if not r["fresh"] and not np.isfinite(r["y_foreign"])))
print("COUNTS:", json.dumps(cnt), flush=True); OUT["counts"] = cnt

# ---------------------------------------------------------------- 8. SE and power, then 9. beta
names, X = design(S); M = C.lpm(X, yf, art); se = float(M["se"][0])
pw, pw05 = C.power(PRED, se, ALPHA), C.power(PRED, se, 0.05)
kill_if_true = float(N.sf(-PRED / se))   # kill = beta >= 0: P(beta_hat >= 0 | beta = PRED)
print(f"PRIMARY LPM: N {M['N']}, artists {M['G']}, columns {M['K']}; clustered SE of beta(z_fresh) {se:.4f} pp; power at {PRED} and p < .00833: {pw:.3f}; "
      f"at .05: {pw05:.3f}; kill (beta >= 0) fires {kill_if_true:.0%} if {PRED} is true, 50% if 0", flush=True)
b, p = float(M["b"][0]), float(M["p"][0])
print(f"beta(z_fresh) = {b:+.4f} pp per SD, SE {se:.4f}, p = {p:.5f}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f} (predicted {PRED})", flush=True)
print("  other columns: " + ", ".join(f"{names[i]} {M['b'][i]:+.3f} ({M['se'][i]:.3f})" for i in (1, 2)), flush=True)
OUT["primary"] = dict(N=M["N"], artists=M["G"], K=M["K"], **C.summ(M, 0), power_at_alpha=r4(pw), power_at_05=r4(pw05),
                      kill_fires_if_prediction_true=r4(kill_if_true), z_seen=C.summ(M, 1), z_ch_rep=C.summ(M, 2), columns=names)
hb = []; OUT["halves"] = []
for h in (0, 1):
    idx = [i for i, r in enumerate(S) if r["half"] == h]
    Mh = C.lpm(X[idx], yf[idx], [art[i] for i in idx]); hb.append(float(Mh["b"][0]))
    nf = sum(S[i]["fresh"] for i in idx)
    print(f"  half {h}: {Mh['N']} songs ({nf} fresh), {Mh['G']} artists; beta {Mh['b'][0]:+.4f} (SE {Mh['se'][0]:.4f}, p {Mh['p'][0]:.4f})", flush=True)
    OUT["halves"].append(dict(half=h, songs=Mh["N"], fresh=int(nf), artists=Mh["G"], **C.summ(Mh, 0)))
pr_, bse_, pv_, conv, ks, kg = C.cond_logit(X, yf / 100, art); cb = float(pr_[0])
print(f"  conditional logit: keeps {ks} songs in {kg} artists (drops {len(S) - ks} songs, {len(set(art)) - kg} artists with all-0 or all-1); "
      f"beta(z_fresh) {cb:+.4f} log-odds per SD (SE {bse_[0]:.4f}, p {pv_[0]:.4f}); converged: {conv}", flush=True)
bad = [names[i] for i in range(len(names)) if not np.isfinite(bse_[i]) or abs(pr_[i]) > 10]
if bad: print(f"  conditional logit columns with no finite / huge estimate (nuisance): {bad}", flush=True)
OUT["conditional_logit"] = dict(beta=r4(cb), se=r4(bse_[0]), p=float(f"{pv_[0]:.4g}"), converged=conv, songs_kept=ks, artists_kept=kg,
                                songs_dropped=len(S) - ks, artists_dropped=len(set(art)) - kg, nuisance_columns_unstable=bad)
if b > 0 and p < ALPHA: verdict = "kill (opposite sign, p < .00833: reported as a new hypothesis, not a pass)"
elif b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0 and conv and cb < 0: verdict = "pass"
elif b >= 0: verdict = "kill (beta >= 0; closes R03-I2)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00833")
    if not (hb[0] < 0 and hb[1] < 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb < 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (H on y_foreign, fresh songs): {verdict}", flush=True)

# ---------------------------------------------------------------- 10. reported, deciding nothing
dn = {}
def sub(label, idx, yv=None, drop=()):
    Rb = [S[i] for i in idx] if idx is not None else S
    yv_ = np.array([r[yv or "y_foreign"] for r in Rb], float); ok = np.isfinite(yv_); Rb = [r for r, k in zip(Rb, ok) if k]; yv_ = yv_[ok]
    nm, Xs_ = design(Rb, drop); Ms = C.lpm(Xs_, yv_, [r["artist"] for r in Rb])
    dn[label] = dict(N=Ms["N"], artists=Ms["G"], fresh=int(sum(r["fresh"] for r in Rb)), y_1_fresh=int(sum(yv_[i] > 0 for i, r in enumerate(Rb) if r["fresh"])),
                     **C.summ(Ms, 0))
dn["z_seen"] = C.summ(M, 1)
sub("on_y", None, "y")
sub("early_uptake_y_early", None, "y_early"); sub("late_uptake_y_late", None, "y_late")
sub("y_foreign_without_karaoke_tribute", None, "y_kt")
dn["y_foreign_without_karaoke_tribute"].update(rows_flipped=int(sum((r["y_foreign"] > 0) != (r["y_kt"] > 0) for r in S)),
                                               fresh_rows_flipped=int(sum((r["y_foreign"] > 0) != (r["y_kt"] > 0) for r in fS)),
                                               rows_with_a_karaoke_or_tribute_set=sum(1 for r in S if r.get("versions") and any(KT(e[0]) for e in r["versions"])))
sub("clique_collision_dropped", [i for i, r in enumerate(S) if not (r["fresh"] and r.get("clique_seen"))])
sub("fresh_rows_with_video_id_only", [i for i, r in enumerate(S) if not r["fresh"] or r["vids"]])
sub("without_has_mel", None, drop=("has_mel",))
sub("fresh_home_piece_not_whole_graph_dropped", [i for i, r in enumerate(S) if not r["fresh"] or r["tpiece"] == r["n_tok"]])
dn["fresh_home_piece_not_whole_graph_rows"] = sum(1 for r in fS if r["tpiece"] != r["n_tok"])
nfa = collections.Counter(r["artist"] for r in fr_b); FO = [r for r in fS if nfa[r["artist"]] >= 2]
yfo = np.array([r["y_foreign"] for r in FO]); nmf, Xf = design(FO, drop=("z_seen", "fresh")); Mf = C.lpm(Xf, yfo, [r["artist"] for r in FO])
dn["fresh_only_within_artist"] = dict(N=Mf["N"], artists=Mf["G"], artists_with_2plus_fresh_in_battery=sum(1 for a in nfa if nfa[a] >= 2),
                                      y_foreign_1=int((yfo > 0).sum()), **C.summ(Mf, 0))
fa = [r for r in fRB if np.isfinite(r["A"])]
dn["rho_H_A_fresh"] = dict(rho=r4(spearmanr([r["H"] for r in fa], [r["A"] for r in fa])[0]), rows=len(fa))
dn["fresh_counts"] = dict(y_1=cnt["fresh_y1"], y_foreign_1=cnt["fresh_y_foreign1"], rows=cnt["fresh"])
dn["per_half_counts"] = [dict(half=h["half"], songs=h["songs"], fresh=h["fresh"], artists=h["artists"]) for h in OUT["halves"]]
print("REPORTED, DECIDING NOTHING:", flush=True)
for k, v_ in dn.items(): print(f"  {k}: {json.dumps(v_, default=str)}", flush=True)
OUT["reported_deciding_nothing"] = dn
finish(verdict)
