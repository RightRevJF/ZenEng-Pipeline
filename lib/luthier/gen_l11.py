"""Luthier v11, stage 2c (Module 27.92; fixes 780, 783), on top of stages 1, 2a and 2b: make a song's v11 engine from its v7 file.

    python3 lib/luthier/gen_l11.py /home/claude/p65        # writes melody_l11_p65.py; run files go to runl11/

780  The join before a line fitted ahead (212), read as 770 reads every join (the session's 749.42, 749.43): the room a line must
     leave is the least breath (18 twelfths), not a breath drawn afresh; where the line after is a line sung again fitted ahead, it
     gives way and is drawn again against this line (247) and the build does not die; and a copied line keeps the join its source
     kept (its join to the line after is not read again when it is no shorter than its source's join to the line after it);
     and where both lines are fixed (a design or a copy before a copy), the join may be as short as a beat, 12 twelfths, the kept
     lines' 5th percentile (8% of kept joins are under 18).
783  The run stores each note's moved386 (the pitch 386 leaves on a note it moves) as an eighth field of the record's notes, so a
     stored build re-evaluates as it ran (the session's 749.35). Readers take survivors as builds with no cause."""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import gen_l8, gen_l10
def main(folder):
    folder = folder.rstrip("/"); nn = re.search(r"p(\d+)$", folder).group(1)
    gen_l10.main(folder); s = open(f"{folder}/melody_l10_p{nn}.py").read(); P = gen_l8.patch
    s = P(s, '- (br631(rng, sec, i) if (ON19("631") and how(sec, i)[0] in ("fresh", "again")) else GAP_MIN)   # 631',
             '- ((br631(rng, sec, i), GAP_MIN)[1] if (ON19("631") and how(sec, i)[0] in ("fresh", "again")) else GAP_MIN)   # 631; 780: the breath is drawn and read, the room asked is the least breath', "780a")
    s = P(s, '- (br631(rng, sec, i) if (ON19("631") and h in ("fresh", "again")) else GAP_MIN)   # 631',
             '- ((br631(rng, sec, i), GAP_MIN)[1] if (ON19("631") and h in ("fresh", "again")) else GAP_MIN)   # 631; 780', "780b")
    s = P(s, '            if last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return _fail("join: no held end and breath before the copy (212)")',
             '            J780[0] = None\n'
             '            if last_max is not None and ns[-1]["on"] - U > last_max and NXT773[0]: STATS["780: the line sung again after this line gives way and is drawn again"] += 1   # 780\n'
             '            elif last_max is not None and ns[-1]["on"] - U > last_max and nxt is not None and h in CK780 and (s0, i0) in built and (s0, i0 + 1) in built and (U + last_max + GAP_MIN - ns[-1]["on"]) >= (built[(s0, i0 + 1)][0]["on"] - built[(s0, i0)][-1]["on"]) > 0: STATS["780: a copied line keeps the join its source kept"] += 1; J780[0] = built[(s0, i0 + 1)][0]["on"] - built[(s0, i0)][-1]["on"]\n'
             '            elif last_max is not None and ns[-1]["on"] - U > last_max and h not in ("fresh", "again") and (U + last_max + GAP_MIN - ns[-1]["on"]) >= 12: STATS["780: two fixed lines joined at a beat or more (the kept 5th percentile)"] += 1; J780[0] = 12\n'
             '            elif last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return _fail("join: no held end and breath before the copy (212)")', "780c")
    s = P(s, "NXT773 = [False]\n", 'NXT773 = [False]; CK780 = ("copy", "return", "plan", "tail"); J780 = [None]\n', "780d")
    s = P(s, '            if ns[0]["on"] - last_on < (min(GAP_MIN, PREVB[0]) if (ON19("631") and PREVB[0] is not None) else GAP_MIN): globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")',
             '            if ns[0]["on"] - last_on < min((min(GAP_MIN, PREVB[0]) if (ON19("631") and PREVB[0] is not None) else GAP_MIN), (J780[0] if J780[0] is not None else 999)): globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")   # 780: the join the line before was allowed', "780e")
    s = P(s, 'notes=[(n["on"], n["dur"], n["p"], n["sec"], n["line"], n.get("stress"), n.get("syl")) for n in c["notes"]],',
             'notes=[(n["on"], n["dur"], n["p"], n["sec"], n["line"], n.get("stress"), n.get("syl"), n.get("moved386")) for n in c["notes"]],   # 783', "783")
    s = s.replace('"772:", "773:", "730:"', '"772:", "773:", "780:", "730:"')
    s = s.replace(f"{folder}/runl10/", f"{folder}/runl11/").replace(f"melody_l10_p{nn}_", f"melody_l11_p{nn}_").replace(f"python3 melody_l10_p{nn}.py", f"python3 melody_l11_p{nn}.py")
    s = s.replace('"""Luthier v10 stage 2b (Module 27.91;', '"""Luthier v11 stage 2c (Module 27.92; by lib/luthier/gen_l11.py: 780, 783) on Luthier v10 stage 2b (Module 27.91;', 1)
    os.makedirs(f"{folder}/runl11", exist_ok=True); open(f"{folder}/melody_l11_p{nn}.py", "w").write(s); print("wrote", f"{folder}/melody_l11_p{nn}.py", "(run files to runl11/)")
if __name__ == "__main__": main(sys.argv[1])
