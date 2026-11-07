"""Melody measures for the by-hand Module 27 run (ZenEng v39 27.10 sec. 8).

Approximations of the app's functions, calibrated on the Open Hymnal sopranos with the
same code, so floors are 'the 5th percentile of real tunes scored with the same functions'.
A melody is a list of (onset_beats, dur_beats, midi). Beats are quarter notes.
"""
import math, re, collections
import numpy as np

MAJOR = [0, 2, 4, 5, 7, 9, 11]

def intervals(m):
    return [b[2] - a[2] for a, b in zip(m, m[1:])]

# ---------------- invariants / bands (Window 51-52) ----------------
def basic(m, tonic_pc):
    iv = intervals(m)
    a = [abs(x) for x in iv]
    n = max(1, len(a))
    ps = [x[2] for x in m]
    lo, hi = min(ps), max(ps)
    med = float(np.median(ps))
    tess = (med - lo) / max(1, hi - lo)
    steps = sum(1 for x in a if x in (1, 2)) / n
    reps = sum(1 for x in a if x == 0) / n
    thirds = sum(1 for x in a if x in (3, 4)) / n
    leaps = sum(1 for x in a if x >= 5) / n
    # gap-fill: a leap of 5+ followed by motion in the opposite direction
    gl = [(iv[i], iv[i + 1]) for i in range(len(iv) - 1) if abs(iv[i]) >= 5]
    gap = (sum(1 for x, y in gl if y != 0 and (x > 0) != (y > 0)) / len(gl)) if gl else 1.0
    scale = sum(1 for p in ps if (p - tonic_pc) % 12 in MAJOR) / len(ps)
    peakpos = ps.index(hi) / max(1, len(ps) - 1)
    return dict(range=hi - lo, tessitura=tess, steps=steps, repeats=reps, thirds=thirds,
                leaps=leaps, gapfill=gap, scale=scale, peakpos=peakpos, lo=lo, hi=hi, median=med)

