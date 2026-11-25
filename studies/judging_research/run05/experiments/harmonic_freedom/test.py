"""Run 05, harmonic_freedom (idea I2, revised): within an artist's own songs, does a tune with more harmonic freedom (more plain
diatonic triads fit its melody as well as the written chord does) go with a higher chance that another artist released it (y_foreign)?

The rule is PREDICTION.md in this folder, frozen and pushed in commit 1f6c36d (branch judging-research) before any outcome was joined.
  Prediction: beta(I2) on y_foreign = +0.6 pp per SD, within artist, holding pcs_span, ch_rep, ch_ic_mean and run 04's controls.
  Pass: beta > 0, p < .05/7 (= .00714, two-sided), beta > 0 in both artist halves, conditional logit > 0 and converged.
  Kill: beta < +0.2. Opposite sign (beta < 0, p < .00714): killed, reported as a new hypothesis. Unsettled: anything else.
Order, as the rule says: unit values; rows, I2 and pcs_span from the notes; GATE (stop if it fails, no outcome joined); notes-side
power; only then common.load_outcomes(); counts; clustered SE and power; beta, halves, conditional logit, verdict; reported items.
Single process (no workers). FAKE_Y=<dir> runs the code on a random fake outcome (no outcome file read) and writes there instead.

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
python3 test.py -> result.json in this folder
"""
import json, os, sys, time, collections
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

