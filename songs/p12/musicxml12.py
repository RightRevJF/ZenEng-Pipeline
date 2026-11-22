"""Wood and Cloth (second edition): MusicXML of the hymnal setting (SATB, five stanzas under the soprano) and of the organ score
(choir, descant, organ, pedal), from song_record.json."""
import json
from music21 import stream, note, chord, meter, key, tempo, metadata, clef
import lyric_p12 as L
H = "/home/claude/zeneng-pipeline/songs/p12"; OUT = f"{H}/out"
R = json.load(open(f"{H}/song_record.json")); V = R["voices"]; BAR = 36; ST = {int(k): v for k, v in R["stanza_offsets"].items()}; ED = R["edition"]
def part(name, ev, t0, t1, cl=None, lyr=None):
    p = stream.Part(); p.partName = name
    p.insert(0, meter.TimeSignature("3/4")); p.insert(0, key.Key("D"))
    if cl: p.insert(0, cl)
    for e in ev:
        if not (t0 <= e["on"] < t1): continue
        ps = e["p"] if isinstance(e["p"], list) else [e["p"]]
        x = chord.Chord(ps) if len(ps) > 1 else note.Note(ps[0])
        x.quarterLength = e["dur"] / 12
        p.insert((e["on"] - t0) / 12, x)
    p.makeRests(fillGaps=True, inPlace=True, timeRangeFromBarDuration=True)
    p = p.makeMeasures(); p.makeTies(inPlace=True)
    return p
def hymnal():
    s = stream.Score(); s.insert(0, metadata.Metadata(title=f"{L.TITLE}{ED} - hymnal setting", composer="Words and music: Jason Bryant"))
    a = ST[1]; b = a + 16 * BAR
    sop = part("Soprano", V["S"], a, b)
    ns = [x for x in sop.recurse().notes if not (x.tie and x.tie.type in ("stop", "continue"))]
    tune = R["tune"]; idx = [k for k, t in enumerate(tune) if not t["melisma"]]
    for si in range(5):
        sy = [w for li in range(4) for w, _, _ in L.syls(L.STANZAS[si][li])]
        for j, k in enumerate(idx): ns[k].addLyric(sy[j], lyricNumber=si + 1)
    s.append([sop, part("Alto", V["A"], a, b), part("Tenor", V["T"], a, b, clef.Treble8vbClef()), part("Bass", V["B"], a, b, clef.BassClef())])
    s.write("musicxml", f"{OUT}/{L.TITLE}{ED} - hymnal setting.musicxml")
def organ():
    s = stream.Score(); s.insert(0, metadata.Metadata(title=f"{L.TITLE}{ED} - organ score with choir", composer="Words and music: Jason Bryant"))
    E = R["end"]
    s.append([part("Descant", V["Desc"], 0, E), part("Soprano", V["S"], 0, E), part("Alto", V["A"], 0, E), part("Tenor", V["T"], 0, E, clef.Treble8vbClef()),
              part("Bass", V["B"], 0, E, clef.BassClef()), part("Organ RH", V["org_rh"], 0, E), part("Organ LH", V["org_lh"], 0, E, clef.BassClef()),
              part("Pedal", V["org_ped"], 0, E, clef.BassClef())])
    s.write("musicxml", f"{OUT}/{L.TITLE}{ED} - organ score with choir.musicxml")
hymnal(); organ(); print("ok")
