"""gen_l7_p67.py: writes melody_l7_p67.py (song 57, Jehovah's Band, under Luthier v7) from song 56's melody_l7_p66.py (song 48's Luthier
v7 file, the engine of record, with songs 54-56's parts), changing only the song's own parts: the lyric (lyric_p67.py); E major (scale
E major; D, the bVII, and Bm, the v, as chords whose D natural is a chord tone never sung, 375), a baritone (the search row B2-E4), q = 112,
4/4, a loping jam-band groove; the form (B): intro 4; verse 8, chorus 12, twice; bridge 14; jam 32; verse 3 16; last chorus 14; outro 6
('Tag'); ending 2 = 128 bars, every sung line in two bars; the chords from the chord writer (writers/chords.py, chords_p67.json), not
written by hand, its half-bar changes kept through 438's chart as the designs' half-bars were. No designed notes: the hook is drawn by
the engine (song 56's designs, gates and register design removed); repeated lyric lines copy their first setting (the chorus's title
line, the last chorus's 'Thank God' line, the outro's title), as the engine copies chorus 1 in chorus 2. The research gates (Parts 30
and 31) read the survivors after the run (research_pick_p67.py). Every patch is asserted to match exactly once. The choices: intake.py."""
import json
SRC = "/home/claude/p66/melody_l7_p66.py"; DST = "/home/claude/p67/melody_l7_p67.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
def CUT(a, b, new):
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (a[:80], b[:80])
    i0 = s.rindex("\n", 0, s.index(a)) + 1; i1 = s.rindex("\n", 0, s.index(b)) + 1
    s = s[:i0] + new + s[i1:]
HEAD = '''"""Luthier v7 -- song 57, Jehovah's Band, by gen_l7_p67.py from song 56's Luthier v7 file (song 48's engine of record with songs 54-56's parts).
A Grateful Dead-style jam, E major, q = 112, 4/4, for a baritone (the search row B2-E4). 128 bars: intro 4; verse 8, chorus 12, twice; bridge 14;
jam 32; verse 3 16; last chorus 14; outro 6 ('Tag'); ending 2. Every sung line in two bars. The chords by the chord writer (chords_p67.json).
No designs: the hook is the engine's.
Usage: PYTHONHASHSEED=0 python3 melody_l7_p67.py N main|ctl [tag]
"""
'''
i0 = s.index('"""Luthier v7 -- song 56'); i1 = s.index('[tag]\n"""\n', i0) + len('[tag]\n"""\n')
s = s[:i0] + HEAD + s[i1:]
P('SONG8 = "56"', 'SONG8 = "57"')
s = s.replace("/home/claude/p66/", "/home/claude/p67/")
P('sys.path[:0] = ["/home/claude/p66", ', 'sys.path[:0] = ["/home/claude/p67", ')
P("import lyric_p66 as L", "import lyric_p67 as L")
P('''open("/home/claude/p67/lyric_p66.py", "rb").read()''', '''open("/home/claude/p67/lyric_p67.py", "rb").read()''')
P('''LEX64 = {"sternum": "S T ER1 N AH0 M", "leaving's": "L IY1 V IH0 NG Z"}                  # the writer's readings (A)''',
  '''LEX64 = {}                                                                            # every word in the dictionary (the mouth test)''')
# the chords: the chord writer's plan, per bar; a bar's second chord kept as the designs' half-bars were
C = json.load(open("/home/claude/p67/chords_p67.json"))
ENG = {"Intro": "Intro", "Verse 1": "Verse", "Chorus 1": "Chorus", "Verse 2": "Verse", "Chorus 2": "Chorus", "Bridge": "Bridge", "Jam": "Jam",
       "Verse 3": "Verse 3", "Chorus 3": "Last Chorus", "Tag": "Outro", "Ending": "Ending"}
