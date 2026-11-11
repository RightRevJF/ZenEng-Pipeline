"""Writes melody_v111_p40.py: the v111 port (fixes 322-329) on song 40, from the tested v110 port (songs/p42/melody_v110_p40.py)."""
s = open("/home/claude/p42/melody_v110_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)

s = '''"""ZenEng v111 PORT (fixes 322-329) on song 40: Nothing Else on Earth again, same lyric, intake and seed (Window 131, 27.55).
  322 a partner of another length (more than one syllable apart) keeps its partner's stressed onsets, the rest drawn freely, with no
      one-onset check; partners within one syllable copy every bar as under 310.
  323 a source bar one onset over the line's cap is copied without its weakest onset (lowest metric weight; the later on a tie);
      bars more than one over are still left out.
  324 a tonic ending takes the tonic nearest the centre of its section's drawn register (the register's drawn median), and the
      test is read there.
  325 every condition a design places on a note is checked against the drawn registers, which are redrawn until it can be met
      (none on this path).
  327 a unit's last line ends by beat 3, or the copy after it enters after the downbeat: where a line cannot end with a breath
      before the copy that follows, the copy is fitted again to enter after its downbeat, then the join is read again.
  328 the sixteenth share printed beside the tempo band's kept figures (the report).
  329 the song's lowest and highest drawn notes are each sung, the lowest in a verse or the bridge and the highest in a chorus or
      the bridge (one fresh line each, chosen per build); no section's floor and cap narrower than the kept window range's 75th
      percentile (13 semitones) where the song's range allows.
Usage: PYTHONHASHSEED=0 python3 melody_v111_p40.py N main|ctl [tag]
From the v110 port:
''' + s[3:]
R('MODE = _MODE; HERE = "/home/claude/p40"; H109 = "/home/claude/p41"; H110 = "/home/claude/p42"; VAR = MODE; NEW = True',
  'MODE = _MODE; HERE = "/home/claude/p40"; H109 = "/home/claude/p41"; H110 = "/home/claude/p42"; H111 = "/home/claude/p43"; VAR = MODE; NEW = True')

# ---- 322: a partner of another length keeps the stresses ----
R('''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False):''',
  '''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None):''')
R('''    def dp(kind_, tgt, cb):
        def cbw(t): return 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else 0.04''',
  '''    def dp(kind_, tgt, cb, sb=None):
        def cbw(t, k=0):
            w = 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else 0.04
            if sb and st[k] and (t // BAR) in sb and t not in sb[t // BAR]: w *= 0.04           # 322: a stressed syllable on the partner's stresses
            return w''')
R('''                alpha[0][(t, 1)] = A(0, t) * cbw(t); continue
            alpha[0][(t, 1)] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t) * cbw(t)''',
  '''                alpha[0][(t, 1)] = A(0, t) * cbw(t, 0); continue
            alpha[0][(t, 1)] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t) * cbw(t, 0)''')
R('''                w_ = A(k, t) * cbw(t)''', '''                w_ = A(k, t) * cbw(t, k)''')
R('''        cb = {}
        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or rng.random() < 0.40}   # 293 at 40%; 310: a pair takes every bar
        elif copybars and _try == 14: STATS["293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if tgt + step * post > end or tgt - step * Ls < tmin: continue
        alpha, cbw = dp(kind_, tgt, cb)''',
  '''        cb = {}; sb = {}
        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or rng.random() < 0.40}   # 293 at 40%; 310: a pair takes every bar
        elif copybars and _try == 14: STATS["293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if stressbars and _try < 14 and not free: sb = stressbars                         # 322
        elif stressbars and _try == 14: STATS["322: partner's stresses given up for a line"] += 1
        if tgt + step * post > end or tgt - step * Ls < tmin: continue
        alpha, cbw = dp(kind_, tgt, cb, sb)''')
R('''        STATS["293: bars copied" if not pair else "310: partner bars copied"] += len(cb)
        return ons''', '''        STATS["293: bars copied" if not pair else "310: partner bars copied"] += len(cb)
        if sb: STATS["322: partner's stresses kept"] += 1
        return ons''')
R('''    kw = {}
    if partner is not None: kw = dict(copybars=again_kw(*partner)["copybars"], pair=True)                       # 310: the partner's bars''',
  '''    kw = {}
    if partner is not None:
        if abs(partner[2] - len(sy)) > 1 and "322" not in OFF:                             # 322: another length: the partner's stressed onsets
            kw = dict(stressbars=stress_bars(partner[0], partner[1])); STATS["322: paired lines of another length"] += 1
        else: kw = dict(copybars=again_kw(partner[0], partner[1])["copybars"], pair=True)  # 310: the partner's bars''')
R('''def units_of(sec):''', '''def ordinary_end(sec, i):
    n = slot_len(sec, i); return 36 if n == 1 else n * BAR - 24                         # 327: the end without 310's unit rule
def units_of(sec):''')
R('''def again_kw(S, SU):''', '''def stress_bars(S, SU):
    """322: the partner's stressed onsets, bar by bar (relative to its line's start)."""
    sb = collections.defaultdict(set)
    for n in S:
        t = n["on"] - SU
        if t >= 0 and n.get("stress"): sb[t // BAR].add(t)
    return dict(sb)
def again_kw(S, SU):''')
R('''                pj = pair_of(sec, i); partner = (built[(sec, pj)], line_start(sec, pj)) if pj is not None and (sec, pj) in built else None''',
  '''                pj = pair_of(sec, i); partner = (built[(sec, pj)], line_start(sec, pj), len(LINES[sec][pj])) if pj is not None and (sec, pj) in built else None''')

# ---- 323: a bar one onset over the cap ----
R('''    if copybars:                                                                         # 313: only bars the cap allows can be copied
        allowed = {bb: ts for bb, ts in copybars.items() if len(ts) <= cap}
        if len(allowed) < len(copybars): STATS["313: copied bars the cap does not allow, left out"] += len(copybars) - len(allowed)
        copybars = allowed''',
  '''    if copybars:                                                                         # 313: only bars the cap allows can be copied
        allowed = {}
        for bb, ts in copybars.items():
            if len(ts) <= cap: allowed[bb] = ts
            elif len(ts) == cap + 1:                                                       # 323: one over: copied without its weakest onset
                wk = min(ts, key=lambda t: (M.mw(t), -t)); allowed[bb] = [t for t in ts if t != wk]
                STATS["323: bar one onset over the cap, weakest onset dropped"] += 1
            else: STATS["313: copied bars the cap does not allow, left out"] += 1
        copybars = allowed''')

# ---- 325: designs read when the registers are drawn ----
R('''ENDING_NEEDS = {}                                                                     # 311: kind -> the degrees an ending section must find in its register''',
  '''ENDING_NEEDS = {}                                                                     # 311: kind -> the degrees an ending section must find in its register
DESIGN_REG = []                                                                       # 325: (name, test on the drawn registers); none on the default path''')
R('''        ok = all(any(p % 12 in need for p in range(int(R_[k][2]), int(R_[k][1]) + 1)) for k, need in ENDING_NEEDS.items())
        if ok: break
        STATS["311: register redrawn for its ending"] += 1
    else: STATS["311: ending degree missing after 50 draws"] += 1''',
  '''        ok = all(any(p % 12 in need for p in range(int(R_[k][2]), int(R_[k][1]) + 1)) for k, need in ENDING_NEEDS.items())
        dz = [nm for nm, t in DESIGN_REG if not t(R_, info)]
        if ok and not dz: break
        if not ok: STATS["311: register redrawn for its ending"] += 1
        for nm in dz: STATS["325: register redrawn for a design: " + nm] += 1
    else: STATS["311/325: ending or design missing after 50 draws"] += 1''')

# ---- 329: no section narrower than the kept window range allows; the drawn extremes sung ----
R('''    R = {"Verse": (V_MU, V_CAP, V_FLOOR), "Chorus": (c_mu, c_cap, c_floor), "Pre": ((V_MU + c_mu) / 2, max(V_CAP, c_cap), V_FLOOR),
         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}
    return R, dict(u=u, ub=ub, chorus_median=lm, chorus_top=lt, chorus_floor=lf, bridge_median=lb)''',
  '''    R = {"Verse": (V_MU, V_CAP, V_FLOOR), "Chorus": (c_mu, c_cap, c_floor), "Pre": ((V_MU + c_mu) / 2, max(V_CAP, c_cap), V_FLOOR),
         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}
    R = {k: widen_329(v, lo, hi) for k, v in R.items()}
    return R, dict(u=u, ub=ub, chorus_median=lm, chorus_top=lt, chorus_floor=lf, bridge_median=lb)
WIN_MIN = 13                                                                          # 329: the kept eight-bar range's 75th percentile (8 to 13)
def widen_329(reg, lo, hi):
    """329: a section's floor and cap no narrower than the kept window range allows, inside the song's range; the cap first."""
    mu, cap, fl = reg; need = WIN_MIN - (cap - fl)
    if need > 0:
        up = min(hi - cap, (need + 1) // 2); cap += up; need -= up
        dn = min(fl - lo, need); fl -= dn; need -= dn
        cap += min(hi - cap, max(0, need))
        STATS["329: a section's register widened"] += 1
    return (mu, cap, fl)''')
R('''    info.update(song_lo=lo, song_hi=hi, song_range=r, verse_share=round((V_MU - lo) / max(1, r), 3), v_mu=V_MU, v_cap=V_CAP, v_floor=V_FLOOR)''',
  '''    info.update(song_lo=lo, song_hi=hi, song_range=r, verse_share=round((V_MU - lo) / max(1, r), 3), v_mu=V_MU, v_cap=R_["Verse"][1], v_floor=R_["Verse"][2],
                sections={k: tuple(round(x, 2) for x in v) for k, v in R_.items()})''')
R('''    meta["plans"] = plans''', '''    meta["plans"] = plans
    meta["tonic_endings"] = []''')
R('''    def endok_of(sec, i):''', '''    # 329: one fresh line carries the song's lowest drawn note (a verse or the bridge), one its highest (a chorus or the bridge)
    xlo = min(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)
    xhi = max(p for p in range(meta["registers"]["song_lo"], meta["registers"]["song_hi"] + 1) if p % 12 in M.SCALE)
    lowc = [(s_, j) for s_ in SUNG if s_ in CARRY_LOW for j in range(len(LINES[s_])) if how(s_, j)[0] == "fresh"]
    highc = [(s_, j) for s_ in SUNG if s_ in CARRY_HIGH for j in range(len(LINES[s_])) if how(s_, j)[0] == "fresh"]
    car_lo = rng.choice(lowc) if lowc else None
    highc = [x for x in highc if x != car_lo] or highc
    car_hi = rng.choice(highc) if highc else None
    CARRY = {}
    if "329" in OFF: car_lo = car_hi = None                                                 # diagnostics only
    if car_lo: CARRY[car_lo] = xlo
    if car_hi: CARRY[car_hi] = xhi
    meta["carriers"] = dict(low=(car_lo, xlo), high=(car_hi, xhi))
    for (s_, j), x in CARRY.items():                                                       # the carrying section's register reaches it
        k_ = KIND[s_]; mu_, cap_, fl_ = REGS[k_]; REGS[k_] = (mu_, max(cap_, x), min(fl_, x))
    def endok_of(sec, i):''')
R('''                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)''',
  '''                    if (sec, i) in CARRY and _try < 6:                                    # 329: the drawn extreme on this line
                        x = CARRY[(sec, i)]; hiq = x >= mu; on_ = notes_on_all | {x_["on"] for x_ in ns}
                        order_ = sorted(range(len(ns)), key=lambda j: -shape[j][0] if hiq else shape[j][0])
                        jx = next((j for j in order_ if not ns[j]["slur"] and not (fx and j in fx) and not tri(x, M.chord_for(ns[j], on_))
                                   and not M.clash(x, M.chord_for(ns[j], on_))), None)
                        if jx is not None:
                            d0 = x - shape[jx][0]; xj = shape[jx][1]
                            shape = [(h_ + d0 * math.exp(-((x_ - xj) / 0.25) ** 2), x_) for h_, x_ in shape]
                            fx = dict(fx or {}); fx[jx] = x
                        else: STATS["329: no note on the carrying line can take the extreme"] += 1
                    elif (sec, i) in CARRY and _try == 6: STATS["329: extreme dropped after six tries"] += 1
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)''')

# ---- 324: the tonic ending read on the drawn register's centre (recorded) ----
R('''                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1''',
  '''                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1
                if need_end:                                                                   # 324: a tonic ending, against its register's centre
                    tc = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]
                    if tc and all((p - M.TONIC) % 12 == 0 for p in tc):
                        meta["tonic_endings"].append(dict(line=f"{sec}:{i}", centre=mu, nearest=min(tc, key=lambda p: (abs(p - mu), p)), drawn=ns[-1]["p"]))''')

# ---- 327: the unit's end and the join read together ----
R('''            if last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return _fail("join: no held end and breath before the copy (212)")''',
  '''            if last_max is not None and ns[-1]["on"] - U > last_max and nxt is not None:      # 327: the copy fitted again to enter after its downbeat
                if refit_327(*nxt):
                    pf = pending[nxt]; f0 = (pf[1][0]["on"] - line_start(*nxt)) if pf[0] == "ns" else pf[1][0]
                    last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
                    STATS["327: copy fitted again after its downbeat" + ("" if ns[-1]["on"] - U <= last_max else ", join still short")] += 1
            if last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return _fail("join: no held end and breath before the copy (212)")''')
R('''    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]''',
  '''    def refit_327(sec2, i2):
        """327: the copy after a line that cannot breathe, fitted again with no pickup added before its source's entry; a unit's last
        line so fitted keeps the ordinary end (beat 4 of a one-bar line) instead of 310's beat 3. An exact copy cannot move."""
        pf = pending.get((sec2, i2))
        if not pf or pf[0] == "fail": return False
        U2 = line_start(sec2, i2); f0 = (pf[1][0]["on"] - U2) if pf[0] == "ns" else pf[1][0]
        if f0 > 0: return False
        h2, s2, j2 = how(sec2, i2)
        if h2 in ("return", "plan") and (s2, j2) in built:
            S = built[(s2, j2)]; SU = line_start(s2, j2); lo_, hi_ = REGS[KIND[sec2]][2], REGS[KIND[sec2]][1]
            ALIGN_END[0] = ordinary_end(sec2, i2)
            ns2, kd = vary_return(rng, S, LINES[s2][j2], LINES[sec2][i2], SU, U2, 6, lo_, hi_, notes_on_all, endok=endok_of(sec2, i2))
            if ns2 and ns2[0]["on"] - U2 > f0:
                pending[(sec2, i2)] = ("ns", ns2, kd); STATS[f"327: {h2} fitted again without a pickup" + (", ordinary end" if unit_end(sec2, i2) else "")] += 1; return True
        elif h2 == "again" and (s2, j2) in built:
            AIMP = globals()["AIM"]; globals()["AIM"] = AIMS[pool_of(sec2)]
            ons = line_rhythm(LINES[sec2][i2], rng, 6, sec2, i=i2, **again_kw(built[(s2, j2)], line_start(s2, j2))); globals()["AIM"] = AIMP
            if ons and ons[0] > f0: pending[(sec2, i2)] = ("ons", ons, None); STATS["327: sung-again line fitted after its downbeat"] += 1; return True
        STATS[f"327: copy could not enter later ({h2}, entry {'pickup' if f0 < 0 else 'on'})"] += 1
        return False
    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]''')

R('''DESIGN_GATES = []                                                                     # the default path: none in force''',
  '''DESIGN_GATES = []                                                                     # the default path: none in force
CARRY_LOW = [s_ for s_ in SUNG if KIND[s_] in ("Verse", "Bridge") and s_ in ("Verse 1", "Bridge")]     # 329: the first verse or the bridge
CARRY_HIGH = [s_ for s_ in SUNG if s_ in ("Chorus 1", "Bridge")]                                  # 329: the first chorus or the bridge''')
R('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v110_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v111_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
R('''                open(f"{H110}/melody_v110_p40_{MODE}{_TAG}.pkl", "wb"))''', '''                open(f"{H111}/melody_v111_p40_{MODE}{_TAG}.pkl", "wb"))''')
open("/home/claude/p43/melody_v111_p40.py", "w").write(s)
print("written")
