"""The full score of 'Through Its Breaking' from the song record: VOICE (with the lyric and chord names), PIANO (grand staff: the
right hand's chord and the bell's crack; the left hand's figure and the bell's toll), CELLO, STRINGS (a reduction on one staff).
Cello and strings staves are hidden where they rest for whole systems. Every staff is written from the same events the demo plays,
and LilyPond's MIDI is read back per staff. Section dynamics follow the demo's arc."""
import re, sys, collections
SRC = open("/home/claude/p26/engrave_p26.py").read()
exec(SRC[:SRC.index("assert min(vp)")])        # the lyric setting, pitch names, 6/8 splitting and the voice stream, shared with the lead sheet
VB, LYR = stream(VOC, "r", lyric=True)
def pack(evs, rank):
    """greedy voices: an event goes to the first voice free at its onset (the given rank first at a shared onset)"""
    voices = []
    for e in sorted(evs, key=lambda e: (e["on"], rank(e), -max(e["p"]))):
        for v in voices:
            if v[-1]["on"] + v[-1]["dur"] <= e["on"]: v.append(e); break
        else: voices.append([e])
    return voices
RH = [dict(e) for e in REC["pno"] if e["hand"] == "rh"] + [dict(e) for e in REC["bell"] if e["kind"] == "crack"]
LH = [dict(e) for e in REC["pno"] if e["hand"] == "lh"] + [dict(e) for e in REC["bell"] if e["kind"] == "toll"]
RHV = pack(RH, lambda e: 0 if e.get("kind") == "crack" else 1)
LHV = pack(LH, lambda e: 1 if e.get("kind") == "toll" else 0)
CEL = [dict(e) for e in REC["cello"]]; STR = [dict(e) for e in REC["strings"]]
DYN = {"Intro": "p", "Verse 1": "pp", "Chorus 1": "mp", "Interlude 1": "p", "Verse 2": "mp", "Chorus 2": "mf", "Interlude 2": "p",
       "Bridge": "p", "Chorus 3": "f", "Tag": "p", "Outro": "pp"}
def dyn(byb, marks):
    """a section's dynamic on its first token (and the bridge's crescendo to chorus 3)"""
    for s, nb, b0, met in REC["plan"]:
        if s not in marks: continue
        hit = next(((bi, j) for bi in range(b0, b0 + nb) for j, t in enumerate(byb[bi]) if t[0] not in "rs"), None)
        if hit is None: continue                                # the instrument rests through the section: no mark
        bi, j = hit; t = byb[bi][j]; d = "\\" + marks[s] + ("\\<" if s == "Bridge" else "")
        byb[bi][j] = t[:-1] + d + "~" if t.endswith("~") else t + d
    return byb
def streams(voices, first_rest="r"):
    return [dyn(stream(v, first_rest if i == 0 else "s")[0], DYN if i == 0 else {}) for i, v in enumerate(voices)]
RHS = streams(RHV); LHS = streams(LHV); CS = streams(pack(CEL, lambda e: 0)); SS = streams(pack(STR, lambda e: 0))
def staff_music(bys):
    if len(bys) == 1: return "{ " + body(bys[0], False) + " }"
    vs = ["\\voiceOne", "\\voiceTwo", "\\voiceThree"]
    return "<< " + " \\\\ ".join("{ " + vs[i] + " " + body(b, False) + " }" for i, b in enumerate(bys)) + " >>"
vp = [n["midi"] for n in VOC]
footer = "Piano: pedal with each chord; let the bell ring through its bar. The bell’s crack = the chord’s root with the half step below it, struck together."
footer2 = "Words and music: Jason Bryant"
src = f"""\\version "2.24.3"
\\header {{ title = "Through Its Breaking" subtitle = "Full score: voice, piano, cello, strings" composer = "Words and music: Jason Bryant" meter = "slow 6/8, felt in two" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 11\\mm bottom-margin = 20\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1 \\override LyricHyphen.minimum-distance = #1.0 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff \\with {{ instrumentName = "Voice" shortInstrumentName = "V." }} {{ \\clef "treble" \\new Voice = "voc" {{ {body(VB, True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(LYR)} }}
    \\new PianoStaff \\with {{ instrumentName = "Piano" shortInstrumentName = "Pno." }} <<
      \\new Staff = "rh" {{ \\clef "treble" {staff_music(RHS)} }}
      \\new Staff = "lh" {{ \\clef "bass" {staff_music(LHS)} }}
    >>
    \\new Staff \\with {{ instrumentName = "Cello" shortInstrumentName = "Vc." \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "bass" {staff_music(CS)} }}
    \\new Staff \\with {{ instrumentName = "Strings" shortInstrumentName = "Str." \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "treble" {staff_music(SS)} }}
  >>
}}
"""
path, warns = compile_ly(src, "Through Its Breaking - full score", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYS, notes in (("voice", [VB], VOC), ("piano RH", RHS, RH), ("piano LH", LHS, LH), ("cello", CS, CEL), ("strings", SS, STR)):
    got = []
    for k, BYB in enumerate(BYS):
        toks = [re.sub(r"\\\\[a-z<!]+", "", t) for bi in range(NB) for t in BYB[bi]]
        toks = [t for t in toks if t[0] not in "rs"]
        chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }'
        compile_ly(chk, f"check_{name.replace(' ', '_')}_{k}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/check_{name.replace(' ', '_')}_{k}.midi")[0]
    want = [p for n in notes for p in n["p"]]
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
