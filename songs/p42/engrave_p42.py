"""'Nothing Important' (song 42) -- the lead sheet, the piano-vocal score (the voice over the complete piano part: the song as one player
at the piano performs it with the singer, Q7), and the parts (cello, bass, guitar, drums), written bar by bar from the song record (the
events the demo plays, before any humanizing). Straight eighths at q = 76; B-flat major; grid: twelfths of a beat. Rehearsal marks, bar
numbers, chord symbols; empty bars compressed in the parts. Every pitched staff read back from LilyPond's MIDI against the record."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p42"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p42/song_record.pkl", "rb"))
_NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
RANGE = f"{_NM[min(_ps) % 12]}{min(_ps) // 12 - 1}–{_NM[max(_ps) % 12]}{max(_ps) // 12 - 1}"                # read from the record (v2)
OUT = "/home/claude/p42/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); BAR = 48; TOT = NB * BAR
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}               # flats, from B-flat major
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
    toks = ["\\time 4/4", TEMPO] + (["\\key bes \\major"] if key else []); bi = 0; rest_bars = set()
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
CHR = {"Bb": "bes", "Eb": "ees", "F": "f", "Gm": "g", "Cm": "c", "Dm": "d", "N.C.": "r"}
QUAL = {"Gm": ":m", "Cm": ":m", "Dm": ":m"}
TEMPO = '\\tempo "Gently" 4 = 76'
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
VMARKS = {"Intro": "piano alone", "Verse 2": "cello in", "Bridge": "the last night", "Verse 3": "three days", "Last Chorus": "the band, bars 53-62", "Outro": "piano alone; one chord, let ring"}
VBODY, VREST = body(VOX, VMARKS, multirest=False)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def nm_(p): return f"{_NM[p % 12]}{p // 12 - 1}"
_lc4 = [n for n in REC["lead"] if n["sec"] == "Last Chorus" and n["line"] == 4]; _tag = REC["lead"][-1]
NOTE0 = f"The voice: an alto, {RANGE}. The piano part is complete: one player can accompany the whole song alone."
NOTE1 = (f"Last chorus: “Nothing important” is held longer than before (bars {_lc4[0]['on'] // 48 + 1}-{_lc4[-1]['on'] // 48 + 1}); "
         f"“I'll call you back” falls quietly to {nm_(_tag['midi'])} (bar {_tag['on'] // 48 + 1}), the piano alone under it.")
NOTE2 = "Bar 68: one B-flat chord, let it ring."
FOOT = "Nothing Important · Words and music: Jason Bryant · ♩ = 76 · B-flat major · 3:35"
PRH, PRW = pitched([dict(e) for e in REC["piano_rh"]]); PLH, PLW = pitched([dict(e) for e in REC["piano_lh"]])
PRB, _ = body(PRH, {}, multirest=False); PLB, _ = body(PLH, {}, multirest=False)
import re as _re
PRB = _re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", PRB); PLB = _re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", PLB)
if __name__ == "__main__":
    lead_ly = HEAD % (18, FOOT, FOOT) + f'''\\header {{ title = "Nothing Important" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Piano ballad · ♩ = 76" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(set())} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "{NOTE0}" "{NOTE1}" "{NOTE2}" }}
'''
    path, warns = compile_ly(lead_ly, "Nothing Important - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    score_ly = HEAD % (16, FOOT, FOOT) + f'''\\header {{ title = "Nothing Important" subtitle = "Piano-vocal score" composer = "Words and music: Jason Bryant" meter = "Piano ballad · ♩ = 76" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(set())} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
  \\new PianoStaff \\with {{ instrumentName = "Piano" }} <<
    \\new Staff = "rh" {{ \\clef "treble" {PRB} }}
    \\new Staff = "lh" {{ \\clef "bass" {PLB} }}
  >>
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "{NOTE0}" "{NOTE1}" "{NOTE2}" }}
'''
    path, warns = compile_ly(score_ly, "Nothing Important - piano-vocal score", cwd=OUT)
    print("score:", [w for w in warns][:4], len(warns))
    okr = readback("piano_rh", PRH, PRW); okl = readback("piano_lh", PLH, PLW)
    print("  readback piano rh:", okr, "lh:", okl)
    parts_src = [("vc", "Cello", [e for e in REC["cello"]], "\\clef bass", {"Verse 2": "in: held notes", "Bridge": "the countermelody, in the voice's gaps", "Verse 3": "out for 4 bars, then held", "Last Chorus": "the countermelody", "Outro": "one note, let ring"}),
                 ("bas", "Bass", [e for e in REC["bass"]], "\\clef bass", {"Last Chorus": "bars 53-58 whole notes, 59-62 root and fifth; out at bar 63"}),
                 ("gtr", "Guitar (clean)", [e for e in REC["gtr"]], '\\clef "treble_8"', {"Last Chorus": "arpeggios, bars 53-62; out at bar 63"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    DN = {36: "bd", 38: "sn", 40: "sne", 42: "hh", 49: "cymc", 51: "cymr"}
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
    dmarks = {"Last Chorus": "BRUSHES bars 53-58 (kick 1, 3; tap 2, 4; swirl); STICKS 59-62 (crash); out at 63"}
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
    books.append(f'''\\bookpart {{ \\header {{ subtitle = "Drums (last chorus)" }}
\\score {{ \\new DrumStaff \\with {{ drumStyleTable = #drums-style }} \\drummode {{ {" ".join(dt)} }} \\layout {{ }} }} }}''')
    nh = sum(len(v) for v in HITS.values()); nd = len({(e["on"], p) for e in REC["drums"] for p in e["p"]})
    parts = HEAD % (17, FOOT, FOOT) + '\\header { title = "Nothing Important" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    path, warns = compile_ly(parts, "Nothing Important - parts", cwd=OUT)
    print("parts:", [w for w in warns][:4], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, piano_rh=okr, piano_lh=okl, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
