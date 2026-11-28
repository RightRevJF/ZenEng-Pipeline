"""Count (b): on a 6/8 record, which gate takes builds, the title lines' stressed syllables on a beat in builds that die on 840 and in those that do not, and first-beat onsets by section.  python3 studies/other_metres/count_b.py RECORD.song.json [BUILDS] -> prints JSON"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, metre_engine as M
def read(record, builds=400, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); rng = random.Random(seed); hooks = list(sp.get("hooks", ())); G = collections.Counter(); hk = collections.defaultdict(list); sec1 = collections.defaultdict(list); how = collections.defaultdict(collections.Counter); made = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err: continue
        made += 1; g = E.gates(c) or "living"; G[g.split(":")[0]] += 1
        for h in hooks:
            s_, i_ = h.rsplit(":", 1); st = [x for x in c["notes"] if x["sec"] == s_ and x["line"] == int(i_) and x["stress"]]; hk[(h, g.startswith("840"))].append(float(np.mean([E.on_beat(x["on"]) for x in st]))); how[h][E._made.get((s_, int(i_)))] += 1
        for s_ in {x["sec"] for x in c["notes"]}: sec1[s_].append(float(np.mean([x["on"] % E.BAR == 0 for x in c["notes"] if x["sec"] == s_])))
    line = lambda h: E.LINES[h.rsplit(":", 1)[0]][int(h.rsplit(":", 1)[1])]
    return dict(builds=builds, made=made, gates=dict(G), stress_scored_by_the_table=bool(sp.get("stress_place")), title_lines={h: dict(syllables=len(line(h)), stressed=sum(1 for x in line(h) if x[1]), sung_bars=E.SUNGB.get(id(line(h))), how_made=dict(how[h]), stressed_on_a_beat_median_in_builds_that_die_on_840=round(float(np.median(hk[(h, True)])), 3) if hk[(h, True)] else None, in_builds_that_do_not=round(float(np.median(hk[(h, False)])), 3) if hk[(h, False)] else None) for h in hooks}, first_beat_onsets_by_section_median={k: round(float(np.median(v)), 3) for k, v in sorted(sec1.items())}, syllables_a_sung_bar_by_section={s_: round(sum(len(x) for x in E.LINES[s_]) / sum(sp["sung_bars"][s_]), 2) for s_ in sp["sung_bars"]})
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 400), indent=1))
