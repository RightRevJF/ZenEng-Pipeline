"""Dance Anyway, version 3: the music rebuilt under ZenEng v95 on the locked lyric (draft 5).
Ported before the search, in the order given:
  201  a line takes its bars from its syllables: about five a bar at q = 118, the opening unstressed syllables sung as a pickup;
       over ten after the pickup takes a third bar; every copy of a tune takes its first statement's span. Verse lines 2 and 4,
       chorus line 4 (and its return, line 8) and bridge line 2 take three bars: 99 bars, 3:21.
  199  the chord-tone term in the walk on the beat, aimed at the class's shares (pop: 72% on the beat, 62% off; chart 69% and 62%).
  206  at most five note lengths in any 8-bar span: onsets on eighths (gaps of an eighth, quarter, dotted quarter or half), and a
       line's last note held one of two lengths (a half or a dotted half), shorter only where the next line comes sooner.
  205  say it twice: AABC/AAAB in the plans at about one section in five where they are admissible; the pre-chorus may open by
       repeating its first unit (its lines are within three syllables); where no section opens that way, the pre-chorus does.
  208  the bridge's job: its opening unit related to neither the verse's nor the chorus's opening (a gate, read on lines as 195
       reads the 181 gate); its median pitch above the verse's (the writer: lifted, 'A'); no pace term.
  209  the instrumental hook (searched after the melody, in arrange_v3).
  194-198, 200, 202, 203, 195 as in the paper; 196: the pop floor is the run clause, three pitches a line a reading.
  The summit (202, the writer 'A'): D5 on chorus line 6's last stressed syllable in every chorus ('twelve'; 'July' in the last).
  210-211: the distance from the centre printed (partial: Table CU's measures only); the composite is the rank of record.
Usage: PYTHONHASHSEED=0 python3 melody_v3_p36.py N [main|ctl]     ctl: 199, 201, 205 and 206 off (same seed and N)."""
import sys, os, json, math, random, pickle, hashlib, collections, platform, copy
import numpy as np
_MODE = sys.argv[2] if len(sys.argv) > 2 else "main"; _N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
sys.argv = [sys.argv[0], "1", "main"]
sys.path[:0] = ["/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyric_v2 as L2
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec
MODE = _MODE; HERE = "/home/claude/p36"
F = dict(f199=MODE == "main", f201=MODE == "main", f205=MODE == "main", f206=MODE == "main")
BAR, BEAT = M.BAR, M.BEAT
M.WORDS_OF = dict(L2.SECTIONS)
LINES = {s: [M.syl(t) for _, t in M.WORDS_OF[s]] for s in M.SUNG}
M.LINES = LINES
SUNG = M.SUNG

# ---- 201: spans ----
def counted(sy):
    k = 0
    while k < len(sy) - 1 and not sy[k][1] and k < 2: k += 1
    return len(sy) - k
PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Pre": ["Pre 1", "Pre 2"], "Chorus": ["Chorus 1", "Chorus 2", "Last Chorus"], "Bridge": ["Bridge"]}
RETURN_OF = {"Chorus": {7: 3, 5: 1, 4: 0, 6: 2}}            # the 16-bar period: the second half sings the first
def spans_for(kind):
    n = len(LINES[PAIRS[kind][0]]); sp = []
    for i in range(n):
        c = max(counted(LINES[s][i]) for s in PAIRS[kind])
        sp.append(3 if (F["f201"] and c > 10) else 2)
    if kind in RETURN_OF:
        for i, j in RETURN_OF[kind].items(): sp[i] = sp[j] = max(sp[i], sp[j])
    return sp
SPANS = {k: spans_for(k) for k in PAIRS}
# chords by the section jobs (177), one a bar, laid on the spans
def chords_for(kind):
    sp = SPANS[kind]
    if kind == "Verse":
        two = [["Eb", "Eb"], ["Ab", "Eb"], ["Cm", "Ab"], ["Eb", "Bb"]]; three = [None, ["Ab", "Eb", "Eb"], None, ["Eb", "Ab", "Bb"]]
    elif kind == "Pre":
        two = [["Ab", "Bb"], ["Cm", "Bb"]]; three = [["Ab", "Ab", "Bb"], ["Cm", "Ab", "Bb"]]
    elif kind == "Chorus":
        two = [["Eb", "Bb"], ["Cm", "Ab"], ["Eb", "Bb"], ["Ab", "Ab"], ["Eb", "Bb"], ["Cm", "Bb"], ["Eb", "Bb"], ["Db", "Eb"]]   # line 6: the summit's D on the V
        three = [None, ["Cm", "Ab", "Ab"], None, ["Ab", "Ab", "Bb"], None, ["Cm", "Ab", "Bb"], None, ["Ab", "Db", "Eb"]]
    else:
        two = [["Ab", "Cm"], ["Fm", "Db"], ["Ab", "Cm"], ["Fm", "Bb"]]; three = [None, ["Fm", "Db", "Db"], ["Ab", "Cm", "Cm"], None]
    out = []
    for i, s in enumerate(sp): out += (three[i] if s == 3 else two[i])
    return out
PLAN = dict(M.PLAN); PLAN.update({k: chords_for(k) for k in ("Verse", "Pre", "Chorus", "Bridge")})
FORM = [(nm, kind, len(PLAN[kind])) for nm, kind, _ in M.FORM]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b
if F["f201"]:                                   # the last line's three bars: the hook keeps its own chords (I under it), 'I'm still here' on the bVII
    e = BAR0["Last Chorus"] + len(PLAN["Chorus"]); CHORD[e - 3:e] = ["Db", "Eb", "Eb"]
M.FORM, M.BAR0, M.CHORD, M.NBARS, M.PLAN = FORM, BAR0, CHORD, NBARS, PLAN
KIND = M.KIND
def line_start(sec, i): return (BAR0[sec] + sum(SPANS[KIND[sec]][:i])) * BAR
def line_bars(sec, i): return SPANS[KIND[sec]][i]
SECLEN = {nm: nb for nm, _, nb in FORM}
SPANS8 = [(s, 0) for s in SUNG if SECLEN[s] >= 8] + [(s, 8) for s in SUNG if SECLEN[s] >= 16]
SPANS16 = [s for s in SUNG if SECLEN[s] >= 16]
M.SPANS8, M.SPANS16 = SPANS8, SPANS16
SECS = 60 / M.QBPM * 4 * NBARS

# ---- register, summit, the bridge lifted (208) ----
MUS = {"Verse": 64, "Pre": 66, "Chorus": 68, "Bridge": 67}
CAPS = {"Verse": 70, "Pre": 72, "Chorus": 72, "Bridge": 72}
FLOORS = {"Verse": 58, "Pre": 60, "Chorus": 62, "Bridge": 62}
SUMMIT = 74

# ---- the rhythm of a line over its own bars ----
def line_rhythm(sy, rng, tmin, nb, cadence=False):
    grid_step = 6 if F["f206"] else 3
    end = BAR * nb - 24
    old = M.GRID; M.GRID = list(range(-12, end + 1, grid_step))
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d): return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max(k for k in range(n) if st[k]); post = n - 1 - Ls
    def A(k, t):
        m = M.mw(t)
        return {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
    last = BAR * (nb - 1)
    tg = [(last, 0.55), (last + 24, 0.25), (last - 24, 0.12), (last + 12, 0.08)]
    if cadence and F["f201"]: tg = [(last, 0.7), (last + 24, 0.3)]          # a section's last line lands in its own last bar (201: its chord)
    try:
        for _ in range(8):
            tgt = rng.choices([t for t, _ in tg], [w for _, w in tg])[0]
            if tgt + grid_step * post > end or tgt - grid_step * Ls < tmin: continue
            G = [t for t in M.GRID if t >= tmin]
            alpha = [dict() for _ in range(n)]
            for t in G:
                if t > tgt: break
                if Ls == 0 and t != tgt: continue
                alpha[0][t] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t)
            for k in range(1, n):
                for t in G:
                    if k == Ls and t != tgt: continue
                    if k < Ls and t >= tgt: continue
                    s = 0.0
                    for tp, a in alpha[k - 1].items():
                        d = t - tp
                        if grid_step <= d <= 24: s += a * M.RT[tp % BAR][d] * H(k - 1, d)
                    if s > 0: alpha[k][t] = s * A(k, t)
            if not alpha[n - 1]: continue
            ks = list(alpha[n - 1]); ws = [alpha[n - 1][t] * (1.0 + (end - t) / 40) for t in ks]
            ons = [rng.choices(ks, ws)[0]]
            for k in range(n - 1, 0, -1):
                t = ons[-1]; ks = [tp for tp in alpha[k - 1] if grid_step <= t - tp <= 24]
                ws = [alpha[k - 1][tp] * M.RT[tp % BAR][t - tp] * H(k - 1, t - tp) for tp in ks]
                ons.append(rng.choices(ks, ws)[0])
            ons.reverse(); return ons
        return None
    finally:
        M.GRID = old
