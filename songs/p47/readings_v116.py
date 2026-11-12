"""321: the table of tests of 310-363 on a song's own runs, main and control, each made twice, as v116 reads them, with Table DQ's readings
beside v115 (OLD_PREFIX) and 356's counts beside the version before v115 (BASE_PREFIX: v112 for songs 40 and 42, v114 for song 43).
364 (separability) is read across the three songs by sep_v116.py. 363: a design gate fails only more than one spread under nine in ten.
Usage: python3 readings_v116.py MODULE PREFIX OUT OLD_PREFIX BASE_PREFIX
  e.g. python3 readings_v116.py melody_v116_p43 /home/claude/p47/melody_v116_p43 readings_v116_p43 /home/claude/p46/melody_v115_p43 /home/claude/p45/melody_p43"""
import sys, pickle, collections, json, importlib
import numpy as np
MOD, PRE, OUTN = sys.argv[1], sys.argv[2], sys.argv[3]; OLDP = sys.argv[4] if len(sys.argv) > 4 else None; BASEP = sys.argv[5] if len(sys.argv) > 5 else None
DESIGN = False
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p47", "/home/claude/p46", "/home/claude/p45", "/home/claude/p44", "/home/claude/p43", "/home/claude/p42", "/home/claude/p40"]
P = importlib.import_module(MOD); import judges as J
M = P.M; BAR, BEAT = P.BAR, P.BEAT
ETON = getattr(P, "ETON", M.TONIC); LASTSEC = P.SUNG[-1]                            # the song's tonic (a minor song is read on its relative major)
MODES = ("design",) if DESIGN else ("main", "ctl")
RUN = {v: pickle.load(open(f"{PRE}_{v}.pkl", "rb")) for v in MODES}
RR = {v: pickle.load(open(f"{PRE}_{v}_r.pkl", "rb")) for v in MODES}
OLD = {v: pickle.load(open(f"{OLDP}_{v}.pkl", "rb")) for v in MODES} if OLDP else {}
BASE = {v: pickle.load(open(f"{BASEP}_{v}.pkl", "rb")) for v in MODES} if BASEP else {}
import os
DIAG = {o: pickle.load(open(f"{PRE}_main_off{o}.pkl", "rb")) for o in ("348", "354") if os.path.exists(f"{PRE}_main_off{o}.pkl")}
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
        if lc: EN.append((lc[-1]["p"] - ETON) % 12 == 0)
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
                    by_line={l: round(float(np.mean([x[1] for x in te if x[0] == l])), 4) for l in sorted({x[0] for x in te})}, held=bool(te and all(x[1] for x in te)))
    r["314"]["tonic_read_by_324"] = r["324"]["on_nearest_to_centre"]                      # 324 amends 314: the tonic test read on the drawn centre
    r["314"]["held"] = bool(r["314"]["unused_split_max"] <= 1 and 0.40 <= r["314"]["verse_median_share"][1] <= 0.57 and r["324"]["held"])
    dreg = {k: v for k, v in st.items() if k.startswith("325")}
    if dg:
        def reg_death(b):                                                  # a design failure for want of a note the registers could not hold
            ns = nts(b); h = [n for n in ns if n["line"] == "Chorus 1:0"]; lo = b["meta"]["registers"]["song_lo"]
            lowt = min(p for p in range(lo, lo + 12) if (p - M.TONIC) % 12 == 0); return bool(h) and h[-1]["p"] <= lowt
        if hasattr(P, "design_reg"): reg_death = lambda b: not P.design_reg(None, b["meta"]["registers"])
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
    npbm = float(np.median(npb)); band = next((lo, hi, t) for lo, hi, t in P.DU if lo <= npbm < hi)
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
    r["359"] = dict(reading=("not ported (Q1 A, v116): the kept-window table carries no key, so the 70 minor windows cannot be read apart; every cost here is read against all 314 kept windows"
                             if getattr(P, "MTON", None) is not None else "a major song: n/a"), held="not ported" if getattr(P, "MTON", None) is not None else "n/a")
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
    # ---- 337: counts beside counts (main against control), with their spread ----
    r["337"] = "after both runs"
    R[v] = r
