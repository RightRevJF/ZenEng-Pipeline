"""Writes melody_v118_p40.py: v117's and v118's fixes 365-383 (27.61, 27.62) on the v116 port (songs/p47/melody_v116_p40.py), without
editing the paper. Fixes 377 and 380 are song designs (songs 44 and 45 carry their lifts); 379 is an arrangement rule (in force in song 45's
build and its consistency checks); 383 is the report's; 364 and 374 are read by sep_v118.py."""
s = open("/home/claude/p47/melody_v116_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)
s = '''"""ZenEng v118 PORT (fixes 365-383; Windows 137 and 138, 27.61 and 27.62) on the v116 port. Songs 40, 42, 43, 44 and 45 run again on it,
same lyrics, intakes, designs and seeds; song 43 twice more with fix 358 off and with fix 361 off (368's diagnostic runs).
  365 one calibration a measure: 249's gap knobs (gap16, gap8, gap4) leave its aimed calibration and stay at one; the gaps are set once,
      by the 354 knobs on unaimed builds.
  366 a share is set by a draw: each drawn line is drawn as one that may run sixteenths or may not, at a rate set on unaimed builds
      toward the kept 31% in runs; a line that may not is placed with no run, and falls back to runs only when nothing fits (counted).
  367 356's stop read against the rhythm band's kept quartiles, read with the table in use (372): 1.93 and 2.74 bits a note (the pooled
      kept table on 105 kept songs; 2.20 and 2.94 with the v88 table).
  368 the report's: song 43 run with 358 off and with 361 off; memory read with 373's limit.
  369 the kept windows' songs and modes on file (zeneng_v117_kept_songs_and_modes.json): 359 ported as written (the report's readings
      and costs for a minor song against the 70 kept minor windows; the judge of record kept); 364 read on the true songs.
  370 a failed bar is fitted within one onset: the copy's onsets, then the copy with its weakest onset dropped, then with one onset
      added at the bar's weakest free place, each strict; the bar kept when it comes within one onset of the copy.
  371 unit returns on the bar grid in every section of eight bars or more, at rates set on unaimed builds toward the kept readings
      (unit 2 returns unit 1 17.2%, unit 3 returns unit 1 31.5%, unit 4 returns unit 2 18.8%); 346/350's line-plan returns retired; a
      drawn unit return takes the bars it covers from 310's pairing.
  372 the rhythm table is the kept songs': an onset's gap to the next drawn from zeneng_v117_kept_rhythm_tables.json, the table for the
      band of the section's notes a bar (its syllables over its bars), in place of the v88 pop table; the melisma's sixteenth split at
      the band's kept share. The knobs of 354, 355, 365 and 366 start at one; a knob ending more than a factor of two from one is reported.
  373 limits read on the kept songs: the rhythm band read with the pooled kept table, soft 1.62-3.38, hard 1.43-3.61; memory soft 0.12,
      no hard limit; cmp unchanged.
  374 the report's (the yardstick, 0.57 and 0.63).
  375 a chord's own tones outside the scale are chord tones for its bar; a sung note a semitone from one clashes; 349's target read on
      the notes whose chord allows an outside pitch class.
  376 the frozen knob's message reads the round counter.
  377, 380 song designs (songs 44 and 45). 378 a line fills its slot: where the next line is in the same section, the line's span
      (first onset to the end of its last note, over the time to the next line's first onset) is drawn first inside the kept middle
      half for its notes (43-75% for up to five, 53-80% for six to eight, 66-88% for nine to twelve, 78-94% for more; Window 138) and the
      rhythm fills it; given up only when nothing fits (counted).
  379 an arrangement rule. 381 358's passing notes taken from the song's sung extra pitch classes. 382 surprisal soft 0.24, hard 0.08.
  383 the report's.
Usage: PYTHONHASHSEED=0 python3 melody_v118_p40.py N main|ctl [tag]
The v116 port it is built on:
''' + s[3:]
R('H116 = "/home/claude/p47"; VAR', 'H116 = "/home/claude/p47"; H118 = "/home/claude/p50"; VAR')
R('''L286 = json.load(open(f"{HERE}/limits286.json"))["limits"]''', '''L286 = json.load(open(f"{HERE}/limits286.json"))["limits"]
KT = json.load(open(f"{H118}/tables/zeneng_v117_kept_rhythm_tables.json"))                  # 372
SS118 = json.load(open(f"{H118}/tables/zeneng_v118_slot_and_surprisal.json"))                # 378, 382
YS117 = json.load(open(f"{H118}/tables/zeneng_v117_yardstick.json"))                         # 373, 374''')
# ---- 365: 249's gap knobs leave the aimed calibration ----
R('''             "beat3": "on_beat3", "beats24": "on_beats_2_4", "gap8": "gap_eighth", "gap4": "gap_quarter", "gap16": "gap_sixteenth"}''',
  '''             "beat3": "on_beat3", "beats24": "on_beats_2_4"}                                    # 365: gap8, gap4 and gap16 leave 249's aimed calibration (they stay at one)''')
# ---- 366 and 371: the run rate and the unit-return rates; 372: the knobs at one ----
R('''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=0.01, on16=1.0)   # 355: run, on16 (the run knob starts low: a run is taken wherever it is allowed)''',
  '''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=1.0, on16=1.0)   # 366: run is the rate at which a line may run; 372: every gap knob starts at one
GAPKNOBS = ("s16", "g8", "g4", "glong", "run", "on16")                                     # 372: the knobs of 354, 355, 365 and 366 (reported if they end more than a factor of two from one)
UR_KEPT = {1: (0, 0.172, "unit2_returns"), 2: (0, 0.315, "unit3_returns"), 3: (1, 0.188, "unit4_to_unit2")}   # 371: the kept readings
UR_RATE = {j: v[1] for j, v in UR_KEPT.items()}                                             # 371: drawn at rates set on unaimed builds (they start at the kept readings)
# ---- 372: the kept rhythm tables, by the band of the section's notes a bar, on the twelfth grid ----
KBANDS = [("under 3.5", 0, 3.5), ("3.5 to 4.5", 3.5, 4.5), ("4.5 to 5.5", 4.5, 5.5), ("5.5 and over", 5.5, 99)]
def kband(npb): return next(b for b, lo_, hi_ in KBANDS if lo_ <= npb < hi_)
def _rt12(tab):
    out = [[0.0] * 97 for _ in range(48)]
    for p16 in range(16):
        for g in range(1, 33): out[3 * p16][3 * g] = float(tab[p16][g])
    return out
KRT = {b: _rt12(KT["tables"][b]) for b in list(KT["tables"])}
KSH = KT["gap shares (sixteenth, eighth, quarter, longer than a quarter)"]
SEC_NPB = {}; SEC_BAND = {}
SH16_NOW = [float(KSH["all"][0])]                                                         # the melisma's sixteenth split: the band's kept share
for _s in SUNG:
    SEC_NPB[_s] = len([x for l_ in LINES[_s] for x in l_]) / SECLEN[_s]; SEC_BAND[_s] = kband(SEC_NPB[_s])''')
R('''def du_target(npb): return next(t for lo, hi, t in DU if lo <= npb < hi)         # 341-346 knobs (338: set on unaimed builds)''',
  '''def du_target(npb): return tuple(KSH[kband(npb)])                                    # 372 (with 365): the four gaps toward the kept table's shares for the density''')
R('''              rhythm_bits=(2.2541 - 0.6732 * 0.674 / 1.645, 2.2541 + 0.6732 * 0.674 / 1.645))     # 356: the rhythm band's middle half, from 286's soft limits''',
  '''              rhythm_bits=(1.934, 2.735))                                                       # 367 with 372: the kept quartiles read with the pooled kept table''')
# ---- 372: the rhythm band read with the pooled kept table ----
R('''# ---- 225/226/243: targets are one whole kept window ----''', '''def rhythm_bits_kept(notes):
    """372/373: the rhythm band, bits a note, read with the pooled kept table."""
    ons = [n["on"] for n in notes] + [NBARS * BAR]; out = []
    T_ = KRT["all"]
    for a, b2 in zip(ons, ons[1:]):
        d = min(96, b2 - a); d -= d % 3
        out.append(-math.log2(max(1e-9, T_[a % BAR - a % 3][d])))
    return float(np.mean(out))
M.rhythm_bits = rhythm_bits_kept
# ---- 375: a chord's own tones outside the scale are chord tones; a sung note a semitone from one clashes ----
_clash200 = M.clash
def clash375(p, ch):
    if _clash200(p, ch): return True
    if "375" in OFF: return False
    out = [t for t in M.CH[ch][1] if t not in M.SCALE]
    return any((p - t) % 12 in (1, 11) for t in out) and p % 12 not in M.CH[ch][1]
M.clash = clash375
# ---- 225/226/243: targets are one whole kept window ----''')
# ---- 372 and 366 in a line's rhythm ----
R('''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False):
    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)''',
  '''SPAN_TO = [None]; SPAN_E = [None]
SPAN_MID = [(5, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["3 to 5"]),
            (8, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["6 to 8"]),
            (12, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["9 to 12"]),
            (999, SS118["378 kept lines: the share of the time to the next line that a line sings (first onset to the end of its last note)"]["by note count"]["13 to 24"])]
def span_mid(n): return next((q[1], q[3]) for k_, q in SPAN_MID if n <= k_)                # 378: the kept middle half for a line's notes
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False, span_to=None):
    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)
    RTS = KRT[SEC_BAND[sec]] if "372" not in OFF else M.RT; SH16_NOW[0] = float(KSH[SEC_BAND[sec]][0]) if "372" not in OFF else SIXTEENTH   # 372
    SPAN_E[0] = None''')
R('''    runs_ok = len([t for t in G if t % 6 == 0 and (t >= 0 or not st[0])]) < n               # 348 (Q1 A): no room on the eighth grid: runs allowed
    if runs_ok: STATS["348: a drawn line with no room on the eighth grid (runs allowed)"] += 1''',
  '''    runs_ok = len([t for t in G if t % 6 == 0 and (t >= 0 or not st[0])]) < n               # 348 (Q1 A): no room on the eighth grid: runs allowed
    if runs_ok: STATS["348: a drawn line with no room on the eighth grid (runs allowed)"] += 1
    may_run = [runs_ok or "366" in OFF or rng.random() < LK["run"]]                          # 366: a line may run sixteenths, drawn at a rate
    STATS["366: lines drawn that may run" if may_run[0] else "366: lines drawn that may not run"] += 1
    sp = span_mid(n) if (span_to is not None and not fix) else None                          # 378: the span drawn first
    s_span = rng.uniform(*sp) if sp else None''')
R('''        w = M.RT[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)''', '''        w = RTS[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)                               # 372: the kept table for the section's band''')
R('''        if tp % 6 == 3 and d < 6 and not runs_ok and "348" not in OFF: w *= LK["run"]        # 355 (amends 348): a run at the kept rate, the rest pushes''',
  '''        if tp % 6 == 3 and d < 6 and not may_run[0] and "348" not in OFF: w = 0.0               # 366 (amends 355): a line that may not run is placed with no run''')
R('''        key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None)''',
  '''        key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None, may_run[0])''')
R('''        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1''',
  '''        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1
        if _try == NT and not may_run[0]: may_run[0] = True; STATS["366: fallback to runs (nothing fitted without)"] += 1
        if _try == NT and s_span is not None: s_span = None; STATS["378: span given up (nothing fitted inside it)"] += 1''')
R('''        if Ls in fix: tgt = fix[Ls]
        elif free: tgt = rng.choice(list(range(max(0, tmin + step * Ls), end - step * post + 1, step)) or [end])
        elif fits is not None: tgt = land_draw(rng, sec, n, i, allowed={t for k_, t in fits if k_ == kind_})
        else: tgt = land_draw(rng, sec, n, i)''',
  '''        spa = None
        if s_span is not None and not free:                                                   # 378: the landing inside the drawn span
            f0g = {"on": 0, "after": 12, "pickup": -6}.get(kind_, max(0, tmin))
            E0 = f0g + s_span * (span_to - f0g)
            spa = {t for t in range(-12, end + 1, 3) if E0 - 48 <= t <= E0 - 3 * (post + 1)}
        if Ls in fix: tgt = fix[Ls]
        elif free: tgt = rng.choice(list(range(max(0, tmin + step * Ls), end - step * post + 1, step)) or [end])
        elif fits is not None:
            al_ = {t for k_, t in fits if k_ == kind_}
            if spa is not None and al_ & spa: al_ = al_ & spa
            tgt = land_draw(rng, sec, n, i, allowed=al_)
        else: tgt = land_draw(rng, sec, n, i, allowed=spa if spa else None)''')
R('''        ons = sample(alpha)
        if ons is None: continue''', '''        ons = sample(alpha)
        if ons is None: continue
        if s_span is not None and not free:                                                   # 378: the line ends inside its drawn span
            E = ons[0] + s_span * (span_to - ons[0])
            if not (ons[-1] + 3 <= E <= ons[-1] + 48): STATS["378: rhythm outside its span, redrawn"] += 1; continue
            SPAN_E[0] = E''')
# ---- 370: a failed bar fitted within one onset ----
R('''            if bad and "360" not in OFF:                                                   # 360: the failed bars fitted again, the copy's onsets required there
                a2, _ = dp(kind_, tgt, cb, sb, strict=set(bad))
                o2 = sample(a2) if a2[n - 1] else None
                if o2 is not None and len(badf(o2)) < len(bad):
                    STATS["360: bars fitted again and kept"] += len(bad) - len(badf(o2)); ons = o2; bad = badf(o2)
                else: STATS["360: bars fitted again without success"] += len(bad)''',
  '''            if bad and "360" not in OFF:                                                   # 360 with 370: the failed bars fitted again within one onset
                def _drop(ts_): wk = min(ts_, key=lambda t: (M.mw(t), -t)); return [t for t in ts_ if t != wk] if len(ts_) > 1 else list(ts_)
                def _add(bb, ts_):
                    fr = [t for t in range(bb * BAR, (bb + 1) * BAR, 6) if t not in ts_ and tmin <= t <= end]
                    return sorted(ts_ + [min(fr, key=lambda t: (M.mw(t), -t))]) if fr else list(ts_)
                variants = [cb, {bb: (_drop(ts) if bb in bad else ts) for bb, ts in cb.items()}, {bb: (_add(bb, ts) if bb in bad else ts) for bb, ts in cb.items()}]
                kept_ = False
                for vi, cbv in enumerate(variants if "370" not in OFF else variants[:1]):
                    a2, _ = dp(kind_, tgt, cbv, sb, strict=set(bad))
                    o2 = sample(a2) if a2[n - 1] else None
                    if o2 is not None and len(badf(o2)) < len(bad):
                        STATS["360: bars fitted again and kept"] += len(bad) - len(badf(o2)); STATS[f"370: kept by variant {('copy', 'one dropped', 'one added')[vi]}"] += len(bad) - len(badf(o2))
                        ons = o2; bad = badf(o2); kept_ = True; break
                if not kept_: STATS["360: bars fitted again without success"] += len(bad)''')
# ---- 372: the melisma's sixteenth split at the band's kept share ----
R('''        sx = rng.random() < SIXTEENTH / 0.431 * LK["s16"]                                  # a sixteenth split (a push: held to the next onset), 341's knob''',
  '''        sx = rng.random() < SH16_NOW[0] / 0.431 * LK["s16"]                                # a sixteenth split at the band's kept share (372), 341's knob''')
# ---- 378 in a fresh line ----
R('''    if not kw and unitbars: kw = dict(copybars=unitbars, allbars=True)                    # 361: the returning unit's onsets, bar by bar
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, **kw)
    if ons is None: return None
    se = slot_end(sec, i); rows = melismas(ons, rng, se if last_max is None else min(se, last_max), PALS.get(KIND[sec])) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]
    return [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]''',
  '''    if not kw and unitbars: kw = dict(copybars=unitbars, allbars=True)                    # 361: the returning unit's onsets, bar by bar
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, span_to=SPAN_TO[0], **kw)
    if ons is None: return None
    E_ = SPAN_E[0]
    se = slot_end(sec, i); me_ = se if last_max is None else min(se, last_max)
    if E_ is not None: me_ = min(me_, int(E_) - 3)                                          # 378: a final melisma inside the span
    rows = melismas(ons, rng, me_, PALS.get(KIND[sec])) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]
    ns_ = [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]
    if E_ is not None and U + E_ - ns_[-1]["on"] >= 3:                                       # 378: the last note held to the span's end
        ns_[-1]["hold"] = int(U + E_ - ns_[-1]["on"]); STATS["378: lines drawn to a span"] += 1
    return ns_''')
# ---- 371: unit returns on the bar grid in every section ----
R('''    if len(pl) >= 4 and all(x == 2 for x in slots_of(sec)):                                # 346: a later unit returns an earlier one at the kept rates''',
  '''    if len(pl) >= 4 and all(x == 2 for x in slots_of(sec)) and "371" in OFF:              # 346: retired by 371 (unit returns on the bar grid in every section)''')
R('''        if all(x == 2 for x in slots_of(s1_)) or SECLEN[s1_] < 8 or "361" in OFF: continue
        UR[k_] = {}
        for j, src, rate in ((1, 0, 0.172), (2, 0, 0.315), (3, 1, 0.188)):
            if rng.random() < rate: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1''',
  '''        if SECLEN[s1_] < 8 or "361" in OFF or ("371" in OFF and all(x == 2 for x in slots_of(s1_))): continue   # 371: every section of eight bars or more
        UR[k_] = {}
        for j, (src, kept_, _m) in UR_KEPT.items():
            if rng.random() < UR_RATE[j]: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1''')
R('''                if ub and partner is not None: STATS["361: unit return under a paired line (310 kept)"] += 1; ub, upit = {}, {}''',
  '''                if ub and partner is not None:                                                # 371: a drawn unit return takes its bars from 310's pairing
                    if "371" in OFF: STATS["361: unit return under a paired line (310 kept)"] += 1; ub, upit = {}, {}
                    else: STATS["371: unit return over a paired line (the return kept)"] += 1; partner = None''')
# ---- 378: the time to the next line's first onset ----
R('''            h, s0, i0 = how(sec, i)
            if h in ("copy", "return", "plan", "tail") and (prefit(sec, i) or ("",))[0] == "ns":''',
  '''            h, s0, i0 = how(sec, i)
            SPAN_TO[0] = (line_start(*nxt) - U + (f0 if f0 is not None else 0)) if (nxt and nxt[0] == sec and "378" not in OFF) else None   # 378
            if h in ("copy", "return", "plan", "tail") and (prefit(sec, i) or ("",))[0] == "ns":''')
R('''            last_max = None
            if nxt:''', '''            last_max = None; f0 = None
            if nxt:''')
# ---- 375: 349's target on the notes whose chord allows an outside pitch class; 381: 358 from the song's sung extras ----
R('''    want = OS_T[0] * len(ns) + meta.get("os_carry", 0.0); k = int(want)
    on_ = set(notes_on) | {x["on"] for x in ns}; cand = []''',
  '''    on_ = set(notes_on) | {x["on"] for x in ns}; cand = []
    elig = len(ns) if "375" in OFF else sum(1 for j in range(len(ns) - 1) if any(not M.clash(ns[j]["p"] + d_, M.chord_for(ns[j], on_)) and (ns[j]["p"] + d_) % 12 in extra
                                                                                 and not tri(ns[j]["p"] + d_, M.chord_for(ns[j], on_)) for d_ in (-1, 1)))   # 375: the notes whose chord allows one
    want = OS_T[0] * elig + meta.get("os_carry", 0.0); k = int(want)''')
R('''            if j > 0 and n["on"] % BEAT and q % 12 not in M.SCALE and "358" not in OFF \\''',
  '''            if j > 0 and n["on"] % BEAT and q % 12 in (M.SUNGPC - M.SCALE if "381" not in OFF else set(range(12)) - M.SCALE) and "358" not in OFF \\''')
# ---- 373 and 382: the limits read on the kept songs ----
R('''        "cmp": ("at least", L286["cmp"]["soft"], L286["cmp"]["hard"]), "memory": ("at least", L286["memory"]["soft"], L286["memory"]["hard"]),
        "surprisal": ("at least", L286["surprisal"]["soft"], L286["surprisal"]["hard"]),
        "rhythm band": ("between", L286["rhythm band"]["soft"], L286["rhythm band"]["hard"]), "sequence legs": ("at most", L286["sequence legs"]["soft"], L286["sequence legs"]["hard"])}''',
  '''        "cmp": ("at least", L286["cmp"]["soft"], L286["cmp"]["hard"]), "memory": ("at least", 0.12, -1e9),                  # 373: memory soft 0.12, no hard limit
        "surprisal": ("at least", 0.24, 0.08),                                                                          # 382: read on the kept songs
        "rhythm band": ("between", [1.62, 3.38], [1.43, 3.61]),                                                          # 373: with the pooled kept table (372)
        "sequence legs": ("at most", L286["sequence legs"]["soft"], L286["sequence legs"]["hard"])}
LIM_CORPUS = {"spectral": "kept chart songs (286, Window 128)", "realness": "withdrawn; printed (300)", "rhythm band": "kept chart songs, the pooled kept table (373)",
              "memory": "kept chart songs (373)", "surprisal": "kept chart songs (382)", "cmp": "POP909 pairs; unchanged, 94% of kept songs pass (373)", "sequence legs": "a count (286)"}''')
# ---- 376: the frozen knob's message ----
R('CAL_STOP.append(f"round {rd + 1}: {sorted(big & big_prev)}', 'CAL_STOP.append(f"round {CAL_ROUNDS[0]}: {sorted(big & big_prev)}')
# ---- the calibration: 366's run rate, 371's unit-return rates, 372's knobs ----
R('''            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)            # 355''',
  '''            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)            # 355''' + '''
            for s_ in ("Verse 1", "Chorus 1"):                                                             # 371: the unit returns as read
                f_ = win_feats(c2["notes"], BAR0[s_])
                for j_, (_src, _kp, m_) in UR_KEPT.items():
                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua["_ur" + str(j_)].append(f_[m_])''')
R('''            if "348" not in OFF:                                                             # 355: the run knob and the sixteenth-onset knob
                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))
                f_ = float(np.clip((KEPT355["in_runs"] / max(0.02, ir)) ** 4, 0.1, 10.0)); LK["run"] = float(np.clip(LK["run"] * f_, 1e-7, 5.0))   # on a log scale: the run weight acts across a line's many paths
                if f_ in (0.1, 10.0): full_now.add("run")''',
  '''            if "348" not in OFF:                                                             # 366: the run rate; 355: the sixteenth-onset knob
                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))
                f_ = float(np.clip(KEPT355["in_runs"] / max(0.02, ir), 0.6, 1.6)); LK["run"] = float(np.clip(LK["run"] * f_, 0.0, 1.0))   # a rate, at most one
                if f_ in (0.6, 1.6) and 0.0 < LK["run"] < 1.0: full_now.add("run")''')
R('''            row["356 (middle half, unaimed reading)"] =''', '''            if "371" not in OFF:                                                             # 371: the unit-return rates toward the kept readings
                for j_, (_src, kp_, m_) in UR_KEPT.items():
                    if ua.get("_ur" + str(j_)):
                        rd_u = float(np.mean(ua["_ur" + str(j_)])); f_ = float(np.clip(max(0.02, kp_) / max(0.02, rd_u), 0.6, 1.6))
                        UR_RATE[j_] = float(np.clip(UR_RATE[j_] * f_, 0.0, 1.0))
                row["371 (kept, unaimed reading, rate)"] = {UR_KEPT[j_][2]: (UR_KEPT[j_][1], round(float(np.mean(ua["_ur" + str(j_)])), 3) if ua.get("_ur" + str(j_)) else None, round(UR_RATE[j_], 3)) for j_ in UR_KEPT}
            row["356 (middle half, unaimed reading)"] =''')
R('''        row["338: unaimed builds read"] = k2''', '''        row["338: unaimed builds read"] = k2
        row["372: knobs"] = {k_: round(LK[k_], 4) for k_ in GAPKNOBS}''')
# ---- the run's record: the knobs against a factor of two, the limits with their corpus, the new tables ----
R('''    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)''',
  '''    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)
    rerun["tables118"] = {f: hashlib.sha256(open(f"{H118}/tables/{f}", "rb").read()).hexdigest()[:16] for f in sorted(os.listdir(f"{H118}/tables"))}
    rerun["knobs372"] = {k_: dict(final=round(LK[k_], 4), past_a_factor_of_two=bool(LK[k_] > 2.0 or LK[k_] < 0.5)) for k_ in GAPKNOBS}
    rerun["unit_return_rates371"] = {UR_KEPT[j_][2]: round(UR_RATE[j_], 4) for j_ in UR_KEPT}
    rerun["limits"] = {k_: dict(rule=LIM7[k_], corpus=LIM_CORPUS[k_]) for k_ in LIM7} | {"realness": dict(rule="printed", corpus=LIM_CORPUS["realness"])}
    rerun["section_bands372"] = {s_: (round(SEC_NPB[s_], 2), SEC_BAND[s_]) for s_ in SUNG}
    print("372: gap knobs", {k_: (round(LK[k_], 3), "PAST A FACTOR OF TWO" if (LK[k_] > 2.0 or LK[k_] < 0.5) else "") for k_ in GAPKNOBS}, "| 371: rates", rerun["unit_return_rates371"])''')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_v116_p40.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_v118_p40.py {N} {MODE}"')
R('open(f"{H116}/melody_v116_p40_{MODE}{_TAG}.pkl", "wb"))', 'open(f"{H118}/melody_v118_p40_{MODE}{_TAG}.pkl", "wb"))')
open("/home/claude/p50/melody_v118_p40.py", "w").write(s)
print("written")
