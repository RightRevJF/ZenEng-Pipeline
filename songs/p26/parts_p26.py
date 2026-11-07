"""The production parts pack for 'Five-Oh-One': six parts in one PDF -- HORNS, GUITAR, ELECTRIC PIANO, BASS, DRUMS (with claps) and a
GANG cue sheet -- each written out bar by bar from the song record (the same events the demo plays, before any humanizing), so the parts
and the demo agree. 4/4 at q = 112, sixteenth grid; Eb major, F major from bar 65. Rehearsal marks, bar numbers, chord symbols; empty
bars compressed. Absolute pitch, sounding (guitar and bass under 8vb clefs); horns in concert pitch. Guitar ghosts as x-noteheads, stabs
staccato."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p26"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p26/song_record.pkl", "rb"))
OUT = "/home/claude/p26/out"
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_slots"]
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "16", 2: "8", 3: "8.", 4: "4", 6: "4.", 8: "2", 12: "2.", 16: "1"}
def split(pos, n):
    out = []
    while n > 0:
        if pos == 0 and n >= 16: L = 16
        elif pos == 0 and n >= 12: L = 12
        elif pos % 8 == 0 and n >= 8: L = 8
        elif pos % 8 == 0 and n >= 6: L = 6
        elif pos % 4 == 0 and n >= 4: L = 4
        elif pos % 4 in (0, 1) and n >= 3: L = 3
        elif pos % 2 == 0 and n >= 2: L = 2
        else: L = 1
        out.append((pos, L)); pos += L; n -= L
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
starts = {b0: s for s, nb, b0, met in REC["plan"]}
KEYLY = {"Eb major": "\\key ees \\major", "F major": "\\key f \\major"}
def pitched(notes):
    notes = sorted(notes, key=lambda n: n["on"]); cur = 0; seq = []
    for n in notes:
        assert n["on"] >= cur, n
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list)
    for kind, s, d, n in seq:
        first = True
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; m = min(d, b["start"] + b["len"] - s)
            sp = split(s - b["start"], m)
            for k, (pos, L) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = "r" + DUR[L]
                else:
                    ps = n["p"]; nm = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    art = n.get("art", "")
                    tok = ("\\xNote " if art == "ghost" else "") + nm + DUR[L] + ("~" if tie else "") + ("-." if (first and art == "stab") else "")
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, notes
DN = {36: "bd", 38: "sn", 42: "hh", 46: "hho", 49: "cymc", 39: "hc", 45: "tomml"}
HITS = collections.defaultdict(set)
for e in REC["drums"] + REC["claps"]:
    for p in e["p"]: HITS[e["on"]].add(DN[p])
def drumbar(bi):
    b = BARS[bi]; toks = []
    for beat in range(4):
        base = b["start"] + beat * 4
        hs = [e for e in range(4) if HITS.get(base + e)]
        if not hs: toks.append("r4"); continue
        if hs[0] > 0: toks.append("r" + DUR[hs[0]])
        for j, e in enumerate(hs):
            ln = (hs[j + 1] if j + 1 < len(hs) else 4) - e
            toks.append("<" + " ".join(sorted(HITS[base + e])) + ">" + DUR[ln])
    return toks
SECTXT = {
 "hrn": {"Intro": "the chant", "Chorus 1": "stabs", "Hook 1": "the chant, with the voice", "Chorus 3": "stabs and hold", "Hook 3": "the chant", "Outro": "the chant", "Ending": "HIT"},
 "gtr": {"Intro": "scratch", "Verse 1": "stabs; ghosts from bar 7", "Breakdown": "tacet", "Lift": "let ring", "Ending": "HIT"},
 "key": {"Pre 1": "hold", "Chorus 1": "hold", "Breakdown": "tacet"},
 "bas": {"Intro": "in at bar 3", "Verse 1": "light", "Breakdown": "busy", "Lift": "eighths over C", "Ending": "HIT"},
 "drm": {"Intro": "in at bar 3", "Verse 1": "8th hats", "Pre 1": "fill in bar 16", "Chorus 1": "crash; 16th hats", "Hook 1": "claps 2 and 4",
         "Breakdown": "kit out: kick on 1; claps answer CLAP", "Lift": "snare build", "Chorus 3": "harder: open hats, crash every 2", "Ending": "HIT"}}
RESTB = {}
def body(bybar, kind):
    RESTB[kind] = set(); toks = []; last_key = None; bi = 0
    def has_(i):
        if kind == "drm": return any(HITS.get(BARS[i]["start"] + e) for e in range(16))
        return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        b = BARS[bi]
        if bi in starts:
            s = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\tempo 4 = 112"]
            if kind != "drm" and b["key"] != last_key: toks.append(KEYLY[b["key"]]); last_key = b["key"]
            txt = SECTXT.get(kind, {}).get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + txt) if txt else ""}"')
        if not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not has_(bi + run): run += 1
            toks.append(f"R1*{run}")
            RESTB[kind].update(range(bi, bi + run))
            bi += run; continue
        toks += drumbar(bi) if kind == "drm" else bybar[bi]; bi += 1
    return " ".join(toks)
CHR = {"Eb": "ees", "Ab": "aes", "Bb": "bes", "Cm": "c", "Gm": "g", "C": "c", "F": "f", "Dm": "d"}
QUAL = {"Cm": ":m", "Gm": ":m", "Dm": ":m"}
def chords_for(kind):
    out, i, rb = [], 0, RESTB.get(kind, set())
    while i < NB:
        if i in rb:
            j = i
            while j + 1 < NB and (j + 1) in rb and (j + 1) not in starts: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        out.append(f"{CHR[BARS[i]['chord']]}1{QUAL.get(BARS[i]['chord'], '')}"); i += 1
    return " ".join(out)
PARTS = {k: pitched([dict(e) for e in REC[src]]) for k, src in (("hrn", "horns"), ("gtr", "gtr"), ("key", "keys"), ("bas", "bass"))}
MUS = {k: body(PARTS[k][0], k) for k in PARTS}; MUS["drm"] = body(None, "drm")
# the gang cue sheet: its lines, bar by bar
gang_rows = []
for sec in ("Hook 1", "Hook 2", "Hook 3"):
    b0 = next(i for i, b in enumerate(BARS) if b["sec"] == sec)
    gang_rows.append(f"Bar {b0 + 2} and bar {b0 + 4} ({sec}), on the 'and' of beat 3: HEY! then GO!")
lift = [n for n in REC["lead"] if n["singer"] == "gang"]
gang_rows.append(f"Bar {bar_at[lift[0]['on']] + 1} (Lift), beats 1, 2, 3: FIVE (E4) - OH (E4) - ONE (G4, hold), over C")
for sec in ("Chorus 3", "Chorus 4"):
    b0 = next(i for i, b in enumerate(BARS) if b["sec"] == sec)
    gang_rows.append(f"Bars {b0 + 1}, {b0 + 3}, {b0 + 7} ({sec}): shout FIVE-oh-ONE with the lead (C4-F4-A4, beat 1, the 'a' of 1, beat 2)")
NOTES = {
 "hrn": "Horns (trumpet, alto or tenor sax, trombone), written in CONCERT pitch: transpose for B-flat and E-flat instruments. The intro, hooks and outro play the chant -- FIVE-oh FIVE-oh FIVE-oh-ONE, a 3+3+2 tresillo -- in unison an octave above the voice. Choruses: a short stab on 1 and the 'and' of 2 (top line to the trumpet); choruses 3 and 4 also hold the chord on beats 3-4. One hit on F at bar 87.",
 "gtr": "Guitar (sounds an octave below the written notes). The sixteenth 'chicken scratch': x-noteheads are muted ghost strokes on every sixteenth; the chord's top three notes are stabbed (staccato) on each 'and'. Verse 1 plays only the stabs until bar 7. Tacet in the breakdown and the last two bars of the lift; let the chord ring in bars 61-62. One hit on F at bar 87.",
 "key": "Electric piano. Hold the chord through each bar in the pre-choruses, choruses, hooks, lift and outro; lay out in the intro, verses and breakdown. Final chord at bar 87, held three beats.",
 "bas": "Bass (slap or fingers; sounds an octave below the written bass-clef notes). The groove: root on 1, again on the 'a' of 1, octave on the 'and' of 2, root on 3, fifth and octave pops, a chromatic approach into the next bar. Verses lighter; the breakdown busiest; eighths over C in bars 63-64. In at bar 3. One hit (F, octave) at bar 87.",
 "drm": "Drums and claps (hc = handclaps). Groove: kick 1, the 'a' of 2 and 3; snare 2 and 4; sixteenth hats, open on the 'and' of 4. Verses: kick 1 and 3, eighth hats. Pre-choruses: eighth hats, snare-and-tom fill in the last bar. Breakdown: kick on 1 only; claps answer each CLAP (three). Lift: hats, then a sixteenth snare build over bars 63-64. Choruses 3-4: open hats on every 'and', crash every two bars. In at bar 3. One hit at bar 87.",
}
def part(title, kind, music, clef):
    staff = "DrumStaff" if kind == "drm" else "Staff"; mode = "\\drummode" if kind == "drm" else ""
    cl = "" if kind == "drm" else f'\\clef "{clef}"'
    return f"""\\bookpart {{
  \\header {{ title = "Five-Oh-One" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #0.6
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\markup \\vspace #1.0
  \\score {{
    <<
      \\new ChordNames \\chordmode {{ {chords_for(kind)} }}
      \\new {staff} {{ {cl} \\compressMMRests {mode} {{ {music} \\bar "|." }} }}
    >>
    \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }} }}
  }}
}}
"""
gang_md = " ".join(f"\\line {{ \\small \"{r}\" }}" for r in gang_rows)
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #12 }}
{part("Horns (concert pitch)", "hrn", MUS["hrn"], "treble")}
{part("Guitar", "gtr", MUS["gtr"], "treble_8")}
{part("Electric piano", "key", MUS["key"], "treble")}
{part("Bass", "bas", MUS["bas"], "bass_8")}
{part("Drums and claps", "drm", MUS["drm"], "")}
\\bookpart {{
  \\header {{ title = "Five-Oh-One" subtitle = "Gang vocals and claps: cue sheet" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #1
  \\markup \\column {{ \\line {{ \\bold "The gang (everyone not singing lead): shouted, not sung pretty; any comfortable octave." }} \\vspace #0.5 {gang_md}
    \\vspace #0.5 \\line {{ \\small "Claps: on 2 and 4 in the hooks (bars 25-28, 49-52, 81-84), choruses 3-4 (bars 65-80) and the outro;" }}
    \\line {{ \\small "in the breakdown, three claps (sixteenth-eighth apart) after every CLAP the singer calls: bars 54, 56, 58, 60." }} }}
}}
"""
path, warns = compile_ly(src, "Five-Oh-One - parts (horns, guitar, keys, bass, drums, gang)", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:4], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for k in ("hrn", "gtr", "key", "bas"):
    BYB, notes = PARTS[k]
    toks = [re.sub(r"-\.$", "", t.replace("\\xNote ", "")) for bi in range(NB) for t in BYB.get(bi, []) if not t.startswith("r")]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_part_{k}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_part_{k}.midi")[0]
    want = [p for n in notes for p in n["p"]]
    print(f"readback ({k}):", "matches" if sorted(got) == sorted(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print("drum and clap hits written:", sum(len(v) for v in HITS.values()), "of", sum(len(e["p"]) for e in REC["drums"] + REC["claps"]))
