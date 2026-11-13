"""v129 (ZenEng v129, Module 27.73): the session's 500-518 as ruled, ported once onto Run 3's final code (songs/p54, melody_v128_*.py),
with no new aims (521). Songs 40, 42 and 43 keep Run 3's Part 2 (their 438 charts); songs 44 and 45 keep Run 3's Part 1 (their own charts).
Whole-statement patches, each matched the stated number of times (384). ZE_PART=0 reproduces Run 3 as it stood; ZE_PART=1 (default) is the port:
  500 465's class drawn by the slot's length as well as the line's notes; the classes out of a slot's reach counted
  501 458 read in onsets a beat between the first and last onset (the kept 25th-75th by notes), for half a line's tries
  502 song 45: 392's floor at the verse's median and three (the lift)
  503 verse 2's chord tones on the beat aimed at verse 1's by one knob in the sing-again walk
  504 452's band knobs keyed by the line's own notes a bar (syllables a slot bar times the song's notes to syllables)
  505 the run weight aimed alone: 389's rate held at one; the runs read on every section of the band, on two rounds' builds (60)
  508 a return or sung-again line is fitted to the breath a designed line before it needs (the line a copy follows)
  513 440's step tested on the finished chart; an inversion that has lost it is taken back
  519 the content judge of record is zeneng_v129_judge.json (the engine's reading); its kept fifth percentiles printed
  520 455 and 408 withdrawn: no knob named for either in the run
Usage: python3 gen_v129.py  (writes /home/claude/p55/melody_v129_p40.py ... _p45.py)"""
import os, sys, json
SRC = "/home/claude/p54"; DST = os.environ.get("GEN_DST", "/home/claude/p55")
SONGS = ("40", "42", "43", "44", "45"); V128_OF = {"40": 2, "42": 2, "43": 2, "44": 1, "45": 1}
HEADER = '''"""ZenEng v129 (Module 27.73) onto Run 3 (songs/p54), by gen_v129.py. ZE_PART: 0 = Run 3 as it stood (this song at Run 3's Part {v8}); 1 = the port
(500-505, 508, 513, 519, 520). ZE_OFF switches a fix off (side runs only).
"""
import os as _os9
V129 = int(_os9.environ.get("ZE_PART", "1"))
P129 = {{f_: 1 for f_ in ("500", "501", "502", "503", "504", "505", "508", "513", "519", "520")}}
OFF9 = set(filter(None, _os9.environ.get("ZE_OFF", "").split(",")))
def ON9(f_): return P129.get(f_, 0) <= V129 and f_ not in OFF9
'''
def P(old, new, count=1, songs=None): return (old, new, count, songs)
KL = json.load(open("/home/claude/p55/tables/zeneng_v128_kept_lines.json"))
T465 = KL["465: where a kept line's last onset falls before the next line, by notes in the line"]
K_CLS = "the last onset's bar, counted back from the bar in which the next line begins (0 = the same bar, 1 = the bar before, 2, 3 or more): share of lines"
NB = ("3 to 5", "6 to 8", "9 to 12", "13 and over"); CK = ("0", "1", "2", "3 or more")
lines_ = [T465[b]["lines"] for b in NB]
PALL = [sum(T465[b][K_CLS][c] * l for b, l in zip(NB, lines_)) / sum(lines_) for c in CK]
TS = KL["465: the same by the slot's length"]
SL465 = [(6, TS["slot of 6 beats or less"]["last onset's bar counted back (0, 1, 2, 3 or more)"]), (10, TS["over 6 to 10 beats (two bars)"]["last onset's bar counted back (0, 1, 2, 3 or more)"]),
         (999, TS["over 10 to 16 beats (four bars)"]["last onset's bar counted back (0, 1, 2, 3 or more)"])]
T458 = KL["458: syllables a second across a kept line's sung span, by notes in the line"]
OB501 = [(5, T458["3 to 5"]["onsets a beat between the first and last onset (5, 25, 50, 75, 95)"]), (8, T458["6 to 8"]["onsets a beat between the first and last onset (5, 25, 50, 75, 95)"]),
         (12, T458["9 to 12"]["onsets a beat between the first and last onset (5, 25, 50, 75, 95)"]), (999, T458["13 and over"]["onsets a beat between the first and last onset (5, 25, 50, 75, 95)"])]
