"""Windows Down (song 37): the melody search under ZenEng v96. Rock class, heartland drive: 4/4, q = 122, A major, male baritone.
Ported before the search, in the order given:
  224  each build's targets drawn from the kept middle halves (chart pop, Table CU / the v96 discriminator file) and recorded:
       interval shares, chord tones on and off the beat, eighth- and quarter-note gaps, the line-end hold (through the longest note
       over the median), notes a bar. The walk, the rhythm draw, the holds and the melismas are aimed at the build's own point.
  212  line ends before copies: a line followed by a copy is drawn knowing the copy's first onset, so its held end and breath finish
       before the copy's pickup.
  214  the chord term as one draw over every candidate pitch (each interval category tilted by the chord it offers).
  215  no sung note a tritone from its chord's root on a beat or held a quarter or longer; a copied note moves a step to a chord tone.
  216  the summit (the writer's A): F#4 on 'hollering' (chorus line 4's first stress) in every chorus pass, on the line's downbeat,
       over D (the bar's chord holds F#).
  217  copies count from the end of their line (two-bar lines here, so a copy keeps its place); every chorus's last line lands on
       the tonic.
  218  ~4 syllables a bar; line ends held one of three lengths (a quarter, a dotted quarter, a half); quarters inside lines too.
  219  the 181 gate read on lines, onsets and contour from the line's own downbeat.
  223  a compound of two monosyllables takes its primary on the first part only, except at a line's end.
  Kept from earlier: 181/195 returns, 182 walk, 196 run clause, 197 turn after a leap, 200 flat 3/7, 205 plans (213: the chorus
  offered by the lyric), 208 bridge gate and register (the writer's A: lifted), 209 (riff_p37.py), 210/211 (readings).
  220: every section a multiple of four bars, every line two bars (no three-bar line chosen).
Usage: PYTHONHASHSEED=0 python3 melody_p37.py N [main|ctl]     ctl: 224 off (every build aimed at the kept medians)."""
import sys, os, json, math, random, pickle, hashlib, collections, platform, itertools, inspect
import numpy as np
_MODE = sys.argv[2] if len(sys.argv) > 2 else "main"; _N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
sys.argv = [sys.argv[0], "1", "main"]
sys.path[:0] = ["/home/claude/p37", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyric_p37 as L
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec
MODE = _MODE; HERE = "/home/claude/p37"
F = dict(f224=MODE in ("main", "wide"), wide=MODE == "wide")       # wide: a probe, targets drawn from the kept 5th-95th (finding 225)
DT = json.load(open(f"{HERE}/tables/zeneng_v96_discriminator_tables.json")); DM = DT["measures"]

# ---- the key, the chords, the form (A major; 220: every section a multiple of four) ----
BAR, BEAT = 48, 12
M.TONIC = 9; M.SCALE = {9, 11, 1, 2, 4, 6, 8}; M.SUNGPC = M.SCALE | {0, 7}          # flat 3 (C) and flat 7 (G), as 200 allows
M.CH = {"A": (9, {9, 1, 4}), "E": (4, {4, 8, 11}), "F#m": (6, {6, 9, 1}), "D": (2, {2, 6, 9}), "Bm": (11, {11, 2, 6}), "C#m": (1, {1, 4, 8})}
M.ROMAN = {"A": "I", "E": "V", "F#m": "vi", "D": "IV", "Bm": "ii", "C#m": "iii"}
M.QBPM = 122; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 50; SUMMIT = 66; M.SUMMIT = SUMMIT
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
CHOR8 = ["A", "E", "F#m", "D", "A", "E", "D", "A"]                     # line 4 opens on D (the summit's chord) and closes on A
PLAN = {"Intro": ["A", "D", "A", "E", "A", "D", "A", "E"], "Verse": ["A", "A", "D", "A", "F#m", "D", "E", "E"], "Pre": ["D", "E", "F#m", "E"],
        "Chorus": CHOR8 + CHOR8, "Bridge": ["F#m", "D", "A", "E", "F#m", "D", "Bm", "E"], "Solo": CHOR8 + CHOR8, "Outro": CHOR8}
FORM = [("Intro", "Intro", 8), ("Verse 1", "Verse", 8), ("Pre 1", "Pre", 4), ("Chorus 1", "Chorus", 16), ("Verse 2", "Verse", 8), ("Pre 2", "Pre", 4),
        ("Chorus 2", "Chorus", 16), ("Bridge", "Bridge", 8), ("Solo", "Solo", 16), ("Last Chorus", "Chorus", 16), ("Outro", "Outro", 8)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 112 and all(nb % 4 == 0 for _, _, nb in FORM)
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"]
M.FORM, M.PLAN, M.BAR0, M.CHORD, M.NBARS, M.KIND, M.SUNG = FORM, PLAN, BAR0, CHORD, NBARS, KIND, SUNG
M.SPANS8 = [(s, 0) for s in SUNG if SECLEN[s] >= 8] + [(s, 8) for s in SUNG if SECLEN[s] >= 16]; M.SPANS16 = [s for s in SUNG if SECLEN[s] >= 16]
SECS = 60 / M.QBPM * 4 * NBARS

# ---- the stress reading (194, 223) ----
_W1 = {}
def _mono(w):
    if w not in _W1: _W1[w] = len(M.E.syllables(w)) == 1
    return _W1[w]
def syl(text):
    """M.syl (191, 194) and 223: a compound of two monosyllables ('someday', 'somewhere') takes the primary on its first part only,
    except as the line's last word."""
    out = M.syl(text); words = []
    for i, (w, s) in enumerate(out):
        if words and words[-1][0] == w and words[-1][2] == i - 1 and len(words[-1][1]) == 1: words[-1][1].append(i); words[-1][2] = i
        elif words and words[-1][0] == w and words[-1][2] == i - 1: words[-1][1].append(i); words[-1][2] = i
        else: words.append([w, [i], i])
    for wi, (w, idx, _) in enumerate(words):
        if len(idx) == 2 and out[idx[0]][1] and out[idx[1]][1] and wi != len(words) - 1:
            core = w.strip(",.;:—'\"").lower()
            if any(_mono(core[:k]) and _mono(core[k:]) for k in range(2, len(core) - 1)): out[idx[1]][1] = False
    return out
M.WORDS_OF = dict(L.SECTIONS)
LINES = {s: [syl(t.replace('"', "")) for _, t in M.WORDS_OF[s]] for s in SUNG}
M.LINES = LINES
def line_start(sec, i): return (BAR0[sec] + 2 * i) * BAR

# ---- 224: the build's targets ----
def q(name, lo=25, hi=75):
    c = DM[name]["chart"]; return dict(zip((5, 25, 50, 75, 95), c))[lo], dict(zip((5, 25, 50, 75, 95), c))[hi]
TARGETS = ["repeat", "step", "third", "fourth_fifth", "past_fifth", "chord_tones_on_beat", "chord_tones_off_beat", "gap_eighth", "gap_quarter",
           "longest_over_median_note", "notes_per_bar"]
def draw_targets(rng):
    t = {}
    for k in TARGETS:
        a, b2 = q(k, 5, 95) if F["wide"] else q(k)
        t[k] = rng.uniform(a, b2) if F["f224"] else dict(zip((5, 25, 50, 75, 95), DM[k]["chart"]))[50]
    s = sum(t[k] for k in ("repeat", "step", "third", "fourth_fifth", "past_fifth"))
    for k in ("repeat", "step", "third", "fourth_fifth", "past_fifth"): t[k] /= s
    return {k: round(v, 4) for k, v in t.items()}
CG = M.CG
AIM0 = dict(repeat=1.25, step=2.8, third=0.6, fourth_fifth=0.25, larger=0.45)        # recalibrated on this song so each build reads near its own targets (224)
if os.environ.get("AIM0"): AIM0.update(zip(("repeat", "step", "third", "fourth_fifth", "larger"), map(float, os.environ["AIM0"].split(","))))
CW0 = (2.5, 0.38, 5.0, 1.0); BASE_ON, BASE_OFF = float(os.environ.get("BON", "0.74")), float(os.environ.get("BOFF", "0.65"))
G6_K = float(os.environ.get("G6K", "2.0")); BASE_G8 = float(os.environ.get("BASEG8", "0.70"))
TG_HI, TG_W = float(os.environ.get("TGHI", "0.70")), float(os.environ.get("TGW", "0.30"))
MEL0 = float(os.environ.get("MEL0", "0.0")); Q_BASE = float(os.environ.get("QB", "0.30")); L_TILT = float(os.environ.get("LT", "2.0"))
def odds(x): x = min(0.97, max(0.03, x)); return x / (1 - x)
class Aim:
    """a build's aim: the walk's category weights, the chord term, the rhythm's gap tilt, the holds and melismas, from its targets."""
    def __init__(self, t):
        self.t = t
        cg = dict(repeat=CG["repeat"], step=CG["step"], third=CG["third"], fourth_fifth=CG["fourth_fifth"], larger=CG["larger"])
        tt = dict(repeat=t["repeat"], step=t["step"], third=t["third"], fourth_fifth=t["fourth_fifth"], larger=t["past_fifth"])
        self.cat = {c: AIM0[c] * tt[c] / cg[c] for c in cg}
        r_on = CW0[0] / CW0[1] * odds(t["chord_tones_on_beat"]) / odds(BASE_ON); r_off = CW0[2] / CW0[3] * odds(t["chord_tones_off_beat"]) / odds(BASE_OFF)
        self.cw = (r_on, 1.0, r_off, 1.0)
        g = (odds(t["gap_eighth"]) / odds(BASE_G8)) ** G6_K
        self.tilt = {6: g, 12: t["gap_quarter"] / Q_BASE, 18: L_TILT, 24: L_TILT}
        p72 = min(0.85, max(0.05, (TG_HI - t["gap_eighth"]) / TG_W))                 # 218: a line that lands later spreads its syllables into quarters
        self.tg = [(48, (1 - p72) * 0.8), (72, p72), (24, (1 - p72) * 0.12), (60, (1 - p72) * 0.08)]
        H = min(24, max(12, 6 * t["longest_over_median_note"]))
        self.holds = {L_: math.exp(-(L_ - H) ** 2 / (2 * 4.0 ** 2)) for L_ in (12, 18, 24)}
        x = max(0.0, t["notes_per_bar"] / 3.9 - 1.0)
        self.mel_inner, self.mel_final = min(0.45, MEL0 + 1.2 * x), min(0.6, MEL0 + 0.05 + 1.5 * x)
AIM = None                                                                     # set per build

# ---- the rhythm of a line (two bars; 218's eighths and quarters; 212's limit; 216's fixed onset) ----
GRID = list(range(-12, 73, 6))
def line_rhythm(sy, rng, tmin, last_max=None, fix=None, cadence=False):
    end = 72 if last_max is None else min(72, last_max)
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d): return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max(k for k in range(n) if st[k]); post = n - 1 - Ls
    def A(k, t):
        m = M.mw(t)
        return {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
    tilt = AIM.tilt
    tg = AIM.tg if not cadence else [(48, 0.7), (72, 0.3)]
    fix = fix or {}
    for _ in range(10):
        tgt = rng.choices([t for t, _ in tg], [w for _, w in tg])[0]
        if tgt + 6 * post > end or tgt - 6 * Ls < tmin: continue
        G = [t for t in GRID if tmin <= t <= end]
        alpha = [dict() for _ in range(n)]
        for t in G:
            if t > tgt: break
            if Ls == 0 and t != tgt: continue
            if 0 in fix and t != fix[0]: continue
            if st[0] and t < 0: continue                                         # a stressed syllable is never a pickup
            alpha[0][t] = (1.0 if t < 0 else (0.35 if t == 0 else 0.5)) * A(0, t)
        for k in range(1, n):
            for t in G:
                if k == Ls and t != tgt: continue
                if k < Ls and t >= tgt: continue
                if k in fix and t != fix[k]: continue
                if st[k] and t < 0: continue
                s = 0.0
                for tp, a in alpha[k - 1].items():
                    d = t - tp
                    if 6 <= d <= 24: s += a * M.RT[tp % BAR][d] * H(k - 1, d) * tilt.get(d, 1.0)
                if s > 0: alpha[k][t] = s * A(k, t)
        if not alpha[n - 1]: continue
        ks = list(alpha[n - 1]); ws = [alpha[n - 1][t] * (1.0 + (end - t) / 40) for t in ks]
        ons = [rng.choices(ks, ws)[0]]
        for k in range(n - 1, 0, -1):
            t = ons[-1]; ks = [tp for tp in alpha[k - 1] if 6 <= t - tp <= 24]
            ws = [alpha[k - 1][tp] * M.RT[tp % BAR][t - tp] * H(k - 1, t - tp) * tilt.get(t - tp, 1.0) for tp in ks]
            ons.append(rng.choices(ks, ws)[0])
        ons.reverse(); return ons
    return None
def melismas(ons, rng, end):
    rows = []
    for k, t in enumerate(ons):
        rows.append([t, k, False]); nxt = ons[k + 1] if k + 1 < len(ons) else None
        if nxt is None:
            if t + 6 <= end and rng.random() < AIM.mel_final: rows.append([t + 6, k, True])
        elif nxt - t >= 12 and rng.random() < AIM.mel_inner: rows.append([t + (nxt - t) // 2 // 6 * 6, k, True])
    return rows

# ---- the walk: 182 with 197, 214's one draw, 215 ----
def chord_w(p, n, ch):
    tones = M.CH[ch][1]; on_beat = n["on"] % BEAT == 0; cw = AIM.cw
    return (cw[0] if p % 12 in tones else cw[1]) if on_beat else (cw[2] if p % 12 in tones else cw[3])
def tri(p, ch): return (p - M.CH[ch][0]) % 12 == 6
def next_pitch(rng, prev, run, n, ch, mu, lo, hi, last_iv=None, toward=None):
    if prev is None:
        cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and not tri(p, ch)]
        return rng.choices(cands, [math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * chord_w(p, n, ch) for p in cands])[0]
    cats = [(c, AIM.cat[c], sz) for c, _, sz in M.CATS]
    if last_iv is not None and abs(last_iv) > 7: cats = [x for x in cats if x[0] in ("step", "third")]
    allc, allw = [], []
    for c in cats:
        cands, ws, base = [], [], 0.0
        for sz in c[2]:
            for sg in ((0,) if sz == 0 else (-1, 1)):
                p = prev + sg * sz
                if not (lo <= p <= hi) or p % 12 not in M.SUNGPC or M.clash(p, ch): continue
                if tri(p, ch): continue                                                    # 215
                if sz == 0 and run >= 3: continue
                if last_iv is not None and abs(last_iv) > 7 and (sg > 0) == (last_iv > 0): continue
                if toward is not None and (abs(toward - p) > 7 or abs(toward - p) == 6): continue
                w0 = math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * M.SIZE_W.get(sz, 1.0)
                w0 *= 1.0 if sz == 0 else (M.DESC if sg < 0 else 1 - M.DESC)
                cands.append(p); ws.append(w0 * chord_w(p, n, ch)); base += w0
        if cands and base > 0 and c[1] > 0:
            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * w / base)
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]
    return None
def walk_notes(rng, notes, prev, run, mu, lo, hi, notes_on, fixed=None):
    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None
    for i, n in enumerate(notes): n["dur"] = notes[i + 1]["on"] - n["on"] if i + 1 < len(notes) else 24
    for i, n in enumerate(notes):
        if fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:
            q_ = out[-1]; ch_ = M.chord_for(n, notes_on)
            opts = [x for x in (q_ - 2, q_ - 1, q_ + 1, q_ + 2) if lo <= x <= hi and x % 12 in M.SCALE and not tri(x, ch_)]
            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) for x in opts])[0] if opts else q_
        else:
            tw = fixed.get(i + 1) if fixed else None
            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw)
            if p is None: return None
        run = run + 1 if p == prev else 1
        last_iv = (p - prev) if prev is not None else None
        prev = p; out.append(p)
    return out
