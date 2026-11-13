"""gen_v132.py: writes melody_v132_p57.py (song 47, The Singer Doesn't Stop, run again under ZenEng v132 as a regression) from
melody_v131_p57.py, with v132's generic patches: 548 (the judge of record, 39 measures, zeneng_v132_judge.json, for content scores and the
pick; the floor stays on the v108 judge), 551 (a line of more than two syllables a beat draws its gaps from the kept table for its band
directly; a run of equal gaps capped at the band's kept 95th percentile), 552 (501 read on the rate the line's span and slot allow where
its syllables cannot fit the kept rate, counted, not redrawn), 553 (the calibration runs to ten rounds while 503's knob is still stepping),
555 (a copy's source drawn with the designed line's entry as its next line's when a designed line follows the copy), 556 (class 0 drawn
only where the next line can take a pickup), 528 (the classes from the file's table by slot bars and the line's notes, as 525 already
reads them), 529 (524's three-bar rule withdrawn; 527 by syllables), 550 (527 read by the section, printed). Every patch replaces whole
statements and is asserted to match exactly once. The song's own parts are unchanged from v131 (same seed)."""
import sys
SONG = sys.argv[1] if len(sys.argv) > 1 else "p57"
SRC = "/home/claude/p57/melody_v131_p57.py"; DST = "/home/claude/p57/melody_v132_p57.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:140]); s = s.replace(a, b)

# ---- the header and the v132 flags ----
P('''"""ZenEng v131 (Module 27.75) -- song 47''', '''"""ZenEng v132 (Module 27.76; by gen_v132.py from melody_v131_p57.py: 548, 550-553, 555, 556, 528, 529) -- formerly ZenEng v131 (Module 27.75) -- song 47''')
P('''ON11 = ON10
''', '''ON11 = ON10
V132 = int(_os11.environ.get("ZE_PART132", "1"))
P132 = {f_: 1 for f_ in ("548", "550", "551", "552", "553", "555", "556", "528", "529")}
def ON12(f_): return P132.get(f_, 0) <= V132 and f_ not in OFF11
if ON12("529"): OFF11.add("524")                                                       # 529: 524's three-bar rule withdrawn
''')
# ---- 548: the judge of record, 39 measures ----
P('''RJ = json.load(open(f"{H118}/tables/" + ("zeneng_v129_judge.json" if ON9("519") else "zeneng_v128_judge.json" if ON8("476") else "zeneng_v126_judge.json")))["content_judge"]   # 519                 # 470''',
  '''RJ = (json.load(open("/home/claude/p57/tables/zeneng_v132_judge.json")) if ON12("548") else
      json.load(open(f"{H118}/tables/" + ("zeneng_v129_judge.json" if ON9("519") else "zeneng_v128_judge.json" if ON8("476") else "zeneng_v126_judge.json")))["content_judge"])   # 548: 39 measures; 519; 470''')
P('''    """470: intercept + sum of weight x (value - mean) / sd over the 37 measures; a measure the window lacks takes the kept median."""''',
  '''    """470 (548): intercept + sum of weight x (value - mean) / sd over the judge's measures (39 at v132); a measure the window lacks takes the kept median."""''')
# ---- 551: dense lines drawn from the kept table for their band; equal-gap runs capped ----
P('''    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)
    RTS = KRT[SEC_BAND[sec]] if "372" not in OFF else M.RT; SH16_NOW[0] = float(KSH[SEC_BAND[sec]][0]) if "372" not in OFF else SIXTEENTH   # 372''',
  '''    se = slot_end(sec, i); end = se if last_max is None else min(se, last_max)
    RTS = KRT[SEC_BAND[sec]] if "372" not in OFF else M.RT; SH16_NOW[0] = float(KSH[SEC_BAND[sec]][0]) if "372" not in OFF else SIXTEENTH   # 372
    D551 = False; CAP551_ = None
    if ON12("551") and i is not None and not fix and len(sy) >= 3:                       # 551: the line's syllables a beat over the kept span its notes sing
        r551_ = rate551(len(sy), sec, i, span_to)
        if r551_ > 2.0:
            D551 = True; b551_ = band504(len(sy), sec, i); RTS = KRT[b551_]; CAP551_ = CAP551.get(b551_)
            STATS[f"551: dense line drawn from the kept table ({b551_})"] += 1''')
