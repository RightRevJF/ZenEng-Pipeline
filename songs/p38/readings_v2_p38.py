"""Song 38 rerun under v107 (v2): the report's readings, items 1-9 of the brief, from the three runs (A gates only, B full v107,
C control) and their reruns, beside the first run (v1, v103). Writes readings_v2.json and readings_v2.pkl."""
import sys, pickle, collections, json, math
import numpy as np
sys.argv = ["x", "1", "B"]; sys.path.insert(0, "/home/claude/p38")
import melody_v2_p38 as P, judges as J
H = "/home/claude/p38"; M = P.M; BAR, BEAT = P.BAR, P.BEAT
RUN = {v: pickle.load(open(f"{H}/melody_v2_{v}.pkl", "rb")) for v in "ABC"}
RR = {v: pickle.load(open(f"{H}/melody_v2_{v}_r.pkl", "rb")) for v in "ABC"}
V1 = pickle.load(open(f"{H}/melody_main.pkl", "rb")); V1C = pickle.load(open(f"{H}/melody_ctl.pkl", "rb"))
TB = json.load(open(f"{H}/tableb_v2.json")); DJ = P.LIT["bands"]["bands (5, 25, 50, 75, 95)"]
def pct(v, q=(5, 50, 95)):
    v = [x for x in v if x is not None and np.isfinite(x)]
    return [round(float(np.percentile(v, k)), 3) for k in q] if v else None
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
R = {}

# 1 survivors and frozen orders
R["1"] = {v: dict(made=RUN[v]["made"], survivors=RUN[v]["survivors"], share=round(RUN[v]["survivors"] / RUN[v]["made"], 4), order=RUN[v]["order_fp"],
                  rerun_order=RR[v]["order_fp"], reproduced=RUN[v]["order_fp"] == RR[v]["order_fp"] and RUN[v]["survivors"] == RR[v]["survivors"],
                  code=RUN[v]["rerun"]["code_sha"], line_knobs=RUN[v]["line_knobs"]) for v in "ABC"}
R["1"]["v1"] = dict(made=V1["made"], survivors=V1["survivors"], order=V1["order_fp"], ctl_survivors=V1C["survivors"])

# 2 deaths per gate beside the first run
MAP = [("limits: a hard limit or three soft breaks (276/277)", ["leaps: tritone or past an octave", "monotony run (166/196)", "register (133)", "chorus at or above the verse, floor lifted (227)",
        "no tone a tritone from the root (215)", "note lengths <= 5 per 8 bars (206)"]),
       ("era: fewer than four of five bands inside CLASSIC's 5th-95th (264)", ["era CLASSIC bands (242)"]),
       ("returns related (267)", ["returns related, on shared events (181/219/248)"]),
       ("return: first or top note not kept (239)", ["return: first or top note not kept (239)"]),
       ("summit placed (design gate; 216, 244)", ["summit placed (the writer's A; 216, 244)"]),
       ("bridge above the verse, under the summit (design gate; 208)", ["bridge above the verse, under the summit (208)"]),
       ("chorus opening another tune (227; 279)", ["chorus opening another tune (227)"]), ("bridge opening unrelated (208; 279)", ["bridge opening unrelated (208)"]),
       ("rhythm band (163; unaudited)", ["rhythm band (163)"]), ("pushed notes (159; 279)", ["pushed notes (159)"]), ("density (159; 279)", ["density (159)"]),
       ("sequence legs (148; unaudited)", ["sequence legs (148)"]), ("key word on a chord tone (134; 279)", ["key word on a chord tone (134)"]),
       ("the judge's floor (254; 279)", ["the judge's floor (254)"])]
for k in ("spectral", "cmp", "memory", "surprisal", "realness"): MAP.append((f"{k} (Table B; unaudited)", [f"{k} (Table B)"]))
for k in ("join: no held end and breath before the line (212)", "join: no held end and breath before the copy (212)", "align: the words do not fit the returning tune",
          "rhythm: no placement", "walk: no note", "range (the voice row)"): MAP.append((k, [k, "range"] if k.startswith("range") else [k]))
rows2 = []
for new, old in MAP:
    rows2.append(dict(gate=new, v1=sum(V1["deaths"].get(o, 0) for o in old), v1_parts={o: V1["deaths"].get(o, 0) for o in old if len(old) > 1},
                      **{v: RUN[v]["deaths"].get(new, 0) for v in "ABC"}))
