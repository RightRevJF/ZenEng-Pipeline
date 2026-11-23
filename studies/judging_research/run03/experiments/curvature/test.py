"""Run 03, curvature test: lazy Ollivier curvature of the pooled chord walk (kbar) against covers, within each artist's own songs.
The rule is PREDICTION.md in this folder (rows, graph and model from ../bridge/PREDICTION.md), committed before this script was written.
Order: build rows and measure -> audit (no outcome) -> stop rule -> only then load covers / first_year / versions -> SE and power -> estimate.
python3 test.py [--audit-only] -> result.json (the full run)."""
import json, gzip, collections, re, hashlib, os, sys, time
import numpy as np, statsmodels.api as sm, networkx as nx, ot
from scipy.optimize import linprog
from scipy.sparse.csgraph import shortest_path, connected_components
from scipy.stats import norm as N, spearmanr

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/home/claude/jdata"   # a read-only copy of origin/main:studies/judging_data
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF
OUT = {}

# ---------------------------------------------------------------- W1 and curvature
_AEQ = {}
def w1_lp(a, b, C):
    """exact W1 by linear programme (scipy highs), a on rows, b on columns"""
    p, q = C.shape
    if (p, q) not in _AEQ:
        A = np.zeros((p + q, p * q))
        for i in range(p): A[i, i * q:(i + 1) * q] = 1
        for j in range(q): A[p + j, j::q] = 1
        _AEQ[(p, q)] = A
    res = linprog(C.ravel(), A_eq=_AEQ[(p, q)], b_eq=np.concatenate([a, b]), bounds=(0, None), method="highs")
    assert res.status == 0
    return float(res.fun)
def w1_ot(a, b, C): return float(ot.emd2(a, b, C))   # exact network simplex (POT); used for the shuffles only

def curv(M, w1=w1_lp):
    """M: pooled move counts (n x n, zero diagonal). Returns dict link(i<j) -> kappa, lazy matrix, distance matrix."""
    n = len(M); P = M / M.sum(1, keepdims=True); L = 0.5 * np.eye(n) + 0.5 * P
    A = ((M + M.T) > 0).astype(float); np.fill_diagonal(A, 0)
    D = shortest_path(A, unweighted=True, directed=False)
    kap = {}
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j]:
                si, sj = np.nonzero(L[i] > 0)[0], np.nonzero(L[j] > 0)[0]
                a, b = L[i, si], L[j, sj]
                kap[(i, j)] = 1.0 - w1(a / a.sum(), b / b.sum(), D[np.ix_(si, sj)])
    return kap, L, A, D

def kbar_of(M, kap):
    num = den = 0.0
    for (i, j), k in kap.items():
        w = M[i, j] + M[j, i]; num += w * k; den += w
    return num / den

# ---------------------------------------------------------------- 1. unit tests (card 1's lazy values)
C3 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], float)
C4 = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0]], float)
H = np.zeros((5, 5)); H[0, 1:] = 1; H[1:, 0] = 1
K4 = np.ones((4, 4)) - np.eye(4)
unit = {}
for name, W, want in (("directed 3-cycle", C3, 0.5), ("directed 4-cycle", C4, 0.0), ("hub with 4 spokes", H, 0.25), ("K4", K4, 0.667)):
    kap, *_ = curv(W); vals = sorted(set(round(v, 3) for v in kap.values()))
    kap2, *_ = curv(W, w1_ot); assert max(abs(kap[e] - kap2[e]) for e in kap) < 1e-9
    unit[name] = dict(want=want, got=vals, ok=vals == [want])
    print(f"unit test {name}: want {want}, got {vals}", flush=True)
assert all(u["ok"] for u in unit.values()), "unit tests failed: the code is wrong"
OUT["audit_unit_tests"] = unit

# ---------------------------------------------------------------- rows (notes only)
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
def merge(seq):
    out = []
    for x in seq:
        if not out or out[-1] != x: out.append(x)
    return out
def moves(seqs, ix, n):
    M = np.zeros((n, n))
    for s in seqs:
        for a, b in zip(s, s[1:]): M[ix[a], ix[b]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[ix[s[-1]], ix[s[0]]] += 1
    return M

CL = json.load(gzip.open(os.path.join(DATA, "hooktheory_clips.json.gz")))["clips"]
S = json.load(gzip.open(os.path.join(DATA, "hooktheory_surprise.json.gz")))
RH = {r["k"]: r for r in json.load(gzip.open(os.path.join(DATA, "hooktheory_rhythm.json.gz")))}
_cov = json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json"))); SONGS = list(_cov.keys()); del _cov   # only the keys (song ids) are used before the audit
by = collections.defaultdict(list)
for c in S:
    if c["k"] in RH and c["k"] in CL and CL[c["k"]]["video"] == c["vid"]:
        by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))

