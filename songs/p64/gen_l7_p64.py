"""gen_l7_p64.py: writes melody_l7_p64.py (song 54, The Man Mama Prayed I'd Be, under Luthier v7) from song 51's melody_l7_p61.py (song 48's
Luthier v7 file, the engine of record, with song 51's parts), changing only the song's own parts: the lyric (lyric_p64.py, with six lexicon
readings), G major for a baritone (the search row A2-D4; she sings chorus 4 and the tag's second line an octave up, in the record only),
q = 120, a mid-tempo country two-step, 4/4; the form (A): intro 4; verse 16, chorus 12, three times; turnaround 4; verse 16; chorus 12;
tag 4; ending 2 = 126 bars, every sung line in two bars; the chart drawn by 438 (the default path; song 51 held its writer's chords); the
hook (A), the tag, and the chorus above the verse. The song has no bridge: the readings that read one are guarded (finding 749.24).
Every patch is asserted to match exactly once. The song's choices: intake.py."""
SRC = "/home/claude/p61/melody_l7_p61.py"; DST = "/home/claude/p64/melody_l7_p64.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)
def CUT(a, b, new):
    """Replace from the line holding a (inclusive) to the line holding b (exclusive)."""
    global s
    assert s.count(a) == 1 and s.count(b) == 1, (a[:80], b[:80])
    i0 = s.rindex("\n", 0, s.index(a)) + 1; i1 = s.rindex("\n", 0, s.index(b)) + 1
    s = s[:i0] + new + s[i1:]
HEAD = '''"""Luthier v7 -- song 54, The Man Mama Prayed I'd Be, by gen_l7_p64.py from song 51's Luthier v7 file (song 48's engine of record with song
51's parts). A mid-tempo country story song (neotraditional two-step), G major, q = 120, for a baritone (the search row A2-D4); she sings
chorus 4 and the tag's second line an octave up (the record only). 126 bars: intro 4; verse 16, chorus 12, three times; turnaround 4;
verse 16; chorus 12; tag 4; ending 2; every sung line in two bars. Designs in force (317, pass rates printed): the hook (A): 'The man Mama
prayed he'd be' climbs G3 B3 to D4, the chorus's top, on 'Ma-', and in choruses 1-3 settles open on D3 over D, through F#3; in chorus 4
('The woman Daddy prayed I'd be') and the tag the F#3 resolves up to G3, home, over G. The chorus above the verse. No bridge.
Usage: PYTHONHASHSEED=0 python3 melody_l7_p64.py N main|ctl [tag]
"""
'''
i0 = s.index('"""Luthier v7 -- song 51'); i1 = s.index('[tag]\n"""\n', i0) + len('[tag]\n"""\n')
s = s[:i0] + HEAD + s[i1:]
P('SONG8 = "51"', 'SONG8 = "54"')
s = s.replace("/home/claude/p61/", "/home/claude/p64/")
P('sys.path[:0] = ["/home/claude/p61", ', 'sys.path[:0] = ["/home/claude/p64", ')
P("import lyric_p61 as L", "import lyric_p64 as L")
P('''open("/home/claude/p64/lyric_p61.py", "rb").read()''', '''open("/home/claude/p64/lyric_p64.py", "rb").read()''')
# ---- the lexicon (Protocol 0b v67: the writer's answer A) ----
P('''import lyricsearch; lyricsearch.OVERRIDE["pleather"] = ("P L EH1 DH ER0",)          # not in the pronouncing dictionary''',
  '''import lyricsearch
LEX64 = {"sleepin'": "S L IY1 P IH0 N", "mildewed": "M IH1 L D UW2 D", "'n'": "AH0 N", "rooster's": "R UW1 S T ER0 Z",
         "mornin'": "M AO1 R N IH0 N", "fixin'": "F IH1 K S IH0 N", "am": "EY2 EH1 M"}          # the writer's readings (A); 'a.m.' is read as 'am'
for _w, _p in LEX64.items(): lyricsearch.OVERRIDE[_w] = (_p,)
lyricsearch.FUNCTION.add("'n'")                                                      # Git 'n' Split: the 'n' unstressed (A)''')
P('''LINES = {s: [syl(t.replace('"', "")) for _, t in M.WORDS_OF[s]] for s in SUNG}''',
  '''LINES = {s: [syl(t.replace('"', "").replace("a.m.", "am")) for _, t in M.WORDS_OF[s]] for s in SUNG}''')
