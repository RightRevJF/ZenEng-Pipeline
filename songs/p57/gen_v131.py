"""gen_v131.py: writes melody_v131_p57.py (song 47, The Singer Doesn't Stop) from songs/p55's melody_v129_p43.py, as gen_v130.py did
for song 46, with every generic v130 patch (530 as amended by 541, 531, 524's per-slot count) and v131's (540/525, 541, 542, 527).
Every patch replaces whole statements and is asserted to match exactly once. The song: intake.py and lyric_p57.py."""
SRC = "/home/claude/p55/melody_v129_p43.py"; DST = "/home/claude/p57/melody_v131_p57.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)
HEAD = '''"""ZenEng v131 (Module 27.75) -- song 47, The Singer Doesn't Stop, by gen_v131.py from song 43's v129 file. Acoustic-driven modern CCM,
4/4 at q = 84, sixteenth-note strum; G major for a tenor (the search row C3-G4; the second bridge is lifted a whole step in the record,
so its last 'do' sounds A4); 88 bars, every line two bars (Q: the form, A; 527: each line's slot beside the kept slots for its syllables,
none under a tenth). v130's 530 (as 541 amends it) and 531; v131's 540 and 525 (a line's ending class from the kept shares for its notes
and its slot's bars, zeneng_v131_kept_slots.json; a class the kept lines of that slot never take is not drawn), 541 (503's knob takes the
full step only while the gap keeps its sign two rounds running, read on two rounds' builds), 542 (501's give-ups counted apart from 465's).
Designs in force, named: the hook (Q A): 'The song can stop' a short falling figure landing on the tonic, then a full beat of silence;
'But the singer doesn't stop' the same figure a scale step higher, held straight into the next line. The bridge's build (Q A): the second
bridge's first five lines are the first's, note for note (the record lifts them a whole step); 'But You do / Yes You do' rise by step to
G4 (A4 in the record), held; 'You remember all of me' drawn, back in G. Design gates (317), their pass rates printed.
Usage: PYTHONHASHSEED=0 python3 melody_v131_p57.py N main|ctl [tag]
"""
import os as _os11
V131 = int(_os11.environ.get("ZE_PART", "1"))
P131 = {f_: 1 for f_ in ("524", "530", "531", "525", "540", "541", "542", "527")}
OFF11 = set(filter(None, _os11.environ.get("ZE_OFF", "").split(",")))
def ON10(f_): return P131.get(f_, 0) <= V131 and f_ not in OFF11
ON11 = ON10
'''
s = HEAD + s
P('SONG8 = "43"', 'SONG8 = "47"')
P('sys.path[:0] = ["/home/claude/p45", ', 'sys.path[:0] = ["/home/claude/p57", "/home/claude/p45", ')
P("import lyric_p43 as L", "import lyric_p57 as L")
# ---- the frame: G major ----
P('''M.TONIC = 0; M.SCALE = {0, 2, 4, 5, 7, 9, 11}; M.SUNGPC = M.SCALE | {8, 6}               # the frame: C (relative major); G-sharp and F-sharp sung (344)
ETON = 9                                                                              # the song's tonic: A (endings)
OUT_PCS = (8, 6)
M.CH = {"Am": (9, {9, 0, 4}), "F": (5, {5, 9, 0}), "C": (0, {0, 4, 7}), "G": (7, {7, 11, 2}), "Dm": (2, {2, 5, 9}), "Em": (4, {4, 7, 11}), "E": (4, {4, 8, 11})}
M.ROMAN = {"Am": "i", "F": "VI", "C": "III", "G": "VII", "Dm": "iv", "Em": "v", "E": "V"}''',
  '''M.TONIC = 7; M.SCALE = {7, 9, 11, 0, 2, 4, 6}; M.SUNGPC = M.SCALE | {5}                 # G major (the key, Q A); F natural sung (the flat seventh)
ETON = 7                                                                              # the song's tonic: G (endings)
OUT_PCS = (5,)
M.CH = {"G": (7, {7, 11, 2}), "D": (2, {2, 6, 9}), "Em": (4, {4, 7, 11}), "C": (0, {0, 4, 7}), "Am": (9, {9, 0, 4}), "Bm": (11, {11, 2, 6})}
M.ROMAN = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "Bm": "iii"}''')
P('''M.QBPM = 118; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 69; M.SUMMIT = TOP     # the voice row C3-A4 (Q10 A)''',
  '''M.QBPM = 84; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 67; M.SUMMIT = TOP      # the search row C3-G4 (Q5 A: tenor C3-A4; A4 only in the lifted bridge)
LIFT2 = 2                                                                              # the second bridge's first seven lines, a whole step up in the record''')
P('FEEL = "up-tempo dance-pop, q = 118, four on the floor, straight"', 'FEEL = "acoustic-driven modern CCM, q = 84, sixteenth-note strum (Q4 B, Q6 A)"')
i0 = s.index('PLAN = {"Intro": ["Am", "F", "C", "G"] * 2'); i1 = s.index('M.FORM, M.PLAN, M.BAR0')
s = s[:i0] + '''PLAN = {"Intro": ["G", "D", "Em", "C"], "Verse": ["G", "D", "Em", "C", "G", "D", "C", "D"],
        "Chorus": ["C", "G", "Am", "D", "Em", "C", "C", "D", "Em", "C", "D", "G"],
        "Bridge": ["Em", "C", "G", "D", "Em", "C", "Am", "D", "Em", "C", "D", "D"],
        "Bridge2": ["Em", "C", "G", "D", "Em", "C", "Am", "D", "Em", "C", "D", "D", "G", "G", "C", "D"], "Tag": ["C", "G", "D", "G"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 12), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 12),
        ("Bridge", "Bridge", 12), ("Bridge 2", "Bridge2", 16), ("Last Chorus", "Chorus", 12), ("Tag", "Tag", 4)]          # Q7 A; the form's slots, A
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 88 and len(CHORD) == NBARS
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Bridge 2", "Last Chorus", "Tag"]
''' + s[i1:]
P('''    CHORD[:] = CHORD2[0::2]                                                                 # the bar's first chord (readers of the bar)''',
  '''    _b1, _b2 = BAR0["Bridge"], BAR0["Bridge 2"]                                             # the second bridge's first ten bars keep the first's chart (its copies)
    CHORD2[2 * _b2:2 * (_b2 + 10)] = CHORD2[2 * _b1:2 * (_b1 + 10)]
    CHORD[:] = CHORD2[0::2]                                                                 # the bar's first chord (readers of the bar)''')
