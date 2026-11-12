"""v119 port (Module 27.63, fixes 384-401) onto the v118 search of songs 40, 42, 43, 44 and 45 (songs/p50).
384: every patch replaces whole statements, each matched exactly once in each file; each patched path is run once in a smoke run
before a run of record. The fixes are switched on by step (ZE_STEP, default 3), so that the runs between steps can be made again:
  step 1, repairs: 384, 385, 386, 387, 389, 394, 395 (395 is read in readings_v119.py)
  step 2: 388's two side runs only (ZE_OFF=378 and ZE_PIN388=1); 399 and 401 withdrawn by v120 (421)
  step 3, harmony and line: 398, 400, 390, 391, 392, 393, and v120's 424
Usage: python3 gen_v119.py  (writes melody_v119_p40.py ... melody_v119_p45.py)"""
import re, sys
import os
SRC = "/home/claude/p50"; DST = os.environ.get("GEN_DST", "/home/claude/p51")
SONGS = ("40", "42", "43", "44", "45")

HEADER = '''"""ZenEng v119 port (Module 27.63, Window 139), fixes 384-401, onto the v118 search (songs/p50), by gen_v119.py.
Steps (ZE_STEP): 1 = 384-387, 389, 394, 395; 2 = 388's side runs only (ZE_OFF=378, ZE_PIN388=1; 399 and 401 withdrawn, v120 421); 3 = and 398, 400, 390-393, 424 (v120).
"""
'''

def P(old, new, count=1, songs=None):
    return (old, new, count, songs)

