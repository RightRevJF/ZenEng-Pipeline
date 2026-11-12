"""v127 Run 2, Parts 2 and 3: the patches gen_v127.py adds after Parts 0 and 1. Each fix is gated by ON7() on its part (ZE_PART), and with it off
every weight is multiplied by exactly 1.0 and no draw is added, so the earlier parts' runs reproduce from these files.
  Part 2: 452 (gaps equal to the one before at 38%, the longest run of equal gaps at the kept figure for the section's notes a bar, three moves
          that zigzag at 32%), 455 (the sixteenth-gap weight by band), 406 (the landing drawn jointly with the kept table), 457 (unit-return lines
          strictly on the unit's onsets for half their tries). 465 and 458 wait for their kept tables (not in the session's tables).
  Part 3: 408 with 468 (257's contour aimed at the kept turns; 400's knob at 0.5 or above), 467 (392's chorus floor no higher than the top less
          eight; the window's range aimed at the kept mean by the register's spread), 461 with 450 (398's first-beat knob by section; the chorus's
          first-beat third at 27%; notes a second or seventh from the bass at 19%), 456 (readings)."""
def P(old, new, count=1, songs=None): return (old, new, count, songs)
PATCHES = [
    # ---- the knobs, from one
    P('ct398=1.0, ctb398=1.0, ctd398=1.0, res398=1.0, turn400=1.0, ff424=1.0, lt424=1.0, eb424=0.25)',
      'ct398=1.0, ctb398=1.0, ctd398=1.0, res398=1.0, turn400=1.0, ff424=1.0, lt424=1.0, eb424=0.25, gs452=1.0, er452=1.0, zz452=1.0, ctd398V=1.0, ctd398C=1.0, th461=1.0, sb461=1.0, rg467=1.0, sh408=1.0)'),
    P('RUNR = {b_: 1.0 for b_ in RUN_KEPT_BAND}',
      'S16B = {b_: 1.0 for b_ in RUN_KEPT_BAND}                                                 # 455: the sixteenth-gap weight by band\nRUNR = {b_: 1.0 for b_ in RUN_KEPT_BAND}'),
    P('PICK108 = [None, None]\n',
      'PICK108 = [None, None]\n'
      'ZZ452 = [0, 0]; LW406 = [None]\n'
      'ER452 = {"3.5 to 4.5": 4.582, "4.5 to 5.5": 5.5, "5.5 to 9": 6.172}                         # 452: the kept longest run of equal gaps by notes a bar (zeneng_v125_port_reread.json)\n'
      'def er_kept(npb): return ER452["3.5 to 4.5"] if npb < 4.5 else ER452["4.5 to 5.5"] if npb < 5.5 else ER452["5.5 to 9"]\n'
      'def outer_reads(notes, b0):\n'
      '    """461: the window\'s first-beat notes on a chord tone and on the third; notes a second or seventh above the root (the bass), as Window 143 reads them."""\n'
      '    W_ = [n_ for n_ in notes if b0 * BAR <= n_["on"] < (b0 + 8) * BAR]\n'
      '    if len(W_) < 12: return None\n'
      '    rel_ = [((n_["p"] - M.CH[M.chord_at(n_["on"])][0]) % 12, n_["p"] % 12 in M.CH[M.chord_at(n_["on"])][1], n_["on"] % BAR == 0) for n_ in W_]\n'
      '    db_ = [x_ for x_ in rel_ if x_[2]]\n'
      '    return dict(db_ct=float(np.mean([x_[1] for x_ in db_])) if len(db_) >= 3 else None, db_third=float(np.mean([x_[0] in (3, 4) for x_ in db_])) if len(db_) >= 3 else None,\n'
      '                sb=float(np.mean([x_[0] in (1, 2, 10, 11) for x_ in rel_])))\n'),
    # ---- 455: the sixteenth-gap weight by band
    P('if "354" not in OFF: w *= LK["s16"] if d in (3, 9) else',
      'if "354" not in OFF: w *= (LK["s16"] * (S16B.get(SEC_BAND[sec], 1.0) if ON7("455") else 1.0)) if d in (3, 9) else'),
    P('RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0))',
      'RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0)); S16B[b_] = float(np.clip(S16B[b_] * f_, 0.05, 5.0)) if ON7("455") else S16B[b_]'),
    # ---- 406: the landing drawn with the rhythm, weighted by the landing shares
    P('def land_draw(rng, sec, n_syl, i=None, allowed=None):\n',
      'def land_w406(sec, n_syl, i=None, allowed=None):\n'
      '    """406: the landing\'s weight at each place, by Window 124\'s line ends (each class\'s share spread over its places), for the joint draw."""\n'
      '    nb = slot_len(sec, i); lo_ = 0 if nb == 1 else (nb - 1) * BAR - 24; hi_ = slot_end(sec, i)\n'
      '    cls = lambda t: "b1" if t % BAR == 0 else "b3" if t % BAR == 24 else "b24" if t % BEAT == 0 else "off"\n'
      '    opts = [t for t in range(lo_, hi_ + 1, 6)]\n'
      '    if allowed is not None: opts = [t for t in opts if t in allowed] or sorted(allowed)\n'
      '    sh = dict(b1=0.26, b3=0.10) if is_title(sec, i) else dict(LAND_SH); cnt = collections.Counter(cls(t) for t in opts)\n'
      '    return {t: sh.get(cls(t), 0.0) / cnt[cls(t)] for t in opts}\n'
      'def land_draw(rng, sec, n_syl, i=None, allowed=None):\n'),
    P('        if PIN388 and not free and Ls not in fix: tgt = None; STATS["388: landing left to the draw (side run)"] += 1\n',
      '        if PIN388 and not free and Ls not in fix: tgt = None; STATS["388: landing left to the draw (side run)"] += 1\n'
      '        LW406[0] = None\n'
      '        if ON7("406") and not free and Ls not in fix and tgt is not None:                     # 406: the landing drawn jointly with the kept table\n'
      '            LW406[0] = land_w406(sec, n, i, (al_ if fits is not None else (spa or None))); tgt = None; STATS["406: landing drawn with the rhythm"] += 1\n'),
    # ---- 457: a unit-return line strictly on the unit's onsets, falling back at half its tries
    P('        alpha, cbw = dp(kind_, tgt, cb, sb)\n',
      '        st457 = set(cb) if (ON7("457") and allbars and cb and _try < NT // 2) else ()\n'
      '        if ON7("457") and allbars and cb and _try == NT // 2: STATS["457: unit-return line falls back to the weighted copy"] += 1\n'
      '        alpha, cbw = dp(kind_, tgt, cb, sb, strict=st457)\n'),
    # ---- 452 and 406 in the draw of the onsets (backward from the last)
    P('            ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) for x in ks]\n',
      '            lw_ = LW406[0]; ert_ = int(er_kept(SEC_NPB[sec])); rl_ = [0]\n'
      '            ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) * (lw_.get(x[0], 0.0) if (lw_ is not None and Ls == n - 1) else 1.0) for x in ks]\n'),
    P('                ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) for x in ks]\n'
      '                if not ks or sum(ws) <= 0: return None\n'
      '                cur = rng.choices(ks, ws)[0]; ons.append(cur[0])\n',
      '                g_ = (ons[-2] - t) if len(ons) >= 2 else None\n'
      '                def e452(d_):                                                                    # 452: a gap equal to the one after it; a run past the kept figure\n'
      '                    if not ON7("452") or g_ is None or d_ != g_: return 1.0\n'
      '                    return LK["gs452"] * (LK["er452"] if rl_[0] + 1 > ert_ else 1.0)\n'
      '                ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) * e452(t - x[0]) * (lw_.get(x[0], 0.0) if (lw_ is not None and k - 1 == Ls) else 1.0) for x in ks]\n'
      '                if not ks or sum(ws) <= 0: return None\n'
      '                cur = rng.choices(ks, ws)[0]; ons.append(cur[0]); rl_[0] = (rl_[0] + 1) if (g_ is not None and t - cur[0] == g_) else 1\n'),
    # ---- 452: three moves that zigzag, in the walk
    P('    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None\n',
      '    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None; ZZ452[0] = ZZ452[1] = 0\n'),
    P('        run = run + 1 if p == prev else 1\n',
      '        if prev is not None and p != prev: ZZ452[0], ZZ452[1] = ZZ452[1], (1 if p > prev else -1)   # 452: the last two moves\n'
      '        run = run + 1 if p == prev else 1\n'),
    P('                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0\n',
      '                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0\n'
      '                if ON7("452") and sz and ZZ452[0] and ZZ452[1] and sg != ZZ452[1] and ZZ452[1] != ZZ452[0]: w0 *= LK["zz452"]   # 452: a third move that zigzags\n'),
    # ---- 408: 257's contour aimed at the kept turns (its width a knob); 467: the register's spread a knob
    P('sf = math.exp(-(p - SHAPE[0]) ** 2 / (2 * 2.5 ** 2)) if SHAPE is not None else 1.0',
      'sf = math.exp(-(p - SHAPE[0]) ** 2 / (2 * (2.5 * (LK["sh408"] if ON7("408") else 1.0)) ** 2)) if SHAPE is not None else 1.0'),
    P('(2 * M.RSD ** 2)', '(2 * (M.RSD * (LK["rg467"] if ON7("467") else 1.0)) ** 2)', 2),
    # ---- 467 (song 45): 392's chorus floor no higher than the chorus top less eight
    P('cl_ = max(lo, min(ch_ - 3, int(round(vm_ + 3)))) if ON("392")', 'cl_ = max(lo, min(ch_ - (8 if ON7("467") else 3), int(round(vm_ + 3)))) if ON("392")', 1, ("45",)),
    # ---- 461 with 450: 398's first-beat knob by section; the chorus's first-beat third; a second or seventh from the bass
    P('(LK["ctd398"] if n["on"] % BAR == 0 else 1.0)', '((LK["ctd398" + AIM.p] if ON7("461") else LK["ctd398"]) if n["on"] % BAR == 0 else 1.0)'),
    P('    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]',
      '    if ON7("461") and DRAWN398[0]:                                                         # 461: the chorus\'s first-beat third; 450: a second or seventh from the bass\n'
      '        r461 = (p - M.CH[ch][0]) % 12\n'
      '        if AIM.p == "C" and n["on"] % BAR == 0 and r461 in (3, 4) and p % 12 in tones: w *= LK["th461"]\n'
      '        if r461 in (1, 2, 10, 11): w *= LK["sb461"]\n'
      '    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]'),
    # ---- the calibration: the new aims read on unaimed builds
    P('                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])\n        row["338: unaimed builds read"] = k2\n',
      '                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua[m_].append(f_[m_])\n'
      '                if V127 >= 2:                                                                 # v127: 452, 461, 467 read on the same windows\n'
      '                    N_ = sorted(win_N(c2["notes"], BAR0[s_])); c_ = cand(N_) if N_ else None\n'
      '                    if c_ and ON7("452"):\n'
      '                        ua["_gs452"].append(c_["gap_same_as_before"]); ua["_er452"].append(c_["equal_gap_run_max"] / er_kept(len(N_) / 8))\n'
      '                        if np.isfinite(c_["zigzag_of_three"]): ua["_zz452"].append(c_["zigzag_of_three"])\n'
      '                    if ON7("467") and N_: ua["_rng467"].append(max(x_[2] for x_ in N_) - min(x_[2] for x_ in N_))\n'
      '                    o_ = outer_reads(c2["notes"], BAR0[s_]) if ON7("461") else None\n'
      '                    if o_:\n'
      '                        if o_["db_ct"] is not None: ua["_ctd" + pool_of(s_)].append(o_["db_ct"])\n'
      '                        if s_ == "Chorus 1" and o_["db_third"] is not None: ua["_th461"].append(o_["db_third"])\n'
      '                        ua["_sb461"].append(o_["sb"])\n'
      '        row["338: unaimed builds read"] = k2\n'),
    P('                for kn_, m_ in (("ct398", "chord_tones"), ("ctb398", "chord_tones_on_beat"), ("ctd398", "chord_tones_on_downbeat"), ("res398", "non_chord_resolved_by_step")):\n'
      '                    if not ua.get(m_): continue\n',
      '                for kn_, m_ in (("ct398", "chord_tones"), ("ctb398", "chord_tones_on_beat"), ("ctd398", "chord_tones_on_downbeat"), ("res398", "non_chord_resolved_by_step")):\n'
      '                    if not ua.get(m_): continue\n'
      '                    if kn_ == "ctd398" and ON7("461"): continue                                 # 461: the first-beat knob by section (below)\n'),
    P('            if ON("400") and ua.get("turns_per_move"):',
      '            def aim7(kn_, key_, t_, lo_=0.05, hi_=20.0, pw_=2):                                 # v127: one knob a measure, toward its kept figure, on unaimed builds\n'
      '                if not ua.get(key_): return None\n'
      '                r_ = float(np.mean(ua[key_])); f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** pw_, 0.6, 1.6)); LK[kn_] = float(np.clip(LK[kn_] * f_, lo_, hi_))\n'
      '                if f_ in (0.6, 1.6): full_now.add(kn_)\n'
      '                return (t_, round(r_, 3), round(LK[kn_], 3))\n'
      '            if ON7("452"):\n'
      '                row["452 (kept, unaimed reading, knob)"] = dict(gap_same_as_before=aim7("gs452", "_gs452", 0.38), zigzag_of_three=aim7("zz452", "_zz452", 0.32),\n'
      '                                                            equal_gap_run_over_kept=aim7("er452", "_er452", 1.0, 0.02, 5.0))\n'
      '            if ON7("461"):\n'
      '                row["461 (kept, unaimed reading, knob)"] = dict(verse_first_beat=aim7("ctd398V", "_ctdV", KEPT398["chord_tones_on_downbeat"], 0.1, 10.0),\n'
      '                                                            chorus_first_beat=aim7("ctd398C", "_ctdC", KEPT398["chord_tones_on_downbeat"], 0.1, 10.0),\n'
      '                                                            chorus_first_beat_third=aim7("th461", "_th461", 0.27, 0.1, 10.0), second_or_seventh=aim7("sb461", "_sb461", 0.19, 0.1, 10.0))\n'
      '            if ON7("467"): row["467 (kept, unaimed reading, knob)"] = aim7("rg467", "_rng467", 10.895, 0.5, 3.0, 1)\n'
      '            if ON7("408") and ua.get("turns_per_move"):                                      # 408: 257\'s contour width toward the kept turns (narrower turns less)\n'
      '                r_ = float(np.mean(ua["turns_per_move"])); f_ = float(np.clip((KEPT400 / max(0.05, r_)) ** 2, 0.6, 1.6)); LK["sh408"] = float(np.clip(LK["sh408"] * f_, 0.2, 3.0))\n'
      '                row["408 (kept, unaimed reading, knob)"] = (KEPT400, round(r_, 3), round(LK["sh408"], 3))\n'
      '            if ON("400") and ua.get("turns_per_move"):'),
    P('LK["turn400"] = float(np.clip(LK["turn400"] * f_, 0.1, 10.0))', 'LK["turn400"] = float(np.clip(LK["turn400"] * f_, 0.5 if ON7("468") else 0.1, 10.0))   # 468: held at a half or above'),
    P('    rerun["v127_part"] = V127;', '    rerun["knobs127"] = {k_: round(LK[k_], 4) for k_ in ("gs452", "er452", "zz452", "ctd398V", "ctd398C", "th461", "sb461", "rg467", "sh408", "turn400")} | {"s16_by_band": {b_: round(v_, 4) for b_, v_ in S16B.items()}}\n    rerun["v127_part"] = V127;'),
]
