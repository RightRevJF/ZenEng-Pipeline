"""Swallowed Up -- the riffs, bass and drums, written and frozen before the voice (ZenEng v78, Module 9-M: Death preset, SCENE aim).
Tuning B standard (B1 E2 A2 D3 F#3 B3, low string B1 = MIDI 35, the tonic: 9-M.4). Grid: sixteenths, 16 to a bar.
q = 200 throughout except the Slowdown (q = 100, a true drop in tempo: 9-M.5's SLOWDOWN for Death).
Eight riffs (a long song holds eight and variations: 9-M.4):
  A 'the straps'    2-bar cell, pedal plus accents (F5 E5 C5 | F5 G5 F#5); stated three times, the fourth changed (G F# F C: b2 to 1)
  B 'the lowering'  1-bar cell, sixteenth chug with accents (B5 D5 C5 F5); the fourth bar changed (G5 to F#5: b6 to 5)
  B' 'the edge'     B moved up a semitone (centre C): verse 3's first eight bars (Death: shifting centres)
  C 'swallowed'     2-bar tremolo cell in dyads (B C D | F E); the fourth statement changed (F E C: b2 to 1)
  D 'the bed'       the solo's loop, i-bVII-bVI-V (B A G F#), two bars a chord, a gallop chug
  E 'the taunt'     q = 100, long chords: B | C F (the tritone) | B | G F#; its last bar F C and a beat of silence (the gap)
  F 'the breakdown' q = 100, guitar, bass and kick in unison on low B, silence between strokes; bars 4 and 8 add strokes and a C
  G 'the end'       unison strokes, then one B5 let ring
Feel ladder (9-M.5, Table BY): intro tacet then layers; riff and verses double time with the kick from the guitar's rhythm (Death);
choruses the blast (quadruple); solo double; the slowdown half time; the breakdown quarter time, the cymbal thinning; re-intro
normal to double; last chorus the blast; outro double, then the strokes."""
import pickle, hashlib, json, collections
B1 = 35
TONIC_PC = 11

# ---- the form (fix 139: summed, and the time computed) ----
FORM = [("Intro", 16, 200), ("Riff", 8, 200), ("Verse 1", 16, 200), ("Chorus 1", 8, 200), ("Verse 2", 16, 200), ("Chorus 2", 8, 200),
        ("Verse 3", 16, 200), ("Chorus 3", 8, 200), ("Solo", 16, 200), ("Slowdown", 16, 100), ("Riff 2", 8, 200),
        ("Last Chorus", 8, 200), ("Outro", 8, 200)]
NBARS = sum(b for _, b, _ in FORM)
SECONDS = sum(b * 4 * 60 / q for _, b, q in FORM)
assert NBARS == 152 and round(SECONDS) == 202

# ---- riff cells: per bar, strokes (slot, dur, offset from B1, palm-muted?) ----
PMs = lambda *ss: [(s, 1, 0, True) for s in ss]
A1 = PMs(0, 2) + [(4, 2, 6, False)] + PMs(6, 7) + [(8, 2, 5, False)] + PMs(10) + [(12, 4, 1, False)]
A2 = PMs(0, 2) + [(4, 2, 6, False)] + PMs(6, 7) + [(8, 4, 8, False), (12, 4, 7, False)]
A2T = PMs(0, 2) + [(4, 2, 6, False)] + PMs(6, 7) + [(8, 2, 8, False), (10, 2, 7, False), (12, 2, 6, False), (14, 2, 1, False)]
B_ = [(0, 2, 0, False)] + PMs(2, 3) + [(4, 2, 3, False)] + PMs(6, 8, 9) + [(10, 2, 1, False)] + PMs(12, 13) + [(14, 2, 6, False)]
BT = [(0, 2, 0, False)] + PMs(2, 3, 4, 5, 6, 7) + [(8, 4, 8, False), (12, 4, 7, False)]
def trem(*spans): return [(s, 1, off, False) for a, b, off in spans for s in range(a, b)]
C1 = trem((0, 8, 0), (8, 12, 1), (12, 16, 3))
C2 = trem((0, 8, 6), (8, 16, 5))
C2T = trem((0, 4, 6), (4, 8, 5), (8, 16, 1))
def gallop(off): return [(0, 2, off, False), (2, 1, off, True), (3, 1, off, True), (4, 2, off, False), (6, 1, off, True), (7, 1, off, True),
                         (8, 2, off, False), (10, 1, off, True), (11, 1, off, True), (12, 2, off, False), (14, 1, off, True), (15, 1, off, True)]
