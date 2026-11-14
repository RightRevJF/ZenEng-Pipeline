"""gen_l3_p58.py: writes melody_l3_p58.py (song 48 under Luthier v3: Module 27.84, Window 160) from melody_l2_p58.py, porting 650-656 with
luthier_v3_tables.json (reissued 13 Nov with 655's cap and the ruling on 652 with 653). 657 is a reading; 658-660 are the paper's.
Every patch replaces whole statements and is asserted to match exactly once. ZE_PART_L3 picks the run the paper asks for:
  1 = run A, the rhythm (652, 653, 654, 655, 656); 2 = run B, run A and the pitch (650, 651); 0 = Luthier v2 as it stood.
- 653: a drawn line in a two-bar slot draws one kept line of its cell (notes over the slot's bars) whole: its entry (before, on or after the
  bar line), its span (first to last onset, as a share of its slot, set on this slot) and its breath (a least distance from the last onset to
  the next line's first, held to the cell's kept 75th for lines on the downbeat or not). The span stands in 600's place, the breath in 631's.
  The entry is the kept line's where the first syllable allows (a stressed first syllable is not sung before the bar line); otherwise the
  nearest entry of its kind; otherwise as before, counted.
- 652: a line of 5.5 notes to the slot's bar and over in a two-bar slot, not on copied bars, is sung in whole kept bars of its count of
  notes, drawn by the times they are sung and the stresses on their places, inside 653's entry and breath (the ruling of 13 Nov): a pickup
  as the kept line had it (unstressed syllables only), the first bar from the entry, the last bar a kept bar whose last onset lies within an
  eighth of the kept line's last onset where one fits, otherwise the fitting bar that ends latest; 308's cap holds; no melisma is added. The
  span follows the bars. Where no whole bars fit, the line is drawn as before, counted. A line on the template's bars keeps them (605).
- 654: a line on the template's bars (605) or a returning unit's (361) keeps their span whatever its source did; 631's condition on copies
  holds for copies of whole lines only (none is drawn bar by bar here).
- 655: the palette's share of each gap class is capped at the 95th percentile across kept songs of a song's pooled share in the cell
  ('655: THE CAP'), the excess spread over the classes under their caps. The band's spare (a build not killed by the rhythm band where
  its palette's kept song lies outside the soft band 1.62-3.38) reads each kept song's rhythm-band reading from the reissued tables
  ('655: the band's spare'), used only to say inside or outside; builds spared are counted.
- 656: a line of 13 notes and over in a two-bar slot whose drawn span was not met and whose class was given up has its class drawn again
  from 579's shares at the rate of the rhythm as placed, where its last onset is in its last bar; the next line's entry follows the class.
- 650: every pitch the walk may draw (the walk's moves, a line's first note, a slurred note) is weighted by its ease probability raised to
  a power: the kept model of the tables file (the token: the move clipped to -12..12 and the class of the gap) mixed half and half with
  the song so far (from 8 tokens). The power is set in the calibration so a sung note beats a neighbour on ease in 89% of comparisons;
  the share easier than every neighbour (kept 73%) is read beside it.
- 651: at the first note of a bar of three notes or more that the line sings alone, at a calibrated rate, the bar's intervals are taken from
  a bar of as many notes already sung in the song (drawn among them by how often each was sung), set on the chord: the start drawn near
  the note before, weighted by the chord, where every note of the figure is in the scale, in the register and on no clash. The rate is
  set so 49% of bars of three notes or more sing a figure already sung (kept quartiles 35% and 62%). It replaces 634's classes of move."""
SRC = "/home/claude/p58/melody_l2_p58.py"; DST = "/home/claude/p58/melody_l3_p58.py"
s = open(SRC).read()
def P(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:160]); s = s.replace(a, b)

