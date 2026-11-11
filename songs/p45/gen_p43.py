"""Writes melody_p43.py: song 43, Blue Movie, on the v114 port (melody_v114_p40.py): its song constants, lyric, designs and seed."""
s = open("/home/claude/p45/melody_v114_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
s = '''"""ZenEng v114 -- song 43, Blue Movie (findings from 348; v114's fixes are 340-347). Up-tempo dance-pop, q = 118, four on the floor,
straight; A minor for a light tenor (row C3-A4); 80 bars. The range centred in the row (314/333). Designs in force, named:
  Q15 A  the chorus's 'blue movie, blue movie' is one rhythmic figure sung twice, the second a scale step lower: a falling sequence
         from the chorus's high note; 'starring nobody but you' lifts back to the chorus's top (it carries 329's high extreme);
         the post-chorus chants: 'blue, blue' and 'no one else in the' on one pitch each, each line ending on the figure.
         A design gate (317), its pass rate printed.
  Q16 A  the arrangement (no melody gate). Q14 A: the lyric's density kept as written (342).
The frame: the engine's tables are major-keyed (the key profile, the window measures, the PPM), so the song is read on its relative
major (C); its endings are on its own tonic, A (ETON).
Usage: PYTHONHASHSEED=0 python3 melody_p43.py N main|ctl [tag]
The v114 port it is built on:
''' + s[3:]
R('sys.path[:0] = ["/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]',
  'sys.path[:0] = ["/home/claude/p45", "/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]')
R('import lyric_p40 as L', '''import lyricsearch; lyricsearch.OVERRIDE["pleather"] = ("P L EH1 DH ER0",)          # not in the pronouncing dictionary
import lyric_p43 as L''')
a = s.index("M.TONIC = 2;"); b = s.index("STOP_BARS = set()")
s = s[:a] + '''M.TONIC = 0; M.SCALE = {0, 2, 4, 5, 7, 9, 11}; M.SUNGPC = M.SCALE | {8, 6}               # the frame: C (relative major); G-sharp and F-sharp sung (344)
ETON = 9                                                                              # the song's tonic: A (endings)
OUT_PCS = (8, 6)
M.CH = {"Am": (9, {9, 0, 4}), "F": (5, {5, 9, 0}), "C": (0, {0, 4, 7}), "G": (7, {7, 11, 2}), "Dm": (2, {2, 5, 9}), "Em": (4, {4, 7, 11}), "E": (4, {4, 8, 11})}
M.ROMAN = {"Am": "i", "F": "VI", "C": "III", "G": "VII", "Dm": "iv", "Em": "v", "E": "V"}
M.QBPM = 118; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 69; M.SUMMIT = TOP     # the voice row C3-A4 (Q10 A)
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
FEEL = "up-tempo dance-pop, q = 118, four on the floor, straight"
PLAN = {"Intro": ["Am", "F", "C", "G"] * 2, "Verse": ["Am", "F", "C", "G"] * 2, "Pre": ["Dm", "Em", "F", "G"],
        "Chorus": ["F", "G", "Am", "C", "F", "G", "F", "G"], "LastChorus": ["F", "G", "Am", "C", "F", "G", "F", "G"],
        "Post": ["Am", "F", "C", "G"], "LastPost": ["Am", "F", "G", "Am"], "Bridge": ["Dm", "Am", "F", "C", "Dm", "Am", "E", "E"], "Outro": ["Am", "F", "G", "Am"]}
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
    return True''', '''TRIAD = {9, 0, 4}
ENDING_NEEDS.update(Post={ETON})                                                     # 311: the last post-chorus (the song's last line) ends on the tonic
def end_ok(sec, i, p):
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return (p - ETON) % 12 != 0                                     # the verse ends off the tonic
    if sec == "Post 3": return (p - ETON) % 12 == 0                                      # 'scene after scene': home
    return True''')
s = s.replace("(p - M.TONIC) % 12 == 0", "(p - ETON) % 12 == 0")
a = s.index('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)'''); b = s.index('''        plan = plans[kind]; first = plan.index(plan[i])''')
s = s[:a] + '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Post 2": return ("copy", "Post 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", i) if i < 3 else ("return", "Chorus 1", 3)   # 'starring only me and you'
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 2: return ("figure", None, None)                     # Q15 A: the falling sequence
        if sec == "Post 1": return ("chant", None, None)                                   # Q15 A: the chant on the figure
        if kind in ("Chorus", "Post"): return ("fresh", None, None)
