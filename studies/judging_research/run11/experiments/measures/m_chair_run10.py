"""Run 11, the chair: run 10's deductions (R10-*) re-built on Hooktheory clip melodies, plus one reading the round-2 answers asked
for. Notes only; no outcome is read; deterministic; no fitted settings. NO TheSession data is read and run10's common10 is NOT
imported: the recipes are copied from run10/experiments/measures/*.py (functions of mel only) and adapted to a clip.

mel = common11.melody(a): pitch (12*octave + pc), dur, onset, beatpos (onset mod bpb, in Hooktheory beats), bar, bpb, tonic_pc.
SKELETON = the notes whose onset falls exactly on a beat (beatpos an integer), in order (run 10's Geometer; McBride & Fitch).

R_PE_H0   (R10-G1) persistent entropy of the H0 barcode of the skeleton's pitch-transition metric: nodes = MIDI pitches,
          p_sym = (c + c^T)/total without self-loops, edge length -ln p_sym; H0 bars = MST edge lengths; normalised entropy.
R_PE_H0I  reading: the same with edge length 1/p_sym (card 1 of run 10, literal).
R_IRR     (R10-G2) free (tree) reduction of the skeleton walk: merge repeats, cancel x y x -> x; (reduced - 1)/(merged - 1).
R_SGAP    (R10-G3) S = 1 + g/pi, g = 1 - lambda_2 of D^-1/2 W D^-1/2 on the skeleton's PITCH-CLASS graph (W = c + c^T, loops kept).
R_ARCH    (R10-I1) normalised persistent entropy of the contour's sublevel + superlevel H0 barcode (repeats merged; >= 8 runs).
R_SLG     (R10-L1) self-learnability gain: mean over the second half of the unison-collapsed tonic-relative pc sequence of
          log2 p_self(x_i | x_i-1) - log2 p_corpus(x_i | x_i-1); add-one bigrams; p_self from the clip's own earlier notes.
          CORPUS (Hooktheory has no tune types): every raw Hooktheory clip with a melody, in sorted key order, kept separately for
          major keys (first two scale steps sum to 4) and the rest (as TYP11); leave-one-out: the clip's own counts subtracted.
R_SLGW    reading: share of those notes with p_self > p_corpus.
R_CORE_IC (R10-L2) mean corpus surprisal (bits) of the skeleton's tonic-relative pc bigrams (skeleton corpus, same rule).
R_SURF_IC reading: mean corpus surprisal of off-beat notes under the surface bigram.  R_TSG (R10-L2b) = R_CORE_IC - R_SURF_IC.
R_CUT_AB  (R10-L3) |Pearson r| over the clip's notes between each note's Fiedler coordinate D^-1/2 v2 (pitch graph, unisons
          dropped, not cyclic) and the indicator 'note in the second half of the clip'.
R_CHEEGER (R10-C1) conductance of the Fiedler sweep cut of the same graph (Cheeger: gap/2 <= h <= sqrt(2 gap)). Merged with GAP.
R_H0MAX   reading: longest MST edge / total MST length, edge length 1/p_sym, same graph.
G_TIE_BC  reading for G_TIE (the Geometer's round 2): Bergsma's (2013) bias-corrected Cramer's V^2 on NOTE COUNTS: n[pc, chord] =
          the number of melody notes of pitch class pc that overlap chord (root pc, root-position intervals) in time (a note
          counts once under every chord it overlaps; the same overlap rule as G_TIE). phi2 = chi2/n; phi2c = max(0, phi2 -
          (r-1)(c-1)/(n-1)); rc = r - (r-1)^2/(n-1); cc = c - (c-1)^2/(n-1); V2c = phi2c / min(rc-1, cc-1). Needs r, c >= 2, n > 1.
Thresholds as in run 10: skeleton >= 8 notes and >= 3 nodes; surface >= 16 collapsed notes for R_SLG / R_CORE_IC."""
import math
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

KEYS = ["R_PE_H0", "R_PE_H0I", "R_IRR", "R_SGAP", "R_ARCH", "R_SLG", "R_SLGW", "R_CORE_IC", "R_SURF_IC", "R_TSG",
        "R_CUT_AB", "R_CHEEGER", "R_H0MAX", "G_TIE_BC"]
E = 1e-6


def _onbeat(b):
    return abs(b - round(b)) < 1e-4


# ---------------------------------------------------------------- run 10 Geometer (skeleton)
def _counts(seq):
    nodes = sorted(set(int(x) for x in seq)); ix = {v: i for i, v in enumerate(nodes)}
    C = np.zeros((len(nodes), len(nodes)))
    for a, b in zip(seq[:-1], seq[1:]): C[ix[int(a)], ix[int(b)]] += 1
    return C