def melismas(ons, sy, rng, end, final_mel=0.33, inner=0.14):
    rows = []; step = 6 if F["f206"] else 3
    for k, t in enumerate(ons):
        rows.append([t, k, False]); nxt = ons[k + 1] if k + 1 < len(ons) else None
        if nxt is None:
            if t + 6 <= end and rng.random() < final_mel: rows.append([t + 6, k, True])
        elif nxt - t >= 12 and rng.random() < inner: rows.append([t + (nxt - t) // 2 // step * step, k, True])
    return rows

# ---- the walk: 182 with 197, 198's aim and 199's chord term ----
AIM = dict(repeat=0.95, step=1.35, third=0.8, fourth_fifth=1.0, larger=1.6)
if os.environ.get("AIM"): AIM.update(zip(("repeat", "step", "larger", "third"), map(float, os.environ["AIM"].split(","))))
CW = [2.5, 0.38, 5.0, 1.0]                                    # 199: chord tone / other, on the beat; chord tone / other, off it (calibrated, below)
if os.environ.get("CW"): CW = list(map(float, os.environ["CW"].split(",")))   # 198: the draw aimed so the finished melody meets Table CG
CATS = [(c, w * (AIM[c] if True else 1.0), sz) for c, w, sz in M.CATS]
def chord_w(p, n, ch):
    tones = M.CH[ch][1]; on_beat = n["on"] % BEAT == 0
    if F["f199"]:                                             # 199: the chord on the beat, and lightly off it
        return (CW[0] if p % 12 in tones else CW[1]) if on_beat else (CW[2] if p % 12 in tones else CW[3])
    return (2.0 if p % 12 in tones else 0.5) if (on_beat and n.get("stress")) else (1.3 if p % 12 in tones else 1.0)
def next_pitch(rng, prev, run, n, ch, mu, lo, hi, last_iv=None, toward=None):
    if prev is None:
        cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and not (F["f206"] and (p - M.CH[ch][0]) % 12 == 6)]
        return rng.choices(cands, [math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * chord_w(p, n, ch) for p in cands])[0]
    cats = list(CATS)
    if last_iv is not None and abs(last_iv) > 7: cats = [x for x in CATS if x[0] in ("step", "third")]
    # 199: one draw over every candidate; a category's share tilts by how much chord it offers (its weight with the chord term over
    # its weight without), so the chord term can reach the beat instead of being decided inside whatever category came up first.
    allc, allw = [], []
    for c in cats:
        cands, ws, base = [], [], 0.0
        for sz in c[2]:
            for sg in ((0,) if sz == 0 else (-1, 1)):
                p = prev + sg * sz
                if not (lo <= p <= hi) or p % 12 not in M.SUNGPC or M.clash(p, ch): continue
                if F["f206"] and (p - M.CH[ch][0]) % 12 == 6: continue        # (212) no scale tone a tritone from a borrowed chord's root
                if sz == 0 and run >= 3: continue
                if last_iv is not None and abs(last_iv) > 7 and (sg > 0) == (last_iv > 0): continue
                if toward is not None and (abs(toward - p) > 7 or abs(toward - p) == 6): continue
                w0 = math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * M.SIZE_W.get(sz, 1.0)
                w0 *= 1.0 if sz == 0 else (M.DESC if sg < 0 else 1 - M.DESC)
                cands.append(p); ws.append(w0 * chord_w(p, n, ch)); base += w0
        if cands and base > 0:
            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * w / base)
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]
    return None
