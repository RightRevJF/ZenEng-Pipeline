"""musicxml_p58.py: 'The Ratios Hold' (song 48) as MusicXML, written from the song record (the events the demo plays, before humanizing),
on the same grid as the lead sheet and parts (sixteenths; each staff's notes held to the next onset). Two scores: the lead sheet (voice,
lyrics, chord symbols) and the full score (every part). Each as .musicxml and compressed .mxl. Read back with music21 and counted against
the record. Words and music: Jason Bryant."""
import pickle, collections, os, sys, copy
from music21 import percussion, stream, note, chord, meter, key, tempo, metadata, harmony, instrument, clef, converter, pitch
REC = pickle.load(open("/home/claude/p58/song_record.pkl", "rb")); OUT = "/home/claude/p58/out"
BARS = REC["bars"]; NB = len(BARS); TPQ = 12
BST = [b["start"] for b in BARS]; BEND = BST[-1] + BARS[-1]["len"]
def bar_of(t):
    lo, hi = 0, NB - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if BST[m] <= t: lo = m
        else: hi = m - 1
    return lo
def events(src, key_="p"):
    """[(on, dur, [midi...], lyric)] with simultaneous onsets merged and each held to the next onset, on the sixteenth grid."""
    by = collections.OrderedDict()
    for e in sorted(src, key=lambda e: e["on"]):
        ps = e[key_] if isinstance(e[key_], list) else [e[key_]]
        if e["on"] in by: by[e["on"]][1] = sorted(set(by[e["on"]][1]) | set(ps)); by[e["on"]][0] = max(by[e["on"]][0], e["dur"])
        else: by[e["on"]] = [e["dur"], list(ps), e]
    ons = list(by); out = []
    for i, o in enumerate(ons):
        nxt = ons[i + 1] if i + 1 < len(ons) else BEND
        d = max(3, min(int(round(by[o][0] / 3)) * 3, nxt - o)); out.append((o, d, by[o][1], by[o][2]))
    return out
def syllabic(lead):
    out = {}; prev_h = False
    for n in sorted(lead, key=lambda n: n["on"]):
        if not n.get("first"): continue
        s = ("middle" if prev_h else "begin") if n["hyph"] else ("end" if prev_h else "single")
        out[n["on"]] = (n["text"], s); prev_h = n["hyph"]
    return out
def build_part(name, inst, evs, lyr=None, clef_=None, drums=False, chords=False, marks=False):
    p = stream.Part(); p.partName = name; p.insert(0, inst)
    met = None
    for bi, b in enumerate(BARS):
        m = stream.Measure(number=bi + 1)
        if bi == 0:
            if clef_: m.insert(0, clef_)
            m.insert(0, key.Key("E")); m.insert(0, tempo.MetronomeMark(number=REC["qbpm"], referent=note.Note(type="quarter")))
        if b["meter"] != met: met = b["meter"]; m.insert(0, meter.TimeSignature(met))
        if chords and b["sec"] not in ("Overture", "Study", "Window", "Coda") or (chords and True):
            for off, c in ((0, b["chord"]), (24, b["chord2"])):
                if off and (c == b["chord"] or b["len"] != 48): continue
                try: cs = harmony.ChordSymbol(c.replace("Ab", "G#")); cs.writeAsChord = False; m.insert(off / TPQ, cs)
                except Exception: pass
        if marks and (bi == 0 or BARS[bi - 1]["sec"] != b["sec"]):
            from music21 import expressions
            m.insert(0, expressions.RehearsalMark(b["sec"]))
        p.append(m)
    ms = list(p.getElementsByClass(stream.Measure))
    for o, d, ps, e in evs:
        first = True
        while d > 0:
            bi = bar_of(o); room = BST[bi] + BARS[bi]["len"] - o; seg = min(d, room)
            if drums:
                el = percussion.PercussionChord([note.Unpitched() for _ in ps]) if len(ps) > 1 else note.Unpitched()
                if isinstance(el, percussion.PercussionChord):
                    for x_, mid_ in zip(el.notes, ps): x_.displayStep, x_.displayOctave = {36: ("F", 4), 38: ("C", 5), 37: ("C", 5), 42: ("G", 5), 46: ("G", 5), 49: ("A", 5), 51: ("F", 5), 48: ("E", 5), 45: ("D", 5), 41: ("A", 4)}.get(mid_, ("C", 5))
                else: el.displayStep, el.displayOctave = {36: ("F", 4), 38: ("C", 5), 37: ("C", 5), 42: ("G", 5), 46: ("G", 5), 49: ("A", 5), 51: ("F", 5), 48: ("E", 5), 45: ("D", 5), 41: ("A", 4)}.get(ps[0], ("C", 5))
            else:
                el = chord.Chord([pitch.Pitch(midi=x_) for x_ in ps]) if len(ps) > 1 else note.Note(pitch.Pitch(midi=ps[0]))
                if not isinstance(el, chord.Chord): el.pitch = el.pitch.simplifyEnharmonic(mostCommon=False)
            el.quarterLength = seg / TPQ
            if seg < d or not first:
                from music21 import tie
                el.tie = tie.Tie("start" if first else ("continue" if seg < d else "stop"))
            if first and lyr and o in lyr:
                from music21 import note as n_
                el.lyrics = [n_.Lyric(text=lyr[o][0], syllabic=lyr[o][1])]
            ms[bi].insert((o - BST[bi]) / TPQ, el)
            o += seg; d -= seg; first = False
    for m in ms: m.makeRests(fillGaps=True, inPlace=True, timeRangeFromBarDuration=True)
    return p
