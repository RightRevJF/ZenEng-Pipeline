"""gen_v137s_p58.py: the side run for finding 610 (not of record). Writes melody_v137s_p58.py from melody_v137_p58.py: for lines drawn under
600, the last onset may run to the slot's end less the breath (212's GAP_MIN, 18 twelfths) in place of beat 3 of the slot's last bar
(slot_end), and still no later than the next line's known entry less the breath (last_max); 406's landing weights, which stop at slot_end,
are not applied while the span is held. Everything else is v137's."""
SRC = "/home/claude/p58/melody_v137_p58.py"; DST = "/home/claude/p58/melody_v137s_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)
P('''"""ZenEng v137 (Module 27.81; by gen_v137_p58.py''', '''"""SIDE RUN for 610 (by gen_v137s_p58.py; not of record) -- ZenEng v137 (Module 27.81; by gen_v137_p58.py''')
P('''        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
''', '''        SPAN600[0] = (S600_, len(sy)); STATS[f"600: span drawn ({c600_}, {tb600_})"] += 1
        se = slot_len(sec, i) * BAR - GAP_MIN; end = se if last_max is None else min(se, last_max)   # 610 (side run): the slot's end less the breath
        STATS["610: line may end at the slot's end less the breath"] += 1
''')
P('''                t0_ = rng.choice(f0s_); F600C[0] = (t0_, t0_ + T600_); tgt = None''', '''                t0_ = rng.choice(f0s_); F600C[0] = (t0_, t0_ + T600_); tgt = None; LW406[0] = None   # 610 (side run): 406's weights stop at slot_end''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_v137_p58.py {N} {MODE}"''', '''cmd=f"PYTHONHASHSEED=0 python3 melody_v137s_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/run137/melody_v137_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/run137s/melody_v137s_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s); print("wrote", DST)
