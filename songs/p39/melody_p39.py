"""Fixed by Fall (song 39): the melody search under ZenEng v103. Rock with a swagger: 4/4 at q = 108, a shuffle (eighths written
straight, played swung) in the verses, bridge and solo, the choruses a straight rally march (Q12); E major; one gritty baritone
(A2-E4), double-tracked as two candidates in the last chorus (Q2). No era set (Q5: the bands as fitted). Character (Q6): the verses
aimed at kept windows 1.4-2.1 on the off-beat axis (10 kept), the choruses at 1.4-2.1 on chord-bound (22 kept), the bridge free (314).
Ported as for song 38 (225/226/243, 249, 251, 227, 228, 230-232, 239/240/246-248, 244/216, 208, 252-255); 242 not set.
  The summit (the writer's A at Q9): E4 on 'Vote', beat 1 of each chorus's first bar, over E; the second line said twice a whole step
  down (D4 over D); the last chorus's unison 'Vote for us' returns it (239: its first note is the source's). Four summits.
  The tag 'Fixed by fall.' designed: G#3 - F#3 - E3, falling, deadpan.
  Verse plans for eight lines: lines 1-4 from the plan list, lines 5-8 either a varied return of 1-4 (239) or fresh.
Usage: PYTHONHASHSEED=0 python3 melody_p39.py N [main|ctl]     ctl: 243 off (every build aimed at its pool's medians)."""
import sys, os, json, math, random, pickle, hashlib, collections, platform, inspect
import numpy as np
from scipy.stats import norm
_MODE = sys.argv[2] if len(sys.argv) > 2 else "main"; _N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
sys.argv = [sys.argv[0], "1", "main"]
sys.path[:0] = ["/home/claude/p39", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyric_p39 as L
import judges as J
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec
MODE = _MODE; HERE = "/home/claude/p39"
F = dict(f243=MODE == "main")
DT = json.load(open(f"{HERE}/tables/zeneng_v96_discriminator_tables.json")); DM = DT["measures"]
AX = json.load(open(f"{HERE}/tables/zeneng_v97_axes_of_character.json"))
TR = json.load(open(f"{HERE}/tables/zeneng_v103_selector.json"))["judges, ready to use"]["training rows"]
ERA = json.load(open(f"{HERE}/tables/zeneng_v101_band_returns_eras.json"))
ERA = [v for k, v in ERA.items() if k.startswith("era_settings")][0]["CLASSIC (to 1979)"]

# ---- the key, the chords, the form ----
BAR, BEAT = 48, 12
M.TONIC = 4; M.SCALE = {4, 6, 8, 9, 11, 1, 3}; M.SUNGPC = M.SCALE | {7, 2}           # flat 3 (G) and flat 7 (D), as 200 allows
M.CH = {"E": (4, {4, 8, 11}), "A": (9, {9, 1, 4}), "B": (11, {11, 3, 6}), "C#m": (1, {1, 4, 8}), "F#m": (6, {6, 9, 1}), "D": (2, {2, 6, 9})}
M.ROMAN = {"E": "I", "A": "IV", "B": "V", "C#m": "vi", "F#m": "ii", "D": "bVII"}
M.QBPM = 108; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 45; SUMMIT = 64; M.SUMMIT = SUMMIT
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
CHOR8 = ["E", "A", "D", "A", "C#m", "A", "B", "E"]
VERSE16 = ["E", "E", "A", "E", "E", "D", "A", "E", "E", "E", "A", "E", "C#m", "A", "B", "B"]
PLAN = {"Intro": ["E", "D", "A", "E"], "Verse": VERSE16, "Chorus": CHOR8, "LastChorus": CHOR8 + CHOR8 + ["E", "E"],
        "Bridge": ["C#m", "A", "E", "B", "C#m", "A", "F#m", "B"], "Solo": CHOR8, "Outro": ["E", "D", "A", "E"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 16), ("Chorus 1", "Chorus", 8), ("Verse 2", "Verse", 16), ("Chorus 2", "Chorus", 8),
        ("Bridge", "Bridge", 8), ("Solo", "Solo", 8), ("Last Chorus", "Chorus", 18), ("Outro", "Outro", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else kind]; b += nb
NBARS = b; assert NBARS == 90 and len(CHORD) == NBARS
STOP_BARS = set()
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Last Chorus"]
M.FORM, M.PLAN, M.BAR0, M.CHORD, M.NBARS, M.KIND, M.SUNG = FORM, PLAN, BAR0, CHORD, NBARS, KIND, SUNG
M.SPANS8 = [(s, 0) for s in SUNG if SECLEN[s] >= 8] + [(s, 8) for s in SUNG if SECLEN[s] >= 16]; M.SPANS16 = [s for s in SUNG if SECLEN[s] >= 16]
SECS = 60 / M.QBPM * 4 * NBARS

# ---- the stress reading (194, 223; the writer's chant) ----
_W1 = {}
def _mono(w):
    if w not in _W1: _W1[w] = len(M.E.syllables(w)) == 1
    return _W1[w]
UNSTRESS_FIRST = {"downstairs"}                                                       # down-STAIRS, as said
def syl(text):
    out = M.syl(text); words = []
    for i, (w, s) in enumerate(out):
        if words and words[-1][0] == w and words[-1][2] == i - 1: words[-1][1].append(i); words[-1][2] = i
        else: words.append([w, [i], i])
    for wi, (w, idx, _) in enumerate(words):
        core = w.strip(",.;:—'\"").lower()
        if core in UNSTRESS_FIRST and len(idx) == 2: out[idx[0]][1] = False; out[idx[1]][1] = True; continue
        if len(idx) == 2 and out[idx[0]][1] and out[idx[1]][1] and wi != len(words) - 1:
            if any(_mono(core[:k]) and _mono(core[k:]) for k in range(2, len(core) - 1)): out[idx[1]][1] = False
    return out
M.WORDS_OF = dict(L.SECTIONS)
LINES = {s: [syl(t.replace('"', "")) for _, t in M.WORDS_OF[s]] for s in SUNG}
M.LINES = LINES
def line_start(sec, i): return (BAR0[sec] + 2 * i) * BAR
CHANT = set()
TAG = ("Last Chorus", 8)                                                              # 'Fixed by fall.'

# ---- 225/226/243: targets are one whole kept window ----
KR = [dict(zip(TR["measures"], r)) for r in TR["kept_real"]]
def axes_of(f):
    z = []
    for m in AX["measures"]:
        v = f.get(m, np.nan) if f else np.nan; q = AX["percentiles"][m]
        if v is None or not np.isfinite(v): z.append(0.0); continue
        z.append(norm.ppf(np.clip(np.interp(v, q, AX["percentile_grid"]), 1, 99) / 100))
    return (np.array(z) @ np.array(AX["projection"]) / np.array(AX["axis_sd"])).round(3).tolist()
AXN = [a["name"] for a in AX["axes"]]
KAX = [axes_of(r) for r in KR]
POOL = {"V": [i for i, a in enumerate(KAX) if 1.4 <= a[5] <= 2.1],                    # off-beat (Q6), the verses
        "C": [i for i, a in enumerate(KAX) if 1.4 <= a[1] <= 2.1],                    # chord-bound (Q6), the choruses
        "B": list(range(len(KR)))}                                                    # the bridge, free
AIMED = ["repeat", "step", "third", "fourth_fifth", "past_fifth", "chord_tones_on_beat", "chord_tones_off_beat", "gap_eighth", "gap_quarter",
         "longest_over_median_note", "notes_per_bar", "on_tonic", "on_third", "on_fifth", "on_beat3", "on_beats_2_4", "turns_per_move"]
MED = {p: {k: (float(np.nanmedian([KR[i][k] for i in POOL[p]])) if k in TR["measures"] else float(DM[k]["chart"][2])) for k in AIMED} for p in POOL}
NOT_IN_ROWS = [k for k in AIMED if k not in TR["measures"]]                            # read from the chart median (the rows lack them)
def draw_targets(rng, p):
    if F["f243"]:
        i = rng.choice(POOL[p]); t = {k: KR[i].get(k, np.nan) for k in AIMED}
        for k in AIMED:
            if not np.isfinite(t[k]): t[k] = MED[p][k]
        return i, t
    return None, dict(MED[p])

# ---- 249: knobs, calibrated on this song ----
KNOB0 = {k: 1.0 for k in ("repeat", "step", "third", "fourth_fifth", "larger", "ct_on", "ct_off", "on_tonic", "on_third", "on_fifth", "turn",
                          "beat3", "beats24", "gap8", "gap4")}
KNOBS = {"V": dict(KNOB0), "C": dict(KNOB0), "B": dict(KNOB0)}
GAMMA = 1.5
def rel(t, p, k): return max(0.05, t[k]) / max(0.05, MED[p][k])
class Aim:
    def __init__(self, t, p):
        self.t, self.p = t, p; K = KNOBS[p]; r = lambda k: rel(t, p, k) ** GAMMA
        self.cat = dict(repeat=K["repeat"] * r("repeat"), step=K["step"] * r("step"), third=K["third"] * r("third"),
                        fourth_fifth=K["fourth_fifth"] * r("fourth_fifth"), larger=K["larger"] * r("past_fifth"))
        self.cw = (K["ct_on"] * r("chord_tones_on_beat"), 1.0, K["ct_off"] * r("chord_tones_off_beat"), 1.0)
        self.deg = {0: K["on_tonic"] * r("on_tonic"), 3: K["on_third"] * r("on_third"), 4: K["on_third"] * r("on_third"), 7: K["on_fifth"] * r("on_fifth")}
        self.turn = K["turn"] * r("turns_per_move")
        self.b3, self.b24 = K["beat3"] * r("on_beat3"), K["beats24"] * r("on_beats_2_4")
        self.tilt = {6: K["gap8"] * r("gap_eighth"), 12: K["gap4"] * r("gap_quarter"), 18: 1.6, 24: 1.6}
        H = min(36, max(12, 6 * t["longest_over_median_note"]))
        self.holds = {L_: math.exp(-(L_ - H) ** 2 / (2 * 9.0 ** 2)) for L_ in (12, 18, 24, 36)}
        x = max(0.0, t["notes_per_bar"] / 3.9 - 1.0)
        self.mel_inner, self.mel_final = min(0.40, 0.04 + 1.2 * x), min(0.5, 0.08 + 1.5 * x)
AIMS = {}; AIM = None
def pool_of(sec): return {"Verse": "V", "Chorus": "C", "Bridge": "B"}[KIND[sec]]

# ---- 231: where a line lands (relative to its downbeat; a two-bar slot, the hold and breath after) ----
LAND = {"b1": [48], "b3": [24, 72], "b24": [36, 60], "off": [30, 42, 54, 66]}
def land_draw(rng, sec, n_syl):
    sh = dict(b1=0.26, b3=0.20, b24=0.18, off=0.36) if KIND[sec] == "Chorus" else dict(b1=0.20, b3=0.20, b24=0.18, off=0.42)
    while True:
        k = rng.choices(list(sh), list(sh.values()))[0]; opts = [t for t in LAND[k] if (t >= 24 or n_syl <= 5) and (t <= 66 or k == "b3")]
        if opts: return rng.choice(opts)

# ---- the rhythm of a line ----
GRID = list(range(-12, 73, 6))
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None):
    end = 72 if last_max is None else min(72, last_max)
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d): return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max([k for k in range(n) if st[k]] or [n - 1]); post = n - 1 - Ls
    def A(k, t):
        m = M.mw(t); w = {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
        tm = t % BAR
        return w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0)
    tilt = AIM.tilt; fix = fix or {}
    for _ in range(14):
        tgt = fix.get(Ls) if Ls in fix else land_draw(rng, sec, n)
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

