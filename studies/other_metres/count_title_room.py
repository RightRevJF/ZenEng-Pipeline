"""What the title's room costs and whether 749.244 makes it unneeded: for each title line, its syllables, the bars the density rule gave it and the bars the title's room raised it to, and at each bar count how many kept windows (with the engine's pickups) pass 840's own test (half the line's stresses on a beat).
python3 studies/other_metres/count_title_room.py RECORD.song.json -> prints JSON. A count; nothing is run."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def passing(E, sy, bars):
    """kept windows offered to this line at this many bars, and how many pass 840's test; a line of three or four bars is read in its two parts, as the draw does"""
    def one(part, b):
        n = len(part); lead = next((k for k, x in enumerate(part) if x[1]), n); tot = ok = 0
        for p in sorted({0, min(1, lead), min(2, lead)}):
            for w, c in E.kept_windows(n - p, b):
                if w[0] != 0 and p > 0: continue
                if b == 2 and E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o in w if o < E.BAR) <= 2: continue
                ons = [-6 * (p - j) for j in range(p)] + list(w); st = [t for t, x in zip(ons, part) if x[1]]; tot += 1; ok += (not st) or 2 * sum(1 for t in st if E.on_beat(t)) >= len(st)
        return tot, ok
    if bars == 2: return one(sy, 2)
    n1 = (len(sy) + 1) // 2 if bars == 4 else int(round(2 * len(sy) / 3.0)); a = one(sy[:n1], 2); b = one(sy[n1:], 2 if bars == 4 else 1); return [a, b]
def read(record):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); tr = sp.get("title_room") or {}; out = {}; back = 0
    for h in sp.get("hooks", ()):
        s_, i_ = h.rsplit(":", 1); sy = E.LINES[s_][int(i_)]; now = sp["sung_bars"][s_][int(i_)]; was = tr.get(h, [now])[0]; w2 = passing(E, sy, was) if was in (2, 3, 4) else None; fits = (w2[1] > 0) if was == 2 else all(x[1] > 0 for x in w2)
        out[h] = dict(syllables=len(sy), stressed=sum(1 for x in sy if x[1]), bars_by_the_density_rule=was, bars_now=now, raised_by_the_titles_room=now - was, kept_windows_offered_and_passing_840_at_the_density_rules_bars=w2, a_passing_window_exists_there=bool(fits), how=E.HOW.get((s_, int(i_)), ["fresh"])[0]); back += (now - was) if fits else 0
    dens = {s: [sum(len(x) for x in E.LINES[s]), sum(sp["sung_bars"][s]), round(sum(len(x) for x in E.LINES[s]) / sum(sp["sung_bars"][s]), 3)] for s in sp["sung_bars"]}; tot = [sum(v[0] for v in dens.values()), sum(v[1] for v in dens.values())]; raised = sum(v["raised_by_the_titles_room"] for v in out.values())
    return dict(title_lines=out, by_section_syllables_bars_density=dens, whole_song=tot + [round(tot[0] / tot[1], 3)], bars_the_titles_room_added=raised, bars_that_could_come_back_where_a_passing_window_exists=back, whole_song_if_they_did=round(tot[0] / (tot[1] - back), 3), table_middle_half=E.T["readings_quartiles"]["notes a bar"])
if __name__ == "__main__": print(json.dumps(read(sys.argv[1]), indent=1))
