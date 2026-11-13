"""read_v137s.py (the side run for 610, read as read_v137.py reads v137): song 48 on v137 (600, 601, 602, 603) beside v136, main and control, the judge not refitted.
- 600: drawn lines' spans (first to last onset over the slot) at the kept quartiles of their cell (notes over the slot's bars); each section's
  sixteenths, eighths and quarters beside the kept shares for its lines' cells (the chorus on drawn lines, 590); the dense lines' longest run.
- 601: reachable drawn lines of 13 notes and over in two-bar slots, class 0 by the rate as sung.
- 602: the window's last note on the tonic by the chord under it (kept 39% where the tonic is a chord tone, 19% where not); designed lines
  set aside and counted.
- 603: the verse window's leaps past a fifth and mean interval (kept dense 2%, 1.94).
- 604: each section's score less the band's kept mean in three parts: on designed lines (the window scored without them, the form's two
  measures held), following from the form (empty bars, notes a bar), and the rest; with the costliest measures.
- 557 by section, survivors, deaths, counts.
Usage: python3 read_v137.py  ->  read/read_v137s.json"""
import sys, io, contextlib, json, pickle, collections
import numpy as np
sys.argv = ["x", "10", "main"]; sys.path.insert(0, "/home/claude/p58")
with contextlib.redirect_stdout(io.StringIO()): import melody_v137_p58 as E
BAR, BEAT = E.BAR, E.BEAT
RUNS = {"side main": "/home/claude/p58/run137s/melody_v137s_p58_main.pkl", "side ctl": "/home/claude/p58/run137s/melody_v137s_p58_ctl.pkl"}
KB557 = json.load(open("/home/claude/p58/tables/zeneng_v133_density.json"))["557: kept windows by band on zeneng_v132_judge.json: n, mean, 5th, 25th, 50th percentile (last figure: mean on the v129 judge)"]
SP = json.load(open("/home/claude/p58/tables/zeneng_v137_span.json"))
CELL2 = dict(SP["600: cells below 5.5, two-bar slots"], **SP["600: cells at 5.5 and over, two-bar slots"])
GV = {3: "sixteenth", 6: "eighth", 12: "quarter"}
DRAWN = ("fresh", "fresh (361 unit return)", "sung again")
J = E.RJ; MS = J["measures"]; W = np.array(J["weight"]); MU = np.array(J["mean"]); SD = np.array(J["sd"]); FL = np.array(J["fill_missing_with"])
FORM = ("empty_bars", "notes_per_bar")
# the kept windows' mean z by band, per measure (the judge of v132)
KW = json.load(open("/home/claude/p58/tables/zeneng_v132_kept_windows.json"))
ZB = collections.defaultdict(list)
for w_ in KW["windows"]:
    x_ = np.array([FL[k] if (w_.get(m) is None or not np.isfinite(w_.get(m))) else w_[m] for k, m in enumerate(MS)], float)
    ZB[E.kband(w_["notes_per_bar"])].append((x_ - MU) / SD)
ZB = {b: np.mean(v, axis=0) for b, v in ZB.items()}
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
def xvec(N):
    f = E.feats(N, E.mton()) or {}; c = E.cand(sorted(N)) or {}; x = []
    for m, fl in zip(MS, FL):
        v = f.get(m) if m in f else c.get(m)
        x.append(fl if v is None or not np.isfinite(v) else v)
    return np.array(x, float), f
def longest(ons):
    g = [b - a for a, b in zip(ons, ons[1:])]; r, m = 1, 1 if g else 0
    for a, b in zip(g, g[1:]): r = r + 1 if a == b else 1; m = max(m, r)
    return m
