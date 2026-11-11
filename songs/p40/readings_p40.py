"""Song 40 under v108: the report's readings from the main run (243 on) and the control (243 off), each made twice.
Items 1-8 of song 38's rerun report, plus: the lift the registers drew (288), the spectral reading beside it (286), soft breaks with
the seven new limits, the most note lengths in eight bars, the tests of 257-297, the three builds of 255 and the pick under the
old fit term (296). Writes readings_p40.json and readings_p40.pkl."""
import sys, pickle, collections, json
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p40")
import melody_p40 as P, judges as J
H = "/home/claude/p40"; M = P.M; BAR, BEAT = P.BAR, P.BEAT
RUN = {v: pickle.load(open(f"{H}/melody_{v}.pkl", "rb")) for v in ("main", "ctl")}
RR = {v: pickle.load(open(f"{H}/melody_{v}_r.pkl", "rb")) for v in ("main", "ctl")}
LJ = json.load(open(f"{H}/limits286_joint.json")); L286 = json.load(open(f"{H}/limits286.json"))
DJ = P.LIT["bands"]["bands (5, 25, 50, 75, 95)"]; REG = P.REG
V = ("main", "ctl")
def pct(v, q=(5, 50, 95)):
    v = [float(x) for x in v if x is not None and np.isfinite(x)]
    return [round(float(np.percentile(v, k)), 3) for k in q] if v else None
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
def done(v): return [e for e in RUN[v]["every"] if e["soft"] is not None]
R = {}

# 1 survivors and frozen orders
R["1"] = {v: dict(made=RUN[v]["made"], survivors=RUN[v]["survivors"], share=round(RUN[v]["survivors"] / RUN[v]["made"], 4), order=RUN[v]["order_fp"],
                  rerun_order=RR[v]["order_fp"], reproduced=RUN[v]["order_fp"] == RR[v]["order_fp"] and RUN[v]["survivors"] == RR[v]["survivors"]
                  and RUN[v]["pick"]["fp"] == RR[v]["pick"]["fp"], code=RUN[v]["rerun"]["code_sha"], line_knobs=RUN[v]["line_knobs"],
                  calib_lines=RUN[v]["calibration"][-1].get("lines"), seed=RUN[v]["rerun"]["seed"]) for v in V}

# 2 deaths per gate, and what would fail
keys = sorted(set(RUN["main"]["deaths"]) | set(RUN["ctl"]["deaths"]), key=lambda k: -RUN["main"]["deaths"].get(k, 0))
R["2"] = dict(rows=[dict(gate=k, **{v: RUN[v]["deaths"].get(k, 0) for v in V}) for k in keys],
              would={v: {k: RUN[v]["would"].get(k, 0) for k in P.GATES} for v in V},
              broken={v: {k[len("limit broken: "):]: n for k, n in sorted(RUN[v]["would"].items(), key=lambda x: -x[1]) if k.startswith("limit broken: ")} for v in V})

# 3 the limits: 276/277 with 286's seven
LIM7 = list(P.LIM7)
def lim_row(k):
    if k in P.SOFT:
        d = P.DIRN[k]; return ("under 10" if k == "run_max" else P.SOFT[k]), ("under 15" if k == "run_max" else P.HARD[k]), d
    d, s_, h_ = P.LIM7[k]; return s_, h_, d
