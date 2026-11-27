"""Run 09 measures, frozen by the chair before any outcome is joined. NOTES ONLY.

Reads: the chart caches ($DL/choco/charts_run09.json, charts_run08.json, through common09.load_charts and directly), the run 09
design ($DL/choco/design_run09.json: clique ids, composer key, genre, chart ids; no counts, no years), and, for the two seen-song
leads, ONLY the 'clique' and 'charts' fields of studies/judging_research/data/choco_songs_discogs_run08.json (that file also holds
run 08's outcomes; no other field is read here). It never reads $SHAPE, $DL/discogs or any covers/versions/HOLDOUT file and never
calls common09.load_outcomes or run 08's common.load_outcomes.

Usage (from this folder):  python3 -I measures09.py        (about 2 to 3 minutes on one core)
Writes  $DL/choco/measures_run09.json   (outside the repo): per chart every value; per design song the unweighted mean over its
                                         measured charts; the seen-song lead tables (section 'seen08')
        ./measure_gates.json             coverage, two-chart stability, within-set Spearman with ch_rep, V and IIV, the gates

THE RECIPES. Run 08's frozen measures are imported from run08/experiments/measures.py (committed): listener_measures gives IIV,
ch_rep, V, ln_chg, ln_bars; geometer_measures gives w_chr. Every new recipe is COPIED below from the imaginers' scripts (not imported):
  /home/claude/scripts/geometer/g09_measures.py  tokens_with_dur, ii_collapse, TR (G09-2), TE (G09-3), u_path, levy, CH
  /home/claude/scripts/geometer/g09_tq.py        TQ (G09-1, the lead-lag construction)
  /home/claude/scripts/listener/checks_r09.py    DRES and FUL (R09-L2); n_bars
  /home/claude/scripts/listener/checks_r09b.py   CARC (R09-L3), with the round-2 change (arrivals in the first 2 and last 2 bars dropped)
  /home/claude/scripts/inventor/r09_measures.py  IRR (R09-I1), vr4, areas and typicality (R09-I3, TYP)
  /home/claude/scripts/inventor/r09_vr4c.py      VR4c (R09-I2 revised: VR4 with the m7 of each ii-V dropped)

THE CHAIR'S RULES (frozen here):
  * Chart filter: run 08's (listener_measures defined: >= 8 events and >= 6 change tokens). A measure that is nan on a chart is
    left out of that song's mean; a song with no defined value has None.
  * TIMEBASE. Charts timed in SECONDS (recordings except rock-corpus) have no bars: ln_bars, DRES and CARC are set to missing on
    them (nan). The song value is the mean over the charts where defined. In the models (harness09.py) a song with no bar-timed chart
    gets ln_bars = the mean of ln_bars over the analysed songs that have one, plus the indicator column no_bars = 1 (0 otherwise).
    Every other measure here is per change and is defined on both timebases.
  * TYP reference: within the chart's coarse genre (common09.coarse_genre: jazz, pop, biab, wikifonia, other), over every chart of
    common09.load_charts() (run 09 partitions + run 08's charts outside the run 08 design) that passes the filter and has six finite
    areas (the Inventor's round 2: coarse genre, not partition).
  * Halves (frozen for every test): common09.halves(the song's composer key in the design) = md5 of the name-matched person key,
    else of nrm(the clique's first Discogs-VI writer), else of 'solo:<clique>'.
  * SEEN08 (the two seen-song leads; run 08 songs, whose outcomes were opened in run 08):
      - run 08 songs = the 8,640 cliques of choco_songs_discogs_run08.json with their chart lists (fields 'clique' and 'charts' only).
      - per song: IIV, DRES, w_chr, ch_rep, V, ln_chg, ln_bars as the unweighted mean over all its charts (run 08's song value; all
        run 08 charts are bar-timed), and the same over its iReal Pro charts only (ireal-forum, ireal-playlists): *_ireal, n_ireal.
      - genre8: run 08's rule (common.genre_of, most common over the song's charts, ties alphabetical).
      - UPSTREAM charts: a run 09 real-book or biab-internet-corpus chart (>= 8 chords, not in the run 09 design) is matched to a run 08
        song when the chart's raw title (brackets removed, cut at ' - ') has at least two words and the union of its common.variants()
        hits the variants of the chart titles of exactly ONE run 08 song (notes-side title match; no Discogs field is read).
      - IIV_up and the controls *_up = the mean over the song's matched upstream charts (real-book and BiaB pooled).
"""
import sys, os, json, math, re, collections, time, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from scipy.stats import norm, spearmanr
import common09 as C9
C8 = C9.C8
sys.path.insert(0, os.path.join(C9.REPO, "studies/judging_research/run08/experiments"))
import measures as M8          # run 08 frozen measures (listener_measures, geometer_measures, change_tokens)

