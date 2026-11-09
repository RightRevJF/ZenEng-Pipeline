"""The full score of 'I Took Him for the Gardener' from the song record (keyboard-led: always): VOICE (soprano, with the lyric and chord
names), PIANO (grand staff: the right hand's chords, the left hand's walking figure), CELLO (the answers, the interlude, the held bass;
hidden where it rests for whole systems), STRINGS (a reduction on one staff, hidden where they rest). Every staff is written from the same events the demo plays,
and LilyPond's MIDI is read back per staff. Section dynamics follow the demo's arc."""
import re, sys, collections
SRC = open("/home/claude/p32/engrave_p32.py").read()
exec(SRC[:SRC.index("NM = ([")])          # the lyric setting, pitch names, 6/8 splitting and the voice streams, shared with the lead sheet
def pack(evs):
    """greedy voices: an event goes to the first voice free at its onset"""
    voices = []
    for e in sorted(evs, key=lambda e: (e["on"], -max(e["p"]))):
        for v in voices:
            if v[-1]["on"] + v[-1]["dur"] <= e["on"]: v.append(e); break
        else: voices.append([e])
    return voices
def istream(notes, rest="r", drum=False):
    notes = sorted(notes, key=lambda n: n["on"]); cur = 0; seq = []
    for n in notes:
        assert n["on"] >= cur, ("overlap", n)
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list)
    for kind, s, d, n in seq:
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; m = min(d, b["start"] + b["len"] - s)
            sp = split(s - b["start"], m)
            for k, (pos, Lh) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = (("R2." if rest == "r" else "s2.") if Lh == 6 else rest + DUR[Lh])
                else:
                    ps = n["p"]
                    if drum: nm_ = "<" + " ".join(DN[p] for p in ps) + ">" if len(ps) > 1 else DN[ps[0]]
                    else: nm_ = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in sorted(ps)) + ">"
                    tok = nm_ + DUR[Lh] + ("~" if tie and not drum else "")
                    if drum and tie: tok = nm_ + DUR[Lh]; n = None; kind = "r"           # a drum hit sounds once
                bybar[bi].append(tok)
            s += m; d -= m
    return bybar
DN = {}
DYN = {"Intro": "p", "Verse 1": "pp", "Refrain 1": "mp", "Verse 2": "p", "Refrain 2": "mf", "Interlude": "mp", "Verse 3": "p", "The Name": "p",
       "Verse 4": "f", "Refrain 3": "f", "Coda": "p"}
def dyn(byb):
    for s, nb, b0, met in REC["plan"]:
        hit = next(((bi, j) for bi in range(b0, b0 + nb) for j, t in enumerate(byb[bi]) if t[0] not in "rsR"), None)
        if hit is None: continue
        bi, j = hit; t = byb[bi][j]; d = "\\" + DYN[s]
        byb[bi][j] = t[:-1] + d + "~" if t.endswith("~") else t + d
    return byb
def streams(voices, drum=False):
    return [dyn(istream(v, "r" if i == 0 else "s", drum)) if i == 0 else istream(v, "s", drum) for i, v in enumerate(voices)]
PN = [dict(e) for e in REC["pno"]]
RH = [dict(e) for e in PN if e["hand"] == "rh"] + [dict(e, p=[p for p in e["p"] if p >= 60]) for e in PN if e["hand"] == "both" and any(p >= 60 for p in e["p"])]
LH = [dict(e) for e in PN if e["hand"] == "lh"] + [dict(e, p=[p for p in e["p"] if p < 60]) for e in PN if e["hand"] == "both" and any(p < 60 for p in e["p"])]   # by hand, not by pitch
RHS = streams(pack(RH)); LHS = streams(pack(LH)); CS = streams(pack([dict(e) for e in REC["cello"]])); SS = streams(pack([dict(e) for e in REC["strings"]]))
def ibody(byb, drum=False):
    toks = []
    for bi in range(NB):
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 6/8", f"\\key {KEYS[0]} \\minor"]
        if bi == MARY_BI: toks += ['\\bar "||"', f"\\key {KEYS[0]} \\major"]
        toks += byb[bi]
    return " ".join(toks)
def staff_music(bys, drum=False):
    if len(bys) == 1: return "{ " + ibody(bys[0], drum) + " }"
    vs = ["\\voiceOne", "\\voiceTwo", "\\voiceThree", "\\voiceFour"]
    return "<< " + " \\\\ ".join("{ " + vs[i] + " " + ibody(b, drum) + " }" for i, b in enumerate(bys)) + " >>"
footer = "Bar 54 (“said my name”): the whole band silent, the voice alone · bar 55 (“Mary”): everyone back on D major, softly · bar 77: only the strings hold"
footer2 = "Words and music: Jason Bryant · two co-equal editions: soprano as written, mezzo a minor third lower · F♯5 ossia on “earth”"
src = f"""\\version "2.24.3"
#(set-global-staff-size 16)
\\header {{ title = "I Took Him for the Gardener" subtitle = "Full score: voice, piano, cello, strings" composer = "Words and music: Jason Bryant" meter = "an Easter solo, 6/8" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 12\\mm right-margin = 12\\mm top-margin = 11\\mm bottom-margin = 20\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1.2 \\override LyricHyphen.minimum-distance = #0.6 }}
  \\context {{ \\Staff \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff = "vstaff" \\with {{ instrumentName = "Voice" shortInstrumentName = "V." \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble" \\new Voice = "voc" {{ {body(VB["voc"][0], True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(VB["voc"][1])} }}
    \\new PianoStaff \\with {{ instrumentName = "Piano" shortInstrumentName = "Pno." }} <<
      \\new Staff = "rh" \\with {{ \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble" {staff_music(RHS)} }}
      \\new Staff = "lh" \\with {{ \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "bass" {staff_music(LHS)} }}
    >>
    \\new Staff \\with {{ instrumentName = "Cello" shortInstrumentName = "Vc." }} {{ \\clef "bass" {staff_music(CS)} }}
    \\new Staff \\with {{ instrumentName = "Strings" shortInstrumentName = "Str." }} {{ \\clef "treble" {staff_music(SS)} }}
  >>
}}
"""
path, warns = compile_ly(src, "I Took Him for the Gardener - full score", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYS, notes in (("voice", [VB["voc"][0]], VO["voc"]), ("piano RH", RHS, RH), ("piano LH", LHS, LH), ("cello", CS, REC["cello"]), ("strings", SS, REC["strings"])):
    got = []
    for k, BYB in enumerate(BYS):
        toks = [re.sub(r"\\\\[a-z<!]+", "", t) for bi in range(NB) for t in BYB[bi]]
        toks = [t for t in toks if t[0] not in "rsR"]
        chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }'
        compile_ly(chk, f"check_{name.replace(' ', '_')}_{k}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/check_{name.replace(' ', '_')}_{k}.midi")[0]
    want = [p for n in notes for p in n["p"]]
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