P('''        return (w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (LK["offb"] if t % 12 == 6 else 1.0)   # 346: the off-beat eighth
                * (LK["on16"] if t % 6 == 3 and "348" not in OFF else 1.0))                       # 355: onsets on a sixteenth aimed at the kept 9.4%''',
  '''        if D551: return w                                                                   # 551: the stress on the beat, no aimed weights
        return (w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (LK["offb"] if t % 12 == 6 else 1.0)   # 346: the off-beat eighth
                * (LK["on16"] if t % 6 == 3 and "348" not in OFF else 1.0))                       # 355: onsets on a sixteenth aimed at the kept 9.4%''')
P('''    may_run = [runs_ok or "366" in OFF or rng.random() < (RUNR[SEC_BAND[sec]] if ON("389") else LK["run"])]                          # 366: a line may run sixteenths, drawn at a rate''',
  '''    may_run = [D551 or runs_ok or "366" in OFF or rng.random() < (RUNR[SEC_BAND[sec]] if ON("389") else LK["run"])]                          # 366: a line may run sixteenths, drawn at a rate; 551: the kept table decides''')
P('''        w = RTS[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)                               # 372: the kept table for the section's band''',
  '''        if D551: return RTS[tp % BAR][d] * H(k - 1, d)                                        # 551: the kept table for the line's band, directly
        w = RTS[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)                               # 372: the kept table for the section's band''')
P('''                def e452(d_):                                                                    # 452: a gap equal to the one after it; a run past the kept figure
                    if not ON7("452") or g_ is None or d_ != g_: return 1.0''',
  '''                def e452(d_):                                                                    # 452: a gap equal to the one after it; a run past the kept figure
                    if D551: return 0.0 if (CAP551_ is not None and g_ is not None and d_ == g_ and rl_[0] + 1 > CAP551_) else 1.0   # 551: no weights; the run capped
                    if not ON7("452") or g_ is None or d_ != g_: return 1.0''')
P('''                r490_ = R490.get(SEC_BAND[sec], 1.0) if (ON8("490") and t % 6 == 3 and g_ == 3) else 1.0   # 490: t on a sixteenth with a sixteenth after it''',
  '''                r490_ = R490.get(SEC_BAND[sec], 1.0) if (ON8("490") and t % 6 == 3 and g_ == 3 and not D551) else 1.0   # 490: t on a sixteenth with a sixteenth after it (551: not on a dense line)''')
P('''        if ON("405") and i is not None and CUR405[0] is not None:                         # 405: a line that could be placed without runs''',
  '''        if D551:
            g551_ = [b_ - a_ for a_, b_ in zip(ons, ons[1:])]; rr_, mx_ = 1, 1
            for a_, b_ in zip(g551_, g551_[1:]): rr_ = rr_ + 1 if a_ == b_ else 1; mx_ = max(mx_, rr_)
            STATS["551: dense lines placed"] += 1; STATS["551: dense lines, longest equal-gap run (sum)"] += mx_
        if ON("405") and i is not None and CUR405[0] is not None:                         # 405: a line that could be placed without runs''')
# ---- 552: 501 read on the rate the line's span and slot allow ----
P('''            q_ = next(x_ for k_, x_ in OB501 if n <= k_); ob_ = (n - 1) / max(0.25, (ons[-1] - ons[0]) / BEAT)
            lo501, hi501 = (q_[0], q_[4]) if ON10("531") else (q_[1], q_[3])                  # 531: the kept 5th-95th''',
  '''            q_ = next(x_ for k_, x_ in OB501 if n <= k_); ob_ = (n - 1) / max(0.25, (ons[-1] - ons[0]) / BEAT)
            lo501, hi501 = (q_[0], q_[4]) if ON10("531") else (q_[1], q_[3])                  # 531: the kept 5th-95th
            if ON12("552"):                                                                   # 552: the slowest rate the drawn span and the slot allow this line
                e552_ = min(end, (SPAN_E[0] - 3) if SPAN_E[0] is not None else end)
                slow_ = (n - 1) / max(0.25, (e552_ - ons[0]) / BEAT)
                if slow_ > hi501: hi501 = max(hi501, ob_); STATS["552: read on the rate its span and slot allow (the kept rate cannot be met)"] += 1''')