# ---- the walk: 182 with 197, 214's one draw, 215, 251's tilts ----
def chord_w(p, n, ch):
    tones = M.CH[ch][1]; on_beat = n["on"] % BEAT == 0; cw = AIM.cw
    return (cw[0] if p % 12 in tones else cw[1]) if on_beat else (cw[2] if p % 12 in tones else cw[3])
def deg_w(p): return AIM.deg.get((p - M.TONIC) % 12, 1.0)
def tri(p, ch): return (p - M.CH[ch][0]) % 12 == 6
def next_pitch(rng, prev, run, n, ch, mu, lo, hi, last_iv=None, toward=None):
    if prev is None:
        cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and not tri(p, ch)]
        return rng.choices(cands, [math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * chord_w(p, n, ch) * deg_w(p) for p in cands])[0]
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
                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0
                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p)); base += w0
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
        last_iv = (p - prev) if prev is not None else last_iv
        prev = p; out.append(p)
    return out
def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None):
    if fix and len(fix) == len(sy):                                                   # a designed rhythm
        if fix[0] < tmin: return None
        return [dict(on=U + fix[k], p=None, syl=k, slur=False, stress=sy[k][1]) for k in range(len(sy))]
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix)
    if ons is None: return None
    rows = melismas(ons, rng, 72 if last_max is None else min(72, last_max)) if not fix or len(fix) < len(sy) else [[t, k, False] for k, t in enumerate(ons)]
    return [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]

