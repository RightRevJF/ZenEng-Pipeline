"""Writes melody_v115_p40.py: the v115 port (fixes 348-354; Window 135) on the v114 port (songs/p45/melody_v114_p40.py)."""
s = open("/home/claude/p45/melody_v114_p40.py").read()
def R(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:120]); s = s.replace(a, b)
s = '''"""ZenEng v115 PORT (fixes 348-354; Window 135, 27.59) on the v114 port. Songs 40, 42 and 43 run again on it before any new song.
  348 a sixteenth only as a push in a drawn line: an onset on a sixteenth position is followed by an eighth or more (a run is not
      drawn); a returning line's words are fitted by splitting on the eighth grid unless there is no room. The writer's reading (Q1 A):
      "unless there is no room" holds for drawn lines too: a line with more syllables than eighth-grid places in its slot may run.
  349 the share outside the scale placed: the build's drawn share is met by moving notes a semitone to the song's sung extra pitch
      class where fix 200 allows it (no chord tone a semitone away, no tritone from the root; no tritone or leap past a sixth made with
      a neighbour; never a line's last note); the walk no longer offers them by weight. A minor song's share is drawn at the kept minor rate (4.5%).
  350 four-line plans keep their returns: unit 3 returns unit 1 at the kept 31.5%, units 2 and 4 as 346.
  351 a bar that fails the one-onset check drops out of the copy; the rest of the line keeps its copied bars; the rate read after.
  352 the pick of record is the judge's first; the composite's first (255's pick) and each one's rank on the other printed.
  353 a minor song's window measures read on its own tonic with the natural minor scale (MTON, MAJ set by the song).
  354 the gaps between onsets (a sixteenth, an eighth, a quarter, longer) aimed together at the kept means for the song's notes a
      bar (Table DU), by four knobs set on unaimed builds.
Usage: PYTHONHASHSEED=0 python3 melody_v115_p40.py N main|ctl [tag]
From the v114 port:
''' + s[3:]
R('H114 = "/home/claude/p45"; VAR = MODE', 'H114 = "/home/claude/p45"; H115 = "/home/claude/p46"; VAR = MODE')
# ---- 348 ----
R('''        if tp % 6 == 3: w *= RUNW if d == 3 else PUSHW                                     # 341: a run weighted down, a push up''',
  '''        if tp % 6 == 3 and d < 6 and not runs_ok: return 0.0                               # 348: a sixteenth only as a push''')
R('''    G = [t for t in range(-12, end + 1, step) if tmin <= t <= end]''',
  '''    G = [t for t in range(-12, end + 1, step) if tmin <= t <= end]
    runs_ok = len([t for t in G if t % 6 == 0 and (t >= 0 or not st[0])]) < n               # 348 (Q1 A): no room on the eighth grid: runs allowed
    if runs_ok: STATS["348: a drawn line with no room on the eighth grid (runs allowed)"] += 1''')
R('''        if d in (3, 9): w *= LK["s16"]                                                     # 341: sixteenth gaps at the kept share''',
  '''        w *= LK["s16"] if d in (3, 9) else LK["g8"] if d == 6 else LK["g4"] if d == 12 else LK["glong"] if d > 12 else 1.0   # 354: the gaps together''')
R('''    M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 3                                  # 288: sixteenths are on the grid now
    ns = M.align3(src, src_sy, sy, U0, U, tmin)''', '''    M.END_T = ALIGN_END[0]; M.MINSPLIT = 12; M.STEP = 6                                  # 348: split on the eighth grid first
    ns = M.align3(src, src_sy, sy, U0, U, tmin)
    if ns is None:
        M.STEP = 3; ns = M.align3(src, src_sy, sy, U0, U, tmin)                            # unless there is no room
        if ns is not None: STATS["348: a returning line split on the sixteenth grid (no room)"] += 1''')
# ---- 349 ----
R('''    if p % 12 not in M.SCALE: w *= LK["k44"] * OS_T[0] / KEPT114["outside_scale"]''', '''    if p % 12 not in M.SCALE: w = 0.0                                                    # 349: placed, not offered''')
R('''    OS_T[0] = 0.0 if rng.random() < 0.5 else rng.choice(OS_KEPT)                               # 344''',
  '''    OS_T[0] = 0.0 if rng.random() < 0.5 else rng.choice(OS_KEPT) * OS_SCALE                    # 344; 349: a minor song at the kept minor rate
    meta["os_carry"] = 0.0''')
R('''PALS = {}; OS_T = [0.0]; SEC_USED = set()''', '''PALS = {}; OS_T = [0.0]; SEC_USED = set()
OS_SCALE = 1.0                                                                        # 349: 4.5 / 7.1 for a minor song (set by the song)
MTON = None                                                                           # 353: a minor song's tonic for the window measures (set by the song)
def mton(): return M.TONIC if MTON is None else MTON
def place_outside(rng, ns, notes_on, meta):
    """349: the build's drawn share outside the scale, met by moving notes as fix 200 chooses them."""
    extra = sorted(M.SUNGPC - M.SCALE)
    if not extra or len(ns) < 3: return
    want = OS_T[0] * len(ns) + meta.get("os_carry", 0.0); k = int(want)
    on_ = set(notes_on) | {x["on"] for x in ns}; cand = []
    for j in range(0, len(ns) - 1):                                                       # not a line's last note (its ending)
        n = ns[j]; ch = M.chord_for(n, on_)
        for q in (n["p"] - 1, n["p"] + 1):
            if q % 12 not in extra or M.clash(q, ch) or tri(q, ch): continue                   # fix 200: no chord tone a semitone away; no tritone from the root
            if j > 0 and (abs(q - ns[j - 1]["p"]) in (6,) or abs(q - ns[j - 1]["p"]) > 9): continue
            if abs(ns[j + 1]["p"] - q) in (6,) or abs(ns[j + 1]["p"] - q) > 9: continue
            cand.append((j, q)); break
    rng.shuffle(cand); used = set(); placed = 0
    for j, q in cand:
        if placed >= k: break
        if j in used or j - 1 in used or j + 1 in used: continue
        ns[j]["p"] = q; ns[j]["outside"] = True; used.add(j); placed += 1
    STATS["349: notes placed outside the scale"] += placed
    if placed < k: STATS["349: places wanting"] += k - placed
    meta["os_carry"] = want - placed''')
