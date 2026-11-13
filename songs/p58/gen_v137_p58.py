"""gen_v137_p58.py: writes melody_v137_p58.py (song 48 under ZenEng v137, Module 27.81, Window 157) from melody_v136_p58.py, porting in one
pass 600, 601, 602 and 603 (604 is a reading: read_v137.py), with zeneng_v137_span.json. Every patch replaces whole statements and is
asserted to match exactly once. ZE_PART137=0 gives v136 as it stood; ZE_OFF switches a fix off (side runs only).
- 600 (amends 578): a drawn line draws its span (first onset to last, as a share of its slot) from the kept quartiles of its slot-rate cell
  (under 3.5, 3.5-4.5, 4.5-5.5, 5.5-6.5, 6.5-7.5, 7.5 and over; the two-bar-slot tables for two-bar slots), then its gaps from that cell's
  values and runs to fill it. The span is drawn from the piecewise-linear distribution through the kept quartiles (tails one interquartile
  range out); the rhythm is drawn again from the same table until its first-to-last onset lies within a sixteenth of the drawn span (half
  the tries, then given up and counted). The drawn span stands in place of 378's for these lines.
- 601 (amends 579): the ending class of a line of 13 notes and over is drawn at the rate the drawn span gives it.
- 602 (amends 424; the writer's ruling over 262): the window's last note is the tonic at the kept share for the chord under it (39% where
  the tonic is a tone of that chord, 19% where not), drawn, excused from 398's chord-tone weight; 424's knob no longer touches it. Where the
  window's last line returns a line of its own section, the weight goes on the source line's last note, read against the chord under the
  return's. 262's rule that the first verse ends off the tonic is lifted for that note only. Designed lines are left alone.
- 603: in lines at 5.5 notes to the slot's bar and over, a leap past a fifth is held to 2% of a move's weight."""
SRC = "/home/claude/p58/melody_v136_p58.py"; DST = "/home/claude/p58/melody_v137_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""ZenEng v136 (Module 27.80; by gen_v136_p58.py''', '''"""ZenEng v137 (Module 27.81; by gen_v137_p58.py from melody_v136_p58.py: 600-603) -- ZenEng v136 (Module 27.80; by gen_v136_p58.py''')
P('''def ON16(f_): return P136.get(f_, 0) <= V136 and f_ not in OFF11
''', '''def ON16(f_): return P136.get(f_, 0) <= V136 and f_ not in OFF11
V137 = int(_os11.environ.get("ZE_PART137", "1"))
P137 = {f_: 1 for f_ in ("600", "601", "602", "603")}
def ON17(f_): return P137.get(f_, 0) <= V137 and f_ not in OFF11
''')
# ---- the tables of 600 ----
P('''        RUNSH578[_tb][_b] = list(_v["runs of equal gaps by length 1..8 (8 = 8 or more), shares"])
''', '''        RUNSH578[_tb][_b] = list(_v["runs of equal gaps by length 1..8 (8 = 8 or more), shares"])
_S137 = json.load(open("/home/claude/p58/tables/zeneng_v137_span.json"))
CELLS600 = [("under 3.5", 0, 3.5), ("3.5 to 4.5", 3.5, 4.5), ("4.5 to 5.5", 4.5, 5.5), ("5.5 to 6.5", 5.5, 6.5), ("6.5 to 7.5", 6.5, 7.5), ("7.5 and over", 7.5, 99)]
def cell600(x_): return next(c_ for c_, a_, b_ in CELLS600 if a_ <= x_ < b_)
F600 = {}; RUNSH600 = {}; SPQ600 = {}
for _tb, _ks in (("two-bar", ("600: cells below 5.5, two-bar slots", "600: cells at 5.5 and over, two-bar slots")), ("all", ("600: cells below 5.5, all slots", "600: cells at 5.5 and over, all slots"))):
    F600[_tb] = {}; RUNSH600[_tb] = {}; SPQ600[_tb] = {}
    for _k in _ks:
        for _c, _v in _S137[_k].items():
            _b = kband(0.5 * (dict((c_, (a_, b_)) for c_, a_, b_ in CELLS600)[_c][0] + min(9.0, dict((c_, (a_, b_)) for c_, a_, b_ in CELLS600)[_c][1])))
            _gs = dict(_v["gap values, shares"]); _gs.pop("triplet eighth", None); _gs.pop("longer than a half", None); _z = sum(_gs.values()); _gs = {k_: x_ / _z for k_, x_ in _gs.items()}
            _mg = collections.Counter()
            for _p in range(48):
                for _d in range(3, 25, 3): _mg[_cls578(_d)] += KRT[_b][_p][_d]
            _zm = sum(_mg.values())
            F600[_tb][_c] = {_d: (_gs.get(_cls578(_d), 0.0) / (_mg[_cls578(_d)] / _zm)) if _mg[_cls578(_d)] > 0 else 0.0 for _d in range(3, 25, 3)}
            RUNSH600[_tb][_c] = list(_v["runs of equal gaps by length 1..8 (8 = 8 or more), shares"])
            SPQ600[_tb][_c] = list(_v["first to last onset as a share of the slot: 25th, 50th, 75th"])
def draw_span600(rng, q_):
    """600: a span from the kept quartiles, piecewise linear between them, the tails one interquartile range out."""
    iq_ = q_[2] - q_[0]; lo_, hi_ = max(0.05, q_[0] - iq_), min(0.97, q_[2] + iq_)
    return float(np.interp(rng.random(), [0, 0.25, 0.5, 0.75, 1.0], [lo_, q_[0], q_[1], q_[2], hi_]))
SPAN600 = [None]; T602 = [None]; SRC602 = {}; OFF602 = {}; DENSE603 = [False]
''')
# ---- 600 in the rhythm of a line ----
P('''        STATS[f"578: line drawn by its slot's rate ({b578_}, {'two-bar' if slot_len(sec, i) == 2 else 'other'} slot)"] += 1
''', '''        STATS[f"578: line drawn by its slot's rate ({b578_}, {'two-bar' if slot_len(sec, i) == 2 else 'other'} slot)"] += 1
    D600 = False; S600_ = None; SPAN600[0] = None
    if ON17("600") and D578:                                                             # 600: the span first, from the kept quartiles of the slot-rate cell
        x600_ = len(sy) * MEL504[0] / max(1, slot_len(sec, i)); c600_ = cell600(x600_); tb600_ = "two-bar" if slot_len(sec, i) == 2 else "all"
        FW578_ = F600[tb600_][c600_]; SH578_ = RUNSH600[tb600_][c600_]; S600_ = draw_span600(rng, SPQ600[tb600_][c600_]); D600 = True
        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
''')
P('''    s_span = rng.uniform(*sp) if sp else None
    rq465 = REQ465.pop((sec, i), None) if ON8("465") else None''', '''    s_span = rng.uniform(*sp) if sp else None
    if D600: s_span = None; sp = None                                                   # 600: the drawn span stands in place of 378's
    rq465 = REQ465.pop((sec, i), None) if ON8("465") else None''')
P('''        alpha = [dict() for _ in range(n)]
''', '''        alpha = [dict() for _ in range(n)]; f600_ = F600C[0]
''')
P('''            if 0 in fix and t != fix[0]: continue
''', '''            if 0 in fix and t != fix[0]: continue
            if f600_ is not None and t != f600_[0]: continue                                 # 600: the first onset drawn for the span
''')
P('''                if k in fix and t != fix[k]: continue
''', '''                if k in fix and t != fix[k]: continue
                if f600_ is not None and k == n - 1 and abs(t - f600_[1]) > 3: continue       # 600: the last onset at the drawn span, within a sixteenth
''')
P('''    d465 = None
''', '''    F600C = [None]
    d465 = None
''')
P('''        free = _try >= NT or (fits is not None and not fits)
''', '''        F600C[0] = None
        free = _try >= NT or (fits is not None and not fits)
''')
P('''        cb = {}; sb = {}
''', '''        if D600 and not free and _try < NT // 2:                                          # 600: the first onset drawn, the last at the drawn span; the gaps fill it
            T600_ = int(round(S600_ * slot_len(sec, i) * BAR / 3)) * 3
            f0s_ = [t for t in range(max(-12, tmin), end - T600_ + 4, 3) if (kind_ is None or ENTRY_T[kind_](t)) and not (st[0] and t < 0)]
            if f0s_:
                t0_ = rng.choice(f0s_); F600C[0] = (t0_, t0_ + T600_); tgt = None
            else: STATS["600: no first onset leaves room for the drawn span (a try)"] += 1
        elif D600 and not free and _try == NT // 2: STATS["600: the drawn span given up for a line"] += 1
        cb = {}; sb = {}
''')
P('''        ons = sample(alpha)
        if ons is None:
            if h465: G542[1] += 1                                                          # 542: no rhythm ends in 465's drawn bar
            continue
''', '''        ons = sample(alpha)
        if ons is None:
            if h465: G542[1] += 1                                                          # 542: no rhythm ends in 465's drawn bar
            if F600C[0] is not None: STATS["600: no rhythm at the drawn span (a try)"] += 1
            continue
        if F600C[0] is not None: STATS["600: line at its drawn span"] += 1
''')
# ---- 601: the class at the rate the drawn span gives ----
P('''        x579_ = 4 * rate551(n, c_["at"][0], c_["at"][1], SPAN_TO[0]); p579_ = 0.65 if x579_ < 8 else 0.51 if x579_ < 10 else 0.34''',
  '''        x579_ = 4 * rate551(n, c_["at"][0], c_["at"][1], SPAN_TO[0])
        if ON17("601") and SPAN600[0] is not None and SPAN600[0][1] == n:                   # 601: the rate as the drawn span sings it
            x579_ = (n - 1) / max(0.25, SPAN600[0][0] * c_["nb"]); STATS["601: class drawn after the span"] += 1
        p579_ = 0.65 if x579_ < 8 else 0.51 if x579_ < 10 else 0.34''')
# ---- 602: the window's last note by its chord ----
P('''    if sec == "Verse 1": return (p - ETON) % 12 != 0                                     # the verse ends off the tonic''',
  '''    if sec == "Verse 1": return True if (ON17("602") and wlast409(sec, i)) else (p - ETON) % 12 != 0   # the verse ends off the tonic (262; lifted by 602 for the window's last note, the writer's ruling)''')
