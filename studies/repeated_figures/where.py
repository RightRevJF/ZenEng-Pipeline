"""749.104, the study asked for first: where do kept tunes' repeated four-interval figures sit?
For every figure a kept tune has already sung: how far back the earlier singing is (in beats), whether that distance is a whole number of bars,
and how early in the tune it comes. Then the same reading on Luthier's songs (their .song.json), if given.
python3 studies/repeated_figures/where.py [song.json ...]  ->  studies/repeated_figures/where.json"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "lib", "luthier"))
import kept_corpus as KC, page_gate as PG
def read(p, t, bar=4.0):
    """p pitches, t onsets in beats"""
    s = PG.ivs(p); seen = {}; back = []; first = None; n = len(s) - 3; early = []
    for i in range(n):
        g = tuple(s[i:i + 4])
        if g in seen: back.append(t[i] - t[seen[g]]); early.append(i / max(n, 1))
        seen[g] = i
    if not back: return None
    b = np.array(back); whole = np.abs(b / bar - np.round(b / bar)) < 0.03
    h = lambda lo, hi: float(np.mean((b >= lo) & (b < hi)))
    return dict(again=len(b) / max(n, 1), whole_bars=float(whole.mean()), within_2_bars=h(0, 2 * bar + .01), bars_2_to_8=h(2 * bar + .01, 8 * bar + .01), bars_8_to_16=h(8 * bar + .01, 16 * bar + .01), over_16_bars=h(16 * bar + .01, 1e9),
                median_back_bars=float(np.median(b) / bar), first_quarter=float(np.mean(np.array(early) < .25)), exact_1_2_4_8_bars=float(np.mean([any(abs(x - k * bar) < 0.03 for k in (1, 2, 4, 8)) for x in b])))
K = [read([int(x) for x in k["p"]], np.asarray(k["t"], float) / 12.0) for k in KC.kept_songs(min_notes=100)]; K = [r for r in K if r]
cols = list(K[0]); q = {c: [round(float(x), 3) for x in np.percentile([r[c] for r in K], (25, 50, 75))] for c in cols}; out = dict(kept_songs=len(K), kept_quartiles=q, luthier={})
print(f"kept 4/4 tunes: {len(K)}"); [print(f"  {c:22} {q[c]}") for c in cols]
for f in sys.argv[1:]:
    R = json.load(open(f)); N = [n for n in sorted(R["melody"]["notes"], key=lambda n: n["on"]) if n.get("melisma") != "second"]; p = [n["midi"] for n in N]; t = [float(n["on"]) * 4.0 / R["bar"] for n in N]; r = read(p, t); out["luthier"][os.path.basename(f)] = {c: round(r[c], 3) for c in cols}
    print(os.path.basename(f)); [print(f"  {c:22} {r[c]:.3f}   kept place: {'under 25th' if r[c] < q[c][0] else 'over 75th' if r[c] > q[c][2] else 'middle half'}") for c in cols]
if __name__ == "__main__": json.dump(out, open(os.path.join(HERE, "where.json"), "w"), indent=1)
