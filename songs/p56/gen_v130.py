"""gen_v130.py: writes melody_v130_p56.py (song 46, Dry Ground) from songs/p55's melody_v129_p43.py (song 43: q = 118, four on the floor,
A minor, tenor row C3-A4). Every patch replaces whole statements and is asserted to match exactly once.
v130 (Module 27.74): 530 (503's knob at full step until verse 2 is within two points), 531 (501 on the kept 5th-95th), 524 (the form's
slots; the kept endings a slot cannot reach, printed). The song: the writer's intake (intake.py) and lyric (lyric_p56.py)."""
SRC = "/home/claude/p55/melody_v129_p43.py"; DST = "/home/claude/p56/melody_v130_p56.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)
HEAD = '''"""ZenEng v130 (Module 27.74) -- song 46, Dry Ground: the next song (522) on the default path, by gen_v130.py from song 43's v129 file.
Atmospheric pop, q = 118, four on the floor, straight; A minor for a tenor (row C3-A4, the falsetto B4 once, designed); 120 bars.
The form gives a line room (524): a line of nine syllables or more has a slot of three bars or more (Q11 A); for each slot the kept
endings (465's classes, 500's shares by notes and slot) it cannot reach are counted and printed. 530: 503's knob takes its full step
each round until verse 2's chord tones on the beat are within two points of verse 1's. 531: 501's bound is the kept 5th-95th percentile.
Designs in force, named (Q12 A): 'And I miss the water': 'water' on the chorus's high note; 'God I miss the flood': choruses 1 and 2,
'flood' falls to the tonic A and holds; the last chorus, 'flood' leaps to the falsetto B4 and holds. A design gate (317), its pass
rate printed. Q13 A, the arrangement: no melody gate. Usage: PYTHONHASHSEED=0 python3 melody_v130_p56.py N main|ctl [tag]
"""
import os as _os10
V130 = int(_os10.environ.get("ZE_PART", "1"))
P130 = {f_: 1 for f_ in ("524", "530", "531")}
OFF10 = set(filter(None, _os10.environ.get("ZE_OFF", "").split(",")))
def ON10(f_): return P130.get(f_, 0) <= V130 and f_ not in OFF10
'''
s = HEAD + s
P('SONG8 = "43"', 'SONG8 = "46"')
P('sys.path[:0] = ["/home/claude/p45", ', 'sys.path[:0] = ["/home/claude/p56", "/home/claude/p45", ')
P("import lyric_p43 as L", "import lyric_p56 as L")
# ---- the frame, the plan and the form ----
P('''M.QBPM = 118; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 69; M.SUMMIT = TOP     # the voice row C3-A4 (Q10 A)''',
  '''M.QBPM = 118; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 48; TOP = 69; M.SUMMIT = TOP     # the voice row C3-A4 (Q5 A); the falsetto B4 is the design's (Q12 A)
FALSETTO = 71''')
P('FEEL = "up-tempo dance-pop, q = 118, four on the floor, straight"', 'FEEL = "atmospheric pop, q = 118, four on the floor, straight (Q4 C, Q6 A)"')
i0 = s.index('PLAN = {"Intro": ["Am", "F", "C", "G"] * 2'); i1 = s.index('M.FORM, M.PLAN, M.BAR0')
s = s[:i0] + '''PLAN = {"Intro": ["Am", "F", "C", "G"] * 2, "Verse": ["Am", "F", "C", "G", "Am", "F", "C", "G", "F", "G"],
        "Pre": ["Dm", "Em", "F", "G", "Dm", "Em", "F", "F", "G", "G"],
        "Chorus": ["F", "G", "Am", "C", "F", "G", "Am", "F", "G", "G", "F", "G", "Am", "F", "Am", "F"],
        "LastChorus": ["F", "G", "Am", "C", "F", "G", "Am", "F", "G", "G", "F", "G", "Em", "Em", "G", "G"],
        "Bridge": ["Dm", "Dm", "Am", "F", "F", "C", "Dm", "Dm", "Am", "F", "E", "E"], "Outro": ["Am", "F", "C", "Am", "F", "C", "F", "G", "Am", "F", "Am", "Am"]}
FORM = [("Intro", "Intro", 8), ("Verse 1", "Verse", 10), ("Pre 1", "Pre", 10), ("Chorus 1", "Chorus", 16), ("Verse 2", "Verse", 10), ("Pre 2", "Pre", 10),
        ("Chorus 2", "Chorus", 16), ("Bridge", "Bridge", 12), ("Last Chorus", "Chorus", 16), ("Outro", "Outro", 12)]      # Q7 A, Q11 A (524)
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else kind]; b += nb
NBARS = b; assert NBARS == 120 and len(CHORD) == NBARS
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus", "Outro"]
''' + s[i1:]
P('''SLOTS = {"Verse": [2] * 4, "Pre": [2] * 2, "Chorus": [2] * 4, "Post": [2] * 2, "Bridge": [2] * 4, "Last Chorus": [2] * 4}      # every line two bars''',
  '''SLOTS = {"Verse": [2, 2, 3, 3], "Pre": [2, 2, 3, 3], "Chorus": [2, 2, 3, 3, 2, 4], "Bridge": [3, 3, 3, 3], "Outro": [3, 3, 2, 4],
         "Last Chorus": [2, 2, 3, 3, 2, 4]}                                                  # 524 (Q11 A): every line of nine syllables or more has three bars''')
