"""Run 03, tonic resistance H: is the home chord the electrical hub of the chord graph, and are such songs covered more within artist?
The rule is PREDICTION.md in this folder (frozen and pushed in commit 09ce7bd before this script was written); rows, graph and model
as ../bridge/PREDICTION.md. Code reused from ../bridge/test.py and ../curvature/test.py.

Order (printed as it goes):
  1. unit tests for H (and for p_min, printed deciding nothing);
  2. songs from the notes only (only the key set of hooktheory_covers_discogs.json is read);
  3. the measure-side GATE (clip-to-clip agreement of H_res; overlap of H_res; R2 on the size block), with no outcome loaded.
     If the gate fails: result.json says "stopped", no outcome is joined, the script ends;
  4. only then first_year, covers and discogs_versions_matched.json;
  5. SE and power printed first, then beta; halves; verdict; reported, deciding nothing.
python3 test.py -> result.json in this folder"""
import json, gzip, collections, re, hashlib, os, sys, time
import numpy as np, statsmodels.api as sm
from scipy.sparse.csgraph import connected_components
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/home/claude/jdata"   # a read-only copy of origin/main:studies/judging_data
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF   # the 17 data-pack measures
OUT = dict(rule="PREDICTION.md in this folder, commit 09ce7bd")
r4 = lambda x: round(float(x), 4)
def finish(verdict):
    OUT["verdict"] = verdict; OUT["runtime_s"] = round(time.time() - T0)
    json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item())
    print("VERDICT:", verdict, flush=True); sys.exit(0)

# ---------------------------------------------------------------- the measures
def resist(W):
    """effective resistances of a connected weighted graph W (conductances), via numpy.linalg.pinv of the Laplacian"""
    Qd = np.linalg.pinv(np.diag(W.sum(1)) - W); d = np.diag(Qd)
    return d[:, None] + d[None, :] - 2 * Qd

def H_core(C, t):
    """H = sum_x pi_x w_xT / sum_x sum_y pi_x pi_y w_xy on a connected C; pi = row sums / total; no factor 1/2"""
    om = resist(C); pi = C.sum(1) / C.sum()
    return float(pi @ om[:, t] / (pi @ om @ pi))

