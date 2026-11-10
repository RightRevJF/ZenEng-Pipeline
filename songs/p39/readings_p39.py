"""Song 39's readings for the report (ZenEng v103 tests 225-256 and the band's 233-238), from the two runs, the riff file and the record."""
import sys, pickle, collections, json, numpy as np
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p39")
import melody_p39 as P, judges as J
H = "/home/claude/p39"; M = P.M; BAR, BEAT = P.BAR, P.BEAT
MAIN = pickle.load(open(f"{H}/melody_main.pkl", "rb")); CTL = pickle.load(open(f"{H}/melody_ctl.pkl", "rb"))
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); RF = pickle.load(open(f"{H}/riff_p39.pkl", "rb"))
pick = MAIN["pick"]; notes = pick["notes"]; T = {}
def pct(v, q=(5, 50, 95)): v = [x for x in v if x is not None and np.isfinite(x)]; return [round(float(np.percentile(v, k)), 3) for k in q] if v else None
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
A_ = MAIN["all"]; C_ = CTL["all"]
# 225/226 axes
T["225"] = dict(builds_offbeat_verse=pct([b["read"]["ax_v"][5] for b in A_]), ctl_offbeat_verse=pct([b["read"]["ax_v"][5] for b in C_]),
                builds_chordbound_chorus=pct([b["read"]["ax_c"][1] for b in A_]), ctl_chordbound_chorus=pct([b["read"]["ax_c"][1] for b in C_]),
                pick_axes={w: dict(zip(P.AXN, pick["read"]["ax_" + w])) for w in ("v", "c", "b")}, names=P.AXN)
T["226"] = {}
for w in ("v", "c"):
    for k, nm in enumerate(P.AXN):
        if (w == "v" and k == 5) or (w == "c" and k == 1): continue
        a = [b["read"]["ax_" + w][k] for b in A_]; c = [b["read"]["ax_" + w][k] for b in C_]
        T["226"][f"{w}:{nm}"] = dict(median=round(float(np.median(a)), 2), spread=round(float(np.std(a)), 2), ctl_spread=round(float(np.std(c)), 2))