# ---- the frame: G major, q = 120 ----
CUT("M.TONIC = 9; M.SCALE", "LIFT2 = 0 ", '''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = set(M.SCALE)                   # G major (the key, A; Longing, A: Ionian, the leading tone sung)
ETON = 7                                                                              # the song's tonic: G (endings)
OUT_PCS = ()
M.CH = {"G": (7, {7, 11, 2}), "C": (0, {0, 4, 7}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "Am": (9, {9, 0, 4}), "Bm": (11, {11, 2, 6})}
M.ROMAN = {"G": "I", "C": "IV", "D": "V", "Em": "vi", "Am": "ii", "Bm": "iii"}
M.QBPM = 120; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; TOP = 62; M.SUMMIT = TOP     # the search row A2-D4: the hook's D4 is the song's top (the key, A; the hook, A)
''')
P('FEEL = "slow-build alternative rock, written q = 116 rising to 164 with a half-time feel (felt 58 to 82), 4/4 (the genre, A; the tempo plan, A; the length, A)"',
  'FEEL = "mid-tempo country story song, a neotraditional two-step, q = 120, 4/4 (the sound, A; the form, A)"')
CUT('V_ = ["F#m7", "F#m7", "Dadd9"', 'M.FORM, M.PLAN, M.BAR0', '''PLAN = {"Intro": ["G", "C", "D", "G"],
        "Verse": ["G", "G", "C", "G", "G", "G", "D", "D", "G", "G", "C", "G", "Em", "C", "D", "D"],
        "Chorus": ["C", "C", "G", "D", "C", "G", "Em", "D", "C", "C", "G", "D"],
        "Turnaround": ["C", "G", "D", "D"], "Tag": ["G", "D", "G", "D"], "Ending": ["C", "G"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 16), ("Chorus 1", "Chorus", 12), ("Verse 2", "Verse", 16), ("Chorus 2", "Chorus", 12),
        ("Verse 3", "Verse", 16), ("Chorus 3", "Chorus", 12), ("Turnaround", "Turnaround", 4), ("Verse 4", "Verse", 16), ("Chorus 4", "Chorus", 12),
        ("Tag", "Tag", 4), ("Ending", "Ending", 2)]                                       # the form, A: 126 bars
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 126 and len(CHORD) == NBARS
CHORD0 = list(CHORD)
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Verse 3", "Chorus 3", "Verse 4", "Chorus 4", "Tag"]
INSTRUMENTAL = ["Intro", "Turnaround", "Ending"]
DESIGN_HALF = {}                                                                      # the designs' half-bars keep the plan's chords (the hook, A)
for _c in ("Chorus 1", "Chorus 2", "Chorus 3"): DESIGN_HALF.update({(_c, 10): ("G", "G"), (_c, 11): ("D", "D")})   # open: 'be' on D3 over D
DESIGN_HALF.update({("Chorus 4", 10): ("G", "G"), ("Chorus 4", 11): ("D", "G"), ("Tag", 0): ("G", "G"), ("Tag", 1): ("D", "G"),
                    ("Tag", 2): ("G", "G"), ("Tag", 3): ("D", "G")})                  # home: F#3 over D, 'be' on G3 over G
''')
P('''BASS8.update({"E/G#": 8, "A/C#": 1, "F#/A#": 10})                                          # the writer's slash chords: their bass
''', '')
P('''    CHORD2 = [h_ for c_ in CHORD0 for h_ in (c_, c_)]                                       # the writer's chords (A: 'only if they're good and not boring'), held as chosen; 438's draw printed, not applied
    CHART438["held"] = "the writer's chords, as chosen"
''', '''    for (_s, _j), (_a, _b) in DESIGN_HALF.items(): CHORD2[2 * (BAR0[_s] + _j)], CHORD2[2 * (BAR0[_s] + _j) + 1] = _a, _b   # the designs' half-bars keep the plan's chords
''')
P('''else:
    CHORD2 = [h_ for c_ in CHORD for h_ in (c_, c_)]
''', '''else:
    CHORD2 = [h_ for c_ in CHORD for h_ in (c_, c_)]
    for (_s, _j), (_a, _b) in DESIGN_HALF.items(): CHORD2[2 * (BAR0[_s] + _j)], CHORD2[2 * (BAR0[_s] + _j) + 1] = _a, _b
''')
P('''SLOTS = {"Verse": [4] * 4, "Pre": [2] * 2, "Chorus": [2] * 7 + [6], "Bridge": [2] * 8, "Last Chorus": [2] * 7 + [8], "Tag": [2, 6]}''',
  '''SLOTS = {"Verse": [2] * 8, "Chorus": [2] * 6, "Tag": [2, 2]}   # every sung line in two bars (308; the form, A)
_SLOTS_P61 = {"Verse": [4] * 4, "Pre": [2] * 2, "Chorus": [2] * 7 + [6], "Bridge": [2] * 8, "Last Chorus": [2] * 7 + [8], "Tag": [2, 6]}''')
P('''CAPD = {"Verse": 61, "Pre": 61, "Chorus": 61, "Tag": 61, "Bridge": 62}                 # the hook (A) and the bridge (A): the tops before the final chorus''',
  '''CAPD = {"Verse": 62, "Chorus": 62, "Tag": 62}                                          # the hook (A): D4 the song's top''')
