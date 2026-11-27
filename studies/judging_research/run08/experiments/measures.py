"""Run 08 measures, frozen by the chair before any outcome is joined. NOTES ONLY: this file reads the chart cache
($DL/choco/charts_run08.json) and the design ($DL/choco/design_run08.json, clique ids / composer / genre / chart ids, no counts or
years). It never reads $SHAPE, $DL/discogs or any covers/versions file, and it never calls common.load_outcomes/load_timelines.

Usage (from this folder):  python3 -I measures.py
Writes  $DL/choco/measures_run08.json   (per song: the unweighted mean over its charts of every measure; per chart: every value;
                                          per song: the I2 neighbour lists)
        ./measure_gates.json             (two-chart stability, iReal-vs-Wikifonia agreement, within-composer overlaps, gates)

Every recipe below is copied from the imaginers' scripts (not imported), so the repo holds the code that is frozen:
  /home/claude/scripts/listener/checks_r1.py   ch_rep, V, n_chg, ln_chg, ln_bars, TRAV5, TRAVL1, IIV      (listener_measures)
  /home/claude/scripts/inventor/i_measures.py  E, spread (global fifths spread), interval trigrams          (inventor_measures)
  /home/claude/scripts/inventor/i_neighbours.py the I2 neighbour rule (tf-idf cosine on interval trigrams)  (neighbours)
  /home/claude/scripts/geometer/g_measures.py  w_chr (w-bar), econ (=econ2), L_rep, T_rep                  (geometer_measures)
  run06/experiments/common.py H_song + run 03 QUAL tokens  tonic resistance H (R03-I2), now with the chart's written key
  run07/experiments/chair_gates.py pmin_of             the obtuse statue p_min (R03-G3)
  run07/experiments/common.py song_shape               loop period lnP (R07-L2, adapted to chart length) and burstiness B (R07-I3)
"""
import sys, os, json, math, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.sparse.csgraph import connected_components
import common as C

OUT = os.path.join(C.DL, "choco", "measures_run08.json")
GATES = os.path.join(C.HERE, "measure_gates.json")
FIFTHS = np.array([(7 * i) % 12 for i in range(12)])   # pc -> position on the circle of fifths

def pcs(root, bm): return [(root + i) % 12 for i in range(12) if bm[i]]

def cemd(h, g):
    """card 1, Eq. 12: circular W1 between two 12-bin probability vectors = sum |D - median(D)|, D = F - G (in bin steps)."""
    D = np.cumsum(h) - np.cumsum(g)
    return float(np.abs(D - np.median(D)).sum())

def to_fifths(h):
    out = np.zeros(12)
    for pc in range(12): out[(7 * pc) % 12] += h[pc]
    return out

def change_tokens(ch):
    """(root, bitmap) tokens with consecutive repeats collapsed, and the matching events."""
    toks, seq = [], []
    for t, d, r, bm, b in ch:
        tok = (r, tuple(bm))
        if not toks or toks[-1] != tok:
            toks.append(tok); seq.append((t, d, r, bm))
    return toks, seq

