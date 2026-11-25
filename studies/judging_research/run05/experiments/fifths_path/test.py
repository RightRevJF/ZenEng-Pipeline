"""Run 05, fifths_path: steps around the circle of fifths (FP, R03-F1) on the extensive margin, with R04-G1 diatonicity (D5) reported.

Rule: PREDICTION.md in this folder, frozen and committed in 1f6c36d (branch judging-research) before any outcome was joined.
The measure was first defined in run 03 (../../../run03/experiments/fifths_path/); tonight's PREDICTION.md governs where they differ.

  FP = mean shortest arc on the circle of fifths (phase of the 5th Fourier coefficient of each merged chord run, Amiot) over every
       kept move of the song's clips pooled (consecutive runs, plus the wrap last -> first when tokens differ).
  Prediction: beta(FP) on y_foreign = -0.6 pp per SD, within artist (smaller steps, more uptake by another artist).
  Pass: beta < 0, p < .00714 (.05/7, two-sided), beta < 0 in both artist halves, conditional logit < 0 and converged.
  Kill: beta > -0.2. Opposite sign (beta > 0, p < .00714): killed, reported as a new hypothesis. Unsettled: anything else.

Order (as the rule says): 1. unit values and worked examples; 2. rows, FP, D5, distinct chords, links; 3. gate (stop if it fails,
no outcome read); 4. notes-side power; 5. load_outcomes; 6. counts; 7. clustered SE and power; 8. beta, halves, conditional logit,
verdict; 9. reported items; 10. result.json.
Code check on a fake random outcome (no outcome file read): FAKE_Y=/some/dir python3 test.py (writes result.json there, not here).
One process; BLAS threads are pinned to 1.

Data credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
             Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
python3 test.py -> result.json in this folder
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, collections
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

ALPHA = 0.05 / 7; ZC = 2.690; PRED = -0.6; KILL = -0.2
FAKE = os.environ.get("FAKE_Y")
OUTDIR = FAKE if FAKE else HERE
OUT = dict(rule="PREDICTION.md in this folder, commit 1f6c36d", test="fifths_path (R03-F1 on the extensive margin; R04-G1 D5 reported)",
           alpha=round(ALPHA, 5), prediction_pp_per_sd=PRED, kill_line=KILL, fake_outcome=bool(FAKE),
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)")
r4 = C.r4
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- the measure (run 03's rules, PREDICTION.md steps 1-7)
QUAL = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
def qual(iv): return QUAL.get(tuple(iv or []), 8)

def phase(S):
    f = sum(np.exp(-2j * np.pi * 5 * k / 12) for k in S)
    return None if abs(f) < 1e-6 else float(np.angle(f))

def arc(a, b): d = abs(a - b) % (2 * np.pi); return float(min(d, 2 * np.pi - d))

def runs_of(a):
    """merged runs (consecutive equal tokens), each (token, phase of its first event's tonic-relative pc set)"""
    tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0; R = []
    for ev in sorted(a.get("harmony") or [], key=lambda c: c["onset"]):
        r = (ev["root_pitch_class"] - tonic) % 12; t = r * 9 + qual(ev["root_position_intervals"])
        if R and R[-1][0] == t: continue
        S = {r} | {int((r + s) % 12) for s in np.cumsum(ev["root_position_intervals"] or [])}
        R.append((t, phase(S)))
    return R

def moves_of(R):
    mv = list(zip(R, R[1:]))
    if len(R) > 1 and R[-1][0] != R[0][0]: mv.append((R[-1], R[0]))
    return mv

def clip_steps(a):
    """kept steps of one clip and the number of moves"""
    mv = moves_of(runs_of(a))
    return [arc(x[1], y[1]) for x, y in mv if x[1] is not None and y[1] is not None], len(mv)

def D5(a, c=None):
    v = np.zeros(12)
    for h in a.get("harmony") or []:
        d = h["offset"] - h["onset"]
        if d > 0:
            for p in C.chord_pcs(h): v[p] += d
    if v.sum() == 0: return np.nan
    return float(abs((v * np.exp(-2j * np.pi * 5 * np.arange(12) / 12)).sum()) / v.sum())

def fake_clip(chords):   # (root relative to C, root_position_intervals), tonic C, one beat each
    return dict(keys=[dict(tonic_pitch_class=0, beat=0)],
                harmony=[dict(root_pitch_class=r, root_position_intervals=iv, onset=i, offset=i + 1) for i, (r, iv) in enumerate(chords)])

# ---------------------------------------------------------------- 1. unit values and worked examples
MAJ, MIN, DOM7 = [4, 3], [3, 4], [4, 3, 3]
CH = dict(I=(0, MAJ), V=(7, MAJ), IV=(5, MAJ), vi=(9, MIN), ii=(2, MIN), iii=(4, MIN), bVII=(10, MAJ), i=(0, MIN), bVI=(8, MAJ), bII=(1, MAJ), V7=(7, DOM7))
UNIT = [("I", "V", np.pi / 6), ("I", "IV", np.pi / 6), ("I", "vi", np.pi / 6), ("ii", "V", np.pi / 6), ("I", "iii", np.pi / 3), ("I", "bVII", np.pi / 3),
        ("I", "i", np.pi / 3), ("IV", "V", np.pi / 3), ("I", "bVI", 2 * np.pi / 3), ("I", "bII", 5 * np.pi / 6), ("V", "vi", 0.0), ("I", "ii", 0.0)]
unit = {}
for x, y_, want in UNIT:
    got = clip_steps(fake_clip([CH[x], CH[y_]]))[0][0]; unit[f"{x}->{y_}"] = dict(want=r4(want), got=r4(got))
    print(f"unit {x}->{y_}: {got:.4f} (want {want:.4f})"); assert abs(got - want) < 1e-9, (x, y_, got, want)
pI = runs_of(fake_clip([CH["I"]]))[0][1]; pV7 = runs_of(fake_clip([CH["V7"]]))[0][1]
assert abs(pV7 - pI) < 1e-9; print(f"unit: phase(V7) {pV7:.4f} = phase(I) {pI:.4f}")
assert runs_of(fake_clip([(0, [4, 4])]))[0][1] is None and runs_of(fake_clip([(0, [3, 3, 3])]))[0][1] is None
print("unit: augmented triad and diminished seventh have no phase")
unit.update(V7_phase_equals_I=True, aug_and_dim7_no_phase=True)
WORK = {}
for nm, prog, want in (("I-V-vi-IV", ["I", "V", "vi", "IV"], [0.524, 0, 1.047, 0.524]), ("I-IV-V", ["I", "IV", "V"], [0.524, 1.047, 0.524])):
    st, _ = clip_steps(fake_clip([CH[c] for c in prog]))
    labels = [f"{a}->{b}" for a, b in zip(prog, prog[1:] + prog[:1])]
    assert np.allclose(st, want, atol=5e-4), (nm, st)
    WORK[nm] = dict(steps={l: r4(s) for l, s in zip(labels, st)}, FP=r4(np.mean(st)))
    print(f"worked example {nm}: " + ", ".join(f"{l} {s:.3f}" for l, s in zip(labels, st)) + f" (last = wrap) -> FP {np.mean(st):.3f} rad", flush=True)
assert abs(WORK["I-V-vi-IV"]["FP"] - 0.5236) < 1e-3 and abs(WORK["I-IV-V"]["FP"] - 0.6981) < 1e-3
OUT.update(unit_values=unit, worked_example=WORK)

# ---------------------------------------------------------------- 2. rows, FP, D5, distinct chords, links (notes only)
D = C.load_rows(); rows = D["rows"]; R = C.raw_clips()
n_moves = n_kept = n_zero = 0; missing = 0
for r in rows:
    per, seqs = [], []
    for c in r["clips"]:
        a = R.get(c["k"])
        if a is None: missing += 1; per.append(([], 0)); seqs.append([]); continue
        per.append(clip_steps(a)); seqs.append([t for t, _ in runs_of(a)])
    allst = [x for st, _ in per for x in st]
    n_moves += sum(m for _, m in per); n_kept += len(allst); n_zero += sum(1 for x in allst if x < 1e-9)
    r["FP"] = float(np.mean(allst)) if allst else np.nan
    r["zero_share"] = float(np.mean([x < 1e-9 for x in allst])) if allst else np.nan
    cv = [float(np.mean(st)) if st else np.nan for st, _ in per]
    r["FP_c12"] = (cv[0], cv[1]) if len(cv) >= 2 and np.isfinite(cv[:2]).all() else None
    r["distinct_chords"] = len({t for s in seqs for t in s})
    links = set()
    for s in seqs:
        for x, y_ in zip(s, s[1:]):
            if x != y_: links.add(frozenset((x, y_)))
        if len(s) > 1 and s[-1] != s[0]: links.add(frozenset((s[-1], s[0])))
    r["links"] = len(links)
mD5 = C.song_measure(rows, D5, "D5")
fp = np.array([r["FP"] for r in rows]); ok_fp = np.isfinite(fp); pct = np.nanpercentile(fp, (10, 50, 90))
rho_fp_d5 = C.sp(fp, [r["D5"] for r in rows])
print(f"[{time.time() - T0:.0f}s] FP: {int(ok_fp.sum())} of {len(rows)} songs have a value [chair 9,588]; clips missing from the raw file: {missing}; "
      f"moves {n_moves}, kept {n_kept}, skipped (no phase) {n_moves - n_kept}; zero steps {n_zero / n_kept:.4f} of kept moves", flush=True)
print(f"  FP 10th / 50th / 90th: {pct[0]:.3f} / {pct[1]:.3f} / {pct[2]:.3f} rad [chair 0.449 / 0.714 / 1.197]", flush=True)
print(f"  D5: {int(np.isfinite([r['D5'] for r in rows]).sum())} songs; rho(FP, D5) {rho_fp_d5[0]:+.4f} on {rho_fp_d5[1]} [chair -0.73]", flush=True)
OUT["measure"] = dict(songs=len(rows), songs_with_FP=int(ok_fp.sum()), clips_missing_raw=missing, moves=n_moves, moves_kept=n_kept,
                      moves_skipped_no_phase=n_moves - n_kept, share_zero_steps=r4(n_zero / n_kept), FP_p10_p50_p90=[r4(x) for x in pct],
                      rho_FP_D5=[r4(rho_fp_d5[0]), rho_fp_d5[1]])

# ---------------------------------------------------------------- 3. GATE (no outcome loaded)
G = C.gate(rows, "FP", extra={"distinct_chords": [r["distinct_chords"] for r in rows], "links": [r["links"] for r in rows]})
top5 = sorted(G["overlap_all"].items(), key=lambda kv: -abs(kv[1] or 0))[:5]
print(f"GATE 1, clip 1 vs clip 2: Spearman {G['clip_to_clip']:.4f} on {G['clip_pairs']} pairs (needs >= 0.20) [chair 0.407 on 4,268]", flush=True)
print(f"GATE 2, overlap: largest {G['overlap_largest']} (needs |rho| <= 0.7) [chair ch_ic_mean +0.286; distinct chords +0.231]; top 5 {top5}", flush=True)
print(f"  ch_rep {G['overlap_all']['ch_rep']:+.4f}; all: {json.dumps(G['overlap_all'])}", flush=True)
print(f"GATE: {'PASSED' if G['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = G
if not G["passed"]:
    OUT["outcome_joined"] = False; finish("stopped (gate failed before any outcome was read)")

# ---------------------------------------------------------------- design (columns as the rule lists them)
art_all = np.array([r["artist"] for r in rows]); half_all = np.array([r["half"] for r in rows])
cn, Xc = C.controls(rows)
Zfp = C.zs(fp); Zrep = C.zs([r["ch_rep"] for r in rows]); Zic = C.zs([r["ch_ic_mean"] for r in rows]); Zd5 = C.zs([r["D5"] for r in rows])
def design(first="FP", ic=True, extra=None):
    cols = {"z_" + first: {"FP": Zfp, "D5": Zd5}[first], "z_ch_rep": Zrep}
    if ic: cols["z_ch_ic_mean"] = Zic
    cols.update({k: Xc[:, j] for j, k in enumerate(cn)})
    if extra: cols.update(extra)
    return list(cols), np.column_stack(list(cols.values()))
NAMES, X = design()
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)

# ---------------------------------------------------------------- 4. notes-side power
def demean(M, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); cnt = np.bincount(gg)
    M2 = np.asarray(M, float).reshape(len(g), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / cnt[:, None])[gg]
okn = ok_fp
Xw = demean(X[okn], art_all[okn]); xw = Xw[:, 0]; ow = Xw[:, 1:]; ow = ow[:, np.abs(ow).sum(0) > 1e-12]
xt = xw - ow @ np.linalg.lstsq(ow, xw, rcond=None)[0]
se_bound = np.sqrt(0.22 * 0.78) * 100 / np.sqrt(xt @ xt)
pw_n = C.power(PRED, se_bound, ALPHA); pw_n05 = C.power(PRED, se_bound, 0.05)
print(f"NOTES-SIDE POWER: residual share {xt @ xt / okn.sum():.3f} [0.670]; SE bound {se_bound:.3f} pp [0.52]; power at -0.6, p < .00714: {pw_n:.3f} [0.06]; "
      f"at p < .05: {pw_n05:.3f} [0.21]", flush=True)
OUT["notes_side_power"] = dict(residual_share=r4(xt @ xt / okn.sum()), se_bound_pp=r4(se_bound), power_p00714=r4(pw_n), power_p05=r4(pw_n05))

# ---------------------------------------------------------------- 5. outcome
if FAKE:   # code check: a random outcome; no outcome file is read
    rs = np.random.default_rng(7)
    for r in rows:
        r["y"] = 100.0 if rs.random() < 0.23 else 0.0
        r["y_foreign"] = (np.nan if rs.random() < 0.02 else (100.0 if rs.random() < 0.8 else 0.0)) if r["y"] > 0 else 0.0
        r["covers"] = int(rs.integers(1, 30)) if r["y"] > 0 else None; r["lcov"] = float(np.log1p(r["covers"])) if r["covers"] else None
        r["first_year"] = int(rs.integers(1960, 2020)) if r["y"] > 0 else None
        r["versions"] = [[["Fake Artist"], 2000, [1]], [["Karaoke Kings"], 2001, [1]]] if r["y"] > 0 else None
    LO = dict(md5=["fake", "fake"], drops=int(sum(np.isnan(r["y_foreign"]) for r in rows)))
else:
    LO = C.load_outcomes(rows, HERE)
yf = np.array([r["y_foreign"] for r in rows], float); yv = np.array([r["y"] for r in rows], float)
keep = np.isfinite(yf) & ok_fp
Xk, yk, ak, hk = X[keep], yf[keep], art_all[keep], half_all[keep]

# ---------------------------------------------------------------- 6. counts
print(f"\nOUTCOME (md5 {LO['md5']}): y = 100 rows {int((yv > 0).sum())}; y_foreign dropped (NaN) {int((~np.isfinite(yf)).sum())}; "
      f"model N {int(keep.sum())} songs, {len(set(ak))} artists; y_foreign = 100: {int((yk > 0).sum())} ({(yk > 0).mean():.4f})", flush=True)
OUT["outcome"] = dict(md5=LO["md5"], y1=int((yv > 0).sum()), y_foreign_dropped=int((~np.isfinite(yf)).sum()), N=int(keep.sum()),
                      artists=len(set(ak)), y_foreign1=int((yk > 0).sum()), share_y_foreign1=r4((yk > 0).mean()))

# ---------------------------------------------------------------- 7. clustered SE and power (before any beta)
M = C.lpm(Xk, yk, ak); se = float(M["se"][0])
pw = C.power(PRED, se, ALPHA); pw05 = C.power(PRED, se, 0.05)
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_bound:.3f}]; power at -0.6 pp, p < .00714: {pw:.3f}; at p < .05: {pw05:.3f}", flush=True)
OUT["power"] = dict(se=r4(se), power_p00714=r4(pw), power_p05=r4(pw05))

