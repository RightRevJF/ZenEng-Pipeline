"""v127 Run 2 (ZenEng v127, Modules 27.69-27.71): the judge of record refitted and the session's adopted fixes, ported onto Run 1 (songs/p52) by parts.
384: every patch replaces whole statements, matched the stated number of times in each file it names. The parts are switched by ZE_PART (default 3),
so that each part's runs can be made again from the final files:
  part 0 (no rerun of its own): the judge (470 content from the refit, 471 the floor on the v108 judge, 472 the refit's pick, 473 no second verse),
         464 (267 reads song 45's bridge G before its raise), 459 (verse 2's bars where syllable counts differ by one or less)
  part 1, the second verse: 434 (sing-again: no move of stressed on-beat notes to chord tones, no repeat the source did not sing; verse 2's
         chord tones from 398's knobs, as verse 1's), 435 (where both verses strike the same place, verse 1's pitch at three in four)
  part 2, rhythm: 452, 455, 406, 465, 457, 458
  part 3, pitch: 408 with 468, 467, 461 with 450, 456
Usage: python3 gen_v127.py  (writes melody_v127_p40.py ... melody_v127_p45.py)"""
import os, sys
SRC = "/home/claude/p52"; DST = os.environ.get("GEN_DST", "/home/claude/p53")
SONGS = ("40", "42", "43", "44", "45")
HEADER = '''"""ZenEng v127 Run 2 (Modules 27.69-27.71) onto Run 1 (songs/p52), by gen_v127.py. ZE_PART: 0 = the judge (470-473), 464, 459; 1 = and 434, 435;
2 = and 452, 455, 406, 465, 457, 458; 3 = and 408/468, 467, 461/450, 456. ZE_OFF switches a fix off (side runs only).
"""
'''
def P(old, new, count=1, songs=None): return (old, new, count, songs)

