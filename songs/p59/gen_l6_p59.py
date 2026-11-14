"""gen_l6_p59.py (from gen_l4_p59.py, the source now melody_l6_p58.py: Luthier v6): writes melody_l6_p59.py (song 49, The World Is Asking, under Luthier v4) from songs/p58's melody_l4_p58.py (the engine of
record: every generic patch through Luthier v4's 680-683), with the song's own parts: the lyric (lyric_p59.py), G major for a baritone
(the search row A2-E4), q = 84 fingerpicked, the form (A): intro 4, verse 16, chorus 16, verse 16, chorus 16, bridge 12, last chorus 16,
outro 4 = 100 bars, every sung line in two bars; the hook (A), the bridge (A) and the chorus above the verse as designed. Every patch
replaces whole statements and is asserted to match exactly once. The song's choices: intake.py."""
SRC = "/home/claude/p58/melody_l6_p58.py"; DST = "/home/claude/p59/melody_l6_p59.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
HEAD = '''"""Luthier v6 -- song 49, The World Is Asking, by gen_l6_p59.py from song 48's Luthier v6 file (the engine of record). Indie folk, G major,
q = 84 fingerpicked, for a baritone (the search row A2-E4); 100 bars: intro 4, verse 16, chorus 16, verse 16, chorus 16, bridge 12, last
chorus 16, outro 4, every sung line in two bars (the form, A). Designs in force (317, pass rates printed): the hook (A): 'The world is
asking', three notes climbing to D4 on 'ask-', '-ing' held on D4, unresolved; chorus line 7 the same figure; the last chorus's 'Speak, I'm
listening' comes down to G3. The bridge (A): lines 1-4 low and close (B2-G3); a bar of silence before 'Here I am'; 'Speak, I'm listening'
held on D3, open. The chorus above the verse: the chorus's register centre four semitones or more over the verse's, its median (the hooks
aside) two or more. Usage: PYTHONHASHSEED=0 python3 melody_l6_p59.py N main|ctl [tag]
"""
'''
s = HEAD + s
P('SONG8 = "48"', 'SONG8 = "49"')
s = s.replace("/home/claude/p58/", "/home/claude/p59/")
P('sys.path[:0] = ["/home/claude/p58", "/home/claude/p45", ', 'sys.path[:0] = ["/home/claude/p59", "/home/claude/p45", ')
P("import lyric_p58 as L", "import lyric_p59 as L")
P('''open("/home/claude/p59/lyric_p58.py", "rb").read()''', '''open("/home/claude/p59/lyric_p59.py", "rb").read()''')
# ---- the frame: G major ----
P('''M.TONIC = 4; M.SCALE = {4, 6, 8, 9, 11, 1, 3}; M.SUNGPC = M.SCALE | {2}                 # E major (the key, A); D natural sung (the flat seventh)
ETON = 4                                                                              # the song's tonic: E (endings)
OUT_PCS = (2,)
M.CH = {"E": (4, {4, 8, 11}), "B": (11, {11, 3, 6}), "C#m": (1, {1, 4, 8}), "A": (9, {9, 1, 4}), "F#m": (6, {6, 9, 1}), "G#m": (8, {8, 11, 3}), "D": (2, {2, 6, 9})}
M.ROMAN = {"E": "I", "B": "V", "C#m": "vi", "A": "IV", "F#m": "ii", "G#m": "iii", "D": "bVII"}
M.QBPM = 92; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 50; TOP = 71; M.SUMMIT = TOP      # the search row D3-B4 (the voice, A: high tenor D3-C5; C#5 only in the bridge's design)''',
  '''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = M.SCALE | {5}                 # G major (the key, A); F natural sung (the flat seventh)
ETON = 7                                                                              # the song's tonic: G (endings)
OUT_PCS = (5,)
M.CH = {"G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "C": (0, {0, 4, 7}), "Am": (9, {9, 0, 4}), "Bm": (11, {11, 2, 6}), "F": (5, {5, 9, 0})}
M.ROMAN = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "Bm": "iii", "F": "bVII"}
M.QBPM = 84; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 64; M.SUMMIT = TOP      # the search row A2-E4 (the singer, A: baritone A2-E4)''')
P('FEEL = "symphonic prog, q = 92; the verses in sixteenths, the choruses open (the sound, A; the tempo, A)"', 'FEEL = "indie folk, q = 84, walking, fingerpicked 4/4 (the sound, A; the tempo, A)"')
i0 = s.index('PLAN = {"Overture": ["E", "B", "C#m", "A"]'); i1 = s.index('M.FORM, M.PLAN, M.BAR0')
s = s[:i0] + '''PLAN = {"Intro": ["G", "C", "Em", "D"],
        "Verse": ["G", "G", "C", "G", "Em", "C", "D", "D", "G", "G", "C", "G", "Em", "C", "D", "D"],
        "Chorus": ["C", "D", "Em", "C", "G", "D", "C", "G", "C", "D", "Em", "C", "C", "D", "Em", "D"],
        "Bridge": ["Em", "C", "G", "D", "Em", "C", "Am", "D", "Em", "Em", "Am", "D"],
        "Outro": ["C", "G", "D", "G"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 16), ("Chorus 1", "Chorus", 16), ("Verse 2", "Verse", 16), ("Chorus 2", "Chorus", 16),
        ("Bridge", "Bridge", 12), ("Last Chorus", "Chorus", 16), ("Outro", "Outro", 4)]   # the form, A
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 100 and len(CHORD) == NBARS
CHORD[BAR0["Last Chorus"] + 15] = "G"                                                  # the last chorus comes home: 'Speak, I'm listening' lands on G (the hook, A)
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus"]
INSTRUMENTAL = ["Intro", "Outro"]
''' + s[i1:]
P('''    for _s, _bars in (("Chorus 1", (6, 7)), ("Chorus 2", (6, 7)), ("Last Chorus", (6, 7)), ("Tag", (0, 1, 2, 3)), ("Bridge", (8, 9, 10, 11))):   # the designs' bars keep the plan's chords
        for _j in _bars: CHORD2[2 * (BAR0[_s] + _j)] = CHORD2[2 * (BAR0[_s] + _j) + 1] = PLAN[KIND[_s]][_j]''',
  '''    for _s, _bars in (("Chorus 1", (0, 1, 12, 13)), ("Chorus 2", (0, 1, 12, 13)), ("Last Chorus", (0, 1, 14, 15)), ("Bridge", (8, 9, 10, 11))):   # the designs' bars keep the plan's chords
        for _j in _bars: CHORD2[2 * (BAR0[_s] + _j)] = CHORD2[2 * (BAR0[_s] + _j) + 1] = CHORD0[BAR0[_s] + _j]''')
