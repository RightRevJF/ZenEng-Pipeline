"""'Dance Anyway' -- the lead sheet and the production parts (synth, electric piano, guitar, pad, bass, drums), written bar by bar from the
song record (the events the demo plays, before any humanizing). 4/4 at q = 118, E-flat major; grid: twelfths of a beat (a bar is 48),
onsets on sixteenths. Rehearsal marks, bar numbers, chord symbols; empty bars compressed. Every pitched staff read back from
LilyPond's MIDI against the record."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p36"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p36/song_record.pkl", "rb"))
OUT = "/home/claude/p36/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); BAR = 48; TOT = NB * BAR
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {3: "16", 6: "8", 9: "8.", 12: "4", 18: "4.", 24: "2", 36: "2.", 48: "1"}
def split(pos, n):
    out = []
    while n > 0:
        if pos == 0 and n >= 48: L = 48
        elif pos == 0 and n >= 36: L = 36
        elif pos in (0, 24) and n >= 24: L = 24
        elif pos in (0, 24) and n >= 18: L = 18
        elif pos % 12 == 0 and n >= 12: L = 12
        elif pos % 12 == 0 and n >= 9: L = 9
        elif pos % 6 == 0 and n >= 6: L = 6
        else: L = 3
        if pos % 12: L = min(L, 12 - pos % 12)
        L = min(L, BAR - pos)
        while L not in DUR: L -= 3
        out.append((pos, L)); pos += L; n -= L
    return out
starts = {b0: s for s, nb, b0, met in REC["plan"]}
def pitched(notes, slur_groups=None):
    """notes: dicts with on, dur, p (list), art. Returns tokens per bar, and the pitch list read in order."""
    notes = sorted(notes, key=lambda n: n["on"]); cur = 0; seq = []
    for i, n in enumerate(notes):                     # durations written on the sixteenth grid (a 5-twelfth stab is a sixteenth or an eighth)
        nxt = notes[i + 1]["on"] if i + 1 < len(notes) else TOT
        n["dur"] = max(3, min(int(round(n["dur"] / 3)) * 3, nxt - n["on"]))
    for n in notes:
        assert n["on"] >= cur, (n, cur)
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list); want = []
    for kind, s, d, n in seq:
        first = True
        while d > 0:
            bi = s // BAR; m = min(d, (bi + 1) * BAR - s)
            sp = split(s - bi * BAR, m)
            for k, (pos, L) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = "r" + DUR[L]
                else:
                    ps = n["p"]; nm = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    art = n.get("art", "")
                    tok = ("\\xNote " if art == "ghost" else "") + nm + DUR[L] + ("~" if tie else "") + ("-." if (first and art == "stab") else "")
                    if n.get("slur_open") and first: tok += "("
                    if n.get("slur_close") and not tie and k == len(sp) - 1 and m == d: tok += ")"
                    if first: want += sorted(ps)
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, want
def body(bybar, marks, key=True, multirest=True):
    toks = ["\\time 4/4", "\\tempo 4 = 118"] + (["\\key ees \\major"] if key else []); bi = 0; rest_bars = set()
    def has_(i): return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            txt = marks.get(starts[bi], "")
            toks.append(f'\\mark \\markup \\box \\bold "{starts[bi]}{(" · " + txt) if txt else ""}"')
        if multirest and not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not has_(bi + run): run += 1
            toks.append(f"R1*{run}"); rest_bars.update(range(bi, bi + run)); bi += run; continue
        toks += bybar[bi]; bi += 1
    toks.append('\\bar "|."')
    return " ".join(toks), rest_bars
CHR = {"Eb": "ees", "Ab": "aes", "Bb": "bes", "Cm": "c", "Db": "des", "Fm": "f"}
QUAL = {"Cm": ":m", "Fm": ":m"}
def chords_for(rest_bars):
    out, i = [], 0
    while i < NB:
        if i in rest_bars:
            j = i
            while j + 1 < NB and (j + 1) in rest_bars and (j + 1) not in starts: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        out.append(f"{CHR[BARS[i]['chord']]}1{QUAL.get(BARS[i]['chord'], '')}"); i += 1
    return " ".join(out)
def esc(t): return t.replace('"', '\\"')
def readback(name, bybar, want, clef=""):
    toks = [re.sub(r"[()]", "", t).replace("\\xNote ", "").replace("-.", "") for b in sorted(bybar) for t in bybar[b] if not t.startswith(("r", "R"))]
    compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    # chords come back in any order within a stack; compare as onset-grouped sorted lists by sorting each run of equal onsets
    return sorted(got) == sorted(want) and len(got) == len(want), len(got), len(want)

# ---- the voice ----
lead = [dict(n) for n in REC["lead"]]
groups = collections.defaultdict(list)
for n in lead: groups[(n["sec"], n["line"], n["syl"])].append(n)
for g in groups.values():
    g.sort(key=lambda n: n["on"])
    if len(g) > 1: g[0]["slur_open"] = True; g[-1]["slur_close"] = True
VOX, VWANT = pitched([dict(n, p=[n["midi"]]) for n in lead])
LYR = []
for n in sorted(lead, key=lambda n: n["on"]):
    if not n["first"]: continue
    w = n["text"].replace("'", "’"); q = '"' + esc(w) + '"' if re.search(r"[’?!,.;:\"—]", w) or w in ("_",) else w
    LYR.append(q + (" --" if n["hyph"] else ""))
VMARKS = {"Intro": "synth plays the hook", "Outro": "synth: the hook"}
VBODY, VREST = body(VOX, VMARKS)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
FOOT = "Dance Anyway · Words and music: Jason Bryant · ♩ = 118 · E♭ major · 2:59"
if __name__ == "__main__":
    lead_ly = HEAD % (19, FOOT, FOOT) + f'''\\header {{ title = "Dance Anyway" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Disco-pop · ♩ = 118" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(set())} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "Female voice, B♭3–D5. The one D5 falls on “for-EV-er” in the last chorus (bar 82); every other note is C5 or lower." "Chorus 2 is chorus 1 again. The last line of the song sings the hook a third time and ends on E♭." }}
'''
    path, warns = compile_ly(lead_ly, "Dance Anyway - lead sheet", cwd=OUT)
    if os.environ.get("LEAD_ONLY"): print("lead sheet:", len(warns), "warnings"); print("  readback voice:", readback("voice", VOX, VWANT)); sys.exit(0)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    # ---- the parts ----
    parts_src = [("syn", "Synth (hook)", "synth", "", {"Intro": "the hook, bars 3–4", "Outro": "the hook"}),
                 ("key", "Electric piano", "keys", "", {"Verse 1": "stabs on the 'and' of 2 and 4", "Chorus 1": "stabs on every 'and'", "Bridge": "hold, then stabs from bar 67"}),
                 ("gtr", "Guitar", "gtr", '\\clef "treble_8"', {"Pre 1": "muted sixteenths, the chord on each 'and'", "Verse 1": "tacet", "Verse 2": "in", "Bridge": "tacet to bar 67"}),
                 ("pad", "Pad", "pad", "", {"Pre 1": "in", "Last Chorus": "an octave up"}),
                 ("bas", "Bass", "bass", "\\clef bass", {"Intro": "in at bar 3", "Verse 1": "root and octave, quarters", "Chorus 1": "disco octaves, eighths", "Bridge": "whole notes, then quarters from bar 67"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in REC[src]]
        if k == "gtr":
            for e in ev: e["p"] = [p - 12 for p in e["p"]]                # written an octave up under the treble-8 clef: give LilyPond sounding pitch
            for e in ev: e["p"] = [p + 12 for p in e["p"]]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    # drums: one staff, by the beat
    DN = {36: "bd", 38: "sn", 39: "hc", 42: "hh", 46: "hho", 49: "cymc", 45: "tomml", 51: "cymr"}
    HITS = collections.defaultdict(set)
    for e in REC["drums"]:
        for p in e["p"]: HITS[e["on"]].add(DN[p])
    def drumbar(bi):
        toks = []
        for beat in range(4):
            base = bi * BAR + beat * 12
            hs = [x for x in range(0, 12, 3) if HITS.get(base + x)]
            if not hs: toks.append("r4"); continue
            if hs[0] > 0: toks.append("r" + DUR[hs[0]])
            for j, x in enumerate(hs):
                ln = (hs[j + 1] if j + 1 < len(hs) else 12) - x
                toks.append("<" + " ".join(sorted(HITS[base + x])) + ">" + DUR[ln])
        return toks
    dmarks = {"Intro": "in at bar 3", "Verse 1": "four on the floor; clap and snare 2 and 4; eighth hats", "Pre 1": "snare build, bar 16",
              "Chorus 1": "crash; sixteenth hats, open on each 'and'", "Bridge": "kick on 1 and 3 only; hats from bar 65; build bars 67–68",
              "Last Chorus": "crash every 4 bars"}
    dt = ["\\time 4/4"]; bi = 0
    while bi < NB:
        if bi in starts:
            if bi > 0: dt.append('\\bar "||"')
            tx = dmarks.get(starts[bi], ""); dt.append(f'\\mark \\markup \\box \\bold "{starts[bi]}{(" · " + tx) if tx else ""}"')
        if not any(HITS.get(bi * BAR + x) for x in range(0, 48, 3)):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not any(HITS.get((bi + run) * BAR + x) for x in range(0, 48, 3)): run += 1
            dt.append(f"R1*{run}"); bi += run; continue
        dt += drumbar(bi); bi += 1
    dt.append('\\bar "|."')
    books.append(f'''\\bookpart {{ \\header {{ subtitle = "Drums" }}
\\score {{ \\new DrumStaff \\with {{ drumStyleTable = #drums-style }} \\drummode {{ {" ".join(dt)} }} \\layout {{ }} }} }}''')
    nh = sum(len(v) for v in HITS.values()); nd = sum(len(e["p"]) for e in REC["drums"])
    parts = HEAD % (17, FOOT, FOOT) + '\\header { title = "Dance Anyway" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    path, warns = compile_ly(parts, "Dance Anyway - parts", cwd=OUT)
    print("parts:", [w for w in warns][:4], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
