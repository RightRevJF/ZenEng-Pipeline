"""v124 Run 1 (readings_v119.py with the v119 block and readings_v124_block.py). 321: the table of tests of 310-401 on a song's own runs, main and control, each made twice, as v119 reads them (readings_v118.py with the v119 block), with Table DQ's readings
beside v116 (OLD_PREFIX; for songs 44 and 45 their first runs on the v116 port). 364/372/374 (separability) are read across the five songs by
sep_v118.py. 363: a design gate fails only more than one spread under nine in ten.
Usage: python3 readings_v118.py MODULE PREFIX OUT OLD_PREFIX BASE_PREFIX
  e.g. python3 readings_v118.py melody_v118_p43 /home/claude/p50/melody_v118_p43 readings_v118_p43 /home/claude/p47/melody_v116_p43 /home/claude/p47/melody_v116_p43"""
import sys, pickle, collections, json, importlib
import numpy as np
MOD, PRE, OUTN = sys.argv[1], sys.argv[2], sys.argv[3]; OLDP = sys.argv[4] if len(sys.argv) > 4 else None; BASEP = sys.argv[5] if len(sys.argv) > 5 else None
DESIGN = False
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p54", "/home/claude/p50", "/home/claude/p49", "/home/claude/p48", "/home/claude/p47", "/home/claude/p46", "/home/claude/p45", "/home/claude/p44", "/home/claude/p43", "/home/claude/p42", "/home/claude/p40"]
P = importlib.import_module(MOD); import judges as J
M = P.M; BAR, BEAT = P.BAR, P.BEAT
ETON = getattr(P, "ETON", M.TONIC); LASTSEC = P.SUNG[-1]
LIFTED = {"Last Chorus", "Tag"} if getattr(P, "LIFT", 0) else set()                             # 395: the sections the record lifts (song 45, Q6 A)
def LIFT_(sec): return getattr(P, "LIFT", 0) if sec in LIFTED else 0
                           # the song's tonic (a minor song is read on its relative major)