P('''"""Luthier v2 (Module 27.83; by gen_l2_p58.py''', '''"""Luthier v3 (Module 27.84; by gen_l3_p58.py from melody_l2_p58.py: 650-656; ZE_PART_L3 1 = run A, 2 = run B) -- Luthier v2 (Module 27.83; by gen_l2_p58.py''')
P('''def ON19(f_): return PL2.get(f_, 0) <= VL2 and f_ not in OFF11
''', '''def ON19(f_): return PL2.get(f_, 0) <= VL2 and f_ not in OFF11
VL3 = int(_os11.environ.get("ZE_PART_L3", "2"))
PL3 = {"652": 1, "653": 1, "654": 1, "655": 1, "656": 1, "650": 2, "651": 2}
def ON20(f_): return PL3.get(f_, 0) <= VL3 and f_ not in OFF11
''')
# ---- the tables and the helpers ----
P('''def mix634(gs_, pal_):
''', '''_T3 = json.load(open("/home/claude/p58/tables/luthier_v3_tables.json"))
def _k3(p_): return next(k_ for k_ in _T3 if k_.startswith(p_))
_E650 = _T3[_k3("650: the ease model")]; KC1, KC2, KC3, KN650 = _E650["c1"], _E650["c2"], _E650["c3"], float(_E650["N"])
KB652 = {int(k_): v_ for k_, v_ in _T3[_k3("652: kept bar rhythms")].items() if v_}
KL653 = _T3[_k3("653: kept lines in two-bar slots, whole")]; KS653 = _T3[_k3("653 (answers 638)")]
CAP655 = _T3[_k3("655: THE CAP")]; SP655 = dict(_T3[_k3("655: the band's spare")]["readings"])   # 655: each kept song's rhythm-band reading (the reissue of 13 Nov)
POW650 = [1.0]; R651 = [0.3]; DR653 = {}; W652 = [False]; SONG650 = [None]; LAST650 = [None, None]; PL651 = []; FIGS651 = [{}]; CTX650 = [None]
def kl653(rng_, sec_, i_):
    """653: one kept line of the cell, drawn once a build for the line: entry, span (share of its slot), breath (held to the cell's 75th)."""
    if (sec_, i_) not in DR653:
        c_ = cell600(len(LINES[sec_][i_]) * MEL504[0] / max(1, slot_len(sec_, i_))); e_, sp_, br_, sl_, nn_ = rng_.choice(KL653[c_])
        s_ = KS653[c_]; cap_ = (s_["breath, lines on the downbeat: 25th, 50th, 75th"] if e_ == 0 else s_["breath, other lines"])[2]
        sh_ = sp_ / max(1, sl_); T_ = int(round(sh_ * slot_len(sec_, i_) * BAR / 3)) * 3
        DR653[(sec_, i_)] = dict(e=int(e_), share=sh_, br=max(3, int(round(min(br_, cap_) / 3)) * 3), last=int(e_) + T_, cell=c_)
        STATS["653: a kept line drawn whole (entry, span, breath)"] += 1
        if br_ > cap_: STATS["653: breath held to the cell's kept 75th"] += 1
    return DR653[(sec_, i_)]
_N655 = {0: "sixteenth", 2: "eighth", 3: "dotted eighth", 4: "quarter", 5: "dotted quarter", 6: "half"}
def cap655(pal_, tb_, c_):
    """655: the palette's class shares capped at the cell's 95th across kept songs, the excess spread over the classes under their caps."""
    tab_ = CAP655["two-bar slots (over 6 to 10 beats)" if tb_ == "two-bar" else "all slots (to 24 beats)"][c_]
    cl_ = list(_N655); z_ = sum(pal_[c] for c in cl_) or 1.0; sh_ = {c: pal_[c] / z_ for c in cl_}; capd_ = set()
    for _ in range(6):
        over_ = [c for c in cl_ if c not in capd_ and sh_[c] > tab_[_N655[c]]["95th"] + 1e-9]
        if not over_: break
        ex_ = sum(sh_[c] - tab_[_N655[c]]["95th"] for c in over_)
        for c in over_: sh_[c] = tab_[_N655[c]]["95th"]; capd_.add(c)
        fr_ = [c for c in cl_ if c not in capd_]; zf_ = sum(sh_[c] for c in fr_)
        if not fr_ or zf_ <= 0: break
        for c in fr_: sh_[c] += ex_ * sh_[c] / zf_
    out_ = list(pal_)
    for c in cl_: out_[c] = sh_[c]
    STATS["655: palette capped at the cell's kept 95th" if capd_ else "655: palette inside the cell's caps"] += 1
    return out_
def gcl650(g_): return LR605.gclass(max(1, min(96, int(g_))))
def tok650(dp_, g_): return f"{max(-12, min(12, int(dp_)))}:{gcl650(g_)}"
def pk650(a_, b_, x_):
    """650: the kept model, the three terms present and the floor, over the weights of the terms present."""
    s_ = 0.15 * KC1.get(x_, 0) / KN650 + 0.05 / 225; w_ = 0.2
    c2_ = KC2.get(f"{a_} {b_}", 0) if (a_ is not None and b_ is not None) else 0
    if c2_ > 0: s_ += 0.5 * KC3.get(f"{a_} {b_} {x_}", 0) / c2_; w_ += 0.5
    c1_ = KC1.get(b_, 0) if b_ is not None else 0
    if c1_ > 0: s_ += 0.3 * KC2.get(f"{b_} {x_}", 0) / c1_; w_ += 0.3
    return s_ / w_
class Song650:
    """650: the song so far, as counts of tokens, pairs and triples."""
    def __init__(self): self.c1 = collections.Counter(); self.c2 = collections.Counter(); self.c3 = collections.Counter(); self.n = 0; self.h = []
    def add(self, x_):
        a_ = self.h[-2] if len(self.h) >= 2 else None; b_ = self.h[-1] if self.h else None
        self.c1[x_] += 1; self.n += 1
        if b_ is not None: self.c2[(b_, x_)] += 1
        if a_ is not None: self.c3[(a_, b_, x_)] += 1
        self.h.append(x_)
    def ctx(self): return (self.h[-2] if len(self.h) >= 2 else None, self.h[-1] if self.h else None)
    def copy(self):
        o_ = Song650(); o_.c1 = collections.Counter(self.c1); o_.c2 = collections.Counter(self.c2); o_.c3 = collections.Counter(self.c3); o_.n = self.n; o_.h = list(self.h[-2:]); return o_
def ps650(S_, a_, b_, x_):
    if S_ is None or S_.n < 8: return None
    s_ = 0.15 * S_.c1.get(x_, 0) / S_.n; w_ = 0.15
    c2_ = S_.c2.get((a_, b_), 0) if (a_ is not None and b_ is not None) else 0
    if c2_ > 0: s_ += 0.5 * S_.c3.get((a_, b_, x_), 0) / c2_; w_ += 0.5
    c1_ = S_.c1.get(b_, 0) if b_ is not None else 0
    if c1_ > 0: s_ += 0.3 * S_.c2.get((b_, x_), 0) / c1_; w_ += 0.3
    return s_ / w_
def pe650(S_, a_, b_, x_):
    """650: the ease probability: half the kept model and half the song so far (the kept model alone under 8 tokens)."""
    k_ = pk650(a_, b_, x_); s_ = ps650(S_, a_, b_, x_)
    return k_ if s_ is None else 0.5 * k_ + 0.5 * s_
def e650(p_):
    """650: the weight of a pitch: its ease probability raised to the calibrated power."""
    if CTX650[0] is None: return 1.0
    S_, a_, b_, g_, pv_ = CTX650[0]
    return pe650(S_, a_, b_, tok650(p_ - pv_, g_)) ** POW650[0]
def add650(ns_):
    """650 and 651: a placed line's notes into the song so far, and the bars already sung by their figures."""
    if SONG650[0] is None: return
    for n_ in sorted(ns_, key=lambda x_: x_["on"]):
        if n_.get("p") is None: continue
        if LAST650[0] is not None: SONG650[0].add(tok650(n_["p"] - LAST650[1], n_["on"] - LAST650[0]))
        LAST650[0], LAST650[1] = n_["on"], n_["p"]; PL651.append((n_["on"], n_["p"]))
    if ON20("651") and LAST650[0] is not None:
        by_ = collections.defaultdict(list)
        for o_, p_ in PL651: by_[o_ // BAR].append((o_, p_))
        lb_ = LAST650[0] // BAR; F_ = collections.defaultdict(list)
        for b_, v_ in by_.items():
            if b_ < lb_ and len(v_) >= 3:
                v_.sort(); F_[len(v_)].append(tuple(y_[1] - x_[1] for x_, y_ in zip(v_, v_[1:])))
        FIGS651[0] = F_
def read650(notes):
    """650: every fifth note (from the fifth, stopping four from the end) against each in-scale neighbour 1-4 semitones off, by the summed
    ease bits of the three tokens it touches, the song so far being the tokens before the move into it: (share of comparisons the sung
    note wins, share of notes easier than every neighbour)."""
    ns = sorted([n_ for n_ in notes if n_.get("p") is not None], key=lambda n_: n_["on"])
    if len(ns) < 12: return (float("nan"), float("nan"))
    P_ = [n_["p"] for n_ in ns]; O_ = [n_["on"] for n_ in ns]
    tk = [None] + [tok650(P_[k] - P_[k - 1], O_[k] - O_[k - 1]) for k in range(1, len(ns))]
    S_ = Song650(); beat = tot = every = nn = 0
    for j in range(1, len(ns)):
        if j >= 4 and (j - 4) % 5 == 0 and j <= len(ns) - 5:
            def bits(pj):
                t1 = tok650(pj - P_[j - 1], O_[j] - O_[j - 1]); t2 = tok650(P_[j + 1] - pj, O_[j + 1] - O_[j]); t3 = tk[j + 2]
                return -(math.log2(pe650(S_, tk[j - 2], tk[j - 1], t1)) + math.log2(pe650(S_, tk[j - 1], t1, t2)) + math.log2(pe650(S_, t1, t2, t3)))
            sb_ = bits(P_[j]); nb_ = [bits(P_[j] + d_) for d_ in (-4, -3, -2, -1, 1, 2, 3, 4) if (P_[j] + d_) % 12 in M.SCALE]
            if nb_: tot += len(nb_); beat += sum(sb_ < x_ for x_ in nb_); every += all(sb_ < x_ for x_ in nb_); nn += 1
        S_.add(tk[j])
    return (beat / tot if tot else float("nan"), every / nn if nn else float("nan"))
def read651(notes):
    """651: of the song's bars of three notes or more, the share whose figure (the intervals within the bar) was already sung."""
    by_ = collections.defaultdict(list)
    for n_ in notes:
        if n_.get("p") is not None: by_[n_["on"] // BAR].append((n_["on"], n_["p"]))
    seen_ = set(); hit_ = tot_ = 0
    for b_ in sorted(by_):
        v_ = sorted(by_[b_])
        if len(v_) < 3: continue
        f_ = tuple(y_[1] - x_[1] for x_, y_ in zip(v_, v_[1:])); tot_ += 1; hit_ += f_ in seen_; seen_.add(f_)
    return hit_ / tot_ if tot_ else None
def whole652(rng, sy, st, tmin, end, kl, A, cap):
    """652 (with 653, the ruling of 13 Nov): a dense line in whole kept bars inside the kept line's entry and breath, or None."""
    n = len(sy); e = kl["e"] if kl else 0; Lt = kl["last"] if kl else None
    if st[0] and e < 0: e = 0
    pk = []
    if e < 0:
        full_ = list(range(e, 0, 6)); c_ = 0
        while c_ < n and not st[c_]: c_ += 1
        k0 = min(len(full_), c_, n - 2)
        pk = full_ if k0 == len(full_) else (list(range(-6 * k0, 0, 6)) if k0 > 0 else [])
    pk = [t for t in pk if t >= tmin]; k0 = len(pk); m = n - k0
    e1 = 0 if pk else max(0, e)
    splits = [(a, m - a) for a in range(1, m) if a in KB652 and (m - a) in KB652 and a <= cap and (m - a) <= cap]
    if not splits: return None
    def wbar(rows, off, kf, prev_t, first):
        out = []
        for ons_, cnt_, _s in rows:
            ts_ = [off + t for t in ons_]
            if ts_[0] < tmin: continue
            if first and not pk and ((e1 == 0 and ts_[0] != 0) or (e1 > 0 and ts_[0] <= 0)): continue   # the entry on, or after, the bar line
            if prev_t is not None and not (3 <= ts_[0] - prev_t <= 24): continue
            w = float(cnt_) * (3.0 if (first and not pk and e1 > 0 and ts_[0] == e1) else 1.0)
            for j, t in enumerate(ts_): w *= A(kf + j, t)
            if w > 0: out.append((ts_, w))
        return out
    B0 = {}
    for a, c in splits:
        b0 = wbar(KB652[a], 0, k0, pk[-1] if pk else None, True)
        if b0: B0[(a, c)] = b0
    if not B0: return None
    keys_ = list(B0)
    for _ in range(12):
        a, c = rng.choices(keys_, [sum(w for _, w in B0[k_]) for k_ in keys_])[0]
        t0 = rng.choices(B0[(a, c)], [w for _, w in B0[(a, c)]])[0][0]
        b1 = [x for x in wbar(KB652[c], BAR, k0 + a, t0[-1], False) if x[0][-1] <= end]
        if not b1: continue
        near = [x for x in b1 if Lt is not None and abs(x[0][-1] - Lt) <= 6]
        if near: t1 = rng.choices(near, [w for _, w in near])[0][0]; STATS["652: last bar within an eighth of the kept line's last onset"] += 1
        elif Lt is not None: t1 = max(b1, key=lambda x: (x[0][-1], x[1]))[0]; STATS["652: last bar the fitting bar that ends latest"] += 1
        else: t1 = rng.choices(b1, [w for _, w in b1])[0][0]
        return pk + t0 + t1
    return None
def mix634(gs_, pal_):
''')
P('''    PAL606[0] = None; BR631.clear(); MET600.clear(); PREVB[0] = None; PALCAT634[0] = None
''', '''    PAL606[0] = None; BR631.clear(); MET600.clear(); PREVB[0] = None; PALCAT634[0] = None
    DR653.clear(); SONG650[0] = Song650() if (ON20("650") or ON20("651")) else None; LAST650[:] = [None, None]; PL651.clear(); FIGS651[0] = {}; CTX650[0] = None   # 650-653
''')
# ---- 653: the breath of the kept line, in 631's place ----
P('''    if (sec_, i_) not in BR631:
        q_ = BR631T''', '''    if ON20("653") and slot_len(sec_, i_) == 2: return kl653(rng_, sec_, i_)["br"]          # 653: the kept line's breath
    if (sec_, i_) not in BR631:
        q_ = BR631T''')
