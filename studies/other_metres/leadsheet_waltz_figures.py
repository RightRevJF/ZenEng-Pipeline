"""For 749.227: the lead-sheet waltzes' own figures, by song, for the readings the plan form moved.  python3 studies/other_metres/leadsheet_waltz_figures.py [record.song.json ...] -> leadsheet_waltz_figures.json"""
import os, sys, json, glob, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, tables_3_4 as T34, atlas_build as AB, make_leadsheet_table as MK
BL = 36
def figs(ns):
    r = {**AB.readings(ns, BL, [0, 12, 24], 12), **MK.structure(ns, BL)}; p = [x[2] for x in ns]; bars = collections.defaultdict(list)
    for on, d, q in ns: bars[on // BL].append(on % BL)
    held = sum(1 for b, v in bars.items() if v == [0] and not bars.get(b + 1) is None and next((d for on, d, q in ns if on == b * BL), 0) >= BL)
    return {"bars on a rhythm already sung": r["bars on a rhythm already sung"], "bars on a figure already sung": r["bars on a figure already sung"], "distinct rhythms over bars": r["distinct rhythms over bars"], "commonest pitch, whole tune": max(collections.Counter(p).values()) / len(p), "range": r["range"], "distinct pitches": r["distinct pitches"], "notes a bar": r["notes a bar"], "bars of one note on the first beat": sum(v == [0] for v in bars.values()) / len(bars)}
if __name__ == "__main__":
    with Pool(2) as pool: V = [x for x in pool.map(T34.one, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if x]
    F = [figs(x["ns"]) for x in V]; out = dict(songs=len(F), percentiles_10_25_50_75_90={k: [round(float(q), 3) for q in np.percentile([f[k] for f in F], (10, 25, 50, 75, 90))] for k in F[0]}, tunes={})
    for path in sys.argv[1:]:
        R = json.load(open(path)); ns = sorted([[n["on"], n["dur"], n["midi"]] for n in R["melody"]["notes"]]); out["tunes"][path.split("scratchpad/")[-1]] = {k: round(float(v), 3) for k, v in figs(ns).items()}
    for k, v in out["percentiles_10_25_50_75_90"].items(): print(f"{k:36} {v}  " + "  ".join(f"{t.split('/')[1]}:{d[k]}" for t, d in out["tunes"].items()))
    json.dump(out, open(os.path.join(HERE, "leadsheet_waltz_figures.json"), "w"), indent=1)