R["3"] = {}
for v in V:
    E = done(v); n_ = len(E); pk = RUN[v]["pick"]
    sb = collections.Counter(min(3, len(e["soft"])) for e in E)
    s8 = collections.Counter(min(3, len([k for k in e["soft"] if k in P.SOFT])) for e in E)
    lim = {}
    for k in P.LIMITS: lim[k] = [round(float(np.median([e["limits"][k] for e in E])), 4), round(float(pk["info"]["limits"][k]), 4)] + list(lim_row(k))
    for k in LIM7: lim[k] = [round(float(np.median([e["limits7"][k] for e in E if e["limits7"][k] is not None])), 4), round(float(pk["info"]["limits7"][k]), 4)] + list(lim_row(k))
    R["3"][v] = dict(complete=n_, soft_share={str(k): round(sb[k] / n_, 3) for k in range(4)}, soft_share_eight_only={str(k): round(s8[k] / n_, 3) for k in range(4)},
                     hard_any=sum(bool(e["hard"]) for e in E), deaths_on_hard=RUN[v]["deaths"].get(P.GATES[0], 0) and sum(bool(e["hard"]) and e["cause"] == P.GATES[0] for e in E),
                     deaths_on_three_soft=sum((not e["hard"]) and len(e["soft"]) >= 3 and e["cause"] == P.GATES[0] for e in E),
                     soft_by_limit=dict(collections.Counter(k for e in E for k in e["soft"]).most_common()),
                     hard_by_limit=dict(collections.Counter(k for e in E for k in e["hard"]).most_common()),
                     pick_soft=pk["info"]["soft"], pick_hard=pk["info"]["hard"], limits=lim,
                     lengths=pct([e["limits"]["max_lengths_8_bars"] for e in E], (5, 25, 50, 75, 95)),
                     lengths_dist=dict(sorted(collections.Counter(e["limits"]["max_lengths_8_bars"] for e in E).items())),
                     lengths_pick=pk["info"]["limits"]["max_lengths_8_bars"],
                     run_max=pct([e["limits"]["run_max"] for e in E], (5, 25, 50, 75, 95)))
R["3"]["kept_soft_eight"] = P.GL["kept songs: soft breaks 0, 1, 2, 3 or more"]
R["3"]["pairs_seven"] = LJ

# 4 the kept pass rate of every gate in the search
A_ = P.GL["audit, as coded"]["gates (share of kept songs that pass; songs it could be read on)"]
R["4"] = dict(gates=[
    ("limits: a hard limit or three soft breaks, the eight of 276 (276/277)", 0.92, "Table DL (v106 file)"),
    ("the seven of 286 as limits, alone (a hard limit or three soft breaks among them)", LJ["pass_as_limits"], "the 515 POP909 calibration pairs (the spectral limits the v108 file's)"),
    ("returns related (267)", None, "not printed by the paper"),
    ("chorus opening unrelated (227)", A_["227: chorus opening unrelated to the verse's"][0], "Table DL"),
    ("bridge opening unrelated (208)", A_["208: bridge opening unrelated to verse and chorus"][0], "Table DL"),
    ("pushed notes at most 42% (159)", A_["159: pushed notes at most 42%"][0], "Table DL"),
    ("density 1.1 to 4.9 notes a second (159)", P.GL["audit, as coded"]["159 density, 1.1 to 4.9 notes a second (top-five singles 1950-2024)"][0], "Table DL"),
    ("key word on a chord tone (134)", 0.9, "Window 94 ('about nine in ten')"),
    ("the judge's floor (254, 291)", 0.95, "kept held-out 5th percentile (v108 judges file)"),
    ("joins: a held end and a breath (212)", None, "unread by the paper (a lyric-placement rule)"),
    ("the voice's range (intake)", None, "the writer's voice row")],
    seven_soft_alone=LJ["soft_alone"], seven_hard_alone=LJ["hard_alone"], pairs=LJ["pairs"], corpus=L286["corpus"])

# 5 Table DJ line readings; entry (260/297) and landing (289)
KEYS = ["arch_or_falling", "valley", "arch_positive", "arch_term", "falling_term", "peak_first_third", "end_minus_mean", "last_over_mean", "widening",
        "first_note_extra_bits", "starts_on_downbeat", "starts_after_downbeat", "starts_as_pickup", "ends_on_downbeat"]
def landing(ns):
    c = collections.Counter(); n_ = 0
    for ln in dict.fromkeys(n["line"] for n in ns):
        x = [n for n in ns if n["line"] == ln]; t = x[-1]["on"] % BAR; n_ += 1
        c["b1" if t == 0 else "b3" if t == 24 else "b24" if t in (12, 36) else "off"] += 1
    return {k: c[k] / n_ for k in ("b1", "b3", "b24", "off")}
