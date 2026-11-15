"""Sung to Sleep (song 53): the record. The hymn tune (melody_final.json, D-space) harmonized in four parts by the carol pipeline's beam
search (harmonize53.py), then laid on one timeline in sounding pitch, from which both documents (the organ full score and the choir's hymn
page) are written, so their bars, line breaks and notes agree by construction.

Timeline (twelfths of a quarter; bar n spans (n-1)*36 to n*36):
  bars 1-8    organ introduction, E-flat: the refrain's first line, then its last, over a rocking left hand and a held pedal
  bars 9-24   verses 1-3 (stanzas printed together), pickup on bar 8 beat 3; the organ a fuller form of the choir's harmony
  bars 25-40  refrain, sung after each of verses 1-3; the organ as in the verses
  bars 41-44  organ link to F major (E-flat, G minor 7, C7sus4, C7), the rocking figure going on
  bars 45-60  verse 4 in F: the choir in unison on the tune (men an octave lower); the organ's own accompaniment: its own chords held
              under the tune (not doubling it), suspensions at chord changes, the rocking left hand, the pedal on the new bass (749.8)
  bars 61-76  final refrain in F: four parts and the sopranos' descant; the organ's own accompaniment: held chords with the tune on top,
              the rocking left hand, a tonic pedal under 'Hush now' and a dominant pedal under 'is sleeping, sleeping'
  bars 77-80  organ coda: the refrain's last phrase once more over a tonic pedal, ending on F
The whole-song shape (749.10): verses 1-3 and their refrains in E-flat, the last verse and refrain a step higher in F; the tune's top (E-flat5,
then F5) and the descant's top (A5) both in the final refrain."""
import json, copy, collections
import harmonize53 as HZ, harm68, lyric_p63 as L, gen34 as G
H = "/home/claude/p63"
MELODY = "melody_final_v2.json"                                   # the second edition: the hymn-mode tune (gen34h.py)
M = json.load(open(f"{H}/{MELODY}")); TUNE = M["pick"]["tune"]
BAR = 36
REHARM = ["F#m", "Em7", "Bm7", "A7", "G", "Em7", "C", "A7", "Bm7", "F#7", "Bm", "Em7", "G", "A7", "D", "D"]
def sec_notes(sec):
    out = []
    for ln in TUNE[sec]:
        for j, n in enumerate(ln):
            out.append(dict(n, melisma=bool(j and ln[j - 1]["slur"]), last=(j == len(ln) - 1)))
    return out
VERSE, REFRAIN = sec_notes("verse"), sec_notes("refrain")
def hz_input(notes, chs, pickup_chord="D", final=True):
    out = []; downs = {}
    for k, n in enumerate(notes):
        if n["on"] % BAR == 0: downs[n["line"]] = k
    for k, n in enumerate(notes):
        b = n["on"] // BAR
        bc = chs[b] if b >= 0 else pickup_chord
        out.append(dict(s=n["p"], dur=n["dur"], strong=n["on"] % BAR == 0, bar_chord=bc, phrase_end=downs[n["line"]] == k and n["last"],
                        final=final and k == len(notes) - 1, melisma=n["melisma"], summit=(n["p"] == 74 and n["on"] % BAR == 0),
                        passing_ok=(n["dur"] <= 12 and n["on"] % BAR != 0 and not n["last"])))
    return out
def set_ranges(shift):
    HZ.RANGE = {"A": (55 + shift, 69 + shift), "T": (48 + shift, 66 + shift), "B": (38 + shift, 60 + shift)}
    HZ.MEDIAN_COMPASS = {"A": (58 + shift, 67 + shift), "T": (52 + shift, 62 + shift), "B": (43 + shift, 57 + shift)}
def harmonize(notes, chs, shift, final=True):
    set_ranges(shift)
    cost, path, _, _ = HZ.harmonize(hz_input(notes, chs, final=final), 8)
    for k, n in enumerate(notes):                                     # under the tune's slurred second note the lower voices hold
        if n["melisma"] and k: path[k] = (path[k - 1][0],) + tuple(path[k - 1][1:])
    return path, cost