OUT = os.path.join(C9.DL, "choco", "measures_run09.json")
GATES = os.path.join(HERE, "measure_gates.json")
RUN08_DATA = os.path.join(C9.REPO, "studies/judging_research/data/choco_songs_discogs_run08.json")

# ================================================================ the Geometer (g09_measures.py, g09_tq.py; copied)
def tokens_with_dur(ch):
    out = []                                            # [root, bm tuple, dur]
    for t, d, r, bm, b in ch:
        if not any(bm): continue
        k = (r, tuple(bm))
        if out and (out[-1][0], out[-1][1]) == k: out[-1][2] += max(d, 0.0)
        else: out.append([r, k[1], max(d, 0.0)])
    return out

def m7(bm): return bm[3] and bm[10] and not bm[4]
def d7(bm): return bm[4] and bm[10] and not bm[3]
def tri(bm): return int(any(bm[i] and bm[(i + 6) % 12] for i in range(6)))

def levy(x, y):
    x = np.asarray(x, float) - x[0]; y = np.asarray(y, float) - y[0]
    return 0.5 * float(np.sum(x[:-1] * y[1:] - x[1:] * y[:-1]))

def u_path(roots):
    f = [(7 * r) % 12 for r in roots]; u = [0]
    for a, b in zip(f, f[1:]): u.append(u[-1] + ((b - a + 5) % 12) - 5)
    return np.array(u, float)

def TE(toks):
    """G09-3: Levy area of the path (u_k, h_k) per chord change. nan if fewer than 6 tokens."""
    if len(toks) < 6: return np.nan
    u = u_path([t[0] for t in toks]); h = np.array([tri(t[1]) for t in toks], float)
    return levy(u, h) / (len(toks) - 1)

def ii_collapse(toks):
    """delete every m7 token immediately followed by a d7 token a fourth up; merge consecutive repeats again."""
    keep = [t for i, t in enumerate(toks)
            if not (i + 1 < len(toks) and m7(t[1]) and d7(toks[i + 1][1]) and (toks[i + 1][0] - t[0]) % 12 == 5)]
    out = []
    for t in keep:
        if out and (out[-1][0], out[-1][1]) == (t[0], t[1]): out[-1] = [t[0], t[1], out[-1][2] + t[2]]
        else: out.append(list(t))
    return out

def TR(toks):
    """G09-2: share of changes on the ii-collapsed path where a d7 moves to a root a fifth down ((r2-r1)%12 == 5) or a semitone
    down ((r2-r1)%12 == 11). nan if the collapsed path has < 6 tokens."""
    c = ii_collapse(toks)
    if len(c) < 6: return np.nan
    n = sum(1 for a, b in zip(c, c[1:]) if d7(a[1]) and (b[0] - a[0]) % 12 in (5, 11))
    return n / (len(c) - 1)

def TQ(t):
    """G09-1: lead-lag Levy area of the tension channel h per change = 1/2 * mean (h_k - h_{k-1})^2. nan if < 6 tokens."""
    if len(t) < 6: return np.nan
    h = np.array([tri(x[1]) for x in t], float)
    lead = np.repeat(h, 2)[1:]; lag = np.repeat(h, 2)[:-1]
    A = levy(lead, lag)
    assert abs(abs(A) - 0.5 * np.sum(np.diff(h) ** 2)) < 1e-9
    return abs(A) / (len(t) - 1)

