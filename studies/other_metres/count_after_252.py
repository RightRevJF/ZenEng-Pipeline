"""PREDICTION_counts_252.md: (2) the stress score's own best for each line among the rhythms the draw may offer; (1) the twelve draws of 749.252; (3) the same-count lines by the bars of their slot.  python3 studies/other_metres/count_after_252.py LYRIC.json RECORD_251.song.json RECORD_252.song.json -> prints JSON. Counts; no note is changed."""
import os, sys, json, random, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA
M = CA.M
def offered(E, sy, bars, hook):
    """-> [(onsets, kept count, the draw's log weight, stress score)] as rhythm() lists them, with no limit from the line before"""
    n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); out = []
    for p in sorted({0, min(1, lead), min(2, lead)}):
        for w, c in E.kept_windows(n - p, bars):
            if w[0] != 0 and p > 0: continue
            if bars == 2 and E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o in w if o < E.BAR) <= 2: continue
            ons = [-6 * (p - j) for j in range(p)] + list(w); st = [t for t, x in zip(ons, sy) if x[1]]
            if hook and E.S.get("title_840") and st and 2 * sum(1 for t in st if E.on_beat(t)) < len(st): continue
            sc = E.stress_score(ons, sy); e = E.ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]
            out.append((ons, c, math.log(c + 1) + ((E.S["title_pull"] if "title_pull" in E.S else 2.8) if hook else 1.4) * sc + math.log(e), sc))
    return out
def count_2(R):
    sp = R["spec"]; E = M.Engine(sp); hooks = set(sp.get("hooks", ())); G = collections.defaultdict(lambda: collections.defaultdict(float)); nowin = []
    for s_, i_ in E.KEYS:
        sy = E.LINES[s_][i_]; sb = E.SUNGB.get(id(sy)) or E.SLOTS[s_][i_]; hook = f"{s_}:{i_}" in hooks; how = E.HOW.get((s_, i_), ["fresh"])[0]
        if sb == 2 or len(sy) < 4: parts = [(sy, 2 if sb != 1 else 1)]
        else: n1 = (len(sy) + 1) // 2 if sb == 4 else int(round(2 * len(sy) / 3.0)); parts = [(sy[:n1], 2), (sy[n1:], 2 if sb == 4 else 1)]
        acc = collections.defaultdict(float); ok = True
        for syp, b in parts:
            ws = offered(E, syp, b, hook)
            if not ws: ok = False; break
            f = lambda o: (sum(1 for t, x in zip(o, syp) if x[1] and t % E.BAR == 0), sum(1 for t, x in zip(o, syp) if x[1] and not E.on_beat(t)))
            best = max(ws, key=lambda x: x[3]); b1, bo = f(best[0]); acc["score_best_first"] += b1; acc["score_best_off"] += bo; acc["ceiling_first"] += max(f(x[0])[0] for x in ws)
            top = max(x[2] for x in ws); pw = [math.exp(x[2] - top) for x in ws]; z = sum(pw); acc["draw_first"] += sum(p * f(x[0])[0] for p, x in zip(pw, ws)) / z; acc["draw_off"] += sum(p * f(x[0])[1] for p, x in zip(pw, ws)) / z
            tied = [x for x in ws if abs(x[3] - best[3]) < 1e-9]; acc["tied_at_best"] += len(tied); acc["tied_first_least"] += min(f(x[0])[0] for x in tied); acc["tied_first_most"] += max(f(x[0])[0] for x in tied)
        if not ok: nowin.append(f"{s_}:{i_}"); continue
        st = sum(1 for x in sy if x[1])
        for g in ("all lines", "lines sung again or copied (marked)" if how in ("again", "copy") else "lines not marked"):
            G[g]["stressed"] += st; G[g]["lines"] += 1
            for k, v in acc.items(): G[g][k] += v
    sp_ = sp.get("stress_place") or {}
    def row(v): t = v["stressed"]; return dict(lines=int(v["lines"]), stressed_syllables=int(t), the_scores_best_first_beat=round(v["score_best_first"] / t, 3), the_scores_best_off_the_beat=round(v["score_best_off"] / t, 3), where_rhythms_tie_at_the_best_first_beat_least_and_most=[round(v["tied_first_least"] / t, 3), round(v["tied_first_most"] / t, 3)], the_ceiling_first_beat=round(v["ceiling_first"] / t, 3), the_draws_expectation_first_beat=round(v["draw_first"] / t, 3), the_draws_expectation_off_the_beat=round(v["draw_off"] / t, 3))
    return dict(lines_with_no_kept_window_for_a_part=nowin, rows={k: row(v) for k, v in G.items()}, the_stress_file_as_the_score_reads_it=dict(weight=sp_.get("weight"), place=sp_.get("place")))
