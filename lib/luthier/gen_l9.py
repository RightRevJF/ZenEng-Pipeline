"""Luthier v9, stage 2a (Module 27.90; fixes 760 to 762), on top of stage 1 (750 to 752): make a song's v9 engine from its v7 file.

    python3 lib/luthier/gen_l9.py /home/claude/p64        # reads melody_l7_p64.py, writes melody_l9_p64.py; run files go to runl9/

760  A line the rhythm draw cannot place is no longer a death. The draw is tried once more without its borrowed rhythm (a partner's,
     a returning unit's or its source's bars); if that fails too, the line is set by weighted rules inside the same window (its
     earliest start, its slot's end, the next line's room): each syllable's place is drawn with the kept share of stressed and of
     unstressed syllables at that place in the bar (studies/words, 199 Billboard songs), each gap with the kept mean palette's share
     (606), no gap of three beats or more. A build dies for want of a placement only when the syllables cannot fit the window on
     the sixteenth grid.
761  No drawn line of eight syllables or fewer keeps a gap of three beats or more between two of its onsets (kept lines: none do;
     749.31): such a line is drawn again, and set by 760's rule if it comes out so three times.
764  A line leaves the next line of its section room: its last onset comes no later than lets the next line sing its syllables in
     eighths before its own slot's end, after the breath (18 twelfths), unless that leaves this line less than eighths for itself.
765  The breath before a line (631's drawn breath) gives way, down to the least breath of 18 twelfths, before the line is given up
     (the session's 741).
762  Printed: how many lines each build set by 760's rule, by section; the report's test is deaths for want of a placement under
     one build in ten."""