# ---------------------------------------------------------------- 8. beta, halves, conditional logit, verdict
b, p = float(M["b"][0]), float(M["p"][0])
print(f"PRIMARY LPM: beta(FP) {b:+.4f} pp per SD (predicted -0.6), SE {se:.4f}, p {p:.4g}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; "
      f"N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print(f"  ch_rep {M['b'][1]:+.4f} (SE {M['se'][1]:.4f}), ch_ic_mean {M['b'][2]:+.4f} (SE {M['se'][2]:.4f})", flush=True)
OUT["primary"] = dict(FP=C.summ(M, 0), ch_rep=C.summ(M, 1), ch_ic_mean=C.summ(M, 2), N=M["N"], artists=M["G"], K=M["K"])
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = hk == h; HM[h] = C.lpm(Xk[s], yk[s], ak[s])
    OUT["halves"].append(dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], y_foreign1=int((yk[s] > 0).sum()), FP=C.summ(HM[h], 0)))
    print(f"HALF {h}: {HM[h]['N']} songs, {HM[h]['G']} artists; beta {HM[h]['b'][0]:+.4f} (SE {HM[h]['se'][0]:.4f}, p {HM[h]['p'][0]:.3g})", flush=True)
hb = [float(HM[h]["b"][0]) for h in (0, 1)]

