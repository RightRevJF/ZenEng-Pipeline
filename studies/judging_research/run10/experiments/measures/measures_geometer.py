"""Run 10, the Geometer: three melody measures for TheSession tunes (notes side only; no outcome is read here).

measure(t) -> dict, where t is a common10.tunes() entry (only t['mel'] is used: pitch, dur, onset, bar, beatpos).

The SKELETON (shared by all three): the notes whose onset falls exactly on a beat of the meter (beatpos an integer;
beats are quarters in x/4 and x/2, dotted quarters in 6/8, 9/8, 12/8), in order, as MIDI pitches. McBride & Fitch
(run 10 card 2) find strong-beat notes are the conserved part of a tune across settings; nothing is fitted.

G10-1  pe_h0     Persistent entropy of the H0 barcode (card 1, M4) of the skeleton's pitch-transition metric.
                 Nodes = distinct MIDI pitches; c(a,b) = count of a->b steps; p_sym = (c + c^T)/total, self-loops dropped;
                 edge length = -ln p_sym (the transition's surprisal); the finite H0 bars of the Vietoris-Rips filtration on
                 the shortest-path metric are exactly the minimum-spanning-tree edge lengths l_i (the infinite bar dropped).
                 pe_h0 = -sum q_i ln q_i / ln(#bars), q_i = l_i / sum l. Reading: pe_h0_inv uses card 1's literal 1/p_sym.
G10-2  irr_skel  Tree reduction of the skeleton walk (free reduction, run 09's IRR on a melody): merge repeated pitches,
                 then cancel every immediate back-track x y x -> x (stack); irr = (reduced length - 1)/(merged length - 1).
                 A walk on a tree reduces to a geodesic; what survives is the walk's word in the fundamental group of its own
                 transition graph (circulation round H1 loops).
G10-3  S_gap     Jason's S = 1 + g/pi, g = spectral gap 1 - lambda_2 of the reversible random walk on the skeleton's
                 PITCH-CLASS transition graph (W = c + c^T, self-loops kept; lambda_2 of D^-1/2 W D^-1/2). By Cheeger,
                 g/2 <= h <= sqrt(2g), h = the conductance of the best two-way cut of the pitch classes.
Degenerate tunes (skeleton < 8 notes or < 3 nodes) give NaN.
"""
import math
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

NAN = float("nan")


def skeleton(mel):
    bp = np.asarray(mel["beatpos"], float)
    p = np.asarray(mel["pitch"], int)
    return p[np.abs(bp - np.round(bp)) < 1e-4]


def _counts(seq):
    nodes = sorted(set(int(x) for x in seq))
    ix = {v: i for i, v in enumerate(nodes)}
    C = np.zeros((len(nodes), len(nodes)))
    for a, b in zip(seq[:-1], seq[1:]):
        C[ix[int(a)], ix[int(b)]] += 1
    return C


def _pe_h0(C, metric="log"):
    S = C + C.T
    np.fill_diagonal(S, 0)
    P = S / S.sum()
    L = np.zeros_like(P)
    m = P > 0
    L[m] = -np.log(P[m]) if metric == "log" else 1.0 / P[m]
    bars = minimum_spanning_tree(L).toarray()
    bars = bars[bars > 0]            # H0 finite bars = MST edge lengths (Rips on the shortest-path metric)
    if len(bars) < 2:
        return NAN
    q = bars / bars.sum()
    return float(-(q * np.log(q)).sum() / math.log(len(bars)))


def _irr(seq):
    q = [int(seq[0])]
    for x in seq[1:]:
        if int(x) != q[-1]:
            q.append(int(x))
    st = []
    for x in q:
        if len(st) >= 2 and st[-2] == x:
            st.pop()
        else:
            st.append(x)
    return (len(st) - 1) / max(len(q) - 1, 1)


def _gap(C):
    W = C + C.T
    d = W.sum(1)
    Dm = 1.0 / np.sqrt(d)
    ev = np.sort(np.linalg.eigvalsh(Dm[:, None] * W * Dm[None, :]))[::-1]
    return float(1.0 - ev[1])


def measure(t):
    s = skeleton(t["mel"])
    out = dict(pe_h0=NAN, pe_h0_inv=NAN, irr_skel=NAN, S_gap=NAN)
    if len(s) < 8:
        return out
    C = _counts(s)
    if C.shape[0] >= 3:
        out["pe_h0"] = _pe_h0(C, "log")
        out["pe_h0_inv"] = _pe_h0(C, "inv")
    out["irr_skel"] = float(_irr(s))
    Cpc = _counts(s % 12)
    if Cpc.shape[0] >= 3:
        out["S_gap"] = 1.0 + _gap(Cpc) / math.pi
    return out
