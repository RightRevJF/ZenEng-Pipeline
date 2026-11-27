"""The lead-sheet waltzes of like length to a tune, for the 3/4 package's marks.  python3 studies/other_metres/like_length.py BARS -> like_length_3_4.json
A waltz's length is its bars from its first sung note to its last. Like length: within a quarter of BARS; if under 60 songs, within a third."""
import os, sys, json, glob, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, tables_3_4 as T34, leadsheet_waltz_figures as LW, atlas_build as AB
def one(path):
    x = T34.one(path)
    if x is None: return None
    ns = x["ns"]; f = LW.figs(ns); r = AB.readings(ns, 36, [0, 12, 24], 12); b0, b1 = ns[0][0] // 36, ns[-1][0] // 36; f["bars"] = b1 - b0 + 1; f["notes a bar, over its bars first to last"] = len(ns) / f["bars"]; f["onsets on the beat"] = r["onsets on the beat"]; return f
if __name__ == "__main__":
    bars = int(sys.argv[1])
    with Pool(2) as pool: F = [x for x in pool.map(one, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if x]
    band = 0.25; V = [f for f in F if abs(f["bars"] - bars) <= band * bars]
    if len(V) < 60: band = 1 / 3.0; V = [f for f in F if abs(f["bars"] - bars) <= band * bars]
    out = dict(tune_bars=bars, band="a quarter" if band == 0.25 else "a third", bars_from_to=[round(bars * (1 - band), 1), round(bars * (1 + band), 1)], songs=len(V), of=len(F), all_songs_bars_10_25_50_75_90=[float(q) for q in np.percentile([f["bars"] for f in F], (10, 25, 50, 75, 90))],
               percentiles_10_25_50_75_90={k: [round(float(q), 3) for q in np.percentile([f[k] for f in V], (10, 25, 50, 75, 90))] for k in V[0]} if V else None)
    print(json.dumps(out, indent=0)); json.dump(out, open(os.path.join(HERE, "like_length_3_4.json"), "w"), indent=1)
