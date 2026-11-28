"""PREDICTION_counts_K6.md, count 3: in the pop 3/4 clips, how often a two-bar unit takes the rhythm of the unit two before it (and one before), units counted from the clip's first sung bar; clips of six bars or more. python3 -I studies/other_metres/pop_units_again.py -> prints JSON. The corpus stays outside the repository."""
import os, sys, json, gzip, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "lib", "luthier"), os.path.join(HERE, "..", "..", "lib", "carol"), os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, hooktheory_tables as HT
BL = 36
if __name__ == "__main__":
    D = json.load(gzip.open(HT.SRC)); tot = [0, 0, 0, 0]; by2 = []; by1 = []; clips = 0
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != (3, 4) or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns is None: continue
        ons = [n[0] for n in ns]; b0 = ons[0] // BL
        if ons[-1] // BL - b0 + 1 < 6: continue
        U = collections.defaultdict(list)
        for o in ons: U[(o // BL - b0) // 2].append(o - (b0 + 2 * ((o // BL - b0) // 2)) * BL)
        c = [0, 0, 0, 0]
        for k_ in U:
            if k_ - 2 in U: c[0] += 1; c[1] += tuple(U[k_]) == tuple(U[k_ - 2])
            if k_ - 1 in U: c[2] += 1; c[3] += tuple(U[k_]) == tuple(U[k_ - 1])
        clips += 1; tot = [a + b for a, b in zip(tot, c)]
        if c[0]: by2.append(c[1] / c[0])
        if c[2]: by1.append(c[3] / c[2])
    q = lambda v: [round(float(a), 3) for a in np.percentile(v, (10, 25, 50, 75, 90))]
    print(json.dumps(dict(source="Hooktheory clips written in 3/4, the pop table's filter, six bars or more", clips=clips, units_with_a_unit_two_back=tot[0], taking_the_rhythm_two_back=round(tot[1] / tot[0], 3), by_clip_two_back_p10_25_50_75_90=q(by2), units_with_a_unit_one_back=tot[2], taking_the_rhythm_one_back=round(tot[3] / tot[2], 3), by_clip_one_back_p10_25_50_75_90=q(by1)), indent=1))
