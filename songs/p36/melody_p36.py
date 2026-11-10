"""Dance Anyway -- the sung line searched (ZenEng v91; the pop, rock and country class).
4/4 at q = 118, E-flat major; female mezzo. Grid: twelfths of a beat (the tables' unit), onsets on sixteenths; a bar is 48.
Form (intake Q8): Intro 4 | Verse 8 | Pre 4 | Chorus 16 | Verse 8 | Pre 4 | Chorus 16 | Bridge 8 | Last Chorus 16 | Outro 4.
Every lyric line is a two-bar unit. Chords are written per bar by the section jobs (177), one chord a bar (174); the bass is the
chord roots, so the outer voices are read against the implied-bass bands (183).
Ported before the search, in the order given:
  181 (27.32): where a section's form names a return, the returning unit takes the first unit's rhythm and contour, at the same
      or another pitch, so the two are RELATED by 27.31's test (onset Jaccard >= 0.6, contour correlation >= 0.6); its ending may
      change. The forms are drawn per section (verse ABAC/AABC/ABAB, bridge AABC/ABAC; the chorus a 16-bar period).
  182 (amends 27.26): the walk draws each move from Table CG's pop interval shares (repeat 27.6%, step 42.6%, third 18.5%,
      fourth/fifth 8.4%, beyond a fifth 3.0%; descending 53%), then the pitch by the class's range and key terms (R 5, K major);
      after a leap past a fifth the next move turns back by a step or a third (the walk's own rule, logged).
      Under the class's 25th percentile of pitch surprise (2.76) the card is flagged and nothing is ranked by it; under the 5th
      (2.39) the build dies.
  178-180 (27.31): the phrase-design reading at 8 and 16 bars; the 16-bar chorus a period with rhymed ends (unit 3 returns to
      unit 1, unit 4 to unit 2 with its ending changed); the last chorus states its idea a third time (line 8 on the hook).
  184 (27.33): every gate met by construction reports a control with its construction off (melody_p36.py ctlB).
  191: a word with two primary stresses that is not a compound takes the first, without a list.
  192: the chord at each note can be completed by the band's inner voices without doubling the leading note or a seventh, and
      the bass is a fifth or more below the tune (read; the band writes whole triads).
  193: contrary perfects printed beside the parallel ones.
  183: the bass of chord roots read against billboard_implied_bass.
The pop rules of v88 kept: 157 (no rhythm floor), 148 (two legs), 150 (text setting by class), 159-160 (pushed notes <= 42%,
read against the chord they anticipate), 163 (rhythm band 1.33-3.57), 134 (key word on a chord tone >= 40% of lines),
133 (chorus top not below the verse top), 165 (the summit D5 placed once, on 'for-EV-er'), 166 (monotony floor),
173-177 (harmony readings). Table B on the pop calibration; Table C ranks (118). Rerun record (145).
Usage: python3 melody_p36.py N [main|ctlA|ctlB]   ctlA: 181 and 182 off.  ctlB: the constructions off (184), the 182 walk kept."""
import sys, os, json, math, random, pickle, hashlib, collections, platform
import numpy as np
sys.path[:0] = ["/home/claude/p36", "/home/claude/carol", "/home/claude/pop"]
import engine_p36 as E, phrasestress48 as PS; PS.install(E); E.install_patches()
from measures import beta_pitch, s_spectral, cmp_score, m_horizon, PPM, ic_profile, feature_vec, basic
import lyric as L

HERE = "/home/claude/p36"
T = json.load(open(f"{HERE}/tables/zeneng_v88_tables.json"))
PM = T["pitch_model"]["pop_rock_country"]; KMAJ = PM["K_major"]; RSD, PSD = PM["R"], PM["P"]
BB = T["surprise_bands_pitch"]["billboard"]; PBAND = BB["surprise_bits_per_note"]; CG = BB["intervals"]
RT = T["rhythm_tables"]["pop_rock_country"]["4/4"]["table"]; RT = json.loads(RT) if isinstance(RT, str) else RT
RBAND = T["surprise_bands_rhythm"]["pop_hooktheory"]["4/4"]["rhythm_bits_per_note"]
RBC = T["rhythm_by_class"]["pop_hooktheory"]
OV = T["outer_voices"]["billboard_implied_bass"]
CAL = json.load(open("/home/claude/pop/pop_calibration.json")); C = CAL["cal"]
MU, SD = np.array(CAL["mu"]), np.array(CAL["sd"]); ZREF = np.array(CAL["Z"]); REAL_KNN = CAL["real_knn"]
PPMM = pickle.load(open("/home/claude/pop/pop_ppm.pkl", "rb"))

MODE = sys.argv[2] if len(sys.argv) > 2 else "main"
ON = dict(returns=MODE == "main", cg=MODE in ("main", "ctlB"), summit=MODE != "ctlB", monotony=MODE != "ctlB", leaps=MODE != "ctlB", caps=MODE != "ctlB")

TONIC = 3; BEAT = 12; BAR = 48; QBPM = 118; SEC_PER_TW = 60 / QBPM / BEAT
LO, SUMMIT = 58, 74                              # B-flat 3 .. the one D5
SCALE = {3, 5, 7, 8, 10, 0, 2}
SUNGPC = SCALE | {6, 1}                         # Table CG: pop alone sings flat 3 and flat 7 in major
CH = {"Eb": (3, {3, 7, 10}), "Bb": (10, {10, 2, 5}), "Cm": (0, {0, 3, 7}), "Ab": (8, {8, 0, 3}), "Db": (1, {1, 5, 8}), "Fm": (5, {5, 8, 0})}
ROMAN = {"Eb": "I", "Bb": "V", "Cm": "vi", "Ab": "IV", "Db": "bVII", "Fm": "ii"}
# section jobs (177): verse home, pre-chorus leaves, chorus arrives with a new chord (Db), bridge furthest and ends on V
PLAN = {"Intro": ["Eb", "Bb", "Cm", "Ab"],
        "Verse": ["Eb", "Eb", "Ab", "Eb", "Cm", "Ab", "Eb", "Bb"],
        "Pre": ["Ab", "Bb", "Cm", "Bb"],
        "Chorus": ["Eb", "Bb", "Cm", "Ab", "Eb", "Bb", "Ab", "Ab", "Eb", "Bb", "Cm", "Ab", "Eb", "Bb", "Db", "Eb"],
        "Bridge": ["Ab", "Cm", "Fm", "Db", "Ab", "Cm", "Fm", "Bb"],
        "Outro": ["Eb", "Bb", "Ab", "Eb"]}
FORM = [("Intro", "Intro", 4), ("Verse 1", "Verse", 8), ("Pre 1", "Pre", 4), ("Chorus 1", "Chorus", 16), ("Verse 2", "Verse", 8),
        ("Pre 2", "Pre", 4), ("Chorus 2", "Chorus", 16), ("Bridge", "Bridge", 8), ("Last Chorus", "Chorus", 16), ("Outro", "Outro", 4)]
BAR0, CHORD = {}, []
b = 0
for nm, kind, nb in FORM:
    BAR0[nm] = b; CHORD += PLAN[kind]; b += nb
NBARS = b; assert NBARS == 88 and len(CHORD) == 88
KIND = {nm: kind for nm, kind, _ in FORM}
SUNG = ["Verse 1", "Pre 1", "Chorus 1", "Verse 2", "Pre 2", "Chorus 2", "Bridge", "Last Chorus"]
WORDS_OF = dict(L.SECTIONS)
MUS = {"Verse": 64, "Pre": 66, "Chorus": 68, "Bridge": 65}
CAPS = {"Verse": 70, "Pre": 72, "Chorus": 72, "Bridge": 72}         # 133 by plan: verse top B-flat 4, the rest C5; 165: D5 once
FLOORS = {"Verse": 58, "Pre": 60, "Chorus": 62, "Bridge": 58}       # the plan: the chorus sung from D4 up (its lift over the verse)