# ---- 653: the span of the kept line, in 600's place ----
P('''S600_ = draw_span600(rng, SPQ600[tb600_][c600_]); D600 = True''',
  '''S600_ = (kl653(rng, sec, i)["share"] if (ON20("653") and slot_len(sec, i) == 2) else draw_span600(rng, SPQ600[tb600_][c600_])); D600 = True   # 653: the kept line's span''')
# ---- 653: the entry of the kept line ----
P('''            if f0s_:
                t0_ = rng.choice(f0s_); F600C[0] = (t0_, t0_ + T600_); tgt = None
            else: STATS["600: no first onset leaves room for the drawn span (a try)"] += 1''',
  '''            k6_ = False
            if ON20("653") and slot_len(sec, i) == 2:                                         # 653: the entry as the kept line had it, where the first syllable allows
                e653_ = kl653(rng, sec, i)["e"]; f0a_ = [t for t in range(max(-12, tmin), end - T600_ + 4, 3) if not (st[0] and t < 0)]
                if e653_ in f0a_: f0s_ = [e653_]; k6_ = True; STATS["653: entry as the kept line had it"] += 1
                else:
                    kd6_ = entry_kind(e653_) if not (st[0] and e653_ < 0) else "on"; sk6_ = [t for t in f0a_ if entry_kind(t) == kd6_]
                    if sk6_: f0s_ = [min(sk6_, key=lambda t: abs(t - e653_))]; k6_ = True; STATS["653: entry of the kept line's kind, the nearest"] += 1
                    else: STATS["653: the kept line's entry out of reach (a try)"] += 1
            if f0s_:
                t0_ = rng.choice(f0s_); F600C[0] = (t0_, t0_ + T600_); tgt = None
                if k6_: kind_ = None                                                        # 653: the entry is the kept line's, not 340's draw
            else: STATS["600: no first onset leaves room for the drawn span (a try)"] += 1''')