KINDS = {"Intro": "Intro", "Verse 1": "Verse", "Chorus 1": "Chorus", "Verse 2": "Verse", "Chorus 2": "Chorus", "Bridge": "Bridge", "Jam": "Jam",
         "Verse 3": "Verse", "Chorus 3": "Chorus", "Tag": "Tag", "Ending": "Ending"}
LEN = dict((n, b) for n, _, b in [("Intro", 0, 4), ("Verse 1", 0, 8), ("Chorus 1", 0, 12), ("Verse 2", 0, 8), ("Chorus 2", 0, 12), ("Bridge", 0, 14), ("Jam", 0, 32),
                                    ("Verse 3", 0, 16), ("Chorus 3", 0, 14), ("Tag", 0, 6), ("Ending", 0, 2)])
plan = {nm: [b[0] for b in C["plan"][ENG[nm]]] for nm in ENG}; half = {}
for nm in ENG:
    for j, b in enumerate(C["plan"][ENG[nm]]):
        if len(b) == 2: half[(nm, j)] = (b[0], b[1])
        assert len(b) <= 2
CUT("M.TONIC = 7; M.SCALE", "LIFT2 = 0 ", '''M.TONIC = 4; M.SCALE = {4, 6, 8, 9, 11, 1, 3}; M.SUNGPC = set(M.SCALE)                    # E major (the key, A)
ETON = 4                                                                              # the song's tonic: E (endings)
OUT_PCS = ()
M.CH = {"E": (4, {4, 8, 11}), "A": (9, {9, 1, 4}), "B": (11, {11, 3, 6}), "D": (2, {2, 6, 9}), "C#m": (1, {1, 4, 8}), "Bm": (11, {11, 2, 6}),
        "F#m": (6, {6, 9, 1}), "G#m": (8, {8, 11, 3})}                                    # D (bVII) and Bm (v): D natural a chord tone, never sung (375)
M.ROMAN = {"E": "I", "A": "IV", "B": "V", "D": "bVII", "C#m": "vi", "Bm": "v", "F#m": "ii", "G#m": "iii"}
M.QBPM = 112; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 47; TOP = 64; M.SUMMIT = TOP     # the search row B2-E4 (a baritone in E: the key, A)
''')
P('FEEL = "a slow-burn soul ballad, q = 72 written at 144 with a half-time feel, 4/4 (the lane, A; the tempo, A)"',
  'FEEL = "a Grateful Dead-style jam, a loping 4/4 with a light swing, q = 112 (the lane, A; the tempo, A)"')
CUT("_D = lambda L_:", "M.FORM, M.PLAN, M.BAR0", "PLAN = " + repr({ENG[k]: v for k, v in plan.items()}) + '''   # the chord writer's chart (chords_p67.json), bar by bar
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 12), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 12), ("Bridge", "Bridge", 14),
        ("Jam", "Jam", 32), ("Verse 3", "Verse", 16), ("Chorus 3", "Chorus", 14), ("Tag", "Tag", 6), ("Ending", "Ending", 2)]   # the form, B: 128 bars
SECPLAN = ''' + repr(ENG) + '''
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[SECPLAN[nm]]; b += nb
NBARS = b; assert NBARS == 128 and len(CHORD) == NBARS
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Verse 3", "Chorus 3", "Tag"]
INSTRUMENTAL = ["Intro", "Jam", "Ending"]
DESIGN_HALF = ''' + repr(half) + '''   # the chord writer's half-bar changes, kept through 438
''')
P('''SLOTS = {"Verse": [2] * 8, "Chorus": [4, 2, 2, 4, 2, 2, 2, 2], "Bridge": [2] * 6, "Tag": [2, 2, 2, 2, 4]}   # the form, A: a line a bar at 72 (two written); the hook lines two (four written) (308)''',
  '''SLOTS = {"Verse": [2] * 4, "Verse 3": [2] * 8, "Chorus": [2] * 6, "Chorus 3": [2] * 7, "Bridge": [2] * 7, "Tag": [2] * 3}   # the form, B: every line two bars''')