P('''SLOTS = {"Verse": [2] * 4, "Pre": [2] * 2, "Chorus": [2] * 4, "Post": [2] * 2, "Bridge": [2] * 4, "Last Chorus": [2] * 4}      # every line two bars''',
  '''SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 6, "Bridge": [2] * 6, "Bridge2": [2] * 8, "Tag": [2] * 2, "Last Chorus": [2] * 6}     # every line two bars (the form, A)''')
P('''DESIGNED_TWO_BAR = [(s, i, len(LINES[s][i])) for s in SUNG for i in range(len(LINES[s])) if len(LINES[s][i]) >= 9 and slot_len(s, i) == 2]''',
  '''DESIGNED_TWO_BAR = [(s, i, len(LINES[s][i])) for s in SUNG for i in range(len(LINES[s])) if len(LINES[s][i]) >= 9 and slot_len(s, i) == 2]
K527 = json.load(open("/home/claude/p57/tables/zeneng_v131_kept_slots.json"))["527: the same by each syllable count"]
def k527(n_): return K527[str(n_)] if str(n_) in K527 else K527["16 and over"] if n_ >= 16 else K527["3"]
ROOM527 = [(s_, i_, len(LINES[s_][i_]), slot_len(s_, i_), round(k527(len(LINES[s_][i_]))["shares"][min(slot_len(s_, i_), 5) - 1], 3)) for s_ in SUNG for i_ in range(len(LINES[s_]))]
FLAG527 = [x for x in ROOM527 if x[4] < 0.10]                                               # 527: a slot under a tenth of kept lines of its syllables (shown at intake)''')
# ---- registers and endings ----
P('''    R["Post"] = R["Chorus"]                                                            # the post-chorus sings in the chorus's register''',
  '''    R["Bridge2"] = R["Bridge"]; R["Tag"] = R["Chorus"]                                  # the second bridge in the first's register; the tag in the chorus's''')
P('''ENDING_NEEDS.update(Post={ETON})                                                     # 311: the last post-chorus (the song's last line) ends on the tonic''',
  '''ENDING_NEEDS.update(Chorus={ETON})                                                   # 311: the chorus's last line (the tag's, the song's last) ends on the tonic''')