songs = []
for vid in SONGS:
    cs = by.get(vid)
    if not cs: continue
    seqs = [chords(CL[c["k"]]) for c in cs]
    names = sorted(set(t for s in seqs for t in s))
    if len(names) < 3: continue
    ix = {t: i for i, t in enumerate(names)}; n = len(names); M = moves(seqs, ix, n)
    assert (M.sum(1) >= 1).all(), f"dead end in song {vid}"
    w = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nd=n, seqs=seqs, M=M, moves=float(M.sum()))
    songs.append(r)
print(f"songs with at least 3 distinct chords (before the first-year filter): {len(songs)}  [chair 2,672]", flush=True)

# ---------------------------------------------------------------- measure, B, Prop. 29
viol = []; t1 = time.time()
for r in songs:
    M = r["M"]; n = r["nd"]
    kap, L, A, D = curv(M)
    r["kbar"] = kbar_of(M, kap); r["kmin"] = min(kap.values()); r["kmean_unweighted"] = float(np.mean(list(kap.values())))
    r["links"] = len(kap)
    npc, lab = connected_components(A, directed=False); r["pieces"] = int(npc)
    big = max(range(npc), key=lambda p: ((lab == p).sum(), -p)); gl = {}
    for p in range(npc):
        idx = np.nonzero(lab == p)[0]
        if len(idx) < 2: continue
        Lp = L[np.ix_(idx, idx)]; assert np.allclose(Lp.sum(1), 1)
        ev = np.sort(np.abs(np.linalg.eigvals(Lp)))[::-1]; g = 1 - ev[1]; gl[p] = g
        kp = min(k for (i, j), k in kap.items() if lab[i] == p)
        if g < kp - 1e-9: viol.append(dict(vid=r["vid"], piece=p, g=g, kmin=kp))
    r["g_lazy"] = float(gl[big])
    # bridge indicator B by ../bridge/PREDICTION.md: Laplacian pseudoinverse, c = 1, any link with c*omega = 1 within 1e-8
    Q = np.diag(A.sum(1)) - A; Qd = np.linalg.pinv(Q)
    om = {e: Qd[e[0], e[0]] + Qd[e[1], e[1]] - 2 * Qd[e[0], e[1]] for e in kap}
    r["B"] = float(any(abs(v - 1) < 1e-8 for v in om.values()))
    G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(kap)
    r["B_nx"] = float(any(True for _ in nx.bridges(G)))
    r["foster_ok"] = abs(sum(om.values()) - (n - npc)) < 1e-8
    r["kap"] = kap
print(f"curvature by linprog(highs) on {len(songs)} songs: {time.time() - t1:.0f}s", flush=True)
# exactness cross-check: POT network simplex against highs on every link
dmax = 0.0
for r in songs:
    k2, *_ = curv(r["M"], w1_ot); dmax = max(dmax, max(abs(k2[e] - r["kap"][e]) for e in k2))
print(f"max |kappa(highs) - kappa(POT)| over all links: {dmax:.2e}", flush=True)

print(f"Prop. 29 (g_lazy >= min link kappa - 1e-9 in every piece with 2+ nodes): {len(viol)} violations  [chair 0]", flush=True)
assert not viol, "Prop. 29 failed: the code is wrong"
bmatch = sum(r["B"] == r["B_nx"] for r in songs); foster = sum(r["foster_ok"] for r in songs)
print(f"B from resistance = B from networkx.bridges: {bmatch} of {len(songs)}; Foster holds: {foster} of {len(songs)}", flush=True)
assert bmatch == len(songs) and foster == len(songs)
OUT["audit_prop29"] = dict(pieces_checked=sum(1 for r in songs for _ in range(r["pieces"])), violations=len(viol), chair=0)
OUT["audit_bridge_code"] = dict(B_resistance_equals_networkx=bmatch, foster_holds=foster, songs=len(songs), share_with_bridge=round(float(np.mean([r["B"] for r in songs])), 4))
OUT["audit_kappa_highs_vs_pot_max_diff"] = dmax

# ---------------------------------------------------------------- 3. measure shape
def size_block(R):
    nd = np.array([r["nd"] for r in R])
    dums = [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)]
    return np.column_stack(dums + [[r["links"] for r in R], np.log([r["nclips"] for r in R])])
