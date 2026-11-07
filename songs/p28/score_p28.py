"""The full score of 'Tinted Glass' from the song record (a keyboard-led song: the score is always made): HER and HIM (each with the
lyric; a staff hides where its singer rests), ELECTRIC PIANO (grand staff: the right hand's chords and answers, the left hand's chord),
BASS, ORGAN (hidden where it rests for whole systems), DRUMS (brushes). Every staff is written from the same events the demo plays, and
LilyPond's MIDI is read back per staff (drum hits counted). Section dynamics follow the demo's arc."""
import re, sys, collections
SRC = open("/home/claude/p28/engrave_p28.py").read()
exec(SRC[:SRC.index("NM = ['C'")])          # the lyric setting, pitch names, 6/8 splitting and the voice streams, shared with the lead sheet
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
DN = {36: "bd", 38: "sn", 37: "ss", 42: "hh", 51: "cymr", 49: "cymc"}
DYN = {"Intro": "p", "Verse 1": "p", "Verse 2": "mp", "Chorus 1": "mf", "Verse 3": "mp", "Verse 4": "mp", "Chorus 2": "mf", "Bridge": "p",
       "Verse 5": "p", "Verse 6": "p", "Chorus 3": "f", "Chorus 4": "f", "Outro": "pp"}
def dyn(byb):
    for s, nb, b0, met in REC["plan"]:
        hit = next(((bi, j) for bi in range(b0, b0 + nb) for j, t in enumerate(byb[bi]) if t[0] not in "rsR"), None)
        if hit is None: continue
        bi, j = hit; t = byb[bi][j]; d = "\\" + DYN[s]
        byb[bi][j] = t[:-1] + d + "~" if t.endswith("~") else t + d
    return byb
def streams(voices, drum=False):
    return [dyn(istream(v, "r" if i == 0 else "s", drum)) if i == 0 else istream(v, "s", drum) for i, v in enumerate(voices)]
KEYS = [dict(e) for e in REC["keys"]]
RH = [dict(e, p=[p for p in e["p"] if p >= 60]) for e in KEYS if any(p >= 60 for p in e["p"])]
LH = [dict(e, p=[p for p in e["p"] if p < 60]) for e in KEYS if any(p < 60 for p in e["p"])]
RHS = streams(pack(RH)); LHS = streams(pack(LH)); BS = streams(pack([dict(e) for e in REC["bass"]]))
OS = streams(pack([dict(e) for e in REC["organ"]])); DS = streams(pack([dict(e) for e in REC["drums"]]), drum=True)
def ibody(byb, drum=False):
    toks = []
    for bi in range(NB):
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 6/8"] + ([] if drum else ["\\key ees \\major"])
        toks += byb[bi]
    return " ".join(toks)
def staff_music(bys, drum=False):
    if len(bys) == 1: return "{ " + ibody(bys[0], drum) + " }"
    vs = ["\\voiceOne", "\\voiceTwo", "\\voiceThree", "\\voiceFour"]
    return "<< " + " \\\\ ".join("{ " + vs[i] + " " + ibody(b, drum) + " }" for i, b in enumerate(bys)) + " >>"
footer = "Electric piano: in each four-bar verse or bridge line the voice is done by bar 3; bar 4 is the piano’s answer. Drums with brushes throughout."
footer2 = "Words and music: Jason Bryant · Him written in treble 8vb, sounding an octave lower · the singers never overlap"
src = f"""\\version "2.24.3"
#(set-global-staff-size 16)
\\header {{ title = "Tinted Glass" subtitle = "Full score: her, him, electric piano, bass, organ, drums" composer = "Words and music: Jason Bryant" meter = "slow-burn soul, 6/8 felt in two" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 12\\mm right-margin = 12\\mm top-margin = 11\\mm bottom-margin = 20\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1.5 \\override LyricHyphen.minimum-distance = #0.6 }}
  \\context {{ \\Staff \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }}
  \\context {{ \\DrumStaff \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff = "her" \\with {{ instrumentName = "Her" shortInstrumentName = "Her" }} {{ \\clef "treble" \\new Voice = "her" {{ {body(VB["her"][0], True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "her" {{ {" ".join(VB["her"][1])} }}
    \\new Staff = "him" \\with {{ instrumentName = "Him" shortInstrumentName = "Him" }} {{ \\clef "treble_8" \\new Voice = "him" {{ {body(VB["him"][0], False)} }} }}
    \\new Lyrics \\lyricsto "him" {{ {" ".join(VB["him"][1])} }}
    \\new PianoStaff \\with {{ instrumentName = "Electric piano" shortInstrumentName = "E.P." }} <<
      \\new Staff = "rh" \\with {{ \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble" {staff_music(RHS)} }}
      \\new Staff = "lh" \\with {{ \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "bass" {staff_music(LHS)} }}
    >>
    \\new Staff \\with {{ instrumentName = "Bass" shortInstrumentName = "Bs." }} {{ \\clef "bass_8" {staff_music(BS)} }}
    \\new Staff \\with {{ instrumentName = "Organ" shortInstrumentName = "Org." }} {{ \\clef "treble" {staff_music(OS)} }}
    \\new DrumStaff \\with {{ instrumentName = "Drums" shortInstrumentName = "Dr." }} \\drummode {{ {staff_music(DS, True)} }}
  >>
}}
"""
path, warns = compile_ly(src, "Tinted Glass - full score", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYS, notes in (("her", [VB["her"][0]], VO["her"]), ("him", [VB["him"][0]], VO["him"]), ("ep RH", RHS, RH), ("ep LH", LHS, LH),
                         ("bass", BS, REC["bass"]), ("organ", OS, REC["organ"])):
    got = []
    for k, BYB in enumerate(BYS):
        toks = [re.sub(r"\\\\[a-z<!]+", "", t) for bi in range(NB) for t in BYB[bi]]
        toks = [t for t in toks if t[0] not in "rsR"]
        chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }'
        compile_ly(chk, f"check_{name.replace(' ', '_')}_{k}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/check_{name.replace(' ', '_')}_{k}.midi")[0]
    want = [p for n in notes for p in n["p"]]
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
hits = sum(len(re.findall(r"(?<![a-z])(bd|sn|ss|hh|cymr|cymc)(?![a-z])", t)) for b in DS for bi in range(NB) for t in b[bi])
print("drum hits written:", hits, "of", sum(len(e["p"]) for e in REC["drums"]))