def _pe_h0(C, metric):
    S = C + C.T; np.fill_diagonal(S, 0)
    if S.sum() == 0: return None
    P = S / S.sum(); L = np.zeros_like(P); m = P > 0
    L[m] = -np.log(P[m]) if metric == "log" else 1.0 / P[m]
    bars = minimum_spanning_tree(L).toarray(); bars = bars[bars > 0]
    if len(bars) < 2: return None
    q = bars / bars.sum()
    return float(-(q * np.log(q)).sum() / math.log(len(bars)))


def _irr(seq):
    q = [int(seq[0])]
    for x in seq[1:]:
        if int(x) != q[-1]: q.append(int(x))
    st = []
    for x in q:
        if len(st) >= 2 and st[-2] == x: st.pop()
        else: st.append(x)
    return (len(st) - 1) / max(len(q) - 1, 1)


def _sgap(C):
    W = C + C.T; d = W.sum(1)
    if (d == 0).any(): return None
    Dm = 1.0 / np.sqrt(d)
    ev = np.sort(np.linalg.eigvalsh(Dm[:, None] * W * Dm[None, :]))[::-1]
    return 1.0 + float(1.0 - ev[1]) / math.pi


# ---------------------------------------------------------------- run 10 Inventor (contour arches)
def _sublevel_bars(v):
    n = len(v); order = sorted(range(n), key=lambda i: (v[i], i)); parent = [-1] * n; birth = [0.0] * n

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    bars = []
    for i in order:
        parent[i] = i; birth[i] = v[i]
        for j in (i - 1, i + 1):
            if 0 <= j < n and parent[j] != -1:
                ri, rj = find(i), find(j)
                if ri == rj: continue
                young, old = (ri, rj) if birth[ri] > birth[rj] else (rj, ri)
                if birth[young] == birth[old] and young < old: young, old = old, young
                L = v[i] - birth[young]
                if L > 0: bars.append(L)
                parent[young] = old
    return bars


def _arch(P):
    v = [float(x) for x in P]
    bars = _sublevel_bars(v) + _sublevel_bars([-x for x in v])
    if len(bars) < 2: return None
    q = np.asarray(bars, float); q = q / q.sum()
    return float(-(q * np.log(q)).sum() / math.log(len(bars)))


# ---------------------------------------------------------------- run 10 Listener (corpus bigrams; Hooktheory corpus)
def _is_major(a):
    ks = (a.get("keys") or [{}])[0].get("scale_degree_intervals") or [2, 2]
    return sum(ks[:2]) == 4


def _seqs(mel):
    t = mel["tonic_pc"]; surf, onb, last = [], [], None
    for pi, b in zip(mel["pitch"], mel["beatpos"]):
        if pi == last: continue
        last = pi; surf.append((pi - t) % 12); onb.append(_onbeat(b))
    skel = [(pi - t) % 12 for pi, b in zip(mel["pitch"], mel["beatpos"]) if _onbeat(b)]
    return surf, onb, skel


def _bigram(seq):
    M = np.zeros((12, 12))
    for a, b in zip(seq[:-1], seq[1:]): M[a, b] += 1
    return M


_CORP = None
def _corpus():
    global _CORP
    if _CORP is None:
        import os, sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import common11 as C
        acc = {True: [np.zeros((12, 12)), np.zeros((12, 12))], False: [np.zeros((12, 12)), np.zeros((12, 12))]}
        RAW = C.C5.raw_clips()
        for k in sorted(RAW):
            m = C.melody(RAW[k])
            if m is None: continue
            s, _, sk = _seqs(m); d = acc[_is_major(RAW[k])]
            d[0] += _bigram(s); d[1] += _bigram(sk)
        _CORP = acc
    return _CORP


def _lp(M, a, b):
    return math.log2((M[a, b] + 1.0) / (M[a].sum() + 12.0))


def _listener(mel, a, out):
    surf, onb, skel = _seqs(mel)
    if len(surf) < 16 or len(skel) < 8: return
    S0, K0 = _corpus()[_is_major(a)]
    S = S0 - _bigram(surf); K = K0 - _bigram(skel)          # leave the clip out
    own = np.zeros((12, 12)); gains, wins = [], []; h = len(surf) // 2
    for i in range(1, len(surf)):
        x0, x1 = surf[i - 1], surf[i]
        if i >= h:
            ls = _lp(own, x0, x1); lc = _lp(S, x0, x1); gains.append(ls - lc); wins.append(1.0 if ls > lc else 0.0)
        own[x0, x1] += 1
    out["R_SLG"] = float(np.mean(gains)); out["R_SLGW"] = float(np.mean(wins))
    core = [-_lp(K, x0, x1) for x0, x1 in zip(skel[:-1], skel[1:])]
    offb = [-_lp(S, surf[i - 1], surf[i]) for i in range(1, len(surf)) if not onb[i]]
    out["R_CORE_IC"] = float(np.mean(core))
    if offb:
        out["R_SURF_IC"] = float(np.mean(offb)); out["R_TSG"] = out["R_CORE_IC"] - out["R_SURF_IC"]


