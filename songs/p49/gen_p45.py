"""Writes melody_p45.py: song 45, Before It's Done, on the v116 port (songs/p47/melody_v116_p40.py), built as song 44 was (songs/p48/gen_p44.py):
every line two bars, with this song's constants, lyric, key, lift and designs (intake Q1-Q15)."""
s = open("/home/claude/p47/melody_v116_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
s = '''"""ZenEng v116 -- song 45, Before It's Done, on the v116 port (fixes 355-363 in force; findings from 375). A fingerpicked ballad, q = 72,
4/4 (Q4 B); searched in G major, the last chorus and the tag lifted a whole step to A in the record (Q6 A); a man's middle voice (the search
row B2-D4, so the lifted chorus tops at E4; Q5 A); 56 bars (Q7 A).
Designs in force, named (Q14 A, Q15 A):
  the chorus over the verse: the verse low and narrow, the chorus to the song's top (constructive registers, as song 44).
  'Hold that thought': 'thought' held two and a half beats, on G or D (the guitar's sus resolves under it).
  'before it's done' steps down D4 C4 B3 A3 in choruses 1-2 (ends on the 2nd, over D); C4 B3 A3 G3 in the last chorus (home).
  the tag's last note on A3, the 2nd (B after the lift), left open.
  A design gate (317), its pass rate printed.
Usage: PYTHONHASHSEED=0 python3 melody_p45.py N main|ctl [tag]
The v116 port it is built on:
''' + s[3:]
R('sys.path[:0] = ["/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]',
  'sys.path[:0] = ["/home/claude/p49", "/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]')
R('import lyric_p40 as L', 'import lyric_p45 as L')
a = s.index("M.TONIC = 2;"); b = s.index("STOP_BARS = set()")
s = s[:a] + '''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = M.SCALE | {8}                 # G major; G-sharp sung over the bridge's E (V of A)
OUT_PCS = (8,)
M.CH = {"G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "C": (0, {0, 4, 7}), "Am": (9, {9, 0, 4}), "E": (4, {4, 8, 11})}
M.ROMAN = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "E": "VI"}
M.QBPM = 72; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 47; TOP = 62; M.SUMMIT = TOP      # the search row B2-D4; the lifted last chorus tops at E4 (Q5 A)
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
FEEL = "a fingerpicked acoustic ballad, q = 72, 4/4; a cello from verse 2 (Q4 B)"
LIFT = 2                                                                               # the last chorus and the tag, a whole step up in the record (Q6 A)
PLAN = {"Intro": ["Em", "C", "G", "D"], "Verse": ["Em", "C", "G", "D", "Em", "C", "Am", "D"], "Chorus": ["G", "D", "Em", "C", "G", "D", "C", "D"],
        "LastChorus": ["G", "D", "Em", "C", "G", "D", "C", "G"], "Bridge": ["Am", "Em", "C", "G", "Am", "Em", "C", "E"], "Tag": ["Em", "C", "G", "C"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 8), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 8),
        ("Bridge", "Bridge", 8), ("Last Chorus", "Chorus", 8), ("Tag", "Tag", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else kind]; b += nb
NBARS = b; assert NBARS == 56 and len(CHORD) == NBARS
''' + s[b:]
R('SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"]',
  'SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus", "Tag"]')
R('SLOTS = {"Verse": [2, 1, 3, 3, 2, 1], "Pre": [2, 2], "Chorus": [2] * 8, "Bridge": [2, 1, 1, 2, 1, 1], "Last Chorus": [2] * 9}',
  'SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 4, "Bridge": [2] * 4, "Last Chorus": [2] * 4, "Tag": [2] * 2}      # every line two bars')
R('SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}',
  'SRC = {"Verse 2": "Verse 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}')
R('''         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}''',
  '''         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}
    R["Tag"] = R["Chorus"]                                                             # the tag sings in the chorus's register''')
R('''    R = {k: widen_329(v, lo, hi) for k, v in R.items()}''', '''    R = {k: widen_329(v, lo, hi) for k, v in R.items()}
    vf_ = lo + (1 if rng.random() < 0.5 else 0); vc_ = min(hi - 3, vf_ + 8); vm_ = (vf_ + vc_) / 2           # Q14 A: the verse low and narrow (eight semitones)
    ch_ = hi; cl_ = max(lo, min(vc_ - 2, ch_ - 10)); cm_ = (cl_ + ch_) / 2                                     # the chorus over it, to the song's top
    R["Verse"] = (vm_, vc_, vf_); R["Chorus"] = (cm_, ch_, cl_); R["Tag"] = R["Chorus"]
    globals().update(V_MU=vm_, V_CAP=vc_, V_FLOOR=vf_)''')
R('''TRIAD = {2, 6, 9}
ENDING_NEEDS.update(Chorus={M.TONIC % 12})                                            # 311: the hook (and the tag that copies it) ends on the tonic
def end_ok(sec, i, p):
    if sec == "Chorus 1" and i == 0: return (p - M.TONIC) % 12 == 0                       # the hook ends where the last chorus ends (its tag): the tonic
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return (p - M.TONIC) % 12 != 0                                   # the verse ends off the tonic
    if sec == "Chorus 1": return p % 12 in TRIAD                                         # an earlier chorus on a note of the tonic triad
    return True''', '''TRIAD = {7, 11, 2}
ENDING_NEEDS.update(Verse={2, 9})                                                     # 311: the verse closes on D or A, over its D (the half cadence)
def end_ok(sec, i, p):
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return p % 12 in (2, 9)
    return True                                                                         # the choruses and the tag end on designed notes (Q15 A)''')
a = s.index('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)'''); b = s.index('''        plan = plans[kind]; first = plan.index(plan[i])''')
s = s[:a] + '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("return", "Chorus 1", i) if i in (1, 2) else ("fresh", None, None)   # the morning's words on the chorus's tune (line 0 designed on it); its last line new
        if sec == "Verse 2": return ("again", "Verse 1", i)
        if kind in ("Chorus", "Tag"): return ("fresh", None, None)
''' + s[b:]
R('''        rule = (sec, i) == ("Chorus 1", 0) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''',
  '''        rule = sec == "Verse 1" and i == len(LINES[sec]) - 1''')
R('''        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("copy", "return", "plan", "tail") and (s0, i0) in built:''', '''        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if (sec, i) in FIXR: r = ("ons", [FIXR[(sec, i)][k] for k in sorted(FIXR[(sec, i)])], None)   # Q15 A: the designed rhythm, known ahead
        if h in ("copy", "return", "plan", "tail") and (s0, i0) in built:''')
R('''                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner, unitbars=ub or None)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")''',
  '''                ns = fresh_line(sy, rng, U, tmin, sec, last_max, FIXR.get((sec, i)), i=i, partner=partner, unitbars=ub or None)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                if (sec, i) in PIN: ns = [n_ for n_ in ns if not n_["slur"]]                   # Q15 A: one note a syllable where the notes are designed''')
