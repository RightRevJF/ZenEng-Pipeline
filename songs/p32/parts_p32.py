"""The production parts pack for 'I Took Him for the Gardener': PIANO (grand staff), CELLO and STRINGS (a reduction on one staff, divisi
as written) -- written bar by bar from the song record, the same events the demo plays and the full score shows. 6/8 at dotted quarter
= 52, broadening for the last refrain; D minor, D major from MARY (bar 55). Rehearsal marks with each part's cues, bar numbers, chord
symbols; empty bars compressed. LilyPond's MIDI read back per part."""
import os, pickle
SRC = open("/home/claude/p32/score_p32.py").read()
exec(SRC[:SRC.index('footer = "Bar 54')])
CUE = {"pno": {"Intro": "the walking figure", "Verse 1": "left hand only, bare", "Refrain 1": "right-hand chords", "Verse 4": "both hands full",
               "Refrain 3": "thin in the last line", "Coda": "alone: the refrain's first phrase, then ring the last chord"},
       "vc": {"Verse 2": "answer each line: its last three notes, an octave below", "Interlude": "the refrain's first two lines, one note changed (DAWN on C-sharp)",
              "Verse 3": "answer each line", "The Name": "held", "Refrain 3": "out in bar 77"},
       "str": {"Refrain 1": "a soft pad", "Interlude": "swell", "The Name": "build softly; silent in bar 54", "Verse 4": "full",
               "Refrain 3": "full, a held top line; alone in bar 77"}, "_none": {}}
NC_BI = next(i for i, b in enumerate(BARS) if b["start"] == REC["nc_bar"])
MARY_BI_ = REC["mary"]["bar"] - 1
def pbody(byb, kind):
    toks = []
    for bi in range(NB):
        if kind == "_none":                                        # lower voices: no marks
            if bi == 0: toks.append("\\key d \\minor")
            if bi == MARY_BI_: toks.append("\\key d \\major")
            toks += byb[bi]; continue
        if bi in starts:
            s = starts[bi][0]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 6/8", "\\tempo 4. = 52", "\\key d \\minor"]
            if s == "Refrain 3": toks.append('\\tempo "Broadening" 4. = 48')
            if s == "Coda": toks.append('\\tempo "Slower" 4. = 44')
            c_ = CUE[kind].get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + c_) if c_ else ""}"')
        if bi == MARY_BI_: toks += ['\\bar "||"', "\\key d \\major"]
        bt = list(byb[bi])
        if bi == NC_BI and bt: bt[0] = bt[0] + '^\\markup \\italic \\small "everyone silent: the voice alone"'
        if bi == MARY_BI_ and bt and bt[0][0] not in "rRs": bt[0] = bt[0] + '^\\markup \\italic \\small "Mary: D major, softly"'
        if bt == ["R2."] and toks and re.match(r"R2\.(\*\d+)?$", toks[-1]) and bi not in starts and bi != MARY_BI_:   # one rest token for a run of empty bars
            n_ = int(toks[-1].split("*")[1]) if "*" in toks[-1] else 1
            toks[-1] = f"R2.*{n_ + 1}"; continue
        toks += bt
    return " ".join(toks)
def pmusic(bys, kind):
    if len(bys) == 1: return "\\compressMMRests { " + pbody(bys[0], kind) + ' \\bar "|." }'
    vs = ["\\voiceOne", "\\voiceTwo", "\\voiceThree", "\\voiceFour"]
    return "\\compressMMRests << " + " \\\\ ".join("{ " + vs[i] + " " + pbody(b, kind if i == 0 else "_none") + " }" for i, b in enumerate(bys)) + " >>"
