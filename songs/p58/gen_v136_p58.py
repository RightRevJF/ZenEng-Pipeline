"""gen_v136_p58.py: writes melody_v136_p58.py (song 48 under ZenEng v136, Module 27.80, Window 156) from melody_v134_p58.py, porting in one
pass v135's 573 and 577 and v136's 578 and 579 (589 is a reading: read_v136.py). Every patch replaces whole statements and is asserted to
match exactly once. ZE_PART136=0 gives v134 as it stood; ZE_OFF switches a fix off (side runs only).
- 573: a plan return whose words add three syllables or more to its source's falls back to a fresh line when its fit fails, counted.
- 577: a second redraw of a return's source (566's loop runs three times); the redraws printed.
- 578: every drawn line takes its gap values and its run lengths from kept lines of the band of its SLOT's rate (notes over the slot's bars,
  as 504 reads it), from zeneng_v136_slot_rate.json, the two-bar-slot tables for two-bar slots. The gap values: the kept position table for
  that band (372), reweighted so its share of each gap value is the kept lines'; no aimed weights on the line (as 551). The runs: each new
  run's length drawn from the kept shares (1..8, 8 = 8 or more), as 558 drew them. 551's caps stand where 551 and 558 put them.
- 579: lines of 13 notes and over in two-bar slots draw class 0 at the kept share for the line's own rate (65% under 8 notes a bar, 51% at 8
  to 10, 34% at 10 and over; class 1 the rest), the rate read as 551 expects it before the rhythm is drawn."""
SRC = "/home/claude/p58/melody_v134_p58.py"; DST = "/home/claude/p58/melody_v136_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""ZenEng v134 (Module 27.78; by gen_v134.py''', '''"""ZenEng v136 (Module 27.80; by gen_v136_p58.py from melody_v134_p58.py: 573, 577, 578, 579) -- ZenEng v134 (Module 27.78; by gen_v134.py''')
P('''def ON14(f_): return P134.get(f_, 0) <= V134 and f_ not in OFF11
''', '''def ON14(f_): return P134.get(f_, 0) <= V134 and f_ not in OFF11
V136 = int(_os11.environ.get("ZE_PART136", "1"))
P136 = {f_: 1 for f_ in ("573", "577", "578", "579")}
def ON16(f_): return P136.get(f_, 0) <= V136 and f_ not in OFF11
''')
# ---- the tables of 578 ----
P('''RET560 = [None]
''', '''RET560 = [None]
_S136 = json.load(open("/home/claude/p58/tables/zeneng_v136_slot_rate.json"))
def _cls578(d_): return {3: "sixteenth", 6: "eighth", 9: "dotted eighth", 12: "quarter", 18: "dotted quarter", 24: "half"}.get(d_, "longer than a half" if d_ > 24 else "other")
F578 = {}; RUNSH578 = {}
for _tb in ("all slots", "two-bar slots (over 6 to 10 beats)"):
    F578[_tb] = {}; RUNSH578[_tb] = {}
    for _b, _v in _S136[_tb].items():
        _gs = dict(_v["gap values, shares"]); _gs.pop("triplet eighth", None); _gs.pop("longer than a half", None); _z = sum(_gs.values())
        _gs = {k_: x_ / _z for k_, x_ in _gs.items()}                                    # 578: the kept shares over the gaps the grid can draw (3 to 24 twelfths)
        _mg = collections.Counter()
        for _p in range(48):
            for _d in range(3, 25, 3): _mg[_cls578(_d)] += KRT[_b][_p][_d]
        _zm = sum(_mg.values())
        F578[_tb][_b] = {_d: (_gs.get(_cls578(_d), 0.0) / (_mg[_cls578(_d)] / _zm)) if _mg[_cls578(_d)] > 0 else 0.0 for _d in range(3, 25, 3)}
        RUNSH578[_tb][_b] = list(_v["runs of equal gaps by length 1..8 (8 = 8 or more), shares"])
''')
# ---- 578 in the rhythm of a line ----
P('''            STATS["558: line drawn as runs of the kept lengths (" + ("8 and over" if x558_ >= 8 else "5.5 to 8") + ")"] += 1
''', '''            STATS["558: line drawn as runs of the kept lengths (" + ("8 and over" if x558_ >= 8 else "5.5 to 8") + ")"] += 1
    CAPL_ = D551 or R558                                                                # 551's caps stand where 551 and 558 put them
    D578 = False; SH578_ = None; FW578_ = None
    if ON16("578") and i is not None and not fix and len(sy) >= 3:                       # 578: the gaps and the runs by the band of the slot's rate
        b578_ = band504(len(sy), sec, i); tb578_ = "two-bar slots (over 6 to 10 beats)" if slot_len(sec, i) == 2 else "all slots"
        D578 = True; RTS = KRT[b578_]; FW578_ = F578[tb578_][b578_]; SH578_ = RUNSH578[tb578_][b578_]; R558 = False
        STATS[f"578: line drawn by its slot's rate ({b578_}, {'two-bar' if slot_len(sec, i) == 2 else 'other'} slot)"] += 1
''')
P('''        if D551: return w                                                                   # 551: the stress on the beat, no aimed weights''',
  '''        if D551 or D578: return w                                                           # 551 (578): the stress on the beat, no aimed weights''')
