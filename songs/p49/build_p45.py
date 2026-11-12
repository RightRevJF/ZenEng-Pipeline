"""Before It's Done (song 45): the song record from melody_final.pkl (the pick of record) -- a fingerpicked ballad, q = 72, 4/4; G major,
the last chorus and the tag lifted a whole step to A (Q6 A); 56 bars, about 3:07 (Q7 A).
  voice   a man's middle voice, every line; the last chorus and the tag a whole step up (the search ran in G; the lift is in the record).
  guitar  (Q4 B; Q6 note: nothing simplified) steel-string, fingerpicked, standard tuning, no capo. Every note carries its string and fret,
          so the score's TAB is the record's. Open-string voicings that keep the top two strings ringing on D and G through the G-major
          sections (G, D/F#, Em7, Cadd9, Am7, Dsus4-D); the chorus bass walks G-F#-E down to C; 'thought' is held over a G whose sus4 (C)
          resolves to the third (B) under it; every Dsus4 resolves at the half bar. In A: Asus4-A, E/G#, F#m7, Dadd9, the bass walking
          A-G#-F#-D. The intro's last bar and the tag's last bar play 'before it's done' on the top strings (D C B A; then in A, E D C# B,
          arriving on the voice's last note).
          Patterns, eighths: verses bass, 3, 2, 1, alternate bass, 3, 2, 3; choruses the top string pinched with the bass on 1 and string 2
          with the alternate bass on 3; the bridge slower (quarters, let ring), its last two bars strummed, building into the lift; the last
          chorus pinched on 1 and 3, fullest.
  cello   from verse 2: long roots under verse 2; a high line over chorus 2 (whole notes, chord tones led by step); low held roots in the
          bridge, swelling in its last bar; the last chorus a higher line in half notes; the tag low, ending on D (the tag's IV), let ring.
  Verses thinner, the last chorus the fullest (9.12)."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p49", "/home/claude/p40"]
import melody_p45 as P
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p49/melody_final.pkl", "rb")); c = F["pick"]
BAR = 48; NB = P.NBARS; QB = 72; LIFT = P.LIFT
LIFTED = ("Last Chorus", "Tag")
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"civil": ["civ", "il"], "different": ["dif", "fer", "ent"], "saving": ["sav", "ing"], "kitchen": ["kitch", "en"], "number's": ["num", "ber's"],
        "coming": ["com", "ing"], "only": ["on", "ly"], "Somebody": ["Some", "bo", "dy"], "open": ["o", "pen"], "tissue": ["tis", "sue"],
        "doctor": ["doc", "tor"], "sitting": ["sit", "ting"], "speaking": ["speak", "ing"], "doorway": ["door", "way"], "hundred": ["hun", "dred"],
        "other": ["oth", "er"], "families": ["fam", "i", "lies"], "Never": ["Nev", "er"], "brother": ["broth", "er"], "walking": ["walk", "ing"],
        "nowhere": ["no", "where"], "birthday": ["birth", "day"], "Everything's": ["Ev", "ery", "thing's"], "already": ["al", "read", "y"],
        "waiting": ["wait", "ing"], "morning": ["morn", "ing"], "doesn't": ["does", "n't"], "believe": ["be", "lieve"], "anyway": ["an", "y", "way"],
        "before": ["be", "fore"], "saying": ["say", "ing"], "never": ["nev", "er"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",.;:?")
        if n <= 1: out.append((w, False)); continue
        parts = list(HFIX.get(core) or _PY.inserted(core).split("-"))
        tail = w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
UP = {"G": "A", "D": "E", "Em": "F#m", "C": "D", "Am": "Bm", "E": "F#"}
ROMAN_A = {"A": "I", "E": "V", "F#m": "vi", "D": "IV"}
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k; ch = P.CHORD[b]; up = nm in LIFTED
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=UP[ch] if up else ch, roman=ROMAN_A[UP[ch]] if up else M.ROMAN[ch], start=b * BAR, len=BAR, qbpm=QB,
                         key="A major" if up else "G major", search_chord=ch, stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"] + (LIFT if sec in LIFTED else 0), search_midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"],
                     text=t, hyph=hy, stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
lead.sort(key=lambda n: n["on"])

# ---- the guitar: voicings as frets, strings 6 (low E) to 1 (high E); None = not played ----
OPEN = {6: 40, 5: 45, 4: 50, 3: 55, 2: 59, 1: 64}
VOIC = {"G": ([3, 2, 0, 0, 3, 3], 6, 5), "Gsus4": ([3, None, 0, 0, 1, 3], 6, 4), "Gres": ([3, None, 0, 0, 0, 3], 6, 4),
        "D/F#": ([2, 0, 0, 2, 3, 2], 6, 4), "Em7": ([0, 2, 2, 0, 3, 3], 6, 4), "Cadd9": ([None, 3, 2, 0, 3, 3], 5, 4),
        "Am7": ([None, 0, 2, 0, 1, 3], 5, 4), "Dsus4": ([None, 0, 0, 2, 3, 3], 4, 5), "D": ([None, 0, 0, 2, 3, 2], 4, 5), "E": ([0, 2, 2, 1, 0, 0], 6, 5),
        "A": ([None, 0, 2, 2, 2, 0], 5, 4), "Asus4": ([None, 0, 2, 2, 3, 0], 5, 4), "E/G#": ([4, None, 2, 1, 0, 0], 6, 4),
        "F#m7": ([2, None, 2, 2, 0, 0], 6, 4), "Dadd9": ([None, 5, 4, 2, 3, 0], 5, 4), "Esus4": ([0, 2, 2, 2, 0, 0], 6, 5)}
NAME = {"Gsus4": "Gsus4", "Gres": "G", "Asus4": "Asus4", "Esus4": "Esus4"}                                  # shapes and the names written over them
def sf(v, s):
    fr = VOIC[v][0][6 - s]; assert fr is not None, (v, s); return (OPEN[s] + fr, s, fr)
def sung(bi, half):
    """the voice's sounding time by pitch class in half a bar (the notes held into it counted)."""
    a, z = bi * BAR + 24 * half, bi * BAR + 24 * half + 24; out = {}
    for n in lead:
        ov = min(z, n["on"] + n["dur"]) - max(a, n["on"])
        if ov > 0: out[n["midi"] % 12] = out.get(n["midi"] % 12, 0) + ov
    return out
