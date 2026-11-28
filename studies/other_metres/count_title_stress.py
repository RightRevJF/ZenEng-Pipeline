"""749.249's second mark: each fresh line's stressed syllables on a beat (its median over the builds where it was drawn fresh), the title lines drawn fresh against the median of the lyric's other fresh lines.  python3 studies/other_metres/count_title_stress.py RECORD.song.json [BUILDS] -> prints JSON. A count."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, metre_engine as M
def read(record, builds=600, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = set(sp.get("hooks", ())); V = collections.defaultdict(list); rng = random.Random(seed); made = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err: continue
        made += 1; by = collections.defaultdict(list)
        for x in c["notes"]:
            if x["stress"]: by[(x["sec"], x["line"])].append(E.on_beat(x["on"]))
        for (s_, i_), v in by.items():
            if E._made.get((s_, i_)) in ("fresh", "870 wait"): V[f"{s_}:{i_}"].append(float(np.mean(v)))
    fig = {k: float(np.median(v)) for k, v in V.items() if len(v) >= 30}; others = [v for k, v in fig.items() if k not in hooks]; med = float(np.median(others)) if others else None; titles = {k: round(v, 3) for k, v in fig.items() if k in hooks}
    return dict(builds=builds, made=made, other_fresh_lines=len(others), their_median=None if med is None else round(med, 3), title_lines_drawn_fresh=titles, every_title_line_at_or_over=bool(med is not None and all(v >= med - 1e-9 for v in titles.values())))
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600)))
