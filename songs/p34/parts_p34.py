"""Swallowed Up -- the parts (9-M.9): rhythm guitars 1 and 2 (one part: the same riff, left and right), lead guitar, bass, drums,
and the voice. Guitars and bass in standard notation at sounding pitch (treble 8vb, bass 8vb), the tuning at the head, palm mutes
marked (P.M.), the open strokes accented; the feel named at each change; drums on a drum staff (kick below, hands above).
Every part read back from LilyPond's MIDI against the record."""
import pickle, re, sys, os, collections
sys.path[:0] = ["/home/claude/p34", "/home/claude/carol"]
from lily import compile_ly, midi_readback
from lily34 import stream, pname, DUR, esc
import engrave_p34 as EG
REC = EG.REC; BARS = EG.BARS; NB = EG.NB; OUT = EG.OUT
EV = REC["events"]

def chords_of(part):
    g = collections.OrderedDict()
    for e in EV:
        if e["part"] != part: continue
        k = (e["bar"], e["slot"]); g.setdefault(k, dict(abs16=e["bar"] * 16 + e["slot"], dur=e["dur"], ps=[], pm=e.get("pm", False)))["ps"].append(e["pitch"])
    return list(g.values())

def pitched_part(part, pm_marks=True):
    items = chords_of(part)
    # P.M. spans: in each bar, from the first palm-muted stroke to the last
    first_pm, last_pm = {}, {}
    for it in items:
        if it["pm"]:
            b = it["abs16"] // 16; first_pm.setdefault(b, it["abs16"]); last_pm[b] = it["abs16"]
    def tok(it, Ln, tie, first):
        ps = sorted(it["ps"]); t = (pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">") + DUR[Ln] + ("~" if tie else "")
        if first and pm_marks:
            b = it["abs16"] // 16
            if not it["pm"] and part != "Lead" and it["dur"] <= 4 and BARS[b]["riff"] in ("A", "B", "B'", "D"): t += "->"
            if b in first_pm and first_pm[b] != last_pm[b]:
                if it["abs16"] == first_pm[b]: t += "\\startTextSpan"
                elif it["abs16"] == last_pm[b]: t += "\\stopTextSpan"
            elif b in first_pm and it["abs16"] == first_pm[b]: t += '_\\markup \\tiny "P.M."'
        return t
    return stream(items, NB, tok), items

DRUM = {36: "bd", 38: "sn", 42: "hh", 51: "cymr", 49: "cymc", 52: "cymch", 41: "tomfl"}
def drum_voices():
    ups, downs = collections.defaultdict(list), collections.defaultdict(list)
    for e in EV:
        if e["part"] != "Drums": continue
        (downs if e["pitch"] == 36 else ups)[e["bar"] * 16 + e["slot"]].append(e["pitch"])
    out = {}
    for name, d in (("up", ups), ("down", downs)):
        ks = sorted(d); items = []
        for a, b in zip(ks, ks[1:] + [NB * 16]):
            L = min(b - a, 4, 16 - a % 16); items.append(dict(abs16=a, dur=L, ps=d[a]))
        def tok(it, Ln, tie, first):
            ps = sorted(set(it["ps"]))
            if not first: return "r" + DUR[Ln]                     # a drum stroke is not held: the rest of its value is silence
            return (DRUM[ps[0]] if len(ps) == 1 else "<" + " ".join(DRUM[p] for p in ps) + ">") + DUR[Ln]
        out[name] = (stream(items, NB, tok, mmrest=False), items)
    return out

def feel_marks():
    m = {}
    for k, bb in enumerate(BARS):
        if bb["sec"] == "Intro" and bb["i"] == 8: m[k] = '\\mark \\markup \\box "guitar 2 and bass in; floor tom and china on the accents"'
        if bb["sec"] == "Intro" and bb["i"] == 12: m[k] = '\\mark \\markup \\box "normal time"'
    return m

