"""v128 Run 3 (ZenEng v128, Module 27.72): the session's 480-496 as ruled, ported onto Run 2's Part 3 code (songs/p53, melody_v127_*.py).
Every patch replaces whole statements, matched the stated number of times in each file it names (384). The parts are switched by ZE_PART
(default 3), and with a part's fixes off every weight is multiplied by exactly 1.0 and no draw is added, so ZE_PART=0 reproduces Run 2's
Part 3 and each part's runs can be made again from the final files:
  part 0: Run 2's Part 3 as it was (v127 at ZE_PART=3, the v126 judge)
  part 1, clean-up: 491 (467's knob on the walk's spread and 408's on the contour's width withdrawn; song 45's chorus floor no lower than its
         lift allows), 476 (the v128 judge), 465 and 458 (from zeneng_v128_kept_lines.json), 484 (435's rate aimed at the kept pitch kept),
         478 (verse 2's repeats and steps at verse 1's rates; 434's bar on repeats lifted), 486 (389's rates read on the judged sections),
         489 (452's knobs by band of density), 490 (a weight on a sixteenth that follows a sixteenth, by band), 494 (457 falls back at once)
  part 2, the chart: 438, 440, the chord at the note (gen_v128_parts23.py)
  part 3, the bass: 439, 444-449 (bass_v128.py; no melody rerun)
Usage: python3 gen_v128.py  (writes /home/claude/p54/melody_v128_p40.py ... _p45.py)"""
import os, sys
SRC = "/home/claude/p53"; DST = os.environ.get("GEN_DST", "/home/claude/p54")
SONGS = ("40", "42", "43", "44", "45")
HEADER = '''"""ZenEng v128 Run 3 (Module 27.72) onto Run 2's Part 3 (songs/p53), by gen_v128.py. ZE_PART: 0 = Run 2's Part 3 as it was; 1 = and 491,
476, 465, 458, 484, 478, 486, 489, 490, 494; 2 = and 438, 440, the chord at the note. ZE_OFF switches a fix off (side runs only); ZE_465 = A or B.
"""
import os as _os8
V128 = int(_os8.environ.get("ZE_PART", "3"))                                                  # v128 Run 3: the parts, runs between them
P128 = {f_: 1 for f_ in ("491", "476", "465", "458", "484", "478", "486", "489", "490", "494")} | {f_: 2 for f_ in ("438", "440", "at_note")}
OFF8 = set(filter(None, _os8.environ.get("ZE_OFF", "").split(",")))
def ON8(f_): return P128.get(f_, 0) <= V128 and f_ not in OFF8
OPT465 = _os8.environ.get("ZE_465", "A")                                                     # 465: A, class 0 through the next line's pickup; B, the slot's classes alone
'''
def P(old, new, count=1, songs=None): return (old, new, count, songs)

# the 465 and 458 tables, read once here and written into the engine as constants (zeneng_v128_kept_lines.json)
import json
KL = json.load(open("/home/claude/p54/tables/zeneng_v128_kept_lines.json"))
T465 = KL["465: where a kept line's last onset falls before the next line, by notes in the line"]
K_CLS = "the last onset's bar, counted back from the bar in which the next line begins (0 = the same bar, 1 = the bar before, 2, 3 or more): share of lines"
SH465 = [(5, [T465["3 to 5"][K_CLS][k] for k in ("0", "1", "2", "3 or more")]), (8, [T465["6 to 8"][K_CLS][k] for k in ("0", "1", "2", "3 or more")]),
         (12, [T465["9 to 12"][K_CLS][k] for k in ("0", "1", "2", "3 or more")]), (999, [T465["13 and over"][K_CLS][k] for k in ("0", "1", "2", "3 or more")])]
T458 = KL["458: syllables a second across a kept line's sung span, by notes in the line"]
K_R = "notes a second, first onset to the end of the last note (5, 25, 50, 75, 95)"
R458 = [(5, T458["3 to 5"][K_R]), (8, T458["6 to 8"][K_R]), (12, T458["9 to 12"][K_R]), (999, T458["13 and over"][K_R])]