FAKE = os.environ.get("FAKE_Y")
OUTDIR = FAKE if FAKE else HERE
ALPHA = 0.05 / 7; ZC = 2.690
PRED, KILL = 0.6, 0.2
OUT = dict(rule="PREDICTION.md in this folder, commit 1f6c36d (branch judging-research)", fake_outcome=bool(FAKE),
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           prediction_pp_per_sd=PRED, kill_below=KILL, threshold_p=ALPHA)
r4 = C.r4
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(OUTDIR, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", json.dumps(verdict), flush=True)


# ---------------------------------------------------------------- the measure (frozen in PREDICTION.md)
SKIP = collections.Counter()   # span accounting, filled when STATS is on
def scale_pcs(a, beat):
    ks = a.get("keys") or []
    if not ks: return None
    cur = ks[0]
    for k in ks:
        if k["beat"] <= beat: cur = k
    t = cur["tonic_pitch_class"] % 12; pcs = [t]; acc = t
    for iv in cur.get("scale_degree_intervals") or []:
        acc += iv; pcs.append(acc % 12)
    return pcs

def spans(a, cnt=None):
    """kept spans as (W, log2 n, distinct melody pcs). cnt (Counter) records why spans were skipped."""
    mel = [(n["onset"], n["offset"], n["pitch_class"] % 12) for n in (a.get("melody") or [])
           if n.get("pitch_class") is not None and n["offset"] > n["onset"]]
    out = []
    for h in a.get("harmony") or []:
        if cnt is not None: cnt["spans"] += 1
        on, off = h["onset"], h["offset"]; w = {}
        for (s, e, pc) in mel:
            ov = min(e, off) - max(s, on)
            if ov > 0: w[pc] = w.get(pc, 0.0) + ov
        W = sum(w.values())
        if W < 0.5:
            if cnt is not None: cnt["skip_W_below_half_beat"] += 1
            continue
        sc = scale_pcs(a, on)
        if sc is None or len(sc) != 7:
            if cnt is not None:
                cnt["skip_no_7pc_scale"] += 1
                if sc is not None and len(set(sc)) == 7: cnt["diag_7_distinct_but_not_7_entries"] += 1
            continue
        if cnt is not None and len(set(sc)) != 7: cnt["diag_7_entries_but_repeated_pcs"] += 1
        tri = [frozenset({sc[i], sc[(i + 2) % 7], sc[(i + 4) % 7]}) for i in range(7)]
        ch = frozenset(C.chord_pcs(h))
        if ch not in tri:
            if cnt is not None: cnt["skip_not_diatonic_triad"] += 1
            continue
        fit = lambda S: sum(v for p, v in w.items() if p in S) / W
        f0 = fit(ch) - 1e-9
        n = sum(1 for T in tri if fit(T) >= f0)
        out.append((W, float(np.log2(n)), len(w)))
        if cnt is not None: cnt["kept"] += 1
    return out

def wmean(s, j):
    if not s: return np.nan
    W = np.array([x[0] for x in s]); return float((W * np.array([x[j] for x in s])).sum() / W.sum())

# ---------------------------------------------------------------- 1. unit values (must reproduce)
KC = [dict(beat=0, tonic_pitch_class=0, scale_degree_intervals=[2, 2, 1, 2, 2, 2])]
CH = [dict(onset=0, offset=1, root_pitch_class=0, root_position_intervals=[4, 3])]
u1 = dict(keys=KC, harmony=CH, melody=[dict(onset=0, offset=1, pitch_class=0, octave=0)])
u2 = dict(keys=KC, harmony=CH, melody=[dict(onset=i / 3, offset=(i + 1) / 3, pitch_class=p, octave=0) for i, p in enumerate((0, 4, 7))])
uv = dict(c_over_C=wmean(spans(u1), 1), ceg_over_C=wmean(spans(u2), 1), ceg_pcs_span=wmean(spans(u2), 2))
print(f"UNIT VALUES: one beat of C over C -> {uv['c_over_C']:.3f} [1.585]; C-E-G over C in one beat -> {uv['ceg_over_C']:.3f} [0.000], "
      f"pcs_span {uv['ceg_pcs_span']:.0f} [3]", flush=True)
assert abs(uv["c_over_C"] - 1.585) < 5e-4 and abs(uv["ceg_over_C"]) < 1e-9 and uv["ceg_pcs_span"] == 3
OUT["unit_values"] = {k: r4(v) for k, v in uv.items()}

# ---------------------------------------------------------------- 2. rows, I2 and pcs_span
D = C.load_rows(); rows = D["rows"]; n = len(rows)
R = C.raw_clips()
CACHE = {}; HALFCNT = {0: collections.Counter(), 1: collections.Counter()}
for r in rows:
    for c in r["clips"]:
        a = R.get(c["k"])
        if a is not None and c["k"] not in CACHE: CACHE[c["k"]] = spans(a, HALFCNT[r["half"]])
sp_ = lambda a, c: CACHE.get(c["k"], [])
s3 = lambda a, c: [x for x in CACHE.get(c["k"], []) if x[2] >= 3]
miss = C.song_measure(rows, lambda a, c: wmean(sp_(a, c), 1), "I2")
C.song_measure(rows, lambda a, c: wmean(sp_(a, c), 2), "pcs_span")
C.song_measure(rows, lambda a, c: wmean(s3(a, c), 1), "I2_3")
C.song_measure(rows, lambda a, c: wmean(s3(a, c), 2), "pcs_span_3")
I2 = np.array([r["I2"] for r in rows]); PS = np.array([r["pcs_span"] for r in rows])
hasv = np.isfinite(I2) & np.isfinite(PS)
q = np.percentile(I2[hasv], [10, 50, 90])
print(f"I2: {int(hasv.sum())} songs with a value [9,049]; 10/50/90th pct {q[0]:.2f} / {q[1]:.2f} / {q[2]:.2f} [0.81 / 1.49 / 2.02]; "
      f"clips missing from the raw file {miss}", flush=True)
tot = HALFCNT[0] + HALFCNT[1]
kept_share = {h: r4(HALFCNT[h]["kept"] / HALFCNT[h]["spans"]) for h in (0, 1)}
print(f"spans: {dict(tot)}; share kept per half {kept_share}", flush=True)
OUT["measure"] = dict(songs_with_value=int(hasv.sum()), pct_10_50_90=[r4(x) for x in q], clips_missing=miss,
                      span_accounting=dict(tot), span_accounting_per_half={h: dict(HALFCNT[h]) for h in (0, 1)})

# ---------------------------------------------------------------- 3. GATE (no outcome loaded)
G = C.gate(rows, "I2", extra={"pcs_span": list(PS)})
print(f"GATE: clip-to-clip {G['clip_to_clip']} on {G['clip_pairs']} pairs [0.267 on 3,796] (needs >= 0.20); largest overlap "
      f"{G['overlap_largest']} [pcs_span -0.343] (needs |rho| <= 0.7); ch_rep {G['overlap_all']['ch_rep']} [+0.203], "
      f"mel_ic_mean {G['overlap_all']['mel_ic_mean']} [-0.255] -> {'PASSED' if G['passed'] else 'FAILED'}", flush=True)
OUT["gate"] = G
if not G["passed"]:
    finish("stopped (gate failed; no outcome joined)"); sys.exit(0)

# columns
NAMES_C, XC = C.controls(rows)
art = np.array([r["artist"] for r in rows]); HV = np.array([r["half"] for r in rows])
zI2 = np.full(n, np.nan); zPS = np.full(n, np.nan)
zI2[hasv] = C.zs(I2[hasv]); zPS[hasv] = C.zs(PS[hasv])      # over songs with a value, population SD
zREP = C.zs([r["ch_rep"] for r in rows]); zIC = C.zs([r["ch_ic_mean"] for r in rows])   # over the 9,588 rows
def design(meas=None, ps=None, with_ps=True, extra=None):
    cols = {"z_I2": zI2 if meas is None else meas}
    if with_ps: cols["z_pcs_span"] = zPS if ps is None else ps
    cols.update(z_ch_rep=zREP, z_ch_ic_mean=zIC)
    if extra: cols.update(extra)
    for j, nm in enumerate(NAMES_C): cols[nm] = XC[:, j]
    return list(cols), np.column_stack(list(cols.values()))
NAMES, X = design()
print(f"columns ({len(NAMES)}): {NAMES}", flush=True)

# ---------------------------------------------------------------- 4. notes-side power
def demean(M, gv):
    codes = {a: i for i, a in enumerate(sorted(set(gv)))}; gg = np.array([codes[a] for a in gv]); c_ = np.bincount(gg)
    M2 = np.asarray(M, float).reshape(len(M), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2)
    return M2 - (s / c_[:, None])[gg]
Xd = demean(X[hasv], art[hasv]); o = Xd[:, 1:]; xt = Xd[:, 0] - o @ np.linalg.lstsq(o, Xd[:, 0], rcond=None)[0]
se_nb = np.sqrt(0.22 * 0.78) * 100 / np.sqrt(xt @ xt)
print(f"NOTES-SIDE POWER: residual share {xt @ xt / hasv.sum():.3f} [0.601], SE bound {se_nb:.3f} pp [0.56]; power at +0.6, p < .00714 "
      f"{C.power(PRED, se_nb, ALPHA):.3f} [0.05]; at p < .05 {C.power(PRED, se_nb, 0.05):.3f} [0.19]", flush=True)
OUT["notes_side_power"] = dict(residual_share=r4(xt @ xt / hasv.sum()), se_bound_pp=r4(se_nb),
                               power_p00714=r4(C.power(PRED, se_nb, ALPHA)), power_p05=r4(C.power(PRED, se_nb, 0.05)))

# ---------------------------------------------------------------- 5. outcome
if FAKE:   # code check: random outcomes, no outcome file read
    rs = np.random.default_rng(1)
    for r in rows:
        r["y"] = 100.0 if rs.random() < 0.23 else 0.0
        r["y_foreign"] = (np.nan if rs.random() < 0.05 else (100.0 if rs.random() < 0.6 else 0.0)) if r["y"] else 0.0
        r["lcov"] = float(rs.exponential()) if r["y"] else None; r["first_year"] = int(rs.integers(1960, 2020)) if r["y"] else None
        r["versions"] = None
    OS = dict(fake=True)
else:
    OS = C.load_outcomes(rows, HERE)
OUT["outcome_files"] = OS
yF = np.array([r["y_foreign"] for r in rows], float); y = np.array([r["y"] for r in rows], float)
S = hasv & np.isfinite(yF)

# ---------------------------------------------------------------- 6. counts
nS, gS = int(S.sum()), len(set(art[S]))
print(f"\nCOUNTS: rows {n}; with I2 and pcs_span {int(hasv.sum())}; y_foreign NaN among them {int((hasv & ~np.isfinite(yF)).sum())}; "
      f"model N {nS}, artists {gS}, y_foreign = 1 {int((yF[S] > 0).sum())} ({(yF[S] > 0).mean():.4f}); "
      f"load_outcomes: {json.dumps(OS)}", flush=True)
OUT["counts"] = dict(rows=n, with_value=int(hasv.sum()), y_foreign_nan_among_with_value=int((hasv & ~np.isfinite(yF)).sum()),
                     N=nS, artists=gS, y_foreign1=int((yF[S] > 0).sum()), share_y_foreign1=r4((yF[S] > 0).mean()))

# ---------------------------------------------------------------- 7. clustered SE and power (before beta)
M = C.lpm(X[S], yF[S], art[S]); se = float(M["se"][0])
pw = dict(se=r4(se), power_p00714=r4(C.power(PRED, se, ALPHA)), power_p05=r4(C.power(PRED, se, 0.05)))
print(f"POWER: clustered SE {se:.4f} pp [notes bound {se_nb:.3f}]; power at +0.6, p < .00714 {pw['power_p00714']:.3f}; at p < .05 {pw['power_p05']:.3f}", flush=True)
OUT["power"] = pw
try:
    import statsmodels.api as sm
    Xw, yw = demean(X[S], art[S]), demean(yF[S], art[S]).ravel()
    gg = np.unique(art[S], return_inverse=True)[1]
    keepc = np.where(np.abs(Xw).sum(0) > 1e-12)[0]
    smf = sm.OLS(yw, Xw[:, keepc]).fit(cov_type="cluster", cov_kwds={"groups": gg, "df_correction": True})
    OUT["statsmodels_crosscheck_lpm"] = dict(beta_diff=float(abs(smf.params[0] - M["b"][0])), se_diff=float(abs(smf.bse[0] - M["se"][0])))
except Exception as e:
    OUT["statsmodels_crosscheck_lpm"] = dict(error=repr(e))
print(f"  (CR1 vs statsmodels cluster SE for I2: {OUT['statsmodels_crosscheck_lpm']})", flush=True)

# ---------------------------------------------------------------- 8. beta, halves, conditional logit, verdict
b, p = float(M["b"][0]), float(M["p"][0])
OUT["primary"] = dict(**C.summ(M, 0), N=M["N"], artists=M["G"], K=M["K"],
                      other_columns={nm: C.summ(M, j) for j, nm in enumerate(NAMES[:4])})
print(f"PRIMARY LPM I2: beta {b:+.4f} pp per SD (predicted +0.6, kill below +0.2), SE {se:.4f}, p {p:.4g}, "
      f"95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f}; N {M['N']}, artists {M['G']}, K {M['K']}", flush=True)
print("  other columns: " + "; ".join(f"{nm} {M['b'][j]:+.3f} (SE {M['se'][j]:.3f})" for j, nm in enumerate(NAMES[1:4], 1)), flush=True)
HM = {}; OUT["halves"] = []
for h in (0, 1):
    s = S & (HV == h); HM[h] = C.lpm(X[s], yF[s], art[s])
    d = dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"], y_foreign1=int((yF[s] > 0).sum()), **C.summ(HM[h], 0))
    OUT["halves"].append(d)
    print(f"HALF {h}: {d['songs']} songs, {d['artists']} artists, y_foreign=1 {d['y_foreign1']}; beta {d['beta']:+.4f} (SE {d['se']:.4f}, p {d['p']:.3g})", flush=True)

yb = (yF[S] > 0).astype(float)
params, bse, pv, conv, ks, kg = C.cond_logit(X[S], yb, list(art[S]))
cl = dict(coef=r4(params[0]), se=r4(bse[0]), p=float(f"{pv[0]:.4g}"), converged=conv, kept_songs=ks, kept_artists=kg,
          dropped_songs=nS - ks, dropped_artists=gS - kg, convergence_test="max|score|/nobs < 1e-5 (BFGS, then Newton)")
OUT["conditional_logit"] = cl
print(f"CONDITIONAL LOGIT: drops {cl['dropped_artists']} artists and {cl['dropped_songs']} songs (all 0 or all 1); keeps {kg} artists, {ks} songs; "
      f"I2 coef {params[0]:+.4f} log-odds per SD (SE {bse[0]:.4f}, p {pv[0]:.4g}); converged {conv}", flush=True)
nonfinite = [nm for nm, v, s_ in zip(NAMES, params, bse) if not (np.isfinite(v) and np.isfinite(s_)) or abs(v) > 10]
if nonfinite: print(f"  columns with non-finite or large (>10) coefficients: {nonfinite}", flush=True)
cl["columns_nonfinite_or_large"] = nonfinite

hb = [HM[h]["b"][0] for h in (0, 1)]
if b > 0 and p < ALPHA and hb[0] > 0 and hb[1] > 0 and conv and params[0] > 0: verdict = "pass"
elif b < 0 and p < ALPHA: verdict = "killed (opposite sign: beta < 0, p < .00714); reported as a new hypothesis, not a pass"
elif b < KILL: verdict = "kill (beta < +0.2 pp)"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00714")
    if not (hb[0] > 0 and hb[1] > 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not params[0] > 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
h3 = np.array([np.isfinite(r["I2_3"]) and np.isfinite(r["pcs_span_3"]) for r in rows])
z3 = np.full(n, np.nan); p3 = np.full(n, np.nan)
z3[h3] = C.zs(np.array([r["I2_3"] for r in rows])[h3]); p3[h3] = C.zs(np.array([r["pcs_span_3"] for r in rows])[h3])
g3 = C.gate(rows, "I2_3")
S3 = h3 & np.isfinite(yF); _, X3 = design(meas=z3, ps=p3); m = C.lpm(X3[S3], yF[S3], art[S3])
dn["spans_with_3plus_pcs_only"] = dict(songs_with_value=int(h3.sum()), clip_to_clip=g3["clip_to_clip"], clip_pairs=g3["clip_pairs"],
                                      N=m["N"], artists=m["G"], **C.summ(m, 0))
_, Xn = design(with_ps=False); m = C.lpm(Xn[S], yF[S], art[S]); dn["without_pcs_span"] = dict(N=m["N"], **C.summ(m, 0))
Sy = hasv & np.isfinite(y); m = C.lpm(X[Sy], y[Sy], art[Sy]); dn["on_y_in_discogs_vi"] = dict(N=m["N"], artists=m["G"], y1=int((y[Sy] > 0).sum()), **C.summ(m, 0))
lc = np.array([np.nan if r["lcov"] is None else r["lcov"] for r in rows], float)
fy = np.array([np.nan if r["first_year"] is None else float(r["first_year"]) for r in rows], float)
Si = hasv & (y > 0) & np.isfinite(lc) & np.isfinite(fy)
if Si.sum() > 50:
    zl = np.full(n, np.nan); zl[Si] = C.zs(lc[Si])
    _, Xi = design(extra={"first_year": fy}); m = C.lpm(Xi[Si], zl[Si], art[Si])
    dn["intensive_margin_sd_per_sd"] = dict(N=m["N"], artists=m["G"], **C.summ(m, 0))
def foreign_no_kt(r):
    if not r["y"]: return 0.0
    if not np.isfinite(r["y_foreign"]) or r["versions"] is None: return np.nan
    nrm = lambda s: __import__("re").sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
    sets = [e[0] for e in r["versions"]]
    sets = [s for s in sets if not any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)]
    a = nrm(r["artist"]); own = [s for s in sets if any(nrm(nm) == a for nm in s)]
    if not own: return np.nan
    O = {nrm(nm) for s in own for nm in s}
    return 100.0 if [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)] else 0.0
if not FAKE:
    yk = np.array([foreign_no_kt(r) for r in rows], float); Sk = hasv & np.isfinite(yk)
    m = C.lpm(X[Sk], yk[Sk], art[Sk])
    dn["y_foreign_without_karaoke_tribute"] = dict(N=m["N"], artists=m["G"], y1=int((yk[Sk] > 0).sum()),
                                                  changed_from_1_to_0=int(((yF > 0) & (yk == 0) & hasv).sum()),
                                                  newly_nan=int((np.isfinite(yF) & ~np.isfinite(yk) & hasv).sum()), **C.summ(m, 0))
dn["share_of_spans_kept_per_half"] = kept_share
dn["songs_artists_per_half"] = [dict(half=h, songs=HM[h]["N"], artists=HM[h]["G"]) for h in (0, 1)]
OUT["reported_deciding_nothing"] = dn
print("\nREPORTED, DECIDING NOTHING:", flush=True)
for k, v in dn.items(): print(f"  {k}: {json.dumps(v)}", flush=True)
print(f"\nVERDICT (rule written first): {verdict}", flush=True)
finish(verdict)
