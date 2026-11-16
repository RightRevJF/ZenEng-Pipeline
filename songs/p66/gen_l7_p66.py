"""gen_l7_p66.py: writes melody_l7_p66.py (song 56, Terpsichore, under Luthier v7) from song 55's melody_l7_p65.py (song 48's Luthier v7
file, the engine of record, with songs 54 and 55's parts), changing only the song's own parts: the lyric (lyric_p66.py; 'sternum' and
"leaving's" read as the writer chose, 'own' stressed); E minor (the frame G, the scale E Aeolian, an A major chord borrowed from Dorian,
B major the dominant), a baritone (the search row B2-D4), q = 72, 4/4, a half-time soul groove; the form (A): intro 4; verse 8, chorus 10,
twice; bridge 6; breath 2; verse 8, chorus 10; outro 6 (the engine's 'Tag'); ending 2 = 74 bars; verse and bridge lines one bar, the
chorus's 'Come back, come back' lines two bars and the rest one, the outro's lines one bar and its last 'Come back' two; the type (A):
V/L Longing with Paradox's colour; the hook (A): two reaches, held on B, the band turning to C. Every patch is asserted to match exactly
once. The song's choices: intake.py."""
SRC = "/home/claude/p65/melody_l7_p65.py"; DST = "/home/claude/p66/melody_l7_p66.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
def CUT(a, b, new):
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (a[:80], b[:80])
    i0 = s.rindex("\n", 0, s.index(a)) + 1; i1 = s.rindex("\n", 0, s.index(b)) + 1
    s = s[:i0] + new + s[i1:]
HEAD = '''"""Luthier v7 -- song 56, Terpsichore, by gen_l7_p66.py from song 55's Luthier v7 file (song 48's engine of record with songs 54 and 55's parts).
A Longing love song with Paradox's colour (V/L), a slow-burn soul ballad, E minor, q = 72 (written at 144, half-time, as song 51), for a baritone (the search row B2-D4).
74 bars: intro 4; verse 8, chorus 10, twice; bridge 6; breath 2; verse 8, chorus 10; outro 6 ('Tag'); ending 2. Verse and bridge lines one
bar; the chorus's 'Come back, come back' (lines 1 and 4) two bars, the rest one; the outro's lines one bar, its last 'Come back' two.
Designs in force (317, pass rates printed): the hook (A): 'Come back, come back' G3 to B3 held, then D4 (the song's top) back to B3, held
while the band turns from Em to C (the deceptive turn, V/L); every chorus the same; the outro's last 'Come back' D4 to B3, held over C,
open. The chorus above the verse.
Usage: PYTHONHASHSEED=0 python3 melody_l7_p66.py N main|ctl [tag]
"""
'''
i0 = s.index('"""Luthier v7 -- song 55'); i1 = s.index('[tag]\n"""\n', i0) + len('[tag]\n"""\n')
s = s[:i0] + HEAD + s[i1:]
P('SONG8 = "55"', 'SONG8 = "56"')
s = s.replace("/home/claude/p65/", "/home/claude/p66/")
P('sys.path[:0] = ["/home/claude/p65", ', 'sys.path[:0] = ["/home/claude/p66", ')
P("import lyric_p65 as L", "import lyric_p66 as L")
P('''open("/home/claude/p66/lyric_p65.py", "rb").read()''', '''open("/home/claude/p66/lyric_p66.py", "rb").read()''')
P('''LEX64 = {"callin'": "K AO1 L IH0 N"}                                                    # the writer's reading (A)''',
  '''LEX64 = {"sternum": "S T ER1 N AH0 M", "leaving's": "L IY1 V IH0 NG Z"}                  # the writer's readings (A)''')
P('''lyricsearch.FUNCTION.discard("own")                                                  # 'my OWN man', against 'your YARD man' (the hook, A)''',
  '''lyricsearch.FUNCTION.discard("own")                                                  # 'its OWN kind of ravishing' (verse 3)''')