P('''    if ON("398") and (DRAWN398[0] or not ON("412")) and p % 12 in tones: w *= LK["ct398"]''', '''    if ON("398") and T602[0] is None and (DRAWN398[0] or not ON("412")) and p % 12 in tones: w *= LK["ct398"]''')
P('''                if tri(p, ch): continue                                                    # 215
''', '''                if tri(p, ch): continue                                                    # 215
                if T602[0] is not None and (((p - ETON) % 12 == 0) != T602[0]): continue      # 602: the tonic drawn, or not
''')
P('''                lt_ = LK["lt424"] if (LAST424[0] and (p - mton()) % 12 == 0) else 1.0             # 424: the window's last note on the tonic''',
  '''                lt_ = LK["lt424"] if (LAST424[0] and T602[0] is None and not ON17("602") and (p - mton()) % 12 == 0) else 1.0   # 424 (602: not on the window's last note)''')
# 603: leaps past a fifth held in dense lines
P('''    allc, allw = [], []
    for c in cats:''', '''    allc, allw, allk = [], [], []
    for c in cats:''')
P('''            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * wd * w / base)
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]''', '''            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * wd * w / base); allk.append(c[0])
    if DENSE603[0] and allc:                                                              # 603: a leap past a fifth held to 2% of the move's weight in a dense line
        L603_ = sum(w for w, k in zip(allw, allk) if k == "larger"); T603_ = sum(allw)
        if T603_ > 0 and L603_ / T603_ > 0.02:
            f603_ = 0.02 * (T603_ - L603_) / (0.98 * L603_); allw = [w * f603_ if k == "larger" else w for w, k in zip(allw, allk)]; STATS["603: leaps past a fifth held in a dense line"] += 1
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]''')
P('''            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) * (LK["lt424"] if (w409 and (x - mton()) % 12 == 0) else 1.0) for x in opts])[0] if opts else q_''',
  '''            t602_ = isinstance(CUR424[0], tuple) and i == len(notes) - 1 and ON17("602") and SRC602.get(CUR424[0][0]) == CUR424[0][1]
            if t602_:                                                                        # 602: a slurred last note, by the chord under the window's last note
                c602_ = M.chord_for(dict(n, on=n["on"] + OFF602.get(CUR424[0][0], 0)), notes_on); w602_ = rng.random() < (0.39 if ETON in M.CH[c602_][1] else 0.19)
                o602_ = [x for x in opts if ((x - ETON) % 12 == 0) == w602_]
                STATS[f"602: window's last note drawn ({'tonic' if w602_ else 'not tonic'}, tonic {'in' if ETON in M.CH[c602_][1] else 'not in'} the chord){'' if o602_ else ', not reachable'}"] += 1
                if o602_: opts = o602_
            p = rng.choices(opts, [(3 if x < q_ else 1) * (chord_w(x, n, ch_) if not t602_ else 1.0) * (LK["lt424"] if (w409 and not t602_ and (x - mton()) % 12 == 0) else 1.0) for x in opts])[0] if opts else q_''')