P('''def slot_end(sec, i):
    n = slot_len(sec, i)''', '''def slot_end(sec, i):
    n = slot_len(sec, i)
    if KIND[sec] == "Chorus" and i == 5: return 2 * BAR                                  # Q12 A: 'flood' sung by the slot's third downbeat, room to hold''')
P('''DESIGNED_TWO_BAR = [(s, i, len(LINES[s][i])) for s in SUNG for i in range(len(LINES[s])) if len(LINES[s][i]) >= 9 and slot_len(s, i) == 2]''',
  '''DESIGNED_TWO_BAR = [(s, i, len(LINES[s][i])) for s in SUNG for i in range(len(LINES[s])) if len(LINES[s][i]) >= 9 and slot_len(s, i) == 2]
ROOM524 = [(s, i, len(LINES[s][i]), slot_len(s, i)) for s in SUNG for i in range(len(LINES[s])) if len(LINES[s][i]) >= 9]   # 524: the long lines and their slots
FLAG524 = [x for x in ROOM524 if x[3] < 3]                                                  # 524: where the lyric does not allow three bars (flagged to the writer)
assert not DESIGNED_TWO_BAR''')
# ---- registers and endings ----
P('''    R["Post"] = R["Chorus"]                                                            # the post-chorus sings in the chorus's register''',
  '''    R["Outro"] = R["Verse"]                                                            # the sung outro in the verse's register''')
P('''ENDING_NEEDS.update(Post={ETON})                                                     # 311: the last post-chorus (the song's last line) ends on the tonic''',
  '''ENDING_NEEDS.update(Outro={ETON}, Chorus={ETON})                                       # 311: the outro (the song's last line) and the chorus's 'flood' (Q12 A) end on the tonic''')
P('''    if sec == "Post 3": return (p - ETON) % 12 == 0                                      # 'scene after scene': home''',
  '''    if sec == "Outro": return (p - ETON) % 12 == 0                                       # 'And let the grey come in': home
    if sec in ("Chorus 1", "Chorus 2"): return (p - ETON) % 12 == 0                       # Q12 A: 'flood' on the tonic''')
# ---- how each line is made ----
P('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Post 2": return ("copy", "Post 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", i) if i < 3 else ("return", "Chorus 1", 3)   # 'starring only me and you'
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if sec == "Chorus 1" and i == 2: return ("figure", None, None)                     # Q15 A: the falling sequence
        if sec == "Post 1": return ("chant", None, None)                                   # Q15 A: the chant on the figure
        if kind in ("Chorus", "Post"): return ("fresh", None, None)''',
  '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("return", "Chorus 1", 3) if i == 3 else ("copy", "Chorus 1", i)   # 'I stand out in it till I'm soaked'
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if kind in ("Chorus", "Outro"): return ("fresh", None, None)''')
P('''    car_hi = ("Chorus 1", 3)                                                               # Q15 A: 'starring nobody but you' lifts to the chorus's top''',
  '''    car_hi = ("Chorus 1", 4)                                                               # Q12 A: 'water' on the chorus's high note''')
