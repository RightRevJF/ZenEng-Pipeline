"""A rough test of 'network theory and harmonic transition graphs' as a greatness vector, on McGill Billboard (as tda_mcgill.py).
Each song is a directed graph: nodes are its chords (Roman numerals), edges its chord changes (every change, across bars, inside verse, chorus, bridge
and pre-chorus sections), weighted by count. Readings: nodes, edges, density; mean clustering (undirected); mean shortest path; small-world sigma
against 20 random graphs of the same size; hub share (the most-connected chord's share of transitions) and degree Gini; betweenness centralization;
shortcut share (changes whose roots lie three or more steps apart on the circle of fifths); transition entropy (bits a change).
Compared with plain readings (distinct chords, out-of-key share, bars, loop share) and chart peak (1 is best).
    python3 studies/tda/network_mcgill.py      # writes studies/tda/network_mcgill.json"""
import json, sys, os, math, collections, random
import numpy as np, networkx as nx
from scipy.stats import spearmanr, rankdata
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "..", "lib", "luthier")); import chord_writer as C
S = json.load(open(os.path.join(H, "..", "harmony", "billboard_sections.json")))
def rootpc(rn):
    import re
    m = re.match(r"(b|#)?(VII|III|IV|VI|II|V|I|vii|iii|iv|vi|ii|v|i)", rn or "")
    if not m: return None
    return (C.DEG[m.group(2).upper()] + (-1 if m.group(1) == "b" else 1 if m.group(1) == "#" else 0)) % 12
def fifths(a, b): d = ((b - a) * 7) % 12; return min(d, 12 - d)
def gini(x):
    x = np.sort(np.array(x, float)); n = len(x); return float((2 * np.arange(1, n + 1) - n - 1) @ x / (n * x.sum())) if x.sum() else 0.0
rng = random.Random(1); rows = []
for s in S:
    seq = []; bars = []; out = 0; IN = C.IN.get(s["mode"], C.IN["major"])
    for sec in s["sections"]:
        if C.KIND.get(sec["label"]) not in ("verse", "chorus", "bridge", "pre"): continue
        for b in sec["bars"]:
            t = [C.norm(r) for r in b["rn"] if C.norm(r) and rootpc(C.norm(r)) is not None]
            if not t: continue
            bars.append(t[0]); out += t[0] not in IN
            for x in t:
                if not seq or seq[-1] != x: seq.append(x)
    if len(bars) < 16 or len(seq) < 8: continue
    try: peak = int(s["peak"])
    except Exception: continue
    E = collections.Counter(zip(seq, seq[1:])); G = nx.DiGraph(); [G.add_edge(a, b, weight=w) for (a, b), w in E.items()]
    U = G.to_undirected(); n, m = U.number_of_nodes(), U.number_of_edges()
    cc = nx.average_clustering(U); L = nx.average_shortest_path_length(U) if nx.is_connected(U) else float("nan")
    rc, rl = [], []
    for _ in range(20):
        R = nx.gnm_random_graph(n, m, seed=rng.randrange(10 ** 9))
        if nx.is_connected(R): rc.append(nx.average_clustering(R)); rl.append(nx.average_shortest_path_length(R))
    sigma = (cc / np.mean(rc)) / (L / np.mean(rl)) if rc and np.mean(rc) > 0 and not math.isnan(L) else float("nan")
    deg = collections.Counter(); [deg.update({a: w, b: w}) for (a, b), w in E.items()]
    hub = max(deg.values()) / sum(deg.values()); bt = nx.betweenness_centrality(U); bmax = max(bt.values()); bc = sum(bmax - v for v in bt.values()) / max(1, (n - 1))
    sc = sum(w for (a, b), w in E.items() if fifths(rootpc(a), rootpc(b)) >= 3) / sum(E.values())
    ent = 0.0; tot = sum(E.values())
    for a in G.nodes:
        ws = [d["weight"] for _, _, d in G.out_edges(a, data=True)]; t_ = sum(ws)
        if t_: ent += t_ / tot * -sum(w / t_ * math.log2(w / t_) for w in ws)
    per = sum(1 for i in range(len(bars) - 8) if bars[i:i + 4] == bars[i + 4:i + 8]) / max(1, len(bars) - 8)
    rows.append(dict(title=s["title"], artist=s["artist"], peak=peak, nodes=n, edges=m, density=nx.density(U), clustering=cc, path=L, sigma=sigma, hub=hub,
                     degree_gini=gini(list(deg.values())), betweenness_central=bc, shortcut=sc, entropy=ent, distinct=len(set(bars)), out=out / len(bars), bars=len(bars), loop_share=per))
NET = ("nodes", "density", "clustering", "path", "sigma", "hub", "degree_gini", "betweenness_central", "shortcut", "entropy"); PLAIN = ("distinct", "out", "bars", "loop_share")
R = {k: np.array([r[k] for r in rows], float) for k in NET + PLAIN + ("peak",)}; good = -R["peak"]
def sp(a, b):
    ok = ~(np.isnan(a) | np.isnan(b)); r = spearmanr(a[ok], b[ok]); return [round(float(r[0]), 3), round(float(r[1]), 3), int(ok.sum())]
Xp = np.column_stack([rankdata(R[p]) for p in PLAIN] + [np.ones(len(rows))])
def resid(y):
    ok = ~np.isnan(y); out_ = np.full(len(y), np.nan); yy = rankdata(y[ok]); X = Xp[ok]; b = np.linalg.lstsq(X, yy, rcond=None)[0]; out_[ok] = yy - X @ b; return out_
small = sum(1 for r in rows if r["sigma"] == r["sigma"] and r["sigma"] > 1); valid = sum(1 for r in rows if r["sigma"] == r["sigma"])
res = dict(songs=len(rows), small_world_share=[small, valid], spread={k: [round(float(x), 3) for x in np.nanquantile(R[k], (0.1, 0.25, 0.5, 0.75, 0.9))] for k in NET},
           against_peak={k: sp(R[k], good) for k in NET + PLAIN}, against_distinct={k: sp(R[k], R["distinct"])[0] for k in NET},
           beyond_plain_against_peak={k: sp(resid(R[k]), good) for k in NET})
json.dump(res, open(os.path.join(H, "network_mcgill.json"), "w"), indent=1); print(json.dumps(res, indent=1))