def stress_landing(ns):
    off = b13 = n_ = 0
    for ln in dict.fromkeys(n["line"] for n in ns):
        st = [n for n in ns if n["line"] == ln and n["stress"]]
        if not st: continue
        t = st[-1]["on"] % BAR; n_ += 1; off += t % BEAT != 0; b13 += t in (0, 24)
    return b13 / n_, off / n_
DEG = {0: "1", 2: "2", 4: "3", 5: "4", 7: "5", 9: "6", 11: "7", 3: "b3", 10: "b7", 1: "b2", 6: "#4", 8: "b6"}
def ends(ns): return {s: DEG[([n for n in ns if n["sec"] == s][-1]["p"] - M.TONIC) % 12] for s in P.SUNG}
R["5"] = {"kept": {k: DJ[k]["kept songs"] for k in KEYS}, "kept_kinds": P.KEPT_KINDS}
for v in V:
    Al = RUN[v]["all"]; pk = RUN[v]["pick"]; pl = pk["lines"]
    kinds = collections.Counter()
    for b in Al:
        for k, x in b["lines"]["kinds"].items(): kinds[k] += x
    LD = [landing(nts(b)) for b in Al]; SL = [stress_landing(nts(b)) for b in Al]; EN = [ends(nts(b)) for b in Al]
    R["5"][v] = dict(builds={k: pct([b["lines"][k] for b in Al]) for k in KEYS}, pick={k: round(float(pl[k]), 3) for k in KEYS},
                     outside_mid={k: round(float(np.mean([not (DJ[k]["kept songs"][1] <= b["lines"][k] <= DJ[k]["kept songs"][3]) for b in Al if np.isfinite(b["lines"][k])])), 3) for k in KEYS},
                     kinds={k: round(x / len(Al), 3) for k, x in kinds.most_common()}, pick_kinds=pl["kinds"],
                     join_fourth=pct([b["lines"]["join_fourth"] for b in Al]), pick_join_fourth=round(pl["join_fourth"], 3),
                     landing={k: pct([x[k] for x in LD]) for k in ("b1", "b3", "b24", "off")}, landing_pick={k: round(x, 3) for k, x in landing(pk["notes"]).items()},
                     stress_b13=pct([x[0] for x in SL]), stress_off=pct([x[1] for x in SL]), stress_pick=[round(x, 3) for x in stress_landing(pk["notes"])],
                     last_longest=pct([b["lines"]["last_longest"] for b in Al]), ends_pick=ends(pk["notes"]),
                     ends_builds={s: dict(collections.Counter(e[s] for e in EN).most_common(4)) for s in ("Verse 1", "Chorus 1", "Bridge", "Last Chorus")},
                     contour_drawn=dict(collections.Counter(k for b in Al for k in b["meta"].get("contour", {}).values()).most_common()))

# 6 fix 255 (and 291, 296)
R["6"] = {}
for v in V:
    D = RUN[v]; out = {}
    for lab, c in (("composite first", D["comp_first"]), ("shortlist pick", D["pick"]), ("judge first", D["judge_first"]), ("pick under the old fit term (296)", D["pick_old_fit"])):
        out[lab] = dict(fp=c["fp"], composite=round(c["meas"]["composite"], 3), composite_old=round(c["meas"]["composite_old_fit"], 3), content=round(c["judge"]["content"], 3),
                        order=round(c["judge"]["order"], 3), combined=round(c["judge"]["combined"], 3), lift={k: float(x) for k, x in c["info"]["lift"].items()},
                        spectral=round(float(c["info"]["tb"]["spectral"]), 3))
    byj = sorted(D["all_alive"], key=lambda x: (-x[1], x[0])); rank = [x[0] for x in byj].index(D["comp_first"]["fp"]) + 1
    byo = sorted(D["all_alive"], key=lambda x: (-x[5], x[0])); old_first = byo[0][0]
    out.update(shortlist_size=len(D["short"]), survivors=D["survivors"], comp_first_rank_by_judge=rank, pick_changed=D["comp_first"]["fp"] != D["pick"]["fp"],
               old_fit_first=old_first, old_fit_rank_of_pick=[x[0] for x in byo].index(D["pick"]["fp"]) + 1,
               pick_old_differs=D["pick_old_fit"]["fp"] != D["pick"]["fp"])
    jall = [b["judge"] for b in D["all"]]
    out["builds"] = dict(content=pct([j["content"] for j in jall]), order=pct([j["order"] for j in jall]), combined=pct([j["combined"] for j in jall]))
    out["above_kept_median"] = round(float(np.mean([j["combined"] >= J.KEPT["combined"]["50"] for j in jall])), 3)
    out["above_kept_25"] = round(float(np.mean([j["combined"] >= J.KEPT["combined"]["25"] for j in jall])), 3)
    out["below_floor"] = round(float(np.mean([j["combined"] < J.FLOOR for j in jall])), 3)
    R["6"][v] = out