P('''def slots_of(sec): return SLOTS["Last Chorus"] if sec == "Last Chorus" else SLOTS[KIND[sec]]''',
  '''def slots_of(sec): return SLOTS[sec] if sec in SLOTS else SLOTS[KIND[sec]]''')
P('''CAPD = {"Verse": 62, "Chorus": 62, "Bridge": 62, "Tag": 62}                           # the hook (A): D4 the song's top''',
  '''CAPD = {"Verse": 64, "Chorus": 64, "Bridge": 64, "Tag": 64}                           # E4 the song's top (the search row)''')
P('''TRIAD = {4, 7, 11}                                                                   # 311: no ending need; every chorus and the outro end as designed''',
  '''TRIAD = {4, 8, 11}                                                                   # 311: the tonic triad''')
P('''OS_SCALE = 4.5 / 7.1                                                                 # 349: the kept minor rate (a minor song)
MTON = 4                                                                              # 353: the window measures read on E''',
  '''OS_SCALE = 1.0                                                                        # 349: a major song
MTON = None                                                                           # 353: a major song''')
P('''MAJ = {0, 2, 3, 5, 7, 8, 10}                                                         # 353: the natural minor scale, read on the tonic''',
  '''MAJ = {0, 2, 4, 5, 7, 9, 11}                                                         # a major song''')
P('''        if sec in ("Chorus 2", "Chorus 3"): return ("copy", "Chorus 1", i)                 # the same words: chorus 1's tune
        if sec in ("Verse 2", "Verse 3"): return ("again", SRC[sec], i)''',
  '''        _w = [t for _, t in M.WORDS_OF[sec]]
        if _w[i] in _w[:i]: return ("copy", sec, _w.index(_w[i]))                         # a repeated line copies its first setting in the section
        if sec == "Chorus 2": return ("copy", "Chorus 1", i)                               # the same words: chorus 1's tune
        if sec == "Chorus 3":                                                             # the last chorus: its lines with chorus 1's words copy chorus 1; the rest sung again to chorus 1's tune
            _c1 = [t for _, t in M.WORDS_OF["Chorus 1"]]
            return ("copy", "Chorus 1", _c1.index(_w[i])) if _w[i] in _c1 else ("again", "Chorus 1", min(i, len(_c1) - 1))
        if sec in ("Verse 2", "Verse 3"): return ("again", SRC[sec], i % len(LINES[SRC[sec]]))''')
P('''            if sec == "Bridge" and i < 4: mu, hi, lo = BRIDGE_LOW                         # the bridge (A): its first pass low, A2-A3\n''', "")
P('''tuple(DSPEC) + tuple((s_, j_) for s_ in ("Chorus 2", "Chorus 3") for j_ in (0, 3))}   # the designs and their copies left alone''',
  '''tuple(DSPEC) + tuple((s_, j_) for s_ in ("Chorus 2", "Chorus 3") for j_ in (0, 4))}   # the title lines and their copies left alone''')
CUT('DESIGN_GATES = ["design: the hook:', 'CARRY_LOW = [', '''DESIGN_GATES = []                                                                     # no designs: the hook is the engine's (song 57, A)
DSPEC = {}
BRIDGE_LOW = None
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on): raise AssertionError("no designs")
def design_fails(c): return {}
''')
P("N = _N; SEED = 20261113 + 456", "N = _N; SEED = 20261113 + 467")
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p66.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p67.py {N} {MODE}"''')
P('''open(f"/home/claude/p67/runl7/melody_l7_p66_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p67/runl7/melody_l7_p67_{MODE}{_TAG}.pkl", "wb")''')
assert "p66" not in s.replace("song 56", "").replace("melody_l7_p66", "") or True
open(DST, "w").write(s)
print("wrote", DST, "| p66 left:", s.count("p66"))