P('''    may_run = [D551 or runs_ok or''', '''    may_run = [D551 or D578 or runs_ok or''')
P('''        if D551: return RTS[tp % BAR][d] * H(k - 1, d)                                        # 551: the kept table for the line's band, directly''',
  '''        if D578: return RTS[tp % BAR][d] * H(k - 1, d) * FW578_.get(d, 0.0)                  # 578: the slot band's table, its gap values at the kept lines' shares
        if D551: return RTS[tp % BAR][d] * H(k - 1, d)                                        # 551: the kept table for the line's band, directly''')
P('''                    if D551 or R558: return 0.0 if (CAP551_ is not None''', '''                    if D551 or R558 or D578: return 0.0 if (CAP551_ is not None''')
P('''if (ON8("490") and t % 6 == 3 and g_ == 3 and not D551) else 1.0''', '''if (ON8("490") and t % 6 == 3 and g_ == 3 and not D551 and not D578) else 1.0''')
P('''                if R558 and g_ is not None and L558_[0] is not None: STATS["558: run-length draws"] += 1
                if R558 and g_ is not None and L558_[0] is not None:                             # 558: the run goes on to its drawn length, then breaks''',
  '''                if R558 and g_ is not None and L558_[0] is not None: STATS["558: run-length draws"] += 1
                f578_ = bool(D578 and g_ is not None and L558_[0] is not None and not (L558_[0] >= 8 and rl_[0] >= 8))   # 578: a drawn 8 is 8 or more
                if f578_: STATS["578: run-length draws"] += 1
                if (R558 and g_ is not None and L558_[0] is not None) or f578_:                  # 558 (578): the run goes on to its drawn length, then breaks''')
P('''                    else: STATS["558: the drawn run length could not be met (no gap fits)"] += 1''',
  '''                    else: STATS["578: the drawn run length could not be met (no gap fits)" if D578 else "558: the drawn run length could not be met (no gap fits)"] += 1''')
P('''                if R558 and rl_[0] == 1: L558_[0] = rng.choices(range(1, 13), SH558_)[0]        # 558: a new run, its length from the kept shares''',
  '''                if R558 and rl_[0] == 1: L558_[0] = rng.choices(range(1, 13), SH558_)[0]        # 558: a new run, its length from the kept shares
                if D578 and rl_[0] == 1: L558_[0] = rng.choices(range(1, 9), SH578_)[0]         # 578: a new run, its length from the slot band's kept shares''')