R["6"]["kept"] = J.KEPT; R["6"]["floor"] = J.FLOOR
R["give_away"] = {}
for v in V:
    ga = collections.defaultdict(list)
    for b in RUN[v]["all"][:400]:
        for w in ("v", "c"):
            if b["read"][w]:
                for m, x in J.give_away(b["read"][w], k=46): ga[m].append(x)
    R["give_away"][v] = sorted(((m, round(float(np.mean(x)), 3)) for m, x in ga.items()), key=lambda x: x[1])[:5]

# 7 distance, outside, reciting, era (no era chosen: read, not gated)
R["7"] = {}
for v in V:
    Al = RUN[v]["all"]; pk = RUN[v]["pick"]; er = pk["read"]["era"]
    R["7"][v] = dict(distance=pct([b["read"]["dist"] for b in Al]), pick_distance=round(pk["read"]["dist"], 3),
                     outside=pct([b["read"]["outside"] for b in Al]), pick_outside=pk["read"]["outside"],
                     reciting_verse=pct([b["read"]["ax_v"][4] for b in Al]), pick_reciting=round(float(pk["read"]["ax_v"][4]), 3),
                     era_pick={k: round(er[k], 3) for k in P.ERA_K}, windows_years={p: (P.YEAR[i] if i is not None else None) for p, i in pk["meta"]["win"].items()},
                     pool_years={p: [min(P.YEAR[i] for i in P.POOL[p]), int(np.median([P.YEAR[i] for i in P.POOL[p]])), max(P.YEAR[i] for i in P.POOL[p])] for p in P.POOL})