# 181's mapping, splits on the eighth grid
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

# ---- 239/246: the varied return ----
STATS = collections.Counter()
def _durs(ns):
    for j, n in enumerate(ns): n["dur"] = ns[j + 1]["on"] - n["on"] if j + 1 < len(ns) else 24
    return ns
def redraw_added(rng, ns, src_rel, U, lo, hi, notes_on):
    """246: an added note (an onset the source lacks) is drawn: repeat .28, step .48, leap .24 from the note before it."""
    on_all = set(notes_on) | {n["on"] for n in ns}
    for j, n in enumerate(ns):
        if n["on"] - U in src_rel or j == 0: continue
        prev = ns[j - 1]["p"]; ch = M.chord_for(n, on_all); kind = rng.choices(["repeat", "step", "leap"], [0.28, 0.48, 0.24])[0]
        sizes = {"repeat": [0], "step": [1, 2], "leap": [3, 4, 5]}[kind]
        opts = [prev + s * sz for sz in sizes for s in ((0,) if sz == 0 else (-1, 1))]
        nxt = ns[j + 1]["p"] if j + 1 < len(ns) else None
        opts = [p for p in opts if lo <= p <= hi and p % 12 in M.SUNGPC and not M.clash(p, ch) and not tri(p, ch) and (nxt is None or abs(nxt - p) <= 7)]
        if opts: n["p"] = rng.choice(opts); STATS["added_" + ("repeat" if n["p"] == prev else "step" if abs(n["p"] - prev) <= 2 else "leap")] += 1
        n["added"] = True
    return ns
def vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late=0.5):
    for _ in range(6):
        ns, kd = _vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late)
        if ns is not None: return ns, kd
        if kd == "align": break
    return None, kd
def _vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late=0.5):
    hi = max(hi, max(n["p"] for n in S)); lo = min(lo, min(n["p"] for n in S))
    ns = [dict(n) for n in S] if [x[0] for x in Ssy] == [x[0] for x in sy] else align(S, Ssy, sy, SU, U, tmin)
    if ns is None: return None, "align"
    if [x[0] for x in Ssy] == [x[0] for x in sy]:
        ns = [dict(n, on=n["on"] - SU + U) for n in S]
        if rng.random() >= late: return ns, "exact"
    src_rel = {n["on"] - SU for n in S}; src_p = {n["on"] - SU: n["p"] for n in S}
    ns = _durs([dict(n) for n in ns]); [n.pop("hold", None) for n in ns]
    ns = redraw_added(rng, ns, src_rel, U, lo, hi, notes_on)
    span = max(n["on"] - U for n in ns); q4 = 0.75 * span                                 # 239(c): the change in the last quarter
    if rng.random() < late:
        idx = [j for j, n in enumerate(ns) if n["on"] - U >= q4 and j > 0 and not (n["on"] % BEAT == 0 and (n["on"] - U) in src_rel)]
        for j in idx:
            prev = ns[j - 1]["p"]; ch = M.chord_for(ns[j], notes_on)
            opts = [prev + d for d in (-2, -1, 0, 1, 2, -3, 3, -4, 4) if lo <= prev + d <= hi and (prev + d) % 12 in M.SCALE and not tri(prev + d, ch)]
            if opts: ns[j]["p"] = rng.choice(opts)
    ns = repair(rng, _durs(ns), None, lo, max(hi, max(n["p"] for n in S)), notes_on, keep={j for j, n in enumerate(ns) if n["on"] - U in src_rel and n["on"] % BEAT == 0})
    if max(n["p"] for n in ns) < max(n["p"] for n in S): return None, "kept"                 # 239(f): the top note kept or higher
    sh = [j for j, n in enumerate(ns) if n["on"] - U in src_rel]
    if not sh or ns[sh[0]]["p"] != S[0]["p"]: return None, "kept"                          # 239(b): the first note kept
    shared = [(n["on"] - U) for n in ns if (n["on"] - U) in src_rel]
    rch = len({n["on"] - U for n in ns} ^ src_rel) > 0
    pch = any(src_p[n["on"] - U] != n["p"] for n in ns if n["on"] - U in src_rel) or any(n.get("added") for n in ns)
    return ns, {(False, False): "exact", (True, False): "rhythm", (False, True): "pitch", (True, True): "both"}[(rch, pch)]

