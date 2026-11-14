"""gen_l7_p61.py: writes melody_l7_p61.py (song 51, A Wire Pulled Tight, under Luthier v7) from song 50's melody_l7_p60.py (song 48's
Luthier v7 file, the engine of record, with song 50's parts), changing only the song's own parts: the lyric (lyric_p61.py), A major for a
baritone (the search row A2-E4), slow-build alternative rock written at double tempo with a half-time feel (q = 116 rising to 164, felt as
58 to 82; the engine's beat grid is 4/4 throughout, so the tempo plan touches nothing here), the form: intro 4; verse 16, pre-chorus 4, chorus
20 (three times); verse 16; bridge 16; approach 8; final chorus 22; tag 8 = 194 bars, verse lines in four bars (felt as two), the rest in two, the hook's line held;
the writer's chords (held as chosen); the hook (A), the bridge (A), the tag, and the chorus above the verse. Every patch is asserted to match
exactly once. The song's choices: intake.py."""
SRC = "/home/claude/p60/melody_l7_p60.py"; DST = "/home/claude/p61/melody_l7_p61.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
HEAD = '''"""Luthier v7 -- song 51, A Wire Pulled Tight, by gen_l7_p61.py from song 50's Luthier v7 file (song 48's engine of record with song 50's parts).
Slow-build alternative rock, A major, for a baritone (the search row A2-E4); written at double tempo with a half-time feel (q = 116 rising to
164, felt as 58 to 82: the tempo plan is the playing's, the beat grid 4/4); 194 bars: intro 4; verse 16, pre-chorus 4, chorus 20, three
times; verse 16; bridge 16; approach 8 (instrumental); final chorus 22; tag 8. Verse lines in four bars (felt as two), the rest in two;
the hook's line held.
Designs in force (317, pass rates printed): the hook (A): 'time is breaking through' lands on C#4 and holds in choruses 1-3 (their top);
only the final chorus climbs to E4, held over Asus4 to A, and E4 is sung nowhere else. The bridge (A): its first pass low (A2-A3); its
second pass presses to D4 on 'none of it was ever lost'. The tag: 'There's a chair in the waiting room' sung as verse 1 sang it; 'and the
weight inside it is a grace' settles home on A2. The chorus above the verse. The writer's chords held as chosen.
Usage: PYTHONHASHSEED=0 python3 melody_l7_p61.py N main|ctl [tag]
"""
'''
i0 = s.index('"""Luthier v7 -- song 50'); i1 = s.index('[tag]\n"""\n', i0) + len('[tag]\n"""\n')
s = s[:i0] + HEAD + s[i1:]
P('SONG8 = "50"', 'SONG8 = "51"')
s = s.replace("/home/claude/p60/", "/home/claude/p61/")
P('sys.path[:0] = ["/home/claude/p60", ', 'sys.path[:0] = ["/home/claude/p61", ')
P("import lyric_p60 as L", "import lyric_p61 as L")
P('''open("/home/claude/p61/lyric_p60.py", "rb").read()''', '''open("/home/claude/p61/lyric_p61.py", "rb").read()''')
# ---- the frame: A major, the writer's chords ----
P('''M.TONIC = 2; M.SCALE = {2, 4, 6, 7, 9, 11, 1}; M.SUNGPC = M.SCALE | {0}                 # D major (the key, A); C natural sung (the flat seventh)
ETON = 2                                                                              # the song's tonic: D (endings)
OUT_PCS = (0,)
M.CH = {"D": (2, {2, 6, 9}), "A": (9, {9, 1, 4}), "Bm": (11, {11, 2, 6}), "G": (7, {7, 11, 2}), "Em": (4, {4, 7, 11}), "F#m": (6, {6, 9, 1}), "C": (0, {0, 4, 7})}
M.ROMAN = {"D": "I", "A": "V", "Bm": "vi", "G": "IV", "Em": "ii", "F#m": "iii", "C": "bVII"}
M.QBPM = 88; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 62; M.SUMMIT = TOP      # the search row A2-D4: the hook's D4 is the song's top (the hook, A)''',
  '''M.TONIC = 9; M.SCALE = {9, 11, 1, 2, 4, 6, 8}; M.SUNGPC = set(M.SCALE)                  # A major (the key, A); the voice in the scale (the flat seventh in the chords only: G, the bridge and the final chorus)
ETON = 9                                                                              # the song's tonic: A (endings)
OUT_PCS = ()
M.CH = {"A": (9, {9, 1, 4}), "E": (4, {4, 8, 11}), "D": (2, {2, 6, 9}), "G": (7, {7, 11, 2}), "Bm": (11, {11, 2, 6}),
        "F#m7": (6, {6, 9, 1, 4}), "Dadd9": (2, {2, 6, 9, 4}), "Asus2": (9, {9, 11, 4}), "Bm7": (11, {11, 2, 6, 9}), "C#m7": (1, {1, 4, 8, 11}),
        "Dmaj7": (2, {2, 6, 9, 1}), "C#dim7": (1, {1, 4, 7, 10}), "Asus4": (9, {9, 2, 4}), "E/G#": (4, {4, 8, 11}), "A/C#": (9, {9, 1, 4}),
        "F#/A#": (6, {6, 10, 1})}                                                     # the writer's chords (A)
M.ROMAN = {"A": "I", "E": "V", "D": "IV", "G": "bVII", "Bm": "ii", "F#m7": "vi7", "Dadd9": "IVadd9", "Asus2": "Isus2", "Bm7": "ii7", "C#m7": "iii7",
           "Dmaj7": "IVmaj7", "C#dim7": "#i dim7", "Asus4": "Isus4", "E/G#": "V6", "A/C#": "I6", "F#/A#": "III6"}
M.QBPM = 136; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 64; M.SUMMIT = TOP     # the search row A2-E4 (the singer, A: baritone); q = 136 the written mean (116-164)''')
P('FEEL = "gentle acoustic folk, q = 88 swung, fingerpicked 4/4 (the sound, A; the swing, A; the tempo, C)"',
  'FEEL = "slow-build alternative rock, written q = 116 rising to 164 with a half-time feel (felt 58 to 82), 4/4 (the genre, A; the tempo plan, A; the length, A)"')
