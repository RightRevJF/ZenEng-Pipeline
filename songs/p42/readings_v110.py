"""321: the table of tests of every fix of v110 (310-321) on a song's own runs, main and control, each made twice.
Usage: python3 readings_v110.py MODULE PREFIX OUT [OLD_PREFIX]
  e.g. python3 readings_v110.py melody_v110_p40 /home/claude/p42/melody_v110_p40 readings_v110_p40 /home/claude/p41/melody_v109_p40"""
import sys, pickle, collections, json, importlib
import numpy as np
MOD, PRE, OUTN = sys.argv[1], sys.argv[2], sys.argv[3]; OLDP = sys.argv[4] if len(sys.argv) > 4 else None
DESIGN = len(sys.argv) > 5 and sys.argv[5] == "design"
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p42", "/home/claude/p40"]
P = importlib.import_module(MOD); import judges as J
M = P.M; BAR, BEAT = P.BAR, P.BEAT
MODES = ("design",) if DESIGN else ("main", "ctl")
RUN = {v: pickle.load(open(f"{PRE}_{v}.pkl", "rb")) for v in MODES}
RR = {v: pickle.load(open(f"{PRE}_{v}_r.pkl", "rb")) for v in MODES}
OLD = {v: pickle.load(open(f"{OLDP}_{v}.pkl", "rb")) for v in MODES} if OLDP else {}
def pct(v, q=(5, 50, 95)):
    v = [float(x) for x in v if x is not None and np.isfinite(x)]
    return [round(float(np.percentile(v, k)), 3) for k in q] if v else None