def _cut(mel, out):
    p = np.array(mel["pitch"], int); nodes = sorted(set(p.tolist())); ix = {v: i for i, v in enumerate(nodes)}; n = len(nodes)
    if n < 3: return
    W = np.zeros((n, n))
    for x, y in zip(p[:-1], p[1:]):
        if x != y: W[ix[x], ix[y]] += 1; W[ix[y], ix[x]] += 1
    deg = W.sum(1)
    if (deg == 0).any(): return
    Dm = 1 / np.sqrt(deg); ev, V = np.linalg.eigh(np.eye(n) - Dm[:, None] * W * Dm[None, :])
    f = Dm * V[:, 1]; order = np.argsort(f, kind="stable"); vol = deg.sum(); best = np.inf; inS = np.zeros(n, bool)
    for k in range(n - 1):
        inS[order[k]] = True; cut = W[inS][:, ~inS].sum(); vs = deg[inS].sum(); best = min(best, cut / min(vs, vol - vs))
    out["R_CHEEGER"] = float(best)
    P = W / W.sum(); Lw = np.where(P > 0, 1.0 / np.where(P > 0, P, 1), 0.0)
    e = minimum_spanning_tree(Lw).toarray(); e = e[e > 0]
    if len(e): out["R_H0MAX"] = float(e.max() / e.sum())
    fn = f[[ix[x] for x in p.tolist()]]; half = (np.arange(len(p)) >= len(p) / 2).astype(float)
    if fn.std() > 1e-12: out["R_CUT_AB"] = float(abs(np.corrcoef(fn, half)[0, 1]))


def _tie_bc(mel, a):
    H = [(h["onset"], h["offset"], (h["root_pitch_class"], tuple(h.get("root_position_intervals") or [])))
         for h in (a.get("harmony") or []) if h.get("root_pitch_class") is not None and h["offset"] > h["onset"]]
    if len(H) < 2: return None
    B = {}
    for o, dd, p in zip(mel["onset"], mel["dur"], mel["pitch"]):
        for h0, h1, ch in H:
            if min(o + dd, h1) - max(o, h0) > 0: B[(p % 12, ch)] = B.get((p % 12, ch), 0) + 1
    rws = sorted({k[0] for k in B}); cls = sorted({k[1] for k in B})
    if len(rws) < 2 or len(cls) < 2: return None
    M = np.zeros((len(rws), len(cls)))
    for (c, ch), v in B.items(): M[rws.index(c), cls.index(ch)] += v
    n = M.sum()
    if n <= 1: return None
    Ex = np.outer(M.sum(1), M.sum(0)) / n; chi2 = float(((M - Ex) ** 2 / Ex).sum())
    r, c = M.shape; phi2 = chi2 / n
    phi2c = max(0.0, phi2 - (r - 1) * (c - 1) / (n - 1)); rc = r - (r - 1) ** 2 / (n - 1); cc = c - (c - 1) ** 2 / (n - 1)
    den = min(rc - 1, cc - 1)
    return float(phi2c / den) if den > 0 else None


def clip_measure(mel, a):
    out = {k: None for k in KEYS}
    p = mel["pitch"]; bp = mel["beatpos"]
    sk = np.array([x for x, b in zip(p, bp) if _onbeat(b)], int)
    if len(sk) >= 8:
        Cm = _counts(sk)
        if Cm.shape[0] >= 3:
            out["R_PE_H0"] = _pe_h0(Cm, "log"); out["R_PE_H0I"] = _pe_h0(Cm, "inv")
        out["R_IRR"] = float(_irr(sk))
        Cp = _counts(sk % 12)
        if Cp.shape[0] >= 3: out["R_SGAP"] = _sgap(Cp)
    P = []
    for x in p:
        if not P or P[-1] != x: P.append(x)
    if len(P) >= 8: out["R_ARCH"] = _arch(P)
    _listener(mel, a, out)
    _cut(mel, out)
    out["G_TIE_BC"] = _tie_bc(mel, a)
    return out