i0 = s.index('PLAN = {"Intro": ["D", "G", "D", "A"],'); i1 = s.index('M.FORM, M.PLAN, M.BAR0')
s = s[:i0] + '''V_ = ["F#m7", "F#m7", "Dadd9", "Dadd9", "Asus2", "Asus2", "E/G#", "E/G#"] * 2
C_ = ["D", "D", "A/C#", "A/C#", "Bm7", "Bm7", "E", "E", "F#m7", "F#m7", "D", "D", "Bm7", "Bm7", "E", "Dmaj7", "Dmaj7", "Dmaj7", "Dmaj7", "Dmaj7"]
SECCH = {"Intro": ["F#m7", "F#m7", "Dadd9", "Dadd9"], "Pre 1": ["Bm7", "C#m7", "Dmaj7", "E"], "Pre 2": ["Bm7", "C#m7", "Dmaj7", "E"],
         "Pre 3": ["Bm7", "C#m7", "Dmaj7", "C#dim7"],
         "Last Chorus": ["D", "D", "A/C#", "A/C#", "Bm7", "Bm7", "E", "E", "F#m7", "F#m7", "D", "D", "G", "G", "G", "Asus4", "Asus4", "A", "A", "A", "A", "A"],
         "Bridge": ["D", "D", "F#/A#", "F#/A#", "Bm", "Bm", "G", "G"] * 2, "Approach": ["G"] * 6 + ["Asus2"] * 2,
         "Tag": ["F#m7", "F#m7", "Dadd9", "Dadd9", "A", "A", "A", "A"]}
for _v in ("Verse 1", "Verse 2", "Verse 3", "Verse 4"): SECCH[_v] = list(V_)
for _c in ("Chorus 1", "Chorus 2", "Chorus 3"): SECCH[_c] = list(C_)
PLAN = {"Intro": SECCH["Intro"], "Verse": V_, "Pre": SECCH["Pre 1"], "Chorus": C_, "Bridge": SECCH["Bridge"], "Approach": SECCH["Approach"], "Tag": SECCH["Tag"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 16), ("Pre 1", "Pre", 4), ("Chorus 1", "Chorus", 20), ("Verse 2", "Verse", 16), ("Pre 2", "Pre", 4),
        ("Chorus 2", "Chorus", 20), ("Verse 3", "Verse", 16), ("Pre 3", "Pre", 4), ("Chorus 3", "Chorus", 20), ("Verse 4", "Verse", 16),
        ("Bridge", "Bridge", 16), ("Approach", "Approach", 8), ("Last Chorus", "Chorus", 22), ("Tag", "Tag", 8)]   # the length, A, then A: 194 bars
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; assert len(SECCH[nm]) == nb, nm; CHORD += SECCH[nm]; b += nb
NBARS = b; assert NBARS == 194 and len(CHORD) == NBARS
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Verse 3", "Pre 3", "Chorus 3", "Verse 4", "Bridge", "Last Chorus", "Tag"]
INSTRUMENTAL = ["Intro", "Approach"]
''' + s[i1:]
P('''PCN8 = {0: "C",''', '''BASS8.update({"E/G#": 8, "A/C#": 1, "F#/A#": 10})                                          # the writer's slash chords: their bass
PCN8 = {0: "C",''')
P('''    for _s, _bars in (("Chorus 1", (12, 13, 14, 15)), ("Chorus 2", (12, 13, 14, 15)), ("Last Chorus", (12, 13, 14, 15)), ("Bridge", (6, 7))):   # the designs' bars keep the plan's chords
        for _j in _bars: CHORD2[2 * (BAR0[_s] + _j)] = CHORD2[2 * (BAR0[_s] + _j) + 1] = CHORD0[BAR0[_s] + _j]''',
  '''    CHORD2 = [h_ for c_ in CHORD0 for h_ in (c_, c_)]                                       # the writer's chords (A: 'only if they're good and not boring'), held as chosen; 438's draw printed, not applied
    CHART438["held"] = "the writer's chords, as chosen"''')