def fresh_line(sy, rng, U, tmin, last_max=None, fix=None, cadence=False):
    ons = line_rhythm(sy, rng, tmin, last_max, fix, cadence)
    if ons is None: return None
    rows = melismas(ons, rng, 72 if last_max is None else min(72, last_max))
    return [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]

# 181's mapping, splits on the eighth grid (v3's align3)
_src = inspect.getsource(M.align) + inspect.getsource(M._align)
_src = (_src.replace("def align(", "def align3(").replace("def _align(", "def _align3(").replace("r = _align(", "r = _align3(")
        .replace('min(12, 72 - ev[k]["t"])', 'min(12, END_T - ev[k]["t"])').replace("if d < 6: return None", "if d < MINSPLIT: return None")
        .replace("d // 2 // 3 * 3", "d // 2 // STEP * STEP").replace("gap = 6 if t0 - 6 * npk >= max(tmin, -12) else 3", "gap = 6 if t0 - 6 * npk >= max(tmin, -12) else STEP"))
exec(_src, M.__dict__)
def align(src, src_sy, sy, U0, U, tmin):
    M.END_T = 72; M.MINSPLIT = 12; M.STEP = 6
    ns = M.align3(src, src_sy, sy, U0, U, tmin)
    if ns is None or any((n["on"] - U) % 6 for n in ns): return None
    return ns