known = {r["gate"] for r in rows2}
for v in "ABC":
    for k in RUN[v]["deaths"]:
        assert k in known, k
R["2"] = dict(rows=rows2, survivors={v: RUN[v]["survivors"] for v in "ABC"}, v1_survivors=V1["survivors"], made=3000,
              would={v: {k: RUN[v]["would"].get(k, 0) for k in list(P.GATES) + [f"{k} (Table B; unaudited)" for k in ("spectral", "cmp", "memory", "surprisal", "realness")]} for v in "ABC"})

# 3 fix 277: soft breaks, hard limits, each limit for the pick and the builds' median beside Table DL
R["3"] = {}
for v in "ABC":
    E = RUN[v]["every"]; done = [e for e in E if e["soft"] is not None]; n_ = len(done)
    sb = collections.Counter(min(3, len(e["soft"])) for e in done)
    pk = RUN[v]["pick"]; lim = {k: [round(float(np.median([e["limits"][k] for e in done])), 4), round(float(pk["info"]["limits"][k]), 4), P.SOFT[k], P.HARD[k]] for k in P.LIMITS}
    R["3"][v] = dict(complete=n_, soft_share={str(k): round(sb[k] / n_, 3) for k in range(4)}, hard_any=sum(bool(e["hard"]) for e in done),
                     deaths_on_hard=sum(bool(e["hard"]) for e in done), deaths_on_three_soft=sum((not e["hard"]) and len(e["soft"]) >= 3 for e in done),
                     soft_by_limit=dict(collections.Counter(k for e in done for k in e["soft"])), hard_by_limit=dict(collections.Counter(k for e in done for k in e["hard"])),
                     pick_soft=pk["info"]["soft"], pick_hard=pk["info"]["hard"], limits=lim,
                     survivors_soft=dict(collections.Counter(len(c["info"]["soft"]) for c in RUN[v]["alive"])),
                     run_max_builds=pct([e["limits"]["run_max"] for e in done], (5, 25, 50, 75, 95)),
                     lengths_builds=pct([e["limits"]["max_lengths_8_bars"] for e in done], (5, 25, 50, 75, 95)),
                     tritone_leap_any=round(float(np.mean([e["limits"]["tritone_leap_share"] > 0 for e in done])), 3),
                     octave_any=round(float(np.mean([e["limits"]["past_octave_share"] > 0 for e in done])), 3))
R["3"]["kept_soft_share"] = GLK = P.GL["kept songs: soft breaks 0, 1, 2, 3 or more"]

# 4 fixes 275 and 280: kept pass rates of every gate in the search
A_ = P.GL["audit, as coded"]["gates (share of kept songs that pass; songs it could be read on)"]
R["4"] = dict(gates=[
    ("limits: three soft breaks or one hard (276/277)", 0.92, "Table DL", None),
    ("summit placed (216, 244)", None, "design gate (exempt from 275)", None),
    ("bridge median above the verse's, top under the summit (208)", A_["208 register as coded (both)"][0], "design gate (exempt); kept as coded", None),
    ("era: four of five bands inside CLASSIC's 5th-95th (264)", P.CHK["era bands and joint pass rates"]["CLASSIC (to 1979)"]["5th-95th"]["inside four or more"], "Table DK", None),
    ("returns related (267)", None, "not printed by the paper; 239 as a gate: first note 80%, top 92% of kept returns", None),
    ("chorus opening unrelated (227)", A_["227: chorus opening unrelated to the verse's"][0], "Table DL", None),
    ("bridge opening unrelated (208)", A_["208: bridge opening unrelated to verse and chorus"][0], "Table DL", None),
    ("pushed notes at most 42% (159)", A_["159: pushed notes at most 42%"][0], "Table DL", None),
    ("density 1.1 to 4.9 notes a second (159)", P.GL["audit, as coded"]["159 density, 1.1 to 4.9 notes a second (top-five singles 1950-2024)"][0], "Table DL", None),
    ("key word on a chord tone (134)", 0.9, "Window 94 ('about nine in ten')", None),
    ("the judge's floor (254)", 0.95, "kept 5th percentile by its making", None),
    ("joins: a held end and a breath before the line or copy (212)", None, "unread by the paper and here (a lyric-placement rule)", None),
    ("the voice's range (intake)", None, "the writer's voice row, not a kept-song gate", None)]
    + [(f"{k} (session, 280)", TB["alone"][k], TB["corpus"], None) for k in TB["alone"]],
    table_b_together=TB["table_b_together"], all_seven=TB["all_seven"], breaks=TB["breaks"], corpus=TB["corpus"], pairs=TB["pairs"])