# section A (E-flat, sounding +1): verse and refrain as one phrase chain
pathA, costA = harmonize(VERSE + REFRAIN, G.VERSE_CH + G.REFRAIN_CH, 0)
pathAV, pathAR = pathA[:len(VERSE)], pathA[len(VERSE):]
# section B (F, sounding +3): ranges lowered three in D-space so they sound where they should
path4, cost4 = harmonize(VERSE, REHARM, -3)                                      # the organ's own harmony under the unison verse 4
pathFR, costFR = harmonize(REFRAIN, G.REFRAIN_CH, -3)
def descant(notes, path, lo=64, hi=78, pin_world=78):
    """above the soprano, in its rhythm and words: a third to a sixth above, chord tones of the four-part chord on strong or long notes;
    one line by least cost (harm68's: holds and contrary motion cheap, parallels ruled out); 'world' pinned a third above (A5 in F)."""
    span = [dict(on=n["on"], dur=n["dur"], midi=n["p"], stress=n["on"] % BAR == 0, sec="refrain", line=n["line"]) for n in notes]
    chords = [HZ.CHORDS[c][1] for c, *_ in path]
    def tones_at(t):
        k = next(i for i, n in enumerate(notes) if n["on"] == t)
        if notes[k]["p"] == 74 and notes[k]["on"] % BAR == 0: return {pin_world % 12}          # the pin inside the search, so its neighbours fit it
        return set(chords[k]) - {pin_world % 12}                                             # the summit's pitch class nowhere else: A5 once
    ps = harm68.high(span, tones_at, lo=lo, hi=hi)
    assert all(p == pin_world for p, n in zip(ps, notes) if n["p"] == 74 and n["on"] % BAR == 0)
    return ps