# ---- 218: holds ----
END_LENS = (24, 18, 12); GAP_MIN = 18                                    # the shortest hold (a quarter) and an eighth's breath
def finish(notes, rng):
    for i, n in enumerate(notes):
        nx = notes[i + 1]["on"] if i + 1 < len(notes) else None
        if nx is None: n["dur"] = 24
        elif notes[i + 1]["line"] != n["line"]:
            room = nx - n["on"] - 6
            if "hold" not in n:
                opts = [L_ for L_ in END_LENS if L_ <= room]
                n["hold"] = rng.choices(opts, [AIM.holds[L_] for L_ in opts])[0] if opts else max(6, room)
            n["dur"] = min(n["hold"], max(6, room))
        else: n["dur"] = nx - n["on"]
    return notes

# ---- 195/219: the 181 gate read on lines (from v3) ----
def unit_lines(notes, a, b2, U):
    ns = [n for n in notes if a <= n["on"] < b2]
    if len(ns) < 2: return set(), [], ns
    ons = {n["on"] - U for n in ns}; body = ns[:-1]; ser = []; k = 0; cur = body[0]["p"]
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
    ln = [n for n in notes if n["line"] == f"{sec}:{i}"]
    nxt = [n for n in notes if n["line"] == f"{sec}:{i + k}"] if i + k < len(LINES[sec]) else []
    a = ln[0]["on"]; b2 = nxt[0]["on"] if nxt else max(n["on"] for n in notes if n["sec"] == sec) + 1
    return a, b2, line_start(sec, i)
