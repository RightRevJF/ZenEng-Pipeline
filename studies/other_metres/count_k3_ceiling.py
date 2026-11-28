"""K3's ceiling and floor on a plan: for each line, from the kept windows the draw may offer it at its planned bars (the engine's pickups; the title lines only among windows that pass 840's test; the pickup-shaped windows left out where the record says so), the most stressed syllables any window puts on the bar's first beat (the ceiling), the fewest off the beat, and what the windows give when taken by kept count alone (the floor of the trade). Summed over the song and divided by its stressed syllables.
python3 studies/other_metres/count_k3_ceiling.py RECORD.song.json -> prints JSON. A count from the table and the plan; nothing is run."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def part(E, sy, bars, hook):
    """-> [(kept count, stressed on the first beat, stressed off the beat)] for every window offered"""
    n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); out = []
    for p in sorted({0, min(1, lead), min(2, lead)}):
        for w, c in E.kept_windows(n - p, bars):
            if w[0] != 0 and p > 0: continue
            if bars == 2 and E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o in w if o < E.BAR) <= 2: continue
            ons = [-6 * (p - j) for j in range(p)] + list(w); st = [t for t, x in zip(ons, sy) if x[1]]
            if hook and E.S.get("title_840") and st and 2 * sum(1 for t in st if E.on_beat(t)) < len(st): continue
            out.append((c, sum(1 for t in st if t % E.BAR == 0), sum(1 for t in st if not E.on_beat(t))))
    return out
def read(record):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); hooks = set(sp.get("hooks", ())); tot = 0; best1 = 0; bestoff = 0; exp1 = 0.0; expoff = 0.0; nowin = []; fresh = dict(tot=0, best1=0, exp1=0.0, bestoff=0, expoff=0.0); rows = []
    for s_, i_ in E.KEYS:
        sy = E.LINES[s_][i_]; st = sum(1 for x in sy if x[1]); sb = E.SUNGB.get(id(sy)) or E.SLOTS[s_][i_]; hook = f"{s_}:{i_}" in hooks
        if sb == 2: parts = [(sy, 2)]
        else: n1 = (len(sy) + 1) // 2 if sb == 4 else int(round(2 * len(sy) / 3.0)); parts = [(sy[:n1], 2), (sy[n1:], 2 if sb == 4 else 1)]
        b1 = bo = 0; e1 = eo = 0.0; ok = True
        for syp, b in parts:
            ws = part(E, syp, b, hook)
            if not ws: ok = False; break
            t = float(sum(c for c, _, _ in ws)); b1 += max(x for _, x, _ in ws); bo += min(x for _, _, x in ws); e1 += sum(c * x for c, x, _ in ws) / t; eo += sum(c * x for c, _, x in ws) / t
        if not ok: nowin.append(f"{s_}:{i_}"); continue
        tot += st; best1 += b1; bestoff += bo; exp1 += e1; expoff += eo; how = E.HOW.get((s_, i_), ["fresh"])[0]
        if how not in ("again", "copy"): fresh["tot"] += st; fresh["best1"] += b1; fresh["exp1"] += e1; fresh["bestoff"] += bo; fresh["expoff"] += eo
        rows.append([f"{s_}:{i_}", len(sy), st, sb, how, b1, round(e1, 2)])
    r = lambda a, b: round(a / b, 3) if b else None
    return dict(lines=len(E.KEYS), lines_with_no_kept_window_at_their_bars=nowin, stressed_syllables_counted=tot, ceiling_first_beat=r(best1, tot), by_kept_count_alone_first_beat=r(exp1, tot), floor_off_the_beat=r(bestoff, tot), by_kept_count_alone_off_the_beat=r(expoff, tot), lines_not_sung_again_or_copied=dict(stressed=fresh["tot"], ceiling_first_beat=r(fresh["best1"], fresh["tot"]), by_kept_count_alone_first_beat=r(fresh["exp1"], fresh["tot"]), floor_off_the_beat=r(fresh["bestoff"], fresh["tot"]), by_kept_count_alone_off_the_beat=r(fresh["expoff"], fresh["tot"])), note="the ceiling takes each line's best window for the first beat and the floor each line's best for off the beat; one window need not be both, so the two are separate bounds", by_line=rows)
if __name__ == "__main__": print(json.dumps(read(sys.argv[1]), indent=1))