# ---- 228: sung again ----
def sing_again(rng, S, Ssy, sy, SU, U, tmin, sec, lo, hi, notes_on, last_max=None, ons=None):
    """verse 1's line as contour and cadence; the rhythm fitted again to the new words; a stressed note on a beat moves a step to a
    chord tone where it lands on none."""
    if ons is None:
        ons = line_rhythm(sy, rng, tmin, sec, last_max)
        if ons is None: return None
    rows = melismas(ons, rng, 72 if last_max is None else min(72, last_max))
    ns = _durs([dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows])
    srel = [(n["on"] - SU, n["p"]) for n in S]; s0, s1 = srel[0][0], srel[-1][0]; n0, n1 = ns[0]["on"] - U, ns[-1]["on"] - U
    on_all = set(notes_on) | {n["on"] for n in ns}
    for j, n in enumerate(ns):
        x = (n["on"] - U - n0) / max(1, n1 - n0) * (s1 - s0) + s0
        n["p"] = min(srel, key=lambda e: abs(e[0] - x))[1]
    ns[-1]["p"] = S[-1]["p"]; ns[0]["p"] = S[0]["p"]
    for n in ns:
        ch = M.chord_for(n, on_all); tones = M.CH[ch][1]
        if (n["stress"] and n["on"] % BEAT == 0 and n["p"] % 12 not in tones) or tri(n["p"], ch):
            opts = [n["p"] + d for d in (-1, 1, -2, 2) if (n["p"] + d) % 12 in tones and lo <= n["p"] + d <= hi]
            if opts: n["p"] = opts[0]
    return repair(rng, ns, None, lo, hi, on_all, keep={0, len(ns) - 1})
def repair(rng, ns, prev, lo, hi, notes_on, keep=()):
    """a mapped line's leaps past a sixth, tritones and runs of four are re-walked, the other notes held."""
    for _pass in range(5):
        bad = set(); run = 1
        for j in range(1, len(ns)):
            iv = abs(ns[j]["p"] - ns[j - 1]["p"]); run = run + 1 if iv == 0 else 1
            if iv > 9 or iv == 6: bad.add(j if j not in keep else j - 1)
            if run > 3: bad |= {j, j - 1, j - 2}
        bad -= set(keep)
        if not bad: return ns
        mu = float(np.median([n["p"] for n in ns]))
        ps = walk_notes(rng, ns, prev if 0 in bad else None, 1, mu, lo, hi, notes_on, fixed={j: ns[j]["p"] for j in range(len(ns)) if j not in bad})
        if ps:
            for n, p in zip(ns, ps): n["p"] = p if p % 12 in M.SCALE or not M.clash(p, M.chord_for(n, notes_on)) else n["p"]
    return ns

# ---- 218: holds ----
END_LENS = (36, 24, 18, 12); GAP_MIN = 18; PALETTE = (6, 12, 18, 24, 36)    # 206: five lengths at most, all five offered (242)
def finish(notes, rng):
    have = collections.defaultdict(set)                                              # 242: the section's first 8 bars offered all five lengths
    for i, n in enumerate(notes[:-1]):
        if notes[i + 1]["line"] == n["line"] and "fixdur" not in n: have[n["sec"]].add(notes[i + 1]["on"] - n["on"])
    for i, n in enumerate(notes):
        nx = notes[i + 1]["on"] if i + 1 < len(notes) else None
        if "fixdur" in n: n["dur"] = n["fixdur"]; continue
        if nx is None: n["dur"] = 24
        elif notes[i + 1]["line"] != n["line"]:
            room = nx - n["on"] - 6
            if "hold" not in n:
                opts = [L_ for L_ in END_LENS if L_ <= room]
                first8 = n["on"] < (BAR0[n["sec"]] + 8) * BAR
                n["hold"] = rng.choices(opts, [AIMS[pool_of(n["sec"])].holds[L_] * (4.0 if first8 and L_ not in have[n["sec"]] else 1.0) for L_ in opts])[0] if opts else max(6, room)
                if first8: have[n["sec"]].add(max(L_ for L_ in PALETTE if L_ <= max(6, room) and L_ <= n["hold"]))
            n["dur"] = max(L_ for L_ in PALETTE if L_ <= max(6, room) and L_ <= n["hold"]) if n["hold"] >= 6 else 6
        else: n["dur"] = nx - n["on"]
    return notes

# ---- 181/219/248: the return gate on lines, on shared events ----
def unit_lines(notes, a, b2, U, keep=None):
    ns = [n for n in notes if a <= n["on"] < b2 and (keep is None or n["on"] - U in keep)]
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
def line_span(notes, sec, i):
    ln = [n for n in notes if n["line"] == f"{sec}:{i}"]
    nxt = [n for n in notes if n["line"] == f"{sec}:{i + 1}"]
    a = ln[0]["on"]; b2 = nxt[0]["on"] if nxt else max(n["on"] for n in ln) + 1
    return a, b2, line_start(sec, i)
def returns_related(c):
    out = []
    for sec, i, s0, i0, kind in c["meta"]["returns"]:
        if kind == "sung again": continue
        a, b2, U = line_span(c["notes"], sec, i); a0, b0, U0 = line_span(c["notes"], s0, i0)
        shared = {n["on"] - U for n in c["notes"] if a <= n["on"] < b2} & {n["on"] - U0 for n in c["notes"] if a0 <= n["on"] < b0}
        out.append(((sec, i, s0, i0, kind),) + related_lines(unit_lines(c["notes"], a, b2, U, shared), unit_lines(c["notes"], a0, b0, U0, shared)))
    return out
def opening_rel(notes, s1, s2):
    return related_lines(unit_lines(notes, *line_span(notes, s1, 0)), unit_lines(notes, *line_span(notes, s2, 0)))

# ---- plans (181, 205, 213) ----
VERSE_PLANS = [("ABAC", 0.4), ("ABAB", 0.3), ("ABCD", 0.2), ("AABC", 0.1)]          # lines 1-4; lines 5-8 return them or go on
BRIDGE_PLANS = [("ABAC", 0.4), ("ABCD", 0.4), ("ABCB", 0.2)]
PRE_PLANS = [("AB", 0.75), ("AA", 0.25)]
PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Bridge": ["Bridge"]}
def admissible(sec, plan):
    for i, x in enumerate(plan):
        j = plan.index(x)
        if j != i and any(abs(len(LINES[s][i]) - len(LINES[s][j])) > 3 for s in PAIRS[KIND[sec]]): return False
    return True