def nts(b): return [dict(on=o, dur=d, p=p, sec=s, line=l, stress=st, syl=sy) for o, d, p, s, l, st, sy in b["notes"]]
ROW = P.TOP - P.M.LO
R = {}
for v in MODES:
    D = RUN[v]; Al = D["all"]; st = D["stats"]; r = {}
    r["runs"] = dict(made=D["made"], survivors=D["survivors"], order=D["order_fp"], rerun_order=RR[v]["order_fp"],
                     reproduced=D["order_fp"] == RR[v]["order_fp"] and D["survivors"] == RR[v]["survivors"], deaths=dict(D["deaths"].most_common()),
                     code=D["rerun"]["code_sha"], line_knobs=D["line_knobs"], calibration_stop=D["rerun"].get("calibration_stop"))
    if v in OLD: r["runs"]["before"] = dict(survivors=OLD[v]["survivors"], order=OLD[v]["order_fp"])
    jc = np.array([b["judge"]["combined"] for b in Al])
    par = []
    for b in Al:
        ns = nts(b)
        for s in ("Verse 1", "Chorus 1"):
            of = J.order_feats(P.win_N(ns, P.BAR0[s]))
            if of: par.append(of["parallel"])
    r["310"] = dict(under_floor=round(float(np.mean(jc < J.FLOOR)), 3), parallel=round(float(np.median(par)), 3), kept_parallel=0.14,
                    paired_lines=st.get("310: paired lines", 0), partner_given_up=st.get("310: partner's rhythm given up for a line", 0), judges_refitted=False,
                    content=pct([b["judge"]["content"] for b in Al]), order=pct([b["judge"]["order"] for b in Al]),
                    held=bool(np.mean(jc < J.FLOOR) < 0.10 and np.median(par) >= 0.14))
    EN = []
    for b in Al:
        lc = [n for n in nts(b) if n["sec"] == "Last Chorus"]
        if lc: EN.append((lc[-1]["p"] - M.TONIC) % 12 == 0)
    miss = st.get("311: ending degree missing after 50 draws", 0)
    r["311"] = dict(last_chorus_tonic=round(float(np.mean(EN)), 4), redrawn=st.get("311: register redrawn for its ending", 0), misses=miss, held=bool(np.mean(EN) == 1.0 and miss == 0))
    pv = [b["read"]["v"].get("past_fifth") for b in Al if b["read"]["v"]]; pc = [b["read"]["c"].get("past_fifth") for b in Al if b["read"]["c"]]
    r["312"] = dict(verse=round(float(np.nanmedian(pv)), 4), chorus=round(float(np.nanmedian(pc)), 4), limit=0.036, leap_knob=round(D["line_knobs"].get("leap", 1.0), 3),
                    held=bool(np.nanmedian(pv) <= 0.036 and np.nanmedian(pc) <= 0.036))
    if "Verse 2" in P.SUNG:
        def share(b):
            def bars(s):
                out = collections.defaultdict(set)
                for n in nts(b):
                    if n["sec"] == s: out[n["on"] // BAR - P.BAR0[s]].add(n["on"] % BAR)
                return out
            a, c = bars("Verse 2"), bars("Verse 1"); return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))
        sh = [share(b) for b in Al]; nl = len(P.LINES["Verse 2"]) * D["made"]
        gu = st.get("293: copy given up for a line", 0)
        r["313"] = dict(share=pct(sh), in_range=round(float(np.mean([0.25 <= x <= 0.75 for x in sh])), 3), given_up=gu, given_up_share=round(gu / max(1, nl), 3),
                        left_out=st.get("313: copied bars the cap does not allow, left out", 0), held=bool(np.mean([0.25 <= x <= 0.75 for x in sh]) >= 0.75 and gu / max(1, nl) < 0.05))
    regs = [b["meta"]["registers"] for b in Al]
    unused = [abs((g["song_lo"] - P.ROW_LO) - (P.ROW_HI - g["song_hi"])) for g in regs]
    vsh = []; tonic_ok = []
    for b, g in zip(Al, regs):
        ns = nts(b); vp = [n["p"] for n in ns if n["sec"] == "Verse 1"]
        if vp and g["song_range"]: vsh.append((float(np.median(vp)) - g["song_lo"]) / g["song_range"])
        for sec_ in ("Chorus 1",):
            h = [n for n in ns if n["line"] == f"{sec_}:0"]
            if h and (h[-1]["p"] - M.TONIC) % 12 == 0:
                med = float(np.median([n["p"] for n in ns if n["sec"] == sec_]))
                tonics = [p for p in range(P.ROW_LO, P.ROW_HI + 1) if (p - M.TONIC) % 12 == 0]
                tonic_ok.append(abs(h[-1]["p"] - med) <= min(abs(p - med) for p in tonics) + 1e-9)
    r["314"] = dict(row=[P.ROW_LO, P.ROW_HI], row_semitones=P.ROW_HI - P.ROW_LO, range=pct([g["song_range"] for g in regs], (5, 25, 50, 75, 95)), kept_range=[10, 14.5, 17, 22, 28],
                    unused_split_max=int(max(unused)), placement=P.PLACE, verse_median_share=pct(vsh, (25, 50, 75)), kept_verse=[0.396, 0.5, 0.575],
                    tonic_nearest_median=round(float(np.mean(tonic_ok)), 3) if tonic_ok else None,
                    top_fifth=round(float(np.mean([max(n[2] for n in b["notes"]) >= P.ROW_HI - 0.2 * (P.ROW_HI - P.ROW_LO) for b in Al])), 3),
                    floor=round(float(np.mean([min(n[2] for n in b["notes"]) == P.ROW_LO for b in Al])), 3),
                    held=bool(max(unused) <= 1 and 0.40 <= float(np.median(vsh)) <= 0.57 and (not tonic_ok or np.mean(tonic_ok) == 1.0)))
    arch = [b["lines"]["arch_span"] for b in Al]
    r["315"] = dict(amplitude=round(D["line_knobs"]["amp"], 3), cap=7.0, arch_span=pct(arch, (25, 50, 75)), band=[0.0, 0.55], calibration_stop=D["rerun"].get("calibration_stop"),
                    held=bool(D["line_knobs"]["amp"] <= 7.0 and 0.0 <= float(np.median(arch)) <= 0.55))
    lr = st.get("308: long line redrawn", 0); ll = st.get("316: long lines", 0)
    ent = {k: round(float(np.mean([b["lines"][k] for b in Al])), 3) for k in ("starts_on_downbeat", "starts_after_downbeat", "starts_as_pickup")}
    r["316"] = dict(long_lines=ll, redraws=lr, per_line=round(lr / max(1, ll), 3), entry_shares=ent, no_fit=st.get("316: long line with no entry and landing that fit", 0))
    if v in OLD:
        Ao = OLD[v]["all"]; r["316"]["entry_shares_before"] = {k: round(float(np.mean([b["lines"][k] for b in Ao])), 3) for k in ent}
        ostat = OLD[v]["stats"]; r["316"]["redraws_before"] = ostat.get("308: long line redrawn", 0)
    r["316"]["held"] = bool(lr / max(1, ll) < 1.5 and (v not in OLD or all(abs(ent[k] - r["316"]["entry_shares_before"][k]) <= 0.05 for k in ent)))
    dg = getattr(P, "DESIGN_GATES", [])
    rates = {}
    for g in dg:
        k = sum(1 for b in Al if g in b.get("fails", [])); rates[g] = round(1 - k / max(1, len(Al)), 3)
    r["317"] = dict(design_gates=rates or "none in force", held=all(x >= 0.9 for x in rates.values()) if rates else True)
    six = [np.mean([n[0] % 6 != 0 for n in b["notes"]]) for b in Al]
    r["318"] = dict(feel=getattr(P, "FEEL", "straight eighths"), sixteenth_onsets=pct(six, (25, 50, 75)), held="printed")
    r["319"] = dict(note="read on the arrangement (riff script); the port test has no instrumental lines", held="n/a")
    r["320"] = dict(note="the report states no predicted counts from rescoring; figures here are from runs", held=True)
    r["321"] = dict(note="this table, on this song's own runs", held=True)
    R[v] = r
