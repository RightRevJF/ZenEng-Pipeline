"""The First Wood -- the tune and its bass, searched together (ZenEng v88; the hymn and carol class).
3/4 at q = 92, F major; Common Metre with a refrain: L1 8, L2 6, L3 8, L4 6, R1 6 ('Sleep in the first wood, child'), R2 6; 24 bars a
stanza, a pickup to each line but R1. One tune for all four stanzas; the declamation is read on every stanza's words.
Grid: twelfths of a beat (the tables' unit); a bar is 36.
Class tables from zeneng_v88_tables.json (hymn_carol / hymns), not refitted:
  152 the walk's priors: pitch model R 4, P 3, the major key profile; 153 the pitch band 2.02-3.11 bits;
  159 the bar rhythms from the 3/4 vocabulary, pushed notes <= 1.3%; 163 the rhythm band in 3/4, 0.68-3.30 bits;
  147 the rhythm floor (a bar's rhythm heard before in >= 38% of bars); 148 sequences of two legs;
  161 the line's last stress on a strong beat (3/4: the downbeat) in >= 2/3 of lines;
  136 the outer-voice gates (contrary + oblique > similar + parallel; parallel perfects <= 10% of bass moves; imperfect >= 25%);
  137 the bass written with the tune, inversions chosen to move it by step; 138 cadence arrivals by strength;
  174 the chord engine's first choices for the class (the dominant governs, roots falling by fifth, inversions);
  134 the key word on a chord tone (>= 40% of lines); 133 the refrain's top not below the stanza's;
  165 the summit declared and placed: D5 once, on FIRST (refrain line 1), every other note at C5 or below.
Earlier floors kept (Table B on the hymn calibration, carol/calibration.json): spectral, CMP, memory, IC, mean bits, realness.
The composite (Table C) ranks the survivors (118). The rerun record names the seed, N, the code's hash, the versions and
PYTHONHASHSEED (145)."""
import sys, os, json, math, random, pickle, hashlib, collections, platform, re
import numpy as np
sys.path[:0] = ["/home/claude/p35", "/home/claude/carol", "/home/claude/pop"]
import engine_p35 as E, phrasestress48 as PS; PS.install(E); E.install_patches()
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec, intervals, basic
import lyric as L

T = json.load(open("/home/claude/p35/tables/zeneng_v88_tables.json"))
PMOD = T["pitch_model"]["hymn_carol"]; KMAJ = PMOD["K_major"]; RSD, PSD = PMOD["R"], PMOD["P"]
PBAND = T["surprise_bands_pitch"]["hymns"]["surprise_bits_per_note"]
RT = T["rhythm_tables"]["hymn_carol"]["3/4"]["table"]; RT = json.loads(RT) if isinstance(RT, str) else RT
RBAND = T["surprise_bands_rhythm"]["hymns"]["3/4"]["rhythm_bits_per_note"]
VOCAB = [tuple(v["onsets_in_twelfths_of_a_beat"]) for v in T["bar_rhythm_vocabulary"]["hymn_carol"]["3/4"]]
OV = T["outer_voices"]["hymns"]
CAL = json.load(open("/home/claude/carol/calibration.json")); C = CAL["cal"]
MU, SD = np.array(CAL["mu"]), np.array(CAL["sd"]); ZREF = np.array(CAL["Z"]); REAL_KNN = CAL["real_knn"]
PPMM = pickle.load(open("/home/claude/carol/ppm.pkl", "rb"))

TONIC = 5; BAR = 36; BEAT = 12
LO, CAP, SUMMIT = 60, 72, 74                       # C4 .. C5, and the one D5
SCALE = {5, 7, 9, 10, 0, 2, 4}
LINES = ["L1", "L2", "L3", "L4", "R1", "R2"]
NSYL = dict(L1=8, L2=6, L3=8, L4=6, R1=6, R2=6)
START = dict(L1=0, L2=4, L3=8, L4=12, R1=16, R2=20)  # the bar of each line's first downbeat
NBARS = 24
CLOSE = dict(L1="half", L2="half", L3="half", L4="full", R1="half", R2="full")   # from the lyric's sentence and stanza ends (138)
# bar rhythms for an iambic bar (a stressed then a weak syllable), from the 3/4 vocabulary; and where they put the syllables
IAMB = {(0, 24): [(0, 24, 0), (24, 12, 1)],                 # half, quarter            (44% of hymn bars)
        (0, 12, 24): [(0, 12, 0), (12, 12, 0), (24, 12, 1)],   # three quarters, the first two slurred on the stress (29%)
        (0, 18, 24): [(0, 18, 0), (18, 6, 0), (24, 12, 1)],    # dotted quarter, eighth, quarter (6%)
        (0, 24, 30): [(0, 24, 0), (24, 6, 1), (30, 6, 1)]}     # half, two eighths on the weak syllable (2.7%)
for k in IAMB: assert k in VOCAB, k
W_IAMB = {k: [v["share"] for v in T["bar_rhythm_vocabulary"]["hymn_carol"]["3/4"] if tuple(v["onsets_in_twelfths_of_a_beat"]) == k][0] for k in IAMB}

