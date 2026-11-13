"""read_v136.py: song 48 on v136 (573, 577, 578, 579), main and control, beside its v134 runs of record, the judge not refitted. 557 by section
(the first verse's and chorus's windows beside their density peers on zeneng_v132_judge.json); each sung section's shares of sixteenths,
eighths and quarters among its lines' gaps beside the kept shares for the band of each line's slot rate (zeneng_v136_slot_rate.json, two-bar
slots, weighted by the lines' gaps); the dense lines' longest equal-gap run (nine notes or more at eight a bar and over, the line's own rate;
kept 4); 579's classes (reachable drawn lines of 13 notes and over in two-bar slots, by the line's own rate); 589 (the window's last note:
on the tonic, the chord under it, whether the tonic is a tone of that chord); survivors, deaths and the fixes' counts.
Usage: python3 read_v136.py  ->  read/read_v136.json"""
import sys, io, contextlib, json, pickle, collections
import numpy as np
sys.argv = ["x", "10", "main"]; sys.path.insert(0, "/home/claude/p58")
with contextlib.redirect_stdout(io.StringIO()): import melody_v136_p58 as E
BAR, BEAT = E.BAR, E.BEAT
RUNS = {"v136 main": "/home/claude/p58/run136/melody_v136_p58_main.pkl", "v136 ctl": "/home/claude/p58/run136/melody_v136_p58_ctl.pkl",
        "v134 main": "/home/claude/p58/run/melody_v134_p58_main_r.pkl", "v134 ctl": "/home/claude/p58/run/melody_v134_p58_ctl_r.pkl"}
KB557 = json.load(open("/home/claude/p58/tables/zeneng_v133_density.json"))["557: kept windows by band on zeneng_v132_judge.json: n, mean, 5th, 25th, 50th percentile (last figure: mean on the v129 judge)"]
SR = json.load(open("/home/claude/p58/tables/zeneng_v136_slot_rate.json"))
SR2 = SR["two-bar slots (over 6 to 10 beats)"]; SRA = SR["all slots"]
GV = {3: "sixteenth", 6: "eighth", 12: "quarter"}
K579 = {"under 8": 0.65, "8 to 10": 0.51, "10 and over": 0.34}
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
def longest(ons):
    g = [b - a for a, b in zip(ons, ons[1:])]; r, m = 1, 1 if g else 0
    for a, b in zip(g, g[1:]): r = r + 1 if a == b else 1; m = max(m, r)
    return m