def rate(o): return 4 * (len(o) - 1) / max(0.25, (o[-1] - o[0]) / BEAT)
def rband(x): return "under 8" if x < 8 else "8 to 10" if x < 10 else "10 and over"
K579 = {"under 8": 0.65, "8 to 10": 0.51, "10 and over": 0.34}
out = {}
for lab, path in RUNS.items():
    D = pickle.load(open(path, "rb")); A = D["all"]; r = {}; C2 = D["chords2"]
    r["runs"] = dict(made=D["made"], complete=len(A), survivors=D["survivors"], order=D["order_fp"], deaths=dict(D["deaths"].most_common()),
                     pick=D["pick"]["fp"] if D.get("pick") else None, calibration_rounds=D["rerun"].get("calibration_rounds"))
    r["join deaths, where"] = dict(collections.Counter(c.get("where") for c in D["every"] if c["cause"] and "join" in c["cause"]).most_common())
    r["limit deaths, by limit"] = dict(collections.Counter(x for c in D["every"] if c["cause"] and "limits" in c["cause"] for x in (c.get("hard") or []) + (c.get("soft") or [])).most_common())
    SEC = collections.defaultdict(list); P604 = collections.defaultdict(list); M604 = collections.defaultdict(lambda: collections.defaultdict(list))
    L602 = collections.defaultdict(lambda: collections.defaultdict(list)); D602 = collections.Counter(); V603 = collections.defaultdict(list)
    SPN = collections.defaultdict(list); GS = collections.defaultdict(collections.Counter); KX = collections.defaultdict(lambda: collections.defaultdict(float)); LN = []
    CL = collections.defaultdict(lambda: [0, 0, 0, 0])
    for b in A:
        ns = nts(b); kinds = b["kinds"]
        for s_ in ("Verse 1", "Chorus 1"):
            N_ = E.win_N(ns, E.BAR0[s_])
            if not N_: continue
            x_, f_ = xvec(N_)
            if not f_: continue
            sc_ = float(J["intercept"] + W @ ((x_ - MU) / SD)); bd_ = E.kband(f_["notes_per_bar"]); rel_ = sc_ - KB557[bd_][1]
            SEC[s_].append((rel_, sc_ < KB557[bd_][2], f_["notes_per_bar"], bd_))
            cm_ = W * ((x_ - MU) / SD - ZB[bd_])                                         # each measure's part of the score less the band's kept mean
            ns2_ = [n for n in ns if kinds.get((n["sec"], int(n["line"].split(":")[1]))) != "design"]
            des_ = 0.0; dm_ = np.zeros(len(MS))
            if len(ns2_) < len(ns) and any(E.BAR0[s_] * BAR <= n["on"] < (E.BAR0[s_] + 8) * BAR and kinds.get((n["sec"], int(n["line"].split(":")[1]))) == "design" for n in ns):
                N2_ = E.win_N(ns2_, E.BAR0[s_]); x2_, _ = xvec(N2_)
                for m in FORM: x2_[MS.index(m)] = x_[MS.index(m)]
                dm_ = W * ((x_ - x2_) / SD); des_ = float(dm_.sum())
            form_ = float(sum(cm_[MS.index(m)] for m in FORM)); P604[s_].append((rel_, des_, form_, rel_ - des_ - form_, float(cm_.sum())))
            for k, m in enumerate(MS): M604[s_][m].append((cm_[k], dm_[k]))
            # 602: the window's last note
            ln_ = max([n for n in ns if E.BAR0[s_] * BAR <= n["on"] < (E.BAR0[s_] + 8) * BAR], key=lambda n: n["on"])
            kl_ = kinds.get((ln_["sec"], int(ln_["line"].split(":")[1])))
            c_ = C2[ln_["on"] // (BAR // 2)].split("/")[0]; inch_ = E.ETON in E.M.CH[c_][1]
            if kl_ == "design": D602[s_] += 1
            else: L602[s_]["tonic in the chord" if inch_ else "tonic not in the chord"].append(ln_["p"] % 12 == E.ETON)
            if s_ == "Verse 1": V603["past_fifth"].append(f_["past_fifth"]); V603["mean_interval"].append(f_["mean_interval"])
        byl = collections.defaultdict(list)
        for n in ns: byl[n["line"]].append(n["on"])
        for s in E.SUNG:
            for i in range(len(E.LINES[s])):
                o = sorted(byl.get(f"{s}:{i}", []))
                if len(o) < 2: continue
                nb_ = E.slot_len(s, i); c6_ = E.cell600(len(o) / nb_); kd_ = kinds.get((s, i)); g = [y - x for x, y in zip(o, o[1:])]
                if kd_ in DRAWN and nb_ == 2: SPN[c6_].append((o[-1] - o[0]) / (nb_ * BAR))
                chor_ = s.startswith("Chorus") or s in ("Last Chorus", "Tag")
                if kd_ != "design" and (kd_ in DRAWN or not chor_):                             # 590: the choruses on drawn lines; designed lines aside
                    for d in g: GS[s][GV.get(d, "other")] += 1
                    tab = CELL2[c6_]["gap values, shares"]
                    for k_ in ("sixteenth", "eighth", "quarter"): KX[s][k_] += tab[k_] * len(g)
                    KX[s]["n"] += len(g)
                if len(o) >= 9 and rate(o) >= 8: LN.append(longest(o))
                if i + 1 < len(E.LINES[s]) and len(o) >= 13 and nb_ == 2 and kd_ not in ("exact", "design", "both", "pitch"):
                    n_ = byl.get(f"{s}:{i + 1}")
                    if not n_: continue
                    kn = kinds.get((s, i + 1)); f0 = min(n_) - E.line_start(s, i + 1)
                    if not ((kn in DRAWN and not E.LINES[s][i + 1][0][1]) or f0 < 0): continue
                    k = min(3, min(n_) // BAR - max(o) // BAR); CL[rband(rate(o))][k] += 1; CL["all"][k] += 1
    r["557: by section"] = {s_: dict(rel=round(float(np.mean([x[0] for x in v])), 2), under5=round(float(np.mean([x[1] for x in v])), 3), npb=round(float(np.mean([x[2] for x in v])), 2)) for s_, v in SEC.items()}
    allw = [x for v in SEC.values() for x in v]
    r["557: both windows"] = dict(rel=round(float(np.mean([x[0] for x in allw])), 2), under5=round(float(np.mean([x[1] for x in allw])), 3))
    r["604: score less the band's kept mean in three parts (total, on designed lines, from the form, the rest; check: the measures' parts summed)"] = {s_: [round(float(np.mean([x[k] for x in v])), 2) for k in range(5)] for s_, v in P604.items()}
    r["604: costliest measures (points as a cost, of which on designed lines)"] = {s_: [(m, round(-float(np.mean([a for a, _ in v])), 2), round(-float(np.mean([d for _, d in v])), 2)) for m, v in sorted(mm.items(), key=lambda kv: float(np.mean([a for a, _ in kv[1]])))[:12]] for s_, mm in M604.items()}
    r["604: on designed lines, by measure (largest costs, then largest gains; points as a cost)"] = {s_: dict(costs=[(m, round(-float(np.mean([d for _, d in v])), 2)) for m, v in sorted(mm.items(), key=lambda kv: float(np.mean([d for _, d in kv[1]])))[:6]],
        gains=[(m, round(-float(np.mean([d for _, d in v])), 2)) for m, v in sorted(mm.items(), key=lambda kv: -float(np.mean([d for _, d in kv[1]])))[:6]]) for s_, mm in M604.items() if s_ != "Verse 1"}
    r["604: largest gains"] = {s_: [(m, round(-float(np.mean([a for a, _ in v])), 2)) for m, v in sorted(mm.items(), key=lambda kv: -float(np.mean([a for a, _ in kv[1]])))[:3]] for s_, mm in M604.items()}
    r["600: drawn lines' spans by cell (lines; 25th, 50th, 75th; kept)"] = {c: dict(lines=len(v), drawn=[round(float(np.percentile(v, q)), 3) for q in (25, 50, 75)], kept=CELL2[c]["first to last onset as a share of the slot: 25th, 50th, 75th"]) for c, v in sorted(SPN.items())}
    r["600: gap values by section (sixteenth, eighth, quarter: drawn / kept for the lines' cells; choruses on drawn lines)"] = {
        s: {k_: [round(GS[s][k_] / max(1, sum(GS[s].values())), 3), round(KX[s][k_] / max(1, KX[s]["n"]), 3)] for k_ in ("sixteenth", "eighth", "quarter")} for s in E.SUNG if GS[s]}
    r["600: dense lines' longest equal-gap run (50th, 75th, 90th, 95th; kept median 4)"] = dict(lines=len(LN), q=[float(np.percentile(LN, k)) for k in (50, 75, 90, 95)] if LN else None)
    r["601: class 0 by the rate as sung (lines, shares 0/1/2/3, kept class 0)"] = {k_: dict(lines=sum(c), shares=[round(x / max(1, sum(c)), 3) for x in c], kept=K579.get(k_, 0.517)) for k_, c in CL.items()}
    r["602: the window's last note on the tonic, by the chord under it (windows, share; kept 0.39 / 0.19); designed set aside"] = {
        s_: dict({k_: [len(v), round(float(np.mean(v)), 3)] for k_, v in d.items()}, designed=D602[s_]) for s_, d in L602.items()} | {s_: dict(designed=D602[s_]) for s_ in D602 if s_ not in L602}
    r["603: verse window, leaps past a fifth and mean interval (kept dense 0.02, 1.94)"] = {k_: round(float(np.mean(v)), 3) for k_, v in V603.items()}
    r["counts"] = dict(D["rerun"].get("v137_stats", {}))
    out[lab] = r
json.dump(out, open("/home/claude/p58/read/read_v137s.json", "w"), indent=1, default=str)
for lab, r in out.items():
    print("==", lab, r["runs"]["survivors"], r["runs"]["order"], r["runs"]["deaths"])
    for k, v in r.items():
        if k not in ("runs", "counts"): print("  ", k, json.dumps(v, default=str))
