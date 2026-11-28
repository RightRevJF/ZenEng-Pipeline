"""749.239 (PREDICTION_239_grammar.md): a rhythm grammar fitted on half a table's songs and checked on the other half.
python3 studies/other_metres/grammar.py essen68|pop34 -> grammar_fit_<name>.json (weights, the held-out check (a) (b) (c), one-bar rhythms reported)
P(window | n, span) is proportional to the product over onsets of L(level, n over bars) * G(step from the onset before). Levels: 0 the bar's first beat, 1 another beat, 2 the beat's first division, 3 finer."""
import os, sys, json, gzip, hashlib, collections, heapq
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [HERE, os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
from scipy.optimize import minimize
GRID = 3
def songs_of(name):
    """-> (bar, beats, division, {song key: [notes]})"""
    import atlas_build as AB
    if name == "essen68":
        out = {}
        for abc in AB.tunes("6/8", "sung"):
            ns = AB.notes_of(abc, 36)
            if ns: out[hashlib.md5(abc.encode()).hexdigest()] = ns
        return 36, [0, 18], 6, out
    import hooktheory_tables as HT
    D = json.load(gzip.open(HT.SRC)); songs = collections.defaultdict(list)
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != (3, 4) or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns is not None: songs[x["hooktheory"]["artist"] + "/" + x["hooktheory"]["song"]].append(ns)
    out = {}
    for key, clips in sorted(songs.items()):
        allns = []; shift = 0
        for ns in clips: b0 = ns[0][0] // 36; ns = [[on - b0 * 36 + shift, d, p] for on, d, p in ns]; shift = (ns[-1][0] // 36 + 2) * 36; allns += ns
        if len(allns) >= 24: out[key] = allns
    return 36, [0, 12, 24], 6, out
def windows(ns, BL):
    bars = collections.defaultdict(list); W = []; B = []
    for on, d, q in ns: bars[on // BL].append(on % BL)
    for b, v in bars.items():
        B.append(tuple(v))
        if b + 1 in bars: W.append(tuple(v) + tuple(o + BL for o in bars[b + 1]))
    return W, B
class Grammar:
    def __init__(self, BL, beats, div, steps, theta=None):
        self.BL = BL; self.beats = set(beats); self.div = div; self.steps = sorted(steps); self.si = {s: i for i, s in enumerate(self.steps)}; self.theta = np.zeros(6 + len(self.steps)) if theta is None else np.array(theta, float)
    def level(self, pos): p = pos % self.BL; return 0 if p == 0 else 1 if p in self.beats else 2 if p % self.div == 0 else 3
    def parts(self, n, bars, theta=None):
        th = self.theta if theta is None else theta; P = bars * self.BL // GRID; lv = np.array([self.level(i * GRID) for i in range(P)]); w = np.concatenate([th[:3], [0.0]]); v = np.concatenate([th[3:6], [0.0]]); la = w[lv] + v[lv] * (n / bars)
        K = np.full((P, P), -np.inf)
        for q in range(P):
            for p in range(q + 1, P):
                s = p - q
                if s in self.si: K[q, p] = th[6 + self.si[s]]
        return P, lv, la, K
    def logZ(self, n, bars, theta=None):
        P, lv, la, K = self.parts(n, bars, theta); f = la.copy()
        for _ in range(n - 1):
            m = f[:, None] + K; mx = np.max(m, axis=0); ok = np.isfinite(mx); g = np.full(P, -np.inf); g[ok] = mx[ok] + np.log(np.sum(np.exp(m[:, ok] - mx[ok]), axis=0)); f = g + la
        mx = np.max(f); return mx + np.log(np.sum(np.exp(f - mx))) if np.isfinite(mx) else -np.inf
    def score(self, w, bars, theta=None):
        th = self.theta if theta is None else theta; n = len(w); s = 0.0
        for i, o in enumerate(w):
            l = self.level(o)
            if l < 3: s += th[l] + th[3 + l] * (n / bars)
            if i:
                st = (o - w[i - 1]) // GRID
                if st not in self.si: return -np.inf
                s += th[6 + self.si[st]]
        return s
    def logp(self, w, bars): return self.score(w, bars) - self.logZ(len(w), bars)
    def marginals(self, n, bars):
        """the chance of an onset at each place, for windows of n onsets"""
        P, lv, la, K = self.parts(n, bars); a = np.exp(la); M = np.where(np.isfinite(K), np.exp(K), 0.0); f = [a.copy()]
        for _ in range(n - 1): f.append((f[-1] @ M) * a)
        h = [np.ones(P)]
        for _ in range(n - 1): h.append(M @ (a * h[-1]))
        Z = f[-1].sum(); return sum(f[k] * h[n - 1 - k] for k in range(n)) / Z
    def best(self, n, bars, k=5, lo=None, hi=None):
        """the k likeliest windows of n onsets (first onset at or after lo, last at or before hi, in twelfths) -> [(chance, window)]"""
        P, lv, la, K = self.parts(n, bars); ok = lambda p: (lo is None or p * GRID >= lo) and (hi is None or p * GRID <= hi); cur = [[(la[p], (p,))] if (lo is None or p * GRID >= lo) else [] for p in range(P)]
        for _ in range(n - 1):
            nxt = [[] for _ in range(P)]
            for p in range(P):
                c = [(s + K[q, p] + la[p], path + (p,)) for q in range(p) if np.isfinite(K[q, p]) for s, path in cur[q]]; nxt[p] = heapq.nlargest(k, c)
            cur = nxt
        z = self.logZ(n, bars); allc = [(s, path) for p in range(P) if (hi is None or p * GRID <= hi) for s, path in cur[p]]; return [(float(np.exp(s - z)), tuple(x * GRID for x in path)) for s, path in heapq.nlargest(k, allc)]
def fit(G, counts):
    """maximum likelihood: counts = {(window, bars): occurrences}"""
    byn = collections.Counter(); feat = np.zeros(len(G.theta))
    for (w, bars), c in counts.items():
        n = len(w); byn[(n, bars)] += c
        for i, o in enumerate(w):
            l = G.level(o)
            if l < 3: feat[l] += c; feat[3 + l] += c * n / bars
            if i: feat[6 + G.si[(o - w[i - 1]) // GRID]] += c
    def nll(th): return -(feat @ th - sum(c * G.logZ(n, bars, th) for (n, bars), c in byn.items()))
    r = minimize(nll, G.theta, method="L-BFGS-B", options=dict(maxiter=500, gtol=1e-5)); G.theta = r.x; return dict(converged=bool(r.success), iterations=int(r.nit), log_likelihood=round(float(-r.fun), 1), windows=int(sum(byn.values())))
def check(G, held, bars, beats, BL):
    cells = {}
    for n in sorted({len(w) for w in held}):
        occ = {w: c for w, c in held.items() if len(w) == n}; tot = sum(occ.values())
        if tot < 20: continue
        onb = np.repeat([np.mean([o % BL in beats for o in w]) for w in occ], list(occ.values())); on1 = np.repeat([np.mean([o % BL == 0 for o in w]) for w in occ], list(occ.values())); m = G.marginals(n, bars); P = len(m); gb = float(sum(m[p] for p in range(P) if (p * GRID) % BL in beats) / n); g1 = float(sum(m[p] for p in range(P) if (p * GRID) % BL == 0) / n)
        def inside(x, v): lo, hi = np.percentile(v, 25), np.percentile(v, 75); return bool(abs(x - lo) <= 1.0 / n + 1e-9) if hi - lo < 1e-9 else bool(lo - 1e-9 <= x <= hi + 1e-9)
        mass = float(sum(np.exp(G.logp(w, bars)) for w in occ)); top_c = [w for w, _ in sorted(occ.items(), key=lambda x: (-x[1], x[0]))[:5]]; top_g = [w for _, w in G.best(n, bars, 5)]
        cells[n] = dict(windows=tot, distinct=len(occ), on_beat=dict(generated=round(gb, 3), counted_middle_half=[round(float(np.percentile(onb, 25)), 3), round(float(np.percentile(onb, 75)), 3)], inside=inside(gb, onb)), first_beat=dict(generated=round(g1, 3), counted_middle_half=[round(float(np.percentile(on1, 25)), 3), round(float(np.percentile(on1, 75)), 3)], inside=inside(g1, on1)), counted_carry_of_generated_chance=round(mass, 3), top5_shared=len(set(top_c) & set(top_g)), generated_top5=[[list(w), round(p, 3)] for p, w in G.best(n, bars, 5)], counted_top5=[[list(w), occ[w]] for w in top_c])
    k = len(cells); a = sum(c["on_beat"]["inside"] and c["first_beat"]["inside"] for c in cells.values()); b = sum(c["counted_carry_of_generated_chance"] >= 0.60 for c in cells.values()); c3 = sum(c["top5_shared"] >= 3 for c in cells.values())
    return dict(cells=k, a_cells_inside=a, a_met=bool(a >= 0.9 * k), b_cells_at_0_60=b, b_met=bool(b == k), c_cells_three_of_five=c3, c_met=bool(c3 >= 0.8 * k), by_cell=cells)
if __name__ == "__main__":
    name = sys.argv[1]; BL, beats, div, S = songs_of(name); A = {}; B = {}; A1 = {}; B1 = {}; na = nb = 0
    for key, ns in S.items():
        W, Bs = windows(ns, BL); even = int(hashlib.md5(key.encode()).hexdigest(), 16) % 2 == 0; na += even; nb += not even
        for w in W:
            if all(o % GRID == 0 for o in w): (A if even else B)[w] = (A if even else B).get(w, 0) + 1
        for w in Bs:
            if all(o % GRID == 0 for o in w): (A1 if even else B1)[w] = (A1 if even else B1).get(w, 0) + 1
    steps = {(b - a) // GRID for w in A for a, b in zip(w, w[1:])}; G = Grammar(BL, beats, div, steps); f = fit(G, {(w, 2): c for w, c in A.items()}); heldB = {w: c for w, c in B.items() if all((b - a) // GRID in G.si for a, b in zip(w, w[1:]))}
    out = dict(table=name, songs=len(S), fitting_half_songs=int(na), held_out_half_songs=int(nb), fit=f, weights=dict(level_weight=dict(zip(("first beat", "beat", "division"), [round(float(x), 4) for x in G.theta[:3]])), level_slope_per_note_a_bar=dict(zip(("first beat", "beat", "division"), [round(float(x), 4) for x in G.theta[3:6]])), finer="0 (the reference)", step_in_sixteenths={str(s): round(float(G.theta[6 + i]), 4) for s, i in G.si.items()}), held_out_windows_with_a_step_never_fitted=int(sum(B.values()) - sum(heldB.values())), two_bar=check(G, B, 2, set(beats), BL), one_bar_reported=check(G, B1, 1, set(beats), BL), theta=[float(x) for x in G.theta], steps=G.steps)
    json.dump(out, open(os.path.join(HERE, f"grammar_fit_{name}.json"), "w"), indent=1); t = out["two_bar"]; print(name, json.dumps({k: v for k, v in out.items() if k in ("songs", "fitting_half_songs", "held_out_half_songs", "fit", "weights", "held_out_windows_with_a_step_never_fitted")})); print(json.dumps({k: v for k, v in t.items() if k != "by_cell"}))
    for n, c in t["by_cell"].items(): print(n, c["windows"], c["on_beat"]["generated"], c["on_beat"]["counted_middle_half"], c["first_beat"]["generated"], c["first_beat"]["counted_middle_half"], "mass", c["counted_carry_of_generated_chance"], "top5", c["top5_shared"])
    print("one bar:", json.dumps({k: v for k, v in out["one_bar_reported"].items() if k != "by_cell"}))