def spell(pt):
    """sharps from the key (E major)."""
    for n in pt.recurse().notes:
        for pp in ((n.pitches if isinstance(n, chord.Chord) else [n.pitch]) if not isinstance(n, (note.Unpitched, percussion.PercussionChord)) else []):
            if pp.accidental is not None and pp.accidental.name == "flat": pp.getEnharmonic(inPlace=True)
def score(title, parts):
    s = stream.Score(); s.insert(0, metadata.Metadata()); s.metadata.title = "The Ratios Hold"; s.metadata.movementName = title
    s.metadata.composer = "Words and music: Jason Bryant"
    for p in parts: spell(p); s.insert(0, p)
    return s
lead = REC["lead"]; LY = syllabic(lead)
def voice_part(): return build_part("Voice", instrument.Vocalist(), events(lead, "midi"), lyr=LY, clef_=clef.Treble8vbClef(), chords=True, marks=True)
P_ = REC["parts"]
def full_parts():
    hi = [dict(n, p=n["midi"]) for n in REC["harm_hi"]]; lo = [dict(n, p=n["midi"]) for n in REC["harm_lo"]]
    ins = lambda cls, nm: (lambda i_: (setattr(i_, "partName", nm), i_)[1])(cls())
    return [voice_part(),
            build_part("Harmony (high)", ins(instrument.Vocalist, "Harmony (high)"), events(hi), clef_=clef.Treble8vbClef()),
            build_part("Harmony (low)", ins(instrument.Vocalist, "Harmony (low)"), events(lo), clef_=clef.Treble8vbClef()),
            build_part("Moog lead", ins(instrument.Instrument, "Moog lead"), events(P_["moog"])),
            build_part("Hammond organ", ins(instrument.ElectricOrgan, "Hammond organ"), events(P_["hammond"])),
            build_part("Church organ", ins(instrument.PipeOrgan, "Church organ"), events(P_["organ"])),
            build_part("Mellotron", ins(instrument.StringInstrument, "Mellotron"), events(P_["strings"] + P_["choir"])),
            build_part("Piano", ins(instrument.Piano, "Piano"), events(P_["piano"]), clef_=clef.BassClef()),
            build_part("Electric guitar", ins(instrument.ElectricGuitar, "Electric guitar"), events(P_["guitar"]), clef_=clef.Treble8vbClef()),
            build_part("Acoustic guitar", ins(instrument.AcousticGuitar, "Acoustic guitar"), events(P_["acoustic"]), clef_=clef.Treble8vbClef()),
            build_part("Bass", ins(instrument.ElectricBass, "Bass"), events(P_["bass"]), clef_=clef.BassClef()),
            build_part("Drums", ins(instrument.Percussion, "Drums"), events(P_["drums"]), clef_=clef.PercussionClef(), drums=True)]
if __name__ == "__main__":
    want = {"Voice": len(events(lead, "midi")), "Harmony (high)": len(events([dict(n, p=n["midi"]) for n in REC["harm_hi"]])), "Harmony (low)": len(events([dict(n, p=n["midi"]) for n in REC["harm_lo"]])),
            "Moog lead": len(events(P_["moog"])), "Hammond organ": len(events(P_["hammond"])), "Church organ": len(events(P_["organ"])), "Mellotron": len(events(P_["strings"] + P_["choir"])),
            "Piano": len(events(P_["piano"])), "Electric guitar": len(events(P_["guitar"])), "Acoustic guitar": len(events(P_["acoustic"])), "Bass": len(events(P_["bass"])), "Drums": len(events(P_["drums"]))}
    for lab, parts in (("lead sheet", [voice_part()]), ("full score", full_parts())):
        s = score(lab.capitalize(), parts)
        base = f"{OUT}/The Ratios Hold - {lab}"
        print("  wrote", s.write("mxl", fp=base + ".mxl"), s.write("musicxml", fp=base + ".musicxml"))
        back = converter.parse(base + ".mxl")
        for p in back.parts:
            n_on = sum(1 for n in p.recurse().notes if not isinstance(n, harmony.ChordSymbol) and not (n.tie is not None and n.tie.type in ("stop", "continue")))
            nm = p.partName
            print(f"{lab}: {nm}: {n_on} onsets read back, record {want.get(nm)}", "OK" if n_on == want.get(nm) else "CHECK")
        if lab == "lead sheet":
            ly = [n.lyric for n in back.parts[0].recurse().notes if n.lyric]; print("  lyrics read back:", len(ly), "record", len(LY))
    back = converter.parse(f"{OUT}/The Ratios Hold - full score.musicxml")
    for p in back.parts:
        if p.partName in ("Voice", "Bass", "Moog lead"):
            got = sorted(x.midi for n in p.recurse().notes if not isinstance(n, harmony.ChordSymbol) and not (n.tie is not None and n.tie.type in ("stop", "continue")) for x in n.pitches)
            src = {"Voice": events(lead, "midi"), "Bass": events(P_["bass"]), "Moog lead": events(P_["moog"])}[p.partName]
            print(f"pitches, {p.partName}:", "match" if got == sorted(x for e in src for x in e[2]) else "MISMATCH")