P('''SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 6, "Bridge": [2] * 6, "Tag": [2] * 2, "Last Chorus": [2] * 6}     # every line two bars (the form, A)''',
  '''SLOTS = {"Verse": [2] * 8, "Chorus": [2] * 8, "Bridge": [2] * 6, "Last Chorus": [2] * 8}     # every line two bars (the form, A)''')
P('''VERSE_PLANS = [("ABCDAB", 0.25), ("ABCDAE", 0.25), ("ABCCAB", 0.15), ("ABCCDE", 0.15), ("ABCDEF", 0.20)]''',
  '''VERSE_PLANS = [("ABCDABCE", 0.30), ("ABCDABCD", 0.20), ("ABCDEFGH", 0.20), ("ABCDEBCF", 0.15), ("ABACABAD", 0.15)]   # eight-line verses: the second half may sing the first's tunes''')
P('''TRIAD = {4, 8, 11}
ENDING_NEEDS.update(Chorus={ETON})                                                   # 311: the chorus's last line (the tag's, the song's last) ends on the tonic''',
  '''TRIAD = {7, 11, 2}                                                                   # 311: no ending need; the chorus ends open, the last chorus's landing is designed''')
P('''    if sec in ("Chorus 1", "Chorus 2", "Last Chorus"): return (p - ETON) % 12 == 0      # 'And the song was not my own' / 'And I believe the song': home''',
  '''    if sec in ("Chorus 1", "Chorus 2"): return (p - ETON) % 12 != 0                     # 'Will I let the question in': open, off the tonic (the hook, A)''')
