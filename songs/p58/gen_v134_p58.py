"""gen_v134_p58.py: writes melody_v134_p58.py (song 48, The Ratios Hold) from songs/p57's melody_v134_p57.py (the engine of record at
v134: every generic patch through 566 and 569's reading), with the song's own parts: the lyric (lyric_p58.py), E major for a high tenor
(D3-B4 drawn; the bridge's designed C#5), q = 92, the suite's form (174 bars; the instrumentals carry chords only), every sung line in two
bars (the form, A), the hook and the bridge's build as designed (A, A). Every patch replaces whole statements and is asserted to match
exactly once. The song's choices: intake.py."""
SRC = "/home/claude/p57/melody_v134_p57.py"; DST = "/home/claude/p58/melody_v134_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
HEAD = '''"""ZenEng v134 (Module 27.78) -- song 48, The Ratios Hold, by gen_v134_p58.py from song 47's v134 file (the engine of record). Symphonic
prog in five movements, E major, q = 92, for a high tenor (the search row D3-B4; the bridge's designed C#5); 174 bars, every sung line in
two bars (the form, A: 550 flags both verses and the bridge, shown to the writer). The instrumentals (Overture 24, Study 48, the Window
Closes 10, Coda 24) carry chords only; the record gives them their meters. Designs in force (317, pass rates printed): the hook (A):
'The ratios hold', three notes stepping up to B4 on 'hold', held two beats, a beat of silence before 'Something was singing'; the tag ends
on the same figure. The bridge's build (A): lines 1-2 low, lines 3-4 a step higher; 'Whoever can hear' climbing, 'The instrument is
ready' landing on C#5, held. The chorus above the verse (B, after the first run): the chorus's register centre four semitones or more
over the verse's, its median (the hook aside) two or more. Usage: PYTHONHASHSEED=0 python3 melody_v134_p58.py N main|ctl [tag]
"""
'''
s = HEAD + s
P('SONG8 = "47"', 'SONG8 = "48"')
P('sys.path[:0] = ["/home/claude/p57", "/home/claude/p45", ', 'sys.path[:0] = ["/home/claude/p58", "/home/claude/p45", ')
P("import lyric_p57 as L", "import lyric_p58 as L")
s = s.replace("/home/claude/p57/tables/", "/home/claude/p58/tables/")
# ---- the frame: E major ----
P('''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = M.SCALE | {5}                 # G major (the key, Q A); F natural sung (the flat seventh)
ETON = 7                                                                              # the song's tonic: G (endings)
OUT_PCS = (5,)
M.CH = {"G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "C": (0, {0, 4, 7}), "Am": (9, {9, 0, 4}), "Bm": (11, {11, 2, 6})}
M.ROMAN = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "Bm": "iii"}
M.QBPM = 84; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 67; M.SUMMIT = TOP      # the search row C3-G4 (Q5 A: tenor C3-A4; A4 only in the lifted bridge)
LIFT2 = 2                                                                              # the second bridge's first seven lines, a whole step up in the record''',
  '''M.TONIC = 4; M.SCALE = {4, 6, 8, 9, 11, 1, 3}; M.SUNGPC = M.SCALE | {2}                 # E major (the key, A); D natural sung (the flat seventh)
ETON = 4                                                                              # the song's tonic: E (endings)
OUT_PCS = (2,)
M.CH = {"E": (4, {4, 8, 11}), "B": (11, {11, 3, 6}), "C#m": (1, {1, 4, 8}), "A": (9, {9, 1, 4}), "F#m": (6, {6, 9, 1}), "G#m": (8, {8, 11, 3}), "D": (2, {2, 6, 9})}
M.ROMAN = {"E": "I", "B": "V", "C#m": "vi", "A": "IV", "F#m": "ii", "G#m": "iii", "D": "bVII"}
M.QBPM = 92; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 50; TOP = 71; M.SUMMIT = TOP      # the search row D3-B4 (the voice, A: high tenor D3-C5; C#5 only in the bridge's design)
LIFT2 = 0                                                                              # no lift''')
P('FEEL = "acoustic-driven modern CCM, q = 84, sixteenth-note strum (Q4 B, Q6 A)"', 'FEEL = "symphonic prog, q = 92; the verses in sixteenths, the choruses open (the sound, A; the tempo, A)"')
i0 = s.index('PLAN = {"Intro": ["G", "D", "Em", "C"]'); i1 = s.index('M.FORM, M.PLAN, M.BAR0')
s = s[:i0] + '''PLAN = {"Overture": ["E", "B", "C#m", "A"] * 4 + ["E", "D", "A", "B"] * 2,
        "Verse": ["E", "B", "C#m", "A", "E", "B", "A", "B"],
        "Chorus": ["A", "B", "C#m", "A", "F#m", "B", "A", "E", "C#m", "A", "B", "E"],
        "Study": ["E", "B", "C#m", "A"] * 4 + ["F#m", "D", "A", "E"] * 2 + ["C#m", "A", "E", "B"] * 2 + ["A", "E", "F#m", "B"] * 2 + ["E", "D", "A", "B"] * 2,
        "Window": ["C#m", "A", "E", "B", "C#m", "A", "B", "B", "B", "B"],
        "Bridge": ["C#m", "A", "E", "B", "C#m", "A", "F#m", "B", "C#m", "B", "A", "F#m"],
        "Tag": ["A", "E", "A", "E"],
        "Coda": ["E", "B", "C#m", "A"] * 4 + ["E", "D", "A", "E"] * 2}
FORM = [("Overture", "Overture", 24), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 12), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 12),
        ("Study", "Study", 48), ("Window", "Window", 10), ("Bridge", "Bridge", 12), ("Last Chorus", "Chorus", 12), ("Tag", "Tag", 4), ("Coda", "Coda", 24)]   # the form, A
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 174 and len(CHORD) == NBARS
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus", "Tag"]
INSTRUMENTAL = ["Overture", "Study", "Window", "Coda"]
''' + s[i1:]
P('''    _b1, _b2 = BAR0["Bridge"], BAR0["Bridge 2"]                                             # the second bridge's first ten bars keep the first's chart (its copies)
    CHORD2[2 * _b2:2 * (_b2 + 10)] = CHORD2[2 * _b1:2 * (_b1 + 10)]''',
  '''    for _s, _bars in (("Chorus 1", (6, 7)), ("Chorus 2", (6, 7)), ("Last Chorus", (6, 7)), ("Tag", (0, 1, 2, 3)), ("Bridge", (8, 9, 10, 11))):   # the designs' bars keep the plan's chords
        for _j in _bars: CHORD2[2 * (BAR0[_s] + _j)] = CHORD2[2 * (BAR0[_s] + _j) + 1] = PLAN[KIND[_s]][_j]''')