def moves(seqs):
    names = sorted(set(t for s in seqs for t in s)); ix = {t: i for i, t in enumerate(names)}; M = np.zeros((len(names), len(names)))
    for s in seqs:
        for a, b in zip(s, s[1:]): M[ix[a], ix[b]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[ix[s[-1]], ix[s[0]]] += 1
    return names, M

def H_of(seqs):
    """returns (H, chords in T's piece, distinct chords, distinct links) or (None, reason, n, links)"""
    names, M = moves(seqs); n = len(names)
    C = M + M.T; np.fill_diagonal(C, 0); links = int((np.triu(C, 1) > 0).sum())
    cand = [i for i, t in enumerate(names) if t // 9 == 0]
    if not cand: return None, "no_T", n, links
    rs = C.sum(1); T = min(cand, key=lambda i: (-rs[i], names[i]))   # largest row sum, ties to the smaller token
    _, lab = connected_components(C > 0, directed=False); idx = np.nonzero(lab == lab[T])[0]
    if len(idx) < 3: return None, "T_piece_under_3", n, links
    return H_core(C[np.ix_(idx, idx)], int(np.nonzero(idx == T)[0][0])), len(idx), n, links

def pmin_of(seqs):
    """the obtuse_statue measure (printed here deciding nothing): unit weights, largest piece, p_i = 1 - 1/2 sum_j A_ij w_ij"""
    names, M = moves(seqs); A = ((M + M.T) > 0).astype(float); np.fill_diagonal(A, 0)
    npc, lab = connected_components(A, directed=False); big = max(range(npc), key=lambda p: ((lab == p).sum(), -p))
    idx = np.nonzero(lab == big)[0]
    if len(idx) < 3: return None
    Ap = A[np.ix_(idx, idx)]; p = 1 - 0.5 * (Ap * resist(Ap)).sum(1); assert abs(p.sum() - 1) < 1e-8
    return float(p.min())

# ---------------------------------------------------------------- 1. unit tests (unit weights)
def cyc(n): W = np.zeros((n, n)); [W.__setitem__((i, (i + 1) % n), 1) for i in range(n)]; return W + W.T
star = np.zeros((4, 4)); star[0, 1:] = 1; star = star + star.T
unit = {}
for name, W, t, want in (("5-cycle", cyc(5), 0, 1.0), ("star (3 leaves), T at the hub", star, 0, 0.6), ("star (3 leaves), T on a leaf", star, 1, 1.4)):
    got = H_core(W, t); unit[name] = dict(want=want, got=r4(got), ok=abs(got - want) < 1e-9)
    print(f"unit test H, {name}: want {want}, got {got:.10f}", flush=True)
# the full path (tokens -> T -> piece -> H) on the same graphs written as clips: tokens 0 (root 0, the hub) and 18, 27, 45 (other roots)
for name, seqs, want in (("star via tokens, T = token 0 at the hub", [[0, 18], [0, 27], [0, 45]], 0.6),
                         ("star via tokens, T = token 0 on a leaf", [[18, 0], [18, 27], [18, 45]], 1.4)):
    got = H_of(seqs)[0]; unit[name] = dict(want=want, got=r4(got), ok=abs(got - want) < 1e-9)
    print(f"unit test H, {name}: want {want}, got {got:.10f}", flush=True)
assert all(u["ok"] for u in unit.values()), "H unit tests failed: the code is wrong"
OUT["unit_tests"] = unit

# ---------------------------------------------------------------- 2. rows from the notes
def qual(iv):   # as in studies/surprise/surprise_hooktheory.py (origin/main)
    iv = tuple(iv)
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(iv, 8)
def chords(clip):
    tonic = clip["keys"][0]["tonic_pitch_class"] if clip.get("keys") else 0; ch = []
    for c in sorted(clip.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((c["root_pitch_class"] - tonic) % 12) * 9 + qual(c["root_position_intervals"])
        if not ch or ch[-1] != t: ch.append(t)
    return ch

CL = json.load(gzip.open(os.path.join(DATA, "hooktheory_clips.json.gz")))["clips"]
S = json.load(gzip.open(os.path.join(DATA, "hooktheory_surprise.json.gz")))
RH = {r["k"]: r for r in json.load(gzip.open(os.path.join(DATA, "hooktheory_rhythm.json.gz")))}
_cov = json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json"))); SONGS = list(_cov.keys()); del _cov   # key set only before the gate
by = collections.defaultdict(list)   # the song's clips, in surprise-file order
for c in S:
    if c["k"] in RH and c["k"] in CL and CL[c["k"]]["video"] == c["vid"]:
        by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))

base = []; drop = collections.Counter()
for vid in SONGS:
    cs = by.get(vid)
    if not cs: continue
    seqs = [chords(CL[c["k"]]) for c in cs]
    names, M = moves(seqs)
    if len(names) < 3: continue
    assert (M.sum(1) >= 1).all(), f"dead end in song {vid}"
    w = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    H, tp, nd, links = H_of(seqs)
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nd=nd, links=links, seqs=seqs, H=H, tpiece=tp, pmin=pmin_of(seqs))
    if H is None: drop[tp] += 1
    base.append(r)
songs = [r for r in base if r["H"] is not None]
print(f"songs with >= 3 distinct chords (before the first-year filter): {len(base)} [chair 2,672]; no root-0 chord: {drop['no_T']} [chair 80]; "
      f"T's piece under 3 chords: {drop['T_piece_under_3']}; H defined: {len(songs)}", flush=True)
print(f"  of these, T's piece is not the whole graph: {sum(r['tpiece'] < r['nd'] for r in songs)}", flush=True)
OUT["counts"] = dict(songs_3plus_chords=len(base), dropped_no_root0_chord=drop["no_T"], chair_no_root0=80, dropped_T_piece_under_3=drop["T_piece_under_3"],
                     H_defined=len(songs), T_piece_not_whole_graph=sum(r["tpiece"] < r["nd"] for r in songs))
hv = np.array([r["H"] for r in songs])
print(f"H: 10th {np.percentile(hv, 10):.3f}, median {np.median(hv):.3f}, 90th {np.percentile(hv, 90):.3f}; share H < 1: {np.mean(hv < 1):.3f}", flush=True)
OUT["H_shape"] = dict(p10_p50_p90=[r4(x) for x in np.percentile(hv, (10, 50, 90))], share_below_1=r4(np.mean(hv < 1)))

# ---------------------------------------------------------------- 3. GATE (no outcome loaded)
def dums(nd): nd = np.asarray(nd); return [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)]
def size_block(R): return np.column_stack(dums([r["nd"] for r in R]) + [[r["links"] for r in R], np.log([r["nclips"] for r in R])])
def zs(x): x = np.asarray(x, float); return (x - x.mean()) / x.std()

# 3.1 clip-to-clip: songs (H defined) with 2+ clips; H on clip 1 and on clip 2 alone; each must be defined
pairs = []
for r in songs:
    if r["nclips"] < 2: continue
    a, b = H_of([r["seqs"][0]]), H_of([r["seqs"][1]])
    if a[0] is None or b[0] is None: continue
    pairs.append((a, b))