ybk = (yk > 0).astype(float)
codes = {a: i for i, a in enumerate(sorted(set(ak)))}; gk = np.array([codes[a] for a in ak]); cntk = np.bincount(gk); gak = np.bincount(gk, weights=ybk)
kg = (gak > 0) & (gak < cntk)
try:
    prm, bse, pv, conv, ks, kgn = C.cond_logit(Xk, ybk, list(ak))
    cl = dict(coef=r4(prm[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=bool(conv), kept_songs=ks, kept_artists=kgn,
              dropped_songs=int(len(ak) - ks), dropped_artists=int(len(codes) - kgn), convergence_test="max|score|/nobs < 1e-5 (BFGS, then Newton)",
              ch_rep=r4(prm[1]), ch_ic_mean=r4(prm[2]), large_nuisance_coefs={NAMES[j]: r4(prm[j]) for j in range(len(NAMES)) if abs(prm[j]) > 5})
except Exception as e:
    prm = None; conv = False; cl = dict(error=repr(e), converged=False)
print(f"CONDITIONAL LOGIT: {json.dumps(cl)}", flush=True)
OUT["conditional_logit"] = cl
cb = float(prm[0]) if prm is not None else np.nan

if b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0 and conv and cb < 0: verdict = "pass"
elif b > 0 and p < ALPHA: verdict = "opposite sign (beta > 0, p < .00714): killed; reported as a new hypothesis ('bold steps are what others take up'), not a pass"
elif b > KILL: verdict = "kill (beta > -0.2 pp)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00714")
    if not (hb[0] < 0 and hb[1] < 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb < 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (by the rule): {verdict}", flush=True)

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
_, Xd = design(first="D5"); okd = keep & np.isfinite(Zd5)
dn["D5_in_place_of_FP"] = dict(songs=int(okd.sum()), **C.summ(C.lpm(Xd[okd], yf[okd], art_all[okd]), 0), author_prediction="positive")
dn["rho_FP_D5"] = r4(rho_fp_d5[0])
_, Xn = design(ic=False); dn["FP_without_ch_ic_mean"] = C.summ(C.lpm(Xn[keep], yf[keep], art_all[keep]), 0)
oky = ok_fp; dn["FP_on_y"] = dict(songs=int(oky.sum()), **C.summ(C.lpm(X[oky], yv[oky], art_all[oky]), 0))
ints = np.array([r["y"] > 0 and r["lcov"] is not None and bool(r["first_year"]) for r in rows]) & ok_fp
lc = np.array([r["lcov"] if r["lcov"] is not None else np.nan for r in rows], float)
fy = np.array([float(r["first_year"]) if r["first_year"] else np.nan for r in rows])
zl = np.full(len(rows), np.nan); zl[ints] = C.zs(lc[ints])
_, Xi = design(extra={"first_year": fy})
mi = C.lpm(Xi[ints], zl[ints], art_all[ints])
dn["intensive_margin"] = dict(songs=mi["N"], artists=mi["G"], outcome="z(log(1 + covers)) among y = 100 with covers and first_year", **C.summ(mi, 0))
KT = lambda s: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)
nrm = lambda s: __import__("re").sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
ykt = np.full(len(rows), np.nan)
for i, r in enumerate(rows):
    if not np.isfinite(r["y_foreign"]): continue
    if r["y"] <= 0: ykt[i] = 0.0; continue
    sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"])
    own = [s for s in sets if any(nrm(nm) == a for nm in s)]; O = {nrm(nm) for s in own for nm in s}
    foreign = [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)]
    ykt[i] = 100.0 if [s for s in foreign if not KT(s)] else 0.0
okk = np.isfinite(ykt) & ok_fp
dn["y_foreign_without_karaoke_tribute"] = dict(count1=int((ykt[okk] > 0).sum()), changed_vs_primary=int((ykt[okk] != yf[okk]).sum()),
                                               **C.summ(C.lpm(X[okk], ykt[okk], art_all[okk]), 0))
dn["share_zero_steps"] = dict(all_kept_moves=OUT["measure"]["share_zero_steps"], mean_over_model_songs=r4(np.nanmean([r["zero_share"] for r, k in zip(rows, keep) if k])))
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k, v in dn.items(): print(f"  {k}: {json.dumps(v)}", flush=True)
OUT["reported_deciding_nothing"] = dn
OUT["outcome_joined"] = not FAKE
finish(verdict)