P('''            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None; LAST424[0] = False
            if p is None: return None''', '''            if ON17("602") and isinstance(CUR424[0], tuple) and i == len(notes) - 1 and SRC602.get(CUR424[0][0]) == CUR424[0][1]:   # 602: the window's last note
                c602_ = M.chord_for(dict(n, on=n["on"] + OFF602.get(CUR424[0][0], 0)), notes_on); T602[0] = rng.random() < (0.39 if ETON in M.CH[c602_][1] else 0.19)
                k602_ = f"602: window's last note drawn ({'tonic' if T602[0] else 'not tonic'}, tonic {'in' if ETON in M.CH[c602_][1] else 'not in'} the chord)"
                p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); T602[0] = None
                if p is None: p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); k602_ += ", not reachable"
                STATS[k602_] += 1
            else: p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw)
            SHAPE = None; LAST424[0] = False
            if p is None: return None''')
P('''                            cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p) and not tri(p, M.chord_for(ns[-1], notes_on_all | {x_["on"] for x_ in ns}))]
                            if cands:''', '''                            cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p) and not tri(p, M.chord_for(ns[-1], notes_on_all | {x_["on"] for x_ in ns}))]
                            t602_ = bool(ON17("602") and SRC602.get(sec) == i)
                            if t602_ and cands:                                                # 602: the window's last note on a drawn ending line
                                c602_ = M.chord_for(dict(ns[-1], on=ns[-1]["on"] + OFF602.get(sec, 0)), notes_on_all | {x_["on"] for x_ in ns}); w602_ = rng.random() < (0.39 if ETON in M.CH[c602_][1] else 0.19)
                                o602_ = [p for p in cands if ((p - ETON) % 12 == 0) == w602_]
                                STATS[f"602: window's last note drawn ({'tonic' if w602_ else 'not tonic'}, tonic {'in' if ETON in M.CH[c602_][1] else 'not in'} the chord){'' if o602_ else ', not reachable'}"] += 1
                                if o602_: cands = o602_
                            if cands:''')