MODES = ("design",) if DESIGN else ("main", "ctl")
RUN = {v: pickle.load(open(f"{PRE}_{v}.pkl", "rb")) for v in MODES}
RR = {v: pickle.load(open(f"{PRE}_{v}_r.pkl", "rb")) for v in MODES}
OLD = {v: pickle.load(open(f"{OLDP}_{v}.pkl", "rb")) for v in MODES} if OLDP else {}
BASE = {v: pickle.load(open(f"{BASEP}_{v}.pkl", "rb")) for v in MODES} if BASEP else {}
import os
DIAG = {o: pickle.load(open(f"{PRE}_main_off{o}.pkl", "rb")) for o in ("358", "361") if os.path.exists(f"{PRE}_main_off{o}.pkl")}
def spread(x, y, n=1000): return float(np.sqrt(x * (1 - x / n) + y * (1 - y / n)))
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
        lc = [n for n in nts(b) if n["sec"] == LASTSEC]
        if lc: EN.append(((lc[-1]["p"] + LIFT_(LASTSEC)) - (ETON + LIFT_(LASTSEC))) % 12 == 0)                # 395: in the section's own key (the record's lift on both sides)
    miss = st.get("311: ending degree missing after 50 draws", 0)
    r["311"] = dict(last_chorus_tonic=round(float(np.mean(EN)), 4), redrawn=st.get("311: register redrawn for its ending", 0), misses=miss, held=bool(np.mean(EN) == 1.0 and miss == 0))
    pv = [b["read"]["v"].get("past_fifth") for b in Al if b["read"]["v"]]; pc = [b["read"]["c"].get("past_fifth") for b in Al if b["read"]["c"]]
    r["312"] = dict(verse=round(float(np.nanmedian(pv)), 4), chorus=round(float(np.nanmedian(pc)), 4), limit=0.036, leap_knob=round(D["line_knobs"].get("leap", 1.0), 3),
                    held=bool(np.nanmedian(pv) <= 0.036 and np.nanmedian(pc) <= 0.036))
    if "Verse 2" in P.SUNG:
        EQ393 = {i_ for i_ in range(min(len(P.LINES["Verse 1"]), len(P.LINES["Verse 2"]))) if len(P.LINES["Verse 2"][i_]) == len(P.LINES["Verse 1"][i_])}   # 393
        def share(b, which="equal"):
            def bars(s, keep=None):
                out = collections.defaultdict(set)
                for n in nts(b):
                    if n["sec"] == s and (keep is None or int(n["line"].rsplit(":", 1)[1]) in keep): out[n["on"] // BAR - P.BAR0[s]].add(n["on"] % BAR)
                return out
            other = set(range(len(P.LINES["Verse 2"]))) - EQ393
            keep = (EQ393 or None) if which == "equal" else (other or None) if which == "other" else None
            if which == "other" and not other: return None
            a, c = bars("Verse 2", keep), bars("Verse 1"); return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))
        sh = [share(b) for b in Al]; nl = len(P.LINES["Verse 2"]) * D["made"]
        sh_other = [x for x in (share(b, "other") for b in Al) if x is not None]; sh_all = [share(b, "all") for b in Al]
        gu = st.get("293: copy given up for a line", 0)
        r["313"] = dict(share=pct(sh), equal_lines=sorted(EQ393), share_other_lines=pct(sh_other), share_all_lines=pct(sh_all), in_range=round(float(np.mean([0.25 <= x <= 0.75 for x in sh])), 3), given_up=gu, given_up_share=round(gu / max(1, nl), 3),
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
    sp317 = {g: round(float(np.sqrt(x * (1 - x) / max(1, len(Al)))), 4) for g, x in rates.items()}                # 363: a rate read with its spread
    r["317"] = dict(design_gates=rates or "none in force", spreads=sp317, held=all(x >= 0.9 - sp317[g] for g, x in rates.items()) if rates else True)
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
                    by_line={l: round(float(np.mean([x[1] for x in te if x[0] == l])), 4) for l in sorted({x[0] for x in te})}, held=bool(all(x[1] for x in te)) if te else "n/a (no tonic ending drawn)")
    r["314"]["tonic_read_by_324"] = r["324"]["on_nearest_to_centre"]                      # 324 amends 314: the tonic test read on the drawn centre
    r["314"]["held"] = bool(r["314"]["unused_split_max"] <= 1 and 0.40 <= r["314"]["verse_median_share"][1] <= 0.57 and r["324"]["held"] is not False)
    dreg = {k: v for k, v in st.items() if k.startswith("325")}
    if dg:
        def reg_death(b):                                                  # a design failure for want of a note the registers could not hold
            ns = nts(b); h = [n for n in ns if n["line"] == "Chorus 1:0"]; lo = b["meta"]["registers"]["song_lo"]
            lowt = min(p for p in range(lo, lo + 12) if (p - M.TONIC) % 12 == 0); return bool(h) and h[-1]["p"] <= lowt
        if hasattr(P, "design_reg"):
            def reg_death(b):
                g_ = b["meta"]["registers"]
                try: return not P.design_reg(g_.get("sections"), g_)
                except (TypeError, KeyError): return not P.design_reg(None, g_)
        rd = sum(1 for b in Al if any(g in b.get("fails", []) for g in dg) and reg_death(b))
        lt = [((([n for n in nts(b) if n["sec"] == LASTSEC] or [dict(p=-1)])[-1]["p"] - ETON) % 12 == 0) for b in Al]
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
    # ---- v113 ----
    sh_ = r.get("313", {}).get("share")
    if sh_: r["338"] = dict(verse2_share=sh_, kept=[0.25, 0.50, 0.70], rate=D["rerun"].get("rate293"), copies_given_up=r["313"]["given_up"],
                            held=bool(abs(sh_[1] - 0.5) <= 0.10 and 0.25 <= sh_[1] <= 0.70) if v == "main" else bool(0.25 <= sh_[1] <= 0.70))
    # ---- v114 ----
    from sklearn.linear_model import LogisticRegression
    MS = J.CJ["measures"]
    SM = json.load(open("/home/claude/p54/tables/zeneng_v117_kept_songs_and_modes.json"))
    KX = np.array([[row_.get(m_, np.nan) for m_ in MS] for row_ in P.KRW], float)
    BW = [(b["read"][w], w) for b in Al for w in ("v", "c") if b["read"][w]]
    BX = np.array([[f_.get(m_, np.nan) if f_.get(m_) is not None else np.nan for m_ in MS] for f_, _ in BW], float)
    colm = np.nanmean(KX, 0); KX = np.where(np.isfinite(KX), KX, colm); BX = np.where(np.isfinite(BX), BX, colm)
    XX = np.vstack([KX, BX]); mu_, sd_ = XX.mean(0), XX.std(0) + 1e-9
    yy = np.r_[np.ones(len(KX)), np.zeros(len(BX))]
    lr_ = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced").fit((XX - mu_) / sd_, yy)
    wv = lr_.coef_[0]; km, bm = KX.mean(0), BX.mean(0)
    cost = wv * (km - bm) / sd_                                                           # 340: points from the kept mean, measure by measure
    order_ = np.argsort(-cost)
    def cost_of(m_, which=None):
        j = MS.index(m_)
        if which is None: return float(cost[j])
        sub = np.array([x for x, (_, w) in zip(BX, BW) if w == which]); return float(wv[j] * (km[j] - sub[:, j].mean()) / sd_[j])
    r["340"] = dict(gap=round(float(cost.sum()), 2), window_134=[11.0, 10.4], kept_windows=len(KX), build_windows=len(BX),
                    eight=[(MS[j], round(float(cost[j]), 2), round(float(km[j]), 3), round(float(bm[j]), 3)) for j in order_[:8]], held="printed")
    s6p, s6r, s6n = 0, 0, 0
    for b in Al:
        ns = nts(b)
        for s_ in ("Verse 1", "Chorus 1"):
            ons = sorted({n["on"] for n in ns if P.BAR0[s_] * BAR <= n["on"] < (P.BAR0[s_] + 8) * BAR})
            S_ = set(ons)
            for t_ in ons:
                if t_ % 6 == 3:
                    s6n += 1; s6p += (t_ + 3) not in S_; s6r += (t_ - 3) in S_ and (t_ + 3) in S_
    gsc = cost_of("gap_sixteenth")
    r["341"] = dict(sixteenth_onsets=s6n, pushed=round(s6p / max(1, s6n), 3), in_runs=round(s6r / max(1, s6n), 3), kept=[0.54, 0.31], gap_sixteenth_cost=round(gsc, 2),
                    knob=round(D["line_knobs"].get("s16", 1.0), 3), held=bool(s6p / max(1, s6n) >= 0.44 and s6r / max(1, s6n) <= 0.41 and gsc < 0.5))
    npb = [b["read"][w]["notes_per_bar"] for b in Al for w in ("v", "c") if b["read"][w]]
    r["342"] = dict(lyric="printed at intake", builds_notes_a_bar=pct(npb, (25, 50, 75)), kept=[3.6, 4.1], held="printed")
    ddc = cost_of("distinct_durations"); ddm = float(np.median([b["read"][w]["distinct_durations"] for b in Al for w in ("v", "c") if b["read"][w]]))
    r["343"] = dict(median=ddm, kept=4.04, cost=round(ddc, 2), palette_dropped=st.get("343: palette dropped for a line", 0), held=bool(ddc < 0.5 and ddm == 4))
    osv = [b["read"][w]["outside_scale"] for b in Al for w in ("v", "c") if b["read"][w]]; osc = cost_of("outside_scale")
    OSK = 0.045 if getattr(P, "MTON", None) is not None else 0.071                         # 349: 4.5% for a minor song
    r["344"] = dict(mean=round(float(np.mean(osv)), 3), kept=OSK, cost=round(osc, 2), knob=round(D["line_knobs"].get("k44", 1.0), 3), held=bool(abs(np.mean(osv) - OSK) <= 0.02 and osc < 0.5))
    clv, clc = cost_of("chord_tones_on_long_notes", "v"), cost_of("chord_tones_on_long_notes", "c")
    r["345"] = dict(verse_cost=round(clv, 2), chorus_cost=round(clc, 2), kept=0.716, means=round(float(bm[MS.index("chord_tones_on_long_notes")]), 3),
                    knob=round(D["line_knobs"].get("ctl", 1.0), 3), held=bool(clv < 0.5 and clc < 0.5))
    sm = {m_: round(cost_of(m_), 2) for m_ in ("on_offbeat_eighth", "distinct_pitches", "unit2_returns", "unit3_returns", "unit4_to_unit2") if m_ in MS}
    r["346"] = dict(costs=sm, means={m_: round(float(bm[MS.index(m_)]), 3) for m_ in sm}, held=bool(all(x < 0.5 for x in sm.values())))
    worst = [(MS[j], round(float(cost[j]), 2)) for j in order_ if cost[j] > 0.5]
    r["347"] = dict(over_half_a_point=worst, gap=r["340"]["gap"], held=bool(not worst))
    # ---- v115 ----
    r["348"] = dict(pushed=r["341"]["pushed"], in_runs=r["341"]["in_runs"], kept=[0.54, 0.31], gap_sixteenth_cost=r["341"]["gap_sixteenth_cost"],
                    runs_allowed_no_room=st.get("348: a drawn line with no room on the eighth grid (runs allowed)", 0),
                    returns_split_on_sixteenths=st.get("348: a returning line split on the sixteenth grid (no room)", 0), held=r["341"]["held"])
    r["349"] = dict(mean=r["344"]["mean"], kept=OSK, cost=r["344"]["cost"], placed=st.get("349: notes placed outside the scale", 0), wanting=st.get("349: places wanting", 0), held=r["344"]["held"])
    uc = {m_: r["346"]["costs"].get(m_) for m_ in ("unit2_returns", "unit3_returns", "unit4_to_unit2")}
    r["350"] = dict(costs=uc, means={m_: r["346"]["means"].get(m_) for m_ in uc}, kept={"unit3_returns": 0.315}, held=bool(all(x is not None and x < 0.5 for x in uc.values())))
    if "313" in r:
        nl = len(P.LINES["Verse 2"]) * D["made"]; gu = st.get("293: copy given up for a line", 0)
        r["351"] = dict(bars_left_out=st.get("351: bars left out of a copy", 0), lines_given_up=gu, share_given_up=round(gu / max(1, nl), 3), verse2_share=r["313"]["share"],
                        held=bool(gu / max(1, nl) < 0.10 and abs(r["313"]["share"][1] - 0.5) <= 0.10))
    kr = {sec_: [x["repeat"] for x, sc in zip(P.KRW, P.KW["section"]) if sc == sec_ and np.isfinite(x.get("repeat", np.nan))] for sec_ in ("verse", "chorus")}
    kmr = {k_: [round(float(np.percentile(v_, 25)), 3), round(float(np.percentile(v_, 75)), 3)] for k_, v_ in kr.items()}
    byfp = {b["fp"]: b for b in Al}; aa = D["all_alive"]; ocomp = [x[0] for x in aa]; ojudge = [x[0] for x in sorted(aa, key=lambda x: (-x[1], x[0]))]
    def who(c_):
        if c_ is None: return None
        b_ = byfp[c_["fp"]]
        return dict(fp=c_["fp"], judge=round(c_["judge"]["combined"], 2), rank_by_composite=ocomp.index(c_["fp"]) + 1, rank_by_judge=ojudge.index(c_["fp"]) + 1,
                    repeats=[round(b_["read"]["v"]["repeat"], 3), round(b_["read"]["c"]["repeat"], 3)])
    pk, cf = who(D["pick"]), who(D["comp_first"]); p255 = who(D.get("pick_255"))
    r["352"] = dict(pick=pk, composite_first=cf, pick_255=p255, kept_repeats_middle_half=kmr, held="amended by 362")
    r["353"] = dict(reading=("a minor song: the window measures on its tonic with the natural minor scale" if getattr(P, "MTON", None) is not None else "a major song: n/a"), held=True if getattr(P, "MTON", None) is not None else "n/a")
    npbm = float(np.median(npb)); _tg = np.mean([P.du_target(x) for x in npb], 0); band = (P.kband(npbm), "", tuple(round(float(x), 3) for x in _tg))   # 372: the kept table's shares, window by window
    gm = {m_: round(float(np.mean([b["read"][w][m_] for b in Al for w in ("v", "c") if b["read"][w] and np.isfinite(b["read"][w].get(m_, np.nan))])), 3) for m_ in P.GAPS}
    g8c = cost_of("gap_eighth")
    r["354"] = dict(notes_a_bar=round(npbm, 2), band=[band[0], band[1]], kept=dict(zip(P.GAPS, band[2])), builds=gm, gap_eighth_cost=round(g8c, 2),
                    knobs={k_: round(D["line_knobs"].get(k_, 1.0), 3) for k_ in ("s16", "g8", "g4", "glong")},
                    held=bool(all(abs(gm[m_] - t_) <= 0.05 for m_, t_ in zip(P.GAPS, band[2])) and g8c < 0.5))
    # ---- v116 ----
    nd = D["made"]; rpd = D["deaths"].get("rhythm: no placement", 0)
    r["355"] = dict(pushed=r["341"]["pushed"], in_runs=r["341"]["in_runs"], kept=[0.54, 0.31], on_sixteenth=round(float(bm[MS.index("on_sixteenth")]), 3), kept_on_sixteenth=0.094,
                    rhythm_placement_deaths=round(rpd / nd, 3), knobs=dict(run=D["line_knobs"].get("run"), on16=round(D["line_knobs"].get("on16", 1.0), 3)),
                    held=bool(abs(r["341"]["pushed"] - 0.54) <= 0.10 and abs(r["341"]["in_runs"] - 0.31) <= 0.10 and abs(float(bm[MS.index("on_sixteenth")]) - 0.094) <= 0.02 and rpd / nd < 0.05))
    W = D["would"]; Wb = BASE[v]["would"] if v in BASE else {}
    c356 = {}
    for k_ in ("rhythm band", "memory"):
        x_, y_ = W.get("limit broken: " + k_, 0), Wb.get("limit broken: " + k_, 0); c356[k_] = (x_, y_, round(spread(x_, y_), 1))
    sb = BASE[v]["survivors"] if v in BASE else None
    r["356"] = dict(breaks_now_base_spread=c356, distinct_lengths_median=ddm, survivors=(D["survivors"], sb, round(spread(D["survivors"], sb), 1) if sb else None),
                    stop356=D["rerun"].get("stop356"), rounds=D["rerun"].get("calibration_rounds"),
                    diagnostics={o: dict(survivors=X["survivors"], order=X["order_fp"], rhythm_band=X["would"].get("limit broken: rhythm band", 0), memory=X["would"].get("limit broken: memory", 0),
                                         rhythm_placement=X["deaths"].get("rhythm: no placement", 0)) for o, X in DIAG.items()} if v == "main" else "main run only",
                    held=bool(all(abs(x_ - y_) <= 2 * sp_ for x_, y_, sp_ in c356.values()) and ddm == 4 and (sb is None or "p43" not in MOD or abs(D["survivors"] - sb) <= 2 * spread(D["survivors"], sb))))
    r["357"] = dict(builds=gm, kept=dict(zip(P.GAPS, band[2])), rounds=D["rerun"].get("calibration_rounds"), knobs=r["354"]["knobs"], stopped=bool(D["rerun"].get("stop356")),
                    held=bool(all(abs(gm[m_] - t_) <= 0.05 for m_, t_ in zip(P.GAPS, band[2]))))
    tb = (W.get("limit broken: tritone_from_root_share", 0), OLD[v]["would"].get("limit broken: tritone_from_root_share", 0) if v in OLD else 0)
    r["358"] = dict(mean=r["344"]["mean"], kept=OSK, cost=r["344"]["cost"], passing_placed=st.get("358: chromatic passing notes placed", 0), placed=st.get("349: notes placed outside the scale", 0),
                    wanting=st.get("349: places wanting", 0), tritone_from_root_breaks=(tb[0], tb[1], round(spread(*tb), 1)),
                    held=bool(abs(r["344"]["mean"] - OSK) <= 0.02 and abs(tb[0] - tb[1]) <= 2 * spread(*tb)))
    if getattr(P, "MTON", None) is not None:                                              # 359 as written (369): against the 70 kept minor windows
        mi = np.array([md_ == "minor" for md_ in SM["mode"]]); kmm = KX[mi].mean(0)
        cost_m = wv * (kmm - bm) / sd_; om = np.argsort(-cost_m)
        r["359"] = dict(minor_windows=int(mi.sum()), judge="the judge of record (70 windows too few to fit one); costs on 340's fresh judge against the minor means",
                        gap_minor=round(float(cost_m.sum()), 2), gap_all=r["340"]["gap"], eight_minor=[(MS[j], round(float(cost_m[j]), 2), round(float(kmm[j]), 3), round(float(bm[j]), 3)) for j in om[:8]],
                        outside_scale=dict(builds=round(float(bm[MS.index("outside_scale")]), 3), minor_mean=round(float(kmm[MS.index("outside_scale")]), 3), cost_minor=round(float(cost_m[MS.index("outside_scale")]), 2),
                                           cost_all=round(float(cost[MS.index("outside_scale")]), 2)), held="printed")
    else: r["359"] = dict(reading="a major song: n/a", held="n/a")
    if "313" in r:
        r["360"] = dict(verse2_share=r["313"]["share"], fitted_again_kept=st.get("360: bars fitted again and kept", 0), fitted_again_failed=st.get("360: bars fitted again without success", 0),
                        bars_left_out=st.get("351: bars left out of a copy", 0),
                        held=bool(0.25 <= r["313"]["share"][1] <= 0.70 and (abs(r["313"]["share"][1] - 0.5) <= 0.10 if v == "main" else True)))
    KUR = {"unit2_returns": 0.172, "unit3_returns": 0.315, "unit4_to_unit2": 0.188}
    um = {m_: round(float(bm[MS.index(m_)]), 3) for m_ in KUR}
    r["361"] = dict(means=um, kept=KUR, drawn={k_: v_ for k_, v_ in st.items() if k_.startswith("361") or k_.startswith("346")},
                    held=bool(abs(um["unit3_returns"] - 0.315) <= 0.10 and abs(um["unit4_to_unit2"] - 0.188) <= 0.10))
    pj = who(D.get("pick_352"))
    r["362"] = dict(pick=pk, judges_first=pj, survivors_with_no_soft_break=D.get("clean"), survivors=D["survivors"], pick_soft=[c_ for c_ in (D["pick"] or {}).get("info", {}).get("soft", [])],
                    held=bool(D["pick"] is not None and (not D["pick"]["info"]["soft"] or D.get("clean") == 0)))
    r["363"] = dict(design_gates=r["317"]["design_gates"], spreads=r["317"]["spreads"], held=r["317"]["held"])
    # ---- v118 ----
    def spans(b):
        """378: each line followed by another in its section: (notes, syllables, share of the time to the next line's first onset sung)."""
        byl = collections.OrderedDict()
        for n in sorted(nts(b), key=lambda n: n["on"]): byl.setdefault(n["line"], []).append(n)
        out = []
        for sec_ in P.SUNG:
            for j in range(len(P.LINES[sec_]) - 1):
                a_, b_ = byl.get(f"{sec_}:{j}"), byl.get(f"{sec_}:{j + 1}")
                if not a_ or not b_: continue
                slot_ = b_[0]["on"] - a_[0]["on"]
                if slot_ <= 0: continue
                out.append((len(a_), len({n["syl"] for n in a_}), (a_[-1]["on"] + a_[-1]["dur"] - a_[0]["on"]) / slot_, slot_))
        return out
    sp_ = [x for b in Al for x in spans(b)]
    KSP = {"3-5": (0.429, 0.75), "6-8": (0.531, 0.80), "9-12": (0.656, 0.875), "13+": (0.783, 0.938)}
    def grp_(nn): return "3-5" if nn <= 5 else "6-8" if nn <= 8 else "9-12" if nn <= 12 else "13+"
    med_sp = {g_: round(float(np.median([x[2] for x in sp_ if grp_(x[0]) == g_])), 3) for g_ in KSP if any(grp_(x[0]) == g_ for x in sp_)}
    full_ = [x for x in sp_ if x[1] * 6 >= 0.5 * x[3]]; under_ = float(np.mean([x[2] < 0.5 for x in full_])) if full_ else 0.0
    r["378"] = dict(median_share_by_notes=med_sp, kept_middle_half=KSP, lines=len(sp_), under_half_of_full=round(under_, 3), kept_under_half_of_full=0.046,
                    all_median=round(float(np.median([x[2] for x in sp_])), 3), kept_all_median=0.71,
                    drawn_to_a_span=st.get("378: lines drawn to a span", 0), given_up=st.get("378: span given up (nothing fitted inside it)", 0), redrawn=st.get("378: rhythm outside its span, redrawn", 0),
                    held=bool(all(KSP[g_][0] <= x <= KSP[g_][1] for g_, x in med_sp.items()) and under_ < 0.05))
    KN = D["rerun"].get("knobs372", {})
    r["372"] = dict(knobs=KN, past_a_factor_of_two=[k_ for k_, x in KN.items() if x["past_a_factor_of_two"]], bands=D["rerun"].get("section_bands372"),
                    builds=gm, kept=dict(zip(P.GAPS, band[2])), held=bool(all(abs(gm[m_] - t_) <= 0.05 for m_, t_ in zip(P.GAPS, band[2]))))
    k249 = {p_: {k_: round(D["knobs"][p_].get(k_, 1.0), 3) for k_ in ("gap8", "gap4", "gap16")} for p_ in ("V", "C")}
    r["365"] = dict(knobs249=k249, builds=gm, kept=dict(zip(P.GAPS, band[2])),
                    held=bool(all(x == 1.0 for d_ in k249.values() for x in d_.values()) and r["372"]["held"]))
    r["366"] = dict(pushed=r["341"]["pushed"], in_runs=r["341"]["in_runs"], kept=[0.54, 0.31], rate=round(D["line_knobs"].get("run", 1.0), 3),
                    may_run=st.get("366: lines drawn that may run", 0), may_not=st.get("366: lines drawn that may not run", 0), fallback=st.get("366: fallback to runs (nothing fitted without)", 0),
                    held=bool(abs(r["341"]["pushed"] - 0.54) <= 0.10 and abs(r["341"]["in_runs"] - 0.31) <= 0.10))
    r["367"] = dict(band=list(P.MID356["rhythm_bits"]), source="the pooled kept table on 105 kept chart songs (373); the v88 table on 103: 2.20-2.94 (367)",
                    stop356=D["rerun"].get("stop356"), held=True)
    if "p43" in MOD and v == "main":
        def mem_breaks(Dx): return sum(1 for b in Dx["all"] if (b["info"].get("limits7") or {}).get("memory", 1.0) is not None and (b["info"].get("limits7") or {}).get("memory", 1.0) < 0.12)
        V114 = pickle.load(open("/home/claude/p45/melody_p43_main.pkl", "rb")); m114 = mem_breaks(V114); mnow = mem_breaks(D)
        r["368"] = dict(memory_breaks_now=mnow, v114=m114, spread=round(spread(mnow, m114), 1), limit="soft 0.12 (373)",
                        diagnostics={o: dict(survivors=X["survivors"], order=X["order_fp"], memory=mem_breaks(X)) for o, X in DIAG.items()},
                        held=bool(abs(mnow - m114) <= 2 * spread(mnow, m114)))
    if "313" in r:
        r["370"] = dict(verse2_share=r["313"]["share"], kept=0.5, by_variant={k_: v_ for k_, v_ in st.items() if k_.startswith("370")}, fitted_again_kept=st.get("360: bars fitted again and kept", 0),
                        fitted_again_failed=st.get("360: bars fitted again without success", 0), held=bool(abs(r["313"]["share"][1] - 0.5) <= 0.10) if v == "main" else "main run only")
    r["371"] = dict(means=um, kept=KUR, rates=D["rerun"].get("unit_return_rates371"), over_pairs=st.get("371: unit return over a paired line (the return kept)", 0),
                    drawn={k_: v_ for k_, v_ in st.items() if k_.startswith("361: unit")}, held=r["361"]["held"])
    W_ = D["would"]; lim_ = D["deaths"].get("limits: a hard limit or three soft breaks (276/277, with 286's seven)", 0)
    r["373"] = dict(limits={k_: (str(x["rule"]), x["corpus"]) for k_, x in D["rerun"].get("limits", {}).items()},
                    soft_breaks=dict(rhythm_band=W_.get("limit broken: rhythm band", 0), memory=W_.get("limit broken: memory", 0)), complete=len(Al),
                    held=bool(W_.get("limit broken: rhythm band", 0) <= 0.12 * len(Al) and W_.get("limit broken: memory", 0) <= 0.12 * len(Al)))
    CH_ = P.CHORD; viol = 0; seen_ = 0; viol3 = 0; seen3 = 0; vk = collections.Counter()
    def raised3(ch_):
        r0, tones_ = M.CH[ch_]; t3 = (r0 + 4) % 12
        return [t3] if t3 in tones_ and t3 not in M.SCALE else []
    for b in Al:
        byl_ = collections.defaultdict(list)
        for n in nts(b): byl_[n["line"]].append(n)
        for n in nts(b):
            if n["on"] % BEAT and n["dur"] < 12: continue
            ch_ = M.chord_at(n["on"]); tones_ = M.CH[ch_][1]; out_ = [t_ for t_ in tones_ if t_ not in M.SCALE]
            if out_:
                seen_ += 1; bad_ = any((n["p"] - t_) % 12 in (1, 11) for t_ in out_) and n["p"] % 12 not in tones_; viol += bad_
                if bad_:
                    ln_ = byl_[n["line"]]; kd_ = b["kinds"].get(tuple(n["line"].rsplit(":", 1)[:1]) + (int(n["line"].rsplit(":", 1)[1]),), "?") if isinstance(b.get("kinds"), dict) else "?"
                    vk["first note" if n is ln_[0] else "last note" if n is ln_[-1] else "inside"] += 1; vk["line: " + str(kd_)] += 1
            r3 = raised3(ch_)
            if r3: seen3 += 1; viol3 += any((n["p"] - t_) % 12 in (1, 11) for t_ in r3) and n["p"] % 12 not in tones_
    pw, pl_ = st.get("349: places wanting", 0), st.get("349: notes placed outside the scale", 0)
    r["375"] = dict(notes_read=seen_, semitone_from_a_raised_tone=viol, where=dict(vk), secondary_dominant_notes=seen3, semitone_from_a_raised_third=viol3,
                    places_wanting=pw, placed=pl_, held=bool(viol3 == 0 and pw <= 0.1 * max(1, pw + pl_)))
    r["376"] = dict(calibration_stop=D["rerun"].get("calibration_stop"), frozen=D["rerun"].get("frozen"), held=True)
    if getattr(P, "PIN", None):
        drawn_, pinned_, lift_ok = [], [], []
        for b in Al:
            l3 = (b["info"] or {}).get("lift377")
            if l3: drawn_.append(l3["drawn"]); pinned_.append(l3["pinned"]); lift_ok.append(l3["drawn"] >= 3)
        r["377"] = dict(drawn_minus_verse=pct(drawn_, (25, 50, 75)), pinned_minus_verse=pct([x for x in pinned_ if x is not None], (25, 50, 75)),
                        lift_fails=round(1 - float(np.mean(lift_ok)), 3) if lift_ok else None, held=bool(lift_ok and 1 - np.mean(lift_ok) < 0.05))
    else: r["377"] = dict(note="no pinned notes in this song", held="n/a")
    r["379"] = dict(note="an arrangement rule: in song 45's build and its consistency checks (songs/p49); these runs build no arrangement", held="n/a")
    if dg:
        lifts = [b["info"]["lift"]["median"] for b in Al]
        r["380"] = dict(chosen_lift=getattr(P, "LIFT", None) or "the design gate's", lift_median=pct(lifts, (25, 50, 75)), design_pass=r["317"]["design_gates"], spreads=r["317"]["spreads"],
                        redraws_design=sum(v_ for k_, v_ in st.items() if k_.startswith("325")), redraws_ending=st.get("311: register redrawn for its ending", 0),
                        held=r["317"]["held"] and sum(v_ for k_, v_ in st.items() if k_.startswith("325")) <= max(st.get("311: register redrawn for its ending", 0), 1) * 1.0 if "p44" in MOD or "p45" in MOD else "n/a")
    else: r["380"] = dict(note="no lift chosen at intake", held="n/a")
    offp = 0
    for b in Al:
        for n in nts(b):
            if n["p"] % 12 not in M.SUNGPC and n["p"] % 12 not in M.CH[M.chord_at(n["on"])][1]: offp += 1
    r["381"] = dict(notes_outside_the_sung_pitch_classes=offp, passing_placed=st.get("358: chromatic passing notes placed", 0), held=bool(offp == 0))
    r["382"] = dict(limits=r["373"]["limits"], lost_to_limits=round(lim_ / D["made"], 3), surprisal_breaks=W_.get("limit broken: surprisal", 0), memory_breaks=W_.get("limit broken: memory", 0),
                    beside_design=(dg if dg else "no design narrows a section or repeats a figure"), held=bool(lim_ / D["made"] < 0.2))
    r["383"] = dict(note="no hand edits in these runs (song 45 as drawn)", held="n/a")
    # ---- 337: counts beside counts (main against control), with their spread ----
    exec(open("/home/claude/p54/readings_v119_block_for128.py").read())
    exec(open("/home/claude/p54/readings_v124_block_for128.py").read())                               # v124 Run 1: 405, 409, 412-415, 417, 419, 428
    exec(open("/home/claude/p54/readings_v127_block_for128.py").read())                                  # v127 Run 2: 470-473, 464, 459
    exec(open("/home/claude/p54/readings_v128_block.py").read())                                       # v128 Run 3: 465, 458, 478, 484, 476, 477, 486, 489-491, 494
    r["337"] = "after both runs"
    R[v] = r