CUT("M.TONIC = 9; M.SCALE", "LIFT2 = 0 ", '''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = set(M.SCALE)                    # E minor on its relative major's frame (G), as songs 33 and 47 (the key, A)
ETON = 4                                                                              # the song's tonic: E (endings)
OUT_PCS = ()
M.CH = {"Em": (4, {4, 7, 11}), "A": (9, {9, 1, 4}), "C": (0, {0, 4, 7}), "G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "B": (11, {11, 3, 6}),
        "Am": (9, {9, 0, 4}), "Bm": (11, {11, 2, 6})}                                     # A: Dorian's IV (C# a chord tone, never sung, 375); B: the dominant (D# likewise)
M.ROMAN = {"Em": "i", "A": "IV", "C": "VI", "G": "III", "D": "VII", "B": "V", "Am": "iv", "Bm": "v"}
M.QBPM = 144; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 47; TOP = 62; M.SUMMIT = TOP     # the search row B2-D4: the hook's D4 is the song's top (the key, A; the hook, A)
''')
P('FEEL = "a country story song with an anthem chorus, a neotraditional two-step, q = 120, 4/4 (song 54\'s sound; the form, A)"',
  'FEEL = "a slow-burn soul ballad, q = 72 written at 144 with a half-time feel, 4/4 (the lane, A; the tempo, A)"')
CUT('PLAN = {"Intro": ["A", "D", "E", "A"],', 'M.FORM, M.PLAN, M.BAR0', '''_D = lambda L_: [c_ for c_ in L_ for _ in (0, 1)]                                       # written at double tempo (q = 144, felt in half time at 72): each chord two bars
PLAN = {"Intro": _D(["Em", "A", "C", "B"]),
        "Verse": _D(["Em", "A", "Em", "A", "C", "G", "D", "B"]),
        "Chorus": _D(["Em", "C", "G", "D", "Em", "C", "A", "C", "D", "B"]),
        "Bridge": _D(["Am", "Em", "Am", "Em", "C", "D"]), "Breath": _D(["B", "B"]),
        "Tag": _D(["C", "G", "Am", "B", "Em", "C"]), "Ending": _D(["C", "C"])}
FORM = [("Intro", "Intro", 8), ("Verse 1", "Verse", 16), ("Chorus 1", "Chorus", 20), ("Verse 2", "Verse", 16), ("Chorus 2", "Chorus", 20),
        ("Bridge", "Bridge", 12), ("Breath", "Breath", 4), ("Verse 3", "Verse", 16), ("Chorus 3", "Chorus", 20), ("Tag", "Tag", 12), ("Ending", "Ending", 4)]   # the form, A: 74 bars at 72 (148 written)
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 148 and len(CHORD) == NBARS
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Verse 3", "Chorus 3", "Tag"]
INSTRUMENTAL = ["Intro", "Breath", "Ending"]
DESIGN_HALF = {}                                                                      # the designs' bars keep the plan's chords (the hook, A): Em, then C under the held B
for _c in ("Chorus 1", "Chorus 2", "Chorus 3"): DESIGN_HALF.update({(_c, k_): (c_, c_) for k_, c_ in ((0, "Em"), (1, "Em"), (2, "C"), (3, "C"), (8, "Em"), (9, "Em"), (10, "C"), (11, "C"))})
DESIGN_HALF.update({("Tag", k_): (c_, c_) for k_, c_ in ((8, "Em"), (9, "Em"), (10, "C"), (11, "C"))})
''')
P('''SLOTS = {"Verse": [2] * 8, "Chorus": [1, 1, 1, 1, 2, 2, 2, 2, 1, 1], "Tag": [1, 1]}   # the form, A: one bar for lines of 4-7 syllables, two for the rest (308)''',
  '''SLOTS = {"Verse": [2] * 8, "Chorus": [4, 2, 2, 4, 2, 2, 2, 2], "Bridge": [2] * 6, "Tag": [2, 2, 2, 2, 4]}   # the form, A: a line a bar at 72 (two written); the hook lines two (four written) (308)''')
P('''CAPD = {"Verse": 64, "Chorus": 64, "Tag": 64}                                          # the hook (A): E4 the song's top''',
  '''CAPD = {"Verse": 62, "Chorus": 62, "Bridge": 62, "Tag": 62}                           # the hook (A): D4 the song's top''')
