"""'They Did the Right Thing' (song 66) -- the full score: every part of the record on one set of systems, in one PDF. Written from the same
record and the same bar writer as the lead sheet and the parts (engrave66.py); resting staves are hidden system by system. Every pitched
staff is read back from LilyPond's MIDI; guitar slashes and drum hits are counted."""
import pickle, re, sys
sys.path[:0] = ["/home/claude/p76"]
import engrave66 as E
REC, P_ = E.REC, E.REC["parts"]
def nomarks(bd): return re.sub(r'\\tempo "Dark, steady" 4 = 72', "", re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", bd))
checks, ly = {}, {}
by, want = E.pitched([dict(e) for e in E.SLASH]); bd, _ = E.body(by, {}, multirest=False); checks["guitar"] = E.readback("score_guitar", by, want)
ly["guitar"] = f'\\new Staff \\with {{ instrumentName = "Guitar" shortInstrumentName = "Gtr." }} {{ \\clef "treble" \\improvisationOn {nomarks(bd)} }}'
by, want = E.pitched([dict(e) for e in P_["bass"]]); bd, _ = E.body(by, {}, multirest=False); checks["bass"] = E.readback("score_bass", by, want)
ly["bass"] = f'\\new Staff \\with {{ instrumentName = "Bass" shortInstrumentName = "Bass" }} {{ \\clef "bass_8" {nomarks(bd)} }}'
dstaff, nh = E.drums_staff(); nd = len({(e["on"], p) for e in P_["drums"] for p in e["p"]})
VB = {}
for who, by_ in (("him", E.HIM), ("harmony", E.HAR)):
    VB[who], _ = E.body(by_, {}, multirest=False)
    if who != "him": VB[who] = nomarks(VB[who])
CH = E.chords_for(set())
HEAD = r'''\version "2.24.3"
#(set-global-staff-size 13)
\paper { #(set-paper-size "letter") left-margin = 12\mm right-margin = 10\mm top-margin = 10\mm bottom-margin = 12\mm ragged-last-bottom = ##t
  system-separator-markup = \slashSeparator
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
  \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }
  \context { \DrumStaff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }
  \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
src = HEAD % (E.FOOT, E.FOOT) + f'''\\header {{ title = "{E.TITLE}" subtitle = "Full score ({E.REC['edition']})" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {CH} }}
  \\new ChoirStaff <<
    \\new Staff \\with {{ instrumentName = "Voice" shortInstrumentName = "Vox" }} {{ \\clef "treble_8" \\new Voice = "him" {{ {VB["him"]} }} }}
    \\new Lyrics \\lyricsto "him" {{ {" ".join(E.HIM_L)} }}
    \\new Staff \\with {{ instrumentName = "Harmony" shortInstrumentName = "Harm." }} {{ \\clef "treble_8" \\new Voice = "har" {{ {VB["harmony"]} }} }}
    \\new Lyrics \\lyricsto "har" {{ {" ".join(E.HAR_L)} }}
  >>
  \\new StaffGroup << {ly["guitar"]} {ly["bass"]} >>
  {dstaff}
>> \\layout {{ }} }}
'''
if __name__ == "__main__":
    path, warns = E.compile_ly(src, f"{E.FT} - full score", cwd=E.OUT)
    print("score:", warns[:6], len(warns))
    vok = {k: E.readback("score_" + k, b_, w_) for k, b_, w_ in (("him", E.HIM, E.HIM_W), ("harmony", E.HAR, E.HAR_W))}
    for k, v in vok.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=vok, parts=checks, drums=(nh, nd)), open(f"{E.OUT}/readback_score.pkl", "wb"))