P('''        rule = sec in ("Verse 1", "Post 3") and i == len(LINES[sec]) - 1''', '''        rule = sec in ("Verse 1", "Outro", "Chorus 1") and i == len(LINES[sec]) - 1''')
P('''            if h == "copy": r = ("ns", [dict(n, on=n["on"] - SU + U) for n in S], "exact")''',
  '''            if h == "copy": r = ("ns", [dict(n, on=n["on"] - SU + U) for n in S], "exact")
            if h == "copy" and (sec, i) == ("Last Chorus", 5):                               # Q12 A: the last 'flood' leaps to the falsetto B4
                r[1][-1].update(p=FALSETTO, falsetto=True, pin=True); r = (r[0], r[1], "design")''')
# the carrier of the chorus's top: the word 'water'
P('''                        order_ = sorted(range(len(ns)), key=lambda j: -shape[j][0] if hiq else shape[j][0])''',
  '''                        order_ = sorted(range(len(ns)), key=lambda j: -shape[j][0] if hiq else shape[j][0])
                        if (sec, i) == car_hi: order_ = [j for j in order_ if ns[j]["syl"] in (4, 5)]              # Q12 A: 'wa-ter'
                        if (sec, i) == car_hi and _try == 5: STATS["design: 'water' could not take the top (six tries)"] += 1''')
P('''                            fx = dict(fx or {}); fx[jx] = x''', '''                            fx = dict(fx or {}); fx[jx] = x
                            if (sec, i) == car_hi: ns[jx]["pin"] = True''')
P('''(("Chorus 2", 2), ("Last Chorus", 2), ("Post 2", 0), ("Post 2", 1))}   # the design and its copies left alone''',
  '''tuple((s_, j_) for s_ in ("Chorus 1", "Chorus 2", "Last Chorus") for j_ in (4, 5))}   # the design and its copies left alone''')
P('''    finish(notes, rng)
    return dict(notes=notes, meta=meta), None''', '''    for k_ in ("Chorus 1:5", "Chorus 2:5", "Last Chorus:5"):                               # Q12 A: 'flood' holds
        ln_ = [n for n in notes if n["line"] == k_]
        if ln_: ln_[-1]["holdlong"] = True
    finish(notes, rng)
    return dict(notes=notes, meta=meta), None''')
P('''        if "fixdur" in n: n["dur"] = n["fixdur"]; continue''', '''        if "fixdur" in n: n["dur"] = n["fixdur"]; continue
        if n.get("holdlong") and nx is not None: n["dur"] = int(min(96, max(3, (nx - n["on"] - 6) // 6 * 6))); continue   # Q12 A: up to two bars''')
# ---- the design gate ----
i0 = s.index('DESIGN_GATES = ["design: ' + "'blue movie'"); i1 = s.index('CARRY_LOW = [')
s = s[:i0] + '''DESIGN_GATES = ["design: 'water' on the chorus's high note; 'flood' falls to the tonic and holds (choruses 1, 2); the last 'flood' leaps to the falsetto B4 and holds (Q12 A)"]
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}; g = DESIGN_GATES[0]
    by = collections.defaultdict(list)
    for n in notes: by[n["line"]].append(n)
    w4, f5, l5 = by.get("Chorus 1:4", []), by.get("Chorus 1:5", []), by.get("Last Chorus:5", [])
    if not (w4 and f5 and l5): f[g] = "missing"; return f
    ch = [n for n in notes if n["sec"] == "Chorus 1"]; top_ = max(n["p"] for n in ch)
    wat = [n for n in w4 if n.get("syl") in (4, 5)]
    water = bool(wat) and max(n["p"] for n in wat) == top_
    fl = f5[-1]; falls = (fl["p"] - ETON) % 12 == 0 and fl["p"] < (max(n["p"] for n in wat) if wat else top_) and fl.get("dur", 0) >= 48
    lf = l5[-1]; leap = lf["p"] == FALSETTO and len(l5) > 1 and lf["p"] - l5[-2]["p"] >= 5 and lf.get("dur", 0) >= 48
    if not (water and falls and leap): f[g] = dict(water=water, falls=falls, leap=leap)
    return f
''' + s[i1:]
P('''    if min(ps) < M.LO or max(ps) > TOP: return ("range (the voice row)", (min(ps), max(ps))), None''',
  '''    ps = [n["p"] for n in notes if not n.get("falsetto")]                                 # Q12 A: the designed falsetto stands outside the row
    if min(ps) < M.LO or max(ps) > TOP: return ("range (the voice row)", (min(ps), max(ps))), None
    ps = [n["p"] for n in notes]''')