# ---- the words of every stanza, with the stress readings ----
WEAK_168 = {"like", "you'll", "i'll", "there's"}
ONE_STRESS = {"mortise", "everything", "sunday"}      # fix 168's list, with the dictionary's double-stressed 'mortise'
def syl(line):
    s = [list(x) for x in E.syllables(line)]
    for k, x in enumerate(s):
        if x[0] in ONE_STRESS and k > 0 and s[k - 1][0] == x[0]: x[2] = False
        if x[0] in WEAK_168: x[2] = False
    # a monosyllable at the line's end carries the rhyme and is stressed (v77, fix 2.1)
    if s and (len(s) < 2 or s[-2][0] != s[-1][0]): s[-1][2] = True
    return s
WORDS = []
for si, st in enumerate(L.STANZAS):
    ls = st + [L.REFRAIN1, L.REFRAIN2[si]]
    WORDS.append({ln: syl(t) for ln, t in zip(LINES, ls)})
for st in WORDS:
    for ln in LINES: assert len(st[ln]) == NSYL[ln], (ln, len(st[ln]))

def pickup(ln): return ln != "R1"
# ---- the rhythm of a line: (onset, dur, syllable index) relative to the stanza (bar 0 = the first downbeat) ----
def line_rhythm(ln, bars):
    """bars: the bar rhythms for the line's iambic bars."""
    b0 = START[ln] * BAR; out = []
    if ln == "R1":
        out = [(b0, 12, 0), (b0 + 12, 12, 1), (b0 + 24, 12, 2), (b0 + BAR, 24, 3), (b0 + BAR + 24, 12, 4), (b0 + 2 * BAR, 60, 5)]
        return out
    out.append((b0 - 12, 12, 0))
    k = 1
    for i, br in enumerate(bars):
        for on, du, j in IAMB[br]: out.append((b0 + i * BAR + on, du, k + j))
        k += 2
    fb = b0 + len(bars) * BAR
    out.append((fb, 24 if NSYL[ln] == 8 else 60, k))
    assert k == NSYL[ln] - 1, (ln, k)
    return out
NIB = dict(L1=3, L2=2, L3=3, L4=2, R2=2)            # iambic bars per line

def kprob(p): return KMAJ[(p - TONIC) % 12]
def walk_note(rng, prev, mu, lo, hi, pool=None, ban=None):
    cands = [p for p in range(lo, hi + 1) if p % 12 in SCALE and (pool is None or p % 12 in pool) and p != ban]
    w = [math.exp(-(p - mu) ** 2 / (2 * RSD ** 2)) * math.exp(-(p - prev) ** 2 / (2 * PSD ** 2)) * kprob(p) for p in cands]
    if not cands: return None
    return rng.choices(cands, w)[0]