P('''TRIAD = {9, 1, 4}                                                                    # 311: no ending need; every chorus and the tag end as designed''',
  '''TRIAD = {4, 7, 11}                                                                   # 311: no ending need; every chorus and the outro end as designed''')
P('''OS_SCALE = 1.0                                                                        # 349: 4.5 / 7.1 for a minor song (set by the song)
MTON = None                                                                           # 353: a minor song's tonic for the window measures (set by the song)''',
  '''OS_SCALE = 4.5 / 7.1                                                                 # 349: the kept minor rate (a minor song)
MTON = 4                                                                              # 353: the window measures read on E''')
P('''MAJ = {0, 2, 4, 5, 7, 9, 11}                                                         # a major song''',
  '''MAJ = {0, 2, 3, 5, 7, 8, 10}                                                         # 353: the natural minor scale, read on the tonic''')
P('''        if sec in ("Chorus 2", "Chorus 3"):                                                 # lines with chorus 1's words on its tune; new words sung again
            same = i in (0, 1, 8, 9) or (sec == "Chorus 2" and i in (2, 3))
            return ("copy", "Chorus 1", i) if same else ("again", "Chorus 1", i)''',
  '''        if sec in ("Chorus 2", "Chorus 3"): return ("copy", "Chorus 1", i)                 # the same words: chorus 1's tune''')
P('''tuple(DSPEC) + tuple((s_, j_) for s_ in ("Chorus 2", "Chorus 3") for j_ in (0, 8, 9))}   # the designs and their copies left alone''',
  '''tuple(DSPEC) + tuple((s_, j_) for s_ in ("Chorus 2", "Chorus 3") for j_ in (0, 3))}   # the designs and their copies left alone''')
CUT('DESIGN_GATES = ["design: the hook:', 'CARRY_LOW = [', '''DESIGN_GATES = ["design: the hook: 'Come back, come back' (chorus lines 1 and 4) G3, B3 held, D4, B3 held over C; every chorus the same; D4 the song's top, sung only on the hook",
                "design: the outro's last 'Come back' D4, B3 held over C to the bar's end (open)"]
HOOK = [(24, 55, 24), (48, 59, 36), (96, 62, 24), (120, 59, 72)]                       # Come back, come back (at 72): G3 on beat 2, 'back' B3 on beat 3 over Em; D4 on the next downbeat over C, 'back' B3 held
HOOK_T = [(24, 62, 24), (48, 59, 144)]                                                  # the outro: D4, then B3 held over Em into C, open
DSPEC = {("Chorus 1", 0): HOOK, ("Chorus 1", 3): HOOK, ("Tag", 4): HOOK_T}
BRIDGE_LOW = (50.0, 55, 47)                                                                 # the bridge (the sensible chair): its first four lines low, B2-G3
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The designed lines: the hook ('figure': chorus 1's lines 1 and 4, copied in choruses 2 and 3) and the outro's last line ('chant')."""
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
    fig = all(rel((s_, 0)) == sp(HOOK) and rel((s_, 3)) == sp(HOOK) for s_ in ("Chorus 1", "Chorus 2", "Chorus 3"))
    hook_lines = {f"{s_}:{j_}" for s_ in ("Chorus 1", "Chorus 2", "Chorus 3") for j_ in (0, 3)} | {"Tag:4"}
    stop = max(n["p"] for n in notes) == 62 and all(n["line"] in hook_lines for n in notes if n["p"] >= 62)
    if not (fig and stop): f[g1] = dict(figure=fig, top=stop)
    tag = rel(("Tag", 4)) == sp(HOOK_T)
    if not tag: f[g2] = dict(tag=tag)
    return f
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hook aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(8) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in (1, 2, 4, 5, 6, 7) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[2]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''')
P("N = _N; SEED = 20261113 + 455", "N = _N; SEED = 20261113 + 456")
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p65.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p66.py {N} {MODE}"''')
P('''open(f"/home/claude/p66/runl7/melody_l7_p65_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p66/runl7/melody_l7_p66_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