def rate(o): return 4 * (len(o) - 1) / max(0.25, (o[-1] - o[0]) / BEAT)
def rband(x): return "under 8" if x < 8 else "8 to 10" if x < 10 else "10 and over"
out = {}
for lab, path in RUNS.items():
    D = pickle.load(open(path, "rb")); A = D["all"]; r = {}; C2 = D["chords2"]
    r["runs"] = dict(made=D["made"], complete=len(A), survivors=D["survivors"], order=D["order_fp"], deaths=dict(D["deaths"].most_common()),
                     pick=D["pick"]["fp"] if D.get("pick") else None, calibration_rounds=D["rerun"].get("calibration_rounds"))
    r["join deaths, where"] = dict(collections.Counter(c.get("where") for c in D["every"] if c["cause"] and "join" in c["cause"]).most_common())
    r["align deaths, where"] = dict(collections.Counter(c.get("where") for c in D["every"] if c["cause"] and "align" in c["cause"]).most_common())
    # 557, by section and in all
    sec557 = collections.defaultdict(list)
    for b in A:
        for s_ in ("Verse 1", "Chorus 1"):
            N_ = E.win_N(nts(b), E.BAR0[s_]); f_ = E.feats(N_, E.mton())
            if not f_: continue
            sc_ = E.refit_score(f_, N_); bd_ = E.kband(f_["notes_per_bar"]); sec557[s_].append((sc_ - KB557[bd_][1], sc_ < KB557[bd_][2], f_["notes_per_bar"], bd_))
    r["557: by section (less the band's kept mean; under the band's kept 5th; notes a bar; windows by band)"] = {
        s_: dict(rel=round(float(np.mean([x[0] for x in v])), 2), under5=round(float(np.mean([x[1] for x in v])), 3), npb=round(float(np.mean([x[2] for x in v])), 2),
                 bands={k_: round(c_ / len(v), 2) for k_, c_ in collections.Counter(x[3] for x in v).items()}) for s_, v in sec557.items()}
    allw = [x for v in sec557.values() for x in v]
    r["557: both windows"] = dict(rel=round(float(np.mean([x[0] for x in allw])), 2), under5=round(float(np.mean([x[1] for x in allw])), 3))
    # 578: gap values by section beside the kept shares for each line's slot band
    GS = collections.defaultdict(collections.Counter); KX = collections.defaultdict(lambda: collections.defaultdict(float)); LN = []
    CL = collections.defaultdict(lambda: [0, 0, 0, 0])
    for b in A:
        ns = nts(b); byl = collections.defaultdict(list)
        for n in ns: byl[n["line"]].append(n["on"])
        for s in E.SUNG:
            for i in range(len(E.LINES[s])):
                o = sorted(byl.get(f"{s}:{i}", []))
                if len(o) < 2: continue
                g = [y - x for x, y in zip(o, o[1:])]; nb_ = E.slot_len(s, i); band = E.kband(len(o) / nb_); tab = (SR2 if nb_ == 2 else SRA)[band]["gap values, shares"]
                for d in g: GS[s][GV.get(d, "other")] += 1
                for k_ in ("sixteenth", "eighth", "quarter"): KX[s][k_] += tab[k_] * len(g)
                KX[s]["n"] += len(g)
                if len(o) >= 9 and rate(o) >= 8: LN.append(longest(o))
                # 579: reachable drawn lines of 13 notes and over in two-bar slots
                if i + 1 < len(E.LINES[s]) and len(o) >= 13 and nb_ == 2 and b["kinds"].get((s, i)) not in ("exact", "design", "both", "pitch"):
                    n_ = byl.get(f"{s}:{i + 1}")
                    if not n_: continue
                    kn = b["kinds"].get((s, i + 1)); f0 = min(n_) - E.line_start(s, i + 1)
                    reach = (kn in ("fresh", "fresh (361 unit return)", "sung again") and not E.LINES[s][i + 1][0][1]) or f0 < 0
                    if not reach: continue
                    k = min(3, min(n_) // BAR - max(o) // BAR); CL[rband(rate(o))][k] += 1; CL["all"][k] += 1
    r["578: gap values by section (sixteenth, eighth, quarter; drawn / kept for the lines' slot bands)"] = {
        s: {k_: [round(GS[s][k_] / max(1, sum(GS[s].values())), 3), round(KX[s][k_] / max(1, KX[s]["n"]), 3)] for k_ in ("sixteenth", "eighth", "quarter")} for s in E.SUNG if GS[s]}
    r["578/558: dense lines (nine notes or more at eight a bar and over), longest equal-gap run (50th, 75th, 90th, 95th; kept median 4)"] = dict(lines=len(LN), q=[float(np.percentile(LN, k)) for k in (50, 75, 90, 95)] if LN else None)
    r["579: reachable drawn lines of 13 notes and over in two-bar slots, classes 0/1/2/3 by the line's own rate (kept class 0 beside)"] = {
        k_: dict(lines=sum(c), shares=[round(x / max(1, sum(c)), 3) for x in c], kept_class0=K579.get(k_, 0.517)) for k_, c in CL.items()}
    # 589: the window's last note
    R589 = {}
    for s_ in ("Verse 1", "Chorus 1"):
        ton, chs, ct_ = [], collections.Counter(), []
        for b in A:
            N_ = E.win_N(nts(b), E.BAR0[s_])
            if not N_: continue
            ln = max(nts(b), key=lambda n: n["on"] if E.BAR0[s_] * BAR <= n["on"] < (E.BAR0[s_] + 8) * BAR else -1)
            c_ = C2[ln["on"] // (BAR // 2)]; base = c_.split("/")[0]
            ton.append(ln["p"] % 12 == E.ETON); chs[c_] += 1; ct_.append(E.ETON in E.M.CH[base][1])
        R589[s_] = dict(builds=len(ton), last_note_tonic=round(float(np.mean(ton)), 3), chord_under=dict((k_, round(v_ / len(ton), 3)) for k_, v_ in chs.most_common()),
                        tonic_a_chord_tone=round(float(np.mean(ct_)), 3))
    r["589: the window's last note (first verse and chorus)"] = R589
    r["counts"] = dict(D["rerun"].get("v136_stats", {}))
    out[lab] = r
json.dump(out, open("/home/claude/p58/read/read_v136.json", "w"), indent=1, default=str)
for lab, r in out.items():
    print("==", lab, r["runs"]["survivors"], r["runs"]["order"], r["runs"]["deaths"])
    for k, v in r.items():
        if k not in ("runs", "counts"): print("  ", k, json.dumps(v, default=str))