# ---- the stress reading (191, and the secondary stresses: finding) ----
def is_weak_contraction(w): return "'" in w and w.split("'")[0] in {"i", "it", "they", "that", "there", "you", "we", "he", "she"}
def syl(text):
    """(word, stressed) per syllable. Polysyllables: the dictionary's primary stress only; two primaries in a word that is not a
    compound take the first (191); a secondary stress is kept only on a line's last syllable. Monosyllables as the engine reads
    them, a pronoun-auxiliary contraction or 'like' weak (fix 168's class, by rule), the line's last monosyllable stressed."""
    raw = E.syllables(text); out = []; i = 0
    while i < len(raw):
        j = i
        while j + 1 < len(raw) and raw[j + 1][0] == raw[i][0] and raw[j + 1][3] == raw[i][3] and len(raw[i][0]) > 1: j += 1
        grp = raw[i:j + 1]
        if len(grp) == 1:
            w = grp[0][0]; s = grp[0][2] and not is_weak_contraction(w) and w != "like"
            out.append([w, s])
        else:
            prim = [k for k, x in enumerate(grp) if x[1].endswith("1")]
            keep = (set(prim) if "-" in grp[0][0] else set(prim[:1])) if prim else {k for k, x in enumerate(grp) if x[2]}   # 191: a compound keeps both
            for k, x in enumerate(grp): out.append([x[0], k in keep])
            if j == len(raw) - 1 and grp[-1][1].endswith("2"): out[-1][1] = True
        i = j + 1
    if len(out) >= 1 and (len(out) < 2 or out[-2][0] != out[-1][0]): out[-1][1] = True
    return out
LINES = {nm: [syl(t) for _, t in WORDS_OF[nm]] for nm in SUNG}

# ---- metric weights, chords ----
def mw(t):
    t %= BAR
    return 1.0 if t == 0 else 0.8 if t == 24 else 0.55 if t % 12 == 0 else 0.35 if t % 6 == 0 else 0.08