PATCHES = [
    # ---- 520: 455 withdrawn (its weight already one under 490); 408's width knob gone from the knobs and the record
    P('def ON7(f_): return P127.get(f_, 0) <= V127 and f_ not in OFF and not (f_ in ("408", "467") and ON8("491"))',
      'def ON7(f_): return P127.get(f_, 0) <= V127 and f_ not in OFF and not (f_ in ("408", "467") and ON8("491")) and not (f_ == "455" and ON9("520"))   # 520'),
    P('rg467=1.0, sh408=1.0)', 'rg467=1.0)'),
    P('"rg467", "sh408", "turn400")} | {"s16_by_band": {b_: round(v_, 4) for b_, v_ in S16B.items()}}', '"rg467", "turn400")}   # 520: no knob named for 408 or 455'),
    # ---- 519: the v129 judge
    P('RJ = json.load(open(f"{H118}/tables/" + ("zeneng_v128_judge.json" if ON8("476") else "zeneng_v126_judge.json")))["content_judge"]',
      'RJ = json.load(open(f"{H118}/tables/" + ("zeneng_v129_judge.json" if ON9("519") else "zeneng_v128_judge.json" if ON8("476") else "zeneng_v126_judge.json")))["content_judge"]   # 519'),
    # ---- 502 (song 45): the floor at the verse's median and three
    P('cl_ = (max(lo, min(ch_ - 3, int(round(vm_ + 3)), max(ch_ - 8, int(round(2 * (vm_ + 3) - ch_ + 2))))) if ON8("491") else max(lo, min(ch_ - (8 if ON7("467") else 3), int(round(vm_ + 3))))) if ON("392")',
      'cl_ = (max(lo, min(ch_ - 3, int(round(vm_ + 3)))) if ON9("502") else (max(lo, min(ch_ - 3, int(round(vm_ + 3)), max(ch_ - 8, int(round(2 * (vm_ + 3) - ch_ + 2))))) if ON8("491") else max(lo, min(ch_ - (8 if ON7("467") else 3), int(round(vm_ + 3)))))) if ON("392")', 1, ("45",)),
    # ---- 500: the class by the slot's length as well as the notes (the two kept shares combined over the kept classes' overall share)
    P('C465 = [None]; CLS465 = [None]; REQ465 = {}; CURB8 = [None]; AGAIN478 = [False]\n',
      'C465 = [None]; CLS465 = [None]; REQ465 = {}; CURB8 = [None]; AGAIN478 = [False]\n'
      f'SL465 = {SL465!r}   # 500: by the slot\'s beats\n'
      f'PALL465 = {[round(x, 4) for x in PALL]!r}   # 500: the kept classes\' overall shares (lines weighted)\n'
      f'OB501 = {OB501!r}   # 501: onsets a beat between the first and last onset, by notes\n'
      'MEL504 = [1.0]; P505 = {}\n'
      'def band504(n_, sec, i):\n'
      '    """504: the line\'s own notes a bar: its syllables a slot bar times the song\'s notes to syllables (read on unaimed builds)."""\n'
      '    return kband(n_ * MEL504[0] / max(1, slot_len(sec, i))) if i is not None else SEC_BAND[sec]\n'
      'def tmin508(sec, i):\n'
      '    """508: a designed line known ahead keeps the breath before the line after it."""\n'
      '    fx_ = globals().get("FIXR", {})\n'
      '    if not ON9("508") or not i or (sec, i - 1) not in fx_: return -12\n'
      '    t_ = line_start(sec, i - 1) + max(fx_[(sec, i - 1)].values()) + GAP_MIN - line_start(sec, i)\n'
      '    STATS["508: fitted to the breath of the designed line before"] += 1\n'
      '    return max(-12, int(t_ // 3 * 3 + (3 if t_ % 3 else 0)))\n'),
    P('    sh_ = next(s_ for k_, s_ in SH465 if n <= k_); lo_l = tmin + step * (n - 1); opts = []\n',
      '    sh_ = next(s_ for k_, s_ in SH465 if n <= k_); lo_l = tmin + step * (n - 1); opts = []\n'
      '    if ON9("500"):                                                                          # 500: by the slot\'s length as well\n'
      '        ss_ = next(s_ for k_, s_ in SL465 if c_["nb"] * 4 <= k_)\n'
      '        sh_ = [a_ * b_ / max(1e-9, p_) for a_, b_, p_ in zip(sh_, ss_, PALL465)]\n'),
    P('        if a_ <= b_ and sh_[k_] > 0 and (feas is None or feas(a_, b_)): ok_.append((k_, a_, b_, rq_))\n',
      '        if a_ <= b_ and sh_[k_] > 0 and (feas is None or feas(a_, b_)): ok_.append((k_, a_, b_, rq_))\n'
      '        elif sh_[k_] > 0 and ON9("500"): STATS[f"500: class {k_} out of reach, {c_[\'nb\']}-bar slot, {n} syllables"] += 1\n'),
    # ---- 501: 458 in onsets a beat (the seconds bound off), held for half the tries
    P('    if sp and ON("414") and span_to * M.SEC_PER_TW > 0:', '    if sp and ON("414") and span_to * M.SEC_PER_TW > 0 and not ON9("501"):'),
    P('        h465 = bool(d465 is not None and _try < NT // 2 and not free and tgt is None)\n',
      '        h465 = bool(d465 is not None and _try < NT // 2 and not free and tgt is None)\n'
      '        h501 = bool(ON9("501") and span_to is not None and not fix and n >= 3 and _try < NT // 2 and not free)\n'
      '        if ON9("501") and span_to is not None and not fix and n >= 3 and _try == NT // 2: STATS["501: onsets a beat given up for a line"] += 1\n'),
    P('        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy\n',
      '        if h501:                                                                           # 501: the kept onsets a beat (25th-75th) across the line\n'
      '            q_ = next(x_ for k_, x_ in OB501 if n <= k_); ob_ = (n - 1) / max(0.25, (ons[-1] - ons[0]) / BEAT)\n'
      '            if not (q_[1] <= ob_ <= q_[3]): STATS["501: outside the kept onsets a beat, redrawn"] += 1; continue\n'
      '            STATS["501: line inside the kept onsets a beat"] += 1\n'
      '        if cb:                                                                             # 303 with 351: a bar off by more than one onset leaves the copy\n'),
    # ---- 503: verse 2's chord tones on the beat, one knob in the sing-again walk
    P('    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]',
      '    if ON9("503") and AGAIN478[0] and on_beat and p % 12 in tones: w *= LK["ctb503"]     # 503\n'
      '    if n.get("dur", 0) >= 12 and p % 12 in tones: w *= LK["ctl"]'),
    P('rep478=1.0, stp478=1.0,', 'rep478=1.0, stp478=1.0, ctb503=1.0,'),
    P('                    for x_, w_ in (("1", w1_), ("2", w2_)):\n',
      '                    if ON9("503"):\n'
      '                        f1_, f2_ = win_feats(c2["notes"], BAR0["Verse 1"]), win_feats(c2["notes"], BAR0["Verse 2"])\n'
      '                        if f1_ and f2_ and np.isfinite(f1_.get("chord_tones_on_beat", np.nan)) and np.isfinite(f2_.get("chord_tones_on_beat", np.nan)):\n'
      '                            ua["_ctb1"].append(f1_["chord_tones_on_beat"]); ua["_ctb2"].append(f2_["chord_tones_on_beat"])\n'
      '                    for x_, w_ in (("1", w1_), ("2", w2_)):\n'),
    P('                row["478 (verse 1, verse 2 unaimed, knob)"] = o_\n',
      '                row["478 (verse 1, verse 2 unaimed, knob)"] = o_\n'
      '            if ON9("503") and ua.get("_ctb2"):                                                 # 503: verse 2\'s chord tones on the beat toward verse 1\'s\n'
      '                t_, r_ = float(np.mean(ua["_ctb1"])), float(np.mean(ua["_ctb2"])); f_ = float(np.clip((max(0.02, t_) / max(0.02, r_)) ** 2, 0.6, 1.6)); LK["ctb503"] = float(np.clip(LK["ctb503"] * f_, 0.05, 20.0))\n'
      '                if f_ in (0.6, 1.6): full_now.add("ctb503")\n'
      '                row["503 (verse 1, verse 2 unaimed, knob)"] = (round(t_, 3), round(r_, 3), round(LK["ctb503"], 3))\n'),
    # ---- 504: the band knobs by the line's own notes a bar
    P('                    b_ = B489.get(SEC_BAND[sec]) if ON8("489") else None\n',
      '                    b_ = B489.get(band504(n, sec, i) if ON9("504") else SEC_BAND[sec]) if ON8("489") else None\n'),
    P('                    b_ = SEC_BAND[s_]; kd_ = KD489[kd_band(len(N_) / 8)]',
      '                    b_ = kband(len(N_) / 8) if ON9("504") else SEC_BAND[s_]; kd_ = KD489[kd_band(len(N_) / 8)]\n'
      '                    if ON9("504"): ua["_mel504"].append(len(N_) / max(1, sum(1 for n_ in c2["notes"] if BAR0[s_] * BAR <= n_["on"] < (BAR0[s_] + 8) * BAR and not n_.get("slur"))))'),
    P('                row["489 (kept, unaimed reading, knob)"] = o_\n',
      '                row["489 (kept, unaimed reading, knob)"] = o_\n'
      '                if ON9("504") and ua.get("_mel504"): MEL504[0] = float(np.mean(ua["_mel504"])); row["504: notes to syllables"] = round(MEL504[0], 3)\n'),
    P('                for _try in range(8):\n', '                if ON9("504"): CURB8[0] = band504(len(sy), sec, i)                   # 504: the zigzag knob by the line\'s band\n                for _try in range(8):\n'),
    P('                ns = sing_again(rng, S, LINES[s0][i0], sy, line_start(s0, i0), U, tmin, sec, lo, hi, notes_on_all, last_max, ons=pf[1] if pf else None)',
      '                if ON9("504"): CURB8[0] = band504(len(sy), sec, i)\n'
      '                ns = sing_again(rng, S, LINES[s0][i0], sy, line_start(s0, i0), U, tmin, sec, lo, hi, notes_on_all, last_max, ons=pf[1] if pf else None)'),
    # ---- 505: the run weight alone; 389's rate held at one; read on every section of the band, on two rounds' builds
    P('    jb_ = {SEC_BAND[x_] for x_ in ("Verse 1", "Chorus 1") if x_ in SEC_BAND} if ON8("486") else set()\n',
      '    jb_ = {SEC_BAND[x_] for x_ in ("Verse 1", "Chorus 1") if x_ in SEC_BAND} if (ON8("486") and not ON9("505")) else set()   # 505: every section of the band\n'),
    P('                        n_ = sum(ua.get("_n6b" + b_, [])); r_ = sum(ua.get("_r6b" + b_, []))\n',
      '                        n_ = sum(ua.get("_n6b" + b_, [])); r_ = sum(ua.get("_r6b" + b_, []))\n'
      '                        if ON9("505"): pn_, pr_ = P505.get(b_, (0, 0)); P505[b_] = (n_, r_); n_ += pn_; r_ += pr_   # 505: this round\'s builds and the last\n'),
    P('RUNR[b_] = float(np.clip(RUNR[b_] * f_, 0.0, 1.0)); S16B[b_]', 'RUNR[b_] = 1.0 if ON9("505") else float(np.clip(RUNR[b_] * f_, 0.0, 1.0)); S16B[b_]'),
    P('                        if ON8("490"): R490[b_] = float(np.clip(R490[b_] * f_, 0.02, 20.0))   # 490: the run weight, toward the band\'s kept share\n',
      '                        if ON8("490"): R490[b_] = float(np.clip(R490[b_] * f_, 0.02, 20.0))   # 490: the run weight, toward the band\'s kept share\n'
      '                        if ON9("505") and f_ in (0.6, 1.6): full_now.add("run490 " + b_)\n'),
    # ---- 508: the return fitted to the breath the designed line before it needs
    P('ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, -12, lo_, hi_, notes_on_all, endok=endok_of(sec, i))',
      'ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, tmin508(sec, i), lo_, hi_, notes_on_all, endok=endok_of(sec, i))'),
    P('ons = line_rhythm(LINES[sec][i], rng, -12, sec, i=i, **again_kw(built[(s0, i0)], line_start(s0, i0))); globals()["AIM"] = AIMP',
      'ons = line_rhythm(LINES[sec][i], rng, tmin508(sec, i), sec, i=i, **again_kw(built[(s0, i0)], line_start(s0, i0))); globals()["AIM"] = AIMP'),
    # ---- 513: the step tested on the finished chart
    P('    H_ = full(); s2_, sh_, nev_ = chart_shares(full())\n',
      '    rev513 = []\n'
      '    if ON9("513") and inv:                                                                   # 513: every inversion keeps a step on the finished chart\n'
      '        def bm9(a_, b2_): d_ = (b2_ - a_) % 12; return d_ if d_ <= 6 else d_ - 12\n'
      '        for it_ in range(20):\n'
      '            F_ = full(); ch9 = [c_ for h_, c_ in enumerate(F_) if h_ == 0 or c_ != F_[h_ - 1]]; bad9 = set()\n'
      '            for j_, c_ in enumerate(ch9):\n'
      '                if c_ not in BASS8: continue\n'
      '                nb_ = [ch9[j_ + d_] for d_ in (-1, 1) if 0 <= j_ + d_ < len(ch9)]\n'
      '                if not any(abs(bm9(bass_of(x_), bass_of(c_))) in (1, 2) for x_ in nb_): bad9.add(c_)\n'
      '            if not bad9: break\n'
      '            nm_ = sorted(bad9)[0]; base_ = nm_.split("/")[0]\n'
      '            for U_ in units.values():\n'
      '                for q_ in range(len(U_)):\n'
      '                    if U_[q_] == nm_: U_[q_] = base_\n'
      '            inv = [x_ for x_ in inv if x_[2] != nm_]; rev513.append(nm_)\n'
      '    H_ = full(); s2_, sh_, nev_ = chart_shares(full())\n'),
    P('ops=ops, inversions=inv,', 'ops=ops, inversions=inv, reverted513=rev513,'),
    # ---- the record
    P('    rerun["v128_part"] = V128;', '    rerun["v129_part"] = V129; rerun["v129_on"] = sorted(f_ for f_ in P129 if ON9(f_))\n'
      '    rerun["knobs129"] = dict(ctb503=round(LK["ctb503"], 4), mel504=round(MEL504[0], 4), runr={b_: round(v_, 4) for b_, v_ in RUNR.items()})\n    rerun["v128_part"] = V128;'),
]

def port(song):
    s = open(f"{SRC}/melody_v128_p{song}.py").read()
    s = s.replace("/home/claude/p54", DST).replace("melody_v128_", "melody_v129_")
    old = 'V128 = int(_os8.environ.get("ZE_PART", "3"))'
    assert s.count(old) == 1
    s = s.replace(old, f'V128 = {V128_OF[song]}                                                                          # v129: this song as Run 3 left it')
    for old, new, cnt, only in PATCHES:
        if only and song not in only: continue
        k = s.count(old)
        if k != cnt: sys.exit(f"song {song}: patch not matched {k} times (want {cnt}): {old[:90]!r}")
        s = s.replace(old, new)
    s = HEADER.format(v8=V128_OF[song]) + s
    open(f"{DST}/melody_v129_p{song}.py", "w").write(s); compile(s, f"melody_v129_p{song}.py", "exec")
    print(song, "ok", len(s.splitlines()), "lines")

if __name__ == "__main__":
    for so in SONGS: port(so)