PLANS = [("A", "B", "A2", "C", "D", "B2"), ("A", "B", "A2", "B2", "D", "C"), ("A", "B", "C", "B2", "D", "B3"), ("A", "B", "A2", "C", "D", "C2")]
HALF_END = {7, 4, 0, 9}          # 2, 7, 5 over V; or 3 over I (138)
def generate(rng):
    plan = rng.choice(PLANS)
    mu = rng.choice([66, 67, 67, 68, 69])
    rhy, mel = {}, {}
    letter_rhy, letter_mel = {}, {}
    prev = rng.choice([60, 65, 65, 67])
    for ln, lt in zip(LINES, plan):
        base = lt[0]
        if ln != "R1":
            if base in letter_rhy:
                bars = list(letter_rhy[base])
                if CLOSE[ln] == "full" and bars and bars[-1] == (0, 24, 30): bars[-1] = (0, 24)
            else:
                bars = []
                for i in range(NIB[ln]):
                    ks = list(IAMB); w = [W_IAMB[k] for k in ks]
                    if sum(1 for b in bars if b != (0, 24)) >= 1: ks, w = [(0, 24)], [1.0]          # one slurred bar a line at most
                    if i == NIB[ln] - 1 and CLOSE[ln] == "full": ks, w = [k for k in ks if k != (0, 24, 30)], [W_IAMB[k] for k in ks if k != (0, 24, 30)]
                    bars.append(rng.choices(ks, w)[0])
                letter_rhy[base] = bars
            if len(bars) != NIB[ln]: bars = (bars + [(0, 24)] * 3)[:NIB[ln]]
        else: bars = []
        r = line_rhythm(ln, bars); rhy[ln] = r
        n = len(r); ps = []
        hi = CAP
        if base in letter_mel and len(letter_mel[base]) == n and lt != base:
            src = letter_mel[base]; mode = rng.choice(["head", "transpose", "new"])
            if mode == "head":                   # the same rhythm, its first half kept, a new close
                ps = src[: n // 2]
            elif mode == "transpose":            # a second leg: the line moved by a diatonic step or third
                sh = rng.choice([-2, -1, 1, 2]); deg = sorted(SCALE)
                def dshift(p):
                    c = [q for q in range(48, 80) if q % 12 in SCALE]; i = c.index(p); return c[max(0, min(len(c) - 1, i + sh))]
                ps = [dshift(p) for p in src[:-1]]
                if min(ps) < LO or max(ps) > CAP: ps = []                                  # a leg that leaves the compass is not written
            else: ps = []
        for i in range(len(ps), n):
            on, du, j = r[i]
            last = (i == n - 1)
            if ln == "R1" and j == 3: p = SUMMIT
            elif last and CLOSE[ln] == "full": p = 65
            elif i == n - 2 and CLOSE[ln] == "full":
                q = ps[-1] if ps else prev                                         # 2, 7, 5 or 4 before the close, within a third of the last note
                p = walk_note(rng, q, 65, max(LO, q - 4), min(hi, q + 4), pool={7, 4, 0, 10}) or walk_note(rng, 65, 65, 62, 67, pool={7, 4, 0, 10})
            elif last: p = walk_note(rng, ps[-1] if ps else prev, mu, LO, hi, pool={x % 12 for x in HALF_END})
            else:
                ban = ps[-1] if len(ps) >= 2 and ps[-1] == ps[-2] else None                  # the monotony floor, built into the fill (v77)
                p = walk_note(rng, ps[-1] if ps else prev, mu, LO, hi, ban=ban)
                if i >= 1 and r[i - 1][2] == j and len(ps) >= 1:                            # a slurred second note: a step from the first
                    p = walk_note(rng, ps[-1], ps[-1], max(LO, ps[-1] - 2), min(hi, ps[-1] + 2), ban=ps[-1]) or p
                elif i >= 2 and r[i - 1][2] == r[i - 2][2] and len(ps) >= 2 and ps[-1] != ps[-2] and rng.random() < 0.85:
                    d = 1 if ps[-1] > ps[-2] else -1                                           # and on through it by step: a passing note
                    q = walk_note(rng, ps[-1] + 2 * d, ps[-1] + 2 * d, max(LO, min(ps[-1] + d, ps[-1] + 2 * d)), min(hi, max(ps[-1] + d, ps[-1] + 2 * d)))
                    p = q or p
                if ln == "R1" and j == 2: p = walk_note(rng, 70, 70, 67, 72)                  # the climb into the summit
            ps.append(p)
        if ln == "R1":
            ps[2] = max(ps[2], 67)
        if CLOSE[ln] == "full" and (ps[-2] % 12) not in (7, 4, 0, 10):
            q = ps[-3]; bn = q if len(ps) >= 4 and ps[-3] == ps[-4] else None
            ps[-2] = walk_note(rng, q, 65, max(LO, q - 4), min(CAP, q + 4), pool={7, 4, 0, 10}, ban=bn) or walk_note(rng, q, 65, 62, 67, pool={7, 4, 0, 10}, ban=bn)               # 2, 7, 5 or 4: the dominant before the close
        mel[ln] = ps; prev = ps[-1]
        if lt == base: letter_mel[base] = ps
    notes = []
    for ln in LINES:
        for (on, du, j), p in zip(rhy[ln], mel[ln]): notes.append(dict(on=on, dur=du, p=p, line=ln, syl=j))
    notes.sort(key=lambda n: n["on"])
    return dict(plan=plan, mu=mu, notes=notes)

# ---- the chords and the bass, drawn with the tune (137, 174) ----
CHORDS = {"I": (5, [5, 9, 0]), "ii": (7, [7, 10, 2]), "iii": (9, [9, 0, 4]), "IV": (10, [10, 2, 5]), "V": (0, [0, 4, 7]),
          "V7": (0, [0, 4, 7, 10]), "vi": (2, [2, 5, 9]), "vii": (4, [4, 7, 10])}
FUNC = {"I": "T", "vi": "T", "iii": "T", "IV": "S", "ii": "S", "V": "D", "V7": "D", "vii": "D"}
NEXT = {"I": {"I", "IV", "ii", "V", "V7", "vi", "iii", "vii", "I64"}, "vi": {"ii", "IV", "V", "V7", "iii", "I64", "vi"}, "iii": {"vi", "IV", "iii"},
        "IV": {"V", "V7", "ii", "I", "vii", "I64", "IV"}, "ii": {"V", "V7", "vii", "I64", "ii"}, "I64": {"V", "V7"}, "V": {"I", "vi", "V7", "V"},
        "V7": {"I", "vi"}, "vii": {"I"}}
BLO, BHI = 41, 60
def bass_opts(ch):
    if ch == "I64": return [p for p in range(BLO, BHI + 1) if p % 12 == 0]
    root, tones = CHORDS[ch]
    if ch == "vii": return [p for p in range(BLO, BHI + 1) if p % 12 == 7]            # vii only as vii6
    ok = {root, tones[1]} | ({tones[3]} if ch == "V7" else set()) | ({tones[2]} if ch == "V7" else set())
    return [p for p in range(BLO, BHI + 1) if p % 12 in ok]
def tones_of(ch): return set(CHORDS["I"][1]) if ch == "I64" else set(CHORDS[ch][1])
def root_of(ch): return 5 if ch == "I64" else CHORDS[ch][0]

def slots_of(notes):
    """chord slots: every beat, from the pickup bar to the end (a chord may hold across beats)."""
    sl = []
    for b in range(-1, NBARS):
        for a, z in ((0, 12), (12, 24), (24, 36)):
            s0, s1 = b * BAR + a, b * BAR + z
            if s1 <= notes[0]["on"]: continue
            sl.append((s0, s1))
    return sl
def sounding(notes, t):
    for n in notes:
        if n["on"] <= t < n["on"] + n["dur"]: return n
    return None

ABLATE = False                                    # the control: a bass of chord roots, the outer-voice terms off
def harmonize(c, rng, noise=0.6):
    notes = c["notes"]; SL = slots_of(notes)
    ends = {}
    for ln in LINES:
        fin = [n for n in notes if n["line"] == ln][-1]; ends[fin["on"]] = (ln, CLOSE[ln])
    # what each slot requires
    req = []
    for k, (s0, s1) in enumerate(SL):
        r = set(); flex = []
        n0 = sounding(notes, s0)
        if n0: r.add(n0["p"] % 12)
        for n in notes:
            if s0 < n["on"] < s1:
                i = notes.index(n); a = notes[i - 1]["p"]; b = notes[i + 1]["p"] if i + 1 < len(notes) else None
                step_in = abs(n["p"] - a) <= 2; step_out = b is not None and abs(b - n["p"]) <= 2
                if step_in and step_out and n["p"] != a: flex.append(n["p"] % 12)       # a passing or neighbour note may lie outside
                else: r.add(n["p"] % 12)
        req.append((r, flex, n0))
    # the cadences: the final syllable's slot and the one before it
    fixed = {}
    for k, (s0, s1) in enumerate(SL):
        if s0 in ends:
            ln, kind = ends[s0]; p = sounding(notes, s0)["p"] % 12
            if kind == "full": fixed[k] = {"I"}; fixed[k - 1] = {"V", "V7"}
            else: fixed[k] = {"V"} if p in (7, 4, 0) else {"I"}
    cand = []
    for k in range(len(SL)):
        r, flex, n0 = req[k]
        chs = [ch for ch in list(CHORDS) + ["I64"] if r <= tones_of(ch)]
        if k in fixed: chs = [ch for ch in chs if ch in fixed[k]]
        if "I64" in chs and not (k + 1 in fixed and fixed[k + 1] <= {"V", "V7"}): chs.remove("I64")
        st = []
        for ch in chs:
            for bp in bass_opts(ch):
                if k in fixed and ch in ("I", "V", "V7") and (SL[k][0] in ends or ends.get(SL[k + 1][0] if k + 1 < len(SL) else -1, ("", ""))[1] == "full") and bp % 12 != root_of(ch): continue
                if ABLATE and bp % 12 != root_of(ch): continue
                mp = n0["p"] if n0 else None
                if mp is not None and mp % 12 == bp % 12 and (bp % 12 == 4 or ch == "V7"): continue   # the leading tone doubled outside; a V7 two inner voices cannot complete
                if mp is not None and mp - bp < 7: continue                                          # the bass at least a fifth under the tune
                st.append((ch, bp))
        if not st:
            global _DBG; _DBG = (k, SL[k], r, flex, fixed.get(k), chs)
            return None, "harmonize: no chord holds the tune here"
        cand.append(st)
    def mel_at(k): n = req[k][2]; return n["p"] if n else None
    best = [{} for _ in SL]
    for st in cand[0]: best[0][st] = (0.0, None)
    for k in range(1, len(SL)):
        m0, m1 = mel_at(k - 1), mel_at(k)
        for st in cand[k]:
            ch, bp = st; top = None
            for pst, (sc, _) in best[k - 1].items():
                pch, pbp = pst
                if ch != pch and not (ch in NEXT.get(pch, set())): continue
                if (ch, bp) != (pch, pbp) and not any(n["on"] == SL[k][0] for n in notes): continue   # the chord holds under a held note or a rest
                v = sc
                if ch == pch and bp == pbp: v += {0: -0.2, 12: 3.0, 24: 1.2}[SL[k][0] % BAR]
                else:
                    ri, rj = root_of(pch), root_of(ch)
                    if ch != pch:
                        if (ri - rj) % 12 == 7: v += 2.0                  # roots falling by fifth (174)
                        elif (rj - ri) % 12 in (1, 2): v += 0.8
                        if FUNC.get(pch) == "D" and ch == "I": v += 1.5
                    d = abs(bp - pbp)
                    v += {0: -0.6, 1: 2.0, 2: 2.0, 3: 0.8, 4: 0.8, 5: 0.5, 7: 0.5}.get(d, -1.5 if d <= 12 else -9)
                    if bp % 12 != root_of(ch): v -= 0.6                    # inversions, about four in ten (174): the step bonus brings them; root position is the default
                    if m0 is not None and m1 is not None and not ABLATE:
                        dm, db = m1 - m0, bp - pbp
                        i0, i1 = (m0 - pbp) % 12, (m1 - bp) % 12
                        if dm == 0 or db == 0: v += 0.5
                        elif (dm > 0) != (db > 0): v += 1.0
                        else:
                            v -= 0.3
                            if i1 in (0, 7) and i0 == i1: v -= 9                # parallel fifths and octaves
                            if i1 in (0, 7) and abs(dm) > 2: v -= 1.0           # a perfect interval reached by similar motion, the tune leaping
                if m1 is not None:
                    iv = (m1 - bp) % 12
                    v += 0.8 if iv in (3, 4, 8, 9) else (0.0 if iv in (0, 7) else (-9 if iv == 5 and ch != "I64" else -0.5))
                    if m1 - bp < 0: v -= 9
                    if m1 - bp < 7: v -= 1.5                                       # the bass well under the tune
                    if m1 % 12 == bp % 12 and (bp % 12 == 4 or ch == "V7"): v -= 9      # the leading tone doubled outside, or a V7 that two inner voices cannot complete   # the leading tone or the seventh doubled in the outer voices
                v += rng.gauss(0, noise)
                if top is None or v > top[0]: top = (v, pst)
            if top: best[k][st] = top
        if not best[k]: return None, "harmonize: no chord path"
    st = max(best[-1], key=lambda s: best[-1][s][0]); path = [st]
    for k in range(len(SL) - 1, 0, -1):
        st = best[k][st][1]; path.append(st)
    path.reverse()
    return [dict(on=s0, end=s1, chord=ch, bass=bp) for (s0, s1), (ch, bp) in zip(SL, path)], None

# ---- readings and gates ----
def pitch_bits(ps):
    mu = float(np.mean(ps)); out = []
    for a, b in zip(ps, ps[1:]):
        cands = range(int(round(mu)) - 26, int(round(mu)) + 27)
        w = {q: math.exp(-(q - mu) ** 2 / (2 * RSD ** 2)) * math.exp(-(q - a) ** 2 / (2 * PSD ** 2)) * kprob(q) for q in cands}
        out.append(-math.log2(w[b] / sum(w.values())))
    return float(np.mean(out))
def rhythm_bits(notes, total):
    out = []
    ons = [n["on"] for n in notes] + [total]
    for a, b in zip(ons, ons[1:]):
        pos = a % BAR; d = min(96, b - a)
        out.append(-math.log2(max(1e-9, RT[pos][d])))                 # columns: the distance itself, 0..96
    return float(np.mean(out))
def bar_rhythms(notes):
    by = collections.OrderedDict()
    for b in range(NBARS): by[b] = tuple(n["on"] - b * BAR for n in notes if b * BAR <= n["on"] < (b + 1) * BAR)
    return by
def repetition(notes):
    br = bar_rhythms(notes); seen = []; rec = 0; cnt = collections.Counter(br.values())
    for b, r in br.items():
        if r in seen: rec += 1
        seen.append(r)
    pitches = {b: tuple(n["p"] for n in notes if b * BAR <= n["on"] < (b + 1) * BAR) for b in range(NBARS)}
    exact = sum(1 for b in range(NBARS) if any(pitches[b] == pitches[a] and br[b] == br[a] for a in range(b)))
    trans = sum(1 for b in range(NBARS) if pitches[b] and any(br[b] == br[a] and len(pitches[a]) == len(pitches[b]) and len({y - x for x, y in zip(pitches[a], pitches[b])}) == 1 and pitches[a] != pitches[b] for a in range(b)))
    common = cnt.most_common(); cov, k4 = 0, 0
    for r, c in common:
        cov += c; k4 += 1
        if cov >= 0.8 * NBARS: break
    return dict(rhythm_recurs=rec / NBARS, distinct=len(cnt), rhythms_for_80=k4, exact=exact / NBARS, transposed=trans / NBARS)
def sequences(notes):
    """legs: consecutive bars whose pitches are one bar's moved by one interval, same rhythm."""
    br = bar_rhythms(notes); legs = []; run = 1
    P = {b: [n["p"] for n in notes if b * BAR <= n["on"] < (b + 1) * BAR] for b in range(NBARS)}
    for b in range(1, NBARS):
        a = b - 1
        same = br[a] == br[b] and len(P[a]) == len(P[b]) >= 2 and len({y - x for x, y in zip(P[a], P[b])}) == 1 and P[a] != P[b]
        if same: run += 1
        else:
            if run >= 2: legs.append(run)
            run = 1
    if run >= 2: legs.append(run)
    return legs
def outer(notes, harm):
    moves = []; prev = None
    for h in harm:
        if prev is None or h["bass"] != prev:
            n = sounding(notes, h["on"])
            if n: moves.append((h["on"], h["bass"], n["p"], n["on"] == h["on"]))
        prev = h["bass"]
    ic = collections.Counter(); mo = collections.Counter(); par = 0; direct = 0
    for t, b, m, s in moves:
        iv = (m - b) % 12
        ic["imperfect" if iv in (3, 4, 8, 9) else "perfect" if iv in (0, 7) else "fourth" if iv == 5 else "dissonance"] += 1
    for (t1, b1, m1, _), (t2, b2, m2, _) in zip(moves, moves[1:]):
        db, dm = b2 - b1, m2 - m1
        if dm == 0: k = "oblique"
        elif (db > 0) != (dm > 0): k = "contrary"
        elif abs(db) == abs(dm): k = "parallel"
        else: k = "similar"
        mo[k] += 1
        if k in ("parallel", "similar") and (m2 - b2) % 12 in (0, 7) and (m1 - b1) % 12 == (m2 - b2) % 12: par += 1
        if k == "similar" and (m2 - b2) % 12 in (0, 7) and abs(dm) > 2: direct += 1
    n = len(moves); nm = max(1, n - 1)
    steps = sum(1 for (_, b1, _, _), (_, b2, _, _) in zip(moves, moves[1:]) if abs(b2 - b1) in (1, 2))
    f45 = sum(1 for (_, b1, _, _), (_, b2, _, _) in zip(moves, moves[1:]) if abs(b2 - b1) in (5, 7))
    return dict(moves=n, imperfect=ic["imperfect"] / n, perfect=ic["perfect"] / n, fourth=ic["fourth"] / n, dissonance=ic["dissonance"] / n,
                oblique=mo["oblique"] / nm, contrary=mo["contrary"] / nm, similar=mo["similar"] / nm, parallel=mo["parallel"] / nm,
                parallel_perfect=par / n, direct_perfect=direct / nm, bass_by_step=steps / nm, bass_by_4th_5th=f45 / nm,
                struck_together=sum(1 for m in moves if m[3]) / n)
def declamation(c):
    rows = []
    for si, st in enumerate(WORDS):
        for ln in LINES:
            ns = [n for n in c["notes"] if n["line"] == ln]
            first = {}
            for n in ns: first.setdefault(n["syl"], n)
            sy = st[ln]
            stresses = [(first[j]["on"], j) for j in range(len(sy)) if sy[j][2]]
            if not stresses: rows.append(dict(stanza=si + 1, line=ln, schema="", last_strong=False)); continue
            b0 = min(t for t, _ in stresses) // BAR; parts = collections.OrderedDict()
            for t, j in stresses: parts.setdefault(t // BAR, []).append(str((t % BAR) // BEAT + 1) if t % BEAT == 0 else f"{(t % BAR) / BEAT + 1:.1f}")
            schema = " | ".join(" ".join(v) for v in parts.values())
            lt = stresses[-1][0]
            rows.append(dict(stanza=si + 1, line=ln, schema=schema, last_strong=(lt % BAR == 0), starts_before_downbeat=ns[0]["on"] % BAR != 0,
                             span=(ns[-1]["on"] // BAR - ns[0]["on"] // BAR + 1), stresses_per_bar=len(stresses) / max(1, len(parts))))
    return rows
def keyword_chord(c, harm):
    hit = 0; tot = 0
    for si, st in enumerate(WORDS):
        for ln in LINES:
            ns = [n for n in c["notes"] if n["line"] == ln]; first = {}
            for n in ns: first.setdefault(n["syl"], n)
            js = [j for j in range(len(st[ln])) if st[ln][j][2]]
            if not js: continue
            n = first[js[-1]]; h = [x for x in harm if x["on"] <= n["on"] < x["end"]][0]
            tot += 1; hit += (n["p"] % 12) in tones_of(h["chord"])
    return hit / tot
def contour(ps):
    if len(ps) < 3: return "flat"
    i = ps.index(max(ps)); j = ps.index(min(ps))
    if 0 < i < len(ps) - 1 and max(ps) - ps[0] >= 3 and max(ps) - ps[-1] >= 3: return "arch"
    if ps[-1] - ps[0] >= 3: return "ascending"
    if ps[0] - ps[-1] >= 3: return "descending"
    return "wave"

NEW_GATES = ["register (133)", "cadence (138)", "pitch band (153)", "rhythm band (163)", "rhythm floor (147)", "pushed notes (159)",
             "sequence legs (148)", "declamation: last stress (161)", "outer voices: motion (136)", "outer voices: parallel perfects (136)",
             "outer voices: imperfect (136)", "key word on a chord tone (134)", "summit once (165)"]
def audit(c, harm):
    """every v76-v88 gate read on its own, so a gate that would fail is counted even when an earlier one killed the build first."""
    notes = c["notes"]; ps = [n["p"] for n in notes]; f = set()
    if max(n["p"] for n in notes if n["line"] in ("R1", "R2")) < max(n["p"] for n in notes if n["line"] in ("L1", "L2", "L3", "L4")): f.add("register (133)")
    for ln in LINES:
        fin = [n for n in notes if n["line"] == ln][-1]; h = [x for x in harm if x["on"] <= fin["on"] < x["end"]][0]; d = (fin["p"] - TONIC) % 12
        if (CLOSE[ln] == "full" and not (d == 0 and h["chord"] == "I")) or (CLOSE[ln] == "half" and not ((d in (2, 11, 7) and h["chord"] == "V") or (d == 4 and h["chord"] == "I"))): f.add("cadence (138)")
    pb = pitch_bits(ps)
    if not (PBAND["p05"] <= pb <= PBAND["p95"]): f.add("pitch band (153)")
    rb = rhythm_bits(notes, NBARS * BAR)
    if not (RBAND["p05"] <= rb <= RBAND["p95"]): f.add("rhythm band (163)")
    if repetition(notes)["rhythm_recurs"] < 0.38: f.add("rhythm floor (147)")
    pushed = sum(1 for n in notes if n["on"] % BEAT != 0 and (n["on"] + n["dur"]) > (n["on"] // BEAT + 1) * BEAT and not any(m["on"] == (n["on"] // BEAT + 1) * BEAT for m in notes)) / len(notes)
    if pushed > 0.013: f.add("pushed notes (159)")
    if any(l >= 3 for l in sequences(notes)): f.add("sequence legs (148)")
    dec = declamation(c)
    if sum(1 for r in dec if r["last_strong"]) / len(dec) < 2 / 3: f.add("declamation: last stress (161)")
    ov = outer(notes, harm)
    if not (ov["contrary"] + ov["oblique"] > ov["similar"] + ov["parallel"]): f.add("outer voices: motion (136)")
    if ov["parallel_perfect"] > 0.10: f.add("outer voices: parallel perfects (136)")
    if ov["imperfect"] < 0.25: f.add("outer voices: imperfect (136)")
    if keyword_chord(c, harm) < 0.40: f.add("key word on a chord tone (134)")
    if ps.count(SUMMIT) != 1: f.add("summit once (165)")
    return f, dict(pitch_bits=pb, rhythm_bits=rb, outer=ov)

def evaluate(c, harm):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    # earlier gates the class keeps
    if min(ps) < LO or max(ps) > SUMMIT: return ("range", (min(ps), max(ps))), None
    ivs = [b - a for a, b in zip(ps, ps[1:])]
    if max(abs(x) for x in ivs) > 12: return ("leap over an octave", max(abs(x) for x in ivs)), None
    if sum(1 for x in ivs if abs(x) > 7) > 1: return ("leaps beyond a fifth (class prior: 1.2%)", sum(1 for x in ivs if abs(x) > 7)), None
    if any(abs(x) in (6, 10, 11) for x in ivs): return ("congregational interval: tritone or seventh", ""), None
    run = 1
    for a, b in zip(ps, ps[1:]):
        run = run + 1 if a == b else 1
        if run > 3: return ("monotony (166)", a), None
    tune0 = [(n["on"] / BEAT, n["dur"] / BEAT, n["p"]) for n in notes]; b0 = basic(tune0, TONIC)
    for k in ("tessitura", "steps", "leaps"):
        if not (C[k]["p05"] <= b0[k] <= C[k]["p95"]): return (f"hymn invariant: {k} (Module 0.4)", round(b0[k], 3)), None
    # 165: the summit placed once, by construction
    if ps.count(SUMMIT) != 1: return ("summit once (165)", ps.count(SUMMIT)), None
    # 133: the refrain's top not below the stanza's
    if max(n["p"] for n in notes if n["line"] in ("R1", "R2")) < max(n["p"] for n in notes if n["line"] in ("L1", "L2", "L3", "L4")): return ("register (133)", ""), None
    # 138: cadence arrivals
    for ln in LINES:
        fin = [n for n in notes if n["line"] == ln][-1]; h = [x for x in harm if x["on"] <= fin["on"] < x["end"]][0]
        d = (fin["p"] - TONIC) % 12
        if CLOSE[ln] == "full" and not (d == 0 and h["chord"] == "I"): return ("cadence (138)", ln), None
        if CLOSE[ln] == "half" and not ((d in (2, 11, 7) and h["chord"] == "V") or (d == 4 and h["chord"] == "I")): return ("cadence (138)", ln), None
    # 153: the pitch band
    pb = pitch_bits(ps)
    if not (PBAND["p05"] <= pb <= PBAND["p95"]): return ("pitch band (153)", round(pb, 3)), None
    # 163: the rhythm band (3/4)
    rb = rhythm_bits(notes, NBARS * BAR)
    if not (RBAND["p05"] <= rb <= RBAND["p95"]): return ("rhythm band (163)", round(rb, 3)), None
    # 147: the rhythm floor
    rep = repetition(notes)
    if rep["rhythm_recurs"] < 0.38: return ("rhythm floor (147)", round(rep["rhythm_recurs"], 3)), None
    # 159: pushed notes
    pushed = sum(1 for n in notes if n["on"] % BEAT != 0 and (n["on"] + n["dur"]) > (n["on"] // BEAT + 1) * BEAT and
                 not any(m["on"] == (n["on"] // BEAT + 1) * BEAT for m in notes)) / len(notes)
    if pushed > 0.013: return ("pushed notes (159)", round(pushed, 3)), None
    # 148: sequences of two legs
    legs = sequences(notes)
    if any(l >= 3 for l in legs): return ("sequence legs (148)", legs), None
    # 161: the line's last stress on a strong beat
    dec = declamation(c); ls = sum(1 for r in dec if r["last_strong"]) / len(dec)
    if ls < 2 / 3: return ("declamation: last stress (161)", round(ls, 3)), None
    # 136: the outer voices
    ov = outer(notes, harm)
    if not (ov["contrary"] + ov["oblique"] > ov["similar"] + ov["parallel"]): return ("outer voices: motion (136)", round(ov["contrary"] + ov["oblique"], 3)), None
    if ov["parallel_perfect"] > 0.10: return ("outer voices: parallel perfects (136)", round(ov["parallel_perfect"], 3)), None
    if ov["imperfect"] < 0.25: return ("outer voices: imperfect (136)", round(ov["imperfect"], 3)), None
    # 134: the key word on a chord tone
    kw = keyword_chord(c, harm)
    if kw < 0.40: return ("key word on a chord tone (134)", round(kw, 3)), None
    # Table B on the hymn calibration (the earlier floors)
    tune = [(n["on"] / BEAT, n["dur"] / BEAT, n["p"]) for n in notes]
    S = [x for x, n in zip(tune, notes) if n["line"] in ("L1", "L2", "L3", "L4")]; H = [x for x, n in zip(tune, notes) if n["line"] in ("R1", "R2")]
    beta = beta_pitch(tune)
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral (Table B)", beta and round(beta, 3)), None
    cmp_, _ = cmp_score(tune, 3.0, TONIC)
    if cmp_ < C["cmp"]["p05"]: return ("cmp (Table B)", round(cmp_, 3)), None
    mh, _, _ = m_horizon(H, S)
    if mh < C["mh"]["p05"]: return ("memory (Table B)", round(mh, 3)), None
    bits = PPMM.bits(PPM.symbols(tune, TONIC))
    ic, icd = ic_profile(bits, ps.index(SUMMIT))
    if ic < C["ic"]["p05"]: return ("surprisal (Table B)", round(ic, 3)), None
    fv = (feature_vec(tune, TONIC, 3.0) - MU) / SD
    dist = np.sort(np.sqrt(((ZREF - fv) ** 2).sum(1)))[:10].mean()
    real = sum(1 for x in REAL_KNN if x >= dist) / len(REAL_KNN)
    if real < C["realness"]["p05"]: return ("realness (Table B)", round(real, 3)), None
    # Table C, the composite: it ranks the survivors (118)
    S_sp = s_spectral(beta, C["beta"]["p25"], C["beta"]["p75"])
    sc = contour([n["p"] for n in notes if n["line"] in ("L1", "L2", "L3", "L4")]); rc = contour([n["p"] for n in notes if n["line"] in ("R1", "R2")])
    b = basic(tune, TONIC)
    fit_items = [sc in ("wave", "arch"), rc == "arch", ov["bass_by_step"] >= OV["median"]["bass_by_step"], b["gapfill"] >= 0.43,
                 [n["p"] for n in notes if n["line"] == "L3"][:3] == [n["p"] for n in notes if n["line"] == "L1"][:3]]
    fit = sum(fit_items) / len(fit_items)
    comp = 0.15 * S_sp + 0.15 * min(1.0, cmp_ / C["cmp"]["p75"]) + 0.10 * min(1, mh) + 0.15 * fit + 0.15 * ic + 0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5
    return None, dict(composite=round(comp, 4), pitch_bits=round(pb, 3), rhythm_bits=round(rb, 3), repetition=rep, legs=legs, pushed=pushed,
                      last_stress_strong=round(ls, 3), outer=ov, keyword_chord=round(kw, 3), beta=beta, CMP=cmp_, M_horizon=mh, IC=ic, realness=real,
                      fit=fit, stanza_contour=sc, refrain_contour=rc, gapfill=b["gapfill"])

def fingerprint(c, harm):
    return hashlib.sha1(json.dumps([[n["on"], n["dur"], n["p"]] for n in c["notes"]] + [[h["on"], h["chord"], h["bass"]] for h in harm]).encode()).hexdigest()[:12]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    SEED = 20261110 + 35
    rng = random.Random(SEED); made, deaths, alive, tries = 0, collections.Counter(), [], 0
    would, spread = collections.Counter(), collections.defaultdict(list)
    while made < N and tries < N * 40:
        tries += 1
        c = generate(rng)
        harm, err = harmonize(c, rng)
        made += 1
        if err: deaths[err] += 1; continue
        fails, rd = audit(c, harm)
        for g in fails: would[g] += 1
        for k in ("pitch_bits", "rhythm_bits"): spread[k].append(rd[k])
        for k in ("imperfect", "parallel_perfect", "contrary", "oblique", "similar", "parallel", "bass_by_step"): spread[k].append(rd["outer"][k])
        cert, m = evaluate(c, harm)
        if cert: deaths[cert[0]] += 1; continue
        c["harm"] = harm; c["meas"] = m; c["fp"] = fingerprint(c, harm); alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    print(f"built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order frozen {order}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("each new gate read on every harmonized build (would fail):")
    for g in NEW_GATES: print(f"   {would[g]:5d}  {g}")
    for k, v in spread.items(): print(f"   {k}: {np.percentile(v, 5):.3f} - {np.median(v):.3f} - {np.percentile(v, 95):.3f}")
    for c in alive[:6]:
        m = c["meas"]; o = m["outer"]
        print(c["fp"], c["plan"], f"comp {m['composite']:.3f} pitch {m['pitch_bits']} rhythm {m['rhythm_bits']} recur {m['repetition']['rhythm_recurs']:.2f} imperf {o['imperfect']:.2f} c+o {o['contrary']+o['oblique']:.2f} step {o['bass_by_step']:.2f} real {m['realness']:.2f}")
    code = hashlib.sha1(open(__file__, "rb").read() + open("/home/claude/p35/lyric.py", "rb").read() + open("/home/claude/p35/phrasestress48.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, N=N, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(), numpy=np.__version__,
                 tables_sha256=hashlib.sha256(open("/home/claude/p35/tables/zeneng_v88_tables.json", "rb").read()).hexdigest()[:16],
                 cmd=f"PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED')} python3 melody_p35.py {N}")
    print("rerun:", rerun)
    pickle.dump(dict(would=would, spread={k: list(v) for k, v in spread.items()}, alive=alive[:60], top20=[c["fp"] for c in alive[:20]], deaths=deaths, made=made, survivors=len(alive), order_fp=order, rerun=rerun),
                open("/home/claude/p35/melody_result.pkl", "wb"))