P('''SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 6, "Bridge": [2] * 6, "Bridge2": [2] * 8, "Tag": [2] * 2, "Last Chorus": [2] * 6}     # every line two bars (the form, A)''',
  '''SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 6, "Bridge": [2] * 6, "Tag": [2] * 2, "Last Chorus": [2] * 6}     # every line two bars (the form, A)''')
P('''    R["Bridge2"] = R["Bridge"]; R["Tag"] = R["Chorus"]                                  # the second bridge in the first's register; the tag in the chorus's''',
  '''    R["Tag"] = R["Chorus"]                                                              # the tag in the chorus's register''')
P('''TRIAD = {9, 0, 4}''', '''TRIAD = {4, 8, 11}''')
P('''    if sec in ("Chorus 1", "Chorus 2", "Last Chorus", "Tag"): return (p - ETON) % 12 == 0  # 'Cause the singer doesn't stop': home''',
  '''    if sec in ("Chorus 1", "Chorus 2", "Last Chorus"): return (p - ETON) % 12 == 0      # 'And the song was not my own' / 'And I believe the song': home''')
# ---- how each line is made ----
P('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("return", "Chorus 1", i) if i in (3, 5) else ("copy", "Chorus 1", i)   # 'Even the high part I sang flat'; 'And it will still be me'
        if sec == "Tag": return ("copy", "Chorus 1", 0 if i == 0 else 5)
        if sec == "Bridge 2": return ("copy", "Bridge", i) if i < 5 else ("chant", None, None) if i in (5, 6) else ("fresh", None, None)   # the bridge's build (A)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i in (0, 1): return ("figure", None, None)               # the hook (A)
        if kind in ("Chorus", "Bridge2", "Tag"): return ("fresh", None, None)''',
  '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", 3) if i == 3 else ("return", "Chorus 1", i)   # the hook kept; the other lines' words changed
        if sec == "Tag": return ("copy", "Chorus 1", 3)                                    # the tag ends on the hook's figure (A)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 3: return ("figure", None, None)                    # the hook (A)
        if sec == "Bridge" and i in (4, 5): return ("chant", None, None)                  # the bridge's build (A): its last two lines
        if sec == "Bridge": return ("fresh", None, None)                                  # the bridge's first four lines drawn, a pair a step higher
        if kind in ("Chorus", "Tag"): return ("fresh", None, None)''')
P('''            if (sec, i) == ("Chorus 1", 5): tmin = max(tmin, 6)                            # the tag sings this line straight after the hook's 'stop': no pickup''',
  '''            mu, hi, lo = REGS[kind]; d_ = BSHIFT.get((sec, i), 0)                          # the bridge's build (A): the first pair low, the second a step higher
            if d_: mu, hi, lo = mu + d_, min(TOP, hi + d_), max(M.LO, lo + d_)
            if sec == "Bridge" and i in (2, 3) and ("Bridge", 0) in built and ("Bridge", 1) in built:   # the second pair over the first pair's middle
                m1_ = float(np.median([n_["p"] for j_ in (0, 1) for n_ in built[("Bridge", j_)]])); lo = max(lo, int(m1_) + 1); mu = max(mu, m1_ + 3); hi = min(TOP, max(hi, lo + 5))''')
P('''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus") for j_ in (0, 1)) + (("Tag", 0), ("Bridge 2", 5), ("Bridge 2", 6))}   # the designs and their copies left alone''',
  '''tuple((s_, 3) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus")) + (("Tag", 0), ("Tag", 1), ("Bridge", 4), ("Bridge", 5))}   # the designs and their copies left alone''')
