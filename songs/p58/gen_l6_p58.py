"""gen_l6_p58.py: writes melody_l6_p58.py (song 48 under Luthier v6: Module 27.87, Window 163) from melody_l4_p58.py, porting 711, 712,
713, 714, 715 and 717 with luthier_judge4.py and the v6 tables; 710 and 718 are readings (read_l6.py). Every patch replaces whole statements
and is asserted to match exactly once. ZE_PART_L6=0 gives Luthier v4 as it stood.
- 711 (amends 680): a kept bar is weighed by its times sung times the geometric mean, over its gaps, of the build's capped palette share for
  the gap's class over the kept mean palette's share (the 159 kept songs' palettes averaged; the classes 655 caps renormalized as 655 does).
  The stress weight on its places stays (as in the v4 port: every syllable is placed in this engine).
- 712: a line sung again whose syllables are its source's count within one takes its source's onsets exactly, melismas included: one
  syllable fewer, the odd note a melisma begun on the source's longest note; one more, the source's own melisma note sung as a syllable, or,
  with none, its longest note split at its middle (as 682). Otherwise the line is drawn in whole kept bars (680) with as many of its source's
  bars as fit, earliest first, the source's entry and last onset as 653's kept line. Neither fitting, the line is drawn as before, counted.
- 713 (amends 683): the repeat's share of a move's weight is held under the kept windows' 75th percentile for the section's density, only
  from above; 650's power stops at the first round, after a raise, whose reading rose by under half a point (it stays as it stood in that
  round; the ease guard may still lower it); a build's mean ease is read by luthier_judge4's reader.
- 714: where 653's kept line enters after its bar line, the first bar is a kept bar whose first onset is that place.
- 715: the pick is luthier_judge4.pick over the clean survivors (no soft break), as (fp, [(onset, pitch, section)]).
- 717: a bar of three notes or more that takes no figure already sung (651) takes, at the calibrated rate R717, a kept pitch figure of its
  count (luthier_v6_kept_figures.json, drawn by times sung), set on the chord as 651 sets its figures; the rate is set in the calibration
  toward 56% of bars (three notes or more) on a figure some kept song sings (the judge's reader)."""
