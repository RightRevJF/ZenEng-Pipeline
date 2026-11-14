"""read_l2.py: Luthier v2 (630, 631, 633, 634) beside Luthier v1; adds the spans read to the next line's first onset, the dense lines' downbeat share, and 635's split. Built on read_l1.py (Luthier v1 (605, 606; 607 and 608 read here) beside v137, and v137's tests again. Built on read_v137.py: song 48 on v137 (600, 601, 602, 603) beside v136, main and control, the judge not refitted.
- 600: drawn lines' spans (first to last onset over the slot) at the kept quartiles of their cell (notes over the slot's bars); each section's
  sixteenths, eighths and quarters beside the kept shares for its lines' cells (the chorus on drawn lines, 590); the dense lines' longest run.
- 601: reachable drawn lines of 13 notes and over in two-bar slots, class 0 by the rate as sung.
- 602: the window's last note on the tonic by the chord under it (kept 39% where the tonic is a chord tone, 19% where not); designed lines
  set aside and counted.
- 603: the verse window's leaps past a fifth and mean interval (kept dense 2%, 1.94).
- 604: each section's score less the band's kept mean in three parts: on designed lines (the window scored without them, the form's two
  measures held), following from the form (empty bars, notes a bar), and the rest; with the costliest measures.
- 557 by section, survivors, deaths, counts.
Usage: python3 read_v137.py  ->  read/read_v137.json"""
import sys, io, contextlib, json, pickle, collections
import numpy as np
sys.argv = ["x", "10", "main"]; sys.path.insert(0, "/home/claude/p58")
with contextlib.redirect_stdout(io.StringIO()): import melody_l2_p58 as E
BAR, BEAT = E.BAR, E.BEAT
RUNS = {"l2 main": "/home/claude/p58/runl2/melody_l2_p58_main.pkl", "l2 ctl": "/home/claude/p58/runl2/melody_l2_p58_ctl.pkl",
        "l1 main": "/home/claude/p58/runl1/melody_l1_p58_main.pkl", "l1 ctl": "/home/claude/p58/runl1/melody_l1_p58_ctl.pkl"}
