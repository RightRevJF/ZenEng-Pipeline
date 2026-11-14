"""gen_l4_p58.py: writes melody_l4_p58.py (song 48 under Luthier v4: Module 27.85, Window 161) from melody_l3_p58.py (run B, ZE_PART_L3=2),
porting 680, 681, 682 and 683 with luthier_v4_tables.json; 684 and 686 are readings, 685 is how the report reads. Every patch replaces whole
statements and is asserted to match exactly once. ZE_PART_L4=0 gives Luthier v3's run B as it stood.
- 680: every drawn line, at every density and slot length, not a copy of another line, is sung in whole kept bars of their counts of notes
  (the tables of 652): a pickup as 653's kept line had it (unstressed syllables only), then the line's notes split over its bars (no empty
  bar inside the line; bars after its last may be empty), each bar a kept bar of its count, drawn by its times sung times the probability
  of its gaps under the build's capped palette (the product of the palette's shares for the classes of the gaps within the bar), and, as
  every syllable is placed in this engine, the stresses on its places (the run A port's weight). The first bar takes 653's entry; the last
  bar's last onset lies within an eighth of the kept line's where one fits, otherwise the fitting bar ending latest; nothing passes the
  line's end less 653's breath. Bars the template gives a line (605) are taken first and as they are. 308's cap holds; joins between bars
  3 to 48 twelfths. Where nothing fits, the line is drawn as before, counted. 551, 558, 578 and 600 shape no such bar.
- 681: the breath before a line sung again is the lesser of the breath drawn and what its source's entry allows, and not under 18.
- 682 (amends 633): a line on the template's bars (all of its slot's bars) takes their onsets exactly where its syllables are the template's
  count within one: one syllable fewer, the odd note is a melisma begun on the template's longest note; one more, the template's longest
  note is split at its middle (the nearest the paper's 'onset' allows the count to be met while every template onset stands). No melisma
  is added to a copied bar (a line on any copied bars takes none from the melisma pass).
- 683 (amends 650): in the walk, as 603 holds leaps, the repeat's share of a move's weight is held at the kept windows' median for the
  section's density (luthier_v4_tables.json); in the calibration a build's mean ease, bits a note as the v3 tables define it, is kept
  between 3.3 and 4.35: the power does not rise while the mean is under 3.3."""