R('''                    if (sec, i) in CARRY and _try < 6:                                    # 329: the drawn extreme on this line''',
  '''                    if (sec, i) in PIN or (sec, i) in HOLDP or (sec, i) in COPYON:         # Q15 A: the designed notes
                        fx = dict(fx or {})
                        if (sec, i) in COPYON:
                            S_ = built[COPYON[(sec, i)]]; SU_ = line_start(*COPYON[(sec, i)]); sp_ = {n_["on"] - SU_: n_["p"] for n_ in S_ if not n_["slur"]}
                            for j, n_ in enumerate(ns):
                                if n_["on"] - U in sp_ and lo <= sp_[n_["on"] - U] <= hi: fx[j] = sp_[n_["on"] - U]
                            for j in range(1, len(ns) - 1):                                    # a syllable between two of them: a step between, not a leap
                                if j not in fx and j - 1 in fx and j + 1 in fx:
                                    a_, b_ = fx[j - 1], fx[j + 1]; ch_ = M.chord_for(ns[j], notes_on_all | {x_["on"] for x_ in ns})
                                    cq = [p for p in range(min(a_, b_) - 1, max(a_, b_) + 2) if p % 12 in M.SCALE and lo <= p <= hi and not tri(p, ch_)]
                                    if cq: fx[j] = min(cq, key=lambda p: (abs(p - (a_ + b_) / 2), p == a_, p))
                        for k_, q_ in PIN.get((sec, i), {}).items(): fx[next(j for j, n_ in enumerate(ns) if n_["syl"] == len(sy) + k_)] = q_
                        if (sec, i) in HOLDP:                                                  # 'thought': G or D in the register, near the contour
                            j_ = next(j for j, n_ in enumerate(ns) if n_["syl"] == HOLDP[(sec, i)])
                            cq = [p for p in range(lo, hi + 1) if p % 12 in (7, 2)]
                            fx[j_] = rng.choices(cq, [math.exp(-(p - shape[j_][0]) ** 2 / 8) + 1e-9 for p in cq])[0]
                    if (sec, i) in CARRY and _try < 6:                                    # 329: the drawn extreme on this line''')