E_ = [[(0, 16, 0, False)], [(0, 8, 1, False), (8, 8, 6, False)], [(0, 16, 0, False)], [(0, 8, 8, False), (8, 8, 7, False)]]
E8 = [(0, 8, 6, False), (8, 4, 1, False)]                                   # beats 3-4: a beat of silence before the breakdown
F_ = [(s, 2, 0, False) for s in (0, 3, 6, 10)]
FT = [(s, 2, 0, False) for s in (0, 3, 6, 8, 10, 12)] + [(14, 2, 1, False)]
G_ = [(s, 2, 0, False) for s in (0, 3, 6, 10)]
GEND = [(0, 16, 0, False)]

def riff_bars(sec, n):
    """(riff letter, strokes) for each bar of a section."""
    out = []
    if sec in ("Intro", "Riff 2"):
        for i in range(n):
            st = (i % 8) // 2
            out.append(("A", A1 if i % 2 == 0 else (A2T if st == 3 else A2)))
    elif sec == "Outro":
        out = [("A", A1), ("A", A2), ("A", A1), ("A", A2T), ("G", G_), ("G", G_), ("G", G_), ("G", GEND)]
    elif sec in ("Riff", "Verse 1", "Verse 2"):
        out = [("B", BT if i % 4 == 3 else B_) for i in range(n)]
    elif sec == "Verse 3":
        out = [("B'", [(s, d, o + 1, pm) for s, d, o, pm in (BT if i % 4 == 3 else B_)]) for i in range(8)] + \
              [("B", BT if i % 4 == 3 else B_) for i in range(8)]
    elif "Chorus" in sec:
        out = [("C", C1 if i % 2 == 0 else (C2T if i == n - 1 else C2)) for i in range(n)]
    elif sec == "Solo":
        roots = [0, 0, 10, 10, 8, 8, 7, 7] * 2
        out = [("D", gallop(r)) for r in roots]
    elif sec == "Slowdown":
        out = [("E", E_[i % 4]) for i in range(7)] + [("E", E8)] + [("F", FT if i in (3, 7) else F_) for i in range(8)]
    assert len(out) == n, (sec, len(out))
    return out

# loop chords named for the documents (power chords), per half bar
NAME = {0: "B5", 1: "C5", 3: "D5", 5: "E5", 6: "F5", 7: "F#5", 8: "G5", 10: "A5"}

def voicing(off, pm, sec):
    r = B1 + off
    if pm: return [r]                                         # the palm-muted pedal: a single low note
    if sec and "Chorus" in sec: return [r, r + 7]              # tremolo dyads
    return [r, r + 7, r + 12]                                 # power chord with the octave (9-M.3)

# ---- the bar map ----
BARS = []
for sec, n, q in FORM:
    for i, (letter, strokes) in enumerate(riff_bars(sec, n)):
        BARS.append(dict(sec=sec, i=i, q=q, riff=letter, strokes=strokes))
def bar_start_s(b): return sum(4 * 60 / BARS[k]["q"] for k in range(b))
def slot_s(b, s): return bar_start_s(b) + s * 60 / BARS[b]["q"] / 4
SEC_FIRST = {}
for k, bb in enumerate(BARS): SEC_FIRST.setdefault(bb["sec"], k)

def chord_names(b):
    """one or two power-chord names for bar b (the accented roots that hold a half bar or more)."""
    st = BARS[b]["strokes"]; halves = []
    for h in (0, 8):
        span = [x for x in st if h <= x[0] < h + 8 and not x[3]]
        if not span: halves.append(None); continue
        cnt = collections.Counter()
        for s, d, o, pm in span: cnt[o] += d
        halves.append(NAME.get(cnt.most_common(1)[0][0], "?"))
    if BARS[b]["riff"] == "C":                                 # the tremolo cell: every change of root
        seq = []
        for x in sorted(st):
            n = NAME[x[2]]
            if not seq or seq[-1] != n: seq.append(n)
        return seq
    if BARS[b]["riff"] in ("A", "B", "B'"): return ["C5" if BARS[b]["riff"] == "B'" else "B5"]      # pedal riffs: named by the pedal
    if halves[1] in (None, halves[0]): return [halves[0]]
    if halves[0] is None: return [halves[1]]
    return halves

# ---- guitars, bass ----
def guitar_events():
    ev = []
    for b, bb in enumerate(BARS):
        sec = bb["sec"]
        for s, d, o, pm in bb["strokes"]:
            ev.append(dict(bar=b, slot=s, dur=d, pitches=voicing(o, pm, sec), pm=pm, riff=bb["riff"]))
    return ev