def draw_plan(rng, sec, plans):
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCD", 1.0)]
    return list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])
MUS = {"Verse": 52, "Chorus": 57, "Bridge": 56}
CAPS = {"Verse": 59, "Chorus": 61, "Bridge": 61}
FLOORS = {"Verse": 45, "Chorus": 49, "Bridge": 49}
SRC = {"Verse 2": "Verse 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}

def generate(rng, cal=None):
    """one build. cal: a calibration build (targets at the pools' medians)."""
    global AIM
    meta = dict(returns=[], kinds={}, win={}, targets={})
    for p in ("V", "C", "B"):
        i, t = (None, dict(MED[p])) if cal else draw_targets(rng, p)
        meta["win"][p] = i; meta["targets"][p] = t; AIMS[p] = Aim(t, p)
    p4 = draw_plan(rng, "Verse 1", VERSE_PLANS); second = rng.choice(["return", "fresh"])
    plans = dict(Verse=p4 + (["="] * 4 if second == "return" else [chr(ord(c) + 4) for c in p4]), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS), verse_second=second)
    meta["plans"] = plans
    built, lines = {}, []; prev, run, last_on = None, 0, -10 ** 6; notes_on_all = set(); pending = {}
    def place(sec, i, ns):
        nonlocal prev, run, last_on
        for n in ns: n["sec"] = sec; n["line"] = f"{sec}:{i}"
        built[(sec, i)] = ns; lines.append(ns)
        prev = ns[-1]["p"]; last_on = ns[-1]["on"]; rr = 1
        for a, b2 in zip(ns[::-1], ns[-2::-1]):
            if a["p"] == b2["p"]: rr += 1
            else: break
        run = rr
    def how(sec, i):
        """how line i of sec is made: ('copy'|'return'|'again'|'plan'|'fresh', source section, source line)."""
        kind = KIND[sec]
        if (sec, i) == TAG: return ("tag", None, None)
        if sec == "Chorus 2": return ("copy", "Chorus 1", i) if i < 3 else ("return", "Chorus 1", 3)
        if sec == "Last Chorus": return ("copy", "Chorus 1", i) if i < 4 else ("return", "Chorus 1", i - 4)
        if sec == "Verse 2": return ("again", "Verse 1", i)
        if kind == "Chorus":
            if i == 1: return ("twice", sec, 0)
            return ("fresh", None, None)
        plan = plans[kind]
        if plan[i] == "=": return ("return", sec, i - 4)
        first = plan.index(plan[i])
        return ("plan", sec, first) if first < i else ("fresh", None, None)
    def prefit(sec, i):
        """247: a copy, return or re-sung line is fitted to its words before the line ahead of it is drawn."""
        if (sec, i) in pending: return pending[(sec, i)]
        h, s0, i0 = how(sec, i); U = line_start(sec, i); r = None
        if h in ("copy", "return", "plan", "twice") and (s0, i0) in built:
            S = built[(s0, i0)]; SU = line_start(s0, i0)
            if h == "copy": r = ("ns", [dict(n, on=n["on"] - SU + U) for n in S], "exact")
            elif h == "twice": r = ("ns", [dict(n, on=n["on"] - SU + U) for n in S], "twice")
            else:
                ns, kd = vary_return(rng, S, LINES[s0][i0], LINES[sec][i], SU, U, -12, FLOORS[KIND[sec]], CAPS[KIND[sec]], notes_on_all)
                r = ("ns", ns, kd) if ns else ("fail", kd, None)
        elif h == "again" and (s0, i0) in built:
            AIMP = AIM; globals()["AIM"] = AIMS[pool_of(sec)]
            ons = line_rhythm(LINES[sec][i], rng, -12, sec); globals()["AIM"] = AIMP
            r = ("ons", ons, None) if ons else ("fail", None, None)
        if r is not None: pending[(sec, i)] = r
        return r
    for sec in SUNG:
        kind = KIND[sec]; mu, hi, lo = MUS[kind], CAPS[kind], FLOORS[kind]; sys_ = LINES[sec]; AIM = AIMS[pool_of(sec)]
        for i, sy in enumerate(sys_):
            U = line_start(sec, i); tmin = max(-12, last_on + GAP_MIN - U)
            # 212/247: the next line, fitted first, fixes how late this line may end
            nxt = (sec, i + 1) if i + 1 < len(sys_) else ((SUNG[SUNG.index(sec) + 1], 0) if SUNG.index(sec) + 1 < len(SUNG) else None)
            last_max = None
            if nxt:
                pf = prefit(*nxt)
                if pf and pf[0] == "fail": return None, ("align: the words do not fit the returning tune" if pf[1] == "align" else "return: first or top note not kept (239)")
                f0 = None
                if pf and pf[1]: f0 = (pf[1][0]["on"] - line_start(*nxt)) if pf[0] == "ns" else pf[1][0]
                elif KIND[nxt[0]] == "Chorus" and nxt[1] == 0 and how(*nxt)[0] == "fresh": f0 = 0
                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
            h, s0, i0 = how(sec, i)
            if h == "tag":                                                              # 'Fixed by fall.' (designed): G#3 - F#3 - E3
                ns = [dict(on=U + 0, p=56, syl=0, slur=False, stress=True), dict(on=U + 12, p=54, syl=1, slur=False, stress=False),
                      dict(on=U + 24, p=52, syl=2, slur=False, stress=True, fixdur=36)]
                meta["kinds"][(sec, i)] = "designed"
            elif h in ("copy", "twice", "return", "plan") and (prefit(sec, i) or ("",))[0] == "ns":
                _, ns, kd = pending[(sec, i)]; ns = [dict(n) for n in ns]
                for n in ns: n.pop("hold", None)
                if h == "twice":                                                       # said twice: a whole step down where it fits the chord
                    on_ = notes_on_all | {n["on"] for n in ns}
                    for n in ns:
                        ch = M.chord_for(n, on_); strong = n["on"] % BEAT == 0 or n["dur"] >= 12
                        opts = [n["p"] - 2, M.dshift(n["p"], -1), n["p"] - 3, n["p"] - 1, n["p"] - 4]
                        ok = [q2 for q2 in opts if q2 % 12 in M.SUNGPC and not M.clash(q2, ch) and not tri(q2, ch) and (not strong or q2 % 12 in M.CH[ch][1])]
                        n["p"] = ok[0] if ok else n["p"] - 2
                    ns = repair(rng, _durs(ns), None, lo, max(hi, max(n["p"] for n in ns)), notes_on_all, keep={0})    # no run of four from the shift
                meta["kinds"][(sec, i)] = kd
                if h in ("return", "plan"): meta["returns"].append((sec, i, s0, i0, kd))
            elif h == "again":
                pf = pending.get((sec, i)); S = built[(s0, i0)]
                if pf and pf[1] and ((last_max is not None and pf[1][-1] > last_max) or pf[1][0] < tmin): pf = None   # redrawn against the line ahead (247)
                ns = sing_again(rng, S, LINES[s0][i0], sy, line_start(s0, i0), U, tmin, sec, lo, hi, notes_on_all, last_max, ons=pf[1] if pf else None)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return None, "rhythm: no placement"
                meta["returns"].append((sec, i, s0, i0, "sung again")); meta["kinds"][(sec, i)] = "sung again"
            elif h in ("copy", "twice", "return", "plan"):
                globals().__setitem__("WHERE", (sec, i)); return None, "align: the words do not fit the returning tune"
            else:
                fix = None
                if kind == "Chorus" and i == 0: fix = {0: 0}                                # 216: 'Vote' on the chorus's first downbeat
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, fix)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return None, "rhythm: no placement"
                fixed = {}
                if kind == "Chorus" and i == 0: fixed = {0: SUMMIT}
                nf = None                                                              # the next line's first pitch, if it is already fitted
                if nxt and pending.get(nxt) and pending[nxt][0] == "ns": nf = pending[nxt][1][0]["p"]
                if nf is None and nxt and KIND[nxt[0]] == "Chorus" and nxt[1] == 0 and how(*nxt)[0] == "fresh": nf = SUMMIT   # toward 'Vote'
                if nf is not None: fixed[len(ns)] = nf
                for _try in range(8):
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fixed or None)
                    if ps is None: continue
                    if kind == "Chorus" and i == 0:                                     # the twice line opens a step down: the join from this line's end
                        if abs(ps[-1] - (SUMMIT - 2)) > 9 or abs(ps[-1] - (SUMMIT - 2)) == 6: ps = None; continue
                    if kind == "Chorus" and i == 3 and SUMMIT - ps[-1] > 12: ps = None; continue    # the last chorus's 'Vote for us' follows it
                    break
                if ps is None: globals().__setitem__("WHERE", (sec, i)); return None, "walk: no note"
                for n, p in zip(ns, ps): n["p"] = p
                meta["kinds"][(sec, i)] = "fresh"
            if nxt and h not in ("copy", "twice", "tag") and (nxt[1] == 0 and KIND[nxt[0]] == "Chorus" or nxt == ("Last Chorus", 4)) and \
               (SUMMIT - ns[-1]["p"] > 12 or SUMMIT - ns[-1]["p"] == 6):                       # the join into 'Vote': the line's last notes re-walked toward it
                k0 = max(1, len(ns) - 2); _durs(ns)
                fx = {j: ns[j]["p"] for j in range(k0)}; fx[len(ns)] = SUMMIT
                ps = walk_notes(rng, ns, prev, run, mu, lo, max(hi, 61), notes_on_all, fixed=fx)
                if ps: [n.__setitem__("p", p) for n, p in zip(ns, ps)]
            if ns[0]["on"] - last_on < GAP_MIN: globals().__setitem__("WHERE", (sec, i)); return None, "join: no held end and breath before the line (212)"
            if last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return None, "join: no held end and breath before the copy (212)"
            if prev is not None and (abs(ns[0]["p"] - prev) > 12 or abs(ns[0]["p"] - prev) == 6) and h not in ("copy", "twice", "tag"):
                pk = [j for j, n in enumerate(ns) if n["on"] < U] or [0]                # the join: the pickup (or first note) re-drawn
                if ns[pk[-1]]["p"] != SUMMIT:
                    ps = walk_notes(rng, ns, prev, run, mu, lo, max(hi, max(n["p"] for n in ns)), notes_on_all, fixed={j: ns[j]["p"] for j in range(len(ns)) if j not in pk})
                    if ps: [n.__setitem__("p", p) for n, p in zip(ns, ps)]
            for n in ns: notes_on_all.add(n["on"])
            place(sec, i, ns)
    notes = sorted([n for l in lines for n in l], key=lambda n: n["on"])
    on = {n["on"] for n in notes}
    for n in notes:
        n.setdefault("dur", 12)
        ch_ = M.chord_for(n, on)
        if n["p"] % 12 in (0, 7) and M.clash(n["p"], ch_):
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q_: (q_ % 12 not in tones, q_ % 12 not in M.SCALE))
        if tri(n["p"], ch_) and n["p"] != SUMMIT:                                          # 215: a copied note moves a step to a chord tone
            tones = M.CH[ch_][1]; n["p"] = min((n["p"] + 1, n["p"] - 1, n["p"] + 2, n["p"] - 2), key=lambda q_: (q_ % 12 not in tones, abs(q_ - n["p"])))
    finish(notes, rng)
    return dict(notes=notes, meta=meta), None

