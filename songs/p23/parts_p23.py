"""The production parts pack for 'What Holds': four parts in one PDF -- RIFF GUITAR (every note of the intro, riff break and outro),
RHYTHM GUITAR, BASS and DRUMS -- each written out bar by bar from the same rules that play the demo (band_p23.py), without the demo's
humanizing, so the charts and the demo agree. Keys by section, rehearsal marks, bar numbers, chord symbols. Absolute pitch, sounding
(guitars and bass under 8vb clefs). Muted notes are staccato, pushed notes accented."""
import pickle, collections, os, sys
sys.path[:0] = ["/home/claude/carol", "/home/claude/p23"]
from lily import compile_ly, midi_readback
import band_p23 as BAND
REC = pickle.load(open("/home/claude/p23/song_record.pkl", "rb"))
OUT = "/home/claude/p23/out"
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_eighths"]
SP = {0: ("c", ""), 1: ("cis", ""), 2: ("d", ""), 3: ("dis", ""), 4: ("e", ""), 5: ("f", ""), 6: ("fis", ""), 7: ("g", ""), 8: ("gis", ""),
      9: ("a", ""), 10: ("ais", ""), 11: ("b", "")}
def pname(p):
    l, a = SP[p % 12]; o = p // 12 - 4
    return l + a + ("'" * o if o > 0 else "," * (-o))
BE, BD = BAND.events()
riff = [dict(on=n["on"], dur=n["dur"], p=[n["midi"]], art=("push" if n["src"].startswith("push") else "")) for n in REC["riff"]]
gtr = sorted([dict(e) for e in BE["gtr"]] + [dict(e, art="clean") for e in BE["cgtr"]], key=lambda e: e["on"])
bass = [dict(e) for e in BE["bass"]]
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
def split(b, pos, n):
    out = []
    while n > 0:
        if pos == 0 and n >= 8: L = 8
        elif pos == 0 and n >= 6: L = 6
        elif pos % 4 == 0 and n >= 4: L = 4
        elif pos % 4 == 0 and n >= 3: L = 3
        elif pos % 2 == 0 and n >= 2: L = 2
        else: L = 1
        out.append((pos, L)); pos += L; n -= L
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
KEYLY = {"E minor": "\\key e \\minor", "G major": "\\key g \\major"}
ART = {"mute": "-.", "push": "->", "": "", "ring": "", "clean": ""}
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
            sp = split(b, s - b["start"], m)
            for k, (pos, L) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = "r" + DUR[L]
                else:
                    ps = n["p"]; nm = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    tok = nm + DUR[L] + ("~" if tie else "") + (ART[n.get("art", "")] if first else "")
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, notes
DNAME = {"bd": "bd", "sn": "sn", "hh": "hh", "hho": "hho", "cymr": "cymr", "cymc": "cymc", "cymch": "cymch", "tomh": "tomh", "tommh": "tommh",
         "tomml": "tomml", "toml": "toml", "tomfl": "tomfl"}
def drumbar(bi):
    b = BARS[bi]; toks = []
    for e in range(b["len"]):
        s = BD.get(b["start"] + e)
        toks.append(("<" + " ".join(sorted(DNAME[x] for x in s)) + ">8") if s else "r8")
    return toks
SECTXT = {"gtr": {"Verse 1": "palm-muted", "Chorus 1": "open", "Verse 2": "palm-muted", "Chorus 2": "open", "Bridge": "build", "Chorus 3": "CLEAN, let ring",
                  "Chorus 4": "open, full", "Intro": "", "Riff": "", "Outro": ""},
          "bass": {"Verse 1": "muted", "Verse 2": "muted", "Chorus 3": "tacet", "Bridge": "build"},
          "drums": {"Chorus 3": "tacet until bar 60", "Bridge": "build"}, "riff": {}}
RESTB = {}
def body(bybar, kind):
    RESTB[kind] = set(); toks = []; last_key = None; bi = 0
    def has_(i):
        if kind == "drums": return any(BD.get(BARS[i]["start"] + e) for e in range(BARS[i]["len"]))
        return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        b = BARS[bi]
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\tempo 4 = 104"]
            if kind != "drums" and b["key"] != last_key: toks.append(KEYLY[b["key"]]); last_key = b["key"]
            txt = SECTXT[kind].get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + txt) if txt else ""}"')
        if not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not has_(bi + run): run += 1
            toks.append(f"R1*{run}")
            if run > 1: RESTB[kind].update(range(bi, bi + run))
            bi += run; continue
        toks += drumbar(bi) if kind == "drums" else bybar[bi]; bi += 1
    return " ".join(toks)