# extras: the lift (288), the spectral reading beside it (286), the lengths
KL = {"median": "chorus_median_minus_verse", "top": "chorus_top_minus_verse", "lowest": "chorus_floor_minus_verse", "bridge": "bridge_median_minus_verse"}
R["lift"] = {"kept": {k: dict(zip(("1", "5", "25", "50", "75", "95", "99"), REG[KL[k]])) for k in KL}}
for v in V:
    E = done(v); pk = RUN[v]["pick"]; S = [e for e in E if e["cause"] is None]
    drawn = [e["registers"] for e in RUN[v]["every"] if e.get("registers")]
    R["lift"][v] = dict(builds={k: pct([e["lift"][k] for e in E], (5, 25, 50, 75, 95)) for k in KL}, survivors={k: pct([e["lift"][k] for e in S], (5, 25, 50, 75, 95)) for k in KL},
                        drawn={k: pct([d[f"chorus_{'floor' if k == 'lowest' else k}" if k != "bridge" else "bridge_median"] for d in drawn], (5, 25, 50, 75, 95)) for k in KL},
                        pick={k: float(pk["info"]["lift"][k]) for k in KL}, pick_drawn={k: round(float(x), 2) for k, x in pk["meta"]["registers"].items()},
                        notes_pick=dict(chorus_top=P.top(pk["notes"], "Chorus 1"), verse_top=P.top(pk["notes"], "Verse 1"), chorus_low=P.low(pk["notes"], "Chorus 1"),
                                        verse_low=P.low(pk["notes"], "Verse 1"), chorus_med=P.med(pk["notes"], "Chorus 1"), verse_med=P.med(pk["notes"], "Verse 1"),
                                        bridge_top=P.top(pk["notes"], "Bridge"), song_top=max(n["p"] for n in pk["notes"])),
                        inside_mid={k: round(float(np.mean([REG[KL[k]][2] <= e["lift"][k] <= REG[KL[k]][4] for e in E])), 3) for k in KL},
                        corr_drawn_read={k: round(float(np.corrcoef([e["registers"][f"chorus_{'floor' if k == 'lowest' else k}" if k != "bridge" else "bridge_median"] for e in E],
                                                                     [e["lift"][k] for e in E])[0, 1]), 3) for k in KL})
    bins = {"within 2": [], "3 to 5": [], "6 or more": []}
    for e in E:
        lm = e["lift"]["median"]; b = "within 2" if abs(lm) <= 2 else "3 to 5" if abs(lm) <= 5 else "6 or more"
        if e["limits7"]["spectral"] is not None: bins[b].append(e["limits7"]["spectral"])
    R["lift"][v]["spectral_by_lift"] = {b: (len(x), round(float(np.median(x)), 3) if x else None) for b, x in bins.items()}
    R["lift"][v]["spectral"] = pct([e["limits7"]["spectral"] for e in E], (1, 5, 50, 95, 99))
    R["lift"][v]["spectral_pick"] = round(float(pk["info"]["limits7"]["spectral"]), 3)
    R["lift"][v]["spectral_soft"] = sum("spectral" in e["soft"] for e in E); R["lift"][v]["spectral_hard"] = sum("spectral" in e["hard"] for e in E)
    R["lift"][v]["deaths_with_spectral"] = sum(e["cause"] == P.GATES[0] and ("spectral" in e["hard"] or "spectral" in e["soft"]) for e in E)
    R["lift"][v]["deaths_spectral_decisive"] = sum(e["cause"] == P.GATES[0] and ("spectral" in e["hard"] or (not e["hard"] and len(e["soft"]) == 3 and "spectral" in e["soft"])) for e in E)
    R["lift"][v]["corr_spectral_lift"] = round(float(np.corrcoef([e["limits7"]["spectral"] for e in E if e["limits7"]["spectral"] is not None],
                                                                 [e["lift"]["median"] for e in E if e["limits7"]["spectral"] is not None])[0, 1]), 3)
R["lift"]["kept_spectral_by_lift"] = {"within 2": 0.83, "3 to 5": 1.08, "6 or more": 1.23}