# 5 line readings of Table DJ, and line entry by 231's and by 260's reading
KEYS = ["arch_or_falling", "valley", "arch_positive", "arch_term", "falling_term", "peak_first_third", "end_minus_mean", "last_over_mean", "widening",
        "first_note_extra_bits", "starts_on_downbeat", "starts_after_downbeat", "starts_as_pickup", "ends_on_downbeat"]
def land(ns):
    off = b13 = pk = n_ = 0
    for ln in dict.fromkeys(n["line"] for n in ns):
        x = [n for n in ns if n["line"] == ln]; s, i = ln.split(":"); U = P.line_start(s, int(i)); st = [n for n in x if n["stress"]]
        if not st: continue
        t = st[-1]["on"] % BAR; n_ += 1; off += t % BEAT != 0; b13 += t in (0, 24); pk += x[0]["on"] < U
    return off / n_, b13 / n_, pk / n_
def section_ends(ns):
    out = {}
    for s in P.SUNG:
        x = [n for n in ns if n["sec"] == s]; out[s] = (x[-1]["p"] - M.TONIC) % 12
    return out
DEG = {0: "1", 2: "2", 4: "3", 5: "4", 7: "5", 9: "6", 11: "7", 3: "b3", 10: "b7", 1: "b2", 6: "#4", 8: "b6"}
R["5"] = {"kept": {k: DJ[k]["kept songs"] for k in KEYS}, "kept_kinds": P.KEPT_KINDS, "song37": {k: DJ[k]["song 37 builds"] for k in KEYS},
          "v1": {}}
for v in "ABC":
    Al = RUN[v]["all"]; pk = RUN[v]["pick"]; pl = P.line_readings(pk["notes"])
    L3 = [land(nts(b)) for b in Al]; kinds = collections.Counter()
    for b in Al:
        for k, x in b["lines"]["kinds"].items(): kinds[k] += x
    ends = [section_ends(nts(b)) for b in Al]
    R["5"][v] = dict(builds={k: pct([b["lines"][k] for b in Al]) for k in KEYS}, pick={k: round(float(pl[k]), 3) for k in KEYS},
                     outside_mid={k: round(float(np.mean([not (DJ[k]["kept songs"][1] <= b["lines"][k] <= DJ[k]["kept songs"][3]) for b in Al if np.isfinite(b["lines"][k])])), 3) for k in KEYS},
                     kinds={k: round(x / len(Al), 3) for k, x in kinds.most_common()}, pick_kinds=pl["kinds"],
                     join_fourth=pct([b["lines"]["join_fourth"] for b in Al]), pick_join_fourth=round(pl["join_fourth"], 3),
                     entry_231=dict(builds_pickup=pct([x[2] for x in L3]), builds_off=pct([x[0] for x in L3]), builds_b13=pct([x[1] for x in L3]), pick=[round(x, 3) for x in land(pk["notes"])]),
                     entry_260=dict(builds_after=pct([b["lines"]["starts_after_downbeat"] for b in Al]), builds_on=pct([b["lines"]["starts_on_downbeat"] for b in Al]),
                                    builds_pickup=pct([b["lines"]["starts_as_pickup"] for b in Al]),
                                    pick=[round(pl[k], 3) for k in ("starts_after_downbeat", "starts_on_downbeat", "starts_as_pickup")]),
                     last_longest=pct([b["lines"]["last_longest"] for b in Al]),
                     ends_pick={s: DEG[d] for s, d in section_ends(pk["notes"]).items()},
                     ends_builds={s: dict(collections.Counter(DEG[e[s]] for e in ends).most_common(4)) for s in ("Verse 1", "Verse 2", "Chorus 1", "Chorus 2", "Last Chorus")},
                     contour_drawn=dict(collections.Counter(k for b in Al for k in b["meta"].get("contour", {}).values()).most_common()) if v != "A" else None)