P = len(pairs)
hs = np.array([a[0] for a, _ in pairs] + [b[0] for _, b in pairs])
Xc = sm.add_constant(np.column_stack(dums([a[2] for a, _ in pairs] + [b[2] for _, b in pairs]) + [[a[3] for a, _ in pairs] + [b[3] for _, b in pairs]]), has_constant="add")
res = sm.OLS(hs, Xc).fit().resid
rho_cc = float(spearmanr(res[:P], res[P:])[0]); rho_cc_raw = float(spearmanr(hs[:P], hs[P:])[0])
print(f"GATE 1, clip-to-clip: Spearman of residualised H, clip 1 vs clip 2: {rho_cc:.4f} on {P} pairs (needs >= 0.20) [chair 0.247, 1,057 pairs]; "
      f"raw {rho_cc_raw:.4f} [chair 0.273]", flush=True)
g1 = rho_cc >= 0.20

# 3.2 overlap
Xs = sm.add_constant(size_block(songs), has_constant="add")
Hres = sm.OLS(hv, Xs).fit().resid; R2 = float(sm.OLS(zs(hv), Xs).fit().rsquared)
cands = dict(**{f: [r[f] for r in songs] for f in FE}, distinct_chords=[r["nd"] for r in songs], links=[r["links"] for r in songs], clips=[r["nclips"] for r in songs])
cor = {k: r4(spearmanr(Hres, v)[0]) for k, v in cands.items()}
top = max(cor, key=lambda k: abs(cor[k]))
print("GATE 2, Spearman of H_res with:", json.dumps(cor), flush=True)
print(f"  largest |rho|: {top} {cor[top]:+.4f} (needs <= 0.7) [chair 0.083, length_variety; ch_ic_mean +0.06]; "
      f"R2 of standardised H on the size block: {R2:.4f} (needs <= 0.8) [chair 0.10]", flush=True)
g2 = abs(cor[top]) <= 0.7 and R2 <= 0.8
rho_raw_nd = float(spearmanr(hv, [r["nd"] for r in songs])[0])
both = [r for r in songs if r["pmin"] is not None]
rho_hp = float(spearmanr([r["H"] for r in both], [r["pmin"] for r in both])[0])
print(f"deciding nothing: raw rho(H, distinct chords) {rho_raw_nd:+.4f} [chair -0.44]; rho(H, p_min) {rho_hp:+.4f} on {len(both)} songs [chair +0.51]", flush=True)
OUT["gate"] = dict(clip_to_clip=dict(rho_residualised=r4(rho_cc), pairs=P, threshold=0.20, passed=bool(g1), raw_rho=r4(rho_cc_raw), chair=0.247, chair_pairs=1057),
                   overlap=dict(spearman_H_res=cor, largest_abs=[top, cor[top]], r2_size_block=r4(R2), passed=bool(g2), chair_largest=0.083, chair_r2=0.10),
                   passed=bool(g1 and g2))
OUT["deciding_nothing_before_outcome"] = dict(raw_rho_H_distinct_chords=r4(rho_raw_nd), rho_H_pmin=r4(rho_hp), songs_both=len(both), chair_rho_H_pmin=0.51)
print(f"GATE: {'PASSED' if g1 and g2 else 'FAILED'}", flush=True)
if not (g1 and g2):
    finish("stopped (gate failed" + (": clip-to-clip" if not g1 else "") + (": overlap" if not g2 else "") + "; no outcome joined)")

# ---------------------------------------------------------------- 4. outcome (first loaded here)
COV = json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json")))
VM = json.load(open(os.path.join(DATA, "discogs_versions_matched.json")))["cliques"]
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))   # as in studies/judging_checks/within_artist/test.py
rows = []
for r in songs:
    cv = COV[r["vid"]]
    if not cv["first_year"]: continue
    r = dict(r); r.update(covers=cv["covers"], first_year=cv["first_year"], clique=cv["clique"]); rows.append(r)
cnt = collections.Counter(r["artist"] for r in rows); sub = [r for r in rows if cnt[r["artist"]] >= 2]
miss = 0
for r in sub:
    a = norm(r["artist"]); vm = VM.get(str(r["clique"]))
    if vm is None: miss += 1; continue
    oth = [y for names, y, _ in vm["versions"] if a not in [norm(x) for x in (names if isinstance(names, list) else [names])]]
    r["early"] = sum(1 for y in oth if y is not None and y <= r["first_year"] + 5); r["late"] = sum(1 for y in oth if y is not None and y > r["first_year"] + 10)
assert miss == 0, f"{miss} cliques missing from the versions file"
print(f"rows with a first year: {len(rows)}; artists with two or more songs: {len(set(r['artist'] for r in sub))} artists, {len(sub)} songs", flush=True)