def CH(toks):
    """run 07 chirality on the change tokens' roots (overlap report only)."""
    K = len(toks) - 1
    if K < 6: return np.nan
    th = [2 * math.pi * ((7 * t[0]) % 12) / 12 for t in toks]
    return 0.5 * sum(math.sin(th[i + 1] - th[i]) for i in range(K)) / K

# ================================================================ the Listener (checks_r09.py, checks_r09b.py; copied)
def n_bars(c):
    ch = c["chords"]
    return int(math.floor(ch[-1][0])) - int(math.floor(ch[0][0])) + 1

def dres_ful(c, seq):
    """R09-L2: DRES = resolved dom7 tokens (next root a fifth or a semitone down) per bar (bar-timed charts only);
    FUL = resolved / all dom7 tokens (>= 2 dom7)."""
    nb = n_bars(c) if c.get("timebase", "beats") == "beats" else np.nan
    ndom = nres = 0
    for i in range(len(seq) - 1):
        r1, b1 = seq[i][2], seq[i][3]; r2 = seq[i + 1][2]
        if d7(b1):
            ndom += 1
            if (r2 - r1) % 12 in (5, 11): nres += 1
    ful = nres / ndom if ndom >= 2 else np.nan
    dres = nres / nb if (np.isfinite(nb) and nb > 0) else np.nan
    return dres, ful

def carc(c, seq):
    """R09-L3 with the round-2 change: Levy area of (tau, N(tau)/N) = mean tau of resolution arrivals - 1/2, over the arrivals whose
    bar lies after the first 2 and before the last 2 bars of the chart (intros and endings dropped); >= 2 arrivals left. tau =
    (onset - first onset) / (last onset + 1 bar - first onset). Bar-timed charts only (the chair's timebase rule)."""
    ch = c["chords"]
    if c.get("timebase", "beats") != "beats": return np.nan
    t0 = ch[0][0]; tN = ch[-1][0] + 1.0
    if tN <= t0: return np.nan
    fb = int(math.floor(ch[0][0])); lb = int(math.floor(ch[-1][0]))
    arr = [(seq[i + 1][0] - t0) / (tN - t0) for i in range(len(seq) - 1)
           if d7(seq[i][3]) and (seq[i + 1][2] - seq[i][2]) % 12 in (5, 11) and fb + 2 <= math.floor(seq[i + 1][0]) <= lb - 2]
    return float(np.mean(arr) - 0.5) if len(arr) >= 2 else np.nan

# ================================================================ the Inventor (r09_measures.py, r09_vr4c.py; copied)
FIF = [(7 * p) % 12 for p in range(12)]
W5 = np.exp(-2j * np.pi * 5 * np.arange(12) / 12)

def step5(r1, r2):
    d = (FIF[r2] - FIF[r1]) % 12
    return d - 12 if d > 6 else d

def irr(toks):
    """R09-I1: (length of the stack-reduced change-token walk - 1) / n_chg (open walk)."""
    st = [toks[0]]
    for t in toks[1:]:
        if len(st) >= 2 and st[-2] == t: st.pop()
        else: st.append(t)
    return (len(st) - 1) / (len(toks) - 1)

def vr4(seq):
    roots = [seq[0][2]]
    for e in seq[1:]:
        if e[2] != roots[-1]: roots.append(e[2])
    s = np.array([step5(a, b) for a, b in zip(roots, roots[1:])], float)
    if len(s) < 8: return np.nan
    s4 = np.convolve(s, np.ones(4), "valid")
    return float(np.mean(s4 ** 2) / (4 * np.mean(s ** 2)))

def vr4c(seq):
    """R09-I2 revised: VR4 after dropping the m7 of each m7 -> dom7 a fourth up."""
    keep = [e for i, e in enumerate(seq) if not (i + 1 < len(seq) and (seq[i + 1][2] - e[2]) % 12 == 5 and m7(e[3]) and d7(seq[i + 1][3]))]
    return vr4(keep) if len(keep) > 1 else np.nan

def tension(r, bm):
    p = np.array([i for i in range(12) if bm[i]])
    return 1 - abs(W5[p].sum()) / len(p)

def quality(bm):
    return 1.0 if bm[4] else (-1.0 if bm[3] else 0.0)

