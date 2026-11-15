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
# intro (E-flat; D-space +1): the refrain's line 1 at bars 1-4 ('small' cut to a half), then its line 4 from the pickup on bar 4 beat 3
intro = []
for k, n in enumerate(REFRAIN):
    if n["line"] == 0: intro.append((n["on"], 24 if k == max(j for j, m in enumerate(REFRAIN) if m["line"] == 0) else n["dur"], k))
    if n["line"] == 3: intro.append((n["on"] - 420 + 132, n["dur"], k))
for on, d, k in intro:
    ch, A, T, B = pathAR[k]; s = REFRAIN[k]["p"]
    put("org_rh", on, d, sorted({A + 1, s + 1}))
for bar in range(8):
    t = bar * BAR; ks = [k for on, d, k in intro if on <= t]; k = ks[-1] if ks else intro[0][2]
    ch, A, T, B = pathAR[k]; dur = 24 if bar == 7 else 36
    for on, d, p in rocking(ch, t, dur, 1): put("org_lh", on, d, p)
    put("org_ped", t, dur, B + 1)
# section A (E-flat): the choir with its passing notes; the organ a fuller form of it (a filled chord in each hand), common tones held
for notes, path, segl, off, part in ((VERSE, pathAV, SEG_AV, OFF["A_verse"], "verse"), (REFRAIN, pathAR, SEG_AR, OFF["A_refrain"], "refrain")):
    for k, n in enumerate(notes):
        ch = path[k][0]; t = n["on"] + off; s = n["p"]
        put("S", t, n["dur"], s + 1, syl=n["syl"], line=n["line"], part=part, slur=n["slur"], melisma=n["melisma"], chord=ch)
        for vi, vn in enumerate(("A", "T", "B")):                     # a voice without the passing note keeps one note
            last = None
            for o, d, *abt in segl[k]:
                if last is not None and last["p"] == abt[vi] + 1: last["dur"] += d
                else: put(vn, t + o, d, abt[vi] + 1); last = V[vn][-1]
        for o, d, A, T, B in segl[k]:
            f = fill_between(ch, A, s)
            if f is None: f = next((q for q in reversed(tones_in(ch, max(A - 8, 55), A - 3))), None)          # no room between: a chord tone under the alto
            rh = sorted({A, s} | ({f} if f else set()))
            g = next((q for q in reversed(tones_in(ch, max(B + 3, 48), T - 3))), None); lh = sorted({T} | ({g} if g else set()))
            put("org_rh", t + o, d, [q + 1 for q in rh]); put("org_lh", t + o, d, [q + 1 for q in lh]); put("org_ped", t + o, d, B + 1)
