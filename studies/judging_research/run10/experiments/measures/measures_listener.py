"""Listener measures for run 10 (TheSession melodies). Notes side only; no outcome is read here.

measure(t) -> dict with
  slg      L1 self-learnability gain: mean over the second half of the (unison-collapsed) note sequence of
           log2 p_self(x_i | x_{i-1}) - log2 p_corpus(x_i | x_{i-1}); x = pitch class relative to the tonic;
           p_self = add-one bigram on the tune's own earlier notes; p_corpus = add-one bigram of the tune's TYPE
           on split A first settings, leave-one-out (the tune's own first setting subtracted).
  slg_win  share of those notes where p_self > p_corpus.
  core_ic  L2 mean corpus surprisal (bits) of the skeleton: pitch classes of on-beat notes, bigram on the skeleton
           sequence, type-specific, leave-one-out.
  surf_ic  mean corpus surprisal (bits) of off-beat notes under the surface bigram (collapsed sequence), same corpus.
  tsg      core_ic - surf_ic (negative = typical skeleton, surprising surface).
  gap      L3 Fiedler value (second-smallest eigenvalue) of the normalised Laplacian of the undirected pitch-transition
           graph (MIDI pitches as nodes, octave kept, unisons dropped, counts p(a,b)+p(b,a)); S = 1 + gap/pi.
  cheeger  conductance of the Fiedler sweep cut (Cheeger: gap/2 <= h <= sqrt(2 gap)).
  cut_ab   L3 PRIMARY: |Pearson r| over the expanded notes between each note's Fiedler coordinate D^-1/2 v2 (of its
           pitch) and the indicator 'note in the second half of the tune' (A part versus B part in a AABB tune).
  h0_max   card 1 H0 check: longest MST edge / total MST length, edge length 1/p_sym (weakest necessary link share).
  aabb     subset flag (not a measure): 1.0 if the tune is a reel or jig whose first setting is written as 16 bars and
           expands to 32 (strict AABB); for the separate CUT_AB report only.
Corpus models are trained on split A only (never C or H), notes only.

ROUND 2 (after the Skeptic): counted keys are FINAL below; tsg, gap (S), cheeger, h0_max, slg_win are estimates only.
"""
FINAL = {
    "slg":     dict(sign=+1, size=+0.03, extra=["bar_rep", "ln_notes"]),
    "core_ic": dict(sign=-1, size=-0.03, extra=["pc_entropy"]),
    "cut_ab":  dict(sign=+1, size=+0.03, extra=["n_bars", "ln_notes"]),
}
ESTIMATES = {"tsg": dict(sign=-1, extra=["pc_entropy"]), "gap": dict(sign=-1, extra=["range", "n_pitch", "ln_notes"])}
import sys, math
import numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/judging_research/run10/experiments")
import common10 as c10
from scipy.sparse.csgraph import minimum_spanning_tree

_CORP = None

def _seqs(mel, tonic_pc):
    p = mel["pitch"]; bp = mel["beatpos"]
    surf = []; onb = []
    last = None
    for pi, b in zip(p, bp):
        if pi == last: continue            # collapse repeated notes (transcription-dependent)
        last = pi
        surf.append((pi - tonic_pc) % 12); onb.append(abs(b - round(b)) < 1e-6)
    skel = [(pi - tonic_pc) % 12 for pi, b in zip(p, bp) if abs(b - round(b)) < 1e-6]
    return surf, onb, skel

def _bigram(seq):
    M = np.zeros((12, 12))
    for a, b in zip(seq[:-1], seq[1:]): M[a, b] += 1
    return M

def _own(t):
    s, _, k = _seqs(t["mel"], t["tonic_pc"])
    return _bigram(s), _bigram(k)

def corpus():
    global _CORP
    if _CORP is not None: return _CORP
    T = c10.tunes(); C = {}
    for tid, t in T.items():
        if t["split"] != "A": continue
        S, K = _own(t)
        d = C.setdefault(t["type"], [np.zeros((12, 12)), np.zeros((12, 12))])
        d[0] += S; d[1] += K
    _CORP = C
    return C

