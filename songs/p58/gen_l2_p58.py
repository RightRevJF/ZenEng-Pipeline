"""gen_l2_p58.py: writes melody_l2_p58.py (song 48 under Luthier v2: Module 27.83, Window 159) from melody_l1_p58.py, porting 630, 631,
633 and 634 with luthier_v2_tables.json (632 was ported under v137 for song 48; 635 asks no change of the draw here; 636 and 637 are the
paper's). Every patch replaces whole statements and is asserted to match exactly once. ZE_PART_L2=0 gives Luthier v1 as it stood.
- 630: the pick is the refit's first among survivors with no soft break whose gain under the kept couplings is 0.14 bits a bar or more
  (the kept median); if none, the pick as before, counted.
- 631: a line drawn under 600 draws its breath (its last onset to the next line's first) from the kept breaths of its cell (10th, 25th, 50th,
  75th percentiles, piecewise linear, the lower tail one step out and none past the 75th: a breath past it leaves a 14-syllable
  line too little of its second bar for 308's cap; on the sixteenth grid). It may run to the next line's first onset
  less that breath (the next line's known entry, or its slot's downbeat), not to beat 3 of its last bar; the next line's earliest entry and
  the join's breath are that breath, not 212's 18. 465's class 0 with a pickup is read with that breath and against the span 600 drew. A
  line on copied bars (361's unit returns, 605's template bars) keeps their span only where their source line met its own; otherwise 600's
  drawn span holds it as well (the verse sung again, 293, is held by 600's span in any case). Plan returns and copies of whole tunes are the form and are left as they are.
- 633: a line whose bars all follow the template takes the template's split of syllables between its bars where the words allow: the
  line's syllables are split in the template's proportion, and each bar's onset places are the template's, less its weakest or with its
  strongest free places added where the count differs.
- 634: the gap classes of 578 and 600 are drawn at 0.7 the palette's shares and 0.3 the cell's, as shares of the gap and not as weights on
  the position tables; the classes of move (repeat, step, third, fourth or fifth, larger) are drawn at the palette's shares (its clipped
  bucket at 7 split between fourth-or-fifth and larger by the kept windows' share of leaps past a fifth). 606's tilt gives way to it."""