def zs(x): x = np.asarray(x, float); return (x - x.mean()) / x.std()
def shape(R):
    kb = np.array([r["kbar"] for r in R]); Xs = sm.add_constant(size_block(R))
    fit = sm.OLS(zs(kb), Xs).fit(); res = sm.OLS(kb, Xs).fit().resid
    return kb, fit.rsquared, res
kb, R2, kres = shape(songs)
pct = np.percentile(kb, (10, 50, 90)); share_kmin = float(np.mean([r["kmin"] > 0 for r in songs]))
print(f"kbar: 10th {pct[0]:.3f}, median {pct[1]:.3f}, 90th {pct[2]:.3f}  [chair 0.00, 0.20, 0.50]; share kmin > 0: {share_kmin:.3f} [chair 0.22]; "
      f"R2 of standardised kbar on the size block: {R2:.3f} [chair 0.46]; disconnected songs: {sum(r['pieces'] > 1 for r in songs)} [chair 110]", flush=True)
OUT["audit_shape"] = dict(songs=len(songs), kbar_p10_p50_p90=[round(float(x), 4) for x in pct], chair_p10_p50_p90=[0.0, 0.20, 0.50],
                          share_kmin_positive=round(share_kmin, 4), chair_share=0.22, r2_size_block=round(float(R2), 4), chair_r2=0.46,
                          disconnected=sum(r["pieces"] > 1 for r in songs), chair_disconnected=110)

# ---------------------------------------------------------------- 4. correlations of residual kbar
cands = dict(distinct_chords=[r["nd"] for r in songs], links=[r["links"] for r in songs], clips=[r["nclips"] for r in songs], merged_moves=[r["moves"] for r in songs],
             g_lazy_largest_piece=[r["g_lazy"] for r in songs], kmin=[r["kmin"] for r in songs], B=[r["B"] for r in songs], **{f: [r[f] for r in songs] for f in FE})
cor = {k: round(float(spearmanr(kres, v)[0]), 4) for k, v in cands.items()}
print("Spearman rho of kbar_res with:", json.dumps(cor), flush=True)
print("  [chair: lazy g +0.35, ch_h_mean -0.24, B +0.22, ch_ic_mean -0.17, ch_rep +0.02; others |rho| <= 0.16]", flush=True)
OUT["audit_correlations_kbar_res"] = cor

# ---------------------------------------------------------------- 5. the chair's g gate (McGill rule, per clip, not lazy) -- decides nothing
def mcgill_graph(seq):   # studies/judging_checks/nights_1_2/gap.py graph()
    seq = list(seq)
    if seq[0] == seq[-1] and len(seq) > 1: seq = seq[:-1]
    names = sorted(set(seq)); ix = {t: i for i, t in enumerate(names)}; n = len(names)
    if n < 2 or len(seq) < 4: return None
    M = np.zeros((n, n))
    for a, b in zip(seq, seq[1:] + seq[:1]):
        if a != b: M[ix[a], ix[b]] += 1
    if (M.sum(1) == 0).any(): return None
    return M
def mcgill_gap(seq):
    if len(seq) < 4: return None
    M = mcgill_graph(seq)
    if M is None: return None
    P = M / M.sum(1, keepdims=True); ev = sorted(np.abs(np.linalg.eigvals(P)), reverse=True); return float(1 - ev[1])
gs, nds, g1, g2 = [], [], [], []
for r in songs:
    cg = [(mcgill_gap(s), len(s)) for s in r["seqs"]]
    ok = [(g, w) for g, w in cg if g is not None]
    if ok: gs.append(np.average([g for g, _ in ok], weights=[w for _, w in ok])); nds.append(r["nd"])
    if len(cg) >= 2 and cg[0][0] is not None and cg[1][0] is not None: g1.append(cg[0][0]); g2.append(cg[1][0])
gate = dict(songs_with_g=len(gs), rho_with_distinct_chords=round(float(spearmanr(gs, nds)[0]), 4), chair_rho_distinct=0.26,
            rho_clip1_clip2=round(float(spearmanr(g1, g2)[0]), 4), pairs=len(g1), chair_rho_clips=0.17, share_g_under_0_01=round(float(np.mean(np.array(gs) < 0.01)), 4), chair_share_under_0_01=0.37)
print("g gate (decides nothing):", json.dumps(gate), flush=True)
OUT["audit_g_gate"] = gate

