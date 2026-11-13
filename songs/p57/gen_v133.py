"""gen_v133.py: writes melody_v133_p57.py (song 47 run again under ZenEng v133 as a regression) from melody_v132_p57.py, with v133's
generic patches: 558 (amends 551: a line of nine notes or more at 5.5 notes a bar and over, by its rate, draws its gaps as runs of equal
gaps whose lengths come from the kept shares for its rate, zeneng_v133_density.json, 5.5 to 8 and 8 and over; 551's cap standing) and
560 (a line whose next line returns it is drawn so that its last onset leaves the breath before its own entry one slot later; such lines
counted). 557 and 562 are readings (read_v133.py). Every patch replaces whole statements and is asserted to match exactly once."""
SRC = "/home/claude/p57/melody_v132_p57.py"; DST = "/home/claude/p57/melody_v133_p57.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)

P('''"""ZenEng v132 (Module 27.76; by gen_v132.py''', '''"""ZenEng v133 (Module 27.77; by gen_v133.py from melody_v132_p57.py: 558, 560) -- ZenEng v132 (Module 27.76; by gen_v132.py''')
P('''def ON12(f_): return P132.get(f_, 0) <= V132 and f_ not in OFF11
''', '''def ON12(f_): return P132.get(f_, 0) <= V132 and f_ not in OFF11
V133 = int(_os11.environ.get("ZE_PART133", "1"))
P133 = {f_: 1 for f_ in ("558", "560")}
def ON13(f_): return P133.get(f_, 0) <= V133 and f_ not in OFF11
''')
# ---- 558: which lines, and the run lengths drawn ----
P('''            STATS[f"551: dense line drawn from the kept table ({b551_})"] += 1''',
  '''            STATS[f"551: dense line drawn from the kept table ({b551_})"] += 1
    R558 = False; SH558_ = None
    if ON13("558") and i is not None and not fix and len(sy) >= 9:                      # 558: nine notes or more at 5.5 a bar and over, by the line's rate
        x558_ = 4 * rate551(len(sy), sec, i, span_to)
        if x558_ >= 5.5:
            R558 = True; SH558_ = RUNSH558["8 and over" if x558_ >= 8 else "5.5 to 8"]
            if CAP551_ is None: CAP551_ = cap551(len(sy), kband(x558_))                  # 551's cap standing
            STATS["558: line drawn as runs of the kept lengths (" + ("8 and over" if x558_ >= 8 else "5.5 to 8") + ")"] += 1''')
P('''            lw_ = LW406[0]; ert_ = int(er_kept(SEC_NPB[sec])); rl_ = [0]''',
  '''            lw_ = LW406[0]; ert_ = int(er_kept(SEC_NPB[sec])); rl_ = [0]; L558_ = [None]''')
P('''                    if D551: return 0.0 if (CAP551_ is not None and g_ is not None and d_ == g_ and rl_[0] + 1 > CAP551_) else 1.0   # 551: no weights; the run capped''',
  '''                    if D551 or R558: return 0.0 if (CAP551_ is not None and g_ is not None and d_ == g_ and rl_[0] + 1 > CAP551_) else 1.0   # 551: no weights; the run capped (558: the runs drawn below)''')
P('''                if not ks or sum(ws) <= 0: return None
                cur = rng.choices(ks, ws)[0]; ons.append(cur[0]); rl_[0] = (rl_[0] + 1) if (g_ is not None and t - cur[0] == g_) else 1''',
  '''                if not ks or sum(ws) <= 0: return None
                if R558 and g_ is not None and L558_[0] is not None:                             # 558: the run goes on to its drawn length, then breaks
                    want_ = rl_[0] < L558_[0]
                    wm_ = [w_ if ((t - x[0] == g_) == want_) else 0.0 for w_, x in zip(ws, ks)]
                    if sum(wm_) > 0: ws = wm_
                    else: STATS["558: the drawn run length could not be met (no gap fits)"] += 1
                cur = rng.choices(ks, ws)[0]; ons.append(cur[0]); rl_[0] = (rl_[0] + 1) if (g_ is not None and t - cur[0] == g_) else 1
                if R558 and rl_[0] == 1: L558_[0] = rng.choices(range(1, 13), SH558_)[0]        # 558: a new run, its length from the kept shares''')
P('''        if D551:                                                                            # 551: the line's longest run of equal gaps against the kept 95th for its own rate''',
  '''        if RET560[0] is not None and ons[-1] > RET560[0] + ons[0] - GAP_MIN:                 # 560: the breath its own return needs, one slot later
            if _try < NT // 2: STATS["560: redrawn for the breath before its own return"] += 1; continue
            STATS["560: the breath before its own return given up for a line"] += 1
        if D551 or R558:                                                                    # 551: the line's longest run of equal gaps against the kept 95th for its own rate''')
P('''RUNSH558 = None''' if False else '''CAP551 = {b_: int(v_["95th"]) for b_, v_ in _F132''', '''_D133 = json.load(open("/home/claude/p57/tables/zeneng_v133_density.json"))
RUNSH558 = {b_: v_["shares"] for b_, v_ in _D133["558: kept run lengths"]["kept lines of nine notes or more: every run of equal gaps in the line, by length in gaps (1 = a gap unlike its neighbours; 12 = 12 or more): counts, then shares"].items()}
RET560 = [None]
CAP551 = {b_: int(v_["95th"]) for b_, v_ in _F132''')
# ---- 560: the line whose next line returns it ----
P('''                set465(sec, i, nxt, f0, tmin); ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner, unitbars=ub or None)''',
  '''                hn_ = how(*nxt) if nxt else (None, None, None)
                RET560[0] = slot_len(sec, i) * BAR if (ON13("560") and nxt and hn_[0] in ("plan", "return") and (hn_[1], hn_[2]) == (sec, i)) else None   # 560
                if RET560[0] is not None: STATS["560: a line drawn with the breath its own return needs"] += 1
                set465(sec, i, nxt, f0, tmin); ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner, unitbars=ub or None); RET560[0] = None''')
P('''    rerun["v132_part"] = V132;''', '''    rerun["v133_part"] = V133; rerun["v133_on"] = sorted(f_ for f_ in P133 if ON13(f_))
    rerun["v133_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("558:", "560:", "551:")}
    rerun["v132_part"] = V132;''')
P('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v132_p57.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v133_p57.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
P('''open(f"/home/claude/p57/run132/melody_v132_p57_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p57/run133/melody_v133_p57_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
