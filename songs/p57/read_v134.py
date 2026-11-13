"""read_v134.py: song 47 under v134 (its last run, 571), beside v133 (a regression), beside its v131 runs. The judge of record (548, 39 measures) on every
complete build; 551: the dense lines' longest equal-gap run within the line by the line's own rate, against the kept lines
(zeneng_v132_figures.json), and the window's run and repeats at 5.5-9 notes a bar against the kept windows; 553's rounds and verse 1 /
verse 2 chord tones on the beat; 552, 555, 556 counts; 556's classes among lines whose next line can take a pickup; where the joins die.
Usage: python3 read_v132.py  ->  read/read_v134.json"""
import sys, io, contextlib, json, pickle, collections
import numpy as np
sys.argv = ["x", "10", "main"]; sys.path.insert(0, "/home/claude/p57")
with contextlib.redirect_stdout(io.StringIO()): import melody_v134_p57 as E
BAR, BEAT = E.BAR, E.BEAT
F = json.load(open("/home/claude/p57/tables/zeneng_v132_figures.json"))
KL = F["551: kept lines (CoCoPops, Window 138's lines, 3 notes or more), longest run of equal gaps within the line, by the line's own rate ((notes - 1) / beats from first to last onset, times 4)"]
KL9 = F["551: the same, lines of nine notes or more"]
KW = F["551: kept windows (545), longest run of equal gaps in the window (equal_gap_run_max, counted in gaps, a twelfth of a beat grid), by the window's notes a bar"]
K525 = json.load(open("/home/claude/p57/tables/zeneng_v131_kept_slots.json"))["525: ending classes by slot bars and by NOTES in the line"]["2"]
RUNS = {"v133 main": "run133/melody_v133_p57_main.pkl", "v133 ctl": "run133/melody_v133_p57_ctl.pkl",
        "v134 main": "run134/melody_v134_p57_main.pkl", "v134 ctl": "run134/melody_v134_p57_ctl.pkl", "v134 main, 558 off": "run134/melody_v134_p57_main_off558.pkl"}
DN = json.load(open("/home/claude/p57/tables/zeneng_v133_density.json"))
KB557 = DN["557: kept windows by band on zeneng_v132_judge.json: n, mean, 5th, 25th, 50th percentile (last figure: mean on the v129 judge)"]
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
def longest(ons):
    g = [b - a for a, b in zip(ons, ons[1:])]; r, m = 1, 1 if g else 0
    for a, b in zip(g, g[1:]): r = r + 1 if a == b else 1; m = max(m, r)
    return m