P('''    if sec == "Post 3": return (p - ETON) % 12 == 0                                      # 'scene after scene': home''',
  '''    if sec in ("Chorus 1", "Chorus 2", "Last Chorus", "Tag"): return (p - ETON) % 12 == 0  # 'Cause the singer doesn't stop': home''')
# ---- how each line is made ----
P('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Post 2": return ("copy", "Post 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", i) if i < 3 else ("return", "Chorus 1", 3)   # 'starring only me and you'
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 2: return ("figure", None, None)                     # Q15 A: the falling sequence
        if sec == "Post 1": return ("chant", None, None)                                   # Q15 A: the chant on the figure
        if kind in ("Chorus", "Post"): return ("fresh", None, None)''',
  '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("return", "Chorus 1", i) if i in (3, 5) else ("copy", "Chorus 1", i)   # 'Even the high part I sang flat'; 'And it will still be me'
        if sec == "Tag": return ("copy", "Chorus 1", 0 if i == 0 else 5)
        if sec == "Bridge 2": return ("copy", "Bridge", i) if i < 5 else ("chant", None, None) if i in (5, 6) else ("fresh", None, None)   # the bridge's build (A)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i in (0, 1): return ("figure", None, None)               # the hook (A)
        if kind in ("Chorus", "Bridge2", "Tag"): return ("fresh", None, None)''')
P('''        rule = sec in ("Verse 1", "Post 3") and i == len(LINES[sec]) - 1''', '''        rule = sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1''')
P('''(("Chorus 2", 2), ("Last Chorus", 2), ("Post 2", 0), ("Post 2", 1))}   # the design and its copies left alone''',
  '''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus") for j_ in (0, 1)) + (("Tag", 0), ("Bridge 2", 5), ("Bridge 2", 6))}   # the designs and their copies left alone''')
P('''        if "fixdur" in n: n["dur"] = n["fixdur"]; continue''', '''        if n.get("holdthrough") and nx is not None: n["dur"] = nx - n["on"]; continue        # the hook (A): held straight into the next line, no breath
        if "fixdur" in n: n["dur"] = n["fixdur"]; continue''')