# ---- the designs ----
i0 = s.index('DESIGN_GATES = ["design: the hook:'); i1 = s.index('CARRY_LOW = [')
s = s[:i0] + '''DESIGN_GATES = ["design: the hook: 'The ratios hold', three notes stepping up to B4 on 'hold', held two beats, a beat of silence after; the tag the same figure",
                "design: the bridge's build: the second pair a step over the first; 'Whoever can hear' climbing, 'The instrument is ready' landing on C#5, held"]
def sstep(p, k):
    """k scale steps from p (down when k < 0)."""
    q = p
    for _ in range(abs(k)):
        q += -1 if k < 0 else 1
        while q % 12 not in M.SCALE: q += -1 if k < 0 else 1
    return q
HOOK = {3: [(30, 59, 6), (36, 64, 6), (42, 68, 3), (45, 69, 3), (48, 71, 24)]}           # 'The ra-ti-os hold': B3 E4, then G#4 A4 B4 stepping up, 'hold' two beats
LIFTL = {4: [(6, 64, 6), (12, 68, 12), (24, 68, 6), (30, 69, 6), (36, 71, 36)],             # 'Who-ev-er can hear': E4 G#4 G#4 A4 B4, climbing, 'hear' held
         5: [(6, 68, 6), (12, 69, 9), (21, 69, 3), (24, 71, 6), (30, 71, 6), (36, 73, 24), (60, 71, None)]}   # 'The in-stru-ment is rea-dy': up to C#5 on 'rea', held two beats; 'dy' held into the last chorus
BSHIFT = {("Bridge", 0): -3, ("Bridge", 1): -3, ("Bridge", 2): 3, ("Bridge", 3): 3}        # the bridge's build (A): the pairs' centres, in semitones
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The hook ('figure', Chorus 1 line 4) and the bridge's last two lines ('chant'), as designed (the writer's choices A)."""
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
    want = [(t, p) for t, p, d in HOOK[3]]
    fig = all(rel(k) == want for k in (("Chorus 1", 3), ("Chorus 2", 3), ("Last Chorus", 3), ("Tag", 0), ("Tag", 1)))
    sil = all(by.get(f"{s_}:4") and by[f"{s_}:4"][0]["on"] - (by[f"{s_}:3"][-1]["on"] + by[f"{s_}:3"][-1].get("dur", 0)) >= 12 for s_ in ("Chorus 1", "Chorus 2", "Last Chorus"))
    if not (fig and sil): f[g1] = dict(figure=fig, silence=sil)
    lo_ = [n["p"] for j in (0, 1) for n in by.get(f"Bridge:{j}", [])]; hi_ = [n["p"] for j in (2, 3) for n in by.get(f"Bridge:{j}", [])]
    step = bool(lo_ and hi_) and float(np.median(hi_)) >= float(np.median(lo_)) + 1
    chant = rel(("Bridge", 4)) == [(t, p) for t, p, d in LIFTL[4]] and rel(("Bridge", 5)) == [(t, p) for t, p, d in LIFTL[5]]
    top = max([n["p"] for j in range(4) for n in by.get(f"Bridge:{j}", [])] or [0]) < 73   # the drawn lines stay under the held C#5
    if not (step and chant and top): f[g2] = dict(step=step, chant=chant, under_the_top=top)
    return f
def design_reg(R_, info):
    """325: the bridge's drawn register under the designed C#5."""
    return R_["Bridge"][1] <= 72
DESIGN_REG.append(("the bridge's register under C#5 (the build, A)", design_reg))
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse, B)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hook aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(4) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in (0, 1, 2, 4, 5) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[2]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''' + s[i1:]
P('''CARRY_LOW = [s_ for s_ in SUNG if KIND[s_] in ("Verse", "Bridge") and s_ in ("Verse 1", "Bridge")]     # 329: the first verse or the bridge''',
  '''CARRY_LOW = [s_ for s_ in SUNG if s_ in ("Verse 1",)]                                            # 329: the first verse (the bridge's pairs rise, A)''')
P('''CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1",)]                                          # 329: the first chorus (the bridge stays under the lift)''',
  '''CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1",)]                                          # 329: the first chorus (the bridge's top is designed)''')
P('''    if min(ps) < M.LO or max(ps) > TOP: return ("range (the voice row)", (min(ps), max(ps))), None''',
  '''    pu_ = [n["p"] for n in notes if not n.get("pin")]                                      # the designed C#5 (the bridge's build, A) above the drawn row
    if min(ps) < M.LO or max(pu_) > TOP or max(ps) > 73: return ("range (the voice row)", (min(ps), max(ps))), None''')
# ---- the run ----
P("N = _N; SEED = 20261113 + 447", "N = _N; SEED = 20261113 + 448")
P('''open("/home/claude/p57/lyric_p57.py", "rb").read()''', '''open("/home/claude/p58/lyric_p58.py", "rb").read()''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v134_p57.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_v134_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p57/run134/melody_v134_p57_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/run/melody_v134_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