T["226"]["distance_builds"] = pct([b["read"]["dist"] for b in A_]); T["226"]["distance_ctl"] = pct([b["read"]["dist"] for b in C_])
T["226"]["chart_mid_half_distance"] = [round(x, 3) for x in [P.DM[next(iter(P.DM))]["centre_reference"].get("q25", 0)]] if False else None
# bar rhythms
def bar_rh(ns, s):
    out = collections.defaultdict(list)
    for n in ns:
        if n["sec"] == s: out[n["on"] // BAR - P.BAR0[s]].append(n["on"] % BAR)
    return [tuple(v) for k, v in sorted(out.items())]
def share_in(a, b): return sum(1 for x in a if x in set(b)) / max(1, len(a))
T["227"] = dict(pick=round(share_in(bar_rh(notes, "Chorus 1"), bar_rh(notes, "Verse 1")), 3),
                builds=pct([share_in(bar_rh(nts(b), "Chorus 1"), bar_rh(nts(b), "Verse 1")) for b in A_]), kept_median=0.12)
v2 = [share_in(bar_rh(nts(b), "Verse 2"), bar_rh(nts(b), "Verse 1")) for b in A_]
def exact_bars(ns):
    cells = collections.defaultdict(list)
    for n in ns: cells[n["on"] // BAR].append((n["on"] % BAR, n["p"]))
    ks = sorted(cells); seen = []; rep = 0
    for k in ks:
        c = tuple(cells[k]); rep += c in seen; seen.append(c)
    return rep / max(1, len(ks))
T["228"] = dict(pick_v2_share=round(share_in(bar_rh(notes, "Verse 2"), bar_rh(notes, "Verse 1")), 3), builds_v2_share=pct(v2),
                builds_in_quarter_to_three_quarters=round(float(np.mean([0.25 <= x <= 0.75 for x in v2])), 3), pick_exact_bars=round(exact_bars(notes), 3), chart_exact=0.38,
                last_chorus_longer_by=2)
br = [n["p"] for n in notes if n["sec"] == "Bridge"]; ch = [n["p"] for n in notes if n["sec"] == "Chorus 1" and n["on"] < (P.BAR0["Chorus 1"] + 8) * BAR]
T["229"] = dict(bridge_bits=round(M.pitch_bits(br), 3), chorus_bits=round(M.pitch_bits(ch), 3), bridge_offbeat=pick["read"]["ax_b"][5], verse_offbeat=pick["read"]["ax_v"][5])
# 230 lyric slots and sung rate
rows = []
for s in P.SUNG:
    for i, sy in enumerate(P.LINES[s]): rows.append((s, i + 1, len(sy), "2 bars"))
def sung_rate(ns):
    rates = []
    for ln in dict.fromkeys(n["line"] for n in ns):
        x = [n for n in ns if n["line"] == ln]; syl = len({n["syl"] for n in x}); span = (x[-1]["on"] + x[-1]["dur"] - x[0]["on"]) / BAR
        rates.append(syl / max(0.25, span))
    return float(np.median(rates))
T["230"] = dict(lines=rows, pick_rate=round(sung_rate(notes), 2), builds_rate=pct([sung_rate(nts(b)) for b in A_]))
# 231 starts and landings
def land(ns):
    off = b13 = pk = n_ = 0
    for ln in dict.fromkeys(n["line"] for n in ns):
        x = [n for n in ns if n["line"] == ln]; s, i = ln.split(":"); U = P.line_start(s, int(i)); st = [n for n in x if n["stress"]]
        if not st: continue
        t = st[-1]["on"] % BAR; n_ += 1; off += t % BEAT != 0; b13 += t in (0, 24); pk += x[0]["on"] < U
    return off / n_, b13 / n_, pk / n_
L3 = [land(nts(b)) for b in A_]; T["231"] = dict(pick=[round(x, 3) for x in land(notes)], builds_off=pct([x[0] for x in L3]), builds_b13=pct([x[1] for x in L3]), builds_pickup=pct([x[2] for x in L3]))
# 232 title
syls = [n["dur"] for n in notes if not n["slur"]]
fixed = [n for n in notes if n["syl"] in [k for k, (w, st) in enumerate(P.LINES[n["sec"]][int(n["line"].split(":")[1])]) if w.lower().startswith("fixed")] and not n["slur"]
         and "fixed by fall" in P.M.WORDS_OF[n["sec"]][int(n["line"].split(":")[1])][1].lower()]
T["232"] = dict(count=len(fixed), first_bar=min(n["on"] for n in fixed) // BAR + 1, beat=sorted({n["on"] % BAR // BEAT + 1 for n in fixed}), offbeat=sorted({n["on"] % BEAT for n in fixed}),
                held=sorted({n["dur"] for n in fixed}), median_syl=float(np.median(syls)))
# 239/240 returns
kinds = collections.Counter(v for v in pick["meta"]["kinds"].values()); allk = collections.Counter(v for b in A_ for v in b["kinds"].values())
def tonic_end(ns, rets):
    a = b_ = 0
    for sec, i, s0, i0, kd in rets:
        if kd == "sung again": continue
        x = [n for n in ns if n["line"] == f"{sec}:{i}"]; y = [n for n in ns if n["line"] == f"{s0}:{i0}"]
        a += x[-1]["p"] % 12 == M.TONIC; b_ += y[-1]["p"] % 12 == M.TONIC
    return a, b_, sum(1 for r in rets if r[4] != "sung again")
T["239"] = dict(pick_kinds=dict(kinds), builds_kinds=dict(allk), pick_returns=[(a, b, c, d, e) for a, b, c, d, e in pick["meta"]["returns"]])
te = [tonic_end(nts(b), b["meta"]["returns"]) for b in A_]; tot = sum(x[2] for x in te)
T["240"] = dict(pick=tonic_end(notes, pick["meta"]["returns"]), builds_returns_tonic=round(sum(x[0] for x in te) / max(1, tot), 3), builds_sources_tonic=round(sum(x[1] for x in te) / max(1, tot), 3))
# 243 targets: share outside the chart middle half; the aimed measures' share of a kept window's distance
out = {}
for k in P.AIMED:
    if k not in P.DM: continue
    c = P.DM[k]["chart"]; vals = [b["meta"]["targets"]["C"][k] for b in A_] + [b["meta"]["targets"]["V"][k] for b in A_]
    out[k] = round(float(np.mean([(x < c[1] or x > c[3]) for x in vals])), 3)
def dist_parts(f):
    tot, aim = 0.0, 0.0
    for k, v in P.DM.items():
        if not v["agree"] or k not in f or f[k] is None or not np.isfinite(f[k]): continue
        cr = v["centre_reference"]; d = min(3.0, max(0.0, cr["q25"] - f[k], f[k] - cr["q75"]) / cr["width"]); tot += d; aim += d if k in P.AIMED else 0
    return aim / tot if tot else np.nan
T["243"] = dict(outside_share=out, kept_aimed_share=round(float(np.nanmedian([dist_parts(r) for r in P.KR])), 3), builds_distance=pct([b["read"]["dist"] for b in A_]),
                pick_windows=pick["meta"]["win"], pool_sizes={k: len(v) for k, v in P.POOL.items()}, not_in_rows=P.NOT_IN_ROWS)
# 245 density from the lyric
need = {s: round(sum(len(sy) for sy in P.LINES[s]) / P.SECLEN[s], 2) for s in P.SUNG}
T["245"] = dict(notes_a_bar_needed=need, dense=any(v >= 4.25 for v in need.values()))
# 246-248
st = MAIN["stats"]; na = sum(st.values())
T["246"] = dict(added=dict(st), repeat_share=round(st.get("added_repeat", 0) / max(1, na), 3), run_deaths=round(MAIN["deaths"].get("monotony run (166/196)", 0) / MAIN["made"], 3))
T["247"] = dict(join_deaths=round(sum(v for k, v in MAIN["deaths"].items() if k.startswith("join")) / MAIN["made"], 3))
T["248"] = dict(return_gate_deaths=MAIN["deaths"].get("returns related, on shared events (181/219/248)", 0), made=MAIN["made"])
# 249 calibration; chord tones against targets
ct = {}
for w, p_ in (("v", "V"), ("c", "C")):
    for k in ("chord_tones_on_beat", "chord_tones_off_beat"):
        r = [b["read"][w][k] for b in A_ if b["read"][w] and np.isfinite(b["read"][w].get(k, np.nan))]; t = [b["meta"]["targets"][p_][k] for b in A_]
        ct[f"{w}:{k}"] = (round(float(np.median(r)), 3), round(float(np.mean(t)), 3))
T["249"] = dict(calibration_last=MAIN["calibration"][-1], chord_tones=ct, seed=MAIN["rerun"]["calibration_seed"])
# 250 outside count
T["250"] = dict(pick=pick["read"]["outside"], builds=pct([b["read"]["outside"] for b in A_]), kept=(16, 8, 26))
# 251 aim followed
cors = {}
for k in ("on_tonic", "on_third", "on_fifth", "on_beat3", "on_beats_2_4", "turns_per_move", "repeat", "step", "chord_tones_on_beat", "gap_eighth"):
    for w, p_ in (("v", "V"), ("c", "C")):
        t = [b["meta"]["targets"][p_][k] for b in A_]; r = [b["read"][w][k] if b["read"][w] else np.nan for b in A_]
        ok = [(a, b_) for a, b_ in zip(t, r) if np.isfinite(a) and np.isfinite(b_)]
        cors[f"{w}:{k}"] = round(float(np.corrcoef(*zip(*ok))[0, 1]), 3) if len(ok) > 5 else None
T["251"] = cors
# 252-255 judges
jc = [b["judge"]["combined"] for b in A_]; jn = [b["judge"]["content"] for b in A_]; jo = [b["judge"]["order"] for b in A_]
ga = collections.defaultdict(list)
for b in A_[:400]:
    for w in ("v", "c"):
        for m, x in J.give_away(b["read"][w], k=46): ga[m].append(x)
T["252"] = dict(pick=pick["judge"]["content"], builds=pct(jn), kept=J.KEPT["content"], give_away=sorted(((m, round(float(np.mean(v)), 3)) for m, v in ga.items()), key=lambda x: x[1])[:5])
kept_c = [J._lo(J.CJ, r) for r in P.KR]
from itertools import product
auc = float(np.mean([a > b for a, b in product(kept_c, jn[:600])]))
T["252"]["auc_kept_rows_vs_song38_builds"] = round(auc, 3)
pr = pick["judge"]["rows"]
T["253"] = dict(pick={s: {k: round(float(v), 3) for k, v in pr[s]["order_measures"].items()} for s in pr}, kept_mid={"parallel": (0.04, 0.23), "pitch_parallel": (0.03, 0.37), "smooth_barline": (-1.65, -0.17), "thin_48": (-0.2, 2.5)},
                builds_called_shuffled=round(float(np.mean([x < 0 for x in jo])), 3), order_builds=pct(jo), pick_order=pick["judge"]["order"])
T["254"] = dict(deaths=MAIN["deaths"].get("the judge's floor (254)", 0), would=MAIN["would"].get("the judge's floor (254)", 0), made=MAIN["made"], builds_combined=pct(jc), kept=J.KEPT["combined"])
cf, jf = MAIN["comp_first"], MAIN["judge_first"]
T["255"] = {lab: dict(fp=c["fp"], composite=c["meas"]["composite"], content=round(c["judge"]["content"], 3), order=round(c["judge"]["order"], 3), combined=round(c["judge"]["combined"], 3))
            for lab, c in (("composite first", cf), ("shortlist pick", pick), ("judge first", jf))}
T["255"]["shortlist_size"] = len(MAIN["short"]); T["255"]["survivors"] = MAIN["survivors"]
T["255"]["comp_first_rank_by_judge"] = 1 + [fp for fp, *_ in sorted(MAIN["all_alive_judge"], key=lambda x: -x[1])].index(cf["fp"])
# 242: not set (Q5)
T["242"] = dict(set=False)
# 227 gates on the pick; 208
T["227_pick"] = dict(chorus_median=P.med(notes, "Chorus 1"), verse_median=P.med(notes, "Verse 1"), chorus_low=P.low(notes, "Chorus 1"), verse_low=P.low(notes, "Verse 1"))
T["swing"] = REC["swung"]
T["208"] = dict(bridge_median=P.med(notes, "Bridge"), verse_median=P.med(notes, "Verse 1"), bridge_top=P.top(notes, "Bridge"))
# the band (233, 236-238)
def bar_of(t): return t // BAR
bass = REC["bass"]; drums = REC["drums"]; bars = REC["bars"]
b1 = [e for e in bass if e["on"] % BAR == 0]; root_b1 = np.mean([e["p"][0] % 12 == M.CH[bars[bar_of(e["on"])]["chord"]][0] for e in b1 if bars[bar_of(e["on"])]["chord"] != "N.C."])
roots = np.mean([e["p"][0] % 12 == M.CH[bars[bar_of(e["on"])]["chord"]][0] for e in bass if bars[bar_of(e["on"])]["chord"] != "N.C."])
kicks = [e["on"] for e in drums if 36 in e["p"]]; bon = {e["on"] for e in bass}
chord_bars = [b for b in range(REC["nbars"]) if bars[b]["kind"] not in ("Intro",) and b != REC["nbars"] - 1]
T["233"] = dict(beat1_carries_root=round(float(root_b1), 3), root_share=round(float(roots), 3), kept_root_share=(0.43, 0.73), kicks_with_bass=round(float(np.mean([k in bon for k in kicks])), 3),
                bars_with_chord_have_beat1=round(float(np.mean([any(e["on"] == b * BAR for e in bass) for b in chord_bars])), 3))
groove = collections.Counter(); sn24 = k1 = nbar = 0
for b in range(REC["nbars"]):
    ks = tuple(sorted(e["on"] % BAR for e in drums if 36 in e["p"] and bar_of(e["on"]) == b)); ss = tuple(sorted(e["on"] % BAR for e in drums if 38 in e["p"] and bar_of(e["on"]) == b))
    if not ks and not ss: continue
    groove[(ks, ss)] += 1; nbar += 1; sn24 += (12 in ss and 36 in ss); k1 += 0 in ks
top3 = sum(v for _, v in groove.most_common(3)) / nbar
fills = sum(1 for b in range(REC["nbars"]) if any(e["on"] % BAR >= 24 and 48 in e["p"] and bar_of(e["on"]) == b for e in drums))
T["236"] = dict(snare_2_4=round(sn24 / nbar, 3), kick_1=round(k1 / nbar, 3), top_groove=round(groove.most_common(1)[0][1] / nbar, 3), top3=round(top3, 3), fills=fills, bars=nbar,
                kicks_a_bar=round(len(kicks) / nbar, 2), enters_bar=min(bar_of(e["on"]) for e in drums) + 1)
org = REC["piano"]; strikes = collections.Counter(bar_of(e["on"]) for e in org)
T["237"] = dict(strikes_a_bar=round(float(np.mean(list(strikes.values()))), 2), range=(min(min(e["p"]) for e in org), max(max(e["p"]) for e in org)),
                with_bass=round(float(np.mean([e["on"] in bon for e in org])), 3))
parts = {}
for s, nb, b0, _ in REC["plan"]:
    a, z = b0 * BAR, (b0 + nb) * BAR; n = 0
    for k in ("drums", "bass", "rgtr", "piano", "lgtr", "voice2"): n += any(a <= e["on"] < z for e in REC[k])
    n += any(a <= e["on"] < z for e in REC["lead"]); parts[s] = n
T["238"] = parts
T["235"] = dict(intro=RF["pick"], fills=[(f["gap"]["after"], round(f["gap"]["beats"], 2), len(f["notes"]), (f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"]) / BEAT, (f["notes"][0]["on"] - f["gap"]["stop"]) / BEAT) for f in RF["fills"]],
                gaps=len(RF["gaps"]), fill_stats=RF["fill_stats"], solo=RF["solo_check"])
T["run"] = dict(main=dict(made=MAIN["made"], survivors=MAIN["survivors"], deaths=dict(MAIN["deaths"]), order=MAIN["order_fp"], rerun=MAIN["rerun"]),
                ctl=dict(made=CTL["made"], survivors=CTL["survivors"], deaths=dict(CTL["deaths"]), order=CTL["order_fp"], rerun=CTL["rerun"]))
pickle.dump(T, open(f"{H}/readings.pkl", "wb"))
for k, v in T.items():
    if k not in ("run",): print(k, json.dumps(v, default=str)[:600])
