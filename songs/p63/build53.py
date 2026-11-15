"""Sung to Sleep (song 53): the record. The hymn tune (melody_final.json, D-space) harmonized in four parts by the carol pipeline's beam
search (harmonize53.py), then laid on one timeline in sounding pitch, from which both documents (the organ full score and the choir's hymn
page) are written, so their bars, line breaks and notes agree by construction.

Timeline (twelfths of a quarter; bar n spans (n-1)*36 to n*36; a pickup at -12):
  bars 1-4    organ introduction: the refrain's last line (with its pickup), E-flat major
  bars 5-20   verses 1-3 (stanzas printed together), pickup on bar 4 beat 3
  bars 21-36  refrain, sung after each of verses 1-3
  bars 37-38  organ link to F major (G minor 7, C7sus4, C7)
  bars 39-54  verse 4 in F: the choir in unison on the tune (men an octave lower); the organ's own harmony (749.8)
  bars 55-70  final refrain in F: four parts, the sopranos' descant above (749.9 for both), the last 'here' held
The whole-song shape (749.10): verses 1-3 and their refrains in E-flat, the last verse and refrain a step higher in F; the tune's top (E-flat5,
then F5) and the descant's top (A5) both in the final refrain."""
import json, copy, collections
import harmonize53 as HZ, harm68, lyric_p63 as L, gen34 as G
H = "/home/claude/p63"
M = json.load(open(f"{H}/melody_final.json")); TUNE = M["pick"]["tune"]
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
        return set(chords[k])
    ps = harm68.high(span, tones_at, lo=lo, hi=hi)
    assert all(p == pin_world for p, n in zip(ps, notes) if n["p"] == 74 and n["on"] % BAR == 0)
    return ps
DESC = descant(REFRAIN, pathFR)
# ---- the timeline, sounding pitch ----
OFF = {"intro": -432, "A_verse": 144, "A_refrain": 720, "B_verse": 1368, "B_refrain": 1944}
END = 70 * BAR
V = collections.defaultdict(list)                     # voice -> events dict(on, dur, p, syl?, slur?, sec)
def put(voice, on, dur, p, **kw): V[voice].append(dict(on=on, dur=dur, p=p, **kw))
# intro: the refrain's last line (organ alone), from its pickup
for k, n in enumerate(REFRAIN):
    if n["line"] != 3: continue
    ch, A, T, B = pathAR[k]; t = n["on"] + OFF["intro"]
    put("org_rh_s", t, n["dur"], n["p"] + 1); put("org_rh_a", t, n["dur"], A + 1); put("org_lh", t, n["dur"], T + 1); put("org_ped", t, n["dur"], B + 1)
# section A: choir and organ together
for notes, path, off, part in ((VERSE, pathAV, OFF["A_verse"], "verse"), (REFRAIN, pathAR, OFF["A_refrain"], "refrain")):
    for k, n in enumerate(notes):
        ch, A, T, B = path[k]; t = n["on"] + off
        put("S", t, n["dur"], n["p"] + 1, syl=n["syl"], line=n["line"], part=part, slur=n["slur"], melisma=n["melisma"], chord=ch)
        put("A", t, n["dur"], A + 1); put("T", t, n["dur"], T + 1); put("B", t, n["dur"], B + 1)
        put("org_rh_s", t, n["dur"], n["p"] + 1); put("org_rh_a", t, n["dur"], A + 1); put("org_lh", t, n["dur"], T + 1); put("org_ped", t, n["dur"], B + 1)
# link: bars 37-38 (sounding pitch, F major's signature): G minor 7, then C7sus4 to C7
L0 = 36 * BAR
for pitches, on, dur in (([65, 70, 74], L0, 36), ([65, 70, 72], L0 + 36, 12), ([64, 70, 72], L0 + 48, 12)):
    put("org_rh_s", on, dur, pitches[-1]); put("org_rh_a", on, dur, pitches[-2]); put("org_lh", on, dur, pitches[0])
