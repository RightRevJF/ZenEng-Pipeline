"""'Keeping Time' (song 44) -- the lead sheet and the parts (synth bass, pulse, pad, drums), written bar by bar from the song record (the
events the demo plays, before any humanizing). q = 112, four on the floor, straight; E-flat major / C minor (flats); grid: twelfths of a beat.
Rehearsal marks, bar numbers, chord symbols; empty bars compressed in the parts. Every pitched staff read back from LilyPond's MIDI."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p48"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p48/song_record.pkl", "rb"))
_NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
RANGE = f"{_NM[min(_ps) % 12]}{min(_ps) // 12 - 1}–{_NM[max(_ps) % 12]}{max(_ps) // 12 - 1}"                # read from the record (v2)
OUT = "/home/claude/p48/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); BAR = 48; TOT = NB * BAR
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}              # E-flat / C minor: flats; B natural (the G chord)
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
    toks = ["\\time 4/4", TEMPO] + (["\\key ees \\major"] if key else []); bi = 0; rest_bars = set()
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
CHR = {"Eb": "ees", "Fm": "f", "Gm": "g", "Ab": "aes", "Bb": "bes", "Cm": "c", "G": "g", "N.C.": "r"}
QUAL = {"Fm": ":m", "Gm": ":m", "Cm": ":m"}
TEMPO = '\\tempo "Four on the floor" 4 = 112'
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
VMARKS = {"Intro": "the pulse drifts", "Pre 1": "claps in; the pulse locks", "Chorus 1": "full; E-flat", "Post 1": "on the one", "Verse 2": "C minor; drifting again", "Bridge": "no kick: space", "Last Chorus": "everything", "Outro": "the pulse drifts; one E-flat chord"}
VBODY, VREST = body(VOX, VMARKS, multirest=False)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def nm_(p): return f"{_NM[p % 12]}{p // 12 - 1}"
_fig = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 2]; _cell = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 3]; _end = REC["lead"][-1]
NOTE0 = f"The voice: a mezzo, {RANGE}. Mid-tempo dance-pop, straight, four on the floor. Verses in C minor, the chorus in E-flat."
NOTE1 = f"Chorus: “Two clocks on the same wall” rocks between two notes ({nm_(max(n['midi'] for n in _fig))} and {nm_(min(n['midi'] for n in _fig))}); the band drops out under it."
NOTE1b = f"“Keeping time, keeping time”: one figure twice, the second a step higher, up to {nm_(max(n['midi'] for n in _cell))}. Every post-chorus phrase lands on the one."
NOTE2 = f"The verses stay narrow and the chorus opens over them. The last line, “Nobody’s leaving anymore,” comes home to {nm_(_end['midi'])}."
FOOT = "Keeping Time · Words and music: Jason Bryant · ♩ = 112 · C minor / E-flat major · 2:51"
if __name__ == "__main__":
    lead_ly = HEAD % (18, FOOT, FOOT) + "\\paper { max-systems-per-page = 8 }\n" + f'''\\header {{ title = "Keeping Time" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Dance-pop · ♩ = 112" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(set())} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "{NOTE0}" "{NOTE1}" "{NOTE1b}" "{NOTE2}" }}
'''
    path, warns = compile_ly(lead_ly, "Keeping Time - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    okr = okl = (True, 0, 0)
    parts_src = [("bas", "Synth bass", [e for e in REC["bass"]], "\\clef bass", {"Intro": "in at bar 5: quarters while the pulse drifts", "Chorus 1": "eighths, root and octave", "Bridge": "whole notes", "Outro": "one E-flat, let ring"}),
                 ("pul", "Pulse (drifts, then locks)", [e for e in REC["pulse"]], "\\clef treble", {"Intro": "dotted eighths: drifting against the kick", "Pre 1": "locks to eighths in the last bar", "Chorus 1": "locked; alone in bar 5, tick and tock", "Verse 2": "drifting again", "Bridge": "quarters, space", "Outro": "drifting; one note, let ring"}),
                 ("pad", "Pad", [e for e in REC["pad"]], "\\clef treble", {"Intro": "in at bar 5", "Bridge": "up a little, wide", "Outro": "one E-flat chord, let ring"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    DN = {36: "bd", 38: "sn", 39: "hc", 42: "hh", 46: "hho", 49: "cymc"}
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
    dmarks = {"Intro": "kick from bar 5; hats in dotted eighths (with the pulse)", "Pre 1": "claps on 2 and 4; snare build", "Chorus 1": "locked: off-beat hats, sixteenths; OUT in bar 5", "Verse 2": "dotted-eighth hats again", "Bridge": "no kick for 6 bars; the build in bars 7-8", "Last Chorus": "every sixteenth", "Outro": "drifting; crash on the last chord"}
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
    nh = sum(len(v) for v in HITS.values()); nd = len({(e["on"], p) for e in REC["drums"] for p in e["p"]})
    parts = HEAD % (17, FOOT, FOOT) + "\\paper { max-systems-per-page = 9 }\n" + '\\header { title = "Keeping Time" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    path, warns = compile_ly(parts, "Keeping Time - parts", cwd=OUT)
    print("parts:", [w for w in warns][:4], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, piano_rh=okr, piano_lh=okl, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