DESC = descant(REFRAIN, pathFR)
SCALE_D = {2, 4, 6, 7, 9, 11, 1}
def passing(notes, path, rate=(0.07, 0.10)):
    """passing notes in the lower voices (the metre atlas: 7% to 10% of a 3/4 hymn's inner-voice notes are shorter than the beat).
    Where a voice moves by a third between two notes of one line and the first is a quarter or a half, its second half takes the scale
    tone between, unless that makes parallel fifths or octaves with any voice into the next chord, crosses a neighbouring voice, or
    lands under a melisma. One voice a note, the alto first, then the tenor, then the bass; quarters (the eighth-note pairs) are kept
    near the hymn rate, halves added after them. Returns per note a list of segments (offset, length, A, T, B)."""
    segs = [[(0, n["dur"], *path[k][1:])] for k, n in enumerate(notes)]
    cands = []
    for k in range(len(notes) - 1):
        n, m = notes[k], notes[k + 1]
        if n["line"] != m["line"] or n["dur"] not in (12, 24) or n.get("slur") or m.get("melisma") and False: continue
        if notes[k]["melisma"] or n["slur"]: continue
        (c0, A0, T0, B0), (c1, A1, T1, B1) = path[k], path[k + 1]
        for vi, (x0, x1) in enumerate(((A0, A1), (T0, T1), (B0, B1))):
            if abs(x1 - x0) not in (3, 4): continue
            if vi == 2 and n["dur"] == 12: continue                         # the bass passes only on longer notes (hymn basses: 5% short notes)
            mid = [q for q in range(min(x0, x1) + 1, max(x0, x1)) if q % 12 in SCALE_D]
            if len(mid) != 1: continue
            q = mid[0]; v0 = [n["p"], A0, T0, B0]; v1 = [m["p"], A1, T1, B1]; vm = list(v0); vm[vi + 1] = q
            ok = all(vm[i] >= vm[i + 1] for i in range(3))
            for i in range(4):
                for j in range(i + 1, 4):
                    if (i == vi + 1 or j == vi + 1):
                        im, i1 = abs(vm[i] - vm[j]) % 12, abs(v1[i] - v1[j]) % 12
                        if im == i1 and im in (0, 7) and vm[i] != v1[i] and vm[j] != v1[j]: ok = False
            if ok: cands.append((k, vi, q, n["dur"])); break
    short_total = sum(1 for k, n in enumerate(notes) for _ in range(3))
    want = int(round(rate[1] * short_total / 2))                            # each pair of eighths adds two short notes to one voice
    quarters = [c for c in cands if c[3] == 12][:want]; halves = [c for c in cands if c[3] == 24]
    for k, vi, q, d in quarters + halves:
        A, T, B = segs[k][0][2:]; v = [A, T, B]; v2 = list(v); v2[vi] = q
        segs[k] = [(0, d // 2, *v), (d // 2, d // 2, *v2)]
    return segs
SEG_AV, SEG_AR, SEG_FR = passing(VERSE, pathAV), passing(REFRAIN, pathAR), passing(REFRAIN, pathFR)
# ---- the timeline, sounding pitch ----
OFF = {"A_verse": 288, "A_refrain": 864, "B_verse": 1584, "B_refrain": 2160}
L0 = 40 * BAR; CODA = 76 * BAR; END = 80 * BAR
V = collections.defaultdict(list)                     # voice -> events dict(on, dur, p (int, or a list for a chord), ...)
def put(voice, on, dur, p, **kw): V[voice].append(dict(on=on, dur=dur, p=p, **kw))
def pcs(ch): return HZ.CHORDS[ch][1]
def tones_in(ch, lo, hi): return [q for q in range(lo, hi + 1) if q % 12 in pcs(ch)]
def chord_at(notes, path, t):
    """the four-part chord sounding at time t (the last note at or before t)"""
    k = max(i for i, n in enumerate(notes) if n["on"] <= t); return path[k]
def rocking(ch, on, dur, shift, lo=45, hi=59):
    """the left hand's cradle figure: eighths over each bar, root, fifth, third, fifth, third, fifth, inside a fifth (D-space register A2-B3)"""
    root = next(q for q in range(lo, lo + 12) if q % 12 == pcs(ch)[0]); fifth = next(q for q in range(root + 1, root + 12) if q % 12 == pcs(ch)[2])
    third = next(q for q in range(root + 1, root + 12) if q % 12 == pcs(ch)[1])                       # closed: the hand stays within a fifth
    pat = [root, fifth, third, fifth, third, fifth]
    return [(on + 6 * i, 6, pat[i % 6] + shift) for i in range(dur // 6)]
def fill_between(ch, lo, hi):
    c = [q for q in tones_in(ch, lo + 3, hi - 3)]; return c[len(c) // 2] if c else None

# ---- the organ, third edition (749.14): a plan by section, measured against the Lieder accompaniment tables (organ_readings53.py) ----
#   introduction  the tune in the right hand over an inner line that moves when the tune holds; the rocking left hand; the pedal
#   verses 1-3    hymnal harmony (the right hand doubles sopranos and altos); the left hand a broken chord in quarters, the tenor on
#                 every chord change; the pedal the bass; colour varied verse by verse by registration (printed in the score)
#   refrain       the tune on top, an inner line moving under its held notes, the rocking left hand
#   link          broken eighths in the right hand, held chords in the left, the pedal stepping down E-flat, D, C
#   verse 4       free harmony under the unison tune: chords below the tune that move when the tune holds, suspensions at changes,
#                 held chords in the left hand, a pedal that steps into each new bass
#   final refrain the tune on top, the inner line, the rocking left hand, tonic and dominant pedals
SCALE_PCS = SCALE_D
def idx_at(notes, t):
    return max(i for i, n in enumerate(notes) if n["on"] <= t)
def parallel(a0, a1, b0, b1):
    i0, i1 = abs(a0 - b0) % 12, abs(a1 - b1) % 12
    return i0 == i1 and i0 in (0, 7) and a0 != a1 and b0 != b1
def moved(ch, voicing, ceiling):
    """the inner line: the voicing's top note to the nearest other chord tone, up while it stays two semitones under the tune, else down
    (above the next note of the voicing); None if there is no room"""
    v = sorted(voicing); top = v[-1]; below = v[-2] if len(v) > 1 else top - 8
    ups = tones_in(ch, top + 1, ceiling - 2); downs = tones_in(ch, below + 2, top - 1)
    if ups: return v[:-1] + [ups[0]]
    if downs: return v[:-1] + [downs[-1]]
    if len(v) == 2:                                                   # two notes and no room for the top: the lower note moves
        alt = [q for q in tones_in(ch, v[0] - 5, top - 2) if q != v[0]]
        if alt: return sorted([min(alt, key=lambda q: abs(q - v[0])), top])
    if len(v) >= 3:                                                   # no room for the top: the next voice down moves instead
        lo2 = v[-3] if len(v) > 3 else v[0] - 8
        alt = [q for q in tones_in(ch, lo2 + 1, top - 1) if q != below and q not in v]
        if alt: return sorted(v[:-2] + [min(alt, key=lambda q: abs(q - below)), top])
    return None
def tune_layer(notes, off, shift, last_end=None):
    for k, n in enumerate(notes):
        d = (last_end - (n["on"] + off)) if (last_end and k == len(notes) - 1) else n["dur"]
        put("org_rh", n["on"] + off, d, n["p"] + shift)
def inner_layer(notes, path, segl, off, shift, last_end=None, fill=True, eighths=False):
    """the alto (with its passing notes) and a filling chord tone under the tune; on each beat of a held tune note after its first the
    top of the inner chord moves to a neighbouring chord tone and back (no parallel fifths or octaves with the bass into the next chord)"""
    for k, n in enumerate(notes):
        ch = path[k][0]; s = n["p"]; t = n["on"] + off; nd = n["dur"]
        if last_end and k == len(notes) - 1: nd = last_end - t
        for si, (o, d, A, T, B) in enumerate(segl[k]):
            if last_end and k == len(notes) - 1 and si == len(segl[k]) - 1: d = nd - o
            f = fill_between(ch, A, s) if fill else None
            if fill and f is None: f = next((q for q in reversed(tones_in(ch, max(A - 8, 52), A - 3))), None)     # no room above the alto: a chord tone under it
            base = sorted({A} | ({f} if f else set()))
            pieces = [(o, d)]
            if d >= 24 and (n["on"] + o) % 12 == 0:
                pieces = [(o + 12 * j, 12) for j in range(d // 12)]
                if d % 12: pieces[-1] = (pieces[-1][0], pieces[-1][1] + d % 12)
            nxt = path[k + 1] if k + 1 < len(path) else None
            for j, (po, pd) in enumerate(pieces):
                m = moved(ch, base, s) if j else None
                if m and eighths and pd >= 12:                                  # the fuller form: a neighbour figure in eighths on each held beat
                    put("org_rh_in", t + po, 6, [q + shift for q in m]); put("org_rh_in", t + po + 6, pd - 6, [q + shift for q in base]); continue
                v = base
                if j % 2 == 1 and m and not (j == len(pieces) - 1 and nxt and parallel(max(m), max(nxt[1], fill_between(nxt[0], nxt[1], notes[k + 1]["p"]) or 0), B, nxt[3])):
                    v = m
                put("org_rh_in", t + po, pd, [q + shift for q in v])
def rocking_beats(notes, path, off, shift, t0, t1, lo=45):
    """the left hand's cradle figure, beat by beat from the chord sounding: root and fifth on the downbeat, third and fifth after,
    closed inside a fifth"""
    for t in range(t0, t1, 12):
        ch = path[idx_at(notes, t)][0]; P = pcs(ch)
        root = next(q for q in range(lo, lo + 12) if q % 12 == P[0])
        fifth = next(q for q in range(root + 1, root + 12) if q % 12 == P[2]); third = next(q for q in range(root + 1, root + 12) if q % 12 == P[1])
        a = root if t % BAR == 0 else third
        put("org_lh", t + off, 6, a + shift); put("org_lh", t + off + 6, 6, fifth + shift)
def lh_broken(notes, path, off, shift, t0, t1):
    """verses 1-3: a broken chord in quarters, the tenor's note on each downbeat and chord change, other chord tones between the bass and
    the alto on the other beats, never repeating, a leap of a third or more preferred, no parallels with the bass into a change"""
    prev = None
    for t in range(t0, t1, 12):
        k = idx_at(notes, t); ch, A, T, B = path[k]
        change = t % BAR == 0 or prev is None or (notes[k]["on"] == t and path[k - 1][0] != ch)
        if change: q = T
        else:
            c = [x for x in tones_in(ch, max(B + 3, 47), min(A - 3, 64)) if x != prev]
            if t + 12 < t1:
                k2 = idx_at(notes, t + 12); c2, A2, T2, B2 = path[k2]
                if (t + 12) % BAR == 0 or (notes[k2]["on"] == t + 12 and c2 != ch):
                    c = [x for x in c if not parallel(x, T2, B, B2) and abs(x - T2) <= 7]
            c.sort(key=lambda x: (abs(x - prev) < 3, abs(x - prev)))
            q = c[0] if c else T
        put("org_lh", t + off, 12, q + shift); prev = q
# introduction (E-flat; D-space +1): the refrain's line 1 at bars 1-4 ('small' cut to a half), then its line 4 from the pickup on bar 4 beat 3
intro = []
for k, n in enumerate(REFRAIN):
    if n["line"] == 0: intro.append((n["on"], 24 if k == max(j for j, m in enumerate(REFRAIN) if m["line"] == 0) else n["dur"], k))
    if n["line"] == 3: intro.append((n["on"] - 420 + 132, n["dur"], k))
INTRO_N = [dict(on=on, dur=d, p=REFRAIN[k]["p"]) for on, d, k in intro]
INTRO_P = [pathAR[k] for on, d, k in intro]
INTRO_S = [[(0, d, *pathAR[k][1:])] for on, d, k in intro]
tune_layer(INTRO_N, 0, 1); inner_layer(INTRO_N, INTRO_P, INTRO_S, 0, 1, fill=False)
for bar in range(8):
    t = bar * BAR; ks = [k for on, d, k in intro if on <= t]; k = ks[-1] if ks else intro[0][2]
    ch, A, T, B = pathAR[k]; dur = 24 if bar == 7 else 36
    for on, d, p in rocking(ch, t, dur, 1): put("org_lh", on, d, p)
    put("org_ped", t, dur, (B + 1 - 5) if bar == 7 and (B + 1) % 12 == 3 else B + 1)      # the last bar over B-flat (no octaves with the tune into the verse's pickup)
# section A (E-flat): the choir with its passing notes
for notes, path, segl, off, part in ((VERSE, pathAV, SEG_AV, OFF["A_verse"], "verse"), (REFRAIN, pathAR, SEG_AR, OFF["A_refrain"], "refrain")):
    for k, n in enumerate(notes):
        ch = path[k][0]; t = n["on"] + off; s = n["p"]
        put("S", t, n["dur"], s + 1, syl=n["syl"], line=n["line"], part=part, slur=n["slur"], melisma=n["melisma"], chord=ch)
        for vi, vn in enumerate(("A", "T", "B")):                     # a voice without the passing note keeps one note
            last = None
            for o, d, *abt in segl[k]:
                if last is not None and last["p"] == abt[vi] + 1: last["dur"] += d
                else: put(vn, t + o, d, abt[vi] + 1); last = V[vn][-1]
        for o, d, A, T, B in segl[k]: put("org_ped", t + o, d, B + 1)
# verses 1-3 (fourth edition): the tune on top and an inner line under it (the altos with their passing notes and a filling chord
# tone, moving to a neighbouring chord tone on the held beats), so the harmony stays the hymnal one; the left hand broken
tune_layer(VERSE, OFF["A_verse"], 1); inner_layer(VERSE, pathAV, SEG_AV, OFF["A_verse"], 1)
lh_broken(VERSE, pathAV, OFF["A_verse"], 1, VERSE[0]["on"], VERSE[-1]["on"] + VERSE[-1]["dur"])
# refrain: the tune on top, the inner line, the rocking left hand
tune_layer(REFRAIN, OFF["A_refrain"], 1); inner_layer(REFRAIN, pathAR, SEG_AR, OFF["A_refrain"], 1)
rocking_beats(REFRAIN, pathAR, OFF["A_refrain"], 1, 0, REFRAIN[-1]["on"] + REFRAIN[-1]["dur"])
# link (sounding pitch, F's signature from bar 41): E-flat, G minor 7 over D, C7sus4, C7
LINK = [("Eb", [67, 70, 75], 39, [51, 58, 55]), ("Gm7", [65, 70, 74], 38, [55, 62, 58]), ("C7sus4", [65, 70, 72], 36, [48, 55, 53]), ("C7", [64, 70, 72], 36, [48, 55, 52])]
for i, (nm_, rh, ped, lh) in enumerate(LINK):
    t = L0 + i * BAR; dur = 24 if i == 3 else 36
    pat = [rh[0], rh[1], rh[2], rh[1], rh[2], rh[1]]
    for j in range(dur // 6): put("org_rh", t + 6 * j, 6, pat[j % 6])
    put("org_lh", t, dur, sorted(lh)); put("org_ped", t, dur, ped)
# verse 4 (F; D-space +3): the choir in unison; the organ's free harmony
import itertools
def voicings(ch, lo, hi):
    """four-note chords of ch inside [lo, hi], every pitch class present, spanning at most a tenth"""
    P = set(pcs(ch)); tones = tones_in(ch, lo, hi)
    for gap, span in ((3, 16), (2, 19), (1, 24)):
        out = [list(c) for c in itertools.combinations(tones, 4) if {q % 12 for q in c} >= P and c[-1] - c[0] <= span and all(c[i + 1] - c[i] >= gap for i in range(3))]
        if out: return out
    return [list(c) for c in itertools.combinations(tones, 3) if {q % 12 for q in c} >= set(pcs(ch)[:3])]
def nearest(cands, prev):
    if prev is None: return min(cands, key=lambda c: abs(c[-1] - 69))
    return min(cands, key=lambda c: (sum(abs(x - y) for x, y in zip(c, prev)), abs(c[-1] - prev[-1])))
end4 = OFF["B_refrain"] - OFF["B_verse"]
PED4 = {}
# the pedal under verse 4 (written first, the bass before the hands): the bass on each downbeat and change; on the beat before a change, a scale step into the new bass
for t in range(VERSE[0]["on"], end4, 12):
    k = idx_at(VERSE, t); B = path4[k][3]; q = B
    if t + 12 < end4:
        k2 = idx_at(VERSE, t + 12); B2 = path4[k2][3]
        change_next = (VERSE[k2]["on"] == t + 12 and path4[k2][0] != path4[k][0])
        this_change = t % BAR == 0 or (VERSE[k]["on"] == t and (k == 0 or path4[k - 1][0] != path4[k][0]))
        if change_next and not this_change and B2 != B:
            mel = VERSE[k]["p"]
            for a in ((B2 + 2, B2 + 1) if B2 < B else (B2 - 2, B2 - 1)):
                if a % 12 in SCALE_PCS and (mel - a) % 12 not in (1, 6, 11) and a != B and all((a - x) % 12 not in (1, 11) for x in pcs(path4[k][0])):
                    q = a; break
    PED4[t] = q; put("org_ped", t + OFF["B_verse"], 12, q + 3)
prev_v = None; alt = 0; last_top = None
for t in range(VERSE[0]["on"], end4, 12):
    k = idx_at(VERSE, t); ch = path4[k][0]
    change = prev_v is None or (VERSE[k]["on"] == t and (k == 0 or path4[k - 1][0] != ch))
    tu0, tu1 = VERSE[idx_at(VERSE, max(t - 12, VERSE[0]["on"]))]["p"], VERSE[k]["p"]
    tus = [tu1] + [n["p"] for n in VERSE if t < n["on"] < t + 12]                                       # the tune at the beat and on its half
    okp = lambda top: last_top is None or not (parallel(last_top, top, PED4.get(t - 12, PED4[t]), PED4[t]) or any(parallel(last_top, top, tu0, x) for x in tus))   # no parallel fifths or octaves with the pedal or the tune
    if change:
        tune_now = VERSE[k]["p"]; hi_v = min(72, tune_now - 1)                                   # the sung tune stays on top (top-voice salience)
        cands = sorted(voicings(ch, 52, hi_v) or voicings(ch, 48, hi_v), key=lambda c: (sum(abs(x - y) for x, y in zip(c, prev_v)), abs(c[-1] - prev_v[-1])) if prev_v else abs(c[-1] - 69))
        base = next((c for c in cands if okp(c[-1])), cands[0])
        sus = prev_v is not None and prev_v[-1] % 12 not in pcs(ch) and 0 < prev_v[-1] - base[-1] <= 2      # the old top held over the change, resolving down by step
        v = base[:-1] + [prev_v[-1]] if sus else base; alt = -1 if sus else 0                 # after a suspension the next beat resolves it
        put("org_rh", t + OFF["B_verse"], 12, [q + 3 for q in v], **({"sus": True} if sus else {}))
        cur = base
    else:
        alt += 1; m = moved(ch, cur, VERSE[k]["p"] + 1) if alt % 2 == 1 else None
        if m and not okp(m[-1]): m = None
        v = m or cur
        if t == end4 - 12 and parallel(v[-1], REFRAIN[0]["p"], PED4[t], 62 - 24): v = cur if m else (moved(ch, cur, 77) or cur)   # into the final refrain: no octaves with its tonic pedal
        if v[-1] >= VERSE[k]["p"]: v = cur if cur[-1] < VERSE[k]["p"] else v
        if not okp(v[-1]) or (t == end4 - 12 and parallel(v[-1], REFRAIN[0]["p"], PED4[t], 62 - 24)):
            alts = [c for c in voicings(ch, 52, min(72, VERSE[k]["p"] - 1)) if okp(c[-1]) and not (t == end4 - 12 and parallel(c[-1], REFRAIN[0]["p"], PED4[t], 62 - 24))]
            if alts: v = min(alts, key=lambda c: sum(abs(x - y) for x, y in zip(c, cur)))
        put("org_rh", t + OFF["B_verse"], 12, [q + 3 for q in v])
    prev_v = cur; last_top = v[-1]
# the left hand under verse 4: chord tones in quarters in the tenor's octave, the nearest on each change, a different one on the other beats
prev = None
for t in range(VERSE[0]["on"], end4, 12):
    k = idx_at(VERSE, t); ch = path4[k][0]; ped = path4[k][3]
    c = [q for q in tones_in(ch, 45, 56) if q != ped and q != prev]
    if prev is None: q = c[len(c) // 2]
    else:
        c.sort(key=lambda x: (abs(x - prev) < 3, abs(x - prev))); q = c[0]
    put("org_lh", t + OFF["B_verse"], 12, q + 3); prev = q
for k, n in enumerate(VERSE):
    ch, A, T, B = path4[k]; t = n["on"] + OFF["B_verse"]; m = n["p"] + 3
    put("S", t, n["dur"], m, syl=n["syl"], line=n["line"], part="verse4", slur=n["slur"], melisma=n["melisma"], chord=ch)
    put("A", t, n["dur"], m); put("T", t, n["dur"], m - 12); put("B", t, n["dur"], m - 12)
# final refrain (F): four parts and the descant; the organ: the tune on top, the inner line, the rocking left hand, pedal points
for k, n in enumerate(REFRAIN):
    ch, A, T, B = pathFR[k]; t = n["on"] + OFF["B_refrain"]; d = n["dur"]
    if k == len(REFRAIN) - 1: d = CODA - t
    put("S", t, d, n["p"] + 3, syl=n["syl"], line=n["line"], part="refrain_final", slur=n["slur"], melisma=n["melisma"], chord=ch)
    for vi, vn in enumerate(("A", "T", "B")):
        last = None
        for o, dd, *abt in SEG_FR[k]:
            dd = d - o if (k == len(REFRAIN) - 1 and o + dd >= n["dur"]) else dd
            if last is not None and last["p"] == abt[vi] + 3: last["dur"] += dd
            else: put(vn, t + o, dd, abt[vi] + 3); last = V[vn][-1]
    put("Desc", t, d, DESC[k] + 3, syl=n["syl"], line=n["line"], slur=n["slur"], melisma=n["melisma"])
tune_layer(REFRAIN, OFF["B_refrain"], 3, last_end=CODA); inner_layer(REFRAIN, pathFR, SEG_FR, OFF["B_refrain"], 3, last_end=CODA, eighths=True)
rocking_beats(REFRAIN, pathFR, OFF["B_refrain"], 3, 0, 16 * BAR, lo=42)
PED_TONIC, PED_DOM = (0, 4), (12, 14)                                             # bars of the final refrain: under 'Hush now', under 'is sleeping, sleeping'
pb = []
for k, n in enumerate(REFRAIN):
    b = n["on"] // BAR
    if PED_TONIC[0] <= b < PED_TONIC[1] or PED_DOM[0] <= b < PED_DOM[1]: continue
    d = n["dur"] if k < len(REFRAIN) - 1 else CODA - (n["on"] + OFF["B_refrain"])
    pb.append((n["on"] + OFF["B_refrain"], d, pathFR[k][3] + 3))
pb.append((OFF["B_refrain"], 4 * BAR, 62 - 24 + 3)); pb.append((OFF["B_refrain"] + 12 * BAR, 2 * BAR, 69 - 24 + 3))
for on, d, p in sorted(pb): put("org_ped", on, d, p)
# coda (sounding, F): the refrain's last phrase once more over a tonic pedal; IV to I
l4 = [n for n in REFRAIN if n["line"] == 3]
mot = [(n["on"] - l4[1]["on"], n["dur"], n["p"] + 3) for n in l4[1:-1]]            # 'sleep-ing, sleep-ing' without its pickup and 'here'
for o, d, p in mot:
    under = [58, 62] if o < 36 else [55, 60]
    put("org_rh", CODA + o, d, sorted(set(under + [p])))
put("org_rh", CODA + 2 * BAR, 2 * BAR, [57, 60, 65]); put("org_ped", CODA, 4 * BAR, 41)
for on, d, p in rocking("G", CODA, 36, 3, lo=42, hi=56) + rocking("D", CODA + BAR, 36, 3, lo=42, hi=56): put("org_lh", on, d, p)
put("org_lh", CODA + 2 * BAR, 2 * BAR, [53, 60])
for v in V.values(): v.sort(key=lambda e: (e["on"], -e["dur"]))
def merge_holds(ev):
    """a repeated note or chord joins the one before it (organists hold common tones; a lower voice under a melisma holds)"""
    out = []
    for e in ev:
        if out and out[-1]["p"] == e["p"] and out[-1]["on"] + out[-1]["dur"] == e["on"] and (e.get("hold_ok") or e.get("organ")): out[-1]["dur"] += e["dur"]
        else: out.append(dict(e))
    return out
S_on = {e["on"]: e for e in V["S"]}
for voice in ("A", "T", "B"):
    for e in V[voice]:
        s = S_on.get(e["on"]); e["hold_ok"] = bool(s and s.get("melisma"))
    V[voice] = merge_holds(V[voice])
for voice in ("org_rh", "org_rh_in", "org_lh", "org_ped"):
    for e in V[voice]: e["organ"] = True
    V[voice] = merge_holds(V[voice])
    for a, b in zip(V[voice], V[voice][1:]):                                       # the organ legato: a beat's gap closed by the note before
        if 0 < b["on"] - (a["on"] + a["dur"]) <= 12: a["dur"] = b["on"] - a["on"]
# low intervals (psychoacoustics): a left-hand note that makes a close interval with the pedal or another left-hand note below the
# arranger's low-interval limit goes up an octave (the roughness model ranks these; the limits are a rule of thumb)
LOW_LIMIT = {1: 52, 2: 51, 3: 48, 4: 46, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}
def _sound(voice, t): return [q for e in V[voice] if e["on"] <= t < e["on"] + e["dur"] for q in (e["p"] if isinstance(e["p"], list) else [e["p"]])]
for e in V["org_lh"]:
    for _ in range(2):
        ps_ = e["p"] if isinstance(e["p"], list) else [e["p"]]
        below = _sound("org_ped", e["on"]) + [q for q in _sound("org_lh", e["on"]) if q not in ps_]
        allp = sorted(set(below + ps_)); bad = [x for a, b in zip(allp, allp[1:]) if 0 < b - a < 12 and a < LOW_LIMIT[b - a] for x in (a, b) if x in ps_]
        if not bad: break
        new = [q + 12 if q in bad and q + 12 <= 65 else q for q in ps_]
        e["p"] = sorted(set(new)) if isinstance(e["p"], list) else new[0]
# breaths (749.19, 749.20): a beat's breath before the third line of every verse and refrain (after the half-stanza), sung by every
# part and taken by the organ's hands where their note ends there; held pedal points and notes running through are left
BREATH_REL = 276
BREATHS = [OFF[k] + BREATH_REL for k in ("A_verse", "A_refrain", "B_verse", "B_refrain")]
for voice in ("S", "A", "T", "B", "Desc", "org_rh", "org_rh_in", "org_lh", "org_ped"):
    for e in V.get(voice, []):
        if e["on"] + e["dur"] in BREATHS and e["dur"] > 12 and e["on"] < e["on"] + e["dur"] - 12: e["dur"] -= 12; e["breath"] = True
REC = dict(title=L.TITLE, voices={k: v for k, v in V.items()}, offsets=OFF, end=END, bars=80, pickup=0, keys=[(0, "E-flat major"), (L0, "F major")], link_bar=41, coda_bar=77,
           paths=dict(A=pathA, verse4=path4, final_refrain=pathFR), costs=dict(A=costA, verse4=cost4, final_refrain=costFR), descant_dspace=DESC,
           reharm=REHARM, verse_chords=G.VERSE_CH, refrain_chords=G.REFRAIN_CH, fp=M["pick"]["fp"], qpm=92, breaths=BREATHS)
json.dump(REC, open(f"{H}/song_record.json", "w"))
if __name__ == "__main__":
    print({k: len(v) for k, v in V.items()}, "costs", {k: round(v, 1) for k, v in REC["costs"].items()})
    N = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']; nm = lambda p: N[p % 12] + str(p // 12 - 1)
    for k, v in V.items():
        ps = [q for e in v for q in (e["p"] if isinstance(e["p"], list) else [e["p"]])]; print(k, nm(min(ps)), nm(max(ps)))
    for k in ("org_rh", "org_rh_in", "org_lh", "org_ped"):
        bad = [(e["on"], e["dur"]) for e in V[k] if e["dur"] <= 0]; print(k, "no-length", bad[:3])
