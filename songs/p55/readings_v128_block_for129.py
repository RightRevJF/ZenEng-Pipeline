# ---- v128 Run 3 (exec'd after the v127 block): 465, 458, 478, 484, 476/477, 486, 489, 490, 491, 494 ----
KL8 = json.load(open("/home/claude/p55/tables/zeneng_v128_kept_lines.json"))
K465 = KL8["465: where a kept line's last onset falls before the next line, by notes in the line"]
K458 = KL8["458: syllables a second across a kept line's sung span, by notes in the line"]
KCL = "the last onset's bar, counted back from the bar in which the next line begins (0 = the same bar, 1 = the bar before, 2, 3 or more): share of lines"
def nb8(n_): return "3 to 5" if n_ <= 5 else "6 to 8" if n_ <= 8 else "9 to 12" if n_ <= 12 else "13 and over"
cls8 = collections.defaultdict(collections.Counter); gap8 = collections.defaultdict(list); rate8 = collections.defaultdict(list)
SPT = P.M.SEC_PER_TW
for b in [b for b in D["every"] if not b.get("partial")][:400]:
    Lm = collections.OrderedDict()
    for t in sorted(b["notes"]): Lm.setdefault(t[4], []).append(t)
    ks_ = list(Lm)
    for a_, c_ in zip(ks_, ks_[1:]):
        A_, B_ = Lm[a_], Lm[c_]
        if len(A_) < 3 or A_[0][3] != B_[0][3] or (B_[0][0] - A_[0][0]) / 12 > 16: continue
        k_ = nb8(len(A_)); cls8[k_][min(3, B_[0][0] // 48 - A_[-1][0] // 48)] += 1; gap8[k_].append((B_[0][0] - A_[-1][0]) / 12)
        sp_ = (A_[-1][0] + A_[-1][1] - A_[0][0]) * SPT
        if sp_ > 0: rate8[k_].append(len(A_) / sp_)
r465 = {}
for k_ in ("3 to 5", "6 to 8", "9 to 12", "13 and over"):
    n_ = sum(cls8[k_].values())
    if not n_: continue
    r465[k_] = dict(lines=n_, classes=[round(cls8[k_][j] / n_, 3) for j in range(4)], kept=[K465[k_][KCL][x] for x in ("0", "1", "2", "3 or more")],
                    beats_to_next=pct(gap8[k_], (25, 50, 75)), kept_beats=K465[k_]["beats from the last onset to the next line's first onset (5, 25, 50, 75, 95)"][1:4],
                    four_beats_or_more=round(float(np.mean(np.array(gap8[k_]) >= 4)), 3), kept_four=K465[k_]["share with a whole bar or more between (4 beats or more)"])
drawn465 = sum(v_ for k_, v_ in st.items() if k_.startswith("465: class ") and k_.endswith(" drawn"))
gu465 = st.get("465: class given up for a line", 0); gu378 = st.get("378: span given up (nothing fitted inside it)", 0)
sp378 = st.get("378: lines drawn to a span", 0)
far465 = max((max(abs(a - b) for a, b in zip(x_["classes"], x_["kept"])) for x_ in r465.values() if x_["lines"] >= 200), default=None)
r["465"] = dict(by_notes=r465, drawn=drawn465, held_to_end=st.get("465: line ends in its drawn bar", 0), given_up=gu465, no_class=st.get("465: no class the slot allows", 0),
                landing_fixed=st.get("465: landing fixed elsewhere, class not held", 0), entry_given_up=st.get("465: the entry asked for given up", 0),
                spans_given_up=gu378, span_lines=sp378 + gu378, opt=D["rerun"].get("opt465"), widest_class_gap=far465,
                held=bool(drawn465 and gu465 / max(1, drawn465) < 0.05 and gu378 / max(1, sp378 + gu378) < 0.05))
r458 = {}
for k_ in ("3 to 5", "6 to 8", "9 to 12", "13 and over"):
    if len(rate8[k_]) < 20: continue
    q_ = K458[k_]["notes a second, first onset to the end of the last note (5, 25, 50, 75, 95)"]
    r458[k_] = dict(lines=len(rate8[k_]), notes_a_second=pct(rate8[k_], (25, 50, 75)), kept=q_[1:4])
r["458"] = dict(by_notes=r458, read=st.get("458: span read against the kept rate by notes", 0), tempo=P.M.QBPM,
                held=bool(r458 and all(x_["kept"][0] <= x_["notes_a_second"][1] <= x_["kept"][2] for x_ in r458.values() if x_["lines"] >= 200)))
# 478 and 484: verse 2 against verse 1, build by build (the same windows as Window 147's pair)
rp8, st8, pk8 = [], [], []
for b in [b for b in D["every"] if not b.get("partial")][:400]:
    if "Verse 2" not in P.SUNG: break
    ns_ = nts(b); w1_, w2_ = P.win_tp(ns_, "Verse 1"), P.win_tp(ns_, "Verse 2")
    if len(w1_) < 12 or len(w2_) < 12: continue
    a1_, a2_ = np.abs(np.diff([x[1] for x in w1_])), np.abs(np.diff([x[1] for x in w2_]))
    rp8.append(((a1_ == 0).mean(), (a2_ == 0).mean())); st8.append((((a1_ > 0) & (a1_ <= 2)).mean(), ((a2_ > 0) & (a2_ <= 2)).mean()))
    pk_ = P.pair122(w1_, w2_)["pitch_kept"]
    if np.isfinite(pk_): pk8.append(pk_)
k8 = D["rerun"].get("knobs128") or {}
if rp8:
    rv1, rv2 = np.mean([x[0] for x in rp8]), np.mean([x[1] for x in rp8]); sv1, sv2 = np.mean([x[0] for x in st8]), np.mean([x[1] for x in st8])
    r["478"] = dict(repeat=(round(float(rv1), 3), round(float(rv2), 3)), step=(round(float(sv1), 3), round(float(sv2), 3)), knobs=(k8.get("rep478"), k8.get("stp478")),
                    moved_off_repeats=st.get("434: a repeat the source did not sing, moved", 0), held=bool(abs(rv2 - rv1) <= 0.05 and abs(sv2 - sv1) <= 0.05))
    r["484"] = dict(pitch_kept=round(float(np.mean(pk8)), 3) if pk8 else None, rate=k8.get("k435"), kept=(0.72, 0.79),
                    held=bool(pk8 and 0.72 <= np.mean(pk8) <= 0.79))
else:
    r["478"] = dict(note="no second verse", held="n/a"); r["484"] = dict(note="no second verse", held="n/a")
# 476/477: the v128 judge's content score; the pick's score the mean of content and order
rc8 = np.array([c["judge"]["refit_content"] for c in D["every"] if c.get("judge") and "refit_content" in c["judge"]])
r["476"] = dict(table="zeneng_v128_judge.json", content_mean=round(float(rc8.mean()), 3) if len(rc8) else None, under_kept_25th=round(float(np.mean(rc8 < 0.23)), 3) if len(rc8) else None,
                under_normal_5th=round(float(np.mean(rc8 < 1.53 - 1.645 * 2.0)), 3) if len(rc8) else None, kept="mean 1.53, sd 2.0, 25th percentile 0.23 (no 5th percentile given)", held="printed")
pk_ = D.get("pick")
r["477"] = dict(pick=pk_["fp"] if pk_ else None, score=round(pk_["judge"]["refit_combined"], 3) if pk_ and "refit_combined" in pk_["judge"] else None,
                check=bool(pk_ and abs(pk_["judge"]["refit_combined"] - np.mean([(pk_["judge"]["refit_content"]), pk_["judge"]["order"]])) < 1e-6) if pk_ and "refit_combined" in pk_["judge"] else None,
                note="score = the mean over the windows of (content + order) / 2; the check compares it with (mean content + mean order) / 2, equal when both windows are read", held="printed")
# 486: 389's rates read on the judged sections
cal8 = D.get("calibration") or []
r["486"] = dict(bands_judged=sorted({P.SEC_BAND[s_] for s_ in ("Verse 1", "Chorus 1")}), last_round=(cal8[-1].get("389 (band: kept, unaimed reading, rate)") if cal8 else None), held="printed")
# 489, 490: the band knobs
r["489"] = dict(knobs=k8.get("b489"), last_round=(cal8[-1].get("489 (kept, unaimed reading, knob)") if cal8 else None), held="read in the reread, by density band")
r["490"] = dict(knobs=k8.get("r490"), drawable_runs={b_: (x_["kept"], x_["drawable"]) for b_, x_ in r["405"]["by_band"].items()}, held=r["405"]["held"])
# 491: song 45's lift; 494: 457's fallback
r["491"] = (dict(design_deaths=sum(v_ for k_, v_ in D["deaths"].items() if k_.startswith("design")), survivors=D["survivors"], held=bool(sum(v_ for k_, v_ in D["deaths"].items() if k_.startswith("design")) < 50))
            if SONG_ == "45" else dict(note="467's and 408's knobs withdrawn (all songs); the floor is song 45's", held="n/a"))
r["494"] = dict(at_once=st.get("494: unit-return line falls back at once (no entry and landing fit)", 0), at_half=st.get("457: unit-return line falls back to the weighted copy", 0),
                rhythm_deaths=D["deaths"].get("rhythm: no placement", 0), joins=dict((k_, v_) for k_, v_ in D["deaths"].items() if "join" in k_ or "breath" in k_), held="printed")
# 438, 440 (Part 2): the chart drawn, and the bass at the change
c438 = D["rerun"].get("chart438")
if c438:
    kq2, kqh = c438["kept"]["two_or_more"], c438["kept"]["holding"]; a438 = c438["after"]
    ok2 = (a438["two_or_more"] == 0 and c438["targets"]["none_drawn"]) or (kq2[0] <= a438["two_or_more"] <= kq2[1] and a438["two_or_more"] > 0)
    r["438"] = dict(before=c438["before"], after=a438, targets=c438["targets"], kept=c438["kept"], ops=len(c438["ops"]), held=bool(ok2 and kqh[0] <= a438["holding"] <= kqh[1]))
    H2_ = D.get("chords2") or []; B8_ = D.get("bass8") or {}
    def bpc_(c_): return B8_.get(c_, P.M.CH[c_][0])
    ch_ = [(h_, c_) for h_, c_ in enumerate(H2_) if h_ == 0 or c_ != H2_[h_ - 1]]
    inv_ = [(j_, h_, c_) for j_, (h_, c_) in enumerate(ch_) if c_ in B8_]
    def bm_(a_, b_): d_ = (b_ - a_) % 12; return d_ if d_ <= 6 else d_ - 12
    stp_ = [any(abs(bm_(bpc_(ch_[j_ + d_][1]), bpc_(c_))) in (1, 2) for d_ in (-1, 1) if 0 <= j_ + d_ < len(ch_)) for j_, h_, c_ in inv_]
    rs_ = 1 - len(inv_) / max(1, len(ch_))
    r["440"] = dict(changes=len(ch_), inversions=[c_ for _, _, c_ in inv_], root_share=round(rs_, 3), with_a_step=stp_, held=bool(rs_ >= 0.9 and all(stp_) and len(inv_) <= len(ch_) / 12))
else:
    r["438"] = dict(note="the song's own chart (Part 2 draws it)", held="n/a"); r["440"] = dict(note="the root at every change (the chart's own)", held="n/a")
