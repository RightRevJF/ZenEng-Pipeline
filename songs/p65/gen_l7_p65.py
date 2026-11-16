"""gen_l7_p65.py: writes melody_l7_p65.py (song 55, Your Yard Man, under Luthier v7) from song 54's melody_l7_p64.py (song 48's Luthier v7
file, the engine of record, with song 54's parts and its guards for a song with no bridge), changing only the song's own parts: the lyric
(lyric_p65.py; 'callin'' read CALL-in; 'own' stressed), A major for a baritone (the search row A2-E4), q = 120, a country two-step, 4/4;
the form (A): intro 4; verse 16, chorus 14, twice; break 4; verse 16, chorus 14; tag 2; ending 2 = 102 bars; verse lines two bars, the
chorus's lines 1-4 and 9-10 one bar, its lines 5-8 two; the tag's lines one bar each; the chart drawn by 438 with the designs' half-bars
kept; the hook (A): the call and its answer, and the chorus above the verse. Every patch is asserted to match exactly once. The song's
choices: intake.py."""
SRC = "/home/claude/p64/melody_l7_p64.py"; DST = "/home/claude/p65/melody_l7_p65.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
def CUT(a, b, new):
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (a[:80], b[:80])
    i0 = s.rindex("\n", 0, s.index(a)) + 1; i1 = s.rindex("\n", 0, s.index(b)) + 1
    s = s[:i0] + new + s[i1:]
HEAD = '''"""Luthier v7 -- song 55, Your Yard Man, by gen_l7_p65.py from song 54's Luthier v7 file (song 48's engine of record with song 54's parts).
A country story song with an anthem's chorus (N/A), a neotraditional two-step, A major, q = 120, for a baritone (the search row A2-E4).
102 bars: intro 4; verse 16, chorus 14, twice; break 4; verse 16, chorus 14; tag 2; ending 2. Verse lines two bars; the chorus's lines
1-4 and 9-10 one bar, lines 5-8 two; the tag's two lines one bar each. Designs in force (317, pass rates printed): the hook (A): 'I'm your
yard man' (chorus lines 1 and 9) jumps A3 C#4 to E4 on 'yard', the chorus's top, and 'but I'm my own man' (line 10) answers on the same
rhythm, E4 C#4 B3 C#4, home on A3; every chorus the same; the tag sings both, 'man' held. The chorus above the verse. No bridge.
Usage: PYTHONHASHSEED=0 python3 melody_l7_p65.py N main|ctl [tag]
"""
'''
i0 = s.index('"""Luthier v7 -- song 54'); i1 = s.index('[tag]\n"""\n', i0) + len('[tag]\n"""\n')
s = s[:i0] + HEAD + s[i1:]
P('SONG8 = "54"', 'SONG8 = "55"')
s = s.replace("/home/claude/p64/", "/home/claude/p65/")
P('sys.path[:0] = ["/home/claude/p64", ', 'sys.path[:0] = ["/home/claude/p65", ')
P("import lyric_p64 as L", "import lyric_p65 as L")
P('''open("/home/claude/p65/lyric_p64.py", "rb").read()''', '''open("/home/claude/p65/lyric_p65.py", "rb").read()''')
# ---- the lexicon (the writer's answer A) ----
CUT('LEX64 = {"sleepin\'"', 'lyricsearch.FUNCTION.add("\'n\'")', '''LEX64 = {"callin'": "K AO1 L IH0 N"}                                                    # the writer's reading (A)
for _w, _p in LEX64.items(): lyricsearch.OVERRIDE[_w] = (_p,)
''')
P('''lyricsearch.FUNCTION.add("'n'")                                                      # Git 'n' Split: the 'n' unstressed (A)''',
  '''lyricsearch.FUNCTION.discard("own")                                                  # 'my OWN man', against 'your YARD man' (the hook, A)''')
