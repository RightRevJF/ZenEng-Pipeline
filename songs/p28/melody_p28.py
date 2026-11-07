"""Module 27 melody search for 'Tinted Glass' (ZenEng v64 port, v65 fixes as ports). A duet that never sings together: him (baritone)
and her (female, his chorus tune an octave up). Slow-burn soul in 6/8 at dotted-q = 54; eighth slots. Eb major throughout, the verses
leaning on C minor; no key change anywhere (the writer's choice A).
  * Verses and bridge: a line in four bars (24 eighths; his choice A at the room). Choruses: a line in two bars (12 eighths).
  * Him (11.2 bass/baritone row): C3-Bb3 in Eb (B2 is outside the key), C4 once: 'FOG' in his last chorus.
    Her (11.2 female row): Bb3-Ab4 in the verses; the chorus his tune +12 (Eb4-Bb4), C5 once: 'FOG' in her last chorus.
  * The chorus: GLASS aimed on Ab3 over Ab (line 1's second downbeat); the chorus's last word on F3 over Bb (line 4's second downbeat),
    a half cadence that never resolves. Choruses 2-4 refit chorus 1's tune by stress to their own words.
  * v63/v64 cell grammar per verse; line 2 open.
  Calibration: pop major read in Eb (TCAL 3); verse 1 + chorus 1; CMP on the chorus."""
import sys, math, json, pickle, random, hashlib, collections
import numpy as np
sys.path[:0] = ["/home/claude/p28", "/home/claude/carol", "/home/claude/pop"]
import engine_p28 as E, phrasestress48 as PS; PS.install(E); E.install_patches()
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec, syncopation, intervals
import lyric as L
syllables = E.syllables
TCAL = 3
EB = {3, 5, 7, 8, 10, 0, 2}
CH = {"Eb": {3, 7, 10}, "Ab": {8, 0, 3}, "Bb": {10, 2, 5}, "Cm": {0, 3, 7}, "Fm": {5, 8, 0}, "Gm": {7, 10, 2}}
HIM = dict(lo=48, verse=58, chorus=58, last=60)
HER = dict(lo=58, verse=68, chorus=70, last=72)
LO = 48
METER = {"6/8": dict(bar=6, beats=[0, 3], strong=[0, 3])}
QBPM = 81
LATER_PK = 3
CAL = json.load(open("/home/claude/pop/pop_calibration.json")); C = CAL["cal"]
MU, SD = np.array(CAL["mu"]), np.array(CAL["sd"]); ZREF = np.array(CAL["Z"]); REAL_KNN = CAL["real_knn"]
PPMM = pickle.load(open("/home/claude/pop/pop_ppm.pkl", "rb"))
IM = pickle.load(open("/home/claude/pop/pop_intervals.pkl", "rb"))
VERSE = [["Cm", "Cm", "Ab", "Ab"], ["Eb", "Eb", "Bb", "Bb"], ["Cm", "Cm", "Ab", "Ab"], ["Fm", "Fm", "Bb", "Bb"]]
CHORUS = [["Eb", "Ab"], ["Eb", "Bb"], ["Cm", "Ab"], ["Fm", "Bb"]]
BRIDGE = [["Ab", "Ab", "Bb", "Bb"], ["Gm", "Gm", "Cm", "Cm"], ["Ab", "Ab", "Bb", "Bb"], ["Fm", "Fm", "Bb", "Bb"]]
INTRO = ["Cm", "Ab", "Eb", "Bb"]
OUTRO = ["Ab", "Bb", "Eb", "Eb"]
SECD = dict(L.SECTIONS)
FORM = [("Intro", "6/8", EB, None, INTRO)]
for _s, _ls in L.SECTIONS:
    FORM.append((_s, "6/8", EB, _ls, CHORUS if _s.startswith("Chorus") else (BRIDGE if _s == "Bridge" else VERSE)))
FORM.append(("Outro", "6/8", EB, None, OUTRO))
SINGER = L.SINGER
def singer_of(sec, i): s = SINGER[sec]; return s[i] if isinstance(s, list) else s
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
                              commas=None, singer=singer_of(sec, i)))
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
    for _ln in SECS[_s]: _ln["nomin"] = _ln["n"] < 24        # four-bar lines reach their third bar; two-bar lines no minimum
