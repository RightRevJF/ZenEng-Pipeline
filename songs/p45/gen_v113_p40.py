"""Writes melody_v113_p40.py: the v113 port (fix 338; 337 is the report's) from the tested v112 port (songs/p44/melody_v112_p40.py).
This is the base the new song is built on (339: the debugging is closed)."""
s = open("/home/claude/p44/melody_v112_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)
s = '''"""ZenEng v113 PORT (fixes 337-339): the base for the new song.
  338 verse 2's rate (293, 331) is set on unaimed builds: each calibration round draws its own builds as the main run draws them
      (targets drawn, not set at the pools' medians) and reads verse 2's share there; copies given up printed.
  337 a count read with its spread (the report's); 339 the debugging closed.
Usage: PYTHONHASHSEED=0 python3 melody_v113_p40.py N main|ctl [tag]
From the v112 port:
''' + s[3:]
R('H112 = "/home/claude/p44"; VAR = MODE', 'H112 = "/home/claude/p44"; H113 = "/home/claude/p45"; VAR = MODE')
R('''            k += 1
            if "Verse 2" in SUNG: v2_acc.append(v2_share(c["notes"]))
            if NEW: lines_acc.append(line_readings(c["notes"]))''', '''            k += 1
            if NEW: lines_acc.append(line_readings(c["notes"]))''')
R('''        row = {}
        if v2_acc:''', '''        row = {}
        if "Verse 2" in SUNG:                                                               # 338: verse 2's share read on builds drawn as the run draws them
            k2 = 0; t2 = 0
            while k2 < n and t2 < 40 * n:
                t2 += 1; c2, e2 = generate(rng)
                if e2: continue
                k2 += 1; v2_acc.append(v2_share(c2["notes"]))
            row["338: unaimed builds read"] = k2
        if v2_acc:''')
R('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v112_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v113_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
R('''                open(f"{H112}/melody_v112_p40_{MODE}{_TAG}.pkl", "wb"))''', '''                open(f"{H113}/melody_v113_p40_{MODE}{_TAG}.pkl", "wb"))''')
open("/home/claude/p45/melody_v113_p40.py", "w").write(s)
print("written")