def returns_related(c):
    out = []
    for sec, i, s0, i0, k in c["meta"]["returns"]:
        out.append(((sec, i, s0, i0, k),) + related_lines(unit_lines(c["notes"], *line_span(c["notes"], sec, i, k)), unit_lines(c["notes"], *line_span(c["notes"], s0, i0, k))))
    return out
def bridge_opening(notes):
    ub = unit_lines(notes, *line_span(notes, "Bridge", 0))
    return related_lines(ub, unit_lines(notes, *line_span(notes, "Verse 1", 0))), related_lines(ub, unit_lines(notes, *line_span(notes, "Chorus 1", 0)))

# ---- plans (181, 205; 213: the chorus offered by the lyric) ----
VERSE_PLANS = [("ABAC", 0.4), ("ABAB", 0.4), ("AABC", 0.1), ("AAAB", 0.1)]
BRIDGE_PLANS = [("ABAC", 0.5), ("ABCD", 0.3), ("AABC", 0.1), ("AAAB", 0.1)]
CHORUS_HEADS = [("AABC", 0.3), ("ABAC", 0.35), ("ABCD", 0.35)]
PRE_PLANS = [("AB", 0.75), ("AA", 0.25)]
PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Pre": ["Pre 1", "Pre 2"], "Chorus": ["Chorus 1"], "Bridge": ["Bridge"]}
def admissible(sec, plan):
    kind = KIND[sec]
    for i, x in enumerate(plan):
        j = plan.index(x)
        if j != i and any(abs(len(LINES[s][i]) - len(LINES[s][j])) > 3 for s in PAIRS[kind]): return False
    return True
def draw_plan(rng, sec, plans):
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCD", 1.0)]
    return list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])
MUS = {"Verse": 56, "Pre": 58, "Chorus": 61, "Bridge": 60}
CAPS = {"Verse": 62, "Pre": 64, "Chorus": 64, "Bridge": 64}
FLOORS = {"Verse": 50, "Pre": 52, "Chorus": 54, "Bridge": 54}
SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}

def copy_first_onset(built, sec, i, plan):
    """212: the first onset (relative to its line's downbeat) of line i if it is built as a copy, else None."""
    kind = KIND[sec]
    if sec in SRC and (SRC[sec], i) in built:
        S = built[(SRC[sec], i)]; return S[0]["on"] - line_start(SRC[sec], i)
    if kind == "Chorus" and i >= 4 and (sec, i - 4) in built and LINES[sec][i] == LINES[sec][i - 4]:
        S = built[(sec, i - 4)]; return S[0]["on"] - line_start(sec, i - 4)
    if i < len(plan):
        lt = plan[i]; first = plan.index(lt[0]) if lt[0] in plan else i
        if first < i and (sec, first) in built:
            S = built[(sec, first)]; return S[0]["on"] - line_start(sec, first)
    return None

