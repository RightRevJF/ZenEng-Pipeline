"""Where onsets on the bar's first beat are won and lost, on living builds of a 6/8 record: by section, by how the line was made, and by how the line opens.  python3 studies/other_metres/count_first_beat.py RECORD.song.json [BUILDS] -> prints JSON
First-beat onsets over all onsets = (sung bars whose first beat carries an onset) over (notes); so each group is read as bars hit of its sung bars, beside its notes a bar. A count; nothing is run under a changed form."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, metre_engine as M
def read(record, builds=400, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); rng = random.Random(seed); G = collections.defaultdict(lambda: [0, 0, 0, 0]); n = 0; hooks = set(sp.get("hooks", ()))      # group -> [bars, bars hit, notes, lines]
    for _ in range(builds):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; by = collections.defaultdict(list)
        for x in c["notes"]: by[(x["sec"], x["line"])].append(x["on"])
        for (s_, i_), ons in by.items():
            U = E.line_start(s_, i_); sy = E.LINES[s_][i_]; sb = E.SUNGB.get(id(sy)) or E.SLOTS[s_][i_]; rel = sorted(o - U for o in ons); hit = len({o // E.BAR for o in rel if o % E.BAR == 0 and 0 <= o < sb * E.BAR}); made = E._made.get((s_, i_), "?"); light = not sy[0][1]
            opens = ("light, takes a pickup" if rel[0] < 0 else "light, begins on the bar line" if rel[0] == 0 else "light, begins after the bar line") if light else ("stressed, begins before the bar line" if rel[0] < 0 else "stressed, begins on the bar line" if rel[0] == 0 else "stressed, begins after the bar line")
            for g in (("all", "all"), ("section", E.KIND[s_]), ("how made", "title line" if f"{s_}:{i_}" in hooks else made), ("opens", opens), ("sung bars", str(sb))):
                v = G[g]; v[0] += sb; v[1] += hit; v[2] += len(rel); v[3] += 1
    out = {}
    for (k, g), (b, h, nt, ln) in sorted(G.items()):
        out.setdefault(k, {})[g] = dict(share_of_the_songs_notes=round(nt / G[("all", "all")][2], 3), lines_a_build=round(ln / n, 1), notes_a_bar=round(nt / b, 3), bars_with_an_onset_on_the_first_beat=round(h / b, 3), first_beat_onsets_over_notes=round(h / nt, 3))
    return dict(living_builds=n, groups=out)
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 400), indent=1))
