"""945 (Window 197): tables/kept_rhythm_room.json: where the kept 4/4 songs stand on the two things that carry rhythm scaling (studies/rhythm_memory). python3 lib/luthier/make_kept_rhythm_room.py"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import kept_corpus as KC, lyric_room as LR
K = [LR.read(k["t"]) for k in KC.kept_songs()]; K = [r for r in K if all(v == v for v in r.values())]
q = {c: [round(float(x), 4) for x in np.percentile([r[c] for r in K], (10, 25, 50, 75, 90))] for c in K[0]}
json.dump(dict(source=f"{len(K)} kept 4/4 songs (CoCoPops Billboard), the sung tune; made by lib/luthier/make_kept_rhythm_room.py; studied in studies/rhythm_memory", percentiles_10_25_50_75_90=q,
               what=dict(room="the share of bars, between the first and last sung note, in which nothing is sung", contrast="the spread, across windows of four bars, of onsets a bar, over the mean", rhythm_scaling="detrended fluctuation of the onsets on a grid of sixteenths")),
          open(os.path.join(HERE, "..", "..", "tables", "kept_rhythm_room.json"), "w"), indent=1); print(q)
