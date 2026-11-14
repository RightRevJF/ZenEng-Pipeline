"""gen_l1_p58.py: writes melody_l1_p58.py (song 48 under Luthier v1, formerly ZenEng v138: Module 27.82, Window 158) from melody_v137_p58.py
(v137's 600-604 as ported), porting 605 and 606 with luthier_v1_structure.json (607 and 608 are readings and the pick: read_l1.py). Every
patch replaces whole statements and is asserted to match exactly once. ZE_PART_L1=0 gives v137 as it stood; ZE_OFF switches a fix off.
- 605: the section's template. A section's first four bars (its first lines, drawn as now) stand as its template; in each later unit of four
  bars, each bar of a drawn line follows the template's bar in the same place at a calibrated rate (TP605): the template bar's onsets are
  given to the line as a returning unit's bars (361's machinery, rhythm only, no pitches), exactly where the syllables allow and otherwise
  within one onset (360/370). The rate is set in the calibration so that bars four apart within a section are the same rhythm in 20% of
  pairs. 361's unit 3 and unit 4 returns (the same places) give way to it; its unit 2 return stands. A verse sung again copies its first
  verse's lines (293) and so takes its template.
- 606: the song's palette. Each build first draws one kept song's palette (gap classes; intervals -7..+7) from the kept songs within one
  note a sung bar of this song. The gap tables of 578 and 600 are reweighted so their shares of the palette's gap classes are 0.7 the
  palette's and 0.3 their own; each move's weight is multiplied by 0.7 x (palette share / kept mean share of its interval) + 0.3, so the
  move table tilts seven parts in ten from the kept mean toward the palette."""
SRC = "/home/claude/p58/melody_v137_p58.py"; DST = "/home/claude/p58/melody_l1_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""ZenEng v137 (Module 27.81; by gen_v137_p58.py''', '''"""Luthier v1 (ZenEng v138; Module 27.82; by gen_l1_p58.py from melody_v137_p58.py: 605, 606) -- ZenEng v137 (Module 27.81; by gen_v137_p58.py''')
P('''def ON17(f_): return P137.get(f_, 0) <= V137 and f_ not in OFF11
''', '''def ON17(f_): return P137.get(f_, 0) <= V137 and f_ not in OFF11
VL1 = int(_os11.environ.get("ZE_PART_L1", "1"))
PL1 = {f_: 1 for f_ in ("605", "606")}
def ON18(f_): return PL1.get(f_, 0) <= VL1 and f_ not in OFF11
''')
# ---- the tables of 605 and 606 ----
P('''SPAN600 = [None]; T602 = [None]; SRC602 = {}; OFF602 = {}; DENSE603 = [False]
''', '''SPAN600 = [None]; T602 = [None]; SRC602 = {}; OFF602 = {}; DENSE603 = [False]
_SL1 = json.load(open("/home/claude/p58/tables/luthier_v1_structure.json"))
PALS606 = _SL1["606: the palettes of the kept songs"]; MEANPAL606 = _SL1["606: the kept mean palette (gaps; intervals)"]
PAL606 = [None]; TP605 = [0.5]; KEPT605 = {4: 0.201, 8: 0.249, 1: 0.032}
_C606 = {"sixteenth": 0, "eighth": 2, "dotted eighth": 3, "quarter": 4, "dotted quarter": 5, "half": 6}
def _pc606(d_): return {3: 0, 6: 2, 9: 3, 12: 4, 15: 5, 18: 5, 21: 6, 24: 6}.get(d_)
F606C = {}
def mix606(gs_, band_, pal_):
    """606: the gap table's shares of the palette's classes, 0.7 the palette's and 0.3 its own (the classes the grid can draw)."""
    key_ = (tuple(sorted(gs_.items())), band_, tuple(pal_))
    if key_ in F606C: return F606C[key_]
    cur_ = collections.Counter()
    for k_, v_ in gs_.items():
        if k_ in _C606: cur_[_C606[k_]] += v_
    cl_ = (0, 2, 3, 4, 5, 6); zc_ = sum(cur_[c] for c in cl_) or 1.0; zp_ = sum(pal_[c] for c in cl_) or 1.0
    m_ = {c: 0.7 * pal_[c] / zp_ + 0.3 * cur_[c] / zc_ for c in cl_}
    mg_ = collections.Counter()
    for _p in range(48):
        for _d in range(3, 25, 3): mg_[_pc606(_d)] += KRT[band_][_p][_d]
    zm_ = sum(mg_.values())
    F606C[key_] = {_d: (m_[_pc606(_d)] / (mg_[_pc606(_d)] / zm_)) if mg_[_pc606(_d)] > 0 else 0.0 for _d in range(3, 25, 3)}
    return F606C[key_]
''')
# 606: the palette drawn before any section
P('''    meta = dict(returns=[], kinds={}, win={}, targets={}, drawable405={}); CUR405[0] = meta["drawable405"]; REQ465.clear()   # 405
''', '''    meta = dict(returns=[], kinds={}, win={}, targets={}, drawable405={}); CUR405[0] = meta["drawable405"]; REQ465.clear()   # 405
    PAL606[0] = None
    if ON18("606"):                                                                        # 606: one kept song's palette, within one note a sung bar of this song
        npb606_ = sum(len(l_) for s_ in SUNG for l_ in LINES[s_]) * MEL504[0] / max(1, sum(SECLEN[s_] for s_ in SUNG))
        c606_ = [x_ for x_ in PALS606 if abs(x_["notes a sung bar"] - npb606_) <= 1.0]
        if c606_:
            x606_ = rng.choice(c606_); PAL606[0] = (list(x606_["gap classes, shares"]), list(x606_["interval classes -7..+7 (clipped), shares"]))
            meta["palette606"] = x606_["song"]; STATS["606: palette drawn"] += 1
''')
P('''        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
''', '''        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
    if ON18("606") and D578 and PAL606[0] is not None:                                   # 606: 578's and 600's gap tables mixed with the palette
        x606_ = len(sy) * MEL504[0] / max(1, slot_len(sec, i)); tb606_ = "two-bar" if slot_len(sec, i) == 2 else "all"
        gs606_ = (dict(_S137[("600: cells below 5.5, " if x606_ < 5.5 else "600: cells at 5.5 and over, ") + ("two-bar slots" if tb606_ == "two-bar" else "all slots")][cell600(x606_)]["gap values, shares"])
                  if (ON17("600") and D600) else dict(_S136["two-bar slots (over 6 to 10 beats)" if slot_len(sec, i) == 2 else "all slots"][kband(x606_)]["gap values, shares"]))
        FW578_ = mix606(gs606_, kband(x606_), PAL606[0][0]); STATS["606: a line's gaps drawn from the mixed table"] += 1
''')
# 606: moves
P('''                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_ * lt_); base += w0''',
  '''                pm_ = (0.7 * PAL606[0][1][max(-7, min(7, p - prev)) + 7] / max(1e-4, MEANPAL606[1][max(-7, min(7, p - prev)) + 7]) + 0.3) if (ON18("606") and PAL606[0] is not None) else 1.0   # 606: the move table tilted toward the palette
                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_ * lt_ * pm_); base += w0''')
# ---- 605: the template ----
P('''            if rng.random() < UR_RATE[j]: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1''',
  '''            if ON18("605") and j in (2, 3): continue                                         # 605: the template's places, not 361's
            if rng.random() < UR_RATE[j]: UR[k_][j] = src; STATS[f"361: unit {j + 1} returns unit {src + 1} (bar grid), drawn"] += 1''')
P('''                        if src is None: continue
                        sba = BAR0[sec] + 2 * src + rel % 2''', '''                        if src is None and ON18("605") and rel >= 4 and rng.random() < TP605[0]:   # 605: the bar follows the template's bar in the same place
                            tba_ = BAR0[sec] + rel % 4
                            tn_ = [n_ for l_ in lines for n_ in l_ if n_["sec"] == sec and tba_ * BAR <= n_["on"] < (tba_ + 1) * BAR]
                            if tn_ and (tba_ + 1) * BAR <= U:
                                ub[bl] = [bl * BAR + n_["on"] % BAR for n_ in tn_]; STATS["605: a bar given the template's bar"] += 1
                            else: STATS["605: template bar not sung or not yet drawn"] += 1
                            continue
                        if src is None: continue
                        sba = BAR0[sec] + 2 * src + rel % 2''')
# 605: the rate calibrated toward bars four apart the same in 20% of pairs within a section
P('''            ua["_bits"].append(M.rhythm_bits(c2["notes"]))                                                 # 356''',
  '''            ua["_bits"].append(M.rhythm_bits(c2["notes"]))                                                 # 356
            if ON18("605"):                                                                   # 605: bars four and eight apart within a section, the same rhythm
                r605_ = LR605.recurrence(c2["notes"], (1, 4, 8))
                for k_ in (1, 4, 8):
                    if r605_[k_][0] is not None: ua["_r605_" + str(k_)].append(r605_[k_][0])''')