SRC = "/home/claude/p58/melody_l1_p58.py"; DST = "/home/claude/p58/melody_l2_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""Luthier v1 (ZenEng v138; Module 27.82; by gen_l1_p58.py''', '''"""Luthier v2 (Module 27.83; by gen_l2_p58.py from melody_l1_p58.py: 630, 631, 633, 634) -- Luthier v1 (ZenEng v138; Module 27.82; by gen_l1_p58.py''')
P('''def ON18(f_): return PL1.get(f_, 0) <= VL1 and f_ not in OFF11
''', '''def ON18(f_): return PL1.get(f_, 0) <= VL1 and f_ not in OFF11
VL2 = int(_os11.environ.get("ZE_PART_L2", "1"))
PL2 = {f_: 1 for f_ in ("630", "631", "633", "634")}
def ON19(f_): return PL2.get(f_, 0) <= VL2 and f_ not in OFF11
''')
# ---- tables ----
P('''F606C = {}
''', '''F606C = {}
_SL2 = json.load(open("/home/claude/p58/tables/luthier_v2_tables.json"))
BR631T = {c_: v_[1:5] for c_, v_ in _SL2["610/618: kept lines in two-bar slots, by notes over the slot's bars: the breath, last onset of the line to first onset of the next, in twelfths of a beat (18 = a dotted quarter): lines; 10th, 25th, 50th, 75th percentile; share under 18; share of lines beginning before their bar line or after beat 1 (not on the downbeat)"].items()}
BR631 = {}; MET600 = {}; COPYMET = [True]; PREVB = [None]; MIX634 = [None]; PALCAT634 = [None]
def br631(rng_, sec_, i_):
    """631: the line's breath, drawn once a build from the kept breaths of its cell."""
    if (sec_, i_) not in BR631:
        q_ = BR631T[cell600(len(LINES[sec_][i_]) * MEL504[0] / max(1, slot_len(sec_, i_)))]
        lo_, hi_ = max(3.0, q_[0] - (q_[1] - q_[0])), q_[3]
        BR631[(sec_, i_)] = max(3, int(round(float(np.interp(rng_.random(), [0, 0.1, 0.25, 0.5, 0.75, 1.0], [lo_, q_[0], q_[1], q_[2], q_[3], hi_])) / 3)) * 3)
    return BR631[(sec_, i_)]
_KWW = json.load(open("/home/claude/p58/tables/zeneng_v132_kept_windows.json"))["windows"]
_PF634 = float(np.mean([w_["past_fifth"] for w_ in _KWW if w_.get("past_fifth") is not None])); _FF634 = float(np.mean([w_["fourth_fifth"] for w_ in _KWW if w_.get("fourth_fifth") is not None]))
Q634 = _PF634 / max(1e-6, _PF634 + 0.5 * _FF634)                                       # 634: the share of the clipped bucket at 7 that is a leap past a fifth
def palcat634(iv_):
    """634: the palette's shares of the classes of move."""
    a_ = lambda ks: sum(iv_[k + 7] for k in ks)
    c_ = dict(repeat=a_([0]), step=a_([-2, -1, 1, 2]), third=a_([-4, -3, 3, 4]), fourth_fifth=a_([-5, 5]) + (1 - Q634) * a_([-7, 7]), larger=Q634 * a_([-7, 7]))
    z_ = sum(c_.values()) or 1.0
    return {k: v / z_ for k, v in c_.items()}
def mix634(gs_, pal_):
    """634: a gap's share, 0.7 the palette's class share and 0.3 the cell's, spread over the grid's values in the class."""
    cur_ = collections.Counter()
    for k_, v_ in gs_.items():
        if k_ in _C606: cur_[_C606[k_]] += v_
    cl_ = (0, 2, 3, 4, 5, 6); zc_ = sum(cur_[c] for c in cl_) or 1.0; zp_ = sum(pal_[c] for c in cl_) or 1.0
    m_ = {c: 0.7 * pal_[c] / zp_ + 0.3 * cur_[c] / zc_ for c in cl_}; nd_ = collections.Counter(_pc606(d_) for d_ in range(3, 25, 3))
    return {d_: m_[_pc606(d_)] / nd_[_pc606(d_)] for d_ in range(3, 25, 3)}
''')
P('''    PAL606[0] = None
''', '''    PAL606[0] = None; BR631.clear(); MET600.clear(); PREVB[0] = None; PALCAT634[0] = None
''')
P('''            meta["palette606"] = x606_["song"]; STATS["606: palette drawn"] += 1
''', '''            meta["palette606"] = x606_["song"]; STATS["606: palette drawn"] += 1
            if ON19("634"): PALCAT634[0] = palcat634(PAL606[0][1])
''')
# ---- 631 in the line: the slot's end less the breath; 634's gap shares ----
P('''        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
''', '''        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
        if ON19("631"):                                                                  # 631: the line may run to the next line's first onset less its breath
            B631_ = br631(rng, sec, i); se = slot_len(sec, i) * BAR - B631_; end = se if last_max is None else min(se, last_max)
            SPAN600[0] = (S600_, len(sy), B631_); STATS["631: line may end at the next line's first onset less its breath"] += 1
''')
P('''        FW578_ = mix606(gs606_, kband(x606_), PAL606[0][0]); STATS["606: a line's gaps drawn from the mixed table"] += 1
''', '''        FW578_ = mix606(gs606_, kband(x606_), PAL606[0][0]); STATS["606: a line's gaps drawn from the mixed table"] += 1
        if ON19("634"): MIX634[0] = mix634(gs606_, PAL606[0][0]); STATS["634: a line's gaps drawn at the palette's shares"] += 1
    else: MIX634[0] = None
''')
P('''        if D578: return RTS[tp % BAR][d] * H(k - 1, d) * FW578_.get(d, 0.0)                  # 578: the slot band's table, its gap values at the kept lines' shares''',
  '''        if D578 and MIX634[0] is not None: return MIX634[0].get(d, 0.0) * H(k - 1, d)        # 634: the gap's share from the palette and the cell, not a weight on the position table
        if D578: return RTS[tp % BAR][d] * H(k - 1, d) * FW578_.get(d, 0.0)                  # 578: the slot band's table, its gap values at the kept lines' shares''')
# 631: whether the line met its span (for the copies)
P('''        if h465:                                                                           # 465: held to the end: the melisma's bar, and the next line's entry
            CLS465[0] = d465; STATS["465: line ends in its drawn bar"] += 1
            if d465["req"]: REQ465[d465["nxt"]] = d465["req"]
        return ons''', '''        if h465:                                                                           # 465: held to the end: the melisma's bar, and the next line's entry
            CLS465[0] = d465; STATS["465: line ends in its drawn bar"] += 1
            if d465["req"]: REQ465[d465["nxt"]] = d465["req"]
        if i is not None and D600: MET600[(sec, i)] = bool(F600C[0] is not None or (copybars and allbars and COPYMET[0]))   # 631: the line met its drawn span (or copied a source that met its own)
        return ons''')