def iv_weight(prev_iv, prev_deg, iv):
    c = IM.get((max(-7, min(7, prev_iv)), prev_deg))
    if not c: return 0.05
    return (c.get(iv, 0) + 0.2) / (sum(c.values()) + 5)
def red(x): return x[1].endswith("0") or not x[2]
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
            elif r < p_stretch + 0.2 and ln["meter"] in ("4/4", "3/4", "5/4"): step = 4
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
            if n >= 24: mx, mn = min(mx, 12), 9                       # song 28: a four-bar line sung in its first two and a half bars; the rest is the answer

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
    if n >= 24:                                                  # song 28: a four-bar line breathes inside; its last note holds a bar at most (the answer follows)
        d = [min(x, 3) if k < len(d) - 1 else min(x, 6) for k, x in enumerate(d)]
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


def quarters(ns): return [(o / 2.0, d / 2.0, p) for o, d, p, *_ in ns]   # eighth slots
def contour(ns, unit=10):
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
def rng_of(singer, sec):
    R = HIM if singer == "him" else HER
    return R["lo"], R["chorus" if sec.startswith("Chorus") else "verse"]
def refit(src_ns, sec_src, sec_dst, rng, transpose=0, after_pk=0, designed=None):
    """a later chorus: chorus 1's tune refit by stress to its own words (27.20's fit), each syllable taking the pitch the source
    sounds at its onset; the same words copy outright. Built from the last line back, so each line clears the next one's pickup"""
    lines = SECS[sec_dst]; res = [None] * len(lines); nxt_pk = after_pk
    for i in range(len(lines) - 1, -1, -1):
        if designed and i in designed: res[i] = []; nxt_pk = designed[i]; continue     # a designed line: built after, its pickup known
        ln = lines[i]; src_ln = SECS[sec_src][i]
        sn = [n for n in src_ns if n[4] == i]
        rel = [(o - src_ln["at"], d, p) for o, d, p, x, _ in sn]
        lim = ln["n"] - 1 - nxt_pk
        if ln["line"] == src_ln["line"]:
            ns = [(ln["at"] + r, d, p + transpose, x, i) for (r, d, p), x in zip(rel, ln["syl"])]
            if rel[-1][0] + rel[-1][1] > lim: ns[-1] = ns[-1][:1] + (max(1, lim - rel[-1][0]),) + ns[-1][2:]
            if rel[-1][0] >= lim: return None
            res[i] = ns; nxt_pk = max(0, -rel[0][0]); continue
        src_sl = [r for r, _, _ in rel]
        prev_n = len(lines[i - 1]["syl"]) if i > 0 else 0
        mpk = 2 if prev_n >= 9 else (5 if 0 < prev_n <= 7 else 3)      # after a long line a short pickup; after a short one, a long pickup
        if i > 0:                                                        # never into the source's previous line's held last note (GLASS keeps its length)
            pl = [n for n in src_ns if n[4] == i - 1][-1]; pend = pl[0] + pl[1] - SECS[sec_src][i - 1]["at"]
            mpk = max(1, min(mpk, SECS[sec_src][i - 1]["n"] - pend - 1))
        f = fit_by_stress(src_ln, src_sl, ln)
        if f is None or agreement(ln, f)[1] or f[-1] > lim - 1 or f[0] < -mpk:
            e = max(r for r, x in zip(src_sl, src_ln["syl"]) if x[2])           # the last stress where the source's last stress was
            f = rhythm(ln, rng, lim - 1, cond=lambda sl, e=e: max(s_ for s_, x in zip(sl, ln["syl"]) if x[2]) in (e, e + 3), tries=400, maxpk=mpk)
            if f is None: f = rhythm(ln, rng, lim - 1, cond=lambda sl: max(s_ for s_, x in zip(sl, ln["syl"]) if x[2]) % 3 == 0, tries=600, maxpk=mpk)
            if f is None: return None
        du = durs(ln, f, ln["n"] - nxt_pk)
        if du is None: return None
        ln["_lim"] = ln["n"] - 2 - nxt_pk
        f, du = apply_tail(ln, f, du)
        if f is None: return None
        ps = []
        for s_ in f:
            cand = [p for r, _, p in rel if r <= s_]
            ps.append((cand[-1] if cand else rel[0][2]) + transpose)
        ft = fem_tail(ln["syl"])
        if ft:
            for k in range(len(ps) - ft, len(ps)): ps[k] = ps[len(ps) - ft - 1]
        res[i] = [(ln["at"] + s_, d, p, x, i) for s_, d, p, x in zip(f, du, ps, ln["syl"])]
        nxt_pk = max(0, -f[0])
    return [n for r in res for n in r]