R('''                for n, p in zip(ns, ps): n["p"] = p
                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1''',
  '''                for n, p in zip(ns, ps): n["p"] = p
                for n_ in ns:
                    if n_["syl"] - len(sy) in PIN.get((sec, i), {}) or n_["syl"] == HOLDP.get((sec, i)) or (sec, i) in COPYON: n_["pin"] = True
                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1''')
R('''        n = ns[j]; ch = M.chord_for(n, on_)
        for q in (n["p"] - 1, n["p"] + 1):''', '''        n = ns[j]; ch = M.chord_for(n, on_)
        if n.get("pin"): continue                                                          # a designed note stays (Q15 A)
        for q in (n["p"] - 1, n["p"] + 1):''')
R('''        if n["line"] in built_ret or n.get("pass358"): continue''', '''        if M.chord_for(n, on) == "E" and n["p"] % 12 == 7: n["p"] += 1; STATS["the bridge's E: a sung G raised to G-sharp"] += 1   # finding 375
        if n["line"] in built_ret or n.get("pass358") or n.get("pin"): continue''')
R('''        if n["p"] % 12 in (5, 0) and M.clash(n["p"], ch_):''', '''        if n["p"] % 12 in OUT_PCS and M.clash(n["p"], ch_):''')
R('''DESIGN_GATES = []                                                                     # the default path: none in force''',
  '''DESIGN_GATES = ["design: 'thought' held on G or D, 'morning' held on it in the last chorus; 'before it's done' D C B A (choruses), C B A G (last chorus); the tag on A; the chorus over the verse (Q14 A, Q15 A)"]
FIXR = {("Chorus 1", 0): {0: 0, 1: 12, 2: 24, 3: 54, 4: 60, 5: 72, 6: 84},             # 'HOLD that THOUGHT (held), I'm STILL COM-ing'
        ("Last Chorus", 0): {0: 12, 1: 24, 2: 54, 3: 60, 4: 66, 5: 72, 6: 78, 7: 84}}   # 'It's MOR (held) -ning, and I HELD the THOUGHT': the held note where 'thought' was
assert len(LINES["Last Chorus"][0]) == 8, LINES["Last Chorus"][0]
COPYON = {("Last Chorus", 0): ("Chorus 1", 0)}                                        # its notes on the chorus's onsets take the chorus's pitches
assert len(LINES["Chorus 1"][0]) == 7, LINES["Chorus 1"][0]
HOLDP = {("Chorus 1", 0): 2}                                                         # 'thought' on G or D
PIN = {("Chorus 1", 3): {-4: 62, -3: 60, -2: 59, -1: 57}, ("Last Chorus", 3): {-4: 60, -3: 59, -2: 57, -1: 55}, ("Tag", 1): {-1: 57}}
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}; g = DESIGN_GATES[0]
    by = collections.defaultdict(list)
    for n in notes:
        if not n.get("slur"): by[n["line"]].append(n)
    c0, c3, l0, l3, t1 = (by.get(k, []) for k in ("Chorus 1:0", "Chorus 1:3", "Last Chorus:0", "Last Chorus:3", "Tag:1"))
    if not (len(c0) == 7 and len(c3) >= 4 and len(l0) == 8 and len(l3) >= 4 and t1): f[g] = "missing"; return f
    hold = c0[2]["p"] % 12 in (7, 2) and c0[3]["on"] - c0[2]["on"] >= 30 and l0[1]["p"] == c0[2]["p"] and l0[2]["on"] - l0[1]["on"] >= 30
    done = [n["p"] for n in c3[-4:]] == [62, 60, 59, 57] and [n["p"] for n in l3[-4:]] == [60, 59, 57, 55] and t1[-1]["p"] == 57
    vp = [n["p"] for n in notes if n["sec"] == "Verse 1"]; cp = [n["p"] for n in notes if n["sec"] == "Chorus 1"]
    lift = float(np.median(cp)) - float(np.median(vp)) >= 3 and max(cp) > max(vp)
    if not (hold and done and lift): f[g] = dict(hold=hold, done=done, lift=lift)
    return f
def design_reg(R_, info):
    """325: the designed notes (G3-D4) inside the chorus's drawn register; the chorus over the verse."""
    vm, vh, vl = R_["Verse"]; cm, ch, cl = R_["Chorus"]
    return cl <= 55 and ch >= 62 and cm - vm >= 3 and ch - vh >= 3
DESIGN_REG.append(("the designed notes inside the chorus register; the chorus over the verse (Q14 A, Q15 A)", design_reg))''')
R('''    f = gate_fails(c, c.get("judge"))
    for g in GATES:''', '''    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))
    for g in DESIGN_GATES + GATES:''')
