"""Writes melody_p44.py: song 44, Keeping Time, on the v116 port (songs/p47/melody_v116_p40.py), built as song 43 was (songs/p47/gen_p43_v116.py):
the same form of two-bar lines, with this song's constants, lyric, key and designs (intake Q1-Q16)."""
s = open("/home/claude/p47/melody_v116_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
s = '''"""ZenEng v116 -- song 44, Keeping Time, on the v116 port (fixes 355-363 in force; findings from 365). Mid-tempo dance-pop, q = 112, four on the
floor, straight (Q5 A); the frame E-flat major, the verses in C minor (the relative pair, Q9 A); a mezzo (row G3-D5, Q6 A); 80 bars (Q7 A).
Designs in force, named (Q16 A):
  'Two clocks on the same wall' rocks between two pitches a scale step apart; 'It was always the same wall' (the last chorus) on the same two.
  'Can't help keeping time, keeping time': one rhythmic cell twice, the second a scale step higher.
  'Fall on the one': every post-chorus phrase lands on a downbeat, the two 'one's on the clocks' two pitches.
  A design gate (317), its pass rate printed. The verse closes on C; the song ends on E-flat.
Usage: PYTHONHASHSEED=0 python3 melody_p44.py N main|ctl [tag]
The v116 port it is built on:
''' + s[3:]
R('sys.path[:0] = ["/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]',
  'sys.path[:0] = ["/home/claude/p48", "/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]')
R('import lyric_p40 as L', 'import lyric_p44 as L')
a = s.index("M.TONIC = 2;"); b = s.index("STOP_BARS = set()")
s = s[:a] + '''M.TONIC = 3; M.SCALE = {3, 5, 7, 8, 10, 0, 2}; M.SUNGPC = M.SCALE | {11, 6}             # E-flat major; B natural (G, V of C minor) and G-flat sung (344)
ETON = 3                                                                              # the song ends on E-flat (the chorus's home); the verse closes on C
OUT_PCS = (11, 6)
M.CH = {"Eb": (3, {3, 7, 10}), "Fm": (5, {5, 8, 0}), "Gm": (7, {7, 10, 2}), "Ab": (8, {8, 0, 3}), "Bb": (10, {10, 2, 5}), "Cm": (0, {0, 3, 7}), "G": (7, {7, 11, 2})}
M.ROMAN = {"Eb": "I", "Fm": "ii", "Gm": "iii", "Ab": "IV", "Bb": "V", "Cm": "vi", "G": "III"}
M.QBPM = 112; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 55; TOP = 74; M.SUMMIT = TOP     # the voice row G3-D5 (Q6 A)
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
FEEL = "mid-tempo dance-pop, q = 112, four on the floor, straight (Q5 A)"
PLAN = {"Intro": ["Cm", "Ab", "Eb", "Bb"] * 2, "Verse": ["Cm", "Ab", "Eb", "Bb", "Cm", "Ab", "Bb", "Cm"], "Pre": ["Fm", "Gm", "Ab", "Bb"],
        "Chorus": ["Eb", "Bb", "Cm", "Ab", "Eb", "Bb", "Ab", "Bb"], "LastChorus": ["Eb", "Bb", "Cm", "Ab", "Eb", "Bb", "Ab", "Bb"],
        "Post": ["Eb", "Bb", "Cm", "Ab"], "LastPost": ["Eb", "Bb", "Ab", "Eb"], "Bridge": ["Ab", "Eb", "Fm", "Cm", "Ab", "Bb", "G", "G"], "Outro": ["Cm", "Ab", "Bb", "Eb"]}
FORM = [("Intro", "Intro", 8), ("Verse 1", "Verse", 8), ("Pre 1", "Pre", 4), ("Chorus 1", "Chorus", 8), ("Post 1", "Post", 4),
        ("Verse 2", "Verse", 8), ("Pre 2", "Pre", 4), ("Chorus 2", "Chorus", 8), ("Post 2", "Post", 4), ("Bridge", "Bridge", 8),
        ("Last Chorus", "Chorus", 8), ("Post 3", "Post", 4), ("Outro", "Outro", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else "LastPost" if nm == "Post 3" else kind]; b += nb
NBARS = b; assert NBARS == 80 and len(CHORD) == NBARS
''' + s[b:]
R('SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"]',
  'SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Post 1", "Verse 2", "Pre 2", "Chorus 2", "Post 2", "Bridge", "Last Chorus", "Post 3"]')
R('SLOTS = {"Verse": [2, 1, 3, 3, 2, 1], "Pre": [2, 2], "Chorus": [2] * 8, "Bridge": [2, 1, 1, 2, 1, 1], "Last Chorus": [2] * 9}',
  'SLOTS = {"Verse": [2] * 4, "Pre": [2] * 2, "Chorus": [2] * 4, "Post": [2] * 2, "Bridge": [2] * 4, "Last Chorus": [2] * 4}      # every line two bars')
R('SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}',
  'SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1", "Post 2": "Post 1"}')
R('''         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}''',
  '''         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}
    R["Post"] = R["Chorus"]                                                            # the post-chorus sings in the chorus's register''')
R('''TRIAD = {2, 6, 9}
ENDING_NEEDS.update(Chorus={M.TONIC % 12})                                            # 311: the hook (and the tag that copies it) ends on the tonic
def end_ok(sec, i, p):
    if sec == "Chorus 1" and i == 0: return (p - M.TONIC) % 12 == 0                       # the hook ends where the last chorus ends (its tag): the tonic
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return (p - M.TONIC) % 12 != 0                                   # the verse ends off the tonic
    if sec == "Chorus 1": return p % 12 in TRIAD                                         # an earlier chorus on a note of the tonic triad
    return True''', '''TRIAD = {3, 7, 10}
ENDING_NEEDS.update(Verse={0}, Post={ETON})                                          # 311: the verse closes on C; the last post-chorus (the song's last line) on E-flat
def end_ok(sec, i, p):
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return p % 12 == 0                                             # the verse closes in C minor (Q9 A)
    if sec == "Post 3": return (p - ETON) % 12 == 0                                      # 'nobody's leaving anymore': home
    return True''')
a = s.index('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)'''); b = s.index('''        plan = plans[kind]; first = plan.index(plan[i])''')
s = s[:a] + '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Post 2": return ("copy", "Post 1", i)
        if sec == "Last Chorus": return ("rock", None, None) if i == 2 else ("copy", "Chorus 1", i)   # 'It was always the same wall'
        if sec == "Post 3": return ("copy", "Post 1", 0) if i == 0 else ("post", None, None)        # 'Nobody's leaving anymore'
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 2: return ("rock", None, None)                       # Q16 A: the two clocks
        if sec == "Chorus 1" and i == 3: return ("cell", None, None)                       # Q16 A: keeping time, keeping time
        if sec == "Post 1": return ("post", None, None)                                    # Q16 A: on the one
        if kind in ("Chorus", "Post"): return ("fresh", None, None)
''' + s[b:]
R('''        rule = (sec, i) == ("Chorus 1", 0) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''',
  '''        rule = sec == "Verse 1" and i == len(LINES[sec]) - 1''')
R('''        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("copy", "return", "plan", "tail") and (s0, i0) in built:''', '''        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("rock", "cell", "post"):                                                    # Q16 A: the designed lines
            ns_ = design_line(rng, h, sec, i, U, meta, notes_on_all)
            r = ("ns", ns_, "design") if ns_ else ("fail", "design", None)
        elif h in ("copy", "return", "plan", "tail") and (s0, i0) in built:''')
R('''            if h in ("copy", "return", "plan", "tail") and (prefit(sec, i) or ("",))[0] == "ns":''',
  '''            if h in ("copy", "return", "plan", "tail", "rock", "cell", "post") and (prefit(sec, i) or ("",))[0] == "ns":''')
R('''                meta["kinds"][(sec, i)] = kd if h != "tail" else "tail"''', '''                meta["kinds"][(sec, i)] = kd if h != "tail" else "tail"
                if h in ("rock", "cell", "post"): meta["kinds"][(sec, i)] = "design"''')
R('''            elif h in ("copy", "return", "plan", "tail"):
                globals().__setitem__("WHERE", (sec, i)); return _fail("align: the words do not fit the returning tune")''',
  '''            elif h in ("copy", "return", "plan", "tail", "rock", "cell", "post"):
                globals().__setitem__("WHERE", (sec, i)); return _fail("align: the words do not fit the returning tune")''')
R('''    built_ret = {f"{sec}:{i}" for sec, i, s0, i0, kd in meta["returns"] if kd != "sung again"}''',
  '''    built_ret = {f"{sec}:{i}" for sec, i, s0, i0, kd in meta["returns"] if kd != "sung again"}
    built_ret |= {f"{sec}:{i}" for (sec, i), kd in meta["kinds"].items() if kd == "design" or (sec, i) in (("Chorus 2", 2), ("Chorus 2", 3), ("Last Chorus", 3), ("Post 2", 0), ("Post 2", 1), ("Post 3", 0))}   # the design and its copies left alone''')
R('''        if n["p"] % 12 in (5, 0) and M.clash(n["p"], ch_):''', '''        if n["p"] % 12 in OUT_PCS and M.clash(n["p"], ch_):''')
R('''    REGS, meta["registers"] = draw_registers(rng)''', '''    REGS, meta["registers"] = draw_registers(rng); DES.clear()''')
R('''DESIGN_GATES = []                                                                     # the default path: none in force''',
  '''DESIGN_GATES = ["design: the two clocks rock a step apart; keeping time twice, a step higher; every post-chorus phrase on the one (Q16 A)"]
ROCK_R = {6: (0, 12, 24, 30, 36, 48), 7: (0, 6, 12, 18, 30, 36, 48)}                  # 'TWO CLOCKS on the SAME WALL'; 'It was AL-ways the SAME WALL'
CELL_R = (-24, -12, 0, 6, 12, 48, 54, 60)                                             # 'can't HELP | KEEP-ing TIME, | KEEP-ing TIME'
POST_R = {0: (-9, -6, -3, 0, 39, 42, 45, 48), 1: (0, 6, 12, 24, 30, 36, 42, 48)}      # 'fall on the ONE, fall on the ONE'; 'NO-bo-dy's COUNT-ing a-ny-MORE'
DES = {}
def sstep(p, k):
    """k scale steps from p (down when k < 0)."""
    q = p
    for _ in range(abs(k)):
        q += -1 if k < 0 else 1
        while q % 12 not in M.SCALE: q += -1 if k < 0 else 1
    return q
def design_pick(R_):
    """Q16 A: the clocks' pitches (T on E-flat's G or E-flat; the step under it F or D, on the B-flat chord), the cell's start x (B-flat: the cell
    ends C on the A-flat chord and D on the B-flat chord), and the post-chorus landings, all inside the chorus's drawn register."""
    mu, hi, lo = R_["Chorus"]; hi, lo = int(hi), int(lo); _, phi, plo = R_["Post"]; phi, plo = int(phi), int(plo)
    Ts = [t for t in range(lo, hi + 1) if t % 12 in (7, 3) and sstep(t, -1) >= lo and sstep(t, -3) >= plo and sstep(t, 2) <= phi]
    xs = [x for x in range(lo, hi + 1) if x % 12 == 10 and sstep(x, -1) >= lo and sstep(x, 2) <= hi]
    if not Ts or not xs: return None
    T = min(Ts, key=lambda t: (abs(t - (mu + hi) / 2), t)); x = max(xs); base = sstep(T, -3)
    l1 = [p for p in range(plo, phi + 1) if p % 12 in (8, 0, 3)]; l3 = [p for p in range(plo, phi + 1) if p % 12 == ETON]
    if not l1 or not l3: return None
    return dict(T=T, U=sstep(T, -1), x=x, land1=min(l1, key=lambda p: (abs(p - base), p)), land3=min(l3, key=lambda p: (abs(p - base), p)))
def design_line(rng, h, sec, i, U, meta, notes_on):
    """Q16 A. 'rock': the clocks, alternating T and the step under it, the last syllable ('wall') on the step under.
    'cell': 'can't help', then 'keeping time' twice, the second a scale step higher. 'post': 'fall on the one' twice, landing on T and then the
    step under it; 'nobody's counting / leaving anymore' falling from T to its landing on a downbeat (the song's last on E-flat)."""
    sy = LINES[sec][i]
    if "pick" not in DES: DES["pick"] = design_pick(CUR_REGS)
    d = DES["pick"]
    if d is None: STATS["design: no pitches in the chorus register"] += 1; return None
    T, Ud, x = d["T"], d["U"], d["x"]
    if h == "rock":
        r_ = ROCK_R[len(sy)]; n = len(sy); ps = [Ud if (n - 1 - k) % 2 == 0 else T for k in range(n)]
    elif h == "cell":
        r_ = CELL_R; c1 = [x, x, sstep(x, 1)]; ps = [sstep(x, -1), x] + c1 + [sstep(p, 1) for p in c1]
    else:
        r_ = POST_R[i]
        if i == 0: ps = [sstep(T, 2), sstep(T, 1), sstep(T, 1), T, sstep(Ud, 2), sstep(Ud, 1), sstep(Ud, 1), Ud]
        else: ps = [T, T, sstep(T, -1), T, sstep(T, -1), sstep(T, -2), sstep(T, -3), d["land3"] if sec == "Post 3" else d["land1"]]
    assert len(r_) == len(sy) == len(ps), (sec, i, len(r_), len(sy), len(ps))
    return [dict(on=U + t, p=p, syl=k, slur=False, stress=sy[k][1]) for k, (t, p) in enumerate(zip(r_, ps))]
CUR_REGS = {}
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}; g = DESIGN_GATES[0]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    rk, cl, lc, p0, p1, p3 = (by.get(k, []) for k in ("Chorus 1:2", "Chorus 1:3", "Last Chorus:2", "Post 1:0", "Post 1:1", "Post 3:1"))
    if not (len(rk) == 6 and len(cl) == 8 and len(lc) == 7 and len(p0) == 8 and len(p1) == 8 and len(p3) == 8): f[g] = "missing"; return f
    def rocks(ns): return len({n["p"] for n in ns}) == 2 and all(a["p"] != b_["p"] for a, b_ in zip(ns, ns[1:])) and sstep(max(n["p"] for n in ns), -1) == min(n["p"] for n in ns)
    rock = rocks(rk) and rocks(lc) and {n["p"] for n in rk} == {n["p"] for n in lc}
    a3, b3 = cl[2:5], cl[5:8]
    cell = [n["on"] + BAR for n in a3] == [n["on"] for n in b3] and all(sstep(m["p"], 1) == n["p"] for m, n in zip(a3, b3))
    one = all(n["on"] % BAR == 0 for n in (p0[3], p0[7], p1[-1], p3[-1])) and (p3[-1]["p"] - ETON) % 12 == 0 and {p0[3]["p"], p0[7]["p"]} == {n["p"] for n in rk}
    if not (rock and cell and one): f[g] = dict(rock=rock, cell=cell, one=one)
    return f
def design_reg(R_, info):
    """325: the design's pitches inside the chorus's drawn register."""
    return design_pick(R_) is not None
DESIGN_REG.append(("the design's pitches inside the chorus register (Q16 A)", design_reg))''')
R('''    REGS, meta["registers"] = draw_registers(rng); DES.clear()''', '''    REGS, meta["registers"] = draw_registers(rng); DES.clear(); CUR_REGS.clear(); CUR_REGS.update(REGS)''')
R('''    f = gate_fails(c, c.get("judge"))
    for g in GATES:''', '''    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))
    for g in DESIGN_GATES + GATES:''')
R('''        fails = gate_fails(c, c["judge"]); info = c["info"]''', '''        fails = gate_fails(c, c["judge"]); fails.update(design_fails(c)); info = c["info"]''')
R('''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in list(GATES) + sorted(k for k in would if k not in GATES)]''',
  '''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in DESIGN_GATES + list(GATES) + sorted(k for k in would if k not in GATES and k not in DESIGN_GATES)]''')
R('N = _N; SEED = 20261110 + 401', 'N = _N; SEED = 20261110 + 444')
R('open(f"{HERE}/lyric_p40.py", "rb").read()', 'open("/home/claude/p48/lyric_p44.py", "rb").read()')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_v116_p40.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_p44.py {N} {MODE}"')
R('open(f"{H116}/melody_v116_p40_{MODE}{_TAG}.pkl", "wb"))', 'open(f"/home/claude/p48/melody_p44_{MODE}{_TAG}.pkl", "wb"))')
R('''    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''',
  '''    plans = [(p[:len(LINES[sec])], w) for p, w in plans]                                  # four-line sections: each plan cut to its first lines
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''')
R('''if j > 0 and n["on"] % BEAT and q % 12 not in M.SCALE and "358" not in OFF''',
  '''if j > 0 and n["on"] % BEAT and q % 12 in (M.SUNGPC - M.SCALE) and "358" not in OFF''')   # 358 read on the song's own sung extras (344): B natural, G-flat
R('''    R = {k: widen_329(v, lo, hi) for k, v in R.items()}''', '''    R = {k: widen_329(v, lo, hi) for k, v in R.items()}
    vf_ = lo + (1 if rng.random() < 0.5 else 0); vc_ = min(hi, vf_ + 7); vm_ = (vf_ + vc_) / 2              # Q17 C: a narrow verse (seven semitones) low in the song's range
    ch_ = hi; cl_ = max(lo, min(vc_ - 1, ch_ - 10)); cm_ = (cl_ + ch_) / 2                                    # the chorus over it and wider, to the song's top
    R["Verse"] = (vm_, vc_, vf_); R["Chorus"] = (cm_, ch_, cl_); R["Post"] = (cm_, ch_, vf_); R["Pre"] = ((vm_ + cm_) / 2, ch_, vf_)   # the post-chorus falls back toward the verse
    globals().update(V_MU=vm_, V_CAP=vc_, V_FLOOR=vf_)''')
R('''CARRY_LOW = [s_ for s_ in SUNG if KIND[s_] in ("Verse", "Bridge") and s_ in ("Verse 1", "Bridge")]''',
  '''CARRY_LOW = [s_ for s_ in SUNG if s_ == "Bridge"]                                    # Q17 C: the verse stays narrow; the bridge carries the song's low note (329)''')
R('''DESIGN_REG.append(("the design's pitches inside the chorus register (Q16 A)", design_reg))''', '''DESIGN_REG.append(("the design's pitches inside the chorus register (Q16 A)", design_reg))
def lift_reg(R_, info):
    """Q17 C: the chorus over the narrow verse, and wider."""
    vm, vh, vl = R_["Verse"]; cm, ch, cl = R_["Chorus"]
    return cm - vm >= 3 and ch - vh >= 3 and (ch - cl) - (vh - vl) >= 3
DESIGN_REG.append(("the chorus over the narrow verse and wider (Q17 C)", lift_reg))''')
R('''    if not (rock and cell and one): f[g] = dict(rock=rock, cell=cell, one=one)''', '''    vp = [n["p"] for n in notes if n["sec"] == "Verse 1"]; cp = [n["p"] for n in notes if n["sec"] == "Chorus 1"]
    lift = float(np.median(cp)) - float(np.median(vp)) >= 3 and max(cp) - min(cp) > max(vp) - min(vp)          # Q17 C, read on what is sung
    if not (rock and cell and one and lift): f[g] = dict(rock=rock, cell=cell, one=one, lift=lift)''')
R('''DESIGN_GATES = ["design: the two clocks rock a step apart; keeping time twice, a step higher; every post-chorus phrase on the one (Q16 A)"]''',
  '''DESIGN_GATES = ["design: the two clocks rock a step apart; keeping time twice, a step higher; every post-chorus phrase on the one (Q16 A); the chorus over the narrow verse and wider (Q17 C)"]''')
R('ROW_LO, ROW_HI = M.LO, TOP; PLACE = "centre"', 'ROW_LO, ROW_HI = M.LO, TOP; PLACE = "high"                                             # Q17 C: the song placed high in the row, so the chorus opens to its top')
open("/home/claude/p48/melody_p44.py", "w").write(s)
print("written")
