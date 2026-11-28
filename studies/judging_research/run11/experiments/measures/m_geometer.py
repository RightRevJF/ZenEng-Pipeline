"""Run 11, the Geometer (round 1). Three measures; no fitted settings; deterministic.
G_GAP : Jason's g (S = 1 + g/pi) on the clip melody: lambda_2 of the normalised Laplacian of the octave-distinct pitch-transition
        graph, counts, repeated notes kept as self-loops, cyclic (last note joined to first). = m00 GAP (run 10's recipe), adopted.
G_ROOMS: the low-half Kemeny sum: mean of 1/lambda_k over k = 2 .. 1 + floor((n-1)/2) (the nontrivial eigenvalues in the lower
        half of the spectrum), normalised Laplacian of the same melody's pitch graph with repeated notes merged (no loops) and no
        wrap (card 1's primary choices (b), (c)); n = distinct pitches. Theorem 1.1 + LOT: 1/(2 phi_k) <= 1/lambda_k <=
        C^2 log(k+1) / phi_k^2, so this sums the room profile over k = 2, 3, ... (the upper half is the near-bipartite side).
G_TIE : melody-harmony rooms: B[pc, chord] = beats of overlap between melody notes of pitch class pc and chord (root pc, root-position
        intervals); N = Dr^-1/2 B Dc^-1/2 (singular values 1 = s1 >= s2 >= ...); TIE = sum_{k>=2} s_k^2 / (min(rows, cols) - 1)
        (= Cramer's V^2). B is the biadjacency of a bipartite graph whose normalised Laplacian has eigenvalues 1 -+ s_k."""
import numpy as np

KEYS = ["G_GAP", "G_ROOMS", "G_TIE"]

def _lap_eigs(seq, loops, cyclic):
    if not loops:
        q = []
        for x in seq:
            if not q or q[-1] != x: q.append(x)
        seq = q
    labs = sorted(set(seq)); n = len(labs)
    if n < 3: return None
    ix = {x: i for i, x in enumerate(labs)}; s = [ix[x] for x in seq]
    W = np.zeros((n, n))
    for a, b in zip(s, s[1:] + (s[:1] if cyclic else [])): W[a, b] += 1
    W = W + W.T
    d = W.sum(1); Dm = 1.0 / np.sqrt(d)
    return np.linalg.eigvalsh(np.eye(n) - Dm[:, None] * W * Dm[None, :])

def _tie(mel, a):
    H = [(h["onset"], h["offset"], (h["root_pitch_class"], tuple(h.get("root_position_intervals") or [])))
         for h in (a.get("harmony") or []) if h.get("root_pitch_class") is not None and h["offset"] > h["onset"]]
    if len(H) < 2: return None
    B = {}
    for o, dd, p in zip(mel["onset"], mel["dur"], mel["pitch"]):
        for h0, h1, ch in H:
            ov = min(o + dd, h1) - max(o, h0)
            if ov > 0: B[(p % 12, ch)] = B.get((p % 12, ch), 0.0) + ov
    rws = sorted({k[0] for k in B}); cls = sorted({k[1] for k in B})
    if len(rws) < 2 or len(cls) < 2: return None
    M = np.zeros((len(rws), len(cls)))
    for (c, ch), v in B.items(): M[rws.index(c), cls.index(ch)] += v
    N = M / np.sqrt(M.sum(1))[:, None] / np.sqrt(M.sum(0))[None, :]
    s = np.linalg.svd(N, compute_uv=False)
    return float((s[1:] ** 2).sum() / (min(M.shape) - 1))

def clip_measure(mel, a):
    p = mel["pitch"]
    e1 = _lap_eigs(p, loops=True, cyclic=True)
    e2 = _lap_eigs(p, loops=False, cyclic=False)
    return dict(G_GAP=None if e1 is None else float(e1[1]),
                G_ROOMS=None if e2 is None else float(np.mean(1.0 / e2[1:1 + (len(e2) - 1) // 2])),
                G_TIE=_tie(mel, a))