# ---- 530 and 531 ----
P('''                t_, r_ = float(np.mean(ua["_ctb1"])), float(np.mean(ua["_ctb2"])); f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK["ctb503"] = float(np.clip(LK["ctb503"] * f_, 0.05, 20.0))''',
  '''                t_, r_ = float(np.mean(ua["_ctb1"])), float(np.mean(ua["_ctb2"])); f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** 2, 0.6, 1.6))
                if ON10("530"): f_ = (0.6 if r_ > t_ else 1.6) if abs(r_ - t_) > 0.02 else 1.0     # 530: the full step each round until within two points
                LK["ctb503"] = float(np.clip(LK["ctb503"] * f_, 0.05, 20.0))''')
P('''            if not (q_[1] <= ob_ <= q_[3]): STATS["501: outside the kept onsets a beat, redrawn"] += 1; continue''',
  '''            lo501, hi501 = (q_[0], q_[4]) if ON10("531") else (q_[1], q_[3])                  # 531: the kept 5th-95th
            if not (lo501 <= ob_ <= hi501): STATS["501: outside the kept onsets a beat, redrawn"] += 1; continue''')
# ---- 524: the kept endings each slot cannot reach ----
P('''    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]))''',
  '''    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]), at=(sec, i))''')
P('''        elif sh_[k_] > 0 and ON9("500"): STATS[f"500: class {k_} out of reach, {c_['nb']}-bar slot, {n} syllables"] += 1''',
  '''        elif sh_[k_] > 0 and ON9("500"):
            STATS[f"500: class {k_} out of reach, {c_['nb']}-bar slot, {n} syllables"] += 1
            if ON10("524"): STATS[f"524: {c_['at'][0]}:{c_['at'][1]} ({c_['nb']} bars, {n} syllables) class {k_} out of reach"] += 1''')
P('''PRE_PLANS = [("AB", 0.75), ("AA", 0.25)]''', '''PRE_PLANS = VERSE_PLANS                                                               # song 46: four-line pre-choruses take the verse's plans (their first four letters)''')
P('''nb = slot_len(sec, i); lo_ = 0 if nb == 1 else (nb - 1) * BAR - 24''', '''nb = slot_len(sec, i); lo_ = land_lo(sec, i, nb)''', 3)
P('''def land_w406(sec, n_syl, i=None, allowed=None):''', '''def land_lo(sec, i, nb):
    if KIND[sec] == "Chorus" and i == 5: return BAR + 24                                    # Q12 A: 'flood' lands in the slot's second or third bar, to hold
    return 0 if nb == 1 else (nb - 1) * BAR - 24
def land_w406(sec, n_syl, i=None, allowed=None):''')
# ---- the run ----
P("N = _N; SEED = 20261110 + 443", "N = _N; SEED = 20261113 + 446")
P('''open(f"{H114}/lyric_p43.py", "rb").read()''', '''open("/home/claude/p56/lyric_p56.py", "rb").read()''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v129_p43.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_v130_p56.py {N} {MODE}"''')
P('''    rerun["chart438"] = CHART438''', '''    rerun["chart438"] = CHART438
    rerun["v130_part"] = V130; rerun["v130_on"] = sorted(f_ for f_ in P130 if ON10(f_)); rerun["room524"] = ROOM524; rerun["flag524"] = FLAG524
    rerun["out_of_reach524"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_.startswith("524:")}''')
P('''open(f"{H118}/melody_v129_p43_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p56/melody_v130_p56_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST, len(s.splitlines()), "lines")
