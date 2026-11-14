"""luthier_judge4.py — the two-sided judge from kept songs alone (Luthier v6, fix 715). Reference reader supplied by the paper; read-only.
Usage:
    import luthier_judge4 as J4          # builds its models from luthier_judge4_data.json in the same folder
    r = J4.score(notes)                  # notes: list of (onset in twelfths of a beat from the song's first bar line, pitch, section label)
    r["charge"]                          # 0 = no reading outside the kept songs' middle half; larger is worse
    r["place among kept songs"]          # share of kept songs with a larger charge
    r["eligible for the pick"]           # ease bits a note and repeated notes inside the kept middle half
    r["distance from the kept medians"]  # sum over the thirteen readings of |reading - kept median| in kept standard deviations
    r["charges"], r["components"], r["ease bits a note"]
The pick (fix 715): among clean survivors that are eligible, the least charge; among builds within 0.02 of the least, the least
distance from the kept medians. Nothing in this file was fitted on engine output. Needs numpy and scipy."""
import json, re, math, os, collections, numpy as np
from scipy.optimize import minimize
GB = [3, 4, 6, 9, 12, 18, 24, 48]; LAGS = [1, 2, 4, 8, 16]; EXP = ["corpus", "song so far"] + [f"{k} back" for k in LAGS] + ["last like section"]
norm = lambda x: re.sub(r"[\d\s]+$", "", str(x)).strip().lower()
def barlist(s):
    """sung bars in order: (bar index, rhythm tuple, pitches tuple, section)"""
    b = collections.OrderedDict()
    for t, p, x in zip(s["t"], s["p"], s["sec"]): b.setdefault(int(t // 48), []).append((int(t % 48), int(p), x))
    return [(k, tuple(a for a, _, _ in v), tuple(q for _, q, _ in v), v[0][2]) for k, v in sorted(b.items())]

def song_bars(s):
    """-> list of dict(b, rhythm, shape, sec, inst, off)"""
    B = barlist(s); out = []; inst = -1; start = None; prev = None; prevb = None
    for b, r, p, sec in B:
        lab = norm(sec)
        if lab != prev or (prevb is not None and b - prevb > 4): inst += 1; start = b
        out.append(dict(b=b, rhythm=r, shape=tuple(int(x) for x in np.diff(p)), sec=lab, inst=inst, off=b - start)); prev = lab; prevb = b
    return out
def experts(SB, var, corpus, base, cond=None):
    """rows: per bar the probability each expert gives the true symbol (nan = expert unavailable). cond: None or a function giving the conditioning key (for pitch given rhythm)."""
    rows = []; seen = collections.Counter(); byb = {}; n = 0; insts = collections.defaultdict(dict); lastinst = {}; byrh = {}
    for x in SB:
        v = x[var]; key = cond(x) if cond else None; e = np.full(len(EXP) + (1 if cond else 0), np.nan)
        e[0] = corpus(v, key)
        if cond:
            tot = sum(c for (k2, _), c in seen.items() if k2 == key); e[1] = (seen[(key, v)] / tot) if tot else np.nan
        else: e[1] = (seen[v] / n) if n else np.nan
        for j, k in enumerate(LAGS):
            o = byb.get(x["b"] - k)
            if o is not None and (not cond or cond(o) == key): e[2 + j] = float(o[var] == v)
        li = [i for i in insts[x["sec"]] if i < x["inst"]]
        if li:
            o = insts[x["sec"]][max(li)].get(x["off"])
            if o is not None and (not cond or cond(o) == key): e[2 + len(LAGS)] = float(o[var] == v)
        if cond:
            o = byrh.get(key); e[-1] = float(o == v) if o is not None else np.nan
        rows.append(e); seen[(key, v) if cond else v] += 1; n += 1; byb[x["b"]] = x; insts[x["sec"]].setdefault(x["inst"], {})[x["off"]] = x
        if cond: byrh[key] = v
    return np.array(rows)
def make_corpus(train, var, cond=None):
    if var == "rhythm":
        C = collections.Counter(x["rhythm"] for S in train for x in S); N = sum(C.values()); pos = np.zeros(48); nb = 0
        for S in train:
            for x in S:
                nb += 1
                for t in x["rhythm"]: pos[t] += 1
        q = np.clip(pos / nb, 1e-4, 1 - 1e-4); lq, l1q = np.log(q), np.log(1 - q)
        def base(v): m = np.zeros(48, bool); m[list(v)] = True; return float(np.exp(lq[m].sum() + l1q[~m].sum()))
        return lambda v, key=None: 0.8 * C[v] / N + 0.2 * base(v)
    U = collections.Counter(i for S in train for x in S for i in x["shape"]); UN = sum(U.values()); V = len(U) + 1
    if cond is None:
        C = collections.Counter(x["shape"] for S in train for x in S); N = sum(C.values()); L = collections.Counter(len(x["shape"]) for S in train for x in S); LN = sum(L.values())
        base = lambda v: ((L[len(v)] + 0.5) / (LN + 20)) * float(np.prod([(U[i] + 0.5) / (UN + 0.5 * V) for i in v])) if len(v) else (L[0] + 0.5) / (LN + 20)
        return lambda v, key=None: 0.8 * C[v] / N + 0.2 * base(v)
    CL = collections.defaultdict(collections.Counter)
    for S in train:
        for x in S: CL[len(x["shape"])][x["shape"]] += 1
    def f(v, key):                                   # the corpus's shapes of this length (the rhythm fixes the length)
        c = CL[len(v)]; n = sum(c.values()); b = float(np.prod([(U[i] + 0.5) / (UN + 0.5 * V) for i in v])) if len(v) else 1.0
        return 0.8 * c[v] / n + 0.2 * b if n else b
    return f
def loss(w, E):
    W = np.exp(w); A = np.isfinite(E); P = np.where(A, E, 0) @ W / (A @ W); return float(-np.mean(np.log2(np.clip(P, 1e-12, None))))
def fit(E, use):
    idx = [i for i in range(E.shape[1]) if i in use]; Es = E[:, idx]; r = minimize(lambda w: loss(w, Es), np.zeros(len(idx)), method="L-BFGS-B"); return idx, r.x
def bits(E, idx, w): return loss(w, E[:, idx])
def per_song_bits(Es, idx, w): return [bits(E, idx, w) for E in Es]

LAM = (0.5, 0.3, 0.15, 0.05); V = 25 * 9
def toks(t, p): return [(int(np.clip(x, -12, 12)), int(np.searchsorted(GB, min(max(y, 1), 96)))) for x, y in zip(np.diff(p), np.diff(t))]
class NG:
    def __init__(self): self.c3 = collections.Counter(); self.c2 = collections.Counter(); self.c1 = collections.Counter(); self.n2 = collections.Counter(); self.n1 = collections.Counter(); self.n0 = 0
    def add(self, seq, i):
        x = seq[i]; self.c1[x] += 1; self.n0 += 1
        if i >= 1: self.c2[(seq[i - 1], x)] += 1; self.n1[seq[i - 1]] += 1
        if i >= 2: self.c3[(seq[i - 2], seq[i - 1], x)] += 1; self.n2[(seq[i - 2], seq[i - 1])] += 1
    def p(self, seq, i, uni=True):
        x = seq[i]; out = 0.0; w = 0.0
        if i >= 2 and self.n2[(seq[i - 2], seq[i - 1])]: out += LAM[0] * self.c3[(seq[i - 2], seq[i - 1], x)] / self.n2[(seq[i - 2], seq[i - 1])]; w += LAM[0]
        if i >= 1 and self.n1[seq[i - 1]]: out += LAM[1] * self.c2[(seq[i - 1], x)] / self.n1[seq[i - 1]]; w += LAM[1]
        if self.n0: out += LAM[2] * self.c1[x] / self.n0; w += LAM[2]
        if uni: out += LAM[3] / V; w += LAM[3]
        return out / w if w else 0.0
def coupling(B):
    idx = {b[0]: b[1] for b in B}; cnt = collections.Counter(idx.values()); vocab = list(cnt); q = np.array([cnt[v] for v in vocab], float); q /= q.sum(); vi = {v: i for i, v in enumerate(vocab)}; lq = np.log(q); t = 0
    for bb, x in idx.items():
        F = np.zeros((len(vocab), 5))
        for j, k in enumerate(LAGS):
            for o in (bb - k, bb + k):
                if o in idx: F[vi[idx[o]], j] += 1
        aa = lq + F @ JF; aa -= aa.max(); c = lq - lq.max(); t += (aa[vi[x]] - np.log(np.exp(aa).sum())) - (c[vi[x]] - np.log(np.exp(c).sum()))
    return t / len(idx) / np.log(2)
class Model:
    """everything a reading needs from a set of kept songs"""
    def __init__(self, train):
        self.ng = NG(); self.so = collections.defaultdict(int); self.sh = collections.defaultdict(int); gc = np.zeros(9)
        for s in train:
            q = toks(s["t"], s["p"])
            for j in range(len(q)): self.ng.add(q, j)
            B = barlist(s)
            for r in set(b[1] for b in B): self.so[r] += 1
            for f in set(tuple(int(x) for x in np.diff(b[2])) for b in B if len(b[2]) >= 3): self.sh[f] += 1
            g = np.searchsorted(GB, np.clip(np.diff(s["t"]), 1, 96)); gc += np.bincount(g, minlength=9)
        self.gap = (gc + 0.5) / (gc.sum() + 4.5); SB = [song_bars(s) for s in train]; self.coder = {}
        for var in ("rhythm", "shape"):
            corp = make_corpus(SB, var); E = np.vstack([experts(S, var, corp, None) for S in SB[:: max(1, len(SB) // 60)]]); self.coder[var] = (corp, fit(E, list(range(8))), fit(E, [0]))
COMP = ["ease bits a note", "typicality bits a note", "rhythm bits a bar", "rhythm bits saved by structure", "pitch figure bits a bar", "pitch figure bits saved by structure", "gain under the couplings", "bars sung in another kept song", "pitch figures sung in another kept song", "bars on a figure already sung", "bits saved a gap", "repeated notes", "same rhythm four bars on"]
def read(s, M):
    t, p = s["t"], s["p"]; q = toks(t, p); cache = NG(); ez = ty = 0.0
    for j in range(len(q)):
        pc = M.ng.p(q, j); pk = cache.p(q, j, uni=False) if cache.n0 >= 8 else None; ty += -math.log2(pc); ez += -math.log2(0.5 * pc + 0.5 * pk if pk is not None else pc); cache.add(q, j)
    B = barlist(s); SB = song_bars(s); out = [ez / len(q), ty / len(q)]
    for var in ("rhythm", "shape"):
        corp, (i1, w1), (i0, w0) = M.coder[var]; E = experts(SB, var, corp, None); full = bits(E, i1, w1); out += [full, bits(E, i0, w0) - full]
    out.append(coupling(B)); out.append(float(np.mean([M.so[b[1]] > 0 for b in B])))
    fig = [tuple(int(x) for x in np.diff(b[2])) for b in B if len(b[2]) >= 3]; out.append(float(np.mean([M.sh[f] > 0 for f in fig])) if fig else np.nan)
    seen = set(); h = 0
    for f in fig: h += f in seen; seen.add(f)
    out.append(h / len(fig) if fig else np.nan)
    g = np.searchsorted(GB, np.clip(np.diff(t), 1, 96)); hh = len(g) // 2; own = np.bincount(g[:hh], minlength=9) / max(1, hh); out.append(float(np.mean(-np.log2(M.gap[g[hh:]])) - np.mean(-np.log2(0.7 * own[g[hh:]] + 0.3 * M.gap[g[hh:]]))))
    out.append(float(np.mean(np.diff(p) == 0)))
    idx = {b[0]: b for b in B}; pr = [(b[1] == idx[b[0] + 4][1]) for b in B if b[0] + 4 in idx and norm(idx[b[0] + 4][3]) == norm(b[3])]; out.append(float(np.mean(pr)) if len(pr) >= 6 else np.nan)
    return np.array(out, float), len(t) / len(B)


_D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "luthier_judge4_data.json")))
_KEPT = [dict(t=np.array(s["t"]), p=np.array(s["p"]), sec=np.array(s["sec"])) for s in _D["kept songs"]]
JF = np.array(_D["bar couplings"]); _M = Model(_KEPT); _P = _D["prep"]; _MED = np.array(_P["median"]); _BETA = np.array(_P["beta"]); _SD = np.array(_P["sd"]); _TH = np.array(_D["theta"]); _KS = np.array(_D["kept scores, sorted"]); _Q1 = np.array(_D["q1"]); _Q3 = np.array(_D["q3"]); _Z50 = np.array(_D["kept z 50th"]); _E1 = np.array(_D["kept z 25th"]); _E3 = np.array(_D["kept z 75th"]); _MID = [COMP.index("ease bits a note"), COMP.index("repeated notes")]
def score(notes):
    notes = sorted(notes, key=lambda n: n[0]); s = dict(t=np.array([int(n[0]) for n in notes]), p=np.array([int(n[1]) for n in notes]), sec=np.array([str(n[2]) for n in notes]))
    c, d = read(s, _M); c2 = np.where(np.isfinite(c), c, _MED); z = (c2 - np.array([1.0, d, d * d]) @ _BETA) / _SD; hi = np.maximum(0, z - _Q3); lo = np.maximum(0, _Q1 - z); k = len(COMP); ch_hi = hi * _TH[1:1 + k]; ch_lo = lo * _TH[1 + k:]; charge = float(ch_hi.sum() + ch_lo.sum()); sc = float(_TH[0] - charge)
    mid = [COMP[i] for i in _MID if not (_E1[i] <= z[i] <= _E3[i])]; charges = {COMP[i] + (" high" if j == 0 else " low"): float(v[i]) for j, v in enumerate((ch_hi, ch_lo)) for i in range(k) if v[i] > 0}
    return {"charge": charge, "place among kept songs": float(np.searchsorted(_KS, sc, side="left") / len(_KS)), "eligible for the pick": len(mid) == 0, "ease or repeats outside the kept middle half": mid, "distance from the kept medians": float(np.abs(z - _Z50).sum()), "charges": charges, "components": dict(zip(COMP, [float(x) for x in c])), "components in kept standard deviations": dict(zip(COMP, [float(x) for x in z])), "ease bits a note": float(c[0]), "notes a sung bar": float(d)}
def pick(builds):
    """builds: list of (id, notes). Returns (id of the pick, list of results)."""
    R = [(i, score(n)) for i, n in builds]; el = [(i, r) for i, r in R if r["eligible for the pick"]]
    if not el: return None, R
    least = min(r["charge"] for _, r in el); near = [(i, r) for i, r in el if r["charge"] <= least + 0.02]; return min(near, key=lambda x: x[1]["distance from the kept medians"])[0], R
