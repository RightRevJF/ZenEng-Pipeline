"""The v109 port (fixes 298-309) tested on song 40's default path: the tests of 298-309 on the main run and the control, beside the
v108 runs. Writes readings_v109_p40.json/.pkl."""
import sys, pickle, collections, json
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p41")
import melody_v109_p40 as P, judges as J
H = "/home/claude/p41"; M = P.M; BAR, BEAT = P.BAR, P.BEAT
RUN = {v: pickle.load(open(f"{H}/melody_v109_p40_{v}.pkl", "rb")) for v in ("main", "ctl")}
RR = {v: pickle.load(open(f"{H}/melody_v109_p40_{v}_r.pkl", "rb")) for v in ("main", "ctl")}
OLD = {v: pickle.load(open(f"/home/claude/p40/melody_{v}.pkl", "rb")) for v in ("main", "ctl")}
L109 = json.load(open(f"{H}/limits_v109.json"))
def pct(v, q=(5, 50, 95)):
    v = [float(x) for x in v if x is not None and np.isfinite(x)]
    return [round(float(np.percentile(v, k)), 3) for k in q] if v else None
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
R = {}
for v in ("main", "ctl"):
    D = RUN[v]; O = OLD[v]; Al = D["all"]; r = {}
    r["runs"] = dict(survivors=D["survivors"], order=D["order_fp"], rerun_order=RR[v]["order_fp"], reproduced=D["order_fp"] == RR[v]["order_fp"] and D["survivors"] == RR[v]["survivors"],
                     v108_survivors=O["survivors"], deaths=dict(D["deaths"].most_common()), code=D["rerun"]["code_sha"], line_knobs=D["line_knobs"], calib=D["calibration"][-1].get("lines"))
    jc = [b["judge"]["combined"] for b in Al]; jo = [b["judge"]["combined"] for b in O["all"]]
    ga = collections.defaultdict(list)
    for b in Al[:400]:
        for w in ("v", "c"):
            if b["read"][w]:
                for m, x in J.give_away(b["read"][w], k=46): ga[m].append(x)
    r["299"] = dict(under_floor=round(float(np.mean(np.array(jc) < J.FLOOR)), 3), v108=round(float(np.mean(np.array(jo) < J.FLOOR)), 3),
                    deaths=D["deaths"].get("the judge's floor (254; 279)", 0), v108_deaths=O["deaths"].get("the judge's floor (254; 279)", 0),
                    content=pct([b["judge"]["content"] for b in Al]), order=pct([b["judge"]["order"] for b in Al]),
                    v108_content=pct([b["judge"]["content"] for b in O["all"]]), v108_order=pct([b["judge"]["order"] for b in O["all"]]),
                    give_aways=sorted(((m, round(float(np.mean(x)), 3)) for m, x in ga.items()), key=lambda z: z[1])[:5])
    om = {k: {"new": [], "old": []} for k in J.OJ["measures"]}
    for lab, src in (("new", Al[:300]), ("old", O["all"][:300])):
        for b in src:
            ns = nts(b)
            for s in ("Verse 1", "Chorus 1"):
                of = J.order_feats(P.win_N(ns, P.BAR0[s]))
                if of:
                    for k in om: om[k][lab].append(of[k])
    r["order_measures"] = {k: dict(new=round(float(np.nanmedian(x["new"])), 3), v108=round(float(np.nanmedian(x["old"])), 3), kept_mean=round(J.OJ["mean"][J.OJ["measures"].index(k)], 3),
                                   weight=round(J.OJ["weight"][J.OJ["measures"].index(k)], 3)) for k, x in om.items()}
    E = [e for e in D["every"] if e["soft"] is not None]
    r["300"] = dict(realness=pct([e["limits7"].get("realness") for e in E], (5, 25, 50, 75, 95)), in_count=any("realness" in e["soft"] + e["hard"] for e in E),
                    pick=round(float(D["pick"]["info"]["limits7"]["realness"]), 3), kept_chart=[0.004, 0.029, 0.088, 0.303, 0.636])
    r["301"] = dict(eight_kept=0.92, six_pairs=L109["chosen"]["joint"], refit=L109["chosen"]["hard_percentile"] != 1)
    EN = [([n for n in nts(b) if n["sec"] == "Last Chorus"][-1]["p"] - M.TONIC) % 12 == 0 for b in Al]
    r["302"] = dict(moved=D["stats"].get("262: last note moved", 0), made=D["made"], share=round(D["stats"].get("262: last note moved", 0) / D["made"], 3),
                    last_chorus_tonic=round(float(np.mean(EN)), 3), v108_moved=O["stats"].get("262: last note moved", 0))
    def share(b):
        def bars(s):
            out = collections.defaultdict(set)
            for n in nts(b):
                if n["sec"] == s: out[n["on"] // BAR - P.BAR0[s]].add(n["on"] % BAR)
            return out
        a, c = bars("Verse 2"), bars("Verse 1"); return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))
    sh = [share(b) for b in Al]
    r["303"] = dict(share=pct(sh), in_range=round(float(np.mean([0.25 <= x <= 0.75 for x in sh])), 3), copied=D["stats"].get("293: bars copied", 0), given_up=D["stats"].get("293: copy given up for a line", 0))
    cv = []
    for b in Al:
        t = b["meta"]["targets"]["C"]["turns_per_move"]; rd = b["read"]["c"]["turns_per_move"] if b["read"]["c"] else np.nan
        if np.isfinite(rd): cv.append((t, rd))
    r["304"] = dict(dropped_in_chorus=True, chorus_corr=round(float(np.corrcoef(*zip(*cv))[0, 1]), 3) if len(cv) > 5 and np.std([a for a, _ in cv]) > 0 else None,
                    chorus_reading=pct([x for _, x in cv]))
    r["305"] = dict(arch_span=pct([b["lines"]["arch_span"] for b in Al], (5, 25, 50, 75, 95)), kept=[0.0, 0.23, 0.55], amp=D["line_knobs"]["amp"],
                    past_fifth=dict(new=pct([b["read"]["v"]["past_fifth"] for b in Al if b["read"]["v"]]), v108=pct([b["read"]["v"]["past_fifth"] for b in O["all"] if b["read"]["v"]])))
    r["306"] = dict(last_over_mean=pct([b["lines"]["last_over_mean"] for b in Al]), kept=[1.182, 1.478, 1.714], v108=pct([b["lines"]["last_over_mean"] for b in O["all"]]))
    def top(b):
        ns = nts(b); mx = max(n["p"] for n in ns); tops = [n for n in ns if n["p"] == mx]; med = float(np.median([n["dur"] for n in ns]))
        return len(tops), max(n["dur"] for n in tops) / med, any(n["on"] % BEAT == 0 for n in tops)
    T = [top(b) for b in Al]; pk = top(dict(notes=[(n["on"], n["dur"], n["p"], n["sec"], n["line"], n.get("stress"), n.get("syl")) for n in D["pick"]["notes"]]))
    r["307"] = dict(soundings=pct([x[0] for x in T]), once=round(float(np.mean([x[0] == 1 for x in T])), 3), longest_over_median=pct([x[1] for x in T]),
                    never_on_beat=round(float(np.mean([not x[2] for x in T])), 3), pick=dict(soundings=pk[0], longest_over_median=round(pk[1], 2), on_beat=pk[2]),
                    kept=dict(soundings_median=4, once=0.22, longest_over_median=2, never_on_beat=0.21))
    sh8, f45, sdc = [], [], []
    for b in Al:
        lines = collections.defaultdict(list)
        for n in b["notes"]: lines[n[4]].append(n)
        for ns in lines.values():
            if len(ns) >= 9:
                c = collections.Counter(x[0] // BAR for x in ns); m = max(c.values()) / len(ns); sh8.append(m); f45.append(m >= 0.8)
        if b["read"]["c"]: sdc.append(b["read"]["c"]["notes_per_bar_sd"])
    r["308"] = dict(fullest_share=pct(sh8), four_fifths=round(float(np.mean(f45)), 3), chorus_spread=pct(sdc), spread_under_291=round(float(np.mean(np.array(sdc) < 2.91)), 3),
                    redrawn=D["stats"].get("308: long line redrawn", 0), kept=dict(fullest_share=0.46, middle=[0.35, 0.57], four_fifths=0.04, spread=1.60))
    pkn = D["pick"]["notes"]
    def lmed(sec, i): return float(np.median([n["p"] for n in pkn if n["line"] == f"{sec}:{i}"]))
    vm = float(np.median([n["p"] for n in pkn if n["sec"] == "Verse 1"]))
    tl = []
    for b in Al:
        ns = nts(b); h = [n["p"] for n in ns if n["line"] == "Chorus 1:0"]; vv = [n["p"] for n in ns if n["sec"] == "Verse 1"]
        d = float(np.median(h)) - float(np.median(vv)); tl.append("above" if d > 0 else "level" if d == 0 else "below")
    c_ = collections.Counter(tl)
    r["298"] = dict(pick_title_minus_verse=lmed("Chorus 1", 0) - vm, builds={k: round(c_[k] / len(tl), 3) for k in ("above", "level", "below")}, kept=dict(above=0.56, level=0.18, below=0.26),
                    lift=pct([b["info"]["lift"]["median"] for b in Al], (25, 50, 75)))
    R[v] = r
pickle.dump(R, open(f"{H}/readings_v109_p40.pkl", "wb")); json.dump(R, open(f"{H}/readings_v109_p40.json", "w"), indent=1, default=str)
print(json.dumps(R["main"], indent=1, default=str)[:6000])
