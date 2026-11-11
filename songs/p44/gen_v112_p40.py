"""Writes melody_v112_p40.py: the v112 port (fixes 330-333) on song 40, from the tested v111 port (songs/p43/melody_v111_p40.py).
334-336 are the report's (readings_v112.py)."""
s = open("/home/claude/p43/melody_v111_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)

s = '''"""ZenEng v112 PORT (fixes 330-336) on song 40: Nothing Else on Earth once more, same lyric, intake and seed (Window 132, 27.56).
  330 a partner whose bar copy fails the one-onset check keeps its partner's stressed onsets (322) and is not given up.
  331 293's per-bar copy rate set in the calibration so that verse 2's median share of verse 1's bar rhythms (within one onset)
      is the kept 50%.
  332 a knob that takes its largest step two rounds running is frozen and reported; the other knobs finish their rounds.
  333 the song's range drawn no wider than the row less two semitones.
  334-336 the report's: every tempo band's quartiles; each test read against its kept figure or marked a reading; the floor's
      share a reading.
Usage: PYTHONHASHSEED=0 python3 melody_v112_p40.py N main|ctl [tag]
From the v111 port:
''' + s[3:]
R('H111 = "/home/claude/p43"; VAR = MODE', 'H111 = "/home/claude/p43"; H112 = "/home/claude/p44"; VAR = MODE')

# ---- 330: a failed copy falls back to the stresses ----
R('''        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or rng.random() < 0.40}   # 293 at 40%; 310: a pair takes every bar
        elif copybars and _try == 14: STATS["293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if stressbars and _try < 14 and not free: sb = stressbars                         # 322
        elif stressbars and _try == 14: STATS["322: partner's stresses given up for a line"] += 1''',
  '''        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or rng.random() < RATE293[0]}   # 293 at 331's rate; 310: a pair takes every bar
        elif copybars and _try == 14 and not (pair and fallback): STATS["293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if pair and fallback and 14 <= _try < NT and not free: sb = fallback                  # 330: the copy failed: the partner's stresses
        elif pair and fallback and _try == NT: STATS["330: partner given up after its stresses"] += 1
        if stressbars and _try < 14 and not free: sb = stressbars                         # 322
        elif stressbars and _try == 14: STATS["322: partner's stresses given up for a line"] += 1''')
R('''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None):''',
  '''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None):''')
R('''        if sb: STATS["322: partner's stresses kept"] += 1''',
  '''        if sb and not pair: STATS["322: partner's stresses kept"] += 1
        if sb and pair: STATS["330: copy failed, partner's stresses kept"] += 1''')
R('''        else: kw = dict(copybars=again_kw(partner[0], partner[1])["copybars"], pair=True)  # 310: the partner's bars''',
  '''        else: kw = dict(copybars=again_kw(partner[0], partner[1])["copybars"], pair=True, fallback=stress_bars(partner[0], partner[1]))  # 310; 330''')

# ---- 331: 293's rate from the kept songs ----
R('''LONG_SHARE = 0.57 ''', '''RATE293 = [0.40]                                                                     # 331: set in the calibration (kept verse 2 share 50%)
V2_KEPT = 0.50
def v2_share(notes):
    """331 (and 313's reading): verse 2's bars whose onsets are within one of verse 1's same bar."""
    def bars(s):
        out = collections.defaultdict(set)
        for n in notes:
            if n["sec"] == s: out[n["on"] // BAR - BAR0[s]].add(n["on"] % BAR)
        return out
    a, c = bars("Verse 2"), bars("Verse 1"); return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))
LONG_SHARE = 0.57 ''')
R('''    log = []; lines_acc = []; big_prev = set(); pf_acc = []''', '''    log = []; lines_acc = []; big_prev = set(); pf_acc = []; v2_acc = []''')
R('''            k += 1
            if NEW: lines_acc.append(line_readings(c["notes"]))''', '''            k += 1
            if "Verse 2" in SUNG: v2_acc.append(v2_share(c["notes"]))
            if NEW: lines_acc.append(line_readings(c["notes"]))''')
# ---- 332: the stop freezes one knob ----
R('''        if NEW and lines_acc:
            arch = float''', '''        if v2_acc:                                                                          # 331: the rate moved toward the kept median share
            sh = float(np.median(v2_acc)); RATE293[0] = float(np.clip(RATE293[0] + (V2_KEPT - sh), 0.05, 1.0))
            row["293 rate"] = (V2_KEPT, round(sh, 3), round(RATE293[0], 3)); v2_acc.clear()
        if NEW and lines_acc:
            keep = {k_: LK[k_] for k_ in FROZEN}
            arch = float''')
R('''            if big & big_prev:                                                                  # 315: the largest step two rounds running
                CAL_STOP.append(f"calibration stopped after round {rd + 1}: {sorted(big & big_prev)} took the largest step two rounds running")
                print(CAL_STOP[-1]); log.append(row); return log
            big_prev = big''', '''            LK.update(keep); big -= FROZEN                                                     # 332: a frozen knob stays where it was frozen
            row["lines"]["largest_steps"] = sorted(big)
            if big & big_prev:                                                                  # 315/332: the largest step two rounds running
                FROZEN.update(big & big_prev)
                CAL_STOP.append(f"round {rd + 1}: {sorted(big & big_prev)} took the largest step two rounds running and are frozen at {[round(LK[k_], 3) for k_ in sorted(big & big_prev)]}; the other knobs finish their rounds")
                print(CAL_STOP[-1])
            big_prev = big''')
R('''CAL_STOP = []''', '''CAL_STOP = []; FROZEN = set()''')
# ---- 333: the range inside the row ----
R('''    row = ROW_HI - ROW_LO; r = int(round(min(row, max(5, kq(K314["the song's sung range, semitones (5, 25, 50, 75, 95)"], rng.random())))))''',
  '''    row = ROW_HI - ROW_LO; r = int(round(min(row - 2, max(5, kq(K314["the song's sung range, semitones (5, 25, 50, 75, 95)"], rng.random())))))   # 333''')
R('''    rerun["calibration_stop"] = list(CAL_STOP)''', '''    rerun["calibration_stop"] = list(CAL_STOP); rerun["frozen"] = sorted(FROZEN); rerun["rate293"] = RATE293[0]''')
R('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v111_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v112_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
R('''                open(f"{H111}/melody_v111_p40_{MODE}{_TAG}.pkl", "wb"))''', '''                open(f"{H112}/melody_v112_p40_{MODE}{_TAG}.pkl", "wb"))''')
open("/home/claude/p44/melody_v112_p40.py", "w").write(s)
print("written")