def generate(rng):
    global AIM
    targets = draw_targets(rng); AIM = Aim(targets)
    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS),
                 ChorusHead=draw_plan(rng, "Chorus 1", CHORUS_HEADS), Pre=draw_plan(rng, "Pre 1", PRE_PLANS))
    plans["Chorus"] = plans["ChorusHead"] + ["="] * 4                             # lines 5-8 sing lines 1-4 again (Q12)
    built, lines = {}, []; prev, run, last_on = None, 0, -10 ** 6; notes_on_all = set()
    meta = dict(plans=plans, returns=[], shifts={}, targets=targets)
    def place(sec, i, ns):
        nonlocal prev, run, last_on
        for n in ns: n["sec"] = sec; n["line"] = f"{sec}:{i}"
        built[(sec, i)] = ns; lines.append(ns)
        prev = ns[-1]["p"]; last_on = ns[-1]["on"]; rr = 1
        for a, b2 in zip(ns[::-1], ns[-2::-1]):
            if a["p"] == b2["p"]: rr += 1
            else: break
        run = rr
    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = MUS[kind], CAPS[kind], FLOORS[kind]; sys_ = LINES[sec]
        src_sec = SRC.get(sec); plan = plans["Chorus"] if kind == "Chorus" else plans[kind]
        for i, sy in enumerate(sys_):
            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)
            # 212: the next line, if a copy, fixes how late this line may end (relative to this line's downbeat)
            nfs = []
            if i + 1 < len(sys_): nfs.append(copy_first_onset(built, sec, i + 1, plan))
            else:
                nxt = SUNG[SUNG.index(sec) + 1] if SUNG.index(sec) + 1 < len(SUNG) else None
                if nxt and line_start(nxt, 0) - U == 2 * BAR and nxt in SRC and (SRC[nxt], 0) in built:
                    nfs.append(built[(SRC[nxt], 0)][0]["on"] - line_start(SRC[nxt], 0))
            if sec == "Chorus 1" and i == 3:                       # its copy, line 8, comes right before verse 2's first line (a copy of verse 1's)
                nfs.append(built[("Verse 1", 0)][0]["on"] - line_start("Verse 1", 0))
            nfs = [x for x in nfs if x is not None]
            last_max = (2 * BAR + min(nfs) - GAP_MIN) if nfs else None
            lt = plan[i] if i < len(plan) else chr(65 + i)
            first = plan.index(lt[0]) if lt[0] in plan and lt != "=" else i
            summit_line = kind == "Chorus" and i % 4 == 3
            last_line = sec == "Last Chorus" and i == 7
            if last_line:                                                            # the writer's '(held)': I'm AL-most HOME . . . I'm AL-most HOME
                ns = fresh_line(sy, rng, U, tmin, None, {1: 0, 3: 12, 4: 36, 5: 48, 7: 72}, cadence=True)
                if ns is None: return None, "rhythm: no placement"
                ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all)
                if ps is None: return None, "walk: no note"
                for n, p in zip(ns, ps): n["p"] = p
                h1 = next(n for n in ns if n["syl"] == 3 and not n["slur"]); h1["hold"] = 24
                ns = [n for n in ns if not (n["slur"] and n["syl"] == 3)]
            elif src_sec or (kind == "Chorus" and lt == "="):
                s0, i0 = (src_sec, i) if src_sec else (sec, i - 4)
                if kind == "Chorus" and src_sec and i >= 4 and LINES[sec][i] != LINES[s0][i] and LINES[sec][i] == LINES["Chorus 1"][i - 4]: i0 = i - 4
                S = built[(s0, i0)]; Ssy = LINES[s0][i0]; SU = line_start(s0, i0)
                if [x[0] for x in Ssy] == [x[0] for x in sy]: ns = [dict(n, on=n["on"] - SU + U) for n in S]
                else:
                    ns = align(S, Ssy, sy, SU, U, tmin)
                    if ns is None: return None, "align: the words do not fit the tune"
                    meta["returns"].append((sec, i, s0, i0, 1))
                ns = [dict(n) for n in ns]
                for n in ns: n.pop("hold", None)
                if sec == "Last Chorus" and i == 7:                                # no summit on 'I'm almost home' (5 summits, the writer's A)
                    for n in ns:
                        if n["p"] > CAPS["Chorus"]: n["p"] = 62
            elif first < i and (sec, first) in built:
                S = built[(sec, first)]; Ssy = sys_[first]; SU = line_start(sec, first)
                ns = align(S, Ssy, sy, SU, U, tmin)
                if ns is None: return None, "align: the words do not fit the returning unit"
                meta["returns"].append((sec, i, sec, first, 1))
                k = rng.choices([0, 1, -1, 2, -2], [0.5, 0.15, 0.1, 0.15, 0.1])[0]
                ps = [M.dshift(n["p"], k) for n in ns]
                if max(ps) > hi or min(ps) < lo or any(abs(y - x) > 12 or abs(y - x) == 6 for x, y in zip(ps, ps[1:])): k = 0; ps = [n["p"] for n in ns]
                meta["shifts"][(sec, i)] = k
                for n, p in zip(ns, ps): n["p"] = p
                if len(ns) >= 4 and rng.random() < 0.5:
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed={j: ns[j]["p"] for j in range(len(ns) - 1)})
                    if ps is None: return None, "walk: no note"
                    for n, p in zip(ns, ps): n["p"] = p
                if last_max is not None and ns[-1]["on"] - U > last_max: return None, "join: no held end and breath before the copy (212)"
            else:
                fix = None
                if summit_line:                                                      # 216: 'hol-' on the line's downbeat
                    k0 = next(k for k, x in enumerate(sy) if x[1]); fix = {k0: 0}
                ns = fresh_line(sy, rng, U, tmin, last_max, fix, cadence=(summit_line or i == len(sys_) - 1))
                if ns is None: return None, "rhythm: no placement"
                ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all)
                if ps is None: return None, "walk: no note"
                for n, p in zip(ns, ps): n["p"] = p
            if ns[0]["on"] - last_on < GAP_MIN: return None, "join: no held end and breath before the line (212)"
            if prev is not None and (abs(ns[0]["p"] - prev) > 12 or abs(ns[0]["p"] - prev) == 6):
                pk = [j for j, n in enumerate(ns) if n["on"] < U]
                if pk:
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed={j: ns[j]["p"] for j in range(len(ns)) if j not in pk})
                    if ps: [n.__setitem__("p", p) for n, p in zip(ns, ps)]
            if summit_line and not src_sec and lt != "=" and not last_line:                          # 216: the summit F#4 over D, approach and leave by step or skip
                tgt = next(n for n in ns if n["stress"]); k_ = ns.index(tgt); tgt["p"] = SUMMIT
                if k_ > 0 and abs(ns[k_ - 1]["p"] - SUMMIT) > 7: ns[k_ - 1]["p"] = 61 if abs(ns[k_ - 1]["p"] - 61) <= 9 else 64
                for n in ns[k_ + 1:]:
                    if n["p"] > CAPS["Chorus"]: n["p"] = 64
                if k_ + 1 < len(ns) and abs(ns[k_ + 1]["p"] - SUMMIT) > 7: ns[k_ + 1]["p"] = 62
            if kind == "Chorus" and i % 4 == 3 and (not (src_sec or lt == "=") or last_line):      # 217: the chorus's last line lands on the tonic
                qn = ns[-1]["p"]; opts = [p for p in range(lo, hi + 1) if p % 12 == M.TONIC]
                ns[-1]["p"] = min(opts, key=lambda p: abs(p - qn))
            for n in ns: notes_on_all.add(n["on"])
            place(sec, i, ns)
    notes = sorted([n for l in lines for n in l], key=lambda n: n["on"])
    on = {n["on"] for n in notes}
    for n in notes:
        n.setdefault("dur", 12)
        ch_ = M.chord_for(n, on)
        if n["p"] % 12 in (0, 7) and M.clash(n["p"], ch_):
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q_: (q_ % 12 not in tones, q_ % 12 not in M.SCALE))
        if tri(n["p"], ch_) and n["p"] != SUMMIT:                                    # 215: a copied note moves a step to a chord tone
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] + 1, n["p"] - 1, n["p"] + 2, n["p"] - 2), key=lambda q_: (q_ % 12 not in tones, abs(q_ - n["p"])))
    finish(notes, rng)
    return dict(notes=notes, meta=meta), None

