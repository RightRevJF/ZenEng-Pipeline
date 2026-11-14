"""gen_l7_p60.py: writes melody_l7_p60.py (song 50, Late Afternoon, under Luthier v7) from song 49's melody_l7_p59.py (song 48's Luthier v7
file, the engine of record, with song 49's parts), changing only the song's own parts: the lyric (lyric_p60.py), D major for a baritone (the
search row A2-D4), q = 88 swung (the swing in the playing only), the form (C): intro 4, verse 16, chorus 16, verse 16, chorus 16, bridge 8,
last chorus 16, outro 4 = 96 bars, every sung line in two bars; the hook (A), the bridge (A) and the chorus above the verse. Every patch is
asserted to match exactly once. The song's choices: intake.py."""
SRC = "/home/claude/p59/melody_l7_p59.py"; DST = "/home/claude/p60/melody_l7_p60.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
HEAD = '''"""Luthier v7 -- song 50, Late Afternoon, by gen_l7_p60.py from song 49's Luthier v7 file (song 48's engine of record with song 49's parts).
Gentle acoustic folk, D major, q = 88 swung (the swing in the playing only; the record straight), fingerpicked, for a baritone (the search row
A2-D4); 96 bars: intro 4, verse 16, chorus 16, verse 16, chorus 16, bridge 8, last chorus 16, outro 4, every sung line in two bars (the form,
C). Designs in force (317, pass rates printed): the hook (A): 'I think God likes the small things' climbs to the song's top note, D4, on
'small', held; 'I think He always will' steps down and lands home on D3; every chorus the same. The bridge (A): its first three lines low
(A2-F#3); a beat of silence before 'and the holy showed up clear', which rises to A3 and holds it, open, into the last chorus. The chorus
above the verse. Usage: PYTHONHASHSEED=0 python3 melody_l7_p60.py N main|ctl [tag]
"""
'''
i0 = s.index('"""Luthier v7 -- song 49'); i1 = s.index('[tag]\n"""\n', i0) + len('[tag]\n"""\n')
s = s[:i0] + HEAD + s[i1:]
P('SONG8 = "49"', 'SONG8 = "50"')
s = s.replace("/home/claude/p59/", "/home/claude/p60/")
P('sys.path[:0] = ["/home/claude/p59", "/home/claude/p45", ', 'sys.path[:0] = ["/home/claude/p60", "/home/claude/p45", ')
P("import lyric_p59 as L", "import lyric_p60 as L")
P('''open("/home/claude/p60/lyric_p59.py", "rb").read()''', '''open("/home/claude/p60/lyric_p60.py", "rb").read()''')
# ---- the frame: D major ----
P('''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = M.SCALE | {5}                 # G major (the key, A); F natural sung (the flat seventh)
ETON = 7                                                                              # the song's tonic: G (endings)
OUT_PCS = (5,)
M.CH = {"G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "C": (0, {0, 4, 7}), "Am": (9, {9, 0, 4}), "Bm": (11, {11, 2, 6}), "F": (5, {5, 9, 0})}
M.ROMAN = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "Bm": "iii", "F": "bVII"}
M.QBPM = 84; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 64; M.SUMMIT = TOP      # the search row A2-E4 (the singer, A: baritone A2-E4)''',
  '''M.TONIC = 2; M.SCALE = {2, 4, 6, 7, 9, 11, 1}; M.SUNGPC = M.SCALE | {0}                 # D major (the key, A); C natural sung (the flat seventh)
ETON = 2                                                                              # the song's tonic: D (endings)
OUT_PCS = (0,)
M.CH = {"D": (2, {2, 6, 9}), "A": (9, {9, 1, 4}), "Bm": (11, {11, 2, 6}), "G": (7, {7, 11, 2}), "Em": (4, {4, 7, 11}), "F#m": (6, {6, 9, 1}), "C": (0, {0, 4, 7})}
M.ROMAN = {"D": "I", "A": "V", "Bm": "vi", "G": "IV", "Em": "ii", "F#m": "iii", "C": "bVII"}
M.QBPM = 88; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 62; M.SUMMIT = TOP      # the search row A2-D4: the hook's D4 is the song's top (the hook, A)''')
P('FEEL = "indie folk, q = 84, walking, fingerpicked 4/4 (the sound, A; the tempo, A)"', 'FEEL = "gentle acoustic folk, q = 88 swung, fingerpicked 4/4 (the sound, A; the swing, A; the tempo, C)"')
i0 = s.index('PLAN = {"Intro": ["G", "C", "Em", "D"],'); i1 = s.index('M.FORM, M.PLAN, M.BAR0')
s = s[:i0] + '''PLAN = {"Intro": ["D", "G", "D", "A"],
        "Verse": ["D", "D", "G", "D", "Bm", "G", "A", "A", "D", "D", "G", "D", "Bm", "G", "A", "A"],
        "Chorus": ["D", "D", "A", "A", "G", "G", "D", "D", "Bm", "G", "A", "A", "G", "G", "A", "D"],
        "Bridge": ["Bm", "G", "D", "A", "Bm", "G", "A", "A"],
        "Outro": ["G", "D", "A", "D"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 16), ("Chorus 1", "Chorus", 16), ("Verse 2", "Verse", 16), ("Chorus 2", "Chorus", 16),
        ("Bridge", "Bridge", 8), ("Last Chorus", "Chorus", 16), ("Outro", "Outro", 4)]   # the form, C
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 96 and len(CHORD) == NBARS
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus"]
INSTRUMENTAL = ["Intro", "Outro"]
''' + s[i1:]
P('''    for _s, _bars in (("Chorus 1", (0, 1, 12, 13)), ("Chorus 2", (0, 1, 12, 13)), ("Last Chorus", (0, 1, 14, 15)), ("Bridge", (8, 9, 10, 11))):   # the designs' bars keep the plan's chords''',
  '''    for _s, _bars in (("Chorus 1", (12, 13, 14, 15)), ("Chorus 2", (12, 13, 14, 15)), ("Last Chorus", (12, 13, 14, 15)), ("Bridge", (6, 7))):   # the designs' bars keep the plan's chords''')