# ---------------------------------------------------------------- 6. stop rule
maxrho = max(abs(v) for v in cor.values())
stopped = R2 > 0.8 or maxrho > 0.7
OUT["stop_rule"] = dict(r2=round(float(R2), 4), max_abs_rho=round(maxrho, 4), stopped=bool(stopped))
print(f"stop rule: R2 {R2:.3f} (stop if > 0.8), max |rho| {maxrho:.3f} (stop if > 0.7) -> {'STOPPED' if stopped else 'go on'}", flush=True)
if stopped:
    OUT["verdict"] = "stopped"; json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item()); sys.exit(0)
if "--audit-only" in sys.argv:
    print("audit only: no outcome loaded"); sys.exit(0)

# ---------------------------------------------------------------- shuffle-relative kbar (Geometer; decides nothing). Built before any outcome is read.
def kbar_seqs(seqs, w1=w1_ot):
    names = sorted(set(t for s in seqs for t in s)); ix = {t: i for i, t in enumerate(names)}; M = moves(seqs, ix, len(names))
    kap, *_ = curv(M, w1); return kbar_of(M, kap)
rng = np.random.default_rng(0); t2 = time.time(); SH = []
for rep in range(40):
    if rep == 1:
        per = time.time() - t2
        nsh = 40 if (time.time() - T0) + 39 * per < 45 * 60 else 10
    if rep >= 1 and rep >= nsh: break
    SH.append([kbar_seqs([merge(list(rng.permutation(s))) for s in r["seqs"]]) for r in songs])
nsh = len(SH); SHm = np.mean(SH, 0)
for r, m in zip(songs, SHm): r["kbar_shuf_rel"] = r["kbar"] - float(m)
print(f"shuffle-relative kbar: {nsh} shuffles, {time.time() - t2:.0f}s (each clip's merged sequence permuted with default_rng(0), shuffles outer, songs then clips inner)", flush=True)

# ---------------------------------------------------------------- outcome (first loaded here)
COV = json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json")))
VM = json.load(open(os.path.join(DATA, "discogs_versions_matched.json")))["cliques"]   # per clique: video, first_year, versions [artists (already normed), year, release ids]
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
print(f"rows with a first year: {len(rows)}; artists with two or more songs: {len(set(r['artist'] for r in sub))} artists, {len(sub)} songs; cliques missing from the versions file: {miss}", flush=True)

