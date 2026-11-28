"""For each build that stops at "the syllables cannot fit the window": the line ahead of the line that failed, how it was made, its slot, and whether its last syllable begins past its own slot.  python3 studies/other_metres/why_no_fit_ahead.py RECORD.song.json [BUILDS] -> prints JSON"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, builds=300, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); orig = E.tmin; last = {}
    def tm(lines, k):
        v = orig(lines, k)
        if k: ps, pj = E.KEYS[k - 1]; last["x"] = (E.KEYS[k], (ps, pj), lines[(ps, pj)][-1][0], E.slot_len(ps, pj), E._made.get((ps, pj)), v)
        return v
    E.tmin = tm; rng = random.Random(seed); C = collections.Counter(); stopped = 0; over = 0; made = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if not err: made += 1; continue
        if "cannot fit" not in str(err[0]): continue
        stopped += 1; cur, prev, laston, slot, how, v = last["x"]; o = laston >= slot; over += o; hw = E.HOW.get(prev, ["fresh"]); src = (hw[1], hw[2]) if hw[0] in ("again", "copy") else None
        C[(f"{cur[0]}:{cur[1]}", f"{prev[0]}:{prev[1]}", how, slot // E.BAR, E.SUNGB.get(id(E.LINES[prev[0]][prev[1]])), (f"{src[0]}:{src[1]}", E.SLOTS[src[0]][src[1]]) if src else None, bool(o))] += 1
    return dict(builds=builds, made=made, stopped_at_cannot_fit=stopped, of_them_the_line_ahead_begins_its_last_syllable_past_its_own_slot=over, rows=[dict(line=k[0], line_ahead=k[1], line_ahead_made=k[2], line_ahead_slot_bars=k[3], line_ahead_sung_bars=k[4], line_ahead_source_and_its_slot_bars=k[5], line_ahead_overruns=k[6], builds=v) for k, v in C.most_common()])
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 300), indent=1))
