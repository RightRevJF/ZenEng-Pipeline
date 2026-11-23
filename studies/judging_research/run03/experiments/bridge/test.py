"""Run 03, bridge experiment: does a song whose chord graph has a bridge get covered less, within the artist's own songs?
The rule is frozen in PREDICTION.md (commit ad201ad, written before any outcome was joined). This script implements it as written.

Order (kept honest, and printed as it goes):
  1. build the songs from the notes only (the song list is the key set of hooktheory_covers_discogs.json; nothing else in that file is read here);
  2. the measure B and the audit (code checks, shares, Spearman correlations, stop rule) on the songs BEFORE the first-year filter,
     i.e. before any field of the outcome side is read;
  3. only then read first_year (a row filter, but it sits on the outcome side), filter the rows, keep artists with two or more songs,
     and print the same audit again on the final rows (the stop rule is checked again there; it can only stop, never rescue);
  4. only then read covers and discogs_versions_matched.json;
  5. print the SE and the power, then the estimate; the halves; the reported-deciding-nothing items; write result.json.
python3 studies/judging_research/run03/experiments/bridge/test.py -> result.json in this folder
"""
import json, gzip, collections, re, hashlib, os, sys, time
import numpy as np, networkx as nx, statsmodels.api as sm
from scipy.stats import norm as N, spearmanr
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/home/claude/jdata"  # a read-only copy of origin/main:studies/judging_data (same files, not modified)
T0 = time.time()
RF = ["rhy_ic_mean", "rhy_h_mean", "rhy_cheung", "sync_per_note", "rest_share", "phrase_mean", "phrase_on_downbeat", "density", "length_variety"]
FE = ["mel_ic_mean", "mel_h_mean", "mel_cheung", "ch_ic_mean", "ch_h_mean", "ch_cheung", "mel_rep", "ch_rep"] + RF  # the 17 of study_covers_discogs.py
TOL = 1e-8

def qual(iv):  # copied from studies/surprise/surprise_hooktheory.py (origin/main)
    iv = tuple(iv)
    Q = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
    return Q.get(iv, 8)

def chord_seq(clip):
    """merged chord tokens of one clip: ((root - tonic) % 12)*9 + qual, sorted by onset, a chord equal to the one before merged"""
    tonic = clip["keys"][0]["tonic_pitch_class"] if clip.get("keys") else 0
    s = []
    for c in sorted(clip.get("harmony") or [], key=lambda c: c["onset"]):
        t = ((c["root_pitch_class"] - tonic) % 12) * 9 + qual(c["root_position_intervals"])
        if not s or s[-1] != t: s.append(t)
    return s

