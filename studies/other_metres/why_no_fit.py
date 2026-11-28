"""Why a line cannot be fitted: for each build that stops at "the syllables cannot fit the window", the line, its syllables, the earliest start left to it (tmin), its latest end, the places left on the sixteenth grid, and the kept windows of its count.  python3 studies/other_metres/why_no_fit.py RECORD.song.json [BUILDS] -> prints JSON"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np, metre_engine as M
def read(record, builds=300, seed=1):
    R = json.load(open(record)); E = M.Engine(R["spec"]); log = []; orig = E.rhythm; depth = [0]
    def wrapped(rng, sy, tmin, slot, cap=None, hook=False, room=None):
        depth[0] += 1
        try: o = orig(rng, sy, tmin, slot, cap=cap, hook=hook, room=room)
        finally: depth[0] -= 1
        log.append(dict(depth=depth[0], n=len(sy), tmin=tmin, slot=slot, cap=cap, room=room, ok=o is not None, first=None if o is None else o[0], last=None if o is None else o[-1])); return o
    E.rhythm = wrapped; rng = random.Random(seed); rows = collections.defaultdict(list); made = 0
    for _ in range(builds):
        del log[:]; c, err = E.build(rng)
        if not err: made += 1; continue
        if "cannot fit" not in str(err[0]): continue
        top = [x for x in log if x["depth"] == 0]; last = top[-1] if top else None; inner = [x for x in log if not x["ok"]]; f = inner[0] if inner else last
        if f is None: continue
        rm = (12 if E.LE else E.BREATH) if f["room"] is None else f["room"]; end = f["slot"] - rm if f["cap"] is None else min(f["slot"] - rm, f["cap"]); places = len(range(int(-(-max(f["tmin"], -12) // 3) * 3), int(end) + 1, 3))
        rows[f"{err[1]}:{err[2]}"].append(dict(n=f["n"], tmin=f["tmin"], end=end, places=places, too_few_places=places < f["n"], bars=f["slot"] // E.BAR))
    out = {}
    for k, v in rows.items():
        s_, i_ = k.rsplit(":", 1); sy = E.LINES[s_][int(i_)]; n = v[0]["n"]; bars = v[0]["bars"]; kw = E.kept_windows(n, bars); pv = E.LINES[s_][int(i_) - 1] if int(i_) else None
        out[k] = dict(builds=len(v), syllables=len(sy), slot_bars=E.SLOTS[s_][int(i_)], part_that_failed=dict(syllables=n, bars=bars), kept_windows_of_that_count=len(kw), kept_windows_starting_on_the_bar_line=sum(1 for w, c in kw if w[0] == 0), earliest_start_left_median=float(np.median([x["tmin"] for x in v])), earliest_start_left_quartiles=[float(q) for q in np.percentile([x["tmin"] for x in v], (25, 75))], latest_end=v[0]["end"], too_few_places_share=round(float(np.mean([x["too_few_places"] for x in v])), 3), places_left_median=float(np.median([x["places"] for x in v])), line_ahead_syllables=len(pv) if pv else None, line_ahead_slot_bars=E.SLOTS[s_][int(i_) - 1] if pv else None, how=E.HOW.get((s_, int(i_)), ["fresh"])[0])
    return dict(builds=builds, made=made, bar=E.BAR, by_line=out)
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 300), indent=1))