# ---------------------------------------------------------------- the Listener (checks_r1.py, measures(), unchanged)
def listener_measures(c):
    ch = c["chords"]
    if len(ch) < 8: return None
    toks, seq = change_tokens(ch)
    if len(toks) < 6: return None
    grams = [tuple(toks[i:i + 3]) for i in range(len(toks) - 2)]
    seen = set(); rep = 0
    for g in grams:
        rep += g in seen; seen.add(g)
    ch_rep = rep / len(grams)
    V = len(set(toks)); n_chg = len(toks) - 1
    bars = int(math.floor(ch[-1][0])) + 1
    win = collections.defaultdict(lambda: np.zeros(12))
    for t, d, r, bm, b in ch:
        p = pcs(r, bm); w = max(d, 1e-6) / len(p)
        for q in p: win[int(math.floor(t)) // 4][q] += w
    ks = sorted(k for k in win if win[k].sum() > 0)
    out = dict(ch_rep=ch_rep, V=V, n_chg=n_chg, ln_bars=math.log(bars), ln_chg=math.log(n_chg), TRAV5=np.nan, TRAVL1=np.nan)
    if len(ks) >= 3:
        W = [to_fifths(win[k] / win[k].sum()) for k in ks]
        Wc = [win[k] / win[k].sum() for k in ks]
        out["TRAV5"] = float(np.mean([cemd(W[i], W[i + 1]) for i in range(len(W) - 1)]))
        out["TRAVL1"] = float(np.mean([np.abs(Wc[i] - Wc[i + 1]).sum() for i in range(len(W) - 1)]))
    def m7(bm): return bm[3] and bm[10] and not bm[4]
    def d7(bm): return bm[4] and bm[10] and not bm[3]
    iiv = 0
    for i in range(len(seq) - 1):
        r1, b1 = seq[i][2], seq[i][3]; r2, b2 = seq[i + 1][2], seq[i + 1][3]
        if (r2 - r1) % 12 == 5 and m7(b1) and d7(b2): iiv += 1
    out["IIV"] = iiv / n_chg
    return out

# ---------------------------------------------------------------- the Inventor (i_measures.py, per_chart(), unchanged in substance)
def inventor_measures(c):
    ch = c["chords"]
    toks, _ = change_tokens(ch); seq = toks
    bars = collections.defaultdict(lambda: np.zeros(12))
    for (t, d, r, bm, b) in ch:
        p = pcs(r, bm)
        if not p: continue
        for q in p: bars[int(math.floor(t + 1e-9))][q] += d / len(p)
    tri = set(((b[0] - a[0]) % 12, (cc[0] - b[0]) % 12, a[1], b[1], cc[1]) for a, b, cc in zip(seq, seq[1:], seq[2:]))
    out = dict(E=np.nan, spread=np.nan, tri=tri, B=None)
    if not bars: return out
    b0, b1 = min(bars), max(bars); nb = b1 - b0 + 1
    B = np.zeros((nb, 12))
    for k, v in bars.items(): B[k - b0] = v
    for i in range(1, nb):                      # carry-over: an empty bar keeps the previous bar's profile
        if B[i].sum() == 0: B[i] = B[i - 1]
    out["B"] = B
    G = B.sum(0); G = G / G.sum(); Gf = to_fifths(G)
    out["spread"] = min(cemd(Gf, np.eye(12)[m]) for m in range(12))
    wins = []
    for s in range(0, nb - 4 + 1, 4):
        v = B[s:s + 4].sum(0)
        if v.sum() > 0: wins.append(v / v.sum())
    if len(wins) >= 2:
        out["E"] = float(np.mean([cemd(to_fifths(v), Gf) for v in wins]))
    return out

# ---------------------------------------------------------------- the Geometer (g_measures.py: w_chr, econ2 -> econ, L_rep, T_rep)
_w1c = {}
def w1_chr(a, b):
    if a == b: return 0.0
    k = (a, b) if a < b else (b, a); v = _w1c.get(k)
    if v is None:
        ha = np.zeros(12); hb = np.zeros(12)
        for p in a: ha[p] += 1
        for p in b: hb[p] += 1
        v = cemd(ha / ha.sum(), hb / hb.sum()); _w1c[k] = v
    return v

def geometer_measures(c):
    ev = c["chords"]; nan = dict(w_chr=np.nan, econ=np.nan, L_rep=np.nan, T_rep=np.nan)
    if len(ev) < 8: return nan
    pcsets = [tuple(sorted({(e[2] + i) % 12 for i, b in enumerate(e[3]) if b})) for e in ev]
    rq = [(e[2], tuple(e[3])) for e in ev]
    seq = [pcsets[0]]
    for s in pcsets[1:]:
        if s != seq[-1]: seq.append(s)
    n = len(seq)
    if n < 6: return nan
    sc = [w1_chr(seq[i], seq[i + 1]) for i in range(n - 1)]
    w_chr = float(np.mean(sc))
    types = collections.Counter(seq); tl = list(types.items()); num = 0.0
    for i, (a, na) in enumerate(tl):
        for b, nb in tl[i + 1:]: num += 2 * na * nb * w1_chr(a, b)
    ndiff = n * n - sum(v * v for v in types.values())
    pair2 = num / ndiff if ndiff > 0 else np.nan
    econ = 1 - w_chr / pair2 if pair2 and pair2 > 0 else np.nan
    rqc = [rq[0]]
    for x in rq[1:]:
        if x != rqc[-1]: rqc.append(x)
    lit = set(); shp = set(); L = O = 0; m = len(rqc) - 2
    for i in range(m):
        (r1, q1), (r2, q2), (r3, q3) = rqc[i:i + 3]
        sh = (q1, (r2 - r1) % 12, q2, (r3 - r2) % 12, q3); li = (r1, sh)
        if li in lit: L += 1
        if sh in shp: O += 1
        lit.add(li); shp.add(sh)
    L_rep = L / m if m > 0 else np.nan; O_rep = O / m if m > 0 else np.nan
    return dict(w_chr=w_chr, econ=econ, L_rep=L_rep, T_rep=O_rep - L_rep)

# ---------------------------------------------------------------- R03-I2 tonic resistance H and R03-G3 p_min (run 03 tokens)
QUAL = {(4, 3): 0, (3, 4): 1, (3, 3): 2, (4, 4): 3, (4, 3, 3): 4, (4, 3, 4): 5, (3, 4, 3): 6, (3, 3, 4): 2, (3, 3, 3): 2, (5, 2): 7, (2, 5): 7}
def qual_bm(bm):
    """run 03's quality code from stacked intervals; the chart's bitmap (relative to the root, within one octave) is read as its
    sorted tones from the root, and the stacked intervals are their successive differences."""
    ivs = [i for i in range(12) if bm[i]]
    if not ivs or ivs[0] != 0: ivs = [0] + ivs
    return QUAL.get(tuple(np.diff(ivs).tolist()), 8)

def rel_tokens(c):
    """run 03 tokens_rel on a chart: ((root - written tonic) % 12) * 9 + quality, consecutive repeats merged. None without a key."""
    if not c.get("key"): return None
    tonic = c["key"][0]; out = []
    for t, d, r, bm, b in c["chords"]:
        tok = ((r - tonic) % 12) * 9 + qual_bm(bm)
        if not out or out[-1] != tok: out.append(tok)
    return out

def _resist(W):
    Qd = np.linalg.pinv(np.diag(W.sum(1)) - W); d = np.diag(Qd)
    return d[:, None] + d[None, :] - 2 * Qd

def H_song(seqs):
    """run 06 common.H_song, unchanged: tonic resistance. Returns (H or nan, distinct tokens n, links)."""
    names = sorted(set(t for s in seqs for t in s)); ix = {t: i for i, t in enumerate(names)}; M = np.zeros((len(names), len(names)))
    for s in seqs:
        for x, y in zip(s, s[1:]): M[ix[x], ix[y]] += 1
        if len(s) > 1 and s[-1] != s[0]: M[ix[s[-1]], ix[s[0]]] += 1
    n = len(names); Cm = M + M.T; np.fill_diagonal(Cm, 0); links = int((np.triu(Cm, 1) > 0).sum())
    if n < 3: return np.nan, n, links
    cand = [i for i, t in enumerate(names) if t // 9 == 0]
    if not cand: return np.nan, n, links
    rs = Cm.sum(1); T = min(cand, key=lambda i: (-rs[i], names[i]))
    _, lab = connected_components(Cm > 0, directed=False); idx = np.nonzero(lab == lab[T])[0]
    if len(idx) < 3: return np.nan, n, links
    Cs = Cm[np.ix_(idx, idx)]; t = int(np.nonzero(idx == T)[0][0]); om = _resist(Cs); pi = Cs.sum(1) / Cs.sum()
    return float(pi @ om[:, t] / (pi @ om @ pi)), n, links

def pmin_of(t):
    """run 07 chair_gates.pmin_of, unchanged: min resistance curvature of the unit-weight chord graph (largest piece, wrap move)."""
    names = sorted(set(t)); ix = {x: i for i, x in enumerate(names)}; n = len(names); M = np.zeros((n, n))
    for a, b in zip(t, t[1:]): M[ix[a], ix[b]] += 1
    if len(t) > 1 and t[-1] != t[0]: M[ix[t[-1]], ix[t[0]]] += 1
    A = ((M + M.T) > 0).astype(float); np.fill_diagonal(A, 0); links = int(np.triu(A, 1).sum())
    npc, lab = connected_components(A, directed=False)
    big = max(range(npc), key=lambda p: ((lab == p).sum(), -p)); idx = np.nonzero(lab == big)[0]
    if len(idx) < 3: return np.nan, n, links
    Ap = A[np.ix_(idx, idx)]; p = 1 - 0.5 * (Ap * _resist(Ap)).sum(1); return float(p.min()), n, links

def unit_tests():
    def cyc(k): return [i * 9 for i in range(k)]                     # tokens of distinct roots, quality 0; wrap closes the cycle
    assert abs(H_song([cyc(5)]) [0] - 1.0) < 1e-9
    star_hub = [[0, 9, 0, 18, 0, 27]]                                  # T (root 0) at the hub of a 3-leaf star
    star_leaf = [[9, 0, 9, 18, 9, 27]]                                 # T on a leaf
    assert abs(H_song(star_hub)[0] - 0.6) < 1e-9 and abs(H_song(star_leaf)[0] - 1.4) < 1e-9
    assert abs(pmin_of([0, 1, 2, 3])[0] - 0.25) < 1e-9                 # 4-cycle (wrap)
    assert abs(pmin_of([1, 0, 2, 0, 3, 0])[0] + 0.5) < 1e-9            # star with 3 leaves
    h = np.zeros(12); h[[0, 4, 7]] = 1 / 3; g = np.zeros(12); g[[0, 5, 9]] = 1 / 3
    assert abs(cemd(h, g) - 1.0) < 1e-9                                 # card 1: C -> F = 1 (chromatic)
    g = np.zeros(12); g[[1, 5, 8]] = 1 / 3
    assert abs(cemd(to_fifths(h), to_fifths(g)) - 3.0) < 1e-9          # card 1: C -> Db = 3 on the fifths circle

# ---------------------------------------------------------------- R07-L2 loop period and R07-I3 burstiness (run 07 song_shape)
def loop_period(B):
    """R07-L2 on a chart: bar profiles (the Inventor's duration-weighted, carried-over bars), L1 per bar; D_l = mean over bars of
    the squared Euclidean distance between bar i and bar i+l, for l = 2 .. min(16, nb // 2); P = the smallest argmin; lnP = ln P.
    Run 07 needed 34 bars (lags to 16 on MIDI songs); a one-chorus chart is often 32 bars, so the chart form needs 18 bars and lets
    the longest lag be half the chart (stated adaptation)."""
    if B is None: return np.nan
    S = B[B.sum(1) > 0]
    if len(S) < 18: return np.nan
    L1 = S / S.sum(1, keepdims=True); top = min(16, len(L1) // 2)
    Dl = [((L1[l:] - L1[:-l]) ** 2).sum(1).mean() for l in range(2, top + 1)]
    return math.log(2 + int(np.argmin(Dl)))

def burstiness(t):
    """R07-I3 (run 07 song_shape B, unchanged) on the change tokens."""
    pos = collections.defaultdict(list)
    for i, c in enumerate(t): pos[c].append(i)
    rr = []
    for c, p in pos.items():
        if len(p) >= 3:
            g = np.diff(p).astype(float); rr.extend(g / g.mean())
    return float((np.std(rr) - 1) / (np.std(rr) + 1)) if len(rr) >= 6 else np.nan

MEAS = ["ch_rep", "V", "n_chg", "ln_chg", "ln_bars", "TRAV5", "TRAVL1", "E", "spread", "w_chr", "econ", "L_rep", "T_rep", "IIV",
        "H", "H_links", "pmin", "pmin_links", "lnP", "B"]

def chart_row(c):
    m = listener_measures(c)
    if m is None: return None, None
    inv = inventor_measures(c); geo = geometer_measures(c)
    m.update(E=inv["E"], spread=inv["spread"], **geo)
    rt = rel_tokens(c)
    if rt is not None and len(set(rt)) >= 3:
        h, n, lk = H_song([rt]); m["H"] = h; m["H_links"] = math.log(max(lk, 1))
        p, n2, lk2 = pmin_of(rt); m["pmin"] = p; m["pmin_links"] = math.log(max(lk2, 1))
    else:
        m["H"] = m["H_links"] = m["pmin"] = m["pmin_links"] = np.nan
    m["lnP"] = loop_period(inv["B"])
    m["B"] = burstiness(change_tokens(c["chords"])[0])
    return {k: (float(m[k]) if m[k] is not None else np.nan) for k in MEAS}, inv["tri"]

# ---------------------------------------------------------------- R08-I2: the neighbour rule (frozen)
def neighbours(S, cb, tri, K=10, jmax=0.4):
    """For each design song: its representative chart = the first of its sorted chart ids with at least one interval trigram.
    Songs are binary tf-idf vectors on interval-coded trigrams ((r2-r1)%12, (r3-r2)%12, q1, q2, q3), idf = ln((N+1)/(df+1)) + 1 over
    the design songs, L2-normalised; similarity = cosine. A candidate j for song i must: be another design song (another clique);
    have another composer key; share no name token (common.tokens over all the song's charts' artists strings); share no title
    variant (common.variants of the representative charts' titles); have trigram-set Jaccard < 0.4 with i (contrafacts of one parent
    dropped, the Inventor's round 3); and have cosine > 0. Neighbours = the K most similar candidates (ties: clique id).
    Returns {clique: [[clique_j, cos], ...]} for K = 10 (the first 5 give the K = 5 reading)."""
    rep = {}
    for s in S:
        for k in s["charts"]:
            if k in tri and tri[k]: rep[s["clique"]] = k; break
    cl = [s["clique"] for s in S if s["clique"] in rep]; info = {s["clique"]: s for s in S}
    vocab = {}; rows = []; cols = []
    for n, q in enumerate(cl):
        for t in tri[rep[q]]: cols.append(vocab.setdefault(t, len(vocab))); rows.append(n)
    from scipy import sparse
    X = sparse.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(cl), len(vocab)))
    df = np.asarray(X.sum(0)).ravel(); idf = np.log((len(cl) + 1) / (df + 1)) + 1; X = X @ sparse.diags(idf)
    nr = np.sqrt(np.asarray(X.multiply(X).sum(1)).ravel()); X = (sparse.diags(1 / np.maximum(nr, 1e-12)) @ X).tocsr()
    toks = {q: set().union(*[set(C.tokens(cb[k]["artists"])) for k in info[q]["charts"]]) for q in cl}
    tv = {q: C.variants(cb[rep[q]]["title"]) for q in cl}
    comp = {q: info[q]["composer"] for q in cl}
    out = {}
    for s0 in range(0, len(cl), 1000):
        Sm = (X[s0:s0 + 1000] @ X.T).toarray()
        for a in range(Sm.shape[0]):
            i = s0 + a; qi = cl[i]; order = np.lexsort((np.arange(len(cl)), -Sm[a])); got = []
            for j in order:
                if Sm[a, j] <= 0 or len(got) == K: break
                qj = cl[j]
                if j == i or comp[qj] == comp[qi] or (toks[qj] & toks[qi]) or (tv[qj] & tv[qi]): continue
                A, Bq = tri[rep[qi]], tri[rep[qj]]
                if len(A & Bq) / len(A | Bq) >= jmax: continue
                got.append([qj, round(float(Sm[a, j]), 6)])
            out[qi] = got
    return out, rep, (X, cl, vocab, idf)

# ---------------------------------------------------------------- run
def rank(v): return np.argsort(np.argsort(v)).astype(float)
def spear(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); ok = np.isfinite(a) & np.isfinite(b)
    return float(np.corrcoef(rank(a[ok]), rank(b[ok]))[0, 1]) if ok.sum() > 10 else float("nan")

def main():
    t0 = time.time(); unit_tests()
    info, S = C.load_design(); cb = C.charts_by_id()
    per = {}; tri = {}
    for s in S:
        for k in s["charts"]:
            if k in per: continue
            r, tr = chart_row(cb[k])
            if r is not None: per[k] = r; tri[k] = tr
    print("charts measured", len(per), "of", sum(len(s["charts"]) for s in S), round(time.time() - t0), "s", flush=True)
    songs = {}
    for s in S:
        rows = [per[k] for k in s["charts"] if k in per]
        d = {}
        for m in MEAS:
            v = [r[m] for r in rows if np.isfinite(r[m])]
            d[m] = float(np.mean(v)) if v else None
        d["n_charts_measured"] = len(rows)
        songs[s["clique"]] = d
    nb, rep, _ = neighbours(S, cb, tri)
    print("neighbours", len(nb), round(time.time() - t0), "s", flush=True)
    json.dump(dict(note="run 08 notes-side measures (measures.py); song value = unweighted mean over its measured charts",
                   songs=songs, charts=per, neighbours=nb, rep_chart=rep), open(OUT, "w"))
    # ------------------------------------------------ gates and summary (notes only)
    G = dict(note="run 08 chair measure gates, notes only. stability = Spearman between the first two NON-IDENTICAL measured charts "
                  "(sorted ids, chord lists differ) of each design song; cross-source = first iReal vs first Wikifonia chart of one "
                  "song; within-composer overlaps = Spearman of composer-demeaned song values (composers with >= 2 songs with both "
                  "values). Gates frozen before any outcome: two-chart stability >= 0.5 and |within-composer rho| <= 0.8 with ch_rep "
                  "and with V (else 'renamed').", n_songs=len(S), n_charts=len(per))
    pairs, xs = [], []
    for s in S:
        ks = [k for k in s["charts"] if k in per]
        for i in range(len(ks)):
            j = next((j for j in range(i + 1, len(ks)) if cb[ks[j]]["chords"] != cb[ks[i]]["chords"]), None)
            if j is not None: pairs.append((ks[i], ks[j])); break
        ir = [k for k in ks if cb[k]["part"] != "wikifonia"]; wf = [k for k in ks if cb[k]["part"] == "wikifonia"]
        if ir and wf: xs.append((ir[0], wf[0]))
    G["pairs_nonidentical"] = len(pairs); G["pairs_cross_source"] = len(xs)
    # residual stability: each chart's value after OLS on its own size block (ch_rep, V, ln V, ln_chg, ln_bars), stacked
    allk = list(per)
    Z = np.array([[per[k][m] for m in ("ch_rep", "V", "ln_chg", "ln_bars")] for k in allk])
    Zc = np.column_stack([np.ones(len(Z)), Z, np.log(Z[:, 1])]); pos = {k: i for i, k in enumerate(allk)}
    def resid(m):
        y = np.array([per[k][m] for k in allk]); ok = np.isfinite(y); r = np.full(len(y), np.nan)
        b, *_ = np.linalg.lstsq(Zc[ok], y[ok], rcond=None); r[ok] = y[ok] - Zc[ok] @ b; return r
    stab = {}
    for m in MEAS:
        a = [per[p][m] for p, q in pairs]; b = [per[q][m] for p, q in pairs]
        x1 = [per[p][m] for p, q in xs]; x2 = [per[q][m] for p, q in xs]
        r = resid(m) if m not in ("ch_rep", "V", "ln_chg", "ln_bars", "n_chg") else None
        rs = spear([r[pos[p]] for p, q in pairs], [r[pos[q]] for p, q in pairs]) if r is not None else None
        stab[m] = dict(two_chart=round(spear(a, b), 3), two_chart_resid_size=(round(rs, 3) if rs is not None else None),
                       cross_source=round(spear(x1, x2), 3), n_pairs=int(sum(np.isfinite(a) & np.isfinite(b))),
                       songs_defined=int(sum(songs[s["clique"]][m] is not None for s in S)))
    G["stability"] = stab
    # within-composer overlaps
    comp = np.array([s["composer"] for s in S])
    def wcol(m):
        v = np.array([np.nan if songs[s["clique"]][m] is None else songs[s["clique"]][m] for s in S]); return v
    W = {}
    for m in MEAS:
        v = wcol(m); out = np.full(len(v), np.nan)
        for g in np.unique(comp):
            i = np.nonzero((comp == g) & np.isfinite(v))[0]
            if len(i) >= 2: out[i] = v[i] - v[i].mean()
        W[m] = out
    G["within_composer_spearman"] = {m: {n: round(spear(W[m], W[n]), 3) for n in MEAS} for m in MEAS}
    # within-composer share of variance
    G["within_share"] = {m: round(float(np.nanvar(W[m]) / np.nanvar(wcol(m)[np.isfinite(W[m])])), 3) for m in MEAS}
    # I2 neighbour checks: similarity, neighbour-set overlap between two charts of one song (second chart as a query)
    sims = [np.mean([c for _, c in v]) for v in nb.values() if v]
    G["I2"] = dict(songs_with_10=int(sum(len(v) == 10 for v in nb.values())), songs_with_any=int(sum(len(v) > 0 for v in nb.values())),
                   mean_top10_cos=round(float(np.mean(sims)), 3), p10=round(float(np.percentile(sims, 10)), 3), p90=round(float(np.percentile(sims, 90)), 3))
    gen = {s["clique"]: s["genre"] for s in S}
    sg = [np.mean([gen[j] == gen[q] for j, _ in v]) for q, v in nb.items() if v]
    cnt = collections.Counter(gen.values()); tot = sum(cnt.values())
    G["I2"]["same_genre_share"] = round(float(np.mean(sg)), 3); G["I2"]["same_genre_chance"] = round(sum((c / tot) ** 2 for c in cnt.values()), 3)
    # gate verdicts
    gates = {}
    for m in ["TRAV5", "E", "econ", "T_rep", "IIV", "ch_rep", "H", "pmin", "lnP", "B"]:
        st = stab[m]["two_chart"]; o1 = G["within_composer_spearman"][m]["ch_rep"] if m != "ch_rep" else 0.0
        o2 = G["within_composer_spearman"][m]["V"]
        ok = st >= 0.5 and abs(o1) <= 0.8 and abs(o2) <= 0.8
        gates[m] = dict(two_chart=st, rho_ch_rep=o1, rho_V=o2, passes=bool(ok))
    G["gates"] = gates
    json.dump(G, open(GATES, "w"), indent=1)
    print(json.dumps(gates, indent=1)); print("done", round(time.time() - t0), "s")

if __name__ == "__main__":
    main()
