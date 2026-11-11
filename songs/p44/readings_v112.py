"""321: the table of tests of 310-336 on a song's own runs, main and control, each made twice, as v112 reads them: 335, every test
named against its kept figure or marked a reading (or a check of a rule); 336, the floor's share a reading with the judges' readings.
Usage: python3 readings_v112.py MODULE PREFIX OUT [OLD_PREFIX]
  e.g. python3 readings_v112.py melody_v112_p40 /home/claude/p44/melody_v112_p40 readings_v112_p40 /home/claude/p43/melody_v111_p40"""
import sys, pickle, collections, json, importlib
import numpy as np
MOD, PRE, OUTN = sys.argv[1], sys.argv[2], sys.argv[3]; OLDP = sys.argv[4] if len(sys.argv) > 4 else None
DESIGN = len(sys.argv) > 5 and sys.argv[5] == "design"
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p44", "/home/claude/p43", "/home/claude/p42", "/home/claude/p40"]
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
    r["319"] = dict(note="read on the arrangement; these runs make no instrumental lines", held="n/a")
    r["320"] = dict(note="the report states no predicted counts from rescoring; figures here are from runs", held=True)
    r["321"] = dict(note="this table, on this song's own runs", held=True)
    # ---- v111 ----
    pg = st.get("310: partner's rhythm given up for a line", 0) + st.get("322: partner's stresses given up for a line", 0) + st.get("330: partner given up after its stresses", 0); pl = st.get("310: paired lines", 0)
    r["322"] = dict(paired_lines=pl, of_another_length=st.get("322: paired lines of another length", 0), stresses_kept=st.get("322: partner's stresses kept", 0),
                    given_up=pg, given_up_share=round(pg / max(1, pl), 3), parallel=r["310"]["parallel"], under_floor=r["310"]["under_floor"],
                    held=bool(pg / max(1, pl) < 0.10 and r["310"]["parallel"] >= 0.14 and r["310"]["under_floor"] < 0.10))
    if "313" in r:
        r["323"] = dict(dropped=st.get("323: bar one onset over the cap, weakest onset dropped", 0), left_out=r["313"]["left_out"], in_range=r["313"]["in_range"], held=bool(r["313"]["in_range"] >= 0.75))
    te = []
    for b in Al:
        ns = nts(b)
        for t in b["meta"].get("tonic_endings", []):
            ln = [n for n in ns if n["line"] == t["line"]]
            if ln: te.append((t["line"], ln[-1]["p"] == t["nearest"]))
    r["324"] = dict(tonic_endings=len(te), on_nearest_to_centre=round(float(np.mean([x[1] for x in te])), 4) if te else None,
                    by_line={l: round(float(np.mean([x[1] for x in te if x[0] == l])), 4) for l in sorted({x[0] for x in te})}, held=bool(te and all(x[1] for x in te)))
    r["314"]["tonic_read_by_324"] = r["324"]["on_nearest_to_centre"]                      # 324 amends 314: the tonic test read on the drawn centre
    r["314"]["held"] = bool(r["314"]["unused_split_max"] <= 1 and 0.40 <= r["314"]["verse_median_share"][1] <= 0.57 and r["324"]["held"])
    dreg = {k: v for k, v in st.items() if k.startswith("325")}
    if dg:
        def reg_death(b):                                                  # a design failure for want of a note the registers could not hold
            ns = nts(b); h = [n for n in ns if n["line"] == "Chorus 1:0"]; lo = b["meta"]["registers"]["song_lo"]
            lowt = min(p for p in range(lo, lo + 12) if (p - M.TONIC) % 12 == 0); return bool(h) and h[-1]["p"] <= lowt
        rd = sum(1 for b in Al if any(g in b.get("fails", []) for g in dg) and reg_death(b))
        lt = [((([n for n in nts(b) if n["sec"] == "Last Chorus"] or [dict(p=-1)])[-1]["p"] - M.TONIC) % 12 == 0) for b in Al]
        r["325"] = dict(design_failures_for_the_registers=rd, last_chorus_tonic=round(float(np.mean(lt)), 4), redrawn=dreg, held=bool(rd == 0 and np.mean(lt) == 1.0))
    else:
        r["325"] = dict(design="none in force", last_chorus_tonic=r["311"]["last_chorus_tonic"], redrawn=dreg, held=bool(r["311"]["last_chorus_tonic"] == 1.0))
    r["326"] = dict(design_gates=r["317"]["design_gates"], held=r["317"]["held"])
    jd = D["deaths"].get("join: no held end and breath before the copy (212)", 0)
    r["327"] = dict(join_copy_deaths=jd, v109=92, refits={k: v for k, v in st.items() if k.startswith("327")}, held=bool(jd <= 92))
    BANDS = [(0, 80, "under 80", 0.34, [0.26, 0.43]), (80, 100, "80-100", 0.21, None), (100, 120, "100-120", 0.12, None), (120, 140, "120-140", 0.02, None), (140, 999, "over 140", 0.0, None)]
    bd = next(x for x in BANDS if x[0] <= M.QBPM < x[1])
    r["328"] = dict(tempo=M.QBPM, band=bd[2], kept_median=bd[3], kept_quartiles=bd[4] or "not given in the paper's text (Table DQ's file not attached)",
                    song_share=r["318"]["sixteenth_onsets"], held="printed")
    srn = [max(n[2] for n in b["notes"]) - min(n[2] for n in b["notes"]) for b in Al]; drn = [b["meta"]["registers"]["song_range"] for b in Al]
    gap = [d - x for d, x in zip(drn, srn)]
    cw = [b["read"]["c"]["range"] for b in Al if b["read"]["c"]]; vw = [b["read"]["v"]["range"] for b in Al if b["read"]["v"]]
    ga = collections.defaultdict(list)
    for b in Al:
        for w in ("v", "c"):
            if b["read"][w]:
                for m_, x in J.give_away(b["read"][w], k=999): ga[m_].append(x)
    heavy = sorted(((m_, float(np.median(x))) for m_, x in ga.items()), key=lambda y: y[1])[:5]
    car = [b["meta"].get("carriers") for b in Al]
    def sung_ext(b, which):
        c_ = b["meta"].get("carriers", {}).get(which)
        if not c_ or not c_[0]: return None
        (sec_, j), x = c_; return any(n[2] == x for n in b["notes"] if n[4] == f"{sec_}:{j}")
    r["329"] = dict(sung_range=pct(srn, (25, 50, 75)), drawn_range=pct(drn, (25, 50, 75)), drawn_minus_sung=pct(gap, (25, 50, 75)),
                    chorus_window_range=pct(cw, (25, 50, 75)), verse_window_range=pct(vw, (25, 50, 75)), kept_window=[8, 10, 13],
                    heaviest_give_aways=[(m_, round(x, 3)) for m_, x in heavy], low_extreme_sung=round(float(np.mean([x for x in (sung_ext(b, "low") for b in Al) if x is not None])), 3),
                    high_extreme_sung=round(float(np.mean([x for x in (sung_ext(b, "high") for b in Al) if x is not None])), 3),
                    widened=st.get("329: a section's register widened", 0), dropped=st.get("329: extreme dropped after six tries", 0),
                    held=bool(np.median(gap) <= 2 and np.median(cw) >= 10 and "range" not in [m_ for m_, _ in heavy]))
    def dq(Dx):
        A = Dx["all"]; jc_ = np.array([b["judge"]["combined"] for b in A]); par_ = []
        for b in A:
            ns = nts(b)
            for s in ("Verse 1", "Chorus 1"):
                of = J.order_feats(P.win_N(ns, P.BAR0[s]))
                if of: par_.append(of["parallel"])
        pv_ = [b["read"]["v"].get("past_fifth") for b in A if b["read"]["v"]]
        return {"survivors of 1,000": Dx["survivors"], "builds under the judge's floor": round(float(np.mean(jc_ < J.FLOOR)), 3),
                "content judge, median": round(float(np.median([b["judge"]["content"] for b in A])), 2), "order judge, median": round(float(np.median([b["judge"]["order"] for b in A])), 2),
                "likeness of bar rhythms between lines": round(float(np.median(par_)), 3), "contour amplitude": round(Dx["line_knobs"]["amp"], 1),
                "arch term over the line's span": round(float(np.median([b["lines"]["arch_span"] for b in A])), 2),
                "leaps past a fifth, verse, % of moves": round(100 * float(np.nanmedian(pv_)), 1),
                "the song's sung range, semitones": float(np.median([max(n[2] for n in b["notes"]) - min(n[2] for n in b["notes"]) for b in A])),
                "range in eight bars, verse / chorus": f"{np.median([b['read']['v']['range'] for b in A if b['read']['v']]):.0f} / {np.median([b['read']['c']['range'] for b in A if b['read']['c']]):.0f}",
                "builds that touch the row's floor": round(float(np.mean([min(n[2] for n in b["notes"]) == P.ROW_LO for b in A])), 3),
                "builds that use the row's top fifth": round(float(np.mean([max(n[2] for n in b["notes"]) >= P.ROW_HI - 0.2 * (P.ROW_HI - P.ROW_LO) for b in A])), 3)}
    r["DQ"] = dict(now=dq(D), before=dq(OLD[v]) if v in OLD else None)
    # ---- v112: 335's restatements ----
    LIK = (0.04, 0.23); V2 = (0.25, 0.70)
    r["310"]["held"] = bool(LIK[0] <= r["310"]["parallel"] <= LIK[1])
    r["322"]["held"] = r["310"]["held"]
    if "313" in r:
        r["313"]["held"] = bool(V2[0] <= r["313"]["share"][1] <= V2[1]); r["323"]["held"] = r["313"]["held"]
    r["316"]["held"] = "reading"; r["327"]["held"] = "reading"
    cwm = r["329"]["chorus_window_range"][1]
    r["329"]["held"] = bool(r["329"]["drawn_minus_sung"][1] <= 2 and 8 <= cwm <= 13 and "range" not in [m_ for m_, _ in r["329"]["heaviest_give_aways"]])
    r["330"] = dict(parallel=r["310"]["parallel"], kept=LIK, copy_failed_stresses_kept=st.get("330: copy failed, partner's stresses kept", 0),
                    given_up_after_stresses=st.get("330: partner given up after its stresses", 0), partners_given_up=r["322"]["given_up"], given_up_share=r["322"]["given_up_share"],
                    held=r["310"]["held"])
    if "313" in r:
        r["331"] = dict(rate=D["rerun"].get("rate293"), calibration=[x.get("293 rate") for x in D["calibration"]], share=r["313"]["share"], kept=[0.25, 0.50, 0.70], held=r["313"]["held"])
    kwd = D["deaths"].get("key word on a chord tone (134; 279)", 0); lim = {"main": 89, "ctl": 42}[v]
    r["332"] = dict(key_word_deaths=kwd, v110=lim, frozen=D["rerun"].get("frozen"), calibration_stop=D["rerun"].get("calibration_stop"),
                    held=bool(kwd <= lim and r["315"]["held"]) if "p40" in MOD else "reading")
    mr = max(g["song_range"] for g in regs)
    r["333"] = dict(row=ROW, row_less_two=ROW - 2, widest_drawn=mr, held=bool(mr <= ROW - 2 and r["329"]["held"]))
    QB = [(0, 80, "under 80", (0.26, 0.34, 0.43)), (80, 100, "80-100", (0.11, 0.21, 0.36)), (100, 120, "100-120", (0.04, 0.12, 0.27)), (120, 140, "120-140", (0.0, 0.02, 0.07)), (140, 999, "140 and over", (0.0, 0.0, 0.01))]
    bq = next(x for x in QB if x[0] <= M.QBPM < x[1])
    r["334"] = dict(tempo=M.QBPM, band=bq[2], kept_quartiles=bq[3], song=r["318"]["sixteenth_onsets"], held="printed")
    r["328"]["kept_quartiles"] = bq[3]
    KQ = J._J["kept percentiles, held out (log-odds)"]
    jc_ = np.array([b["judge"]["content"] for b in Al]); jo_ = np.array([b["judge"]["order"] for b in Al])
    kmh = {}
    for m_ in J.CJ["measures"]:
        col = np.array([row_[m_] for row_ in P.KRW if m_ in row_], float); col = col[np.isfinite(col)]
        if len(col): kmh[m_] = (float(np.percentile(col, 25)), float(np.percentile(col, 75)))
    outside = []
    for m_, (q1, q3) in kmh.items():
        vals = [b["read"][w].get(m_) for b in Al for w in ("v", "c") if b["read"][w] and b["read"][w].get(m_) is not None and np.isfinite(b["read"][w].get(m_))]
        if vals and not (q1 <= float(np.median(vals)) <= q3): outside.append(m_)
    r["336"] = dict(under_floor=r["310"]["under_floor"], floor=J.FLOOR,
                    content=dict(median=round(float(np.median(jc_)), 2), at_kept_25th=round(float(np.mean(jc_ >= KQ["content"]["25"])), 3), at_kept_median=round(float(np.mean(jc_ >= KQ["content"]["50"])), 3), kept=(KQ["content"]["25"], KQ["content"]["50"])),
                    order=dict(median=round(float(np.median(jo_)), 2), at_kept_25th=round(float(np.mean(jo_ >= KQ["order"]["25"])), 3), at_kept_median=round(float(np.mean(jo_ >= KQ["order"]["50"])), 3), kept=(KQ["order"]["25"], KQ["order"]["50"])),
                    content_measures=len(kmh), outside_kept_middle_half=len(outside), outside=outside,
                    heaviest_give_away=r["329"]["heaviest_give_aways"][0], held="reading")
    r["335"] = dict(note="every row names its kept figure, or is marked a reading or a check of the rule's own statement", held=True)
    R[v] = r