def count_1(L, R, builds=400, seed=1):
    E, sp = CA.engine(L, R); log = collections.defaultdict(list); inner = E.later_score
    def wrapped(ons, sec, i): v = inner(ons, sec, i); log[(sec, i)].append((tuple(ons), 1.4 * v)); return v
    E.later_score = wrapped; rng = random.Random(seed); D = collections.defaultdict(lambda: dict(distinct=[], spread=[], taken=collections.Counter(), best_taken=0, n=0)); n = 0
    for _ in range(builds):
        log.clear(); c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1
        for (sec, i), cs in log.items():
            U = E.line_start(sec, i); tk = tuple(x["on"] - U for x in c["notes"] if x["sec"] == sec and x["line"] == i); d = D[f"{sec}:{i}"]
            d["distinct"].append(len(set(o for o, _ in cs))); d["spread"].append(max(s for _, s in cs) - min(s for _, s in cs)); d["taken"][tk] += 1; d["n"] += 1; d["best_taken"] += any(o == tk and s >= max(s2 for _, s2 in cs) - 1e-9 for o, s in cs)
    rows = {k: dict(bars=E.slot_len(*[(k.rsplit(":", 1)[0]), int(k.rsplit(":", 1)[1])]) // E.BAR, later_sets=len(E.later_sets(k.rsplit(":", 1)[0], int(k.rsplit(":", 1)[1]))), builds=d["n"], distinct_rhythms_in_twelve_median=float(np.median(d["distinct"])), spread_of_the_later_score_median=round(float(np.median(d["spread"])), 2), the_commonest_rhythm_taken_share=round(d["taken"].most_common(1)[0][1] / d["n"], 3), distinct_rhythms_taken_across_builds=len(d["taken"]), the_best_of_the_twelve_taken_share=round(d["best_taken"] / d["n"], 3)) for k, d in D.items()}
    return dict(living_builds=n, lines_the_form_acts_on=len(rows), over_those_lines=dict(distinct_in_twelve_median=float(np.median([r["distinct_rhythms_in_twelve_median"] for r in rows.values()])), spread_median=float(np.median([r["spread_of_the_later_score_median"] for r in rows.values()])), commonest_taken_share_median=float(np.median([r["the_commonest_rhythm_taken_share"] for r in rows.values()])), best_of_twelve_taken_share_median=float(np.median([r["the_best_of_the_twelve_taken_share"] for r in rows.values()]))), by_line=rows)
def sources_same(L, R, builds=400, seed=1):
    """the watched figure, with and without 749.252: for each drawn line a later line sings again, the share of living builds in which it takes its commonest rhythm"""
    E, sp = CA.engine(L, R); rng = random.Random(seed); T = collections.defaultdict(collections.Counter); n = 0
    for _ in range(builds):
        c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1
        for (sec, i) in E.KEYS:
            if E._made.get((sec, i)) in ("fresh", "870 wait") and E.later_sets(sec, i): U = E.line_start(sec, i); T[(sec, i)][tuple(x["on"] - U for x in c["notes"] if x["sec"] == sec and x["line"] == i)] += 1
    sh = [v.most_common(1)[0][1] / sum(v.values()) for v in T.values()]
    return dict(living_builds=n, lines=len(sh), commonest_rhythm_share_median=round(float(np.median(sh)), 3), commonest_rhythm_share_least_and_most=[round(min(sh), 3), round(max(sh), 3)], distinct_rhythms_a_line_median=float(np.median([len(v) for v in T.values()])))
def count_3(L, R, builds=400, seed=1):
    E, sp = CA.engine(L, R); how = {}; inner = E.again
    def wrapped(rng, src, src_st0, sy, U, sec, i, tmin, slot):
        floor = max(tmin, 0) if (sy[0][1] and not src_st0 and src[0][0] < 0) else tmin; keep = [(t, p) for t, p in src if t >= floor] or src[-1:]
        if E.S.get("again_refit"): keep = [(t, p) for t, p in keep if t <= slot - (12 if E.LE else E.BREATH)] or keep[:1]
        how[(sec, i)] = len(sy) - len(keep); return inner(rng, src, src_st0, sy, U, sec, i, tmin, slot)
    E.again = wrapped; G = collections.defaultdict(lambda: [0, 0, 0]); rng = random.Random(seed); n = 0
    for _ in range(builds):
        how.clear(); c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1
        for x in c["notes"]:
            k = (x["sec"], x["line"])
            if not x["stress"] or E._made.get(k) not in ("again", "818 again") or how.get(k) != 0: continue
            sy = E.LINES[k[0]][k[1]]
            for key in ("all same-count lines", "%s: a slot of %d bars, %s sung" % (E._made[k], E.slot_len(*k) // E.BAR, E.SUNGB.get(id(sy)))): v = G[key]; v[0] += 1; v[1] += x["on"] % E.BAR == 0; v[2] += not E.on_beat(x["on"])
    tot = G["all same-count lines"][0]
    return dict(living_builds=n, rows={k: dict(share_of_same_count_stresses=round(v[0] / tot, 3), on_the_first_beat=round(v[1] / v[0], 3), off_the_beat=round(v[2] / v[0], 3)) for k, v in sorted(G.items())})
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); R1 = json.load(open(sys.argv[2])); R2 = json.load(open(sys.argv[3]))
    print(json.dumps(dict(count_2=count_2(R1), count_1=count_1(L, R2), sources_the_same_without_749_252=sources_same(L, R1), sources_the_same_with_749_252=sources_same(L, R2), count_3=count_3(L, R1), deaths_838=dict(with_749_251=R1["melody"]["deaths"], with_749_252=R2["melody"]["deaths"])), indent=1))
