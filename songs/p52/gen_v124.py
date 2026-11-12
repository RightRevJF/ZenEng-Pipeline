"""v124 Run 1 (ZenEng v124, Modules 27.64-27.68): the session's own repairs ported onto the v119 port of songs 40, 42, 43, 44 and 45 (songs/p51).
384: every patch replaces whole statements, each matched the stated number of times in each file it names; each patched path is run in a smoke run.
Ruled (v124 Run 1):
  405 runs read on drawable lines: 389's rate is set on the lines that could be placed without runs (no-room and fallback lines counted apart)
  428 (withdraws 424's empty-bar rate): empty bars are not drawn or aimed; printed only
  409 the window's last note: 424's last-note knob weights the last note of the window's last line (not bar 8 alone), slurred or walked,
      and the ending draw by the same rule; where the window's last note comes from is printed (readings)
  412 as proposed: a return keeps its source's range (already so in _vary_return) and 398's chord-tone weights act only on drawn notes
      (the fresh-line walk); the cause found in song 45 is reported as finding 450 (a diagnostic switch ZE_DIAG450=1, never in a run of record)
  413 a line drawn on a returning unit keeps the unit's bars through all its copy tries; the losses counted
  414 a line's span drawn inside the kept band for its notes and the kept syllables a second (423, 1.4-2.3); the 5th-95th where they part
  415 verse 2's share read on the bars where the two verses carry the same number of syllables
  417, 419 readings (readings_v124_block.py)
Not ported: 404, 406, 408 (Run 2), 410, 425, 427.
Usage: python3 gen_v124.py  (writes melody_v124_p40.py ... melody_v124_p45.py)"""
import os, sys
SRC = "/home/claude/p51"; DST = os.environ.get("GEN_DST", "/home/claude/p52")
SONGS = ("40", "42", "43", "44", "45")

HEADER = '''"""ZenEng v124 Run 1 (Modules 27.64-27.68): repairs 405, 409, 412-415 and 428 onto the v119 port (songs/p51), by gen_v124.py.
Readings 417, 419 and v121-v123's (426, 431-433, 436, 437, 441-443) in readings_v124_block.py and new_readings_v124.py. ZE_OFF switches a fix off (side runs only).
"""
'''

def P(old, new, count=1, songs=None):
    return (old, new, count, songs)