def areas(seq, ch):
    """six level-2 Levy areas of the rectilinear path (tau, u, h, q): hold (tau moves), then jump. Areas without tau per change.
    Order: tu th tq uh uq hq. None if not computable."""
    cum, acc, prev = [], 0.0, None
    for t, d, r, bm, b in ch:
        tok = (r, tuple(bm))
        if tok != prev: cum.append(acc); prev = tok
        acc += max(d, 0.0)
    T = acc
    if not T > 0 or len(cum) != len(seq): return None
    if any(not any(e[3]) for e in seq): return None        # an empty bitmap has no tension value (the Inventor's nan case)
    u = 0.0; pts = []
    for k, (t, d, r, bm) in enumerate(seq):
        if k: u += step5(seq[k - 1][2], r)
        x = [cum[k] / T, u, tension(r, bm), quality(bm)]
        if pts: pts.append([x[0]] + pts[-1][1:])
        pts.append(x)
    pts.append([1.0] + pts[-1][1:])
    P = np.array(pts); P = P - P[0]; n = len(seq) - 1
    out = []
    for i in range(4):
        for j in range(i + 1, 4):
            a = 0.5 * np.sum(P[:-1, i] * P[1:, j] - P[1:, i] * P[:-1, j])
            out.append(float(a if i == 0 else a / n))
    return out

def _rank(v): return np.argsort(np.argsort(v, kind="stable"), kind="stable").astype(float)

def typicality(A_by_chart, group_of):
    """R09-I3: within each reference group, per-area mid-rank CDF F = (rank + 0.5) / n; TYP = mean_j |2 F_j - 1|;
    TYPM = Mahalanobis on normal scores (group covariance). Charts are taken in sorted id order (ties broken by that order)."""
    byg = collections.defaultdict(list)
    for k in sorted(A_by_chart):
        a = A_by_chart[k]
        if a is not None and all(np.isfinite(a)): byg[group_of[k]].append(k)
    TYPd, TYPMd = {}, {}
    for g, ks in byg.items():
        X = np.array([A_by_chart[k] for k in ks]); n = len(ks)
        if n < 60: continue
        F = np.column_stack([(_rank(X[:, j]) + 0.5) / n for j in range(X.shape[1])])
        Z = norm.ppf(F); Si = np.linalg.pinv(np.cov(Z.T))
        typ = np.abs(2 * F - 1).mean(1); typm = np.sqrt(np.einsum("ij,jk,ik->i", Z, Si, Z))
        for a, k in enumerate(ks): TYPd[k] = float(typ[a]); TYPMd[k] = float(typm[a])
    return TYPd, TYPMd, {g: len(v) for g, v in byg.items()}

# ================================================================ per chart
NEW = ["TR", "TQ", "TE", "DRES", "FUL", "CARC", "IRR", "VR4", "VR4c", "CH"]
BASE = ["IIV", "w_chr", "ch_rep", "V", "ln_chg", "ln_bars"]

def chart_row(c):
    lm = M8.listener_measures(c)
    if lm is None: return None, None
    toks, seq = M8.change_tokens(c["chords"])
    tw = tokens_with_dur(c["chords"])
    geo = M8.geometer_measures(c)
    beats = c.get("timebase", "beats") == "beats"
    row = dict(IIV=lm["IIV"], ch_rep=lm["ch_rep"], V=lm["V"], ln_chg=lm["ln_chg"], ln_bars=(lm["ln_bars"] if beats else np.nan),
               w_chr=geo["w_chr"])
    dres, ful = dres_ful(c, seq)
    row.update(TR=TR(tw), TQ=TQ(tw), TE=TE(tw), DRES=dres, FUL=ful, CARC=carc(c, seq), IRR=irr(toks), VR4=vr4(seq), VR4c=vr4c(seq),
               CH=CH(tw))
    return {k: float(v) for k, v in row.items()}, areas(seq, c["chords"])