P('''SLOTS = {"Verse": [2] * 8, "Chorus": [2] * 8, "Bridge": [2] * 4, "Last Chorus": [2] * 8}     # every line two bars (the form, C)''',
  '''SLOTS = {"Verse": [4] * 4, "Pre": [2] * 2, "Chorus": [2] * 7 + [6], "Bridge": [2] * 8, "Last Chorus": [2] * 7 + [8], "Tag": [2, 6]}   # verse lines four bars (felt as two), the rest two; the hook's and the tag's last lines held (the length, A, then A)''')
P('''    R = {k: widen_329(v, lo, hi) for k, v in R.items()}''',
  '''    R = {k: widen_329(v, lo, hi) for k, v in R.items()}
    R = {k: (min(mu_, CAPD.get(k, 99) - 2), min(cap_, CAPD.get(k, 99)), min(fl_, CAPD.get(k, 99) - 5)) for k, (mu_, cap_, fl_) in R.items()}   # the designs' tops: C#4 outside the bridge (D4) and the final chorus's E4''')
P('''WIN_MIN = 13 ''', '''CAPD = {"Verse": 61, "Pre": 61, "Chorus": 61, "Tag": 61, "Bridge": 62}                 # the hook (A) and the bridge (A): the tops before the final chorus
WIN_MIN = 13 ''')
P('''    xhi = max(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)''',
  '''    xhi = min(CAPD["Chorus"], max(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE))   # 329: the highest drawn note under the designs' tops (E4 and D4 designed)''')
# ---- plans, sources ----
P('''BRIDGE_PLANS = [("ABCABC", 0.25), ("ABCADE", 0.25), ("ABCDBE", 0.15), ("ABCDEF", 0.35)]''',
  '''BRIDGE_PLANS = [("ABCDABGH", 0.35), ("ABCDAEGH", 0.25), ("ABCDEFGH", 0.40)]                       # the bridge's two passes over D F#/A# Bm G (line 7 designed)''')
