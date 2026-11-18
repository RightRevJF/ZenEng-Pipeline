"""Luthier v10, stage 2b (Module 27.91; fixes 770, 771), on top of stages 1 and 2a: make a song's v10 engine from its v7 file.

    python3 lib/luthier/gen_l10.py /home/claude/p64        # writes melody_l10_p64.py; run files go to runl10/

770  The floor under a line's start is the least breath (18 twelfths) after the line before, not the breath that line drew (amends
     631, 765). A kept line's breath runs to the next line's first onset, pickup included; used as a floor it shut out the pickups
     that 731 asks for, and before one-bar lines it shut out the line.
771  The first onset by the stress of the first syllable, in the old draw and in 760's rule: before, on and after the bar line at the
     kept shares (stressed 20 / 42 / 38; unstressed 43 / 10 / 47), in place of weights that did not read the stress (1.0, 0.35, 0.5).
772  A line sung again whose first syllable's stress differs from its source's keeps its source's rhythm and changes only the
     pickup (amends 712): a stressed opening drops the source's pickup and a long note is split for each note lost.
773  Where a line cannot fit before a line sung again that was fitted ahead of it, the line is set to its own slot's end and the
     line sung again is drawn again against it (247), before the build is given up."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen_l8, gen_l9
def main(folder):
    folder = folder.rstrip("/"); nn = re.search(r"p(\d+)$", folder).group(1)
    gen_l9.main(folder); s = open(f"{folder}/melody_l9_p{nn}.py").read(); P = gen_l8.patch
    s = P(s, "            tmin = max(-12, last_on + b681_ - U)\n", "            tmin = max(-12, last_on + GAP_MIN - U)                                              # 770: the least breath is the floor, not the breath drawn\n", "770")
    s = P(s, "    if o is None and PREVB[0] is not None and PREVB[0] > GAP_MIN and tmin > -12:", "    if False and o is None and PREVB[0] is not None and PREVB[0] > GAP_MIN and tmin > -12:   # 770 supersedes 765 here", "770b")
    s = P(s, "            alpha[0][(t, 1)] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t) * cbw(t, 0)",
             "            alpha[0][(t, 1)] = (E771[bool(st[0])][0] if t < 0 else (E771[bool(st[0])][1] if t == 0 else E771[bool(st[0])][2])) * A(0, t) * cbw(t, 0)   # 771", "771a")
    s = P(s, "    w0 = [_pw760(P[j], st[0]) * B[0][j] for j in range(m)]\n",
             "    w0 = [_pw760(P[j], st[0]) * B[0][j] * (E771[st[0]][0] if (P[j] % BAR) > 24 else E771[st[0]][1] if P[j] % BAR == 0 else E771[st[0]][2]) for j in range(m)]   # 771\n", "771b")
    s = P(s, "def weighted760(sy, rng, tmin, end):", "E771 = {True: (0.10, 0.42, 0.063), False: (0.215, 0.10, 0.078)}   # 771: a first onset before, on, after the bar line, a candidate place (kept shares 20/42/38 and 43/10/47 over 2, 1 and 6 places)\ndef weighted760(sy, rng, tmin, end):", "771c")
    s = P(s, "def exact712(S, SU, nsy, tmin, end):\n", "def exact712(S, SU, nsy, tmin, end, st0=None):\n", "772a")
    s = P(s, "    if not src or src[0][1]: return None\n    m = sum(1 for _, sl_ in src if not sl_); d = m - nsy\n",
             "    if not src or src[0][1]: return None\n"
             "    if st0 is not None and bool(min(S, key=lambda n_: n_[\"on\"]).get(\"stress\")) != bool(st0):   # 772: the first syllable's stress differs from its source's: only the pickup changes\n"
             "        if st0 and src[0][0] < 0:                                                           # a stressed opening does not take its source's pickup: the pickup goes and a long note is split for each note lost\n"
             "            pk_ = [x_ for x_ in src if x_[0] < 0 and not x_[1]]; rest_ = [x_ for x_ in src if x_[0] >= 0]\n"
             "            if not rest_ or rest_[0][0] != 0 or rest_[0][1]: return None\n"
             "            src = rest_\n"
             "            for _ in pk_:\n"
             "                c_ = [(src[j_ + 1][0] - src[j_][0], -j_, j_) for j_ in range(len(src) - 1)]\n"
             "                if not c_ or max(c_)[0] < 6: return None\n"
             "                g_, _, j_ = max(c_); src.insert(j_ + 1, [src[j_][0] + (g_ // 2 // 3) * 3, False])\n"
             "            STATS[\"772: a line sung again, stressed opening: its source's pickup dropped and a note split\"] += 1\n"
             "    m = sum(1 for _, sl_ in src if not sl_); d = m - nsy\n", "772b")
    s = P(s, "rows712_ = exact712(S, SU, len(sy), tmin, se7_ if last_max is None else min(se7_, last_max))", "rows712_ = exact712(S, SU, len(sy), tmin, se7_ if last_max is None else min(se7_, last_max), st0=sy[0][1])", "772c")
    s = P(s, "ex712_ = exact712(built[(s0, i0)], line_start(s0, i0), len(LINES[sec][i]), tmin508(sec, i), slot_end(sec, i)) if ON22(\"712\") else None", "ex712_ = exact712(built[(s0, i0)], line_start(s0, i0), len(LINES[sec][i]), tmin508(sec, i), slot_end(sec, i), st0=LINES[sec][i][0][1]) if ON22(\"712\") else None", "772d")
    s = P(s, "kl712_ = dict(e=int(src_[0]) if src_[0] < BAR else 0, last=int(src_[-1]))", "kl712_ = dict(e=((0 if (st[0] and src_[0] < 0) else int(src_[0])) if src_[0] < BAR else 0), last=int(src_[-1]))", "772e")
    s = P(s, "                if pf and pf[1]: f0 = (pf[1][0][\"on\"] - line_start(*nxt)) if pf[0] == \"ns\" else pf[1][0]\n                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - (br631(",
             "                if pf and pf[1]: f0 = (pf[1][0][\"on\"] - line_start(*nxt)) if pf[0] == \"ns\" else pf[1][0]\n                NXT773[0] = bool(pf and pf[1] and pf[0] != \"ns\")                                    # 773: the line after is a line sung again, fitted ahead, that may be drawn again (247)\n                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - (br631(", "773a")
    s = P(s, "    if o is None: STATS[\"760: the syllables cannot fit the window on the sixteenth grid\"] += 1; return None",
             "    if o is None and last_max is not None and NXT773[0]:                                                          # 773: the line after gives way: this line is set to its own slot's end and the line after is drawn again\n        o = weighted760(sy, rng, tmin, slot_end(sec, i))\n        if o is not None: STATS[\"773: set past the room a line sung again had asked; that line drawn again\"] += 1\n    if o is None: STATS[\"760: the syllables cannot fit the window on the sixteenth grid\"] += 1; return None", "773b")
    s = P(s, "E771 = {True:", "NXT773 = [False]\nE771 = {True:", "773c")
    s = s.replace('if k_[:4] in ("760:", "761:", "764:", "765:", "730:"', 'if k_[:4] in ("760:", "761:", "764:", "765:", "772:", "773:", "730:"')
    s = s.replace(f"{folder}/runl9/", f"{folder}/runl10/").replace(f"melody_l9_p{nn}_", f"melody_l10_p{nn}_").replace(f"python3 melody_l9_p{nn}.py", f"python3 melody_l10_p{nn}.py")
    s = s.replace('"""Luthier v9 stage 2a (Module 27.90; by lib/luthier/gen_l9.py: 760, 761)', '"""Luthier v10 stage 2b (Module 27.91; by lib/luthier/gen_l10.py: 770 to 773) on Luthier v9 stage 2a (Module 27.90; by lib/luthier/gen_l9.py: 760, 761)', 1)
    os.makedirs(f"{folder}/runl10", exist_ok=True); open(f"{folder}/melody_l10_p{nn}.py", "w").write(s); print("wrote", f"{folder}/melody_l10_p{nn}.py", "(run files to runl10/)")
if __name__ == "__main__": main(sys.argv[1])