# ---- the discriminator (v96 feats on 8-bar windows) ----
MAJ = {0, 2, 4, 5, 7, 9, 11}
_P37 = open("/home/claude/p37/melody_p37.py").read()
exec(_P37[_P37.index("def feats(N, ton):"):_P37.index("def windows(notes, which=None):")], globals())
def windows(notes, which=None):
    out = []
    for s in SUNG:
        if KIND[s] not in ("Verse", "Chorus") or (which and s not in which): continue
        for k in range(0, SECLEN[s] - 7, 8): out.append((s, BAR0[s] + k))
    return out
def win_N(notes, b0):
    return [((n["on"] - b0 * BAR) / BEAT, n["dur"] / BEAT, n["p"], M.CH[M.chord_at(n["on"])][1]) for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR]
def win_feats(notes, b0): return feats(win_N(notes, b0), M.TONIC)
def win_distance(f):
    ds = []
    for k, v in DM.items():
        if not v["agree"] or f is None or k not in f or not np.isfinite(f[k]): continue
        c = v["centre_reference"]; ds.append(min(3.0, max(0.0, c["q25"] - f[k], f[k] - c["q75"]) / c["width"]))
    return float(np.mean(ds)) if ds else float("nan")
def outside_both(f):
    out = []
    for k, v in DM.items():
        x = f.get(k, np.nan) if f else np.nan
        if not np.isfinite(x): continue
        c, g = v["chart"], v["grid"]
        if (x < c[1] or x > c[3]) and (x < g[1] or x > g[3]): out.append((k, round(x, 3), "low" if x < c[1] else "high"))
    return out