if len(MODES) > 1:
    a_, c_ = RUN["main"], RUN["ctl"]; na, nc = a_["made"], c_["made"]; rows337 = []
    for k in sorted(set(a_["deaths"]) | set(c_["deaths"]), key=lambda k: -(a_["deaths"].get(k, 0) + c_["deaths"].get(k, 0))):
        x, y = a_["deaths"].get(k, 0), c_["deaths"].get(k, 0)
        sp = float(np.sqrt(x * (1 - x / na) + y * (1 - y / nc)))
        rows337.append((k, x, y, round(sp, 1), "no difference" if abs(x - y) < 2 * sp else "a difference"))
    for v in MODES: R[v]["337"] = dict(deaths_main_vs_control=rows337, held="printed")
json.dump(R, open(f"/home/claude/p54/{OUTN}.json", "w"), indent=1, default=str)
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
        "336": ("the share under the floor; builds at the kept 25th and median on each judge; content measures outside the kept middle half", "a reading"),
        "337": ("a count beside another is read with its spread; a difference under two spreads is no difference", "a reading (main against control)"),
        "338": ("verse 2's share within ten points of 50% at the median of the main run, and inside 25-70%; copies given up printed", "kept 25-70% (median 50%)"),
        "340": ("the gap from the kept mean on a judge fitted to kept windows against these builds; the eight costliest measures", "a reading (Window 134: 11.0 and 10.4)"),
        "341": ("of sixteenth-position onsets, 44% or more pushed and 41% or fewer in runs; sixteenth gaps cost under half a point", "kept 54% pushed, 31% in runs"),
        "342": ("the lyric's density printed at intake; the builds' notes a bar", "kept 3.6-4.1 (a reading)"),
        "343": ("distinct note lengths cost under half a point; four at the median", "kept 4.04"),
        "344": ("notes outside the scale within two points of the kept mean; cost under half a point", "kept 7.1%"),
        "345": ("chord tones on long notes cost under half a point in the verse and the chorus", "kept 72%"),
        "346": ("the off-beat eighth, distinct pitches and unit returns each cost under half a point", "kept 0.37, 6.4, 0.17/0.19"),
        "347": ("no measure costs more than half a point; the gap printed", "the kept mean (340's judge)"),
        "348": ("of sixteenth-position onsets, 44% or more pushed, 41% or fewer in runs; sixteenth gaps cost under half a point", "kept 54% pushed, 31% in runs"),
        "349": ("the outside-scale share within two points of the kept mean; cost under half a point", "kept 7.1% (4.5% minor)"),
        "350": ("no unit return costs over half a point", "kept unit 3 returns 31.5%"),
        "351": ("verse 2 lines given up under one in ten; verse 2's share within ten points of 50% at the median", "kept 50% (25-70%)"),
        "352": ("the pick (the judge's first), the composite's first, each one's rank on the other, each one's repeats", "a check; kept repeats' middle half printed"),
        "353": ("a minor song's degree measures read on its tonic with the natural minor scale", "the rule's own statement (a check)"),
        "354": ("each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point", "the kept table (372)"),
        "355": ("pushed within ten points of 54% and runs within ten of 31%; onsets on a sixteenth within two points of 9.4%; rhythm-placement deaths under 1 in 20", "kept 54% / 31%; 9.4%"),
        "356": ("rhythm-band and memory breaks within two spreads of the version before v115; four distinct lengths at the median; song 43's survivors within two spreads of 811; the diagnostic runs printed", "v112 (40, 42), v114 (43)"),
        "357": ("each gap share within five points of the kept table's, main and control; the rounds printed", "the kept table (372)"),
        "358": ("outside the scale within two points of 7.1% (4.5% minor); tritone-from-root breaks within two spreads of v115", "kept 7.1% (4.5% minor)"),
        "359": ("a minor song's readings and costs read against the 70 kept minor windows", "kept minor means (369)"),
        "360": ("verse 2's share inside 25-70% at the median and within ten points of 50% in the main run; bars left out printed", "kept 50% (25-70%)"),
        "361": ("unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate", "kept 31.5%, 18.8%"),
        "362": ("the pick breaks no soft limit, or none qualified and the run says so; the number that qualified printed", "a check"),
        "363": ("a design gate fails only when its rate is more than one spread under nine in ten", "the paper's 317 with 337's spread"),
        "365": ("249's gap knobs do not move; each gap share within five points of the kept table's for the section's notes a bar", "the kept table (372)"),
        "366": ("runs within ten points of 31% and pushes within ten of 54%, main and control; fallback lines printed", "kept 31% / 54%"),
        "367": ("356's band printed with its source", "kept quartiles (a check)"),
        "368": ("song 43: memory breaks (373's limit) within two spreads of v114's read the same way, or the fix responsible named", "v114, read with 373's limit"),
        "369": ("364's figures for v115 reproduce 0.966, 0.954, 0.942 and 0.909 within 0.01; song 43's costs read against the 70 minor windows", "Window 136 (sep_v118)"),
        "370": ("verse 2's share within ten points of 50% at the median in the main run", "kept 50%"),
        "371": ("unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate", "kept 31.5%, 18.8%"),
        "372": ("with every gap knob starting at one, the four gap shares within five points of the kept table's; each knob's final value printed", "the kept table"),
        "373": ("each limit printed with its corpus; soft breaks of the rhythm band and of memory near one build in ten or fewer", "kept chart songs"),
        "374": ("the builds' separation beside 0.57 and 0.63", "the yardstick (sep_v118)"),
        "375": ("no sung note a semitone from a chord's raised tone on a beat or held a beat; 349's places wanting under a tenth of its target", "the rule (a check)"),
        "376": ("a run in which a knob freezes completes and prints the round", "a check"),
        "377": ("song 45: the lift's failures under one complete build in twenty; drawn and pinned medians printed", "the rule"),
        "378": ("the median share of the slot sung, by notes, inside the kept middle half; under one line in twenty under half its slot when its syllables in eighths would fill half", "kept 43-75, 53-80, 66-88, 78-94%; 4.6%"),
        "379": ("no held sung note a semitone or minor ninth from a sustained accompaniment note", "n/a here (song 45's build)"),
        "380": ("a chosen lift met in nine builds in ten (with its spread), with no more redraws than 311's endings take", "the paper's 317 with 337's spread"),
        "381": ("no note outside the song's sung pitch classes (a chord's own tones aside)", "the rule (a check)"),
        "382": ("the seven limits printed with their corpus; builds lost to limits under one in five; surprisal and memory breaks beside a design", "kept chart songs"),
        "383": ("each hand-edited line before and after, with both scores", "n/a (no hand edits)")}