# ---- 652: whole kept bars ----
P('''    NT = 20 if copybars else 14; fb457 = [False]; G542[:] = [0, 0]
    if n >= 9: NT = 60
''', '''    NT = 20 if copybars else 14; fb457 = [False]; G542[:] = [0, 0]
    if n >= 9: NT = 60
    W652[0] = False
    if ON20("652") and i is not None and not fix and not copybars and slot_len(sec, i) == 2 and n * MEL504[0] / 2 >= 5.5:   # 652: a dense line in whole kept bars
        o652_ = whole652(rng, sy, st, tmin, end, kl653(rng, sec, i) if ON20("653") else None, A, cap)
        if o652_ is not None:
            W652[0] = True; MET600[(sec, i)] = True; STATS["652: dense line sung in whole kept bars"] += 1
            return o652_
        STATS["652: no whole kept bars fit; the line drawn as before"] += 1
''')
P('''    rows = melismas(ons, rng, me_, PALS.get(KIND[sec])) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]''',
  '''    rows = melismas(ons, rng, me_, PALS.get(KIND[sec])) if ((not fix or len(fix) < len(sy)) and not W652[0]) else [[t, k, False] for k, t in enumerate(ons)]   # 652: whole bars, no melisma added''')
# ---- 654: the template's bars keep their span ----
P('''                                if ON19("631") and MET600.get((sec, js_)) is False: COPYMET[0] = False''',
  '''                                if ON19("631") and not ON20("654") and MET600.get((sec, js_)) is False: COPYMET[0] = False''')