''' + s[b:]
R('''    car_hi = rng.choice(highc) if highc else None''', '''    car_hi = ("Chorus 1", 3)                                                               # Q15 A: 'starring nobody but you' lifts to the chorus's top''')
R('''        rule = (sec, i) == ("Chorus 1", 0) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''',
  '''        rule = sec in ("Verse 1", "Post 3") and i == len(LINES[sec]) - 1''')
R('''        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("copy", "return", "plan", "tail") and (s0, i0) in built:''', '''        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("figure", "chant"):                                                         # Q15 A: the designed lines
            r = ("ns", design_line(rng, h, sec, i, U, meta, notes_on_all), "design")
        elif h in ("copy", "return", "plan", "tail") and (s0, i0) in built:''')
R('''            if h in ("copy", "return", "plan", "tail") and (prefit(sec, i) or ("",))[0] == "ns":''',
  '''            if h in ("copy", "return", "plan", "tail", "figure", "chant") and (prefit(sec, i) or ("",))[0] == "ns":''')
R('''                meta["kinds"][(sec, i)] = kd if h != "tail" else "tail"''', '''                meta["kinds"][(sec, i)] = kd if h != "tail" else "tail"
                if h in ("figure", "chant"): meta["kinds"][(sec, i)] = "design"''')
R('''    built_ret = {f"{sec}:{i}" for sec, i, s0, i0, kd in meta["returns"] if kd != "sung again"}''',
  '''    built_ret = {f"{sec}:{i}" for sec, i, s0, i0, kd in meta["returns"] if kd != "sung again"}
    built_ret |= {f"{sec}:{i}" for (sec, i), kd in meta["kinds"].items() if kd == "design" or (sec, i) in (("Chorus 2", 2), ("Last Chorus", 2), ("Post 2", 0), ("Post 2", 1))}   # the design and its copies left alone''')
