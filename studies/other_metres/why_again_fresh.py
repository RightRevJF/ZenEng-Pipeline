"""Why a line the lyric marks "again" is drawn fresh (712): for each try, what turned it away.  python3 studies/other_metres/why_again_fresh.py RECORD.song.json [BUILDS] -> prints JSON
A count only; the engine is not changed. The routine that sings a line again and the join are wrapped and their results read."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, builds=300, seed=1):
    R = json.load(open(record)); E = M.Engine(R["spec"]); oa = E.again; oj = E.join; cur = {}; why = collections.Counter(); byline = collections.defaultdict(collections.Counter); tries = [0]; br = 12 if E.LE else E.BREATH; over = []; pre = collections.Counter(); cnt = collections.Counter()
    def again(rng, src, src_st0, sy, U, sec, i, tmin, slot):
        r = oa(rng, src, src_st0, sy, U, sec, i, tmin, slot)
        if not getattr(E, "_818", False):
            tries[0] += 1; cur.clear(); cur.update(key=f"{sec}:{i}", tmin=tmin, slot=slot, r=r, n=len(sy), src_n=len(src), src_first=src[0][0], src_last=src[-1][0])
            if r is None: w = "no fit: the source's notes cannot be matched to the syllables"; why[w] += 1; byline[cur["key"]][w] += 1; cur.clear()
        return r
    def join(r, lines, k, sec, i):
        r2 = oj(r, lines, k, sec, i)
        if cur and cur.get("key") == f"{sec}:{i}" and cur.get("r") is r:
            if r2 is None: w = "the join to the line ahead"
            elif r2[0][0] < cur["tmin"]: w = "begins before the line ahead leaves room"
            elif E.S.get("again_inside") and r2[-1][0] > cur["slot"] - br: w = "ends past its own slot (749.240)"; over.append(r2[-1][0] - (cur["slot"] - br)); pre[bool(r[-1][0] > cur["slot"] - br)] += 1; cnt[(cur["src_n"], cur["n"])] += 1
            elif f"{sec}:{i}" in E.TENTRY and r2[-1][0] > cur["slot"] - E.BAR: w = "the cap ahead of a title line"
            else: w = "taken, or turned away by the span limit"
            why[w] += 1; byline[cur["key"]][w] += 1; cur.clear()
        return r2
    E.again = again; E.join = join; rng = random.Random(seed); made = 0
    for _ in range(builds):
        c, err = E.build(rng); made += not err
    st = E.stats; return dict(builds=builds, made=made, tries_to_sing_a_marked_line_again=tries[0], drawn_fresh_712=sum(v for k, v in st.items() if k.startswith("712")), what_happened=dict(why.most_common()), past_its_slot=dict(by_how_many_twelfths=dict(sorted(collections.Counter(over).items())), already_past_before_the_join=pre[True], past_only_after_the_join=pre[False], source_notes_and_own_syllables=[[a, b, c] for (a, b), c in cnt.most_common(8)]), by_line={k: dict(v.most_common()) for k, v in sorted(byline.items(), key=lambda x: -sum(c for w, c in x[1].items() if not w.startswith("taken")))[:8]})
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 300), indent=1))
