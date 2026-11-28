"""PREDICTION_count_dense_fast.md: in the pop 3/4 clips, notes a bar and notes a second against the bar's length in seconds. python3 -I studies/other_metres/count_dense_fast.py -> prints JSON. The corpus stays outside the repository."""
import os, sys, json, gzip, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "lib", "luthier"), os.path.join(HERE, "..", "..", "lib", "carol"), os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, hooktheory_tables as HT
from scipy.stats import spearmanr
if __name__ == "__main__":
    D = json.load(gzip.open(HT.SRC)); rows = []
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != (3, 4) or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns is None: continue
        t = (x.get("alignment") or {}).get("refined") or (x.get("alignment") or {}).get("user")
        if not t or len(t["beats"]) < 2: continue
        sec_bar = (t["times"][-1] - t["times"][0]) / (t["beats"][-1] - t["beats"][0]) * 3; bars = len(set(n[0] // 36 for n in ns)); rows.append((sec_bar, len(ns) / bars, len(ns) / bars / sec_bar))
    q = lambda v: [round(float(a), 2) for a in np.percentile(v, (10, 25, 50, 75, 90))]
    bands = [("under 1.1 s", 0, 1.1), ("1.1 to 1.5 s", 1.1, 1.5), ("1.5 to 2.0 s", 1.5, 2.0), ("over 2.0 s", 2.0, 99)]
    out = dict(source="Hooktheory clips written in 3/4, the pop table's filter, with a timing; a clip at a time; bars with a note in them", clips=len(rows), seconds_a_bar=q([r[0] for r in rows]), rank_correlation_of_notes_a_bar_with_seconds_a_bar=round(float(spearmanr([r[0] for r in rows], [r[1] for r in rows])[0]), 3), rank_correlation_of_notes_a_second_with_seconds_a_bar=round(float(spearmanr([r[0] for r in rows], [r[2] for r in rows])[0]), 3),
               by_bar_length={name: dict(clips=len(v), notes_a_bar_p10_25_50_75_90=q([r[1] for r in v]), notes_a_second_p10_25_50_75_90=q([r[2] for r in v])) for name, lo, hi in bands for v in [[r for r in rows if lo <= r[0] < hi]] if v})
    out["bars_of_0_9_to_1_1_s_like_song_68"] = (lambda v: dict(clips=len(v), notes_a_bar_p10_25_50_75_90=q([r[1] for r in v]), share_at_or_over_3_5_notes_a_bar=round(float(np.mean([r[1] >= 3.5 for r in v])), 3)))([r for r in rows if 0.9 <= r[0] < 1.1])
    print(json.dumps(out, indent=1))