def judge(notes):
    """252-254: the mean over Verse 1's and Chorus 1's windows (8 bars from the section's first bar)."""
    rows = {}
    for s in ("Verse 1", "Chorus 1"):
        N = win_N(notes, BAR0[s]); f = feats(N, M.TONIC); rows[s] = dict(J.score_window(f, N), feats=f)
    return dict(combined=float(np.mean([r["combined"] for r in rows.values()])), content=float(np.mean([r["content"] for r in rows.values()])),
                order=float(np.mean([r["order"] for r in rows.values()])), rows=rows)
ERA_K = ["notes_per_bar", "range", "repeat", "distinct_durations", "pitch_bits"]
def era_read(notes):
    W = [win_feats(notes, BAR0[s]) for s in ("Verse 1", "Chorus 1", "Bridge")]
    return {k: float(np.median([w[k] for w in W if w])) for k in ERA_K}, W

# ---- gates ----
def top(notes, s): return max(n["p"] for n in notes if n["sec"] == s)
def low(notes, s): return min(n["p"] for n in notes if n["sec"] == s)
def med(notes, s): return float(np.median([n["p"] for n in notes if n["sec"] == s]))
GATES = ["leaps: tritone or past an octave", "monotony run (166/196)", "summit placed (the writer's A; 216, 244)", "register (133)",
         "returns related, on shared events (181/219/248)", "chorus opening another tune (227)", "chorus at or above the verse, floor lifted (227)",
         "bridge opening unrelated (208)", "bridge above the verse, under the summit (208)", "no tone a tritone from the root (215)",
         "rhythm band (163)", "pitch band (153/182)", "pushed notes (159)", "density (159)", "sequence legs (148)",
         "key word on a chord tone (134)", "note lengths <= 5 per 8 bars (206)", "the judge's floor (254)"]
