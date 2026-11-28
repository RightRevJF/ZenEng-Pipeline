"""PREDICTION_counts_AB.md: (A) what the draw's limits remove from each drawn line; (B) the best one rhythm can do over every set of words it carries.  python3 studies/other_metres/count_AB.py LYRIC.json RECORD.song.json -> prints JSON. Counts; no note is changed."""
import os, sys, json, random, math, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA
M = CA.M; BIG = 10 ** 6
def listed(E, sy, bars, hook, tmin=-BIG, end=BIG):
    """the draw's list for one window, as rhythm() makes it: -> (out, early), each [(onsets, log weight)]"""
    n = len(sy); lead = next((k for k, x in enumerate(sy) if x[1]), n); out = []; early = []
    for p in sorted({0, min(1, lead), min(2, lead)}):
        for w, c in E.kept_windows(n - p, bars):
            if w[-1] > end or (w[0] != 0 and p > 0): continue
            if bars == 2 and E.S.get("no_pickup_windows") and w[0] >= E.BAR - 12 and sum(1 for o_ in w if o_ < E.BAR) <= 2: continue
            ons = [-6 * (p - j) for j in range(p)] + list(w)
            if ons[0] < tmin: continue
            e = E.ENTRY[sy[0][1]][0 if ons[0] < 0 else 1 if ons[0] == 0 else 2]
            out.append((ons, math.log(c + 1) + ((E.S["title_pull"] if "title_pull" in E.S else 2.8) if hook else 1.4) * E.stress_score(ons, sy) + math.log(e)))
            if p == 0 and sy[0][1] and w[0] == 0 and E.S.get("early_entries"):
                for sh in (6, 12):
                    o2 = [x - sh for x in w]
                    if o2[0] >= tmin: early.append((o2, math.log(c + 1) + 1.4 * E.stress_score([x for x in w], sy)))
    if hook and E.S.get("title_840") and (out or early):
        ok8 = lambda o_: (lambda v_: (not v_) or sum(1 for t_ in v_ if E.on_beat(t_)) * 2 >= len(v_))([t_ for t_, x_ in zip(o_, sy) if x_[1]])
        o8 = [x for x in out if ok8(x[0])]
        if o8: out = o8; early = [x for x in early if ok8(x[0])]
    return out, early
def first(E, o, sy): return sum(1 for t, x in zip(o, sy) if x[1] and t % E.BAR == 0)
def expect(E, sy, bars, hook, tmin, end, top12, early_on):
    out, early = listed(E, sy, bars, hook, tmin, end)
    if not out: return None
    def ex(lst):
        lst = sorted(lst, key=lambda x: -x[1]); lst = lst[:12] if top12 else lst; pw = [math.exp(s - lst[0][1]) for _, s in lst]; return sum(p * first(E, o, sy) for p, (o, _) in zip(pw, lst)) / sum(pw)
    if early and early_on: e0 = E.ENTRY[True][0]; return e0 * ex(early) + (1 - e0) * ex(out)
    return ex(out)
