"""Module 27 melody search for 'Five-Oh-One' (ZenEng v64 port, v65 fixes as ports; one male tenor; funk-pop, 4/4 at q = 112 on a
SIXTEENTH grid -- the run's port: meter '4/4s', 16 slots a bar, stresses on the eighths, the quarter beats strong; a line two bars =
32 slots). Eb major to the lift, F major from the gang's shout to the end.
  * Singer (11.2 tenor, v65 fix 14 row): D3-A4, Bb4 once. Verses low and close (D3-F4); the chorus to G4 in Eb, A4 in F; Bb4 once, on the
    last chorus's turn word HERE, over Bb.
  * The title cell first: 'FIVE-oh-ONE' -- dotted eighth, sixteenth, eighth (slots 0, 3, 4); Bb3-Eb4-G4, the tonic triad up to the
    chorus's top on ONE (beat 2). Every 'five-oh-one' line opens with it; the hook chants it on a tresillo (3+3+2).
  * The gang's shout (the lift): FIVE-OH-ONE on three quarter-note hits over C, the pivot into F.
  * v63/v64 cell grammar for the verses, pre-choruses and breakdown (drawn / surface / skeleton); line 2 open.
  Calibration: pop major, read in Eb (TCAL 3) on verse 1 and the chorus."""
import sys, math, json, pickle, random, hashlib, collections
import numpy as np
sys.path[:0] = ["/home/claude/p26", "/home/claude/carol", "/home/claude/pop"]
import engine_p26 as E, phrasestress48 as PS; PS.install(E); E.install_patches()
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec, syncopation, intervals
import lyric as L
syllables = E.syllables
TCAL = 3
EB = {3, 5, 7, 8, 10, 0, 2}
FM = {5, 7, 9, 10, 0, 2, 4}
CH = {"Eb": {3, 7, 10}, "Ab": {8, 0, 3}, "Bb": {10, 2, 5}, "Cm": {0, 3, 7}, "Gm": {7, 10, 2}, "C": {0, 4, 7}, "F": {5, 9, 0}, "Dm": {2, 5, 9}}
HIM = dict(lo=50, verse=65, pre=65, chorus=67, hook=67, breakdown=63, lift=67, chorusF=69, peak=70)
HER = HIM
LO = 50
METER = {"4/4s": dict(bar=16, beats=[0, 2, 4, 6, 8, 10, 12, 14], strong=[0, 4, 8, 12], fin=4)}
QBPM = 112
LATER_PK = 4          # the run's port (16ths): inside a section a line's pickup is at most a quarter (four sixteenths)
CELL = [(0, 3, 58), (3, 1, 63), (4, 2, 67)]                       # FIVE-oh-ONE: Bb3 Eb4 G4, dotted eighth / sixteenth / eighth
HOOK_RH = [(0, 3), (3, 3), (6, 3), (9, 3), (12, 2), (14, 2), (16, 8)]   # the tresillo chant: FIVE-oh FIVE-oh FIVE-oh-ONE
HOOK_P = [58, 63, 58, 63, 58, 63, 67]
SHOUT = [(0, 3, 64), (4, 3, 64), (8, 8, 67)]                       # the gang: FIVE - OH - ONE over C
CAL = json.load(open("/home/claude/pop/pop_calibration.json")); C = CAL["cal"]
MU, SD = np.array(CAL["mu"]), np.array(CAL["sd"]); ZREF = np.array(CAL["Z"]); REAL_KNN = CAL["real_knn"]
PPMM = pickle.load(open("/home/claude/pop/pop_ppm.pkl", "rb"))
IM = pickle.load(open("/home/claude/pop/pop_intervals.pkl", "rb"))
def iv_weight(prev_iv, prev_deg, iv):
    c = IM.get((max(-7, min(7, prev_iv)), prev_deg))
    if not c: return 0.05
    return (c.get(iv, 0) + 0.2) / (sum(c.values()) + 5)
def red(x): return x[1].endswith("0") or not x[2]
VERSE = [["Eb", "Ab"], ["Eb", "Ab"], ["Eb", "Ab"], ["Cm", "Bb"]]
PRE = [["Ab", "Bb"], ["Cm", "Bb"]]
CHO = [["Eb", "Bb"], ["Cm", "Ab"], ["Eb", "Bb"], ["Ab", "Bb"]]
HOOKC = [["Eb", "Ab"], ["Eb", "Ab"]]
BRK = [["Cm", "Cm"], ["Ab", "Ab"], ["Cm", "Cm"], ["Ab", "Bb"]]
LIFTC = [["Ab", "Bb"], ["C", "C"]]
CHOF = [["F", "C"], ["Dm", "Bb"], ["F", "C"], ["Bb", "C"]]
HOOKF = [["F", "Bb"], ["F", "Bb"]]
FORM = [
    ("Intro", "4/4s", EB, None, ["Eb", "Ab", "Eb", "Ab"]),
    ("Verse 1", "4/4s", EB, L.V1, VERSE),
    ("Pre 1", "4/4s", EB, L.PRE1, PRE),
    ("Chorus 1", "4/4s", EB, L.CHORUS, CHO),
    ("Hook 1", "4/4s", EB, L.HOOK, HOOKC),
    ("Verse 2", "4/4s", EB, L.V2, VERSE),
    ("Pre 2", "4/4s", EB, L.PRE2, PRE),
    ("Chorus 2", "4/4s", EB, L.CHORUS, CHO),
    ("Hook 2", "4/4s", EB, L.HOOK, HOOKC),
    ("Breakdown", "4/4s", EB, L.BREAK, BRK),
    ("Lift", "4/4s", EB, L.LIFT, LIFTC),
    ("Chorus 3", "4/4s", FM, L.CHORUS, CHOF),
    ("Chorus 4", "4/4s", FM, L.LAST, CHOF),
    ("Hook 3", "4/4s", FM, L.HOOK, HOOKF),
    ("Outro", "4/4s", FM, L.OUTRO, [["F", "Bb"]]),
    ("Ending", "4/4s", FM, None, ["F", "F"]),
]
SINGER = L.SINGER
BARS, SECS, STARTS = [], {}, {}
pos = 0
for sec, met, scale, lines, chs in FORM:
    STARTS[sec] = (len(BARS), pos)
    bl = METER[met]["bar"]
    if lines is None:
        for c in chs: BARS.append(dict(sec=sec, meter=met, chord=c, start=pos, len=bl, scale=scale)); pos += bl
        continue
    SECS[sec] = []
    for i, ((role, l), cl) in enumerate(zip(lines, chs)):
        at = pos
        for c in cl: BARS.append(dict(sec=sec, meter=met, chord=c, start=pos, len=bl, scale=scale)); pos += bl
        SECS[sec].append(dict(line=l, role=role, syl=syllables(l), at=at, n=len(cl) * bl, meter=met, scale=scale, idx=i,
                              commas=None))
