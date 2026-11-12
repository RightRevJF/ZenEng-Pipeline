"""Writes melody_v116_p40.py: v116's fixes 355-363 on the v115 port (songs/p46/melody_v115_p40.py). 359 stays as v115 (Q1 A, v116:
the kept-window table has no key); 364 is the report's (sep_v116.py)."""
s = open("/home/claude/p46/melody_v115_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
s = '''"""ZenEng v116 PORT (fixes 355-364; Window 136, 27.60) on the v115 port. Songs 40, 42 and 43 run again on it, and song 43 twice more
with fix 348 off and with fix 354 off (356's diagnostic runs, ZE_OFF=348 / ZE_OFF=354).
  355 sixteenths: runs at the kept rate. A sixteenth-position onset followed by a sixteenth (a run) is weighted by a knob set on unaimed
      builds toward the kept 31% in runs; onsets on a sixteenth position weighted by a second knob toward the kept 9.4%.
  356 the rhythm band's bits and the distinct note lengths are read on each calibration round; the four 354 knobs stop when either
      leaves the kept middle half (distinct lengths: the kept windows' quartiles; the rhythm band: the middle half of a normal band
      fitted to 286's soft limits as the kept 5th and 95th, 1.98-2.53, since the tables give no quartiles).
  357 the calibration runs while a knob still moves at full step, up to six rounds, the rounds printed; s16 does not rise while the
      onsets on a sixteenth read over the kept 9.4%.
  358 a note outside the scale that moves by step (one or two semitones) to both its neighbours, on a weak eighth or a sixteenth, is
      allowed whatever the chord; fix 200's rule stays for notes on the beat.
  359 not ported (Q1 A, v116): the kept-window table carries no key, so the 70 minor windows cannot be read apart; costs are read
      against all 314 and the report says so.
  360 a bar that fails 303's check is fitted again (the copy's onsets required in that bar) before it is left out.
  361 unit returns drawn on the section's two-bar units whatever the line lengths: a fresh line covering a returning unit takes the
      earlier unit's onsets bar by bar and its pitches as the contour; sections of two-bar lines keep 350's line plans.
  362 the pick: the judge's first among the survivors that break no soft limit; if none, the judge's first, and the run says so.
  363 and 364 are the report's.
Usage: PYTHONHASHSEED=0 python3 melody_v116_p40.py N main|ctl [tag]
The v115 port it is built on:
''' + s[3:]
R('H115 = "/home/claude/p46"; VAR', 'H115 = "/home/claude/p46"; H116 = "/home/claude/p47"; VAR')
R('LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0)',
  'LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=0.01, on16=1.0)   # 355: run, on16 (the run knob starts low: a run is taken wherever it is allowed)')
R('KEPT114 = dict(', '''KEPT355 = dict(in_runs=0.31, on_sixteenth=0.094)                                          # 355
_dd = sorted(r_["distinct_durations"] for r_ in KRW if np.isfinite(r_.get("distinct_durations", np.nan)))
MID356 = dict(distinct_durations=(float(np.percentile(_dd, 25)), float(np.percentile(_dd, 75))),
              rhythm_bits=(2.2541 - 0.6732 * 0.674 / 1.645, 2.2541 + 0.6732 * 0.674 / 1.645))     # 356: the rhythm band's middle half, from 286's soft limits
STOP356 = []
def s16_shape(notes):
    """355: of onsets on a sixteenth position in the verse and chorus windows: how many, how many in runs, how many pushed."""
    n6 = r6 = p6 = 0
    for s_ in ("Verse 1", "Chorus 1"):
        ons = sorted({n_["on"] for n_ in notes if BAR0[s_] * BAR <= n_["on"] < (BAR0[s_] + 8) * BAR}); S_ = set(ons)
        for t_ in ons:
            if t_ % 6 == 3: n6 += 1; r6 += (t_ - 3) in S_ and (t_ + 3) in S_; p6 += (t_ + 3) not in S_
    return n6, r6, p6
KEPT114 = dict(''')
# ---- 355: runs at the kept rate; the sixteenth-position onsets aimed ----
R('''        return w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (LK["offb"] if t % 12 == 6 else 1.0)   # 346: the off-beat eighth''',
  '''        return (w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (LK["offb"] if t % 12 == 6 else 1.0)   # 346: the off-beat eighth
                * (LK["on16"] if t % 6 == 3 and "348" not in OFF else 1.0))                       # 355: onsets on a sixteenth aimed at the kept 9.4%''')
R('''        w *= LK["s16"] if d in (3, 9) else LK["g8"] if d == 6 else LK["g4"] if d == 12 else LK["glong"] if d > 12 else 1.0   # 354: the gaps together
        if tp % 6 == 3 and d < 6 and not runs_ok: return 0.0                               # 348: a sixteenth only as a push''',
  '''        if "354" not in OFF: w *= LK["s16"] if d in (3, 9) else LK["g8"] if d == 6 else LK["g4"] if d == 12 else LK["glong"] if d > 12 else 1.0   # 354: the gaps together
        if tp % 6 == 3 and d < 6 and not runs_ok and "348" not in OFF: w *= LK["run"]        # 355 (amends 348): a run at the kept rate, the rest pushes''')
R('''    M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 6                                  # 348: split on the eighth grid first''',
  '''    M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 3 if "348" in OFF else 6            # 348: split on the eighth grid first (diagnostic: off)''')
# ---- 360: a failed bar fitted again before it is left out ----
R('''    def dp(kind_, tgt, cb, sb=None):
        def cbw(t, k=0):
            w = 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else 0.04''',
  '''    def dp(kind_, tgt, cb, sb=None, strict=()):
        def cbw(t, k=0):
            w = 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else (0.0 if (t // BAR) in strict else 0.04)   # 360: a bar fitted again''')
R('''        ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) for x in ks]
        cur = rng.choices(ks, ws)[0]; ons = [cur[0]]
        for k in range(n - 1, 0, -1):
            t, c = cur
            ks = [(tp, cp) for (tp, cp) in alpha[k - 1] if step <= t - tp <= 24 and (cp + 1 if t // BAR == tp // BAR else 1) == c]
            ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) for x in ks]
            cur = rng.choices(ks, ws)[0]; ons.append(cur[0])
        ons.reverse()
        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy
            bad = [bb for bb, ts in cb.items() if len(set(ts) ^ {t for t in ons if t // BAR == bb}) > 1]
            if bad: STATS["351: bars left out of a copy"] += len(bad); cb = {bb: ts for bb, ts in cb.items() if bb not in bad}''',
  '''        def sample(alpha):
            ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) for x in ks]
            if not ks or sum(ws) <= 0: return None
            cur = rng.choices(ks, ws)[0]; ons = [cur[0]]
            for k in range(n - 1, 0, -1):
                t, c = cur
                ks = [(tp, cp) for (tp, cp) in alpha[k - 1] if step <= t - tp <= 24 and (cp + 1 if t // BAR == tp // BAR else 1) == c]
                ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) for x in ks]
                if not ks or sum(ws) <= 0: return None
                cur = rng.choices(ks, ws)[0]; ons.append(cur[0])
            ons.reverse(); return ons
        ons = sample(alpha)
        if ons is None: continue
        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy
            badf = lambda o_: [bb for bb, ts in cb.items() if len(set(ts) ^ {t for t in o_ if t // BAR == bb}) > 1]
            bad = badf(ons)
            if bad and "360" not in OFF:                                                   # 360: the failed bars fitted again, the copy's onsets required there
                a2, _ = dp(kind_, tgt, cb, sb, strict=set(bad))
                o2 = sample(a2) if a2[n - 1] else None
                if o2 is not None and len(badf(o2)) < len(bad):
                    STATS["360: bars fitted again and kept"] += len(bad) - len(badf(o2)); ons = o2; bad = badf(o2)
                else: STATS["360: bars fitted again without success"] += len(bad)
            if bad: STATS["351: bars left out of a copy"] += len(bad); cb = {bb: ts for bb, ts in cb.items() if bb not in bad}''')
# ---- 361: unit returns on the bar grid ----
R('def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None):',
  'def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False):')
R('''        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or rng.random() < RATE293[0]}   # 293 at 331's rate; 310: a pair takes every bar
        elif copybars and _try == 14 and not (pair and fallback): STATS["293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1''',
  '''        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or allbars or rng.random() < RATE293[0]}   # 293 at 331's rate; 310 and 361: every bar
        elif copybars and _try == 14 and not (pair and fallback): STATS["361: unit return given up for a line" if allbars else "293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1''')
R('''        STATS["293: bars copied" if not pair else "310: partner bars copied"] += len(cb)''',
  '''        STATS["361: unit bars copied" if allbars else "293: bars copied" if not pair else "310: partner bars copied"] += len(cb)''')
R('''def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None, entry=None, i=None, partner=None):''',
  '''def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None, entry=None, i=None, partner=None, unitbars=None):''')
R('''    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, **kw)
    if ons is None: return None''',
  '''    if not kw and unitbars: kw = dict(copybars=unitbars, allbars=True)                    # 361: the returning unit's onsets, bar by bar
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, **kw)
    if ons is None: return None''')
R('''    meta["plans"] = plans''', '''    meta["plans"] = plans
    UR = {}                                                                              # 361: unit returns on the bar grid, for sections not all of two-bar lines
    for k_ in sorted({KIND[s_] for s_ in SUNG}):
        s1_ = next(s_ for s_ in SUNG if KIND[s_] == k_)
        if all(x == 2 for x in slots_of(s1_)) or SECLEN[s1_] < 8 or "361" in OFF: continue
        UR[k_] = {}
        for j, src, rate in ((1, 0, 0.172), (2, 0, 0.315), (3, 1, 0.188)):
            if rng.random() < rate: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1
    meta["unit_returns"] = {k_: dict(v) for k_, v in UR.items()}''')
R('''                if partner is not None: STATS["310: paired lines"] += 1
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner)''',
  '''                if partner is not None: STATS["310: paired lines"] += 1
                ub, upit = {}, {}                                                          # 361: the bars of a returning unit this line covers
                for bl in range(slot_len(sec, i)):
                    ba = U // BAR + bl; rel = ba - BAR0[sec]; j = rel // 2
                    src = UR.get(kind, {}).get(j) if rel < 8 else None
                    if src is None: continue
                    sba = BAR0[sec] + 2 * src + rel % 2
                    if (BAR0[sec] + 2 * src + 2) * BAR > U: STATS["361: unit return inside one line, not drawn"] += 1; continue
                    sn = [n_ for l_ in lines for n_ in l_ if n_["sec"] == sec and sba * BAR <= n_["on"] < (sba + 1) * BAR]
                    if not sn: continue
                    ub[bl] = [bl * BAR + n_["on"] % BAR for n_ in sn]
                    for n_ in sn: upit[U + bl * BAR + n_["on"] % BAR] = n_["p"]
                if ub and partner is not None: STATS["361: unit return under a paired line (310 kept)"] += 1; ub, upit = {}, {}
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner, unitbars=ub or None)''')
R('''                    _durs(ns); ck, shape = draw_shape(rng, ns, mu, lo, hi); meta["contour"][(sec, i)] = ck''',
  '''                    _durs(ns); ck, shape = draw_shape(rng, ns, mu, lo, hi); meta["contour"][(sec, i)] = ck
                    if upit:                                                              # 361: the earlier unit's pitches as the contour
                        shape = [((upit[n_["on"]] if n_["on"] in upit else h_), x_) for n_, (h_, x_) in zip(ns, shape)]''')
R('''                    if need_end:                                                          # 302: the last note drawn first, the walk runs back to it
                        tgt = end_target''', '''                    if need_end:                                                          # 302: the last note drawn first, the walk runs back to it
                        if upit and ns[-1]["on"] in upit: shape[-1] = (end_target(sec, i, shape[-1][0], lo, hi, mu), shape[-1][1])
                        tgt = end_target''')
R('''                meta["kinds"][(sec, i)] = "fresh"''', '''                meta["kinds"][(sec, i)] = "fresh" if not upit else "fresh (361 unit return)"
                if upit: STATS["361: lines drawn on a returning unit"] += 1''')
R('''                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)''',
  '''                    if upit:                                                              # 361: the earlier unit's pitches kept where the chord allows
                        on_ = notes_on_all | {x_["on"] for x_ in ns}; fx = dict(fx or {})
                        for j_, n_ in enumerate(ns[:-1]):
                            q_ = upit.get(n_["on"])
                            if q_ is not None and j_ not in fx and lo <= q_ <= hi and not n_["slur"] and not tri(q_, M.chord_for(n_, on_)) and not M.clash(q_, M.chord_for(n_, on_)): fx[j_] = q_
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)''')
# ---- 358: a chromatic passing note ----
R('''        for q in (n["p"] - 1, n["p"] + 1):
            if q % 12 not in extra or M.clash(q, ch) or tri(q, ch): continue                   # fix 200: no chord tone a semitone away; no tritone from the root''',
  '''        for q in (n["p"] - 1, n["p"] + 1):
            if j > 0 and n["on"] % BEAT and q % 12 not in M.SCALE and "358" not in OFF \\
               and 1 <= abs(q - ns[j - 1]["p"]) <= 2 and 1 <= abs(ns[j + 1]["p"] - q) <= 2:    # 358: a chromatic passing or neighbour note, off the beat, any chord
                cand.append((j, q, True)); STATS["358: chromatic passing places"] += 1; break
            if q % 12 not in extra or M.clash(q, ch) or tri(q, ch): continue                   # fix 200: no chord tone a semitone away; no tritone from the root''')
R('''            cand.append((j, q)); break
    rng.shuffle(cand); used = set(); placed = 0
    for j, q in cand:
        if placed >= k: break
        if j in used or j - 1 in used or j + 1 in used: continue
        ns[j]["p"] = q; ns[j]["outside"] = True; used.add(j); placed += 1''', '''            cand.append((j, q, False)); break
    rng.shuffle(cand); used = set(); placed = 0
    for j, q, pas in cand:
        if placed >= k: break
        if j in used or j - 1 in used or j + 1 in used: continue
        ns[j]["p"] = q; ns[j]["outside"] = True; used.add(j); placed += 1
        if pas: ns[j]["pass358"] = True; STATS["358: chromatic passing notes placed"] += 1''')
R('''        if n["line"] in built_ret: continue                                                 # 287: a built return is left alone (the limits read it)''',
  '''        if n["line"] in built_ret or n.get("pass358"): continue                            # 287: a built return is left alone (the limits read it); 358: a passing note stays''')
# ---- 355-357: the calibration ----
R('def calibrate(rng, n=30, rounds=3):', 'def calibrate(rng, n=30, rounds=6):                                                    # 357: up to six rounds')
R('''    for rd in range(rounds):
        acc = {"V": collections.defaultdict(list), "C": collections.defaultdict(list)}; k = 0; tries = 0''',
  '''    full_prev = {"s16", "g8", "g4", "glong", "run", "on16"}
    for rd in range(rounds):
        if rd >= 3 and not full_prev:                                                     # 357: past three rounds only while a knob still moves at full step
            CAL_ROUNDS[0] = rd; break
        CAL_ROUNDS[0] = rd + 1; full_now = set()
        acc = {"V": collections.defaultdict(list), "C": collections.defaultdict(list)}; k = 0; tries = 0''')
R('''            if "Verse 2" in SUNG: v2_acc.append(v2_share(c2["notes"]))''', '''            if "Verse 2" in SUNG: v2_acc.append(v2_share(c2["notes"]))
            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)            # 355
            ua["_bits"].append(M.rhythm_bits(c2["notes"]))                                                 # 356''')
R('''            for kn_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg):
                r_ = float(np.mean(ua[m_])) if ua.get(m_) else t_
                LK[kn_] = float(np.clip(LK[kn_] * np.clip(max(0.01, t_) / max(0.01, r_), 0.6, 1.6), 0.05, 5.0))''',
  '''            on16 = float(np.mean(ua["on_sixteenth"])) if ua.get("on_sixteenth") else KEPT355["on_sixteenth"]
            dd = float(np.median(ua["distinct_durations"])) if ua.get("distinct_durations") else 4.0; bits = float(np.median(ua["_bits"]))
            out356 = [m_ for m_, v_ in (("distinct_durations", dd), ("rhythm_bits", bits)) if not (MID356[m_][0] <= v_ <= MID356[m_][1])]
            if out356 and not STOP356 and "354" not in OFF:                                    # 356: the 354 knobs stop when either reading leaves the kept middle half
                STOP356.append(f"round {CAL_ROUNDS[0]}: {out356} outside the kept middle half (distinct lengths {dd}, rhythm bits {round(bits, 3)}); the 354 knobs stop at "
                               f"{[round(LK[k_], 3) for k_ in ('s16', 'g8', 'g4', 'glong')]}"); print(STOP356[-1])
            for kn_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg):
                if STOP356 or "354" in OFF: break
                r_ = float(np.mean(ua[m_])) if ua.get(m_) else t_
                f_ = float(np.clip(max(0.01, t_) / max(0.01, r_), 0.6, 1.6))
                if kn_ == "s16" and f_ > 1.0 and on16 > KEPT355["on_sixteenth"]: f_ = 1.0         # 357: s16 aimed with the onsets on a sixteenth
                if f_ in (0.6, 1.6): full_now.add(kn_)
                LK[kn_] = float(np.clip(LK[kn_] * f_, 0.05, 5.0))
            if "348" not in OFF:                                                             # 355: the run knob and the sixteenth-onset knob
                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))
                f_ = float(np.clip((KEPT355["in_runs"] / max(0.02, ir)) ** 4, 0.1, 10.0)); LK["run"] = float(np.clip(LK["run"] * f_, 1e-7, 5.0))   # on a log scale: the run weight acts across a line's many paths
                if f_ in (0.1, 10.0): full_now.add("run")
                f_ = float(np.clip(KEPT355["on_sixteenth"] / max(0.01, on16), 0.6, 1.6)); LK["on16"] = float(np.clip(LK["on16"] * f_, 0.05, 5.0))
                if f_ in (0.6, 1.6): full_now.add("on16")
                row["355 (kept, unaimed reading, knob)"] = dict(in_runs=(0.31, round(ir, 3), round(LK["run"], 3)), on_sixteenth=(0.094, round(on16, 3), round(LK["on16"], 3)))
            row["356 (middle half, unaimed reading)"] = dict(distinct_durations=(MID356["distinct_durations"], dd), rhythm_bits=(tuple(round(x, 3) for x in MID356["rhythm_bits"]), round(bits, 3)))''')
R('''        log.append(row)
    return log''', '''        full_prev = full_now; row["357: knobs at full step"] = sorted(full_now)
        log.append(row)
    return log''')
R('''                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar"]:''', '''                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"]:''')
R('CAL_STOP = []; FROZEN = set()', 'CAL_STOP = []; FROZEN = set(); CAL_ROUNDS = [0]')
# ---- 362: the pick ----
R('''    pick = byj[0] if byj else None                                                       # 352: the pick of record is the judge's first''',
  '''    clean = [c for c in byj if not c["info"]["soft"]]                                      # 362: the judge's first among survivors with no soft break
    pick = clean[0] if clean else (byj[0] if byj else None); pick_352 = byj[0] if byj else None
    print(f"362: survivors with no soft break {len(clean)} of {len(byj)}" + ("" if clean else "; none qualified: the pick is the judge's first"))''')
R('''        for lab, c in (("composite first", alive[0]), ("pick (judge 1st)", pick), ("255's pick", pick_255), ("pick, old fit", pick_old)):''',
  '''        for lab, c in (("composite first", alive[0]), ("pick (362)", pick), ("judge's first", pick_352), ("255's pick", pick_255), ("pick, old fit", pick_old)):''')
R('''cmd=f"PYTHONHASHSEED=0 python3 melody_v115_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''cmd=f"PYTHONHASHSEED=0 python3 melody_v116_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
R('''    rerun["calibration_stop"] = list(CAL_STOP); rerun["frozen"] = sorted(FROZEN); rerun["rate293"] = RATE293[0]''',
  '''    rerun["calibration_stop"] = list(CAL_STOP); rerun["frozen"] = sorted(FROZEN); rerun["rate293"] = RATE293[0]
    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)''')
R('''pick=pick, pick_255=pick_255,''', '''pick=pick, pick_352=pick_352, clean=len(clean), pick_255=pick_255,''')
R('''                open(f"{H115}/melody_v115_p40_{MODE}{_TAG}.pkl", "wb"))''', '''                open(f"{H116}/melody_v116_p40_{MODE}{_TAG}.pkl", "wb"))''')
open("/home/claude/p47/melody_v116_p40.py", "w").write(s)
print("ok")