def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
def within(R, yname, feats, ctrl):   # copied from studies/judging_checks/within_artist/test.py (origin/main), via ../curvature/test.py
    art = np.array([r["artist"] for r in R]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    y = zc(np.log1p([r[yname] for r in R])); X = zc(np.column_stack([[r[f] for r in R] for f in feats] + [ctrl(R)]))
    def dm(M):
        M = np.array(M, float).reshape(len(R), -1); out = M.copy()
        for k in range(len(codes)): out[g == k] -= M[g == k].mean(0)
        return out
    m = sm.OLS(dm(y).ravel(), dm(X)).fit(cov_type="cluster", cov_kwds={"groups": g, "df_correction": True})
    return {f: dict(beta=float(m.params[i]), se=float(m.bse[i]), p=float(m.pvalues[i])) for i, f in enumerate(feats)}, len(R), len(codes)
def ctrl(R):   # first_year, log(clips per song), distinct links, distinct-chord dummies 4..11 and 12+
    return np.column_stack([[r["first_year"] for r in R], np.log([r["nclips"] for r in R]), [r["links"] for r in R]] + dums([r["nd"] for r in R]))
half = lambda r: int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
F = ["H", "ch_rep", "ch_ic_mean"]; F0 = ["H", "ch_rep"]

# ---------------------------------------------------------------- 5. SE and power first, then beta
main, n, na = within(sub, "covers", F, ctrl); t = main["H"]
power = float(N.cdf(0.03 / t["se"] - 2.638) + N.cdf(-0.03 / t["se"] - 2.638))
print(f"primary model: {n} songs, {na} artists; SE of beta {t['se']:.4f} [chair ~0.0165]; power to see -0.03 at p < .0083 two-sided: {power:.3f} [chair ~0.21]", flush=True)
b, p = t["beta"], t["p"]
print(f"beta(H) = {b:+.4f}, p = {p:.5f}, 95% range {b - 1.96 * t['se']:+.4f} to {b + 1.96 * t['se']:+.4f}  (predicted -0.03)", flush=True)
Hh = {h: within([r for r in sub if half(r) == h], "covers", F, ctrl) for h in (0, 1)}
hb = [Hh[h][0]["H"]["beta"] for h in (0, 1)]
for h in (0, 1):
    print(f"  half {h}: {Hh[h][1]} songs, {Hh[h][2]} artists; beta {hb[h]:+.4f} (SE {Hh[h][0]['H']['se']:.4f}, p {Hh[h][0]['H']['p']:.4f})", flush=True)
if b < 0 and p < 0.0083 and hb[0] < 0 and hb[1] < 0: verdict = "pass"
elif b > 0 and p < 0.0083: verdict = "kill (opposite sign, p < .0083: a new hypothesis, not a pass)"
elif b > -0.01: verdict = "kill"
else: verdict = "unsettled" + (" (the halves split)" if not (hb[0] < 0 and hb[1] < 0) else "")
OUT.update(rows_with_first_year=len(rows), songs=n, artists=na, prediction=-0.03, threshold_p=0.0083, se=r4(t["se"]), power=r4(power),
           primary=dict(beta=r4(b), se=r4(t["se"]), p=round(p, 5), ci95=[r4(b - 1.96 * t["se"]), r4(b + 1.96 * t["se"])],
                        ch_rep={k: r4(v) for k, v in main["ch_rep"].items()}, ch_ic_mean={k: r4(v) for k, v in main["ch_ic_mean"].items()}),
           halves=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2], beta=r4(hb[h]), se=r4(Hh[h][0]["H"]["se"]), p=r4(Hh[h][0]["H"]["p"])) for h in (0, 1)])

# ---------------------------------------------------------------- reported, deciding nothing
def one(R, yname, feats=F): r_, n_, a_ = within(R, yname, list(feats), ctrl); return dict(beta=r4(r_["H"]["beta"]), se=r4(r_["H"]["se"]), p=r4(r_["H"]["p"]), songs=n_, artists=a_)
whole = [r for r in sub if r["tpiece"] == r["nd"]]   # artists not re-filtered after the drop (a lone song is demeaned to zero and adds nothing)
dn = dict(covers_within_5_years=one(sub, "early"), covers_after_10_years=one(sub, "late"), beta_without_ch_ic_mean=one(sub, "covers", F0),
          T_piece_not_whole_graph_dropped=one(whole, "covers"),
          counts_per_half=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2]) for h in (0, 1)],
          median_covers_early_late=[float(np.median([r[k] for r in sub])) for k in ("covers", "early", "late")])
for k, v in dn.items(): print(f"  deciding nothing, {k}: {v}", flush=True)
OUT["deciding_nothing"] = dn
finish(verdict)
