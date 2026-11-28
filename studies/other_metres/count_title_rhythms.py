"""How many distinct rhythms each title line drawn fresh takes over the builds made, and the share of the commonest.  python3 studies/other_metres/count_title_rhythms.py RECORD.song.json [BUILDS] -> prints JSON. A count."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, builds=600, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = [h for h in sp.get("hooks", ()) if E.HOW.get((h.rsplit(":", 1)[0], int(h.rsplit(":", 1)[1])), ["fresh"])[0] not in ("copy", "again")]; C = {h: collections.Counter() for h in hooks}; rng = random.Random(seed); made = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err: continue
        made += 1
        for h in hooks: s_, i_ = h.rsplit(":", 1); U = E.line_start(s_, int(i_)); C[h][tuple(sorted(x["on"] - U for x in c["notes"] if x["sec"] == s_ and x["line"] == int(i_)))] += 1
    return dict(builds=builds, made=made, title_lines={h: dict(distinct_rhythms=len(c), commonest_share=round(c.most_common(1)[0][1] / made, 3), rhythms_in_ten_builds_or_more=sum(1 for v in c.values() if v >= 10)) for h, c in C.items()})
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 600)))