P('''SLOTS = {"Verse": [2] * 8, "Chorus": [2] * 8, "Bridge": [2] * 6, "Last Chorus": [2] * 8}     # every line two bars (the form, A)''',
  '''SLOTS = {"Verse": [2] * 8, "Chorus": [2] * 8, "Bridge": [2] * 4, "Last Chorus": [2] * 8}     # every line two bars (the form, C)''')
P('''TRIAD = {7, 11, 2}                                                                   # 311: no ending need; the chorus ends open, the last chorus's landing is designed''',
  '''TRIAD = {2, 6, 9}
ENDING_NEEDS.update(Chorus={ETON})                                                   # 311: the chorus's last line ends on the tonic (designed: 'I think He always will' lands home on D3)''')
P('''    if sec in ("Chorus 1", "Chorus 2"): return (p - ETON) % 12 != 0                     # 'Will I let the question in': open, off the tonic (the hook, A)''',
  '''    if sec in ("Chorus 1", "Chorus 2", "Last Chorus"): return (p - ETON) % 12 == 0      # 'I think He always will': home (the hook, A)''')
# ---- how each line is made ----
P('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus":                                                           # the hook and the unchanged lines kept; 'And I won't call it the wind' and 'Here I am, here I am' return; the landing designed
            if i == 7: return ("figure", None, None)
            return ("return", "Chorus 1", i) if i in (5, 6) else ("copy", "Chorus 1", i)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i in (0, 6): return ("figure", None, None)               # the hook (A)
        if sec == "Bridge" and i in (4, 5): return ("chant", None, None)                  # the bridge (A): 'Here I am', 'Speak, I'm listening'
        if sec == "Bridge": return ("fresh", None, None)                                  # the bridge's first four lines drawn, low and close''',
  '''        if sec in ("Chorus 2", "Last Chorus"): return ("copy", "Chorus 1", i)               # every chorus the same words: sung the same
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i in (6, 7): return ("figure", None, None)               # the hook (A): 'I think God likes the small things / I think He always will'
        if sec == "Bridge" and i == 3: return ("chant", None, None)                       # the bridge (A): 'and the holy showed up clear'
        if sec == "Bridge": return ("fresh", None, None)                                  # the bridge's first three lines drawn, low''')
