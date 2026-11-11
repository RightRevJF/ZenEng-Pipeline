"""Stay Tuned (song 38): the melody search rerun under ZenEng v107, a regression run (v2). v1 (melody_p38.py, v103) is kept unchanged.
The locked lyric, every intake answer, the form, key, tempo and chords as v1; seed 20261491, calibration seed 20261492; the judges'
weights as in zeneng_v103_selector.json (not refitted). Three variants:
  A  gates only: the v1 generator with 276/277 (eight limits; a build dies on a hard limit or its third soft break), 278 (comparisons
     are aims; design gates: the summit of 216/244 and the bridge's register of 208), 270 (the walk's ban on a fourth repeat and the
     repair step's re-walk of runs lifted), 264 (era: rejected only when fewer than four of five bands lie inside CLASSIC's 5th-95th),
     267 (the return gate reads what 239 builds).
  B  full v107: A plus 265/266 (chorus and bridge targets from kept windows to 1979, every aimed measure from the window; the verse
     pool keeps its 20 reciting windows of any year, the writer's Q14), 257 (line contour), 258 (widening), 259 (fresh start),
     260 with 269 (line entry at 260's rates), 262 (section endings), 268 (verse 2 with verse 1's onsets as prior), 281, 282 (said
     twice, moved whole), 271 as amended by 285 (turns aimed; beat 3 to the landing draw), 272-274 (arrangement and lyric).
  C  control: B with 243 off (each build aimed at its pool's medians).
Every build is kept on file, dead or alive: fingerprint, notes, cause of death, soft breaks, the judge's three scores.
Usage: PYTHONHASHSEED=0 python3 melody_v2_p38.py N A|B|C [tag]"""
import sys, os, json, math, random, pickle, hashlib, collections, platform, inspect
import numpy as np
from scipy.stats import norm
_MODE = sys.argv[2] if len(sys.argv) > 2 else "B"; _N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000; _TAG = sys.argv[3] if len(sys.argv) > 3 else ""
sys.argv = [sys.argv[0], "1", "main"]
sys.path[:0] = ["/home/claude/p38", "/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import melody_p36 as M
import lyric_p38 as L
import judges as J
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec
MODE = _MODE; HERE = "/home/claude/p38"; VAR = MODE; NEW = VAR in ("B", "C")
F = dict(f243=VAR != "C")
KW = json.load(open(f"{HERE}/tables/zeneng_v105_kept_windows.json"))
LIT = json.load(open(f"{HERE}/tables/zeneng_v104_line_in_time.json"))
CHK = json.load(open(f"{HERE}/tables/zeneng_v105_song38_checks.json"))
GL = json.load(open(f"{HERE}/tables/zeneng_v106_gate_limits.json"))
ERA95 = CHK["era bands and joint pass rates"]["CLASSIC (to 1979)"]["5th-95th"]["bands"]
DT = json.load(open(f"{HERE}/tables/zeneng_v96_discriminator_tables.json")); DM = DT["measures"]
AX = json.load(open(f"{HERE}/tables/zeneng_v97_axes_of_character.json"))
TR = json.load(open(f"{HERE}/tables/zeneng_v103_selector.json"))["judges, ready to use"]["training rows"]
ERA = json.load(open(f"{HERE}/tables/zeneng_v101_band_returns_eras.json"))
ERA = [v for k, v in ERA.items() if k.startswith("era_settings")][0]["CLASSIC (to 1979)"]

# ---- the key, the chords, the form ----
BAR, BEAT = 48, 12
M.TONIC = 9; M.SCALE = {9, 11, 1, 2, 4, 6, 8}; M.SUNGPC = M.SCALE | {0, 7}          # flat 3 (C) and flat 7 (G), as 200 allows
M.CH = {"A": (9, {9, 1, 4}), "E": (4, {4, 8, 11}), "F#m": (6, {6, 9, 1}), "D": (2, {2, 6, 9}), "Bm": (11, {11, 2, 6}), "G": (7, {7, 11, 2})}
M.ROMAN = {"A": "I", "E": "V", "F#m": "vi", "D": "IV", "Bm": "ii", "G": "bVII"}
M.QBPM = 132; M.SEC_PER_TW = 60 / M.QBPM / BEAT; M.LO = 47; SUMMIT = 69; M.SUMMIT = SUMMIT
M.DEG = sorted(p for p in range(36, 90) if p % 12 in M.SCALE)
RIFF = ["A", "G", "D", "A"]
CHOR8 = ["A", "D", "G", "D", "F#m", "D", "E", "E"]
PLAN = {"Intro": RIFF + RIFF[:3] + ["E"], "Verse": RIFF + RIFF[:3] + ["E"], "Pre": ["F#m", "D", "E", "E"], "Chorus": CHOR8 + CHOR8,
        "LastChorus": CHOR8 + CHOR8 + ["A", "A"], "Bridge": ["F#m", "D", "A", "E", "F#m", "D", "Bm", "E"], "Solo": CHOR8,
        "Breakdown": RIFF + RIFF, "Outro": ["A"] * 8}
FORM = [("Intro", "Intro", 8), ("Verse 1", "Verse", 8), ("Pre 1", "Pre", 4), ("Chorus 1", "Chorus", 16), ("Verse 2", "Verse", 8),
        ("Pre 2", "Pre", 4), ("Chorus 2", "Chorus", 16), ("Bridge", "Bridge", 8), ("Solo", "Solo", 8), ("Breakdown", "Breakdown", 8),
        ("Last Chorus", "Chorus", 18), ("Outro", "Outro", 8)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM: BAR0[nm] = b; CHORD += PLAN["LastChorus" if nm == "Last Chorus" else kind]; b += nb
NBARS = b; assert NBARS == 114 and len(CHORD) == NBARS
STOP_BARS = {BAR0["Last Chorus"] + 16, BAR0["Last Chorus"] + 17}                    # the band stops under 'Turn it off.' (N.C.)
KIND = {nm: kind for nm, kind, _ in FORM}; SECLEN = {nm: nb for nm, _, nb in FORM}
SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"]
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
    for i, (w, s) in enumerate(out):                                                   # 'stay TUNED, stay MAD': 'stay' is the pickup
        if w.strip(",.;:").lower() == "stay" and i + 1 < len(out): out[i][1] = False
    return out
M.WORDS_OF = dict(L.SECTIONS)
LINES = {s: [syl(t.replace('"', "")) for _, t in M.WORDS_OF[s]] for s in SUNG}
M.LINES = LINES
def line_start(sec, i): return (BAR0[sec] + 2 * i) * BAR
CHANT = {0, 1, 4}                                                                     # chorus lines sung 'Stay tuned, stay X'
TAG = ("Last Chorus", 8)                                                              # 'Turn it off.'

# ---- 225/226/243: targets are one whole kept window ----
KR = [dict(zip(TR["measures"], r)) for r in TR["kept_real"]]
KRW = [dict(zip(KW["measures"], [np.nan if x is None else x for x in r])) for r in KW["rows"]]   # 266: all 56 + 4 measures, same order
YEAR = KW["year"]
def axes_of(f):
    z = []
    for m in AX["measures"]:
        v = f.get(m, np.nan) if f else np.nan; q = AX["percentiles"][m]
        if v is None or not np.isfinite(v): z.append(0.0); continue
        z.append(norm.ppf(np.clip(np.interp(v, q, AX["percentile_grid"]), 1, 99) / 100))
    return (np.array(z) @ np.array(AX["projection"]) / np.array(AX["axis_sd"])).round(3).tolist()
AXN = [a["name"] for a in AX["axes"]]
KAX = [axes_of(r) for r in KR]
ERA4 = ("range", "repeat", "distinct_durations", "pitch_bits")
POOL = {"V": [i for i, a in enumerate(KAX) if 1.4 <= a[4] <= 2.1],                    # the reciting end (Q6, Q14)
        "C": [i for i, r in enumerate(KR) if sum(ERA[k][0] <= r[k] <= ERA[k][2] for k in ERA4) >= 3]}   # CLASSIC: inside 3 of the era's 4 bands the rows carry
if NEW:
    POOL["C"] = [i for i in range(len(YEAR)) if YEAR[i] <= 1979]                       # 265: the era's own windows (the verse keeps its 20, Q14)
    KR = KRW
AIMED = ["repeat", "step", "third", "fourth_fifth", "past_fifth", "chord_tones_on_beat", "chord_tones_off_beat", "gap_eighth", "gap_quarter",
         "longest_over_median_note", "notes_per_bar", "on_tonic", "on_third", "on_fifth", "on_beat3", "on_beats_2_4", "turns_per_move"]
MED = {p: {k: (float(np.nanmedian([KR[i][k] for i in POOL[p]])) if k in KR[0] else float(DM[k]["chart"][2])) for k in AIMED} for p in POOL}
NOT_IN_ROWS = [k for k in AIMED if k not in (KW["measures"] if NEW else TR["measures"])]                            # read from the chart median (the rows lack them)
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
KNOBS = {"V": dict(KNOB0), "C": dict(KNOB0)}
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
        self.b3land = 1.0
        if NEW: self.b3land, self.b3 = r("on_beat3"), 1.0                               # 285: beat 3 leaves the walk for 231's landing draw
        self.tilt = {6: K["gap8"] * r("gap_eighth"), 12: K["gap4"] * r("gap_quarter"), 18: 1.6, 24: 1.6}
        H = min(36, max(12, 6 * t["longest_over_median_note"]))
        self.holds = {L_: math.exp(-(L_ - H) ** 2 / (2 * 9.0 ** 2)) for L_ in (12, 18, 24, 36)}
        x = max(0.0, t["notes_per_bar"] / 3.9 - 1.0)
        self.mel_inner, self.mel_final = min(0.40, 0.04 + 1.2 * x), min(0.5, 0.08 + 1.5 * x)
AIMS = {}; AIM = None
LK = dict(amp=5.0, widen=1.0, fresh=2.0)                                              # 257/258/259 strengths, set by 249's pass (B, C)
PRIOR_W = 8.0                                                                         # 268: weight on verse 1's onsets in verse 2's rhythm walk
def pool_of(sec): return "V" if KIND[sec] in ("Verse", "Pre") else "C"

# ---- 231: where a line lands (relative to its downbeat; a two-bar slot, the hold and breath after) ----
LAND = {"b1": [48], "b3": [24, 72], "b24": [36, 60], "off": [30, 42, 54, 66]}
def land_draw(rng, sec, n_syl):
    sh = dict(b1=0.26, b3=0.20, b24=0.18, off=0.36) if KIND[sec] == "Chorus" else dict(b1=0.20, b3=0.20, b24=0.18, off=0.42)
    sh["b3"] *= AIM.b3land
    while True:
        k = rng.choices(list(sh), list(sh.values()))[0]; opts = [t for t in LAND[k] if (t >= 24 or n_syl <= 5) and (t <= 66 or k == "b3")]
        if opts: return rng.choice(opts)

# ---- the rhythm of a line ----
GRID = list(range(-12, 73, 6))
ENTRY = dict(on=0.179, after=0.525, pickup=0.143)                                  # 260: kept song medians (normalised when drawn)
ENTRY_T = dict(on=lambda t: t == 0, after=lambda t: 6 <= t <= 30, pickup=lambda t: -12 <= t <= -6)
def entry_kind(t): return "pickup" if t < 0 else "on" if t == 0 else "after" if t <= 30 else "late"
def line_rhythm(sy, rng, tmin, sec, last_max=None, fix=None, entry=None, prior=None):
    end = 72 if last_max is None else min(72, last_max)
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d): return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max([k for k in range(n) if st[k]] or [n - 1]); post = n - 1 - Ls
    def A(k, t):
        m = M.mw(t); w = {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
        tm = t % BAR
        return w * (AIM.b3 if tm == 24 else AIM.b24 if tm in (12, 36) else 1.0) * (PRIOR_W if prior and t in prior else 1.0)
    tilt = AIM.tilt; fix = fix or {}
    for _ in range(14):
        kind_ = None
        if NEW and not fix:
            kind_ = entry if entry in ENTRY_T else rng.choices(list(ENTRY), list(ENTRY.values()))[0]
            if kind_ == "pickup" and st[0]: kind_ = rng.choices(["on", "after"], [ENTRY["on"], ENTRY["after"]])[0]
        tgt = fix.get(Ls) if Ls in fix else land_draw(rng, sec, n)
        if tgt + 6 * post > end or tgt - 6 * Ls < tmin: continue
        G = [t for t in GRID if tmin <= t <= end]
        alpha = [dict() for _ in range(n)]
        for t in G:
            if t > tgt: break
            if Ls == 0 and t != tgt: continue
            if 0 in fix and t != fix[0]: continue
            if st[0] and t < 0: continue                                         # a stressed syllable is never a pickup
            if kind_ is not None:
                if not ENTRY_T[kind_](t): continue
                alpha[0][t] = A(0, t); continue                                     # 269: the pickup weight no longer decides the entry
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
                if last_iv is not None and abs(last_iv) > 7 and (sg > 0) == (last_iv > 0): continue
                if toward is not None and (abs(toward - p) > 7 or abs(toward - p) == 6): continue
                w0 = math.exp(-(p - mu) ** 2 / (2 * M.RSD ** 2)) * M.kp(p) * M.SIZE_W.get(sz, 1.0)
                w0 *= 1.0 if sz == 0 else (M.DESC if sg < 0 else 1 - M.DESC)
                if sz and last_iv: w0 *= AIM.turn if (sg > 0) != (last_iv > 0) else 1.0
                if SHAPE is not None:                                                  # 257: toward the line's contour; 258: wider late
                    w0 *= math.exp(-(p - SHAPE[0]) ** 2 / (2 * 2.5 ** 2))
                cands.append(p); ws.append(w0 * chord_w(p, n, ch) * deg_w(p)); base += w0
        if cands and base > 0 and c[1] > 0:
            wd = math.exp(LK["widen"] * (SHAPE[1] - 0.5) * (-1 if c[0] in ("repeat", "step") else 1)) if SHAPE is not None else 1.0   # 258: on the category
            for p, w in zip(cands, ws): allc.append(p); allw.append(c[1] * wd * w / base)
    if allc and sum(allw) > 0: return rng.choices(allc, allw)[0]
    return None
SHAPE = None
CONTOURS = {"arch": [(0, 0), (0.3, 1), (1, -0.2)], "falling": [(0, 0), (1, -1)], "valley": [(0, 0), (0.5, -1), (1, 0)], "rising": [(0, 0), (1, 1)],
            "level then falling": [(0, 0), (0.4, 0), (1, -1)], "falling then level": [(0, 0), (0.6, -1), (1, -1)], "rising then level": [(0, 0), (0.6, 1), (1, 1)],
            "level then rising": [(0, 0), (0.4, 0), (1, 1)], "level": [(0, 0), (1, 0)]}
KEPT_KINDS = LIT["findings"]["kept"]["contour kinds"]
def draw_shape(rng, ns, mu, lo, hi):
    """257: a contour chosen before the notes; 259: the line's first pitch from the contour's start in the section's register."""
    kind = rng.choices(list(KEPT_KINDS), list(KEPT_KINDS.values()))[0]; pts = CONTOURS[kind]; D = LK["amp"] * rng.uniform(0.7, 1.3)
    t0, t1 = ns[0]["on"], ns[-1]["on"]; xs = [(n["on"] - t0) / max(1, t1 - t0) for n in ns]
    f = [D * float(np.interp(x, [a for a, _ in pts], [b for _, b in pts])) for x in xs]
    h0 = mu + rng.gauss(0, LK["fresh"]) - float(np.mean(f))
    h0 = min(hi - max(f) - 0.5, max(lo - min(f) + 0.5, h0)) if max(f) - min(f) < hi - lo - 1 else (lo + hi) / 2 - float(np.mean(f))
    return kind, [(h0 + y, x) for y, x in zip(f, xs)]
def first_note(rng, n, ch, h0, lo, hi):
    cands = [p for p in range(lo, hi + 1) if p % 12 in M.SCALE and not tri(p, ch)]
    return rng.choices(cands, [math.exp(-(p - h0) ** 2 / (2 * 1.5 ** 2)) * M.kp(p) * chord_w(p, n, ch) * deg_w(p) + 1e-12 for p in cands])[0]
def walk_notes(rng, notes, prev, run, mu, lo, hi, notes_on, fixed=None, shape=None):
    global SHAPE
    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None
    for i, n in enumerate(notes): n["dur"] = notes[i + 1]["on"] - n["on"] if i + 1 < len(notes) else 24
    for i, n in enumerate(notes):
        if fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:
            q_ = out[-1]; ch_ = M.chord_for(n, notes_on)
            opts = [x for x in (q_ - 2, q_ - 1, q_ + 1, q_ + 2) if lo <= x <= hi and x % 12 in M.SCALE and not tri(x, ch_)]
            p = rng.choices(opts, [(3 if x < q_ else 1) * chord_w(x, n, ch_) for x in opts])[0] if opts else q_
        elif shape is not None and i == 0:
            p = first_note(rng, n, M.chord_for(n, notes_on), shape[0][0], lo, hi)       # 259: not the next step from the line before
        else:
            tw = fixed.get(i + 1) if fixed else None
            SHAPE = shape[i] if shape is not None else None
            p = next_pitch(rng, prev, run, n, M.chord_for(n, notes_on), mu, lo, hi, last_iv, toward=tw); SHAPE = None
            if p is None: return None
        run = run + 1 if p == prev else 1
        last_iv = (p - prev) if prev is not None else last_iv
        prev = p; out.append(p)
    return out
def fresh_line(sy, rng, U, tmin, sec, last_max=None, fix=None, entry=None):
    if fix and len(fix) == len(sy):                                                   # a designed rhythm
        if fix[0] < tmin: return None
        return [dict(on=U + fix[k], p=None, syl=k, slur=False, stress=sy[k][1]) for k in range(len(sy))]
    ons = line_rhythm(sy, rng, tmin, sec, last_max, fix, entry=entry)
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
    last = None
    for _ in range(6):
        ns, kd = _vary_return(rng, S, Ssy, sy, SU, U, tmin, lo, hi, notes_on, late)
        if ns is not None: return ns, kd
        if kd == "align": break
        last = LAST_TRY
    if last is not None:                                                               # 278: steered six times, then kept
        STATS["return: first or top note not kept (aim)"] += 1; return last
    return None, kd
LAST_TRY = None
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
    global LAST_TRY
    rch = len({n["on"] - U for n in ns} ^ src_rel) > 0
    pch = any(src_p[n["on"] - U] != n["p"] for n in ns if n["on"] - U in src_rel) or any(n.get("added") for n in ns)
    kd_ = {(False, False): "exact", (True, False): "rhythm", (False, True): "pitch", (True, True): "both"}[(rch, pch)]
    sh = [j for j, n in enumerate(ns) if n["on"] - U in src_rel]
    LAST_TRY = (ns, kd_)
    if max(n["p"] for n in ns) < max(n["p"] for n in S): return None, "kept"                 # 239(f): the top note kept or higher
    if not sh or ns[sh[0]]["p"] != S[0]["p"]: return None, "kept"                          # 239(b): the first note kept
    return ns, kd_

# ---- 228: sung again ----
def sing_again(rng, S, Ssy, sy, SU, U, tmin, sec, lo, hi, notes_on, last_max=None, ons=None):
    """verse 1's line as contour and cadence; the rhythm fitted again to the new words; a stressed note on a beat moves a step to a
    chord tone where it lands on none."""
    if ons is None:
        ons = line_rhythm(sy, rng, tmin, sec, last_max, **again_kw(S, SU))
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
def again_kw(S, SU):
    if not NEW: return {}
    return dict(entry=entry_kind(S[0]["on"] - SU), prior={n["on"] - SU for n in S})
def repair(rng, ns, prev, lo, hi, notes_on, keep=()):
    """a mapped line's leaps past a sixth, tritones and runs of four are re-walked, the other notes held."""
    for _pass in range(5):
        bad = set(); run = 1
        for j in range(1, len(ns)):
            iv = abs(ns[j]["p"] - ns[j - 1]["p"]); run = run + 1 if iv == 0 else 1
            if iv > 9 or iv == 6: bad.add(j if j not in keep else j - 1)
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
VERSE_PLANS = [("ABAC", 0.4), ("ABAB", 0.3), ("ABCD", 0.2), ("AABC", 0.1)]
BRIDGE_PLANS = [("ABAC", 0.4), ("ABCD", 0.4), ("ABCB", 0.2)]
PRE_PLANS = [("AB", 0.75), ("AA", 0.25)]
PAIRS = {"Verse": ["Verse 1", "Verse 2"], "Pre": ["Pre 1", "Pre 2"], "Bridge": ["Bridge"]}
def admissible(sec, plan):
    for i, x in enumerate(plan):
        j = plan.index(x)
        if j != i and any(abs(len(LINES[s][i]) - len(LINES[s][j])) > 3 for s in PAIRS[KIND[sec]]): return False
    return True
def draw_plan(rng, sec, plans):
    ok = [(p, w) for p, w in plans if admissible(sec, p)] or [("ABCD", 1.0)]
    return list(rng.choices([p for p, _ in ok], [w for _, w in ok])[0])
MUS = {"Verse": 54, "Pre": 57, "Chorus": 62, "Bridge": 60}
CAPS = {"Verse": 59, "Pre": 64, "Chorus": 66, "Bridge": 66}
FLOORS = {"Verse": 47, "Pre": 50, "Chorus": 54, "Bridge": 54}
SRC = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}

# ---- 262: how a section ends ----
TRIAD = {9, 1, 4}
def end_ok(sec, i, p):
    if i != len(LINES[sec]) - 1: return True
    if sec == "Verse 1": return (p - M.TONIC) % 12 != 0                                   # the verse ends off the tonic
    if sec == "Chorus 1": return p % 12 in TRIAD                                         # an earlier chorus on a note of the tonic triad
    return True                                                                          # the last chorus ends on the tag's A3 (designed)
def end_rule(sec, i, ns, notes_on, lo, hi):
    if end_ok(sec, i, ns[-1]["p"]): return
    n = ns[-1]; ch = M.chord_for(n, set(notes_on) | {x["on"] for x in ns}); q0 = n["p"]
    opts = [q0 + d for d in (-1, 1, -2, 2, -3, 3) if lo <= q0 + d <= max(hi, q0) and (q0 + d) % 12 in M.SCALE and not tri(q0 + d, ch) and end_ok(sec, i, q0 + d)]
    if opts: n["p"] = opts[0]; STATS["262: last note moved"] += 1
def generate(rng, cal=None):
    """one build. cal: a calibration build (targets at the pools' medians)."""
    global AIM
    meta = dict(returns=[], kinds={}, win={}, targets={})
    for p in ("V", "C"):
        i, t = (None, dict(MED[p])) if cal else draw_targets(rng, p)
        meta["win"][p] = i; meta["targets"][p] = t; AIMS[p] = Aim(t, p)
    plans = dict(Verse=draw_plan(rng, "Verse 1", VERSE_PLANS), Bridge=draw_plan(rng, "Bridge", BRIDGE_PLANS), Pre=draw_plan(rng, "Pre 1", PRE_PLANS),
                 tail=rng.choice(["return", "fresh"]))
    meta["plans"] = plans
    built, lines = {}, []; prev, run, last_on = None, 0, -10 ** 6; notes_on_all = set(); pending = {}
    meta["contour"] = {}; meta["free"] = collections.Counter(); meta["twice_changed"] = 0
    def _fail(err): return dict(notes=sorted([dict(n) for l in lines for n in l], key=lambda n: n["on"]), meta=meta, partial=True), err
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
        if sec == "Chorus 2": return ("copy", "Chorus 1", i)
        if sec == "Last Chorus": return ("copy", "Chorus 1", i) if i < 6 else ("return", "Chorus 1", i)
        if sec in ("Verse 2", "Pre 2"): return ("again", SRC[sec], i)
        if kind == "Chorus":
            if i == 4: return ("copy", sec, 0)
            if i == 1: return ("twice", sec, 0)
            if i == 5: return ("return", sec, 1)
            if i in (6, 7) and plans["tail"] == "return": return ("return", sec, i - 4)
            return ("fresh", None, None)
        plan = plans[kind]; first = plan.index(plan[i])
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
            ons = line_rhythm(LINES[sec][i], rng, -12, sec, **again_kw(built[(s0, i0)], line_start(s0, i0))); globals()["AIM"] = AIMP
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
                if pf and pf[0] == "fail": return _fail(("align: the words do not fit the returning tune" if pf[1] == "align" else "return: first or top note not kept (239)"))
                f0 = None
                if pf and pf[1]: f0 = (pf[1][0]["on"] - line_start(*nxt)) if pf[0] == "ns" else pf[1][0]
                elif KIND[nxt[0]] == "Chorus" and nxt[1] in CHANT and how(*nxt)[0] == "fresh": f0 = -6
                if f0 is not None: last_max = (line_start(*nxt) + f0 - U) - GAP_MIN
            h, s0, i0 = how(sec, i)
            if h == "tag":                                                              # 'Turn it off.' (designed)
                ns = [dict(on=U + 0, p=64, syl=0, slur=False, stress=True), dict(on=U + 12, p=61, syl=1, slur=False, stress=False),
                      dict(on=U + 24, p=57, syl=2, slur=False, stress=True, fixdur=36)]
                meta["kinds"][(sec, i)] = "designed"
            elif h in ("copy", "twice", "return", "plan") and (prefit(sec, i) or ("",))[0] == "ns":
                _, ns, kd = pending[(sec, i)]; ns = [dict(n) for n in ns]
                for n in ns: n.pop("hold", None)
                if h == "twice" and NEW:                                               # 282: the source moved whole, a whole step down
                    on_ = notes_on_all | {n["on"] for n in ns}
                    for n in ns:
                        n["p"] -= 2; ch = M.chord_for(n, on_)
                        if tri(n["p"], ch) and (n["on"] % BEAT == 0 or n.get("dur", 0) >= 12):   # changed only for 276's tritone reading
                            n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q2: (tri(q2, ch), q2 % 12 not in M.SUNGPC)); meta["twice_changed"] += 1
                elif h == "twice":                                                     # said twice: a whole step down where it fits the chord
                    on_ = notes_on_all | {n["on"] for n in ns}
                    for n in ns:
                        ch = M.chord_for(n, on_); strong = n["on"] % BEAT == 0 or n["dur"] >= 12
                        opts = [n["p"] - 2, M.dshift(n["p"], -1), n["p"] - 3, n["p"] - 1, n["p"] - 4]
                        ok = [q2 for q2 in opts if q2 % 12 in M.SUNGPC and not M.clash(q2, ch) and not tri(q2, ch) and (not strong or q2 % 12 in M.CH[ch][1])]
                        n["p"] = ok[0] if ok else n["p"] - 2
                meta["kinds"][(sec, i)] = kd
                if h in ("return", "plan"): meta["returns"].append((sec, i, s0, i0, kd))
                if NEW and h in ("return", "plan"): end_rule(sec, i, ns, notes_on_all, lo, hi)  # 262 on a returning last line
            elif h == "again":
                pf = pending.get((sec, i)); S = built[(s0, i0)]
                if pf and pf[1] and ((last_max is not None and pf[1][-1] > last_max) or pf[1][0] < tmin): pf = None   # redrawn against the line ahead (247)
                ns = sing_again(rng, S, LINES[s0][i0], sy, line_start(s0, i0), U, tmin, sec, lo, hi, notes_on_all, last_max, ons=pf[1] if pf else None)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                meta["returns"].append((sec, i, s0, i0, "sung again")); meta["kinds"][(sec, i)] = "sung again"
            elif h in ("copy", "twice", "return", "plan"):
                globals().__setitem__("WHERE", (sec, i)); return _fail("align: the words do not fit the returning tune")
            else:
                fix = None
                if kind == "Chorus" and i in CHANT: fix = {0: -6, 1: 0, 2: 36, 3: 48}       # the writer's chant; 232: 'tuned' on beat 1
                ns = fresh_line(sy, rng, U, tmin, sec, last_max, fix)
                if ns is None: globals().__setitem__("WHERE", (sec, i)); return _fail("rhythm: no placement")
                meta["free"][sec] += len(ns) if not (kind == "Chorus" and i == 0) else 0
                fixed = {}
                if kind == "Chorus" and i == 0: fixed = {1: SUMMIT}; ns[1]["hold"] = 36
                nf = None                                                              # the next line's first pitch, if it is already fitted
                if nxt and pending.get(nxt) and pending[nxt][0] == "ns": nf = pending[nxt][1][0]["p"]
                if nf is None and nxt and KIND[nxt[0]] == "Chorus" and nxt[1] == 0 and how(*nxt)[0] == "fresh": nf = 64     # toward the chant's pickup
                if nf is not None and not NEW: fixed[len(ns)] = nf                   # 259: B and C do not steer a line's end toward the next
                if kind == "Chorus" and i == 0:                                         # the chant, designed: E4 or G#4 - A4 - E4 or F#4 - F#4 or D4
                    ps = [rng.choice([64, 68]), SUMMIT, rng.choice([64, 66]), rng.choices([66, 62], [0.6, 0.4])[0]]; _durs(ns)
                for _try in range(0 if kind == "Chorus" and i == 0 else 8):
                    shape = None
                    if NEW and not (kind == "Chorus" and i == 0):
                        _durs(ns); ck, shape = draw_shape(rng, ns, mu, lo, hi); meta["contour"][(sec, i)] = ck
                    ps = walk_notes(rng, ns, prev, run, mu, lo, SUMMIT if 1 in fixed and kind == "Chorus" and i == 0 else hi, notes_on_all, fixed=fixed or None, shape=shape)
                    if ps is None: continue
                    if NEW and not end_ok(sec, i, ps[-1]) and _try < 7: ps = None; continue   # 262
                    if kind == "Chorus" and i == 0:                                     # the twice line's pickup is this one's a step down
                        if abs(ps[-1] - (ps[0] - 2)) > 9 or abs(ps[-1] - (ps[0] - 2)) == 6 or any(p > hi for j, p in enumerate(ps) if j != 1): ps = None; continue
                    break
                if ps is None: globals().__setitem__("WHERE", (sec, i)); return _fail("walk: no note")
                for n, p in zip(ns, ps): n["p"] = p
                if NEW: end_rule(sec, i, ns, notes_on_all, lo, hi)
                meta["kinds"][(sec, i)] = "fresh"
            if ns[0]["on"] - last_on < GAP_MIN: globals().__setitem__("WHERE", (sec, i)); return _fail("join: no held end and breath before the line (212)")
            if last_max is not None and ns[-1]["on"] - U > last_max: globals().__setitem__("WHERE", (sec, i, h)); return _fail("join: no held end and breath before the copy (212)")
            if not NEW and prev is not None and (abs(ns[0]["p"] - prev) > 12 or abs(ns[0]["p"] - prev) == 6) and h not in ("copy", "twice", "tag"):
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

