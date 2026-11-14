"""gen_l7_p58.py: writes melody_l7_p58.py (song 48 under Luthier v7: Module 27.88, Window 164) from melody_l6_p58.py, porting 730 to 736 with
luthier_judge5.py and luthier_v7_tables.json; 737, 738 and 739 are readings (read_l7.py). Every patch replaces whole statements and is asserted
to match exactly once. ZE_PART_L7=0 gives Luthier v6 as it stood.
- 730: the pick is luthier_judge5.pick over the clean survivors, as 715's was.
- 731: 653's kept line is drawn among kept lines of the cell whose first syllable's stress matches the line's (the table's lines whole; lines of
  unknown stress set aside; the whole cell where none match); a pickup may carry a stressed first syllable: in 680 the pickup then runs to the
  next stressed syllable, and in the old draw the first syllable may stand before the bar line.
- 732: 717 takes its turn before 651, at its rate; a bar that takes no kept figure goes to 651, which draws from every bar the song has sung.
- 733: while the window's repeats so far (the section's first eight bars: the lines placed, then this line's notes so far) stand at or over 713's
  ceiling, 717 draws only kept figures that repeat no note.
- 734: the unaimed builds of a calibration round are a hundred or more; the per-note reading is taken with its standard error; a raise counts
  when the reading rises by more than two standard errors of the difference; after two raises in turn that do not count the power returns to
  the last value that did (the starting power if none did) and stays.
- 735: 711's ratio is raised to the power Q735, set in the calibration by a one-dimensional search (a step up, reversed and narrowed when the
  gap grows) until drawn lines (two-bar slots, under 6.5 notes a bar) meet the build's capped palette within ten points for the sixteenth,
  eighth and quarter, read on the unaimed builds.
- 736: 308's cap binds drawn bars, not copied ones: 313 keeps a copied bar whatever its count, 680 takes it as a fixed bar, and the old draw's
  cap is raised to the count of a copied bar inside that bar."""