def generate(rng):
    out = {}; plans = {}; log = []
    def pk_of(ns, sec):
        st = STARTS[sec][1]; return max(0, st - min(n[0] for n in ns))
    # ---- chorus 1 (him): GLASS on Ab3 over Ab; the last word on F3 over Bb ----
    drawn = draw(rng, PRIORS)
    if drawn[3] == drawn[0]: drawn = drawn[:3] + "D"            # the last line lands on its own aimed note (F3): a letter of its own
    def chorus():
        rb = rng.uniform(53.5, 55.5)
        cens = [lambda j, n: rb + 1.0 * math.sin(j / max(1, n - 1) * math.pi), lambda j, n: rb + 0.5, lambda j, n: rb + 1.0 * j / max(1, n - 1),
                lambda j, n: rb - 1.5]
        return build_cells("Chorus 1", rng, cens, 51, HIM["chorus"], 7, drawn, 3,
                           fixed_by_line={0: {-1: 56}, 3: {-1: 53}}, first_maxpk=3,
                           conds={0: lambda sl: sl[-1] == 6, 3: lambda sl: sl[-1] == 6}, log=log, after_pk=0)
    r = retry(chorus, 12)
    if r is None: return None, "chorus"
    C1 = r[0]
    plans["Chorus 1"] = f"{drawn}; GLASS on Ab3 over Ab, the last word on F3 over Bb (aimed)"
    out["Chorus 1"] = C1
    C2 = refit(C1, "Chorus 1", "Chorus 2", rng, 12, after_pk=3)
    if C2 is None: return None, "chorus 2 refit"
    out["Chorus 2"] = C2
    C3 = refit(C1, "Chorus 1", "Chorus 3", rng, 0, after_pk=pk_of(C1, "Chorus 1"), designed={2: 2})
    if C3 is None: return None, "chorus 3 refit"
    ln2 = SECS["Chorus 3"][2]; src2 = SECS["Chorus 1"][2]                # the turn's line, designed: I still | FOG (C4, the downbeat) the window on your | STREET
    rel2 = [(o - src2["at"], p) for o, d, p, x, li in C1 if li == 2]
    sl2 = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
    du2 = durs(ln2, sl2, min(n[0] for n in C3 if n[4] == 3) - ln2["at"])
    if du2 is None: return None, "chorus 3:FOG line"
    ps2 = []
    for s_ in sl2:
        cand = [p for r_, p in rel2 if r_ <= s_]; ps2.append(cand[-1] if cand else rel2[0][1])
    ps2[2] = 60; ps2[1] = 55                                            # STILL on G3, a step up to the leap: FOG on C4
    C3 = C3 + [(ln2["at"] + s_, d, p, x, 2) for s_, d, p, x in zip(sl2, du2, ps2, ln2["syl"])]
    C3.sort(key=lambda n: n[0])
    l2 = [n[2] for n in C3 if n[4] == 2]
    if any(abs(b - a) > 7 or abs(b - a) == 6 for a, b in zip(l2, l2[1:])): return None, "chorus 3:FOG reach"
    out["Chorus 3"] = C3
    out["Chorus 4"] = [(o + STARTS["Chorus 4"][1] - STARTS["Chorus 3"][1], d, p + 12, x, li) for o, d, p, x, li in C3]
    plans["Chorus 2"] = "chorus 1's tune, an octave up, refit by stress to its words"
    plans["Chorus 3"] = "chorus 1's tune refit to its words; FOG raised to C4"
    plans["Chorus 4"] = "chorus 3 an octave up (FOG on C5)"
    # ---- the verses and the bridge, built from the end ----
    order = [("Verse 6", "Chorus 3"), ("Verse 5", "Verse 6"), ("Bridge", "Verse 5"), ("Verse 4", "Chorus 2"), ("Verse 3", "Verse 4"),
             ("Verse 2", "Chorus 1"), ("Verse 1", "Verse 2")]
    for sec, nx in order:
        apk = pk_of(out[nx], nx)
        if sec == "Bridge":
            lines = SECS[sec]
            rh = section_rhythms(lines, rng, after_pk=apk, first_maxpk=3)
            if rh is None: return None, "bridge:rhythm"
            ns, prev = [], None
            for i, ln in enumerate(lines):
                lo, cap = rng_of(ln["singer"], sec)
                c = rng.uniform(lo + 3.5, lo + 5.5)
                nxt = (lines[i + 1]["at"] + rh[i + 1][0] - ln["at"]) if i + 1 < len(lines) else ln["n"] - apk
                rr = None
                for _ in range(10):
                    rr = build_line(ln, rng, None, (lambda j, n, c=c: c + 0.8 * math.sin(j / max(1, n - 1) * math.pi)), lo, cap, 7, rh[i], nxt_on=nxt)
                    if rr: break
                if rr is None: return None, "bridge"
                ns += rr
            out[sec] = ns; plans[sec] = "lines traded, her/him/her/him; each in its own register"
            continue
        sg = SECS[sec][0]["singer"]; lo, cap = rng_of(sg, sec)
        n_ = len(SECS[sec]); pl = draw(rng, PRIORS)[:n_]
        vb = rng.uniform(lo + 3.0, lo + 5.0)
        offs = [rng.choice([-1, 0, 0.5, 1]) for _ in range(n_)]
        cens = [lambda j, m, o=o: vb + o + 0.8 * math.sin(j / max(1, m - 1) * math.pi) for o in offs]
        rr = retry(lambda: build_cells(sec, rng, cens, lo, cap, 7, pl, 3, after_pk=apk, log=log, first_maxpk=3), 10)
        if rr is None: return None, sec
        out[sec] = rr[0]; plans[sec] = pl
    allz = sorted([(o, d, p, x, (s_, i), s_) for s_ in SINGS for o, d, p, x, i in out[s_]], key=lambda n: n[0])
    for j in range(len(allz) - 1):
        a, b = allz[j], allz[j + 1]
        if b[0] <= a[0]: return None, f"join:{a[5]}>{b[5]}"
        if a[4] != b[4] and a[0] + a[1] > b[0] - 1:
            nd = b[0] - 1 - a[0]
            if nd < 1: return None, f"join:{a[5]}>{b[5]}"
            allz[j] = (a[0], nd) + a[2:]
    for s_ in SINGS: out[s_] = [(o, d, p, x, k_[1]) for o, d, p, x, k_, ss in allz if ss == s_]
    out["plans"] = plans; out["cell_log"] = log
    return out, None