json.dump(R, open(f"/home/claude/p44/{OUTN}.json", "w"), indent=1, default=str)
TEST = {"310": ("likeness of bar rhythms between lines inside the kept middle half at the median (335); the floor's share a reading (336)", "kept 0.04-0.23"),
        "311": ("the last chorus on the tonic in every build; misses none", "the rule's own statement (a check)"),
        "312": ("leaps past a fifth at or under the kept 75th at the median, verse and chorus", "kept 75th 3.6%"),
        "313": ("verse 2's share of verse 1's bar rhythms inside the kept middle half at the median (335)", "kept 25-70% (median 50%)"),
        "314": ("unused semitones split within 1; verse median inside the kept share; tonic endings nearest the centre (324)", "kept verse share 40-57%; the rule (a check)"),
        "315": ("amplitude at or under 7; arch over the span inside the kept middle half at the median", "kept 0.00-0.55; the cap (a check)"),
        "316": ("redraws per long line and entry shares", "a reading (335: tries and redraws)"),
        "317": ("each design gate's pass rate", "the paper's 317: nine in ten"),
        "318": ("the feel named; sixteenths printed", "a reading"), "319": ("no instrumental note outside its instrument", "n/a here"),
        "320": ("rescorings stated as bounds", "a check"), "321": ("this table", "a check"),
        "322": ("as 310 (335)", "kept 0.04-0.23"), "323": ("as 313 (335)", "kept 25-70%"),
        "324": ("every tonic ending on the tonic nearest the centre of its section's drawn register", "the rule's own statement (a check)"),
        "325": ("no design death for want of a note the registers hold; the last chorus on the tonic in every complete build", "the rule's own statement (a check)"),
        "326": ("nine builds in ten pass each design gate", "the paper's 317"),
        "327": ("deaths at the breath before a copy", "a reading (335: a count kept songs do not have)"),
        "328": ("the sixteenth share beside its band", "a reading"),
        "329": ("sung range within 2 of the drawn; chorus window range inside the kept middle half (335); range not among the five heaviest give-aways", "kept 8-13; the rule (a check)"),
        "330": ("likeness inside the kept middle half at the median; partners given up printed", "kept 0.04-0.23"),
        "331": ("verse 2's share inside 25-70% at the median, main and control", "kept 25-70% (median 50%)"),
        "332": ("song 40: key-word deaths at or under v110's 89 (main) and 42 (control); 315's tests held", "v110's counts (the paper's test)"),
        "333": ("329's tests held; no drawn range wider than the row less two", "the rule's own statement (a check)"),
        "334": ("the sixteenth share beside its band's three quartiles", "a reading"), "335": ("every test names its kept figure or is marked a reading", "a check"),
        "336": ("the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half", "a reading")}
