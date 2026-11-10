"""The band parts for 'Sadie' (the production package, fix 79/8): DRUMS, BASS, RHYTHM GUITAR, LEAD GUITAR (the riff and the answers),
ACOUSTIC GUITAR, ORGAN and the GANG -- written bar by bar from the song record, the same events the demo plays. 4/4 at q = 124, A major;
rehearsal marks with each part's cues, bar numbers, chord symbols; empty bars compressed (one rest token a run, chord skips one token a run).
Guitars and the gang in treble 8vb, the bass in bass 8vb, at sounding pitch. LilyPond's MIDI read back per part; drum hits counted."""
import os, pickle, re, collections
SRC = open("/home/claude/p33/engrave_p33.py").read()
exec(SRC[:SRC.index("if __name__")])
CUE = {"drums": {"Intro": "tacet 4, then in", "Pre 1": "floor tom eighths, fill to the chorus", "Chorus 1": "four on the floor", "Bridge": "half time; rim 4 bars, then the kit",
                 "Drop": "one hit, then the heartbeat (lub-dub on 1 and 3)", "Chorus 4": "tambourine eighths; crash bars 73 and 77", "Outro": "out on the last bar"},
       "bass": {"Intro": "tacet 4", "Chorus 1": "root-fifth-octave eighths", "Bridge": "half notes", "Drop": "one hit, then tacet"},
       "rhy": {"Intro": "palm-muted from bar 5", "Pre 1": "open", "Bridge": "ring", "Drop": "one hit, then tacet"},
       "riff": {"Intro": "the riff: the title's notes", "Verse 1": "answer each line (as written: two or three notes, or none)", "Riff": "the riff",
                "Chorus 4": "double 'Sadie! Sadie!' an octave up", "Outro": "the riff"},
       "ac": {"Chorus 1": "strum eighths", "Drop": "tacet"}, "org": {"Pre 1": "pad", "Drop": "tacet"},
       "gang": {"Chorus 1": "Sadie! Sadie!", "Chorus 4": "the whole chorus, with the lead", "Outro": "two shouts"}}
NC_BI = [i for i, b in enumerate(BARS) if b.get("silence")]
def pbody(byb, kind):
    toks = []
    for bi in range(NB):
        if bi in starts:
            s = starts[bi][0]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\tempo 4 = 124"] + ([] if kind == "drums" else ["\\key a \\major"])
            c_ = CUE.get(kind, {}).get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + c_) if c_ else ""}"')
        bt = list(byb[bi])
        if bt == ["R1"] and toks and re.match(r"R1(\*\d+)?$", toks[-1]) and bi not in starts:
            n_ = int(toks[-1].split("*")[1]) if "*" in toks[-1] else 1
            toks[-1] = f"R1*{n_ + 1}"; continue
        toks += bt
    return " ".join(toks)
def chords_for(byb):
    rest = [all(t[0] in "rR" for t in byb[bi]) for bi in range(NB)]
    out, i = [], 0
    while i < NB:
        if rest[i]:
            j = i
            while j + 1 < NB and rest[j + 1] and (j + 1) not in starts: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        out.append(chord_tok(BARS[i]["chord"])); i += 1
    return " ".join(out)
DN = {36: "bd", 38: "sn", 37: "ss", 42: "hh", 46: "hho", 49: "cymc", 51: "cymr", 41: "tomfl", 54: "tamb"}
def drum_bars():
    by = collections.defaultdict(set)
    for e in REC["drums"]: by[e["on"]].add(e["p"][0])
    out = collections.defaultdict(list)
    for bi, b in enumerate(BARS):
        hits = [(e, by.get(b["start"] + e)) for e in range(8)]
        if not any(h for _, h in hits): out[bi] = ["R1"]; continue
        toks = []
        for e, h in hits:
            toks.append(("<" + " ".join(DN[p] for p in sorted(h)) + ">8") if h else "r8")
        out[bi] = toks
    return out
PITCHED = {"bass": REC["bass"], "rhy": REC["rhy"], "riff": REC["riff"], "ac": REC["ac"], "org": REC["organ"]}
BYB = {k: stream([dict(e) for e in v], texts=False)[0] for k, v in PITCHED.items()}
# the gang with its words (from the lead's syllables at the same onsets; the outro's shouts 'Sa-die! Sa-die!')
txt_at = {n["on"]: n for n in VO["voc"]}
G = [dict(e) for e in REC["gang"]]
sh = 0
for e in G:
    src_ = txt_at.get(e["on"])
    if src_: e["text"], e["hy"] = src_["text"], src_.get("hy", False)
    else:
        e["text"], e["hy"] = (["Sa", "die!"][sh % 2], sh % 2 == 0); sh += 1
