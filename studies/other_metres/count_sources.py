"""749.252, mark 3: the lines that are later sung again, read on their first singing. On living builds: every line drawn (fresh, a title line, after 870's wait, or on a borrowed rhythm) that a later line of the build sings again (the lyric's "again", a copy sung again, or 818's), and its stressed syllables on the first beat and off the beat; the other drawn lines beside them.  python3 studies/other_metres/count_sources.py RECORD.song.json [BUILDS] -> prints JSON. A count; no note is changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
DRAWN = ("fresh", "870 wait", "818 rhythm")
def read(record, builds=400, seed=1):
    R = json.load(open(record)); E = M.Engine(R["spec"]); G = collections.defaultdict(lambda: [0, 0, 0]); rng = random.Random(seed); n = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; src = {}
        for (sec, i) in E.KEYS:
            made = E._made.get((sec, i)); how = E.HOW.get((sec, i), ["fresh"])
            if made == "again" and how[0] in ("again", "copy"): src[(sec, i)] = (how[1], how[2])
            elif made == "818 again": src[(sec, i)] = (sec, next(j for j in (i - 2, i - 1) if j >= 0 and E.HOW.get((sec, j), ["fresh"])[0] != "design"))
        roots = set()
        for k in src:
            r = src[k]
            while r in src: r = src[r]
            roots.add(r)
        for x in c["notes"]:
            if not x["stress"]: continue
            k = (x["sec"], x["line"]); made = E._made.get(k)
            if made not in DRAWN: continue
            v = G["drawn lines later sung again" if k in roots else "drawn lines not sung again"]; v[0] += 1; v[1] += x["on"] % E.BAR == 0; v[2] += not E.on_beat(x["on"])
    return dict(living_builds=n, rows={k: dict(stressed_syllables=v[0], on_the_first_beat=round(v[1] / v[0], 3), off_the_beat=round(v[2] / v[0], 3)) for k, v in sorted(G.items())})
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 400), indent=1))