# v1 on the same readings (its survivors' notes were the only ones kept; its 'all' has every complete build)
v1l = [P.line_readings(nts(b)) for b in V1["all"]]
R["5"]["v1"] = {k: pct([x[k] for x in v1l]) for k in KEYS}; R["5"]["v1_builds_read"] = len(v1l)

# 6 fix 255
R["6"] = {}
for v in "ABC":
    D = RUN[v]; out = {}
    for lab, c in (("composite first", D["comp_first"]), ("shortlist pick", D["pick"]), ("judge first", D["judge_first"])):
        out[lab] = dict(fp=c["fp"], composite=round(c["meas"]["composite"], 3), content=round(c["judge"]["content"], 3), order=round(c["judge"]["order"], 3), combined=round(c["judge"]["combined"], 3))
    byj = sorted(D["all_alive"], key=lambda x: (-x[1], x[0])); rank = [x[0] for x in byj].index(D["comp_first"]["fp"]) + 1
    out["shortlist_size"] = len(D["short"]); out["survivors"] = D["survivors"]; out["comp_first_rank_by_judge"] = rank; out["pick_changed"] = D["comp_first"]["fp"] != D["pick"]["fp"]
    jall = [b["judge"] for b in D["all"]]
    out["builds"] = dict(content=pct([j["content"] for j in jall]), order=pct([j["order"] for j in jall]), combined=pct([j["combined"] for j in jall]))
    out["survivors_judge"] = dict(combined=pct([x[1] for x in D["all_alive"]]))
    R["6"][v] = out

# 7 distance, outside count, reciting, era
R["7"] = {}
for v in "ABC":
    Al = RUN[v]["all"]; pk = RUN[v]["pick"]
    er = pk["read"]["era"]
    R["7"][v] = dict(distance=pct([b["read"]["dist"] for b in Al]), pick_distance=round(pk["read"]["dist"], 3),
                     outside=pct([b["read"]["outside"] for b in Al]), pick_outside=pk["read"]["outside"],
                     reciting_verse=pct([b["read"]["ax_v"][4] for b in Al]), pick_reciting=pk["read"]["ax_v"][4],
                     era_pick={k: round(er[k], 3) for k in P.ERA_K}, era_mid={k: [P.ERA[k][0], P.ERA[k][2]] for k in P.ERA_K}, era_95={k: P.ERA95[k] for k in P.ERA_K},
                     pick_inside_mid=[k for k in P.ERA_K if P.ERA[k][0] <= er[k] <= P.ERA[k][2]], pick_inside_95=P.era_inside(er),
                     era_inside_four_builds=round(float(np.mean([len(b["info"]["era_inside_95"]) >= 4 for b in Al])), 3))
R["7"]["v1"] = dict(distance=[0.11, 0.168, 0.245], outside=[11.5, 15.5, 19], reciting=[0.27, 1.153, 2.072], pick_outside=10.5, pick_distance=0.086, pick_reciting=1.48)

