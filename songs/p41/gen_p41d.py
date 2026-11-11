s = open("melody_p41.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)
s = '''"""The Water Used to Sing (song 41), DESIGN VERSION: the song made for real after delivery (the writer's Q21-Q25), on the same lyric,
form and arrangement. Design gates (named, 278):
  Q22  the hook climbs to 'sing' on D4, its top, on beat 1 of its second bar over G, held; the tag 'It sings.' comes home to G3.
  Q23  the verses low-middle (centre D3, B2-B3); the chorus a fourth above (median three or more over the verse's), to D4.
  Q24  swung eighths and longer, no sixteenths; steps and small leaps (a leap past a fifth weighted down, and never onto an
       unstressed syllable); the arch amplitude held to 7 (v108's 249 cap) since 305's uncapped draw widens leaps (finding 315).
  Q25  'living water doesn't shine' climbs to E4 on 'shine' (beat 3 of its first bar, over C), the song's only E4.
  Q16 B the bridge median under the verse's (kept from the default run).
The registers are designed, not drawn. Usage: PYTHONHASHSEED=0 python3 melody_p41d.py 1000 design
The default-path search it grew from (melody_p41.py):
''' + s[3:]
R('_MODE = sys.argv[2] if len(sys.argv) > 2 else "main"', '_MODE = sys.argv[2] if len(sys.argv) > 2 else "design"')
R('F = dict(f243=MODE == "main")', 'F = dict(f243=MODE in ("main", "design"))')
R('    step = 3                                                                            # 288: the sixteenth grid, at the class table\'s rates and the window\'s aim',
  '    step = 6                                                                            # Q24 (design): the eighth grid, no sixteenths')
R('        sx = rng.random() < SIXTEENTH / 0.431', '        sx = False')
R('M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 3', 'M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 6')
R('if ns is None or any((n["on"] - U) % 3 for n in ns): return None', 'if ns is None or any((n["on"] - U) % 6 for n in ns): return None')
R('PALETTE = (3, 6, 9, 12, 18, 24, 36, 48)', 'PALETTE = (6, 12, 18, 24, 36, 48)')
R('''                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0''',
  '''                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0
                if sz > 7: w0 *= 0.25 if n.get("stress") else 0.0                         # Q24 (design): past a fifth only onto a stressed syllable, and rarely''')
R('''            else: LK["amp"] = float(max(1.5, LK["amp"] * float(np.clip(ARCH_SPAN / max(0.02, arch), 0.6, 1.6))))''',
  '''            else: LK["amp"] = float(np.clip(LK["amp"] * float(np.clip(ARCH_SPAN / max(0.02, arch), 0.6, 1.6)), 1.5, 7.0))   # Q24 (design): held to 7 (315)''')
R('V_MU, V_CAP, V_FLOOR = 52, 57, 45                                                     # the verse in the baritone\'s low-middle: E3, to A3, from A2 (sounding)',
  '''V_MU, V_CAP, V_FLOOR = 50, 59, 47                                                     # Q23 (design): the verse low-middle, D3, to B3, from B2 (sounding)
HOOK_TOP, PEAK, TAG_END = 62, 64, 55                                                   # Q22: 'sing' D4; Q25: 'shine' E4; Q22: the tag home to G3
def draw_registers(rng):
    """design: the registers are the writer's (Q23): the chorus a fourth over the verse, to D4; the bridge under the verse (Q16 B)."""
    ub = rng.random(); lb = -float(np.interp(ub, [0, 1], [1.5, 5.0])); b_mu = V_MU + lb
    R = {"Verse": (V_MU, V_CAP, V_FLOOR), "Chorus": (55.5, HOOK_TOP, 50), "Pre": (53, V_CAP, V_FLOOR),
         "Bridge": (b_mu, int(round(b_mu + 7)), int(round(max(M.LO, b_mu - 5))))}
    return R, dict(u=None, ub=ub, chorus_median=5.5, chorus_top=HOOK_TOP - V_CAP, chorus_floor=50 - V_FLOOR, bridge_median=lb, design=True)
def draw_registers_kept(rng):''')
R("def draw_registers_kept(rng):\ndef draw_registers(rng):", "def draw_registers_kept(rng):")
R('''    if sec == "Chorus 1" and i == 0: return (p - M.TONIC) % 12 == 0                       # the hook ends where the last chorus ends (its tag): the tonic''',
  '''    if sec == "Chorus 1" and i == 0: return p == HOOK_TOP                                 # Q22: 'sing' on D4
    if (sec, i) == ("Last Chorus", 6): return p == PEAK                                     # Q25: 'shine' on E4
    if (sec, i) == ("Last Chorus", 7): return p == TAG_END                                  # Q22: 'It sings.' home to G3''')
R('''            if i == 6 and plans["tail"] == "return": return ("return", "Chorus 1", 3)      # 'living water doesn't shine' on 'Now it only shines\'''',
  '''            if i == 6: return ("fresh", None, None)                                         # Q25: the peak is drawn fresh''')
R('''                r = ("ns", [dict(n, on=n["on"] - SU + U, syl=n["syl"] - k0) for n in S if n["syl"] >= k0], "exact")''',
  '''                tl = [dict(n, on=n["on"] - SU + U, syl=n["syl"] - k0) for n in S if n["syl"] >= k0 and not n["slur"]]
                tl[-1]["p"] = TAG_END; tl[0]["p"] = 59 if len(tl) > 1 else tl[0]["p"]          # Q22: 'It' B3, 'sings' home to G3 (the hook's rhythm)
                r = ("ns", tl, "exact")''')
R('''        rule = (sec, i) == ("Chorus 1", 0) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''',
  '''        rule = (sec, i) in (("Chorus 1", 0), ("Last Chorus", 6)) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''')
R('''                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                meta["free"][sec] += len(ns)''',
  '''                fixr = {5: 48} if (sec, i) == ("Chorus 1", 0) else {6: 24} if (sec, i) == ("Last Chorus", 6) else None   # Q22 'sing' bar 2 beat 1; Q25 'shine' beat 3 over C
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, fixr, i=i)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                meta["free"][sec] += len(ns)
                if (sec, i) == ("Last Chorus", 6): hi = PEAK                                        # Q25: E4 for this line only''')
R('''                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1''',
  '''                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1
                if (sec, i) == ("Last Chorus", 6): hi = REGS[kind][1]''')
R('''DESIGN_GATES = ["bridge median under the verse's (design, Q16 B)"]                    # 208's bridge-above reading set aside by the design''',
  '''DESIGN_GATES = ["bridge median under the verse's (design, Q16 B)",
                "design: the hook climbs to 'sing' on D4, its top, beat 1 of its second bar over G, held (Q22)",
                "design: the chorus median three or more over the verse's, its top over the verse's (Q23)",
                "design: E4 once, on 'shine' in the last chorus (Q25)", "design: the tag 'It sings.' home to G3 (Q22)",
                "design: no sixteenths; no leap past a fifth onto an unstressed syllable (Q24)"]
def design_fails(c):
    notes = c["notes"]; f = {}
    h = [n for n in notes if n["line"] == "Chorus 1:0"]; U = line_start("Chorus 1", 0); sing = [n for n in h if n["syl"] == 5]
    if not (sing and sing[0]["p"] == HOOK_TOP and max(n["p"] for n in h) == HOOK_TOP and sing[0]["on"] == U + 48 and sing[0]["dur"] >= 24
            and M.chord_at(sing[0]["on"]) == "G" and all(n["p"] < HOOK_TOP for n in h if n["syl"] < 5)): f[DESIGN_GATES[1]] = 1
    if not (med(notes, "Chorus 1") - med(notes, "Verse 1") >= 3 and top(notes, "Chorus 1") > top(notes, "Verse 1")): f[DESIGN_GATES[2]] = 1
    pk = [n for n in notes if n["p"] >= PEAK]
    if not (len(pk) >= 1 and all(n["line"] == "Last Chorus:6" and n["p"] == PEAK for n in pk) and any(n["syl"] == 6 and not n["slur"] for n in pk)): f[DESIGN_GATES[3]] = 1
    tag = [n for n in notes if n["line"] == "Last Chorus:7"]
    if not (tag and tag[-1]["p"] == TAG_END): f[DESIGN_GATES[4]] = 1
    bad = any(b["on"] - a["on"] < 6 for a, b in zip(notes, notes[1:])) or any(abs(b["p"] - a["p"]) > 7 and not b.get("stress") for a, b in zip(notes, notes[1:]) if a["line"] == b["line"])
    if bad: f[DESIGN_GATES[5]] = 1
    return f''')
R('''    f = gate_fails(c, c.get("judge"))
    for g in GATES:''', '''    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))
    for g in DESIGN_GATES[1:] + GATES:''')
R('''        fails = gate_fails(c, c["judge"]); info = c["info"]''', '''        fails = gate_fails(c, c["judge"]); fails.update(design_fails(c)); info = c["info"]''')
R('''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in list(GATES) + sorted(k for k in would if k not in GATES)]''',
  '''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in DESIGN_GATES[1:] + list(GATES) + sorted(k for k in would if k not in GATES and k not in DESIGN_GATES)]''')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_p41.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_p41d.py {N} {MODE}"')
R('open(f"{OUT}/melody_p41_{MODE}{_TAG}.pkl", "wb"))', 'open(f"{OUT}/melody_p41d_{MODE}{_TAG}.pkl", "wb"))')
open("melody_p41d.py", "w").write(s)
s = open("melody_p41d.py").read()
R('''            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)''',
  '''            U = line_start(sec, i); tmin = max(-12, last_on + gap_for(sec) - U)''')
R('''                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - GAP_MIN''', '''                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - gap_for(nxt[0])''')
R('''            if ns[0]["on"] - last_on < GAP_MIN: globals()''', '''            if ns[0]["on"] - last_on < gap_for(sec): globals()''')
R('''GAP_MIN = 18''', '''GAP_MIN = 18
def gap_for(sec): return 12 if sec in ("Verse 1", "Verse 2") else GAP_MIN             # Q24 with Q20: a quick breath (a beat) between the verses' one-bar lines''')
R('"LastChorus": ["C", "G", "Em", "D", "C", "G", "Em", "D", "C", "G", "Am", "D", "C", "D", "G", "G"]',
  '"LastChorus": ["C", "G", "Em", "D", "C", "G", "Em", "D", "C", "G", "Am", "D", "C", "C", "G", "G"]')   # Q25: 'shine' E4 held over C, then IV-I into the tag
R('''else {6: 24} if (sec, i) == ("Last Chorus", 6) else None   # Q22 'sing' bar 2 beat 1; Q25 'shine' beat 3 over C''',
  '''else {6: 48} if (sec, i) == ("Last Chorus", 6) else None   # Q22 'sing' bar 2 beat 1; Q25 'shine' bar 2 beat 1 over C''')
R("""  Q25  'living water doesn't shine' climbs to E4 on 'shine' (beat 3 of its first bar, over C), the song's only E4.""",
  """  Q25  'living water doesn't shine' climbs to E4 on 'shine' (beat 1 of its second bar, over C; that bar's chord C, not D, so the
       tag comes home by IV-I), the song's only E4. With Q24, the verses' one-bar lines take a breath of one beat, not 212's 1.5.""")
open("melody_p41d.py", "w").write(s)
s = open("melody_p41d.py").read()
R('''                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)''',
  '''                    whi = HOOK_TOP - 1 if (sec, i) == ("Chorus 1", 0) else PEAK - 1 if (sec, i) == ("Last Chorus", 6) else hi   # Q22/Q25: the designed note is the line's top
                    ps = walk_notes(rng, ns, prev, run, mu, lo, whi, notes_on_all, fixed=fx, shape=shape)''')
open("melody_p41d.py", "w").write(s)
s = open("melody_p41d.py").read()
R('''            if iv > 9 or iv == 6: bad.add(j if j not in keep else j - 1)''',
  '''            if iv > 9 or iv == 6 or (iv > 7 and not ns[j].get("stress")): bad.add(j if j not in keep else j - 1)   # Q24: no leap past a fifth onto a weak syllable''')
open("melody_p41d.py", "w").write(s)
s = open("melody_p41d.py").read()
R('''                if (sec, i) == ("Last Chorus", 6): hi = PEAK                                        # Q25: E4 for this line only''',
  '''                if (sec, i) == ("Last Chorus", 6): hi = PEAK                                        # Q25: E4 for this line only
                if fixr: ns = [n for n in ns if not (n["slur"] and n["syl"] == len(sy) - 1)]          # the designed word is struck on its note, not slurred into''')
open("melody_p41d.py", "w").write(s)