NOTES = {"pno": "Piano. The left hand's walking figure (root, fifth, tenth | octave, tenth, fifth in eighths) throughout; verse 1 bare (root and fifth in dotted quarters). The right hand holds a chord on each downbeat from refrain 1; both hands full in verse 4 and the last refrain. Bar 54 ('said my name'): silent. Bar 55 ('Mary'): one soft D major chord a bar, no figure, through bar 56. Bar 77: silent (the strings alone). Coda, alone: the refrain's first phrase in D major (F-sharp, A, G, A, C-sharp, D), then D and the last chord, D with an added E, A on top. Let it ring.",
         "vc": "Cello. From verse 2, the root a bar, held. In verses 2 and 3, answer each line: the singer's last three notes an octave below, in eighths, as she lands. Interlude: the refrain's first two lines an octave below the voice, with one note changed: 'dawn' rises to C-sharp instead of A. Silent in bar 54; back on 'Mary'. Held bass from verse 4; out in bar 77.",
         "str": "Strings (a reduction: violins and violas divisi as written, the top line in the last refrain to the first violins). A soft pad under the refrains; the interlude swells; the Name builds softly under its first two lines; silent in bar 54; 'Mary' (bar 55) soft and full in D major; verse 4 and the last refrain full; in bar 77 the strings alone hold A."}
def chords_for(bys):
    """the skill's lesson: chord names over a run of empty bars are one skip, or the rests will not compress"""
    rest = [all(all(t[0] in "rRs" for t in b[bi]) for b in bys) for bi in range(NB)]
    out, i = [], 0
    while i < NB:
        if rest[i]:
            j = i
            while j + 1 < NB and rest[j + 1] and (j + 1) not in starts and (j + 1) != MARY_BI_: j += 1
            out.append(f"s2.*{j - i + 1}"); i = j + 1; continue
        out.append(chord_tok(BARS[i]["chord"])); i += 1
    return " ".join(out)
def part(title, kind, staves, bys):
    return f"""\\bookpart {{
  \\header {{ title = "I Took Him for the Gardener" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #1.4
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\markup \\vspace #1.0
  \\score {{
    <<
      \\new ChordNames \\chordmode {{ {chords_for(bys)} }}
      {staves}
    >>
    \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }} }}
  }}
}}
"""
src = f"""\\version "2.24.3"
#(set-global-staff-size 18)
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #13 page-breaking = #ly:optimal-breaking }}
{part("Piano", "pno", '\\new PianoStaff << \\new Staff { \\clef "treble" ' + pmusic(RHS, "pno") + ' } \\new Staff { \\clef "bass" ' + pmusic(LHS, "_none") + ' } >>', RHS + LHS)}
{part("Cello", "vc", '\\new Staff { \\clef "bass" ' + pmusic(CS, "vc") + ' }', CS)}
{part("Strings (reduction)", "str", '\\new Staff { \\clef "treble" ' + pmusic(SS, "str") + ' }', SS)}
"""
path, warns = compile_ly(src, "I Took Him for the Gardener - parts (piano, cello, strings)", cwd=OUT)
print("compiled", path, [w for w in warns if "clashing" not in w][:6], f"({len(warns)} warnings)")
os.makedirs(OUT + "/check", exist_ok=True)
RB = {}
for name, BYS, notes in (("piano RH", RHS, RH), ("piano LH", LHS, LH), ("cello", CS, REC["cello"]), ("strings", SS, REC["strings"])):
    got = []
    for k, byb in enumerate(BYS):
        toks = [re.sub(r"\\[a-z<!]+", "", t.split("^")[0]) for bi in range(NB) for t in byb[bi] if t[0] not in "rRs\\"]
        compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }', f"pcheck_{name.replace(' ', '_')}_{k}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/pcheck_{name.replace(' ', '_')}_{k}.midi")[0]
    want = sorted(p for e in notes for p in e["p"]); RB[name] = sorted(got) == want
    print(f"readback ({name}):", "matches" if RB[name] else f"MISMATCH ({len(got)} vs {len(want)})", len(got))
pickle.dump(dict(readback=RB), open(f"{OUT}/parts_report.pkl", "wb"))