# 8 the tests of 257-297
def share_bars(ns):
    def bar_rh(s):
        out = collections.defaultdict(list)
        for n in ns:
            if n["sec"] == s: out[n["on"] // BAR - P.BAR0[s]].append(n["on"] % BAR)
        return [tuple(x) for k, x in sorted(out.items())]
    a, c = bar_rh("Verse 2"), bar_rh("Verse 1"); return sum(1 for x in a if x in set(c)) / max(1, len(a))
def runs(ns):
    out = []
    for ln in dict.fromkeys(n["line"] for n in ns):
        ps = [n["p"] for n in ns if n["line"] == ln]; run = best = 1
        for a, b2 in zip(ps, ps[1:]): run = run + 1 if a == b2 else 1; best = max(best, run)
        out.append(best)
    return out
T8 = {}
for v in V:
    D = RUN[v]; Al = D["all"]; pk = D["pick"]; L5 = R["5"][v]; t = {}
    sl = [b["lines"] for b in Al if b["cause"] is None]
    t["257"] = dict(median_af=L5["builds"]["arch_or_falling"][1], median_pos=L5["builds"]["arch_positive"][1], n=len(sl),
                    surv_outside=sum(not (0.31 <= x["arch_or_falling"] <= 0.94) for x in sl), surv_valley=sum(x["valley"] > 0.33 for x in sl))
    t["258"] = dict(median=L5["builds"]["widening"][1], surv_outside=sum(not (-1.4 <= x["widening"] <= 1.9) for x in sl))
    t["259"] = dict(median=L5["builds"]["first_note_extra_bits"][1], joins=L5["join_fourth"][1], surv_under=sum(x["first_note_extra_bits"] < -0.1 for x in sl))
    t["260"] = dict(median=L5["builds"]["starts_after_downbeat"][1], surv_under=sum(x["starts_after_downbeat"] < 0.10 for x in sl))
    t["261"] = dict(last_over_mean=L5["builds"]["last_over_mean"], last_longest=L5["last_longest"])
    EN = [ends(nts(b)) for b in Al]
    t["262"] = dict(last_tonic=round(float(np.mean([e["Last Chorus"] == "1" for e in EN])), 3), c1_triad=round(float(np.mean([e["Chorus 1"] in ("1", "3", "5") for e in EN])), 3),
                    v1_off=round(float(np.mean([e["Verse 1"] != "1" for e in EN])), 3), moved=D["stats"].get("262: last note moved", 0))
    t["265"] = dict(windows=R["7"][v]["windows_years"])
    t["266"] = dict(not_in_rows=P.NOT_IN_ROWS)
    t["267"] = dict(deaths=D["deaths"].get("returns related (267)", 0), would=D["would"].get("returns related (267)", 0),
                    by_reading=dict(collections.Counter(r[2] for b in Al for r in b["info"]["returns"])))
    sh = [share_bars(nts(b)) for b in Al]
    t["268"] = dict(share=pct(sh), in_range=round(float(np.mean([0.25 <= x <= 0.75 for x in sh])), 3))
    rr = [runs(nts(b)) for b in Al]
    t["270"] = dict(lines_run4=round(float(np.mean([x >= 4 for r in rr for x in r])), 3), longest=pct([max(r) for r in rr], (5, 25, 50, 75, 95)),
                    reciting=R["7"][v]["reciting_verse"][1])
    cv = {}
    for k in ("turns_per_move", "on_beat3", "on_tonic", "on_third", "on_fifth", "repeat", "step", "chord_tones_on_beat", "gap_eighth", "gap_sixteenth"):
        for w, p_ in (("v", "V"), ("c", "C")):
            tt = [b["meta"]["targets"][p_][k] for b in Al]; rd = [b["read"][w][k] if b["read"][w] else np.nan for b in Al]
            ok = [(a, b_) for a, b_ in zip(tt, rd) if np.isfinite(a) and np.isfinite(b_)]
            cv[f"{w}:{k}"] = round(float(np.corrcoef(*zip(*ok))[0, 1]), 3) if len(ok) > 5 and np.std([a for a, _ in ok]) > 0 else None
    t["271"] = cv
    t["278"] = {k: (round(float(np.mean([b["aims"][k] for b in Al if b["aims"][k] is not None])), 3)) for k in P.AIMS_278}
    t["288"] = dict(lengths=R["3"][v]["lengths"], inside_mid=R["lift"][v]["inside_mid"])
    t["289"] = dict(landing=L5["landing"], stress_b13=L5["stress_b13"], ends_down=L5["builds"]["ends_on_downbeat"])
    t["293"] = dict(bars_copied=D["stats"].get("293: bars copied", 0), copy_given_up=D["stats"].get("293: copy given up for a line", 0), share=t["268"]["share"])
    t["295"] = dict(moved=D["stats"].get("262: last note moved", 0), made=D["made"], share=round(D["stats"].get("262: last note moved", 0) / D["made"], 3))
    t["free"] = D["stats"].get("rhythm: placed with a free entry and landing", 0)
    T8[v] = t
R["8"] = T8
R["stats"] = {v: RUN[v]["stats"] for v in V}
R["pick"] = dict(fp=RUN["main"]["pick"]["fp"], soft=RUN["main"]["pick"]["info"]["soft"], hard=RUN["main"]["pick"]["info"]["hard"], meta_moved=RUN["main"]["pick"]["meta"]["moved"],
                 free=dict(RUN["main"]["pick"]["meta"]["free"]), plans=RUN["main"]["pick"]["meta"]["plans"], contour=RUN["main"]["pick"]["meta"].get("contour"))
def _k(x):
    if isinstance(x, dict): return {(":".join(map(str, k)) if isinstance(k, tuple) else k): _k(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [_k(y) for y in x]
    return x
pickle.dump(R, open(f"{H}/readings_p40.pkl", "wb")); R = _k(R)
json.dump(R, open(f"{H}/readings_p40.json", "w"), indent=1, default=str)
print(json.dumps({k: R[k] for k in ("1",)}, indent=1, default=str)[:1500])