PART1 = [
    # ---- the parts: v127's fixes stay at its Part 3; 491 withdraws 467's knob and 408's
    P('V127 = int(os.environ.get("ZE_PART", "3"))', 'V127 = 3'),
    P('def ON7(f_): return P127.get(f_, 0) <= V127 and f_ not in OFF\n',
      'def ON7(f_): return P127.get(f_, 0) <= V127 and f_ not in OFF and not (f_ in ("408", "467") and ON8("491"))   # 491: 467\'s knob and 408\'s withdrawn\n'),
    # ---- 491 (song 45): the chorus floor no lower than the lift allows: the register's centre a semitone over the verse's median and three
    P('cl_ = max(lo, min(ch_ - (8 if ON7("467") else 3), int(round(vm_ + 3)))) if ON("392")',
      'cl_ = (max(lo, min(ch_ - 3, int(round(vm_ + 3)), max(ch_ - 8, int(round(2 * (vm_ + 3) - ch_ + 2))))) if ON8("491") else max(lo, min(ch_ - (8 if ON7("467") else 3), int(round(vm_ + 3))))) if ON("392")', 1, ("45",)),
    # ---- 476: the v128 judge (fitted with every song in its own key)
    P('RJ = json.load(open(f"{H118}/tables/zeneng_v126_judge.json"))["content_judge"]',
      'RJ = json.load(open(f"{H118}/tables/" + ("zeneng_v128_judge.json" if ON8("476") else "zeneng_v126_judge.json")))["content_judge"]'),
    # ---- 458: the span's bounds from kept lines' notes a second across the sung span, by notes in the line (25th to 75th)
    P('        T_ = span_to * M.SEC_PER_TW; d_ = (n / (2.3 * T_), n / (1.4 * T_)); a_, b_ = max(sp[0], d_[0]), min(sp[1], d_[1])\n',
      '        T_ = span_to * M.SEC_PER_TW; rq_ = next(q_ for k_, q_ in R458 if n <= k_) if ON8("458") else (None, 1.4, None, 2.3, None)   # 458: the kept 25th-75th by notes\n'
      '        d_ = (n / (rq_[3] * T_), n / (rq_[1] * T_)); a_, b_ = max(sp[0], d_[0]), min(sp[1], d_[1])\n'
      '        if ON8("458"): STATS["458: span read against the kept rate by notes"] += 1\n'),
    # ---- 465: the class of the last onset's bar, drawn by the kept share for the line's notes, among the classes the slot allows
    P('PICK108 = [None, None]\n',
      'PICK108 = [None, None]\n'
      f'SH465 = {SH465!r}                                                                        # 465 (zeneng_v128_kept_lines.json): 0, 1, 2, 3+ bars back\n'
      f'R458 = {R458!r}                                                                          # 458: notes a second, first onset to the end of the last note\n'
      'C465 = [None]; CLS465 = [None]; REQ465 = {}; CURB8 = [None]; AGAIN478 = [False]\n'
      'def set465(sec, i, nxt, f0, tmin):\n'
      '    """465: what the next line\'s first onset is known to be (a prefitted copy) or may be (a drawn line: on its slot\'s bar, or a pickup)."""\n'
      '    C465[0] = None; CLS465[0] = None\n'
      '    if not ON8("465") or not nxt or nxt[0] != sec or SPAN_TO[0] is None: return\n'
      '    nb_ = slot_len(sec, i)\n'
      '    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]))\n'
      'def draw465(rng, n, tmin, end, step, feas=None):\n'
      '    """465: the class drawn, and the bar its last onset must fall in (relative ticks), or None."""\n'
      '    c_ = C465[0]\n'
      '    if c_ is None: return None\n'
      '    sh_ = next(s_ for k_, s_ in SH465 if n <= k_); lo_l = tmin + step * (n - 1); opts = []\n'
      '    if c_["f0"] is not None:\n'
      '        Nb = (c_["nb"] * BAR + c_["f0"]) // BAR\n'
      '        for k_ in range(4): opts.append((k_, Nb - k_, None))\n'
      '    else:\n'
      '        Nb = c_["nb"]\n'
      '        if OPT465 == "A" and c_["pk"]: opts.append((0, Nb - 1, "pickup"))\n'
      '        for k_ in range(1, 4): opts.append((k_, Nb - k_, "no pickup" if OPT465 == "A" else None))\n'
      '    ok_ = []\n'
      '    for k_, lb_, rq_ in opts:\n'
      '        a_ = -10 ** 6 if k_ == 3 else lb_ * BAR; b_ = (lb_ + 1) * BAR - 1\n'
      '        if rq_ == "pickup": b_ = min(b_, c_["nb"] * BAR - 6 - GAP_MIN)\n'
      '        a_, b_ = max(a_, lo_l), min(b_, end)\n'
      '        if a_ <= b_ and sh_[k_] > 0 and (feas is None or feas(a_, b_)): ok_.append((k_, a_, b_, rq_))\n'
      '    if not ok_: STATS["465: no class the slot allows"] += 1; return None\n'
      '    k_, a_, b_, rq_ = rng.choices(ok_, [sh_[x_[0]] for x_ in ok_])[0]\n'
      '    STATS[f"465: class {k_} drawn"] += 1\n'
      '    return dict(k=k_, lo=a_, hi=b_, req=rq_, nxt=c_["nxt"])\n'),
    P('    s_span = rng.uniform(*sp) if sp else None\n',
      '    s_span = rng.uniform(*sp) if sp else None\n'

      '    rq465 = REQ465.pop((sec, i), None) if ON8("465") else None                             # 465: the line before asked this one to pick up, or not\n'),
    P('            if kind_ == "pickup" and st[0] and fits is None: kind_ = rng.choices(["on", "after"], [ENTRY["on"], ENTRY["after"]])[0]\n',
      '            if kind_ == "pickup" and st[0] and fits is None: kind_ = rng.choices(["on", "after"], [ENTRY["on"], ENTRY["after"]])[0]\n'
      '            if rq465 and _try < NT // 2:                                                       # 465: the entry the line before was drawn for\n'
      '                if rq465 == "pickup" and "pickup" in ek and not st[0]: kind_ = "pickup"\n'
      '                elif rq465 == "no pickup" and kind_ == "pickup":\n'
      '                    ek2 = [k_ for k_ in ek if k_ != "pickup"]\n'
      '                    if ek2: kind_ = rng.choices(ek2, [ENTRY[k_] for k_ in ek2])[0]\n'
      '            if rq465 and _try == NT // 2: STATS["465: the entry asked for given up"] += 1\n'),
    P('            ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) * (lw_.get(x[0], 0.0) if (lw_ is not None and Ls == n - 1) else 1.0) for x in ks]\n',
      '            ks = list(alpha[n - 1]); ws = [alpha[n - 1][x] * (1.0 + (end - x[0]) / 40) * (lw_.get(x[0], 0.0) if (lw_ is not None and Ls == n - 1) else 1.0) for x in ks]\n'
      '            if h465: ws = [w_ * (1.0 if d465["lo"] <= x[0] <= d465["hi"] else 0.0) for w_, x in zip(ws, ks)]   # 465: the last onset in its drawn bar\n'),
    P('        return ons\n    return None\nRATE293 = [0.40]',
      '        if h465:                                                                           # 465: held to the end: the melisma\'s bar, and the next line\'s entry\n'
      '            CLS465[0] = d465; STATS["465: line ends in its drawn bar"] += 1\n'
      '            if d465["req"]: REQ465[d465["nxt"]] = d465["req"]\n'
      '        return ons\n    return None\nRATE293 = [0.40]'),
    P('drawable405={}); CUR405[0] = meta["drawable405"]', 'drawable405={}); CUR405[0] = meta["drawable405"]; REQ465.clear()'),
    # 465: the class drawn among those the slot and the rhythm's rules can reach (the cap, the palette, the grid), read off the unweighted lattice
    P('    fits = None\n    if n >= 9 and not fix:',
      '    d465 = None\n'
      '    if span_to is not None and not fix and C465[0] is not None:                             # 465\n'
      '        a465_ = dp(None, None, {})[0][n - 1]\n'
      '        d465 = draw465(rng, n, tmin, end, step, lambda a_, b_: any(a_ <= t_ <= b_ for (t_, c_) in a465_))\n'
      '    C465[0] = None\n'
      '    fits = None\n    if n >= 9 and not fix:'),
    # 465 held for the first half of the tries, with a landing the draw sets (not a free or fixed one)
    P('        st457 = set(cb) if (ON7("457") and allbars and cb and _try < NT // 2) else ()\n',
      '        h465 = bool(d465 is not None and _try < NT // 2 and not free and tgt is None)\n'
      '        if d465 is not None and _try == NT // 2: STATS["465: class given up for a line"] += 1\n'
      '        if d465 is not None and tgt is not None and not free and _try == 0: STATS["465: landing fixed elsewhere, class not held"] += 1\n'
      '        st457 = set(cb) if (ON7("457") and allbars and cb and _try < NT // 2 and not fb457[0]) else ()\n'),
    # 465 with 378: the span's share drawn inside what the drawn bar allows, while the class is held
    P('            E0 = f0g + s_span * (span_to - f0g)\n',
      '            if d465 is not None and _try < NT // 2 and sp:                                    # 465: the share drawn again inside the drawn bar\'s reach\n'
      '                lo_s = (d465["lo"] + 3 - f0g) / max(1, span_to - f0g); hi_s = (d465["hi"] + 48 - f0g) / max(1, span_to - f0g); a_s, b_s = max(sp[0], lo_s), min(sp[1], hi_s)\n'
      '                if a_s <= b_s: s_span = rng.uniform(a_s, b_s); STATS["465: span share drawn inside the bar\'s reach"] += 1\n'
      '                else: STATS["465: span band and the bar apart"] += 1\n'
      '            E0 = f0g + s_span * (span_to - f0g)\n'),
    # ---- 494: 457 falls back as soon as no entry and landing fit the strict copy
    P('        alpha, cbw = dp(kind_, tgt, cb, sb, strict=st457)\n',
      '        alpha, cbw = dp(kind_, tgt, cb, sb, strict=st457)\n'
      '        if st457 and ON8("494") and not alpha[n - 1]:                                         # 494: nothing fits the strict copy: the weighted copy at once\n'
      '            fb457[0] = True; STATS["494: unit-return line falls back at once (no entry and landing fit)"] += 1; alpha, cbw = dp(kind_, tgt, cb, sb, strict=())\n'),
    P('    NT = 20 if copybars else 14\n', '    NT = 20 if copybars else 14; fb457 = [False]\n'),
    # 465: a final melisma inside the drawn bar
    P('    if E_ is not None: me_ = min(me_, int(E_) - 3)                                          # 378: a final melisma inside the span\n',
      '    if E_ is not None: me_ = min(me_, int(E_) - 3)                                          # 378: a final melisma inside the span\n'
      '    if CLS465[0] is not None: me_ = min(me_, (CLS465[0]["hi"] // BAR + 1) * BAR - 1); CLS465[0] = None   # 465: the last note in its bar\n'),
    P('                ns = fresh_line(sy, rng, U, tmin, sec, last_max, ',
      '                set465(sec, i, nxt, f0, tmin); ns = fresh_line(sy, rng, U, tmin, sec, last_max, '),
    # ---- 489: the band of the section being walked (452's zigzag knob by band)
    P('AIM = AIMS[pool_of(sec)]; SEC_USED.clear()', 'AIM = AIMS[pool_of(sec)]; SEC_USED.clear(); CURB8[0] = SEC_BAND[sec]'),
    P('                if ON7("452") and sz and ZZ452[0] and ZZ452[1] and sg != ZZ452[1] and ZZ452[1] != ZZ452[0]: w0 *= LK["zz452"]   # 452: a third move that zigzags\n',
      '                if ON7("452") and sz and ZZ452[0] and ZZ452[1] and sg != ZZ452[1] and ZZ452[1] != ZZ452[0]: w0 *= LK["zz452"] * (B489[CURB8[0]]["zz"] if (ON8("489") and CURB8[0] in B489) else 1.0)   # 452; 489: by band\n'),
    P('                    return LK["gs452"] * (LK["er452"] if rl_[0] + 1 > ert_ else 1.0)\n',
      '                    b_ = B489.get(SEC_BAND[sec]) if ON8("489") else None\n'
      '                    return LK["gs452"] * (b_["gs"] if b_ else 1.0) * ((LK["er452"] * (b_["er"] if b_ else 1.0)) if rl_[0] + 1 > ert_ else 1.0)   # 489: by band\n'),
    # ---- 490: a weight on a sixteenth that follows a sixteenth (an onset in a run), by band
    P('                ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) * e452(t - x[0]) * (lw_.get(x[0], 0.0) if (lw_ is not None and k - 1 == Ls) else 1.0) for x in ks]\n',
      '                r490_ = R490.get(SEC_BAND[sec], 1.0) if (ON8("490") and t % 6 == 3 and g_ == 3) else 1.0   # 490: t on a sixteenth with a sixteenth after it\n'
      '                ws = [alpha[k - 1][x] * tw(x[0], k, t - x[0]) * e452(t - x[0]) * (r490_ if t - x[0] == 3 else 1.0) * (lw_.get(x[0], 0.0) if (lw_ is not None and k - 1 == Ls) else 1.0) for x in ks]\n'),
    P('S16B = {b_: 1.0 for b_ in RUN_KEPT_BAND}                                                 # 455: the sixteenth-gap weight by band\n',
      'S16B = {b_: 1.0 for b_ in RUN_KEPT_BAND}                                                 # 455: the sixteenth-gap weight by band\n'
      'R490 = {b_: 1.0 for b_ in RUN_KEPT_BAND}                                                 # 490: the weight on an onset in a run, by band\n'
      'B489 = {b_: dict(gs=1.0, er=1.0, zz=1.0) for b_ in RUN_KEPT_BAND}                         # 489: 452\'s knobs by band of density\n'),
    # 490 replaces 455's coupling to the run reading; 489's band knobs aimed in place of the song's
    P('RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0)); S16B[b_] = float(np.clip(S16B[b_] * f_, 0.05, 5.0)) if ON7("455") else S16B[b_]',
      'RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0)); S16B[b_] = float(np.clip(S16B[b_] * f_, 0.05, 5.0)) if (ON7("455") and not ON8("490")) else S16B[b_]\n'
      '                        if ON8("490"): R490[b_] = float(np.clip(R490[b_] * f_, 0.02, 20.0))   # 490: the run weight, toward the band\'s kept share'),
    # ---- 486: 389's rates read on the judged sections (Verse 1, Chorus 1); a band they lack is read on its own sections as before
    P('    for s_ in SUNG:\n        ons = sorted({n_["on"] for n_ in notes if n_["sec"] == s_}); S_ = set(ons); b_ = SEC_BAND[s_]; n6, r6 = out.get(b_, (0, 0))\n',
      '    jb_ = {SEC_BAND[x_] for x_ in ("Verse 1", "Chorus 1") if x_ in SEC_BAND} if ON8("486") else set()\n'
      '    for s_ in SUNG:\n'
      '        if SEC_BAND[s_] in jb_ and s_ not in ("Verse 1", "Chorus 1"): continue             # 486: the judged sections\' bands read on them alone\n'
      '        ons = sorted({n_["on"] for n_ in notes if n_["sec"] == s_}); S_ = set(ons); b_ = SEC_BAND[s_]; n6, r6 = out.get(b_, (0, 0))\n'),
    # ---- 478: verse 2's repeats and steps at verse 1's rates; 434's bar on repeats the source did not sing lifted
    P('        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])\n',
      '        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])\n'
      '        if AGAIN478[0] and c[0] in ("repeat", "step"): c = (c[0], c[1] * LK["rep478" if c[0] == "repeat" else "stp478"], c[2])   # 478\n'),
    P('        d_ = [n_["dur"] for n_ in ns]; DRAWN398[0] = True                                  # 434: verse 2\'s chord tones from 398\'s knobs, as verse 1\'s\n',
      '        d_ = [n_["dur"] for n_ in ns]; DRAWN398[0] = True; AGAIN478[0] = ON8("478")         # 434: verse 2\'s chord tones from 398\'s knobs, as verse 1\'s; 478\n'),
    P('        ps_ = walk_notes(rng, ns, None, 1, float(np.median(mapped)), lo, hi, on_all, fixed=fx, shape=[(h_, 0.0) for h_ in mapped]); DRAWN398[0] = False\n',
      '        ps_ = walk_notes(rng, ns, None, 1, float(np.median(mapped)), lo, hi, on_all, fixed=fx, shape=[(h_, 0.0) for h_ in mapped]); DRAWN398[0] = False; AGAIN478[0] = False\n'),
    P('            if j_ in fx or ps_[j_] != ps_[j_ - 1] or ns[j_]["slur"]: continue\n',
      '            if ON8("478") or j_ in fx or ps_[j_] != ps_[j_ - 1] or ns[j_]["slur"]: continue        # 478: the bar lifted\n'),
    P('eb424=0.25, gs452=1.0,', 'eb424=0.25, rep478=1.0, stp478=1.0, gs452=1.0,'),
    # ---- 484 and 478, 489: read on the unaimed builds of the calibration
    P('        row["338: unaimed builds read"] = k2\n',
      '            if V128 >= 1 and "Verse 2" in SUNG and "Verse 1" in SUNG:                         # 484, 478: verse 2 against verse 1 (Window 142\'s pair; om\'s repeat and step)\n'
      '                w1_, w2_ = win_tp(c2["notes"], "Verse 1"), win_tp(c2["notes"], "Verse 2")\n'
      '                if len(w1_) >= 12 and len(w2_) >= 12:\n'
      '                    pk_ = pair122(w1_, w2_)["pitch_kept"]\n'
      '                    if np.isfinite(pk_): ua["_pk484"].append(pk_)\n'
      '                    for x_, w_ in (("1", w1_), ("2", w2_)):\n'
      '                        a_ = np.abs(np.diff([p_ for _, p_ in w_])); ua["_rep" + x_].append(float((a_ == 0).mean())); ua["_stp" + x_].append(float(((a_ > 0) & (a_ <= 2)).mean()))\n'
      '            if ON8("489"):                                                                    # 489: 452\'s readings by the band of the judged section\n'
      '                for s_ in ("Verse 1", "Chorus 1"):\n'
      '                    N_ = sorted(win_N(c2["notes"], BAR0[s_])); c_ = cand(N_) if N_ else None\n'
      '                    if not c_: continue\n'
      '                    b_ = SEC_BAND[s_]; kd_ = KD489[kd_band(len(N_) / 8)]\n'
      '                    ua["_gs" + b_].append(c_["gap_same_as_before"]); ua["_gst" + b_].append(kd_["gap_same_as_before"][0])\n'
      '                    ua["_er" + b_].append(c_["equal_gap_run_max"] / er_kept(len(N_) / 8))\n'
      '                    if np.isfinite(c_["zigzag_of_three"]): ua["_zz" + b_].append(c_["zigzag_of_three"]); ua["_zzt" + b_].append(kd_["zigzag_of_three"][0])\n'
      '        row["338: unaimed builds read"] = k2\n'),
    P('            if ON7("452"):\n                row["452 (kept, unaimed reading, knob)"]',
      '            if ON8("484") and ua.get("_pk484"):                                                # 484: 435\'s rate toward the kept pitch kept (0.72-0.79)\n'
      '                r_ = float(np.mean(ua["_pk484"])); f_ = float(np.clip((0.755 / max(0.05, r_)) ** 2, 0.6, 1.6)); K435[0] = float(np.clip(K435[0] * f_, 0.02, 1.0))\n'
      '                if f_ in (0.6, 1.6): full_now.add("k435")\n'
      '                row["484 (kept, unaimed reading, rate)"] = (0.755, round(r_, 3), round(K435[0], 3))\n'
      '            if ON8("478") and ua.get("_rep2"):                                                 # 478: verse 2\'s repeats and steps toward verse 1\'s, on the same builds\n'
      '                o_ = {}\n'
      '                for kn_, a_, b_ in (("rep478", "_rep1", "_rep2"), ("stp478", "_stp1", "_stp2")):\n'
      '                    t_, r_ = float(np.mean(ua[a_])), float(np.mean(ua[b_])); f_ = float(np.clip(max(0.02, t_) / max(0.02, r_), 0.6, 1.6)); LK[kn_] = float(np.clip(LK[kn_] * f_, 0.05, 20.0))\n'
      '                    if f_ in (0.6, 1.6): full_now.add(kn_)\n'
      '                    o_[kn_] = (round(t_, 3), round(r_, 3), round(LK[kn_], 3))\n'
      '                row["478 (verse 1, verse 2 unaimed, knob)"] = o_\n'
      '            if ON8("489"):                                                                    # 489: each band\'s knobs toward the kept figures at the window\'s density\n'
      '                o_ = {}\n'
      '                for b_ in B489:\n'
      '                    if len(ua.get("_gs" + b_, [])) < 10: continue\n'
      '                    for k_, rk_, tk_, pw_ in (("gs", "_gs", "_gst", 2), ("er", "_er", None, 2), ("zz", "_zz", "_zzt", 2)):\n'
      '                        if not ua.get(rk_ + b_): continue\n'
      '                        r_ = float(np.mean(ua[rk_ + b_])); t_ = float(np.mean(ua[tk_ + b_])) if tk_ else 1.0\n'
      '                        f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** pw_, 0.6, 1.6)); B489[b_][k_] = float(np.clip(B489[b_][k_] * f_, 0.02, 20.0))\n'
      '                        if f_ in (0.6, 1.6): full_now.add(k_ + "489 " + b_)\n'
      '                        o_[f"{k_} {b_}"] = (round(t_, 3), round(r_, 3), round(B489[b_][k_], 3))\n'
      '                row["489 (kept, unaimed reading, knob)"] = o_\n'
      '            if ON8("490"): row["490 (band: run weight)"] = {b_: round(v_, 3) for b_, v_ in R490.items()}\n'
      '            if ON7("452") and not ON8("489"):\n                row["452 (kept, unaimed reading, knob)"]'),
    # K435 becomes a list so the calibration can move it
    P('K435 = 0.75                                                                              # 435: the kept three in four\n',
      'K435 = [0.75]                                                                            # 435: the kept three in four; 484: aimed on unaimed builds\n'
      'import re as _re8\n'
      '_T122 = json.load(open(f"{H118}/tables/zeneng_v122_whole_song.json"))["code"]\n'
      'exec(_re8.search(r"^def pair\\(.*?(?=^\\S)", _T122, _re8.S | _re8.M).group(0).replace("def pair(", "def pair122("))   # 484: Window 142\'s pair()\n'
      'def win_tp(notes, sec):\n'
      '    """484: a section\'s first eight bars as (beats from its first bar line, pitch), as Window 147 reads them."""\n'
      '    b0 = BAR0[sec]; return [((n_["on"] - b0 * BAR) / BEAT, n_["p"]) for n_ in sorted(notes, key=lambda x_: x_["on"]) if b0 * BAR <= n_["on"] < (b0 + 8) * BAR and n_["sec"] == sec]\n'
      'KD489 = {k_.replace(" notes a bar", ""): v_ for k_, v_ in json.load(open(f"{H118}/tables/zeneng_v125_port_reread.json"))["findings"]["at the builds\' own density: kept mean, builds\' mean, difference in kept sd"].items() if isinstance(v_, dict)}\n'
      'def kd_band(npb): return "3.5 to 4.5" if npb < 4.5 else "4.5 to 5.5" if npb < 5.5 else "5.5 to 9"\n'),
    P('                if rng.random() < K435: fx[j_] = src_at[t_]', '                if rng.random() < K435[0]: fx[j_] = src_at[t_]'),
    # the record
    P('    rerun["v127_part"] = V127;',
      '    rerun["v128_part"] = V128; rerun["v128_on"] = sorted(f_ for f_ in P128 if ON8(f_)); rerun["opt465"] = OPT465\n'
      '    rerun["knobs128"] = dict(k435=round(K435[0], 4), rep478=round(LK["rep478"], 4), stp478=round(LK["stp478"], 4), r490={b_: round(v_, 4) for b_, v_ in R490.items()},\n'
      '                             b489={b_: {k_: round(x_, 4) for k_, x_ in v_.items()} for b_, v_ in B489.items()})\n'
      '    rerun["v127_part"] = V127;'),
]
PARTS = PART1

def port(song, patches):
    s = open(f"{SRC}/melody_v127_p{song}.py").read()
    s = s.replace("/home/claude/p53", DST).replace("melody_v127_", "melody_v128_")
    for old, new, cnt, only in patches:
        if only and song not in only: continue
        k = s.count(old)
        if k != cnt: sys.exit(f"song {song}: patch not matched {k} times (want {cnt}): {old[:90]!r}")
        s = s.replace(old, new)
    s = HEADER + f'SONG8 = "{song}"\n' + s
    open(f"{DST}/melody_v128_p{song}.py", "w").write(s); compile(s, f"melody_v128_p{song}.py", "exec")
    print(song, "ok", len(s.splitlines()), "lines")

if __name__ == "__main__":
    extra = []
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(f"{here}/gen_v128_parts23.py"):
        sys.path.insert(0, here); import gen_v128_parts23 as G23; extra = G23.PATCHES
    for so in SONGS: port(so, PARTS + extra)