P('''            if "371" not in OFF:                                                             # 371: the unit-return rates toward the kept readings''',
  '''            if ON18("605") and ua.get("_r605_4"):                                             # 605: the template's rate toward 20% at four bars
                r4_ = float(np.mean(ua["_r605_4"])); f_ = float(np.clip(KEPT605[4] / max(0.02, r4_), 0.6, 1.6)); TP605[0] = float(np.clip(TP605[0] * f_, 0.0, 1.0))
                if f_ in (0.6, 1.6) and 0.0 < TP605[0] < 1.0: full_now.add("tp605")
                row["605 (kept, unaimed reading, rate)"] = {k_: (KEPT605[k_], round(float(np.mean(ua["_r605_" + str(k_)])), 3) if ua.get("_r605_" + str(k_)) else None) for k_ in (1, 4, 8)} | {"rate": round(TP605[0], 3)}
            if "371" not in OFF:                                                             # 371: the unit-return rates toward the kept readings''')
P('''import lyric_p58 as L
''', '''import lyric_p58 as L
import luthier_read as LR605
''')
# 605 with 600: a line given the template's (or a returning unit's) bars takes its span from them, not from 600's draw
P('''        if D600 and not free and _try < NT // 2:                                          # 600: the first onset drawn, the last at the drawn span; the gaps fill it''',
  '''        if D600 and not free and _try < NT // 2 and not (ON18("605") and copybars and allbars):   # 600 (605: a line on the template's bars takes their span)''')
P('''        elif D600 and not free and _try == NT // 2: STATS["600: the drawn span given up for a line"] += 1
''', '''        elif D600 and not free and _try == NT // 2: STATS["600: the drawn span given up for a line"] += 1
        if ON18("605") and copybars and allbars and not free and _try < NT // 2: kind_ = None; tgt = None; LW406[0] = None   # 605: the template's bars set the entry and the landing
''')
# ---- the record ----
P('''    rerun["v137_part"] = V137;''', '''    rerun["l1_part"] = VL1; rerun["l1_on"] = sorted(f_ for f_ in PL1 if ON18(f_)); rerun["tp605"] = round(TP605[0], 4)
    rerun["l1_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("605:", "606:", "361:", "600:", "602:", "603:")}
    rerun["v137_part"] = V137;''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v137_p58.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_l1_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/run137/melody_v137_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/runl1/melody_l1_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