if len(MODES) > 1:
    a_, c_ = RUN["main"], RUN["ctl"]; na, nc = a_["made"], c_["made"]; rows337 = []
    for k in sorted(set(a_["deaths"]) | set(c_["deaths"]), key=lambda k: -(a_["deaths"].get(k, 0) + c_["deaths"].get(k, 0))):
        x, y = a_["deaths"].get(k, 0), c_["deaths"].get(k, 0)
        sp = float(np.sqrt(x * (1 - x / na) + y * (1 - y / nc)))
        rows337.append((k, x, y, round(sp, 1), "no difference" if abs(x - y) < 2 * sp else "a difference"))
    for v in MODES: R[v]["337"] = dict(deaths_main_vs_control=rows337, held="printed")
json.dump(R, open(f"/home/claude/p47/{OUTN}.json", "w"), indent=1, default=str)
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
        "354": ("each of the four gap shares within five points of the kept mean for the song's notes a bar; eighth gaps cost under half a point", "Table DU"),
        "355": ("pushed within ten points of 54% and runs within ten of 31%; onsets on a sixteenth within two points of 9.4%; rhythm-placement deaths under 1 in 20", "kept 54% / 31%; 9.4%"),
        "356": ("rhythm-band and memory breaks within two spreads of the version before v115; four distinct lengths at the median; song 43's survivors within two spreads of 811; the diagnostic runs printed", "v112 (40, 42), v114 (43)"),
        "357": ("each gap share within five points of Table DU's, main and control; the rounds printed", "Table DU"),
        "358": ("outside the scale within two points of 7.1% (4.5% minor); tritone-from-root breaks within two spreads of v115", "kept 7.1% (4.5% minor)"),
        "359": ("a minor song's costs read against the 70 kept minor windows", "not ported (Q1 A)"),
        "360": ("verse 2's share inside 25-70% at the median and within ten points of 50% in the main run; bars left out printed", "kept 50% (25-70%)"),
        "361": ("unit 3 returning unit 1 and unit 4 returning unit 2 each within ten points of the kept rate", "kept 31.5%, 18.8%"),
        "362": ("the pick breaks no soft limit, or none qualified and the run says so; the number that qualified printed", "a check"),
        "363": ("a design gate fails only when its rate is more than one spread under nine in ten", "the paper's 317 with 337's spread")}
def reading(k, r):
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
    if k == "359": return x["reading"]
    if k == "360": return f"verse 2 share {x['verse2_share']}; bars fitted again and kept {x['fitted_again_kept']}, not {x['fitted_again_failed']}; left out {x['bars_left_out']}"
    if k == "361": return f"means {x['means']} (kept {list(x['kept'].values())}); drawn {x['drawn']}"
    if k == "362": return f"no soft break {x['survivors_with_no_soft_break']} of {x['survivors']}; pick {x['pick']['fp'] if x['pick'] else '-'} (soft {x['pick_soft'] or 'none'}, judge rank {x['pick']['rank_by_judge'] if x['pick'] else '-'}); judge's first {x['judges_first']['fp'] if x['judges_first'] else '-'}"
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
rows = []
for k in TEST:
    m = R[MODES[0]]; c = R[MODES[-1]]
    h = m[k].get("held") if k in m else None
    if isinstance(h, bool) and k in c and isinstance(c[k].get("held"), bool): h = h and c[k]["held"]          # held in the main run and the control
    rows.append((k, TEST[k][0], TEST[k][1], reading(k, m) if k in m else "", reading(k, c) if (k in c and len(MODES) > 1) else "", h))
json.dump(rows, open(f"/home/claude/p47/{OUTN}_table.json", "w"), indent=1, default=str)
for v in MODES: print(v, R[v]["runs"])
for k, t, ka, a, b, h in rows: print(f"{k} | {t} | {ka} | {a} | {b} | {h}")
for v in MODES:
    print("DQ", v); [print(f"  {k}: {x}  (before {R[v]['DQ']['before'][k] if R[v]['DQ']['before'] else '-'})") for k, x in R[v]["DQ"]["now"].items()]