def walk_notes(rng, notes, prev, run, mu, lo, hi, notes_on, fixed=None):
    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None
    for i, n in enumerate(notes): n["dur"] = notes[i + 1]["on"] - n["on"] if i + 1 < len(notes) else 24
    for i, n in enumerate(notes):
        if fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:
            q = out[-1]; ch_ = M.chord_for(n, notes_on)
            opts = [x for x in (q - 2, q - 1, q + 1, q + 2) if lo <= x <= hi and x % 12 in M.SCALE and not (F["f206"] and (x - M.CH[ch_][0]) % 12 == 6)]
            p = rng.choices(opts, [(3 if x < q else 1) * (chord_w(x, n, ch_) if F["f199"] else 1.0) for x in opts])[0] if opts else q
        else:
            tw = fixed.get(i + 1) if fixed else None
            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw)
            if p is None: return None
        run = run + 1 if p == prev else 1
        last_iv = (p - prev) if prev is not None else None
        prev = p; out.append(p)
    return out
def fresh_line(sy, rng, U, tmin, nb, cadence=False):
    ons = line_rhythm(sy, rng, tmin, nb, cadence)
    if ons is None: return None
    rows = melismas(ons, sy, rng, BAR * nb - 24)
    return [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]

import inspect as _insp
_src = _insp.getsource(M.align) + _insp.getsource(M._align)
_src = (_src.replace("def align(", "def align3(").replace("def _align(", "def _align3(").replace("r = _align(", "r = _align3(")
        .replace('min(12, 72 - ev[k]["t"])', 'min(12, END_T - ev[k]["t"])').replace("if d < 6: return None", "if d < MINSPLIT: return None")
        .replace("d // 2 // 3 * 3", "d // 2 // STEP * STEP").replace("gap = 6 if t0 - 6 * npk >= max(tmin, -12) else 3", "gap = 6 if t0 - 6 * npk >= max(tmin, -12) else STEP"))
assert _src.count("END_T") == 1 and _src.count("MINSPLIT") == 1 and _src.count("STEP") == 3
exec(_src, M.__dict__)
def align_v3(src, src_sy, sy, U0, U, tmin, nb):
    """181's mapping on the line's own bars (201): a split falls on the eighth grid when 206 is on, the last event's room runs to
    the line's own end; otherwise M.align unchanged."""
    M.END_T = BAR * nb - 24; M.MINSPLIT = 12 if F["f206"] else 6; M.STEP = 6 if F["f206"] else 3
    ns = M.align3(src, src_sy, sy, U0, U, tmin)
    if ns is None: return None
    if F["f206"] and any((n["on"] - U) % 6 for n in ns): return None
    return ns

# ---- 206: the line's last note held one of two lengths ----
END_LENS = (24, 18)
GAP_MIN = 24 if F["f206"] else 12                                   # 206: room for the shorter held end (18) and an eighth's breath
def finish(notes):
    for i, n in enumerate(notes):
        nx = notes[i + 1]["on"] if i + 1 < len(notes) else None
        if nx is None: n["dur"] = 48 if not F["f206"] else 24
        elif notes[i + 1]["line"] != n["line"]:
            room = nx - n["on"] - 6
            if F["f206"]:
                n["dur"] = next((L_ for L_ in END_LENS + (18, 12, 6) if L_ <= room), max(6, room))
            else: n["dur"] = min(60, max(3, room))
        else: n["dur"] = nx - n["on"]
    return notes

# ---- 195: the 181 gate read on lines ----
def unit_lines(notes, a, b, U):
    """a unit read on lines (195): its notes from its line's first onset to the next line's first onset, onsets and the contour
    both counted from the line's own downbeat U (a pickup added or dropped does not move the tune); the last note left out."""
    ns = [n for n in notes if a <= n["on"] < b]
    if len(ns) < 2: return set(), [], ns
    ons = {n["on"] - U for n in ns}
    body = ns[:-1]; ser = []; k = 0; cur = body[0]["p"]
    for t in range(U, body[-1]["on"] + 3, 3):
        while k < len(body) and body[k]["on"] <= t: cur = body[k]["p"]; k += 1
        ser.append(cur)
    return ons, ser, ns