def chord_at(t): return CHORD[max(0, min(NBARS - 1, t // BAR))]
def pushed(n, notes_on):
    nb = (n["on"] // BEAT + 1) * BEAT
    return n["on"] % BEAT != 0 and n["on"] + n["dur"] > nb and nb not in notes_on
def chord_for(n, notes_on):
    """160: a pushed note is read against the chord it anticipates."""
    if pushed(n, notes_on): return chord_at((n["on"] // BEAT + 1) * BEAT)
    return chord_at(n["on"])
def kp(p): return KMAJ[(p - TONIC) % 12]

# ---- the line's rhythm: a draw over the class's rhythm table, the stresses toward strong places (159, 161) ----
GRID = list(range(-12, 73, 3))          # pickups up to a beat; the line done by beat 3 of its second bar (v43's breath)
def line_rhythm(sy, rng, tmin):
    n = len(sy); st = [x[1] for x in sy]
    mono_weak = [not sy[k][1] and (k == 0 or sy[k - 1][0] != sy[k][0]) and (k == n - 1 or sy[k + 1][0] != sy[k][0]) for k in range(n)]
    def H(k, d):                                             # a weak monosyllable is not held (pop holds a word's last syllable, 150)
        return 1.0 if not mono_weak[k] else (0.1 if d >= 18 else 0.3 if d >= 12 else 1.0)
    Ls = max(k for k in range(n) if st[k]); post = n - 1 - Ls
    def A(k, t):
        m = mw(t)
        return {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if st[k] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
    tg = [(48, 0.55), (72, 0.25), (24, 0.12), (60, 0.08)]
    rng_t = [t for t, _ in tg]; w_t = [w for _, w in tg]
    for _ in range(6):
        tgt = rng.choices(rng_t, w_t)[0]
        if tgt + 3 * post > 72 or tgt - 3 * Ls < tmin: continue
        G = [t for t in GRID if t >= tmin]
        alpha = [dict() for _ in range(n)]
        for t in G:
            if t > tgt: break
            pr = 1.0 if t < 0 else (0.35 if t == 0 else 0.5)
            if Ls == 0 and t != tgt: continue
            alpha[0][t] = pr * A(0, t)
        for k in range(1, n):
            for t in G:
                if k == Ls and t != tgt: continue
                if k < Ls and t >= tgt: continue
                s = 0.0
                for tp, a in alpha[k - 1].items():
                    d = t - tp
                    if 3 <= d <= 24: s += a * RT[tp % BAR][d] * H(k - 1, d)
                if s > 0: alpha[k][t] = s * A(k, t)
        if not alpha[n - 1]: continue
        ks = list(alpha[n - 1]); ws = [alpha[n - 1][t] * (1.0 + (72 - t) / 40) for t in ks]
        ons = [rng.choices(ks, ws)[0]]
        for k in range(n - 1, 0, -1):
            t = ons[-1]; ks = [tp for tp in alpha[k - 1] if 3 <= t - tp <= 24]
            ws = [alpha[k - 1][tp] * RT[tp % BAR][t - tp] * H(k - 1, t - tp) for tp in ks]
            ons.append(rng.choices(ks, ws)[0])
        ons.reverse()
        return ons
    return None

def melismas(ons, sy, rng, final_mel=0.33, inner=0.11):
    """150: pop sets about 16% of syllables on two notes, a third of them at the phrase's end. Returns note rows (rel_on, syl, slur)."""
    rows = []
    for k, t in enumerate(ons):
        rows.append([t, k, False])
        nxt = ons[k + 1] if k + 1 < len(ons) else None
        if nxt is None:
            if t + 6 <= 72 and rng.random() < final_mel: rows.append([t + 6 if t % 6 == 0 else t + 3, k, True])
        elif nxt - t >= 12 and rng.random() < inner: rows.append([t + (nxt - t) // 2 // 3 * 3, k, True])
    return rows

# ---- the walk (182): Table CG's moves, then the pitch by the class's range and key terms ----
CATS = [("repeat", CG["repeat"], [0]), ("step", CG["step"], [1, 2]), ("third", CG["third"], [3, 4]), ("fourth_fifth", CG["fourth_fifth"], [5, 7]),
        ("larger", CG["larger"], [8, 9, 12, 10, 11])]
SIZE_W = {8: 1.0, 9: 1.0, 12: 0.8, 10: 0.35, 11: 0.15}
DESC = 1 - CG["ascending_share_of_moves"]
def clash(p, ch):
    """flat 3 and flat 7 are sung where no chord tone lies a semitone away and the note is no tritone from the root."""
    pc = p % 12
    if pc in SCALE: return False
    root, tones = CH[ch]
    return any(abs((pc - t) % 12) in (1, 11) for t in tones) or (pc - root) % 12 == 6
def chord_w(p, n, ch, cg):
    tones = CH[ch][1]; strong = n["on"] % BEAT == 0
    if cg: return (2.0 if p % 12 in tones else 0.5) if (strong and n.get("stress")) else (1.3 if p % 12 in tones else 1.0)
    return (4.0 if p % 12 in tones else 0.3) if strong else (1.6 if p % 12 in tones else 1.0)
def next_pitch(rng, prev, run, n, ch, mu, lo, hi, cg=True, monotony=True, leaps=True, last_iv=None):
    if prev is None:
        cands = [p for p in range(lo, hi + 1) if p % 12 in SCALE]
        return rng.choices(cands, [math.exp(-(p - mu) ** 2 / (2 * RSD ** 2)) * kp(p) * chord_w(p, n, ch, cg) for p in cands])[0]
    if cg:
        cats = list(CATS)
        if last_iv is not None and abs(last_iv) > 7:          # after a leap past a fifth the line turns back by a step or a third
            cats = [x for x in CATS if x[0] in ("step", "third")]
        while cats:
            c = rng.choices(cats, [x[1] for x in cats])[0]
            sizes = list(c[2]) if leaps else (list(c[2]) + ([6] if c[0] == "fourth_fifth" else []) + ([13, 14] if c[0] == "larger" else []))
            cands, ws = [], []
            for sz in sizes:
                for sg in ((0,) if sz == 0 else (-1, 1)):
                    p = prev + sg * sz
                    if not (lo <= p <= hi) or p % 12 not in SUNGPC or clash(p, ch): continue
                    if sz == 0 and monotony and run >= 3: continue
                    if last_iv is not None and abs(last_iv) > 7 and (sg > 0) == (last_iv > 0): continue
                    w = math.exp(-(p - mu) ** 2 / (2 * RSD ** 2)) * kp(p) * chord_w(p, n, ch, True) * SIZE_W.get(sz, 1.0)
                    w *= 1.0 if sz == 0 else (DESC if sg < 0 else 1 - DESC)
                    cands.append(p); ws.append(w)
            if cands and sum(ws) > 0: return rng.choices(cands, ws)[0]
            cats.remove(c)
        return None
    # the walk before 182 (the back-test's engine): proximity sd 2 round the last note, leaps to a fifth, the old chord weights
    cands, ws = [], []
    for p in range(lo, hi + 1):
        if p % 12 not in SCALE and p % 12 not in CH[ch][1]: continue
        if leaps and (abs(p - prev) > 7 or abs(p - prev) == 6): continue
        if monotony and run >= 3 and p == prev: continue
        w = math.exp(-(p - prev) ** 2 / (2 * 2.0 ** 2)) * math.exp(-(p - mu) ** 2 / (2 * RSD ** 2)) * kp(p) * chord_w(p, n, ch, False)
        cands.append(p); ws.append(w)
    return rng.choices(cands, ws)[0] if cands else None

def walk_notes(rng, notes, prev, run, mu, lo, hi, notes_on, fixed=None):
    out = []; notes_on = set(notes_on) | {n["on"] for n in notes}; last_iv = None
    for i, n in enumerate(notes): n["dur"] = notes[i + 1]["on"] - n["on"] if i + 1 < len(notes) else 24
    for i, n in enumerate(notes):
        if fixed and i in fixed: p = fixed[i]
        elif n["slur"] and out:                                   # the second note of a syllable: a step, mostly down
            q = out[-1]; opts = [x for x in (q - 2, q - 1, q + 1, q + 2) if lo <= x <= hi and x % 12 in SCALE]
            p = rng.choices(opts, [3 if x < q else 1 for x in opts])[0] if opts else q
        else:
            p = next_pitch(rng, prev, run, n, chord_for(n, notes_on), mu, lo, hi, ON["cg"], ON["monotony"], ON["leaps"], last_iv)
            if p is None: return None
        run = run + 1 if p == prev else 1
        last_iv = (p - prev) if prev is not None else None
        prev = p; out.append(p)
    return out

# ---- a line's notes ----
def fresh_line(sy, rng, U, tmin):
    ons = line_rhythm(sy, rng, tmin)
    if ons is None: return None
    rows = melismas(ons, sy, rng)
    return [dict(on=U + t, p=None, syl=k, slur=s, stress=(sy[k][1] and not s)) for t, k, s in rows]

def align(src, src_sy, sy, U0, U, tmin=-12):
    """map a line's words onto a source line's notes (181): the source's events kept; a syllable may take two events (a slur);
    up to three unstressed leading syllables go before the first event as a pickup (outside the unit, so the unit's onsets are
    untouched); where words remain over, the longest events are split. Returns notes at unit U with the source's pitches."""
    best = None
    for npk in range(0, 4):
        if npk and any(x[1] for x in sy[:npk]): break
        ev = [dict(t=n["on"] - U0, p=n["p"]) for n in src]
        t0 = ev[0]["t"]; gap = 6 if t0 - 6 * npk >= max(tmin, -12) else 3
        if npk and t0 - gap * npk < max(tmin, -12): break
        sgn = -1 if dshift(ev[0]["p"], -npk) >= LO else 1
        pk = [dict(t=t0 - gap * (npk - q), p=dshift(ev[0]["p"], sgn * (npk - q))) for q in range(npk)]
        r = _align(ev, sy[npk:])
        if r is None: continue
        cost, out = r; cost += 0.35 * npk
        out = [dict(on=U + e["t"], p=e["p"], syl=q, slur=False, stress=False) for q, e in enumerate(pk)] + \
              [dict(on=U + t, p=p, syl=i + npk, slur=sl, stress=stv) for t, p, i, sl, stv in out]
        if best is None or cost < best[0]: best = (cost, out)
    return best[1] if best else None
def _align(ev, sy):
    n_s = len(sy); splits = 0
    while len(ev) < n_s:                                         # split the longest event
        iois = [(ev[k + 1]["t"] - ev[k]["t"] if k + 1 < len(ev) else min(12, 72 - ev[k]["t"]), k) for k in range(len(ev))]
        d, k = max(iois)
        if d < 6: return None
        p0 = ev[k]["p"]; p1 = ev[k + 1]["p"] if k + 1 < len(ev) else p0 - 1
        pn = dshift(p0, 1 if p1 > p0 else -1) if p1 != p0 else dshift(p0, -1)
        if pn < LO: pn = p0
        ev.insert(k + 1, dict(t=ev[k]["t"] + d // 2 // 3 * 3, p=pn)); splits += 1
    m = len(ev); INF = 1e9
    st = [x[1] for x in sy]
    def cost(i, j0, j1):                                        # syllable i on events j0..j1-1
        mm = mw(ev[j0]["t"]); c = (1 - mm) * 1.2 if st[i] else mm * 0.6
        return c + 0.45 * (j1 - j0 - 1) + (0.6 if j1 - j0 > 2 else 0)
    f = [[INF] * (m + 1) for _ in range(n_s + 1)]; bk = [[None] * (m + 1) for _ in range(n_s + 1)]; f[0][0] = 0
    for i in range(1, n_s + 1):
        for j in range(i, m + 1):
            for j0 in range(max(i - 1, j - 3), j):
                if f[i - 1][j0] + cost(i - 1, j0, j) < f[i][j]: f[i][j] = f[i - 1][j0] + cost(i - 1, j0, j); bk[i][j] = j0
    if f[n_s][m] >= INF: return None
    seg = []; j = m
    for i in range(n_s, 0, -1): j0 = bk[i][j]; seg.append((i - 1, j0, j)); j = j0
    seg.reverse(); out = []
    for i, j0, j1 in seg:
        for jj in range(j0, j1): out.append((ev[jj]["t"], ev[jj]["p"], i, jj > j0, st[i] and jj == j0))
    return f[n_s][m] + 0.8 * splits, out

DEG = sorted(p for p in range(48, 84) if p % 12 in SCALE)
def dshift(p, k):
    if p not in DEG: return dshift(p + 1, k) if (p + 1) in DEG else dshift(p - 1, k)   # flat 3 / flat 7 move as the degree above
    i = DEG.index(p); return DEG[max(0, min(len(DEG) - 1, i + k))]

def finish(notes):
    """durations: each note to the next onset in its line; the line's last note held to a half-beat breath before the next line (v43)."""
    for i, n in enumerate(notes):
        nx = notes[i + 1]["on"] if i + 1 < len(notes) else None
        if nx is None: n["dur"] = 48
        elif notes[i + 1]["line"] != n["line"]: n["dur"] = min(60, max(3, nx - n["on"] - 6))
        else: n["dur"] = nx - n["on"]
    return notes

def join_bad(a, b2): return a is not None and (abs(b2 - a) > 9 or abs(b2 - a) == 6)
def fix_join(rng, ns, prev, run, mu, lo, hi, U, notes_on):
    """a copied or returning line that leaps into its first note past a sixth: its pickup (which sits in the unit before, so the
    return's own unit is untouched) is drawn again by the walk; a line with no pickup is moved by a diatonic step if that mends it."""
    if not join_bad(prev, ns[0]["p"]): return True
    pk = [j for j, n in enumerate(ns) if n["on"] < U]
    if pk:
        for _ in range(12):
            fx = {j: ns[j]["p"] for j in range(len(ns)) if j not in pk}
            ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on, fixed=fx)
            if ps and not join_bad(prev, ps[0]) and not join_bad(ps[len(pk) - 1], ps[len(pk)]) if len(pk) < len(ns) else ps:
                for n, p in zip(ns, ps): n["p"] = p
                return True
        return False
    return "prev"

# ---- letter plans (181) ----
VERSE_PLANS = ["ABAC", "AABC", "ABAB"]
BRIDGE_PLANS = ["AABC", "ABAC"]
CHORUS_HEADS = ["ABCD", "ABAC"]
def admissible(sec, plans):
    """a form may name a return only between lines whose syllable counts differ by three or fewer: past that, no mapping of the
    words onto the first unit's rhythm keeps the two related (181), and the plan falls back to ABCD."""
    ok = []
    for pl in plans:
        if all(abs(len(LINES[sec][i]) - len(LINES[sec][pl.index(x)])) <= 3 for i, x in enumerate(pl)): ok.append(pl)
    return ok or ["ABCD"]
def repair_returns(c, lines, built):
    """181 by construction: a declared return that the ending's change (or a transposition across the key) has left unrelated is
    given back its first unit's pitches exactly; the chorus's rhymed end (line 8) keeps the tonic close."""
    notes = c["notes"]
    for sec, i, s0, i0, ub in c["meta"]["returns"]:
        if (sec, i) == ("Last Chorus", 7): continue
        U = (BAR0[sec] + 2 * i) * BAR; U0 = (BAR0[s0] + 2 * i0) * BAR
        if related(unit(notes, U, ub * BAR), unit(notes, U0, ub * BAR))[0]: continue
        for d in range(ub // 2):
            ns = built[(sec, i + d)]; src = align(built[(s0, i0 + d)], LINES[s0][i0 + d], LINES[sec][i + d], U0 + 2 * d * BAR, U + 2 * d * BAR)
            if src is None or len(src) != len(ns): continue
            old = [n["p"] for n in ns]
            keep_last = KIND[sec] == "Chorus" and i + d == 7
            for j, (n, m) in enumerate(zip(ns, src)):
                if keep_last and j == len(ns) - 1: continue
                if n["on"] < U + 2 * d * BAR: continue                   # the pickup, outside the unit, stays as the join mended it
                n["p"] = m["p"]
            k0 = notes.index(ns[0]); k1 = notes.index(ns[-1])
            seg = notes[max(0, k0 - 1): k1 + 2]
            if any(abs(b3["p"] - a["p"]) > 12 or abs(b3["p"] - a["p"]) == 6 for a, b3 in zip(seg, seg[1:])):
                for n, p in zip(ns, old): n["p"] = p                   # a restoration that would break a join is not made
def generate(rng):
    plans = dict(Verse=list(rng.choice(admissible("Verse 1", VERSE_PLANS))), Bridge=list(rng.choice(admissible("Bridge", BRIDGE_PLANS))),
                 ChorusHead=list(rng.choice(admissible("Chorus 1", CHORUS_HEADS))), Pre=list("AB"))
    plans["Chorus"] = plans["ChorusHead"] + [x + "'" for x in plans["ChorusHead"]]     # the 16-bar period with rhymed ends
    lines = []                                           # per line: dict(sec, idx, U, notes)
    built = {}                                           # (sec, idx) -> notes
    prev, run, last_on = None, 0, -10 ** 6
    notes_on_all = set()
    meta = dict(plans=plans, returns=[], shifts={})
    def place(sec, i, notes):
        nonlocal prev, run, last_on
        for n in notes: n["sec"] = sec; n["line"] = f"{sec}:{i}"
        built[(sec, i)] = notes; lines.append(dict(sec=sec, idx=i, notes=notes))
        prev = notes[-1]["p"]; last_on = notes[-1]["on"]
        rr = 1
        for a, b2 in zip(notes[::-1], notes[-2::-1]):
            if a["p"] == b2["p"]: rr += 1
            else: break
        run = rr
    for sec in SUNG:
        kind = KIND[sec]; U0 = BAR0[sec] * BAR; mu = MUS[kind]; hi = CAPS[kind] if ON["caps"] else SUMMIT; lo = FLOORS[kind] if ON["caps"] else LO
        sys_ = LINES[sec]
        src_sec = {"Verse 2": "Verse 1", "Pre 2": "Pre 1", "Chorus 2": "Chorus 1", "Last Chorus": "Chorus 1"}.get(sec)
        plan = plans["Chorus"] if kind == "Chorus" else plans[kind]
        for i, sy in enumerate(sys_):
            U = U0 + 2 * i * BAR; tmin = max(-12, last_on + 12 - U)
            lt = plan[i] if i < len(plan) else chr(65 + i)
            first = plan.index(lt[0]) if lt[0] in plan else i
            if src_sec:                                                       # a later verse, pre-chorus or chorus: its first's tune
                S = built[(src_sec, i)]; Ssy = LINES[src_sec][i]; SU = BAR0[src_sec] * BAR + 2 * i * BAR
                if sec == "Last Chorus" and i == 7:                          # 180: the idea stated a third time -- line 8 on the hook
                    S = built[("Chorus 1", 0)]; Ssy = LINES["Chorus 1"][0]; SU = BAR0["Chorus 1"] * BAR
                if [x[0] for x in Ssy] == [x[0] for x in sy]: ns = [dict(n, on=n["on"] - SU + U) for n in S]
                elif sec == "Last Chorus" and i == 7 and [x[0] for x in sy[-len(Ssy) + 1:]] == [x[0] for x in Ssy[1:]]:
                    # the hook's notes kept whole under 'so I dance anyway' ('so' for 'so'); 'I'm still here' sung before it
                    hk = [dict(n, on=n["on"] - SU + U) for n in S]; npre = len(sy) - len(Ssy)
                    room = [t for t in range(max(tmin, -6), hk[0]["on"] - U - 5, 3)]
                    if len(room) < 2 * npre:                                  # no room: the hook a bar later, its last word on the outro's downbeat
                        for n in hk: n["on"] += BAR
                        room = [t for t in range(max(tmin, -6), hk[0]["on"] - U - 5, 3)]
                    h0 = hk[0]["on"] - U; slots = [t for t in range(max(tmin, h0 - 27), h0 - 2, 3)]
                    best = None
                    import itertools
                    for comb in itertools.combinations(slots, npre):
                        iois = [b3 - a for a, b3 in zip(comb, list(comb[1:]) + [h0])]
                        if max(iois) > 12: continue
                        w = 1.0
                        for q, t in enumerate(comb):
                            m = mw(t); w *= {1.0: 1.0, 0.8: 0.8, 0.55: 0.5, 0.35: 0.3, 0.08: 0.05}[m] if sy[q][1] else {1.0: 0.06, 0.8: 0.15, 0.55: 0.5, 0.35: 1.0, 0.08: 0.8}[m]
                        if best is None or w > best[0]: best = (w, comb)
                    if best is None: return None, "align: no room before the hook"
                    pre_on = [U + t for t in best[1]]
                    pre = [dict(on=t, p=None, syl=q, slur=False, stress=sy[q][1]) for q, t in enumerate(pre_on)]
                    ps = walk_notes(rng, pre, prev, run, mu, lo, hi, notes_on_all)
                    if ps is None: return None, "walk: no note"
                    for n, p in zip(pre, ps): n["p"] = p
                    for n in hk: n["syl"] += npre
                    ns = pre + hk
                else: ns = align(S, Ssy, sy, SU, U, tmin)
                if ns is None: return None, "align: the words do not fit the tune"
                ns = [dict(n) for n in ns]
                if sec == "Last Chorus" and i == 7:
                    meta["returns"].append(("Last Chorus", 7, "Chorus 1", 0, 2))
            elif first < i and lt[0] in plan and len(lt) >= 1 and (sec, first) in built:   # a return named by the form (181)
                S = built[(sec, first)]; Ssy = sys_[first]; SU = U0 + 2 * first * BAR
                ns = align(S, Ssy, sy, SU, U, tmin)
                if ns is None: return None, "align: the words do not fit the returning unit"
                if kind != "Chorus" or i < 4: meta["returns"].append((sec, i, sec, first, 2))
                if kind == "Chorus" and i in (4, 6): meta["returns"].append((sec, i, sec, i - 4, 4))   # the 16-bar period: units of four bars
                if ON["returns"]:
                    k = rng.choices([0, 1, -1, 2, -2], [0.55, 0.13, 0.12, 0.1, 0.1])[0]
                    if kind == "Chorus" and i == 6:                              # the rhymed end (180): the level that closes on the tonic
                        last3 = built[(sec, 3)][-1]["p"]
                        ks = [k2 for k2 in (0, 1, -1, 2, -2) if dshift(last3, k2) % 12 == TONIC] or \
                             [k2 for k2 in (0, 1, -1, 2, -2) if dshift(last3, k2) % 12 in (7, 10)]
                        if ks: k = ks[0]
                    if kind == "Chorus" and i in (5, 7): k = meta["shifts"].get((sec, i - 1), 0)   # one level for a four-bar unit
                    ps = [dshift(n["p"], k) for n in ns]
                    def bad_iv(ps): return any(abs(y - x) > 12 or abs(y - x) == 6 for x, y in zip(ps, ps[1:]))
                    if max(ps) > hi or min(ps) < lo or bad_iv(ps): k = 0; ps = [n["p"] for n in ns]
                    meta["shifts"][(sec, i)] = k
                    for n, p in zip(ns, ps): n["p"] = p
                    tail = 1 if len(ns) >= 4 else 0                            # its ending may change
                    if tail and rng.random() < 0.6 and not (kind == "Chorus" and i in (4, 6, 7)):
                        fx = {j: ns[j]["p"] for j in range(len(ns) - tail)}
                        ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all, fixed=fx)
                        if ps is None: return None, "walk: no note"
                        for n, p in zip(ns, ps): n["p"] = p
                else:                                                         # the old cell grammar: the same rhythm, new pitches
                    ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all)
                    if ps is None: return None, "walk: no note"
                    for n, p in zip(ns, ps): n["p"] = p
            else:
                ns = fresh_line(sy, rng, U, tmin)
                if ns is None: return None, "rhythm: no placement"
                ps = walk_notes(rng, ns, prev, run, mu, lo, hi, notes_on_all)
                if ps is None: return None, "walk: no note"
                for n, p in zip(ns, ps): n["p"] = p
            if ns[0]["on"] - last_on < 12: return None, "join: no breath before the line"
            fj = fix_join(rng, ns, prev, run, mu, lo, hi, U, notes_on_all)
            if fj == "prev" and lines:                     # no pickup: the line before ends on a chord tone a sixth or less from both sides
                pl = lines[-1]["notes"]; q0 = pl[-2]["p"] if len(pl) >= 2 else None; ch = CH[chord_at(pl[-1]["on"])][1]
                opts = [p for p in range(lo, hi + 1) if p % 12 in ch and not join_bad(p, ns[0]["p"]) and not join_bad(q0, p)]
                if opts and not (lines[-1]["sec"] == "Last Chorus" and lines[-1]["idx"] == 6):
                    pl[-1]["p"] = min(opts, key=lambda p: abs(p - pl[-1]["p"])); prev = pl[-1]["p"]; fj = True
            if fj is not True: return None, "join: a leap into the line nothing can mend"
            # 165: the summit placed -- D5 on 'for-EV-er', its phrase capped a step below (the caps hold everywhere else)
            if sec == "Last Chorus" and i == 6 and ON["summit"]:
                j = [x[0] for x in sy].index("forever"); j = j + 1
                tgt = [n for n in ns if n["syl"] == j and not n["slur"]][0]; tgt["p"] = SUMMIT
                k = ns.index(tgt)
                ok = lambda a, b3: abs(b3 - a) <= 7 and abs(b3 - a) != 6
                if k > 0 and not ok(ns[k - 1]["p"], SUMMIT):
                    q = ns[k - 2]["p"] if k >= 2 else prev
                    ns[k - 1]["p"] = min([67, 70, 72], key=lambda p: (not ok(q, p) if q is not None else 0, abs(p - (q or 70))))
                for n in ns[k + 1:]:
                    if n["p"] > 72: n["p"] = 72
                if k + 1 == len(ns) - 1 and ns[k + 1]["on"] - tgt["on"] < 12:      # 151/150: the summit held, the last syllable after it
                    ns[k + 1]["on"] = min(U + 72, tgt["on"] + 12)
                if k + 1 < len(ns) and not ok(SUMMIT, ns[k + 1]["p"]):
                    q = ns[k + 2]["p"] if k + 2 < len(ns) else None
                    ns[k + 1]["p"] = min([67, 70, 72], key=lambda p: (not ok(p, q) if q is not None else 0, abs(p - (q or 70))))
            # 180 / the chorus close: the chorus ends on a tone of the tonic chord (the nearest, so the rhymed end stays related);
            # the song's last line on the tonic itself
            if kind == "Chorus" and i == 7:
                pcs = (TONIC,) if sec == "Last Chorus" else (TONIC, 7, 10)
                if ns[-1]["p"] % 12 not in pcs:
                    q = ns[-1]["p"]; opts = [p for p in range(lo, 73) if p % 12 in pcs and not join_bad(ns[-2]["p"], p)] or [p for p in range(lo, 73) if p % 12 in pcs]
                    ns[-1]["p"] = min(opts, key=lambda p: (abs(p - q), p % 12 != TONIC))
            for n in ns: notes_on_all.add(n["on"])
            place(sec, i, ns)
    notes = [n for l in lines for n in l["notes"]]
    notes.sort(key=lambda n: n["on"])
    c = dict(notes=notes, meta=meta)
    if ON["returns"]: repair_returns(c, lines, built)
    on = {n["on"] for n in notes}
    for i, n in enumerate(notes):                    # a copied flat 3 or flat 7 that now clashes with its chord moves to the scale
        n.setdefault("dur", 12)
        if n["p"] % 12 in (6, 1) and clash(n["p"], chord_for(n, on)):
            tones = CH[chord_for(n, on)][1]
            n["p"] = min((n["p"] - 1, n["p"] + 1), key=lambda q: (q % 12 not in tones, q % 12 not in SCALE))
    finish(notes)
    return c, None

# ---- readings ----
def pitch_bits(ps):
    mu = float(np.mean(ps)); out = []
    cands = range(int(round(mu)) - 26, int(round(mu)) + 27)
    for a, b2 in zip(ps, ps[1:]):
        w = {q: math.exp(-(q - mu) ** 2 / (2 * RSD ** 2)) * math.exp(-(q - a) ** 2 / (2 * PSD ** 2)) * kp(q) for q in cands}
        out.append(-math.log2(w[b2] / sum(w.values())))
    return float(np.mean(out))
def rhythm_bits(notes):
    ons = [n["on"] for n in notes] + [NBARS * BAR]; out = []
    for a, b2 in zip(ons, ons[1:]):
        out.append(-math.log2(max(1e-9, RT[a % BAR][min(96, b2 - a)])))
    return float(np.mean(out))
def interval_shares(ps):
    iv = [b2 - a for a, b2 in zip(ps, ps[1:])]; n = len(iv)
    mv = [x for x in iv if x]
    return dict(repeat=sum(1 for x in iv if x == 0) / n, step=sum(1 for x in iv if abs(x) in (1, 2)) / n, third=sum(1 for x in iv if abs(x) in (3, 4)) / n,
                fourth_fifth=sum(1 for x in iv if abs(x) in (5, 6, 7)) / n, larger=sum(1 for x in iv if abs(x) > 7) / n,
                descending=sum(1 for x in mv if x < 0) / max(1, len(mv)), mean_abs=float(np.mean([abs(x) for x in iv])))
def sung_bars():
    return [b2 for s in SUNG for b2 in range(BAR0[s], BAR0[s] + dict((nm, nb) for nm, _, nb in FORM)[s])]
def bar_cells(notes):
    by = collections.OrderedDict((b2, []) for b2 in sung_bars())
    for n in notes:
        b2 = n["on"] // BAR
        if b2 in by: by[b2].append((n["on"] - b2 * BAR, n["p"]))
    return by
def repetition(notes):
    by = bar_cells(notes); seen = []; out = collections.Counter(); bars = 0
    rhy_seen = set()
    for b2, cell in by.items():
        if not cell: continue
        bars += 1; r = tuple(t for t, _ in cell); p = tuple(q for _, q in cell)
        ivs = tuple(y - x for x, y in zip(p, p[1:])); kind = "new"
        for r0, p0, iv0 in seen:
            if r0 == r and p0 == p: kind = "exact"; break
        else:
            for r0, p0, iv0 in seen:
                if r0 == r and iv0 == ivs: kind = "transposed"; break
            else:
                for r0, p0, iv0 in seen:
                    if r0 == r and len(p0) == len(p) and all((a > 0) == (b3 > 0) and (a < 0) == (b3 < 0) for a, b3 in zip(iv0, ivs)): kind = "reshaped"; break
                else:
                    if r in rhy_seen: kind = "rhythm_only"
        out[kind] += 1; seen.append((r, p, ivs)); rhy_seen.add(r)
    res = {k: out[k] / bars for k in ("exact", "transposed", "reshaped", "rhythm_only", "new")}
    res["rhythm_recurs"] = 1 - res["new"] - 0  # rhythm heard before (any kind but new)
    res["rhythm_recurs"] = (out["exact"] + out["transposed"] + out["reshaped"] + out["rhythm_only"]) / bars
    res["bars"] = bars; res["distinct_rhythms"] = len(rhy_seen)
    return res
def sequences(notes):
    by = bar_cells(notes); legs = []; run = 1; ks = list(by)
    for a, b2 in zip(ks, ks[1:]):
        A_, B_ = by[a], by[b2]
        same = b2 == a + 1 and len(A_) == len(B_) >= 2 and [t for t, _ in A_] == [t for t, _ in B_] and len({y - x for (_, x), (_, y) in zip(A_, B_)}) == 1 and A_ != B_
        if same: run += 1
        else:
            if run >= 2: legs.append(run)
            run = 1
    if run >= 2: legs.append(run)
    return legs

# 27.31: relatedness and the phrase design
def unit(notes, s, ln):
    ns = [n for n in notes if s <= n["on"] < s + ln]
    ons = {n["on"] - s for n in ns}
    ser = []
    if ns:
        k = 0; cur = ns[0]["p"]
        for t in range(s, s + ln, 3):
            while k < len(ns) and ns[k]["on"] <= t: cur = ns[k]["p"]; k += 1
            ser.append(cur)
    return ons, ser, ns
def related(u1, u2):
    o1, s1, _ = u1; o2, s2, _ = u2
    if not o1 or not o2: return False, 0.0, 0.0
    jac = len(o1 & o2) / len(o1 | o2)
    a, b2 = np.array(s1, float), np.array(s2, float)
    if a.std() == 0 and b2.std() == 0: r = 1.0
    elif a.std() == 0 or b2.std() == 0: r = 0.0
    else: r = float(np.corrcoef(a, b2)[0, 1])
    return (jac >= 0.6 and r >= 0.6), jac, r
def design(notes, start_bar, unit_bars):
    ln = unit_bars * BAR; us = [unit(notes, (start_bar + k * unit_bars) * BAR, ln) for k in range(4)]
    r2 = related(us[1], us[0]); r3 = related(us[2], us[0]); r42 = related(us[3], us[1])
    lab = "repeated idea" if r2[0] and r3[0] else "sentence" if r2[0] else "period" if r3[0] else "contrasting"
    end2 = us[1][2][-1]["p"] % 12 == TONIC if us[1][2] else False; end4 = us[3][2][-1]["p"] % 12 == TONIC if us[3][2] else False
    return dict(label=lab, u2=r2, u3=r3, u4_returns_u2=r42[0], u42=r42, second_half_closes=(end4 and not end2))
SPANS8 = [("Verse 1", 0), ("Chorus 1", 0), ("Chorus 1", 8), ("Verse 2", 0), ("Chorus 2", 0), ("Chorus 2", 8), ("Bridge", 0), ("Last Chorus", 0), ("Last Chorus", 8)]
SPANS16 = ["Chorus 1", "Chorus 2", "Last Chorus"]
def phrase_designs(notes):
    d8 = {f"{s} bars {o + 1}-{o + 8}": design(notes, BAR0[s] + o, 2) for s, o in SPANS8}
    d16 = {s: design(notes, BAR0[s], 4) for s in SPANS16}
    stock8 = sum(1 for v in d8.values() if v["label"] != "contrasting") / len(d8)
    stock16 = sum(1 for v in d16.values() if v["label"] != "contrasting") / len(d16)
    return dict(at8=d8, at16=d16, stock8=stock8, stock16=stock16)
def returns_related(c):
    """181's check: every return the form named is related to its first unit (the ending may change)."""
    out = []
    for sec, i, s0, i0, ub in c["meta"]["returns"]:
        U = (BAR0[sec] + 2 * i) * BAR; U0 = (BAR0[s0] + 2 * i0) * BAR
        out.append(((sec, i, s0, i0, ub),) + related(unit(c["notes"], U, ub * BAR), unit(c["notes"], U0, ub * BAR)))
    return out

def outer(notes):
    """183: the bass is the chord roots, read against the implied-bass bands; 193: contrary perfects printed."""
    roots = [36 + ((CH[ch][0] - 3) % 12) + 3 for ch in CHORD]                 # E-flat 2 .. D3
    moves = []; prev = None; ons = {n["on"] for n in notes}
    for b2 in range(NBARS):
        if roots[b2] != prev:
            n = next((m for m in notes if m["on"] <= b2 * BAR < m["on"] + m["dur"]), None)
            if n: moves.append((b2 * BAR, roots[b2], n["p"], n["on"] == b2 * BAR))
        prev = roots[b2]
    ic = collections.Counter(); mo = collections.Counter(); par = dirp = contp = 0
    for t, bb, m, s in moves:
        iv = (m - bb) % 12
        ic["imperfect" if iv in (3, 4, 8, 9) else "perfect" if iv in (0, 7) else "fourth" if iv == 5 else "dissonance"] += 1
    for (t1, b1, m1, _), (t2, b2_, m2, _) in zip(moves, moves[1:]):
        db, dm = b2_ - b1, m2 - m1
        k = "oblique" if dm == 0 or db == 0 else "contrary" if (db > 0) != (dm > 0) else "parallel" if abs(db) == abs(dm) else "similar"
        mo[k] += 1; pf = (m2 - b2_) % 12 in (0, 7)
        if k in ("parallel", "similar") and pf and (m1 - b1) % 12 == (m2 - b2_) % 12: par += 1
        if k == "similar" and pf and abs(dm) > 2: dirp += 1
        if k == "contrary" and pf: contp += 1
    n = max(1, len(moves)); nm = max(1, len(moves) - 1)
    steps = sum(1 for a, b3 in zip(moves, moves[1:]) if abs(b3[1] - a[1]) in (1, 2)); f45 = sum(1 for a, b3 in zip(moves, moves[1:]) if abs(b3[1] - a[1]) in (5, 7))
    return dict(moves=len(moves), imperfect=ic["imperfect"] / n, perfect=ic["perfect"] / n, fourth=ic["fourth"] / n, dissonance=ic["dissonance"] / n,
                oblique=mo["oblique"] / nm, contrary=mo["contrary"] / nm, similar=mo["similar"] / nm, parallel=mo["parallel"] / nm,
                parallel_perfect=par / n, direct_perfect=dirp / nm, contrary_perfect=contp / nm, bass_by_step=steps / nm, bass_by_4th_5th=f45 / nm,
                struck_together=sum(1 for m in moves if m[3]) / n)
def keyword_chord(notes):
    on = {n["on"] for n in notes}; hit = tot = 0; rows = []
    for ln in dict.fromkeys(n["line"] for n in notes):
        ns = [n for n in notes if n["line"] == ln]; ks = [n for n in ns if n["stress"]]
        if not ks: continue
        n = ks[-1]; ch = chord_for(n, on); ok = n["p"] % 12 in CH[ch][1]
        tot += 1; hit += ok; rows.append((ln, n["p"], ch, ok))
    return hit / tot, rows
def chord_tone_share(notes):
    on = {n["on"] for n in notes}; ct = 0; res = 0; nct = 0
    for i, n in enumerate(notes):
        ch = chord_for(n, on)
        if n["p"] % 12 in CH[ch][1]: ct += 1
        else:
            nct += 1
            if i + 1 < len(notes) and notes[i + 1]["line"] == n["line"] and abs(notes[i + 1]["p"] - n["p"]) <= 2 and notes[i + 1]["p"] % 12 in CH[chord_for(notes[i + 1], on)][1]: res += 1
    return ct / len(notes), res / max(1, nct)
def pushed_share(notes):
    on = {n["on"] for n in notes}; return sum(1 for n in notes if pushed(n, on)) / len(notes)
def density(notes):
    secs = sum(dict((nm, nb) for nm, _, nb in FORM)[s] for s in SUNG) * BAR * SEC_PER_TW
    return len(notes) / secs
def monotony(notes):
    run = 1; worst = 1
    for a, b2 in zip(notes, notes[1:]):
        run = run + 1 if a["p"] == b2["p"] and a["line"] == b2["line"] else 1; worst = max(worst, run)
    distinct = min(len({n["p"] for n in notes if n["line"] == ln}) for ln in dict.fromkeys(n["line"] for n in notes))
    return worst, distinct
def leaps(notes):
    iv = [b2["p"] - a["p"] for a, b2 in zip(notes, notes[1:])]
    return max(abs(x) for x in iv), sum(1 for x in iv if abs(x) == 6)
def sec_notes(notes, s): return [n for n in notes if n["sec"] == s]
def contour(ps):
    if len(ps) < 3 or max(ps) - min(ps) <= 2: return "flat"
    i = ps.index(max(ps))
    if 0 < i < len(ps) - 1 and max(ps) - ps[0] >= 3 and max(ps) - ps[-1] >= 3: return "arch"
    if ps[-1] - ps[0] >= 3: return "ascending"
    if ps[0] - ps[-1] >= 3: return "descending"
    return "wave"
def quarters(ns, off=0): return [((n["on"] - off) / BEAT, n["dur"] / BEAT, n["p"]) for n in ns]
def chords_completable(notes):
    """192: at each note, two inner voices complete the chord (the band's triad) without doubling the leading note or a seventh in
    the outer voices, and the bass sits a fifth or more below the tune. Roots in E-flat 2 .. D3; the tune B-flat 3 up."""
    bad = 0; on = {n["on"] for n in notes}
    for n in notes:
        ch = chord_for(n, on); root = 36 + ((CH[ch][0] - 3) % 12) + 3
        if n["p"] - root < 7: bad += 1
        if ch == "Bb" and n["p"] % 12 == 2 and root % 12 == 2: bad += 1
    return bad

def register_bad(notes):
    """133: each chorus's top not below its verse's (the last chorus after the bridge: against verse 2)."""
    top = lambda s: max(n["p"] for n in notes if n["sec"] == s)
    return [(v, h) for v, h in (("Verse 1", "Chorus 1"), ("Verse 2", "Chorus 2"), ("Verse 2", "Last Chorus")) if top(h) < top(v)]
NEW_GATES = ["pitch band (153/182)", "rhythm band (163)", "pushed notes (159)", "density (159)", "sequence legs (148)",
             "key word on a chord tone (134)", "register (133)", "summit once (165)", "monotony (166)", "leaps: tritone or past an octave",
             "returns related (181)", "chords completable (192)"]
CONSTRUCTED = {"summit once (165)": "summit", "monotony (166)": "monotony", "leaps: tritone or past an octave": "leaps",
               "register (133)": "caps", "returns related (181)": "returns"}
def audit(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]; f = set()
    pb = pitch_bits(ps); rb = rhythm_bits(notes)
    if not (PBAND["p05"] <= pb <= PBAND["p95"]): f.add("pitch band (153/182)")
    if not (RBAND["p05"] <= rb <= RBAND["p95"]): f.add("rhythm band (163)")
    if pushed_share(notes) > 0.42: f.add("pushed notes (159)")
    de = density(notes)
    if not (1.1 <= de <= 4.9): f.add("density (159)")
    if any(l >= 3 for l in sequences(notes)): f.add("sequence legs (148)")
    if keyword_chord(notes)[0] < 0.40: f.add("key word on a chord tone (134)")
    if register_bad(notes): f.add("register (133)")
    if ps.count(max(ps)) != 1 or max(ps) != SUMMIT: f.add("summit once (165)")
    w, dct = monotony(notes)
    if w > 3 or dct < 3: f.add("monotony (166)")
    mx, tri = leaps(notes)
    if mx > 12 or tri: f.add("leaps: tritone or past an octave")
    if not all(r[1] for r in returns_related(c) if (r[0][0], r[0][1]) != ("Last Chorus", 7)): f.add("returns related (181)")
    if chords_completable(notes): f.add("chords completable (192)")
    return f, dict(pitch_bits=pb, rhythm_bits=rb, density=de)

def evaluate(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    if min(ps) < LO or max(ps) > SUMMIT: return ("range", (min(ps), max(ps))), None
    mx, tri = leaps(notes)
    if mx > 12 or tri: return ("leaps: tritone or past an octave", (mx, tri)), None
    w, dct = monotony(notes)
    if w > 3 or dct < 3: return ("monotony (166)", (w, dct)), None
    if ps.count(SUMMIT) != 1: return ("summit once (165)", ps.count(SUMMIT)), None
    if register_bad(notes): return ("register (133)", register_bad(notes)), None
    rr = returns_related(c)
    bad = [r for r in rr if not r[1] and (r[0][0], r[0][1]) != ("Last Chorus", 7)]
    if bad and ON["returns"]: return ("returns related (181)", bad[0][0]), None
    pb = pitch_bits(ps)
    if pb < PBAND["p05"]: return ("pitch band (153/182): under the 5th percentile", round(pb, 3)), None
    if pb > PBAND["p95"]: return ("pitch band (153/182): over the 95th percentile", round(pb, 3)), None
    rb = rhythm_bits(notes)
    if not (RBAND["p05"] <= rb <= RBAND["p95"]): return ("rhythm band (163)", round(rb, 3)), None
    pu = pushed_share(notes)
    if pu > 0.42: return ("pushed notes (159)", round(pu, 3)), None
    de = density(notes)
    if not (1.1 <= de <= 4.9): return ("density (159)", round(de, 2)), None
    legs = sequences(notes)
    if any(l >= 3 for l in legs): return ("sequence legs (148)", legs), None
    kw, _ = keyword_chord(notes)
    if kw < 0.40: return ("key word on a chord tone (134)", round(kw, 3)), None
    if chords_completable(notes): return ("chords completable (192)", chords_completable(notes)), None
    # Table B on the pop calibration: verse 1 and chorus 1, read in E-flat
    V = sec_notes(notes, "Verse 1"); H = sec_notes(notes, "Chorus 1")
    off = V[0]["on"]; qv = quarters(V, off); qh = quarters(H, off); tune = qv + qh
    beta = beta_pitch(tune)
    if beta is None or not (C["beta"]["p05"] <= beta <= C["beta"]["p95"]): return ("spectral (Table B)", beta and round(beta, 3)), None
    cmp_, _ = cmp_score(tune, 4, TONIC)
    if cmp_ < C["cmp"]["p05"]: return ("cmp (Table B)", round(cmp_, 3)), None
    hq = quarters(H, H[0]["on"]); vq = quarters(V, V[0]["on"])
    mh, _, _ = m_horizon(hq, vq)
    if mh < C["mh"]["p05"]: return ("memory (Table B)", round(mh, 3)), None
    bits = PPMM.bits(PPM.symbols(tune, TONIC))[len(V):]
    hp = [n["p"] for n in H]
    ic, _ = ic_profile(bits, hp.index(max(hp)))
    if ic < C["ic"]["p05"]: return ("surprisal (Table B)", round(ic, 3)), None
    fv = (feature_vec(hq, TONIC, 4) - MU) / SD
    dist = np.sort(np.sqrt(((ZREF - fv) ** 2).sum(1)))[:10].mean()
    real = sum(1 for x in REAL_KNN if x >= dist) / len(REAL_KNN)
    if real < C["realness"]["p05"]: return ("realness (Table B)", round(real, 3)), None
    S_sp = s_spectral(beta, C["beta"]["p25"], C["beta"]["p75"])
    vps = [n["p"] for n in V]; lift = float(np.median(hp) - np.median(vps))
    fit_items = [contour(hp) in ("arch", "ascending", "wave", "descending"), 1.0 if lift >= 4 else (0.5 if lift >= 2 else 0.0),
                 contour(vps) in ("flat", "wave"), max(vps) <= CAPS["Verse"]]
    fitv = float(np.mean([float(x) for x in fit_items]))
    comp = (0.15 * S_sp + 0.15 * min(1.0, cmp_ / C["cmp"]["p75"]) + 0.10 * min(1, mh) + 0.15 * fitv + 0.15 * ic +
            0.25 * min(1.0, real / C["realness"]["p50"]) + 0.05 * 0.5)
    flag = pb < PBAND["p25"]
    return None, dict(composite=round(comp, 4), pitch_bits=round(pb, 3), flag_p25=flag, rhythm_bits=round(rb, 3), pushed=pu, density=de, legs=legs,
                      keyword_chord=kw, beta=beta, CMP=cmp_, M_horizon=mh, IC=ic, realness=real, fit=fitv, lift=lift)

def readings(c):
    notes = c["notes"]; ps = [n["p"] for n in notes]
    ct, res = chord_tone_share(notes)
    return dict(pitch_bits=pitch_bits(ps), intervals=interval_shares(ps), repetition=repetition(notes), designs=phrase_designs(notes),
                returns=returns_related(c), outer=outer(notes), rhythm_bits=rhythm_bits(notes), pushed=pushed_share(notes), density=density(notes),
                keyword_chord=keyword_chord(notes)[0], chord_tones=ct, nct_resolved=res, legs=sequences(notes), range=(min(ps), max(ps)))

def fingerprint(c): return hashlib.sha1(json.dumps([[n["on"], n["dur"], n["p"]] for n in c["notes"]]).encode()).hexdigest()[:12]

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    SEED = 20261110 + 36
    rng = random.Random(SEED); made, deaths, alive = 0, collections.Counter(), []
    would, spread, ret_fail = collections.Counter(), collections.defaultdict(list), collections.Counter()
    first_built = None
    while made < N:
        c, err = generate(rng); made += 1
        if err: deaths[err] += 1; continue
        if first_built is None: first_built = c
        fails, rd = audit(c)
        for g in fails: would[g] += 1
        for r in returns_related(c):
            if not r[1] and (r[0][0], r[0][1]) != ("Last Chorus", 7): ret_fail[f"{r[0][0]} line {r[0][1] + 1} -> line {r[0][3] + 1} ({r[0][4]} bars)"] += 1
        for k, v in rd.items(): spread[k].append(v)
        iv = interval_shares([n["p"] for n in c["notes"]])
        for k in ("repeat", "step", "larger"): spread["iv_" + k].append(iv[k])
        spread["exact_bars"].append(repetition(c["notes"])["exact"])
        spread["stock8"].append(phrase_designs(c["notes"])["stock8"])
        cert, m = evaluate(c)
        if cert: deaths[cert[0]] += 1; continue
        c["meas"] = m; c["fp"] = fingerprint(c); alive.append(c)
    alive.sort(key=lambda c: (-c["meas"]["composite"], c["fp"]))
    order = hashlib.sha1("".join(c["fp"] for c in alive).encode()).hexdigest()[:12]
    print(f"[{MODE}] built {made}, survivors {len(alive)} ({100 * len(alive) / max(1, made):.1f}%), order frozen {order}")
    for k, v in deaths.most_common(): print(f"   {v:5d}  {k}")
    print("each gate read on every complete build (would fail):")
    for g in NEW_GATES: print(f"   {would[g]:5d}  {g}")
    for k, v in spread.items(): print(f"   {k}: p05 {np.percentile(v, 5):.3f}  median {np.median(v):.3f}  p95 {np.percentile(v, 95):.3f}")
    print("declared returns not related, by place:", dict(ret_fail))
    flagged = sum(1 for c in alive if c["meas"]["flag_p25"])
    print(f"   survivors flagged under p25 (2.76): {flagged}")
    for c in alive[:6]:
        m = c["meas"]
        print(c["fp"], c["meta"]["plans"]["Verse"], c["meta"]["plans"]["Chorus"], c["meta"]["plans"]["Bridge"], f"comp {m['composite']:.3f} pitch {m['pitch_bits']} rhythm {m['rhythm_bits']} real {m['realness']:.2f} kw {m['keyword_chord']:.2f}")
    code = hashlib.sha1(open(__file__, "rb").read() + open(f"{HERE}/lyric.py", "rb").read() + open(f"{HERE}/phrasestress48.py", "rb").read()).hexdigest()[:12]
    rerun = dict(seed=SEED, N=N, mode=MODE, code_sha=code, pythonhashseed=os.environ.get("PYTHONHASHSEED"), python=platform.python_version(), numpy=np.__version__,
                 tables_sha256=hashlib.sha256(open(f"{HERE}/tables/zeneng_v88_tables.json", "rb").read()).hexdigest()[:16],
                 cmd=f"PYTHONHASHSEED={os.environ.get('PYTHONHASHSEED')} python3 melody_p36.py {N} {MODE}")
    print("rerun:", rerun)
    pick = alive[0] if alive else None
    pickle.dump(dict(ret_fail=ret_fail, would=would, spread={k: list(v) for k, v in spread.items()}, alive=alive[:40], deaths=deaths, made=made, survivors=len(alive),
                     order_fp=order, rerun=rerun, pick_readings=readings(pick) if pick else None, first_built=first_built,
                     first_readings=readings(first_built) if first_built else None),
                open(f"{HERE}/melody_{MODE}.pkl", "wb"))
