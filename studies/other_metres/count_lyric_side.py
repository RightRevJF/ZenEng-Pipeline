"""PREDICTION_count_lyric_side.md: on a lyric and its plan (no notes made), how often a line has the syllable count of the line two above, of the line above, and of the line it is marked to sing again; and on the pop 3/4 clips, how often a two-bar unit has the note count of the unit two before and of the unit before, and then the same rhythm.  python3 studies/other_metres/count_lyric_side.py NAME=LYRIC.json ... -> prints JSON."""
import os, sys, json, gzip, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "lib", "luthier"), os.path.join(HERE, "..", "..", "lib", "carol"), os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
def lyric(path):
    L = json.load(open(path)); r = SL.plan(L); spec = r[0]; E = type("P", (), {})(); E.SUNG = [s_ for s_, _, _ in spec["sung"]]; E.LINES = {s_: ls for s_, _, ls in spec["sung"]}; E.HOW = {(k.rsplit(":", 1)[0], int(k.rsplit(":", 1)[1])): v for k, v in spec.get("how", {}).items()}; two = [0, 0]; one = [0, 0]; ag = [0, 0]; dist = collections.Counter(); lens = []
    for sec in E.SUNG:
        n = [len(sy) for sy in E.LINES[sec]]; lens += n
        for i in range(len(n)):
            if i >= 2: two[0] += 1; two[1] += n[i] == n[i - 2]
            if i >= 1: one[0] += 1; one[1] += n[i] == n[i - 1]
    for (sec, i), h in E.HOW.items():
        if h[0] in ("again", "copy"): d = len(E.LINES[sec][i]) - len(E.LINES[h[1]][h[2]]); ag[0] += 1; ag[1] += d == 0; dist["the same" if d == 0 else "one apart" if abs(d) == 1 else "two or three apart" if abs(d) <= 3 else "more than three"] += 1
    sh = lambda v: round(v[1] / v[0], 3) if v[0] else None
    return dict(title=L.get("title"), metre=L.get("metre", "4/4"), lines=len(lens), median_syllables_a_line=sorted(lens)[len(lens) // 2], the_count_of_the_line_two_above=sh(two), of_the_line_above=sh(one), marked_lines=ag[0], the_count_of_the_line_it_sings_again=sh(ag), marked_lines_by_distance={k: round(v / ag[0], 3) for k, v in dist.most_common()} if ag[0] else None)
def clips():
    import hooktheory_tables as HT
    D = json.load(gzip.open(HT.SRC)); c2 = [0, 0, 0]; c1 = [0, 0, 0]; n = 0
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != (3, 4) or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns is None: continue
        ons = [q[0] for q in ns]; b0 = ons[0] // 36
        if ons[-1] // 36 - b0 + 1 < 6: continue
        n += 1; U = collections.defaultdict(list)
        for o in ons: U[(o // 36 - b0) // 2].append(o - (b0 + 2 * ((o // 36 - b0) // 2)) * 36)
        for k_ in U:
            for back, c in ((2, c2), (1, c1)):
                if k_ - back in U: c[0] += 1; s = len(U[k_]) == len(U[k_ - back]); c[1] += s; c[2] += s and tuple(U[k_]) == tuple(U[k_ - back])
    f = lambda c: dict(units=c[0], the_same_note_count=round(c[1] / c[0], 3), of_those_the_same_rhythm=round(c[2] / max(1, c[1]), 3), the_same_rhythm_over_all=round(c[2] / c[0], 3))
    return dict(clips=n, the_unit_two_before=f(c2), the_unit_before=f(c1))
if __name__ == "__main__":
    out = {}
    for a in sys.argv[1:]: name, p = a.split("=", 1); out[name] = lyric(p)
    out["pop 3/4 clips"] = clips(); print(json.dumps(out, indent=1))