# ---- gates (v107) ----
def top(notes, s): return max(n["p"] for n in notes if n["sec"] == s)
def low(notes, s): return min(n["p"] for n in notes if n["sec"] == s)
def med(notes, s): return float(np.median([n["p"] for n in notes if n["sec"] == s]))
SOFT, HARD, DIRN = GL["soft limits (kept 5th or 95th percentile)"], GL["hard limits (kept 1st or 99th percentile)"], GL["direction"]
LIMITS = list(SOFT)
def limit_readings(notes):
    """276: the eight readings on the whole song's sung notes (Table DL)."""
    on = {n["on"] for n in notes}; iv = [b2["p"] - a2["p"] for a2, b2 in zip(notes, notes[1:])]
    r = dict(tritone_leap_share=sum(abs(x) == 6 for x in iv) / max(1, len(iv)), past_octave_share=sum(abs(x) > 12 for x in iv) / max(1, len(iv)))
    run = 1; worst = 1
    for a2, b2 in zip(notes, notes[1:]):
        run = run + 1 if a2["p"] == b2["p"] and a2["line"] == b2["line"] else 1; worst = max(worst, run)
    r["run_max"] = worst
    bh = [n for n in notes if n["on"] % BEAT == 0 or n["dur"] >= 12]
    r["tritone_from_root_share"] = sum(tri(n["p"], M.chord_for(n, on)) for n in bh) / max(1, len(bh))
    r["max_lengths_8_bars"] = max(len({n["dur"] for n in notes if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) for b0 in range(NBARS - 7))
    r["chorus_top_minus_verse"] = top(notes, "Chorus 1") - top(notes, "Verse 1")
    r["chorus_median_minus_verse"] = med(notes, "Chorus 1") - med(notes, "Verse 1")
    r["chorus_floor_minus_verse"] = low(notes, "Chorus 1") - low(notes, "Verse 1")
    return r
def limit_breaks(r):
    soft, hard = [], []
    for k in LIMITS:
        v = r[k]
        if k == "run_max": s_, h_ = v >= 10, v >= 15                                       # the writer's reading of 270 under 276: soft at 10, hard at 15
        elif DIRN[k] == "at most": s_, h_ = v > SOFT[k] + 1e-9, v > HARD[k] + 1e-9
        else: s_, h_ = v < SOFT[k] - 1e-9, v < HARD[k] - 1e-9
        if h_: hard.append(k)
        elif s_: soft.append(k)
    return soft, hard
def era_inside(er): return [k for k in ERA_K if ERA95[k][0] - 1e-9 <= er[k] <= ERA95[k][1] + 1e-9]
NEAR_LEVEL = 2                                                                         # 267: the session's number, uncounted
def return_267(c):
    """267: a return built by 239 is related when the first three-quarters of its shared events keep their pitches, or both near-level."""
    out = []; notes = c["notes"]
    for sec, i, s0, i0, kind in c["meta"]["returns"]:
        if kind == "sung again": continue
        a2, b2, U = line_span(notes, sec, i); a0, b0, U0 = line_span(notes, s0, i0)
        R = {n["on"] - U: n["p"] for n in notes if a2 <= n["on"] < b2}; S_ = {n["on"] - U0: n["p"] for n in notes if a0 <= n["on"] < b0}
        sh = sorted(set(R) & set(S_))
        if not sh: out.append(((sec, i, s0, i0, kind), False, "no shared events")); continue
        q4 = 0.75 * max(R)                                                             # read on the quarter 239 builds: the last quarter of the line's span
        keep = all(R[t] == S_[t] for t in sh if t < q4)
        lvl = (max(R[t] for t in sh) - min(R[t] for t in sh) <= NEAR_LEVEL) and (max(S_[t] for t in sh) - min(S_[t] for t in sh) <= NEAR_LEVEL)
        out.append(((sec, i, s0, i0, kind), keep or lvl, "kept" if keep else "near-level" if lvl else "changed early"))
    return out
GATES = ["limits: a hard limit or three soft breaks (276/277)", "summit placed (design gate; 216, 244)",
         "returns related (267)", "chorus opening another tune (227; 279)", "bridge opening unrelated (208; 279)",
         "bridge above the verse, under the summit (design gate; 208)", "rhythm band (163; unaudited)",
         "era: fewer than four of five bands inside CLASSIC's 5th-95th (264)", "pushed notes (159; 279)", "density (159; 279)",
         "sequence legs (148; unaudited)", "key word on a chord tone (134; 279)", "the judge's floor (254; 279)"]
AIMS_278 = ["chorus top at or above the verse's", "chorus median not below", "chorus lowest note above", "bridge median above the verse's",
            "bridge top under the song's", "returns keep their first note", "returns keep their top note or higher", "five note lengths at most (V1, C1 windows)",
            "no tritone leap", "no note a tritone from the root"]
def aims_278(c):
    notes = c["notes"]; on = {n["on"] for n in notes}; ret = []
    for sec, i, s0, i0, kind in c["meta"]["returns"]:
        if kind == "sung again": continue
        R = [n for n in notes if n["line"] == f"{sec}:{i}"]; S_ = [n for n in notes if n["line"] == f"{s0}:{i0}"]
        ret.append((R[0]["p"] == S_[0]["p"], max(n["p"] for n in R) >= max(n["p"] for n in S_)))
    w5 = all(len({n["dur"] for n in notes if BAR0[s] * BAR <= n["on"] < (BAR0[s] + 8) * BAR}) <= 5 for s in ("Verse 1", "Chorus 1"))
    iv = [b2["p"] - a2["p"] for a2, b2 in zip(notes, notes[1:])]
    return {AIMS_278[0]: top(notes, "Chorus 1") >= top(notes, "Verse 1"), AIMS_278[1]: med(notes, "Chorus 1") >= med(notes, "Verse 1"),
            AIMS_278[2]: low(notes, "Chorus 1") > low(notes, "Verse 1"), AIMS_278[3]: med(notes, "Bridge") > med(notes, "Verse 1"),
            AIMS_278[4]: top(notes, "Bridge") < max(n["p"] for n in notes), AIMS_278[5]: float(np.mean([x[0] for x in ret])) if ret else None,
            AIMS_278[6]: float(np.mean([x[1] for x in ret])) if ret else None, AIMS_278[7]: w5, AIMS_278[8]: not any(abs(x) == 6 for x in iv),
            AIMS_278[9]: not any(tri(n["p"], M.chord_for(n, on)) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in notes)}
def gate_fails(c, jd=None):
    notes = c["notes"]; ps = [n["p"] for n in notes]; f = {}; on = {n["on"] for n in notes}; info = {}
    rb = M.rhythm_bits(notes)
    if not (M.RBAND["p05"] <= rb <= M.RBAND["p95"]): f["rhythm band (163; unaudited)"] = round(rb, 3)
    er, _ = era_read(notes); ins = era_inside(er); info["era"] = er; info["era_inside_95"] = ins
    if len(ins) < 4: f["era: fewer than four of five bands inside CLASSIC's 5th-95th (264)"] = [k for k in ERA_K if k not in ins]
    if M.pushed_share(notes) > 0.42: f["pushed notes (159; 279)"] = 1
    de = len(notes) / sum(SECLEN[s] * 4 * 60 / M.QBPM for s in SUNG)
    if not (1.1 <= de <= 4.9): f["density (159; 279)"] = de
    if any(l >= 3 for l in M.sequences(notes)): f["sequence legs (148; unaudited)"] = 1
    if M.keyword_chord(notes)[0] < 0.40: f["key word on a chord tone (134; 279)"] = 1
    summ = [n for n in notes if n["p"] == SUMMIT]
    if len(summ) != 6 or max(ps) > SUMMIT or any(KIND[n["sec"]] != "Chorus" or int(n["line"].split(":")[1]) not in (0, 4) or n["on"] % BAR or M.chord_for(n, on) != "A" for n in summ):
        f["summit placed (design gate; 216, 244)"] = len(summ)
    lr = limit_readings(notes); soft, hard = limit_breaks(lr); info["limits"] = lr; info["soft"] = soft; info["hard"] = hard
    if hard or len(soft) >= 3: f["limits: a hard limit or three soft breaks (276/277)"] = (hard, soft)
    rr = return_267(c); info["returns"] = rr
    if any(not x[1] for x in rr): f["returns related (267)"] = next(x for x in rr if not x[1])[0]
    if opening_rel(notes, "Chorus 1", "Verse 1")[0]: f["chorus opening another tune (227; 279)"] = 1
    if opening_rel(notes, "Bridge", "Verse 1")[0] or opening_rel(notes, "Bridge", "Chorus 1")[0]: f["bridge opening unrelated (208; 279)"] = 1
    if not med(notes, "Bridge") > med(notes, "Verse 1") or top(notes, "Bridge") >= SUMMIT: f["bridge above the verse, under the summit (design gate; 208)"] = 1
    jd = jd or judge(notes)
    if jd["combined"] < J.FLOOR: f["the judge's floor (254; 279)"] = round(jd["combined"], 3)
    c["info"] = info
    return f
def table_b(notes):
    """the five readings of Table B, unaudited (280), as v1 reads them: returns (cause, value) or None, and the parts for the composite."""
    V = M.sec_notes(notes, "Verse 1"); H = [n for n in M.sec_notes(notes, "Chorus 1") if n["on"] < (BAR0["Chorus 1"] + 8) * BAR]
    off = V[0]["on"]; tune = M.quarters(V, off) + M.quarters(H, off)
    beta = beta_pitch(tune); C = M.C
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral (Table B; unaudited)", beta), None
    cmp_, _ = cmp_score(tune, 4, M.TONIC)
    if cmp_ < C["cmp"]["p05"]: return ("cmp (Table B; unaudited)", cmp_), None
    hq = M.quarters(H, H[0]["on"]); vq = M.quarters(V, V[0]["on"]); mh, _, _ = m_horizon(hq, vq)
    if mh < C["mh"]["p05"]: return ("memory (Table B; unaudited)", mh), None
    bits = M.PPMM.bits(PPM.symbols(tune, M.TONIC))[len(V):]; hp = [n["p"] for n in H]
    ic, _ = ic_profile(bits, hp.index(max(hp)))
    if ic < C["ic"]["p05"]: return ("surprisal (Table B; unaudited)", ic), None
    fv = (feature_vec(hq, M.TONIC, 4) - M.MU) / M.SD
    dist = np.sort(np.sqrt(((M.ZREF - fv) ** 2).sum(1)))[:10].mean(); real = sum(1 for x in M.REAL_KNN if x >= dist) / len(M.REAL_KNN)
    if real < C["realness"]["p05"]: return ("realness (Table B; unaudited)", real), None
    return None, dict(beta=beta, cmp=cmp_, mh=mh, ic=ic, real=real, H=H, V=V)
def evaluate(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    if min(ps) < M.LO or max(ps) > SUMMIT: return ("range (the voice row)", (min(ps), max(ps))), None
    f = gate_fails(c, c.get("judge"))
    for g in GATES:
        if g in f: return (g, f[g]), None
    cert, tb = table_b(notes)
    if cert: return cert, None
    C = M.C; beta, cmp_, mh, ic, real, H, V = (tb[k] for k in ("beta", "cmp", "mh", "ic", "real", "H", "V")); hp = [n["p"] for n in H]
    S_sp = s_spectral(beta, C["beta"]["p25"], C["beta"]["p75"]); vps = [n["p"] for n in V]; lift = float(np.median(hp) - np.median(vps))
    fit = float(np.mean([M.contour(hp) in ("arch", "ascending", "wave", "descending"), 1.0 if lift >= 4 else (0.5 if lift >= 2 else 0.0), M.contour(vps) in ("flat", "wave"), max(vps) <= CAPS["Verse"]]))
    comp = 0.15 * S_sp + 0.15 * min(1.0, cmp_ / C["cmp"]["p75"]) + 0.10 * min(1, mh) + 0.15 * fit + 0.15 * ic + 0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5
    return None, dict(composite=round(comp, 4), pitch_bits=round(M.pitch_bits(ps), 3), rhythm_bits=round(M.rhythm_bits(notes), 3), IC=ic, CMP=cmp_, M_horizon=mh, realness=real, fit=fit, lift=lift)

# ---- the line readings of Table DJ (27.48), with the v104 file's own contour code ----
from scipy.fft import dct
PM_ = np.array(LIT["pitch model: rows are the scale degree left (0-11 above the tonic), columns the interval -24..+24, probabilities"])
def _contour(ps, ds):
    e = np.cumsum(ds); x = np.linspace(0, e[-1], 31)[:-1] + e[-1] / 60; y = np.array([ps[min(np.searchsorted(e, v, side="right"), len(ps) - 1)] for v in x], float)
    th = [y[:10].mean(), y[10:20].mean(), y[20:].mean()]; cc = dct(y, type=2, norm="ortho")
    s1 = np.sign(round(th[1] - th[0], 6)) if abs(th[1] - th[0]) > 0.5 else 0; s2 = np.sign(round(th[2] - th[1], 6)) if abs(th[2] - th[1]) > 0.5 else 0
    kind = {(1, -1): "arch", (-1, 1): "valley", (1, 1): "rising", (-1, -1): "falling", (0, 0): "level", (1, 0): "rising then level", (0, 1): "level then rising", (-1, 0): "falling then level", (0, -1): "level then falling"}[(s1, s2)]
    return kind, float(cc[1]), float(-cc[2])
def _ic(p, prev):
    if prev is None: return np.nan
    iv = int(np.clip(p - prev, -24, 24)); return float(-np.log2(max(1e-6, PM_[(prev - M.TONIC) % 12][iv + 24])))
AF = ("arch", "falling", "falling then level", "level then falling")
def line_readings(notes):
    """Table DJ on a build: one line per lyric line (the engine's own lines, not found by rule); shares and medians across its lines."""
    by = collections.OrderedDict()
    for n in notes: by.setdefault(n["line"], []).append(n)
    Ls = [l for l in by.values() if len(l) >= 3]; rows = []; prev_last = None; first_ic, other_ic, joins = [], [], []
    for L_ in Ls:
        ps = [n["p"] for n in L_]; ds = [n["dur"] / BEAT for n in L_]; t0 = L_[0]["on"] / BEAT; tl = L_[-1]["on"] / BEAT
        kind, fall, arch = _contour(ps, ds); iv = np.abs(np.diff(ps)); q = max(1, len(iv) // 5)
        ic = [_ic(L_[0]["p"], prev_last)] + [_ic(ps[k], ps[k - 1]) for k in range(1, len(ps))]
        if prev_last is not None: first_ic.append(ic[0]); joins.append(abs(ps[0] - prev_last))
        other_ic += ic[1:]
        rows.append(dict(kind=kind, arch=arch, fall=fall, widen=float(iv[-q:].mean() - iv[:q].mean()), peak_first_third=float(np.argmax(ps) / (len(ps) - 1) < 1 / 3),
                         end_minus_mean=float(ps[-1] - np.mean(ps)), last_over_mean=float(ds[-1] / np.mean(ds)), last_longest=float(ds[-1] >= max(ds)),
                         on=float(t0 % 4 < 0.5), after=float(0.5 <= t0 % 4 < 3.0), pickup=float(t0 % 4 >= 3.0), end_down=float(tl % 4 < 0.26 or tl % 4 >= 3.74),
                         sec=L_[0]["sec"], line=L_[0]["line"]))
        prev_last = ps[-1]
    m = lambda k: float(np.mean([r[k] for r in rows])); md = lambda k: float(np.median([r[k] for r in rows]))
    kinds = collections.Counter(r["kind"] for r in rows)
    return dict(lines=len(rows), arch_or_falling=float(np.mean([r["kind"] in AF for r in rows])), valley=float(np.mean([r["kind"] == "valley" for r in rows])),
                arch_positive=float(np.mean([r["arch"] > 0 for r in rows])), arch_term=md("arch"), falling_term=md("fall"), peak_first_third=m("peak_first_third"),
                end_minus_mean=md("end_minus_mean"), last_over_mean=md("last_over_mean"), last_longest=m("last_longest"), widening=m("widen"),
                first_note_extra_bits=float(np.nanmean(first_ic) - np.nanmean(other_ic)) if first_ic else float("nan"),
                join_fourth=float(np.mean([j >= 5 for j in joins])) if joins else float("nan"), join_mean=float(np.mean(joins)) if joins else float("nan"),
                starts_on_downbeat=m("on"), starts_after_downbeat=m("after"), starts_as_pickup=m("pickup"), ends_on_downbeat=m("end_down"),
                kinds={k: round(v / len(rows), 3) for k, v in kinds.items()}, rows=rows)

# ---- readings for each build ----
def reading(c):
    notes = c["notes"]; Wv = win_feats(notes, BAR0["Verse 1"]); Wc = win_feats(notes, BAR0["Chorus 1"])
    er, _ = era_read(notes); r = dict(v=Wv, c=Wc, era=er, ax_v=axes_of(Wv), ax_c=axes_of(Wc), ax_b=axes_of(win_feats(notes, BAR0["Bridge"])),
                                      dist=float(np.mean([win_distance(Wv), win_distance(Wc)])), outside=len(outside_both(Wv)) / 2 + len(outside_both(Wc)) / 2)
    return r

def calibrate(rng, n=30, rounds=3):
    """249: the knobs are set on this song so that a build aimed at its pool's medians reads near them."""
    log = []; lines_acc = []
    pairs = {"repeat": "repeat", "step": "step", "third": "third", "fourth_fifth": "fourth_fifth", "larger": "past_fifth", "ct_on": "chord_tones_on_beat",
             "ct_off": "chord_tones_off_beat", "on_tonic": "on_tonic", "on_third": "on_third", "on_fifth": "on_fifth", "turn": "turns_per_move",
             "beat3": "on_beat3", "beats24": "on_beats_2_4", "gap8": "gap_eighth", "gap4": "gap_quarter"}
    for rd in range(rounds):
        acc = {"V": collections.defaultdict(list), "C": collections.defaultdict(list)}; k = 0; tries = 0
        while k < n and tries < 40 * n:
            tries += 1; c, err = generate(rng, cal=True)
            if err: continue
            k += 1
            if NEW: lines_acc.append(line_readings(c["notes"]))
            for p, s in (("V", "Verse 1"), ("C", "Bridge")):
                f = win_feats(c["notes"], BAR0[s])
                for kn, m in pairs.items():
                    if f and np.isfinite(f.get(m, np.nan)): acc[p][kn].append(f[m])
        row = {}
        if NEW and lines_acc:
            arch = float(np.mean([x["arch_term"] for x in lines_acc])); wid = float(np.mean([x["widening"] for x in lines_acc])); fr = float(np.nanmean([x["first_note_extra_bits"] for x in lines_acc]))
            LK["amp"] = float(np.clip(LK["amp"] * float(np.clip(1.452 / max(0.2, arch), 0.6, 1.6)), 1.5, 12))     # Table DJ kept medians
            LK["widen"] = float(np.clip(LK["widen"] + 2.0 * (0.326 - wid), -1.0, 5.0))
            LK["fresh"] = float(np.clip(LK["fresh"] * float(np.clip(1.338 / max(0.1, fr), 0.6, 1.6)), 0.5, 6))
            row["lines"] = dict(arch=(1.452, round(arch, 3), round(LK["amp"], 3)), widening=(0.326, round(wid, 3), round(LK["widen"], 3)), fresh=(1.338, round(fr, 3), round(LK["fresh"], 3)))
            lines_acc.clear()
        for p in ("V", "C"):
            for kn, m in pairs.items():
                if NEW and kn == "beat3": continue                                            # 285
                rd_ = float(np.mean(acc[p][kn])) if acc[p][kn] else MED[p][m]; tg = MED[p][m]
                KNOBS[p][kn] = float(np.clip(KNOBS[p][kn] * (max(0.02, tg) / max(0.02, rd_)) ** 1.0, 0.05, 20))
                row[f"{p}:{kn}"] = (round(tg, 3), round(rd_, 3), round(KNOBS[p][kn], 3))
        log.append(row)
    return log

if __name__ == "__main__":
    import time; T0 = time.time()
    N = _N; SEED = 20261110 + 381
    rng = random.Random(SEED)
    cal_log = calibrate(random.Random(SEED + 1))
    made, deaths, alive, allb = 0, collections.Counter(), [], []
    would = collections.Counter(); every = []
    STATS.clear()
    while made < N:
        c, err = generate(rng); made += 1
        for n in c["notes"]: n.setdefault("dur", 12)
        rec = dict(n=made, fp=M.fingerprint(c), notes=[(n["on"], n["dur"], n["p"], n["sec"], n["line"], n.get("stress"), n.get("syl")) for n in c["notes"]],
                   cause=err, partial=bool(c.get("partial")), soft=None, hard=None, judge=None, win=dict(c["meta"]["win"]))
        every.append(rec)
        if err: deaths[err] += 1; continue
        c["judge"] = judge(c["notes"]); rec["judge"] = {k: c["judge"][k] for k in ("combined", "content", "order")}
        fails = gate_fails(c, c["judge"]); info = c["info"]; rec["soft"], rec["hard"], rec["limits"] = info["soft"], info["hard"], info["limits"]
        for g in fails: would[g] += 1
        r = reading(c); c["read"] = r; c["lines"] = line_readings(c["notes"]); lr = {k: v for k, v in c["lines"].items() if k != "rows"}
        allb.append(dict(meta=c["meta"], read=r, judge=rec["judge"], fails=list(fails), info=info, lines=lr, aims=aims_278(c),
                         kinds=dict(c["meta"]["kinds"]), notes=rec["notes"], fp=rec["fp"]))
        cert, m = evaluate(c)
        tb_cert, _ = table_b(c["notes"])
        if tb_cert: would[tb_cert[0]] += 1
        if cert: deaths[cert[0]] += 1; rec["cause"] = cert[0]; allb[-1]["cause"] = cert[0]; continue
        allb[-1]["cause"] = None
        c["meas"] = m; c["fp"] = rec["fp"]; alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    byj = sorted(alive, key=lambda c: (-c["judge"]["combined"], c["fp"])); short = byj[:max(1, len(byj) // 2)]       # 255
    sfp = {c["fp"] for c in short}; pick = next(c for c in alive if c["fp"] in sfp) if alive else None
    print(f"[{VAR}{_TAG}] {NBARS} bars; built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order {order}, {time.time() - T0:.0f}s")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("would fail:"); [print(f"   {would[g]:5d}  {g}") for g in list(GATES) + sorted(k for k in would if k not in GATES)]
    if alive:
        for lab, c in (("composite first", alive[0]), ("shortlist pick", pick), ("judge first", byj[0])):
            print(f"{lab:16s} {c['fp']} comp {c['meas']['composite']:.3f} judge {c['judge']['combined']:.3f} (content {c['judge']['content']:.3f}, order {c['judge']['order']:.3f})"
                  f" soft {c['info']['soft']} plans {c['meta']['plans']}")
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{HERE}/lyric_p38.py", "rb").read() + open(f"{HERE}/judges.py", "rb").read()
                        + open("/home/claude/p36/melody_p36.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, calibration_seed=SEED + 1, N=N, variant=VAR, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(),
                 numpy=np.__version__, tables={f: hashlib.sha256(open(f"{HERE}/tables/{f}", "rb").read()).hexdigest()[:16] for f in sorted(os.listdir(f"{HERE}/tables"))},
                 cmd=f"PYTHONHASHSEED=0 python3 melody_v2_p38.py {N} {VAR}", line_knobs=dict(LK), prior_w=PRIOR_W, near_level=NEAR_LEVEL)
    print("rerun:", rerun)
    pickle.dump(dict(would=would, deaths=deaths, made=made, survivors=len(alive), order_fp=order, alive=alive[:80], short=[c["fp"] for c in short],
                     pick=pick, comp_first=alive[0] if alive else None, judge_first=byj[0] if byj else None, all=allb, every=every, stats=dict(STATS),
                     calibration=cal_log, knobs=KNOBS, line_knobs=dict(LK), rerun=rerun, form=FORM, chords=CHORD,
                     all_alive=[(c["fp"], c["judge"]["combined"], c["judge"]["content"], c["judge"]["order"], c["meas"]["composite"]) for c in alive]),
                open(f"{HERE}/melody_v2_{VAR}{_TAG}.pkl", "wb"))