import luthier_read as LR
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
PICKS = {}
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
    # 607: the layout read (every complete build); the survivors' gains kept for the pick
    RC = collections.defaultdict(list); RJc = collections.defaultdict(list); G7 = {}; SV = collections.defaultdict(list)
    for b in A:
        ns7 = [dict(on=o, p=p, sec=s_) for o, d, p, s_, l, st, sy in b["notes"]]
        for k_, v_ in LR.recurrence(ns7).items():
            if v_[0] is not None: RC[k_].append(v_[0]); RJc[k_].append(v_[1])
        G7[b["fp"]] = LR.coupling_gain(ns7)
        for w_, (g_, i_) in LR.saved_both(ns7).items(): SV[w_].append((g_[0], g_[1], i_[0], i_[1]))
    gs7 = [g for g in G7.values() if g is not None]
    r["607: recurrence within sections (exactly the same; Jaccard 0.6 or more), by bars apart; kept beside"] = {k_: [round(float(np.mean(RC[k_])), 3), round(float(np.mean(RJc[k_])), 3),
        LR.T["605: kept bar-rhythm recurrence within a section, by bars apart"][str(k_)]["exactly the same rhythm, share of pairs (songs' mean)"], LR.T["605: kept bar-rhythm recurrence within a section, by bars apart"][str(k_)]["pairs with Jaccard 0.6 or more"]] for k_ in sorted(RC)}
    r["607: coupling gain, bits a bar (mean; 25th, 50th, 75th; kept held out 0.16)"] = [round(float(np.mean(gs7)), 3), [round(float(x), 3) for x in np.percentile(gs7, [25, 50, 75])]]
    r["607: bits saved on the second half (w: corpus bits a gap, saved a gap, corpus bits an interval, saved an interval; kept 0.29 and 0.18 at 0.85)"] = {w_: [round(float(x), 3) for x in np.mean(v_, axis=0)] for w_, v_ in SV.items()}
    alive_ = {a[0] for a in D["all_alive"]}; surv_ = [b for b in A if b["fp"] in alive_]
    PICKS[lab] = dict(pick_now=r["runs"]["pick"], survivors=[dict(fp=b["fp"], refit_combined=b["judge"]["refit_combined"], soft=bool(b.get("info", {}).get("soft")) if isinstance(b.get("info"), dict) else None, gain=G7.get(b["fp"])) for b in surv_])
    sg_ = [G7[b["fp"]] for b in surv_ if G7.get(b["fp"]) is not None]
    r["607: survivors' coupling gain (n; share at or over 0, 0.1, 0.16; the pick's own)"] = [len(sg_), round(float(np.mean(np.array(sg_) >= 0)), 3), round(float(np.mean(np.array(sg_) >= 0.1)), 3), round(float(np.mean(np.array(sg_) >= 0.16)), 3), round(G7.get(r["runs"]["pick"]) or float("nan"), 3)]
    # 631: spans read to the next line's first onset (the kept reading), and whether dense lines begin on their downbeat; 635: classes by kind
    SP2 = collections.defaultdict(list); DB = collections.defaultdict(list); BRx = collections.defaultdict(list); CL5 = collections.defaultdict(lambda: [0, 0, 0, 0])
    for b in A:
        byl = collections.defaultdict(list)
        for o, d, p, s_, l, st, sy in b["notes"]: byl[l].append(o)
        for l, v in byl.items():
            s_, i_ = l.split(":"); i_ = int(i_); v.sort(); n_ = byl.get(f"{s_}:{i_ + 1}"); kd_ = b["kinds"].get((s_, i_))
            if E.slot_len(s_, i_) != 2 or kd_ not in DRAWN: continue
            c6_ = E.cell600(len(v) / 2)
            DB[c6_].append(v[0] == E.line_start(s_, i_))
            if n_:
                sl_ = min(n_) - v[0]
                if 72 < sl_ <= 120: SP2[c6_].append((v[-1] - v[0]) / sl_); BRx[c6_].append(min(n_) - v[-1])
            if n_ and len(v) >= 13:
                kn = b["kinds"].get((s_, i_ + 1)); f0 = min(n_) - E.line_start(s_, i_ + 1)
                if (kn in DRAWN and not E.LINES[s_][i_ + 1][0][1]) or f0 < 0:
                    tpl_ = (E.line_start(s_, i_) - E.BAR0[s_] * BAR) < 4 * BAR
                    grp_ = "template lines (the section's first four bars)" if tpl_ else ("lines that follow no template" if kd_ == "fresh" else "lines on copied bars")
                    CL5[(grp_, rband(rate(v)))][min(3, min(n_) // BAR - max(v) // BAR)] += 1
    KB2 = json.load(open("/home/claude/p58/tables/luthier_v2_tables.json"))["610/618: kept lines in two-bar slots, by notes over the slot's bars: the breath, last onset of the line to first onset of the next, in twelfths of a beat (18 = a dotted quarter): lines; 10th, 25th, 50th, 75th percentile; share under 18; share of lines beginning before their bar line or after beat 1 (not on the downbeat)"]
    r["631: spans to the next line's first onset by cell (lines; 25th, 50th, 75th; kept)"] = {c: dict(lines=len(v), drawn=[round(float(np.percentile(v, q)), 3) for q in (25, 50, 75)], kept=CELL2[c]["first to last onset as a share of the slot: 25th, 50th, 75th"]) for c, v in sorted(SP2.items()) if len(v) > 30}
    r["631: breaths by cell (10th, 25th, 50th, 75th; kept)"] = {c: [[round(float(np.percentile(v, q)), 1) for q in (10, 25, 50, 75)], KB2[c][1:5]] for c, v in sorted(BRx.items()) if len(v) > 30}
    r["631: drawn lines beginning on their downbeat, by cell (share; kept)"] = {c: [round(float(np.mean(v)), 3), round(1 - KB2[c][6], 3)] for c, v in sorted(DB.items()) if len(v) > 30}
    r["635: class 0 by group and the rate as sung (lines, share 0; kept)"] = {f"{g_} | {rb_}": [sum(c), round(c[0] / max(1, sum(c)), 3), K579[rb_]] for (g_, rb_), c in sorted(CL5.items())}
    r["630"] = D["rerun"].get("pick630")
    r["counts"] = dict(D["rerun"].get("l2_stats", D["rerun"].get("l1_stats", {})))
    r["605: the template's rate (calibrated)"] = D["rerun"].get("tp605")
    r["605: calibration rounds (kept, read, rate)"] = [row.get("605 (kept, unaimed reading, rate)") for row in D["calibration"]]
    out[lab] = r
json.dump(out, open("/home/claude/p58/read/read_l2.json", "w"), indent=1, default=str)
json.dump(PICKS, open("/home/claude/p58/read/l2_pick_candidates.json", "w"), indent=1, default=str)
for lab, r in out.items():
    print("==", lab, r["runs"]["survivors"], r["runs"]["order"], r["runs"]["deaths"])
    for k, v in r.items():
        if k not in ("runs", "counts"): print("  ", k, json.dumps(v, default=str))