STEP1 = [
    # the step switch (next to the diagnostic switch)
    P('OFF = set(filter(None, os.environ.get("ZE_OFF", "").split(",")))                       # diagnostics only: a fix switched off for a side run (never in a run of record)\n',
      'OFF = set(filter(None, os.environ.get("ZE_OFF", "").split(",")))                       # diagnostics only: a fix switched off for a side run (never in a run of record)\n'
      'V119 = int(os.environ.get("ZE_STEP", "3"))                                             # v119: the fixes ported in three steps, runs between them\n'
      'STEP119 = {f_: 1 for f_ in ("384", "385", "386", "387", "389", "394", "395")} | {f_: 2 for f_ in ("388",)} | {f_: 3 for f_ in ("398", "400", "390", "391", "392", "393", "424")}\n'
      'def ON(f_): return STEP119.get(f_, 0) <= V119 and f_ not in OFF\n'),
    # 385: 349's target a share of all the build's notes; 375 only chooses where they go
    P('    elig = len(ns) if "375" in OFF else sum(1 for j in range(len(ns) - 1)',
      '    elig = len(ns) if ("375" in OFF or ON("385")) else sum(1 for j in range(len(ns) - 1)'),
    P('        ns[j]["p"] = q; ns[j]["outside"] = True; used.add(j); placed += 1\n',
      '        if pas: ns[j]["pre358"] = ns[j]["p"]                                               # 394: the note it replaced\n'
      '        ns[j]["p"] = q; ns[j]["outside"] = True; used.add(j); placed += 1\n'),
    # 387: 356's stop is a reading; it moves and freezes no knob
    P('                STOP356.append(f"round {CAL_ROUNDS[0]}: {out356} outside the kept middle half (distinct lengths {dd}, rhythm bits {round(bits, 3)}); the 354 knobs stop at "\n'
      '                               f"{[round(LK[k_], 3) for k_ in (\'s16\', \'g8\', \'g4\', \'glong\')]}"); print(STOP356[-1])\n',
      '                STOP356.append(f"round {CAL_ROUNDS[0]}: {out356} outside the kept middle half (distinct lengths {dd}, rhythm bits {round(bits, 3)}); "\n'
      '                               + ("a reading (387): no knob stops" if ON("387") else f"the 354 knobs stop at {[round(LK[k_], 3) for k_ in (\'s16\', \'g8\', \'g4\', \'glong\')]}")); print(STOP356[-1])\n'),
    P('                if STOP356 or "354" in OFF: break\n',
      '                if (STOP356 and not ON("387")) or "354" in OFF: break                          # 387: the stop no longer moves or freezes a knob\n'),
    # 389: 366's rate aimed at the runs of the section's own band in the kept table; a line that may not run falls back before it dies
    P('    may_run = [runs_ok or "366" in OFF or rng.random() < LK["run"]]',
      '    may_run = [runs_ok or "366" in OFF or rng.random() < (RUNR[SEC_BAND[sec]] if ON("389") else LK["run"])]'),
    P('        free = _try >= NT or (fits is not None and not fits)\n',
      '        if ON("389") and not may_run[0] and (_try == NT // 2 or (_try == 0 and fits is not None and not fits)):   # 389: falls back before it dies\n'
      '            may_run[0] = True; STATS["366: fallback to runs (nothing fitted without)"] += 1; STATS["389: fallback at half the tries" if _try else "389: fallback at once (no entry and landing fit)"] += 1\n'
      '            if n >= 9 and not fix:                                                         # the entries and landings that fit, read again with runs allowed\n'
      '                key = (sec, i, tmin, end, tuple(lands), tuple(sorted(pal)) if pal else None, True)\n'
      '                if key not in FITS: FITS[key] = {(k_, t) for k_ in ENTRY for t in lands if dp(k_, t, {})[0][n - 1]}\n'
      '                fits = FITS[key]\n'
      '        free = _try >= NT or (fits is not None and not fits)\n'),
    P('        if _try == NT and not may_run[0]: may_run[0] = True; STATS["366: fallback to runs (nothing fitted without)"] += 1\n',
      '        if _try == NT and not may_run[0]: may_run[0] = True; STATS["366: fallback to runs (nothing fitted without)"] += 1; STATS["389: fallback at the free tries" if ON("389") else "366: fallback at the free tries"] += 1\n'),
    P('STOP356 = []\n',
      'STOP356 = []\n'
      'def _runs_kept(T):\n'
      '    """389: of onsets on a sixteenth position, the share in runs (a sixteenth before and after), read off a kept table as a chain on the bar\'s 16 positions."""\n'
      '    T = np.array(T, float); P_ = np.zeros((16, 16))\n'
      '    for p_ in range(16):\n'
      '        for g_ in range(1, 33): P_[p_, (p_ + g_) % 16] += T[p_][g_]\n'
      '    P_ = P_ / P_.sum(1, keepdims=True); w_, v_ = np.linalg.eig(P_.T); pi_ = np.real(v_[:, np.argmin(abs(w_ - 1))]); pi_ = pi_ / pi_.sum()\n'
      '    return float(sum(pi_[p_ - 1] * T[p_ - 1][1] / T[p_ - 1][1:].sum() * T[p_][1] / T[p_][1:].sum() for p_ in range(1, 16, 2)) / sum(pi_[p_] for p_ in range(1, 16, 2)))\n'
      'RUN_POOLED = _runs_kept(KT["tables"]["all"])\n'
      'RUN_KEPT_BAND = {b_: round(0.31 * _runs_kept(KT["tables"][b_]) / RUN_POOLED, 3) for b_ in KT["tables"] if b_ != "all"}   # 389: the kept 31%, scaled by the band\'s table\n'
      'RUNR = {b_: 1.0 for b_ in RUN_KEPT_BAND}                                                 # 389: the run rate of each band, set on unaimed builds\n'
      'def s16_bands(notes):\n'
      '    """389: onsets on a sixteenth position and those in runs, by the band of their section."""\n'
      '    out = {}\n'
      '    for s_ in SUNG:\n'
      '        ons = sorted({n_["on"] for n_ in notes if n_["sec"] == s_}); S_ = set(ons); b_ = SEC_BAND[s_]; n6, r6 = out.get(b_, (0, 0))\n'
      '        for t_ in ons:\n'
      '            if t_ % 6 == 3: n6 += 1; r6 += (t_ - 3) in S_ and (t_ + 3) in S_\n'
      '        out[b_] = (n6, r6)\n'
      '    return out\n'),
    P('            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)',
      '            n6, r6, p6 = s16_shape(c2["notes"]); ua["_n6"].append(n6); ua["_r6"].append(r6)\n'
      '            if ON("389"):\n'
      '                for b_, (n_, r_) in s16_bands(c2["notes"]).items(): ua["_n6b" + b_].append(n_); ua["_r6b" + b_].append(r_)\n'
      '           '),
    P('            if "348" not in OFF:                                                             # 366: the run rate; 355: the sixteenth-onset knob\n'
      '                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))\n'
      '                f_ = float(np.clip(KEPT355["in_runs"] / max(0.02, ir), 0.6, 1.6)); LK["run"] = float(np.clip(LK["run"] * f_, 0.0, 1.0))   # a rate, at most one\n'
      '                if f_ in (0.6, 1.6) and 0.0 < LK["run"] < 1.0: full_now.add("run")\n',
      '            if "348" not in OFF:                                                             # 366: the run rate; 355: the sixteenth-onset knob\n'
      '                ir = sum(ua["_r6"]) / max(1, sum(ua["_n6"]))\n'
      '                if not ON("389"):\n'
      '                    f_ = float(np.clip(KEPT355["in_runs"] / max(0.02, ir), 0.6, 1.6)); LK["run"] = float(np.clip(LK["run"] * f_, 0.0, 1.0))   # a rate, at most one\n'
      '                    if f_ in (0.6, 1.6) and 0.0 < LK["run"] < 1.0: full_now.add("run")\n'
      '                else:                                                                        # 389: a rate for each band, toward its kept share\n'
      '                    rb_ = {}\n'
      '                    for b_ in RUNR:\n'
      '                        n_ = sum(ua.get("_n6b" + b_, [])); r_ = sum(ua.get("_r6b" + b_, []))\n'
      '                        if n_ < 30: continue\n'
      '                        f_ = float(np.clip(RUN_KEPT_BAND[b_] / max(0.02, r_ / n_), 0.6, 1.6)); RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0))\n'
      '                        if f_ in (0.6, 1.6) and 0.0 < RUNR[b_] < 1.0: full_now.add("run " + b_)\n'
      '                        rb_[b_] = (RUN_KEPT_BAND[b_], round(r_ / n_, 3), round(RUNR[b_], 3))\n'
      '                    row["389 (band: kept, unaimed reading, rate)"] = rb_\n'),
    # 394: a passing note in a tune that returns is placed in every occurrence or none
    P('    notes = sorted([n for l in lines for n in l], key=lambda n: n["on"])\n',
      '    if ON("394"):                                                                          # 394: a passing note in a tune that returns, in every occurrence or none\n'
      '        def root394(k):\n'
      '            seen = {k}\n'
      '            while True:\n'
      '                h_, s_, i_ = how(*k)\n'
      '                if h_ in ("copy", "return", "plan", "tail", "again") and (s_, i_) in built and (s_, i_) not in seen: k = (s_, i_); seen.add(k)\n'
      '                else: return k\n'
      '        occ = collections.defaultdict(list)\n'
      '        for k in built: occ[root394(k)].append(k)\n'
      '        for r_, ks in occ.items():\n'
      '            if len(ks) < 2: continue\n'
      '            RU_ = line_start(*r_)\n'
      '            for n in built[r_]:\n'
      '                if not n.get("pass358") or "pre358" not in n: continue\n'
      '                rel_ = n["on"] - RU_; ok = True; spots = []\n'
      '                for k in ks:\n'
      '                    if k == r_: continue\n'
      '                    L = built[k]; LU = line_start(*k); j = next((jj for jj, m in enumerate(L) if m["on"] - LU == rel_), None)\n'
      '                    if j is None or j == 0 or j == len(L) - 1 or L[j].get("pin"): ok = False; break\n'
      '                    m = L[j]\n'
      '                    if m.get("pass358") or m["p"] == n["p"]: m["pass358"] = True; m["outside"] = True; m.setdefault("pre358", n["pre358"]); continue   # it already sings the passing note\n'
      '                    q = m["p"] + (n["p"] - n["pre358"])\n'
      '                    if q % 12 in (M.SUNGPC - M.SCALE) and 1 <= abs(q - L[j - 1]["p"]) <= 2 and 1 <= abs(L[j + 1]["p"] - q) <= 2: spots.append((m, q))\n'
      '                    else: ok = False; break\n'
      '                if ok:\n'
      '                    for m, q in spots: m["pre358"] = m["p"]; m["p"] = q; m["pass358"] = True; m["outside"] = True\n'
      '                    STATS["394: passing note placed in every occurrence"] += 1; STATS["394: occurrences given the passing note"] += len(spots)\n'
      '                else:\n'
      '                    pp_ = n["p"]; pr_ = n["pre358"]\n'
      '                    for k in ks:\n'
      '                        LU = line_start(*k)\n'
      '                        for m in built[k]:\n'
      '                            if m["on"] - LU == rel_ and (m.get("pass358") or m["p"] == pp_):\n'
      '                                m["p"] = pr_ if m["p"] == pp_ else m.get("pre358", m["p"]); m.pop("pass358", None); m.pop("outside", None)\n'
      '                    STATS["394: passing note withdrawn (an occurrence could not take it)"] += 1\n'
      '    notes = sorted([n for l in lines for n in l], key=lambda n: n["on"])\n'),
    # 386: 375's clash read on every line, returning and copied lines too; a clashing note moved as 215 moves a tritone
    P('    finish(notes, rng)\n',
      '    if ON("386"):                                                                          # 386: 375\'s clash read on returning and copied lines too\n'
      '        for n in notes:\n'
      '            if n.get("pin") or (n.get("pass358") and n["on"] % BEAT and n.get("dur", 12) < BEAT): continue\n'
      '            ch_ = M.chord_for(n, on)\n'
      '            if clash375(n["p"], ch_) and not _clash200(n["p"], ch_):\n'
      '                tones = M.CH[ch_][1]; q0 = n["p"]\n'
      '                opts = [q_ for q_ in (q0 + 1, q0 - 1, q0 + 2, q0 - 2) if not clash375(q_, ch_) and not tri(q_, ch_)]\n'
      '                if opts:\n'
      '                    n["p"] = min(opts, key=lambda q_: (q_ % 12 not in tones, q_ % 12 not in M.SCALE and q_ % 12 not in tones, abs(q_ - q0))); n["moved386"] = q0\n'
      '                    STATS["386: notes moved off a semitone from a chord\'s outside tone"] += 1; STATS[f"386: moved in a {meta[\'kinds\'].get(tuple(n[\'line\'].split(\':\')[:1]) + (int(n[\'line\'].split(\':\')[1]),), \'line\')} line"] += 1\n'
      '                else: STATS["386: a clashing note with no move"] += 1\n'
      '    finish(notes, rng)\n'),
    # 386 with 267 (the writer's Q1 A): 267 reads a return's pitches as drawn, before 386's moves
    P('        R = {n["on"] - U: n["p"] for n in notes if a2 <= n["on"] < b2}; S_ = {n["on"] - U0: n["p"] for n in notes if a0 <= n["on"] < b0}\n',
      '        R = {n["on"] - U: n.get("moved386", n["p"]) for n in notes if a2 <= n["on"] < b2}; S_ = {n["on"] - U0: n.get("moved386", n["p"]) for n in notes if a0 <= n["on"] < b0}   # 386 (Q1 A): read before its moves\n'),
    P('        keep = all(R[t] == S_[t] for t in sh if t < q4)\n',
      '        keep = all(R[t] == S_[t] for t in sh if t < q4)\n'
      '        if not keep:                                                                       # a reading: what changed early\n'
      '            NB_ = {n["on"]: n for n in notes}\n'
      '            for t in sh:\n'
      '                if t < q4 and R[t] != S_[t]:\n'
      '                    r_, s_ = NB_.get(t + U, {}), NB_.get(t + U0, {})\n'
      '                    STATS["267: changed early, " + kind + (", the return\'s note a passing note" if r_.get("pass358") else "") + (", the source\'s note a passing note" if s_.get("pass358") else "")\n'
      '                          + (", the return\'s note placed outside" if r_.get("outside") and not r_.get("pass358") else "") + (", the source\'s note placed outside" if s_.get("outside") and not s_.get("pass358") else "")] += 1\n'),
    # the rerun record
    P('    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)\n',
      '    rerun["calibration_rounds"] = CAL_ROUNDS[0]; rerun["stop356"] = list(STOP356); rerun["off"] = sorted(OFF)\n'
      '    rerun["v119_step"] = V119; rerun["fixes_on"] = sorted(f_ for f_ in STEP119 if ON(f_))\n'
      '    rerun["run_rates389"] = dict(kept=RUN_KEPT_BAND, rate={b_: round(v_, 4) for b_, v_ in RUNR.items()}, pooled_table_reading=round(RUN_POOLED, 3))\n'),
]
STEP2 = [
    # 399 and 401 withdrawn by v120 (421): not ported
    # 388's second side run: the landing pinned to the draw (ZE_PIN388=1): the last stress lands where the kept table's draw puts it
    P('        else: tgt = land_draw(rng, sec, n, i, allowed=spa if spa else None)\n',
      '        else: tgt = land_draw(rng, sec, n, i, allowed=spa if spa else None)\n'
      '        if PIN388 and not free and Ls not in fix: tgt = None; STATS["388: landing left to the draw (side run)"] += 1\n'),
    P('            if t > tgt: break\n', '            if tgt is not None and t > tgt: break\n'),
    P('            if Ls == 0 and t != tgt: continue\n', '            if Ls == 0 and tgt is not None and t != tgt: continue\n'),
    P('                if k == Ls and t != tgt: continue\n', '                if k == Ls and tgt is not None and t != tgt: continue\n'),
    P('                if k < Ls and t >= tgt: continue\n', '                if k < Ls and tgt is not None and t >= tgt: continue\n'),
    P('        if tgt + step * post > end or tgt - step * Ls < tmin: continue\n',
      '        if tgt is not None and (tgt + step * post > end or tgt - step * Ls < tmin): continue\n'),
    P('STOP356 = []\n', 'STOP356 = []\nPIN388 = os.environ.get("ZE_PIN388") == "1"                                                # 388: a side run only\n'),
    P('    rerun["v119_step"] = V119; rerun["fixes_on"] = sorted(f_ for f_ in STEP119 if ON(f_))\n',
      '    rerun["v119_step"] = V119; rerun["fixes_on"] = sorted(f_ for f_ in STEP119 if ON(f_)); rerun["pin388"] = PIN388\n'),
]
STEP3 = [
    # 398: chord tones at the kept rates, each aimed by one knob on unaimed builds
    P('    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]',
      '    if ON("398") and p % 12 in tones: w *= LK["ct398"] * (LK["ctb398"] if on_beat else 1.0) * (LK["ctd398"] if n["on"] % BAR == 0 else 1.0)   # 398: overall, on a beat, on a downbeat\n'
      '    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]'),
    P('                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p)); base += w0',
      '                rs_ = LK["res398"] if (ON("398") and PREV_NC[0] and 0 < abs(p - prev) <= 2 and p % 12 in M.CH[ch][1]) else 1.0   # 398: a note off its chord left by step\n'
      '                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_); base += w0'),
    P('            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None',
      '            PREV_NC[0] = bool(out) and i > 0 and out[-1] % 12 not in M.CH[M.chord_for(notes[i - 1], notes_on)][1]   # 398: the note before off its chord\n'
      '            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None'),
    P('SHAPE = None\nCONTOURS = {', 'SHAPE = None\nPREV_NC = [False]\nCONTOURS = {'),
    P('LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=1.0, on16=1.0)',
      'LK = dict(amp=5.0, widen=1.0, fresh=2.0, leap=1.0, s16=1.0, ctl=1.0, offb=1.0, dpk=1.0, k44=1.0, g8=1.0, g4=1.0, glong=1.0, run=1.0, on16=1.0,\n'
      '          ct398=1.0, ctb398=1.0, ctd398=1.0, res398=1.0, turn400=1.0)                            # 398, 400: one knob each, from one'),
    P('                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"]:',
      '                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"] + list(KEPT398) + ["turns_per_move"]:'),
    P('            LK["k44"] = float(np.clip(LK["k44"]',
      '            if ON("398"):                                                                     # 398: each rate toward its kept mean by one knob on unaimed builds\n'
      '                for kn_, m_ in (("ct398", "chord_tones"), ("ctb398", "chord_tones_on_beat"), ("ctd398", "chord_tones_on_downbeat"), ("res398", "non_chord_resolved_by_step")):\n'
      '                    if not ua.get(m_): continue\n'
      '                    r_ = float(np.mean(ua[m_])); f_ = float(np.clip((max(0.02, KEPT398[m_]) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK[kn_] = float(np.clip(LK[kn_] * f_, 0.1, 10.0))\n'
      '                    if f_ in (0.6, 1.6): full_now.add(kn_)\n'
      '                row["398 (kept, unaimed reading, knob)"] = {m_: (KEPT398[m_], round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[kn_], 3)) for kn_, m_ in (("ct398", "chord_tones"), ("ctb398", "chord_tones_on_beat"), ("ctd398", "chord_tones_on_downbeat"), ("res398", "non_chord_resolved_by_step"))}\n'
      '            if ON("400") and ua.get("turns_per_move"):                                        # 400: turns per move toward the kept 0.58 by one knob on unaimed builds\n'
      '                r_ = float(np.mean(ua["turns_per_move"])); f_ = float(np.clip((KEPT400 / max(0.05, r_)) ** 2, 0.6, 1.6)); LK["turn400"] = float(np.clip(LK["turn400"] * f_, 0.1, 10.0))\n'
      '                if f_ in (0.6, 1.6): full_now.add("turn400")\n'
      '                row["400 (kept, unaimed reading, knob)"] = (KEPT400, round(r_, 3), round(LK["turn400"], 3))\n'
      '            LK["k44"] = float(np.clip(LK["k44"]'),
    P('STOP356 = []\n', 'STOP356 = []\nKEPT398 = dict(chord_tones=0.639, chord_tones_on_beat=0.669, chord_tones_on_downbeat=0.722, non_chord_resolved_by_step=0.501)   # 398 (zeneng_v119_families.json)\nKEPT400 = 0.584                                                                          # 400\n'),
    # 400: turns per move aimed again, by one knob on the walk's choice to continue or turn (both pools); 249's turn and 398's measures leave its calibration
    P('        self.turn = K["turn"] * r("turns_per_move") if p == "V" else 1.0',
      '        self.turn = LK["turn400"] if ON("400") else (K["turn"] * r("turns_per_move") if p == "V" else 1.0)   # 400 (reverses 304)'),
    P('                if p == "C" and kn == "turn": continue',
      '                if (p == "C" or ON("400")) and kn == "turn": continue                          # 304; 400: one knob, on unaimed builds\n'
      '                if ON("398") and kn in ("ct_on", "ct_off"): continue                            # 398: one knob a measure'),
    # 390: returns the plan gives count toward 371's rate, read on the units free to draw
    P('                    if f_ and np.isfinite(f_.get(m_, np.nan)): ua["_ur" + str(j_)].append(f_[m_])',
      '                    if f_ and np.isfinite(f_.get(m_, np.nan)) and not (ON("390") and c2["meta"].get("ur_given", {}).get(KIND[s_], {}).get(j_)): ua["_ur" + str(j_)].append(f_[m_])   # 390: read on the free units'),
    P('    # 329: one fresh line carries',
      '    if ON("390"):                                                                          # 390: a unit the plan already returns is not drawn again\n'
      '        meta["ur_given"] = {}\n'
      '        for k_, d_ in UR.items():\n'
      '            s1_ = next(s_ for s_ in SUNG if KIND[s_] == k_); g_ = {}\n'
      '            for j, (src, kept_, _m) in UR_KEPT.items():\n'
      '                ls_ = [ii for ii in range(len(LINES[s1_])) if 2 * j * BAR <= line_start(s1_, ii) - BAR0[s1_] * BAR < 2 * (j + 1) * BAR]\n'
      '                def _given(ii):\n'
      '                    h_, s_, i_ = how(s1_, ii)\n'
      '                    return h_ in ("plan", "return", "copy") and s_ == s1_ and line_start(s1_, ii) - line_start(s1_, i_) == 2 * (j - src) * BAR\n'
      '                if ls_ and all(_given(ii) for ii in ls_):\n'
      '                    g_[j] = True; STATS[f"390: unit {j + 1} returned by the plan"] += 1\n'
      '                    if j in d_: d_.pop(j); STATS["390: drawn unit return dropped (the plan gives it)"] += 1\n'
      '            meta["ur_given"][k_] = g_\n'
      '        meta["unit_returns"] = {k_: dict(v) for k_, v in UR.items()}\n'
      '    # 329: one fresh line carries'),
    # 391: a span widened to the kept 5th to 95th percentiles before it is given up
    P('        free = _try >= NT or (fits is not None and not fits)\n',
      '        if ON("391") and s_span is not None and _try == NT // 2: s_span = rng.uniform(*span_wide(n)); STATS["391: span widened to the kept 5th-95th"] += 1\n'
      '        free = _try >= NT or (fits is not None and not fits)\n'),
    P('def span_mid(n): return next((q[1], q[3]) for k_, q in SPAN_MID if n <= k_)',
      'def span_wide(n): return next((q[0], q[4]) for k_, q in SPAN_MID if n <= k_)               # 391: the kept 5th to 95th percentiles\n'
      'def span_mid(n): return next((q[1], q[3]) for k_, q in SPAN_MID if n <= k_)'),
    # 392 (song 45): the chorus floor for drawn notes is the verse's drawn median plus the writer's lift
    P('    ch_ = hi; cl_ = max(lo, min(vc_ - 1, ch_ - 8)); cm_ = (cl_ + ch_) / 2',
      '    ch_ = hi; cl_ = max(lo, min(ch_ - 3, int(round(vm_ + 3)))) if ON("392") else max(lo, min(vc_ - 1, ch_ - 8)); cm_ = (cl_ + ch_) / 2   # 392: the verse\'s drawn median plus the lift (Q14 A: 3)', 1, ("45",)),
    # 393: verse 2's share read on the lines with verse 1's syllable count
    P('    def bars(s):\n', '    eq_ = {i_ for i_ in range(min(len(LINES["Verse 1"]), len(LINES["Verse 2"]))) if len(LINES["Verse 2"][i_]) == len(LINES["Verse 1"][i_])} if (ON("393") and "Verse 2" in LINES) else None   # 393\n'
      '    if eq_ is not None and not eq_: eq_ = None\n'
      '    def bars(s):\n'),
    P('            if n["sec"] == s: out[n["on"] // BAR - BAR0[s]].add(n["on"] % BAR)',
      '            if n["sec"] == s and (eq_ is None or s != "Verse 2" or int(n["line"].rsplit(":", 1)[1]) in eq_): out[n["on"] // BAR - BAR0[s]].add(n["on"] % BAR)'),
    P('    rerun["v119_step"] = V119;', '    rerun["knobs398_400"] = {k_: round(LK[k_], 4) for k_ in ("ct398", "ctb398", "ctd398", "res398", "turn400")}\n    rerun["v119_step"] = V119;'),
    # 424 (v120): the aims that hold on both collections, each by one knob on unaimed builds, toward the pooled kept means (CoCoPops and BiMMuDa, 1958-1991)
    P('        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])',
      '        if c[0] == "larger": c = (c[0], c[1] * LK["leap"], c[2])\n'
      '        if c[0] == "fourth_fifth" and ON("424"): c = (c[0], c[1] * LK["ff424"], c[2])         # 424: leaps of a fourth or fifth'),
    P('                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape)',
      '                    CUR424[0] = sec\n'
      '                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx, shape=shape); CUR424[0] = None'),
    P('            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None',
      '            LAST424[0] = ON("424") and CUR424[0] is not None and i == len(notes) - 1 and (n["on"] // BAR - BAR0[CUR424[0]]) % 8 == 7   # 424: a window\'s last note\n'
      '            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None; LAST424[0] = False'),
    P('                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_); base += w0',
      '                lt_ = LK["lt424"] if (LAST424[0] and (p - mton()) % 12 == 0) else 1.0             # 424: the window\'s last note on the tonic\n'
      '                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_ * lt_); base += w0'),
    P('rng.choices(cands, [math.exp(-(p - tgt) ** 2 / 4.5) for p in cands])[0]   # 314',
      'rng.choices(cands, [math.exp(-(p - tgt) ** 2 / 4.5) * (LK["lt424"] if (ON("424") and (p - mton()) % 12 == 0 and (ns[-1]["on"] // BAR - BAR0[sec]) % 8 == 7) else 1.0) for p in cands])[0]   # 314; 424'),
    P('SHAPE = None\nPREV_NC = [False]\n', 'SHAPE = None\nPREV_NC = [False]\nCUR424 = [None]; LAST424 = [False]\n'),
    P('          ct398=1.0, ctb398=1.0, ctd398=1.0, res398=1.0, turn400=1.0)',
      '          ct398=1.0, ctb398=1.0, ctd398=1.0, res398=1.0, turn400=1.0, ff424=1.0, lt424=1.0, eb424=0.25)   # 424: the empty-bar rate starts at a quarter'),
    # empty bars: a line of two bars or more drawn, at a rate, to leave its slot's last bar unsung
    P('        ons = sample(alpha)\n'
      '        if ons is None: continue\n',
      '        ons = sample(alpha)\n'
      '        if ons is None: continue\n'
      '        if eb424 and not free and _try < NT // 2 and max(ons) >= (slot_len(sec, i) - 1) * BAR: STATS["424: redrawn to leave the slot\'s last bar empty"] += 1; continue\n'
      '        if eb424 and _try >= NT // 2 and max(ons) >= (slot_len(sec, i) - 1) * BAR: STATS["424: empty bar given up for a line"] += 1; eb424 = False\n'
      '        if eb424: STATS["424: line leaves its slot\'s last bar empty"] += 1\n'),
    P('    sp = span_mid(n) if (span_to is not None and not fix) else None                          # 378: the span drawn first',
      '    eb424 = bool(ON("424") and i is not None and slot_len(sec, i) >= 2 and not fix and rng.random() < LK["eb424"])   # 424: bars left empty, at a rate\n'
      '    sp = span_mid(n) if (span_to is not None and not fix) else None                          # 378: the span drawn first'),
    P('                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"] + list(KEPT398) + ["turns_per_move"]:',
      '                for m_ in list(KEPT114) + list(GAPS) + ["notes_per_bar", "on_sixteenth", "distinct_durations"] + list(KEPT398) + ["turns_per_move"] + list(KEPT424):'),
    P('            if ON("400") and ua.get("turns_per_move"):',
      '            if ON("424"):                                                                     # 424: toward the pooled kept means\n'
      '                for kn_, m_ in (("ff424", "fourth_fifth"), ("lt424", "last_note_tonic")):\n'
      '                    if not ua.get(m_): continue\n'
      '                    r_ = float(np.mean(ua[m_])); f_ = float(np.clip((max(0.02, KEPT424[m_]) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK[kn_] = float(np.clip(LK[kn_] * f_, 0.1, 10.0))\n'
      '                    if f_ in (0.6, 1.6): full_now.add(kn_)\n'
      '                if ua.get("empty_bars"):\n'
      '                    r_ = float(np.mean(ua["empty_bars"])); f_ = float(np.clip(max(0.02, KEPT424["empty_bars"]) / max(0.02, r_), 0.6, 1.6)); LK["eb424"] = float(np.clip(LK["eb424"] * f_, 0.0, 1.0))\n'
      '                    if f_ in (0.6, 1.6) and 0.0 < LK["eb424"] < 1.0: full_now.add("eb424")\n'
      '                row["424 (pooled kept, unaimed reading, knob)"] = {m_: (KEPT424[m_], round(float(np.mean(ua[m_])), 3) if ua.get(m_) else None, round(LK[k_], 3)) for k_, m_ in (("ff424", "fourth_fifth"), ("lt424", "last_note_tonic"), ("eb424", "empty_bars"))}\n'
      '            if ON("400") and ua.get("turns_per_move"):'),
    P('KEPT400 = 0.584                                                                          # 400\n',
      'KEPT400 = 0.584                                                                          # 400\n'
      '_SC120 = {r_["measure"]: r_ for r_ in json.load(open(f"{H118}/tables/zeneng_v120_second_collection.json"))["every measure: collections\' gap in sd, means (CoCoPops, BiMMuDa 1958-1991, builds v118)"]}\n'
      'KEPT424 = {m_: round((314 * _SC120[m_]["cocopops"] + 231 * _SC120[m_]["bimmuda"]) / 545, 4) for m_ in ("fourth_fifth", "last_note_tonic", "empty_bars")}   # 424: both collections pooled (314 and 231 windows)\n'),
    P('                if ON("398") and kn in ("ct_on", "ct_off"): continue                            # 398: one knob a measure',
      '                if ON("398") and kn in ("ct_on", "ct_off"): continue                            # 398: one knob a measure\n'
      '                if ON("424") and kn == "fourth_fifth": continue                                  # 424: one knob, on unaimed builds'),
    P('    rerun["knobs398_400"] = {k_: round(LK[k_], 4) for k_ in ("ct398", "ctb398", "ctd398", "res398", "turn400")}\n',
      '    rerun["knobs398_400"] = {k_: round(LK[k_], 4) for k_ in ("ct398", "ctb398", "ctd398", "res398", "turn400")}\n'
      '    rerun["knobs424"] = {k_: round(LK[k_], 4) for k_ in ("ff424", "lt424", "eb424")}; rerun["kept424"] = KEPT424\n'),
]
PATCHES = STEP1 + STEP2 + STEP3

def port(song):
    s = open(f"{SRC}/melody_v118_p{song}.py").read()
    s = s.replace("/home/claude/p50", DST).replace("melody_v118_", "melody_v119_")
    for old, new, cnt, only in PATCHES:
        if only and song not in only: continue
        k = s.count(old)
        if k != cnt: sys.exit(f"song {song}: patch not matched {k} times (want {cnt}): {old[:90]!r}")
        s = s.replace(old, new)
    assert s.startswith('"""') or s.startswith("#") or True
    s = HEADER + s
    open(f"{DST}/melody_v119_p{song}.py", "w").write(s)
    compile(s, f"melody_v119_p{song}.py", "exec")
    print(song, "ok", len(s.splitlines()), "lines")

for so in SONGS: port(so)