GB, GL = stream(G, texts=True)
BYB["gang"] = GB
BYB["drums"] = drum_bars()
NOTES = {"drums": "Drums. Verses, intro (from bar 5), riff break and outro: kick 1, 3 and the and of 3, snare 2 and 4, closed hats in eighths. Pre-choruses: floor tom eighths, snare 2 and 4, a snare fill in the last bar. Choruses: four on the floor, snare 2 and 4, open hats on the off-beats, crash on bar 1; tambourine on the off-beats in choruses 2 and 3, eighths in chorus 4 (crash bars 73 and 77). Bridge: half time, rim clicks for four bars then the kit, a snare build in its last bar. The drop: bar 61 one hit (kick and crash) on beat 1, then only the heartbeat, lub-dub on beats 1 and 3, in bars 62-64. Last bar: one crash.",
         "bass": "Bass. Tacet for the riff's first four bars. Eighths on the root (verses, pre-choruses, riff break, outro); root-fifth-octave eighths in the choruses; half notes in the bridge. The drop: one hit on beat 1 of bar 61, then tacet to bar 65.",
         "rhy": "Rhythm guitar (distorted). Palm-muted power chords in eighths: intro from bar 5, verses, riff break. Open from the pre-chorus: a hit on beat 1, eighths after. Bridge: one ringing chord a bar. The drop: one hit, then tacet. Last bar: A, ring.",
         "riff": "Lead guitar (overdriven). THE RIFF: the title's own notes -- E, C-sharp, E (pushed onto the and of 2), C-sharp, A, B -- then the open-A chug with a lick, in the intro, the riff break and the outro. In the verses, answer each line as written (its last two or three notes an octave up, as the room allows; bar 13 has none). Chorus 4: double 'Sadie! Sadie!' an octave up, ring a chord tone in the other bars.",
         "ac": "Acoustic guitar (steel string). Strummed eighths from chorus 1: the choruses, the bridge, the outro. Tacet in the drop.",
         "org": "Organ (drawbar). A pad: one chord a bar in the pre-choruses, choruses and bridge. Tacet in the drop. Last bar: A.",
         "gang": "Gang (a crowd: unison and the octave below). 'Sadie! Sadie!' at the top of every chorus. The last chorus: all of it, with the lead. The outro: two 'Sadie! Sadie!' shouts (bars 83 and 87)."}
TITLES = {"drums": "Drums", "bass": "Bass", "rhy": "Rhythm guitar", "riff": "Lead guitar (the riff and the answers)", "ac": "Acoustic guitar", "org": "Organ", "gang": "Gang"}
CLEF = {"bass": "bass_8", "rhy": "treble_8", "riff": "treble_8", "ac": "treble_8", "org": "treble", "gang": "treble_8"}
def part(kind):
    music = pbody(BYB[kind], kind)
    if kind == "drums": staff = f'\\new DrumStaff \\drummode {{ \\compressMMRests {{ {music} \\bar "|." }} }}'
    elif kind == "gang":
        staff = (f'\\new Staff {{ \\clef "{CLEF[kind]}" \\compressMMRests {{ \\new Voice = "g" {{ {music} \\bar "|." }} }} }} '
                 f'\\new Lyrics \\lyricsto "g" {{ {" ".join(GL)} }}')
    else: staff = f'\\new Staff {{ \\clef "{CLEF[kind]}" \\compressMMRests {{ {music} \\bar "|." }} }}'
    return f"""\\bookpart {{
  \\header {{ title = "Sadie" subtitle = "{TITLES[kind]}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #1.2
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\markup \\vspace #0.8
  \\score {{
    << \\new ChordNames \\chordmode {{ {chords_for(BYB[kind])} }} {staff} >>
    \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }} }}
  }}
}}
"""
KINDS = ["drums", "bass", "rhy", "riff", "ac", "org", "gang"]
src = f"""\\version "2.24.3"
#(set-global-staff-size 18)
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #13 page-breaking = #ly:optimal-breaking max-systems-per-page = 7 }}
{"".join(part(k) for k in KINDS)}
"""
path, warns = compile_ly(src, "Sadie - parts (band and gang)", cwd=OUT)
print("compiled", path, [w for w in warns if "clashing" not in w][:6], f"({len(warns)} warnings)")
os.makedirs(OUT + "/check", exist_ok=True)
RB = {}
for k in ["bass", "rhy", "riff", "ac", "org", "gang"]:
    toks = [re.sub(r"\\\\[a-z<!]+", "", t.split("^")[0]) for bi in range(NB) for t in BYB[k][bi] if t[0] not in "rRs\\"]
    compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"pcheck_{k}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/pcheck_{k}.midi")[0]
    want = sorted(p for e in (REC["gang"] if k == "gang" else PITCHED[k]) for p in e["p"]); RB[k] = sorted(got) == want
    print(f"readback ({k}):", "matches" if RB[k] else f"MISMATCH ({len(got)} vs {len(want)})", len(got))
hits = sum(len(re.findall(r"\b(bd|sn|ss|hh|hho|cymc|cymr|tomfl|tamb)\b", " ".join(t for bi in range(NB) for t in BYB["drums"][bi]))) for _ in [0])
RB["drums"] = hits == len(REC["drums"])
print("drum hits:", hits, "(the demo's:", len(REC["drums"]), ")", "match" if RB["drums"] else "MISMATCH")
pickle.dump(dict(readback=RB), open(f"{OUT}/parts_report.pkl", "wb"))