# ---- the frame: A major, q = 120 ----
CUT("M.TONIC = 7; M.SCALE", "LIFT2 = 0 ", '''M.TONIC = 9; M.SCALE = {9, 11, 1, 2, 4, 6, 8}; M.SUNGPC = set(M.SCALE)                    # A major (the key, A)
ETON = 9                                                                              # the song's tonic: A (endings)
OUT_PCS = ()
M.CH = {"A": (9, {9, 1, 4}), "D": (2, {2, 6, 9}), "E": (4, {4, 8, 11}), "F#m": (6, {6, 9, 1}), "Bm": (11, {11, 2, 6}), "C#m": (1, {1, 4, 8})}
M.ROMAN = {"A": "I", "D": "IV", "E": "V", "F#m": "vi", "Bm": "ii", "C#m": "iii"}
M.QBPM = 120; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 64; M.SUMMIT = TOP     # the search row A2-E4: the hook's E4 is the song's top (the key, A; the hook, A)
''')
P('FEEL = "mid-tempo country story song, a neotraditional two-step, q = 120, 4/4 (the sound, A; the form, A)"',
  'FEEL = "a country story song with an anthem chorus, a neotraditional two-step, q = 120, 4/4 (song 54\'s sound; the form, A)"')
CUT('PLAN = {"Intro": ["G", "C", "D", "G"],', 'M.FORM, M.PLAN, M.BAR0', '''PLAN = {"Intro": ["A", "D", "E", "A"],
        "Verse": ["A", "A", "D", "A", "A", "A", "E", "E", "A", "A", "D", "A", "F#m", "D", "E", "E"],
        "Chorus": ["A", "D", "A", "E", "D", "A", "Bm", "E", "D", "A", "Bm", "E", "A", "A"],
        "Turnaround": ["D", "A", "E", "E"], "Tag": ["A", "A"], "Ending": ["D", "A"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 16), ("Chorus 1", "Chorus", 14), ("Verse 2", "Verse", 16), ("Chorus 2", "Chorus", 14),
        ("Turnaround", "Turnaround", 4), ("Verse 3", "Verse", 16), ("Chorus 3", "Chorus", 14), ("Tag", "Tag", 2), ("Ending", "Ending", 2)]   # the form, A: 102 bars
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 102 and len(CHORD) == NBARS
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Verse 3", "Chorus 3", "Tag"]
INSTRUMENTAL = ["Intro", "Turnaround", "Ending"]
DESIGN_HALF = {}                                                                      # the designs' bars keep the plan's chords (the hook, A): A under the call and the answer
for _c in ("Chorus 1", "Chorus 2", "Chorus 3"): DESIGN_HALF.update({(_c, 0): ("A", "A"), (_c, 12): ("A", "A"), (_c, 13): ("A", "A")})
DESIGN_HALF.update({("Tag", 0): ("A", "A"), ("Tag", 1): ("A", "A")})
''')
P('''SLOTS = {"Verse": [2] * 8, "Chorus": [2] * 6, "Tag": [2, 2]}   # every sung line in two bars (308; the form, A)''',
  '''SLOTS = {"Verse": [2] * 8, "Chorus": [1, 1, 1, 1, 2, 2, 2, 2, 1, 1], "Tag": [1, 1]}   # the form, A: one bar for lines of 4-7 syllables, two for the rest (308)''')
P('''CAPD = {"Verse": 62, "Chorus": 62, "Tag": 62}                                          # the hook (A): D4 the song's top''',
  '''CAPD = {"Verse": 64, "Chorus": 64, "Tag": 64}                                          # the hook (A): E4 the song's top''')
P('''TRIAD = {7, 11, 2}                                                                   # 311: no ending need; every chorus and the tag end as designed''',
  '''TRIAD = {9, 1, 4}                                                                    # 311: no ending need; every chorus and the tag end as designed''')
P('''PAIRS = {"Verse": ["Verse 1", "Verse 2", "Verse 3", "Verse 4"], "Pre": ["Pre 1", "Pre 2", "Pre 3"], "Bridge": ["Bridge"]}''',
  '''PAIRS = {"Verse": ["Verse 1", "Verse 2", "Verse 3"], "Pre": ["Pre 1", "Pre 2", "Pre 3"], "Bridge": ["Bridge"]}''')
# ---- how each line is made ----
P('''        if (sec, i) in DSPEC: return ("figure" if sec == "Chorus 1" else "chant", None, None)   # the designs: the hook (A), its homecoming in chorus 4 and the tag
        if sec in ("Chorus 2", "Chorus 3", "Chorus 4"): return ("again", "Chorus 1", i) if i == 4 else ("copy", "Chorus 1", i)   # line 5 new words (sung again); the rest on chorus 1's tune
        if sec in ("Verse 2", "Verse 3", "Verse 4"): return ("again", SRC[sec], i)''',
  '''        if (sec, i) in DSPEC: return ("figure" if sec == "Chorus 1" else "chant", None, None)   # the designs: the call and the answer (A), and the tag's
        if sec in ("Chorus 2", "Chorus 3"):                                                 # lines with chorus 1's words on its tune; new words sung again
            same = i in (0, 1, 8, 9) or (sec == "Chorus 2" and i in (2, 3))
            return ("copy", "Chorus 1", i) if same else ("again", "Chorus 1", i)
        if sec in ("Verse 2", "Verse 3"): return ("again", SRC[sec], i)''')