def gate_fails(c, jd=None):
    notes = c["notes"]; ps = [n["p"] for n in notes]; f = {}; on = {n["on"] for n in notes}
    rb = M.rhythm_bits(notes)
    if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): f["rhythm band (163)"] = round(rb, 3)
    pb = M.pitch_bits(ps)
    if not (M.PBAND["p05"] <= pb <= M.PBAND["p95"]): f["pitch band (153/182)"] = round(pb, 3)
    if M.pushed_share(notes) > 0.42: f["pushed notes (159)"] = 1
    de = len(notes) / sum(SECLEN[s] * 4 * 60 / M.QBPM for s in SUNG)
    if not (1.1 <= de <= 4.9): f["density (159)"] = de
    if any(l >= 3 for l in M.sequences(notes)): f["sequence legs (148)"] = 1
    if M.keyword_chord(notes)[0] < 0.40: f["key word on a chord tone (134)"] = 1
    if any(top(notes, h) < top(notes, v) for v, h in (("Verse 1", "Chorus 1"), ("Verse 2", "Chorus 2"), ("Verse 2", "Last Chorus"))): f["register (133)"] = 1
    summ = [n for n in notes if n["p"] == SUMMIT]
    want = {"Chorus 1:0", "Chorus 2:0", "Last Chorus:0", "Last Chorus:4"}
    if len(summ) != 4 or max(ps) > SUMMIT or {n["line"] for n in summ} != want or any(n["on"] % BAR or n["syl"] != 0 or M.chord_for(n, on) != "E" for n in summ):
        f["summit placed (the writer's A; 216, 244)"] = len(summ)
    w, _ = M.monotony(notes)
    if w > 3: f["monotony run (166/196)"] = w
    mx, tr = M.leaps(notes)
    if mx > 12 or tr: f["leaps: tritone or past an octave"] = (mx, tr)
    rr = [r for r in returns_related(c) if not r[1]]
    if rr: f["returns related, on shared events (181/219/248)"] = rr[0][0]
    if opening_rel(notes, "Chorus 1", "Verse 1")[0]: f["chorus opening another tune (227)"] = 1
    if med(notes, "Chorus 1") < med(notes, "Verse 1") or low(notes, "Chorus 1") <= low(notes, "Verse 1"): f["chorus at or above the verse, floor lifted (227)"] = 1
    if opening_rel(notes, "Bridge", "Verse 1")[0] or opening_rel(notes, "Bridge", "Chorus 1")[0]: f["bridge opening unrelated (208)"] = 1
    if not med(notes, "Bridge") > med(notes, "Verse 1") or top(notes, "Bridge") >= SUMMIT: f["bridge above the verse, under the summit (208)"] = 1
    if any(tri(n["p"], M.chord_for(n, on)) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in notes): f["no tone a tritone from the root (215)"] = 1
    if any(len({n["dur"] for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) > 5 for b0 in range(NBARS - 7)): f["note lengths <= 5 per 8 bars (206)"] = 1
    jd = jd or judge(notes)
    if jd["combined"] < J.FLOOR: f["the judge's floor (254)"] = round(jd["combined"], 3)
    return f
def evaluate(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    if min(ps) < M.LO or max(ps) > SUMMIT: return ("range", (min(ps), max(ps))), None
    f = gate_fails(c, c.get("judge"))
    for g in GATES:
        if g in f: return (g, f[g]), None
    V = M.sec_notes(notes, "Verse 1"); H = [n for n in M.sec_notes(notes, "Chorus 1") if n["on"] < (BAR0["Chorus 1"] + 8) * BAR]
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

# ---- readings for each build ----
def reading(c):
    notes = c["notes"]; Wv = win_feats(notes, BAR0["Verse 1"]); Wc = win_feats(notes, BAR0["Chorus 1"])
    er, _ = era_read(notes); r = dict(v=Wv, c=Wc, era=er, ax_v=axes_of(Wv), ax_c=axes_of(Wc), ax_b=axes_of(win_feats(notes, BAR0["Bridge"])),
                                      dist=float(np.mean([win_distance(Wv), win_distance(Wc)])), outside=len(outside_both(Wv)) / 2 + len(outside_both(Wc)) / 2)
    return r

def calibrate(rng, n=30, rounds=3):
    """249: the knobs are set on this song so that a build aimed at its pool's medians reads near them."""
    log = []
    pairs = {"repeat": "repeat", "step": "step", "third": "third", "fourth_fifth": "fourth_fifth", "larger": "past_fifth", "ct_on": "chord_tones_on_beat",
             "ct_off": "chord_tones_off_beat", "on_tonic": "on_tonic", "on_third": "on_third", "on_fifth": "on_fifth", "turn": "turns_per_move",
             "beat3": "on_beat3", "beats24": "on_beats_2_4", "gap8": "gap_eighth", "gap4": "gap_quarter"}
    for rd in range(rounds):
        acc = {p: collections.defaultdict(list) for p in ("V", "C", "B")}; k = 0; tries = 0
        while k < n and tries < 40 * n:
            tries += 1; c, err = generate(rng, cal=True)
            if err: continue
            k += 1
            for p, s in (("V", "Verse 1"), ("C", "Chorus 1"), ("B", "Bridge")):
                f = win_feats(c["notes"], BAR0[s])
                for kn, m in pairs.items():
                    if f and np.isfinite(f.get(m, np.nan)): acc[p][kn].append(f[m])
        row = {}
        for p in ("V", "C", "B"):
            for kn, m in pairs.items():
                rd_ = float(np.mean(acc[p][kn])) if acc[p][kn] else MED[p][m]; tg = MED[p][m]
                KNOBS[p][kn] = float(np.clip(KNOBS[p][kn] * (max(0.02, tg) / max(0.02, rd_)) ** 1.0, 0.05, 20))
                row[f"{p}:{kn}"] = (round(tg, 3), round(rd_, 3), round(KNOBS[p][kn], 3))
        log.append(row)
    return log

if __name__ == "__main__":
    N = _N; SEED = 20261110 + 391
    rng = random.Random(SEED)
    cal_log = calibrate(random.Random(SEED + 1))
    made, deaths, alive, allb = 0, collections.Counter(), [], []
    would = collections.Counter()
    STATS.clear()
    while made < N:
        c, err = generate(rng); made += 1
        if err: deaths[err] += 1; continue
        c["judge"] = judge(c["notes"]); fails = gate_fails(c, c["judge"])
        for g in fails: would[g] += 1
        r = reading(c); c["read"] = r
        allb.append(dict(meta=c["meta"], read=r, judge={k: c["judge"][k] for k in ("combined", "content", "order")}, fails=list(fails),
                         kinds=dict(c["meta"]["kinds"]), notes=[(n["on"], n["dur"], n["p"], n["sec"], n["line"], n["stress"], n["syl"]) for n in c["notes"]]))
        cert, m = evaluate(c)
        if cert: deaths[cert[0]] += 1; continue
        c["meas"] = m; c["fp"] = M.fingerprint(c); alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    byj = sorted(alive, key=lambda c: (-c["judge"]["combined"], c["fp"])); short = byj[:max(1, len(byj) // 2)]       # 255
    sfp = {c["fp"] for c in short}; pick = next(c for c in alive if c["fp"] in sfp) if alive else None
    print(f"[{MODE}] {NBARS} bars; built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order {order}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in GATES]
    if alive:
        for lab, c in (("composite first", alive[0]), ("shortlist pick", pick), ("judge first", byj[0])):
            print(f"{lab:16s} {c['fp']} comp {c['meas']['composite']:.3f} judge {c['judge']['combined']:.3f} (content {c['judge']['content']:.3f}, order {c['judge']['order']:.3f})"
                  f" plans {c['meta']['plans']}")
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{HERE}/lyric_p39.py", "rb").read() + open(f"{HERE}/judges.py", "rb").read()
                        + open("/home/claude/p36/melody_p36.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, calibration_seed=SEED + 1, N=N, mode=MODE, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(),
                 numpy=np.__version__, tables={f: hashlib.sha256(open(f"{HERE}/tables/{f}", "rb").read()).hexdigest()[:16] for f in sorted(os.listdir(f"{HERE}/tables"))},
                 cmd=f"PYTHONHASHSEED=0 python3 melody_p39.py {N} {MODE}")
    print("rerun:", rerun)
    pickle.dump(dict(would=would, deaths=deaths, made=made, survivors=len(alive), order_fp=order, alive=alive[:60], short=[c["fp"] for c in short],
                     pick=pick, comp_first=alive[0] if alive else None, judge_first=byj[0] if byj else None, all=allb, stats=dict(STATS),
                     calibration=cal_log, knobs=KNOBS, rerun=rerun, form=FORM, chords=CHORD, all_alive_judge=[(c["fp"], c["judge"]["combined"], c["meas"]["composite"]) for c in alive]),
                open(f"{HERE}/melody_{MODE}.pkl", "wb"))
