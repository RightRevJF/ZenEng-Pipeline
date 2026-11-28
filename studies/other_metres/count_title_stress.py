"""Mark 2 as rewritten (28 Nov 02:33 ET): each fresh line's share of stressed syllables on a beat, over what its stresses and beats allow (min(1, beats / stresses), the beats of its sung bars); a line's figure is its median over the builds where it was drawn fresh; each title line drawn fresh against the median of the other fresh lines' figures. Also mark 3 of 749.250: how often a section's last line begins its last syllable at or past its slot's end.
python3 studies/other_metres/count_title_stress.py RECORD.song.json [BUILDS] -> prints JSON. A count."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, metre_engine as M
def read(record, builds=600, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = set(sp.get("hooks", ())); V = collections.defaultdict(list); rng = random.Random(seed); made = 0; over = 0; lasts = {(s, len(E.LINES[s]) - 1) for s in E.SUNG}; nb = len(E.BEATS)
    for _ in range(builds):
        c, err = E.build(rng)
        if err: continue
        made += 1; by = collections.defaultdict(list); lo = collections.defaultdict(int)
        for x in c["notes"]:
            if x["stress"]: by[(x["sec"], x["line"])].append(E.on_beat(x["on"]))
            lo[(x["sec"], x["line"])] = max(lo[(x["sec"], x["line"])], x["on"])
        over += any(lo[k] - E.line_start(*k) >= E.slot_len(*k) for k in lasts if k in lo)
        for (s_, i_), v in by.items():
            if E._made.get((s_, i_)) in ("fresh", "870 wait"):
                sy = E.LINES[s_][i_]; sb = E.SUNGB.get(id(sy)) or E.SLOTS[s_][i_]; ceil = min(1.0, nb * sb / float(sum(1 for x in sy if x[1]))); V[f"{s_}:{i_}"].append(float(np.mean(v)) / ceil)
    fig = {k: float(np.median(v)) for k, v in V.items() if len(v) >= 30}; others = [v for k, v in fig.items() if k not in hooks]; med = float(np.median(others)) if others else None; titles = {k: round(v, 3) for k, v in fig.items() if k in hooks}
    return dict(builds=builds, made=made, other_fresh_lines=len(others), their_median_share_over_ceiling=None if med is None else round(med, 3), title_lines_drawn_fresh_share_over_ceiling=titles, every_title_line_at_or_over=bool(med is not None and all(v >= med - 1e-9 for v in titles.values())), builds_where_a_sections_last_line_begins_its_last_syllable_past_its_slot=over)
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600)))