R('''        if n["p"] % 12 in (5, 0) and M.clash(n["p"], ch_):''', '''        if n["p"] % 12 in OUT_PCS and M.clash(n["p"], ch_):''')
R('''DESIGN_GATES = []                                                                     # the default path: none in force''',
  '''DESIGN_GATES = ["design: 'blue movie' a falling sequence from the chorus's top; 'starring nobody but you' lifts back to it; the post-chorus chants the figure (Q15 A)"]
FIG_RH = [((0, 24, 30), 0.35), ((12, 24, 30), 0.30), ((18, 24, 30), 0.15), ((0, 24, 36), 0.20)]      # 'BLUE MO-vie': 'mo' on beat 1 or 3 (232)
FIG = {}
def sstep(p, k):
    """k scale steps from p (down when k < 0)."""
    q = p
    for _ in range(abs(k)):
        q += -1 if k < 0 else 1
        while q % 12 not in M.SCALE: q += -1 if k < 0 else 1
    return q
def design_line(rng, h, sec, i, U, meta, notes_on):
    """Q15 A. 'figure' (Chorus 1, line 3): the figure on 'blue movie', then again a scale step lower, from the chorus's top.
    'chant' (Post 1): 'blue, blue' on the figure's first pitch, then the figure; 'no one else in the' on its third, then the figure lower."""
    sy = LINES[sec][i]
    if h == "figure":
        xhi = meta["carriers"]["high"][1]; r_ = rng.choices([x for x, _ in FIG_RH], [w for _, w in FIG_RH])[0]
        for T in (xhi, sstep(xhi, -1), sstep(xhi, -2)):
            b1 = [T, sstep(T, -1), sstep(T, -2)]; b2 = [sstep(p, -1) for p in b1]
            ons = [U + o for o in r_] + [U + BAR + o for o in r_]
            if not any(tri(p, M.chord_at(t)) for p, t in zip(b1 + b2, ons)): break
            STATS["design: figure moved below the top (a tritone from the root)"] += 1
        FIG.clear(); FIG.update(r=r_, T=T, b1=b1, b2=b2)
        return [dict(on=t, p=p, syl=k, slur=False, stress=sy[k][1]) for k, (t, p) in enumerate(zip(ons, b1 + b2))]
    r_, b1, b2 = FIG["r"], FIG["b1"], FIG["b2"]
    if i == 0: pre, cp, fig = [0, 24], b1[0], b1                                              # 'Blue, blue,' | 'blue movie'
    else: pre, cp, fig = [12, 18, 24, 30, 36], b1[2], b2                                       # 'no one else in the' | 'blue movie', a step lower
    ons = [U + o for o in pre] + [U + BAR + o for o in r_]; ps = [cp] * len(pre) + fig
    assert len(ons) == len(sy), (sec, i, len(ons), len(sy))
    return [dict(on=t, p=p, syl=k, slur=False, stress=sy[k][1]) for k, (t, p) in enumerate(zip(ons, ps))]
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}; g = DESIGN_GATES[0]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    fl, l3, p0, p1 = by.get("Chorus 1:2", []), by.get("Chorus 1:3", []), by.get("Post 1:0", []), by.get("Post 1:1", [])
    ch = [n for n in notes if n["sec"] == "Chorus 1"]
    if not (len(fl) == 6 and l3 and len(p0) >= 3 and len(p1) >= 3): f[g] = "missing"; return f
    U = line_start("Chorus 1", 2); r1 = [n["on"] - U for n in fl[:3]]; r2 = [n["on"] - U - BAR for n in fl[3:]]
    seq = r1 == r2 and all(sstep(a["p"], -1) == b_["p"] for a, b_ in zip(fl[:3], fl[3:]))
    top_ = max(n["p"] for n in ch); fall = fl[0]["p"] >= max(n["p"] for n in ch if n["line"] in ("Chorus 1:0", "Chorus 1:1")) and fl[0]["p"] >= top_ - 2
    lift = max(n["p"] for n in l3) == top_ and max(n["p"] for n in l3) >= fl[0]["p"]
    chant = [n["p"] for n in p0[-3:]] == [n["p"] for n in fl[:3]] and [n["p"] for n in p1[-3:]] == [n["p"] for n in fl[3:]] and \\
            len({n["p"] for n in p0[:-3]}) == 1 and len({n["p"] for n in p1[:-3]}) == 1
    if not (seq and fall and lift and chant): f[g] = dict(seq=seq, fall=fall, lift=lift, chant=chant)
    return f
def design_reg(R_, info):
    """325: the figure falls three scale steps from the song's top inside the chorus's register."""
    lo, hi = info["song_lo"], info["song_hi"]; xhi = max(p for p in range(lo, hi + 1) if p % 12 in M.SCALE)
    return sstep(xhi, -3) >= lo
DESIGN_REG.append(("the figure's fall inside the song's range (Q15 A)", design_reg))''')
R('''    f = gate_fails(c, c.get("judge"))
    for g in GATES:''', '''    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))
    for g in DESIGN_GATES + GATES:''')
R('''        fails = gate_fails(c, c["judge"]); info = c["info"]''', '''        fails = gate_fails(c, c["judge"]); fails.update(design_fails(c)); info = c["info"]''')
R('''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in list(GATES) + sorted(k for k in would if k not in GATES)]''',
  '''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in DESIGN_GATES + list(GATES) + sorted(k for k in would if k not in GATES and k not in DESIGN_GATES)]''')
R('N = _N; SEED = 20261110 + 401', 'N = _N; SEED = 20261110 + 443')
R('open(f"{HERE}/lyric_p40.py", "rb").read()', 'open(f"{H114}/lyric_p43.py", "rb").read()')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_v114_p40.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_p43.py {N} {MODE}"')
R('open(f"{H114}/melody_v114_p40_{MODE}{_TAG}.pkl", "wb"))', 'open(f"{H114}/melody_p43_{MODE}{_TAG}.pkl", "wb"))')
R('''    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''',
  '''    plans = [(p[:len(LINES[sec])], w) for p, w in plans]                                  # four-line sections: each plan cut to its first lines
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''')
open("/home/claude/p45/melody_p43.py", "w").write(s)
print("written")