# ---- the designs ----
i0 = s.index('DESIGN_GATES = ["design: ' + "'blue movie'"); i1 = s.index('CARRY_LOW = [')
s = s[:i0] + '''DESIGN_GATES = ["design: the hook: 'The song can stop' falls by step to the tonic, a beat of silence; 'But the singer doesn't stop' the same figure a step higher, held into the next line",
                "design: the bridge's build: the second bridge's first five lines the first's; 'But You do / Yes You do' rising by step to G4 (A4 lifted), held"]
def sstep(p, k):
    """k scale steps from p (down when k < 0)."""
    q = p
    for _ in range(abs(k)):
        q += -1 if k < 0 else 1
        while q % 12 not in M.SCALE: q += -1 if k < 0 else 1
    return q
HOOK = {0: [(42, 62, 6), (48, 59, 24), (72, 57, 12), (84, 55, 6)],                                   # 'The song can stop': D4 B3 A3 G3, 'stop' short
        1: [(12, 55, 6), (18, 57, 6), (24, 59, 12), (36, 62, 12), (48, 60, 24), (72, 59, 12), (84, 57, None)]}   # 'But the sing-er does-n't stop': the figure a step up
LIFTL = {5: [(0, 62, 12), (12, 64, 12), (24, 66, 60)], 6: [(0, 64, 12), (12, 66, 12), (24, 67, 60)]}   # 'But You do' / 'Yes You do': rising by step to G4, held
def design_line(rng, h, sec, i, U, meta, notes_on):
    """The hook ('figure', Chorus 1 lines 1-2) and the bridge's build ('chant', Bridge 2 lines 6-7), as designed (the writer's choices A)."""
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
    notes = c["notes"]; f = {}; g1, g2 = DESIGN_GATES
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    l0, l1, l2 = by.get("Chorus 1:0", []), by.get("Chorus 1:1", []), by.get("Chorus 1:2", [])
    if len(l0) >= 3 and len(l1) >= 3 and l2:
        a, b2 = l0[-3:], l1[-3:]
        fall = all(0 < x["p"] - y["p"] <= 2 for x, y in zip(a, a[1:])) and (a[-1]["p"] - ETON) % 12 == 0
        sil = l1[0]["on"] - (l0[-1]["on"] + l0[-1].get("dur", 12)) >= 12
        U0, U1 = line_start("Chorus 1", 0), line_start("Chorus 1", 1)
        fig = [x["on"] - U0 for x in a] == [y["on"] - U1 for y in b2] and all(sstep(x["p"], 1) == y["p"] for x, y in zip(a, b2))
        held = l1[-1]["on"] + l1[-1].get("dur", 0) >= l2[0]["on"]
        if not (fall and sil and fig and held): f[g1] = dict(fall=fall, silence=sil, figure=fig, held=held)
    else: f[g1] = "missing"
    rel = lambda k: [(n["on"] - line_start(*k), n["p"]) for n in by.get(f"{k[0]}:{k[1]}", [])]
    same = all(rel(("Bridge", j)) == rel(("Bridge 2", j)) and rel(("Bridge", j)) for j in range(5))
    b5, b6 = by.get("Bridge 2:5", []), by.get("Bridge 2:6", [])
    rise = len(b5) == 3 and len(b6) == 3 and all(0 < y["p"] - x["p"] <= 2 for L_ in (b5, b6) for x, y in zip(L_, L_[1:])) and b6[0]["p"] > b5[0]["p"]
    top = bool(b6) and b6[-1]["p"] == TOP and b6[-1].get("dur", 0) >= 48
    under = max([n["p"] for j in range(5) for n in by.get(f"Bridge:{j}", [])] or [0]) <= TOP - 1   # lifted, the copies stay under the held A4
    if not (same and rise and top and under): f[g2] = dict(same=same, rise=rise, top=top, copies_under=under)
    return f
def design_reg(R_, info):
    """325: the first bridge's register under the song's top, so its lifted copy stays under the held A4."""
    return R_["Bridge"][1] <= TOP - 1
DESIGN_REG.append(("the bridge's register under G4 (the lift, A)", design_reg))
''' + s[i1:]
P('''CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1", "Bridge")]                                  # 329: the first chorus or the bridge''',
  '''CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1",)]                                          # 329: the first chorus (the bridge stays under the lift)''')
P('''    car_hi = ("Chorus 1", 3)                                                               # Q15 A: 'starring nobody but you' lifts to the chorus's top''',
  '''    car_hi = rng.choice(highc) if highc else None''')
P('''MAJ = {0, 2, 3, 5, 7, 8, 10}                                                         # 353: the natural minor scale, read on the tonic
MTON = ETON; OS_SCALE = 4.5 / 7.1                                                     # 353: the measures on A; 349: the kept minor rate''',
  '''MAJ = {0, 2, 4, 5, 7, 9, 11}                                                         # a major song''')
# ---- 541 (amends 530), 531 ----
P('''                t_, r_ = float(np.mean(ua["_ctb1"])), float(np.mean(ua["_ctb2"])); f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK["ctb503"] = float(np.clip(LK["ctb503"] * f_, 0.05, 20.0))''',
  '''                c1_, c2_ = list(ua["_ctb1"]) + CTB541[0], list(ua["_ctb2"]) + CTB541[1]             # 541: read on two rounds' builds
                CTB541[:] = [list(ua["_ctb1"]), list(ua["_ctb2"])]
                t_, r_ = float(np.mean(c1_)), float(np.mean(c2_)); f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** 2, 0.6, 1.6))
                if ON11("541"):                                                                # 541: the full step only while the gap keeps its sign two rounds running
                    sg_ = 0 if abs(r_ - t_) <= 0.02 else (1 if r_ > t_ else -1)
                    full_ = (0.6 if sg_ > 0 else 1.6); f_ = 1.0 if sg_ == 0 else (full_ if sg_ == SG541[0] else full_ ** 0.5); SG541[0] = sg_
                LK["ctb503"] = float(np.clip(LK["ctb503"] * f_, 0.05, 20.0))''')
P('''            if not (q_[1] <= ob_ <= q_[3]): STATS["501: outside the kept onsets a beat, redrawn"] += 1; continue''',
  '''            lo501, hi501 = (q_[0], q_[4]) if ON10("531") else (q_[1], q_[3])                  # 531: the kept 5th-95th
            if not (lo501 <= ob_ <= hi501): STATS["501: outside the kept onsets a beat, redrawn"] += 1; G542[0] += 1; continue''')
