"""The 3/4 lead-sheet table in the atlas's form, for the trial (PREDICTION_trial_3_4.md): python3 studies/other_metres/make_leadsheet_table.py
-> studies/other_metres/trial_tables/3-4_leadsheet_sung.json and .rows.json (one song a row, as kept_readings.json holds Essen's). Not under tables/: nothing is built."""
import os, sys, json, glob, collections
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, tables_3_4 as T34, atlas_build as AB
BL = 36; BEATS = [0, 12, 24]
def structure(ns, barlen):
    """kept_rows.structure: bars whose rhythm, and whose rhythm and pitch moves, were already sung"""
    bars = {}
    for on, d, p in ns: bars.setdefault(on // barlen, []).append((on % barlen, p))
    seen_r = set(); seen_f = set(); r = f = 0; keys = sorted(bars)
    for k in keys:
        v = bars[k]; rh = tuple(x for x, _ in v); fig = (rh, tuple(b[1] - a[1] for a, b in zip(v, v[1:])))
        r += rh in seen_r; f += fig in seen_f; seen_r.add(rh); seen_f.add(fig)
    return {"bars on a rhythm already sung": r / len(keys), "bars on a figure already sung": f / len(keys)}
if __name__ == "__main__":
    with Pool(2) as pool: V = [x for x in pool.map(T34.one, sorted(glob.glob("/home/claude/corpus/choco/partitions/wikifonia/raw/*.mxl")), chunksize=20) if x]
    R = []; BAR = collections.Counter(); WIN = collections.defaultdict(collections.Counter); IV = collections.Counter(); POS = collections.Counter(); DUR = collections.Counter()
    for x in V:
        ns = x["ns"]; R.append({**AB.readings(ns, BL, BEATS, 12), **structure(ns, BL)}); bars = collections.defaultdict(list)
        for on, d, q in ns: bars[on // BL].append((on % BL, d, q)); DUR[d] += 1
        for b, v in bars.items():
            BAR[tuple(o for o, d, q in v)] += 1
            for o, d, q in v: POS[o] += 1
            if b + 1 in bars: w = tuple(o for o, d, q in v) + tuple(o + BL for o, d, q in bars[b + 1]); WIN[len(w)][w] += 1
        for a, b in zip(ns, ns[1:]): IV[int(max(-12, min(12, b[2] - a[2])))] += 1
    names = sorted(R[0]); tot = sum(POS.values()); src = f"{len(V)} Wikifonia lead sheets in 3/4 (through ChoCo, partitions/wikifonia/raw; not committed)"
    out = dict(metre="3/4", source=src, kind="simple triple", bar=BL, beats=BEATS, beat=12, found=len(V), tunes=len(V), readings_quartiles={k: [float(np.percentile([r[k] for r in R], q)) for q in (25, 50, 75)] for k in names},
               bar_rhythms=[[list(k), v] for k, v in BAR.most_common(40)], bars_total=sum(BAR.values()), two_bar_windows={str(n): [[list(k), v] for k, v in c.most_common(40)] for n, c in WIN.items()},
               intervals={str(k): v for k, v in sorted(IV.items())}, onset_weights={str(k): round(v / tot, 4) for k, v in sorted(POS.items())}, durations={str(k): v for k, v in DUR.most_common(20)}, licence="a trial table; the songs are in copyright; counts only")
    D = os.path.join(HERE, "trial_tables"); os.makedirs(D, exist_ok=True); json.dump(out, open(os.path.join(D, "3-4_leadsheet_sung.json"), "w")); json.dump(dict(names=names, rows=[[round(float(r[n]), 5) for n in names] for r in R], songs=len(R), source=src), open(os.path.join(D, "3-4_leadsheet_sung.rows.json"), "w"))
    print(len(V), "songs;", sum(BAR.values()), "bars; windows by count", {k: sum(c.values()) for k, c in sorted(WIN.items())})