SRC = "/home/claude/p58/melody_l6_p58.py"; DST = "/home/claude/p58/melody_l7_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""Luthier v6 (Module 27.87; by gen_l6_p58.py''', '''"""Luthier v7 (Module 27.88; by gen_l7_p58.py from melody_l6_p58.py: 730-736) -- Luthier v6 (Module 27.87; by gen_l6_p58.py''')
P('''def ON22(f_): return PL6.get(f_, 0) <= VL6 and f_ not in OFF11''', '''def ON22(f_): return PL6.get(f_, 0) <= VL6 and f_ not in OFF11
VL7 = int(_os11.environ.get("ZE_PART_L7", "1"))
PL7 = {f_: 1 for f_ in ("730", "731", "732", "733", "734", "735", "736")}
def ON23(f_): return PL7.get(f_, 0) <= VL7 and f_ not in OFF11''')
# ---- tables and helpers ----
P('''_z711 = sum(MEANPAL606[0][c_] for c_ in _N655)''', '''import luthier_judge5 as J5
_T7 = json.load(open("/home/claude/p58/tables/luthier_v7_tables.json"))
KL731 = _T7[next(k_ for k_ in _T7 if k_.startswith("731: lines whole"))]
Q735 = [1.0]; STEP735 = [1.6]; DIR735 = [1]; PREV735 = [None]; HIST735 = []; POWH734 = []; STOP734 = [None]; GOOD734 = [None]; MISS734 = [0]; CUR733 = [None]
def read735(c):
    """735: drawn lines in two-bar slots under 6.5 notes a bar: the gaps sung (sixteenth, eighth, quarter) and the build's capped palette's shares."""
    pal_ = next((x_ for x_ in PALS606 if x_["song"] == c["meta"].get("palette606")), None)
    if pal_ is None: return None
    byl_ = collections.defaultdict(list); sg_ = np.zeros(3); px_ = np.zeros(3); N_ = 0
    for n_ in c["notes"]: byl_[n_["line"]].append(n_["on"])
    for l_, v_ in byl_.items():
        s_, i_ = l_.split(":"); i_ = int(i_); kd_ = c["meta"]["kinds"].get((s_, i_))
        if slot_len(s_, i_) != 2 or kd_ not in ("fresh", "fresh (361 unit return)", "sung again") or len(v_) < 3: continue
        v_ = sorted(v_); x_ = len(v_) / 2
        if x_ >= 6.5: continue
        cp_ = cap655(pal_["gap classes, shares"], "two-bar", cell600(x_)); z_ = sum(cp_[c2_] for c2_ in (0, 2, 3, 4, 5, 6)) or 1
        g_ = np.diff(v_)
        for k_, (gv_, ci_) in enumerate(((3, 0), (6, 2), (12, 4))): sg_[k_] += float(np.sum(g_ == gv_)); px_[k_] += cp_[ci_] / z_ * len(g_)
        N_ += len(g_)
    return sg_, px_, N_
_z711 = sum(MEANPAL606[0][c_] for c_ in _N655)''')
# ---- 731: the kept line by the first syllable's stress; a stressed pickup ----
P('''        c_ = cell600(len(LINES[sec_][i_]) * MEL504[0] / max(1, slot_len(sec_, i_))); e_, sp_, br_, sl_, nn_ = rng_.choice(KL653[c_])''',
  '''        c_ = cell600(len(LINES[sec_][i_]) * MEL504[0] / max(1, slot_len(sec_, i_)))
        if ON23("731"):                                                                     # 731: among kept lines of the cell whose first syllable's stress matches
            st7_ = 1 if LINES[sec_][i_][0][1] else 0; pool7_ = [r_ for r_ in KL731.get(c_, []) if r_[5] == st7_]
            if not pool7_: pool7_ = [r_ for r_ in KL731.get(c_, []) if r_[5] >= 0] or [list(x_) + [-1] for x_ in KL653[c_]]; STATS["731: no kept line of the cell with the stress; the cell"] += 1
            e_, sp_, br_, sl_, nn_ = rng_.choice(pool7_)[:5]; STATS["731: kept line drawn by the first syllable's stress (" + ("stressed" if st7_ else "unstressed") + ")"] += 1
        else: e_, sp_, br_, sl_, nn_ = rng_.choice(KL653[c_])''')
P('''    n = len(sy); e = kl["e"] if kl else 0; Lt = kl["last"] if kl else None; fixed = fixed or {}
    if st[0] and e < 0: e = 0
    pk = []
    if e < 0 and 0 not in fixed:
        full_ = list(range(e, 0, 6)); c_ = 0
        while c_ < n and not st[c_]: c_ += 1''',
  '''    n = len(sy); e = kl["e"] if kl else 0; Lt = kl["last"] if kl else None; fixed = fixed or {}
    if st[0] and e < 0 and not ON23("731"): e = 0                                             # 731: a pickup may carry a stressed first syllable
    pk = []
    if e < 0 and 0 not in fixed:
        full_ = list(range(e, 0, 6)); c_ = 1 if (ON23("731") and st[0]) else 0               # 731: a stressed opening's pickup runs to the next stress
        while c_ < n and not st[c_]: c_ += 1''')
P('''            if st[0] and t < 0: continue''', '''            if st[0] and t < 0 and not ON23("731"): continue                             # 731: the first syllable may stand before the bar line''')
# ---- 736: the cap binds drawn bars ----
P('''        for bb, ts in copybars.items():
            if len(ts) <= cap: allowed[bb] = ts''', '''        for bb, ts in copybars.items():
            if len(ts) <= cap or ON23("736"):                                                 # 736: a copied bar whatever its count
                allowed[bb] = ts
                if len(ts) > cap: STATS["736: copied bar over 308's cap kept"] += 1''')
P('''                        if c <= cap: acc[c] += a_ * tw(tp, k, d)''', '''                        if c <= (CAPB736.get(t // BAR, cap) if ON23("736") else cap): acc[c] += a_ * tw(tp, k, d)   # 736: a copied bar's own count''')
P('''    G = [t for t in range(-12, end + 1, step) if tmin <= t <= end]
    runs_ok =''', '''    CAPB736 = {bb_: max(cap, len(ts_)) for bb_, ts_ in (copybars or {}).items()}               # 736
    G = [t for t in range(-12, end + 1, step) if tmin <= t <= end]
    runs_ok =''')
P('''            if any(x_ > cap or (x_ not in KB652 and b_ not in fixed) for b_, x_ in enumerate(c_)): continue''',
  '''            if any((x_ > cap and not (ON23("736") and b_ in fixed)) or (x_ not in KB652 and b_ not in fixed) for b_, x_ in enumerate(c_)): continue   # 736''')
# ---- 735: the ratio to a power ----
P('''        if ON22("711") and cp680_ is not None: palw_ = lambda g_: max(0.005, cp680_[LR605.gclass(g_)]) / KMP711[LR605.gclass(g_)]''',
  '''        if ON22("711") and cp680_ is not None: palw_ = lambda g_: (max(0.005, cp680_[LR605.gclass(g_)]) / KMP711[LR605.gclass(g_)]) ** (Q735[0] if ON23("735") else 1.0)   # 735: to a power''')
# ---- 732, 733: kept figures first, under the ceiling ----
P('''                tk651_ = False
                if FIGS651[0].get(len(ix_)):''', '''                tk651_ = False
                if ON23("732") and KF717.get(len(ix_)):                                         # 732: 717 first, at its rate
                    STATS["717: bars eligible (three notes or more, before 651)"] += 1
                    if rng.random() < R717[0]:
                        rw_ = KF717[len(ix_)]
                        if ON23("733") and CUR733[0] is not None:                               # 733: under the ceiling, only kept figures that repeat no note
                            w0_, w1_, cl_ = CUR733[0]; ps_ = sorted([(o_, p_) for o_, p_ in PL651 if w0_ <= o_ < w1_] + [(notes[j]["on"], out[j]) for j in range(len(out)) if w0_ <= notes[j]["on"] < w1_])
                            q_ = [p_ for _, p_ in ps_]; rp_ = float(np.mean(np.diff(q_) == 0)) if len(q_) >= 2 else 0.0
                            if rp_ >= cl_ and w0_ <= notes[i]["on"] < w1_:
                                rw2_ = [r_ for r_ in rw_ if 0 not in r_[0]]; STATS["733: window at or over the ceiling: kept figures without a repeat"] += 1
                                if rw2_: rw_ = rw2_
                        fg_ = rng.choices([f_ for f_, _, _ in rw_], [c_ for _, c_, _ in rw_])[0]
                        qs_ = plc651_(tuple(fg_))
                        if qs_ is not None: fig_.update({j: q_ for j, q_ in zip(ix_, qs_)}); STATS["717: bar takes a kept figure"] += 1; tk651_ = True
                        else: STATS["717: kept figure drawn but not placeable on the chord"] += 1
                if FIGS651[0].get(len(ix_)) and not tk651_:''')
P('''                if ON22("717") and not tk651_ and KF717.get(len(ix_)):''', '''                if ON22("717") and not ON23("732") and not tk651_ and KF717.get(len(ix_)):''')
P('''        REP683[0] = (KREP683[SEC_BAND[sec]]["75th"] if ON22("713")''', '''        CUR733[0] = (BAR0[sec] * BAR, (BAR0[sec] + 8) * BAR, KREP683[SEC_BAND[sec]]["75th"])          # 733: the window and its ceiling
        REP683[0] = (KREP683[SEC_BAND[sec]]["75th"] if ON22("713")''')
# ---- calibration: 734, 735 ----
P('''        while k2 < n and t2 < 40 * n:''', '''        n2_ = max(n, 100) if ON23("734") else n                                             # 734: a hundred unaimed builds a round or more
        while k2 < n2_ and t2 < 40 * n2_:''')
P('''            if ON22("717"):
                f7_ = read717(c2["notes"])''', '''            if ON23("735"):
                r7_ = read735(c2)
                if r7_ is not None: ua["_s735"].append(r7_[0]); ua["_p735"].append(r7_[1]); ua["_n735"].append(r7_[2])
            if ON22("717"):
                f7_ = read717(c2["notes"])''')
P('''                if ON22("713"):                                                              # 713: the power stops''', '''                if ON23("734"):                                                              # 734: the stop in standard errors
                    e7_ = np.array([x_ for x_ in ua["_e650a"] if np.isfinite(x_)]); se_ = float(np.std(e7_, ddof=1) / np.sqrt(len(e7_))) if len(e7_) > 1 else float("nan")
                    POWH734.append(dict(round=CAL_ROUNDS[0], power=round(POW650[0], 4), read=round(r_, 4), se=round(se_, 4), builds=len(e7_)))
                    if GOOD734[0] is None: GOOD734[0] = POW650[0]
                    if STOP734[0] is None and len(POWH734) >= 2 and POWH734[-1]["power"] > POWH734[-2]["power"]:
                        d7_ = r_ - POWH734[-2]["read"]; sd7_ = float(np.hypot(se_, POWH734[-2]["se"]))
                        if d7_ > 2 * sd7_: GOOD734[0] = POW650[0]; MISS734[0] = 0; POWH734[-1]["raise"] = "counts"
                        else: MISS734[0] += 1; POWH734[-1]["raise"] = "does not count"
                        if MISS734[0] >= 2:
                            STOP734[0] = CAL_ROUNDS[0]; print(f"734: two raises in turn that do not count; the power returns to {GOOD734[0]:.3f} (round {CAL_ROUNDS[0]})")
                    if STOP734[0] is not None: POW650[0] = GOOD734[0]; f_ = 1.0
                    row["734: power rounds (round, power, reading, standard error, builds)"] = [dict(x_) for x_ in POWH734]
                if ON22("713") and not ON23("734"):                                         # 713: the power stops''')
P('''                if f_ in (0.6, 1.6) and STOP650[0] is None: full_now.add("pow650")''', '''                if f_ in (0.6, 1.6) and STOP650[0] is None and STOP734[0] is None: full_now.add("pow650")''')
P('''            if ON22("717") and ua.get("_f717"):                                               # 717: the rate toward 56%''', '''            if ON23("735") and ua.get("_n735") and sum(ua["_n735"]) > 0:                          # 735: the palette's power, toward the palette class by class
                S7_ = np.sum(ua["_s735"], axis=0) / sum(ua["_n735"]); X7_ = np.sum(ua["_p735"], axis=0) / sum(ua["_n735"]); dv_ = float(np.max(np.abs(S7_ - X7_)))
                HIST735.append(dict(round=CAL_ROUNDS[0], power=round(Q735[0], 4), sung=[round(x_, 3) for x_ in S7_], palette=[round(x_, 3) for x_ in X7_], largest_gap=round(dv_, 3)))
                if dv_ > 0.10:
                    if PREV735[0] is not None and dv_ >= PREV735[0]: DIR735[0] *= -1; STEP735[0] = float(np.sqrt(STEP735[0]))
                    Q735[0] = float(np.clip(Q735[0] * STEP735[0] ** DIR735[0], 0.25, 8.0)); full_now.add("q735")
                PREV735[0] = dv_; row["735 (power; sung / palette: sixteenth, eighth, quarter; largest gap)"] = HIST735[-1]
            if ON22("717") and ua.get("_f717"):                                               # 717: the rate toward 56%''')
# ---- 730: the pick ----
P('''        pk715_, R715_ = J4.pick([(c_["fp"], [(n_["on"], n_["p"], n_["sec"]) for n_ in c_["notes"]]) for c_ in cl715_])''',
  '''        pk715_, R715_ = (J5 if ON23("730") else J4).pick([(c_["fp"], [(n_["on"], n_["p"], n_["sec"]) for n_ in c_["notes"]]) for c_ in cl715_])   # 730: luthier_judge5''')
P('''                                          components={k_: round(v_, 4) for k_, v_ in r_["components"].items()}) for i_, r_ in RD_.items()})''',
  '''                                          components={k_: round(v_, 4) for k_, v_ in r_["components"].items()}, eligible715=r_.get("eligible under 715"),
                                          window=r_.get("most-repeating window, place for its density"), windows=r_.get("windows: label, notes a bar, repeats, place")) for i_, r_ in RD_.items()})''')
P('''    rerun["l6_part"] = VL6;''', '''    rerun["l7_part"] = VL7; rerun["l7_on"] = sorted(f_ for f_ in PL7 if ON23(f_)); rerun["q735"] = round(Q735[0], 4); rerun["hist735"] = list(HIST735); rerun["pow734"] = list(POWH734)
    rerun["stop734"] = STOP734[0]; rerun["l7_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("730:", "731:", "732:", "733:", "734:", "735:", "736:", "717:", "651:", "712:", "714:", "680:", "682:", "313:", "323:")}
    rerun["l6_part"] = VL6;''')
P('''cmd=f"ZE_PART_L6={VL6} PYTHONHASHSEED=0 python3 melody_l6_p58.py {N} {MODE}"''', '''cmd=f"ZE_PART_L7={VL7} PYTHONHASHSEED=0 python3 melody_l7_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/runl6/melody_l6_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/runl7/melody_l7_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