P('''                        if ON19("631") and MET600.get((sec, js_)) is False: COPYMET[0] = False''',
  '''                        if ON19("631") and not ON20("654") and MET600.get((sec, js_)) is False: COPYMET[0] = False''')
# ---- 655: the palette capped ----
P('''        if ON19("634"): MIX634[0] = mix634(gs606_, PAL606[0][0]);''',
  '''        if ON19("634"): MIX634[0] = mix634(gs606_, cap655(PAL606[0][0], tb606_, cell600(x606_)) if ON20("655") else PAL606[0][0]);''')
P('''    l7, tb = limit7_readings(notes); s7, h7 = limit7_breaks(l7)
''', '''    l7, tb = limit7_readings(notes); s7, h7 = limit7_breaks(l7)
    if ON20("655") and "rhythm band" in s7 + h7:                                          # 655: the band's spare, where the palette's kept song lies outside it
        rb655_ = SP655.get(c["meta"].get("palette606"))
        if rb655_ is not None and not (1.62 <= rb655_ <= 3.38):
            s7 = [x_ for x_ in s7 if x_ != "rhythm band"]; h7 = [x_ for x_ in h7 if x_ != "rhythm band"]; info["spared655"] = c["meta"].get("palette606")
        elif rb655_ is None: info["unspared655"] = "the kept song's rhythm reading is not in the tables"
''')
# ---- 656: the class as sung ----
P('''        if i is not None and D600: MET600[(sec, i)] = bool(F600C[0] is not None or (copybars and allbars and COPYMET[0]))   # 631: the line met its drawn span (or copied a source that met its own)
        return ons''', '''        if i is not None and D600: MET600[(sec, i)] = bool(F600C[0] is not None or (copybars and allbars and COPYMET[0]))   # 631: the line met its drawn span (or copied a source that met its own)
        if (ON20("656") and d465 is not None and not h465 and n >= 13 and i is not None and slot_len(sec, i) == 2 and D600 and F600C[0] is None
                and ons[-1] // BAR == slot_len(sec, i) - 1 and d465.get("nxt") is not None):    # 656: the span not met: the class drawn again from the rhythm as placed
            x656_ = 4 * (n - 1) / max(0.25, (ons[-1] - ons[0]) / BEAT); p656_ = 0.65 if x656_ < 8 else 0.51 if x656_ < 10 else 0.34
            k656_ = 0 if rng.random() < p656_ else 1; REQ465[d465["nxt"]] = "pickup" if k656_ == 0 else "no pickup"
            STATS[f"656: class drawn again from the rhythm as placed (class {k656_})"] += 1
        return ons''')
