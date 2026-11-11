"""Writes melody_v110_p40.py: the v110 port (fixes 310-321) on song 40, from the tested v109 port (melody_v109_p40.py)."""
s = open("/home/claude/p41/melody_v109_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100]); s = s.replace(a, b)
s = '''"""ZenEng v110 PORT (fixes 310-321) on song 40, the test of the port before song 42: Nothing Else on Earth on the default path again.
  310 a paired line (the same slot in parallel four-bar units) takes its partner's bar rhythm as laid under 308; a line ending a four-bar
      unit ends by beat 3 of the unit's last bar; no judge refitted.  311 the register drawn for an ending section holds its ending
      degree, redrawn until it does (counted).  312/315 the contour amplitude capped at 7; the arch aimed at the kept middle half (0.0-0.55),
      raised only while leaps past a fifth stay at or under 3.6% of moves at the median; the calibration stops, and says so, when a knob
      takes its largest step two rounds running.  313 copied bars chosen among those the line's cap allows.  314 the song's range drawn
      first (kept 17 semitones, 14.5-22), cut to the row and centred in it; the verse's median drawn at the kept share of that range
      (50%, 40-57%); a tonic ending takes the tonic nearest its section's median.  316 a long line's entry and landing drawn only from
      those that admit 308's cap.  317 a design gate stands outside 275, its pass rate printed (none on this path).  318-321 printed.
Usage: PYTHONHASHSEED=0 python3 melody_v110_p40.py N main|ctl [tag]
From the v109 port:
''' + s[3:]
R('MODE = _MODE; HERE = "/home/claude/p40"; H109 = "/home/claude/p41"', 'MODE = _MODE; HERE = "/home/claude/p40"; H109 = "/home/claude/p41"; H110 = "/home/claude/p42"')
R('L109 = json.load(open(f"{H109}/limits_v109.json"))', '''L109 = json.load(open(f"{H109}/limits_v109.json"))
C110 = json.load(open(f"{HERE}/tables/zeneng_v110_song41_checks.json"))["kept"]                  # 310, 312, 314: the kept counts of Window 130
K314 = C110["314 the song's range and the verse in it"]''')
# ---- 314: the song's range first, centred in the row; the verse's median at the kept share; 311: the ending's degree held ----
R('''V_MU, V_CAP, V_FLOOR = 64, 69, 57                                                     # the verse in the mezzo's low-middle: E4, to A4, from A3
def draw_registers(rng):''', '''V_MU, V_CAP, V_FLOOR = 64, 69, 57                                                     # replaced per build by 314's draw (below)
ROW_LO, ROW_HI = M.LO, TOP; PLACE = "centre"                                           # 314: the row, and the writer's placement (centre unless chosen)
Q5 = [5, 25, 50, 75, 95]
def kq(vals, u): return float(np.interp(100 * u, [0] + Q5 + [100], [vals[0] - (vals[1] - vals[0])] + list(vals) + [vals[-1] + (vals[-1] - vals[-2])]))
def draw_song_range(rng):
    """314: the song's range drawn at the kept shares, cut to the row, centred (unused semitones split, the odd one above)."""
    row = ROW_HI - ROW_LO; r = int(round(min(row, max(5, kq(K314["the song's sung range, semitones (5, 25, 50, 75, 95)"], rng.random())))))
    spare = row - r
    lo = ROW_LO + (spare // 2 if PLACE == "centre" else 0 if PLACE == "low" else spare); return lo, lo + r
ENDING_NEEDS = {}                                                                     # 311: kind -> the degrees an ending section must find in its register
def draw_registers(rng):
    global V_MU, V_CAP, V_FLOOR
    for tries in range(50):
        R_, info = _draw_registers(rng)
        ok = all(any(p % 12 in need for p in range(int(R_[k][2]), int(R_[k][1]) + 1)) for k, need in ENDING_NEEDS.items())
        if ok: break
        STATS["311: register redrawn for its ending"] += 1
    else: STATS["311: ending degree missing after 50 draws"] += 1
    info["redraws"] = tries; return R_, info
def _draw_registers(rng):
    global V_MU, V_CAP, V_FLOOR
    lo, hi = draw_song_range(rng); r = hi - lo; us = rng.random()
    V_MU = lo + kq(K314["verse median"], us) * r; V_FLOOR = max(lo, int(round(V_MU - 7))); V_CAP = min(hi, int(round(V_MU + 5)))
    R_, info = draw_registers_288(rng, lo, hi)
    info.update(song_lo=lo, song_hi=hi, song_range=r, verse_share=round((V_MU - lo) / max(1, r), 3), v_mu=V_MU, v_cap=V_CAP, v_floor=V_FLOOR)
    return R_, info
def draw_registers_288(rng, lo, hi):''')
R('''    c_mu = V_MU + lm; c_cap = int(round(min(TOP, max(c_mu + 3, V_CAP + lt)))); c_floor = int(round(max(M.LO, min(c_mu - 3, V_FLOOR + lf))))''',
  '''    c_mu = min(hi - 2, max(lo + 2, V_MU + lm)); c_cap = int(round(min(hi, max(c_mu + 3, V_CAP + lt)))); c_floor = int(round(max(lo, min(c_mu - 3, V_FLOOR + lf))))''')
R('''         "Bridge": (b_mu, int(round(min(TOP, b_mu + 6))), int(round(max(M.LO, b_mu - 7))))}''',
  '''         "Bridge": (b_mu, int(round(min(hi, b_mu + 6))), int(round(max(lo, b_mu - 7))))}''')
R('''    b_mu = V_MU + lb''', '''    b_mu = min(hi - 2, max(lo + 2, V_MU + lb))''')
R('''TRIAD = {2, 6, 9}''', '''TRIAD = {2, 6, 9}
ENDING_NEEDS.update(Chorus={M.TONIC % 12})                                            # 311: the hook (and the tag that copies it) ends on the tonic''')
# 314: a tonic ending takes the tonic nearest its section's median
R('''def end_target(sec, i, h_end, lo, hi):
    """295: the contour of an ending line is drawn toward the nearest permitted ending."""
    c = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]''', '''def end_target(sec, i, h_end, lo, hi, mu=None):
    """295: the contour of an ending line is drawn toward the nearest permitted ending; 314: a tonic ending toward the tonic nearest the
    section's median."""
    c = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and end_ok(sec, i, p)]
    if mu is not None and c and all((p - M.TONIC) % 12 == 0 for p in c): return min(c, key=lambda p: (abs(p - mu), p))''')
R('''                        tgt = end_target(sec, i, shape[-1][0], lo, hi); d = tgt - shape[-1][0]''',
  '''                        tgt = end_target(sec, i, shape[-1][0], lo, hi, mu); d = tgt - shape[-1][0]''')
R('''                            last_p = rng.choices(cands, [math.exp(-(p - tgt) ** 2 / 4.5) for p in cands])[0]''',
  '''                            last_p = tgt if tgt in cands and all((p - M.TONIC) % 12 == 0 for p in cands) else rng.choices(cands, [math.exp(-(p - tgt) ** 2 / 4.5) for p in cands])[0]   # 314''')
# composite's fit term reads the build's own verse cap
R('''max(vps) <= V_CAP]''', '''max(vps) <= c["meta"]["registers"].get("v_cap", V_CAP)]''')
# ---- 310: units and pairs; a unit's last line ends by beat 3 ----
R('''def slot_end(sec, i):
    n = slot_len(sec, i); return 36 if n == 1 else n * BAR - 24                       # the line done by beat 3 of its last bar (beat 4 in a one-bar slot)''',
  '''def unit_end(sec, i): return sum(slots_of(sec)[:i + 1]) % 4 == 0                    # 310: the line ends a four-bar unit of its section
def slot_end(sec, i):
    n = slot_len(sec, i)
    if unit_end(sec, i): return (n - 1) * BAR + 24                                       # 310: a unit's last line ends by beat 3 of the unit's last bar
    return 36 if n == 1 else n * BAR - 24
def units_of(sec):
    """310: the section cut into four-bar units at its slot boundaries; None where a boundary falls inside a line."""
    sl = slots_of(sec); out, cur, acc = [], [], 0
    for i, n in enumerate(sl):
        cur.append(i); acc += n
        if acc % 4 == 0: out.append(cur); cur = []
    return out if not cur else None
def pair_of(sec, i):
    """310: the partner of a line in the second of two parallel units (units 2m and 2m+1 with the same slots): the first's line in the same place."""
    us = units_of(sec)
    if not us: return None
    for k, u in enumerate(us):
        if i in u and k % 2 == 1:
            v = us[k - 1]
            if [slot_len(sec, j) for j in u] == [slot_len(sec, j) for j in v]: return v[u.index(i)]
    return None''')
# ---- 310/313/316: the line's rhythm ----
a = s.index("def line_rhythm("); b = s.index("LONG_SHARE = 0.57")
s = s[:a] + '''FITS = {}
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False):
    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)
    step = 3                                                                            # 288: the sixteenth grid, at the class table's rates and the window's aim
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d): return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max([k for k in range(n) if st[k]] or [n - 1]); post = n - 1 - Ls
    def A(k, t):
        m = M.mw(t); w = {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
        tm = t % BAR
        return w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0)
    tilt = AIM.tilt; fix = fix or {}
    cap = int(LONG_SHARE * n) if n >= 9 else n                                           # 308: no bar holds more than 57% of a long line
    if copybars:                                                                         # 313: only bars the cap allows can be copied
        allowed = {bb: ts for bb, ts in copybars.items() if len(ts) <= cap}
        if len(allowed) < len(copybars): STATS["313: copied bars the cap does not allow, left out"] += len(copybars) - len(allowed)
        copybars = allowed
    G = [t for t in range(-12, end + 1, step) if tmin <= t <= end]
    def tw(tp, k, d): return M.RT[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)
    def dp(kind_, tgt, cb):
        def cbw(t): return 1.0 if not cb or (t // BAR) not in cb or t in cb[t // BAR] else 0.04
        alpha = [dict() for _ in range(n)]
        for t in G:
            if t > tgt: break
            if Ls == 0 and t != tgt: continue
            if 0 in fix and t != fix[0]: continue
            if st[0] and t < 0: continue
            if kind_ is not None:
                if not ENTRY_T[kind_](t): continue
                alpha[0][(t, 1)] = A(0, t) * cbw(t); continue
            alpha[0][(t, 1)] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t) * cbw(t)
        for k in range(1, n):
            for t in G:
                if k == Ls and t != tgt: continue
                if k < Ls and t >= tgt: continue
                if k in fix and t != fix[k]: continue
                if st[k] and t < 0: continue
                acc = collections.defaultdict(float)
                for (tp, cp), a_ in alpha[k - 1].items():
                    d = t - tp
                    if step <= d <= 24:
                        c = cp + 1 if t // BAR == tp // BAR else 1
                        if c <= cap: acc[c] += a_ * tw(tp, k, d)
                w_ = A(k, t) * cbw(t)
                for c, v in acc.items():
                    if v > 0: alpha[k][(t, c)] = v * w_
        return alpha, cbw
    fits = None
    if n >= 9 and not fix:                                                               # 316: the entry and landing drawn only from those that admit the cap
        nb = slot_len(sec, i); lo_ = 0 if nb == 1 else (nb - 1) * BAR - 24
        lands = [t for t in range(lo_, min(slot_end(sec, i), end) + 1, 6) if tmin + step * Ls <= t and t + step * post <= end]
        key = (sec, i, tmin, end, tuple(lands))
        if key not in FITS: FITS[key] = {(k_, t) for k_ in ENTRY for t in lands if dp(k_, t, {})[0][n - 1]}   # cached: what fits depends on the slot alone
        fits = FITS[key]
        STATS["316: long lines"] += 1
        if not fits: STATS["316: long line with no entry and landing that fit"] += 1
    NT = 20 if copybars else 14
    if n >= 9: NT = 60
    for _try in range(NT + 10):
        free = _try >= NT or (fits is not None and not fits)
        if free and _try == NT: STATS["rhythm: placed with a free entry and landing"] += 1
        kind_ = None
        if NEW and not fix and not free:
            ek = list(ENTRY) if fits is None else [k_ for k_ in ENTRY if any(f[0] == k_ for f in fits)]
            if entry in ENTRY_T and (fits is None or entry in ek): kind_ = entry
            else: kind_ = rng.choices(ek, [ENTRY[k_] for k_ in ek])[0]
            if kind_ == "pickup" and st[0] and fits is None: kind_ = rng.choices(["on", "after"], [ENTRY["on"], ENTRY["after"]])[0]
        if Ls in fix: tgt = fix[Ls]
        elif free: tgt = rng.choice(list(range(max(0, tmin + step * Ls), end - step * post + 1, step)) or [end])
        elif fits is not None: tgt = land_draw(rng, sec, n, i, allowed={t for k_, t in fits if k_ == kind_})
        else: tgt = land_draw(rng, sec, n, i)
        cb = {}
        if copybars and _try < 14 and not free: cb = {bb: ts for bb, ts in copybars.items() if pair or rng.random() < 0.40}   # 293 at 40%; 310: a pair takes every bar
        elif copybars and _try == 14: STATS["293: copy given up for a line" if not pair else "310: partner's rhythm given up for a line"] += 1
        if tgt + step * post > end or tgt - step * Ls < tmin: continue
        alpha, cbw = dp(kind_, tgt, cb)
        if not alpha[n - 1]:
            if n >= 9: STATS["308: long line redrawn"] += 1
            continue
        ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) for x in ks]
        cur = rng.choices(ks, ws)[0]; ons = [cur[0]]
        for k in range(n - 1, 0, -1):
            t, c = cur
            ks = [(tp, cp) for (tp, cp) in alpha[k - 1] if step <= t - tp <= 24 and (cp + 1 if t // BAR == tp // BAR else 1) == c]
            ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) for x in ks]
            cur = rng.choices(ks, ws)[0]; ons.append(cur[0])
        ons.reverse()
        if cb and any(len(set(ts) ^ {t for t in ons if t // BAR == bb}) > 1 for bb, ts in cb.items()): continue   # 303: within one onset of its source bar
        STATS["293: bars copied" if not pair else "310: partner bars copied"] += len(cb)
        return ons
    return None
''' + s[b:]
R('''def land_draw(rng, sec, n_syl, i=None):''', '''def land_draw(rng, sec, n_syl, i=None, allowed=None):''')
R('''    opts = [t for t in range(lo_, hi_ + 1, 6)]
    sh = dict(LAND_SH)''', '''    opts = [t for t in range(lo_, hi_ + 1, 6)]
    if allowed is not None: opts = [t for t in opts if t in allowed] or sorted(allowed)                   # 316
    sh = dict(LAND_SH)''')
# fresh lines: 310's partner
R('''def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None, entry=None, i=None):''',
  '''def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None, entry=None, i=None, partner=None):''')
R('''    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i)''',
  '''    kw = {}
    if partner is not None: kw = dict(copybars=again_kw(*partner)["copybars"], pair=True)                       # 310: the partner's bars
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry, i=i, **kw)''')
R('''                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i)''',
  '''                pj = pair_of(sec, i); partner = (built[(sec, pj)], line_start(sec, pj)) if pj is not None and (sec, pj) in built else None
                if partner is not None: STATS["310: paired lines"] += 1
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, None, i=i, partner=partner)''')
# ---- 312: leaps past a fifth held; the walk's leap knob ----
R('''LK = dict(amp=5.0, widen=1.0, fresh=2.0)''', '''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0)''')
R('''        if cands and base > 0 and c[1] > 0:''', '''        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])                            # 312: leaps past a fifth held to the kept 75th percentile
        if cands and base > 0 and c[1] > 0:''')
# ---- 312/315: the calibration ----
R('''ARCH_SPAN = 0.23                                                                       # 305: kept median of the arch term over the line's span''',
  '''ARCH_SPAN = 0.23                                                                       # 305: kept median of the arch term over the line's span
ARCH_BAND = (0.0, 0.55); AMP_CAP = 7.0; LEAP_75 = 0.036                                # 312/315: the kept middle half; the cap; the kept 75th percentile
CAL_STOP = []''')
R('''    log = []; lines_acc = []''', '''    log = []; lines_acc = []; big_prev = set(); pf_acc = []''')
R('''            if NEW: lines_acc.append(line_readings(c["notes"]))''', '''            if NEW: lines_acc.append(line_readings(c["notes"]))
            for s_ in ("Verse 1", "Chorus 1"):
                f_ = win_feats(c["notes"], BAR0[s_])
                if f_ and np.isfinite(f_.get("past_fifth", np.nan)): pf_acc.append(f_["past_fifth"])''')
R('''            if "305" in OFF: LK["amp"] = float(np.clip(LK["amp"] * float(np.clip(1.452 / max(0.2, arch), 0.6, 1.6)), 1.5, 7))
            else: LK["amp"] = float(max(1.5, LK["amp"] * float(np.clip(ARCH_SPAN / max(0.02, arch), 0.6, 1.6))))   # 305: aimed at the kept arch over the span; no cap
            LK["widen"] = float(np.clip(LK["widen"] + 2.0 * (0.326 - wid), -1.0, 5.0))
            LK["fresh"] = float(np.clip(LK["fresh"] * float(np.clip(1.338 / max(0.1, fr), 0.6, 1.6)), 0.5, 6))''',
  '''            big = set(); pf = float(np.median(pf_acc)) if pf_acc else 0.0
            if arch < ARCH_BAND[0] and pf <= LEAP_75: m_ = float(np.clip(ARCH_SPAN / max(0.02, arch) if arch > 0 else 1.6, 0.6, 1.6))   # 312: raised only while leaps are in range
            elif arch > ARCH_BAND[1] or pf > LEAP_75: m_ = float(np.clip(ARCH_BAND[1] / max(0.02, arch), 0.6, 1.0)) if arch > ARCH_BAND[1] else 0.85
            else: m_ = 1.0                                                                   # 315: inside the kept middle half: no step
            if m_ in (0.6, 1.6): big.add("amp")
            LK["amp"] = float(np.clip(LK["amp"] * m_, 1.5, AMP_CAP))                          # 315: the cap of 7
            ml = float(np.clip(LEAP_75 / max(1e-3, pf), 0.5, 1.0)) if pf > LEAP_75 else 1.0
            if ml == 0.5: big.add("leap")
            LK["leap"] = float(np.clip(LK["leap"] * ml, 0.05, 1.0)); pf_acc.clear()
            LK["widen"] = float(np.clip(LK["widen"] + 2.0 * (0.326 - wid), -1.0, 5.0))
            mf = float(np.clip(1.338 / max(0.1, fr), 0.6, 1.6))
            if mf in (0.6, 1.6): big.add("fresh")
            LK["fresh"] = float(np.clip(LK["fresh"] * mf, 0.5, 6))''')
R('''            row["lines"] = dict(arch_span=(ARCH_SPAN, round(arch, 3), round(LK["amp"], 3)), widening=(0.326, round(wid, 3), round(LK["widen"], 3)), fresh=(1.338, round(fr, 3), round(LK["fresh"], 3)))''',
  '''            row["lines"] = dict(arch_span=(ARCH_BAND, round(arch, 3), round(LK["amp"], 3)), past_fifth=(LEAP_75, round(pf, 3), round(LK["leap"], 3)),
                                widening=(0.326, round(wid, 3), round(LK["widen"], 3)), fresh=(1.338, round(fr, 3), round(LK["fresh"], 3)), largest_steps=sorted(big))
            if big & big_prev:                                                                  # 315: the largest step two rounds running
                CAL_STOP.append(f"calibration stopped after round {rd + 1}: {sorted(big & big_prev)} took the largest step two rounds running")
                print(CAL_STOP[-1]); log.append(row); return log
            big_prev = big''')
# ---- files, seed ----
R('''    print("rerun:", rerun)''', '''    rerun["calibration_stop"] = list(CAL_STOP)
    print("rerun:", rerun)''')
R('cmd=f"PYTHONHASHSEED=0 python3 melody_v109_p40.py {N} {MODE}"', 'cmd=f"PYTHONHASHSEED=0 python3 melody_v110_p40.py {N} {MODE}"')
R('open(f"{H109}/melody_v109_p40_{MODE}{_TAG}.pkl", "wb"))', 'open(f"{H110}/melody_v110_p40_{MODE}{_TAG}.pkl", "wb"))')
open("/home/claude/p42/melody_v110_p40.py", "w").write(s)
print("written")
