"""'The Room Next Door' (song 52) -- the full score: every part of the record on one set of systems, in one PDF. Written from the same record
and the same bar writer as the lead sheet and the parts (engrave_p62.py); resting staves are hidden system by system. Every pitched staff
is read back from LilyPond's MIDI, and the drums are counted against the record."""
import collections, pickle, re, sys
sys.path[:0] = ["/home/claude/p62"]
import engrave_p62 as E
REC, P_ = E.REC, E.REC["parts"]
def nomarks(bd): return re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", bd)
STAVES = [("harm_hi", "Harmony (high)", "Harm. hi", [dict(n, p=[n["midi"]]) for n in REC["harm_hi"]], ''),
          ("harm_lo", "Harmony (low)", "Harm. lo", [dict(n, p=[n["midi"]]) for n in REC["harm_lo"]], ''),
          ("guitar", "Acoustic guitar", "A. Gtr.", P_.get("guitar", []), '\\clef "treble_8"'),
          ("piano", "Piano", "Pno.", P_.get("piano", []), ""),
          ("cello", "Cello", "Vc.", P_.get("cello", []), "\\clef bass"),
          ("bass", "Acoustic bass", "Bass", P_.get("bass", []), "\\clef bass")]
checks, ly = {}, {}
for k, name, short, src, clef in STAVES:
    by, want = E.pitched([dict(e) for e in src]); bd, _ = E.body(by, {}, multirest=False)
    checks[k] = E.readback("score_" + k, by, want)
    ly[k] = f'\\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{short}" }} {{ {clef} {nomarks(bd)} }}'
# the voice carries the section marks; written bar by bar like the others so every staff lines up
VB, _ = E.body(E.VOX, {}, multirest=False)
nh = nd = 0
# chord names over every bar (no multirests in a full score)
CH = E.chords_for(set())
HEAD = r'''\version "2.24.3"
#(set-global-staff-size 13)
\paper { #(set-paper-size "letter") left-margin = 12\mm right-margin = 10\mm top-margin = 10\mm bottom-margin = 12\mm ragged-last-bottom = ##t
  system-separator-markup = \slashSeparator
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
chExceptionMusic = { <c e g d'>1-\markup { \super "add9" } }
chExceptions = #(append (sequential-music-to-chord-exceptions chExceptionMusic #t) ignatzekExceptions)
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) }
  \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }
  \context { \DrumStaff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t }
  \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
src = HEAD % (E.FOOT, E.FOOT) + f'''\\header {{ title = "{E.TITLE}" subtitle = "Full score · third edition" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {CH} }}
  \\new ChoirStaff <<
    \\new Staff \\with {{ instrumentName = "Voice" shortInstrumentName = "Vox" }} {{ \\clef "treble" \\new Voice = "v" {{ {VB} }} }}
    \\new Lyrics \\lyricsto "v" {{ {" ".join(E.LYR)} }}
    {ly["harm_hi"]}
    {ly["harm_lo"]}
  >>
  \\new StaffGroup << {ly["guitar"]} {ly["piano"]} {ly["cello"]} {ly["bass"]} >>
>> \\layout {{ }} }}
'''
if __name__ == "__main__":
    path, warns = E.compile_ly(src, f"{E.FT} - full score", cwd=E.OUT)
    print("score:", warns[:6], len(warns))
    vok = E.readback("score_voice", E.VOX, E.VWANT); print("  readback voice:", "matches" if vok[0] else "MISMATCH", vok[1:])
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print("  drums: none in this song")
    pickle.dump(dict(voice=vok, parts=checks, drums=(nh, nd)), open(f"{E.OUT}/readback_score.pkl", "wb"))