def unit_tests():
    M7 = (1,0,0,1,0,0,0,1,0,0,1,0); D7 = (1,0,0,0,1,0,0,1,0,0,1,0); MA = (1,0,0,0,1,0,0,1,0,0,0,0)
    assert abs(levy(u_path([2, 7, 0]), [tri(M7), tri(D7), tri(MA)]) - 1.0) < 1e-12          # ii-V-I: +1 (G09-3)
    assert abs(levy(u_path([5, 7, 0]), [tri(MA), tri(D7), tri(MA)]) + 0.5) < 1e-12          # IV-V7-I: -1/2
    a = [[0, MA, 1], [2, M7, 1], [7, D7, 1], [0, MA, 1]]; b = [[0, MA, 1], [7, D7, 2], [0, MA, 1]]
    assert [x[:2] for x in ii_collapse(a)] == [x[:2] for x in ii_collapse(b)]                 # a ii cannot move TR
    P = np.array([[0, 8], [1, 4], [2, 5], [3, 1], [4, 10], [5, 3]], float)
    assert abs(levy(P[:, 0], P[:, 1]) - 2.0) < 1e-12                                          # card 1 Eq. 37-39: A = 2
    assert irr(list("CGCGC")) == 0.0 and abs(irr(list("CFCGFC")) - 0.6) < 1e-12 and irr(list("ABCA")) == 1.0
    chain = [(0, 1, (5 * k) % 12, None) for k in range(12)]; assert abs(vr4(chain) - 4) < 1e-12
    loop = [(0, 1, r, None) for r in [0, 9, 2, 7] * 4]; assert vr4(loop) == 0.0
    # TR: C Dm7 G7 C Dm7 G7 C Db7 C -> collapsed C G7 C G7 C Db7 C: G7->C twice, Db7->C once, over 6 changes
    t = [[0, MA, 1], [2, M7, 1], [7, D7, 1], [0, MA, 1], [2, M7, 1], [7, D7, 1], [0, MA, 1], [1, D7, 1], [0, MA, 1]]
    assert abs(TR(t) - 3 / 6) < 1e-12                                                          # G7->C twice, Db7->C once, 6 changes
    return True

# ================================================================ main
def rank(v): return np.argsort(np.argsort(v)).astype(float)
def spear(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); ok = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(rank(a[ok]), rank(b[ok]))[0, 1]) if ok.sum() > 10 else float("nan")

def song_means(ks, per, meas):
    rows = [per[k] for k in ks if k in per]; d = {}
    for m in meas:
        v = [r[m] for r in rows if r.get(m) is not None and np.isfinite(r[m])]
        d[m] = float(np.mean(v)) if v else None
    return d, len(rows)