BY_CONSTRUCTION = ["GLASS on Ab3 over Ab (aimed)", "the chorus's last word on F3 over Bb (aimed)", "choruses 2-4 refit from chorus 1 (by construction)",
                   "her choruses an octave above his (by construction)", "the turn's line designed: FOG on the downbeat, C4 / C5 in the last choruses (by construction)", "line 2 open (the plan)"]
DESIGNED = {("Chorus 3", 2), ("Chorus 4", 2)}
def fin_count(c):
    bad = []
    for s in SINGS:
        for ln in SECS[s]:
            ws = []
            for n in c[s]:
                if n[4] == ln["idx"] and (not ws or ws[-1][1] != n[3]): ws.append((n[0] - ln["at"], n[3]))
            if len(ws) == len(ln["syl"]) and not fin_ok(ln, [w[0] for w in ws]): bad.append((s, ln["idx"]))
    return bad
SLOT_S = 60.0 / 54 / 3
BREATH_S = 7.5                         # the run's port of fix 47: a four-bar line sung in two and a half bars plus its held last note (a finding: the 6 s ceiling is short for a slow 6/8 ballad)
def evaluate(c):
    fb = [b for b in fin_count(c) if b[0] not in ("Chorus 2", "Chorus 3", "Chorus 4")]
    if len(fb) > 3: return ("final-stress-offbeat", len(fb), "<= 3"), None
    for s in SINGS:
        for ln in SECS[s]:
            ns = [n for n in c[s] if n[4] == ln["idx"]]; ps = [n[2] for n in ns]
            lo, lim = rng_of(ln["singer"], s)
            if (s, ln["idx"]) in DESIGNED: lim += 2
            if max(ps) > lim or min(ps) < lo: return ("range", (s, ln["idx"], min(ps), max(ps)), (lo, lim)), None
            iv = intervals(quarters(ns))
            if iv and max(abs(x) for x in iv) > 7: return ("leap", (s, ln["idx"]), ""), None
            if any(abs(x) == 6 for x in iv): return ("tritone", (s, ln["idx"]), "death"), None
            if (s, ln["idx"]) not in DESIGNED and s == "Chorus 1" or s.startswith(("Verse", "Bridge")):
                if red(next(n for n in ns if n[2] == max(ps))[3]): return ("floor:reduced_peak", (s, ln["idx"]), ""), None
            ft = fem_tail([n[3] for n in ns])
            if ft:
                for n in ns[-ft:]:
                    if n[1] > 1 or n[2] != ns[-ft - 1][2] or strong_abs(n[0]): return ("feminine:tail", (s, ln["idx"]), "21.7a"), None
    him = [n for s in SINGS for ln in SECS[s] for n in c[s] if n[4] == ln["idx"] and ln["singer"] == "him"]
    her = [n for s in SINGS for ln in SECS[s] for n in c[s] if n[4] == ln["idx"] and ln["singer"] == "her"]
    if [n[3][0] for n in him if n[2] >= 60] != ["fog"] or [n[3][0] for n in her if n[2] >= 72] != ["fog"]: return ("tops once", "", "FOG"), None
    V = c["Verse 1"]
    if contour(V, 12) not in ("flat", "wave", "arch", "descending"): return ("verse:contour", contour(V, 12), "flat/wave"), None
    for who in (him, her):
        srt = sorted(who, key=lambda n: n[0]); run0 = srt[0][0]; best = 0
        for a, b in zip(srt, srt[1:] + [None]):
            if b is None or b[0] - (a[0] + a[1]) >= 1:
                best = max(best, a[0] + a[1] - run0)
                if b is not None: run0 = b[0]
        if best * SLOT_S > BREATH_S: return ("breath", round(best * SLOT_S, 2), f"<= {BREATH_S:.2f} s"), None
    allw = him + her
    strong = [n for n in allw if strong_abs(n[0])]
    al = sum(1 for n in strong if n[3][2]) / len(strong)
    if al < 0.444: return ("floor:alignment", round(al, 3), ">= 0.444"), None
    H = c["Chorus 1"]
    qv = quarters(V); qh = quarters(H); off = qv[-1][0] + 6 - qh[0][0]
    tune = qv + [(o + off, d, p) for o, d, p in qh]
    beta = beta_pitch(tune)
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral", beta and round(beta, 3), "p05-p95"), None
    cmp_, _ = cmp_score(qh, 4, TCAL)
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
    fit_items = [contour(H, 12) in ("arch", "ascending", "wave", "descending"), 1.0 if lift >= 4 else (0.5 if lift >= 2 else 0.0),
                 contour(V, 12) in ("flat", "wave"), max(n[2] for n in V) <= HIM["verse"]]
    fitv = float(np.mean([float(x) for x in fit_items]))
    comp = (0.15 * S_sp + 0.15 * min(1.0, cmp_ / 0.6) + 0.10 * min(1, mh) + 0.15 * fitv + 0.15 * ic +
            0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5)
    return None, dict(composite=round(comp, 4), CMP=cmp_, M_horizon=mh, IC=ic, realness=real, fit=fitv, lift=float(lift), align=al,
                      beta=beta, longest_s=round(best * SLOT_S, 2), offbeat_endings=len(fb))

def fingerprint(c):
    return hashlib.sha1(json.dumps([[n[0], n[1], n[2]] for k in SINGS for n in c[k]]).encode()).hexdigest()[:12]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    rng = random.Random(20261107 + 28)
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
    pickle.dump(dict(by_construction=BY_CONSTRUCTION, alive=alive[:60], deaths=deaths, made=made, tries=tries, order_fp=order_fp, rate=rate, survivors=len(alive)), open("/home/claude/p28/melody_result.pkl", "wb"))