def related_lines(u1, u2):
    o1, s1, _ = u1; o2, s2, _ = u2
    if not o1 or not o2: return False, 0.0, 0.0
    jac = len(o1 & o2) / len(o1 | o2); n = min(len(s1), len(s2))
    a, b2 = np.array(s1[:n], float), np.array(s2[:n], float)
    if n < 2 or (a.std() == 0 and b2.std() == 0): r = 1.0 if n >= 2 else 0.0
    elif a.std() == 0 or b2.std() == 0: r = 0.0
    else: r = float(np.corrcoef(a, b2)[0, 1])
    return (jac >= 0.6 and r >= 0.6), jac, r
def line_span(notes, sec, i, k=1):
    """the unit of k lines from line i: its first onset to the first onset of the line after it."""
    ln = [n for n in notes if n["line"] == f"{sec}:{i}"]
    nxt = [n for n in notes if n["line"] == f"{sec}:{i + k}"] if i + k < len(LINES[sec]) else []
    a = ln[0]["on"]; b = nxt[0]["on"] if nxt else max(n["on"] for n in notes if n["sec"] == sec) + 1
    return a, b, line_start(sec, i)
def returns_related(c):
    out = []
    for sec, i, s0, i0, k in c["meta"]["returns"]:
        u = unit_lines(c["notes"], *line_span(c["notes"], sec, i, k)); u0 = unit_lines(c["notes"], *line_span(c["notes"], s0, i0, k))
        out.append(((sec, i, s0, i0, k),) + related_lines(u, u0))
    return out
def bridge_opening(notes):
    """208: the bridge's opening unit against the verse's and the chorus's opening units (a unit: the first line), on lines (195)."""
    ub = unit_lines(notes, *line_span(notes, "Bridge", 0)); uv = unit_lines(notes, *line_span(notes, "Verse 1", 0)); uc = unit_lines(notes, *line_span(notes, "Chorus 1", 0))
    return related_lines(ub, uv), related_lines(ub, uc)

# ---- plans (181, 205) ----
VERSE_PLANS = [("ABAC", 0.4), ("ABAB", 0.4), ("AABC", 0.1), ("AAAB", 0.1)]
BRIDGE_PLANS = [("ABAC", 0.5), ("ABCD", 0.3), ("AABC", 0.1), ("AAAB", 0.1)]
CHORUS_HEADS = [("ABCD", 0.4), ("ABAC", 0.4), ("AABC", 0.2)]
PRE_PLANS = [("AB", 0.75), ("AA", 0.25)]
if not F["f205"]:
    VERSE_PLANS = [("ABAC", 0.34), ("ABAB", 0.33), ("AABC", 0.33)]; BRIDGE_PLANS = [("AABC", 0.5), ("ABAC", 0.5)]
    CHORUS_HEADS = [("ABCD", 0.5), ("ABAC", 0.5)]; PRE_PLANS = [("AB", 1.0)]
def admissible(sec, plan):
    kind = KIND[sec]; sp = SPANS[kind]
    for i, x in enumerate(plan):
        j = plan.index(x)
        if j == i: continue
        for s in PAIRS[kind]:
            if abs(len(LINES[s][i]) - len(LINES[s][j])) > 3: return False
        if sp[i] != sp[j]: return False
    return True
def draw_plan(rng, sec, plans):
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCD", 1.0)]
    return list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])