HEAD = """\\version "2.24.3"
#(set-global-staff-size 17)
\\paper { #(set-paper-size "letter") left-margin = 12\\mm right-margin = 12\\mm top-margin = 10\\mm bottom-margin = 16\\mm
  oddFooterMarkup = \\markup \\fill-line { \\tiny "Swallowed Up · Words and music: Jason Bryant · tuning B E A D F♯ B · ♩ = 200; the slowdown ♩ = 100" }
  evenFooterMarkup = \\markup \\fill-line { \\tiny "Swallowed Up · Words and music: Jason Bryant · tuning B E A D F♯ B · ♩ = 200; the slowdown ♩ = 100" }
  max-systems-per-page = 8 ragged-last-bottom = ##t }
\\header { title = "Swallowed Up" composer = "Words and music: Jason Bryant" tagline = ##f }
\\layout { \\context { \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1.5 }
  \\context { \\Voice \\override TextSpanner.bound-details.left.text = \\markup \\tiny "P.M." \\override TextSpanner.style = #'dashed-line
     \\override TextSpanner.direction = #DOWN } }
"""
def bookpart(name, staff):
    return f"""\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << {staff} >> }} }}
"""
CH = f"\\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {EG.CHORDS} }}"
if __name__ == "__main__":
    os.makedirs(OUT + "/check", exist_ok=True)
    G, gi = pitched_part("Gtr 1"); L, li = pitched_part("Lead", pm_marks=False); Bs, bi = pitched_part("Bass")
    D = drum_voices(); V = EG.voice_tokens(); VL = EG.lyric_tokens()
    fm = feel_marks()
    gstaff = f'{CH} \\new Staff \\with {{ instrumentName = "Gtrs 1, 2" }} {{ \\clef "treble_8" \\key b \\minor \\compressMMRests {{ {EG.body(G, part_marks=fm)} \\bar "|." }} }}'
    lstaff = f'{CH} \\new Staff \\with {{ instrumentName = "Lead" }} {{ \\clef "treble_8" \\key b \\minor \\compressMMRests {{ {EG.body(L)} \\bar "|." }} }}'
    bstaff = f'{CH} \\new Staff \\with {{ instrumentName = "Bass" }} {{ \\clef "bass_8" \\key b \\minor \\compressMMRests {{ {EG.body(Bs, part_marks=fm)} \\bar "|." }} }}'
    dstaff = (f'\\new DrumStaff \\with {{ instrumentName = "Drums" }} << \\new DrumVoice {{ \\voiceOne \\drummode {{ {EG.body(D["up"][0], part_marks=fm)} \\bar "|." }} }} '
              f'\\new DrumVoice {{ \\voiceTwo \\drummode {{ {EG.body(D["down"][0], marks=False)} }} }} >>')
    vstaff = (f'\\new Staff = "vstaff" \\with {{ instrumentName = "Voice" \\override StaffSymbol.line-count = #3 \\override NoteHead.style = #\'cross '
              f'\\override Clef.stencil = ##f \\remove "Accidental_engraver" }} {{ \\compressMMRests {{ \\new Voice = "voc" {{ \\stemUp {EG.body(V)} \\bar "|." }} }} }} '
              f'\\new Lyrics \\lyricsto "voc" {{ {" ".join(VL)} }}')
    tuning = '\\markup \\small "Tuning (low to high): B E A D F♯ B. Sounding pitch, an octave above as written for guitar (treble 8vb). P.M.: palm-muted; > an open stroke."'
    src = HEAD + bookpart("Rhythm guitars 1 and 2 (the same riff, left and right; bars 1-8 guitar 1 alone)", gstaff).replace("\\score", tuning + "\n\\score", 1) + \
          bookpart("Lead guitar (the solo, bars 97-112; the last chorus, bars 137-144)", lstaff) + bookpart("Bass (five-string, low B; the guitar's root an octave below)", bstaff) + \
          bookpart("Drums", dstaff) + bookpart("Voice (harsh: no pitch)", vstaff)
    path, warns = compile_ly(src, "Swallowed Up - parts (band and voice)", cwd=OUT)
    print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:5], f"({len(warns)} total)")
    # readback, part by part
    def rb(name, bybar, mode=""):
        toks = [re.sub(r"(\\startTextSpan|\\stopTextSpan|_\\markup.*$|->|\^\\markup.*$)", "", t) for k in range(NB) for t in bybar[k] if t[0] not in "rR"]
        body = (f"\\drums {{ " if mode == "drum" else "\\new Staff { ") + "\\time 4/4 " + " ".join(toks) + " }"
        compile_ly('\\version "2.24.3"\n\\score { ' + body + ' \\midi { } }', f"check_{name}", cwd=OUT + "/check")
        return sorted(sum(midi_readback(f"{OUT}/check/check_{name}.midi"), []))
    want = lambda part: sorted(e["pitch"] for e in EV if e["part"] == part)
    for name, bb, part in (("gtr", G, "Gtr 1"), ("lead", L, "Lead"), ("bass", Bs, "Bass")):
        got = rb(name, bb); print(f"readback ({part}):", "matches" if got == want(part) else f"MISMATCH {len(got)} vs {len(want(part))}", len(got))
    got = sorted(rb("dup", D["up"][0], "drum") + rb("ddown", D["down"][0], "drum"))
    print("readback (drums):", "matches" if got == want("Drums") else f"MISMATCH {len(got)} vs {len(want('Drums'))}", len(got))