def q(v, ks=(50, 75, 90, 95)): return [round(float(np.percentile(v, k)), 2) for k in ks] if v else None
out = {}
for lab, path in RUNS.items():
    D = pickle.load(open(path, "rb")); A = D["all"]; r = {}
    r["runs"] = dict(made=D["made"], complete=len(A), survivors=D["survivors"], order=D["order_fp"], deaths=dict(D["deaths"].most_common()),
                     pick=D["pick"]["fp"] if D.get("pick") else None, calibration_rounds=D["rerun"].get("calibration_rounds"))
    r["569: align deaths by where and plan"] = {f"{k_[0]} | bridge plan {k_[1]}": v_ for k_, v_ in collections.Counter((c.get("where"), (c.get("plans") or {}).get("Bridge")) for c in D["every"] if c["cause"] and "align" in c["cause"]).most_common()}
    r["join deaths, where"] = dict(collections.Counter(c.get("where") for c in D["every"] if c["cause"] and "join" in c["cause"]).most_common())
    # 548: the judge of record (39 measures), a build's mean over the first verse's and chorus's windows
    sc = [float(np.mean([E.refit_score(E.feats(E.win_N(nts(b), E.BAR0[s]), E.mton()), E.win_N(nts(b), E.BAR0[s])) for s in ("Verse 1", "Chorus 1")])) for b in A]
    w557 = []
    for b in A:
        for s_ in ("Verse 1", "Chorus 1"):
            N_ = E.win_N(nts(b), E.BAR0[s_]); f_ = E.feats(N_, E.mton())
            if not f_: continue
            sc_ = E.refit_score(f_, N_); bd_ = E.kband(f_["notes_per_bar"]); w557.append((bd_, sc_ - KB557[bd_][1], sc_ < KB557[bd_][2], sc_ < KB557[bd_][3]))
    r["557: beside density peers (windows)"] = dict(windows_by_band={k_: round(v_ / len(w557), 3) for k_, v_ in collections.Counter(x[0] for x in w557).items()},
        less_band_mean=round(float(np.mean([x[1] for x in w557])), 3), under_band_5th=round(float(np.mean([x[2] for x in w557])), 3), under_band_25th=round(float(np.mean([x[3] for x in w557])), 3))
    r["548: judge of record (39 measures)"] = dict(mean=round(float(np.mean(sc)), 3), under_kept_song_5th=round(float(np.mean(np.array(sc) < -0.86)), 3),
                                                   pick=round(float(np.mean([E.refit_score(E.feats(E.win_N(nts(b), E.BAR0[s]), E.mton()), E.win_N(nts(b), E.BAR0[s])) for b in [x for x in A if x["fp"] == r["runs"]["pick"]][:1] for s in ("Verse 1", "Chorus 1")])), 3) if r["runs"]["pick"] else None)
    # 551: within the line, by the line's own rate
    LN = collections.defaultdict(list); WN = collections.defaultdict(lambda: collections.defaultdict(list))
    for b in A:
        ns = nts(b); byl = collections.defaultdict(list)
        for n in ns: byl[n["line"]].append(n["on"])
        for l, o in byl.items():
            o = sorted(o)
            if len(o) < 3 or not l.startswith("Verse"): continue
            rate = 4 * (len(o) - 1) / max(0.25, (o[-1] - o[0]) / BEAT); band = E.kband(rate)
            if len(o) >= 9 and rate >= 5.5: LN[("558", "8 and over" if rate >= 8 else "5.5 to 8")].append(longest(o))
            LN[("9+" if len(o) >= 9 else "3-8", band)].append(longest(o))
        for s in ("Verse 1", "Chorus 1"):
            N = E.win_N(ns, E.BAR0[s]); f = E.feats(N, E.mton()); c = E.cand(sorted(N)) or {}
            if not f or not c: continue
            band = E.kband(f["notes_per_bar"])
            for m in ("equal_gap_run_max", "gap_same_as_before"): WN[band][m].append(c[m])
            WN[band]["empty_bars"].append(f["empty_bars"])
    r["551: verse lines, longest equal-gap run within the line (median, 75th, 90th, 95th; kept beside)"] = {
        f"{k[0]} notes, {k[1]}": dict(lines=len(v), drawn=q(v), mean=round(float(np.mean(v)), 2), over_kept_95th=round(float(np.mean(np.array(v) > (KL9 if k[0] == "9+" else KL)[k[1]]["95th"])), 3),
                                    kept=[(KL9 if k[0] == "9+" else KL)[k[1]][x] for x in ("50th", "75th", "90th", "95th")]) for k, v in sorted(LN.items()) if k[0] != "558"}
    r["558: lines of nine notes or more at 5.5 a bar and over, by the line's own rate: longest run (50th, 75th, 90th, 95th; kept 50th, 75th, 95th)"] = {
        k[1]: dict(lines=len(v), drawn=q(v), kept=DN["558 and 561: kept lines by the line's own rate"][k[1]]["lines of nine notes or more"]["longest equal-gap run: 50th, 75th, 95th"],
                   over_cap_10=round(float(np.mean(np.array(v) > 10)), 4)) for k, v in sorted(LN.items()) if k[0] == "558"}
    r["551: the windows (first verse and chorus), by the window's notes a bar"] = {
        b: dict(windows=len(v["equal_gap_run_max"]), equal_gap_run_max=dict(mean=round(float(np.mean(v["equal_gap_run_max"])), 2), q=q(v["equal_gap_run_max"]), kept_q=[KW[b][x] for x in ("50th", "75th", "90th", "95th")], over_kept_95th=round(float(np.mean(np.array(v["equal_gap_run_max"]) > KW[b]["95th"])), 3)),
                gap_same_as_before=round(float(np.mean(v["gap_same_as_before"])), 3), empty_bars=round(float(np.mean(v["empty_bars"])), 3)) for b, v in sorted(WN.items())}
    # 553 with 541/503: verse 1 and verse 2, chord tones on the beat
    ct = {s: [] for s in ("Verse 1", "Verse 2")}
    for b in A:
        ns = nts(b)
        for s in ct:
            f = E.feats(E.win_N(ns, E.BAR0[s]), E.mton())
            if f: ct[s].append(f["chord_tones_on_beat"])
    r["553: verse 1 / verse 2 chord tones on the beat"] = [round(float(np.mean(ct["Verse 1"])), 3), round(float(np.mean(ct["Verse 2"])), 3)]
    r["553: the calibration's 503 rounds"] = [row.get("503 (verse 1, verse 2 unaimed, knob)") for row in D["calibration"]]
    st = D["stats"]
    r["counts"] = {k: v for k, v in sorted(st.items()) if k[:4] in ("551:", "552:", "555:", "556:", "501:", "542:", "558:", "560:", "566:")}
    # 556: classes among lines whose next line can take a pickup (2-bar slots), by notes
    CL = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0, 0]))
    for b in A:
        ns = nts(b); byl = collections.defaultdict(list)
        for n in ns: byl[n["line"]].append(n["on"])
        for s in E.SUNG:
            for i in range(len(E.LINES[s]) - 1):
                a_, n_ = byl.get(f"{s}:{i}"), byl.get(f"{s}:{i + 1}")
                if not a_ or not n_ or b["kinds"].get((s, i)) in ("exact", "design", "both", "pitch"): continue   # drawn lines only
                kn = b["kinds"].get((s, i + 1)); f0 = min(n_) - E.line_start(s, i + 1)
                reach = (kn in ("fresh", "fresh (361 unit return)", "sung again") and not E.LINES[s][i + 1][0][1]) or f0 < 0
                k = min(3, min(n_) // BAR - max(a_) // BAR); CL["reachable" if reach else "not reachable"][E.nband525(len(a_))][k] += 1
    r["556: classes 0/1/2/3 of drawn lines in two-bar slots, by notes (kept beside)"] = {
        g: {nb: dict(lines=sum(c), drawn=[round(x / max(1, sum(c)), 3) for x in c], kept=[round(x, 3) for x in K525[nb]["shares"]]) for nb, c in sorted(v.items())} for g, v in CL.items()}
    out[lab] = r
json.dump(out, open("/home/claude/p57/read/read_v134.json", "w"), indent=1, default=str)
for lab, r in out.items():
    print(lab, r["runs"]["survivors"], r["runs"]["order"], r["548: judge of record (39 measures)"], r["557: beside density peers (windows)"], r["558: lines of nine notes or more at 5.5 a bar and over, by the line's own rate: longest run (50th, 75th, 90th, 95th; kept 50th, 75th, 95th)"])
