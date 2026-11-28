"""749.239, the second equation (PREDICTION_239_b.md): bars as words.  python3 studies/other_metres/grammar_b.py essen68|pop34 [CACHE_DIR] -> grammar_b_<name>.json
P(A, B) = S(A) * T(B given A); a window for n syllables is drawn among pairs whose onsets sum to n. Every part a counted share of the fitting half; bars never counted take the Good-Turing share, spread by the first grammar's one-bar form."""
import os, sys, json, hashlib, collections, heapq, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, grammar as G1
def bar_runs(ns, BL):
    """runs of consecutive sung bars, each bar its tuple of onsets"""
    bars = collections.defaultdict(list)
    for on, d, q in ns: bars[on // BL].append(on % BL)
    runs = []; cur = []
    for b in sorted(bars):
        if cur and b != last + 1: runs.append(cur); cur = []
        cur.append(tuple(bars[b])); last = b
    if cur: runs.append(cur)
    return runs
class Words:
    def __init__(self, runs, g1):
        self.g1 = g1; self.V = collections.defaultdict(collections.Counter); n1 = collections.Counter(); rep = collections.Counter(); self.Mc = collections.defaultdict(collections.Counter)
        for r in runs:
            for A in r: self.V[len(A)][A] += 1
            for A, B in zip(r, r[1:]):
                n1[len(A)] += 1
                if A == B: rep[len(A)] += 1
                else: self.Mc[len(A)][len(B)] += 1
        tot = sum(n1.values()); self.p1 = {a: c / tot for a, c in n1.items()}; self.R = {a: rep[a] / n1[a] for a in n1}; self.M = {a: {b: c / sum(v.values()) for b, c in v.items()} for a, v in self.Mc.items()}
        self.tok = {k: sum(v.values()) for k, v in self.V.items()}; self.U = {k: sum(1 for c in v.values() if c == 1) / self.tok[k] for k, v in self.V.items()}; self._g = {}; self.Gun = {}
        for k, v in self.V.items(): self.Gun[k] = max(1e-12, 1.0 - sum(self.g(A) for A in v))
    def g(self, X):
        if X not in self._g: self._g[X] = float(np.exp(self.g1.logp(X, 1)))
        return self._g[X]
    def q(self, X):
        k = len(X)
        if k not in self.V: return 0.0
        c = self.V[k].get(X)
        return (1 - self.U[k]) * c / self.tok[k] if c else self.U[k] * self.g(X) / self.Gun[k]
    def t(self, a, b): return (self.R.get(a, 0.0) if a == b else 0.0) + (1 - self.R.get(a, 0.0)) * self.M.get(a, {}).get(b, 0.0)
    def T(self, B, A):
        a, b = len(A), len(B); R = self.R.get(a, 0.0); m = self.M.get(a, {}).get(b, 0.0)
        if B == A: return R
        return (1 - R) * m * (self.q(B) / (1 - self.q(A)) if a == b else self.q(B))
    def P(self, seq):
        p = self.p1.get(len(seq[0]), 0.0) * self.q(seq[0])
        for A, B in zip(seq, seq[1:]): p *= self.T(B, A)
        return p
    def Z(self, n, bars):
        f = {a: p for a, p in self.p1.items()}
        for _ in range(bars - 1):
            g = collections.defaultdict(float)
            for (s, a), p in ((k if isinstance(k, tuple) else (k, k), p) for k, p in f.items()):
                for b in self.V:
                    if s + b <= n:
                        x = p * self.t(a, b)
                        if x: g[(s + b, b)] += x
            f = g
        return sum(p for (s, a), p in f.items() if s == n) if bars > 1 else self.p1.get(n, 0.0)
    def pairs(self, n, top=None):
        """every pair of vocabulary bars summing to n -> [(chance among them before renormalising, (A, B))]"""
        out = []
        for a in self.V:
            b = n - a
            if b not in self.V: continue
            VA = self.V[a].most_common(top) if top else self.V[a].items(); VB = self.V[b].most_common(top) if top else self.V[b].items()
            for A, _ in VA:
                pa = self.p1.get(a, 0.0) * self.q(A)
                if not pa: continue
                for B, _ in VB:
                    p = pa * self.T(B, A)
                    if p: out.append((p, (A, B)))
        return out
    def triples(self, n, top=15):
        out = []
        for a in self.V:
            for b in self.V:
                c = n - a - b
                if c not in self.V: continue
                for A, _ in self.V[a].most_common(top):
                    pa = self.p1.get(a, 0.0) * self.q(A)
                    if not pa: continue
                    for B in {x for x, _ in self.V[b].most_common(top)} | ({A} if a == b else set()):
                        pb = pa * self.T(B, A)
                        if not pb: continue
                        for C in {x for x, _ in self.V[c].most_common(top)} | ({B} if b == c else set()):
                            p = pb * self.T(C, B)
                            if p: out.append((p, (A, B, C)))
        return out
def check(W, held, bars, beats):
    """held = Counter of bar sequences of the held-out half"""
    cells = {}; bset = set(beats)
    for n in sorted({sum(len(x) for x in s) for s in held}):
        occ = {s: c for s, c in held.items() if sum(len(x) for x in s) == n}; tot = sum(occ.values())
        if tot < 20: continue
        Z = W.Z(n, bars)
        if not Z: cells[n] = dict(windows=tot, note="no pair of counts fitted sums to this count", inside=False, carry=0.0, top5_shared=0); continue
        cand = W.pairs(n) if bars == 2 else W.triples(n); pv = sum(p for p, _ in cand); flat = lambda s: [o for x in s for o in x]
        gb = sum(p * np.mean([o in bset for o in flat(s)]) for p, s in cand) / pv; g1 = sum(p * np.mean([o == 0 for o in flat(s)]) for p, s in cand) / pv
        onb = np.repeat([np.mean([o in bset for o in flat(s)]) for s in occ], list(occ.values())); on1 = np.repeat([np.mean([o == 0 for o in flat(s)]) for s in occ], list(occ.values()))
        def inside(x, v): lo, hi = np.percentile(v, 25), np.percentile(v, 75); return bool(abs(x - lo) <= 1.0 / n + 1e-9) if hi - lo < 1e-9 else bool(lo - 1e-9 <= x <= hi + 1e-9)
        mass = sum(W.P(s) for s in occ) / Z; tc = [s for s, _ in sorted(occ.items(), key=lambda x: (-x[1], x[0]))[:5]]; tg = [s for _, s in heapq.nlargest(5, cand)]
        cells[n] = dict(windows=tot, distinct=len(occ), on_beat=[round(float(gb), 3), round(float(np.percentile(onb, 25)), 3), round(float(np.percentile(onb, 75)), 3)], first_beat=[round(float(g1), 3), round(float(np.percentile(on1, 25)), 3), round(float(np.percentile(on1, 75)), 3)], inside=bool(inside(gb, onb) and inside(g1, on1)), carry=round(float(mass), 3), chance_on_vocabulary_windows=round(float(pv / Z), 3), top5_shared=len(set(tc) & set(tg)), generated_top5=[[[list(x) for x in s], round(p / Z, 3)] for p, s in heapq.nlargest(5, cand)], counted_top5=[[[list(x) for x in s], occ[s]] for s in tc])
    k = len(cells); a = sum(c["inside"] for c in cells.values()); b = sum(c["carry"] >= 0.60 for c in cells.values()); c3 = sum(c["top5_shared"] >= 3 for c in cells.values())
    return dict(cells=k, a_cells_inside=a, a_met=bool(a >= 0.9 * k), b_cells_at_0_60=b, b_met=bool(b == k), c_cells_three_of_five=c3, c_met=bool(c3 >= 0.8 * k), by_cell=cells)
def load(name, cache=None):
    f = cache and os.path.join(cache, f"songs_{name}.json")
    if f and os.path.exists(f): d = json.load(open(f)); return d["BL"], d["beats"], d["div"], d["songs"]
    BL, beats, div, S = G1.songs_of(name)
    if f: json.dump(dict(BL=BL, beats=beats, div=div, songs=S), open(f, "w"))
    return BL, beats, div, S
if __name__ == "__main__":
    name = sys.argv[1]; BL, beats, div, S = load(name, sys.argv[2] if len(sys.argv) > 2 else None); fitj = json.load(open(os.path.join(HERE, f"grammar_fit_{name}.json"))); g1 = G1.Grammar(BL, beats, div, fitj["steps"], fitj["theta"]); A = []; B = []
    for key, ns in S.items():
        runs = [r for r in bar_runs(ns, BL) if all(o % 3 == 0 for x in r for o in x)]; (A if int(hashlib.md5(key.encode()).hexdigest(), 16) % 2 == 0 else B).extend(runs)
    W = Words(A, g1); ok = lambda s: all(len(x) in W.V and all(((b - a) // 3) in g1.si for a, b in zip(x, x[1:])) for x in s); H2 = collections.Counter(tuple(r[i:i + 2]) for r in B for i in range(len(r) - 1)); H3 = collections.Counter(tuple(r[i:i + 3]) for r in B for i in range(len(r) - 2)); HB = collections.Counter(x for r in B for x in r)
    two = check(W, collections.Counter({s: c for s, c in H2.items() if ok(s)}), 2, beats); three = check(W, collections.Counter({s: c for s, c in H3.items() if ok(s)}), 3, beats); one = {}
    for k in sorted(W.V):
        nov = [X for X in HB if len(X) == k and X not in W.V[k] and ok((X,))]; one[k] = dict(vocabulary=len(W.V[k]), bars=W.tok[k], U=round(W.U[k], 4), one_bar_form_chance_on_uncounted=round(W.Gun[k], 3), of_it_carried_by_held_out_new_bars=round(sum(W.g(X) for X in nov) / W.Gun[k], 3), held_out_new_bars=len(nov), held_out_new_bar_share_of_bars=round(sum(HB[X] for X in nov) / max(1, sum(c for X, c in HB.items() if len(X) == k)), 4))
    out = dict(table=name, fitting_half_runs=len(A), held_out_half_runs=len(B), R={k: round(v, 4) for k, v in sorted(W.R.items())}, M={a: {b: round(c, 4) for b, c in sorted(v.items())} for a, v in sorted(W.M.items())}, p1={k: round(v, 4) for k, v in sorted(W.p1.items())}, by_count=one, two_bar=two, three_bar_reported=three, held_out_two_bar_windows_left_out=int(sum(c for s, c in H2.items() if not ok(s))))
    json.dump(out, open(os.path.join(HERE, f"grammar_b_{name}.json"), "w"), indent=1)
    for lab, t in (("two", two), ("three", three)):
        print(name, lab, json.dumps({k: v for k, v in t.items() if k != "by_cell"}))
        for n, c in t["by_cell"].items(): print(" ", n, c["windows"], c.get("on_beat"), c.get("first_beat"), c["inside"], "carry", c["carry"], "vocab", c.get("chance_on_vocabulary_windows"), "top5", c["top5_shared"])
    print("R", out["R"]); print("by count", json.dumps(one)[:900])