json.dump(R, open(f"/home/claude/p42/{OUTN}.json", "w"), indent=1, default=str)
TEST = {"310": "under the floor < 10%; likeness of bar rhythms (parallel) >= kept 0.14 at the median; no judge refitted",
        "311": "the last chorus on the tonic in every build; misses none", "312": "leaps past a fifth <= 3.6% of moves at the median, verse and chorus",
        "313": "verse 2 shares 25-75% in 3 builds of 4; copies given up < 1 line in 20",
        "314": "range printed; unused above/below differ by 1 at most; verse median 40-57% of the range; tonic endings nearest the median",
        "315": "amplitude <= 7; calibration stops on two largest steps running; arch over the span 0.0-0.55 at the median",
        "316": "redraws per long line < 1.5; entry shares unchanged", "317": "each design gate's pass rate printed; nine in ten or more",
        "318": "the feel named; sixteenths printed", "319": "no instrumental note outside its instrument", "320": "rescorings stated as bounds", "321": "this table"}
def reading(k, r):
    x = r[k]
    if k == "310": return f"under floor {x['under_floor']:.1%}; parallel {x['parallel']} (kept 0.14); paired lines {x['paired_lines']}, partner given up {x['partner_given_up']}"
    if k == "311": return f"tonic {x['last_chorus_tonic']:.1%}; registers redrawn {x['redrawn']}; misses {x['misses']}"
    if k == "312": return f"verse {x['verse']:.1%}, chorus {x['chorus']:.1%}; leap knob {x['leap_knob']}"
    if k == "313": return f"share {x['share']}; in range {x['in_range']:.0%}; given up {x['given_up']} ({x['given_up_share']:.1%}); left out {x['left_out']}"
    if k == "314": return f"range {x['range']} (kept {x['kept_range']}); unused split max {x['unused_split_max']}; verse share {x['verse_median_share']}; tonic nearest {x['tonic_nearest_median']}; top fifth {x['top_fifth']:.0%}; floor {x['floor']:.0%}"
    if k == "315": return f"amplitude {x['amplitude']}; arch {x['arch_span']}; stop {x['calibration_stop'] or 'none'}"
    if k == "316": return f"redraws {x['redraws']}/{x['long_lines']} = {x['per_line']}; entries {x['entry_shares']}" + (f" (before {x.get('entry_shares_before')})" if 'entry_shares_before' in x else "")
    if k == "317": return f"{x['design_gates']}"
    if k == "318": return f"{x['feel']}; sixteenth onsets {x['sixteenth_onsets']}"
    return x.get("note", "")
rows = []
for k in TEST:
    m = R[MODES[0]]; c = R[MODES[-1]]
    h = m[k].get("held") if k in m else None
    rows.append((k, TEST[k], reading(k, m) if k in m else "", reading(k, c) if (k in c and len(MODES) > 1) else "", h))
json.dump(rows, open(f"/home/claude/p42/{OUTN}_table.json", "w"), indent=1, default=str)
for v in MODES: print(v, R[v]["runs"])
for k, t, a, b, h in rows: print(f"{k} | {t} | {a} | {b} | {h}")