SRC = "/home/claude/p58/melody_l4_p58.py"; DST = "/home/claude/p58/melody_l6_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""Luthier v4 (Module 27.85; by gen_l4_p58.py''', '''"""Luthier v6 (Module 27.87; by gen_l6_p58.py from melody_l4_p58.py: 711-715, 717) -- Luthier v4 (Module 27.85; by gen_l4_p58.py''')
P('''def ON21(f_): return PL4.get(f_, 0) <= VL4 and f_ not in OFF11''', '''def ON21(f_): return PL4.get(f_, 0) <= VL4 and f_ not in OFF11
VL6 = int(_os11.environ.get("ZE_PART_L6", "1"))
PL6 = {f_: 1 for f_ in ("711", "712", "713", "714", "715", "717")}
def ON22(f_): return PL6.get(f_, 0) <= VL6 and f_ not in OFF11''')
# ---- tables and helpers ----
P('''def whole680(rng, sy, st, tmin, end, kl, A, cap, nb, palw, fixed=None):''', '''import itertools as _it6
import luthier_judge4 as J4
KF717 = {int(k_): v_ for k_, v_ in json.load(open("/home/claude/p58/tables/luthier_v6_kept_figures.json"))["figures"].items()}
_z711 = sum(MEANPAL606[0][c_] for c_ in _N655)                                        # 711: the kept mean palette (606's table), the classes 655 caps renormalized as 655 does
KMP711 = [MEANPAL606[0][c_] / _z711 if c_ in _N655 else MEANPAL606[0][c_] for c_ in range(9)]
R717 = [0.5]; ONS712 = set(); POWH650 = []; STOP650 = [None]; J4R = [None]
def j4_ease(notes):
    """713: a build's mean ease, bits a note, by the judge's reader (luthier_judge4: the kept trigram mixed with the song so far)."""
    ns = sorted([(n_["on"], n_["p"]) for n_ in notes if n_.get("p") is not None], key=lambda x_: x_[0])
    q = J4.toks(np.array([a_ for a_, _ in ns]), np.array([b_ for _, b_ in ns])); cache = J4.NG(); ez = 0.0
    for j in range(len(q)):
        pc = J4._M.ng.p(q, j); pk = cache.p(q, j, uni=False) if cache.n0 >= 8 else None; ez += -math.log2(0.5 * pc + 0.5 * pk if pk is not None else pc); cache.add(q, j)
    return ez / max(1, len(q))
def read717(notes):
    """717: the share of a build's bars of three notes or more whose pitch figure some kept song sings (the judge's reader)."""
    ns = sorted([(n_["on"], n_["p"], n_.get("sec", "")) for n_ in notes if n_.get("p") is not None], key=lambda x_: x_[0])
    B = J4.barlist(dict(t=np.array([a_ for a_, _, _ in ns]), p=np.array([b_ for _, b_, _ in ns]), sec=np.array([c_ for _, _, c_ in ns])))
    fg = [tuple(int(x) for x in np.diff(b[2])) for b in B if len(b[2]) >= 3]
    return float(np.mean([J4._M.sh[f] > 0 for f in fg])) if fg else float("nan")
def exact712(S, SU, nsy, tmin, end):
    """712: the source line's onsets exactly, as rows (onset, syllable, slur), for a line within one syllable of its source; or None."""
    src = sorted([[n_["on"] - SU, bool(n_.get("slur"))] for n_ in S], key=lambda x_: x_[0])
    if not src or src[0][1]: return None
    m = sum(1 for _, sl_ in src if not sl_); d = m - nsy
    if abs(d) > 1 or src[0][0] < tmin or src[-1][0] > end: return None
    if d == 1:                                                                            # one syllable fewer: the odd note a melisma begun on the longest note
        c_ = [(src[j + 1][0] - src[j][0], -j, j) for j in range(len(src) - 1) if not src[j + 1][1]]
        if not c_: return None
        src[max(c_)[2] + 1][1] = True
    elif d == -1:                                                                         # one more: the source's own melisma sung as a syllable, or its longest note split
        sl_ = [j for j, (_, x_) in enumerate(src) if x_]
        if sl_: src[sl_[0]][1] = False
        else:
            c_ = [(src[j + 1][0] - src[j][0], -j, j) for j in range(len(src) - 1)]
            if not c_ or max(c_)[0] < 6: return None
            g_, _, j = max(c_); src.insert(j + 1, [src[j][0] + (g_ // 2 // 3) * 3, False])
    rows = []; k = -1
    for t_, sl_ in src:
        if not sl_: k += 1
        rows.append([t_, k, sl_])
    return rows if k + 1 == nsy else None
def whole680(rng, sy, st, tmin, end, kl, A, cap, nb, palw, fixed=None):''')
# 711: the geometric mean of the palette ratio over the bar's gaps
P('''            if b_ not in fixed:
                for g_ in (y_ - x_ for x_, y_ in zip(ts_, ts_[1:])): w_ *= palw(g_)   # 680: the palette's probability of the bar's gaps''',
  '''            if b_ not in fixed:
                gg_ = [y_ - x_ for x_, y_ in zip(ts_, ts_[1:])]
                if ON22("711"):                                                            # 711: the geometric mean over the bar's gaps of the palette's ratio to the kept mean palette
                    if gg_: w_ *= float(np.prod([palw(g_) for g_ in gg_])) ** (1.0 / len(gg_))
                else:
                    for g_ in gg_: w_ *= palw(g_)                                          # 680: the palette's probability of the bar's gaps''')
# 714: the first bar's first onset at the kept line's entry
P('''            if first_ and not pk and b_ not in fixed and ((e1 == 0 and ts_[0] != b_ * BAR) or (e1 > 0 and ts_[0] <= b_ * BAR)): continue   # the entry on, or after, the bar line''',
  '''            if first_ and not pk and b_ not in fixed and ((e1 == 0 and ts_[0] != b_ * BAR) or (e1 > 0 and ts_[0] <= b_ * BAR)): continue   # the entry on, or after, the bar line
            if first_ and not pk and b_ not in fixed and ON22("714") and e1 > 0 and ts_[0] != e1: continue   # 714: the first bar's first onset at the kept line's entry''')
# 711: the ratio palette; 712: a line sung again, its source's bars first
P('''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False, span_to=None):''',
  '''def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False, span_to=None, again712=None):''')
P('''    if ON21("680") and i is not None and not fix and (not copybars or allbars) and 1 <= slot_len(sec, i) <= 4:   # 680: every drawn bar a kept bar of its count''',
  '''    if ON21("680") and i is not None and not fix and (not copybars or allbars or again712 is not None) and 1 <= slot_len(sec, i) <= 4:   # 680: every drawn bar a kept bar of its count (712: a line sung again)''')
P('''        palw_ = (lambda g_: max(0.005, cp680_[LR605.gclass(g_)])) if cp680_ is not None else (lambda g_: 1.0)''',
  '''        palw_ = (lambda g_: max(0.005, cp680_[LR605.gclass(g_)])) if cp680_ is not None else (lambda g_: 1.0)
        if ON22("711") and cp680_ is not None: palw_ = lambda g_: max(0.005, cp680_[LR605.gclass(g_)]) / KMP711[LR605.gclass(g_)]   # 711: the share over the kept mean palette's
        if again712 is not None:                                                            # 712: in whole kept bars, as many of its source's bars as fit, earliest first
            src_ = sorted(again712); by_ = collections.defaultdict(list)
            for t_ in src_:
                if 0 <= t_ < nb680_ * BAR: by_[t_ // BAR].append(t_)
            kl712_ = dict(e=int(src_[0]) if src_[0] < BAR else 0, last=int(src_[-1])); bs_ = sorted(by_)
            for keep_ in range(len(bs_), -1, -1):
                for cb_ in _it6.combinations(bs_, keep_):
                    o712_ = whole680(rng, sy, st, tmin, end, kl712_, A, cap, nb680_, palw_, {b_: sorted(by_[b_]) for b_ in cb_})
                    if o712_ is not None and len(o712_) == n:
                        W652[0] = True; W680[0] = True; MET600[(sec, i)] = True; ONS712.add(tuple(o712_))
                        STATS["712: line sung again in whole kept bars, its source's bars kept: " + str(keep_) + " of " + str(len(bs_))] += 1
                        return o712_
            STATS["712: line sung again: no whole kept bars fit; drawn as before"] += 1; again712 = None
        if ON22("714") and nb680_ == 2 and ON20("653") and kl653(rng, sec, i)["e"] > 0 and not copybars: STATS["714: drawn lines whose kept line enters after the bar line"] += 1''')
P('''        if o680_ is not None and len(o680_) == n:
            W652[0] = True; W680[0] = True; MET600[(sec, i)] = True; STATS["680: drawn line sung in whole kept bars" + (" (with the template's bars)" if copybars else "")] += 1''',
  '''        if o680_ is not None and len(o680_) == n:
            if ON22("714") and nb680_ == 2 and ON20("653") and kl653(rng, sec, i)["e"] > 0 and not copybars: STATS["714: ... of them in whole kept bars, the first onset at the entry"] += 1
            W652[0] = True; W680[0] = True; MET600[(sec, i)] = True; STATS["680: drawn line sung in whole kept bars" + (" (with the template's bars)" if copybars else "")] += 1''')
P('''    return dict(entry=entry_kind(S[0]["on"] - SU), copybars=dict(cb))''',
  '''    if ON22("712"): return dict(entry=entry_kind(S[0]["on"] - SU), copybars=dict(cb), again712=[n["on"] - SU for n in S if not n.get("slur")])   # 712
    return dict(entry=entry_kind(S[0]["on"] - SU), copybars=dict(cb))''')
# 712 in sing_again: the source's onsets exactly where the counts are within one
P('''    i_ = int(S[0]["line"].split(":")[1]) if "line" in S[0] else None
    if ons is None:
        ons = line_rhythm(sy, rng, tmin, sec, last_max, i=i_, **again_kw(S, SU))
        if ons is None: return None
    se = slot_end(sec, i_); rows = melismas(ons, rng, se if last_max is None else min(se, last_max))''',
  '''    i_ = int(S[0]["line"].split(":")[1]) if "line" in S[0] else None
    rows712_ = None
    if ON22("712"):                                                                         # 712: the source's onsets exactly, as 682 takes the template's
        se7_ = slot_end(sec, i_); rows712_ = exact712(S, SU, len(sy), tmin, se7_ if last_max is None else min(se7_, last_max))
        if rows712_ is not None: STATS["712: line sung again on its source's onsets exactly" + ("" if len(S) == len(rows712_) and sum(1 for n_ in S if not n_.get("slur")) == len(sy) else " (one syllable apart)")] += 1
        else: STATS["712: line sung again, counts more than one apart or no room: drawn"] += 1
    if ons is None and rows712_ is None:
        ons = line_rhythm(sy, rng, tmin, sec, last_max, i=i_, **again_kw(S, SU))
        if ons is None: return None
    se = slot_end(sec, i_)
    if rows712_ is not None: rows = rows712_
    elif ON22("712") and tuple(ons) in ONS712: rows = [[t_, k_, False] for k_, t_ in enumerate(ons)]   # 712: whole kept bars, no melisma added
    else: rows = melismas(ons, rng, se if last_max is None else min(se, last_max))''')
P('''        elif h == "again" and (s0, i0) in built:
            AIMP = AIM; globals()["AIM"] = AIMS[pool_of(sec)]
            ons = line_rhythm(LINES[sec][i], rng, tmin508(sec, i), sec, i=i, **again_kw(built[(s0, i0)], line_start(s0, i0))); globals()["AIM"] = AIMP''',
  '''        elif h == "again" and (s0, i0) in built:
            AIMP = AIM; globals()["AIM"] = AIMS[pool_of(sec)]
            ex712_ = exact712(built[(s0, i0)], line_start(s0, i0), len(LINES[sec][i]), tmin508(sec, i), slot_end(sec, i)) if ON22("712") else None
            if ex712_ is not None: ons = [t_ for t_, k_, sl_ in ex712_ if not sl_]                # 712: the source's onsets exactly
            else: ons = line_rhythm(LINES[sec][i], rng, tmin508(sec, i), sec, i=i, **again_kw(built[(s0, i0)], line_start(s0, i0)))
            globals()["AIM"] = AIMP''')
# 713: the hold a ceiling at the kept 75th percentile
P('''        REP683[0] = min(0.8, KREP683[SEC_BAND[sec]]["50th"] * K683[pool_of(sec)]) if ON21("683") else None''',
  '''        REP683[0] = (KREP683[SEC_BAND[sec]]["75th"] if ON22("713") else min(0.8, KREP683[SEC_BAND[sec]]["50th"] * K683[pool_of(sec)])) if ON21("683") else None   # 713: the kept 75th, a ceiling''')
P('''        if T683_ > 0 and 0 < R683_ < T683_:                                                 # held at the share, from above or below''',
  '''        if T683_ > 0 and 0 < R683_ < T683_ and (not ON22("713") or R683_ / T683_ > t683_):   # held at the share, from above or below (713: from above only)''')
# 717: a kept figure where no figure already sung is taken
P('''            if (len(ix_) >= 3 and not any(t_ // BAR == b651_ for t_ in on0_) and not (fixed and any(j in fixed for j in ix_)) and not t602b_
                    and FIGS651[0].get(len(ix_))):
                STATS["651: bars eligible"] += 1
                if rng.random() < R651[0]:
                    fg_ = rng.choice(FIGS651[0][len(ix_)]); cs_ = []; ref_ = prev if prev is not None else mu
                    chs_ = [M.chord_for(notes[j], notes_on) for j in ix_]
                    for s0_ in range(lo, hi + 1):
                        if s0_ % 12 not in M.SCALE or abs(s0_ - ref_) > 9: continue
                        qs_ = [s0_]
                        for d_ in fg_: qs_.append(qs_[-1] + d_)
                        if all(lo <= q_ <= hi and q_ % 12 in M.SUNGPC and not M.clash(q_, c_) and not tri(q_, c_) for q_, c_ in zip(qs_, chs_)):
                            cs_.append((qs_, math.exp(-(s0_ - ref_) ** 2 / (2 * 2.5 ** 2)) * chord_w(s0_, notes[i], chs_[0])))
                    if cs_ and sum(w_ for _, w_ in cs_) > 0:
                        qs_ = rng.choices([q_ for q_, _ in cs_], [w_ for _, w_ in cs_])[0]; fig_.update({j: q_ for j, q_ in zip(ix_, qs_)}); STATS["651: bar takes a figure already sung"] += 1
                    else: STATS["651: figure drawn but not placeable on the chord"] += 1''',
  '''            if (len(ix_) >= 3 and not any(t_ // BAR == b651_ for t_ in on0_) and not (fixed and any(j in fixed for j in ix_)) and not t602b_):
                def plc651_(fg_):
                    cs_ = []; ref_ = prev if prev is not None else mu
                    chs_ = [M.chord_for(notes[j], notes_on) for j in ix_]
                    for s0_ in range(lo, hi + 1):
                        if s0_ % 12 not in M.SCALE or abs(s0_ - ref_) > 9: continue
                        qs_ = [s0_]
                        for d_ in fg_: qs_.append(qs_[-1] + d_)
                        if all(lo <= q_ <= hi and q_ % 12 in M.SUNGPC and not M.clash(q_, c_) and not tri(q_, c_) for q_, c_ in zip(qs_, chs_)):
                            cs_.append((qs_, math.exp(-(s0_ - ref_) ** 2 / (2 * 2.5 ** 2)) * chord_w(s0_, notes[i], chs_[0])))
                    if cs_ and sum(w_ for _, w_ in cs_) > 0: return rng.choices([q_ for q_, _ in cs_], [w_ for _, w_ in cs_])[0]
                    return None
                tk651_ = False
                if FIGS651[0].get(len(ix_)):
                    STATS["651: bars eligible"] += 1
                    if rng.random() < R651[0]:
                        qs_ = plc651_(rng.choice(FIGS651[0][len(ix_)]))
                        if qs_ is not None: fig_.update({j: q_ for j, q_ in zip(ix_, qs_)}); STATS["651: bar takes a figure already sung"] += 1; tk651_ = True
                        else: STATS["651: figure drawn but not placeable on the chord"] += 1
                if ON22("717") and not tk651_ and KF717.get(len(ix_)):                           # 717: a kept figure of its count, at the calibrated rate, set on the chord
                    STATS["717: bars eligible (three notes or more, no figure already sung)"] += 1
                    if rng.random() < R717[0]:
                        rw_ = KF717[len(ix_)]; fg_ = rng.choices([f_ for f_, _, _ in rw_], [c_ for _, c_, _ in rw_])[0]
                        qs_ = plc651_(tuple(fg_))
                        if qs_ is not None: fig_.update({j: q_ for j, q_ in zip(ix_, qs_)}); STATS["717: bar takes a kept figure"] += 1
                        else: STATS["717: kept figure drawn but not placeable on the chord"] += 1''')
# ---- calibration ----
P('''            if ON21("683"):
                ua["_ease683"].append(read_ease(c2["notes"]))''',
  '''            if ON22("717"):
                f7_ = read717(c2["notes"])
                if np.isfinite(f7_): ua["_f717"].append(f7_)
            if ON21("683"):
                ua["_ease683"].append(j4_ease(c2["notes"]) if ON22("713") else read_ease(c2["notes"]))   # 713: the judge's reader''')
P('''                POW650[0] = float(np.clip(POW650[0] * f_, 0.05, 8.0))
                for p_ in ("V", "C"):''',
  '''                if ON22("713"):                                                              # 713: the power stops at the round, after a raise, that no longer raises the reading by half a point
                    POWH650.append((CAL_ROUNDS[0], round(POW650[0], 4), round(r_, 4)))
                    if STOP650[0] is None and len(POWH650) >= 2 and POWH650[-1][1] > POWH650[-2][1] and r_ - POWH650[-2][2] < 0.005:
                        STOP650[0] = CAL_ROUNDS[0]; print(f"713: the power stops at round {CAL_ROUNDS[0]} at {POW650[0]:.3f} (reading {r_:.3f}, round before {POWH650[-2][2]:.3f})")
                    if STOP650[0] is not None: f_ = min(1.0, f_) if (ua.get("_ease683") and float(np.nanmean(ua["_ease683"])) < 3.3) else 1.0
                    row["713: power rounds (round, power, reading)"] = list(POWH650)
                POW650[0] = float(np.clip(POW650[0] * f_, 0.05, 8.0))
                for p_ in (() if ON22("713") else ("V", "C")):''')
P('''                if f_ in (0.6, 1.6): full_now.add("pow650")''',
  '''                if f_ in (0.6, 1.6) and STOP650[0] is None: full_now.add("pow650")''')
P('''            if ON18("605") and ua.get("_r605_4"):                                             # 605: the template's rate toward 20% at four bars''',
  '''            if ON22("717") and ua.get("_f717"):                                               # 717: the rate toward 56% of bars on a figure some kept song sings
                r_ = float(np.mean(ua["_f717"])); R717[0] = float(np.clip(R717[0] + 1.5 * (0.56 - r_), 0.0, 1.0))
                if abs(0.56 - r_) > 0.08 and 0.0 < R717[0] < 1.0: full_now.add("r717")
                row["717 (kept, reading, rate)"] = dict(kept=0.56, read=round(r_, 3), rate=round(R717[0], 3))
            if ON18("605") and ua.get("_r605_4"):                                             # 605: the template's rate toward 20% at four bars''')
# ---- 715: the pick ----
P('''    print(f"362: survivors with no soft break {len(clean)} of {len(byj)}" + ("" if clean else "; none qualified: the pick is the judge's first"))''',
  '''    if ON22("715"):                                                                         # 715: the pick is the reader's, over the clean survivors
        cl715_ = [c_ for c_ in alive if not c_["info"]["soft"]]
        pk715_, R715_ = J4.pick([(c_["fp"], [(n_["on"], n_["p"], n_["sec"]) for n_ in c_["notes"]]) for c_ in cl715_])
        RD_ = {i_: r_ for i_, r_ in R715_}; old715_ = pick["fp"] if pick else None
        if pk715_ is None and RD_:
            pk715_ = min(RD_, key=lambda i_: (RD_[i_]["charge"], RD_[i_]["distance from the kept medians"])); print("715: no clean survivor eligible; the least charge among them")
        if pk715_ is not None: pick = next(c_ for c_ in cl715_ if c_["fp"] == pk715_)
        el_ = [i_ for i_, r_ in RD_.items() if r_["eligible for the pick"]]; lst_ = min([RD_[i_]["charge"] for i_ in el_]) if el_ else None
        chs_ = sorted(r_["charge"] for r_ in RD_.values()); pls_ = sorted(r_["place among kept songs"] for r_ in RD_.values())
        J4R[0] = dict(pick=pk715_, before=old715_, clean=len(cl715_), eligible=len(el_), within_002=sum(1 for i_ in el_ if RD_[i_]["charge"] <= lst_ + 0.02) if el_ else 0,
                      pick_charge=round(RD_[pk715_]["charge"], 4) if pk715_ else None, pick_place=round(RD_[pk715_]["place among kept songs"], 3) if pk715_ else None,
                      pick_distance=round(RD_[pk715_]["distance from the kept medians"], 3) if pk715_ else None,
                      median_charge=round(float(np.median(chs_)), 4) if chs_ else None, median_place=round(float(np.median(pls_)), 3) if pls_ else None,
                      most_charged=collections.Counter(k_ for r_ in RD_.values() for k_ in r_["charges"]).most_common(6),
                      per_build={i_: dict(charge=round(r_["charge"], 4), place=round(r_["place among kept songs"], 3), eligible=r_["eligible for the pick"],
                                          distance=round(r_["distance from the kept medians"], 3), charges={k_: round(v_, 3) for k_, v_ in r_["charges"].items()},
                                          components={k_: round(v_, 4) for k_, v_ in r_["components"].items()}) for i_, r_ in RD_.items()})
        print("715:", {k_: v_ for k_, v_ in J4R[0].items() if k_ != "per_build"})
    print(f"362: survivors with no soft break {len(clean)} of {len(byj)}" + ("" if clean else "; none qualified: the pick is the judge's first"))''')
P('''    rerun["l4_part"] = VL4; rerun["k683"] = dict(K683)''',
  '''    rerun["l6_part"] = VL6; rerun["l6_on"] = sorted(f_ for f_ in PL6 if ON22(f_)); rerun["r717"] = round(R717[0], 4); rerun["pow650_rounds"] = list(POWH650); rerun["stop650"] = STOP650[0]
    rerun["j4"] = J4R[0]; rerun["l6_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("711:", "712:", "713:", "714:", "717:", "680:", "682:", "683:", "651:", "653:")}
    rerun["l4_part"] = VL4; rerun["k683"] = dict(K683)''')
P('''cmd=f"ZE_PART_L4={VL4} PYTHONHASHSEED=0 python3 melody_l4_p58.py {N} {MODE}"''', '''cmd=f"ZE_PART_L6={VL6} PYTHONHASHSEED=0 python3 melody_l6_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/runl4/melody_l4_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/runl6/melody_l6_p58_{MODE}{_TAG}.pkl", "wb")''')
P('''                     calibration=cal_log, knobs=KNOBS,''', '''                     calibration=cal_log, j4=J4R[0], knobs=KNOBS,''')
open(DST, "w").write(s)
print("wrote", DST)
