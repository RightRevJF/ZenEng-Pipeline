"""Run 05, tonic_resistance: is home the electrical hub of the chord graph (tonic resistance H, backlog R03-I2), and within an
artist's own songs are songs with a central home (low H) more often taken up by another artist (y_foreign)?

The rule is PREDICTION.md in this folder (frozen and pushed in commit 1f6c36d on branch judging-research before any outcome was
joined). The measure was first defined in run 03 (../../../run03/experiments/tonic_resistance/PREDICTION.md and test.py); where they
differ, tonight's PREDICTION.md governs. Shared code: ../common.py (rows, controls, raw notes, outcomes, LPM, conditional logit).

Order (printed as it goes):
  1. unit tests for H (must reproduce exactly);
  2. rows (run 04's 9,588 songs), tokens, H, distinct chords, links from the raw notes;
  3. the measure-side GATE (residualised clip-to-clip >= 0.20; overlap <= 0.7; R2 on the size block <= 0.8), no outcome loaded.
     If it fails: result.json and verdict "stopped", no outcome joined;
  4. notes-side power;
  5. common.load_outcomes (refuses unless PREDICTION.md is committed);
  6. counts; 7. clustered SE and power; 8. beta, halves, conditional logit, verdict; 9. reported items; 10. result.json.
`python3 test.py --fake` runs every model on a random fake outcome without reading any outcome file and writes nothing.
Runs in one process (BLAS threads pinned to 1).

Credit: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0;
        Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
python3 test.py -> result.json in this folder"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import sys, json, time, collections
import numpy as np
from scipy.sparse.csgraph import connected_components
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C

FAKE = "--fake" in sys.argv
ALPHA = 0.05 / 7; ZC = float(N.isf(ALPHA / 2))   # .00714, two-sided, z 2.690
PRED, KILL = -0.6, -0.2
OUT = dict(rule="PREDICTION.md in this folder, commit 1f6c36d (branch judging-research); measure from run 03's tonic_resistance",
           credit="Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); Discogs-VI 20240701 (CC BY-SA 4.0)",
           threshold_p=ALPHA, threshold_z=round(ZC, 3), prediction_pp_per_sd=PRED, kill_above_pp=KILL)
r4 = C.r4
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    if FAKE: print("FAKE run: nothing written. verdict on fake outcome:", verdict, flush=True); sys.exit(0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- the measure (run 03's code)
def resist(W):
    """effective resistances of a connected weighted graph W (conductances), via numpy.linalg.pinv of the Laplacian"""
    Qd = np.linalg.pinv(np.diag(W.sum(1)) - W); d = np.diag(Qd)
    return d[:, None] + d[None, :] - 2 * Qd

def H_core(Cm, t):
    """H = sum_x pi_x w_xT / sum_x sum_y pi_x pi_y w_xy on a connected Cm; pi = row sums / total; no factor 1/2"""
    om = resist(Cm); pi = Cm.sum(1) / Cm.sum()
    return float(pi @ om[:, t] / (pi @ om @ pi))

def moves(seqs):
    names = sorted(set(t for s in seqs for t in s)); ix = {t: i for i, t in enumerate(names)}; M = np.zeros((len(names), len(names)))
    for s in seqs:
        for a, b in zip(s, s[1:]): M[ix[a], ix[b]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[ix[s[-1]], ix[s[0]]] += 1
    return names, M

def H_of(seqs):
    """(H, chords in T's piece, distinct chords n, links) or (None, reason, n, links). Drops in the rule's order:
    n < 3; no root-0 token; T's piece under 3 chords."""
    names, M = moves(seqs); n = len(names)
    Cm = M + M.T; np.fill_diagonal(Cm, 0); links = int((np.triu(Cm, 1) > 0).sum())
    if n < 3: return None, "under_3_distinct", n, links
    cand = [i for i, t in enumerate(names) if t // 9 == 0]
    if not cand: return None, "no_root0", n, links
    rs = Cm.sum(1); T = min(cand, key=lambda i: (-rs[i], names[i]))   # largest row sum, ties to the smaller token
    _, lab = connected_components(Cm > 0, directed=False); idx = np.nonzero(lab == lab[T])[0]
    if len(idx) < 3: return None, "T_piece_under_3", n, links
    return H_core(Cm[np.ix_(idx, idx)], int(np.nonzero(idx == T)[0][0])), len(idx), n, links

def qual(iv):   # run 03's table (fifths_path/PREDICTION.md); anything else, including none, -> 8
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(tuple(iv or []), 8)

def tokens(a):
    tonic = a["keys"][0]["tonic_pitch_class"] if a.get("keys") else 0; ch = []
    for h in sorted(a.get("harmony") or [], key=lambda h: h["onset"]):
        t = ((h["root_pitch_class"] - tonic) % 12) * 9 + qual(h["root_position_intervals"])
        if not ch or ch[-1] != t: ch.append(t)
    return ch

def A_clip(a):
    """arrow_of_time's A (for the reported rho(H, A) only): chord_pcs, collapse, K >= 6, 1 - sum min(n_ij, n_ji) / sum n_ij"""
    s = []
    for h in sorted(a.get("harmony") or [], key=lambda h: h["onset"]):
        p = C.chord_pcs(h)
        if not s or s[-1] != p: s.append(p)
    K = len(s) - 1
    if K < 6: return None, K
    n = collections.Counter(zip(s, s[1:]))
    return 1 - sum(min(v, n.get((j, i), 0)) for (i, j), v in n.items()) / sum(n.values()), K

# ---------------------------------------------------------------- 1. unit tests (unit weights)
def cyc(n): W = np.zeros((n, n)); [W.__setitem__((i, (i + 1) % n), 1) for i in range(n)]; return W + W.T
star = np.zeros((4, 4)); star[0, 1:] = 1; star = star + star.T
unit = {}
for name, W, t, want in (("5-cycle", cyc(5), 0, 1.0), ("star, T at the hub", star, 0, 0.6), ("star, T on a leaf", star, 1, 1.4)):
    got = H_core(W, t); unit[name] = dict(want=want, got=r4(got), ok=abs(got - want) < 1e-9)
    print(f"unit test H, {name}: want {want}, got {got:.10f}", flush=True)
for name, seqs, want in (("star via tokens [[0,18],[0,27],[0,45]]", [[0, 18], [0, 27], [0, 45]], 0.6),
                         ("star via tokens [[18,0],[18,27],[18,45]]", [[18, 0], [18, 27], [18, 45]], 1.4)):
    got = H_of(seqs)[0]; unit[name] = dict(want=want, got=r4(got), ok=abs(got - want) < 1e-9)
    print(f"unit test H, {name}: want {want}, got {got:.10f}", flush=True)
assert all(u["ok"] for u in unit.values()), "H unit tests failed: the code is wrong"
OUT["unit_tests"] = unit

# ---------------------------------------------------------------- 2. rows, tokens, H
L = C.load_rows(); rows = L["rows"]; R = C.raw_clips()
missing = sum(1 for r in rows for c in r["clips"] if c["k"] not in R)
print(f"raw clips missing for the rows' clips: {missing}", flush=True)
drop = collections.Counter()
for r in rows:
    seqs = [tokens(R[c["k"]]) if c["k"] in R else [] for c in r["clips"]]
    H, tp, nd, links = H_of(seqs)
    r.update(seqs=seqs, nd=nd, links=links, H=(np.nan if H is None else H), tpiece=(tp if H is not None else None))
    if H is None: drop[tp] += 1
    aa = [A_clip(R[c["k"]]) for c in r["clips"] if c["k"] in R]; aa = [(v, k) for v, k in aa if v is not None]
    r["A"] = float(np.average([v for v, _ in aa], weights=[k for _, k in aa])) if aa else np.nan
songs = [r for r in rows if np.isfinite(r["H"])]
hv = np.array([r["H"] for r in songs])
print(f"H defined: {len(songs)} of {len(rows)} songs [chair 9,009]; dropped: under 3 distinct chords {drop['under_3_distinct']} [278], "
      f"no root-0 chord {drop['no_root0']} [266], T's piece under 3 chords {drop['T_piece_under_3']} [35]", flush=True)
pct = np.percentile(hv, (10, 50, 90))
print(f"H: 10th / 50th / 90th {pct[0]:.3f} / {pct[1]:.3f} / {pct[2]:.3f} [0.624 / 0.818 / 1.143]; share H < 1 {np.mean(hv < 1):.3f}; "
      f"T piece not the whole graph: {sum(r['tpiece'] < r['nd'] for r in songs)}", flush=True)
OUT["counts_notes"] = dict(rows=len(rows), artists=len(set(r["artist"] for r in rows)), raw_clips_missing=missing, H_defined=len(songs),
                           dropped_under_3_distinct=drop["under_3_distinct"], dropped_no_root0=drop["no_root0"], dropped_T_piece_under_3=drop["T_piece_under_3"],
                           T_piece_not_whole_graph=sum(r["tpiece"] < r["nd"] for r in songs),
                           chair=dict(H_defined=9009, under_3=278, no_root0=266, T_piece_under_3=35))
OUT["H_shape"] = dict(p10_p50_p90=[r4(x) for x in pct], chair=[0.624, 0.818, 1.143], share_below_1=r4(np.mean(hv < 1)))

# ---------------------------------------------------------------- 3. GATE (notes only; no outcome loaded)
def dums(nd): nd = np.asarray(nd); return [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)]
def ols_resid(y, X): return y - X @ np.linalg.lstsq(X, y, rcond=None)[0]

# 3.1 clip-to-clip, residualised
pairs = []
for r in songs:
    if r["nclips"] < 2: continue
    a, b = H_of([r["seqs"][0]]), H_of([r["seqs"][1]])
    if a[0] is None or b[0] is None: continue
    pairs.append((a, b))
P = len(pairs)
hs = np.array([a[0] for a, _ in pairs] + [b[0] for _, b in pairs])
ndc = [a[2] for a, _ in pairs] + [b[2] for _, b in pairs]; lkc = [a[3] for a, _ in pairs] + [b[3] for _, b in pairs]
Xc = np.column_stack([np.ones(2 * P)] + dums(ndc) + [np.asarray(lkc, float)])
res = ols_resid(hs, Xc)
rho_cc = float(spearmanr(res[:P], res[P:])[0]); rho_cc_raw = float(spearmanr(hs[:P], hs[P:])[0])
g1 = rho_cc >= 0.20
print(f"GATE 1, clip-to-clip (residualised): Spearman {rho_cc:.4f} on {P} pairs (needs >= 0.20) [chair 0.203, 3,512 pairs]; raw {rho_cc_raw:.4f} [0.259]"
      f" -> {'pass' if g1 else 'FAIL'}", flush=True)

# 3.2 overlap
Xs = np.column_stack([np.ones(len(songs))] + dums([r["nd"] for r in songs]) + [np.array([r["links"] for r in songs], float), np.log([r["nclips"] for r in songs])])
Hres = ols_resid(hv, Xs); R2 = float(1 - (Hres ** 2).sum() / ((hv - hv.mean()) ** 2).sum())
cands = {f: [r[f] for r in songs] for f in C.FE}
cands.update(n_ch=[r["n_ch"] for r in songs], beats=[r["beats"] for r in songs], clips_per_song=[r["nclips"] for r in songs],
             distinct_chords=[r["nd"] for r in songs], links=[r["links"] for r in songs])
cor = {k: C.sp(Hres, v) for k, v in cands.items()}
top = max(cor, key=lambda k: abs(cor[k][0]))
g2 = abs(cor[top][0]) <= 0.7 and R2 <= 0.8
print("GATE 2, Spearman of H_res with:", json.dumps({k: r4(v[0]) for k, v in cor.items()}), flush=True)
print(f"  largest |rho|: {top} {cor[top][0]:+.4f} (needs <= 0.7) [chair beats 0.081]; R2 of H on the size block {R2:.4f} (needs <= 0.8) [0.156]"
      f" -> {'pass' if g2 else 'FAIL'}", flush=True)
rho_raw_nd = float(spearmanr(hv, [r["nd"] for r in songs])[0])
print(f"  deciding nothing: raw rho(H, distinct chords) {rho_raw_nd:+.4f} [chair -0.49]", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(rho_residualised=r4(rho_cc), rho_unrounded=rho_cc, pairs=P, threshold=0.20, passed=bool(g1),
                                     raw_rho=r4(rho_cc_raw), chair=0.203, chair_pairs=3512, chair_raw=0.259),
                   overlap=dict(spearman_H_res={k: r4(v[0]) for k, v in cor.items()}, n_per_measure={k: v[1] for k, v in cor.items()},
                                largest_abs=[top, r4(cor[top][0])], r2_size_block=r4(R2), passed=bool(g2), chair_largest=["beats", 0.081], chair_r2=0.156),
                   raw_rho_H_distinct_chords=r4(rho_raw_nd), passed=bool(g1 and g2))
print(f"GATE: {'PASSED' if g1 and g2 else 'FAILED'}", flush=True)
if not (g1 and g2):
    finish("stopped (gate failed" + (": clip-to-clip" if not g1 else "") + (": overlap" if not g2 else "") + "; no outcome joined)")

# ---------------------------------------------------------------- columns
zr = {f: C.zs([r[f] for r in rows]) for f in ("ch_rep", "ch_ic_mean")}   # over the 9,588 rows
for i, r in enumerate(rows): r["z_ch_rep"], r["z_ch_ic_mean"] = zr["ch_rep"][i], zr["ch_ic_mean"][i]
zH = C.zs(hv)                                                                    # over the songs with H (population SD)
for i, r in enumerate(songs): r["zH"] = zH[i]
cn_all, cm_all = C.controls(rows); cidx = {id(r): i for i, r in enumerate(rows)}

def design(R, with_ic=True, extra=None):
    """columns: z(H), z(ch_rep), [z(ch_ic_mean)], distinct-chord dummies 4..11 and 12+, links, run 04's control block, [extra]"""
    names = ["zH", "z_ch_rep"] + (["z_ch_ic_mean"] if with_ic else []) + [f"nd{k}" for k in range(4, 12)] + ["nd12p", "links"] + cn_all
    cols = [np.array([r[f] for r in R], float) for f in names[:2 + with_ic]] + dums([r["nd"] for r in R]) + [np.array([r["links"] for r in R], float)]
    X = np.column_stack(cols + [cm_all[[cidx[id(r)] for r in R]]])
    if extra is not None: names = names + [extra[0]]; X = np.column_stack([X, extra[1]])
    return names, X

# ---------------------------------------------------------------- 4. notes-side power (no outcome)
def demean(M, g):
    codes = {a: i for i, a in enumerate(sorted(set(g)))}; gg = np.array([codes[a] for a in g]); c_ = np.bincount(gg)
    M2 = np.asarray(M, float).reshape(len(M), -1); s = np.zeros((len(codes), M2.shape[1])); np.add.at(s, gg, M2); return M2 - (s / c_[:, None])[gg]
names0, X0 = design(songs); Xw = demean(X0, [r["artist"] for r in songs])
xt = ols_resid(Xw[:, 0], Xw[:, 1:]); ssx = float((xt ** 2).sum())
se_bound = float(np.sqrt(0.22 * 0.78) * 100 / np.sqrt(ssx))
print(f"NOTES-SIDE POWER: residual share of z(H) {ssx / len(songs):.3f} on {len(songs)} songs [chair 0.652]; SE bound {se_bound:.3f} pp [0.54]; "
      f"power at {PRED} and p < .00714: {C.power(PRED, se_bound, ALPHA):.3f} [0.06]; at p < .05: {C.power(PRED, se_bound, 0.05):.3f} [0.20]", flush=True)
OUT["notes_side_power"] = dict(residual_share=r4(ssx / len(songs)), songs=len(songs), se_bound_pp=r4(se_bound),
                               power_at_alpha=r4(C.power(PRED, se_bound, ALPHA)), power_at_05=r4(C.power(PRED, se_bound, 0.05)),
                               chair=dict(residual_share=0.652, se=0.54, power=0.06, power05=0.20))

# ---------------------------------------------------------------- 5. outcome
KT = lambda s: any(("karaoke" in nm.lower()) or ("tribute" in nm.lower()) for nm in s)
if FAKE:
    rs_ = np.random.default_rng(0)
    for r in rows:
        r["y"] = 100.0 * (rs_.random() < 0.23); r["y_foreign"] = (100.0 * (rs_.random() < 0.6) if r["y"] else 0.0)
        if r["y"] and rs_.random() < 0.01: r["y_foreign"] = np.nan
        r["lcov"] = float(np.log1p(rs_.integers(1, 20))) if r["y"] else None; r["first_year"] = int(rs_.integers(1960, 2020)) if r["y"] else None
        r["versions"] = [[["Some Band"], 2000, [1]]] if r["y_foreign"] == 100 else None
    osum = dict(fake=True)
else:
    osum = C.load_outcomes(rows, HERE)
    print(f"OUTCOME joined: md5 {osum['md5']}; y = 100: {osum['y1']}; y_foreign = 100: {osum['y_foreign1']}; dropped (NaN): {osum['drops']}", flush=True)
OUT["outcome_files"] = osum
nrm = lambda s: __import__("re").sub(r"[^a-z0-9]", "", s.lower().replace("&", "and"))
for r in rows:   # y_foreign with karaoke / tribute performer sets removed (reported only), run 04's rule
    r["y_kt"] = r["y_foreign"]
    if r.get("versions") and np.isfinite(r["y_foreign"]) and not FAKE:
        sets = [e[0] for e in r["versions"]]; a = nrm(r["artist"]); own = [s for s in sets if any(nrm(nm) == a for nm in s)]
        O = {nrm(nm) for s in own for nm in s}
        foreign = [s for s in sets if len(s) > 0 and not any(nrm(nm) in O for nm in s)]
        r["y_kt"] = 100.0 if [s for s in foreign if not KT(s)] else 0.0

# ---------------------------------------------------------------- 6. counts
S = [r for r in songs if np.isfinite(r["y_foreign"])]
art = [r["artist"] for r in S]; yf = np.array([r["y_foreign"] for r in S])
nan_drop = len(songs) - len(S)
print(f"COUNTS: {len(S)} songs, {len(set(art))} artists; y_foreign = 100: {int((yf > 0).sum())} ({yf.mean():.2f}%); "
      f"songs with H dropped for y_foreign NaN: {nan_drop}", flush=True)
OUT["counts"] = dict(songs=len(S), artists=len(set(art)), y_foreign_1=int((yf > 0).sum()), y_foreign_rate_pct=r4(yf.mean()), dropped_y_foreign_nan=nan_drop)

# ---------------------------------------------------------------- 7. SE and power, then 8. beta
names, X = design(S)
M = C.lpm(X, yf, art); se = float(M["se"][0])
pw, pw05 = C.power(PRED, se, ALPHA), C.power(PRED, se, 0.05)
kill_if_true = float(N.sf((KILL - PRED) / se)); kill_if_zero = float(N.sf(KILL / se))
print(f"PRIMARY LPM: N {M['N']}, artists {M['G']}, columns {M['K']}; clustered SE of beta(H) {se:.4f} pp; power at {PRED} and p < .00714: {pw:.3f}; "
      f"at p < .05: {pw05:.3f}; kill fires {kill_if_true:.0%} if {PRED} is true, {kill_if_zero:.0%} if 0", flush=True)
b, p = float(M["b"][0]), float(M["p"][0])
print(f"beta(H) = {b:+.4f} pp per SD, SE {se:.4f}, p = {p:.5f}, 95% range {b - 1.96 * se:+.4f} to {b + 1.96 * se:+.4f} (predicted {PRED})", flush=True)
print("  other columns: " + ", ".join(f"{names[i]} {M['b'][i]:+.3f} ({M['se'][i]:.3f})" for i in (1, 2)), flush=True)
OUT["primary"] = dict(N=M["N"], artists=M["G"], K=M["K"], **C.summ(M, 0), power_at_alpha=r4(pw), power_at_05=r4(pw05),
                      kill_fires_if_prediction_true=r4(kill_if_true), kill_fires_if_zero=r4(kill_if_zero),
                      z_ch_rep=C.summ(M, 1), z_ch_ic_mean=C.summ(M, 2), columns=names)
hb = []; OUT["halves"] = []
for h in (0, 1):
    idx = [i for i, r in enumerate(S) if r["half"] == h]
    Mh = C.lpm(X[idx], yf[idx], [art[i] for i in idx]); hb.append(float(Mh["b"][0]))
    print(f"  half {h}: {Mh['N']} songs, {Mh['G']} artists; beta {Mh['b'][0]:+.4f} (SE {Mh['se'][0]:.4f}, p {Mh['p'][0]:.4f})", flush=True)
    OUT["halves"].append(dict(half=h, songs=Mh["N"], artists=Mh["G"], **C.summ(Mh, 0)))
pr_, bse_, pv_, conv, ks, kg = C.cond_logit(X, yf / 100, art)
cb = float(pr_[0])
print(f"  conditional logit: keeps {ks} songs in {kg} artists (drops {len(S) - ks} songs, {len(set(art)) - kg} artists with all-0 or all-1); "
      f"beta(H) {cb:+.4f} log-odds per SD (SE {bse_[0]:.4f}, p {pv_[0]:.4f}); converged: {conv}", flush=True)
bad = [names[i] for i in range(len(names)) if not np.isfinite(bse_[i]) or abs(pr_[i]) > 10]
if bad: print(f"  conditional logit columns with no finite / huge estimate (nuisance): {bad}", flush=True)
OUT["conditional_logit"] = dict(beta=r4(cb), se=r4(bse_[0]), p=float(f"{pv_[0]:.4g}"), converged=conv, songs_kept=ks, artists_kept=kg,
                                songs_dropped=len(S) - ks, artists_dropped=len(set(art)) - kg, nuisance_columns_unstable=bad)

if b > 0 and p < ALPHA: verdict = "kill (opposite sign, p < .00714: reported as a new hypothesis, not a pass)"
elif b < 0 and p < ALPHA and hb[0] < 0 and hb[1] < 0 and conv and cb < 0: verdict = "pass"
elif b > KILL: verdict = "kill"
else:
    why = []
    if not p < ALPHA: why.append("p >= .00714")
    if not (hb[0] < 0 and hb[1] < 0): why.append("halves split")
    if not conv: why.append("conditional logit did not converge")
    elif not cb < 0: why.append("conditional logit sign disagrees")
    verdict = "unsettled (" + "; ".join(why) + ")"
print(f"VERDICT (H on y_foreign): {verdict}", flush=True)

# ---------------------------------------------------------------- 9. reported, deciding nothing
dn = {}
n1, X1 = design(S, with_ic=False); M1 = C.lpm(X1, yf, art); dn["without_z_ch_ic_mean"] = dict(N=M1["N"], **C.summ(M1, 0))
W_ = [i for i, r in enumerate(S) if r["tpiece"] == r["nd"]]
MW = C.lpm(X[W_], yf[W_], [art[i] for i in W_]); dn["T_piece_not_whole_graph_dropped"] = dict(N=MW["N"], artists=MW["G"], **C.summ(MW, 0))
both = [r for r in songs if np.isfinite(r["A"])]
rha = float(spearmanr([r["H"] for r in both], [r["A"] for r in both])[0]); dn["rho_H_A"] = dict(rho=r4(rha), songs=len(both), chair=0.28)
yy = np.array([r["y"] for r in S]); MY = C.lpm(X, yy, art); dn["on_y"] = dict(N=MY["N"], y_1=int((yy > 0).sum()), **C.summ(MY, 0))
I_ = [i for i, r in enumerate(S) if r["y"] > 0 and r["lcov"] is not None and r["first_year"]]
yi = C.zs([S[i]["lcov"] for i in I_]); ni, Xi = design([S[i] for i in I_], extra=("first_year", np.array([S[i]["first_year"] for i in I_], float)))
MI = C.lpm(Xi, yi, [art[i] for i in I_]); dn["intensive_z_log1p_covers"] = dict(N=MI["N"], artists=MI["G"], units="SD per SD", **C.summ(MI, 0))
ykt = np.array([r["y_kt"] for r in S]); MK = C.lpm(X, ykt, art)
dn["y_foreign_without_karaoke_tribute"] = dict(N=MK["N"], y_1=int((ykt > 0).sum()), **C.summ(MK, 0),
                                               songs_with_a_karaoke_or_tribute_set=sum(1 for r in S if r.get("versions") and any(KT(e[0]) for e in r["versions"])),
                                               songs_flipped=int(((yf > 0) != (ykt > 0)).sum()))
dn["per_half_counts"] = [dict(half=h["half"], songs=h["songs"], artists=h["artists"]) for h in OUT["halves"]]
print("REPORTED, DECIDING NOTHING:", flush=True)
for k, v in dn.items(): print(f"  {k}: {json.dumps(v)}", flush=True)
OUT["reported_deciding_nothing"] = dn
finish(verdict)
