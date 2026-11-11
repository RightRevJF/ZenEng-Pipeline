"""Writes melody_v114_p40.py: the v114 port (fixes 340-347) on the v113 base (melody_v113_p40.py). 340, 342 and 347 are read in the
report and at intake; 341 and 343-346 change the draw. The new song is built on this file."""
s = open("/home/claude/p45/melody_v113_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)
s = '''"""ZenEng v114 PORT (fixes 340-347; Window 134) on the v113 base, for the new song.
  341 sixteenths are pushes: gaps of a sixteenth (and a dotted eighth) weighted by a knob set on unaimed builds toward the kept 11% of
      gaps; a sixteenth-position onset followed by a sixteenth (a run) weighted down, followed by an eighth or more (a push) weighted up.
  343 four note lengths: each section kind's palette drawn per build, three to five lengths (four at the median) from 288's eight,
      the eighth always among them; a line's gaps and line-end holds drawn from it (dropped, and counted, when no rhythm fits).
  344 notes outside the scale: a build's share drawn from the kept windows (none in half; else a kept nonzero share), placed by the
      walk among the song's sung extra pitch classes, a knob set toward the kept mean of 7.1%.
  345 long notes (a beat or longer) on chord tones: a knob on chord tones for long notes, set toward the kept 72%.
  346 the off-beat eighth (kept 0.37) and distinct pitches in a section (kept 6.4 in eight bars) aimed by knobs; in sections of
      two-bar lines, a line returns the line before it at the kept 17% (unit 2) and line 4 returns line 2 at the kept 19%.
  340/347 the report's (a judge fitted on the kept windows against the run's builds; no measure over half a point); 342 intake's.
Every knob above is set in the calibration on builds drawn as the run draws them (338).
Usage: PYTHONHASHSEED=0 python3 melody_v114_p40.py N main|ctl [tag]
From the v113 port:
''' + s[3:]
R('H113 = "/home/claude/p45"; VAR = MODE', 'H113 = "/home/claude/p45"; H114 = "/home/claude/p45"; VAR = MODE')
R('''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0)''',
  '''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0)         # 341-346 knobs (338: set on unaimed builds)
RUNW, PUSHW = 0.25, 1.5                                                               # 341: a sixteenth-position onset continued by a sixteenth / held an eighth or more
KEPT114 = dict(gap_sixteenth=0.107, chord_tones_on_long_notes=0.716, on_offbeat_eighth=0.371, distinct_pitches=6.38, outside_scale=0.071)
PAL_K = ([3, 4, 5], [0.25, 0.5, 0.25])                                                 # 343: the kept count of note lengths in eight bars (three to five, four at the median)
RATE343 = {3: 0.147, 9: 0.055, 12: 0.204, 18: 0.050, 24: 0.040, 36: 0.031, 48: 0.031}   # 288's class rates for the lengths other than the eighth
PALS = {}; OS_T = [0.0]; SEC_USED = set()
OS_KEPT = [r_["outside_scale"] for r_ in KRW if np.isfinite(r_.get("outside_scale", np.nan)) and r_["outside_scale"] > 0]   # 344''')
# ---- 341 and 343 in the rhythm ----
R('''    def tw(tp, k, d): return M.RT[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)''',
  '''    def tw(tp, k, d):
        w = M.RT[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)
        if d in (3, 9): w *= LK["s16"]                                                     # 341: sixteenth gaps at the kept share
        if tp % 6 == 3: w *= RUNW if d == 3 else PUSHW                                     # 341: a run weighted down, a push up
        return w''')
R('''                    if step <= d <= 24:''', '''                    if step <= d <= 24 and (pal is None or d in pal):                      # 343: the section's palette''')
R('''    def dp(kind_, tgt, cb, sb=None):''', '''    pal = PALS.get(KIND[sec])
    def dp(kind_, tgt, cb, sb=None):''')
R('''        key = (sec, i, tmin, end, tuple(lands))''', '''        key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None)''')
R('''        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1''',
  '''        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1
        if free and pal is not None: pal = None; STATS["343: palette dropped for a line"] += 1''')
R('''def melismas(ons, rng, end):
    rows = []
    for k, t in enumerate(ons):
        rows.append([t, k, False]); nxt = ons[k + 1] if k + 1 < len(ons) else None
        sx = rng.random() < SIXTEENTH / 0.431                                             # a sixteenth split, against the eighth's kept share
        if nxt is None:
            if t + 6 <= end and rng.random() < AIM.mel_final: rows.append([t + (3 if sx else 6), k, True])
        elif nxt - t >= 12 and rng.random() < AIM.mel_inner: rows.append([t + (3 if sx else (nxt - t) // 2 // 6 * 6), k, True])
    return rows''', '''def melismas(ons, rng, end, pal=None):
    rows = []
    ok = lambda *g: pal is None or all(x in pal for x in g)                                # 343: a split's lengths in the palette
    for k, t in enumerate(ons):
        rows.append([t, k, False]); nxt = ons[k + 1] if k + 1 < len(ons) else None
        sx = rng.random() < SIXTEENTH / 0.431 * LK["s16"]                                  # a sixteenth split (a push: held to the next onset), 341's knob
        if nxt is None:
            if t + 6 <= end and rng.random() < AIM.mel_final:
                g = 3 if sx else 6
                if ok(g): rows.append([t + g, k, True])
        elif nxt - t >= 12 and rng.random() < AIM.mel_inner:
            g = 3 if sx else (nxt - t) // 2 // 6 * 6
            if ok(g, nxt - t - g): rows.append([t + g, k, True])
    return rows''')
R('''    se = slot_end(sec, i); rows = melismas(ons, rng, se if last_max is None else min(se, last_max)) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]''',
  '''    se = slot_end(sec, i); rows = melismas(ons, rng, se if last_max is None else min(se, last_max), PALS.get(KIND[sec])) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]''')
R('''                opts = [L_ for L_ in PALETTE if L_ <= max(3, room)] or [3]''',
  '''                pl = PALS.get(KIND.get(n.get("sec"), ""), PALETTE)                                 # 343: the line-end hold from the section's palette
                opts = [L_ for L_ in pl if L_ <= max(3, room)] or [L_ for L_ in PALETTE if L_ <= max(3, room)] or [3]''')
# ---- 345 long notes on chord tones; 344 outside the scale; 346 distinct pitches and the off-beat eighth ----
R('''def chord_w(p, n, ch):
    tones = M.CH[ch][1]; on_beat = n["on"] % BEAT == 0; cw = AIM.cw
    return (cw[0] if p % 12 in tones else cw[1]) if on_beat else (cw[2] if p % 12 in tones else cw[3])''',
  '''def chord_w(p, n, ch):
    tones = M.CH[ch][1]; on_beat = n["on"] % BEAT == 0; cw = AIM.cw
    w = (cw[0] if p % 12 in tones else cw[1]) if on_beat else (cw[2] if p % 12 in tones else cw[3])
    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]                           # 345: a long note on a chord tone
    return w
def extra_w(p):
    """344: a pitch class outside the scale at the build's drawn share; 346: a pitch already sung in the section."""
    w = 1.0
    if p % 12 not in M.SCALE: w *= LK["k44"] * OS_T[0] / KEPT114["outside_scale"]
    if p in SEC_USED: w *= LK["dpk"]
    return w''')
R('''                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf); base += w0''',
  '''                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p)); base += w0''')
R('''        tm = t % BAR
        return w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0)''',
  '''        tm = t % BAR
        return w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (LK["offb"] if t % 12 == 6 else 1.0)   # 346: the off-beat eighth''')
# ---- per build: the palettes (343), the outside share (344); the section's sung pitches (346) ----
R('''    REGS, meta["registers"] = draw_registers(rng)''', '''    REGS, meta["registers"] = draw_registers(rng)
    PALS.clear()
    for k_ in sorted({KIND[s_] for s_ in SUNG}):                                           # 343
        K_ = rng.choices(*PAL_K)[0]; pool = [L_ for L_ in RATE343]; pal = {6}
        while len(pal) < K_ and pool:
            L_ = rng.choices(pool, [RATE343[x] for x in pool])[0]; pal.add(L_); pool.remove(L_)
        PALS[k_] = pal
    OS_T[0] = 0.0 if rng.random() < 0.5 else rng.choice(OS_KEPT)                               # 344
    meta["palettes"] = {k_: sorted(v) for k_, v in PALS.items()}; meta["outside_target"] = OS_T[0]''')
R('''    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]''',
  '''    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]; SEC_USED.clear()''')
R('''            for n in ns: notes_on_all.add(n["on"])
            place(sec, i, ns)''', '''            for n in ns: notes_on_all.add(n["on"]); SEC_USED.add(n["p"])
            place(sec, i, ns)''')
# ---- 346: unit returns in sections of two-bar lines ----
R('''def draw_plan(rng, sec, plans):
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]
    return list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])''',
  '''def draw_plan(rng, sec, plans):
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCDEF"[:len(LINES[sec])], 1.0)]
    pl = list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])
    if len(pl) >= 4 and all(x == 2 for x in slots_of(sec)):                                # 346: a later unit returns an earlier one at the kept rates
        for j, src, rate in ((1, 0, 0.172), (3, 1, 0.188)):
            if pl.index(pl[j]) == j and rng.random() < rate:
                tr = pl[:j] + [pl[src]] + pl[j + 1:]
                if admissible(sec, "".join(tr)): pl = tr; STATS[f"346: line {j + 1} returns line {src + 1}"] += 1
    return pl''')
# ---- the calibration: 341, 344-346 knobs on unaimed builds (338) ----
R('''        if "Verse 2" in SUNG:                                                               # 338: verse 2's share read on builds drawn as the run draws them
            k2 = 0; t2 = 0
            while k2 < n and t2 < 40 * n:
                t2 += 1; c2, e2 = generate(rng)
                if e2: continue
                k2 += 1; v2_acc.append(v2_share(c2["notes"]))
            row["338: unaimed builds read"] = k2''',
  '''        k2 = 0; t2 = 0; ua = collections.defaultdict(list)                                  # 338: builds drawn as the run draws them
        while k2 < n and t2 < 40 * n:
            t2 += 1; c2, e2 = generate(rng)
            if e2: continue
            k2 += 1
            if "Verse 2" in SUNG: v2_acc.append(v2_share(c2["notes"]))
            for s_ in ("Verse 1", "Chorus 1"):
                f_ = win_feats(c2["notes"], BAR0[s_])
                for m_ in KEPT114:
                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])
        row["338: unaimed builds read"] = k2
        if ua:                                                                              # 341, 344-346: each knob toward its kept figure
            rd = {m_: (float(np.mean(ua[m_])) if ua.get(m_) else KEPT114[m_]) for m_ in KEPT114}
            LK["s16"] = float(np.clip(LK["s16"] * np.clip(KEPT114["gap_sixteenth"] / max(0.01, rd["gap_sixteenth"]), 0.5, 1.6), 0.05, 3.0))
            LK["ctl"] = float(np.clip(LK["ctl"] * np.clip((KEPT114["chord_tones_on_long_notes"] / max(0.05, rd["chord_tones_on_long_notes"])) ** 2, 0.6, 2.0), 0.5, 8.0))
            LK["offb"] = float(np.clip(LK["offb"] * np.clip(KEPT114["on_offbeat_eighth"] / max(0.05, rd["on_offbeat_eighth"]), 0.6, 1.6), 0.3, 3.0))
            LK["dpk"] = float(np.clip(LK["dpk"] * np.clip((rd["distinct_pitches"] / KEPT114["distinct_pitches"]) ** 2, 0.6, 2.0), 0.5, 8.0))
            LK["k44"] = float(np.clip(LK["k44"] * np.clip(KEPT114["outside_scale"] / max(0.005, rd["outside_scale"]), 0.5, 2.0), 0.01, 30.0))
            row["341-346 (kept, unaimed reading, knob)"] = {m_: (KEPT114[m_], round(rd[m_], 3)) for m_ in KEPT114} | {"knobs": {k_: round(LK[k_], 3) for k_ in ("s16", "ctl", "offb", "dpk", "k44")}}''')
R('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v113_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v114_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
R('''                open(f"{H113}/melody_v113_p40_{MODE}{_TAG}.pkl", "wb"))''', '''                open(f"{H114}/melody_v114_p40_{MODE}{_TAG}.pkl", "wb"))''')
open("/home/claude/p45/melody_v114_p40.py", "w").write(s)
print("written")