def reading(k, r):
    x = r[k]
    if k == "310": return f"under floor {x['under_floor']:.1%}; parallel {x['parallel']} (kept 0.14); paired lines {x['paired_lines']}, partner given up {x['partner_given_up']}"
    if k == "311": return f"tonic {x['last_chorus_tonic']:.1%}; registers redrawn {x['redrawn']}; misses {x['misses']}"
    if k == "312": return f"verse {x['verse']:.1%}, chorus {x['chorus']:.1%}; leap knob {x['leap_knob']}"
    if k == "313": return f"share {x['share']}; in range {x['in_range']:.0%}; given up {x['given_up']} ({x['given_up_share']:.1%}); left out {x['left_out']}"
    if k == "314": return f"range {x['range']} (kept {x['kept_range']}); unused split max {x['unused_split_max']}; verse share {x['verse_median_share']}; tonic nearest the sung median {x['tonic_nearest_median']}, the drawn centre {x.get('tonic_read_by_324')}; top fifth {x['top_fifth']:.0%}; floor {x['floor']:.0%}"
    if k == "315": return f"amplitude {x['amplitude']}; arch {x['arch_span']}; stop {x['calibration_stop'] or 'none'}"
    if k == "316": return f"redraws {x['redraws']}/{x['long_lines']} = {x['per_line']}; entries {x['entry_shares']}" + (f" (before {x.get('entry_shares_before')})" if 'entry_shares_before' in x else "")
    if k == "317": return f"{x['design_gates']}"
    if k == "318": return f"{x['feel']}; sixteenth onsets {x['sixteenth_onsets']}"
    if k == "330": return f"likeness {x['parallel']}; copies failed and the stresses kept {x['copy_failed_stresses_kept']}; given up after the stresses {x['given_up_after_stresses']}; partners given up {x['partners_given_up']} ({x['given_up_share']:.1%})"
    if k == "331": return f"rate {round(x['rate'], 3) if x['rate'] is not None else '-'}; verse 2 share {x['share']} (5th, median, 95th)"
    if k == "332": return f"key-word deaths {x['key_word_deaths']} (v110 {x['v110']}); frozen {x['frozen'] or 'none'}"
    if k == "333": return f"row {x['row']}; widest drawn range {x['widest_drawn']} (row less two {x['row_less_two']})"
    if k == "334": return f"q = {x['tempo']}, band {x['band']}: kept {x['kept_quartiles']}; song {x['song']}"
    if k == "336": return (f"under floor {x['under_floor']:.1%}; content median {x['content']['median']}, at kept 25th {x['content']['at_kept_25th']:.1%}, at kept median {x['content']['at_kept_median']:.1%}; "
                           f"order median {x['order']['median']}, at kept 25th {x['order']['at_kept_25th']:.1%}, at kept median {x['order']['at_kept_median']:.1%}; "
                           f"measures outside the kept middle half {x['outside_kept_middle_half']} of {x['content_measures']}; heaviest give-away {x['heaviest_give_away']}")
    if k == "322": return f"paired {x['paired_lines']} ({x['of_another_length']} of another length); given up {x['given_up']} ({x['given_up_share']:.1%}); parallel {x['parallel']}; under floor {x['under_floor']:.1%}"
    if k == "323": return f"one-over bars copied without the weakest onset {x['dropped']}; left out {x['left_out']}; verse 2 in range {x['in_range']:.0%}"
    if k == "324": return f"{x['tonic_endings']} tonic endings, on the nearest to the centre {x['on_nearest_to_centre']}"
    if k == "325": return f"design failures for the registers {x.get('design_failures_for_the_registers', 'n/a')}; last chorus on the tonic {x['last_chorus_tonic']:.1%}; redrawn {x['redrawn'] or 0}"
    if k == "326": return f"{x['design_gates']}"
    if k == "327": return f"join deaths {x['join_copy_deaths']} (v109 92); refits {x['refits']}"
    if k == "328": return f"q = {x['tempo']}, band {x['band']}: kept {x['kept_quartiles']}; song {x['song_share']}"
    if k == "329": return f"sung {x['sung_range']} vs drawn {x['drawn_range']} (gap {x['drawn_minus_sung']}); chorus window {x['chorus_window_range']}; heaviest give-aways {[m for m, _ in x['heaviest_give_aways']]}; extremes sung low {x['low_extreme_sung']:.0%}, high {x['high_extreme_sung']:.0%}"
    return x.get("note", "")
rows = []
for k in TEST:
    m = R[MODES[0]]; c = R[MODES[-1]]
    h = m[k].get("held") if k in m else None
    if isinstance(h, bool) and k in c and isinstance(c[k].get("held"), bool): h = h and c[k]["held"]          # held in the main run and the control
    rows.append((k, TEST[k][0], TEST[k][1], reading(k, m) if k in m else "", reading(k, c) if (k in c and len(MODES) > 1) else "", h))
json.dump(rows, open(f"/home/claude/p44/{OUTN}_table.json", "w"), indent=1, default=str)
for v in MODES: print(v, R[v]["runs"])
for k, t, ka, a, b, h in rows: print(f"{k} | {t} | {ka} | {a} | {b} | {h}")
for v in MODES:
    print("DQ", v); [print(f"  {k}: {x}  (before {R[v]['DQ']['before'][k] if R[v]['DQ']['before'] else '-'})") for k, x in R[v]["DQ"]["now"].items()]
