"""gen_v134.py: writes melody_v134_p57.py (song 47 under ZenEng v134: its last run, closing it, 571) from melody_v133_p57.py, with
v134's generic patches: 566 (a return of the line before it is fitted with the breath after its source's last onset as its earliest
entry; failing a fit, the source is drawn again with its last onset an eighth earlier for each syllable the return adds) and 569's
reading (the align deaths printed by plan; the run-length draws of 558 counted, so the misses read as a share). Every patch replaces
whole statements and is asserted to match exactly once."""
SRC = "/home/claude/p57/melody_v133_p57.py"; DST = "/home/claude/p57/melody_v134_p57.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)

P('''"""ZenEng v133 (Module 27.77; by gen_v133.py''', '''"""ZenEng v134 (Module 27.78; by gen_v134.py from melody_v133_p57.py: 566, 569's reading) -- ZenEng v133 (Module 27.77; by gen_v133.py''')
P('''def ON13(f_): return P133.get(f_, 0) <= V133 and f_ not in OFF11
''', '''def ON13(f_): return P133.get(f_, 0) <= V133 and f_ not in OFF11
V134 = int(_os11.environ.get("ZE_PART134", "1"))
P134 = {f_: 1 for f_ in ("566", "569")}
def ON14(f_): return P134.get(f_, 0) <= V134 and f_ not in OFF11
''')
# ---- 566 (a): the return of the line before fitted after the breath ----
P('''                ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, tmin508(sec, i), lo_, hi_, notes_on_all, endok=endok_of(sec, i))''',
  '''                tm566_ = tmin508(sec, i)
                if ON14("566") and h in ("return", "plan") and i > 0 and (s0, i0) == (sec, i - 1):   # 566: the breath after its source's last onset, its earliest entry
                    tm566_ = max(tm566_, last_on + GAP_MIN - U); STATS["566: a return of the line before fitted after the breath"] += 1
                ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, tm566_, lo_, hi_, notes_on_all, endok=endok_of(sec, i))''')
# ---- 566 (b): failing a fit, the source drawn again an eighth earlier for each syllable the return adds ----
P('''                RET560[0] = slot_len(sec, i) * BAR if (ON13("560") and nxt and hn_[0] in ("plan", "return") and (hn_[1], hn_[2]) == (sec, i)) else None   # 560''',
  '''                RET560[0] = slot_len(sec, i) * BAR if (ON13("560") and nxt and hn_[0] in ("plan", "return") and (hn_[1], hn_[2]) == (sec, i)) else None   # 560
                if RET560[0] is not None and att566_ == 1: RET560[0] -= 6 * max(0, len(LINES[nxt[0]][nxt[1]]) - len(sy))   # 566: an eighth earlier a syllable added''')
a0 = s.index('''            else:
                pj = pair_of(sec, i); partner = (built[(sec, pj)], line_start(sec, pj), len(LINES[sec][pj])) if pj is not None and (sec, pj) in built else None''')
a1 = s.index('''            if ns[0]["on"] - last_on < GAP_MIN: globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")''')
body = s[a0 + len("            else:\n"):a1]
assert all(l.startswith("                ") or not l.strip() for l in body.splitlines())
body = "\n".join(("    " + l) if l.strip() else l for l in body.splitlines()) + "\n"
trial = '''                    if att566_ == 0 and RET560_ON_[0]:                                       # 566: the return tried now, after the breath; no fit, the source drawn again
                        trng_ = random.Random(rng.random()); U2_ = line_start(*nxt); ALIGN_END[0] = slot_end(*nxt)
                        Sx_ = [dict(n_, sec=sec, line=f"{sec}:{i}") for n_ in ns]
                        ns2_, kd2_ = vary_return(trng_, Sx_, LINES[sec][i], LINES[nxt[0]][nxt[1]], U, U2_, max(tmin508(*nxt), ns[-1]["on"] + GAP_MIN - U2_),
                                                 REGS[KIND[nxt[0]]][2], REGS[KIND[nxt[0]]][1], notes_on_all | {x_["on"] for x_ in ns}, endok=endok_of(*nxt))
                        if ns2_ is None: STATS["566: no fit after the breath; the source drawn again an eighth earlier for each syllable added"] += 1; continue
                    break
'''
body = body.replace('''                    RET560[0] = slot_len(sec, i) * BAR if''', '''                    RET560_ON_[0] = bool(ON14("566") and nxt and hn_[0] in ("plan", "return") and (hn_[1], hn_[2]) == (sec, i))
                    RET560[0] = slot_len(sec, i) * BAR if''', 1)
s = s[:a0] + "            else:\n                RET560_ON_ = [False]\n                for att566_ in range(2 if ON14(\"566\") else 1):\n" + body + trial + s[a1:]
# ---- 569's reading, and 558's draws counted ----
P('''        if err: deaths[err] += 1; rec["where"] = str(globals().get("WHERE")); continue''',
  '''        if err: deaths[err] += 1; rec["where"] = str(globals().get("WHERE")); rec["plans"] = {k_: ("".join(v_) if isinstance(v_, list) else v_) for k_, v_ in c["meta"].get("plans", {}).items()}; continue   # 569''')
P('''                if R558 and g_ is not None and L558_[0] is not None:                             # 558: the run goes on to its drawn length, then breaks''',
  '''                if R558 and g_ is not None and L558_[0] is not None: STATS["558: run-length draws"] += 1
                if R558 and g_ is not None and L558_[0] is not None:                             # 558: the run goes on to its drawn length, then breaks''')
P('''    rerun["v133_part"] = V133;''', '''    rerun["v134_part"] = V134; rerun["v134_on"] = sorted(f_ for f_ in P134 if ON14(f_))
    rerun["v134_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("558:", "560:", "566:")}
    rerun["v133_part"] = V133;''')
P('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v133_p57.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v134_p57.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
P('''open(f"/home/claude/p57/run133/melody_v133_p57_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p57/run134/melody_v134_p57_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