SUS = {"D": (7, 6), "E": (9, 8), "G": (0, 11), "A": (2, 1)}                                     # chord -> (its fourth, its third)
SUSLOG = []
def wants(bi, half, ch, default_sus):
    """the guitar listens to the singer: the sus4 where the voice holds the fourth (an eighth or more, and longer than the third), the
    plain chord where it sings the third; otherwise the arrangement's default."""
    f4, f3 = SUS[ch]; v = sung(bi, half)
    if v.get(f4, 0) >= 6 and v.get(f4, 0) >= v.get(f3, 0): r = True
    elif v.get(f3, 0) >= 3: r = False
    else: r = default_sus
    if r != default_sus and (bi + 1, half, ch, "sus4" if r else "plain") not in SUSLOG: SUSLOG.append((bi + 1, half, ch, "sus4" if r else "plain"))
    return r
def shapes_of(b):
    """the voicing for each eighth of a bar (eight entries)."""
    sec, k, ch, kind = b["sec"], b["k"], b["chord"], b["kind"]; bi = b["start"] // BAR; up = sec in LIFTED
    base = {"G": "G", "Em": "Em7", "C": "Cadd9", "Am": "Am7", "E": "E", "A": "A", "F#m": "F#m7"}
    if kind == "Chorus" and k == 0:                                                         # 'thought' (and 'morning'): the sus4 resolving to the third under it
        tonic = "A" if up else "G"; s4 = wants(bi, 1, tonic, True)
        return [tonic] * 4 + ([tonic + "sus4"] * 3 + [("A" if up else "Gres")] if s4 else [tonic] * 4)
    if ch == "D" and up: return ["Dadd9"] * 8
    if ch == "D":
        plain = "D/F#" if (kind == "Chorus" and k in (1, 5)) else "D"
        d0 = not (kind == "Chorus" and k in (1, 5))                                         # every Dsus4 resolves at the half bar (verses, a chorus's last bar)
        return [("Dsus4" if wants(bi, h, "D", d0 and h == 0) else plain) for h in (0, 1) for _ in range(4)]
    if ch == "E" and up:
        plain = "E/G#" if k in (1, 5) else "E"
        return [("Esus4" if wants(bi, h, "E", False) else plain) for h in (0, 1) for _ in range(4)]
    return [base[ch]] * 8
PAT = {"verse": [["B"], [3], [2], [1], ["A"], [3], [2], [3]],
       "chorus": [["B", 1], [3], [2], [3], ["A", 2], [3], [1], [2]],
       "last": [["B", 1], [3], [2], [3], ["A", 1], [3], [2], [3]],
       "bridge": [["B"], [], [3], [], [2], [], [1], []]}