CHR = {"Em": "e", "C": "c", "D": "d", "G": "g", "Am": "a"}
QUAL = {"Em": ":m", "Am": ":m"}
def chords_for(kind):
    out, i, rb = [], 0, RESTB.get(kind, set())
    while i < NB:
        if i in rb:
            j = i
            while j + 1 < NB and (j + 1) in rb: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        out.append(f"{CHR[BARS[i]['chord']]}1{QUAL.get(BARS[i]['chord'], '')}"); i += 1
    return " ".join(out)
RB, RN = pitched(riff); GB, GN = pitched(gtr); BB, BN = pitched(bass)
MUS = dict(riff=body(RB, "riff"), gtr=body(GB, "gtr"), bass=body(BB, "bass"), drums=body(None, "drums"))
NOTES = {
 "riff": "Riff guitar (overdriven; sounds an octave below the written notes) -- intro, bars 25-28 and the outro. Bar 1 states the chorus's opening shape (a held E3, down to C3 and B2); every bar's first note is pushed an eighth early, on the 'and' of 4 (accented), and tied over. The last bar of the song is one low E, let ring.",
 "gtr": "Rhythm guitar (sounds an octave below the written notes) -- verses palm-muted root-fifth on 1, the 'and' of 2, 3 and 4 (staccato); choruses open power chords in eighths; riff and outro root-fifth eighths under the riff; bridge eighths building, full chords in the last two bars; chorus 3 CLEAN, one chord a bar, let ring. Every change pushed on the 'and' of 4 (accented) and tied over.",
 "bass": "Bass (sounds an octave below the written bass-clef notes) -- verses muted, locked with the guitar on 1, the 'and' of 2, 3 and 4; choruses, riff and outro straight eighths; bridge quarters, then eighths; tacet in chorus 3. Every change pushed on the 'and' of 4 (accented) and tied over.",
 "drums": "Drums -- verses: kick 1 and the 'and' of 2, snare 2 and 4, closed eighth hats. Choruses: kick 1, the 'and' of 2 and 3, snare 2 and 4, ride eighths, crash at the top. Riff and outro: open hats on the beats. Bridge: an eight-bar build (floor tom; backbeat; snare quarters; snare eighths). Chorus 3 tacet until a snare build in bar 60. Chorus 4: crash and china on bar 68 (STAND), crash on bar 69 (HOLDS), toms in bar 70. One crash on the last bar.",
}
def part(title, kind, music, clef):
    staff = "DrumStaff" if kind == "drums" else "Staff"; mode = "\\drummode" if kind == "drums" else ""
    cl = "" if kind == "drums" else f'\\clef "{clef}"'
    return f"""\\bookpart {{
  \\header {{ title = "What Holds" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #0.8
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\markup \\vspace #1.2
  \\score {{
    <<
      \\new ChordNames \\chordmode {{ {chords_for(kind)} }}
      \\new {staff} {{ {cl} \\compressMMRests {mode} {{ {music} \\bar "|." }} }}
    >>
    \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
               \\context {{ \\Staff \\consists "Merge_rests_engraver" }} }}
  }}
}}
"""
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #12 }}
{part("Riff guitar", "riff", MUS["riff"], "treble_8")}
{part("Rhythm guitar", "gtr", MUS["gtr"], "treble_8")}
{part("Bass", "bass", MUS["bass"], "bass_8")}
{part("Drums", "drums", MUS["drums"], "")}
"""
path, warns = compile_ly(src, "What Holds - parts (riff guitar, rhythm guitar, bass, drums)", cwd=OUT)
print("compiled", path, "warnings:", warns[:4], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
import re
for name, BYB, notes in (("riff", RB, RN), ("gtr", GB, GN), ("bass", BB, BN)):
    toks = [re.sub(r"(-\.|->)$", "", t) for bi in range(NB) for t in BYB.get(bi, []) if not t.startswith("r")]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_part_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_part_{name}.midi")[0]
    want = []
    for n in notes: want += sorted(n["p"])
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print("drum hits:", sum(len(v) for v in BD.values()), "(= the demo's drum events)")