# link (sounding pitch, F's signature from bar 41): E-flat, G minor 7, C7sus4, C7; the rocking figure over each bar
LINK = [("Eb", [67, 70, 75], 39, [51, 58, 55]), ("Gm7", [65, 70, 74], 43, [55, 62, 58]), ("C7sus4", [65, 70, 72], 48, [48, 55, 53]), ("C7", [64, 70, 72], 48, [48, 55, 52])]          # left hand: root, fifth, third (the fourth in the sus chord), inside a fifth
for i, (nm_, rh, ped, (r, f5, t3)) in enumerate(LINK):
    t = L0 + i * BAR; dur = 24 if i == 3 else 36
    put("org_rh", t, dur, rh); put("org_ped", t, dur, ped)
    pat = [r, f5, t3, f5, t3, f5]
    for j in range(dur // 6): put("org_lh", t + 6 * j, 6, pat[j % 6])
# verse 4 (F; D-space +3): the choir in unison; the organ's own accompaniment
segs4 = []
for k, n in enumerate(VERSE):
    ch = path4[k][0]
    if segs4 and segs4[-1]["ch"] == ch: segs4[-1]["ks"].append(k)
    else: segs4.append(dict(ch=ch, ks=[k]))
prev_top = None
for sg in segs4:
    ks = sg["ks"]; ch = sg["ch"]; on = VERSE[ks[0]]["on"] + OFF["B_verse"]; last = VERSE[ks[-1]]
    end = last["on"] + last["dur"] + OFF["B_verse"]
    if sg is segs4[-1]: end = OFF["B_refrain"] - 12
    mel_lo = min(VERSE[k]["p"] for k in ks)
    tops = [q for q in tones_in(ch, 59, mel_lo - 1)]
    top = tops[-1] if tops else mel_lo - 3
    mids = [q for q in tones_in(ch, max(top - 9, 54), top - 3)]
    chord = sorted({top} | set(mids[-2:]))
    sus = prev_top is not None and prev_top % 12 not in pcs(ch) and any(0 < prev_top - q <= 2 and q % 12 in pcs(ch) for q in [top]) and end - on >= 24
    if sus:
        put("org_rh", on, 12, [q + 3 for q in sorted(set(chord) - {top} | {prev_top})], sus=True)
        put("org_rh", on + 12, end - on - 12, [q + 3 for q in chord])
    else:
        put("org_rh", on, end - on, [q + 3 for q in chord])
    prev_top = top
for k, n in enumerate(VERSE):
    ch, A, T, B = path4[k]; t = n["on"] + OFF["B_verse"]; m = n["p"] + 3
    put("S", t, n["dur"], m, syl=n["syl"], line=n["line"], part="verse4", slur=n["slur"], melisma=n["melisma"], chord=ch)
    put("A", t, n["dur"], m); put("T", t, n["dur"], m - 12); put("B", t, n["dur"], m - 12)
    put("org_ped", t, n["dur"], B + 3)
for bar in range(16):
    t = OFF["B_verse"] + bar * BAR; ch = chord_at(VERSE, path4, bar * BAR)[0]
    dur = 24 if bar == 15 else 36
    for on, d, p in rocking(ch, t, dur, 3, lo=42, hi=56): put("org_lh", on, d, p)
put("org_lh", OFF["B_verse"] - 12, 12, [q + 3 for q in tones_in(path4[0][0], 45, 56)[:2]])
# final refrain (F): four parts and the descant; the organ's own accompaniment
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
segsF = []
for k, n in enumerate(REFRAIN):
    ch = pathFR[k][0]
    if segsF and segsF[-1]["ch"] == ch and n["on"] % BAR != 0: segsF[-1]["ks"].append(k)
    else: segsF.append(dict(ch=ch, ks=[k]))
for i, sg in enumerate(segsF):
    k0 = sg["ks"][0]; ch, A, T, B = pathFR[k0]; s = REFRAIN[k0]["p"]; on = REFRAIN[k0]["on"] + OFF["B_refrain"]
    end = (REFRAIN[segsF[i + 1]["ks"][0]]["on"] + OFF["B_refrain"]) if i + 1 < len(segsF) else CODA
    f = fill_between(ch, A, s); put("org_rh", on, end - on, [q + 3 for q in sorted({A, s} | ({f} if f else set()))])
PED_TONIC, PED_DOM = (0, 4), (12, 14)                                             # bars of the final refrain: under 'Hush now', under 'is sleeping, sleeping'
pb = []
for k, n in enumerate(REFRAIN):
    b = n["on"] // BAR
    if PED_TONIC[0] <= b < PED_TONIC[1] or PED_DOM[0] <= b < PED_DOM[1]: continue
    d = n["dur"] if k < len(REFRAIN) - 1 else CODA - (n["on"] + OFF["B_refrain"])
    pb.append((n["on"] + OFF["B_refrain"], d, pathFR[k][3] + 3))
pb.append((OFF["B_refrain"], 4 * BAR, 62 - 24 + 3)); pb.append((OFF["B_refrain"] + 12 * BAR, 2 * BAR, 69 - 24 + 3))
for on, d, p in sorted(pb): put("org_ped", on, d, p)
for bar in range(16):
    t = OFF["B_refrain"] + bar * BAR; ch = chord_at(REFRAIN, pathFR, bar * BAR)[0]
    for on, d, p in rocking(ch, t, 36, 3, lo=42, hi=56): put("org_lh", on, d, p)
# coda (sounding, F): the refrain's last phrase once more over a tonic pedal; IV to I
l4 = [n for n in REFRAIN if n["line"] == 3]
mot = [(n["on"] - l4[1]["on"], n["dur"], n["p"] + 3) for n in l4[1:-1]]            # 'sleep-ing, sleep-ing' without its pickup and 'here'
CH_CODA = [([58, 62], 0, 24), ([60, 64], 36, 36)]
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
for voice in ("org_rh", "org_lh", "org_ped"):
    for e in V[voice]: e["organ"] = True
    V[voice] = merge_holds(V[voice])
    for a, b in zip(V[voice], V[voice][1:]):                                       # the organ legato: a beat's gap closed by the note before
        if 0 < b["on"] - (a["on"] + a["dur"]) <= 12: a["dur"] = b["on"] - a["on"]
REC = dict(title=L.TITLE, voices={k: v for k, v in V.items()}, offsets=OFF, end=END, bars=80, pickup=0, keys=[(0, "E-flat major"), (L0, "F major")], link_bar=41, coda_bar=77,
           paths=dict(A=pathA, verse4=path4, final_refrain=pathFR), costs=dict(A=costA, verse4=cost4, final_refrain=costFR), descant_dspace=DESC,
           reharm=REHARM, verse_chords=G.VERSE_CH, refrain_chords=G.REFRAIN_CH, fp=M["pick"]["fp"], qpm=88)
json.dump(REC, open(f"{H}/song_record.json", "w"))
if __name__ == "__main__":
    print({k: len(v) for k, v in V.items()}, "costs", {k: round(v, 1) for k, v in REC["costs"].items()})
    N = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']; nm = lambda p: N[p % 12] + str(p // 12 - 1)
    for k, v in V.items():
        ps = [q for e in v for q in (e["p"] if isinstance(e["p"], list) else [e["p"]])]; print(k, nm(min(ps)), nm(max(ps)))
    for k in ("org_rh", "org_lh", "org_ped"):
        bad = [(e["on"], e["dur"]) for e in V[k] if e["dur"] <= 0]; print(k, "no-length", bad[:3])