# ---- how each line is made ----
P('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", 3) if i == 3 else ("return", "Chorus 1", i)   # the hook kept; the other lines' words changed
        if sec == "Tag": return ("copy", "Chorus 1", 3)                                    # the tag ends on the hook's figure (A)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 3: return ("figure", None, None)                    # the hook (A)
        if sec == "Bridge" and i in (4, 5): return ("chant", None, None)                  # the bridge's build (A): its last two lines
        if sec == "Bridge": return ("fresh", None, None)                                  # the bridge's first four lines drawn, a pair a step higher''',
  '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus":                                                           # the hook and the unchanged lines kept; 'And I won't call it the wind' and 'Here I am, here I am' return; the landing designed
            if i == 7: return ("figure", None, None)
            return ("return", "Chorus 1", i) if i in (5, 6) else ("copy", "Chorus 1", i)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i in (0, 6): return ("figure", None, None)               # the hook (A)
        if sec == "Bridge" and i in (4, 5): return ("chant", None, None)                  # the bridge (A): 'Here I am', 'Speak, I'm listening'
        if sec == "Bridge": return ("fresh", None, None)                                  # the bridge's first four lines drawn, low and close''')
P('''            mu, hi, lo = REGS[kind]; d_ = BSHIFT.get((sec, i), 0)                          # the bridge's build (A): the first pair low, the second a step higher
            if d_: mu, hi, lo = mu + d_, min(TOP, hi + d_), max(M.LO, lo + d_)
            if sec == "Bridge" and i in (2, 3) and ("Bridge", 0) in built and ("Bridge", 1) in built:   # the second pair over the first pair's middle
                m1_ = float(np.median([n_["p"] for j_ in (0, 1) for n_ in built[("Bridge", j_)]])); lo = max(lo, int(m1_) + 1); mu = max(mu, m1_ + 3); hi = min(TOP, max(hi, lo + 5))''',
  '''            mu, hi, lo = REGS[kind]
            if sec == "Bridge" and i < 4: mu, hi, lo = BRIDGE_LOW                         # the bridge (A): its first four lines low and close, B2-G3''')
P('''tuple((s_, 3) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus")) + (("Tag", 0), ("Tag", 1), ("Bridge", 4), ("Bridge", 5))}   # the designs and their copies left alone''',
  '''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2") for j_ in (0, 6)) + (("Last Chorus", 0), ("Last Chorus", 7), ("Bridge", 4), ("Bridge", 5))}   # the designs and their copies left alone''')
# ---- the designs ----
i0 = s.index('DESIGN_GATES = ["design: the hook:'); i1 = s.index('CARRY_LOW = [')
s = s[:i0] + '''DESIGN_GATES = ["design: the hook: 'The world is asking', three notes climbing to D4 on 'ask-', '-ing' held on D4; chorus line 7 the same figure; the last chorus's 'Speak, I'm listening' landing on G3",
                "design: the bridge: lines 1-4 low and close (B2-G3); a bar of silence before 'Here I am'; 'Speak, I'm listening' held on D3"]
def sstep(p, k):
    """k scale steps from p (down when k < 0)."""
    q = p
    for _ in range(abs(k)):
        q += -1 if k < 0 else 1
        while q % 12 not in M.SCALE: q += -1 if k < 0 else 1
    return q
HOOK = {0: [(0, 55, 6), (6, 57, 6), (12, 59, 6), (18, 60, 6), (24, 62, 12), (36, 62, 48)],   # 'But the world is ask-ing': G3 A3, then B3 C4 D4 climbing; '-ing' held on D4 (the fifth) over the D chord
        6: [(6, 57, 6), (12, 59, 6), (18, 60, 6), (24, 62, 12), (36, 62, 48)],                # 'The world is ask-ing': the same figure, its pickup 'the'
        7: [(0, 62, 12), (12, 60, 12), (24, 57, 12), (36, 54, 12), (48, 55, 48)]}            # 'Speak, I'm lis-ten-ing': D4 C4 A3 F#3, landing on G3 over G
LIFTL = {4: [(48, 52, 6), (54, 50, 6), (60, 52, 36)],                                      # a bar of silence, then 'Here I am': E3 D3 E3 over Em, 'am' held from beat 2
         5: [(0, 57, 12), (12, 55, 12), (24, 52, 12), (36, 52, 12), (48, 50, 48)]}           # 'Speak, I'm lis-ten-ing': A3 G3 E3 E3, '-ing' held on D3 over D, open
BRIDGE_LOW = (51.0, 55, 47)                                                                 # the bridge (A): centre, cap, floor for its first four lines (B2-G3)
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The hook ('figure': Chorus 1 lines 1 and 7; the last chorus's last line) and the bridge's last two lines ('chant'), as designed (the writer's choices A)."""
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
    w0 = [(t, p) for t, p, d in HOOK[0]]; w6 = [(t, p) for t, p, d in HOOK[6]]; w7 = [(t, p) for t, p, d in HOOK[7]]
    fig = all(rel(k) == w0 for k in (("Chorus 1", 0), ("Chorus 2", 0), ("Last Chorus", 0))) and all(rel(k) == w6 for k in (("Chorus 1", 6), ("Chorus 2", 6)))
    land = rel(("Last Chorus", 7)) == w7
    if not (fig and land): f[g1] = dict(figure=fig, landing=land)
    low_ = [n["p"] for j in range(4) for n in by.get(f"Bridge:{j}", [])]
    low = bool(low_) and min(low_) >= 47 and max(low_) <= 55
    chant = rel(("Bridge", 4)) == [(t, p) for t, p, d in LIFTL[4]] and rel(("Bridge", 5)) == [(t, p) for t, p, d in LIFTL[5]]
    sil = bool(by.get("Bridge:3")) and by["Bridge:3"][-1]["on"] < line_start("Bridge", 4) and all(not (line_start("Bridge", 4) <= n["on"] < line_start("Bridge", 4) + BAR) for n in notes)
    if not (low and chant and sil): f[g2] = dict(low=low, chant=chant, silence=sil)
    return f
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hooks aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(8) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in (1, 2, 3, 4, 5, 7) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[2]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''' + s[i1:]
P('''CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1",)]                                          # 329: the first chorus (the bridge's top is designed)''',
  '''CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1",)]                                          # 329: the first chorus''')
P('''    if min(ps) < M.LO or max(pu_) > TOP or max(ps) > 73: return ("range (the voice row)", (min(ps), max(ps))), None''',
  '''    if min(ps) < M.LO or max(ps) > TOP: return ("range (the voice row)", (min(ps), max(ps))), None''')
# ---- the run ----
P("N = _N; SEED = 20261113 + 448", "N = _N; SEED = 20261113 + 449")
P('''cmd=f"ZE_PART_L6={VL6} PYTHONHASHSEED=0 python3 melody_l6_p58.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l6_p59.py {N} {MODE}"''')
P('''open(f"/home/claude/p59/runl6/melody_l6_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p59/runl6/melody_l6_p59_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