# ---- 553: the calibration runs to ten rounds while 503's knob is still stepping ----
P('''    for rd in range(rounds):
        if rd >= 3 and not full_prev:                                                     # 357: past three rounds only while a knob still moves at full step
            CAL_ROUNDS[0] = rd; break''',
  '''    for rd in range(rounds):
        st553_ = ON12("553") and STEP553[0]
        if rd >= 3 and not full_prev and not st553_:                                       # 357: past three rounds only while a knob still moves at full step (553: or 503's still steps)
            CAL_ROUNDS[0] = rd; break
        if rd >= 6 and not st553_:                                                        # 553: past six rounds only while 503's knob is still stepping, to ten
            CAL_ROUNDS[0] = rd; break
        if rd >= 6: CAL553.append(rd + 1)''')
P('''                    full_ = (0.6 if sg_ > 0 else 1.6); f_ = 1.0 if sg_ == 0 else (full_ if sg_ == SG541[0] else full_ ** 0.5); SG541[0] = sg_''',
  '''                    full_ = (0.6 if sg_ > 0 else 1.6); f_ = 1.0 if sg_ == 0 else (full_ if sg_ == SG541[0] else full_ ** 0.5); SG541[0] = sg_
                    STEP553[0] = sg_ != 0                                                      # 553: the gap over two points, the knob still stepping''')
P('''    cal_log = calibrate(random.Random(SEED + 1))''', '''    cal_log = calibrate(random.Random(SEED + 1), rounds=10 if ON12("553") else 6)''')
# ---- 555: a copy's source fitted to the designed line after the copy ----
P('''    if ON("390"):                                                                          # 390: a unit the plan already returns is not drawn again''',
  '''    COP555 = collections.defaultdict(list)                                                 # 555: the copies of each line, and what follows each copy
    for s5_ in SUNG:
        for j5_ in range(len(LINES[s5_])):
            h5_, a5_, b5_ = how(s5_, j5_)
            if h5_ == "copy": COP555[(a5_, b5_)].append((s5_, j5_))
    def next_of(s5_, j5_):
        return (s5_, j5_ + 1) if j5_ + 1 < len(LINES[s5_]) else ((SUNG[SUNG.index(s5_) + 1], 0) if SUNG.index(s5_) + 1 < len(SUNG) else None)
    def lm555(sec, i):
        """555: where a copy of this line is followed by a designed line, the latest last onset that leaves the copy its breath before it."""
        if not ON12("555"): return None
        out = []
        for c5_ in COP555.get((sec, i), []):
            n5_ = next_of(*c5_)
            if n5_ is None or how(*n5_)[0] not in ("figure", "chant"): continue
            pf5_ = prefit(*n5_)
            if not pf5_ or pf5_[0] != "ns": continue
            out.append(pf5_[1][0]["on"] - line_start(*c5_) - GAP_MIN)
        return min(out) if out else None
    if ON("390"):                                                                          # 390: a unit the plan already returns is not drawn again''')
P('''            h, s0, i0 = how(sec, i)
            SPAN_TO[0] = (line_start(*nxt) - U + (f0 if f0 is not None else 0)) if (nxt and nxt[0] == sec and "378" not in OFF) else None   # 378''',
  '''            h, s0, i0 = how(sec, i)
            if h not in ("copy", "return", "plan", "tail", "figure", "chant"):
                lm5_ = lm555(sec, i)
                if lm5_ is not None and (last_max is None or lm5_ < last_max): last_max = lm5_; STATS["555: a copy's source fitted to the designed line after the copy"] += 1
            SPAN_TO[0] = (line_start(*nxt) - U + (f0 if f0 is not None else 0)) if (nxt and nxt[0] == sec and "378" not in OFF) else None   # 378''')
# ---- 556: class 0 only where the next line can take a pickup ----
P('''    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]), at=(sec, i))''',
  '''    C465[0] = dict(nb=nb_, f0=f0, nxt=tuple(nxt), pk=(f0 is None and not LINES[nxt[0]][nxt[1]][0][1]), at=(sec, i),
                   reach0=((f0 is None and not LINES[nxt[0]][nxt[1]][0][1]) or (f0 is not None and f0 < 0)))   # 556: a fresh line on a weak syllable, or a fixed entry before its downbeat''')