# ---------------------------------------------------------------- 1. songs from the notes
CL = json.load(gzip.open(os.path.join(DATA, "hooktheory_clips.json.gz")))["clips"]
S = json.load(gzip.open(os.path.join(DATA, "hooktheory_surprise.json.gz")))
RH = {r["k"]: r for r in json.load(gzip.open(os.path.join(DATA, "hooktheory_rhythm.json.gz")))}
SONGS = set(json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json"))).keys())  # key set only; covers/first_year not kept here
by = collections.defaultdict(list)  # the song's clips, in surprise-file order
for c in S:
    if c["vid"] in SONGS and c["k"] in RH and c["k"] in CL:
        assert CL[c["k"]]["video"] == c["vid"]
        by[c["vid"]].append(dict(c, **{f: RH[c["k"]][f] for f in RF}))

def lazy_kappa(M, nodes, G):
    """curvature experiment's kbar (Ollivier, laziness 1/2, hop distance, exact W1 by linprog highs), computed per link; within pieces"""
    idx = {a: i for i, a in enumerate(nodes)}; P = M / M.sum(1, keepdims=True)
    dist = dict(nx.all_pairs_shortest_path_length(G)); kap = {}
    def m(x):
        v = collections.defaultdict(float); v[x] += 0.5
        for j in np.nonzero(P[idx[x]])[0]: v[nodes[j]] += 0.5 * P[idx[x], j]
        return v
    for x, y in G.edges():
        mx, my = m(x), m(y); a, b = list(mx), list(my)
        cost = np.array([[dist[i][j] for j in b] for i in a], float).ravel()
        A = np.zeros((len(a) + len(b), len(a) * len(b)))
        for i in range(len(a)): A[i, i * len(b):(i + 1) * len(b)] = 1
        for j in range(len(b)): A[len(a) + j, j::len(b)] = 1
        r = linprog(cost, A_eq=A, b_eq=np.r_[[mx[i] for i in a], [my[j] for j in b]], bounds=(0, None), method="highs")
        assert r.status == 0
        kap[frozenset((x, y))] = 1 - r.fun
    return kap

def kbar_of(M, nodes, G):
    kap = lazy_kappa(M, nodes, G); num = den = 0.0
    for i, x in enumerate(nodes):
        for j, y in enumerate(nodes):
            if i != j and M[i, j] > 0: num += M[i, j] * kap[frozenset((x, y))]; den += M[i, j]
    return num / den

def graph_of(seqs):
    nodes = sorted({t for s in seqs for t in s}); idx = {a: i for i, a in enumerate(nodes)}; M = np.zeros((len(nodes), len(nodes)))
    for s in seqs:
        for i in range(len(s) - 1): M[idx[s[i]], idx[s[i + 1]]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[idx[s[-1]], idx[s[0]]] += 1
    G = nx.Graph(); G.add_nodes_from(nodes)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if M[i, j] + M[j, i] > 0: G.add_edge(nodes[i], nodes[j])
    return nodes, M, G

# unit tests for kbar (the curvature card's lazy values), since kbar is one of the audit's correlates here
def _unit(seqs, link): nodes, M, G = graph_of(seqs); return lazy_kappa(M, nodes, G)[frozenset(link)]
for seqs, link, want in [([[0, 1, 2]], (0, 1), 0.5), ([[0, 1, 2, 3]], (0, 1), 0.0), ([[9, 1], [9, 2], [9, 3], [9, 4]], (9, 1), 0.25),
                         ([[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]], (0, 1), 2 / 3)]:
    got = _unit(seqs, link); assert abs(got - want) < 1e-6, (seqs, got, want)

rows_all = []; n_dead = 0; n_nx_disagree = 0; n_nx_linkset_disagree = 0; foster_worst = 0.0
for vid, cs in by.items():
    seqs = [chord_seq(CL[c["k"]]) for c in cs]
    nodes, M, G = graph_of(seqs)
    if len(nodes) < 3: continue
    outdeg = (M > 0).sum(1)
    if (outdeg < 1).any(): n_dead += 1
    n = len(nodes); A = nx.to_numpy_array(G, nodelist=nodes); Q = np.diag(A.sum(1)) - A; Qd = np.linalg.pinv(Q)
    idx = {a: i for i, a in enumerate(nodes)}; links = list(G.edges()); om = {}
    for a, b in links:
        i, j = idx[a], idx[b]; om[frozenset((a, b))] = Qd[i, i] + Qd[j, j] - 2 * Qd[i, j]
    br = {e for e, w in om.items() if abs(1.0 * w - 1) < TOL}  # c = 1
    B = 1 if br else 0
    nxb = {frozenset(e) for e in nx.bridges(G)}
    n_nx_disagree += int(B != (1 if nxb else 0)); n_nx_linkset_disagree += int(br != nxb)
    pieces = nx.number_connected_components(G); foster_worst = max(foster_worst, abs(sum(om.values()) - (n - pieces)))
    traffic = sum(M[idx[a], idx[b]] + M[idx[b], idx[a]] for a, b in (tuple(e) for e in br)) / M.sum()
    w = np.array([c["n_mel"] for c in cs], float)
    r = {f: float(np.average([c[f] for c in cs], weights=w)) for f in FE}
    r.update(vid=vid, artist=cs[0]["artist"], nclips=len(cs), nchords=n, nlinks=len(links), moves=float(M.sum()), pieces=pieces, B=B,
             bridge_traffic=float(traffic), kbar=kbar_of(M, nodes, G))
    rows_all.append(r)

# ---------------------------------------------------------------- 2. audit on the songs before the first-year filter (no outcome read)
print(f"[{time.time() - T0:.0f}s] songs with at least one clip and >= 3 distinct chords, before the first-year filter: {len(rows_all)} (chair 2,672)")
print(f"  disconnected graphs: {sum(r['pieces'] > 1 for r in rows_all)} (chair 110)")
assert n_dead == 0, f"{n_dead} songs have a chord with no way out"
print("  no dead ends: every chord has out-degree >= 1 in every song")
print(f"  B from resistance vs networkx.bridges: {len(rows_all) - n_nx_disagree} of {len(rows_all)} agree (bridge link sets agree on {len(rows_all) - n_nx_linkset_disagree})")
print(f"  Foster: largest |sum c*omega - (n - pieces)| = {foster_worst:.2e}")
CHECKS = dict(B_matches_networkx=n_nx_disagree == 0, foster_holds=foster_worst < TOL)
assert all(CHECKS.values()), CHECKS  # the rule: fix the code before going on

ALSO = [("distinct chords", "nchords"), ("distinct links", "nlinks"), ("clips per song", "nclips"), ("merged moves", "moves"), ("kbar", "kbar")] + [(f, f) for f in FE]
def audit(R, label):
    Bv = np.array([r["B"] for r in R]); share = float(Bv.mean())
    byclips = {k: float(np.mean([r["B"] for r in R if (r["nclips"] if r["nclips"] < 3 else 3) == k])) for k in (1, 2, 3) if any((min(r["nclips"], 3)) == k for r in R)}
    rho = {lab: float(spearmanr(Bv, [r[k] for r in R])[0]) for lab, k in ALSO}
    top = max(rho, key=lambda k: abs(rho[k]))
    stop = (not 0.15 <= share <= 0.60) or abs(rho[top]) > 0.7
    print(f"  [{label}] songs {len(R)}; share with a bridge {share:.3f} (chair 0.305); by clips per song 1/2/3+: " + ", ".join(f"{byclips[k]:.2f}" for k in byclips))
    print("    Spearman rho of B with: " + "; ".join(f"{k} {v:+.3f}" for k, v in rho.items()))
    print(f"    largest |rho|: {top} {rho[top]:+.3f} (chair 0.18, distinct chords); stop rule {'MET: STOP' if stop else 'not met'}")
    return dict(songs=len(R), share_with_bridge=round(share, 4), share_by_clips_1_2_3plus={str(k): round(v, 4) for k, v in byclips.items()},
                spearman_with_B={k: round(v, 4) for k, v in rho.items()}, largest_abs_rho=[top, round(rho[top], 4)], stop=stop)
out = dict(rule="PREDICTION.md, commit ad201ad", checks=dict(songs=len(rows_all), B_matches_networkx=len(rows_all) - n_nx_disagree,
           bridge_link_sets_match=len(rows_all) - n_nx_linkset_disagree, foster_worst=foster_worst, dead_ends=n_dead,
           disconnected=sum(r["pieces"] > 1 for r in rows_all)))
out["audit_before_first_year"] = audit(rows_all, "before first-year filter, no outcome read")
def finish(verdict):
    out["verdict"] = verdict; json.dump(out, open(os.path.join(HERE, "result.json"), "w"), indent=1); print("VERDICT:", verdict); sys.exit(0)
if out["audit_before_first_year"]["stop"]: finish("stopped (audit, before any outcome was read)")

# ---------------------------------------------------------------- 3. first_year (outcome side, used only as a row filter), then the final rows
FY = {vid: cv["first_year"] for vid, cv in json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json"))).items()}  # first_year only
rows = [dict(r, first_year=FY[r["vid"]]) for r in rows_all if FY[r["vid"]]]
cnt = collections.Counter(r["artist"] for r in rows); rows = [r for r in rows if cnt[r["artist"]] >= 2]
print(f"[{time.time() - T0:.0f}s] with a first year: {sum(1 for r in rows_all if FY[r['vid']])}; artists with two or more songs: "
      f"{len(set(r['artist'] for r in rows))} artists, {len(rows)} songs")
out["audit_final_rows"] = audit(rows, "final rows, first year read, covers not yet read")
if out["audit_final_rows"]["stop"]: finish("stopped (audit on the final rows, before covers were read)")

# ---------------------------------------------------------------- 4. outcomes: covers, then other artists' versions by period
COV = json.load(open(os.path.join(DATA, "hooktheory_covers_discogs.json")))
VER = json.load(open(os.path.join(DATA, "discogs_versions_matched.json")))["cliques"]  # clique -> {video, first_year, versions: [[artists], year, [release ids]]}
norm = lambda s: re.sub(r"[^a-z0-9]", "", (s or "").lower().replace("&", "and"))  # as in within_artist/test.py
for r in rows:
    cv = COV[r["vid"]]; r["covers"] = cv["covers"]; a = norm(r["artist"])
    oth = [y for names, y, _ in VER[cv["clique"]]["versions"] if a not in [norm(x) for x in names]]
    r["early"] = sum(1 for y in oth if y is not None and y <= r["first_year"] + 5)
    r["late"] = sum(1 for y in oth if y is not None and y > r["first_year"] + 10)
    r["undated"] = sum(1 for y in oth if y is None)

def zc(M): M = np.asarray(M, float); s = np.atleast_1d(M.std(0)).copy(); s[s == 0] = 1; return (M - M.mean(0)) / (s if M.ndim > 1 else s[0])
def within(R, yname, feats, ctrl):
    """copied from within_artist/test.py: y and every column standardised over R, demeaned within artist, OLS without a constant,
    SE clustered by artist with statsmodels' small-sample correction"""
    art = np.array([r["artist"] for r in R]); codes = {a: i for i, a in enumerate(sorted(set(art)))}; g = np.array([codes[a] for a in art])
    y = zc(np.log1p([r[yname] for r in R])); X = zc(np.column_stack([[r[f] for r in R] for f in feats] + [ctrl(R)]))
    def dm(M):
        M = np.array(M, float).reshape(len(R), -1); out = M.copy()
        for k in range(len(codes)): out[g == k] -= M[g == k].mean(0)
        return out
    m = sm.OLS(dm(y).ravel(), dm(X)).fit(cov_type="cluster", cov_kwds={"groups": g, "df_correction": True})
    return {f: dict(beta=float(m.params[i]), se=float(m.bse[i]), p=float(m.pvalues[i])) for i, f in enumerate(feats)}, len(R), len(codes)
DUM = [4, 5, 6, 7, 8, 9, 10, 11, 12]  # distinct chords = 4..11 and 12+, 3 the reference
ctrl = lambda R: np.column_stack([[r["first_year"] for r in R], np.log([r["nclips"] for r in R]), [r["nlinks"] for r in R], [r["ch_rep"] for r in R]]
                                 + [[float(r["nchords"] >= 12 if k == 12 else r["nchords"] == k) for r in R] for k in DUM])
half = lambda r: int(hashlib.md5(r["artist"].encode()).hexdigest(), 16) % 2
r4 = lambda x: round(x, 4)

# ---------------------------------------------------------------- 5. SE and power first, then the estimate
res, n, na = within(rows, "covers", ["B"], ctrl); t = res["B"]
power = float(N.cdf(0.025 / t["se"] - 2.2414) + N.cdf(-0.025 / t["se"] - 2.2414))
print(f"[{time.time() - T0:.0f}s] primary model: {n} songs, {na} artists; SE {t['se']:.4f} (chair ~0.015); power to see -0.025 at p<.025 two-sided: {power:.2f} (chair ~0.29)", flush=True)
print(f"  beta {t['beta']:+.4f}, p {t['p']:.4f}  (predicted -0.025; 95% range {t['beta'] - 1.96 * t['se']:+.4f} to {t['beta'] + 1.96 * t['se']:+.4f})")
H = {}
for h in (0, 1):
    Rh = [r for r in rows if half(r) == h]; rh, nh, ah = within(Rh, "covers", ["B"], ctrl)
    H[h] = dict(songs=nh, artists=ah, share_with_bridge=r4(float(np.mean([r["B"] for r in Rh]))), beta=r4(rh["B"]["beta"]), se=r4(rh["B"]["se"]), p=r4(rh["B"]["p"]))
    print(f"  half {h}: {nh} songs, {ah} artists, share with a bridge {H[h]['share_with_bridge']:.3f}; beta {H[h]['beta']:+.4f} (SE {H[h]['se']:.4f}, p {H[h]['p']:.4f})")
b, p = t["beta"], t["p"]
if b < 0 and p < 0.025 and H[0]["beta"] < 0 and H[1]["beta"] < 0: verdict = "pass"
elif b > 0 and p < 0.025: verdict = "kill (opposite sign, p < .025: reported as 'the bridge is the move people remember'; not a pass, needs its own rule first)"
elif b > -0.01: verdict = "kill"
else: verdict = "unsettled" + (" (the halves split)" if not (H[0]["beta"] < 0 and H[1]["beta"] < 0) else "")
out.update(songs=n, artists=na, prediction_beta=-0.025, se=r4(t["se"]), power_for_minus_0_025_at_p_025=round(power, 2),
           primary=dict(beta=r4(b), se=r4(t["se"]), p=r4(p), range95=[r4(b - 1.96 * t["se"]), r4(b + 1.96 * t["se"])]), halves=[H[0], H[1]])

# ---------------------------------------------------------------- reported, deciding nothing
def one(yname, R=rows, feat="B"): rr, nn, aa = within(R, yname, [feat], ctrl); return dict(beta=r4(rr[feat]["beta"]), se=r4(rr[feat]["se"]), p=r4(rr[feat]["p"]), songs=nn, artists=aa)
conn = [r for r in rows if r["pieces"] == 1]  # artists not re-filtered after the drop (a lone song is demeaned to zero and adds nothing)
dn = dict(covers_within_five_years=one("early"), covers_after_ten_years=one("late"),
          median_covers_early_late_undated=[float(np.median([r[k] for r in rows])) for k in ("covers", "early", "late", "undated")],
          without_disconnected_songs=one("covers", conn), share_of_traffic_on_bridges_in_place_of_B=one("covers", rows, "bridge_traffic"),
          sd_of_B=r4(float(np.std([r["B"] for r in rows]))))
out["deciding_nothing"] = dn
for k, v in dn.items(): print(f"  deciding nothing, {k}: {v}")
print(f"[{time.time() - T0:.0f}s]"); finish(verdict)