# 8 the tests of 257-285
def share_bars(b):
    def bar_rh(ns, s):
        out = collections.defaultdict(list)
        for n in ns:
            if n["sec"] == s: out[n["on"] // BAR - P.BAR0[s]].append(n["on"] % BAR)
        return [tuple(x) for k, x in sorted(out.items())]
    a, c = bar_rh(nts(b), "Verse 2"), bar_rh(nts(b), "Verse 1"); return sum(1 for x in a if x in set(c)) / max(1, len(a))
T8 = {}
for v in "ABC":
    D = RUN[v]; Al = D["all"]; pk = D["pick"]; L5 = R["5"][v]; t = {}
    lr = [b["lines"] for b in Al]
    sl = [P.line_readings(nts(e)) for e in D["every"] if e["cause"] is None]                 # every survivor, from the full file
    t["257"] = dict(median_arch_or_falling=L5["builds"]["arch_or_falling"][1], median_arch_positive=L5["builds"]["arch_positive"][1],
                    survivors_outside_31_94=sum(not (0.31 <= x["arch_or_falling"] <= 0.94) for x in sl), survivors_valley_over_33=sum(x["valley"] > 0.33 for x in sl), n_survivors_read=len(sl))
    t["258"] = dict(median=L5["builds"]["widening"][1], survivors_outside=sum(not (-1.4 <= x["widening"] <= 1.9) for x in sl),
                    pick_by_fifths=None)
    t["259"] = dict(median_extra_bits=L5["builds"]["first_note_extra_bits"][1], median_join_fourth=L5["join_fourth"][1],
                    survivors_under_minus_01=sum(x["first_note_extra_bits"] < -0.1 for x in sl))
    t["260"] = dict(median_after=L5["entry_260"]["builds_after"][1], survivors_under_10=sum(x["starts_after_downbeat"] < 0.10 for x in sl))
    t["261"] = dict(last_over_mean=L5["builds"]["last_over_mean"], last_longest=L5["last_longest"], pick=L5["pick"]["last_over_mean"])
    eb = L5["ends_builds"]
    t["262"] = dict(ends_pick=L5["ends_pick"], last_chorus_tonic=round(float(np.mean([section_ends(nts(b))["Last Chorus"] == 0 for b in Al])), 3),
                    chorus1_triad=round(float(np.mean([section_ends(nts(b))["Chorus 1"] in (0, 4, 7) for b in Al])), 3),
                    verse1_off_tonic=round(float(np.mean([section_ends(nts(b))["Verse 1"] != 0 for b in Al])), 3))
    t["264"] = dict(era_deaths=D["deaths"].get("era: fewer than four of five bands inside CLASSIC's 5th-95th (264)", 0), made=D["made"],
                    pick_inside_mid=len(R["7"][v]["pick_inside_mid"]))
    t["265"] = dict(pick_window=pk["meta"]["win"], years={p: (P.YEAR[i] if i is not None else None) for p, i in pk["meta"]["win"].items()},
                    chorus_windows_to_1979=(round(float(np.mean([P.YEAR[b["meta"]["win"]["C"]] <= 1979 for b in Al if b["meta"]["win"]["C"] is not None])), 3) if v != "C" else None))
    t["266"] = dict(not_in_rows=P.NOT_IN_ROWS if v != "A" else [k for k in P.AIMED if k not in P.TR["measures"]])
    t["267"] = dict(deaths=D["deaths"].get("returns related (267)", 0), by_reading=dict(collections.Counter(r[2] for b in Al for r in b["info"]["returns"])))
    t["268"] = dict(v2_share=pct([share_bars(b) for b in Al]), in_range=round(float(np.mean([0.25 <= share_bars(b) <= 0.75 for b in Al])), 3))
    L3 = R["5"][v]["entry_231"]
    t["269"] = dict(after=L5["entry_260"]["builds_after"][1], b13=L3["builds_b13"])
    t["270"] = dict(run_deaths_only_10=(R["3"][v]["soft_by_limit"].get("run_max", 0), R["3"][v]["hard_by_limit"].get("run_max", 0)),
                    lines_with_run4=round(float(np.mean([sum(1 for r in [x for x in _runs(nts(b))] if r >= 4) / max(1, len(_runs(nts(b)))) for b in Al[:600]])), 3) if False else None,
                    reciting_median=R["7"][v]["reciting_verse"][1])
    T8[v] = t
def _runs(ns):
    out = []
    for ln in dict.fromkeys(n["line"] for n in ns):
        ps = [n["p"] for n in ns if n["line"] == ln]; run = best = 1
        for a, b2 in zip(ps, ps[1:]): run = run + 1 if a == b2 else 1; best = max(best, run)
        out.append(best)
    return out
for v in "ABC":
    Al = RUN[v]["all"]; rr = [_runs(nts(b)) for b in Al]
    T8[v]["270"]["lines_with_run4"] = round(float(np.mean([x >= 4 for r in rr for x in r])), 3)
    T8[v]["270"]["songs_longest"] = pct([max(r) for r in rr], (5, 25, 50, 75, 95))
# 271/285: aims followed (correlation of target and reading across builds), two songs running
cors = {}
for v in "BC":
    Al = RUN[v]["all"]; cv = {}
    for k in ("on_tonic", "on_third", "on_fifth", "on_beat3", "on_beats_2_4", "turns_per_move", "repeat", "step", "chord_tones_on_beat", "gap_eighth"):
        for w, p_ in (("v", "V"), ("c", "C")):
            tt = [b["meta"]["targets"][p_][k] for b in Al]; rd = [b["read"][w][k] if b["read"][w] else np.nan for b in Al]
            ok = [(a, b_) for a, b_ in zip(tt, rd) if np.isfinite(a) and np.isfinite(b_)]
            cv[f"{w}:{k}"] = round(float(np.corrcoef(*zip(*ok))[0, 1]), 3) if len(ok) > 5 and np.std([a for a, _ in ok]) > 0 else None
    cors[v] = cv
R["8"] = dict(tests=T8, aims_followed=cors, song38_v1={"v:turns_per_move": 0.17, "c:turns_per_move": 0.12, "v:on_beat3": 0.23, "c:on_beat3": 0.19},
              song39={"v:turns_per_move": 0.56, "c:turns_per_move": 0.33, "v:on_beat3": 0.03, "c:on_beat3": 0.37})
st = RUN["B"]["stats"]
R["8"]["282"] = dict(changed_twice_notes=pct([b["meta"].get("twice_changed", 0) for b in RUN["B"]["all"]]), pick_changed=RUN["B"]["pick"]["meta"].get("twice_changed"))
R["8"]["281"] = dict(free_notes_pick=dict(RUN["B"]["pick"]["meta"]["free"]), free_verse=pct([b["meta"]["free"].get("Verse 1", 0) for b in RUN["B"]["all"]]))
R["8"]["278"] = {}
for v in "ABC":
    Al = RUN[v]["all"]; out = {}
    for k in P.AIMS_278:
        x = [b["aims"][k] for b in Al if b["aims"][k] is not None]; out[k] = round(float(np.mean(x)), 3)
    R["8"]["278"][v] = out
R["8"]["278"]["kept"] = {P.AIMS_278[0]: 0.729, P.AIMS_278[1]: 0.771, P.AIMS_278[2]: 0.557, P.AIMS_278[3]: 0.674, P.AIMS_278[4]: 0.558, P.AIMS_278[5]: 0.802,
                         P.AIMS_278[6]: 0.924, P.AIMS_278[7]: 0.808, P.AIMS_278[8]: 0.659, P.AIMS_278[9]: 0.541}
R["8"]["stats"] = {v: RUN[v]["stats"] for v in "ABC"}
# the content judge's give-aways, Run B against Run A and v1 (weight x z, averaged over the first 400 complete builds)
R["give_away"] = {}
for lab, Al in (("A", RUN["A"]["all"]), ("B", RUN["B"]["all"]), ("v1", V1["all"])):
    ga = collections.defaultdict(list)
    for b in Al[:400]:
        for w in ("v", "c"):
            if b["read"][w]:
                for m, x in J.give_away(b["read"][w], k=46): ga[m].append(x)
    R["give_away"][lab] = sorted(((m, round(float(np.mean(v)), 3)) for m, v in ga.items()), key=lambda x: x[1])[:6]
# item 9: the regression line from the fix list after v103, read on Run B (and C where it says so)
pB = RUN["B"]["pick"]; nb = pB["notes"]
R["9"] = dict(orders={v: (RUN[v]["order_fp"], RR[v]["order_fp"]) for v in "ABC"},
              six_A4=len([n for n in nb if n["p"] == 69]) == 6, chorus_opening_unrelated=not P.opening_rel(nb, "Chorus 1", "Verse 1")[0],
              chorus_floor_above=P.low(nb, "Chorus 1") > P.low(nb, "Verse 1"), chorus_floor=(P.low(nb, "Chorus 1"), P.low(nb, "Verse 1")),
              era_pick_mid=R["7"]["B"]["pick_inside_mid"], era_pick_95=R["7"]["B"]["pick_inside_95"],
              era_deaths={v: RUN[v]["deaths"].get("era: fewer than four of five bands inside CLASSIC's 5th-95th (264)", 0) for v in "ABC"},
              return_deaths={v: RUN[v]["deaths"].get("returns related (267)", 0) for v in "ABC"},
              reciting={v: R["7"][v]["reciting_verse"][1] for v in "ABC"}, v2_share={v: T8[v]["268"]["v2_share"][1] for v in "ABC"})
json.dump(R, open(f"{H}/readings_v2.json", "w"), indent=1, default=str)
pickle.dump(R, open(f"{H}/readings_v2.pkl", "wb"))
print(json.dumps({k: R[k] for k in ("1",)}, indent=1, default=str))
for r in R["2"]["rows"]: print(f'{r["gate"][:60]:60s} v1 {r["v1"]:5d}  A {r["A"]:5d}  B {r["B"]:5d}  C {r["C"]:5d}')
