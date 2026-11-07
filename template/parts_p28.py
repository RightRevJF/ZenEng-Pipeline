"""The production parts pack for 'Either Or': five parts in one PDF -- GUITAR 1, GUITAR 2, BASS, ORGAN and DRUMS -- each written out bar by
bar from the song record (the same events the demo plays, before any humanizing), so the parts and the demo agree. Verses, intro, break
and build in 5/4 (beamed 3+2), refrains and outro in 4/4, q = 132; D Dorian (no key signature) and F major. Rehearsal marks, bar numbers,
chord symbols (N.C. where the band stops); empty bars compressed. Absolute pitch, sounding (guitars and bass under 8vb clefs)."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p28"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p28/song_record.pkl", "rb"))
OUT = "/home/claude/p28/out"
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_eighths"]
SP = {0: "c", 1: "cis", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
def split(pos, n, blen=8):
    out = []
    while n > 0:
        if blen == 10:
            end = 6 if pos < 6 else 10
            room = min(n, end - pos)
            if pos == 0 and room >= 6: L = 6
            elif pos % 2 == 0 and room >= 4 and pos in (0, 2, 6): L = 4
            elif pos % 2 == 0 and room >= 3: L = 3
            elif pos % 2 == 0 and room >= 2: L = 2
            else: L = 1
        else:
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
starts = {b0: s for s, nb, b0, met in REC["plan"]}
MET = {b0: met for s, nb, b0, met in REC["plan"]}
KEYLY = {"D Dorian": "\\key d \\dorian", "F major": "\\key f \\major"}
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
            sp = split(s - b["start"], m, b["len"])
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
DN = {36: "bd", 38: "sn", 42: "hh", 46: "hho", 49: "cymc", 51: "cymr", 45: "tomml", 41: "tomfl"}
HITS = collections.defaultdict(set)
for e in REC["drums"]:
    for p in e["p"]: HITS[e["on"]].add(DN[p])
def drumbar(bi):
    b = BARS[bi]; toks = []
    for beat in range(b["len"] // 2):
        base = b["start"] + beat * 2
        hs = [e for e in range(2) if HITS.get(base + e)]
        if not hs: toks.append("r4"); continue
        if hs[0] > 0: toks.append("r8")
        for j, e in enumerate(hs):
            ln = (hs[j + 1] if j + 1 < len(hs) else 2) - e
            toks.append("<" + " ".join(sorted(HITS[base + e])) + ">" + DUR[ln])
    return toks
SECTXT = {
 "g1": {"Intro": "alone, then guitar 2", "Verse 1": "the figure, 3+2", "Refrain 1": "chords on 1 and 3, ring", "Break": "hocket with guitar 2 (on the beats)", "Build": "every beat, then every eighth, crescendo", "Refrain 4": "STOP at bar 79", "Outro": "D and A, ring"},
 "g2": {"Intro": "in at bar 3", "Verse 1": "tacet", "Verse 2": "dyads: and of 1, 3, 5", "Refrain 1": "driving eighths", "Break": "hocket with guitar 1 (offbeats)", "Build": "tacet", "Refrain 4": "STOP at bar 79"},
 "bas": {"Intro": "in at bar 5", "Verse 1": "the 5/4 line", "Refrain 1": "driving eighths", "Build": "held, then the line", "Refrain 4": "STOP at bar 79", "Outro": "low D, ring"},
 "org": {"Refrain 1": "drone: F and C", "Build": "swell", "Refrain 4": "drone; STOP at bar 79", "Outro": "drone: D and A"},
 "drm": {"Intro": "in at bar 5", "Verse 1": "kick 1+4, snare 3+5; hats on 1 and 4", "Verse 2": "hats on every beat", "Refrain 1": "kick 1+3, snare 2+4, ride; crash", "Break": "floor tom on 1 and 4", "Build": "hats and kick; groove; snare eighths", "Refrain 4": "crash bar 78; STOP at bar 79", "Outro": "tacet"}}
RESTB = {}
def mrest(i): return "R1" if BARS[i]["len"] == 8 else "R4*5"
def body(bybar, kind):
    RESTB[kind] = set(); toks = []; last_key = None; bi = 0; cur = None
    def has_(i):
        if kind == "drm": return any(HITS.get(BARS[i]["start"] + e) for e in range(BARS[i]["len"]))
        return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        b = BARS[bi]
        if bi in starts:
            s = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if MET[bi] != cur: toks.append("\\time 3,2 5/4" if MET[bi] == "5/4" else "\\time 4/4"); cur = MET[bi]
            if bi == 0: toks.append("\\tempo 4 = 132")
            if kind != "drm" and b["key"] != last_key: toks.append(KEYLY[b["key"]]); last_key = b["key"]
            txt = SECTXT.get(kind, {}).get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + txt) if txt else ""}"')
        if not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not has_(bi + run) and BARS[bi + run]["len"] == b["len"]: run += 1
            toks.append(f"{mrest(bi)}*{run}")
            RESTB[kind].update(range(bi, bi + run))
            bi += run; continue
        toks += drumbar(bi) if kind == "drm" else bybar[bi]; bi += 1
    return " ".join(toks)
CHR = {"Dm": "d", "G": "g", "F": "f", "Am": "a", "C": "c", "Bb": "bes", "Gm": "g", "D5": "d", "Em": "e"}
QUAL = {"Dm": ":m", "Am": ":m", "Gm": ":m", "Em": ":m", "D5": ":1.5"}
def cdur(i): return "4*5" if BARS[i]["len"] == 10 else "1"
def chords_for(kind):
    out, i, rb = [], 0, RESTB.get(kind, set())
    while i < NB:
        b = BARS[i]
        if i in rb:
            j = i
            while j + 1 < NB and (j + 1) in rb and (j + 1) not in starts and BARS[j + 1]["len"] == b["len"]: j += 1
            q = sum(BARS[x]["len"] for x in range(i, j + 1)) // 2
            out.append(f"r4*{q}" if b["sec"] == "Refrain 4" and b["start"] >= REC["stop_at"] else f"s4*{q}"); i = j + 1; continue
        if b["sec"] == "Refrain 4" and b["start"] >= REC["stop_at"]: out.append("r1")
        else: out.append(f"{CHR[b['chord']]}{cdur(i)}{QUAL.get(b['chord'], '')}")
        i += 1
    return " ".join(out)
PARTS = {k: pitched([dict(e) for e in REC[src]]) for k, src in (("g1", "g1"), ("g2", "g2"), ("bas", "bass"), ("org", "organ"))}
MUS = {k: body(PARTS[k][0], k) for k in PARTS}; MUS["drm"] = body(None, "drm")
NOTES = {
 "g1": "Guitar 1 (clean, bright; sounds an octave below the written notes). Verses, intro and break in 5/4, felt 3+2: the figure is one note an eighth (on Dm: D F A D F A F D F A), accents on 1 and 4. Refrains: the upper voicing struck on 1 and 3 and left to ring. Break: hocket with guitar 2 (you on the beats). Build: the chord on every beat, then every eighth, crescendo. Everything stops at bar 79; outro: D and A, let ring.",
 "g2": "Guitar 2 (clean, darker; sounds an octave below the written notes). The answer to guitar 1: two-note chords on the and of 1, on 3 and on 5 (tacet in verse 1). Refrains: the lower voicing in driving eighths. Break: hocket with guitar 1 (you on the offbeats). Tacet in the build. Stops at bar 79.",
 "bas": "Bass (fretless; sounds an octave below the written bass-clef notes). The 5/4 line: root on 1 (dotted quarter), the root again, the fifth on beat 3, the octave on 4, an approach on 5. Refrains: driving eighths with octave pops. Build: a held low D for two bars, then the line. In at bar 5. Stops at bar 79; outro: low D, let ring.",
 "org": "Organ (church organ). The drone: F and C held under every refrain; a rising swell through the build; D and A in the outro, let ring. Stops at bar 79 with the band.",
 "drm": "Drums. 5/4: kick on 1 and 4, snare on 3 and 5, hats on every beat (the intro and verse 1: hats on 1 and 4 only). Refrains: kick 1 and 3, snare 2 and 4, ride eighths, crash on the first bar. Break: floor tom on 1 and 4. Build: hats and kick (two bars); the full groove (four bars); two bars of snare eighths with toms on 1, 2, 4 and 5 into refrain 3. Crash on bar 78, then STOP at bar 79: the last line is the voice alone. Tacet in the outro.",
}
def part(title, kind, music, clef):
    staff = "DrumStaff" if kind == "drm" else "Staff"; mode = "\\drummode" if kind == "drm" else ""
    cl = "" if kind == "drm" else f'\\clef "{clef}"'
    return f"""\\bookpart {{
  \\header {{ title = "Either Or" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
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
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #12 }}
{part("Guitar 1", "g1", MUS["g1"], "treble_8")}
{part("Guitar 2", "g2", MUS["g2"], "treble_8")}
{part("Bass (fretless)", "bas", MUS["bas"], "bass_8")}
{part("Organ", "org", MUS["org"], "bass")}
{part("Drums", "drm", MUS["drm"], "")}
"""
path, warns = compile_ly(src, "Either Or - parts (guitars, bass, organ, drums)", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:4], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for k in ("g1", "g2", "bas", "org"):
    BYB, notes = PARTS[k]
    toks = [re.sub(r"-\.$", "", t.replace("\\xNote ", "")) for bi in range(NB) for t in BYB.get(bi, []) if not t.startswith("r")]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_part_{k}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_part_{k}.midi")[0]
    want = [p for n in notes for p in n["p"]]
    print(f"readback ({k}):", "matches" if sorted(got) == sorted(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print("drum hits written:", sum(len(v) for v in HITS.values()), "of", sum(len(e["p"]) for e in REC["drums"]))