P('''    R = {k: (min(mu_, CAPD.get(k, 99) - 2), min(cap_, CAPD.get(k, 99)), min(fl_, CAPD.get(k, 99) - 5)) for k, (mu_, cap_, fl_) in R.items()}   # the designs' tops: C#4 outside the bridge (D4) and the final chorus's E4''',
  '''    R = {k: (min(mu_, CAPD.get(k, 99) - 2), min(cap_, CAPD.get(k, 99)), min(fl_, CAPD.get(k, 99) - 5)) for k, (mu_, cap_, fl_) in R.items()}   # the hook's D4 the top''')
P('''SRC = {"Verse 2": "Verse 1", "Verse 3": "Verse 1", "Verse 4": "Verse 1", "Pre 2": "Pre 1", "Pre 3": "Pre 1", "Chorus 2": "Chorus 1", "Chorus 3": "Chorus 1",''',
  '''SRC = {"Verse 2": "Verse 1", "Verse 3": "Verse 1", "Verse 4": "Verse 1", "Pre 2": "Pre 1", "Pre 3": "Pre 1", "Chorus 2": "Chorus 1", "Chorus 3": "Chorus 1", "Chorus 4": "Chorus 1",''')
P('''TRIAD = {9, 1, 4}                                                                    # 311: no ending need; every chorus and the tag end as designed''',
  '''TRIAD = {7, 11, 2}                                                                   # 311: no ending need; every chorus and the tag end as designed''')
# ---- no bridge (749.24): the readers that read one ----
P('''Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS),''', '''Bridge=(draw_plan(rng, "Bridge", BRIDGE_PLANS) if "Bridge" in SUNG else None),''')
P('''    W = [win_feats(notes, BAR0[s]) for s in ("Verse 1", "Chorus 1", "Bridge")]''',
  '''    W = [win_feats(notes, BAR0[s]) for s in ("Verse 1", "Chorus 1", "Bridge") if s in BAR0]   # 749.24: no bridge, two windows''')