def main():
    t0 = time.time(); unit_tests()
    info, S = C9.load_design()
    charts = C9.load_charts(); cb = {c["id"]: c for c in charts}
    print("charts loaded", len(charts), round(time.time() - t0), "s", flush=True)
    # ---- every chart of load_charts(): base + new measures + areas (the TYP reference pool needs the areas of all of them)
    per = {}; A = {}; grp = {}
    for c in charts:
        r, a = chart_row(c)
        if r is None: continue
        per[c["id"]] = r; A[c["id"]] = a; grp[c["id"]] = C9.coarse_genre(c)
    TYPd, TYPMd, refn = typicality(A, grp)
    for k, r in per.items():
        r["TYP"] = TYPd.get(k, float("nan")); r["TYPM"] = TYPMd.get(k, float("nan"))
    print("charts measured", len(per), "TYP reference sizes", refn, round(time.time() - t0), "s", flush=True)
    MEAS = BASE + NEW + ["TYP", "TYPM"]
    design_charts = {k for s in S for k in s["charts"]}
    per_design = {k: per[k] for k in sorted(design_charts) if k in per}
    songs = {}
    for s in S:
        d, n = song_means(s["charts"], per, MEAS)
        rbb = [k for k in s["charts"] if cb[k]["part"] in ("real-book", "biab-internet-corpus")]
        d_rb, n_rb = song_means(rbb, per, BASE)
        d["n_charts_measured"] = n; d["n_rbb_measured"] = n_rb
        d["no_bars"] = int(not any(cb[k].get("timebase", "beats") == "beats" and k in per for k in s["charts"]))
        for m in BASE: d[m + "_rbb"] = d_rb[m]
        songs[s["clique"]] = d
    print("design songs", len(S), "with a measured chart", sum(v["n_charts_measured"] > 0 for v in songs.values()),
          round(time.time() - t0), "s", flush=True)
    # ---- SEEN08: run 08 songs (fields 'clique' and 'charts' only) and their upstream (real-book / BiaB) charts
    D8 = json.load(open(RUN08_DATA))
    s8 = [dict(clique=v["clique"], charts=list(v["charts"])) for v in D8["songs"]]; del D8
    c8 = {c["id"]: c for c in json.load(open(os.path.join(C9.DL, "choco", "charts_run08.json")))}
    per8 = {}
    for s in s8:
        for k in s["charts"]:
            if k in per8 or k not in c8: continue
            r, _ = chart_row(c8[k])
            if r is not None: per8[k] = {m: r[m] for m in BASE + ["DRES", "TR"]}
    vmap = collections.defaultdict(set)
    for s in s8:
        for k in s["charts"]:
            if k in c8:
                for v in C8.variants(c8[k]["title"]): vmap[v].add(s["clique"])
    up = collections.defaultdict(list); upstat = collections.Counter()
    for c in charts:
        if c["part"] not in ("real-book", "biab-internet-corpus") or len(c["chords"]) < 8: continue
        if c["id"] in design_charts: upstat["in_run09_design"] += 1; continue
        raw = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", c["title"]).split(" - ")[0]
        if len(raw.split()) < 2: upstat["one_word"] += 1; continue
        cand = set().union(*[vmap.get(v, set()) for v in C8.variants(c["title"])]) if C8.variants(c["title"]) else set()
        if len(cand) != 1: upstat["no_match" if not cand else "not_unique"] += 1; continue
        if c["id"] not in per: upstat["unmeasured"] += 1; continue
        up[cand.pop()].append(c["id"]); upstat["matched"] += 1
    seen = {}
    for s in s8:
        ks = [k for k in s["charts"] if k in c8]
        d, n = song_means(ks, per8, BASE + ["DRES", "TR"])
        ir = [k for k in ks if c8[k]["part"].startswith("ireal")]
        di, ni = song_means(ir, per8, BASE)
        d.update({m + "_ireal": di[m] for m in BASE}); d["n_ireal"] = ni; d["n_charts_measured"] = n
        gen = collections.Counter(C8.genre_of(c8[k]) for k in ks)
        d["genre8"] = sorted(gen.items(), key=lambda x: (-x[1], x[0]))[0][0] if gen else None
        ups = sorted(up.get(s["clique"], []))
        du, nu = song_means(ups, per, BASE)
        d.update({m + "_up": du[m] for m in BASE}); d["n_up"] = nu; d["up_charts"] = ups
        d["up_parts"] = sorted({cb[k]["part"] for k in ups})
        seen[s["clique"]] = d
    print("seen08 songs", len(seen), "with upstream", sum(v["n_up"] > 0 for v in seen.values()),
          "with iReal and upstream", sum(v["n_up"] > 0 and v["n_ireal"] > 0 for v in seen.values()), dict(upstat),
          round(time.time() - t0), "s", flush=True)
    json.dump(dict(note="run 09 notes-side measures (measures09.py); song value = unweighted mean over its measured charts; "
                        "ln_bars, DRES, CARC missing on seconds-timed charts; seen08 = run 08 songs (clique and chart ids only read)",
                   songs=songs, charts=per_design, seen08=seen, seen08_upstream_match=dict(upstat), typ_reference_sizes=refn),
              open(OUT, "w"), sort_keys=True)
    # ================================================================ gates (notes only)
    G = dict(note="run 09 chair measure gates, notes only, on the 1,283 unseen design songs. coverage = songs with a defined value; "
                  "stability = Spearman between the first two NON-IDENTICAL measured charts (sorted ids; chord lists differ) of a design "
                  "song, and the stricter reading where the change tokens also differ; overlap = song-level Spearman over the design "
                  "(pooled, and genre-demeaned ranks = within genre). GATE (frozen before any outcome): a measure is stopped if |rho| > 0.8 "
                  "with ch_rep or with V (pooled or within genre). Two-chart stability under 0.5 is flagged (run 08's second gate) and "
                  "stops a measure only when its pairs number 100 or more.", n_songs=len(S), n_design_charts=len(per_design))
    ALL = MEAS
    cov = {m: int(sum(songs[s["clique"]][m] is not None for s in S)) for m in ALL}
    G["coverage_songs"] = cov
    G["coverage_by_genre"] = {g: {m: int(sum(songs[s["clique"]][m] is not None for s in S if s["genre"] == g)) for m in ALL}
                              for g in sorted({s["genre"] for s in S})}
    pairs, pairs_tok = [], []
    for s in S:
        ks = sorted(k for k in s["charts"] if k in per)
        for i in range(len(ks)):
            j = next((j for j in range(i + 1, len(ks)) if cb[ks[j]]["chords"] != cb[ks[i]]["chords"]), None)
            if j is not None: pairs.append((ks[i], ks[j])); break
        for i in range(len(ks)):
            j = next((j for j in range(i + 1, len(ks)) if M8.change_tokens(cb[ks[j]]["chords"])[0] != M8.change_tokens(cb[ks[i]]["chords"])[0]), None)
            if j is not None: pairs_tok.append((ks[i], ks[j])); break
    def st(pr, m):
        a = [per[p][m] for p, q in pr]; b = [per[q][m] for p, q in pr]
        ok = np.isfinite(a) & np.isfinite(b); return round(spear(a, b), 3), int(ok.sum())
    G["stability"] = {m: dict(two_chart=st(pairs, m)[0], n=st(pairs, m)[1], tokens_differ=st(pairs_tok, m)[0], n_tok=st(pairs_tok, m)[1])
                      for m in ALL}
    G["pair_parts"] = dict(collections.Counter("|".join(sorted((cb[p]["part"], cb[q]["part"]))) for p, q in pairs))
    gen = np.array([s["genre"] for s in S])
    def col(m): return np.array([np.nan if songs[s["clique"]][m] is None else songs[s["clique"]][m] for s in S])
    def wg(m):
        v = col(m); r = np.full(len(v), np.nan); ok = np.isfinite(v); r[ok] = rank(v[ok])
        out = np.full(len(v), np.nan)
        for g in np.unique(gen):
            i = np.nonzero((gen == g) & ok)[0]
            if len(i) >= 2: out[i] = r[i] - r[i].mean()
        return out
    REF = ["ch_rep", "V", "IIV", "ln_chg", "TR"]
    G["spearman_pooled"] = {m: {o: round(spear(col(m), col(o)), 3) for o in REF} for m in ALL}
    G["spearman_within_genre"] = {m: {o: round(spear(wg(m), wg(o)), 3) for o in REF} for m in ALL}
    gates = {}
    for m in ["IIV", "TR", "DRES", "TQ", "IRR", "VR4c", "TYP", "CARC", "TE"]:
        o = [G["spearman_pooled"][m]["ch_rep"], G["spearman_pooled"][m]["V"], G["spearman_within_genre"][m]["ch_rep"],
             G["spearman_within_genre"][m]["V"]]
        stb = G["stability"][m]
        renamed = any(abs(x) > 0.8 for x in o if np.isfinite(x))
        unstable = stb["n"] >= 100 and np.isfinite(stb["two_chart"]) and stb["two_chart"] < 0.5
        gates[m] = dict(max_abs_rho_chrep_or_V=round(max(abs(x) for x in o if np.isfinite(x)), 3), two_chart=stb["two_chart"],
                        n_pairs=stb["n"], coverage=cov[m], passes=bool(not renamed and not unstable),
                        flag=("renamed" if renamed else "") + (" unstable" if unstable else ""))
    G["gates"] = gates
    G["design_by_genre"] = dict(collections.Counter(gen.tolist()))
    G["sha256_measures_json"] = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    json.dump(G, open(GATES, "w"), indent=1)
    print(json.dumps(gates, indent=1)); print("pairs", len(pairs), "token-differ pairs", len(pairs_tok)); print("done", round(time.time() - t0), "s")

if __name__ == "__main__":
    main()
