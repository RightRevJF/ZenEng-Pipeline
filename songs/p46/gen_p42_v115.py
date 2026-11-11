"""Writes melody_v115_p42.py: song 42, Nothing Important, again on the v115 port (melody_v115_p40.py): the same song constants, lyric,
intake and seed as songs/p42/gen_p42.py, and 325's design condition on the registers and the hook."""
s = open("/home/claude/p46/melody_v115_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
s = '''"""ZenEng v115 -- song 42, Nothing Important, run again on the v115 port (fixes 348-354 in force; findings from 355).
A piano ballad at q = 76 in B-flat major for a warm alto (row F3-D5); 68 bars. No era, character, summit or lift chosen; the song's range
centred in the row (314, Q8 A); the bridge drawn as kept songs do (Q15 A). Designs in force, named:
  Q13 A  every line two bars (230 failed by a named design choice).
  Q11 note 4  the last chorus: 'Hey, it's me' is the hook's head; 'Nothing important' is the hook's tail held longer (its rhythm
         augmented); 'I'll call you back' is 'Call me back' returned and falling to the tonic. A design gate (317), its pass rate printed.
  Q14 A  the cello's countermelody (arrangement; no melody gate).
Usage: PYTHONHASHSEED=0 python3 melody_v115_p42.py N main|ctl [tag]
The v115 port it is built on:
''' + s[3:]
R('sys.path[:0] = ["/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]',
  'sys.path[:0] = ["/home/claude/p42", "/home/claude/p40", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]')
R('import lyric_p40 as L', '''import lyricsearch; lyricsearch.OVERRIDE["blinker"] = ("B L IH1 NG K ER0",)          # not in the pronouncing dictionary
import lyric_p42 as L''')
a = s.index("M.TONIC = 2;"); b = s.index("STOP_BARS = set()")
s = s[:a] + '''M.TONIC = 10; M.SCALE = {10, 0, 2, 3, 5, 7, 9}; M.SUNGPC = M.SCALE | {1, 8}            # flat 3 (D-flat) and flat 7 (A-flat), as 200 allows
M.CH = {"Bb": (10, {10, 2, 5}), "Eb": (3, {3, 7, 10}), "F": (5, {5, 9, 0}), "Gm": (7, {7, 10, 2}), "Cm": (0, {0, 3, 7}), "Dm": (2, {2, 5, 9})}
M.ROMAN = {"Bb": "I", "Eb": "IV", "F": "V", "Gm": "vi", "Cm": "ii", "Dm": "iii"}
M.QBPM = 76; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 53; TOP = 74; M.SUMMIT = TOP     # the voice row F3-D5 (Q7); no designed summit
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
FEEL = "straight eighths, q = 76"
PLAN = {"Intro": ["Bb", "Dm", "Eb", "F"], "Verse": ["Bb", "Dm", "Eb", "Bb", "Gm", "Eb", "Cm", "F"], "Chorus": ["Eb", "F", "Gm", "Eb", "Cm", "F", "Bb", "Bb"],
        "Bridge": ["Gm", "Dm", "Eb", "Bb", "Gm", "Dm", "Cm", "F"], "LastChorus": ["Eb", "F", "Gm", "Eb", "Cm", "F", "Gm", "Eb", "Cm", "F", "Bb", "Bb"],
        "Outro": ["Eb", "Bb", "Eb", "Bb"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Chorus 1", "Chorus", 8), ("Verse 2", "Verse", 8), ("Chorus 2", "Chorus", 8),
        ("Bridge", "Bridge", 8), ("Verse 3", "Verse", 8), ("Last Chorus", "Chorus", 12), ("Outro", "Outro", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else kind]; b += nb
NBARS = b; assert NBARS == 68 and len(CHORD) == NBARS
''' + s[b:]
R('SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"]',
  'SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Verse 3", "Last Chorus"]')
R('SLOTS = {"Verse": [2, 1, 3, 3, 2, 1], "Pre": [2, 2], "Chorus": [2] * 8, "Bridge": [2, 1, 1, 2, 1, 1], "Last Chorus": [2] * 9}',
  'SLOTS = {"Verse": [2] * 4, "Chorus": [2] * 4, "Bridge": [2] * 4, "Last Chorus": [2] * 6}                # Q13 A: every line two bars')
R('PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Pre": ["Pre 1", "Pre 2"], "Bridge": ["Bridge"]}', 'PAIRS = {"Verse": ["Verse 1", "Verse 2", "Verse 3"], "Bridge": ["Bridge"]}')
R('SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}', 'SRC = {"Verse 2": "Verse 1", "Verse 3": "Verse 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}')
R('''    R = {"Verse": (V_MU, V_CAP, V_FLOOR), "Chorus": (c_mu, c_cap, c_floor), "Pre": ((V_MU + c_mu) / 2, max(V_CAP, c_cap), V_FLOOR),''',
  '''    R = {"Verse": (V_MU, V_CAP, V_FLOOR), "Chorus": (c_mu, c_cap, c_floor),''')
R('TRIAD = {2, 6, 9}', 'TRIAD = {10, 2, 5}')
R('''    if sec == "Chorus 1" and i == 0: return (p - M.TONIC) % 12 == 0                       # the hook ends where the last chorus ends (its tag): the tonic
    if i != len(LINES[sec]) - 1: return True''', '''    if i != len(LINES[sec]) - 1: return True
    if sec == "Last Chorus": return (p - M.TONIC) % 12 == 0                               # Q11 note 4: 'I'll call you back' falls to the tonic''')
R('''    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS), Pre=draw_plan(rng, "Pre 1", PRE_PLANS),''',
  '''    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS),''')
a = s.index('''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)'''); b = s.index('''        plan = plans[kind]; first = plan.index(plan[i])''')
s = s[:a] + '''        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus":
            if i < 3: return ("copy", "Chorus 1", i)
            if i == 3: return ("head", "Chorus 1", 0)                                      # 'Hey, it's me.': the hook's first three syllables
            if i == 4: return ("aug", "Chorus 1", 0)                                       # 'Nothing important.': the hook's tail, held longer (Q11 note 4)
            return ("return", "Chorus 1", 3)                                               # 'I'll call you back.' on 'Call me back.', falling home
        if sec in ("Verse 2", "Verse 3"): return ("again", SRC[sec], i)
        if kind == "Chorus":
            if i == 2: return ("return", sec, 0)                                           # 213 (Q10 A): 'hey, it's me' said again, the line returning
            return ("fresh", None, None)
''' + s[b:]
R('''        rule = (sec, i) == ("Chorus 1", 0) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''',
  '''        rule = (sec, i) == ("Last Chorus", 5) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''')
R('("copy", "return", "plan", "tail")', '("copy", "return", "plan", "tail", "head", "aug")', n=3)
R('''            elif h == "tail":
                k0 = len(LINES[s0][i0]) - len(LINES[sec][i])
                r = ("ns", [dict(n, on=n["on"] - SU + U, syl=n["syl"] - k0) for n in S if n["syl"] >= k0], "exact")''',
  '''            elif h == "tail":
                k0 = len(LINES[s0][i0]) - len(LINES[sec][i])
                r = ("ns", [dict(n, on=n["on"] - SU + U, syl=n["syl"] - k0) for n in S if n["syl"] >= k0], "exact")
            elif h == "head":
                r = ("ns", [dict(n, on=n["on"] - SU + U) for n in S if n["syl"] < len(LINES[sec][i])], "exact")
            elif h == "aug":                                                                 # Q11 note 4: the tail augmented, at the hook's own entry
                k0 = len(LINES[s0][i0]) - len(LINES[sec][i]); T = [n for n in S if n["syl"] >= k0]; t0 = T[0]["on"]; toff = S[0]["on"] - SU
                for fac in (2.0, 1.5, 1.0):
                    ns_ = [dict(n, on=U + toff + int(round(fac * (n["on"] - t0) / 6)) * 6, syl=n["syl"] - k0) for n in T]
                    if ns_[-1]["on"] - U <= slot_end(sec, i) and len({x["on"] for x in ns_}) == len(ns_): break
                if fac < 2.0: STATS[f"design: tail augmented by {fac} only"] += 1
                r = ("ns", ns_, "exact")''')
R('''DESIGN_GATES = []                                                                     # the default path: none in force''',
  '''DESIGN_GATES = ["design: 'Nothing important' held longer than in the hook; 'I'll call you back' falls to the tonic, under it (Q11 note 4)"]
def design_fails(c):
    """317: the writer's design, read on what is sung; outside 275, its pass rate printed."""
    notes = c["notes"]; f = {}
    h = [n for n in notes if n["line"] == "Chorus 1:0"]; k0 = len(LINES["Chorus 1"][0]) - len(LINES["Last Chorus"][4])
    tail = [n for n in h if n["syl"] >= k0]; a4 = [n for n in notes if n["line"] == "Last Chorus:4"]; a5 = [n for n in notes if n["line"] == "Last Chorus:5"]
    if not (tail and a4 and a5): f[DESIGN_GATES[0]] = "missing"; return f
    span = lambda ns: ns[-1]["on"] + ns[-1]["dur"] - ns[0]["on"]
    if not (span(a4) >= 1.5 * span(tail) and (a5[-1]["p"] - M.TONIC) % 12 == 0 and a5[-1]["p"] < a4[-1]["p"]): f[DESIGN_GATES[0]] = (span(a4), span(tail), a5[-1]["p"], a4[-1]["p"])
    return f''')
R('''    f = gate_fails(c, c.get("judge"))
    for g in GATES:''', '''    f = gate_fails(c, c.get("judge")); f.update(design_fails(c))
    for g in DESIGN_GATES + GATES:''')
R('''        fails = gate_fails(c, c["judge"]); info = c["info"]''', '''        fails = gate_fails(c, c["judge"]); fails.update(design_fails(c)); info = c["info"]''')
R('''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in list(GATES) + sorted(k for k in would if k not in GATES)]''',
  '''print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in DESIGN_GATES + list(GATES) + sorted(k for k in would if k not in GATES and k not in DESIGN_GATES)]''')
R('N = _N; SEED = 20261110 + 401', 'N = _N; SEED = 20261110 + 442')
R('open(f"{HERE}/lyric_p40.py", "rb").read()', 'open(f"{H110}/lyric_p42.py", "rb").read()')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_v115_p40.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_v115_p42.py {N} {MODE}"')
R('open(f"{H115}/melody_v115_p40_{MODE}{_TAG}.pkl", "wb"))', 'open(f"{H115}/melody_v115_p42_{MODE}{_TAG}.pkl", "wb"))')
open("/home/claude/p46/melody_v115_p42.py", "w").write(s)
print("written")
s = open("/home/claude/p46/melody_v115_p42.py").read()
R('''    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''',
  '''    plans = [(p[:len(LINES[sec])], w) for p, w in plans]                                  # four-line sections: each plan cut to its first four lines
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]''')
open("/home/claude/p46/melody_v115_p42.py", "w").write(s)
print("patched")
s = open("/home/claude/p46/melody_v115_p42.py").read()
R('''                for fac in (2.0, 1.5, 1.0):
                    ns_ = [dict(n, on=U + toff + int(round(fac * (n["on"] - t0) / 6)) * 6, syl=n["syl"] - k0) for n in T]
                    if ns_[-1]["on"] - U <= slot_end(sec, i) and len({x["on"] for x in ns_}) == len(ns_): break''',
  '''                done = False
                for fac in (2.0, 1.5, 1.0):
                    for to in (toff, -12, -6, 0):
                        ns_ = [dict(n, on=U + to + int(round(fac * (n["on"] - t0) / 6)) * 6, syl=n["syl"] - k0) for n in T]
                        if ns_[-1]["on"] - U <= slot_end(sec, i) and len({x["on"] for x in ns_}) == len(ns_): done = True; break
                    if done: break''')
R('''        return (lambda p: end_ok(sec, i, p)) if rule else None''',
  '''        if (sec, i) == ("Last Chorus", 5) and ("Chorus 1", 0) in built:                    # Q11 note 4: home, under 'nothing important'
            hl = built[("Chorus 1", 0)][-1]["p"]; return lambda p: end_ok(sec, i, p) and p < hl
        return (lambda p: end_ok(sec, i, p)) if rule else None''')
R('''    span = lambda ns: ns[-1]["on"] + ns[-1]["dur"] - ns[0]["on"]''', '''    span = lambda ns: ns[-1]["on"] - ns[0]["on"]                                          # onset to onset: the augmentation''')
open("/home/claude/p46/melody_v115_p42.py", "w").write(s)
print("patched 2")
s = open("/home/claude/p46/melody_v115_p42.py").read()
R('''            return ("return", "Chorus 1", 3)                                               # 'I'll call you back.' on 'Call me back.', falling home''',
  '''            return ("fresh", None, None)                                                   # 'I'll call you back.': drawn, falling home under 'nothing important\'''')
R('''    if sec == "Last Chorus": return (p - M.TONIC) % 12 == 0                               # Q11 note 4: 'I'll call you back' falls to the tonic''',
  '''    if sec == "Last Chorus": return (p - M.TONIC) % 12 == 0 and p < HOOK_LAST[0]         # Q11 note 4: 'I'll call you back' falls to the tonic, under the hook's end''')
R('''TRIAD = {10, 2, 5}''', '''TRIAD = {10, 2, 5}
HOOK_LAST = [999]                                                                     # the hook's last pitch, set as it is placed''')
R('''        built[(sec, i)] = ns; lines.append(ns)''', '''        built[(sec, i)] = ns; lines.append(ns)
        if (sec, i) == ("Chorus 1", 0): HOOK_LAST[0] = ns[-1]["p"]''')
R('''        if (sec, i) == ("Last Chorus", 5) and ("Chorus 1", 0) in built:                    # Q11 note 4: home, under 'nothing important'
            hl = built[("Chorus 1", 0)][-1]["p"]; return lambda p: end_ok(sec, i, p) and p < hl
''', '')
open("/home/claude/p46/melody_v115_p42.py", "w").write(s)
print("patched 3")
s = open("/home/claude/p46/melody_v115_p42.py").read()
R('''                meta["free"][sec] += len(ns)''', '''                meta["free"][sec] += len(ns)
                lo_keep = lo
                if (sec, i) == ("Last Chorus", 5): lo = meta["registers"]["song_lo"]                 # Q11 note 4: the last line may fall below the chorus's register''')
R('''                meta["kinds"][(sec, i)] = "fresh"''', '''                meta["kinds"][(sec, i)] = "fresh"; lo = lo_keep''')
open("/home/claude/p46/melody_v115_p42.py", "w").write(s)
print("patched 4")
s = open("/home/claude/p46/melody_v115_p42.py").read()
# 325: the design's condition read when the registers are drawn: a tonic under the hook's end must exist in the last line's reach
R('''DESIGN_REG = []                                                                       # 325: (name, test on the drawn registers); none on the default path''',
  '''DESIGN_REG = []                                                                       # 325: (name, test on the drawn registers)
def _lowest_tonic(lo): return min(p for p in range(lo, lo + 12) if (p - M.TONIC) % 12 == 0)
def _design_reg(R_, info):
    """Q11 note 4: the last line's tonic (at or above the song's floor) lies under some note the chorus register can end the hook on."""
    t = _lowest_tonic(info["song_lo"]); mu, cap, fl = R_["Chorus"]
    return t <= cap and any(p % 12 in M.SCALE for p in range(max(fl, t + 1), int(cap) + 1))
DESIGN_REG.append(("the last line's tonic under the hook's end (Q11 note 4)", _design_reg))''')
# 325: where a design needs a tonic under the hook's end, the hook's ending is drawn above the song's lowest tonic
R('''        rule = (sec, i) == ("Last Chorus", 5) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''',
  '''        rule = (sec, i) in (("Last Chorus", 5), ("Chorus 1", 0)) or (sec in ("Verse 1", "Chorus 1") and i == len(LINES[sec]) - 1)''')
R('''    if i != len(LINES[sec]) - 1: return True
    if sec == "Last Chorus":''', '''    if (sec, i) == ("Chorus 1", 0): return p > HOOK_FLOOR[0]                           # 325: the hook ends above the song's lowest tonic
    if i != len(LINES[sec]) - 1: return True
    if sec == "Last Chorus":''')
R('''HOOK_LAST = [999]                                                                     # the hook's last pitch, set as it is placed''',
  '''HOOK_LAST = [999]                                                                     # the hook's last pitch, set as it is placed
HOOK_FLOOR = [-1]                                                                     # 325: the song's lowest tonic, set per build''')
R('''    meta["tonic_endings"] = []''', '''    meta["tonic_endings"] = []; HOOK_FLOOR[0] = _lowest_tonic(meta["registers"]["song_lo"])''')
open("/home/claude/p46/melody_v115_p42.py", "w").write(s)
print("patched 325")