P('''        if D551 or R558:                                                                    # 551: the line's longest run of equal gaps against the kept 95th for its own rate''',
  '''        if D551 or CAPL_:                                                                   # 551: the line's longest run of equal gaps against the kept 95th for its own rate''')
# ---- 579: the ending class of the longest lines in two-bar slots ----
P('''        sh_ = list(K525[str(min(5, c_["nb"])) if c_["nb"] < 5 else "5+"][nband525(n)]["shares"])
''', '''        sh_ = list(K525[str(min(5, c_["nb"])) if c_["nb"] < 5 else "5+"][nband525(n)]["shares"])
    if ON16("579") and n >= 13 and c_["nb"] == 2:                                            # 579: class 0 at the kept share for the line's own rate
        x579_ = 4 * rate551(n, c_["at"][0], c_["at"][1], SPAN_TO[0]); p579_ = 0.65 if x579_ < 8 else 0.51 if x579_ < 10 else 0.34
        sh_ = [p579_, 1.0 - p579_, 0.0, 0.0]; STATS[f"579: class drawn by the line's rate ({'under 8' if x579_ < 8 else '8 to 10' if x579_ < 10 else '10 and over'})"] += 1
''')
# ---- 573: a plan return that adds three syllables or more falls back to a fresh line ----
P('''    def how(sec, i):
        """('copy'|'return'|'again'|'plan'|'fresh'|'tail', source section, source line)."""
        kind = KIND[sec]
''', '''    fb573 = set()
    def how(sec, i):
        """('copy'|'return'|'again'|'plan'|'fresh'|'tail', source section, source line)."""
        kind = KIND[sec]
        if (sec, i) in fb573: return ("fresh", None, None)                                 # 573
''')
P('''                ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, tm566_, lo_, hi_, notes_on_all, endok=endok_of(sec, i))
                r = ("ns", ns, kd) if ns else ("fail", kd, None)''',
  '''                ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, tm566_, lo_, hi_, notes_on_all, endok=endok_of(sec, i))
                if not ns and h == "plan" and ON16("573") and len(LINES[sec][i]) - len(LINES[s0][i0]) >= 3:   # 573: the fit fails: a fresh line, counted
                    fb573.add((sec, i)); STATS["573: plan return (three syllables or more added) falls back to a fresh line"] += 1; STATS[f"573: at {sec}:{i}"] += 1; return None
                r = ("ns", ns, kd) if ns else ("fail", kd, None)''')
# ---- 577: a second redraw of the source ----
P('''                for att566_ in range(2 if ON14("566") else 1):''', '''                for att566_ in range((3 if ON16("577") else 2) if ON14("566") else 1):
                    if att566_ == 2: STATS["577: the source drawn a second time"] += 1''')
P('''if RET560[0] is not None and att566_ == 1: RET560[0] -=''', '''if RET560[0] is not None and att566_ >= 1: RET560[0] -=''')
P('''                    if att566_ == 0 and RET560_ON_[0]:                                       # 566: the return tried now, after the breath; no fit, the source drawn again''',
  '''                    if att566_ < (2 if ON16("577") else 1) and RET560_ON_[0]:              # 566 (577): the return tried now, after the breath; no fit, the source drawn again''')
P('''                        if ns2_ is None: STATS["566: no fit after the breath; the source drawn again an eighth earlier for each syllable added"] += 1; continue''',
  '''                        if ns2_ is None: STATS["566: no fit after the breath; the source drawn again an eighth earlier for each syllable added" if att566_ == 0 else "577: no fit after the first redraw; the source drawn a second time"] += 1; continue''')
# ---- the record ----
P('''    rerun["v134_part"] = V134;''', '''    rerun["v136_part"] = V136; rerun["v136_on"] = sorted(f_ for f_ in P136 if ON16(f_))
    rerun["v136_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("551:", "558:", "560:", "566:", "573:", "577:", "578:", "579:")}
    rerun["v134_part"] = V134;''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v134_p58.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_v136_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/run/melody_v134_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/run136/melody_v136_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