# 631: 465's class 0 with a pickup, with the breath and against the span drawn
P('''        if rq_ == "pickup": b_ = min(b_, c_["nb"] * BAR - 6 - GAP_MIN)''', '''        if rq_ == "pickup": b_ = min(b_, c_["nb"] * BAR - 6 - (SPAN600[0][2] if (ON19("631") and SPAN600[0] is not None and len(SPAN600[0]) > 2) else GAP_MIN))   # 631: the drawn breath''')
P('''    if not ok_: STATS["465: no class the slot allows"] += 1; return None''', '''    if ON19("631") and SPAN600[0] is not None and SPAN600[0][1] == n and ok_:              # 631: the classes the span drawn can reach (first onset -12 to 30)
        T6_ = SPAN600[0][0] * c_["nb"] * BAR; ok2_ = [x_ for x_ in ok_ if x_[1] <= 30 + T6_ + 3 and x_[2] >= -12 + T6_ - 3]
        if ok2_: ok_ = ok2_
        else: STATS["631: no class reachable at the span drawn; classes as before"] += 1
    if not ok_: STATS["465: no class the slot allows"] += 1; return None''')
# 631: the main loop's breath
P('''            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)''', '''            U = line_start(sec, i); tmin = max(-12, last_on + (PREVB[0] if (ON19("631") and PREVB[0] is not None) else GAP_MIN) - U)   # 631: the breath the line before drew''')
P('''                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
            h, s0, i0 = how(sec, i)''', '''                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - (br631(rng, sec, i) if (ON19("631") and how(sec, i)[0] in ("fresh", "again")) else GAP_MIN)   # 631
            h, s0, i0 = how(sec, i)''')
P('''            if ns[0]["on"] - last_on < GAP_MIN: globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")''',
  '''            if ns[0]["on"] - last_on < (min(GAP_MIN, PREVB[0]) if (ON19("631") and PREVB[0] is not None) else GAP_MIN): globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")''')
P('''                    last_max = (line_start(*nxt) + f0 - U) - GAP_MIN''', '''                    last_max = (line_start(*nxt) + f0 - U) - (br631(rng, sec, i) if (ON19("631") and h in ("fresh", "again")) else GAP_MIN)   # 631''')
P('''            place(sec, i, ns)
''', '''            place(sec, i, ns)
            PREVB[0] = br631(rng, sec, i) if (ON19("631") and h in ("fresh", "again") and MET600.get((sec, i)) is not None) else None   # 631: this line's breath before the next
''')
# 631: copies bar by bar only from a source that met its span; 633: the template's split
P('''                            if tn_ and (tba_ + 1) * BAR <= U:
                                ub[bl] = [bl * BAR + n_["on"] % BAR for n_ in tn_]; STATS["605: a bar given the template's bar"] += 1''',
  '''                            js_ = next((j_ for j_ in range(len(LINES[sec])) if line_start(sec, j_) <= tba_ * BAR < line_start(sec, j_) + slot_len(sec, j_) * BAR), None)
                            if tn_ and (tba_ + 1) * BAR <= U:
                                ub[bl] = [bl * BAR + n_["on"] % BAR for n_ in tn_]; STATS["605: a bar given the template's bar"] += 1
                                if ON19("631") and MET600.get((sec, js_)) is False: COPYMET[0] = False; STATS["631: template bar's line missed its span: the line draws its own"] += 1''')
P('''                        sn = [n_ for l_ in lines for n_ in l_ if n_["sec"] == sec and sba * BAR <= n_["on"] < (sba + 1) * BAR]
                        if not sn: continue''', '''                        sn = [n_ for l_ in lines for n_ in l_ if n_["sec"] == sec and sba * BAR <= n_["on"] < (sba + 1) * BAR]
                        if not sn: continue
                        js_ = next((j_ for j_ in range(len(LINES[sec])) if line_start(sec, j_) <= sba * BAR < line_start(sec, j_) + slot_len(sec, j_) * BAR), None)
                        if ON19("631") and MET600.get((sec, js_)) is False: COPYMET[0] = False; STATS["631: unit's line missed its span: the line draws its own"] += 1''')
