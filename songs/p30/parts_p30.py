"""The production parts pack for 'She Left the Light On': six parts in one PDF -- ACOUSTIC GUITAR (strums as rhythm slashes under the
chord names, the bridge's picking in notes), ELECTRIC GUITAR (the lick), PEDAL STEEL, ORGAN, BASS and DRUMS -- written bar by bar from
the song record, the same events the demo plays. 4/4 at q = 84, D major (G minor borrowed in bars 45-46), on a sixteenth grid.
Rehearsal marks with each part's cue, bar numbers, chord symbols; empty bars compressed. Guitars and bass sound an octave below the
written notes; steel and organ are written at pitch. LilyPond's MIDI read back per part; drum hits counted against the record."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p30"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p30/song_record.pkl", "rb"))
OUT = "/home/claude/p30/out"
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_slots"]
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
starts = {b0: s for s, nb, b0, met in REC["plan"]}
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}
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
def stream(notes, name=None):
    """per-bar tokens; name(e) gives the note name (a slash's fixed pitch), else the pitches"""
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
                nm = name(n) if name else (pname(n["p"][0]) if len(n["p"]) == 1 else "<" + " ".join(pname(p) for p in n["p"]) + ">")
                byb[bi].append(nm + DUR[L] + ("~" if not (k == len(sp) - 1 and m == d) else "")); has.add(bi)
            s += m; d -= m
    return byb, has
# ---- the parts' streams ----
AC = group(REC["ac"]); SL = [e for e in AC if e["art"] in ("strum", "ring")]; PK = [e for e in AC if e["art"] == "pick"]
SLB, SLH = stream(SL, name=lambda e: "b"); PKB, PKH = stream(PK)
def ac_bars():
    out = {}
    for bi in range(NB):
        if bi in PKH: out[bi] = PKB[bi]
        elif bi in SLH: out[bi] = ["\\improvisationOn"] + SLB[bi] + ["\\improvisationOff"]
    return out
VOICES = {k: pack(group(REC[src])) for k, src in (("lick", "lick"), ("steel", "steel"), ("organ", "organ"), ("bass", "bass"))}
for k, v in VOICES.items(): assert len(v) <= 2, (k, len(v))
VB = {k: [stream(v) for v in vs] for k, vs in VOICES.items()}
DN = {36: "bd", 37: "ss", 38: "sn", 42: "hh", 46: "hho", 49: "cymc", 45: "toml", 47: "tomml", 50: "tomh", 54: "tamb"}
HITS = collections.defaultdict(set)
for e in REC["drums"]:
    for p in e["p"]: HITS[e["on"]].add(DN[p])
def drumbar(bi):
    st = BARS[bi]["start"]; toks = []
    for beat in range(4):
        base = st + beat * 4; hs = [e for e in range(4) if HITS.get(base + e)]
        if not hs: toks.append("r4"); continue
        if hs[0] > 0: toks.append("r" + DUR[hs[0]])
        for j, e in enumerate(hs):
            ln = (hs[j + 1] if j + 1 < len(hs) else 4) - e
            toks.append("<" + " ".join(sorted(HITS[base + e])) + ">" + DUR[ln])
    return toks
SECTXT = {
 "ac": {"Intro": "light: down 1 and 3, up on the 'and' of 2 and 4", "Chorus 1": "full: D . D U . U D U", "Bridge": "pick in eighths",
        "Chorus 3": "the drop: one strum, let ring", "Outro": "last bar: one strum, let ring"},
 "lick": {"Intro": "the lick", "Post 1": "the lick", "Post 2": "the lick", "Outro": "the lick twice; end on B, ring"},
 "steel": {"Verse 1": "swells", "Verse 2": "answers where the voice leaves room", "Bridge": "swells; B-flat under 'thumb'", "Chorus 3": "the drop: swell alone"},
 "organ": {"Chorus 3": "in at bar 49 (the flip)"},
 "bass": {"Intro": "in at bar 3", "Chorus 1": "two-beat, walk into each change", "Bridge": "whole notes", "Chorus 3": "out for the drop; in at bar 49", "Outro": "hold the last G"},
 "drums": {"Intro": "in at bar 3: kick 1 and 3, cross-stick 2 and 4", "Chorus 1": "full; crash", "Verse 2": "full groove, no open hat", "Bridge": "kick on 1; tom swell in bar 46",
           "Chorus 3": "the drop: silent, then a tom fill; crash at bar 49; tambourine from bar 51", "Outro": "last bar: nothing"}}
RESTB = {}
def body(kind, getbar, has_bar):
    RESTB[kind] = set(); toks = []; bi = 0
    while bi < NB:
        if bi in starts:
            s = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\tempo 4 = 84"] + ([] if kind == "drums" else ["\\key d \\major"])
            txt = SECTXT.get(kind, {}).get(s, "")
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + txt) if txt else ""}"')
        if not has_bar(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not has_bar(bi + run): run += 1
            toks.append(f"R1*{run}"); RESTB[kind].update(range(bi, bi + run)); bi += run; continue
        toks += getbar(bi); bi += 1
    return " ".join(toks)
def vbar(vbs):
    def g(bi):
        live = [bb[bi] for bb, h in vbs if bi in h]
        return live[0] if len(live) == 1 else ["<<", "{", *live[0], "}", "\\\\", "{", *live[1], "}", ">>"]
    return g, (lambda bi: any(bi in h for _, h in vbs))
ACB = ac_bars()
MUS = {"ac": body("ac", lambda bi: ACB[bi], lambda bi: bi in ACB)}
for k in VB: MUS[k] = body(k, *vbar(VB[k]))
MUS["drums"] = body("drums", drumbar, lambda bi: any(HITS.get(BARS[bi]["start"] + e) for e in range(16)))
CHR = {"D": "d", "G": "g", "A": "a", "Bm": "b", "Em": "e", "Gm": "g"}; QUAL = {"Bm": ":m", "Em": ":m", "Gm": ":m"}
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
 "ac": "Acoustic guitar, steel-string, open chords (sounds an octave below the written notes). Strums are written as rhythm slashes under the chord names: intro and verse 1 light (down on 1 and 3, up on the 'and' of 2 and 4); from chorus 1 the full pattern (D . D U . U D U). The bridge is picked in eighths, written out. Bar 47: one strum, let it ring two bars (the drop). Bar 60: one strum on G, let it ring.",
 "lick": "Electric guitar, clean (sounds an octave below the written notes). The lick is the chorus's title tune ('she LEFT the LIGHT on') up an octave, answered by a falling line. Intro, both post-choruses and the outro; play it the same every time. The last note, B over G, rings.",
 "steel": "Pedal steel, written at pitch. Swells (volume pedal) under verse 1 and the bridge, a bar at a time. From verse 2, answer the singer where a line leaves room: falling chord tones, slide into the first. Hold B-flat under 'thumb' (bars 45-46). Bars 47-48, the drop: swell alone on A and C-sharp.",
 "organ": "Organ (drawbar, soft). Bars 49-56 only, from the flip: hold the chord a bar at a time, under everything. Felt more than heard.",
 "bass": "Bass (sounds an octave below the written notes). Intro bars 3-4 and verse 1: root on 1, fifth on 3. From chorus 1: the two-beat with an eighth walk into each chord change. Bridge: whole notes. Out for bars 47-48 (the drop). Hold the last G.",
 "drums": "Drums. Intro bars 3-4 and verse 1: kick on 1 and 3, cross-stick on 2 and 4, soft eighth hats. Choruses: kick on 1, the 'and' of 2 and 3; snare 2 and 4; eighth hats, open on the 'and' of 4; crash at the top; a three-note snare pickup at the end of choruses 1 and 2. Verse 2: the groove without the open hat. Bridge: kick on 1; a low-tom swell in bar 46. Bar 47 silent; bar 48 a tom fill; crash at bar 49; tambourine on the eighths from bar 51. Last bar: nothing.",
}
def part(title, kind, music, clef):
    if kind == "drums":
        staff = "\\new DrumStaff"; inner = f"\\compressMMRests \\drummode {{ {music} \\bar \"|.\" }}"
    else:
        staff = "\\new Staff"; inner = f'\\clef "{clef}" \\compressMMRests {{ {music} \\bar "|." }}'
    return f"""\\bookpart {{
  \\header {{ title = "She Left the Light On" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\vspace #1.6
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\markup \\vspace #1.0
  \\score {{
    <<
      \\new ChordNames \\chordmode {{ {chords_for(kind)} }}
      {staff} {{ {inner} }}
    >>
    \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
               \\context {{ \\ChordNames \\override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #2.0 }} }}
  }}
}}
"""
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #12 page-breaking = #ly:optimal-breaking }}
{part("Acoustic guitar", "ac", MUS["ac"], "treble_8")}
{part("Electric guitar (the lick)", "lick", MUS["lick"], "treble_8")}
{part("Pedal steel", "steel", MUS["steel"], "treble")}
{part("Organ", "organ", MUS["organ"], "treble")}
{part("Bass", "bass", MUS["bass"], "bass_8")}
{part("Drums", "drums", MUS["drums"], "")}
"""
path, warns = compile_ly(src, "She Left the Light On - parts (guitars, steel, organ, bass, drums)", cwd=OUT)
print("compiled", path, [w for w in warns if "clashing" not in w][:6], f"({len(warns)} warnings)")
os.makedirs(OUT + "/check", exist_ok=True)
def readback(name, toks_list, want):
    got = []
    for j, toks in enumerate(toks_list):
        toks = [t for t in toks if t[0] not in "rR\\"]
        compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"check_part_{name}{j}", cwd=OUT + "/check")
        got += midi_readback(f"{OUT}/check/check_part_{name}{j}.midi")[0]
    ok = len(got) == want["count"] if isinstance(want, dict) else sorted(got) == sorted(want)
    print(f"readback ({name}):", "matches" if ok else f"MISMATCH ({len(got)} vs {want['count'] if isinstance(want, dict) else len(want)})", len(got))
readback("acoustic picking", [[t for bi in range(NB) for t in PKB.get(bi, [])]], [p for e in PK for p in e["p"]])
readback("acoustic strums (slashes, one per strum)", [[t for bi in range(NB) for t in SLB.get(bi, [])]], {"count": len(SL)})
for k in VB:
    readback(k, [[t for bi in range(NB) for t in bb.get(bi, [])] for bb, h in VB[k]], [p for v in VOICES[k] for e in v for p in e["p"]])
nh = sum(len(v) for v in HITS.values())
print("drum hits:", "matches" if nh == sum(len(e["p"]) for e in REC["drums"]) else "MISMATCH", nh)