def _reading0(k, r):
    x = r[k]
    if k == "310": return f"under floor {x['under_floor']:.1%}; parallel {x['parallel']} (kept 0.14); paired lines {x['paired_lines']}, partner given up {x['partner_given_up']}"
    if k == "311": return f"tonic {x['last_chorus_tonic']:.1%}; registers redrawn {x['redrawn']}; misses {x['misses']}"
    if k == "312": return f"verse {x['verse']:.1%}, chorus {x['chorus']:.1%}; leap knob {x['leap_knob']}"
    if k == "313": return f"share {x['share']}; in range {x['in_range']:.0%}; given up {x['given_up']} ({x['given_up_share']:.1%}); left out {x['left_out']}"
    if k == "314": return f"range {x['range']} (kept {x['kept_range']}); unused split max {x['unused_split_max']}; verse share {x['verse_median_share']}; tonic nearest the sung median {x['tonic_nearest_median']}, the drawn centre {x.get('tonic_read_by_324')}; top fifth {x['top_fifth']:.0%}; floor {x['floor']:.0%}"
    if k == "315": return f"amplitude {x['amplitude']}; arch {x['arch_span']}; stop {x['calibration_stop'] or 'none'}"
    if k == "316": return f"redraws {x['redraws']}/{x['long_lines']} = {x['per_line']}; entries {x['entry_shares']}" + (f" (before {x.get('entry_shares_before')})" if 'entry_shares_before' in x else "")
    if k == "317": return f"{x['design_gates']}" + (f" (spread {x['spreads']})" if x.get('spreads') else "")
    if k == "318": return f"{x['feel']}; sixteenth onsets {x['sixteenth_onsets']}"
    if k == "330": return f"likeness {x['parallel']}; copies failed and the stresses kept {x['copy_failed_stresses_kept']}; given up after the stresses {x['given_up_after_stresses']}; partners given up {x['partners_given_up']} ({x['given_up_share']:.1%})"
    if k == "331": return f"rate {round(x['rate'], 3) if x['rate'] is not None else '-'}; verse 2 share {x['share']} (5th, median, 95th)"
    if k == "332": return f"key-word deaths {x['key_word_deaths']} (v110 {x['v110']}); frozen {x['frozen'] or 'none'}"
    if k == "333": return f"row {x['row']}; widest drawn range {x['widest_drawn']} (row less two {x['row_less_two']})"
    if k == "334": return f"q = {x['tempo']}, band {x['band']}: kept {x['kept_quartiles']}; song {x['song']}"
    if k == "337": return "; ".join(f"{d} {a}/{c} (spread {sp}, {w})" for d, a, c, sp, w in x["deaths_main_vs_control"][:6])
    if k == "338": return f"verse 2 share {x['verse2_share']}; rate {round(x['rate'], 3) if x['rate'] else '-'}; copies given up {x['copies_given_up']}"
    if k == "340": return f"gap {x['gap']} (Window 134: 11.0, 10.4); costliest {[(m, c) for m, c, _, _ in x['eight']]}"
    if k == "341": return f"sixteenth onsets {x['sixteenth_onsets']}: pushed {x['pushed']:.0%}, in runs {x['in_runs']:.0%}; sixteenth gaps cost {x['gap_sixteenth_cost']}"
    if k == "342": return f"builds' notes a bar {x['builds_notes_a_bar']} (kept 3.6-4.1)"
    if k == "343": return f"distinct lengths {x['median']} at the median; cost {x['cost']}; palette dropped for {x['palette_dropped']} lines"
    if k == "344": return f"outside the scale {x['mean']:.1%} (kept 7.1%); cost {x['cost']}"
    if k == "345": return f"cost verse {x['verse_cost']}, chorus {x['chorus_cost']}; chord tones on long notes {x['means']:.0%}"
    if k == "346": return f"costs {x['costs']}"
    if k == "348": return f"pushed {x['pushed']:.0%}, in runs {x['in_runs']:.0%}; sixteenth gaps cost {x['gap_sixteenth_cost']}; lines with no room (runs allowed) {x['runs_allowed_no_room']}"
    if k == "349": return f"outside the scale {x['mean']:.1%} (kept {x['kept']:.1%}); cost {x['cost']}; placed {x['placed']}, places wanting {x['wanting']}"
    if k == "350": return f"costs {x['costs']}; means {x['means']}"
    if k == "351": return f"bars left out {x['bars_left_out']}; lines given up {x['lines_given_up']} ({x['share_given_up']:.1%}); verse 2 share {x['verse2_share']}"
    if k == "352": return f"pick {x['pick']}; composite first {x['composite_first']}; kept repeats {x['kept_repeats_middle_half']}"
    if k == "353": return x["reading"]
    if k == "354": return f"{x['notes_a_bar']} notes a bar, band {x['band']}: kept {list(x['kept'].values())}, builds {list(x['builds'].values())}; eighth gaps cost {x['gap_eighth_cost']}"
    if k == "355": return f"pushed {x['pushed']:.0%}, in runs {x['in_runs']:.0%}; on a sixteenth {x['on_sixteenth']:.1%}; rhythm-placement deaths {x['rhythm_placement_deaths']:.1%}; knobs run {x['knobs']['run']:.2g}, on16 {x['knobs']['on16']}"
    if k == "356": return (f"breaks (now, before, spread) {x['breaks_now_base_spread']}; distinct lengths {x['distinct_lengths_median']}; survivors {x['survivors']}; rounds {x['rounds']}; 354 stopped: {x['stop356'] or 'no'}"
                           + (f"; diagnostics {x['diagnostics']}" if isinstance(x['diagnostics'], dict) else ""))
    if k == "357": return f"builds {list(x['builds'].values())} against {list(x['kept'].values())}; rounds {x['rounds']}; knobs {x['knobs']}" + ("; stopped by 356" if x['stopped'] else "")
    if k == "358": return f"outside the scale {x['mean']:.1%} (kept {x['kept']:.1%}); passing notes {x['passing_placed']} of {x['placed']} placed, places wanting {x['wanting']}; tritone-from-root breaks (now, v115, spread) {x['tritone_from_root_breaks']}"
    if k == "359" and "gap_minor" not in x: return x["reading"]
    if k == "360": return f"verse 2 share {x['verse2_share']}; bars fitted again and kept {x['fitted_again_kept']}, not {x['fitted_again_failed']}; left out {x['bars_left_out']}"
    if k == "361": return f"means {x['means']} (kept {list(x['kept'].values())}); drawn {x['drawn']}"
    if k == "362": return f"no soft break {x['survivors_with_no_soft_break']} of {x['survivors']}; pick {x['pick']['fp'] if x['pick'] else '-'} (soft {x['pick_soft'] or 'none'}, judge rank {x['pick']['rank_by_judge'] if x['pick'] else '-'}); judge's first {x['judges_first']['fp'] if x['judges_first'] else '-'}"
    if k == "365": return f"249's gap knobs {x['knobs249']}; builds {list(x['builds'].values())} against {list(x['kept'].values())}"
    if k == "366": return f"pushed {x['pushed']:.0%}, in runs {x['in_runs']:.0%}; rate {x['rate']}; lines may run {x['may_run']}, may not {x['may_not']}, fallback {x['fallback']}"
    if k == "367": return f"band {x['band']} ({x['source']}); stop {x['stop356'] or 'did not fire'}"
    if k == "368": return f"memory breaks {x['memory_breaks_now']} (v114 {x['v114']}, spread {x['spread']}); diagnostics {x['diagnostics']}"
    if k == "370": return f"verse 2 share {x['verse2_share']}; kept by variant {x['by_variant']}; fitted again kept {x['fitted_again_kept']}, not {x['fitted_again_failed']}"
    if k == "371": return f"means {x['means']} (kept {list(x['kept'].values())}); rates {x['rates']}; returns over pairs {x['over_pairs']}"
    if k == "372": return f"knobs {({k_: v_['final'] for k_, v_ in x['knobs'].items()})}; past a factor of two {x['past_a_factor_of_two'] or 'none'}; builds {list(x['builds'].values())} against {list(x['kept'].values())}"
    if k == "373": return f"soft breaks: rhythm band {x['soft_breaks']['rhythm_band']}, memory {x['soft_breaks']['memory']} of {x['complete']} complete"
    if k == "375": return f"a secondary dominant's raised third: {x['semitone_from_a_raised_third']} of {x['secondary_dominant_notes']} notes a semitone from it; any chord tone outside the scale: {x['semitone_from_a_raised_tone']} of {x['notes_read']} (where {x['where']}); 349 placed {x['placed']}, wanting {x['places_wanting']}"
    if k == "376": return f"stop {x['calibration_stop'] or 'no knob froze'}"
    if k == "377": return f"lift failures {x.get('lift_fails')}; drawn {x.get('drawn_minus_verse')}, pinned {x.get('pinned_minus_verse')}" if 'lift_fails' in x else x['note']
    if k == "378": return f"median share {x['median_share_by_notes']} (all {x['all_median']}, kept 0.71); under half of full lines {x['under_half_of_full']:.1%} (kept 4.6%); drawn to a span {x['drawn_to_a_span']}, given up {x['given_up']}"
    if k == "380": return f"lift {x['lift_median']}; design {x['design_pass']}; redraws design {x['redraws_design']}, ending {x['redraws_ending']}" if 'lift_median' in x else x['note']
    if k == "381": return f"notes outside the sung pitch classes {x['notes_outside_the_sung_pitch_classes']}; passing placed {x['passing_placed']}"
    if k == "382": return f"lost to limits {x['lost_to_limits']:.1%}; surprisal breaks {x['surprisal_breaks']}, memory {x['memory_breaks']}; beside {x['beside_design'] if isinstance(x['beside_design'], str) else 'the design gate'}"
    if k == "359" and "gap_minor" in x: return f"{x['minor_windows']} minor windows; gap {x['gap_minor']} (all {x['gap_all']}); outside the scale {x['outside_scale']}; costliest {[(m, c) for m, c, _, _ in x['eight_minor'][:4]]}"
    if k == "363": return f"{x['design_gates']} (spread {x['spreads']})" if x['design_gates'] != 'none in force' else "none in force"
    if k == "347": return f"over half a point: {x['over_half_a_point'] or 'none'}; gap {x['gap']}"
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