# ---- 542: 501's give-ups apart from 465's ----
P('''    NT = 20 if copybars else 14; fb457 = [False]''', '''    NT = 20 if copybars else 14; fb457 = [False]; G542[:] = [0, 0]''')
P('''        if ON9("501") and span_to is not None and not fix and n >= 3 and _try == NT // 2: STATS["501: onsets a beat given up for a line"] += 1''',
  '''        if ON9("501") and span_to is not None and not fix and n >= 3 and _try == NT // 2:
            STATS["501: onsets a beat given up for a line"] += 1
            if ON11("542"): STATS["542: given up at half the tries: " + ("501's bound and 465's class both missed" if G542[0] and G542[1] else "501's bound missed (465 not)" if G542[0] else "465's class missed (501 not)" if G542[1] else "neither (another bound)")] += 1''')
P('''        ons = sample(alpha)
        if ons is None: continue''', '''        ons = sample(alpha)
        if ons is None:
            if h465: G542[1] += 1                                                          # 542: no rhythm ends in 465's drawn bar
            continue''')
# ---- 524's per-slot count; 525 (540): the kept classes by the slot's bars and the line's notes ----
P('''    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]))''',
  '''    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]), at=(sec, i))''')
P('''        sh_ = [a_ * b_ / max(1e-9, p_) for a_, b_, p_ in zip(sh_, ss_, PALL465)]''',
  '''        sh_ = [a_ * b_ / max(1e-9, p_) for a_, b_, p_ in zip(sh_, ss_, PALL465)]
    if ON11("525"):                                                                         # 525 (540): the kept shares for the slot's bars and the line's notes
        sh_ = list(K525[str(min(5, c_["nb"])) if c_["nb"] < 5 else "5+"][nband525(n)]["shares"])''')
P('''        elif sh_[k_] > 0 and ON9("500"): STATS[f"500: class {k_} out of reach, {c_['nb']}-bar slot, {n} syllables"] += 1''',
  '''        elif sh_[k_] > 0 and ON9("500"):
            STATS[f"500: class {k_} out of reach, {c_['nb']}-bar slot, {n} syllables"] += 1
            if ON10("524"): STATS[f"524: {c_['at'][0]}:{c_['at'][1]} ({c_['nb']} bars, {n} syllables) class {k_} out of reach"] += 1''')
P('''def draw465(rng, n, tmin, end, step, feas=None):''', '''K525 = json.load(open("/home/claude/p57/tables/zeneng_v131_kept_slots.json"))["525: ending classes by slot bars and by NOTES in the line"]
def nband525(n_): return "3 to 5" if n_ <= 5 else "6 to 8" if n_ <= 8 else "9 to 12" if n_ <= 12 else "13 and over"
G542 = [0, 0]; CTB541 = [[], []]; SG541 = [0]
def draw465(rng, n, tmin, end, step, feas=None):''')
P('''Pre=draw_plan(rng, "Pre 1", PRE_PLANS),''', '''Pre=(draw_plan(rng, "Pre 1", PRE_PLANS) if "Pre 1" in SUNG else None),''')
P('''            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)''', '''            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)
            if (sec, i) == ("Chorus 1", 5): tmin = max(tmin, 6)                            # the tag sings this line straight after the hook's 'stop': no pickup''')
# ---- the run ----
P("N = _N; SEED = 20261110 + 443", "N = _N; SEED = 20261113 + 447")
P('''open(f"{H114}/lyric_p43.py", "rb").read()''', '''open("/home/claude/p57/lyric_p57.py", "rb").read()''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v129_p43.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_v131_p57.py {N} {MODE}"''')
P('''    rerun["chart438"] = CHART438''', '''    rerun["chart438"] = CHART438
    rerun["v131_part"] = V131; rerun["v131_on"] = sorted(f_ for f_ in P131 if ON11(f_)); rerun["room527"] = ROOM527; rerun["flag527"] = FLAG527
    rerun["out_of_reach524"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_.startswith("524:")}
    rerun["giveups542"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_.startswith("542:") or k_.startswith("501:") or k_.startswith("465: class given")}''')
P('''open(f"{H118}/melody_v129_p43_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p57/melody_v131_p57_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST, len(s.splitlines()), "lines")
