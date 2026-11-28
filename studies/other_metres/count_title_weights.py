"""What narrows the title line's choice: the draw's own weights for the passing kept windows of each two-bar title line (kept count, the stress score at the title's doubled pull of 2.8, at a line's ordinary 1.4, and at none; the entry's share; the cut to the twelve best), and the commonest window's share under each.
python3 studies/other_metres/count_title_weights.py RECORD.song.json -> prints JSON. A count from the draw's own formula (metre_engine.rhythm); nothing is run."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); out = {}
    for h in sp.get("hooks", ()):
        s_, i_ = h.rsplit(":", 1); sy = E.LINES[s_][int(i_)]
        if E.HOW.get((s_, int(i_)), ["fresh"])[0] in ("copy", "again") or sp["sung_bars"][s_][int(i_)] != 2: continue
        n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); rows = []
        for p in sorted({0, min(1, lead), min(2, lead)}):
            for w, c in E.kept_windows(n - p, 2):
                if w[0] != 0 and p > 0: continue
                if E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o in w if o < E.BAR) <= 2: continue
                ons = [-6 * (p - j) for j in range(p)] + list(w); st = [t for t, x in zip(ons, sy) if x[1]]
                if st and 2 * sum(1 for t in st if E.on_beat(t)) < len(st): continue
                e = E.ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]; rows.append((c, E.stress_score(ons, sy), e))
        def top(mult, entry=True, cut=True):
            sc = sorted((math.log(c + 1) + mult * s + (math.log(e) if entry and e > 0 else (-1e9 if entry else 0)) for c, s, e in rows), reverse=True); sc = sc[:12] if cut else sc; ws = [math.exp(x - sc[0]) for x in sc]; return round(ws[0] / sum(ws), 3)
        cs = sorted((c for c, s, e in rows), reverse=True); ss = [s for c, s, e in rows]
        out[h] = dict(syllables=n, stressed=sum(1 for x in sy if x[1]), passing_windows=len(rows), commonest_share=dict(by_kept_count_alone=round(cs[0] / sum(cs), 3), the_draw_as_built_pull_2_8_entry_and_cut=top(2.8), pull_1_4_entry_and_cut=top(1.4), no_stress_pull_entry_and_cut=top(0.0), pull_2_8_no_entry_weight=top(2.8, entry=False), pull_2_8_no_cut=top(2.8, cut=False)), stress_score_range_over_the_passing_windows=[round(min(ss), 2), round(max(ss), 2)])
    return out
if __name__ == "__main__": print(json.dumps(read(sys.argv[1]), indent=1))
