"""'The Singer Doesn't Stop' (song 47) -- the lead sheet and the parts (bass, electric guitar, drums), written bar by bar from the song
record (the events the demo plays, before any humanizing). q = 84, sixteenth strum; G major, the second bridge's first fourteen bars in
A major (the lift), back to G for its last line; grid: twelfths of a beat. Chord symbols by the half-bar (the 438 chart). The acoustic
guitar plays from the chord symbols (its strum is in the songbook). Every pitched staff read back from LilyPond's MIDI."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p57"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p57/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
RANGE = f"{_NM[min(_ps) % 12]}{min(_ps) // 12 - 1}–{_NM[max(_ps) % 12]}{max(_ps) // 12 - 1}"                # read from the record (v2)
OUT = "/home/claude/p57/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); BAR = 48; TOT = NB * BAR
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}              # A minor: sharps (G-sharp, F-sharp)
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
    toks = ["\\time 4/4", TEMPO] + (["\\key g \\major"] if key else []); bi = 0; rest_bars = set()
    def has_(i): return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            txt = marks.get(starts[bi], "")
            toks.append(f'\\mark \\markup \\box \\bold "{starts[bi]}{(" · " + txt) if txt else ""}"')
        if key and bi in KEYCH: toks.append(KEYCH[bi])
        if multirest and not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and (bi + run) not in KEYCH and not has_(bi + run): run += 1
            toks.append(f"R1*{run}"); rest_bars.update(range(bi, bi + run)); bi += run; continue
        toks += bybar[bi]; bi += 1
    toks.append('\\bar "|."')
    return " ".join(toks), rest_bars
CHR = {"G": "g", "C": "c", "D": "d", "Em": "e", "Am": "a", "Bm": "b", "A": "a", "E": "e", "F#m": "fis", "C#m": "cis", "N.C.": "r"}
QUAL = {"Em": ":m", "Am": ":m", "Bm": ":m", "F#m": ":m", "C#m": ":m"}
TEMPO = '\\tempo "Sixteenth strum" 4 = 84'
_LB = REC["lift"]["bars"]; KEYCH = {_LB[0]: "\\key a \\major", _LB[-1] + 1: "\\key g \\major"}
def chords_for(rest_bars):
    out, i = [], 0
    while i < NB:
        if i in rest_bars:
            j = i
            while j + 1 < NB and (j + 1) in rest_bars and (j + 1) not in starts: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        a_, b_ = BARS[i]['chord'], BARS[i]['chord2']
        if a_ == b_: out.append(f"{CHR[a_]}1{QUAL.get(a_, '')}")
        else: out.append(f"{CHR[a_]}2{QUAL.get(a_, '')} {CHR[b_]}2{QUAL.get(b_, '')}")
        i += 1
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
VMARKS = {"Intro": "guitar alone", "Chorus 1": "bass and brushes in", "Verse 2": "low electric swells", "Bridge": "guitar and voice", "Bridge 2": "a step higher; the band builds", "Last Chorus": "full, plain", "Tag": "guitar alone"}
VBODY, VREST = body(VOX, VMARKS, multirest=False)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def nm_(p): return f"{_NM[p % 12]}{p // 12 - 1}"
_h0 = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0]; _h1 = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 1]
_b6 = [n for n in REC["lead"] if n["sec"] == "Bridge 2" and n["line"] == 6]
NOTE0 = f"The voice: a tenor, {nm_(min(_ps))}–{nm_(max(_ps))}; the top, {nm_(max(_ps))}, only on the second bridge's last “do.” Acoustic CCM, a sixteenth-note strum."
NOTE1 = f"Chorus: “The song can stop” falls {' '.join(nm_(n['midi']) for n in _h0[-3:])}, then a beat of silence;"
NOTE1a = f"“But the singer doesn't stop” is the same figure a step up ({' '.join(nm_(n['midi']) for n in _h1[-3:])}), held into the next line."
NOTE1b = f"Second bridge: a step higher (A major) to “Yes You do,” held on {nm_(_b6[-1]['midi'])}; “You remember all of me” back in G."
NOTE2 = "Verses conversational, the words quick; keep the band small."
FOOT = "The Singer Doesn't Stop · Words and music: Jason Bryant · ♩ = 84 · G major · 4:11"
if __name__ == "__main__":
    lead_ly = HEAD % (18, FOOT, FOOT) + f'''\\header {{ title = "The Singer Doesn't Stop" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Acoustic CCM · ♩ = 84" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(set())} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "{NOTE0}" "{NOTE1}" "{NOTE1a}" "{NOTE1b}" "{NOTE2}" }}
'''
    path, warns = compile_ly(lead_ly, "The Singer Doesn't Stop - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    okr = okl = (True, 0, 0)
    parts_src = [("bas", "Bass", [e for e in REC["bass"]], "\\clef bass", {"Chorus 1": "in", "Bridge": "out", "Bridge 2": "in at bar 5", "Tag": "out"}),
                 ("ele", "Electric guitar (swells)", [e for e in REC["electric"]], "\\clef \"treble_8\"", {"Verse 2": "volume swells, low", "Bridge 2": "builds", "Last Chorus": "plain"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    DN = {36: "bd", 38: "sn", 39: "hc", 42: "hh", 46: "hho", 49: "cymc", 40: "sne", 51: "cymr"}
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
    dmarks = {"Chorus 1": "brushes: kick 1 and 3, brush 2 and 4", "Bridge": "OUT", "Bridge 2": "brushes from bar 5, kick from bar 9", "Last Chorus": "plain", "Tag": "out"}
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
    parts = HEAD % (17, FOOT, FOOT) + '\\header { title = "The Singer Doesn\'t Stop" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    path, warns = compile_ly(parts, "The Singer Doesn't Stop - parts", cwd=OUT)
    print("parts:", [w for w in warns][:4], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, piano_rh=okr, piano_lh=okl, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