P('''tuple(DSPEC) + (("Chorus 2", 5), ("Chorus 3", 5))}   # the designs and their copies left alone''',
  '''tuple(DSPEC) + tuple((s_, j_) for s_ in ("Chorus 2", "Chorus 3") for j_ in (0, 8, 9))}   # the designs and their copies left alone''')
# ---- the designs ----
CUT('DESIGN_GATES = ["design: the hook:', 'CARRY_LOW = [', '''DESIGN_GATES = ["design: the hook: 'I'm your yard man' (chorus lines 1 and 9) A3 C#4, E4 on 'yard', C#4; 'but I'm my own man' (line 10) E4 C#4 B3 C#4, home on A3; every chorus the same; E4 the song's top, sung only on the hook",
                "design: the tag: the call and the answer, 'man' held to the bar's end on A3"]
CALL = [(12, 57, 6), (18, 61, 6), (24, 64, 12), (36, 61, 10)]                          # I'm your yard man: A3 C#4, 'yard' E4 on beat 3 over A, 'man' C#4
ANSWER = [(6, 64, 6), (12, 61, 6), (18, 59, 6), (24, 61, 12), (36, 57, 10)]            # but I'm my own man: E4 C#4 B3, 'own' C#4 on beat 3, 'man' home on A3 over A
ANSWER_T = ANSWER[:-1] + [(36, 57, 12)]                                                 # the tag: 'man' held to the bar's end
DSPEC = {("Chorus 1", 0): CALL, ("Chorus 1", 8): CALL, ("Chorus 1", 9): ANSWER, ("Tag", 0): CALL, ("Tag", 1): ANSWER_T}
BRIDGE_LOW = (52.0, 57, 45)                                                                 # no bridge (kept for the reader)
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The designed lines: the call and the answer ('figure': chorus 1's lines 1, 9 and 10, copied in choruses 2 and 3) and the tag's ('chant')."""
    sy = LINES[sec][i]; spec = DSPEC[(sec, i)]
    assert len(spec) == len(sy), (sec, i, len(spec), len(sy))
    out = []
    for k, (t, p, d) in enumerate(spec):
        n = dict(on=U + t, p=p, syl=k, slur=False, stress=sy[k][1], pin=True)
        if d is None: n["holdthrough"] = True
        else: n["fixdur"] = d
        out.append(n)
    return out
def design_fails(c):
    """317: the designs, read on what is sung; outside 275, their pass rates printed."""
    notes = c["notes"]; f = {}; g1, g2 = DESIGN_GATES[:2]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    rel = lambda k: [(n["on"] - line_start(*k), n["p"]) for n in by.get(f"{k[0]}:{k[1]}", [])]
    sp = lambda L_: [(t, p) for t, p, d in L_]
    fig = all(rel((s_, 0)) == sp(CALL) and rel((s_, 8)) == sp(CALL) and rel((s_, 9)) == sp(ANSWER) for s_ in ("Chorus 1", "Chorus 2", "Chorus 3"))
    hook_lines = {f"{s_}:{j_}" for s_ in ("Chorus 1", "Chorus 2", "Chorus 3") for j_ in (0, 8, 9)} | {"Tag:0", "Tag:1"}
    stop = max(n["p"] for n in notes) == 64 and all(n["line"] in hook_lines for n in notes if n["p"] >= 64)
    if not (fig and stop): f[g1] = dict(figure=fig, top=stop)
    tag = rel(("Tag", 0)) == sp(CALL) and rel(("Tag", 1)) == sp(ANSWER_T)
    if not tag: f[g2] = dict(tag=tag)
    return f
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hook aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(8) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in range(1, 8) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[2]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''')
# ---- the run ----
P("N = _N; SEED = 20261113 + 454", "N = _N; SEED = 20261113 + 455")
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p64.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p65.py {N} {MODE}"''')
P('''open(f"/home/claude/p65/runl7/melody_l7_p64_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p65/runl7/melody_l7_p65_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