def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
def within(R, yname, feats, ctrl):   # copied from studies/judging_checks/within_artist/test.py (origin/main)
    art = np.array([r["artist"] for r in R]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    y = zc(np.log1p([r[yname] for r in R])); X = zc(np.column_stack([[r[f] for r in R] for f in feats] + [ctrl(R)]))
    def dm(M):
        M = np.array(M, float).reshape(len(R), -1); out = M.copy()
        for k in range(len(codes)): out[g == k] -= M[g == k].mean(0)
        return out
    m = sm.OLS(dm(y).ravel(), dm(X)).fit(cov_type="cluster", cov_kwds={"groups": g, "df_correction": True})
    return {f: dict(beta=float(m.params[i]), se=float(m.bse[i]), p=float(m.pvalues[i])) for i, f in enumerate(feats)}, len(R), len(codes)
def ctrl(R):   # first_year, log(clips per song), distinct links, distinct-chord dummies 4..11 and 12+
    nd = np.array([r["nd"] for r in R])
    return np.column_stack([[r["first_year"] for r in R], np.log([r["nclips"] for r in R]), [r["links"] for r in R]] + [(nd == k).astype(float) for k in range(4, 12)] + [(nd >= 12).astype(float)])
half = lambda r: int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
F = ["kbar", "ch_rep", "ch_ic_mean"]; F0 = ["kbar", "ch_rep"]
main, n, na = within(sub, "covers", F, ctrl); t = main["kbar"]
power = float(N.cdf(0.02 / t["se"] - 2.2414) + N.cdf(-0.02 / t["se"] - 2.2414))
print(f"SE of beta: {t['se']:.4f} [chair 0.020]; power to see +0.02 at p < .025: {power:.3f} [chair 0.10]", flush=True)
b, p = t["beta"], t["p"]
print(f"beta(kbar) = {b:+.4f}, p = {p:.4f}, range {b - 1.96 * t['se']:+.4f} to {b + 1.96 * t['se']:+.4f}", flush=True)
m0, _, _ = within(sub, "covers", F0, ctrl); b0 = m0["kbar"]["beta"]
print(f"beta0 (without ch_ic_mean) = {b0:+.4f}, p = {m0['kbar']['p']:.4f}", flush=True)
Hh = {h: within([r for r in sub if half(r) == h], "covers", F, ctrl) for h in (0, 1)}
hb = [Hh[h][0]["kbar"]["beta"] for h in (0, 1)]
print(f"halves: {hb[0]:+.4f} (p {Hh[0][0]['kbar']['p']:.3f}, {Hh[0][1]} songs), {hb[1]:+.4f} (p {Hh[1][0]['kbar']['p']:.3f}, {Hh[1][1]} songs)", flush=True)
if b <= 0: verdict = "kill" + (" (opposite sign, p < .025: a new hypothesis, not a pass)" if p < 0.025 else "")
elif b0 > 0 and b < 0.5 * b0: verdict = "kill as surprise renamed"
elif p < 0.025 and hb[0] > 0 and hb[1] > 0 and b >= 0.5 * b0: verdict = "pass"
else: verdict = "unsettled"
print("VERDICT:", verdict, flush=True)
OUT.update(rows_with_first_year=len(rows), songs=n, artists=na, se=round(t["se"], 4), power=round(power, 4), prediction=0.02,
           primary=dict(beta=round(b, 4), se=round(t["se"], 4), p=round(p, 5), ci95=[round(b - 1.96 * t["se"], 4), round(b + 1.96 * t["se"], 4)],
                        ch_rep=dict((k, round(v, 4)) for k, v in main["ch_rep"].items()), ch_ic_mean=dict((k, round(v, 4)) for k, v in main["ch_ic_mean"].items())),
           beta0=dict(beta=round(b0, 4), se=round(m0["kbar"]["se"], 4), p=round(m0["kbar"]["p"], 5)),
           halves=[dict(half=h, songs=Hh[h][1], artists=Hh[h][2], beta=round(hb[h], 4), p=round(Hh[h][0]["kbar"]["p"], 4)) for h in (0, 1)], verdict=verdict)

# ---------------------------------------------------------------- reported, deciding nothing
def one(R, yname, feats=F, key="kbar"): r_, n_, a_ = within(R, yname, list(feats), ctrl); return dict(beta=round(r_[key]["beta"], 4), se=round(r_[key]["se"], 4), p=round(r_[key]["p"], 4), songs=n_)
conn = [r for r in sub if r["pieces"] == 1]
for r in sub: r["kbar_unw"] = r["kmean_unweighted"]
dn = dict(covers_within_5_years=one(sub, "early"), covers_after_10_years=one(sub, "late"),
          beta0_within_5_years=one(sub, "early", F0), beta0_after_10_years=one(sub, "late", F0),
          disconnected_songs_dropped=one(conn, "covers"),
          unweighted_mean_link_kappa=dict(rho_with_kbar_all_songs=round(float(spearmanr([r["kbar"] for r in songs], [r["kmean_unweighted"] for r in songs])[0]), 4),
                                          rho_with_kbar_model_rows=round(float(spearmanr([r["kbar"] for r in sub], [r["kbar_unw"] for r in sub])[0]), 4), chair_rho=0.91,
                                          model_in_place_of_kbar=one(sub, "covers", ["kbar_unw", "ch_rep", "ch_ic_mean"], "kbar_unw")),
          shuffle_relative_kbar=dict(shuffles=nsh, rho_with_ch_rep_all_songs=round(float(spearmanr([r["kbar_shuf_rel"] for r in songs], [r["ch_rep"] for r in songs])[0]), 4),
                                     rho_with_ch_rep_model_rows=round(float(spearmanr([r["kbar_shuf_rel"] for r in sub], [r["ch_rep"] for r in sub])[0]), 4), geometer_rho=-0.62,
                                     model_in_place_of_kbar=one(sub, "covers", ["kbar_shuf_rel", "ch_rep", "ch_ic_mean"], "kbar_shuf_rel")),
          shape_on_model_rows=dict(zip(("kbar_p10_p50_p90", "r2_size_block"), (lambda s_: ([round(float(x), 4) for x in np.percentile(s_[0], (10, 50, 90))], round(float(s_[1]), 4)))(shape(sub)))),
          median_covers_early_late=[float(np.median([r[k] for r in sub])) for k in ("covers", "early", "late")])
print(json.dumps(dn, indent=1), flush=True)
OUT["deciding_nothing"] = dn
OUT["runtime_s"] = round(time.time() - T0)
json.dump(OUT, open(os.path.join(HERE, "result.json"), "w"), indent=1, default=lambda o: o.item())
print(f"done in {time.time() - T0:.0f}s")