P('''                    if ub and partner is not None:                                                # 371: a drawn unit return takes its bars from 310's pairing''',
  '''                    if ON19("633") and ub and len(ub) == slot_len(sec, i) and sum(len(v_) for v_ in ub.values()) != len(sy):   # 633: the template's split of syllables
                        tot_ = sum(len(v_) for v_ in ub.values()); ks_ = sorted(ub); want_ = [max(1, int(round(len(sy) * len(ub[k_]) / tot_))) for k_ in ks_]
                        while sum(want_) > len(sy): j_ = max(range(len(ks_)), key=lambda x_: want_[x_]); want_[j_] -= 1
                        while sum(want_) < len(sy): j_ = min(range(len(ks_)), key=lambda x_: want_[x_] - len(ub[ks_[x_]])); want_[j_] += 1
                        for k_, w_ in zip(ks_, want_):
                            cur_ = sorted(ub[k_])
                            while len(cur_) > w_ and len(cur_) > 1: cur_.remove(min(cur_, key=lambda t_: (M.mw(t_), -t_)))
                            fr_ = [t_ for t_ in range(k_ * BAR, (k_ + 1) * BAR, 3) if t_ not in cur_]
                            while len(cur_) < w_ and fr_:
                                b_ = max(fr_, key=lambda t_: (M.mw(t_), -(t_ % 6), -t_)); cur_.append(b_); fr_.remove(b_)
                            ub[k_] = sorted(cur_)
                        STATS["633: the line takes the template's split of syllables"] += 1
                    if ub and partner is not None:                                                # 371: a drawn unit return takes its bars from 310's pairing''')
# 631: a line on copied bars keeps their span only where their source met its own; otherwise 600's span holds it too
P('''                    ub, upit = {}, {}                                                          # 361: the bars of a returning unit this line covers''',
  '''                    ub, upit = {}, {}; COPYMET[0] = True                                     # 361: the bars of a returning unit this line covers (631: their source's span)''')
P('''        if D600 and not free and _try < NT // 2 and not (ON18("605") and copybars and allbars):''',
  '''        if D600 and not free and _try < NT // 2 and not (ON18("605") and copybars and allbars and COPYMET[0]):''')
# ---- 634: the classes of move at the palette's shares ----
P('''    cats = [(c, AIM.cat[c], sz) for c, _, sz in M.CATS]''', '''    cats = [(c, (PALCAT634[0][c] if (ON19("634") and PALCAT634[0] is not None) else AIM.cat[c]), sz) for c, _, sz in M.CATS]   # 634: the classes of move at the palette's shares''')
P('''if (ON18("606") and PAL606[0] is not None) else 1.0   # 606: the move table tilted toward the palette''', '''if (ON18("606") and PAL606[0] is not None and not ON19("634")) else 1.0   # 606: the move table tilted toward the palette (634 sets the shares)''')
# ---- 630: the pick ----
P('''        old_ = pick; pick = clean_r[0] if clean_r else (byr[0] if byr else None)''', '''        old_ = pick; pick = clean_r[0] if clean_r else (byr[0] if byr else None)
        if ON19("630"):                                                                     # 630: the refit's first among clean survivors with a gain of 0.14 bits a bar or more
            for c_ in alive: c_["gain630"] = LR605.coupling_gain(c_["notes"])
            g630_ = [c_ for c_ in clean_r if (c_["gain630"] or -9) >= 0.14]
            PICK630[0] = dict(share=round(sum(1 for c_ in alive if (c_["gain630"] or -9) >= 0.14) / max(1, len(alive)), 3), before=pick["fp"] if pick else None, rank=next((j_ + 1 for j_, x_ in enumerate(clean_r) if g630_ and x_["fp"] == g630_[0]["fp"]), None))
            if g630_: pick = g630_[0]
            PICK630[0]["pick"] = pick["fp"] if pick else None; PICK630[0]["gain"] = round(pick.get("gain630") or float("nan"), 3) if pick else None
            print("630:", PICK630[0])''')
P('''PICK108 = [None, None]''', '''PICK108 = [None, None]; PICK630 = [None]''')
# ---- the record ----
P('''    rerun["l1_part"] = VL1;''', '''    rerun["l2_part"] = VL2; rerun["l2_on"] = sorted(f_ for f_ in PL2 if ON19(f_)); rerun["pick630"] = PICK630[0]
    rerun["l2_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("605:", "606:", "631:", "633:", "634:", "600:", "602:", "603:", "361:", "212:")}
    rerun["l1_part"] = VL1;''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l1_p58.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l2_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/runl1/melody_l1_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/runl2/melody_l2_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