P('''    cm, ct, cf, bm = med(notes, "Chorus 1") - med(notes, "Verse 1"), top(notes, "Chorus 1") - top(notes, "Verse 1"), low(notes, "Chorus 1") - low(notes, "Verse 1"), med(notes, "Bridge") - med(notes, "Verse 1")''',
  '''    cm, ct, cf = med(notes, "Chorus 1") - med(notes, "Verse 1"), top(notes, "Chorus 1") - top(notes, "Verse 1"), low(notes, "Chorus 1") - low(notes, "Verse 1")
    HB_ = "Bridge" in BAR0; bm = (med(notes, "Bridge") - med(notes, "Verse 1")) if HB_ else None   # 749.24: no bridge, its aims not read''')
P('''AIMS_278[3]: KB["bridge_median_minus_verse"][0] <= bm <= KB["bridge_median_minus_verse"][1],''',
  '''AIMS_278[3]: (KB["bridge_median_minus_verse"][0] <= bm <= KB["bridge_median_minus_verse"][1]) if HB_ else None,''')
P('''AIMS_278[7]: bm > 0,''', '''AIMS_278[7]: (bm > 0) if HB_ else None,''')
P('''            AIMS_278[8]: top(notes, "Bridge") < max(n["p"] for n in notes),''',
  '''            AIMS_278[8]: (top(notes, "Bridge") < max(n["p"] for n in notes)) if HB_ else None,''')
P('''    if opening_rel(notes, "Bridge", "Verse 1")[0] or opening_rel(notes, "Bridge", "Chorus 1")[0]: f["bridge opening unrelated (208; 279)"] = 1''',
  '''    if "Bridge" in BAR0 and (opening_rel(notes, "Bridge", "Verse 1")[0] or opening_rel(notes, "Bridge", "Chorus 1")[0]): f["bridge opening unrelated (208; 279)"] = 1''')
P('''                        bridge=med(notes, "Bridge") - med(notes, "Verse 1"))''',
  '''                        bridge=(med(notes, "Bridge") - med(notes, "Verse 1")) if "Bridge" in BAR0 else None)''')
P('''ax_b=axes_of(win_feats(notes, BAR0["Bridge"])),''', '''ax_b=(axes_of(win_feats(notes, BAR0["Bridge"])) if "Bridge" in BAR0 else None),''')
# ---- how each line is made ----
P('''        if (sec, i) in DSPEC: return ("figure" if i == 7 else "chant", None, None)        # the designs: the hook (A), the bridge's D4 (A), the tag's last line
        if sec in ("Chorus 2", "Chorus 3", "Last Chorus"): return ("again", "Chorus 1", i) if i in (4, 5) else ("copy", "Chorus 1", i)   # felt / lived / carried: new words on chorus 1's tune
        if sec in ("Verse 2", "Verse 3", "Verse 4", "Pre 2", "Pre 3"): return ("again", SRC[sec], i)
        if sec == "Tag": return ("copy", "Verse 1", 0)                                    # the tag: the opening line as verse 1 sang it''',
  '''        if (sec, i) in DSPEC: return ("figure" if sec == "Chorus 1" else "chant", None, None)   # the designs: the hook (A), its homecoming in chorus 4 and the tag
        if sec in ("Chorus 2", "Chorus 3", "Chorus 4"): return ("again", "Chorus 1", i) if i == 4 else ("copy", "Chorus 1", i)   # line 5 new words (sung again); the rest on chorus 1's tune
        if sec in ("Verse 2", "Verse 3", "Verse 4"): return ("again", SRC[sec], i)''')
P('''tuple(DSPEC) + (("Chorus 2", 7), ("Chorus 3", 7))}   # the designs and their copies left alone''',
  '''tuple(DSPEC) + (("Chorus 2", 5), ("Chorus 3", 5))}   # the designs and their copies left alone''')