PATCHES = [
    # the switches
    P('def ON(f_): return STEP119.get(f_, 0) <= V119 and f_ not in OFF\n',
      'def ON(f_): return STEP119.get(f_, 0) <= V119 and f_ not in OFF\n'
      'FIX124 = ("405", "409", "412", "413", "414", "415", "428")                                  # v124 Run 1: the session\'s repairs (on unless ZE_OFF names one)\n'
      'DIAG450 = os.environ.get("ZE_DIAG450") == "1"                                           # diagnostics only (song 45): 267 reads the bridge\'s G before the raise to G-sharp\n'
      'CUR405 = [None]; DRAWN398 = [False]\n'),
    # ---- 405: 389's runs read on the lines that could be placed without runs
    P('    STATS["366: lines drawn that may run" if may_run[0] else "366: lines drawn that may not run"] += 1\n',
      '    STATS["366: lines drawn that may run" if may_run[0] else "366: lines drawn that may not run"] += 1\n'
      '    mr405 = may_run[0]                                                                    # 405: the draw before any fallback\n'),
    P('        return ons\n    return None\nRATE293 = [0.40]',
      '        if ON("405") and i is not None and CUR405[0] is not None:                         # 405: a line that could be placed without runs\n'
      '            CUR405[0][f"{sec}:{i}"] = bool(not runs_ok and (mr405 or not may_run[0])); STATS["405: line drawable without runs" if CUR405[0][f"{sec}:{i}"] else ("405: line with no room on the eighth grid" if runs_ok else "405: line fell back to runs")] += 1\n'
      '        return ons\n    return None\nRATE293 = [0.40]'),
    P('    meta = dict(returns=[], kinds={}, win={}, targets={})\n',
      '    meta = dict(returns=[], kinds={}, win={}, targets={}, drawable405={}); CUR405[0] = meta["drawable405"]   # 405\n'),
    P('def s16_bands(notes):\n', 'def s16_bands(notes, dr=None):\n'),
    P('        for t_ in ons:\n            if t_ % 6 == 3: n6 += 1; r6 += (t_ - 3) in S_ and (t_ + 3) in S_\n',
      '        D_ = {n_["on"] for n_ in notes if n_["sec"] == s_ and (dr is None or dr.get(n_["line"]))}   # 405: the drawable lines\' onsets\n'
      '        for t_ in ons:\n'
      '            if t_ not in D_: continue\n'
      '            if t_ % 6 == 3: n6 += 1; r6 += (t_ - 3) in S_ and (t_ + 3) in S_\n'),
    P('for b_, (n_, r_) in s16_bands(c2["notes"]).items():',
      'for b_, (n_, r_) in s16_bands(c2["notes"], c2["meta"].get("drawable405") if ON("405") else None).items():'),
    # ---- 428 (withdraws 424's empty-bar rate): empty bars are printed only
    P('    eb424 = bool(ON("424") and i is not None',
      '    eb424 = bool(ON("424") and not ON("428") and i is not None'),
    P('                if ua.get("empty_bars"):\n',
      '                if ua.get("empty_bars") and not ON("428"):                                   # 428: empty bars are not aimed\n'),
    # ---- 409: the window's last note
    P('CUR424 = [None]; LAST424 = [False]\n',
      'CUR424 = [None]; LAST424 = [False]\n'
      'WL409 = {}\n'
      'def wlast409(sec, j):\n'
      '    """409: the line is the last of its section to begin inside the section\'s first eight bars (the window\'s last line)."""\n'
      '    if sec not in WL409: WL409[sec] = max([k for k in range(len(LINES[sec])) if line_start(sec, k) < (BAR0[sec] + 8) * BAR] or [-1])\n'
      '    return j == WL409[sec]\n'),
    P('                    CUR424[0] = sec\n',
      '                    CUR424[0] = (sec, i) if ON("409") else sec                                  # 409: the line, to find the window\'s last\n'),
    P('LAST424[0] = ON("424") and CUR424[0] is not None and i == len(notes) - 1 and (n["on"] // BAR - BAR0[CUR424[0]]) % 8 == 7',
      'LAST424[0] = ON("424") and CUR424[0] is not None and i == len(notes) - 1 and (wlast409(*CUR424[0]) if ON("409") else (n["on"] // BAR - BAR0[CUR424[0]]) % 8 == 7)'),
    P('            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) for x in opts])[0] if opts else q_\n',
      '            w409 = ON("409") and ON("424") and isinstance(CUR424[0], tuple) and i == len(notes) - 1 and wlast409(*CUR424[0])   # 409: a slurred last note too\n'
      '            if w409: STATS["409: the window\'s last note weighted (slurred)"] += 1\n'
      '            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) * (LK["lt424"] if (w409 and (x - mton()) % 12 == 0) else 1.0) for x in opts])[0] if opts else q_\n'),
    P('            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None; LAST424[0] = False',
      '            if LAST424[0] and isinstance(CUR424[0], tuple): STATS["409: the window\'s last note weighted (walk)"] += 1\n'
      '            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None; LAST424[0] = False'),
    P('and (ns[-1]["on"] // BAR - BAR0[sec]) % 8 == 7) else 1.0) for p in cands])[0]',
      'and (wlast409(sec, i) if ON("409") else (ns[-1]["on"] // BAR - BAR0[sec]) % 8 == 7)) else 1.0) for p in cands])[0]'),
    # ---- 412: 398's chord-tone weights on drawn notes only (a return keeps its source's range already: _vary_return widens lo and hi to it)
    P('    if ON("398") and p % 12 in tones: w *=', '    if ON("398") and (DRAWN398[0] or not ON("412")) and p % 12 in tones: w *='),
    P('rs_ = LK["res398"] if (ON("398") and PREV_NC[0]', 'rs_ = LK["res398"] if (ON("398") and (DRAWN398[0] or not ON("412")) and PREV_NC[0]'),
    P('                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape); CUR424[0] = None',
      '                    DRAWN398[0] = True                                                          # 412: the drawn notes\n'
      '                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape); CUR424[0] = None; DRAWN398[0] = False'),
    # ---- 450 diagnostic (song 45 only, never in a run of record): 267 reads the bridge's G before its raise to G-sharp
    P('if M.chord_for(n, on) == "E" and n["p"] % 12 == 7: n["p"] += 1;',
      'if M.chord_for(n, on) == "E" and n["p"] % 12 == 7: n["raised375"] = n["p"]; n["p"] += 1;', 1, ("45",)),
    P('R = {n["on"] - U: n.get("moved386", n["p"]) for n in notes if a2 <= n["on"] < b2}; S_ = {n["on"] - U0: n.get("moved386", n["p"]) for n in notes if a0 <= n["on"] < b0}',
      'R = {n["on"] - U: (n.get("raised375", n.get("moved386", n["p"])) if DIAG450 else n.get("moved386", n["p"])) for n in notes if a2 <= n["on"] < b2}; '
      'S_ = {n["on"] - U0: (n.get("raised375", n.get("moved386", n["p"])) if DIAG450 else n.get("moved386", n["p"])) for n in notes if a0 <= n["on"] < b0}', 1, ("45",)),
    # ---- 413: a line drawn on a returning unit keeps the unit's bars through its copy tries; the losses counted
    P('        if copybars and _try < 14 and not free: cb =', '        if copybars and _try < (NT if (allbars and ON("413")) else 14) and not free: cb ='),
    P('        elif copybars and _try == 14 and not (pair and fallback):', '        elif copybars and _try == (NT if (allbars and ON("413")) else 14) and not (pair and fallback):'),
    P('            if bad: STATS["351: bars left out of a copy"] += len(bad);',
      '            if bad and allbars: STATS["413: unit-return bars left out (more than one onset off)"] += len(bad)\n'
      '            if bad: STATS["351: bars left out of a copy"] += len(bad);'),
    P('partner=partner, unitbars=ub or None)\n',
      'partner=partner, unitbars=ub or None)\n'
      '                if ns is None and ub: STATS["413: build lost on a unit-return line (no rhythm)"] += 1\n'),
    P('not M.clash(q_, M.chord_for(n_, on_)): fx[j_] = q_\n',
      'not M.clash(q_, M.chord_for(n_, on_)): fx[j_] = q_\n'
      '                            elif q_ is not None and j_ not in fx: STATS["413: unit-return pitch not kept (range, slur or chord), a try"] += 1\n'),
    # ---- 414: the span read with the line's syllables a second
    P('    sp = span_mid(n) if (span_to is not None and not fix) else None                          # 378: the span drawn first\n',
      '    sp = span_mid(n) if (span_to is not None and not fix) else None                          # 378: the span drawn first\n'
      '    if sp and ON("414") and span_to * M.SEC_PER_TW > 0:                                     # 414: inside the band and the kept 1.4-2.3 syllables a second (423)\n'
      '        T_ = span_to * M.SEC_PER_TW; d_ = (n / (2.3 * T_), n / (1.4 * T_)); a_, b_ = max(sp[0], d_[0]), min(sp[1], d_[1])\n'
      '        if a_ <= b_: sp = (a_, b_); STATS["414: span inside the band and the density"] += 1\n'
      '        else: sp = span_wide(n); STATS["414: band and density apart: the kept 5th-95th"] += 1\n'),
    # ---- 415: verse 2's share on the bars where the two verses carry the same number of syllables
    P('if (ON("393") and "Verse 2" in LINES) else None   # 393\n', 'if (ON("393") and not ON("415") and "Verse 2" in LINES) else None   # 393 (415 reads bars)\n'),
    P('    a, c = bars("Verse 2"), bars("Verse 1"); return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))\n',
      '    a, c = bars("Verse 2"), bars("Verse 1")\n'
      '    if ON("415"):                                                                          # 415: the bars with the same count of syllable onsets\n'
      '        def syl(s):\n'
      '            out = collections.Counter(); seen = set()\n'
      '            for n in notes:\n'
      '                if n["sec"] == s and (n["line"], n["syl"]) not in seen: seen.add((n["line"], n["syl"])); out[n["on"] // BAR - BAR0[s]] += 1\n'
      '            return out\n'
      '        sa, sc = syl("Verse 2"), syl("Verse 1"); keep = [k for k in a if k in c and sa[k] == sc[k]]\n'
      '        if keep: STATS["415: verse 2 read on bars of equal syllables"] += 1; return sum(1 for k in keep if len(a[k] ^ c[k]) <= 1) / len(keep)\n'
      '        STATS["415: no bar of equal syllables (all bars read)"] += 1\n'
      '    return sum(1 for k, x in a.items() if k in c and len(x ^ c[k]) <= 1) / max(1, len(a))\n'),
    # the record of the run
    P('    rerun["knobs424"] = {', '    rerun["v124"] = [f_ for f_ in FIX124 if ON(f_)]; rerun["diag450"] = DIAG450\n    rerun["knobs424"] = {'),
]

def port(song):
    s = open(f"{SRC}/melody_v119_p{song}.py").read()
    s = s.replace("/home/claude/p51", DST).replace("melody_v119_", "melody_v124_")
    for old, new, cnt, only in PATCHES:
        if only and song not in only: continue
        k = s.count(old)
        if k != cnt: sys.exit(f"song {song}: patch not matched {k} times (want {cnt}): {old[:90]!r}")
        s = s.replace(old, new)
    s = HEADER + s
    open(f"{DST}/melody_v124_p{song}.py", "w").write(s)
    compile(s, f"melody_v124_p{song}.py", "exec")
    print(song, "ok", len(s.splitlines()), "lines")

if __name__ == "__main__":
    for so in SONGS: port(so)