R('''                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1''',
  '''                if need_end and not end_ok(sec, i, ns[-1]["p"]): end_rule(sec, i, ns, notes_on_all, lo, hi); meta["moved"] += 1
                place_outside(rng, ns, notes_on_all, meta)                                       # 349''')
# ---- 350 ----
R('''        for j, src, rate in ((1, 0, 0.172), (3, 1, 0.188)):''', '''        for j, src, rate in ((1, 0, 0.172), (2, 0, 0.315), (3, 1, 0.188)):                     # 346; 350: unit 3 returns unit 1''')
# ---- 351 ----
R('''        if cb and any(len(set(ts) ^ {t for t in ons if t // BAR == bb}) > 1 for bb, ts in cb.items()): continue   # 303: within one onset of its source bar''',
  '''        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy
            bad = [bb for bb, ts in cb.items() if len(set(ts) ^ {t for t in ons if t // BAR == bb}) > 1]
            if bad: STATS["351: bars left out of a copy"] += len(bad); cb = {bb: ts for bb, ts in cb.items() if bb not in bad}''')
# ---- 353 ----
R('''def win_feats(notes, b0): return feats(win_N(notes, b0), M.TONIC)''', '''def win_feats(notes, b0): return feats(win_N(notes, b0), mton())                       # 353: a minor song on its own tonic''')
R('''        N = win_N(notes, BAR0[s]); f = feats(N, M.TONIC); rows[s] = dict(J.score_window(f, N), feats=f)''',
  '''        N = win_N(notes, BAR0[s]); f = feats(N, mton()); rows[s] = dict(J.score_window(f, N), feats=f)''')
R('''def deg_w(p): return AIM.deg.get((p - M.TONIC) % 12, 1.0)''', '''def deg_w(p): return AIM.deg.get((p - mton()) % 12, 1.0)                                # 353: the degrees aimed where they are read''')
# ---- 354 ----
R('''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0)''',
  '''LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0)
DU = [(0, 3.5, (0.04, 0.40, 0.24, 0.29)), (3.5, 4.5, (0.11, 0.50, 0.17, 0.18)), (4.5, 5.5, (0.14, 0.55, 0.16, 0.11)), (5.5, 99, (0.28, 0.49, 0.08, 0.09))]   # 354: Table DU
GAPS = ("gap_sixteenth", "gap_eighth", "gap_quarter", "gap_longer")
def du_target(npb): return next(t for lo, hi, t in DU if lo <= npb < hi)''')
R('''                for m_ in KEPT114:
                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])''', '''                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar"]:
                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])''')
R('''            LK["s16"] = float(np.clip(LK["s16"] * np.clip(KEPT114["gap_sixteenth"] / max(0.01, rd["gap_sixteenth"]), 0.5, 1.6), 0.05, 3.0))''',
  '''            tg = du_target(float(np.mean(ua["notes_per_bar"])))                              # 354: the four gaps toward the kept means for the density
            for kn_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg):
                r_ = float(np.mean(ua[m_])) if ua.get(m_) else t_
                LK[kn_] = float(np.clip(LK[kn_] * np.clip(max(0.01, t_) / max(0.01, r_), 0.6, 1.6), 0.05, 5.0))
            row["354 (band target, unaimed reading, knob)"] = {m_: (t_, round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[k_], 3)) for k_, m_, t_ in zip(("s16", "g8", "g4", "glong"), GAPS, tg)}''')
# ---- 352 ----
R('''    sfp = {c["fp"] for c in short}; pick = next(c for c in alive if c["fp"] in sfp) if alive else None''',
  '''    sfp = {c["fp"] for c in short}; pick_255 = next(c for c in alive if c["fp"] in sfp) if alive else None
    pick = byj[0] if byj else None                                                       # 352: the pick of record is the judge's first''')
R('''        for lab, c in (("composite first", alive[0]), ("shortlist pick", pick), ("judge first", byj[0]), ("pick, old fit", pick_old)):''',
  '''        for lab, c in (("composite first", alive[0]), ("pick (judge 1st)", pick), ("255's pick", pick_255), ("pick, old fit", pick_old)):''')
R('''                     pick=pick, pick_old_fit=pick_old,''', '''                     pick=pick, pick_255=pick_255, pick_old_fit=pick_old,''')
R('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v114_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v115_p40.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
R('''                open(f"{H114}/melody_v114_p40_{MODE}{_TAG}.pkl", "wb"))''', '''                open(f"{H115}/melody_v115_p40_{MODE}{_TAG}.pkl", "wb"))''')
open("/home/claude/p46/melody_v115_p40.py", "w").write(s)
print("written")