def bar_repetition(m, beats_per_bar):
    bars = collections.defaultdict(list)
    for on, d, p in m:
        bars[int(on // beats_per_bar)].append((round(on % beats_per_bar, 3), d, p))
    pats, rep = [], 0
    for b in sorted(bars):
        ns = bars[b]
        if len(ns) < 1: continue
        pat = tuple((o, dd) for o, dd, _ in ns) + tuple(ns[i + 1][2] - ns[i][2] for i in range(len(ns) - 1))
        if pat in pats and len(ns) > 1: rep += 1
        pats.append(pat)
    return rep / max(1, len(pats))

def syncopation(m, beats_per_bar):
    """share of notes that start off the beat and are held across the next beat"""
    s = 0
    for on, d, p in m:
        frac = on - math.floor(on)
        if frac > 1e-6 and (on + d) > math.floor(on) + 1 + 1e-6:
            s += 1
    return s / len(m)

# ---------------- Module 1: spectral exponent of pitch ----------------
def beta_pitch(m):
    x = np.array([p for _, _, p in m], float)
    x = x - x.mean()
    n = len(x)
    if n < 16: return None
    X = np.abs(np.fft.rfft(x * np.hanning(n))) ** 2
    f = np.fft.rfftfreq(n)
    k = (f > 0)
    sl, _ = np.polyfit(np.log(f[k]), np.log(X[k] + 1e-9), 1)
    return -sl

def s_spectral(b, lo, hi):
    if b is None: return 0.5
    if lo <= b <= hi: return 1.0
    d = (lo - b) if b < lo else (b - hi)
    return max(0.0, 1.0 - d / 0.6)

# ---------------- Module 7: characteristic motion profile ----------------
def cmp_score(m, beats_per_bar, tonic_pc, phrase_bars=4):
    strong = [i for i, (on, d, p) in enumerate(m) if abs(on % beats_per_bar) < 1e-6]
    if not strong: return 0.0, {}
    appr = sum(1 for i in strong if i > 0 and abs(m[i][2] - m[i - 1][2]) <= 2) / len(strong)
    iv = intervals(m)
    up = [x for x in iv if x > 0]; dn = [-x for x in iv if x < 0]
    if up and dn:
        asym = abs(np.mean(up) - np.mean(dn)) / 3.0 + abs(len(up) - len(dn)) / len(iv)
    else:
        asym = 1.0
    asym = min(1.0, asym)
    stable = {0, 4, 7}
    grav = sum(1 for i in strong if (m[i][2] - tonic_pc) % 12 in stable) / len(strong)
    # background line: phrase apexes after the global apex step down (or hold)
    ph = collections.defaultdict(list)
    for on, d, p in m:
        ph[int(on // (beats_per_bar * phrase_bars))].append(p)
    apex = [max(v) for _, v in sorted(ph.items())]
    gi = apex.index(max(apex))
    tail = apex[gi:]
    if len(tail) >= 2:
        bl = sum(1 for a, b in zip(tail, tail[1:]) if 0 <= a - b <= 4) / (len(tail) - 1)
    else:
        bl = 0.5
    score = 0.30 * appr + 0.25 * asym + 0.25 * grav + 0.20 * bl
    return score, dict(A_approach=appr, A_asym=asym, G_gravity=grav, B_line=bl)

# ---------------- Module 4: memory horizon (v10 detector) ----------------
def _cells(m):
    out = []
    for i in range(len(m) - 3):
        w = m[i:i + 4]
        con = tuple(int(np.sign(w[j + 1][2] - w[j][2])) for j in range(3))
        rhy = tuple(round(w[j][1], 3) for j in range(4))
        out.append((i, con, rhy))
    return out

def _match(a, b):
    ec = a[1] == b[1]; er = a[2] == b[2]
    if ec and er: return "exact"
    dc = sum(1 for x, y in zip(a[1], b[1]) if x != y)
    dr = sum(1 for x, y in zip(a[2], b[2]) if x != y)
    if (ec and dr <= 1) or (er and dc <= 1): return "varied"
    return None

def m_horizon(hook, other):
    hc = _cells(hook)
    cov = set()
    for j, c in enumerate(hc):
        for c0 in hc[:max(0, j - 3)]:
            if _match(c, c0):
                cov.update(range(c[0], c[0] + 4)); break
    within = len(cov) / max(1, len(hook))
    oc = _cells(other); cov2 = set()
    for c in oc:
        if any(_match(c, h) for h in hc):
            cov2.update(range(c[0], c[0] + 4))
    cross = len(cov2) / max(1, len(other))
    return (within + cross) / 2, within, cross

# ---------------- expectation model (variable order, PPM-C blend) ----------------
class PPM:
    """Interval + scale-degree viewpoint, orders 0-3 over (degree, interval) symbols."""
    def __init__(self, order=3):
        self.order = order
        self.counts = [collections.defaultdict(collections.Counter) for _ in range(order + 1)]
        self.alphabet = set()
    @staticmethod
    def symbols(m, tonic_pc):
        out = []
        for i, (_, _, p) in enumerate(m):
            iv = 0 if i == 0 else max(-12, min(12, p - m[i - 1][2]))
            out.append(((p - tonic_pc) % 12, iv))
        return out
    def train(self, seqs):
        for s in seqs:
            for i, sym in enumerate(s):
                self.alphabet.add(sym)
                for k in range(self.order + 1):
                    if i - k < 0: break
                    self.counts[k][tuple(s[i - k:i])][sym] += 1
    def prob(self, ctx, sym):
        p = 1.0 / (len(self.alphabet) + 1);
        for k in range(0, self.order + 1):
            if len(ctx) < k: break
            c = self.counts[k].get(tuple(ctx[len(ctx) - k:]) if k else ())
            if not c: continue
            tot = sum(c.values()); typ = len(c)
            lam = tot / (tot + typ)
            p = lam * (c[sym] / tot) + (1 - lam) * p
        return p
    def bits(self, s):
        return [-math.log2(self.prob(s[max(0, i - self.order):i], s[i])) for i in range(len(s))]

def ic_profile(bits, peak_idx):
    b = np.array(bits[1:]) if len(bits) > 1 else np.array(bits)
    floor = float(np.median(b))
    fs = 1.0 if floor <= 2.5 else max(0.0, 1 - (floor - 2.5) / 2.0)
    win = bits[max(1, peak_idx - 2): peak_idx + 2]
    spike = max(win) - floor if win else 0
    ss = min(1.0, max(0.0, spike / 2.0))
    thr = floor + 2.0
    stray = sum(1 for i, x in enumerate(bits[1:], 1) if x > thr and abs(i - peak_idx) > 2)
    st = max(0.0, 1 - stray / 8)
    return (fs + ss + st) / 3, dict(floor=floor, spike=spike, stray=stray, mean=float(np.mean(b)))

# ---------------- realness: kNN distance to the reference cloud ----------------
FEATS = ["range", "tessitura", "steps", "repeats", "thirds", "leaps", "gapfill", "peakpos",
         "mean_abs", "up_share", "dur_entropy", "long_share", "density", "end_tonic", "bar_rep"]

def feature_vec(m, tonic_pc, beats_per_bar):
    b = basic(m, tonic_pc)
    iv = intervals(m)
    mv = [x for x in iv if x != 0]
    durs = collections.Counter(round(d, 3) for _, d, _ in m)
    tot = sum(durs.values())
    ent = -sum(c / tot * math.log2(c / tot) for c in durs.values())
    longest = max(durs)
    span = m[-1][0] + m[-1][1] - m[0][0]
    return np.array([b["range"], b["tessitura"], b["steps"], b["repeats"], b["thirds"], b["leaps"],
                     b["gapfill"], b["peakpos"], np.mean([abs(x) for x in iv]),
                     (sum(1 for x in mv if x > 0) / len(mv)) if mv else 0.5, ent,
                     durs[longest] / tot, len(m) / max(1, span),
                     1.0 if (m[-1][2] - tonic_pc) % 12 == 0 else 0.0,
                     bar_repetition(m, beats_per_bar)], float)