VEL = {"Intro": 54, "Verse 1": 52, "Chorus 1": 66, "Verse 2": 56, "Chorus 2": 70, "Bridge": 50, "Last Chorus": 80, "Tag": 50}
gtr = []
def gev(on, dur, notes, vel, art="", voice="up"):
    gtr.append(dict(on=on, dur=dur, p=[x[0] for x in notes], sf=[(x[1], x[2]) for x in notes], vel=vel, art=art, voice=voice))
def motif(st, v, top, vel):
    """'before it's done' on the top strings over the chord: four quarter notes, the chord's bass under the first and third."""
    lo1, lo2 = top[0], top[1]
    for j, (p, s, fr) in enumerate(top[2:]):
        gev(st + 12 * j, 12, [(p, s, fr)], vel - 2 * j, "ring")
    gev(st, 24, [lo1], vel - 4, "ring", "bass"); gev(st + 24, 24, [lo2], vel - 6, "ring", "bass")
for bi, b in enumerate(bars):
    sec, kind, k, st = b["sec"], b["kind"], b["k"], b["start"]; vel = VEL[sec]; sh = shapes_of(b)
    if sec == "Intro" and k == 3:                                                            # D: D C B A (the chorus's last four notes, foreshadowed)
        motif(st, "D", [(50, 4, 0), (45, 5, 0), (62, 2, 3), (60, 2, 1), (59, 2, 0), (57, 3, 2)], vel + 4); continue
    if sec == "Tag" and k == 3:                                                              # Dadd9 in A: E D C# B, arriving on the voice's B
        motif(st, "Dadd9", [(50, 5, 5), (45, 5, 0), (64, 1, 0), (62, 2, 3), (61, 2, 2), (59, 2, 0)], vel + 2); gev(st + 36, 12, [sf("Dadd9", 4), sf("Dadd9", 3)], vel - 8, "ring"); continue
    if kind == "Bridge" and k >= 6:                                                          # the build: strummed, into the lift
        hits = [0, 12, 24, 36] if k == 6 else [0, 12, 18, 24, 30, 36, 42]
        for j, t in enumerate(hits):
            v = "Esus4" if (k == 7 and t < 36) else sh[0]                                  # the E: sus4 under 'it's never missed one yet', the G-sharp on beat 4, into A
            strs = [s for s in range(6, 0, -1) if VOIC[v][0][6 - s] is not None]
            gev(st + t, (hits[j + 1] if j + 1 < len(hits) else 48) - t, [sf(v, s) for s in strs], vel + 12 + (8 if k == 7 else 0) + j * 2, "strum")
        continue
    pat = PAT["last" if sec == "Last Chorus" else "chorus" if kind == "Chorus" else "bridge" if kind == "Bridge" else "verse"]
    for e, slot in enumerate(pat):
        if not slot: continue
        v = sh[e]; bs, al = VOIC[v][1], VOIC[v][2]
        if e == 4 and sf(sh[4], VOIC[sh[4]][1])[0] != sf(sh[0], VOIC[sh[0]][1])[0]: al = VOIC[v][1]       # a new shape at the half bar: its own bass (D/F#'s F#, E/G#'s G#) keeps the walk
        bass = [sf(v, bs if x == "B" else al) for x in slot if isinstance(x, str)]
        ups = [sf(v, x) for x in slot if not isinstance(x, str)]
        L = 12 if kind == "Bridge" else 6
        acc = 8 if e == 0 else 4 if e == 4 else 0
        if bass:
            bl = 24 if kind != "Bridge" else 48 if e == 0 else 0
            if bl: gev(st + 6 * e, bl, bass, vel + 6 + acc, "ring", "bass")
        if ups: gev(st + 6 * e, L, ups, vel + acc // 2 - (2 if e % 2 else 0), "ring")
SHAPE_AT = {}
for bi, b in enumerate(bars):
    sh = shapes_of(b)
    if b["sec"] == "Intro" and b["k"] == 3: sh = ["D"] * 8
    if b["sec"] == "Tag" and b["k"] == 3: sh = ["Dadd9"] * 8
    if b["kind"] == "Bridge" and b["k"] == 7: sh = ["Esus4"] * 6 + ["E"] * 2
    for e in range(8): SHAPE_AT[bi * 8 + e] = sh[e]
def ring_ends(lst):
    """a note rings until its string is played again, or the left hand leaves its fret at a change of shape (an open bass string is
    muted when the new shape leaves it out), or two bars."""
    ons = {}
    for e in lst:
        for st, fr in e["sf"]: ons.setdefault(st, []).append(e["on"])
    for e in lst:
        e["ring"] = []
        for p, (st, fr) in zip(e["p"], e["sf"]):
            end = min([t for t in ons[st] if t > e["on"]] + [e["on"] + 96, NB * BAR + 48])
            t = (e["on"] // 6 + 1) * 6
            while t < end:
                nv = SHAPE_AT.get(t // 6)
                if nv is None: break
                nf = VOIC[nv][0][6 - st]
                if (fr > 0 and nf != fr) or (fr == 0 and nf not in (0, None)) or (fr == 0 and nf is None and st >= 5): end = t; break
                t += 6
            e["ring"].append(end)
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["voice"] != "bass", e["p"][0])); out = []
    for e in lst:                                                                           # one event an onset in each voice (the notation's chords)
        if out and out[-1]["on"] == e["on"] and out[-1]["voice"] == e["voice"]:
            o = out[-1]; z = sorted(zip(o["p"] + e["p"], o["sf"] + e["sf"])); o["p"] = [x for x, _ in z]; o["sf"] = [y for _, y in z]; o["dur"] = max(o["dur"], e["dur"]); continue
        out.append(e)
    return out
gtr = tidy(gtr); ring_ends(gtr)
# ---- the cello: written for this tune (bar: [(beat, length in beats, MIDI)]) ----
CELLO = {}
for k_, p_ in enumerate([52, 48, 47, 45, 43, 48, 45, 50]): CELLO[21 + k_] = [(0, 4, p_)]             # verse 2: E C B A G C A D, a falling line under the voice
for k_, p_ in enumerate([45, 47, 48, 47, 45, 43, 40, 40]): CELLO[37 + k_] = [(0, 4, p_)]             # the bridge: A B C B A G, down to E (the swell into the lift)
CELLO.update({29: [(0, 4, 62)], 30: [(0, 2, 67), (2, 2, 66)], 31: [(0, 2, 62), (2, 1, 64), (3, 1, 67)], 32: [(0, 2, 69), (2, 2, 67)],      # chorus 2: above the voice, the sus under 'thought'
              33: [(0, 4, 67)], 34: [(0, 2, 66), (2, 2, 69)], 35: [(0, 4, 67)], 36: [(0, 2, 62), (2, 2, 66)]})  # answering in its gaps
CELLO.update({45: [(0, 2, 64), (2, 4, 69)], 46: [(2, 2, 68)], 47: [(0, 2, 66), (2, 2, 69)], 48: [(0, 1, 73), (1, 1, 71), (2, 2, 69)],         # the last chorus: the suspension
              49: [(0, 2, 64), (2, 1, 66), (3, 1, 68)], 50: [(0, 2, 71), (2, 2, 69)], 51: [(0, 2, 69), (2, 2, 66)], 52: [(0, 1, 64), (1, 3, 61)]})  # over 'morning' taken, then C#5-B-A
for k_, p_ in enumerate([57, 54, 52, 50]): CELLO[53 + k_] = [(0, 4, p_)]                             # the tag: A F# E D, the last let ring
cello = []
for bar_, evs in sorted(CELLO.items()):
    for bt, ln, p_ in evs:
        st_ = (bar_ - 1) * BAR + int(bt * 12); sec_ = bars[bar_ - 1]["sec"]
        vel_ = {"Verse 2": 56, "Chorus 2": 64, "Bridge": 54, "Last Chorus": 74, "Tag": 52}[sec_] + (12 if bar_ == 44 else 6 if bar_ == 43 else 0)
        cello.append(dict(on=st_, dur=int(ln * 12), p=[p_], vel=vel_, art="swell" if bar_ == 44 else "ring" if bar_ in (52, 56) else "bow"))
for e in cello: assert e["p"][0] % 12 in ({9, 11, 1, 2, 4, 6, 8} if bars[e["on"] // BAR]["sec"] in LIFTED else {7, 9, 11, 0, 2, 4, 6}), e   # in the key
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="Before It's Done", nbars=NB, bars=bars, plan=plan, lead=lead, gtr=gtr, cello=cello, voicings={k: v[0] for k, v in VOIC.items()}, open=OPEN,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"], lift=LIFT, lifted=LIFTED,
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, rerun=F["run"]["rerun"], text=TEXT, liftinfo=c["info"]["lift"], registers=c["meta"]["registers"],
           palettes=c["meta"]["palettes"], outside_target=c["meta"]["outside_target"], carriers=c["meta"]["carriers"],
           sus=SUSLOG, shape_at=SHAPE_AT, design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}, fixr={f"{a}:{b}": v for (a, b), v in P.FIXR.items()},
                       pins={f"{a}:{b}": v for (a, b), v in P.PIN.items()}))
pickle.dump(rec, open("/home/claude/p49/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", dict(gtr=len(gtr), cello=len(cello))); print("the guitar listening:", SUSLOG)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