P('''PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Pre": ["Pre 1", "Pre 2"], "Bridge": ["Bridge"]}''',
  '''PAIRS = {"Verse": ["Verse 1", "Verse 2", "Verse 3", "Verse 4"], "Pre": ["Pre 1", "Pre 2", "Pre 3"], "Bridge": ["Bridge"]}''')
P('''SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1", "Post 2": "Post 1"}''',
  '''SRC = {"Verse 2": "Verse 1", "Verse 3": "Verse 1", "Verse 4": "Verse 1", "Pre 2": "Pre 1", "Pre 3": "Pre 1", "Chorus 2": "Chorus 1", "Chorus 3": "Chorus 1",
       "Last Chorus": "Chorus 1", "Post 2": "Post 1"}''')
# ---- endings ----
P('''TRIAD = {2, 6, 9}
ENDING_NEEDS.update(Chorus={ETON})                                                   # 311: the chorus's last line ends on the tonic (designed: 'I think He always will' lands home on D3)''',
  '''TRIAD = {9, 1, 4}                                                                    # 311: no ending need; every chorus and the tag end as designed''')
P('''    if sec in ("Chorus 1", "Chorus 2", "Last Chorus"): return (p - ETON) % 12 == 0      # 'I think He always will': home (the hook, A)''',
  '''    if KIND[sec] in ("Chorus", "Tag"): return True                                      # designed endings (the hook, A; the tag)''')
# ---- how each line is made ----
P('''        if sec in ("Chorus 2", "Last Chorus"): return ("copy", "Chorus 1", i)               # every chorus the same words: sung the same
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i in (6, 7): return ("figure", None, None)               # the hook (A): 'I think God likes the small things / I think He always will'
        if sec == "Bridge" and i == 3: return ("chant", None, None)                       # the bridge (A): 'and the holy showed up clear'
        if sec == "Bridge": return ("fresh", None, None)                                  # the bridge's first three lines drawn, low''',
  '''        if (sec, i) in DSPEC: return ("figure" if i == 7 else "chant", None, None)        # the designs: the hook (A), the bridge's D4 (A), the tag's last line
        if sec in ("Chorus 2", "Chorus 3", "Last Chorus"): return ("again", "Chorus 1", i) if i in (4, 5) else ("copy", "Chorus 1", i)   # felt / lived / carried: new words on chorus 1's tune
        if sec in ("Verse 2", "Verse 3", "Verse 4", "Pre 2", "Pre 3"): return ("again", SRC[sec], i)
        if sec == "Tag": return ("copy", "Verse 1", 0)                                    # the tag: the opening line as verse 1 sang it''')
P('''            if sec == "Bridge" and i < 3: mu, hi, lo = BRIDGE_LOW                         # the bridge (A): its first three lines low, A2-F#3''',
  '''            if sec == "Bridge" and i < 4: mu, hi, lo = BRIDGE_LOW                         # the bridge (A): its first pass low, A2-A3''')
P('''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus") for j_ in (6, 7)) + (("Bridge", 3),)}   # the designs and their copies left alone''',
  '''tuple(DSPEC) + (("Chorus 2", 7), ("Chorus 3", 7))}   # the designs and their copies left alone''')