# ---- 650: the ease in the walk ----
P('''                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_ * lt_ * pm_); base += w0''',
  '''                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p) * sf * extra_w(p) * rs_ * lt_ * pm_ * (e650(p) if ON20("650") else 1.0)); base += w0   # 650''')
P('''    return rng.choices(cands, [math.exp(-(p - h0) ** 2 / (2 * 1.5 ** 2)) * M.kp(p) * chord_w(p, n, ch) * deg_w(p) + 1e-12 for p in cands])[0]''',
  '''    return rng.choices(cands, [(math.exp(-(p - h0) ** 2 / (2 * 1.5 ** 2)) * M.kp(p) * chord_w(p, n, ch) * deg_w(p) + 1e-12) * (e650(p) if ON20("650") else 1.0) for p in cands])[0]   # 650''')
P('''            p = rng.choices(opts, [(3 if x < q_ else 1) * (chord_w(x, n, ch_) if not t602_ else 1.0)''',
  '''            p = rng.choices(opts, [(e650(x) if ON20("650") else 1.0) * (3 if x < q_ else 1) * (chord_w(x, n, ch_) if not t602_ else 1.0)''')
# 651 replaces 634's classes of move
P('''(PALCAT634[0][c] if (ON19("634") and PALCAT634[0] is not None) else AIM.cat[c])''',
  '''(PALCAT634[0][c] if (ON19("634") and not ON20("651") and PALCAT634[0] is not None) else AIM.cat[c])''')
