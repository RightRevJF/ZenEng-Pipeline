"""PREDICTION_count_bars_again.md: which bars of a section are on a rhythm already sung, and why not. python3 studies/other_metres/count_bars_again.py NAME=LYRIC.json,RECORD.song.json ... [clips] -> prints JSON. A count; no note is changed."""
import os, sys, json, gzip, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA
def sec_stats(bars):
    """bars: ordered list of rhythm tuples -> (n, distinct, again share)"""
    seen = set(); r = 0
    for b in bars: r += b in seen; seen.add(b)
    return len(bars), len(seen), r / len(bars)
def q(v): return [round(float(a), 3) for a in np.percentile(v, (10, 25, 50, 75, 90))]
def engine(lyr, rec, builds=300):
    L = json.load(open(lyr)); R = json.load(open(rec)); E, sp = CA.engine(L, R); seen = {}; inner = E.again
    def wrapped(rng, src, src_st0, sy, U, sec, i, tmin, slot): seen[(sec, i)] = len(sy) - len(src); return inner(rng, src, src_st0, sy, U, sec, i, tmin, slot)
    E.again = wrapped; rng = random.Random(L.get("seed", 1)); S_ = collections.defaultdict(list); G = collections.defaultdict(lambda: [0, 0]); n = 0; fresh2 = []; BL = E.BAR
    for _ in range(builds):
        seen.clear(); c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; by = collections.OrderedDict()
        for x in sorted(E.as_sung(c["notes"]), key=lambda x: x["on"]): by.setdefault(x["sec"], []).append(x)
        for sec, xs in by.items():
            bars = collections.OrderedDict()
            for x in xs: bars.setdefault(x["on"] // BL, []).append(x)
            if len(bars) < 4: continue
            rh = [tuple(x["on"] % BL for x in v) for v in bars.values()]; a, d, r = sec_stats(rh); S_["bars"].append(a); S_["distinct"].append(d); S_["again"].append(r)
            if a >= 16: a2, d2, r2 = sec_stats(rh[:16]); S_["distinct16"].append(d2); S_["again16"].append(r2)
            sn = set(); fr = set()
            for (k, v), t in zip(bars.items(), rh):
                lines = []
                for x in v:
                    if x["line"] not in lines: lines.append(x["line"])
                ln = lines[0]; made = E._made.get((sec, ln), "?"); hook = f"{sec}:{ln}" in set(sp.get("hooks", ())); d_ = seen.get((sec, ln)); slot = E.slot_len(sec, ln) // BL
                what = "two lines in the bar" if len(lines) > 1 else "one line"
                kind = ("title line" if hook and made in ("fresh", "870 wait") else made) + ("" if made not in ("again", "818 again") else ", the source's count" if d_ == 0 else ", one apart" if d_ is not None and abs(d_) == 1 else ", further apart")
                ag = t in sn; sn.add(t)
                for g in ("all bars", what, "made: " + kind, "slot of %d bars" % slot): G[g][0] += 1; G[g][1] += ag
            for i_ in range(len(E.LINES[sec])):
                if E._made.get((sec, i_)) in ("fresh", "870 wait"): U = E.line_start(sec, i_); fr.add(tuple(x["on"] - U for x in xs if x["line"] == i_))
            fresh2.append(len(fr))
    tot = G["all bars"][0]
    return dict(living_builds=n, a_section=dict(sung_bars_p10_25_50_75_90=q(S_["bars"]), different_bar_rhythms=q(S_["distinct"]), bars_on_a_rhythm_already_sung=q(S_["again"]), in_the_first_16_bars_different_bar_rhythms=q(S_["distinct16"]) if S_["distinct16"] else None, in_the_first_16_bars_again=q(S_["again16"]) if S_["again16"] else None, different_rhythms_among_its_lines_drawn_fresh=q(fresh2)),
                bars_by_sort={k: dict(share_of_bars=round(v[0] / tot, 3), on_a_rhythm_already_sung=round(v[1] / v[0], 3)) for k, v in sorted(G.items(), key=lambda x: -x[1][0])})
def clips():
    import hooktheory_tables as HT
    D = json.load(gzip.open(HT.SRC)); S_ = collections.defaultdict(list); n = 0
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != (3, 4) or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns is None: continue
        bars = collections.OrderedDict()
        for o, d_, p in ns: bars.setdefault(o // 36, []).append(o % 36)
        if len(bars) < 4: continue
        n += 1; rh = [tuple(v) for v in bars.values()]; a, d, r = sec_stats(rh); S_["bars"].append(a); S_["distinct"].append(d); S_["again"].append(r)
        if a >= 16: a2, d2, r2 = sec_stats(rh[:16]); S_["distinct16"].append(d2); S_["again16"].append(r2)
        b0 = ns[0][0] // 36; U = collections.defaultdict(list)
        for o, d_, p in ns: U[(o // 36 - b0) // 2].append(o - (b0 + 2 * ((o // 36 - b0) // 2)) * 36)
        if a >= 16: S_["units16"].append(len(set(tuple(U[u]) for u in sorted(U)[:8])))
    return dict(clips=n, clips_of_16_bars_or_more=len(S_["distinct16"]), a_clip=dict(sung_bars_p10_25_50_75_90=q(S_["bars"]), different_bar_rhythms=q(S_["distinct"]), bars_on_a_rhythm_already_sung=q(S_["again"]), in_the_first_16_bars_different_bar_rhythms=q(S_["distinct16"]), in_the_first_16_bars_again=q(S_["again16"]), different_two_bar_units_in_the_first_eight=q(S_["units16"])))
if __name__ == "__main__":
    out = {}
    for a in sys.argv[1:]:
        if a == "clips": out["pop 3/4 clips"] = clips()
        else: name, p = a.split("=", 1); lyr, rec = p.split(","); out[name] = engine(lyr, rec)
    print(json.dumps(out, indent=1))