# ---- the designs ----
i0 = s.index('DESIGN_GATES = ["design: the hook:'); i1 = s.index('CARRY_LOW = [')
s = s[:i0] + '''DESIGN_GATES = ["design: the hook: 'time is breaking through' landing on C#4, held, in choruses 1-3, their top; the final chorus climbing to E4 over Asus4 to A, E4 sung nowhere else",
                "design: the bridge: its first pass low (A2-A3); its second pass pressing to D4 on 'none of it was ever lost', nothing over D4 outside the final chorus's E4",
                "design: the tag: the opening line as verse 1 sang it; 'and the weight inside it is a grace' settling home on A2"]
HOOK = [(12, 56, 6), (18, 57, 6), (24, 59, 12), (36, 59, 12), (48, 61, 216)]        # 'time is break-ing through': G#3 A3 B3 B3 over E, 'through' on C#4 over Dmaj7, held four bars and a half
HOOKL = [(12, 59, 6), (18, 61, 6), (24, 62, 12), (36, 62, 12), (48, 64, 312)]       # the final chorus: B3 C#4 D4 D4 over G, 'through' on E4 over Asus4, held into A
LIFTD = [(12, 57, 6), (18, 59, 6), (24, 61, 12), (36, 59, 12), (48, 62, 18), (66, 61, 6), (72, 59, 18)]   # 'none of it was ev-er lost' over Bm: A3 B3 C#4 B3, D4 on 'ev-', C#4, 'lost' B3
TAGL = [(12, 52, 6), (18, 52, 6), (24, 54, 12), (36, 52, 6), (42, 50, 6), (48, 52, 12), (60, 50, 12), (72, 49, 24), (96, 45, 168)]   # 'and the weight in-side it is a grace': over Dadd9, 'grace' on A2 over A, held
DSPEC = {("Chorus 1", 7): HOOK, ("Last Chorus", 7): HOOKL, ("Bridge", 6): LIFTD, ("Tag", 1): TAGL}
BRIDGE_LOW = (52.0, 57, 45)                                                                 # the bridge (A): centre, cap, floor for its first pass (A2-A3)
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The designed lines: the hook ('figure': chorus 1's last line, copied in choruses 2 and 3; the final chorus's own), the bridge's D4 and the tag's last line ('chant')."""
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
    """317: the writer's designs, read on what is sung; outside 275, their pass rates printed."""
    notes = c["notes"]; f = {}; g1, g2, g3 = DESIGN_GATES[:3]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    rel = lambda k: [(n["on"] - line_start(*k), n["p"]) for n in by.get(f"{k[0]}:{k[1]}", [])]
    sp = lambda L_: [(t, p) for t, p, d in L_]
    fig = all(rel((s_, 7)) == sp(HOOK) for s_ in ("Chorus 1", "Chorus 2", "Chorus 3")) and rel(("Last Chorus", 7)) == sp(HOOKL)
    ctop = all(max([n["p"] for j in range(8) for n in by.get(f"{s_}:{j}", [])] or [99]) == 61 for s_ in ("Chorus 1", "Chorus 2", "Chorus 3"))
    e4 = [n for n in notes if n["p"] >= 64]; only = bool(e4) and all(n["line"] == "Last Chorus:7" for n in e4)
    if not (fig and ctop and only): f[g1] = dict(figure=fig, chorus_top=ctop, e4_only_final=only)
    low_ = [n["p"] for j in range(4) for n in by.get(f"Bridge:{j}", [])]
    low = bool(low_) and min(low_) >= 45 and max(low_) <= 57
    lift = rel(("Bridge", 6)) == sp(LIFTD)
    top62 = all(n["p"] <= 62 for n in notes if n["line"] != "Last Chorus:7")
    if not (low and lift and top62): f[g2] = dict(low=low, lift=lift, top=top62)
    t0 = [(n["on"] - line_start("Tag", 0), n["p"]) for n in by.get("Tag:0", [])]; v0 = [(n["on"] - line_start("Verse 1", 0), n["p"]) for n in by.get("Verse 1:0", [])]
    tag = bool(t0) and t0 == v0 and rel(("Tag", 1)) == sp(TAGL)
    if not tag: f[g3] = dict(tag=tag)
    return f
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hook aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(4) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in range(7) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[3]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''' + s[i1:]
# ---- the run ----
P("N = _N; SEED = 20261113 + 450", "N = _N; SEED = 20261113 + 451")
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p60.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p61.py {N} {MODE}"''')
P('''open(f"/home/claude/p61/runl7/melody_l7_p60_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p61/runl7/melody_l7_p61_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