# the walk: 650's context per note, 651's figures per bar
P('''    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None; ZZ452[0] = ZZ452[1] = 0
''', '''    on0_ = set(notes_on); out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None; ZZ452[0] = ZZ452[1] = 0
    S650l_ = SONG650[0].copy() if (ON20("650") and SONG650[0] is not None) else None; fig_ = {}   # 650: the song so far, this line's tokens added as it goes; 651
''')
P('''    for i, n in enumerate(notes):
        if fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:''', '''    for i, n in enumerate(notes):
        g650_ = (n["on"] - (notes[i - 1]["on"] if i > 0 else LAST650[0])) if (i > 0 or LAST650[0] is not None) else None
        CTX650[0] = (S650l_, *S650l_.ctx(), g650_, prev) if (S650l_ is not None and g650_ is not None and prev is not None) else None   # 650
        if (ON20("651") and i not in fig_ and (i == 0 or notes[i - 1]["on"] // BAR != n["on"] // BAR)):   # 651: a bar this line sings alone, of three notes or more
            b651_ = n["on"] // BAR; ix_ = [j for j in range(i, len(notes)) if notes[j]["on"] // BAR == b651_]
            t602b_ = (len(notes) - 1) in ix_ and ON17("602") and isinstance(CUR424[0], tuple) and SRC602.get(CUR424[0][0]) == CUR424[0][1]
            if (len(ix_) >= 3 and not any(t_ // BAR == b651_ for t_ in on0_) and not (fixed and any(j in fixed for j in ix_)) and not t602b_
                    and FIGS651[0].get(len(ix_))):
                STATS["651: bars eligible"] += 1
                if rng.random() < R651[0]:
                    fg_ = rng.choice(FIGS651[0][len(ix_)]); cs_ = []; ref_ = prev if prev is not None else mu
                    chs_ = [M.chord_for(notes[j], notes_on) for j in ix_]
                    for s0_ in range(lo, hi + 1):
                        if s0_ % 12 not in M.SCALE or abs(s0_ - ref_) > 9: continue
                        qs_ = [s0_]
                        for d_ in fg_: qs_.append(qs_[-1] + d_)
                        if all(lo <= q_ <= hi and q_ % 12 in M.SUNGPC and not M.clash(q_, c_) and not tri(q_, c_) for q_, c_ in zip(qs_, chs_)):
                            cs_.append((qs_, math.exp(-(s0_ - ref_) ** 2 / (2 * 2.5 ** 2)) * chord_w(s0_, notes[i], chs_[0])))
                    if cs_ and sum(w_ for _, w_ in cs_) > 0:
                        qs_ = rng.choices([q_ for q_, _ in cs_], [w_ for _, w_ in cs_])[0]; fig_.update({j: q_ for j, q_ in zip(ix_, qs_)}); STATS["651: bar takes a figure already sung"] += 1
                    else: STATS["651: figure drawn but not placeable on the chord"] += 1
        if i in fig_: p = fig_[i]                                                          # 651: the bar's figure
        elif fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:''')