TEST.update({
    "384": ("generators patched by whole statements; each patched path run once before a run of record", "a check (the smoke run)"),
    "385": ("notes outside the scale within two points of 7.1% (4.5% minor)", "kept 7.1% (4.5% minor)"),
    "386": ("no sung note on a beat or a beat long a semitone from a chord's own outside tone, in drawn, returning or copied lines", "the rule (a check)"),
    "387": ("356's stop a reading: it moves and freezes no knob", "a check"),
    "388": ("the two side runs made and read; nothing changed", "printed (step 2)"),
    "389": ("runs within ten points of the band's kept share; deaths for want of a rhythm within two spreads of v116's (song 45: none)", "the kept table's bands; v116"),
    "390": ("unit returns within ten points of the kept rates on the units free to draw; the free share printed", "kept 17.2%, 31.5%, 18.8%"),
    "391": ("378 read on drawn lines: the median share by notes inside the kept middle half; spans given up under one in twenty", "kept 43-75, 53-80, 66-88, 78-94%"),
    "392": ("song 45: the lift's failures under one complete build in twenty, read on drawn notes", "the rule"),
    "393": ("verse 2's share on the lines of verse 1's syllable count within ten points of 50% (main run); the rest printed", "kept 50%"),
    "394": ("song 43's memory breaks within two spreads of v114's; the others printed", "v114, read with 373's limit"),
    "395": ("311 and 324 read in the section's own key where the record lifts it", "the rule (a check)"),
    "396": ("separability by family printed beside Window 139", "Table DY (sep_v119)"),
    "398": ("chord tones 54-76% at the median, on a beat 56-80%; non-chord notes resolved by step within ten points of 50%", "kept 64%, 67%, 72%; 50%"),
    "399": ("a sung note on the downbeat of Verse 1's and Chorus 1's first bar in 59-79% of builds, unless a design places the entry", "kept 69%"),
    "400": ("turns per move within 0.04 of 0.58 at the mean, verse and chorus", "kept 0.58"),
    "401": ("four distinct note lengths in the judge's window at the median", "kept 4"),
    "424": ("leaps of a fourth or fifth, the window's last note on the tonic and empty bars each between the two collections' means or within a fifth of a sd of the nearer; outside the scale printed (420)", "CoCoPops and BiMMuDa 1958-1991"),
})
TEST.update({
    "459": ("verse 2 read on bars whose syllable counts differ by one or less: half its bars or more read, the median share within ten points of 50% (main run)", "kept 50%"),
    "465": ("a drawn line's last onset in the bar the kept share for its notes draws; class given up and span given up each under one line in twenty", "kept shares by notes (zeneng_v128_kept_lines.json)"),
    "458": ("the span's bounds from kept lines' notes a second; drawn lines' median rate inside the kept 25th-75th by notes (bands of 200 lines or more)", "kept 2.2-3.8 notes a second"),
    "478": ("verse 2's repeats and steps within five points of verse 1's (first eight bars, build by build)", "the first verse's own rates"),
    "484": ("the pitch verse 2 keeps of verse 1 (Window 142's pair) inside 72-79%", "kept 72-79%"),
    "476": ("the content judge of record is zeneng_v128_judge.json; builds under its kept 25th percentile printed", "kept mean 1.53, sd 2.0, 25th 0.23"),
    "477": ("the pick's score the mean of content and order, window by window", "the rule (a check)"),
    "486": ("389's run rates read on Verse 1 and Chorus 1 for their bands", "printed"),
    "489": ("452's knobs by band of density", "read in the reread by density band"),
    "490": ("a weight on an onset in a run, by band; drawable runs within ten points on bands of 200 onsets or more", "kept by band (389)"),
    "491": ("467's and 408's knobs withdrawn; song 45's chorus floor no lower than its lift allows: design deaths under one in twenty", "the design (a check)"),
    "494": ("457 falls back at once when no entry and landing fit the strict copy", "printed"),
    "438": ("the chart's share of bars with two or more changes inside the kept middle half (or none, drawn at the kept rate), and of bars holding the last bar's chord inside its middle half", "kept 0-0.33; 0.08-0.44; none in 25% and 37% of songs"),
    "440": ("the bass on the root at nine changes in ten or more; a third or fifth with a step on one side; at most one chord in twelve", "the rule (a check)"),
    "464": ("song 45: deaths at 267 at or under v118's (267 reads the bridge G before its raise)", "v118 (songs/p50)"),
    "470": ("the content judge of record is the refit: its mean on complete builds, beside the v108 content", "kept median 1.97"),
    "471": ("the floor on the v108 judge; the share of complete builds under the refit's kept 5th percentile (-0.51) printed", "under a third on every song moves it"),
    "472": ("the pick: the refit's first among survivors with no soft break; each pick's rank under the other judge", "printed"),
    "473": ("the judge does not read a second verse", "the rule"),
    "456": ("the last-note test read on windows whose last note the walk chose (100 or more): between the collections' means or within a fifth of a sd of the nearer", "CoCoPops and BiMMuDa 1958-1991"),
})
TEST.update({
    "405": ("389 read on drawable lines: runs within ten points of the band's kept share where 200 onsets or more; song 45's rhythm deaths within two spreads of v116's (none)", "the kept table's bands; v116"),
    "409": ("the window's last note on the tonic between the collections' means (27.7%, 32.9%) or within a fifth of a sd of the nearer, where the endings are not designed; its sources printed", "CoCoPops and BiMMuDa 1958-1991"),
    "412": ("song 45: deaths at 267 within two spreads of v118's, the lift's failures under one in twenty", "v118 (songs/p50)"),
    "413": ("unit returns within ten points of the pooled kept rates on the free units; losses counted", "pooled kept"),
    "414": ("spans given up under one line in twenty", "the rule"),
    "415": ("verse 2 read on bars of equal syllables: half its bars or more read, the median share within ten points of 50% (main run)", "kept 50%"),
    "417": ("311 reads the last chorus; a designed tag printed apart", "the rule (a check)"),
    "419": ("no clash read on the chord at the note", "the rule (a check)"),
    "428": ("empty bars printed, not aimed, beside 378's slot share", "printed"),
})
def reading(k, r):
    x = r.get(k)
    if x is None: return ""
    if k == "470": return f"refit content: complete builds {x['refit_content_mean']}, survivors {x['survivors_refit_mean']} (v108 content {x['v108_content_mean']}; rank correlation {x['rank_correlation']})"
    if k == "471": return f"under the refit's kept 5th percentile {x['under_kept_5th']:.0%} of complete builds; floor deaths (v108) {x['floor_deaths_v108']}; {x['held']}"
    if k == "472": return f"pick {x['pick']}; v108's pick {x.get('v108_pick')} (rank under the refit {x.get('v108_pick_rank_under_refit')}); the refit's pick's rank under v108 {x.get('refit_pick_rank_under_v108')}; clean {x.get('clean')}"
    if k == "473": return x["note"]
    if k == "465": return (f"drawn {x['drawn']}, held {x['held_to_end']}, given up {x['given_up']}, no class {x['no_class']}, landing fixed {x['landing_fixed']}, entry given up {x['entry_given_up']}; spans given up {x['spans_given_up']} of {x['span_lines']}; widest class gap {x['widest_class_gap']}; "
                           + "; ".join(f"{k_}: {v_['classes']} (kept {v_['kept']}), 4+ beats {v_['four_beats_or_more']} (kept {v_['kept_four']})" for k_, v_ in x["by_notes"].items()))
    if k == "458": return "; ".join(f"{k_}: {v_['notes_a_second']} (kept {v_['kept']}, {v_['lines']} lines)" for k_, v_ in x["by_notes"].items()) + f"; tempo {x['tempo']}"
    if k == "478": return f"repeats verse 1 / verse 2 {x['repeat']}, steps {x['step']}; knobs {x['knobs']}" if "repeat" in x else x["note"]
    if k == "484": return f"pitch kept {x['pitch_kept']}; rate {x['rate']}" if "pitch_kept" in x else x["note"]
    if k == "476": return f"content mean {x['content_mean']}; under the kept 25th {x['under_kept_25th']}; under 1.53 - 1.645 sd {x['under_normal_5th']}"
    if k == "477": return f"pick {x['pick']}, score {x['score']}; check {x['check']}"
    if k == "486": return f"judged bands {x['bands_judged']}; last round {x['last_round']}"
    if k == "489": return f"knobs {x['knobs']}"
    if k == "490": return f"run weights {x['knobs']}; drawable runs (kept, (onsets, share)) {x['drawable_runs']}"
    if k == "491": return f"design deaths {x['design_deaths']}; survivors {x['survivors']}" if "design_deaths" in x else x["note"]
    if k == "494": return f"at once {x['at_once']}, at half {x['at_half']}; rhythm deaths {x['rhythm_deaths']}; joins {x['joins']}"
    if k == "438": return f"two or more {x['before']['two_or_more']} -> {x['after']['two_or_more']} (target {x['targets']['two_or_more']}), held bars {x['before']['holding']} -> {x['after']['holding']} (target {x['targets']['holding']}); edits {x['ops']}" if "after" in x else x["note"]
    if k == "440": return f"root at {x['root_share']:.1%} of {x['changes']} changes; inversions {x['inversions']} (a step beside each: {x['with_a_step']})" if "changes" in x else x["note"]
    if k == "456": return f"walked windows {x['walked_windows']}, on the tonic {x['walked_tonic']:.1%} (collections {x['collections']})"
    if k == "464": return f"deaths at 267 {x['deaths267']} (before {x['before']}, v118 {x['v118']})" if "deaths267" in x else x["note"]
    if k == "459": return f"share {x['share']}; bars read {x['bars_read']}; builds with no such bar {x['builds_with_no_bar']}; rate {x['rate']}" if "share" in x else x.get("note", "")
    if k == "405": return f"bands (kept, rate, drawable n/runs, no room or fell back, not drawn) {x['by_band']}; lines {x['lines']}; rhythm deaths {x['rhythm_deaths']} (before {x['rhythm_deaths_before']})"
    if k == "409": return f"on the tonic {x['last_note_tonic']:.1%} (collections {x['collections']}); walked {x['walked_share']:.0%}; by source (n, tonic) {x['by_source']}; knob {x['knob']}"
    if k == "412": return f"deaths at 267 {x['deaths267']} (v119 {x['v119']}, v118 {x['v118']}); with 267 read before the raise (450): {x['diag450']}; lift failures {x['lift_fails']}"
    if k == "413": return f"free units {x['free_units']}; losses {x['losses']}"
    if k == "414": return f"given up {x['given_up']} of {x['drawn_to_a_span'] + x['given_up']} ({x['given_up_share']:.1%}); median share {x['median_share_by_notes_drawn']}; {x['density']}"
    if k == "415": return f"share {x['share']}; bars read {x['bars_read']}; builds with no such bar {x['builds_with_no_bar']}; rate {x['rate']}" if "share" in x else x["note"]
    if k == "417": return f"{x['section_read']} on the tonic {x['last_chorus_tonic']:.1%}; tag {x['tag']}"
    if k == "419": return f"clashes {x['clashes']} of {x['notes_read']} (bar chord: {x['bar_chord_reading']}); by kind {x['by_kind']}; {x['examples'][:3]}"
    if k == "428": return f"empty bars {x['empty_bars']} (CoCoPops {x['cocopops']}, BiMMuDa {x['bimmuda']}); 378's slot share {x['slot_share_378']}; knob {x['knob']}"
    if k == "384": return f"{x['patches']}; smoke paths {x['smoke_paths']}"
    if k == "385": return f"outside the scale {x['outside_scale']:.1%} (kept {x['kept']:.1%}); cost {x['cost']}; placed {x['placed']}, wanting {x['wanting']}; passing {x['passing']}"
    if k == "386": return f"clashes {x['clashes']} of {x['notes_read']} notes read; moved {x['moved']}"
    if k == "387": return f"stop {x['stop']}; knobs {x['knobs']}"
    if k == "389": return f"bands {x['by_band']}; rhythm deaths {x['rhythm_deaths']} (before {x['before']}, v116 {x['v116']}); join deaths {x['join_deaths']}; fallbacks {x['fallbacks']}"
    if k == "390": return f"free units {x['free_units']}; rates {x['rates']}; plan {x['plan_given'] or 'none'}"
    if k == "391": return f"drawn lines {x['lines_drawn']}: median share {x['median_share_by_notes_drawn']}; under half of full {x['under_half_of_full']:.1%}; widened {x['widened']}; given up {x['given_up']} of {x['drawn_to_a_span'] + x['given_up']} ({x['given_up_share']:.1%})"
    if k == "392": return f"lift failures {x['lift_fails']}; drawn {x['drawn']}, pinned {x['pinned']}" if "lift_fails" in x else x["note"]
    if k == "393": return f"equal lines {x['equal_lines']}: share {x['share_equal']}; the rest {x['share_other']}; all lines {x['share_all']}" if "share_equal" in x else x["note"]
    if k == "394": return f"memory breaks {x['memory_breaks']} (before {x['before']}, v114 {x['v114']}); {x['stats']}"
    if k == "395": return f"lifted {x['lifted']}; {x['last_section']} on the tonic {x['last_chorus_tonic']:.1%}; tonic endings {x['tonic_endings']}"
    if k in ("354", "357", "365", "372") and "agreed_two" in x: return _reading0(k, r) + f"; on the agreed two (sixteenth, eighth): {x['agreed_two']}"
    if k in ("341", "343", "344", "346", "348", "349", "355", "356", "358", "366") and "both_collections" in x: return _reading0(k, r) + f"; both collections {x['both_collections']}"
    if k == "340": return f"gap {x['gap']} on the 30 agreed measures, both collections pooled; costliest {[(m, c) for m, c, _, _ in x['eight']]}"
    if k == "385" and "both_collections" in x: return f"outside the scale {x['outside_scale']:.1%} (CoCoPops 7.1%, BiMMuDa 3.8%); placed {x['placed']}, wanting {x['wanting']}; passing {x['passing']}"
    if k == "398": return f"chord tones {x['chord_tones']:.1%}, on a beat {x['on_beat']:.1%}, on a downbeat {x['on_downbeat']}; resolved by step {x['resolved_by_step']:.1%}; knobs {x['knobs']}"
    if k in ("399", "401") and "note" in x: return x["note"]
    if k == "399": return f"on the downbeat {x['shares']}; first line not drawn free {x['first_line_not_drawn_free']}; {x['stats']}"
    if k == "400": return f"verse {x['verse']}, chorus {x['chorus']} (kept 0.584); knob {x['knob']}"
    if k == "424": return f"aims {x['aims']}; knobs {x['knobs']}; {x['stats']}"
    if k in ("399", "401") and "note" in x: return x["note"]
    if k == "401": return f"distinct lengths {x['distinct_durations_median']} at the median; shortened {x['shortened']}; shorter than the palette {x['shorter_than_palette']}"
    if k in ("388", "396"): return x.get("note", "")
    return _reading0(k, r)
rows = []
for k in TEST:
    m = R[MODES[0]]; c = R[MODES[-1]]
    h = m[k].get("held") if k in m else None
    if isinstance(h, bool) and k in c and isinstance(c[k].get("held"), bool): h = h and c[k]["held"]          # held in the main run and the control
    rows.append((k, TEST[k][0], TEST[k][1], reading(k, m) if k in m else "", reading(k, c) if (k in c and len(MODES) > 1) else "", h))
json.dump(rows, open(f"/home/claude/p54/{OUTN}_table.json", "w"), indent=1, default=str)
for v in MODES: print(v, R[v]["runs"])
for k, t, ka, a, b, h in rows: print(f"{k} | {t} | {ka} | {a} | {b} | {h}")
for v in MODES:
    print("DQ", v); [print(f"  {k}: {x}  (before {R[v]['DQ']['before'][k] if R[v]['DQ']['before'] else '-'})") for k, x in R[v]["DQ"]["now"].items()]