P('''            if sec == "Bridge" and i < 4: mu, hi, lo = BRIDGE_LOW                         # the bridge (A): its first four lines low and close, B2-G3''',
  '''            if sec == "Bridge" and i < 3: mu, hi, lo = BRIDGE_LOW                         # the bridge (A): its first three lines low, A2-F#3''')
P('''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2") for j_ in (0, 6)) + (("Last Chorus", 0), ("Last Chorus", 7), ("Bridge", 4), ("Bridge", 5))}   # the designs and their copies left alone''',
  '''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus") for j_ in (6, 7)) + (("Bridge", 3),)}   # the designs and their copies left alone''')
# ---- the designs ----
i0 = s.index('DESIGN_GATES = ["design: the hook:'); i1 = s.index('CARRY_LOW = [')
s = s[:i0] + '''DESIGN_GATES = ["design: the hook: 'I think God likes the small things' climbing to D4 on 'small', held; 'I think He always will' stepping down to land home on D3; every chorus the same",
                "design: the bridge: lines 1-3 low (A2-F#3); a beat of silence before 'and the holy showed up clear', rising to A3, held"]
HOOK = {6: [(12, 55, 6), (18, 57, 6), (24, 59, 12), (36, 57, 6), (42, 59, 6), (48, 62, 24), (72, 59, 24)],   # 'I think God likes the small things': G3 A3 B3 A3 B3, 'small' on D4 (the fifth of G) on the downbeat, held; 'things' B3
        7: [(12, 57, 6), (18, 55, 6), (24, 54, 12), (36, 52, 6), (42, 49, 6), (48, 50, 48)]}          # 'I think He al-ways will': A3 G3 F#3 E3 C#3 over A, 'will' home on D3 over D, held
LIFTL = {3: [(12, 50, 6), (18, 52, 6), (24, 54, 12), (36, 55, 12), (48, 57, 12), (60, 55, 12), (72, 57, 24)]}   # a beat of silence, then 'and the ho-ly showed up clear': D3 E3 F#3 G3, A3 on 'showed', G3, 'clear' held on A3 over A, open
BRIDGE_LOW = (49.0, 54, 45)                                                                 # the bridge (A): centre, cap, floor for its first three lines (A2-F#3)
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The hook ('figure': Chorus 1 lines 7 and 8, copied in every chorus) and the bridge's last line ('chant'), as designed (the writer's choices A)."""
    sy = LINES[sec][i]; spec = HOOK[i] if h == "figure" else LIFTL[i]
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
    notes = c["notes"]; f = {}; g1, g2 = DESIGN_GATES[:2]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    rel = lambda k: [(n["on"] - line_start(*k), n["p"]) for n in by.get(f"{k[0]}:{k[1]}", [])]
    w6 = [(t, p) for t, p, d in HOOK[6]]; w7 = [(t, p) for t, p, d in HOOK[7]]
    fig = all(rel((s_, 6)) == w6 and rel((s_, 7)) == w7 for s_ in ("Chorus 1", "Chorus 2", "Last Chorus"))
    top = max(n["p"] for n in notes) == 62
    if not (fig and top): f[g1] = dict(figure=fig, top=top)
    low_ = [n["p"] for j in range(3) for n in by.get(f"Bridge:{j}", [])]
    low = bool(low_) and min(low_) >= 45 and max(low_) <= 54
    chant = rel(("Bridge", 3)) == [(t, p) for t, p, d in LIFTL[3]]
    L3 = line_start("Bridge", 3)
    sil = bool(by.get("Bridge:2")) and all(not (L3 <= n["on"] < L3 + BEAT) for n in notes)
    if not (low and chant and sil): f[g2] = dict(low=low, chant=chant, silence=sil)
    return f
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hook aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(8) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in range(6) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[2]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''' + s[i1:]
# ---- the run ----
P("N = _N; SEED = 20261113 + 449", "N = _N; SEED = 20261113 + 450")
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p59.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p60.py {N} {MODE}"''')
P('''open(f"/home/claude/p60/runl7/melody_l7_p59_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p60/runl7/melody_l7_p60_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