P('''        if prev is not None and p != prev: ZZ452[0], ZZ452[1] = ZZ452[1], (1 if p > prev else -1)   # 452: the last two moves
''', '''        if S650l_ is not None and g650_ is not None and prev is not None: S650l_.add(tok650(p - prev, g650_))   # 650: the line's tokens into the song so far
        if prev is not None and p != prev: ZZ452[0], ZZ452[1] = ZZ452[1], (1 if p > prev else -1)   # 452: the last two moves
''')
P('''        built[(sec, i)] = ns; lines.append(ns)
''', '''        built[(sec, i)] = ns; lines.append(ns); add650(ns)                                 # 650, 651: the song so far
''')
P('''            if p is None: return None
''', '''            if p is None: CTX650[0] = None; return None
''')
P('''        prev = p; out.append(p)
    return out
def fresh_line(''', '''        prev = p; out.append(p)
    CTX650[0] = None; return out                                                         # 650: no context outside the walk
def fresh_line(''')
# ---- the calibration: 650's power and 651's rate ----
P('''                    if r605_[k_][0] is not None: ua["_r605_" + str(k_)].append(r605_[k_][0])
''', '''                    if r605_[k_][0] is not None: ua["_r605_" + str(k_)].append(r605_[k_][0])
            if ON20("650"): e6_ = read650(c2["notes"]); ua["_e650a"].append(e6_[0]); ua["_e650b"].append(e6_[1])
            if ON20("651"):
                f6_ = read651(c2["notes"])
                if f6_ is not None: ua["_f651"].append(f6_)
''')
P('''            if ON18("605") and ua.get("_r605_4"):''', '''            if ON20("650") and ua.get("_e650a"):                                              # 650: the power toward a sung note easier than a neighbour in 89%
                r_ = float(np.nanmean(ua["_e650a"])); f_ = float(np.clip(((0.89 - 0.5) / max(0.02, r_ - 0.5)) ** 3, 0.6, 1.6)); POW650[0] = float(np.clip(POW650[0] * f_, 0.05, 8.0))
                if f_ in (0.6, 1.6): full_now.add("pow650")
                row["650 (kept, reading, power)"] = dict(neighbour=(0.89, round(r_, 3)), every=(0.727, round(float(np.nanmean(ua["_e650b"])), 3)), power=round(POW650[0], 3))
            if ON20("651") and ua.get("_f651"):                                               # 651: the rate toward 49% of bars of three notes or more on a figure already sung
                r_ = float(np.mean(ua["_f651"])); R651[0] = float(np.clip(R651[0] + 1.5 * (0.488 - r_), 0.0, 1.0))
                if abs(0.488 - r_) > 0.08 and 0.0 < R651[0] < 1.0: full_now.add("r651")
                row["651 (kept, reading, rate)"] = dict(kept=0.488, read=round(r_, 3), rate=round(R651[0], 3))
            if ON18("605") and ua.get("_r605_4"):''')
# ---- the record ----
P('''    rerun["l2_part"] = VL2;''', '''    rerun["l3_part"] = VL3; rerun["l3_on"] = sorted(f_ for f_ in PL3 if ON20(f_)); rerun["pow650"] = round(POW650[0], 4); rerun["r651"] = round(R651[0], 4)
    rerun["l3_stats"] = {k_: v_ for k_, v_ in sorted(STATS.items()) if k_[:4] in ("650:", "651:", "652:", "653:", "655:", "656:", "600:", "631:", "605:", "633:", "634:", "465:")}
    rerun["l2_part"] = VL2;''')
P('''cmd=f"PYTHONHASHSEED=0 python3 melody_l2_p58.py {N} {MODE}"''', '''cmd=f"ZE_PART_L3={VL3} PYTHONHASHSEED=0 python3 melody_l3_p58.py {N} {MODE}"''')
P('''open(f"/home/claude/p58/runl2/melody_l2_p58_{MODE}{_TAG}.pkl", "wb")''', '''open(f"/home/claude/p58/runl3/melody_l3p{VL3}_p58_{MODE}{_TAG}.pkl", "wb")''')
open(DST, "w").write(s)
print("wrote", DST)