put("org_ped", L0, 36, 43); put("org_ped", L0 + 36, 24, 48)
# verse 4: unison choir, the organ's own harmony
for k, n in enumerate(VERSE):
    ch, A, T, B = path4[k]; t = n["on"] + OFF["B_verse"]; m = n["p"] + 3
    put("S", t, n["dur"], m, syl=n["syl"], line=n["line"], part="verse4", slur=n["slur"], melisma=n["melisma"], chord=ch)
    put("A", t, n["dur"], m); put("T", t, n["dur"], m - 12); put("B", t, n["dur"], m - 12)
    put("org_rh_s", t, n["dur"], m); put("org_rh_a", t, n["dur"], A + 3); put("org_lh", t, n["dur"], T + 3); put("org_ped", t, n["dur"], B + 3)
# final refrain: four parts, the descant, the last note held to the end of bar 70
for k, n in enumerate(REFRAIN):
    ch, A, T, B = pathFR[k]; t = n["on"] + OFF["B_refrain"]; d = n["dur"]
    if k == len(REFRAIN) - 1: d = END - t
    put("S", t, d, n["p"] + 3, syl=n["syl"], line=n["line"], part="refrain_final", slur=n["slur"], melisma=n["melisma"], chord=ch)
    put("A", t, d, A + 3); put("T", t, d, T + 3); put("B", t, d, B + 3)
    put("Desc", t, d, DESC[k] + 3, syl=n["syl"], line=n["line"], slur=n["slur"], melisma=n["melisma"])
    put("org_rh_s", t, d, n["p"] + 3); put("org_rh_a", t, d, A + 3); put("org_lh", t, d, T + 3); put("org_ped", t, d, B + 3)
for v in V.values(): v.sort(key=lambda e: e["on"])
def merge_holds(ev):
    """a lower voice under a melisma: the same pitch on the slur's second note joins the first (one held note)"""
    out = []
    for e in ev:
        if out and out[-1]["p"] == e["p"] and out[-1]["on"] + out[-1]["dur"] == e["on"] and e.get("hold_ok"): out[-1]["dur"] += e["dur"]
        else: out.append(dict(e))
    return out
S_on = {e["on"]: e for e in V["S"]}
for voice in ("A", "T", "B", "org_rh_a", "org_lh", "org_ped"):
    for e in V[voice]:
        s = S_on.get(e["on"]); e["hold_ok"] = bool(s and s.get("melisma"))
    V[voice] = merge_holds(V[voice])
REC = dict(title=L.TITLE, voices={k: v for k, v in V.items()}, offsets=OFF, end=END, bars=70, pickup=12, keys=[(-12, "E-flat major"), (L0, "F major")],
           paths=dict(A=pathA, verse4=path4, final_refrain=pathFR), costs=dict(A=costA, verse4=cost4, final_refrain=costFR), descant_dspace=DESC,
           reharm=REHARM, verse_chords=G.VERSE_CH, refrain_chords=G.REFRAIN_CH, fp=M["pick"]["fp"], qpm=88)
json.dump(REC, open(f"{H}/song_record.json", "w"))
if __name__ == "__main__":
    print({k: len(v) for k, v in V.items()}, "costs", {k: round(v, 1) for k, v in REC["costs"].items()})
    N = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']; nm = lambda p: N[p % 12] + str(p // 12 - 1)
    for k in ("S", "A", "T", "B", "Desc"): ps = [e["p"] for e in V[k]]; print(k, nm(min(ps)), nm(max(ps)))
    print("verse 4 organ chords", [c for c, *_ in path4][:16]); print("descant", [nm(p + 3) for p in DESC])
    for nmv, path, notes in (("A", pathA, VERSE + REFRAIN), ("verse4", path4, VERSE), ("final", pathFR, REFRAIN)):
        print(nmv, HZ.stats(hz_input(notes, G.VERSE_CH + G.REFRAIN_CH if nmv == "A" else (REHARM if nmv == "verse4" else G.REFRAIN_CH)), path))