P('''* (LK["lt424"] if (ON("424") and (p - mton()) % 12 == 0 and (wlast409(sec, i) if ON("409") else (ns[-1]["on"] // BAR - BAR0[sec]) % 8 == 7)) else 1.0) for p in cands])[0]   # 314; 424''',
  '''* (LK["lt424"] if (ON("424") and not t602_ and (p - mton()) % 12 == 0 and (wlast409(sec, i) if ON("409") else (ns[-1]["on"] // BAR - BAR0[sec]) % 8 == 7)) else 1.0) for p in cands])[0]   # 314; 424 (602)''')
# ---- where 602 lands, per build; 603's dense lines ----
P('''    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]; SEC_USED.clear(); CURB8[0] = SEC_BAND[sec]
        for i, sy in enumerate(sys_):
''', '''    SRC602.clear(); OFF602.clear()
    if ON17("602"):                                                                        # 602: the window's last line, or the line of its section it returns
        for s6_ in SUNG:
            j6_ = max([k for k in range(len(LINES[s6_])) if line_start(s6_, k) < (BAR0[s6_] + 8) * BAR] or [-1])
            if j6_ < 0: continue
            h6_, a6_, b6_ = how(s6_, j6_)
            if h6_ in ("figure", "chant"): STATS[f"602: window's last line designed, left alone ({s6_})"] += 1; continue
            if h6_ in ("plan", "return", "copy", "tail") and a6_ == s6_: SRC602[s6_] = b6_; OFF602[s6_] = line_start(s6_, j6_) - line_start(s6_, b6_)
            elif h6_ in ("fresh",): SRC602[s6_] = j6_; OFF602[s6_] = 0
            else: STATS[f"602: window's last line not drawn here ({s6_}, {h6_})"] += 1
    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]; SEC_USED.clear(); CURB8[0] = SEC_BAND[sec]
        for i, sy in enumerate(sys_):
            DENSE603[0] = bool(ON17("603") and len(sy) * MEL504[0] / max(1, slot_len(sec, i)) >= 5.5)   # 603: a line at 5.5 notes to the slot's bar and over
''')
# ---- the record ----
P('''    rerun["v136_part"] = V136;''', '''    rerun["v137_part"] = V137; rerun["v137_on"] = sorted(f_ for f_ in P137 if ON17(f_))
    rerun["v137_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("578:", "579:", "600:", "601:", "602:", "603:", "573:", "577:")}
    rerun["v136_part"] = V136;''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v136_p58.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_v137_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/run136/melody_v136_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/run137/melody_v137_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
