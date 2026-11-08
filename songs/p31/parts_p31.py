"""The production parts pack for 'Nothing On': eight parts in one PDF -- FUNK GUITAR (muted), RIFF GUITAR, RHODES, HORNS, PAD (the
hum), BASS, DRUMS AND PERCUSSION (kit staff plus a bongo/tambourine staff) and the BACKING VOCAL with its words -- written bar by bar
from the song record, the same events the demo plays. 4/4 at q = 116, F major signature, on a sixteenth grid. Rehearsal marks with each
part's cue, bar numbers, chord symbols; empty bars compressed; the cuts marked. Guitars and bass sound an octave below the written notes;
Rhodes, horns (concert pitch), pad and voice are written at pitch. LilyPond's MIDI read back per part; drum hits counted against the record."""
import pickle, collections, os, sys
sys.path[:0] = ["/home/claude/carol", "/home/claude/p31"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p31/song_record.pkl", "rb"))
OUT = "/home/claude/p31/out"
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_slots"]
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
starts = {b0: s for s, nb, b0, met in REC["plan"]}
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}
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
def group(evs):
    g = collections.OrderedDict()
    for e in sorted(evs, key=lambda e: (e["on"], -e["dur"])): g.setdefault((e["on"], e["dur"]), []).append(e)
    return [dict(on=o, dur=d, p=sorted({p for e in es for p in e["p"]}), art=es[0].get("art", "")) for (o, d), es in g.items()]
def pack(evs):
    voices = []
    for e in sorted(evs, key=lambda e: (e["on"], -e["dur"])):
        for v in voices:
            if v[-1]["on"] + v[-1]["dur"] <= e["on"]: v.append(e); break
        else: voices.append([e])
    voices.sort(key=lambda v: -sum(sum(e["p"]) / len(e["p"]) for e in v) / len(v))
    return voices
def stream(notes):
    cur, seq = 0, []
    for n in notes:
        assert n["on"] >= cur, n
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    byb = collections.defaultdict(list); has = set()
    for kind, s, d, n in seq:
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; m = min(d, b["start"] + b["len"] - s); sp = split(s - b["start"], m)
            for k, (pos, L) in enumerate(sp):
                if kind == "r": byb[bi].append("r" + DUR[L]); continue
                nm = pname(n["p"][0]) if len(n["p"]) == 1 else "<" + " ".join(pname(p) for p in n["p"]) + ">"
                byb[bi].append(nm + DUR[L] + ("~" if not (k == len(sp) - 1 and m == d) else "")); has.add(bi)
            s += m; d -= m
    return byb, has