def generate(rng):
    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS),
                 ChorusHead=draw_plan(rng, "Chorus 1", CHORUS_HEADS), Pre=draw_plan(rng, "Pre 1", PRE_PLANS))
    if F["f205"] and not any(p[0] == p[1] for p in (plans["Verse"], plans["Bridge"], plans["ChorusHead"], plans["Pre"])):
        if admissible("Pre 1", list("AA")): plans["Pre"] = list("AA")          # 205: one section opens by repeating its first unit
    plans["Chorus"] = plans["ChorusHead"] + [x + "'" for x in plans["ChorusHead"]]
    built, lines = {}, []; prev, run, last_on = None, 0, -10 ** 6; notes_on_all = set()
    meta = dict(plans=plans, returns=[], shifts={})
    def place(sec, i, ns):
        nonlocal prev, run, last_on
        for n in ns: n["sec"] = sec; n["line"] = f"{sec}:{i}"
        built[(sec, i)] = ns; lines.append(dict(sec=sec, idx=i, notes=ns))
        prev = ns[-1]["p"]; last_on = ns[-1]["on"]; rr = 1
        for a, b2 in zip(ns[::-1], ns[-2::-1]):
            if a["p"] == b2["p"]: rr += 1
            else: break
        run = rr
    for sec in SUNG:
        kind = KIND[sec]; mu = MUS[kind]; hi = CAPS[kind]; lo = FLOORS[kind]; sys_ = LINES[sec]
        src_sec = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}.get(sec)
        plan = plans["Chorus"] if kind == "Chorus" else plans[kind]
        for i, sy in enumerate(sys_):
            U = line_start(sec, i); nb = line_bars(sec, i); tmin = max(-12, last_on + GAP_MIN - U)
            lt = plan[i] if i < len(plan) else chr(65 + i); first = plan.index(lt[0]) if lt[0] in plan else i
            if src_sec:
                S = built[(src_sec, i)]; Ssy = LINES[src_sec][i]; SU = line_start(src_sec, i)
                if sec == "Last Chorus" and i == 7:
                    S = built[("Chorus 1", 0)]; Ssy = LINES["Chorus 1"][0]; SU = line_start("Chorus 1", 0)
                if [x[0] for x in Ssy] == [x[0] for x in sy]: ns = [dict(n, on=n["on"] - SU + U) for n in S]
                elif sec == "Last Chorus" and i == 7 and [x[0] for x in sy[-len(Ssy) + 1:]] == [x[0] for x in Ssy[1:]]:
                    off = (nb - SPANS["Chorus"][0]) * BAR          # 201: the line has a bar more than the hook; the hook keeps its place in its bars
                    hk = [dict(n, on=n["on"] - SU + U + off) for n in S]; npre = len(sy) - len(Ssy)
                    step = 6 if F["f206"] else 3
                    h0 = hk[0]["on"] - U; slots = [t for t in range(max(tmin, h0 - 48), h0 - step + 1, step)]
                    import itertools; best = None
                    for comb in itertools.combinations(slots, npre):
                        iois = [b3 - a for a, b3 in zip(comb, list(comb[1:]) + [h0])]
                        if max(iois) > 24: continue
                        w = 1.0
                        for q, t in enumerate(comb):
                            m = M.mw(t); w *= {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if sy[q][1] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
                        if best is None or w > best[0]: best = (w, comb)
                    if best is None: return None, "align: no room before the hook"
                    pre = [dict(on=U + t, p=None, syl=q, slur=False, stress=sy[q][1]) for q, t in enumerate(best[1])]
                    ps = walk_notes(rng, pre, prev, run, mu, lo, hi, notes_on_all)
                    if ps is None: return None, "walk: no note"
                    for n, p in zip(pre, ps): n["p"] = p
                    for n in hk: n["syl"] += npre
                    ns = pre + hk; meta["returns_extra"] = ("Last Chorus", 7, "Chorus 1", 0)
                else: ns = align_v3(S, Ssy, sy, SU, U, tmin, nb)
                if ns is None: return None, "align: the words do not fit the tune"
                ns = [dict(n) for n in ns]
            elif first < i and lt[0] in plan and (sec, first) in built:
                S = built[(sec, first)]; Ssy = sys_[first]; SU = line_start(sec, first)
                ns = align_v3(S, Ssy, sy, SU, U, tmin, nb)
                if ns is None: return None, "align: the words do not fit the returning unit"
                if kind != "Chorus" or i < 4: meta["returns"].append((sec, i, sec, first, 1))
                if kind == "Chorus" and i in (4, 6): meta["returns"].append((sec, i, sec, i - 4, 2))
                k = rng.choices([0, 1, -1, 2, -2], [0.5, 0.15, 0.1, 0.15, 0.1])[0]
                if kind == "Chorus" and i in (5, 7): k = meta["shifts"].get((sec, i - 1), 0)
                ps = [M.dshift(n["p"], k) for n in ns]
                bad_iv = any(abs(y - x) > 12 or abs(y - x) == 6 for x, y in zip(ps, ps[1:]))
                if max(ps) > hi or min(ps) < lo or bad_iv: k = 0; ps = [n["p"] for n in ns]
                meta["shifts"][(sec, i)] = k
                for n, p in zip(ns, ps): n["p"] = p
                if len(ns) >= 4 and rng.random() < 0.5 and not (kind == "Chorus" and i in (4, 6, 7)):
                    fx = {j: ns[j]["p"] for j in range(len(ns) - 1)}
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx)
                    if ps is None: return None, "walk: no note"
                    for n, p in zip(ns, ps): n["p"] = p
            else:
                ns = fresh_line(sy, rng, U, tmin, nb, cadence=(i == len(sys_) - 1 or (kind == "Chorus" and i in (1, 5))))   # the summit's line and its source land on a beat
                if ns is None: return None, "rhythm: no placement"
                ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all)
                if ps is None: return None, "walk: no note"
                for n, p in zip(ns, ps): n["p"] = p
            if ns[0]["on"] - last_on < GAP_MIN: return None, "join: no held end and breath before the line (206)"
            if prev is not None and (abs(ns[0]["p"] - prev) > 12 or abs(ns[0]["p"] - prev) == 6):
                pk = [j for j, n in enumerate(ns) if n["on"] < U]
                if pk:
                    fx = {j: ns[j]["p"] for j in range(len(ns)) if j not in pk}
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx)
                    if ps: [n.__setitem__("p", p) for n, p in zip(ns, ps)]
            # the summit (the writer, 'A'): D5 on chorus line 6's last stressed syllable in every chorus
            if kind == "Chorus" and i == 5:
                st = [n for n in ns if n["stress"]]
                if st:
                    tgt = st[-1]; k_ = ns.index(tgt); tgt["p"] = SUMMIT
                    ok = lambda a, b3: abs(b3 - a) <= 7 and abs(b3 - a) != 6
                    if k_ > 0 and not ok(ns[k_ - 1]["p"], SUMMIT): ns[k_ - 1]["p"] = 70 if ok(ns[k_ - 2]["p"] if k_ >= 2 else 70, 70) else 72
                    for n in ns[k_ + 1:]:
                        if n["slur"] and n["syl"] == tgt["syl"]: n["p"] = 72
                        elif n["p"] > 72: n["p"] = 72
            # the chorus ends on a tone of the tonic chord; the song's last line on the tonic
            if kind == "Chorus" and i == 7:
                pcs = (M.TONIC,) if sec == "Last Chorus" else tuple(sorted(M.CH[M.chord_at(ns[-1]["on"])][1] & {M.TONIC, 7, 10})) or (M.TONIC, 7, 10)
                if ns[-1]["p"] % 12 not in pcs:
                    q = ns[-1]["p"]; opts = [p for p in range(lo, 73) if p % 12 in pcs and not M.join_bad(ns[-2]["p"], p)] or [p for p in range(lo, 73) if p % 12 in pcs]
                    ns[-1]["p"] = min(opts, key=lambda p: (abs(p - q), p % 12 != M.TONIC))
            for n in ns: notes_on_all.add(n["on"])
            place(sec, i, ns)
    notes = sorted([n for l in lines for n in l["notes"]], key=lambda n: n["on"])
    on = {n["on"] for n in notes}
    for n in notes:
        n.setdefault("dur", 12)
        if n["p"] % 12 in (6, 1) and M.clash(n["p"], M.chord_for(n, on)):
            tones = M.CH[M.chord_for(n, on)][1]; n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q: (q % 12 not in tones, q % 12 not in M.SCALE))
        ch_ = M.chord_for(n, on)
        if F["f206"] and (n["p"] - M.CH[ch_][0]) % 12 == 6 and n["p"] != SUMMIT:     # (212) a copied note a tritone from the root moves a step to a chord tone
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] + 1, n["p"] - 1, n["p"] + 2, n["p"] - 2), key=lambda q: (q % 12 not in tones, abs(q - n["p"])))
    finish(notes)
    return dict(notes=notes, meta=meta), None

