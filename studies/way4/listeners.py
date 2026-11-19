"""Way 4: the stranger and the learner (see PREDICTION.md). python3 listeners.py -> listeners.pkl (per-song measures)"""
import pickle, math, collections, sys, json
import numpy as np
ORD = 4
def symbols(ns):
    """ns: [(onset beats, pitch)] in order -> (intervals, iois) each len n-1"""
    iv = [max(-12, min(12, b[1] - a[1])) for a, b in zip(ns, ns[1:])]; io = [max(1, min(32, int(round((b[0] - a[0]) * 4)))) for a, b in zip(ns, ns[1:])]; return iv, io
class PPM:
    def __init__(self, alphabet): self.C = [collections.defaultdict(collections.Counter) for _ in range(ORD + 1)]; self.A = alphabet
    def add(self, seq, sign=1):
        for i, s in enumerate(seq):
            for n in range(min(ORD, i) + 1): self.C[n][tuple(seq[i - n:i])][s] += sign
    def add_one(self, seq, i):
        for n in range(min(ORD, i) + 1): self.C[n][tuple(seq[i - n:i])][seq[i]] += 1
    def dist(self, seq, i, excl=None):
        """the distribution over the alphabet for position i given seq[:i]; excl: a PPM whose counts are taken away"""
        p = np.full(len(self.A), 1.0 / len(self.A))
        for n in range(min(ORD, i) + 1):
            ctx = tuple(seq[i - n:i]); c = self.C[n].get(ctx)
            if not c: continue
            if excl is not None:
                e = excl.C[n].get(ctx); c = {k: v - (e.get(k, 0) if e else 0) for k, v in c.items()}; c = {k: v for k, v in c.items() if v > 0}
                if not c: continue
            N = sum(c.values()); T = len(c); q = np.zeros(len(self.A))
            for k, v in c.items(): q[self.A[k]] = v
            p = (q + T * p) / (N + T)
        return p
IVA = {k: j for j, k in enumerate(range(-12, 13))}; IOA = {k: j for j, k in enumerate(range(1, 33))}
def ent(p): return float(-(p * np.log2(p + 1e-12)).sum())
def mix(p, q):
    a, b = 1.0 / max(ent(p), 1e-3), 1.0 / max(ent(q), 1e-3); return (a * p + b * q) / (a + b)
def read(song, LT, own):
    """-> per note arrays: stranger surprise, learner surprise, flags; over the song's clips in order (the learner keeps what it heard in earlier clips)"""
    ST = (PPM(IVA), PPM(IOA)); S = []; Lr = []; end = []; first = True
    for ns in song["clips"]:
        iv, io = symbols(ns)
        for i in range(len(iv)):
            s = l = 0.0
            for k, (seq, A) in enumerate(((iv, IVA), (io, IOA))):
                p = LT[k].dist(seq, i, own[k]); q = ST[k].dist(seq, i) if (not first or i > 0) else p; m = mix(p, q); j = A[seq[i]]; s += -math.log2(p[j]); l += -math.log2(m[j])
            S.append(s); Lr.append(l); end.append(i + 1 >= len(io) or io[i + 1] >= 8)
            for k, seq in enumerate((iv, io)): ST[k].add_one(seq, i)
        first = False
    return np.array(S), np.array(Lr), np.array(end)
def measures(S, L, end):
    n = len(S); h = n // 2; g = S - L
    return dict(notes=n + 1, S=float(S.mean()), L=float(L.mean()), GAIN=float(g.mean()), SHARE=float(g.mean() / S.mean()), LATE=float(g[h:].mean() - g[:h].mean()), END=float(L[end].mean() - L[~end].mean()) if end.any() and (~end).any() else None)
if __name__ == "__main__":
    G = pickle.load(open("graded.pkl", "rb")); LT = (PPM(IVA), PPM(IOA)); by_title = collections.defaultdict(list)
    for s in G:
        if s["src"] != "HT": continue
        by_title[s["title"]].append(s)
        for ns in s["clips"]:
            iv, io = symbols(ns); LT[0].add(iv); LT[1].add(io)
    print("stranger trained:", sum(len(v) for v in by_title.values()), "songs", flush=True); out = []
    todo = [s for s in G if s["src"] != "HT" or (s.get("peak") is not None and sum(len(c) for c in s["clips"]) >= 40)]
    for k, s in enumerate(todo):
        own = (PPM(IVA), PPM(IOA))
        for t in by_title.get(s["title"], []):
            for ns in t["clips"]:
                iv, io = symbols(ns); own[0].add(iv); own[1].add(io)
        S, L, end = read(s, LT, own); m = measures(S, L, end); m.update({x: s.get(x) for x in ("src", "id", "title", "peak", "weeks", "year", "rank", "position")}); out.append(m)
        if k % 300 == 0: print(k, len(todo), flush=True)
    pickle.dump(out, open("listeners.pkl", "wb")); print("done", len(out))
