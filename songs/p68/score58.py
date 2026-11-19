"""'Same Time Tomorrow' (song 58) -- the full score: every part of the record on one set of systems, in one PDF. Written from the same
record and the same bar writer as the lead sheet and the parts (engrave58.py); resting staves are hidden system by system. Every pitched
staff is read back from LilyPond's MIDI, and the drums are counted against the record."""
import collections, pickle, re, sys
sys.path[:0] = ["/home/claude/p68"]
import engrave58 as E
REC, P_ = E.REC, E.REC["parts"]
def nomarks(bd): return re.sub(r'\\tempo "Gently" 4 = 84', "", re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", bd))
STAVES = [("guitar", "Acoustic guitar", "Gtr.", P_.get("guitar", []), '\\clef "treble_8"'),
          ("bass", "Bass", "Bass", P_.get("bass", []), '\\clef "bass_8"')]
checks, ly = {}, {}
for k, name, short, src, clef in STAVES:
    by, want = E.pitched([dict(e) for e in src]); bd, _ = E.body(by, {}, multirest=False)
    checks[k] = E.readback("score_" + k, by, want)
    ly[k] = f'\\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{short}" }} {{ {clef} {nomarks(bd)} }}'
VB = {}
for who, by_ in (("him", E.HIM), ("harmony", E.HAR)):
    VB[who], _ = E.body(by_, {}, multirest=False)
    if who != "him": VB[who] = nomarks(VB[who])
DN = {36: "bd", 38: "sn", 37: "ss", 42: "hh", 46: "hho", 49: "cymc", 51: "cymr", 48: "tomh", 45: "tommh", 41: "tomfl"}
HITS = collections.defaultdict(set)
for e in P_.get("drums", []):
    for p in e["p"]: HITS[e["on"]].add(DN[p])
def drumbar(bi):
    toks = []; st, L = E.BST[bi], E.BLEN[bi]; step = 12
    for b0 in range(0, L, step):
        base = st + b0; hs = [x for x in range(0, step, 3) if HITS.get(base + x)]
        if not hs: toks.append("r" + E.DUR[step]); continue
        if hs[0] > 0: toks.append("r" + E.DUR[hs[0]])
        for j, x in enumerate(hs):
            ln = (hs[j + 1] if j + 1 < len(hs) else step) - x
            toks.append("<" + " ".join(sorted(HITS[base + x])) + ">" + E.DUR[ln])
    return toks
dt = ["\\time 4/4"]
for bi in range(E.NB):
    if bi in E.starts and bi > 0: dt.append('\\bar "||"')
    dt += drumbar(bi)
dt.append('\\bar "|."')
nh = sum(len(v) for v in HITS.values()); nd = len({(e["on"], p) for e in P_.get("drums", []) for p in e["p"]})
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
  \\new DrumStaff \\with {{ instrumentName = "Drums" shortInstrumentName = "Dr." drumStyleTable = #drums-style }} \\drummode {{ {" ".join(dt)} }}
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