R('''        fails = gate_fails(c, c["judge"]); info = c["info"]''', '''        fails = gate_fails(c, c["judge"]); fails.update(design_fails(c)); info = c["info"]''')
R('''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in list(GATES) + sorted(k for k in would if k not in GATES)]''',
  '''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in DESIGN_GATES + list(GATES) + sorted(k for k in would if k not in GATES and k not in DESIGN_GATES)]''')
R('N = _N; SEED = 20261110 + 401', 'N = _N; SEED = 20261110 + 445')
R('open(f"{HERE}/lyric_p40.py", "rb").read()', 'open("/home/claude/p49/lyric_p45.py", "rb").read()')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_v116_p40.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_p45.py {N} {MODE}"')
R('open(f"{H116}/melody_v116_p40_{MODE}{_TAG}.pkl", "wb"))', 'open(f"/home/claude/p49/melody_p45_{MODE}{_TAG}.pkl", "wb"))')
R('''    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''',
  '''    plans = [(p[:len(LINES[sec])], w) for p, w in plans]                                  # four-line sections: each plan cut to its first lines
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''')
R(''', Pre=draw_plan(rng, "Pre 1", PRE_PLANS),''', ''',''')
R('''if j > 0 and n["on"] % BEAT and q % 12 not in M.SCALE and "358" not in OFF''',
  '''if j > 0 and n["on"] % BEAT and q % 12 in (M.SUNGPC - M.SCALE) and "358" not in OFF''')   # 358 read on the song's own sung extras (373): G-sharp
R('ROW_LO, ROW_HI = M.LO, TOP; PLACE = "centre"', 'ROW_LO, ROW_HI = M.LO, TOP; PLACE = "high"                                             # Q14 A: the song placed high in the row, so the chorus opens to its top')
R('CAL_STOP.append(f"round {rd + 1}: {sorted(big & big_prev)}', 'CAL_STOP.append(f"round {CAL_ROUNDS[0]}: {sorted(big & big_prev)}')   # finding 376: rd is the round's reading there
open("/home/claude/p49/melody_p45.py", "w").write(s)
print("written")