# ---- the discriminator (v96 file: feats() on 8-bar windows from a verse's or chorus's first bar line) ----
MAJ = {0, 2, 4, 5, 7, 9, 11}
def feats(N, ton):
    if len(N) < 12: return None
    t = np.array([n[0] for n in N]); du = np.array([n[1] for n in N]); p = np.array([n[2] for n in N]); iv = np.diff(p); a = np.abs(iv); f = {}
    f["notes_per_bar"] = len(N) / 8; f["range"] = p.max() - p.min(); f["pitch_sd"] = p.std(); f["distinct_pitches"] = len(set(p))
    f["repeat"] = (a == 0).mean(); f["step"] = ((a > 0) & (a <= 2)).mean(); f["third"] = ((a >= 3) & (a <= 4)).mean(); f["fourth_fifth"] = ((a >= 5) & (a <= 7)).mean(); f["past_fifth"] = (a > 7).mean(); f["mean_interval"] = a.mean()
    mv = iv[iv != 0]; f["ascending"] = (mv > 0).mean() if len(mv) else 0.5
    sg = np.sign(mv); f["turns_per_move"] = (sg[1:] != sg[:-1]).mean() if len(sg) > 1 else 0
    runs = []; r = 1
    for i in range(1, len(sg)):
        if sg[i] == sg[i - 1]: r += 1
        else: runs.append(r); r = 1
    runs.append(r); f["longest_run_one_way"] = max(runs) if len(sg) else 0
    lp = [i for i in range(len(iv) - 1) if abs(iv[i]) >= 5]; f["leap_then_back_by_step"] = np.mean([np.sign(iv[i + 1]) == -np.sign(iv[i]) and abs(iv[i + 1]) <= 2 for i in lp]) if len(lp) >= 2 else np.nan
    deg = (p - ton) % 12; f["on_tonic"] = (deg == 0).mean(); f["on_third"] = np.isin(deg, (3, 4)).mean(); f["on_fifth"] = (deg == 7).mean(); f["outside_scale"] = (~np.isin(deg, list(MAJ))).mean()
    f["last_note_tonic"] = float(deg[-1] == 0); f["first_note_tonic_triad"] = float(deg[0] in (0, 3, 4, 7))
    f["peak_position"] = t[int(np.argmax(p))] / 32; f["low_position"] = t[int(np.argmin(p))] / 32; f["peak_count"] = (p == p.max()).sum()
    w = du / du.sum(); f["time_in_top_third"] = w[p >= p.min() + 2 * (p.max() - p.min()) / 3].sum() if p.max() > p.min() else 0
    f["pitch_bits"] = M.pitch_bits([int(x) for x in p])
    fr = np.round((t % 1) * 12).astype(int); beat = np.floor(t + 1e-6) % 4
    f["on_downbeat"] = ((fr == 0) & (beat == 0)).mean(); f["on_beat3"] = ((fr == 0) & (beat == 2)).mean(); f["on_beats_2_4"] = ((fr == 0) & np.isin(beat, (1, 3))).mean(); f["on_offbeat_eighth"] = (fr == 6).mean(); f["on_sixteenth"] = np.isin(fr, (3, 9)).mean()
    ioi = np.diff(t); ioi = ioi[ioi > 0.01]
    f["gap_sixteenth"] = (np.abs(ioi - .25) < .04).mean(); f["gap_eighth"] = (np.abs(ioi - .5) < .04).mean(); f["gap_quarter"] = (np.abs(ioi - 1) < .04).mean(); f["gap_longer"] = (ioi > 1.04).mean()
    f["npvi"] = 100 * np.mean(np.abs(ioi[1:] - ioi[:-1]) / ((ioi[1:] + ioi[:-1]) / 2)) if len(ioi) > 2 else np.nan
    f["sounding_share"] = min(1.0, du.sum() / 32); f["longest_over_median_note"] = du.max() / np.median(du); f["distinct_durations"] = len(set(np.round(du * 12)))
    ons = set(np.round(t * 12).astype(int)); f["pushed"] = np.mean([(fr[i] != 0) and (t[i] + du[i] > np.floor(t[i]) + 1.05) and (int(round((np.floor(t[i]) + 1) * 12)) not in ons) for i in range(len(t))])
    gaps = t[1:] - (t[:-1] + du[:-1]); f["rests_of_a_beat"] = (gaps >= 1).sum(); f["first_onset"] = t[0]; f["longest_rest"] = max(0.0, gaps.max()) if len(gaps) else 0
    bars = collections.defaultdict(list)
    for i in range(len(t)): bars[int(t[i] // 4)].append((int(round((t[i] % 4) * 12)), int(p[i])))
    f["empty_bars"] = 8 - len(bars); rh = [tuple(o for o, _ in bars[b2]) for b2 in sorted(bars)]; ex = [tuple(bars[b2]) for b2 in sorted(bars)]
    f["bar_rhythm_repeats"] = np.mean([rh[i] in rh[:i] for i in range(1, len(rh))]) if len(rh) > 1 else 0; f["bar_exact_repeats"] = np.mean([ex[i] in ex[:i] for i in range(1, len(ex))]) if len(ex) > 1 else 0
    f["distinct_bar_rhythms"] = len(set(rh)); f["notes_per_bar_sd"] = np.std([len(bars.get(b2, [])) for b2 in range(8)])
    wn = [dict(on=int(round(n[0] * 12)), p=int(n[2])) for n in N]
    U = [M.unit(wn, 2 * k * BAR, 2 * BAR) for k in range(4)]
    f["unit2_returns"] = float(M.related(U[0], U[1])[0]); f["unit3_returns"] = float(M.related(U[0], U[2])[0]); f["unit4_to_unit2"] = float(M.related(U[1], U[3])[0])
    hv = [(n, i) for i, n in enumerate(N) if n[3]]
    if len(hv) >= 10:
        ct = np.array([n[2] % 12 in n[3] for n, i in hv]); onb = np.array([fr[i] == 0 for n, i in hv]); dn = np.array([fr[i] == 0 and beat[i] == 0 for n, i in hv]); lg = np.array([du[i] >= np.median(du) * 1.5 for n, i in hv])
        f["chord_tones"] = ct.mean(); f["chord_tones_on_beat"] = ct[onb].mean() if onb.sum() >= 3 else np.nan; f["chord_tones_off_beat"] = ct[~onb].mean() if (~onb).sum() >= 3 else np.nan
        f["chord_tones_on_downbeat"] = ct[dn].mean() if dn.sum() >= 3 else np.nan; f["chord_tones_on_long_notes"] = ct[lg].mean() if lg.sum() >= 3 else np.nan
        nc = [(k, i) for k, ((n, i), c) in enumerate(zip(hv, ct)) if not c and i + 1 < len(N)]
        f["non_chord_resolved_by_step"] = np.mean([0 < abs(p[i + 1] - p[i]) <= 2 and (N[i + 1][3] is not None and p[i + 1] % 12 in N[i + 1][3]) for k, i in nc]) if len(nc) >= 3 else np.nan
    return {k: float(v) for k, v in f.items()}
def windows(notes, which=None):
    out = []
    for s in SUNG:
        if KIND[s] not in ("Verse", "Chorus") or (which and s not in which): continue
        for k in range(0, SECLEN[s] - 7, 8): out.append((s, BAR0[s] + k))
    return out
def win_feats(notes, b0):
    N = [((n["on"] - b0 * BAR) / BEAT, n["dur"] / BEAT, n["p"], M.CH[M.chord_at(n["on"])][1]) for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR]
    return feats(N, M.TONIC)
def win_distance(f):
    ds = []
    for k, v in DM.items():
        if not v["agree"] or f is None or k not in f or not np.isfinite(f[k]): continue
        c = v["centre_reference"]; ds.append(min(3.0, max(0.0, c["q25"] - f[k], f[k] - c["q75"]) / c["width"]))
    return float(np.mean(ds)) if ds else float("nan")
def distance(notes):
    W = [win_feats(notes, b0) for _, b0 in windows(notes, ("Verse 1", "Chorus 1"))]
    return float(np.mean([win_distance(f) for f in W if f]))
def song_feats(notes):
    """the median over the build's verse and chorus windows, measure by measure (Table CX's reading)."""
    W = [f for f in (win_feats(notes, b0) for _, b0 in windows(notes)) if f]
    return {k: float(np.nanmedian([f.get(k, np.nan) for f in W])) if any(np.isfinite(f.get(k, np.nan)) for f in W) else float("nan") for k in DM}, W
def outside_both(sf):
    out = []
    for k, v in DM.items():
        x = sf.get(k, np.nan)
        if not np.isfinite(x): continue
        c, g = v["chart"], v["grid"]
        if (x < c[1] or x > c[3]) and (x < g[1] or x > g[3]): out.append((k, round(x, 3), "low" if x < c[1] else "high"))
    return out
def song_read(notes):
    sf, W = song_feats(notes)
    br = M.sec_notes(notes, "Bridge"); vv = M.sec_notes(notes, "Verse 1"); bo = bridge_opening(notes)
    ends = [n["dur"] for i, n in enumerate(notes) if i + 1 < len(notes) and notes[i + 1]["line"] != n["line"]]
    return dict(feats=sf, distance=distance(notes), outside=outside_both(sf), windows=len(W),
                unit3=float(np.mean([f["unit3_returns"] for f in W])), unit2=float(np.mean([f["unit2_returns"] for f in W])),
                gap_eighth=sf["gap_eighth"], gap_quarter=sf["gap_quarter"], lom=sf["longest_over_median_note"], npb=sf["notes_per_bar"],
                ct_on=sf["chord_tones_on_beat"], ct_off=sf["chord_tones_off_beat"], pitch=M.pitch_bits([n["p"] for n in notes]),
                intervals=M.interval_shares([n["p"] for n in notes]), spread=sf["notes_per_bar_sd"], end_holds=dict(collections.Counter(ends)),
                bridge_rel_verse=bo[0], bridge_rel_chorus=bo[1], bridge_median_minus_verse=float(np.median([n["p"] for n in br]) - np.median([n["p"] for n in vv])),
                bridge_onsets_ratio=(len(br) / SECLEN["Bridge"]) / (len(vv) / SECLEN["Verse 1"]), stock8=M.phrase_designs(notes)["stock8"], exact=M.repetition(notes)["exact"])

# ---- gates ----
def register_bad(notes):
    top = lambda s: max(n["p"] for n in notes if n["sec"] == s)
    return [(v, h) for v, h in (("Verse 1", "Chorus 1"), ("Verse 2", "Chorus 2"), ("Verse 2", "Last Chorus")) if top(h) < top(v)]
GATES = ["leaps: tritone or past an octave", "monotony run (166/196)", "summit placed (the writer's A; 216)", "register (133)", "returns related, on lines (181/219)",
         "bridge opening unrelated (208)", "bridge above the verse (208)", "no tone a tritone from the root (215)", "pitch band (153/182)", "rhythm band (163)",
         "pushed notes (159)", "density (159)", "sequence legs (148)", "key word on a chord tone (134)", "note lengths <= 5 per 8 bars (206)"]
def gate_fails(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]; f = {}; on = {n["on"] for n in notes}
    pb = M.pitch_bits(ps); rb = M.rhythm_bits(notes)
    if not (M.PBAND["p05"] <= pb <= M.PBAND["p95"]): f["pitch band (153/182)"] = round(pb, 3)
    if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): f["rhythm band (163)"] = round(rb, 3)
    if M.pushed_share(notes) > 0.42: f["pushed notes (159)"] = 1
    de = len(notes) / sum(SECLEN[s] * 4 * 60 / M.QBPM for s in SUNG)
    if not (1.1 <= de <= 4.9): f["density (159)"] = de
    if any(l >= 3 for l in M.sequences(notes)): f["sequence legs (148)"] = 1
    if M.keyword_chord(notes)[0] < 0.40: f["key word on a chord tone (134)"] = 1
    if register_bad(notes): f["register (133)"] = 1
    summ = [n for n in notes if n["p"] == SUMMIT]
    if len(summ) != 5 or max(ps) > SUMMIT or any(KIND[n["sec"]] != "Chorus" or int(n["line"].split(":")[1]) % 4 != 3 or n["on"] % BEAT or SUMMIT % 12 not in M.CH[M.chord_for(n, on)][1] for n in summ):
        f["summit placed (the writer's A; 216)"] = len(summ)
    w, _ = M.monotony(notes)
    if w > 3: f["monotony run (166/196)"] = w
    mx, tr = M.leaps(notes)
    if mx > 12 or tr: f["leaps: tritone or past an octave"] = (mx, tr)
    rr = [r for r in returns_related(c) if not r[1]]
    if rr: f["returns related, on lines (181/219)"] = rr[0][0]
    if any(len({n["dur"] for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) > 5 for b0 in range(NBARS - 7)): f["note lengths <= 5 per 8 bars (206)"] = 1
    bo = bridge_opening(notes)
    if bo[0][0] or bo[1][0]: f["bridge opening unrelated (208)"] = 1
    if not np.median([n["p"] for n in M.sec_notes(notes, "Bridge")]) > np.median([n["p"] for n in M.sec_notes(notes, "Verse 1")]): f["bridge above the verse (208)"] = 1
    if any(tri(n["p"], M.chord_for(n, on)) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in notes): f["no tone a tritone from the root (215)"] = 1
    return f
ORDER = GATES
def evaluate(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    if min(ps) < M.LO or max(ps) > SUMMIT: return ("range", (min(ps), max(ps))), None
    f = gate_fails(c)
    for g in ORDER:
        if g in f: return (g, f[g]), None
    V = M.sec_notes(notes, "Verse 1"); H = M.sec_notes(notes, "Chorus 1")[:sum(1 for n in M.sec_notes(notes, "Chorus 1") if n["on"] < (BAR0["Chorus 1"] + 8) * BAR)]
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
    return None, dict(composite=round(comp, 4), pitch_bits=round(M.pitch_bits(ps), 3), rhythm_bits=round(M.rhythm_bits(notes), 3), IC=ic, CMP=cmp_, M_horizon=mh, realness=real, fit=fit, lift=lift)

if __name__ == "__main__":
    N = _N; SEED = 20261110 + 371
    rng = random.Random(SEED); made, deaths, alive = 0, collections.Counter(), []
    would = collections.Counter(); spread = collections.defaultdict(list); tdraws = []; outs = []
    while made < N:
        c, err = generate(rng); made += 1
        if err: deaths[err] += 1; continue
        fails = gate_fails(c)
        for g in fails: would[g] += 1
        r = song_read(c["notes"]); tdraws.append(c["meta"]["targets"])
        for k in ("distance", "unit3", "unit2", "gap_eighth", "gap_quarter", "lom", "npb", "ct_on", "ct_off", "pitch", "spread", "bridge_median_minus_verse", "bridge_onsets_ratio", "stock8", "exact"):
            spread[k].append(float(r[k]))
        spread["outside_n"].append(len(r["outside"])); outs.append([k for k, *_ in r["outside"]])
        for k in ("repeat", "step", "larger"): spread["iv_" + k].append(r["intervals"][k])
        spread["end_hold_kinds"].append(len(r["end_holds"]))
        cert, m = evaluate(c)
        if cert: deaths[cert[0]] += 1; continue
        c["meas"] = m; c["fp"] = M.fingerprint(c); c["read"] = r; alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    print(f"[{MODE}] {NBARS} bars; built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order {order}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in GATES]
    for k, v in spread.items(): print(f"   {k}: {np.percentile(v, 5):.3f} - {np.median(v):.3f} - {np.percentile(v, 95):.3f}")
    print("   too central (builds):", f"{np.mean([x < 0.086 for x in spread['distance']]):.2f}")
    for c in alive[:5]:
        r = c["read"]; print(c["fp"], c["meta"]["plans"]["Verse"], c["meta"]["plans"]["ChorusHead"], c["meta"]["plans"]["Bridge"], f"comp {c['meas']['composite']:.3f} dist {r['distance']:.3f} out {len(r['outside'])} g8 {r['gap_eighth']:.2f} lom {r['lom']:g} on {r['ct_on']:.2f} off {r['ct_off']:.2f}")
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{HERE}/lyric_p37.py", "rb").read() + open("/home/claude/p36/melody_p36.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, N=N, mode=MODE, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(), numpy=np.__version__,
                 tables=dict(v88=hashlib.sha256(open(f"{HERE}/tables/zeneng_v88_tables.json", "rb").read()).hexdigest()[:16], v96=hashlib.sha256(open(f"{HERE}/tables/zeneng_v96_discriminator_tables.json", "rb").read()).hexdigest()[:16]),
                 cmd=f"PYTHONHASHSEED=0 python3 melody_p37.py {N} {MODE}")
    print("rerun:", rerun)
    pickle.dump(dict(would=would, spread={k: list(v) for k, v in spread.items()}, alive=alive[:40], deaths=deaths, made=made, survivors=len(alive), order_fp=order,
                     rerun=rerun, targets=tdraws, outs=outs, form=FORM, chords=CHORD), open(f"{HERE}/melody_{MODE}.pkl", "wb"))