TOTAL = pos; NBARS = len(BARS)
BAR_AT = []
for b in BARS: BAR_AT += [b] * b["len"]
def bar_of(e): return BAR_AT[min(len(BAR_AT) - 1, max(0, int(e)))]
def chord_at(e): return bar_of(e)["chord"]
def strong_abs(e):
    b = bar_of(e); return (e - b["start"]) in METER[b["meter"]]["strong"]
def comma_after(line):
    out, k = set(), 0
    for chunk in line.replace(".", ",").split(","):
        k += len(syllables(chunk)) if chunk.strip() else 0
        out.add(k - 1)
    return out - {k - 1}
for s in SECS:
    for ln in SECS[s]: ln["commas"] = comma_after(ln["line"])
SINGS = list(SECS)
for _s in SECS:
    for _ln in SECS[_s]: _ln["nomin"] = True        # two-bar lines (12 eighths): no minimum reach
# ---- rhythm ----
def beats_of(ln):
    m = METER[ln["meter"]]; bl = m["bar"]
    return {b * bl + x for b in range(-1, ln["n"] // bl + 2) for x in m["beats"]}, {b * bl + x for b in range(0, ln["n"] // bl + 1) for x in m["strong"]}
def walk(ln, rng, pickup, p_stretch=0.4, p_antic=0.25):
    beats, _ = beats_of(ln); syl = ln["syl"]
    slots, pos, prev_st = [], -pickup, True
    for i, (w, v, st, fn) in enumerate(syl):
        if i - 1 in ln["commas"]: pos += 1
        if st and pos not in beats and not prev_st:
            nxt = min((b for b in beats if b > pos), default=pos + 1)
            if nxt - pos == 1 and rng.random() < p_antic: pass
            else: pos = nxt
        slots.append(pos)
        step = 1
        if ln["meter"] == "4/4s":                             # the run's port (16ths): a stress takes a sixteenth to a quarter; a weak syllable a sixteenth or an eighth
            r = rng.random(); sparse = len(syl) / ln["n"] < 0.36      # a short line in two bars takes longer steps
            if st and i < len(syl) - 1:
                step = (1 if r < 0.1 else (2 if r < 0.4 else (3 if r < 0.65 else 4))) if sparse else (1 if r < 0.25 else (2 if r < 0.7 else (3 if r < 0.85 else 4)))
            elif i < len(syl) - 1: step = (1 if r < 0.35 else 2) if sparse else (1 if r < 0.6 else 2)
        elif st and i < len(syl) - 1 and pos in beats:
            r = rng.random()
            if ln["meter"] == "6/8": step = 2 if r < p_stretch else (3 if r < p_stretch + 0.35 else 1)   # 6/8: the quarter or the dotted quarter
            elif r < p_stretch: step = 2
            elif r < p_stretch + (0.25 if ln["n"] >= 24 else 0.15): step = 3
            elif r < p_stretch + 0.2 and ln["meter"] in ("4/4", "3/4"): step = 4
        pos += step; prev_st = st
    return slots
def agreement(ln, sl):
    _, strong = beats_of(ln); syl = ln["syl"]
    on = [(s, x) for s, x in zip(sl, syl) if s in strong]
    ant = sum(1 for s, x in zip(sl, syl) if x[2] and (s + 1) in strong and (s + 1) not in sl)
    bad = any(not x[2] and not x[3] for s, x in on)
    return (sum(1 for s, x in on if x[2]) + 0.5 * ant) / max(1, len(on) + ant), bad
def fin_ok(ln, sl):
    """song 25 finding: a line's last stressed syllable lands on a beat (6/8: a dotted-quarter pulse)"""
    st = [s for s, x in zip(sl, ln["syl"]) if x[2]]
    m = METER[ln["meter"]]
    return not st or (st[-1] % m.get("fin", m["bar"] // len(m["beats"]))) == 0
def rhythm(ln, rng, maxslot, minslot=None, cond=None, tries=200, maxpk=3):
    pool = {}
    for _ in range(tries):
        pk = rng.choice(list(range(0, maxpk + 1)))
        sl = walk(ln, rng, pk)
        if sl[-1] > maxslot or (minslot is not None and sl[-1] < minslot): continue
        ag, bad = agreement(ln, sl)
        if bad or ag < 0.5: continue
        if cond and not cond(sl): continue
        pool[tuple(sl)] = ag + (1.0 if fin_ok(ln, sl) else 0.0)          # song 25: a line-final stress on a beat is preferred
    if not pool: return None
    top = max(pool.values()); ok = [list(k) for k, v in pool.items() if v >= top - 0.2 and (v >= 1.5) == (top >= 1.5)]
    w = [1.0 / (1 + max(0, -k[0])) for k in ok]
    return rng.choices(ok, w)[0]
def fem_tail(syl):
    n = 0
    for k in range(len(syl) - 1, 0, -1):
        if syl[k][2]: break
        if syl[k][0] != syl[k - 1][0]: return 0
        n += 1
    return n
def section_rhythms(lines, rng, after_pk=0, conds=None, first_maxpk=3):
    for _ in range(30):
        out = [None] * len(lines); nxt = after_pk; ok = True
        for i in range(len(lines) - 1, -1, -1):
            ln = lines[i]; n = ln["n"]
            g = 1 if ln["meter"] == "4/4s" else 0
            mx = (n - 2 - nxt if nxt else n - 3) - g
            mn = n - 9 if n >= 24 and not ln.get("nomin") else None

            sl = rhythm(ln, rng, mx, mn, cond=(conds or {}).get(i), maxpk=first_maxpk if i == 0 else LATER_PK)
            if sl is None: ok = False; break
            out[i] = sl; nxt = max(0, -sl[0])
        if ok: return out
    return None
def durs(ln, sl, nxt_on=None):
    syl = ln["syl"]; n = ln["n"]
    gap = 2 if ln["meter"] == "4/4s" else 1                     # 16ths: an eighth's breath before the next line
    end = n - gap if nxt_on is None else min(n - gap, nxt_on - gap)
    d = [b - a for a, b in zip(sl, sl[1:])] + [max(1, end - sl[-1])]
    for k, x in enumerate(syl):
        if not x[2] and d[k] > 2 and not (k == len(d) - 1 and (sl[k] % METER[ln["meter"]]["bar"]) in METER[ln["meter"]]["strong"]): d[k] = 2 if k < len(d) - 1 else min(d[k], 2)   # the run's port (song 24): a line-final syllable on a beat holds
    for k in ln["commas"]:
        if k < len(d) - 1: d[k] = min(d[k], sl[k + 1] - sl[k] - 1)
    return d if min(d) >= 1 else None
def apply_tail(ln, sl, du):
    """21.7a: the feminine tail repeats its stress's pitch (set in the fill), an eighth, never on a beat, on the last eighth
    before the bar line where it fits"""
    ft = fem_tail(ln["syl"])
    if not ft or ln["meter"] == "4/4s": return sl, du             # 16ths: the walk's own tail (a sixteenth or an eighth after the stress) stands
    bl = METER[ln["meter"]]["bar"]; _, strong = beats_of(ln)
    k0 = len(sl) - ft - 1                                  # the stressed syllable
    bar_end = (sl[k0] // bl + 1) * bl
    if ln.get("nomin"): bar_end = (ln["n"] // bl - 1) * bl   # a tail closes the line's own bar; the next bar answers
    cand = [bar_end - ft + j for j in range(ft)]
    lim = ln.get("_lim", ln["n"] - 2)
    if cand[0] <= sl[k0] or cand[-1] > lim or any(c in strong for c in cand):
        late = [e for e in range(lim - ft + 1, sl[k0], -1) if not any((e + j) in strong for j in range(ft))]
        cand = [late[0] + j for j in range(ft)] if late else [sl[k0] + 1 + j for j in range(ft)]   # the run's port: the latest free eighth before the next line when the bar line is out of reach
        if any(c in strong for c in cand): return None, None
    sl = sl[:k0 + 1] + cand
    du = du[:k0] + [cand[0] - sl[k0]] + [1] * ft
    return sl, du

# ---- pitch ----
def runs(ps):
    r = b = 1
    for x, y in zip(ps, ps[1:]):
        r = r + 1 if x == y else 1; b = max(b, r)
    return b
def fill(ons, syl, scale, lo, hi, centers, maxleap, rng, prev=None, prev_iv=0, fixed=None, sigma=2.0):
    out = []
    for k, on in enumerate(ons):
        if fixed and k in fixed: p = fixed[k]
        else:
            ch = chord_at(on); strong = strong_abs(on)
            cands, ws = [], []
            for p in range(lo, hi + 1):
                pc = p % 12
                if pc not in scale and pc not in CH[ch]: continue
                if prev is not None and (abs(p - prev) > maxleap or abs(p - prev) == 6): continue
                if len(out) >= 3 and all(q == p for q in out[-3:]): continue
                if fixed and (k + 1) in fixed and (abs(fixed[k + 1] - p) > maxleap or abs(fixed[k + 1] - p) == 6): continue   # the run's port: look ahead to an aimed note
                w = iv_weight(prev_iv, (prev - TCAL) % 12, p - prev) if prev is not None else 1.0
                tone = pc in CH[ch]
                w *= (4.0 if tone else 0.3) if strong else (1.6 if tone else 1.0)
                w *= math.exp(-((p - centers[k]) ** 2) / (2 * sigma ** 2))
                rd = red(syl[k])
                if rd and out and p > max(out): w *= 0.05
                elif rd and prev is not None and p > prev: w *= 0.4
                cands.append(p); ws.append(w)
            if not cands: return None
            p = rng.choices(cands, ws)[0]
        if prev is not None: prev_iv = p - prev
        prev = p; out.append(p)
    return out
def build_line(ln, rng, prev, centers, lo, cap, maxleap, sl, fixed=None, sigma=2.0, nxt_on=None):
    ln["_lim"] = (nxt_on - 2) if nxt_on is not None else ln["n"] - 2
    du = durs(ln, sl, nxt_on)
    if du is None: return None
    sl2, du2 = apply_tail(ln, sl, du)
    if sl2 is None: return None
    ons = [ln["at"] + x for x in sl2]
    ft = fem_tail(ln["syl"])
    for _ in range(14):
        cen = [centers(j, len(ons)) for j in range(len(ons))] if callable(centers) else centers
        if len(cen) != len(ons): cen = [cen[round(j * (len(cen) - 1) / max(1, len(ons) - 1))] for j in range(len(ons))]
        fx = {(len(ons) + k if k < 0 else k): v for k, v in (fixed or {}).items() if k != "aim"}
        if fixed and "aim" in fixed:                       # v59 fix 9: the line aimed at a stressed full vowel, on a chord tone of its bar
            opts = [(k, p) for k, x in enumerate(ln["syl"]) if x[2] and not x[1].endswith("0") and k < len(ons) - ft
                    for p in fixed["aim"] if p % 12 in CH[chord_at(ons[k])]]
            if not opts: return None
            k, p = rng.choice(opts); fx[k] = p
            cap = min(cap, p - 1)
        ps = fill(ons, ln["syl"], ln["scale"], lo, cap, cen, maxleap, rng, prev=prev, fixed=fx, sigma=sigma)
        if ps is None: continue
        if ft:
            for k in range(len(ps) - ft, len(ps)): ps[k] = ps[len(ps) - ft - 1]
        if runs(ps) > 3 + ft or (len(ps) >= 7 and len(set(ps)) < 3): continue
        if red(ln["syl"][ps.index(max(ps))]) and ps.index(max(ps)) not in fx: continue   # an aimed peak stands even on a weak word (THROUGH) -- a finding
        return [(o, d, p, x, ln["idx"]) for o, d, p, x in zip(ons, du2, ps, ln["syl"])]
    return None
def kidx(syl, word, nth=1):
    c = 0
    for i, x in enumerate(syl):
        if x[0] == word and x[2]:
            c += 1
            if c == nth: return i
    return None
def build_section(sec, rng, centers, lo, cap, maxleap, src=None, fixed_by_line=None, conds=None, sigma=2.0, after_pk=0, first_maxpk=3):
    lines = SECS[sec]; out = []; prev = None
    rh = section_rhythms(lines, rng, after_pk=after_pk, conds=conds, first_maxpk=first_maxpk)
    if rh is None: return None
    for i, ln in enumerate(lines):
        c = centers[i] if src is None else src
        nxt = (lines[i + 1]["at"] + rh[i + 1][0] - ln["at"]) if i + 1 < len(lines) else (ln["n"] - after_pk if after_pk else None)
        r = build_line(ln, rng, prev, c if callable(c) or isinstance(c, list) else (lambda j, n, c=c: c), lo,
                       cap(ln) if callable(cap) else cap, maxleap if ln["role"] != "aside" else 4, rh[i],
                       fixed=(fixed_by_line or {}).get(i), sigma=sigma, nxt_on=nxt)
        if r is None: return None
        out += r; prev = r[-1][2]
    return out
def shift(ns, sec_from, sec_to):
    d = STARTS[sec_to][1] - STARTS[sec_from][1]
    return [(o + d, du, p, x, i) for o, du, p, x, i in ns]
def retry(f, k=8):
    for _ in range(k):
        r = f()
        if r is not None: return r
    return None


def quarters(ns): return [(o / 4.0, d / 4.0, p) for o, d, p, *_ in ns]   # sixteenth slots
def contour(ns, unit=16):
    acc = collections.OrderedDict()
    for o, d, p, *_ in ns:
        k = int(o // unit); w, t = acc.get(k, (0.0, 0.0)); acc[k] = (w + d, t + d * p)
    seq = [t / w for w, t in acc.values()]
    if max(seq) - min(seq) < 2: return "flat"
    turns, dirn = 0, 0
    for x, y in zip(seq, seq[1:]):
        if abs(y - x) < 1.0: continue
        s_ = 1 if y > x else -1
        if dirn and s_ != dirn: turns += 1
        dirn = s_
    i = seq.index(max(seq))
    if 0 < i < len(seq) - 1 and turns <= 2: return "arch"
    if turns == 0: return "ascending" if seq[-1] > seq[0] else "descending"
    return "wave"


def copy_lines(ns_src, sec_src, sec_dst, idxs, dst_idx=None):
    out = []
    for k, i in enumerate(idxs):
        j = dst_idx[k] if dst_idx else i
        d = SECS[sec_dst][j]["at"] - SECS[sec_src][i]["at"]
        out += [(o + d, du, p, x, j) for o, du, p, x, li in ns_src if li == i]
    return out
# ---- v63's cell grammar (Module 27.20 as amended: the fit BY STRESS; the refrain kernel; the hook's own close) ----
PRIORS = {"ABCD": .27, "ABAC": .105, "AAAA": .10, "AABC": .096, "AAAB": .088, "ABAB": .084, "ABCA": .04, "AABA": .04, "ABBA": .03,
          "ABCC": .04, "ABAA": .03, "ABBC": .03, "AABB": .03, "ABCB": .02}
CHORUS_FORMS = {f: w for f, w in PRIORS.items() if f[0] == f[3]}
def draw(rng, forms): ks = list(forms); return rng.choices(ks, [forms[k] for k in ks])[0]
def sgn(x): return (x > 0) - (x < 0)
def stressed(ln): return [k for k, x in enumerate(ln["syl"]) if x[2]]
def spread(a, b, w):
    """w weak onsets strictly between a and b, evenly"""
    if w == 0: return []
    if b - a - 1 < w: return None
    return [a + round((t + 1) * (b - a) / (w + 1)) for t in range(w)]
def fit_by_stress(src_ln, src_sl, ln):
    """27.20 (v63): the cell's stressed onsets take the new line's stressed syllables in order (one fewer: the first anchors; one
    more: the longest gap split where a beat is free); the weak syllables between two stresses share the cell's weak onsets in that
    span when the counts match, an even split otherwise; a weak run before the first stress is the pickup, after the last the tail.
    Refused (None) when the stress counts differ by more than one or the weak syllables cannot fit."""
    S = stressed(src_ln); T = stressed(ln)
    if not S or not T or abs(len(S) - len(T)) > 1: return None
    anc = [src_sl[k] for k in S]; same = len(S) == len(T)
    if len(T) == len(S) - 1: anc = anc[:len(T)]
    elif len(T) == len(S) + 1:
        gaps = sorted([(anc[j + 1] - anc[j], j) for j in range(len(anc) - 1)], reverse=True)
        g, j = gaps[0] if gaps else (0, 0)
        if g < 4: return None
        mid = anc[j] + g // 2; mid -= mid % 2                       # on a beat
        if mid <= anc[j] or mid >= anc[j + 1]: return None
        anc = anc[:j + 1] + [mid] + anc[j + 1:]
    out = [None] * len(ln["syl"])
    for k, a in zip(T, anc): out[k] = a
    pre = T[0]                                                     # the pickup
    src_pre = src_sl[:S[0]]
    if same and len(src_pre) == pre: ps = src_pre
    else: ps = list(range(anc[0] - pre, anc[0]))
    if ps and ps[0] < -4: return None
    out[:pre] = ps
    for j in range(len(T) - 1):                                    # between two stresses
        w = T[j + 1] - T[j] - 1
        src_w = [src_sl[k] for k in range(S[j] + 1, S[j + 1])] if same else None
        ws = src_w if (src_w is not None and len(src_w) == w) else spread(anc[j], anc[j + 1], w)
        if ws is None: return None
        out[T[j] + 1:T[j + 1]] = ws
    t = len(ln["syl"]) - 1 - T[-1]                                 # the tail
    src_t = [src_sl[k] for k in range(S[-1] + 1, len(src_sl))] if same else None
    ts = src_t if (src_t is not None and len(src_t) == t) else list(range(anc[-1] + 1, anc[-1] + 1 + t))
    out[T[-1] + 1:] = ts
    if any(b <= a for a, b in zip(out, out[1:])) or out[-1] > ln["n"] - 2: return None
    return out
def letters(keys):
    seen = []
    for k in keys:
        if k not in seen: seen.append(k)
    return "".join("ABCDEFGH"[seen.index(k)] for k in keys)
def one_apart(a, b):
    """v64: the same stressed onsets with one added or dropped"""
    if abs(len(a) - len(b)) != 1: return False
    lo, hi = (a, b) if len(a) < len(b) else (b, a)
    return any(hi[:k] + hi[k + 1:] == lo for k in range(len(hi)))
def letters_prime(keys):
    out, seen = [], []
    for k in keys:
        if k in seen: out.append("ABCDEFGH"[seen.index(k)]); continue
        base = next((j for j, s_ in enumerate(seen) if one_apart(s_, k)), None)
        if base is not None: out.append("ABCDEFGH"[base] + "\u2032"); continue
        seen.append(k); out.append("ABCDEFGH"[len(seen) - 1])
    return "".join(out)
def forms_of(lines, rh):
    surface = letters([tuple(sl) for sl in rh])
    skel = []
    for ln, sl in zip(lines, rh):
        st = stressed(ln) or [0]; skel.append(tuple(sl[k] - sl[st[0]] for k in st))
    return surface, letters_prime(skel)
def prefix_slots(ln, rng, k0, m, tries=400):
    """the words before the refrain kernel: m onsets before the kernel's first onset k0, pickup to -3, strong-beat agreement"""
    best = None
    rng_pos = list(range(-3, k0))
    if len(rng_pos) < m: return None
    for _ in range(tries):
        sl = sorted(rng.sample(rng_pos, m))
        if m and sl[0] < -3: continue
        full = sl + [None] * (len(ln["syl"]) - m)
        ag, bad = agreement(dict(ln, syl=ln["syl"][:m]), sl) if m else (1.0, False)
        if not any(x[2] for x in ln["syl"][:m]) and not bad: ag = 1.0      # no stress to place: only the weak-on-strong test
        if bad or ag < 0.5: continue
        gaps = [b - a for a, b in zip(sl, sl[1:])] + ([k0 - sl[-1]] if m else [])
        if any(g > 3 for g in gaps): continue                       # the words before the kernel run into it
        sc = ag - 0.05 * sum(1 for x in sl if x < 0)
        if best is None or sc > best[0]: best = (sc, sl)
    return best[1] if best else None
def kernel_line(sec, i, rng, prev, kernel_rel, cap, center, raise_top=0):
    """v63 fix 3: a refrain line -- the kernel's onsets, durations AND pitches copied from the title line's cell; the words before
    walked strictly under the kernel's top"""
    ln = SECS[sec][i]; K = len(kernel_rel); m = len(ln["syl"]) - K
    k0 = kernel_rel[0][0]
    pre = prefix_slots(ln, rng, k0, m) if m else []
    if pre is None: return None
    top = max(p for _, _, p in kernel_rel)
    out = []
    if m:
        ons = [ln["at"] + x for x in pre]
        for _ in range(12):
            ps = fill(ons, ln["syl"][:m], ln["scale"], LO, top - 1, [center] * m, 7, rng, prev=prev)
            if ps is None: continue
            if abs(kernel_rel[0][2] - ps[-1]) > 7 or abs(kernel_rel[0][2] - ps[-1]) == 6: continue
            if runs(ps) > 3: continue
            break
        else: return None
        du = [b - a for a, b in zip(pre, pre[1:])] + [k0 - pre[-1]]
        du = [min(d, 2) if not ln["syl"][k][2] else d for k, d in enumerate(du)]
        out = [(o, d, p, x, i) for o, d, p, x in zip(ons, du, ps, ln["syl"][:m])]
    for k, (r, d, p) in enumerate(kernel_rel):
        if raise_top and p == top: p = p + raise_top
        out.append((ln["at"] + r, d, p, ln["syl"][m + k], i))
    if raise_top:                                                  # 21.7a: the feminine tail keeps its stress's pitch
        out = [(o, d, (out[-2][2] if k == len(out) - 1 else p), x, ii) for k, (o, d, p, x, ii) in enumerate(out)]
    return out
def build_cells(sec, rng, centers, lo, cap, maxleap, plan, tonic, fixed_by_line=None, conds=None, after_pk=0, first_maxpk=3,
                skip=(), log=None, fixed_rh=None):
    """the section's cells: each letter's first line walked; a repeated letter's line fitted BY STRESS to the first's cell, or,
    refused, re-walked with the letter's contour kept (logged); a new letter's rhythm differs from the cells built; line 2 open"""
    lines = SECS[sec]
    rh = section_rhythms(lines, rng, after_pk=after_pk, conds=conds, first_maxpk=first_maxpk)
    if rh is None: return None
    for i, sl in (fixed_rh or {}).items(): rh[i] = list(sl)
    first, cells, loc = {}, [], []
    for i, letter in enumerate(plan):
        if i in skip: cells.append(None); continue
        ln = lines[i]
        if letter in first:
            j = first[letter]
            f = fit_by_stress(lines[j], rh[j], ln)
            ok = f is not None
            if ok:
                ag, bad = agreement(ln, f); ok = not bad and ag >= 0.5 and (not conds or i not in conds or conds[i](f))
                if ok and i + 1 < len(lines) and f[-1] > ln["n"] - 2 - max(0, -rh[i + 1][0]): ok = False   # the run's port: a fitted cell must clear the next line's pickup
            if ok: rh[i] = f; loc.append((sec, i, f"fitted by stress to line {j + 1}"))
            else: loc.append((sec, i, f"fit to line {j + 1} refused; re-walked, contour kept"))
        else:
            first[letter] = i; tries = 0
            while tuple(rh[i]) in [c for c in cells if c] and tries < 20:
                r = rhythm(ln, rng, ln["n"] - 3, None, cond=(conds or {}).get(i)); tries += 1
                if r: rh[i] = r
        cells.append(tuple(rh[i]))
    out, prev, pitches = [], None, {}
    for i, ln in enumerate(lines):
        if i in skip: continue
        nxt = (lines[i + 1]["at"] + rh[i + 1][0] - ln["at"]) if i + 1 < len(lines) and (i + 1) not in skip else (ln["n"] - after_pk if after_pk else None)
        fx = dict((fixed_by_line or {}).get(i, {}))
        c = centers[i]; r = None
        for _ in range(10):
            r = build_line(ln, rng, prev, c if callable(c) or isinstance(c, list) else (lambda j_, n_, c=c: c), lo,
                           cap(ln) if callable(cap) else cap, maxleap, rh[i], fixed=fx, nxt_on=nxt)
            if r is None: continue
            ps = [n[2] for n in r]
            j = first.get(plan[i], i)
            if j != i and len(ps) >= 3 and j in pitches:              # a repeated letter: new pitches, the opening's direction kept
                q = pitches[j]
                if (sgn(ps[1] - ps[0]), sgn(ps[2] - ps[1])) != (sgn(q[1] - q[0]), sgn(q[2] - q[1])) or ps == q: r = None; continue
            if i == 1 and ps[-1] % 12 == tonic: r = None; continue     # the line before the midpoint stays open
            break
        if r is None: return None
        pitches[i] = [n[2] for n in r]
        out += r; prev = r[-1][2]
    sung = [rh[i] for i in range(len(lines)) if i not in skip]
    surf, skel = forms_of([lines[i] for i in range(len(lines)) if i not in skip], sung)
    if log is not None: log.extend(loc); log.append((sec, "forms", dict(drawn=plan, surface=surf, skeleton=skel)))
    return out, rh


CHORUSES = ("Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4")
HOOKS = ("Hook 1", "Hook 2", "Hook 3", "Outro")
TONIC = {"Verse 1": 3, "Verse 2": 3, "Pre 1": 3, "Pre 2": 3, "Breakdown": 3, "Chorus 1": 3}
FSECS = ("Chorus 3", "Chorus 4", "Hook 3", "Outro")
def sub_line(ln, start, k0):
    """the words after the title cell: a line of their own starting at `start` (slots), syllables k0.. of the line"""
    syl = ln["syl"][k0:]
    return dict(ln, syl=syl, at=ln["at"] + start, n=ln["n"] - start, commas={c - k0 for c in ln["commas"] if c >= k0}, nomin=True)
def cell_notes(ln, tr=0, ends=None):
    out = []
    for k, (o, d, p) in enumerate(CELL):
        if ends is not None and k == 2: d = min(d, max(1, ends - o))
        out.append((ln["at"] + o, d, p + tr, ln["syl"][k], ln["idx"]))
    return out
def cell_line(sec, i, rng, prev_after, cap, center, nxt_rel=None, tr=0, fixed_tail=None, tail_rh=None, tail_cond=None):
    """a 'five-oh-one' line: the cell, then the rest walked from beat 2's 'and' to beat 3 (slots 6-8)"""
    ln = SECS[sec][i]
    tl = sub_line(ln, 8, 3)
    nxt_sub = None if nxt_rel is None else nxt_rel - 8
    if tail_rh is None:
        mx = (nxt_sub - 3) if nxt_sub is not None else tl["n"] - 3
        rh = rhythm(tl, rng, mx, cond=tail_cond, maxpk=2)
        if rh is None: return None
    else: rh = list(tail_rh)
    r = build_line(tl, rng, CELL[2][2] + tr, lambda j, n: center, LO, cap, 7, rh, fixed=fixed_tail, nxt_on=nxt_sub)
    if r is None: return None
    first = r[0][0] - ln["at"]
    return cell_notes(ln, tr, ends=first) + r
def hook_line(sec, i, tr=0, hold=None):
    ln = SECS[sec][i]
    out = []
    for k, ((o, d), p) in enumerate(zip(HOOK_RH, HOOK_P)):
        if hold is not None and k == len(HOOK_RH) - 1: d = hold
        out.append((ln["at"] + o, d, p + tr, ln["syl"][k], ln["idx"]))
    return out
def transpose(ns, sec_from, sec_to, tr, idxs=None):
    out = []
    for o, d, p, x, li in ns:
        if idxs is not None and li not in idxs: continue
        dd = SECS[sec_to][li]["at"] - SECS[sec_from][li]["at"]
        out.append((o + dd, d, p + tr, x, li))
    return out
def generate(rng):
    out = {}; plans = {}; log = []
    def pk_of(ns, sec):
        st = STARTS[sec][1]; return max(0, st - min(n[0] for n in ns))
    # ---- the chorus (Eb): lines 1, 2, 4 open on the cell; line 3 walked ----
    def chorus():
        cb = rng.uniform(61.0, 62.5)
        L3 = SECS["Chorus 1"][2]
        rh3 = rhythm(L3, rng, L3["n"] - 2, maxpk=0)                 # line 4 opens on the downbeat: no pickup
        if rh3 is None: return None
        l1 = cell_line("Chorus 1", 0, rng, None, 66, cb, nxt_rel=32)
        if l1 is None: return None
        l2 = cell_line("Chorus 1", 1, rng, None, 66, cb - 0.5, nxt_rel=32 + rh3[0])
        if l2 is None: return None
        l3 = build_line(L3, rng, l2[-1][2], lambda j, n: cb + 1.2 * math.sin(j / max(1, n - 1) * math.pi), 55, 67, 7, rh3, nxt_on=32)
        if l3 is None: return None
        l4 = cell_line("Chorus 1", 3, rng, None, 65, cb - 1.0, nxt_rel=32, tail_cond=lambda sl: (sl[-1] + 8) % 4 == 0)
        if l4 is None: return None
        if abs(l3[-1][2] - 58) > 7 or abs(l1[-1][2] - 58) > 7 or abs(l2[-1][2] - 58) > 7: return None   # into the next cell's Bb3
        return l1 + l2 + l3 + l4
    Ch = retry(chorus, 20)
    if Ch is None: return None, "chorus"
    out["Chorus 1"] = Ch; out["Chorus 2"] = shift(Ch, "Chorus 1", "Chorus 2")
    out["Chorus 3"] = transpose(Ch, "Chorus 1", "Chorus 3", 2)
    plans["Chorus 1"] = "lines 1, 2 and 4 open on the title cell (Bb3-Eb4-G4, ONE on beat 2); line 3 walked; G4 the top"
    # ---- chorus 4: chorus 3's lines 1-3; line 4 the turn, HERE on Bb4 over Bb ----
    def last():
        c4 = transpose(Ch, "Chorus 1", "Chorus 4", 2, idxs=(0, 1, 2))
        l4 = cell_line("Chorus 4", 3, rng, None, 69, 64.0, nxt_rel=32, tr=2, fixed_tail={4: 70}, tail_rh=[-1, 0, 2, 3, 4])
        return None if l4 is None else c4 + l4
    C4 = retry(last, 20)
    if C4 is None: return None, "chorus 4"
    out["Chorus 4"] = C4; plans["Chorus 4"] = "chorus 3's lines 1-3; the turn: and you'll find me HERE, Bb4 over Bb (beat 4), held"
    # ---- the hooks and the outro: the chant ----
    for sec, tr in (("Hook 1", 0), ("Hook 2", 0), ("Hook 3", 2)):
        out[sec] = hook_line(sec, 0, tr) + hook_line(sec, 1, tr)
    out["Outro"] = hook_line("Outro", 0, 2, hold=15)
    plans["Hook 1"] = "the chant on a tresillo (3+3+2): Bb3 Eb4 x3 up to G4 on ONE (bar 2's downbeat)"
    # ---- the lift: the lead's question up to SAY (F4 over Bb); the gang's shout over C ----
    def lift():
        ln = SECS["Lift"][0]
        rh = rhythm(ln, rng, 24, cond=lambda sl: sl[-1] in (16, 20, 24), maxpk=4)
        if rh is None: return None
        r = build_line(ln, rng, None, lambda j, n: 59.0 + 5.0 * j / max(1, n - 1), 53, 65, 7, rh, fixed={-1: 65}, nxt_on=32)
        if r is None: return None
        g = SECS["Lift"][1]
        return r + [(g["at"] + o, d, p, g["syl"][k], 1) for k, (o, d, p) in enumerate(SHOUT)]
    Lf = retry(lift, 12)
    if Lf is None: return None, "lift"
    out["Lift"] = Lf; plans["Lift"] = "the question climbs to SAY on F4 over Bb; the gang shouts FIVE-OH-ONE on three hits over C (the pivot to F)"
    # ---- verses, pre-choruses, breakdown: the cell grammar ----
    for sec, nx, ctr, cap in (("Pre 1", "Chorus 1", 61.0, HIM["pre"]), ("Pre 2", "Chorus 2", 61.0, HIM["pre"]),
                              ("Verse 1", "Pre 1", 57.5, HIM["verse"]), ("Verse 2", "Pre 2", 57.5, HIM["verse"]),
                              ("Breakdown", "Lift", 56.5, HIM["breakdown"])):
        n_ = len(SECS[sec])
        d_ = draw(rng, PRIORS); pl = d_[:n_]
        apk = pk_of(out[nx], nx)
        if sec.startswith("Pre"):
            cens = [lambda j, m: ctr + 1.5 * j / max(1, m - 1), lambda j, m: ctr + 1.5 + 1.0 * math.sin(j / max(1, m - 1) * math.pi)]
        else:
            offs = [rng.choice([-1, 0, 0.5, 1]) for _ in range(n_)]
            cens = [lambda j, m, o=o, c=ctr: c + o + 0.8 * math.sin(j / max(1, m - 1) * math.pi) for o in offs]
        conds = {i: (lambda sl: sl[-1] in (20, 24, 28)) for i in range(n_)} if sec == "Breakdown" else None   # CLAP on beat 2, 3 or 4 of the line's second bar
        r = retry(lambda: build_cells(sec, rng, cens, HIM["lo"], cap, 7, pl, TONIC[sec], after_pk=apk, log=log, first_maxpk=4, conds=conds), 10)
        if r is None: return None, sec
        out[sec] = r[0]; plans[sec] = pl
    allz = sorted([(o, d, p, x, (s_, i), s_) for s_ in SINGS for o, d, p, x, i in out[s_]], key=lambda n: n[0])
    for j in range(len(allz) - 1):
        a, b = allz[j], allz[j + 1]
        if b[0] <= a[0]: return None, f"join:{a[5]}>{b[5]}"
        if a[4] != b[4] and a[0] + a[1] > b[0] - 2:
            nd = b[0] - 2 - a[0]
            if nd < 1: return None, f"join:{a[5]}>{b[5]}"
            allz[j] = (a[0], nd) + a[2:]
    for s_ in SINGS: out[s_] = [(o, d, p, x, k[1]) for o, d, p, x, k, ss in allz if ss == s_]
    out["plans"] = plans; out["cell_log"] = log
    return out, None

BY_CONSTRUCTION = ["the title cell (Bb3-Eb4-G4 / C4-F4-A4) on every 'five-oh-one' line (designed)", "the hook's tresillo chant (designed)",
                   "the gang's shout over C (designed)", "HERE on Bb4 over Bb (aimed)", "SAY on F4 over Bb (aimed)",
                   "the choruses in F transposed from the chorus in Eb (by construction)", "line 2 open (the plan)"]
LIMIT = {"Verse 1": "verse", "Verse 2": "verse", "Pre 1": "pre", "Pre 2": "pre", "Chorus 1": "chorus", "Chorus 2": "chorus", "Hook 1": "hook",
         "Hook 2": "hook", "Breakdown": "breakdown", "Lift": "lift", "Chorus 3": "chorusF", "Chorus 4": "chorusF", "Hook 3": "chorusF", "Outro": "chorusF"}
DESIGNED = {(s, i) for s in CHORUSES for i in (0, 1, 3)} | {(s, i) for s in HOOKS for i in (0, 1)} | {("Lift", 1)}
def fin_count(c):
    bad = []
    for s in SINGS:
        for ln in SECS[s]:
            ws = []
            for n in c[s]:
                if n[4] == ln["idx"] and (not ws or ws[-1][1] != n[3]): ws.append((n[0] - ln["at"], n[3]))
            if len(ws) == len(ln["syl"]) and not fin_ok(ln, [w[0] for w in ws]): bad.append((s, ln["idx"]))
    return bad
SLOT_S = 60.0 / QBPM / 4
def evaluate(c):
    fb = [b for b in fin_count(c) if b[0] not in ("Chorus 2", "Chorus 3")]
    if len(fb) > 2: return ("final-stress-offbeat", len(fb), "<= 2"), None
    for s in SINGS:
        for ln in SECS[s]:
            ns = [n for n in c[s] if n[4] == ln["idx"]]; ps = [n[2] for n in ns]
            lim = HIM[LIMIT[s]] + (1 if (s, ln["idx"]) == ("Chorus 4", 3) else 0)
            if max(ps) > lim or min(ps) < HIM["lo"]: return ("range", (s, ln["idx"], max(ps)), lim), None
            iv = intervals(quarters(ns))
            if iv and max(abs(x) for x in iv) > 7: return ("leap", (s, ln["idx"]), ""), None
            if any(abs(x) == 6 for x in iv): return ("tritone", (s, ln["idx"]), "death"), None
            if (s, ln["idx"]) not in DESIGNED and red(next(n for n in ns if n[2] == max(ps))[3]): return ("floor:reduced_peak", (s, ln["idx"]), ""), None
            ft = fem_tail([n[3] for n in ns])
            if ft:
                for n in ns[-ft:]:
                    if n[1] > 2 or n[2] != ns[-ft - 1][2] or strong_abs(n[0]): return ("feminine:tail", (s, ln["idx"]), "21.7a"), None
    top = [n for s in SINGS for n in c[s] if n[2] > 69]
    if len(top) != 1 or top[0][2] != 70 or top[0][3][0] != "here": return ("Bb4 once", len(top), "on HERE"), None
    V = c["Verse 1"]
    if contour(V) not in ("flat", "wave", "arch", "descending"): return ("verse:contour", contour(V), "flat/wave"), None
    srt = sorted([n for s in SINGS for n in c[s]], key=lambda n: n[0]); run0 = srt[0][0]; best = 0
    for a, b in zip(srt, srt[1:] + [None]):
        if b is None or b[0] - (a[0] + a[1]) >= 2:               # a breath: an eighth's rest
            best = max(best, a[0] + a[1] - run0)
            if b is not None: run0 = b[0]
    if best * SLOT_S > 4.6: return ("breath", round(best * SLOT_S, 2), "<= 4.6 s"), None
    allw = [n for s in SINGS for n in c[s]]
    strong = [n for n in allw if strong_abs(n[0])]
    al = sum(1 for n in strong if n[3][2]) / len(strong)
    if al < 0.444: return ("floor:alignment", round(al, 3), ">= 0.444"), None
    H = c["Chorus 1"]
    qv = quarters(V); qh = quarters(H); off = qv[-1][0] + 8 - qh[0][0]
    tune = qv + [(o + off, d, p) for o, d, p in qh]
    beta = beta_pitch(tune)
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral", beta and round(beta, 3), "p05-p95"), None
    cmp_, _ = cmp_score(tune, 4, TCAL)
    if cmp_ < C["cmp"]["p05"]: return ("cmp", round(cmp_, 3), ">= p05"), None
    mh, _, _ = m_horizon(qh, qv)
    if mh < C["mh"]["p05"]: return ("memory", round(mh, 3), ">= p05"), None
    bits = PPMM.bits(PPM.symbols(tune, TCAL))[len(V):]
    hp = [n[2] for n in H]
    ic, icd = ic_profile(bits, hp.index(max(hp)))
    if ic < C["ic"]["p05"]: return ("surprisal", round(ic, 3), ">= p05"), None
    fv = (feature_vec(qh, TCAL, 4) - MU) / SD
    dist = np.sort(np.sqrt(((ZREF - fv) ** 2).sum(1)))[:10].mean()
    real = sum(1 for x in REAL_KNN if x >= dist) / len(REAL_KNN)
    if real < C["realness"]["p05"]: return ("realness", round(real, 3), ">= p05"), None
    S_sp = s_spectral(beta, C["beta"]["p25"], C["beta"]["p75"])
    lift = np.median(hp) - np.median([n[2] for n in V])
    fit_items = [contour(H) in ("arch", "ascending", "wave", "descending"), 1.0 if lift >= 4 else (0.5 if lift >= 2 else 0.0),
                 contour(V) in ("flat", "wave"), max(n[2] for n in V) <= HIM["verse"]]
    fitv = float(np.mean([float(x) for x in fit_items]))
    comp = (0.15 * S_sp + 0.15 * min(1.0, cmp_ / 0.6) + 0.10 * min(1, mh) + 0.15 * fitv + 0.15 * ic +
            0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5)
    return None, dict(composite=round(comp, 4), CMP=cmp_, M_horizon=mh, IC=ic, realness=real, fit=fitv, lift=float(lift), align=al,
                      beta=beta, longest_s=round(best * SLOT_S, 2), offbeat_endings=len(fb))

def fingerprint(c):
    return hashlib.sha1(json.dumps([[n[0], n[1], n[2]] for k in SINGS for n in c[k]]).encode()).hexdigest()[:12]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    rng = random.Random(20261107)
    made, deaths, alive, tries, unb = 0, collections.Counter(), [], 0, 0
    while made < N and tries < N * 40:
        tries += 1
        c, err = generate(rng)
        if err: deaths["generate:" + err] += 1; unb += 1; continue
        made += 1
        cert, meas = evaluate(c)
        if cert: deaths[cert[0]] += 1; continue
        c["meas"] = meas; c["fp"] = fingerprint(c); alive.append(c)
    alive.sort(key=lambda c: -c["meas"]["composite"])
    order_fp = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    rate = len(alive) / max(1, made)
    print(f"built {made} (attempts {tries}, unbuildable {unb}), survivors {len(alive)} ({100*rate:.1f}% of built, {100*len(alive)/max(1,tries):.1f}% of attempts), order frozen {order_fp}")
    for k, v in deaths.most_common(20): print(f"   {v:6d}  {k}")
    for c in alive[:6]:
        m = c["meas"]
        print(f"{c['fp']} comp {m['composite']:.3f} real {m['realness']:.2f} IC {m['IC']:.2f} CMP {m['CMP']:.2f} M {m['M_horizon']:.2f} fit {m['fit']:.2f} lift {m['lift']:+.1f}")
    pickle.dump(dict(by_construction=BY_CONSTRUCTION, alive=alive[:60], deaths=deaths, made=made, tries=tries, order_fp=order_fp, rate=rate, survivors=len(alive)), open("/home/claude/p26/melody_result.pkl", "wb"))