# ---- readings (v95's list) ----
def windows(notes):
    """8-bar windows from the first bar of each verse and chorus, tiled while eight bars remain (Table CU's windows)."""
    out = []
    for s in SUNG:
        if KIND[s] not in ("Verse", "Chorus"): continue
        b0 = BAR0[s]
        for k in range(0, SECLEN[s] - 7, 8): out.append((s, b0 + k))
    return out
def win_notes(notes, b0): return [n for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR]
def note_lengths(ns): return {n["dur"] for n in ns}
def win_read(notes, b0):
    ns = win_notes(notes, b0); on = {n["on"] for n in notes}
    durs = [n["dur"] for n in ns]; med = float(np.median(durs))
    per_bar = [sum(1 for n in ns if (b0 + k) * BAR <= n["on"] < (b0 + k + 1) * BAR) for k in range(8)]
    ct_on = [n for n in ns if n["on"] % BEAT == 0]; ct_off = [n for n in ns if n["on"] % BEAT]
    long_ = [n for n in ns if n["dur"] >= med * 1.5] or ns
    isct = lambda n: n["p"] % 12 in M.CH[M.chord_for(n, on)][1]
    iv = [b2["p"] - a["p"] for a, b2 in zip(ns, ns[1:])]
    gaps = [b2["on"] - a["on"] for a, b2 in zip(ns, ns[1:]) if a["line"] == b2["line"]]
    u = [M.unit(notes, (b0 + 2 * k) * BAR, 2 * BAR) for k in range(4)]
    return dict(longest_over_median=max(durs) / med, lengths=len(set(durs)), sixteenth=(sum(1 for g in gaps if g == 3) / max(1, len(gaps))),
                spread=float(np.std(per_bar)), chord=sum(map(isct, ns)) / len(ns), chord_on=sum(map(isct, ct_on)) / max(1, len(ct_on)),
                chord_off=sum(map(isct, ct_off)) / max(1, len(ct_off)), chord_long=sum(map(isct, long_)) / len(long_),
                pitch=M.pitch_bits([n["p"] for n in ns]), mean_iv=float(np.mean([abs(x) for x in iv])),
                fourth_fifth=sum(1 for x in iv if abs(x) in (5, 7)) / len(iv), repeat_at_once=M.related(u[1], u[0])[0], returns_third=M.related(u[2], u[0])[0])
# Table CU's chart-pop quartiles for 210's partial distance (11 of the 46 measures; the others are not on file)
CU = dict(longest_over_median=(2, 3, 4), lengths=(3, 4, 5), sixteenth=(0, 0, 0.154), spread=(1.199, 1.615, 2.119), chord=(0.536, 0.651, 0.759),
          chord_on=(0.562, 0.692, 0.8), pitch=(2.532, 2.735, 3.029), mean_iv=(1.638, 2.077, 2.49), chord_long=(0.551, 0.75, 0.931),
          chord_off=(0.475, 0.625, 0.765), fourth_fifth=(0.027, 0.074, 0.121))
def distance(notes):
    ds = []
    for s, b0 in windows(notes):
        if s not in ("Verse 1", "Chorus 1"): continue
        r = win_read(notes, b0); d = []
        for k, (q1, q2, q3) in CU.items():
            w = max(q3 - q1, 1e-6); v = r[k]
            d.append(min(3.0, max(0.0, (q1 - v) / w, (v - q3) / w)))
        ds.append(float(np.mean(d)))
    return float(np.mean(ds))