def _corp_for(t):
    C = corpus(); S, K = C[t["type"]]
    T = c10.tunes(); t0 = T.get(t["tune_id"])
    if t0 is not None and t0["split"] == "A":            # leave the tune out (its first setting is in the corpus)
        s0, k0 = _own(t0); S = S - s0; K = K - k0
    return S, K

def _lp(M, a, b):
    return math.log2((M[a, b] + 1.0) / (M[a].sum() + 12.0))

def _gap(mel):
    p = np.array(mel["pitch"], int)
    nodes = sorted(set(p.tolist())); ix = {v: i for i, v in enumerate(nodes)}; n = len(nodes)
    if n < 3: return None
    W = np.zeros((n, n))
    for a, b in zip(p[:-1], p[1:]):
        if a != b: W[ix[a], ix[b]] += 1; W[ix[b], ix[a]] += 1
    deg = W.sum(1)
    if (deg == 0).any(): return None
    Dm = 1 / np.sqrt(deg)
    L = np.eye(n) - Dm[:, None] * W * Dm[None, :]
    ev, V = np.linalg.eigh(L)
    g = float(ev[1])
    # Fiedler sweep cut conductance
    f = Dm * V[:, 1]; order = np.argsort(f); vol = deg.sum(); best = np.inf
    inS = np.zeros(n, bool)
    for k in range(n - 1):
        inS[order[k]] = True
        cut = W[inS][:, ~inS].sum(); vs = deg[inS].sum()
        best = min(best, cut / min(vs, vol - vs))
    # card 1 H0: MST on edge length 1/p_sym
    P = W / W.sum()
    Lw = np.where(P > 0, 1.0 / np.where(P > 0, P, 1), 0.0)
    mst = minimum_spanning_tree(Lw).toarray(); e = mst[mst > 0]
    # L3 primary: does the Fiedler (Cheeger) cut line up with the tune's halves in time?
    fn = f[[ix[x] for x in p.tolist()]]; half = (np.arange(len(p)) >= len(p) / 2).astype(float)
    cut_ab = float(abs(np.corrcoef(fn, half)[0, 1])) if fn.std() > 1e-12 else float("nan")
    return g, float(best), float(e.max() / e.sum()), cut_ab

def measure(t):
    S, K = _corp_for(t)
    surf, onb, skel = _seqs(t["mel"], t["tonic_pc"])
    if len(surf) < 16 or len(skel) < 8: return None
    own = np.zeros((12, 12)); gains = []; wins = []
    h = len(surf) // 2
    for i in range(1, len(surf)):
        a, b = surf[i - 1], surf[i]
        if i >= h:
            ls = _lp(own, a, b); lc = _lp(S, a, b)
            gains.append(ls - lc); wins.append(1.0 if ls > lc else 0.0)
        own[a, b] += 1
    core = [-_lp(K, a, b) for a, b in zip(skel[:-1], skel[1:])]
    offb = [-_lp(S, surf[i - 1], surf[i]) for i in range(1, len(surf)) if not onb[i]]
    if not offb: return None
    gp = _gap(t["mel"])
    if gp is None: return None
    g, ch, h0, cab = gp
    core_ic = float(np.mean(core)); surf_ic = float(np.mean(offb))
    return dict(slg=float(np.mean(gains)), slg_win=float(np.mean(wins)), core_ic=core_ic, surf_ic=surf_ic,
                tsg=core_ic - surf_ic, cut_ab=cab, gap=g, S=1 + g / math.pi, cheeger=ch, h0_max=h0, aabb=_aabb(t))

def _aabb(t):
    w = t.get("written"); 
    if not w or t["type"] not in ("reel", "jig"): return 0.0
    nw = len(set(w["bar"])); ne = len(set(t["mel"]["bar"]))
    return 1.0 if (nw == 16 and ne == 32) else 0.0
