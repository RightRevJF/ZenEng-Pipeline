"""840's deaths with 749.244 on: how the first title line was drawn in builds that die on 840 and in those that do not (a kept window, the weighted rule 760, the one-bar path 876), and the earliest start left to it.  python3 studies/other_metres/count_840_path.py RECORD.song.json [BUILDS] -> prints JSON. A count; the engine is not changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, builds=600, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = [h for h in sp.get("hooks", ()) if E.HOW.get((h.rsplit(":", 1)[0], int(h.rsplit(":", 1)[1])), ["fresh"])[0] not in ("copy", "again")]; ids = {id(E.LINES[h.rsplit(":", 1)[0]][int(h.rsplit(":", 1)[1])]): h for h in hooks}; ow = E.weighted; orr = E.rhythm; seen = {}
    def weighted(rng, sy, tmin, end):
        o = ow(rng, sy, tmin, end)
        if id(sy) in ids: seen[ids[id(sy)]]["weighted"] = True
        return o
    def rhythm(rng, sy, tmin, slot, cap=None, hook=False, room=None):
        if id(sy) in ids: d = seen.setdefault(ids[id(sy)], dict(weighted=False, tmin=tmin, calls=0, hook=hook)); d["calls"] += 1
        return orr(rng, sy, tmin, slot, cap=cap, hook=hook, room=room)
    E.weighted = weighted; E.rhythm = rhythm; rng = random.Random(seed); T = collections.defaultdict(collections.Counter); made = 0; k0 = {s: v for s, v in E.stats.items()}
    for _ in range(builds):
        seen.clear(); c, err = E.build(rng)
        if err: continue
        made += 1; died = (E.gates(c) or "").startswith("840")
        for h in hooks:
            d = seen.get(h)
            if not d: T[h][("died on 840" if died else "did not", "not drawn by rhythm()")] += 1; continue
            s_, i_ = h.rsplit(":", 1); U = E.line_start(s_, int(i_)); ons = sorted(x["on"] - U for x in c["notes"] if x["sec"] == s_ and x["line"] == int(i_)); st = [x["on"] for x in c["notes"] if x["sec"] == s_ and x["line"] == int(i_) and x["stress"]]; ok = 2 * sum(1 for t in st if E.on_beat(t)) >= len(st)
            T[h][("died on 840" if died else "did not", "the weighted rule (760)" if d["weighted"] else "a kept window", "earliest start " + ("on or before the bar line" if d["tmin"] <= 0 else "after it"), "the line itself passes 840's test" if ok else "the line itself fails it", "all in one bar" if ons[-1] < E.BAR else "over its bars")] += 1
    return dict(builds=builds, made=made, title_lines_drawn_fresh={h: {" | ".join(k): v for k, v in sorted(c.items(), key=lambda x: -x[1])} for h, c in T.items()})
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600), indent=1))
