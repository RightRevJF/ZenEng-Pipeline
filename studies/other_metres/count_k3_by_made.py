"""K3 by how each line was made: on living builds, stressed syllables on the bar's first beat and off the beat, for lines drawn fresh, title lines, lines sung again (the lyric's), copies, and lines made by 818.  python3 studies/other_metres/count_k3_by_made.py RECORD.song.json [BUILDS] -> prints JSON. A count."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, builds=400, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = set(sp.get("hooks", ())); G = collections.defaultdict(lambda: [0, 0, 0]); rng = random.Random(seed); n = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1
        for x in c["notes"]:
            if not x["stress"]: continue
            k = (x["sec"], x["line"]); made = E._made.get(k, "?"); g = "title line" if f"{k[0]}:{k[1]}" in hooks and made in ("fresh", "870 wait") else made
            for key in ("all", g): v = G[key]; v[0] += 1; v[1] += x["on"] % E.BAR == 0; v[2] += not E.on_beat(x["on"])
    tot = G["all"][0]; return dict(living_builds=n, by_how_made={k: dict(share_of_stressed_syllables=round(v[0] / tot, 3), on_the_first_beat=round(v[1] / v[0], 3), off_the_beat=round(v[2] / v[0], 3)) for k, v in sorted(G.items(), key=lambda x: -x[1][0])})
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 400), indent=1))