SRC = "/home/claude/p58/melody_l3_p58.py"; DST = "/home/claude/p58/melody_l4_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""Luthier v3 (Module 27.84; by gen_l3_p58.py''', '''"""Luthier v4 (Module 27.85; by gen_l4_p58.py from melody_l3_p58.py run B: 680-683) -- Luthier v3 (Module 27.84; by gen_l3_p58.py''')
P('''VL3 = int(_os11.environ.get("ZE_PART_L3", "2"))''', '''VL3 = int(_os11.environ.get("ZE_PART_L3", "2"))
VL4 = int(_os11.environ.get("ZE_PART_L4", "1"))
PL4 = {f_: 1 for f_ in ("680", "681", "682", "683")}
def ON21(f_): return PL4.get(f_, 0) <= VL4 and f_ not in OFF11''')
# ---- the tables and the helpers ----
P('''def whole652(rng, sy, st, tmin, end, kl, A, cap):''', '''_T4 = json.load(open("/home/claude/p58/tables/luthier_v4_tables.json"))
KREP683 = _T4[next(k_ for k_ in _T4 if k_.startswith("683: repeated notes by a window's notes a bar"))]
REP683 = [None]; K683 = {"V": 1.0, "C": 1.0}; M682 = [None]; NOMEL = [False]; W680 = [False]
def read_ease(notes):
    """683: a build's mean ease, bits a note (the mean over its tokens of -log2 the ease probability, the song so far from 8 tokens)."""
    ns = sorted([n_ for n_ in notes if n_.get("p") is not None], key=lambda n_: n_["on"]); S_ = Song650(); b_ = []
    for a_, c_ in zip(ns, ns[1:]):
        x_ = tok650(c_["p"] - a_["p"], c_["on"] - a_["on"]); a2_, b2_ = S_.ctx(); b_.append(-math.log2(pe650(S_, a2_, b2_, x_))); S_.add(x_)
    return float(np.mean(b_)) if b_ else float("nan")
def whole680(rng, sy, st, tmin, end, kl, A, cap, nb, palw, fixed=None):
    """680: a drawn line in whole kept bars inside 653's entry and breath (the ruling of 13 Nov for the last bar), or None."""
    n = len(sy); e = kl["e"] if kl else 0; Lt = kl["last"] if kl else None; fixed = fixed or {}
    if st[0] and e < 0: e = 0
    pk = []
    if e < 0 and 0 not in fixed:
        full_ = list(range(e, 0, 6)); c_ = 0
        while c_ < n and not st[c_]: c_ += 1
        k0 = min(len(full_), c_, n - 1)
        pk = full_ if k0 == len(full_) else (list(range(-6 * k0, 0, 6)) if k0 > 0 else [])
    pk = [t for t in pk if t >= tmin]; k0 = len(pk); m = n - k0
    if m < 1: return None
    e1 = 0 if pk else max(0, e)
    def comps(m_, k_):
        if k_ == 1: yield (m_,); return
        for a_ in range(1, m_):
            for r_ in comps(m_ - a_, k_ - 1): yield (a_,) + r_
    cands_ = []
    for act_ in range(1, nb + 1):
        if any(b_ >= act_ for b_ in fixed): continue
        for c_ in comps(m, act_) if m >= act_ else []:
            if any(x_ > cap or (x_ not in KB652 and b_ not in fixed) for b_, x_ in enumerate(c_)): continue
            if any(len(fixed[b_]) != c_[b_] for b_ in fixed): continue
            cands_.append(c_)
    if not cands_: return None
    W_ = {}
    def wbar(b_, cnt_, kf_, first_):
        key_ = (b_, cnt_, kf_, first_)
        if key_ in W_: return W_[key_]
        rows_ = [(list(fixed[b_]), 1, 1)] if b_ in fixed else [([b_ * BAR + t for t in o_], c2_, s2_) for o_, c2_, s2_ in KB652[cnt_]]
        out_ = []
        for ts_, cs_, _s in rows_:
            if ts_[0] < tmin or ts_[-1] > end: continue
            if first_ and not pk and b_ not in fixed and ((e1 == 0 and ts_[0] != b_ * BAR) or (e1 > 0 and ts_[0] <= b_ * BAR)): continue   # the entry on, or after, the bar line
            w_ = float(cs_) * (3.0 if (first_ and not pk and e1 > 0 and ts_[0] == e1) else 1.0)
            if b_ not in fixed:
                for g_ in (y_ - x_ for x_, y_ in zip(ts_, ts_[1:])): w_ *= palw(g_)   # 680: the palette's probability of the bar's gaps
            for j_, t_ in enumerate(ts_): w_ *= A(kf_ + j_, t_)
            if w_ > 0: out_.append((ts_, w_))
        W_[key_] = out_; return out_
    mass_ = []
    for c_ in cands_:
        kf_ = k0; ms_ = 1.0
        for b_, x_ in enumerate(c_):
            ms_ *= sum(w_ for _, w_ in wbar(b_, x_, kf_, b_ == 0)); kf_ += x_
            if ms_ <= 0: break
        mass_.append(ms_)
    if sum(mass_) <= 0: return None
    for _ in range(16):
        c_ = rng.choices(cands_, mass_)[0]; out_ = list(pk); kf_ = k0; ok_ = True
        for b_, x_ in enumerate(c_):
            opt_ = [(ts_, w_) for ts_, w_ in wbar(b_, x_, kf_, b_ == 0) if not out_ or 3 <= ts_[0] - out_[-1] <= 48]
            if not opt_: ok_ = False; break
            if b_ == len(c_) - 1 and Lt is not None and b_ not in fixed:
                near_ = [x2_ for x2_ in opt_ if abs(x2_[0][-1] - Lt) <= 6]
                if near_: ts_ = rng.choices(near_, [w_ for _, w_ in near_])[0][0]; STATS["680: last bar within an eighth of the kept line's last onset"] += 1
                else: ts_ = max(opt_, key=lambda x2_: (x2_[0][-1], x2_[1]))[0]; STATS["680: last bar the fitting bar that ends latest"] += 1
            else: ts_ = rng.choices(opt_, [w_ for _, w_ in opt_])[0][0]
            out_ += ts_; kf_ += x_
        if ok_: return out_
    return None
def whole652(rng, sy, st, tmin, end, kl, A, cap):''')
P('''    DR653.clear(); SONG650[0] = Song650()''', '''    M682[0] = None; NOMEL[0] = False; W680[0] = False
    DR653.clear(); SONG650[0] = Song650()''')
# ---- 682: the template exactly (before 313's cap filters the copied bars) ----
P('''    cap = int(LONG_SHARE * n) if n >= 9 else n                                           # 308: no bar holds more than 57% of a long line
    if copybars:''', '''    cap = int(LONG_SHARE * n) if n >= 9 else n                                           # 308: no bar holds more than 57% of a long line
    M682[0] = None; NOMEL[0] = bool(copybars); W680[0] = False                             # 682: no melisma added to a copied bar
    if ON21("682") and copybars and allbars and i is not None and not fix and len(copybars) == slot_len(sec, i):   # 682: the template's bars exactly
        T682_ = sorted(t for ts_ in copybars.values() for t in ts_); d682_ = len(T682_) - n
        if abs(d682_) <= 1 and T682_ and T682_[0] >= tmin and T682_[-1] <= end:
            L682_ = [(T682_[j_ + 1] - T682_[j_], -j_, j_) for j_ in range(len(T682_) - 1)]
            if d682_ == 0: STATS["682: template bars taken exactly"] += 1; MET600[(sec, i)] = True; return T682_
            if d682_ == 1 and L682_:                                                        # one syllable fewer: a melisma begun on the template's longest note
                j_ = max(L682_)[2]; M682[0] = [(T682_[j_ + 1], j_)]; STATS["682: template bars exactly, the odd note a melisma"] += 1; MET600[(sec, i)] = True
                return T682_[:j_ + 1] + T682_[j_ + 2:]
            if d682_ == -1 and L682_:                                                       # one more: the template's longest note split at its middle
                d_, _, j_ = max(L682_)
                if d_ >= 6:
                    t_ = T682_[j_] + (d_ // 2 // 3) * 3; STATS["682: template bars exactly, the longest note split"] += 1; MET600[(sec, i)] = True
                    return sorted(T682_ + [t_])
        STATS["682: template bars not taken exactly (counts or room)"] += 1
    if copybars:''')
# ---- 680: every drawn bar whole ----
P('''    W652[0] = False
    if ON20("652") and i is not None and not fix and not copybars and slot_len(sec, i) == 2 and n * MEL504[0] / 2 >= 5.5:   # 652: a dense line in whole kept bars''',
  '''    W652[0] = False
    if ON21("680") and i is not None and not fix and (not copybars or allbars) and 1 <= slot_len(sec, i) <= 4:   # 680: every drawn bar a kept bar of its count
        nb680_ = slot_len(sec, i); tb680_ = "two-bar" if nb680_ == 2 else "all"; x680_ = n * MEL504[0] / nb680_
        cp680_ = cap655(PAL606[0][0], tb680_, cell600(x680_)) if (PAL606[0] is not None and ON20("655")) else (PAL606[0][0] if PAL606[0] is not None else None)
        palw_ = (lambda g_: max(0.005, cp680_[LR605.gclass(g_)])) if cp680_ is not None else (lambda g_: 1.0)
        fx680_ = {bb_: sorted(ts_) for bb_, ts_ in (copybars or {}).items()}                   # 680: the template's bars first, as they are
        o680_ = whole680(rng, sy, st, tmin, end, kl653(rng, sec, i) if (ON20("653") and nb680_ == 2) else None, A, cap, nb680_, palw_, fx680_)
        if o680_ is not None and len(o680_) == n:
            W652[0] = True; W680[0] = True; MET600[(sec, i)] = True; STATS["680: drawn line sung in whole kept bars" + (" (with the template's bars)" if copybars else "")] += 1
            return o680_
        STATS["680: no whole kept bars fit; the line drawn as before" + (" (template bars)" if copybars else "")] += 1
    if not ON21("680") and ON20("652") and i is not None and not fix and not copybars and slot_len(sec, i) == 2 and n * MEL504[0] / 2 >= 5.5:   # 652: a dense line in whole kept bars''')
P('''    rows = melismas(ons, rng, me_, PALS.get(KIND[sec])) if ((not fix or len(fix) < len(sy)) and not W652[0]) else [[t, k, False] for k, t in enumerate(ons)]   # 652: whole bars, no melisma added''',
  '''    rows = melismas(ons, rng, me_, PALS.get(KIND[sec])) if ((not fix or len(fix) < len(sy)) and not W652[0] and not (ON21("682") and NOMEL[0])) else [[t, k, False] for k, t in enumerate(ons)]   # 652, 680: whole bars; 682: no melisma added to a copied bar
    if M682[0]: rows = sorted(rows + [[t_, k_, True] for t_, k_ in M682[0]]); M682[0] = None   # 682: the odd note a melisma on the template''')
# ---- 681: the breath before a line sung again ----
P('''            U = line_start(sec, i); tmin = max(-12, last_on + (PREVB[0] if (ON19("631") and PREVB[0] is not None) else GAP_MIN) - U)   # 631: the breath the line before drew''',
  '''            U = line_start(sec, i); b681_ = PREVB[0] if (ON19("631") and PREVB[0] is not None) else GAP_MIN   # 631: the breath the line before drew
            if ON21("681") and how(sec, i)[0] == "again" and (how(sec, i)[1], how(sec, i)[2]) in built:   # 681: before a line sung again, no more than its source's entry allows, not under 18
                h81_ = how(sec, i); e81_ = built[(h81_[1], h81_[2])][0]["on"] - line_start(h81_[1], h81_[2]); al81_ = U + e81_ - last_on
                nb81_ = max(GAP_MIN, min(b681_, al81_))
                if nb81_ != b681_: STATS["681: the breath before a line sung again shortened to its source's entry"] += 1
                b681_ = nb81_; PREVB[0] = b681_ if PREVB[0] is not None else None
            tmin = max(-12, last_on + b681_ - U)''')
# ---- 683: repeats held, as 603 holds leaps ----
P('''        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]; SEC_USED.clear(); CURB8[0] = SEC_BAND[sec]''',
  '''        kind = KIND[sec]; mu, hi, lo = REGS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]; SEC_USED.clear(); CURB8[0] = SEC_BAND[sec]
        REP683[0] = min(0.8, KREP683[SEC_BAND[sec]]["50th"] * K683[pool_of(sec)]) if ON21("683") else None   # 683: the kept windows' median repeats for the section's density (K683 set in the calibration)''')
P('''    if DENSE603[0] and allc:                                                              # 603: a leap past a fifth held to 2% of the move's weight in a dense line''',
  '''    if REP683[0] is not None and allc:                                                    # 683: the repeat's share of the move's weight held at the kept median for the density
        R683_ = sum(w for w, k in zip(allw, allk) if k == "repeat"); T683_ = sum(allw); t683_ = REP683[0]
        if T683_ > 0 and 0 < R683_ < T683_:                                                 # held at the share, from above or below
            f683_ = t683_ * (T683_ - R683_) / ((1 - t683_) * R683_); allw = [w * f683_ if k == "repeat" else w for w, k in zip(allw, allk)]; STATS["683: repeats held at the share " + ("(lowered)" if f683_ < 1 else "(raised)")] += 1
    if DENSE603[0] and allc:                                                              # 603: a leap past a fifth held to 2% of the move's weight in a dense line''')
P('''            if ON20("650"): e6_ = read650(c2["notes"]); ua["_e650a"].append(e6_[0]); ua["_e650b"].append(e6_[1])''',
  '''            if ON20("650"): e6_ = read650(c2["notes"]); ua["_e650a"].append(e6_[0]); ua["_e650b"].append(e6_[1])
            if ON21("683"):
                ua["_ease683"].append(read_ease(c2["notes"]))
                for p_, s_ in (("V", "Verse 1"), ("C", "Chorus 1")):
                    fw_ = win_feats(c2["notes"], BAR0[s_])
                    if fw_ and np.isfinite(fw_.get("repeat", np.nan)): ua["_rep683" + p_].append((fw_["repeat"], KREP683[kband(fw_["notes_per_bar"])]["50th"]))''')
P('''                r_ = float(np.nanmean(ua["_e650a"])); f_ = float(np.clip(((0.89 - 0.5) / max(0.02, r_ - 0.5)) ** 3, 0.6, 1.6)); POW650[0] = float(np.clip(POW650[0] * f_, 0.05, 8.0))''',
  '''                r_ = float(np.nanmean(ua["_e650a"])); f_ = float(np.clip(((0.89 - 0.5) / max(0.02, r_ - 0.5)) ** 3, 0.6, 1.6))
                if ON21("683") and ua.get("_ease683"):                                        # 683: the mean ease kept inside the kept middle half, 3.3 to 4.35 bits a note
                    me_ = float(np.nanmean(ua["_ease683"]))
                    if me_ < 3.3: f_ = min(f_, 0.85)
                    elif me_ > 4.35: f_ = max(f_, 1.15)
                    row["683 (mean ease, bits a note; kept 3.3-4.35)"] = round(me_, 3)
                POW650[0] = float(np.clip(POW650[0] * f_, 0.05, 8.0))
                for p_ in ("V", "C"):                                                         # 683: the hold's share set so each window's repeats read the kept median for its density
                    if ua.get("_rep683" + p_):
                        rr_ = float(np.mean([a_ for a_, _ in ua["_rep683" + p_]])); tt_ = float(np.mean([b_ for _, b_ in ua["_rep683" + p_]]))
                        K683[p_] = float(np.clip(K683[p_] * np.clip(tt_ / max(0.02, rr_), 0.6, 1.6), 0.3, 3.0))
                        row["683 (" + p_ + " window repeats: kept median, read, factor)"] = (round(tt_, 3), round(rr_, 3), round(K683[p_], 3))''')
# ---- the record ----
P('''    rerun["l3_part"] = VL3;''', '''    rerun["l4_part"] = VL4; rerun["k683"] = dict(K683); rerun["l4_on"] = sorted(f_ for f_ in PL4 if ON21(f_))
    rerun["l4_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("680:", "681:", "682:", "683:", "650:", "651:", "652:", "653:", "655:", "656:", "605:", "633:")}
    rerun["l3_part"] = VL3;''')
P('''cmd=f"ZE_PART_L3={VL3} PYTHONHASHSEED=0 python3 melody_l3_p58.py {N} {MODE}"''', '''cmd=f"ZE_PART_L4={VL4} PYTHONHASHSEED=0 python3 melody_l4_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/runl3/melody_l3p{VL3}_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/runl4/melody_l4_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