import sys, os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen_l8
WRAP = '''
# ---- Luthier v9, stage 2a: 760 (a line the draw cannot place is set by weighted rules), 761 (no gap of three beats inside a short line)
P760S = {0: 0.191, 24: 0.156, 12: 0.1035, 36: 0.1035}; P760U = {0: 0.042, 24: 0.048, 12: 0.125, 36: 0.125}      # kept share at a place in the bar: stressed, unstressed
G760 = {3: 0.118, 6: 0.46, 9: 0.033, 12: 0.178, 18: 0.065, 24: 0.04}                                              # the kept mean palette (606)
def _pw760(t, st):
    m = t % BAR
    if m in P760S: return (P760S if st else P760U)[m]
    if m % 6 == 0: return 0.090 if st else 0.129                                                                  # an off-beat eighth
    return 0.011 if st else 0.018                                                                                 # a sixteenth
def weighted760(sy, rng, tmin, end):
    """760: n onsets on the sixteenth grid in [tmin, end], drawn in proportion to the product of place and gap weights; None if they cannot fit."""
    n = len(sy); t0 = int(-(-tmin // 3) * 3); P = list(range(t0, int(end) + 1, 3))
    if len(P) < n: return None
    st = [bool(s_[1]) for s_ in sy]; m = len(P); B = [[0.0] * m for _ in range(n)]
    for j in range(m): B[n - 1][j] = 1.0
    for k in range(n - 2, -1, -1):
        for j in range(m):
            tot = 0.0
            for j2 in range(j + 1, m):
                g = P[j2] - P[j]
                if g >= 36: break
                tot += G760.get(g, 0.01) * _pw760(P[j2], st[k + 1]) * B[k + 1][j2]
            B[k][j] = tot
    w0 = [_pw760(P[j], st[0]) * B[0][j] for j in range(m)]
    if sum(w0) <= 0: return None
    j = rng.choices(range(m), w0)[0]; out = [P[j]]
    for k in range(n - 1):
        c = [(j2, G760.get(P[j2] - P[j], 0.01) * _pw760(P[j2], st[k + 1]) * B[k + 1][j2]) for j2 in range(j + 1, m) if P[j2] - P[j] < 36]
        c = [x for x in c if x[1] > 0]
        if not c: return None
        j = rng.choices([x[0] for x in c], [x[1] for x in c])[0]; out.append(P[j])
    return out
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None, i=None, copybars=None, pair=False, stressbars=None, fallback=None, allbars=False, span_to=None, again712=None):
    kw = dict(fix=fix, entry=entry, prior=prior, i=i, copybars=copybars, pair=pair, stressbars=stressbars, fallback=fallback, allbars=allbars, span_to=span_to, again712=again712)
    if fix or i is None: return _lr760(sy, rng, tmin, sec, last_max, **kw)
    if i + 1 < len(LINES[sec]):                                                                                    # 764: leave the next line room for its syllables in eighths and its breath
        cap_ = slot_len(sec, i) * BAR + slot_end(sec, i + 1) - 6 * (len(LINES[sec][i + 1]) - 1) - GAP_MIN
        if cap_ < slot_end(sec, i) and (last_max is None or cap_ < last_max):
            last_max = max(cap_, tmin + 6 * (len(sy) - 1)); STATS["764: a line's last onset held back for the line after it"] += 1
    free = dict(kw, copybars=None, pair=False, stressbars=None, allbars=False, again712=None); o = None
    for tr_ in range(3):
        o = _lr760(sy, rng, tmin, sec, last_max, **kw)
        if o is None and tr_ == 0 and (copybars or again712 is not None):
            o = _lr760(sy, rng, tmin, sec, last_max, **free)
            if o is not None: STATS["760: placed without its borrowed rhythm"] += 1
        if o is None: break
        if len(sy) <= 8 and any(b_ - a_ >= 36 for a_, b_ in zip(o, o[1:])):                                        # 761
            STATS["761: a gap of three beats inside a short line, drawn again"] += 1; o = None; continue
        return o
    end = slot_end(sec, i) if last_max is None else min(slot_end(sec, i), last_max)
    o = weighted760(sy, rng, tmin, end)
    if o is None and PREVB[0] is not None and PREVB[0] > GAP_MIN and tmin > -12:                                     # 765: the breath before the line gives way, down to 18 twelfths
        t765_ = max(-12, tmin - (PREVB[0] - GAP_MIN)); o = _lr760(sy, rng, t765_, sec, last_max, **free)
        if o is not None and len(sy) <= 8 and any(b_ - a_ >= 36 for a_, b_ in zip(o, o[1:])): o = None
        if o is not None: STATS["765: placed with the breath before it shortened"] += 1; return o
        o = weighted760(sy, rng, t765_, end)
        if o is not None: STATS["765: set by the weighted rule with the breath before it shortened"] += 1
    if o is None: STATS["760: the syllables cannot fit the window on the sixteenth grid"] += 1; return None
    M682[0] = None; NOMEL[0] = False; W680[0] = False; MET600[(sec, i)] = False
    STATS["760: set by the weighted rule"] += 1; STATS["760: set by the weighted rule, " + sec.rstrip("0123456789 ")] += 1
    return o
'''
def main(folder):
    folder = folder.rstrip("/"); nn = re.search(r"p(\d+)$", folder).group(1)
    gen_l8.main(folder); s = open(f"{folder}/melody_l8_p{nn}.py").read()
    s = gen_l8.patch(s, "\ndef line_rhythm(", "\ndef _lr760(", "760a")
    i = s.index("\ndef melismas("); s = s[:i] + WRAP + s[i:]
    s = gen_l8.patch(s, 'if k_[:4] in ("730:", "731:", "732:", "733:", "734:", "735:", "736:", "717:", "651:", "712:", "714:", "680:", "682:", "313:", "323:")}', 'if k_[:4] in ("760:", "761:", "764:", "765:", "730:", "731:", "732:", "733:", "734:", "735:", "736:", "717:", "651:", "712:", "714:", "680:", "682:", "313:", "323:")}', "762")
    s = s.replace(f"{folder}/runl8/", f"{folder}/runl9/").replace(f"melody_l8_p{nn}_", f"melody_l9_p{nn}_").replace(f"python3 melody_l8_p{nn}.py", f"python3 melody_l9_p{nn}.py")
    s = s.replace('"""Luthier v8 stage 1 (Module 27.89; by lib/luthier/gen_l8.py', '"""Luthier v9 stage 2a (Module 27.90; by lib/luthier/gen_l9.py: 760, 761) on Luthier v8 stage 1 (Module 27.89; by lib/luthier/gen_l8.py', 1)
    os.makedirs(f"{folder}/runl9", exist_ok=True); open(f"{folder}/melody_l9_p{nn}.py", "w").write(s); print("wrote", f"{folder}/melody_l9_p{nn}.py", "(run files to runl9/)")
if __name__ == "__main__": main(sys.argv[1])
