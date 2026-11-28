"""What the join to the line ahead (929) refuses when a line the lyric marks "again" is sung again: its own run of one pitch too long, or a run carried in from the line ahead that a step does not mend; with the source's notes against the line's syllables, and the longest run in the source itself.
python3 studies/other_metres/why_join_refuses.py RECORD.song.json [BUILDS] -> prints JSON. A count; the engine is not changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def longest(ps):
    b = r = 1
    for a, c in zip(ps, ps[1:]): r = r + 1 if a == c else 1; b = max(b, r)
    return b
def read(record, builds=300, seed=1):
    R = json.load(open(record)); E = M.Engine(R["spec"]); oa = E.again; oj = E.join; cur = {}; why = collections.Counter(); byline = collections.defaultdict(collections.Counter); shape = collections.Counter(); srcrun = collections.Counter(); tries = [0]
    def again(rng, src, src_st0, sy, U, sec, i, tmin, slot):
        r = oa(rng, src, src_st0, sy, U, sec, i, tmin, slot)
        if not getattr(E, "_818", False) and r is not None: tries[0] += 1; cur.clear(); cur.update(key=f"{sec}:{i}", r=r, n=len(sy), src=[p for _, p in src])
        return r
    def join(r, lines, k, sec, i):
        r2 = oj(r, lines, k, sec, i)
        if cur and cur.get("key") == f"{sec}:{i}" and cur.get("r") is r:
            if r2 is None:
                ps = [p for _, p in r]; own = not E.runs_ok(ps, E.RUN); w = "the line's own run of one pitch is over the cap" if own else "a run carried in from the line ahead, not mended by a step"; why[w] += 1; byline[cur["key"]][w] += 1
                if own: shape[(len(cur["src"]), cur["n"], longest(cur["src"]), longest(ps))] += 1
            cur.clear()
        return r2
    E.again = again; E.join = join; rng = random.Random(seed); made = 0
    for _ in range(builds):
        c, err = E.build(rng); made += not err
    return dict(builds=builds, made=made, aimed=bool(E.AIM), run_cap=E.RUN, tries_that_reached_the_join=tries[0], refused=dict(why.most_common()), by_line={k: dict(v) for k, v in sorted(byline.items(), key=lambda x: -sum(x[1].values()))[:6]}, own_run_cases_source_notes_own_syllables_longest_run_in_source_and_in_the_line=[[a, b, c, d, n] for (a, b, c, d), n in shape.most_common(8)])
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 300), indent=1))
