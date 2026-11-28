"""What the title line's formula leaves out: for a title line drawn fresh, the earliest start and the latest last onset it is given in each build, the windows that survive those limits, and the commonest window's share the draw's own formula gives among the survivors; beside what the builds show, and how often the line is sung in one bar (876).
python3 studies/other_metres/count_title_limits.py RECORD.song.json SECTION:LINE [BUILDS] -> prints JSON. A count; the engine is not changed."""
import os, sys, json, math, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import metre_engine as M
def read(record, key, builds=600, seed=1):
    R = json.load(open(record)); sp = R["spec"]; E = M.Engine(sp); s_, i_ = key.rsplit(":", 1); i_ = int(i_); sy = E.LINES[s_][i_]; orr = E.rhythm; seen = {}; pull = sp.get("title_pull", 2.8)
    def rhythm(rng, sy2, tmin, slot, cap=None, hook=False, room=None):
        if sy2 is sy and slot == 2 * E.BAR and "tmin" not in seen: seen.update(tmin=tmin, cap=cap, room=room)
        return orr(rng, sy2, tmin, slot, cap=cap, hook=hook, room=room)
    E.rhythm = rhythm; n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); rows = []
    for p in sorted({0, min(1, lead), min(2, lead)}):
        for w, c in E.kept_windows(n - p, 2):
            if w[0] != 0 and p > 0: continue
            if E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o in w if o < E.BAR) <= 2: continue
            ons = [-6 * (p - j) for j in range(p)] + list(w); st = [t for t, x in zip(ons, sy) if x[1]]
            if st and 2 * sum(1 for t in st if E.on_beat(t)) < len(st): continue
            e = E.ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]; rows.append((tuple(ons), math.log(c + 1) + pull * E.stress_score(ons, sy) + math.log(e)))
    rng = random.Random(seed); L = collections.Counter(); got = collections.Counter(); onebar = 0; made = 0; pred = collections.Counter()
    for _ in range(builds):
        seen.clear(); c, err = E.build(rng)
        if err: continue
        made += 1; U = E.line_start(s_, i_); ons = tuple(sorted(x["on"] - U for x in c["notes"] if x["sec"] == s_ and x["line"] == i_)); got[ons] += 1; onebar += ons[-1] < E.BAR
        if "tmin" in seen:
            rm = (12 if E.LE else E.BREATH) if seen["room"] is None else seen["room"]; end = 2 * E.BAR - rm if seen["cap"] is None else min(2 * E.BAR - rm, seen["cap"]); L[(seen["tmin"], end)] += 1
    for (tm, end), k in L.items():
        ok = sorted(((o, s) for o, s in rows if o[0] >= tm and o[-1] <= end), key=lambda x: -x[1])[:12]
        if not ok: pred[("none fits", )] += k; continue
        ws = [math.exp(s - ok[0][1]) for _, s in ok]; tot = sum(ws)
        for (o, _), w in zip(ok, ws): pred[o] += k * w / tot
    top = got.most_common(1)[0]; tp = max(pred.items(), key=lambda x: x[1]) if pred else (None, 0)
    return dict(line=key, syllables=n, builds_made=made, passing_windows=len(rows), limits_earliest_start_and_latest_last_onset={f"{a}, {b}": k for (a, b), k in L.most_common(6)}, windows_inside_the_commonest_limits=sum(1 for o, s in rows if L and o[0] >= L.most_common(1)[0][0][0] and o[-1] <= L.most_common(1)[0][0][1]), commonest_share_the_formula_gives_inside_the_limits=round(tp[1] / max(1, sum(L.values())), 3), the_formulas_commonest=list(tp[0]) if tp[0] else None, commonest_share_in_the_builds=round(top[1] / made, 3), the_builds_commonest=list(top[0]), the_same_rhythm=bool(tp[0] == top[0]), sung_all_in_one_bar_share=round(onebar / made, 3))
if __name__ == "__main__": print(json.dumps(read(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 600), indent=1))
