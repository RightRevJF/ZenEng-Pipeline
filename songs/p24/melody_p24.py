"""Module 27 melody search for 'The Song You Sang Me' (ZenEng v64 port; one tenor and one guitar; 3/4 at q = 76, a line four bars =
24 eighths). Key F major throughout (the guitar capo 3, D shapes).
  * Singer (the run's tenor row; v64 11.2 has none): D3-A4, Bb4 once. Verses low and close (D3-D4); the lullaby (the chorus) up to A4.
  * The refrain first: 'it's ME. I'm your SON.' -- designed and copied whole into every verse (the v63 refrain kernel): ME on C4 over
    C, held; SON on F3, the tonic, over F, held to the line's end. Verse 4's 'SONG' takes the same notes.
  * The chorus's cells: 'go to SLEEP, I've got the DARK' -- SLEEP on bar 1's downbeat (Bb), DARK on A4 over F, bar 3, held;
    'and if you WAKE' -- WAKE on F4 over Bb; in the final chorus on Bb4 (the allowance, once); 'till you know you're HERE' on F4 over
    F, held. The chorus's other notes stay under A4.
  * v63/v64 cell grammar per verse (drawn / surface / skeleton, A'); line 2 open (not on F).
  Calibration: pop major, read in F (TCAL 5) on verse 1 and the chorus."""
import sys, math, json, pickle, random, hashlib, collections
import numpy as np
sys.path[:0] = ["/home/claude/p24", "/home/claude/carol", "/home/claude/pop"]
import engine_p24 as E, phrasestress48 as PS; PS.install(E); E.install_patches()
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec, syncopation, intervals
import lyric as L
syllables = E.syllables
TCAL = 5
FM = {5, 7, 9, 10, 0, 2, 4}
CH = {"F": {5, 9, 0}, "Bb": {10, 2, 5}, "C": {0, 4, 7}, "Dm": {2, 5, 9}, "Gm": {7, 10, 2}, "Am": {9, 0, 4}}
HIM = dict(lo=50, verse=62, chorus=67, dark=69, final=70)
LO = 50
METER = {"3/4": dict(bar=6, beats=[0, 2, 4], strong=[0])}
QBPM = 76
CAL = json.load(open("/home/claude/pop/pop_calibration.json")); C = CAL["cal"]
MU, SD = np.array(CAL["mu"]), np.array(CAL["sd"]); ZREF = np.array(CAL["Z"]); REAL_KNN = CAL["real_knn"]
PPMM = pickle.load(open("/home/claude/pop/pop_ppm.pkl", "rb"))
IM = pickle.load(open("/home/claude/pop/pop_intervals.pkl", "rb"))
def iv_weight(prev_iv, prev_deg, iv):
    c = IM.get((max(-7, min(7, prev_iv)), prev_deg))
    if not c: return 0.05
    return (c.get(iv, 0) + 0.2) / (sum(c.values()) + 5)