PART0 = [
    P('CUR405 = [None]; DRAWN398 = [False]\n',
      'CUR405 = [None]; DRAWN398 = [False]\n'
      'V127 = int(os.environ.get("ZE_PART", "3"))                                              # v127 Run 2: the parts, runs between them\n'
      'P127 = {f_: 0 for f_ in ("470", "471", "472", "473", "464", "459")} | {f_: 1 for f_ in ("434", "435")} | {f_: 2 for f_ in ("452", "455", "406", "465", "457", "458")} | {f_: 3 for f_ in ("408", "468", "467", "461", "456")}\n'
      'def ON7(f_): return P127.get(f_, 0) <= V127 and f_ not in OFF\n'
      'PICK108 = [None, None]\n'),
    # ---- 470: the content judge of record is the refit (zeneng_v126_judge.json); 473: it reads the first verse and chorus only, as before
    P('def judge(notes):\n',
      'RJ = json.load(open(f"{H118}/tables/zeneng_v126_judge.json"))["content_judge"]                 # 470\n'
      'exec(next(v_ for k_, v_ in json.load(open(f"{H118}/tables/zeneng_v121_blind_spots.json")).items() if k_.startswith("code: cand")))   # cand(): the four new measures\n'
      'RJ_MU, RJ_SD, RJ_W, RJ_F = (np.array(RJ[k_], float) for k_ in ("mean", "sd", "weight", "fill_missing_with"))\n'
      'def refit_score(f, N):\n'
      '    """470: intercept + sum of weight x (value - mean) / sd over the 37 measures; a measure the window lacks takes the kept median."""\n'
      '    f = f or {}; c_ = cand(sorted(N)) or {}; x_ = []\n'
      '    for m_, fill_ in zip(RJ["measures"], RJ_F):\n'
      '        v_ = f.get(m_) if m_ in f else c_.get(m_)\n'
      '        x_.append(fill_ if v_ is None or not np.isfinite(v_) else v_)\n'
      '    return float(RJ["intercept"] + RJ_W @ ((np.array(x_, float) - RJ_MU) / RJ_SD))\n'
      'def judge(notes):\n'),
    P('N = win_N(notes, BAR0[s]); f = feats(N, mton()); rows[s] = dict(J.score_window(f, N), feats=f)',
      'N = win_N(notes, BAR0[s]); f = feats(N, mton()); rows[s] = dict(J.score_window(f, N), feats=f); rows[s]["refit"] = refit_score(f, N)'),
    P('    return dict(combined=float(np.mean([r["combined"] for r in rows.values()])), content=float(np.mean([r["content"] for r in rows.values()])),',
      '    return dict(refit_content=float(np.mean([r["refit"] for r in rows.values()])), refit_combined=float(np.mean([(r["refit"] + r["order"]) / 2 for r in rows.values()])),   # 470: the order judge and the combining unchanged\n'
      '                combined=float(np.mean([r["combined"] for r in rows.values()])), content=float(np.mean([r["content"] for r in rows.values()])),'),
    P('rec["judge"] = {k: c["judge"][k] for k in ("combined", "content", "order")}',
      'rec["judge"] = {k: c["judge"][k] for k in ("combined", "content", "order", "refit_content", "refit_combined")}'),
    # ---- 472: the pick is the refit's first among survivors with no soft break; 471: the floor stays on the v108 judge (gate_fails unchanged)
    P('    pick = clean[0] if clean else (byj[0] if byj else None); pick_352 = byj[0] if byj else None\n',
      '    pick = clean[0] if clean else (byj[0] if byj else None); pick_352 = byj[0] if byj else None\n'
      '    if ON7("472"):                                                                          # 472: the refit\'s first among survivors with no soft break\n'
      '        byr = sorted(alive, key=lambda c: (-c["judge"]["refit_combined"], c["fp"])); clean_r = [c for c in byr if not c["info"]["soft"]]\n'
      '        old_ = pick; pick = clean_r[0] if clean_r else (byr[0] if byr else None)\n'
      '        rk_ = lambda L, c: next((j_ + 1 for j_, x_ in enumerate(L) if c is not None and x_["fp"] == c["fp"]), None)\n'
      '        PICK108[0] = old_; PICK108[1] = dict(v108_pick=old_["fp"] if old_ else None, refit_pick=pick["fp"] if pick else None, v108_pick_rank_under_refit=rk_(clean_r, old_),\n'
      '                                             refit_pick_rank_under_v108=rk_(clean, pick), clean=len(clean_r))\n'
      '        print("472:", PICK108[1])\n'),
    P('pick=pick, pick_352=pick_352,', 'pick=pick, pick_v108=PICK108[0], pick_ranks=PICK108[1], pick_352=pick_352,'),
    # ---- 464: 267 reads song 45's bridge G before its raise (as Q1 A reads 386's moves)
    P('if DIAG450 else n.get("moved386", n["p"])) for n in notes if a2 <= n["on"] < b2}',
      'if (DIAG450 or ON7("464")) else n.get("moved386", n["p"])) for n in notes if a2 <= n["on"] < b2}', 1, ("45",)),
    P('if DIAG450 else n.get("moved386", n["p"])) for n in notes if a0 <= n["on"] < b0}',
      'if (DIAG450 or ON7("464")) else n.get("moved386", n["p"])) for n in notes if a0 <= n["on"] < b0}', 1, ("45",)),
    # ---- 459: verse 2's bars where the syllable counts differ by one or less
    P('keep = [k for k in a if k in c and sa[k] == sc[k]]', 'keep = [k for k in a if k in c and abs(sa[k] - sc[k]) <= (1 if ON7("459") else 0)]'),
    P('    rerun["v124"] = [f_ for f_ in FIX124 if ON(f_)];', '    rerun["v127_part"] = V127; rerun["v127_on"] = sorted(f_ for f_ in P127 if ON7(f_))\n    rerun["v124"] = [f_ for f_ in FIX124 if ON(f_)];'),
]
PART1 = [
    # ---- 434 (amends 228) and 435: the second verse sung again by the first verse's rule
    P('    ns[-1]["p"] = S[-1]["p"]; ns[0]["p"] = S[0]["p"]\n',
      '    ns[-1]["p"] = S[-1]["p"]; ns[0]["p"] = S[0]["p"]\n'
      '    if ON7("434"):                                                                         # 434, 435: verse 1\'s pitch where both strike the same place, the rest drawn\n'
      '        src_at = {m_["on"] - SU: m_["p"] for m_ in S}; mapped = [n_["p"] for n_ in ns]; fx = {0: ns[0]["p"], len(ns) - 1: ns[-1]["p"]}\n'
      '        for j_, n_ in enumerate(ns[1:-1], 1):\n'
      '            t_ = n_["on"] - U\n'
      '            if t_ in src_at:\n'
      '                STATS["435: verse 2 strikes verse 1\'s place"] += 1\n'
      '                if rng.random() < K435: fx[j_] = src_at[t_]; STATS["435: verse 1\'s pitch kept"] += 1\n'
      '        d_ = [n_["dur"] for n_ in ns]; DRAWN398[0] = True                                  # 434: verse 2\'s chord tones from 398\'s knobs, as verse 1\'s\n'
      '        ps_ = walk_notes(rng, ns, None, 1, float(np.median(mapped)), lo, hi, on_all, fixed=fx, shape=[(h_, 0.0) for h_ in mapped]); DRAWN398[0] = False\n'
      '        for n_, x_ in zip(ns, d_): n_["dur"] = x_\n'
      '        if ps_ is None: STATS["434: walk failed, the mapped pitches kept"] += 1; ps_ = mapped\n'
      '        srep = {(m_["on"] - SU) for k_, m_ in enumerate(S) if k_ and m_["p"] == S[k_ - 1]["p"]}\n'
      '        for j_ in range(1, len(ns)):                                                          # 434: no repeat the source line did not sing\n'
      '            if j_ in fx or ps_[j_] != ps_[j_ - 1] or ns[j_]["slur"]: continue\n'
      '            x_ = (ns[j_]["on"] - U - n0) / max(1, n1 - n0) * (s1 - s0) + s0; sj_ = min(srel, key=lambda e: abs(e[0] - x_))[0]\n'
      '            if sj_ in srep: continue\n'
      '            ch_ = M.chord_for(ns[j_], on_all)\n'
      '            op_ = [ps_[j_] + d for d in (1, -1, 2, -2) if lo <= ps_[j_] + d <= hi and (ps_[j_] + d) % 12 in M.SCALE and not tri(ps_[j_] + d, ch_) and (j_ + 1 >= len(ns) or ps_[j_] + d != ps_[j_ + 1])]\n'
      '            if op_: ps_[j_] = max(op_, key=lambda q_: chord_w(q_, ns[j_], ch_)); STATS["434: a repeat the source did not sing, moved"] += 1\n'
      '        for n_, p_ in zip(ns, ps_): n_["p"] = p_\n'),
    P('        if (n["stress"] and n["on"] % BEAT == 0 and n["p"] % 12 not in tones) or tri(n["p"], ch):\n',
      '        if (n["stress"] and n["on"] % BEAT == 0 and n["p"] % 12 not in tones and not ON7("434")) or tri(n["p"], ch):   # 434: the move to a chord tone removed\n'),
    P('PICK108 = [None, None]\n', 'PICK108 = [None, None]\nK435 = 0.75                                                                              # 435: the kept three in four\n'),
]
PARTS = PART0 + PART1

def port(song, patches):
    s = open(f"{SRC}/melody_v124_p{song}.py").read()
    s = s.replace("/home/claude/p52", DST).replace("melody_v124_", "melody_v127_")
    for old, new, cnt, only in patches:
        if only and song not in only: continue
        k = s.count(old)
        if k != cnt: sys.exit(f"song {song}: patch not matched {k} times (want {cnt}): {old[:90]!r}")
        s = s.replace(old, new)
    s = HEADER + s
    open(f"{DST}/melody_v127_p{song}.py", "w").write(s); compile(s, f"melody_v127_p{song}.py", "exec")
    print(song, "ok", len(s.splitlines()), "lines")

if __name__ == "__main__":
    extra = []
    if os.path.exists(f"{os.path.dirname(os.path.abspath(__file__))}/gen_v127_parts23.py"):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import gen_v127_parts23 as G23; extra = G23.PATCHES
    for so in SONGS: port(so, PARTS + extra)
