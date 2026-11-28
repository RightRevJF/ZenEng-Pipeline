"""Run 11, the Listener's measures (notes only; no fitted settings; deterministic). Recipes in run11/round1_listener.md.

Pitch graph (card 1, section 3, primary settings): one node per octave-distinct pitch; consecutive repeated pitches dropped;
transitions across rests kept; W = C + C^T from consecutive pairs (not cyclic); normalised Laplacian L = I - D^-1/2 W D^-1/2.
Rooms (k = 2): sweep cut of the Fiedler vector (v2 / sqrt(d), ties broken by pitch): the prefix with the least conductance
cut / min(vol S, vol S^c); within sqrt(2 lambda_2) of the best split (Cheeger; card 1 M4).

SETTLE  : 1 - crossings / (2 nA nB / n), on the repeat-free note sequence: the room crossings against their expectation if the
          same notes came in a random order. + = the melody stays in a room longer than its own notes require.
TYP     : Pearson r between the clip's duration-weighted scale-degree profile (12 bins from the tonic) and the corpus profile
          (duration-weighted sum over every Hooktheory clip with a melody, kept separately for major keys, third degree 4
          semitones up, and the rest). A corpus statistic, not a tuned setting; one clip is about 1/20,000 of it.
          + = the melody spends its time on the degrees pop listeners are most exposed to.
TYP11   : TYP without the tonic bin (degrees 1..11 only), so it is not tonic_share renamed.
TYP_KK11: TYP11 against the Krumhansl-Kessler probe-tone profile instead of the corpus (published listener data). Reading.
REP     : C.baseline(mel)['pc_entropy'] under another key (REP is the baseline by design)."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import common11 as C

KEYS = ["SETTLE", "TYP", "TYP11", "TYP_KK11", "REP"]
KK_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KK_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _is_major(a):
    ks = (a.get("keys") or [{}])[0].get("scale_degree_intervals") or [2, 2]
    return sum(ks[:2]) == 4


def _profile(mel):
    prof = np.zeros(12)
    for x, du in zip(mel["pitch"], mel["dur"]): prof[(x - mel["tonic_pc"]) % 12] += du
    return prof


_CORP = None
def _corpus():
    global _CORP
    if _CORP is None:
        acc = {True: np.zeros(12), False: np.zeros(12)}
        RAW = C.C5.raw_clips()
        for k in sorted(RAW):
            m = C.melody(RAW[k])
            if m is not None: acc[_is_major(RAW[k])] += _profile(m)
        _CORP = acc
    return _CORP


def _r(x, y):
    return float(np.corrcoef(x, y)[0, 1]) if x.std() > 0 else None


def _graph(seq):
    labs = sorted(set(seq)); ix = {x: i for i, x in enumerate(labs)}; k = len(labs)
    W = np.zeros((k, k)); s = [ix[x] for x in seq]
    for a, b in zip(s, s[1:]): W[a, b] += 1; W[b, a] += 1
    return labs, s, W


def _sweep(W):
    d = W.sum(1); Dm = 1.0 / np.sqrt(d)
    L = np.eye(len(d)) - Dm[:, None] * W * Dm[None, :]
    ev, vec = np.linalg.eigh(L)
    f = vec[:, 1] * Dm
    order = sorted(range(len(d)), key=lambda i: (round(float(f[i]), 12), i))
    vol = d.sum(); best, bestS = np.inf, None
    for j in range(1, len(d)):
        S = np.zeros(len(d), bool); S[order[:j]] = True
        phi = W[S][:, ~S].sum() / min(d[S].sum(), vol - d[S].sum())
        if phi < best - 1e-12: best, bestS = phi, S
    return ev, bestS


def clip_measure(mel, a):
    maj = _is_major(a); prof = _profile(mel); corp = _corpus()[maj]; kk = KK_MAJ if maj else KK_MIN
    out = dict(SETTLE=None, TYP=_r(prof, corp), TYP11=_r(prof[1:], corp[1:]), TYP_KK11=_r(prof[1:], kk[1:]),
               REP=C.baseline(mel)["pc_entropy"])
    P = []
    for x in mel["pitch"]:
        if not P or P[-1] != x: P.append(x)
    if len(set(P)) < 3 or len(P) < 8: return out
    labs, s, W = _graph(P)
    ev, S = _sweep(W)
    room = np.array([S[i] for i in s]); n = len(P); nA = int(room.sum())
    out["SETTLE"] = float(1.0 - (room[1:] != room[:-1]).sum() / (2.0 * nA * (n - nA) / n))
    return out