# ---- the designs ----
CUT('DESIGN_GATES = ["design: the hook:', 'CARRY_LOW = [', '''DESIGN_GATES = ["design: the hook: 'The man Mama prayed he'd be' climbing G3 B3 to D4 on 'Ma-', the chorus's top, through F#3 to D3 over D, open, in choruses 1-3; chorus 4's 'The woman Daddy prayed I'd be' the same climb, F#3 up to G3 over G, home; nothing over D4",
                "design: the tag: 'The man Mama prayed I'd be' and 'The woman Daddy prayed I'd be', each home on G3 over G"]
HOOK = [(6, 55, 6), (12, 59, 12), (24, 62, 18), (42, 59, 6), (48, 57, 12), (60, 54, 12), (72, 50, 18)]   # the man Ma-ma prayed he'd be: G3 B3, D4 on 'Ma-' (beat 3, over G), B3, A3 F#3 over D, 'be' D3, open
HOME7 = HOOK[:-1] + [(72, 55, 18)]                                                        # the tag's 'The man Mama prayed I'd be': F#3 up to G3 over G, home
HOME8 = [(6, 55, 6), (12, 59, 6), (18, 57, 6), (24, 62, 18), (42, 59, 6), (48, 57, 12), (60, 54, 12), (72, 55, 18)]   # the wo-man Dad-dy prayed I'd be: G3 B3 A3, D4 on 'Dad-', B3, A3 F#3 over D, 'be' G3 over G
HOME8T = HOME8[:-1] + [(72, 55, 24)]                                                      # the tag's last line, 'be' held to the bar's end
DSPEC = {("Chorus 1", 5): HOOK, ("Chorus 4", 5): HOME8, ("Tag", 0): HOME7, ("Tag", 1): HOME8T}
BRIDGE_LOW = (52.0, 57, 45)                                                                 # no bridge (kept for the reader)
BSHIFT = {}
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The designed lines: the hook ('figure': chorus 1's last line, copied in choruses 2 and 3), chorus 4's and the tag's homecoming ('chant')."""
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
    fig = all(rel((s_, 5)) == sp(HOOK) for s_ in ("Chorus 1", "Chorus 2", "Chorus 3")) and rel(("Chorus 4", 5)) == sp(HOME8)
    ctop = all(max([n["p"] for j in range(6) for n in by.get(f"{s_}:{j}", [])] or [99]) == 62 for s_ in ("Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4"))
    stop = max(n["p"] for n in notes) == 62
    if not (fig and ctop and stop): f[g1] = dict(figure=fig, chorus_top=ctop, song_top=stop)
    tag = rel(("Tag", 0)) == sp(HOME7) and rel(("Tag", 1)) == sp(HOME8T)
    if not tag: f[g2] = dict(tag=tag)
    return f
DESIGN_REG.append(("the chorus's centre four semitones or more over the verse's (the chorus above the verse)", lambda R_, info: R_["Chorus"][0] >= R_["Verse"][0] + 4))
DESIGN_GATES.append("design: the chorus above the verse: chorus 1's median (its hook aside) two semitones or more over verse 1's")
_df0 = design_fails
def design_fails(c):
    f = _df0(c); by_ = collections.defaultdict(list)
    for n in c["notes"]: by_[n["line"]].append(n["p"])
    v_ = [p for j in range(8) for p in by_.get(f"Verse 1:{j}", [])]; h_ = [p for j in range(5) for p in by_.get(f"Chorus 1:{j}", [])]
    if not (v_ and h_ and float(np.median(h_)) >= float(np.median(v_)) + 2): f[DESIGN_GATES[2]] = dict(verse=float(np.median(v_)) if v_ else None, chorus=float(np.median(h_)) if h_ else None)
    return f
''')
# ---- the run ----
P("N = _N; SEED = 20261113 + 451", "N = _N; SEED = 20261113 + 454")
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p61.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l7_p64.py {N} {MODE}"''')
P('''open(f"/home/claude/p64/runl7/melody_l7_p61_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p64/runl7/melody_l7_p64_{MODE}{_TAG}.pkl", "wb")''')
assert "Last Chorus\", 7" not in s
open(DST, "w").write(s)
print("wrote", DST)
