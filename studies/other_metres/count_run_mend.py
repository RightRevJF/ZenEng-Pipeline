"""749.247's mend, counted: how many lines sung again have a note moved, and for the moved notes that fall on a beat, whether they are chord tones after the move, against the same notes before the move and against the source line's own notes on a beat.
python3 studies/other_metres/count_run_mend.py RECORD.song.json [BUILDS] -> prints JSON. A count: each line is sung again twice from one random state, with the mend and without, and compared; the engine is not changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, builds=300, seed=1):
    R = json.load(open(record)); E = M.Engine(R["spec"]); oa = E.again; C = collections.Counter(); lines_made = {}
    def again(rng, src, src_st0, sy, U, sec, i, tmin, slot):
        st = rng.getstate(); E.S["again_runs"] = False
        try: r0 = oa(rng, src, src_st0, sy, U, sec, i, tmin, slot)
        finally: E.S["again_runs"] = True
        rng.setstate(st); r1 = oa(rng, src, src_st0, sy, U, sec, i, tmin, slot)
        if getattr(E, "_818", False) or r1 is None or r0 is None or len(r0) != len(r1): return r1
        C["lines sung again (the lyric's own)"] += 1; moved = [(t, a, b) for (t, a), (_, b) in zip(r0, r1) if a != b]
        if moved: C["of them with a note moved"] += 1
        C["notes"] += len(r1); C["notes moved"] += len(moved)
        for t, a, b in moved:
            ch = E.chord_at(U + t)
            if E.on_beat(U + t): C["moved notes on a beat"] += 1; C["of them a chord tone before the move"] += a % 12 in ch; C["of them a chord tone after the move"] += b % 12 in ch
        hw = E.HOW.get((sec, i), ["fresh"])
        if hw[0] == "again":
            U2 = E.line_start(hw[1], hw[2])
            for t, p in src:
                if E.on_beat(U2 + t): C["source line's notes on a beat"] += 1; C["of them chord tones"] += p % 12 in E.chord_at(U2 + t)
        for t, p in r1:
            if E.on_beat(U + t): C["the copy's notes on a beat (with the mend)"] += 1; C["of them chord tones "] += p % 12 in E.chord_at(U + t)
        for t, p in r0:
            if E.on_beat(U + t): C["the copy's notes on a beat (without the mend)"] += 1; C["of them chord tones  "] += p % 12 in E.chord_at(U + t)
        return r1
    E.again = again; rng = random.Random(seed); made = 0
    for _ in range(builds):
        c, err = E.build(rng); made += not err
    sh = lambda a, b: round(C[a] / C[b], 3) if C[b] else None
    return dict(builds=builds, made=made, counts=dict(C), share_of_lines_sung_again_with_a_note_moved=sh("of them with a note moved", "lines sung again (the lyric's own)"), share_of_notes_moved=sh("notes moved", "notes"), moved_notes_on_a_beat_chord_tone_share_before=sh("of them a chord tone before the move", "moved notes on a beat"), moved_notes_on_a_beat_chord_tone_share_after=sh("of them a chord tone after the move", "moved notes on a beat"), source_lines_notes_on_a_beat_chord_tone_share=sh("of them chord tones", "source line's notes on a beat"), the_copys_notes_on_a_beat_chord_tone_share_with_the_mend=sh("of them chord tones ", "the copy's notes on a beat (with the mend)"), without_the_mend=sh("of them chord tones  ", "the copy's notes on a beat (without the mend)"))
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 300), indent=1))
