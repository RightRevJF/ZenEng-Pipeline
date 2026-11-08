"""The production parts pack for 'The Word Without a Word' (revision 1): PIANO (grand staff), CELLO and STRINGS (a reduction on one staff,
divisi as written) -- written bar by bar from the song record, the same events the demo plays and the full score shows. 3/4 at q = 66,
broadening to q = 56 for the last refrain; D-flat major, E-flat from verse 4. Rehearsal marks with each part's cues, bar numbers, chord
symbols; empty bars compressed. LilyPond's MIDI read back per part."""
import os, pickle
SRC = open("/home/claude/p29/score_p29.py").read()
exec(SRC[:SRC.index('footer = "Under')])
CUE = {"pno": {"Intro": "the cradle figure", "Verse 1": "left hand only, thinner", "Refrain 1": "right hand chords", "Verse 4": "both hands full",
               "Refrain 3": "thin under 'goes in, and out, and in'", "Coda": "alone: the refrain's first phrase, then ring the last chord"},
       "vc": {"Verse 2": "answer each line: its last three notes, an octave below", "Interlude": "her lullaby: refrain 1's tune, one note changed (WORLD on F)",
              "Verse 3": "answer each line; nothing moves under 'ma'", "Bridge": "held bass line", "Refrain 3": "out for the last two bars"},
       "str": {"Refrain 1": "a soft pad", "Interlude": "swell in the last two bars", "Bridge": "build", "Verse 4": "full", "Refrain 3": "full, a held top line; thin at the end"}}
ABBA_BI = next(i for i, b in enumerate(BARS) if b["start"] == REC["abba_bar"])
def pbody(byb, kind):
    toks = []
    for bi in range(NB):
        if bi in starts:
            s = starts[bi][0]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 3/4", "\\tempo 4 = 66", "\\key des \\major"]
            if s == "Verse 4": toks.append("\\key ees \\major")
            if s == "Refrain 3": toks.append('\\tempo "Broadening" 4 = 56')
            c_ = CUE[kind].get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + c_) if c_ else ""}"')
        bt = list(byb[bi])
        if bi == ABBA_BI and bt: bt[0] = bt[0] + '^\\markup \\italic \\small "Abba: everyone silent"'
        if bt == ["R2."] and toks and re.match(r"R2\.(\*\d+)?$", toks[-1]) and bi not in starts:   # one rest token for a run of empty bars
            n_ = int(toks[-1].split("*")[1]) if "*" in toks[-1] else 1
            toks[-1] = f"R2.*{n_ + 1}"; continue
        toks += bt
    return " ".join(toks)
def pmusic(bys, kind):
    if len(bys) == 1: return "\\compressMMRests { " + pbody(bys[0], kind) + ' \\bar "|." }'
    vs = ["\\voiceOne", "\\voiceTwo", "\\voiceThree", "\\voiceFour"]
    return "\\compressMMRests << " + " \\\\ ".join("{ " + vs[i] + " " + pbody(b, kind if i == 0 else "_none") + " }" for i, b in enumerate(bys)) + " >>"
CUE["_none"] = {}
_pb = pbody
def pbody(byb, kind):
    if kind == "_none":                                        # lower voices: no marks
        toks = []
        for bi in range(NB):
            if bi in starts:
                if bi == 0: toks += ["\\key des \\major"]
                if starts[bi][0] == "Verse 4": toks.append("\\key ees \\major")
            toks += byb[bi]
        return " ".join(toks)
    return _pb(byb, kind)
NOTES = {"pno": "Piano. The left hand's cradle figure (root, fifth, tenth, octave, tenth, fifth in eighths) throughout; verse 1 thinner. The right hand holds a chord on beat 1 from refrain 1; both hands full in verse 4 and the last refrain. Nothing moves under 'ma' (verse 3); the whole band is silent for the bridge's seventh bar ('Abba'). Coda, alone: the refrain's first phrase (C, C, C, B-flat, C, F), then E-flat and the last chord, E-flat with an added F, B-flat on top. Let it ring.",
         "vc": "Cello. From verse 2, the root a bar, held. In verses 2 and 3, answer each line: the singer's last three notes an octave below, in eighths, as she lands. Interlude: her lullaby, refrain 1's tune an octave below the voice at half voice, with one note changed: 'world' rises to F instead of D-flat. Nothing moves under 'ma'. From the bridge a held bass line; out for the last two bars of the last refrain.",
         "str": "Strings (a reduction: violins and violas divisi as written, the top line in the last refrain to the first violins). A soft pad under the refrains; the interlude's last two bars swell toward the bridge; the bridge builds; verse 4 and the last refrain full. Silent for the bridge's seventh bar ('Abba')."}
CHR_ = {"Db": "des", "Gb": "ges", "Ab": "aes", "Bbm": "bes", "Fm": "f", "Ebm": "ees", "Bb": "bes", "Eb": "ees", "Cm": "c", "Gm": "g", "F": "f"}
QUAL_ = {"Bbm": ":m", "Fm": ":m", "Ebm": ":m", "Cm": ":m", "Gm": ":m"}
def chords_for(bys):
    """the skill's lesson: chord names over a run of empty bars are one skip, or the rests will not compress"""
    rest = [all(all(t[0] in "rRs" for t in b[bi]) for b in bys) for bi in range(NB)]
    out, i = [], 0
    while i < NB:
        if rest[i]:
            j = i
            while j + 1 < NB and rest[j + 1] and (j + 1) not in starts: j += 1
            out.append(f"s2.*{j - i + 1}"); i = j + 1; continue
        c = BARS[i]["chord"]; out.append(f"{CHR_[c]}2.{QUAL_.get(c, '')}"); i += 1
    return " ".join(out)
def part(title, kind, staves, bys):
    return f"""\\bookpart {{
  \\header {{ title = "The Word Without a Word" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
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
path, warns = compile_ly(src, "The Word Without a Word - parts (piano, cello, strings)", cwd=OUT)
print("compiled", path, [w for w in warns if "clashing" not in w][:6], f"({len(warns)} warnings)")
os.makedirs(OUT + "/check", exist_ok=True)
RB = {}
for name, BYS, notes in (("piano RH", RHS, RH), ("piano LH", LHS, LH), ("cello", CS, REC["cello"]), ("strings", SS, REC["strings"])):
    got = []
    for k, byb in enumerate(BYS):
        toks = [t.split("^")[0] for bi in range(NB) for t in byb[bi] if t[0] not in "rRs\\"]
        compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 3/4 ' + " ".join(toks) + ' } \\midi { } }', f"pcheck_{name.replace(' ', '_')}_{k}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/pcheck_{name.replace(' ', '_')}_{k}.midi")[0]
    want = sorted(p for e in notes for p in e["p"]); RB[name] = sorted(got) == want
    print(f"readback ({name}):", "matches" if RB[name] else f"MISMATCH ({len(got)} vs {len(want)})", len(got))
pickle.dump(dict(readback=RB), open(f"{OUT}/parts_report.pkl", "wb"))
