"""PREDICTION_260_and_counts.md, count (a): how many of a section's lines 749.259 can reach. On living builds of a record that carries bar_memory: each line sorted by how it was made; for each line drawn from the kept windows, whether the section had sung a bar yet, how many windows were weighed with the memory on, how many held a bar already sung, and whether the rhythm taken holds one. python3 studies/other_metres/count_memory_reach.py LYRIC.json RECORD.song.json [BUILDS] -> prints JSON. The counter listens to the draw; no note is changed."""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import numpy as np, count_after_251 as CA
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); E, sp = CA.engine(L, R); assert sp.get("bar_memory"), "the record carries no bar_memory"
    cur = {"n": 0, "hit": 0}; inner = E._bar_mem
    def bm(ons): v = inner(ons); cur["n"] += 1; cur["hit"] += v > 0; return v
    E._bar_mem = bm; rng = random.Random(L.get("seed", 1)); n = 0; made = collections.Counter(); per_sec = collections.defaultdict(list); D = collections.defaultdict(list); BL = E.BAR
    for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 300):
        # one build, line by line is not exposed; so the draw's tallies are taken per build by wrapping rhythm at its outer call
        calls = []; depth = [0]; r_in = E.__class__.rhythm
        def rh(rng_, sy, tmin, slot, cap=None, hook=False, room=None):
            top = depth[0] == 0
            if top: cur["n"] = cur["hit"] = 0
            depth[0] += 1
            try: o = r_in(E, rng_, sy, tmin, slot, cap=cap, hook=hook, room=room)
            finally: depth[0] -= 1
            if top: calls.append((id(sy), cur["n"], cur["hit"], bool(E._secbars), tuple(o) if o else None, E._lineU, set(E._secbars or ())))
            return o
        E.rhythm = rh; c, err = E.build(rng)
        if err or E.gates(c): continue
        n += 1; last = {}
        for x in calls: last[x[0]] = x
        for sec in E.SUNG:
            cnt = collections.Counter()
            for i, sy in enumerate(E.LINES[sec]):
                m = E._made.get((sec, i), "?"); hook = f"{sec}:{i}" in set(sp.get("hooks", ())); kind = ("title line" if hook else "fresh") if m in ("fresh", "870 wait") else m
                made[kind] += 1; cnt["drawn" if m in ("fresh", "870 wait") else "not drawn"] += 1
                if m in ("fresh", "870 wait") and id(sy) in last:
                    _, nw, hit, mem, o, U, sb = last[id(sy)]
                    D["the section had sung a bar"].append(mem); 
                    if mem:
                        D["windows weighed"].append(nw); D["of them holding a bar already sung"].append(hit / nw if nw else 0.0); D["no window weighed (the weighted rule, or none offered)"].append(nw == 0)
                        if o:
                            bars = collections.defaultdict(list)
                            for t in o:
                                if t >= 0: bars[(U + t) // BL].append((U + t) % BL)
                            D["the rhythm taken holds a bar already sung"].append(any(tuple(v) in sb for v in bars.values()))
            per_sec["lines"].append(sum(cnt.values())); per_sec["drawn from the windows"].append(cnt["drawn"])
    tot = sum(made.values()); f = lambda v: round(float(np.mean(v)), 3) if v else None
    print(json.dumps(dict(living_builds=n, bar_memory=sp.get("bar_memory"), lines_by_how_made={k: round(v / tot, 3) for k, v in made.most_common()}, a_section=dict(lines_median=float(np.median(per_sec["lines"])), drawn_from_the_windows_mean=f(per_sec["drawn from the windows"]), share_of_lines_drawn=round(sum(per_sec["drawn from the windows"]) / sum(per_sec["lines"]), 3)),
                          lines_drawn=dict(count=len(D["the section had sung a bar"]), the_section_had_sung_a_bar=f(D["the section had sung a bar"]), then_windows_weighed_median=float(np.median(D["windows weighed"])) if D["windows weighed"] else None, then_no_window_weighed=f(D["no window weighed (the weighted rule, or none offered)"]), then_share_of_windows_holding_a_bar_already_sung=f(D["of them holding a bar already sung"]), then_the_rhythm_taken_holds_a_bar_already_sung=f(D["the rhythm taken holds a bar already sung"]))), indent=1))