def line_expect(E, sy, hook, tmin, slot, cap, lim):
    """lim: the set of limits applied, of start, room, cap, twelve, early -> expected stresses on the first beat, or None where a window has no kept rhythm left"""
    if E.RESTB and id(sy) in E.RESTB and slot == E.RESTB[id(sy)][1] * E.BAR: slot = max(2, E.RESTB[id(sy)][0]) * E.BAR
    def one(syp, tm, sl, cp, room):
        room_ = (12 if E.LE else E.BREATH) if room is None else room; end = BIG
        if "room" in lim: end = min(end, sl - room_)
        if "cap" in lim and cp is not None: end = min(end, cp)
        return expect(E, syp, sl // E.BAR, hook, tm if "start" in lim else -BIG, end, "twelve" in lim, "early" in lim)
    if slot in (3 * E.BAR, 4 * E.BAR) and E.SUNGB.get(id(sy)) in (3, 4) and len(sy) >= 4:
        sb = E.SUNGB[id(sy)]; n1 = (len(sy) + 1) // 2 if sb == 4 else int(round(2 * len(sy) / 3.0))
        a = one(sy[:n1], tmin, 2 * E.BAR, None, 3); b = one(sy[n1:], 0, 2 * E.BAR if sb == 4 else E.BAR, None if cap is None else cap - 2 * E.BAR, None if (sb == 4 or slot == 3 * E.BAR) else 0)
        return None if a is None or b is None else a + b
    if slot // E.BAR not in (1, 2): return None
    return one(sy, tmin, slot, cap, None)
ROWS = [("no limit", ()), ("the earliest start alone", ("start",)), ("the room at the slot's end alone", ("room",)), ("the cap alone", ("cap",)), ("the cut to the twelve best alone", ("twelve",)), ("the early entries alone (834)", ("early",)), ("all together", ("start", "room", "cap", "twelve", "early"))]
def count_A(L, R, builds=400, seed=1):
    E, sp = CA.engine(L, R); calls = {}; inner = E.rhythm; depth = [0]; hooks = set(sp.get("hooks", ()))
    def wrapped(rng, sy, tmin, slot, cap=None, hook=False, room=None):
        if depth[0] == 0 and not E._part: calls[id(sy)] = (tmin, slot, cap)
        depth[0] += 1
        try: return inner(rng, sy, tmin, slot, cap=cap, hook=hook, room=room)
        finally: depth[0] -= 1
    E.rhythm = wrapped; rng = random.Random(seed); n = 0; G = collections.defaultdict(lambda: collections.defaultdict(float)); cache = {}
    for _ in range(builds):
        calls.clear(); c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; by = collections.defaultdict(list)
        for x in c["notes"]: by[(x["sec"], x["line"])].append(x)
        for (sec, i) in E.KEYS:
            made = E._made.get((sec, i)); sy = E.LINES[sec][i]
            if made not in ("fresh", "870 wait") or id(sy) not in calls: continue
            tmin, slot, cap = calls[id(sy)]; hook = f"{sec}:{i}" in hooks; key = (sec, i, tmin, slot, cap)
            if key not in cache: cache[key] = {name: line_expect(E, sy, hook, tmin, slot, cap, set(lim)) for name, lim in ROWS}
            ex = cache[key]; st = sum(1 for x in sy if x[1]); built = sum(1 for x in by[(sec, i)] if x["stress"] and x["on"] % E.BAR == 0)
            grp = ["every drawn line", "title lines" if hook else "after 870's wait (749.245's rests)" if made == "870 wait" else "other fresh lines", "a slot of %d bars" % (slot // E.BAR)]
            if cap is not None: grp.append("lines drawn under a cap")
            for g in grp:
                v = G[g]; v["lines"] += 1
                if ex["all together"] is None: v["lines_falling_to_760"] += 1; v["760_stressed"] += st; v["760_built_first"] += built; continue
                v["stressed"] += st; v["built"] += built
                for name, _ in ROWS: v[name] += ex[name] if ex[name] is not None else 0.0
    def row(v):
        t = v["stressed"]; o = dict(lines=int(v["lines"]), stressed_syllables=int(t), lines_falling_to_the_weighted_rule_760=int(v["lines_falling_to_760"]), those_lines_built_first_beat=round(v["760_built_first"] / v["760_stressed"], 3) if v["760_stressed"] else None)
        if t: o.update({name: round(v[name] / t, 3) for name, _ in ROWS}); o["what was built"] = round(v["built"] / t, 3)
        return o
    return dict(living_builds=n, settings=dict(one_bar_share_876_not_replicated=sp.get("one_bar_share"), early_entries=sp.get("early_entries"), the_chance_of_an_early_entry=E.ENTRY[True][0], title_entry_pickup=sp.get("title_entry_pickup"), kept_rests_rate=sp.get("kept_rests_rate")), rows={k: row(v) for k, v in sorted(G.items(), key=lambda x: -x[1]["lines"])})
def refit(E, ons, sy2, slot2):
    n = len(sy2); d = n - len(ons)
    if d == 0: return list(ons)
    if abs(d) > 3: return None
    lim = slot2 - (12 if E.LE else E.BREATH) if E.S.get("again_refit") == 2 else slot2 - 6; st = {tuple(ons): list(ons)}
    for _ in range(abs(d)):
        nx = {}
        for o in st.values():
            if d > 0:
                for j in range(len(o)):
                    g = (o[j + 1] if j + 1 < len(o) else lim) - o[j]; hh = o[j] + (g // 2 // 3) * 3
                    if g >= 6 and hh > o[j]: nx.setdefault(tuple(o[:j + 1] + [hh] + o[j + 1:]), o[:j + 1] + [hh] + o[j + 1:])
            else:
                for j in range(1, len(o) - 1): nx.setdefault(tuple(o[:j] + o[j + 1:]), o[:j] + o[j + 1:])
        st = nx
    c = [o for o in st.values() if len(o) == n and all(y - x >= 3 for x, y in zip(o, o[1:]))]
    return max(c, key=lambda o: E.stress_score(o, sy2)) if c else None
def count_B(L, R):
    E, sp = CA.engine(L, R); hooks = set(sp.get("hooks", ())); rows = {}; pool = collections.defaultdict(lambda: collections.defaultdict(float))
    for (sec, i) in E.KEYS:
        ls = E.later_sets(sec, i)
        if not ls or E.HOW.get((sec, i), ["fresh"])[0] != "fresh": continue
        sy = E.LINES[sec][i]; hook = f"{sec}:{i}" in hooks; slot = E.slot_len(sec, i); sb = E.SUNGB.get(id(sy))
        if slot in (3 * E.BAR, 4 * E.BAR) and sb in (3, 4) and len(sy) >= 4:
            n1 = (len(sy) + 1) // 2 if sb == 4 else int(round(2 * len(sy) / 3.0)); a = sorted(listed(E, sy[:n1], 2, hook)[0], key=lambda x: -x[1])[:40]; b = sorted(listed(E, sy[n1:], 2 if sb == 4 else 1, hook)[0], key=lambda x: -x[1])[:40]
            cands = [oa + [t + 2 * E.BAR for t in ob] for oa, _ in a for ob, _ in b if ob[0] >= 0]
        else: cands = [o for o, _ in listed(E, sy, slot // E.BAR, hook)[0]]
        sets = [(1.0, sy, slot)] + [(w, E.LINES[s2][i2], E.slot_len(s2, i2)) for w, (s2, i2) in ls]; res = []
        for o in cands:
            f = nn = sc = 0.0; own = first(E, o, sy)
            for w, sy2, sl2 in sets:
                o2 = refit(E, o, sy2, sl2)
                if o2 is None: continue
                f += w * first(E, o2, sy2); nn += w * sum(1 for x in sy2 if x[1]); sc += w * E.stress_score(o2, sy2)
            res.append((f, nn, sc, own, E.stress_score(o, sy)))
        if not res: rows[f"{sec}:{i}"] = dict(rhythms=0); continue
        best = max(res, key=lambda x: x[0] / x[1]); bysc = max(res, key=lambda x: x[2]); byown = max(res, key=lambda x: x[4]); st = sum(1 for x in sy if x[1])
        rows[f"{sec}:{i}"] = dict(rhythms=len(res), sets_carried=len(sets), the_best_any_rhythm_reaches=round(best[0] / best[1], 3), its_own_words_then=round(best[3] / st, 3), the_rhythm_of_the_best_summed_score=round(bysc[0] / bysc[1], 3), the_best_rhythm_for_its_own_words_alone=round(byown[0] / byown[1], 3))
        for g in ["all source lines (they overlap)"] + (["the two lines drawn in every build"] if i == 0 else []):
            p = pool[g]; p["best_f"] += best[0]; p["best_n"] += best[1]; p["sc_f"] += bysc[0]; p["sc_n"] += bysc[1]; p["own_f"] += byown[0]; p["own_n"] += byown[1]
    return dict(by_line=rows, pooled={g: dict(the_best_any_rhythm_reaches=round(p["best_f"] / p["best_n"], 3), the_rhythm_of_the_best_summed_score=round(p["sc_f"] / p["sc_n"], 3), the_best_rhythm_for_its_own_words_alone=round(p["own_f"] / p["own_n"], 3)) for g, p in pool.items()})
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); print(json.dumps(dict(A=count_A(L, R), B=count_B(L, R)), indent=1))