def song_read(notes):
    W = [win_read(notes, b0) for _, b0 in windows(notes)]; on = {n["on"] for n in notes}
    ons_b = [n for n in notes if n["on"] % BEAT == 0]; off_b = [n for n in notes if n["on"] % BEAT]
    isct = lambda n: n["p"] % 12 in M.CH[M.chord_for(n, on)][1]
    gaps = [b2["on"] - a["on"] for a, b2 in zip(notes, notes[1:]) if a["line"] == b2["line"]]
    br = M.sec_notes(notes, "Bridge"); vv = M.sec_notes(notes, "Verse 1")
    bo = bridge_opening(notes)
    ps = [n["p"] for n in notes]; d8 = M.phrase_designs(notes)
    return dict(chord_on=sum(map(isct, ons_b)) / len(ons_b), chord_off=sum(map(isct, off_b)) / len(off_b),
                sixteenth=sum(1 for g in gaps if g == 3) / len(gaps),
                longest_over_median=float(np.median([w["longest_over_median"] for w in W])), lengths=float(np.median([w["lengths"] for w in W])),
                lengths_max=max(w["lengths"] for w in W), repeat_at_once=sum(w["repeat_at_once"] for w in W) / len(W),
                returns_third=sum(w["returns_third"] for w in W) / len(W), spread=float(np.median([w["spread"] for w in W])),
                stock8=d8["stock8"], stock16=d8["stock16"], pitch=M.pitch_bits(ps), intervals=M.interval_shares(ps), exact=M.repetition(notes)["exact"],
                bridge_rel_verse=bo[0], bridge_rel_chorus=bo[1],
                bridge_median_minus_verse=float(np.median([n["p"] for n in br]) - np.median([n["p"] for n in vv])),
                bridge_onsets_ratio=(len(br) / SECLEN["Bridge"]) / (len(vv) / SECLEN["Verse 1"]),
                distance=distance(notes), two_pitch=sum(1 for ln in dict.fromkeys(n["line"] for n in notes) if len({n["p"] for n in notes if n["line"] == ln}) <= 2) / len(set(n["line"] for n in notes)),
                windows=len(W))

def register_bad(notes):
    top = lambda s: max(n["p"] for n in notes if n["sec"] == s)
    return [(v, h) for v, h in (("Verse 1", "Chorus 1"), ("Verse 2", "Chorus 2"), ("Verse 2", "Last Chorus")) if top(h) < top(v)]
GATES = ["pitch band (153/182)", "rhythm band (163)", "pushed notes (159)", "density (159)", "sequence legs (148)", "key word on a chord tone (134)",
         "register (133)", "summit placed (the writer's A)", "monotony run (166/196)", "leaps: tritone or past an octave", "returns related, on lines (181/195)",
         "note lengths <= 5 per 8 bars (206)", "bridge opening unrelated (208)", "bridge above the verse (208)"]
CONSTRUCTED = {"summit placed (the writer's A)": "summit", "monotony run (166/196)": "the walk's run ban", "leaps: tritone or past an octave": "the walk",
               "returns related, on lines (181/195)": "181", "note lengths <= 5 per 8 bars (206)": "206", "bridge above the verse (208)": "208 (register)"}
def gate_fails(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]; f = {}
    pb = M.pitch_bits(ps); rb = M.rhythm_bits(notes)
    if not (M.PBAND["p05"] <= pb <= M.PBAND["p95"]): f["pitch band (153/182)"] = round(pb, 3)
    if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): f["rhythm band (163)"] = round(rb, 3)
    pu = M.pushed_share(notes)
    if pu > 0.42: f["pushed notes (159)"] = pu
    de = len(notes) / sum(SECLEN[s] * 4 * 60 / M.QBPM for s in SUNG)
    if not (1.1 <= de <= 4.9): f["density (159)"] = de
    if any(l >= 3 for l in M.sequences(notes)): f["sequence legs (148)"] = 1
    if M.keyword_chord(notes)[0] < 0.40: f["key word on a chord tone (134)"] = 1
    if register_bad(notes): f["register (133)"] = 1
    summ = [n for n in notes if n["p"] == SUMMIT]
    on_ = {n["on"] for n in notes}
    if len(summ) != 3 or any(n["line"].split(":")[1] != "5" or KIND[n["sec"]] != "Chorus" or n["on"] % BEAT or SUMMIT % 12 not in M.CH[M.chord_for(n, on_)][1] for n in summ) or max(ps) > SUMMIT:
        f["summit placed (the writer's A)"] = len(summ)
    w, _ = M.monotony(notes)
    if w > 3: f["monotony run (166/196)"] = w
    mx, tri = M.leaps(notes)
    if mx > 12 or tri: f["leaps: tritone or past an octave"] = (mx, tri)
    rr = [r for r in returns_related(c) if not r[1]]
    if rr: f["returns related, on lines (181/195)"] = rr[0][0]
    if max(len(note_lengths(win_notes(notes, b0))) for b0 in range(0, NBARS - 7)) > 5 and any(win_notes(notes, b0) for b0 in range(NBARS - 7)): f["note lengths <= 5 per 8 bars (206)"] = 1
    bo = bridge_opening(notes)
    if bo[0][0] or bo[1][0]: f["bridge opening unrelated (208)"] = 1
    br = M.sec_notes(notes, "Bridge"); vv = M.sec_notes(notes, "Verse 1")
    if not np.median([n["p"] for n in br]) > np.median([n["p"] for n in vv]): f["bridge above the verse (208)"] = 1
    return f
def lengths_ok(notes):
    return all(len(note_lengths([n for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR])) <= 5 for b0 in range(0, NBARS - 7))