def red(x): return x[1].endswith("0") or not x[2]
VS = [["F", "F", "Bb", "F"], ["Dm", "Dm", "Bb", "C"], ["F", "Am", "Bb", "Bb"], ["C", "C", "F", "F"]]     # the refrain over C -> F
CHL = [["Bb", "Bb", "F", "F"], ["Gm", "Gm", "C", "C"], ["Bb", "Bb", "F", "Dm"], ["Gm", "C", "F", "F"]]  # the lullaby
LULL = ["Bb", "Bb", "F", "F", "Gm", "Gm", "C", "C"]
FORM = [
    ("Intro", "3/4", FM, None, LULL),
    ("Verse 1", "3/4", FM, L.V1, VS),
    ("Verse 2", "3/4", FM, L.V2, VS),
    ("Chorus 1", "3/4", FM, L.CHORUS, CHL),
    ("Verse 3", "3/4", FM, L.V3, VS),
    ("Verse 4", "3/4", FM, L.V4, VS),
    ("Chorus 2", "3/4", FM, L.CHORUS, CHL),
    ("Outro", "3/4", FM, None, ["Bb", "Bb", "F", "Dm", "Gm", "C", "F", "F"]),
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
    for _ln in SECS[_s]: _ln["nomin"] = False      # a four-bar waltz line reaches its third bar (the last syllable at slot 15 or later)
for _s in SECS:                                     # designed cells (the refrain, the chorus's lines 1, 3, 4) and short lines are exempt
    for _ln in SECS[_s]:
        if _ln["role"] == "refrain" or _s.startswith("Chorus") and _ln["idx"] != 1 or len(_ln["syl"]) < 9: _ln["nomin"] = True
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
        if st and i < len(syl) - 1 and pos in beats:
            r = rng.random()
            if r < p_stretch: step = 2
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
def rhythm(ln, rng, maxslot, minslot=None, cond=None, tries=200, maxpk=3):
    pool = {}
    for _ in range(tries):
        pk = rng.choice(list(range(0, maxpk + 1)))
        sl = walk(ln, rng, pk)
        if sl[-1] > maxslot or (minslot is not None and sl[-1] < minslot): continue
        ag, bad = agreement(ln, sl)
        if bad or ag < 0.5: continue
        if cond and not cond(sl): continue
        pool[tuple(sl)] = ag
    if not pool: return None
    top = max(pool.values()); ok = [list(k) for k, v in pool.items() if v >= top - 0.2]
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
            mx = n - 2 - nxt if nxt else n - 3
            mn = n - 9 if n >= 24 and not ln.get("nomin") else None

            sl = rhythm(ln, rng, mx, mn, cond=(conds or {}).get(i), maxpk=first_maxpk if i == 0 else 3)
            if sl is None: ok = False; break
            out[i] = sl; nxt = max(0, -sl[0])
        if ok: return out
    return None
def durs(ln, sl, nxt_on=None):
    syl = ln["syl"]; n = ln["n"]
    end = n - 1 if nxt_on is None else min(n - 1, nxt_on - 1)
    d = [b - a for a, b in zip(sl, sl[1:])] + [max(1, end - sl[-1])]
    for k, x in enumerate(syl):
        if not x[2] and d[k] > 2 and not (k == len(d) - 1 and (sl[k] % METER[ln["meter"]]["bar"]) == 0): d[k] = 2 if k < len(d) - 1 else min(d[k], 2)   # the run's port: a line-final syllable on a downbeat holds, stressed or not
    for k in ln["commas"]:
        if k < len(d) - 1: d[k] = min(d[k], sl[k + 1] - sl[k] - 1)
    return d if min(d) >= 1 else None
def apply_tail(ln, sl, du):
    """21.7a: the feminine tail repeats its stress's pitch (set in the fill), an eighth, never on a beat, on the last eighth
    before the bar line where it fits"""
    ft = fem_tail(ln["syl"])
    if not ft: return sl, du
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
        if red(ln["syl"][ps.index(max(ps))]): continue
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


def quarters(ns): return [(o / 2.0, d / 2.0, p) for o, d, p, *_ in ns]
def contour(ns, unit=8):
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
    if ps and ps[0] < -3: return None
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


HOOKY = ("Chorus 1", "Chorus 2")
TONIC = {"Verse 1": 5, "Verse 2": 5, "Verse 3": 5, "Verse 4": 5, "Chorus 1": 5}
R0 = [(-2, -1, 0, 4, 6, 10, 12), (-2, -1, 0, 5, 6, 10, 12), (-2, -1, 0, 4, 6, 8, 12), (-1, 0, 2, 5, 6, 9, 12)]   # go to SLEEP, I've got the DARK (the run's cells: the walk could not reach both downbeats)
R2 = [(-3, -2, -1, 0, 3, 4, 6, 8, 9, 12), (-3, -2, -1, 0, 2, 4, 6, 9, 10, 12), (-3, -2, -1, 0, 3, 4, 6, 10, 11, 12)]     # and if you WAKE and don't KNOW where you ARE
REFRAIN = [(-1, 1, 57), (0, 6, 60), (9, 1, 57), (10, 2, 55), (12, 10, 53)]      # it's ME. I'm your SON. -- (onset, duration, pitch)
def refrain(sec):
    ln = SECS[sec][3]; return [(ln["at"] + o, d, p, x, 3) for (o, d, p), x in zip(REFRAIN, ln["syl"])]
def generate(rng):
    out = {}; plans = {}; log = []
    c0 = lambda sl: sl[2] == 0 and sl[6] == 12 and sl[0] >= -3                  # SLEEP on bar 1, DARK on bar 3
    c2 = lambda sl: sl[3] == 0 and sl[0] == -3                                   # 'and if you' the pickup, WAKE on bar 1
    c3 = lambda sl: sl[8] == 12                                                  # HERE on bar 3 (F)
    c1 = lambda sl: sl[-1] <= 18                                                 # line 2 clears line 3's three-eighth pickup
    drawn = draw(rng, PRIORS); plan_c = "Z" + drawn[1] + "Y" + "X"
    def chorus():
        cb = rng.uniform(61.5, 63.0)
        cens = [lambda j, n: cb + 2, lambda j, n: cb + 1.2 * math.sin(j / max(1, n - 1) * math.pi),
                lambda j, n: cb + 1.0, lambda j, n: cb]
        return build_cells("Chorus 1", rng, cens, 55, HIM["chorus"], 7, plan_c, 5,
                           fixed_by_line={0: {6: 69}, 2: {3: 65}, 3: {8: 65}}, conds={1: c1, 3: c3}, log=log,
                           fixed_rh={0: rng.choice(R0), 2: rng.choice(R2)})
    r = retry(chorus, 12)
    if r is None: return None, "chorus"
    Ch, rh_c = r
    plans["Chorus 1"] = "the lullaby: designed cells for lines 1, 3 and 4 (SLEEP/DARK, WAKE, HERE); line 2 drawn " + drawn[1]
    out["Chorus 1"] = Ch
    def last():                                                                  # the final chorus: line 3's WAKE on Bb4, the line re-filled around it
        c2_ = copy_lines(Ch, "Chorus 1", "Chorus 2", [0, 1, 3])
        ln = SECS["Chorus 2"][2]; sl = rh_c[2]
        prev = [n for n in c2_ if n[4] == 1][-1][2]
        l3 = build_line(ln, rng, prev, lambda j, n: 64.0 + (2.0 if j >= 3 else 0), 55, HIM["chorus"], 7, sl, fixed={3: 70},
                        nxt_on=SECS["Chorus 2"][3]["at"] + rh_c[3][0] - ln["at"])
        if l3 is None: return None
        return sorted(c2_ + l3, key=lambda n: n[0])
    L2 = retry(last, 20)
    if L2 is None: return None, "chorus 2"
    out["Chorus 2"] = L2; plans["Chorus 2"] = "chorus 1, line 3 re-filled around WAKE on Bb4"
    for sec in ("Verse 1", "Verse 2", "Verse 3", "Verse 4"):
        vb = rng.uniform(55.5, 57.5)
        pl = draw(rng, PRIORS)
        offs = [rng.choice([-1, 0, 0.5, 1]) for _ in range(4)]
        cens = [lambda j, m, o=o: vb + o + 1.0 * math.sin(j / max(1, m - 1) * math.pi) for o in offs]
        r = retry(lambda: build_cells(sec, rng, cens, HIM["lo"], HIM["verse"], 5, pl, TONIC[sec], skip=(3,), log=log), 6)
        if r is None: return None, sec
        out[sec] = r[0] + refrain(sec); plans[sec] = pl + " (line 4 the refrain kernel)"
    allz = sorted([(o, d, p, x, (s_, i), s_) for s_ in SINGS for o, d, p, x, i in out[s_]], key=lambda n: n[0])
    for j in range(len(allz) - 1):
        a, b = allz[j], allz[j + 1]
        if b[0] <= a[0]: return None, "join"
        if a[4] != b[4] and a[0] + a[1] > b[0] - 1:
            nd = b[0] - 1 - a[0]
            if nd < 1: return None, "join"
            allz[j] = (a[0], nd) + a[2:]
    for s_ in SINGS: out[s_] = [(o, d, p, x, k[1]) for o, d, p, x, k, ss in allz if ss == s_]
    out["plans"] = plans; out["cell_log"] = log
    return out, None

BY_CONSTRUCTION = ["the refrain (ME on C4, SON/SONG on F3; copied whole)", "the chorus's DARK on A4 (aimed)", "WAKE on F4, and on Bb4 in the final chorus (aimed)",
                   "HERE on F4 (aimed)", "line 2 open (the plan)", "the chorus's other notes under A4 (capped)"]
def evaluate(c):
    for s in SINGS:
        for ln in SECS[s]:
            ns = [n for n in c[s] if n[4] == ln["idx"]]; ps = [n[2] for n in ns]
            if s in HOOKY: lim = 70 if (s == "Chorus 2" and ln["idx"] == 2) else (69 if ln["idx"] == 0 else 67); lo = 55
            else: lim = HIM["verse"]; lo = HIM["lo"]
            if max(ps) > lim or min(ps) < lo: return ("range", (s, ln["idx"], max(ps)), lim), None
            iv = intervals(quarters(ns))
            if iv and max(abs(x) for x in iv) > 7: return ("leap", (s, ln["idx"]), ""), None
            if any(abs(x) == 6 for x in iv): return ("tritone", (s, ln["idx"]), "death"), None
            if red(next(n for n in ns if n[2] == max(ps))[3]) and ln["role"] != "refrain": return ("floor:reduced_peak", (s, ln["idx"]), ""), None   # the refrain's ME is stressed in the singing ('it's ME') though the lexicon reads 'me' as a function word -- a finding
            ft = fem_tail([n[3] for n in ns])
            if ft:
                for n in ns[-ft:]:
                    if n[1] > 1 or n[2] != ns[-ft - 1][2] or strong_abs(n[0]): return ("feminine:tail", (s, ln["idx"]), "21.7a"), None
    top = [n for s in SINGS for n in c[s] if n[2] > 69]
    if len(top) != 1 or top[0][2] != 70 or top[0][3][0] != "wake": return ("Bb4 once", len(top), "on the last WAKE"), None
    a4 = {n[3][0] for s in SINGS for n in c[s] if n[2] == 69}
    if a4 != {"dark"}: return ("A4 only on DARK", a4, ""), None
    for s in HOOKY:
        dk = [n for n in c[s] if n[4] == 0 and n[3][0] == "dark"][0]
        if dk[0] != SECS[s][0]["at"] + 12 or dk[2] != 69: return ("hook:dark", s, "A4 on bar 3"), None
    for s in ("Verse 1", "Verse 2", "Verse 3", "Verse 4"):
        so = [n for n in c[s] if n[4] == 3][-1]
        if so[2] != 53 or so[0] != SECS[s][3]["at"] + 12: return ("refrain", s, "SON on F3, bar 3"), None
    body = [n for n in c["Chorus 1"] if n[4] in (1, 2, 3)]
    if max(n[2] for n in body) < 65: return ("chorus:cross", max(n[2] for n in body), ">= F4"), None
    V = c["Verse 1"]
    if contour(V) not in ("flat", "wave", "arch", "descending"): return ("verse:contour", contour(V), "flat/wave"), None
    srt = sorted([n for s in SINGS for n in c[s]], key=lambda n: n[0]); cur = best = 0
    for a, b in zip(srt, srt[1:] + [None]):
        cur += 1
        if b is None or b[0] - (a[0] + a[1]) >= 1: best = max(best, cur); cur = 0
    if best > 13: return ("breath", best, "<= 13"), None
    allw = [n for s in SINGS for n in c[s]]
    strong = [n for n in allw if strong_abs(n[0])]
    al = sum(1 for n in strong if n[3][2]) / len(strong)
    if al < 0.444: return ("floor:alignment", round(al, 3), ">= 0.444"), None
    H = c["Chorus 1"]
    tune = quarters(V) + [(o + 70, d, p) for o, d, p in quarters(H)]
    beta = beta_pitch(tune)
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral", beta and round(beta, 3), "p05-p95"), None
    cmp_, _ = cmp_score(tune, 4, TCAL)
    if cmp_ < C["cmp"]["p05"]: return ("cmp", round(cmp_, 3), ">= p05"), None
    mh, _, _ = m_horizon(quarters(H), quarters(V))
    if mh < C["mh"]["p05"]: return ("memory", round(mh, 3), ">= p05"), None
    bits = PPMM.bits(PPM.symbols(tune, TCAL))[len(V):]
    hp = [n[2] for n in H]
    ic, icd = ic_profile(bits, hp.index(max(hp)))
    if ic < C["ic"]["p05"]: return ("surprisal", round(ic, 3), ">= p05"), None
    fv = (feature_vec(quarters(H), TCAL, 4) - MU) / SD
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
                      beta=beta, longest=best)

def fingerprint(c):
    return hashlib.sha1(json.dumps([[n[0], n[1], n[2]] for k in ("Verse 1", "Verse 2", "Chorus 1", "Verse 3", "Verse 4", "Chorus 2") for n in c[k]]).encode()).hexdigest()[:12]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    rng = random.Random(20261124)
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
    pickle.dump(dict(by_construction=BY_CONSTRUCTION, alive=alive[:60], deaths=deaths, made=made, tries=tries, order_fp=order_fp, rate=rate, survivors=len(alive)), open("/home/claude/p24/melody_result.pkl", "wb"))
