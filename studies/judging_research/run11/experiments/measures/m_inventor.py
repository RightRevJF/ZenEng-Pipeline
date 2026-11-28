"""Run 11, the Inventor (round 1). Notes and chords only; no fitted settings. Song value = n_mel-weighted clip mean.

HB    (bound rooms; Li 2026 higher-order Cheeger on the melody-harmony graph): bipartite graph, left nodes = the clip's melody
      pitch classes, right nodes = its chord labels (root pc, root-position intervals), edge weight = total melody duration of
      that pc sounding over that chord (chord active at the note's onset). The graph is exactly bipartite, so the normalised
      Laplacian's spectrum is symmetric about 1 (lambda_max = 2); its eigenvalues are 1 -/+ sigma_i, sigma_i the singular values
      of D_r^-1/2 A D_c^-1/2. HB = mean of sigma_i^2 over i = 2..min(r, c) (= mean (1 - lambda_i)^2 over the low nontrivial
      eigenvalues; equals Cramer's V^2 of the pc x chord table). High = the chords cut the melody into separate rooms
      (small lambda_2..lambda_k): each chord has its own melody notes.
ANT   (push / phase lead): share of chord changes (consecutive chord spans) at which a melody note starts in the half beat before
      the change on a pitch class that belongs to the new chord and not to the old one.
LOCKP (footfall, sharpened LOCK): mean metrical weight of contour peaks minus mean metrical weight of all pitch-change onsets
      (repeated notes merged into their first onset; peak = run higher than both neighbours; >= 3 peaks). Weight = 1 +
      [half-beat grid] + [on a beat] + [on the half-bar, even bpb] + [downbeat].
Readings (dropped as tests, kept for the record): BIP = 2 - lambda_max of the octave-distinct pitch-transition graph (Trevisan's
dual Cheeger; repeats dropped, no wrap); LOCKW = LOCKP over all turning points; CT = duration share of melody on chord tones."""
import numpy as np
KEYS = ["HB", "ANT", "LOCKP", "BIP", "LOCKW", "CT"]
E = 1e-9


def _runs(p, on):
    P, O = [], []
    for x, o in zip(p, on):
        if P and P[-1] == x: continue
        P.append(x); O.append(o)
    return P, O


def _w(b, bpb):
    e = 1e-6; w = 1
    if abs(b * 2 - round(b * 2)) < e: w += 1
    if abs(b - round(b)) < e: w += 1
    if bpb % 2 == 0 and abs(b / (bpb / 2) - round(b / (bpb / 2))) < e: w += 1
    if abs(b) < e or abs(b - bpb) < e: w += 1
    return w


def _bip(seq):
    labs = sorted(set(seq)); k = len(labs)
    if k < 3: return None
    ix = {x: i for i, x in enumerate(labs)}; W = np.zeros((k, k)); s = [ix[x] for x in seq]
    for a, b in zip(s, s[1:]): W[a, b] += 1; W[b, a] += 1
    Dm = 1.0 / np.sqrt(W.sum(1))
    return float(2.0 - np.linalg.eigvalsh(np.eye(k) - Dm[:, None] * W * Dm[None, :])[-1])


def _pcs(h):
    s = {h["root_pitch_class"] % 12}; x = h["root_pitch_class"]
    for i in h.get("root_position_intervals") or []: x += i; s.add(x % 12)
    return s


def _chord_at(H, t):
    for h in H:
        if h["onset"] - E <= t < h["offset"] - E: return h
    return None


def clip_measure(mel, a):
    p, on, du, bpb = mel["pitch"], mel["onset"], mel["dur"], mel["bpb"]
    out = dict(HB=None, ANT=None, LOCKP=None, BIP=None, LOCKW=None, CT=None)
    P, O = _runs(p, on)
    out["BIP"] = _bip(P)
    w = np.array([_w(o % bpb, bpb) for o in O], float)
    pk = [i for i in range(1, len(P) - 1) if P[i] > P[i - 1] and P[i] > P[i + 1]]
    tp = [i for i in range(1, len(P) - 1) if (P[i] - P[i - 1]) * (P[i + 1] - P[i]) < 0]
    if len(pk) >= 3: out["LOCKP"] = float(w[pk].mean() - w.mean())
    if len(tp) >= 4: out["LOCKW"] = float(w[tp].mean() - w.mean())
    H = sorted((h for h in (a.get("harmony") or []) if h.get("root_pitch_class") is not None), key=lambda h: h["onset"])
    if not H: return out
    T = {}; ct = []; cd = []
    for x, o, d in zip(p, on, du):
        h = _chord_at(H, o)
        if h is None: continue
        cl = (h["root_pitch_class"] % 12, tuple(h.get("root_position_intervals") or []))
        T[(x % 12, cl)] = T.get((x % 12, cl), 0.0) + d
        ct.append((x % 12) in _pcs(h)); cd.append(d)
    if len(ct) >= 12: out["CT"] = float(np.average(np.array(ct, float), weights=np.array(cd)))
    rs = sorted({k[0] for k in T}); cs = sorted({k[1] for k in T})
    if len(rs) >= 2 and len(cs) >= 2:
        A = np.zeros((len(rs), len(cs)))
        for (r_, c_), v in T.items(): A[rs.index(r_), cs.index(c_)] += v
        N = A / np.sqrt(A.sum(1))[:, None] / np.sqrt(A.sum(0))[None, :]
        sv = np.linalg.svd(N, compute_uv=False)[1:min(len(rs), len(cs))]
        out["HB"] = float(np.mean(sv ** 2))
    n_ch = n_ant = 0
    for h0, h1 in zip(H, H[1:]):
        t = h1["onset"]; n_ch += 1; new = _pcs(h1) - _pcs(h0)
        if any(t - 0.5 - E <= o < t - E and (x % 12) in new for x, o in zip(p, on)): n_ant += 1
    if n_ch >= 4: out["ANT"] = n_ant / n_ch
    return out