def evaluate(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    if min(ps) < M.LO or max(ps) > SUMMIT: return ("range", (min(ps), max(ps))), None
    f = gate_fails(c)
    if not F["f206"]: f.pop("note lengths <= 5 per 8 bars (206)", None)          # the control: 206 off is not gated
    order = ["leaps: tritone or past an octave", "monotony run (166/196)", "summit placed (the writer's A)", "register (133)", "returns related, on lines (181/195)",
             "bridge opening unrelated (208)", "bridge above the verse (208)", "pitch band (153/182)", "rhythm band (163)", "pushed notes (159)", "density (159)",
             "sequence legs (148)", "key word on a chord tone (134)", "note lengths <= 5 per 8 bars (206)"]
    for g in order:
        if g in f: return (g, f[g]), None
    # Table B on the pop calibration, verse 1 and chorus 1; Table C: the rank of record (211)
    V = M.sec_notes(notes, "Verse 1"); H = M.sec_notes(notes, "Chorus 1")
    off = V[0]["on"]; tune = M.quarters(V, off) + M.quarters(H, off)
    beta = beta_pitch(tune); C = M.C
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral (Table B)", beta), None
    cmp_, _ = cmp_score(tune, 4, M.TONIC)
    if cmp_ < C["cmp"]["p05"]: return ("cmp (Table B)", cmp_), None
    hq = M.quarters(H, H[0]["on"]); vq = M.quarters(V, V[0]["on"]); mh, _, _ = m_horizon(hq, vq)
    if mh < C["mh"]["p05"]: return ("memory (Table B)", mh), None
    bits = M.PPMM.bits(PPM.symbols(tune, M.TONIC))[len(V):]; hp = [n["p"] for n in H]
    ic, _ = ic_profile(bits, hp.index(max(hp)))
    if ic < C["ic"]["p05"]: return ("surprisal (Table B)", ic), None
    fv = (feature_vec(hq, M.TONIC, 4) - M.MU) / M.SD
    dist = np.sort(np.sqrt(((M.ZREF - fv) ** 2).sum(1)))[:10].mean(); real = sum(1 for x in M.REAL_KNN if x >= dist) / len(M.REAL_KNN)
    if real < C["realness"]["p05"]: return ("realness (Table B)", real), None
    S_sp = s_spectral(beta, C["beta"]["p25"], C["beta"]["p75"]); vps = [n["p"] for n in V]; lift = float(np.median(hp) - np.median(vps))
    fit = float(np.mean([M.contour(hp) in ("arch", "ascending", "wave", "descending"), 1.0 if lift >= 4 else (0.5 if lift >= 2 else 0.0), M.contour(vps) in ("flat", "wave"), max(vps) <= CAPS["Verse"]]))
    comp = 0.15 * S_sp + 0.15 * min(1.0, cmp_ / C["cmp"]["p75"]) + 0.10 * min(1, mh) + 0.15 * fit + 0.15 * ic + 0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5
    return None, dict(composite=round(comp, 4), pitch_bits=round(M.pitch_bits(ps), 3), rhythm_bits=round(M.rhythm_bits(notes), 3), IC=ic, CMP=cmp_, M_horizon=mh, realness=real, fit=fit, lift=lift,
                      flag_p25=M.pitch_bits(ps) < M.PBAND["p25"])

if __name__ == "__main__":
    N = _N; SEED = 20261110 + 363
    rng = random.Random(SEED); made, deaths, alive = 0, collections.Counter(), []
    would, spread = collections.Counter(), collections.defaultdict(list)
    while made < N:
        c, err = generate(rng); made += 1
        if err: deaths[err] += 1; continue
        f = gate_fails(c)
        for g in f: would[g] += 1
        r = song_read(c["notes"])
        for k in ("chord_on", "chord_off", "sixteenth", "longest_over_median", "lengths", "repeat_at_once", "stock8", "stock16", "pitch", "exact", "bridge_median_minus_verse", "bridge_onsets_ratio", "distance", "spread"):
            spread[k].append(float(r[k]))
        for k in ("repeat", "step", "larger"): spread["iv_" + k].append(r["intervals"][k])
        spread["bridge_rel_any"].append(float(r["bridge_rel_verse"][0] or r["bridge_rel_chorus"][0]))
        cert, m = evaluate(c)
        if cert: deaths[cert[0]] += 1; continue
        c["meas"] = m; c["fp"] = M.fingerprint(c); c["read"] = r; alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    print(f"[{MODE}] {NBARS} bars, spans {SPANS}; built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order {order}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in GATES]
    for k, v in spread.items(): print(f"   {k}: {np.percentile(v, 5):.3f} - {np.median(v):.3f} - {np.percentile(v, 95):.3f}")
    for c in alive[:5]:
        r = c["read"]; print(c["fp"], c["meta"]["plans"]["Verse"], c["meta"]["plans"]["Pre"], c["meta"]["plans"]["ChorusHead"], c["meta"]["plans"]["Bridge"], f"comp {c['meas']['composite']:.3f} pitch {r['pitch']:.2f} on {r['chord_on']:.2f} off {r['chord_off']:.2f} lengths {r['lengths']} rep1 {r['repeat_at_once']:.2f} dist {r['distance']:.3f}")
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{HERE}/lyric_v2.py", "rb").read() + open(f"{HERE}/melody_p36.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, N=N, mode=MODE, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(), numpy=np.__version__,
                 tables_sha256=hashlib.sha256(open(f"{HERE}/tables/zeneng_v88_tables.json", "rb").read()).hexdigest()[:16], cmd=f"PYTHONHASHSEED=0 python3 melody_v3_p36.py {N} {MODE}")
    print("rerun:", rerun)
    pickle.dump(dict(would=would, spread={k: list(v) for k, v in spread.items()}, alive=alive[:40], deaths=deaths, made=made, survivors=len(alive), order_fp=order,
                     rerun=rerun, spans=SPANS, nbars=NBARS, form=FORM, chords=CHORD), open(f"{HERE}/melody_v3_{MODE}.pkl", "wb"))