P('''    for k_, lb_, rq_ in opts:
        a_ = -10 ** 6 if k_ == 3 else lb_ * BAR; b_ = (lb_ + 1) * BAR - 1''',
  '''    if ON12("556") and not c_["reach0"] and any(x_[0] == 0 for x_ in opts):
        opts = [x_ for x_ in opts if x_[0] != 0]; STATS["556: class 0 not drawn (the next line cannot take a pickup)"] += 1
    elif ON12("556"): STATS["556: class 0 reachable (the next line can take a pickup)"] += 1
    for k_, lb_, rq_ in opts:
        a_ = -10 ** 6 if k_ == 3 else lb_ * BAR; b_ = (lb_ + 1) * BAR - 1''')
P('''G542 = [0, 0]; CTB541 = [[], []]; SG541 = [0]''', '''G542 = [0, 0]; CTB541 = [[], []]; SG541 = [0]; STEP553 = [False]; CAL553 = []
def rate551(n_, sec, i, span_to):
    """551: syllables a beat over the kept span a line of n notes sings in its slot (the kept middle share of the time to the next line)."""
    sp_ = span_mid(n_); to_ = span_to if span_to else slot_len(sec, i) * BAR
    return (n_ - 1) / max(0.25, (0.5 * (sp_[0] + sp_[1]) * to_) / BEAT)
CAP551 = {}
try: CAP551 = {k_: float(v_) for k_, v_ in json.load(open("/home/claude/p57/tables/zeneng_v132_cap551.json"))["kept 95th percentile of the longest equal-gap run, by band"].items()}
except FileNotFoundError: pass                                                           # 551: the cap needs the band's kept 95th (asked for)''')
# ---- 550 (and 529): 527 read by the section ----
P('''FLAG527 = [x for x in ROOM527 if x[4] < 0.10]                                               # 527: a slot under a tenth of kept lines of its syllables (shown at intake)''',
  '''FLAG527 = [x for x in ROOM527 if x[4] < 0.10]                                               # 527: a slot under a tenth of kept lines of its syllables (shown at intake)
def med550(n_):
    """550: the kept median slot in bars for a line of n syllables (Table ER)."""
    sh_ = k527(n_)["shares"]; c_ = 0.0
    for b_, x_ in enumerate(sh_):
        c_ += x_
        if c_ >= 0.5: return b_ + 1
    return 5
KEPT550 = round(sum(K527[k_]["lines"] * sum(K527[k_]["shares"][:med550(int(k_.split()[0])) - 1]) for k_ in K527) / sum(K527[k_]["lines"] for k_ in K527), 3)   # kept lines under their median slot
SEC550 = {s_: round(float(np.mean([slot_len(s_, i_) < med550(len(LINES[s_][i_])) for i_ in range(len(LINES[s_]))])), 3) for s_ in SUNG}''')
# ---- the run ----
P('''        if err: deaths[err] += 1; continue''', '''        if err: deaths[err] += 1; rec["where"] = str(globals().get("WHERE")); continue''')
P('''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v131_p57.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''',
  '''                 cmd=f"PYTHONHASHSEED=0 python3 melody_v132_p57.py {N} {MODE}", line_knobs=dict(LK), near_level=NEAR_LEVEL)''')
P('''    rerun["v131_part"] = V131;''', '''    rerun["v132_part"] = V132; rerun["v132_on"] = sorted(f_ for f_ in P132 if ON12(f_)); rerun["sec550"] = SEC550; rerun["kept550"] = KEPT550; rerun["cap551"] = CAP551
    rerun["v132_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("551:", "552:", "555:", "556:")}; rerun["cal553"] = list(CAL553)
    rerun["judge548"] = dict(measures=len(RJ["measures"]), file="zeneng_v132_judge.json" if ON12("548") else "v129")
    rerun["v131_part"] = V131;''')
P('''open(f"/home/claude/p57/melody_v131_p57_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p57/run132/melody_v132_p57_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