# ---- the parts' streams ----
VOICES = {k: pack(group(REC[k])) for k in ("gtr", "riff", "keys", "horns", "hum", "bass")}
for k, v in VOICES.items(): assert len(v) <= 2, (k, len(v))
VB = {k: [stream(v) for v in vs] for k, vs in VOICES.items()}
BVN = sorted([dict(on=n["on"], dur=n["dur"], p=[n["midi"]], sec=n["sec"]) for n in REC["harm"]], key=lambda n: n["on"])
BVB, BVH = stream(BVN)
BVLYR = []
for s in dict.fromkeys(n["sec"] for n in BVN):
    k = sum(1 for n in BVN if n["sec"] == s)
    BVLYR += (['"(noth" --', "ing", '"on)"'] if s.startswith("Post") else ["noth --", "ing", '"on,"', "noth --", "ing", "on"] * (k // 6))
KIT = {36: "bd", 38: "sn", 39: "hc", 42: "hh", 46: "hho", 49: "cymc", 45: "toml", 47: "tomml", 50: "tomh"}
PERC = {54: "tamb", 60: "boh", 61: "bol"}
def hits(table):
    H = collections.defaultdict(set)
    for e in REC["drums"]:
        for p in e["p"]:
            if p in table: H[e["on"]].add(table[p])
    return H
HITS = hits(KIT); PHITS = hits(PERC)
def drumbar_of(H):
    def f(bi):
        st = BARS[bi]["start"]; toks = []
        for beat in range(4):
            base = st + beat * 4; hs = [e for e in range(4) if H.get(base + e)]
            if not hs: toks.append("r4"); continue
            if hs[0] > 0: toks.append("r" + DUR[hs[0]])
            for j, e in enumerate(hs):
                ln = (hs[j + 1] if j + 1 < len(hs) else 4) - e
                toks.append("<" + " ".join(sorted(H[base + e])) + ">" + DUR[ln])
        return toks
    return f
CUTTXT = {}
for cut in REC["cuts"]: CUTTXT[bar_at[cut["start"]]] = "tape stop: out on beat 3" if cut["kind"] == "tape stop" else "hit 1, then out"
TACET = {i for i, b in enumerate(BARS) if b["sec"].startswith("Chorus") and b["k"] == 0}
SECTXT = {
 "gtr": {"Intro": "in at bar 3", "Pre 1": "sixteenths", "Bridge": "in at bar 59", "Post 3": "out at bar 73"},
 "riff": {"Intro": "the riff", "Verse 2": "answers", "Outro": "first bar, let it ring"},
 "keys": {"Verse 1": "hold the chord", "Pre 1": "half notes", "Chorus 1": "stabs", "Bridge": "whole notes", "Post 3": "with the bass alone at bar 73", "Outro": "ring"},
 "horns": {"Pre 2": "swell", "Chorus 1": "stabs where she holds", "Chorus 3": "three stabs"},
 "hum": {"Bridge": "the fridge's hum"},
 "bass": {"Intro": "in at bar 3", "Pre 1": "disco octaves", "Bridge": "in at bar 55", "Post 3": "whole notes at bar 73", "Outro": "hold"},
 "drums": {"Intro": "hats; groove at bar 3", "Pre 1": "four on the floor", "Bridge": "out; kick and hats at bar 57", "Post 3": "out at bar 73"},
 "bv": {"Post 1": "the echo", "Chorus 3": "a third under the title"}}
RESTB = {}
def body(kind, getbar, has_bar):
    RESTB[kind] = set(); toks = []; bi = 0
    while bi < NB:
        if bi in starts:
            s = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4"] + ([] if kind == "perc" else ["\\tempo 4 = 116"]) + ([] if kind in ("drums", "perc") else ["\\key f \\major"])
            txt = SECTXT.get(kind, {}).get(s, "") if kind != "perc" else ""
            if s.startswith("Chorus") and kind not in ("bv", "perc"): txt = (txt + " · " if txt else "") + "TACET bar 1"
            if kind != "perc": toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + txt) if txt else ""}"')
        if not has_bar(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not has_bar(bi + run): run += 1
            toks.append(f"R1*{run}"); RESTB[kind].update(range(bi, bi + run)); bi += run; continue
        bt = list(getbar(bi))
        if bi in CUTTXT and kind not in ("bv", "perc") and bt and not bt[0].startswith("<<"):
            bt[0] = bt[0] + f'^\\markup \\italic \\small "{CUTTXT[bi]}"'
        toks += bt; bi += 1
    return " ".join(toks)
def vbar(vbs):
    def g(bi):
        live = [bb[bi] for bb, h in vbs if bi in h]
        return live[0] if len(live) == 1 else ["<<", "{", *live[0], "}", "\\\\", "{", *live[1], "}", ">>"]
    return g, (lambda bi: any(bi in h for _, h in vbs))
MUS = {}
for k in VB: MUS[k] = body(k, *vbar(VB[k]))
MUS["drums"] = body("drums", drumbar_of(HITS), lambda bi: any(HITS.get(BARS[bi]["start"] + e) for e in range(16)))
MUS["perc"] = body("perc", drumbar_of(PHITS), lambda bi: any(PHITS.get(BARS[bi]["start"] + e) for e in range(16)))
MUS["bv"] = body("bv", lambda bi: BVB[bi], lambda bi: bi in BVH)
CHR = {"Gm7": "g", "Am7": "a", "Bbmaj7": "bes", "C": "c", "F": "f", "Am": "a", "Bb": "bes"}
QUAL = {"Gm7": ":m7", "Am7": ":m7", "Bbmaj7": ":maj7", "Am": ":m"}
def chords_for(kind):
    out, i, rb = [], 0, RESTB.get(kind, set())
    while i < NB:
        if i in rb:
            j = i
            while j + 1 < NB and (j + 1) in rb and (j + 1) not in starts: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        c = BARS[i]["chord"]; out.append(f"{CHR[c]}1{QUAL.get(c, '')}"); i += 1
    return " ".join(out)
NOTES = {
 "gtr": "Funk guitar, muted (sounds an octave below the written notes). Short, choked chords: off-beat eighths in the intro (from bar 3) and both verses; the sixteenth pattern (accents on the off-beats) from each pre-chorus through the choruses and posts. Out on beat 3 of each pre-chorus's last bar (the tape stop) and TACET in each chorus's first bar. Bridge: in at bar 59 for the build; hit 1 in bar 60, then out. Out for the last line (bar 73).",
 "riff": "Riff guitar, clean single notes (sounds an octave below the written notes). The riff is the chorus's 'nothing on, nothing on' tune with sixteenth fills. Intro (4 bars); in verse 2 it answers in a line's second bar where the singer leaves room; the outro plays its first bar and lets the last note ring. The singer takes the riff over in every chorus.",
 "keys": "Rhodes, written at pitch. Held chords in the verses; half notes in the pre-choruses; three stabs a bar in the choruses and posts. Bridge: whole notes, the first sound when the power comes back, with the pad. Out with the band at every cut. You and the bass alone under the last line (bars 73-74); ring the last chord.",
 "horns": "Horns (brass section: trumpets, tenor sax, trombone), concert pitch, the top three notes of the voicing. Two stabs, beat 4 and its 'and', in every chorus and post bar where the singer holds; a third on the 'and' of 2 in the last chorus. A swell (soft to loud) through pre-chorus 2. Never under a moving vocal line.",
 "hum": "Pad (synth, warm, no attack), written at pitch. Bridge bars 53-56 only: a low F with C above, growing slightly each bar: the fridge's hum as the power comes back.",
 "bass": "Bass, fingers (P-bass, flatwounds; sounds an octave below the written notes). Verses: the syncopated root line. From each pre-chorus: disco octaves in eighths with a sixteenth push on beat 2. Out on beat 3 of each pre-chorus's last bar and TACET in each chorus's first bar. Bridge: in at bar 55 in whole notes, eighths from bar 59; hit 1 in bar 60. Whole notes under the last line; hold the last B-flat.",
 "drums": "Drums (kit, top staff) and percussion (bongos and tambourine, lower staff). Intro: sixteenth hats, a snare pickup, the groove from bar 3. Verses: kick 1, the 'a' of 2, 3; snare 2 and 4 with ghost notes; sixteenth hats. Pre-choruses: four on the floor, open hats on the off-beats, a snare build in the last bar to beat 3, then OUT. Choruses and posts: TACET in the chorus's first bar; crash on the re-entry; four on the floor, snare and handclaps on 2 and 4, sixteenth hats with the open hat on the off-beats. Bridge: out for four bars; kick and hats at bar 57; snare eighths in bar 59; everything hits 1 in bar 60, then out. Bongos in the posts; tambourine eighths in chorus 2, sixteenths in the last chorus. Out for the last line.",
 "bv": "Backing vocal, written at pitch, with the words. The echo '(nothing on)' in each post-chorus's third bar, a third under the lead's tune, before she sings 'nothing on but you'. In the last chorus, a third under every 'nothing on, nothing on'. Match her phrasing exactly; breathy, not loud.",
}
LAYOUT = """\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
               \\context {{ \\ChordNames \\override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #2.0 }} }}"""
def part(title, kind, clef):
    music = MUS[kind]
    if kind == "drums":
        staves = (f'\\new DrumStaff {{ \\compressMMRests \\drummode {{ {music} \\bar "|." }} }}\n'
                  f'      \\new DrumStaff \\with {{ drumStyleTable = #percussion-style \\override StaffSymbol.line-count = #2 instrumentName = \\markup \\small "Perc." }} '
                  f'{{ \\compressMMRests \\drummode {{ {MUS["perc"]} \\bar "|." }} }}')
    elif kind == "bv":
        staves = (f'\\new Staff {{ \\clef "treble" \\compressMMRests \\new Voice = "bv" {{ {music} \\bar "|." }} }}\n'
                  f'      \\new Lyrics \\lyricsto "bv" {{ {" ".join(BVLYR)} }}')
    else:
        staves = f'\\new Staff {{ \\clef "{clef}" \\compressMMRests {{ {music} \\bar "|." }} }}'
    return f"""\\bookpart {{
  \\header {{ title = "Nothing On" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #1.6
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\markup \\vspace #1.0
  \\score {{
    <<
      \\new ChordNames \\chordmode {{ {chords_for(kind)} }}
      {staves}
    >>
    {LAYOUT.format()}
  }}
}}
"""
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #12 page-breaking = #ly:optimal-breaking }}
{part("Funk guitar (muted)", "gtr", "treble_8")}
{part("Riff guitar (clean)", "riff", "treble_8")}
{part("Rhodes", "keys", "treble")}
{part("Horns (concert pitch)", "horns", "treble")}
{part("Pad (the bridge's hum)", "hum", "bass")}
{part("Bass", "bass", "bass_8")}
{part("Drums and percussion", "drums", "")}
{part("Backing vocal", "bv", "treble")}
"""
path, warns = compile_ly(src, "Nothing On - parts (guitars, Rhodes, horns, pad, bass, drums, backing vocal)", cwd=OUT)
print("compiled", path, [w for w in warns if "clashing" not in w][:6], f"({len(warns)} warnings)")
os.makedirs(OUT + "/check", exist_ok=True)
def readback(name, toks_list, want):
    got = []
    for j, toks in enumerate(toks_list):
        toks = [t.split("^")[0] for t in toks if t[0] not in "rR\\"]
        compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"check_part_{name}{j}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/check_part_{name}{j}.midi")[0]
    ok = sorted(got) == sorted(want)
    print(f"readback ({name}):", "matches" if ok else f"MISMATCH ({len(got)} vs {len(want)})", len(got))
    return ok
RB = {}
for k in VB:
    RB[k] = readback(k, [[t for bi in range(NB) for t in bb.get(bi, [])] for bb, h in VB[k]], [p for v in VOICES[k] for e in v for p in e["p"]])
RB["bv"] = readback("backing vocal", [[t for bi in range(NB) for t in BVB.get(bi, [])]], [p for n in BVN for p in n["p"]])
nh = sum(len(v) for v in HITS.values()) + sum(len(v) for v in PHITS.values())
want = len({(e["on"], p) for e in REC["drums"] for p in e["p"]})
print("drum hits:", "matches" if nh == want else f"MISMATCH ({nh} vs {want})", nh, f"(record: {sum(len(e['p']) for e in REC['drums'])} hits; a snare and its ghost or build on the same sixteenth merge)")
pickle.dump(dict(readback=RB, drum_hits=nh, drum_want=want), open(f"{OUT}/parts_report.pkl", "wb"))