def gtr_plays(b):
    """which rhythm guitars play bar b: the intro's first eight bars are guitar 1 alone."""
    bb = BARS[b]
    if bb["sec"] == "Intro" and bb["i"] < 8: return ["Gtr 1"]
    return ["Gtr 1", "Gtr 2"]

def bass_plays(b):
    bb = BARS[b]
    return not (bb["sec"] == "Intro" and bb["i"] < 8)

# ---- drums (GM: kick 36, snare 38, rim 37, hh 42, ride 51, crash 49, china 52, floor tom 41) ----
def drum_bar(b):
    bb = BARS[b]; sec, i = bb["sec"], bb["i"]; hits = []
    ons = sorted({s for s, d, o, pm in bb["strokes"]})
    def H(s, n, v): hits.append((s, n, v))
    if sec == "Intro":
        if i < 8: return [], dict(feel=None, cymbal=None)
        if i < 12:                                                   # layers: floor tom and china on the accents
            for s, d, o, pm in bb["strokes"]:
                if not pm: H(s, 41, 108); H(s, 52, 96)
            H(0, 36, 112)
            return hits, dict(feel=None, cymbal="china on accents")
        for s in (0, 8): H(s, 36, 114)
        for s in (4, 12): H(s, 38, 116 + (i % 3))
        for s in range(0, 16, 2): H(s, 51, 92)
        if i == 15:
            for s in (12, 13, 14, 15): H(s, 38, 115 + (s % 3) * 2)
        if i == 12: H(0, 49, 104)
        return hits, dict(feel=1, cymbal="ride, eighths")
    if sec in ("Riff", "Verse 1", "Verse 2", "Verse 3", "Solo") or (sec == "Outro" and i < 4) or (sec == "Riff 2" and i >= 4):
        for s in ons: H(s, 36, 112 + (s % 4 == 0) * 6)               # the kick from the guitar's rhythm (Death)
        for s in (0, 4, 8, 12): H(s, 36, 118)
        for s in (2, 6, 10, 14): H(s, 38, 115 + (s // 4) % 3 * 2)     # double time (Table BY)
        for s in (0, 4, 8, 12): H(s, 51 if sec != "Solo" else 51, 96)
        if i == 0 or (sec == "Solo" and i % 2 == 0): H(0, 49, 106)
        return hits, dict(feel=2, cymbal="ride, the beat", kick="from the guitar")
    if sec == "Riff 2":                                             # re-intro, normal time
        for s in (0, 8): H(s, 36, 114)
        for s, d, o, pm in bb["strokes"]:
            if not pm and s not in (0, 8): H(s, 36, 110)
        for s in (4, 12): H(s, 38, 117)
        for s in range(0, 16, 2): H(s, 51, 92)
        if i == 0: H(0, 49, 108)
        return hits, dict(feel=1, cymbal="ride, eighths")
    if "Chorus" in sec:                                             # the blast (quadruple), counted in sixteenths
        for s in range(0, 16, 2): H(s, 36, 108 + (s % 4 == 0) * 4)
        for k, s in enumerate(range(1, 16, 2)): H(s, 38, 125 + (k + i) % 3)          # 125-127, never every stroke at 127
        for s in range(0, 16, 2): H(s, 51, 94)
        if i % 2 == 0: H(0, 49, 110)
        return hits, dict(feel=4, cymbal="ride, eighths; crash every two bars")
    if sec == "Slowdown" and i < 8:                                 # half time over the taunt
        for s, d, o, pm in bb["strokes"]: H(s, 36, 118)
        if i != 7 or True: H(8, 38, 118) if i != 7 else H(8, 38, 120)
        for s in (0, 4, 8, 12):
            if not (i == 7 and s >= 12): H(s, 52, 98)
        if i == 0: H(0, 49, 112)
        return hits, dict(feel=0.5, cymbal="china, the beat")
    if sec == "Slowdown":                                           # the breakdown: unison strokes, the cymbal thinning
        j = i - 8
        for s, d, o, pm in bb["strokes"]: H(s, 36, 122)
        if j % 2 == 1: H(8, 38, 120)                                # quarter time: one snare every two bars
        if j < 2:
            for s, d, o, pm in bb["strokes"]: H(s, 52, 104)
        elif j < 4: H(0, 52, 104)
        elif j < 6: H(0, 49, 100)
        return hits, dict(feel=0.25, cymbal=["china on every stroke", "china on every stroke", "china on the first stroke", "china on the first stroke",
                                             "crash on the first stroke", "crash on the first stroke", "none", "none"][j])
    if sec == "Outro":                                              # the strokes, then the end
        for s, d, o, pm in bb["strokes"]: H(s, 36, 122); H(s, 49 if s == 0 else 52, 104)
        return hits, dict(feel=0.5 if i < 7 else None, cymbal="crash and china on the strokes")
    raise ValueError(sec)

def drum_events():
    ev, feel = [], []
    for b in range(len(BARS)):
        hits, f = drum_bar(b)
        seen = set()
        for s, n, v in hits:
            if (s, n) in seen: continue
            seen.add((s, n)); ev.append(dict(bar=b, slot=s, note=n, vel=v))
        feel.append(f)
    return ev, feel

# ---- 9-M.10(d): the heaviness reading (reported; enters no score) ----
def ratio_cost(ps):
    R = {0: 0, 12: 1.0, 7: 2.585, 19: 2.585, 5: 3.585, 4: 4.32, 3: 4.91}
    if len(ps) == 1: return 0.0
    worst = max(R.get((b - a) % 24 if (b - a) % 24 in R else (b - a) % 12, 5.0) for k, a in enumerate(ps) for b in ps[k + 1:])
    return worst * 1.0 * (1 + max(0, (48 - min(ps)) / 12))              # complexity x gain (high, 1.0) x the low-register penalty

def heaviness(gtr, drums):
    out = collections.OrderedDict()
    for sec, n, q in FORM:
        bs = [k for k, bb in enumerate(BARS) if bb["sec"] == sec]
        secs = sum(4 * 60 / BARS[k]["q"] for k in bs)
        g = [e for e in gtr if e["bar"] in bs]; d = [e for e in drums if e["bar"] in bs]
        onsets = {(e["bar"], e["slot"]) for e in g} | {(e["bar"], e["slot"]) for e in d}
        kick = [e for e in d if e["note"] == 36]; snare = [e for e in d if e["note"] == 38]
        kick_at = {(e["bar"], e["slot"]) for e in kick}
        pm = [e for e in g if e["pm"]]
        uni = [e for e in pm if (e["bar"], e["slot"]) in kick_at and bass_plays(e["bar"])]
        cost = sum(ratio_cost(e["pitches"]) * e["dur"] for e in g) / max(1, sum(e["dur"] for e in g))
        out[sec] = dict(onsets_per_s=round(len(onsets) / secs, 2), kick_per_s=round(len(kick) / secs, 2), snare_per_s=round(len(snare) / secs, 2),
                        pm_unison_share=round(len(uni) / max(1, len(g)), 2), distortion_cost=round(cost, 2))
    return out

if __name__ == "__main__":
    gtr = guitar_events(); drums, feel = drum_events()
    # the terminal modification is where 9-M.4 puts it: every fourth statement
    for sec in ("Verse 1", "Verse 2", "Riff"):
        bs = [bb for bb in BARS if bb["sec"] == sec]
        assert all((bb["strokes"] is BT) == (bb["i"] % 4 == 3) for bb in bs), sec
    # the gap before the breakdown: at least a beat with nothing sounding (9-M.5)
    b8 = SEC_FIRST["Slowdown"] + 7
    assert max(s + d for s, d, o, pm in BARS[b8]["strokes"]) <= 12
    assert not [e for e in drums if e["bar"] == b8 and e["slot"] >= 12]
    # every intro bar sounds (fix 144)
    assert all(BARS[k]["strokes"] for k in range(16))
    frozen = dict(FORM=FORM, BARS=BARS, gtr=gtr, drums=drums, feel=feel, chords=[chord_names(b) for b in range(len(BARS))])
    blob = json.dumps(dict(g=[(e["bar"], e["slot"], e["dur"], e["pitches"]) for e in gtr], d=[(e["bar"], e["slot"], e["note"]) for e in drums]))
    frozen["sha"] = hashlib.sha1(blob.encode()).hexdigest()[:12]
    pickle.dump(frozen, open("/home/claude/p34/riffs_frozen.pkl", "wb"))
    print(f"form {NBARS} bars, {int(SECONDS // 60)}:{round(SECONDS % 60):02d}; riffs {sorted({bb['riff'] for bb in BARS})}; guitar strokes {len(gtr)}, drum hits {len(drums)}; frozen {frozen['sha']}")
    H = heaviness(gtr, drums)
    for k, v in H.items(): print(f"  {k:12s} {v}")
    for b in (0, 16, 24, 40, 104, 120, 128, 136, 151): print(b + 1, BARS[b]["sec"], BARS[b]["riff"], chord_names(b), feel[b])
