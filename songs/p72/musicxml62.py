"""Song 62: MusicXML of the full score (voice with words, string quartet, piano), from out/<label>/record.json, on the same sixteenth grid as the engraving.
  python3 musicxml62.py "first edition" -> out/<label>/<title> (<label>) - full score.musicxml"""
import json, sys, re
from music21 import stream, note, chord, meter, key as mkey, tempo, instrument, metadata, clef
LABEL = sys.argv[1]; D = f"out/{LABEL}"; R = json.load(open(f"{D}/record.json")); B = R["bar"]; U = 3
NB = sum(b for _, _, b in R["form"]); q = lambda x: int(round(x / U))
def events(part, mono=True):
    ev = []
    for e in sorted(part, key=lambda e: e["on"]):
        ps = e["p"] if isinstance(e["p"], list) else [e["p"]]; s = q(e["on"]); t = max(s + 1, q(e["on"] + e["dur"]))
        if ev and ev[-1][0] == s: ev[-1] = (s, max(t, ev[-1][1]), sorted(set(ev[-1][2]) | set(ps)), ev[-1][3]); continue
        ev.append((s, t, sorted(ps), e.get("lyric")))
    out = []
    for i, (s, t, ps, ly) in enumerate(ev):
        nxt = ev[i + 1][0] if i + 1 < len(ev) else NB * 16; t = min(t, nxt)
        if t > s: out.append((s, t, ps, ly))
    return out
import engrave_syll as ES
mel = sorted(R["melody"], key=lambda n: n["on"]); sy = ES.syllables(mel)
def build(name, inst, part, cl, lyr=False):
    p = stream.Part(); p.partName = name; p.insert(0, inst); p.insert(0, cl); p.insert(0, mkey.Key("E-")); p.insert(0, meter.TimeSignature("4/4"))
    if lyr: p.insert(0, tempo.MetronomeMark(number=R["bpm"], text="Gently, with space"))
    pos = 0
    for s, t, ps, ly in events(part):
        if s > pos: p.append(note.Rest(quarterLength=(s - pos) / 4))
        n = note.Note(ps[0], quarterLength=(t - s) / 4) if len(ps) == 1 else chord.Chord(ps, quarterLength=(t - s) / 4)
        if ly: n.lyric = ly
        p.append(n); pos = t
    if pos < NB * 16: p.append(note.Rest(quarterLength=(NB * 16 - pos) / 4))
    return p.makeMeasures().makeTies()
sc = stream.Score(); sc.metadata = metadata.Metadata(title=f"{R['title']} ({LABEL})", composer="Words and music: Jason Bryant")
sc.append(build("Voice", instrument.Tenor(), [dict(on=n["on"], dur=n["dur"], p=n["midi"], lyric=l) for n, l in zip(mel, sy)], clef.Treble8vbClef(), True))
for nm_, ins, k, cl in (("Violin I", instrument.Violin(), "violin1", clef.TrebleClef()), ("Violin II", instrument.Violin(), "violin2", clef.TrebleClef()), ("Viola", instrument.Viola(), "viola", clef.AltoClef()), ("Cello", instrument.Violoncello(), "cello", clef.BassClef()),
                        ("Piano (right hand)", instrument.Piano(), "piano", clef.TrebleClef()), ("Piano (left hand)", instrument.Piano(), "bass", clef.BassClef())):
    sc.append(build(nm_, ins, R["parts"][k], cl))
out = f"{D}/{R['title']} ({LABEL}) - full score.musicxml"; sc.write("musicxml", fp=out); print(out)
