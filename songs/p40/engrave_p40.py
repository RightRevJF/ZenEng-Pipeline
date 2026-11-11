"""'Nothing Else on Earth' -- the lead sheet and the production parts (lead guitar, rhythm guitar, electric piano, strings, bass,
drums), written bar by bar from the song record (the events the demo plays, before any humanizing). 4/4 at q = 116, D major; grid: twelfths of a beat (a bar is 48).
Rehearsal marks, bar numbers, chord symbols; empty bars compressed. Every pitched staff read back from LilyPond's MIDI against the record."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p40"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p40/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; _ps = [n["midi"] for n in REC["lead"]]
RANGE = f"{_NM[min(_ps) % 12]}{min(_ps) // 12 - 1}–{_NM[max(_ps) % 12]}{max(_ps) // 12 - 1}"                # read from the record (v2)
OUT = "/home/claude/p40/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); BAR = 48; TOT = NB * BAR
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}
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
    toks = ["\\time 4/4", "\\tempo 4 = 116"] + (["\\key d \\major"] if key else []); bi = 0; rest_bars = set()
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
CHR = {"A": "a", "C": "c", "Em": "e", "D": "d", "Bm": "b", "G": "g", "N.C.": "r"}
QUAL = {"Em": ":m", "Bm": ":m"}
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
VMARKS = {"Intro": "the riff alone; drums at bar 5", "Verse 1": "half time", "Chorus 1": "full beat", "Verse 2": "half time", "Riff break": "guitar solo", "Outro": "the riff; one hit, let ring"}
VBODY, VREST = body(VOX, VMARKS)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
V2S = ""
_hk = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0]; _top = max(REC["lead"], key=lambda n: (n["midi"], -n["on"]))
_hold = max(_hk, key=lambda n: n["dur"])
NOTE1 = (f"The hook, “It used to taste like nothing else on earth,”" , f"sits {_NM[min(n['midi'] for n in _hk) % 12]}{min(n['midi'] for n in _hk) // 12 - 1}–{_NM[max(n['midi'] for n in _hk) % 12]}{max(n['midi'] for n in _hk) // 12 - 1}"
         f" and lands on “{_hold['text'].strip(',.:;')}” ({_NM[_hold['midi'] % 12]}{_hold['midi'] // 12 - 1}, bar {_hold['on'] // 48 + 1}, beat 1, held {_hold['dur'] // 12} beats).")
NOTE2 = f"The top note, {_NM[_top['midi'] % 12]}{_top['midi'] // 12 - 1}, is in the bridge (bar {_top['on'] // 48 + 1}, “{_top['text'].strip(',.:;')}”). Chorus 2 is chorus 1 again; the verses are half time."
NOTE3 = "The last chorus's last line returns the hook; “Nothing else on earth” tags it. Bar 110: one hit, let it ring."
FOOT = "Nothing Else on Earth · Words and music: Jason Bryant · ♩ = 116 · D major · 3:48"
if __name__ == "__main__":
    lead_ly = HEAD % (19, FOOT, FOOT) + f'''\\header {{ title = "Nothing Else on Earth" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Riff-led rock · ♩ = 116" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(set())} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "Mezzo, {RANGE}. {NOTE1[0]}" "{NOTE1[1]}" "{NOTE2}" "{NOTE3}" }}
'''
    path, warns = compile_ly(lead_ly, "Nothing Else on Earth - lead sheet", cwd=OUT)
    if os.environ.get("LEAD_ONLY"): print("lead sheet:", len(warns), "warnings"); print("  readback voice:", readback("voice", VOX, VWANT)); sys.exit(0)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    # ---- the parts ----
    parts_src = [("lgt", "Lead guitar (riff, fills, riff break)", "lgtr", '\\clef "treble_8"', {"Intro": "the riff, alone for 4 bars", "Chorus 1": "fills in the gaps", "Riff break": "solo, 8 bars", "Outro": "the riff, then one hit"}),
                 ("rgt", "Rhythm guitar", "rgtr", '\\clef "treble_8"', {"Verse 1": "let ring: 1 and the 'and' of 2", "Pre 1": "quarters", "Chorus 1": "open eighths", "Bridge": "held", "Outro": "one hit, let ring"}),
                 ("key", "Electric piano", "keys", "", {"Verse 1": "half notes", "Pre 1": "quarters", "Bridge": "arpeggio in eighths", "Riff break": "tacet", "Outro": "one chord, let ring"}),
                 ("str", "Strings (pad)", "strings", "", {"Pre 1": "swell", "Chorus 1": "held", "Verse 2": "tacet", "Outro": "one chord, let ring"}),
                 ("bas", "Bass", "bass", "\\clef bass", {"Verse 1": "in: the kick's half-time cell", "Pre 1": "quarters", "Chorus 1": "eighths: root, root, fifth, root, root, octave, fifth, approach", "Bridge": "quarters", "Outro": "roots; one hit"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in REC[src]]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    # drums: one staff, by the beat
    DN = {36: "bd", 38: "sn", 42: "hh", 46: "hho", 49: "cymc", 51: "cymr", 48: "tommh", 45: "tomml", 41: "tomfl"}
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
    dmarks = {"Intro": "in at bar 5, half time", "Verse 1": "half time: kick 1 and the 'and' of 2, snare 3, eighth hats", "Pre 1": "full beat: kick 1, 3 and the 'and' of 3, snare 2 and 4",
              "Chorus 1": "full beat; ride eighths; crash", "Bridge": "full beat, hats", "Riff break": "full beat, ride", "Last Chorus": "crash every 4 bars", "Outro": "half time; one hit on bar 110"}
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
    parts = HEAD % (17, FOOT, FOOT) + '\\header { title = "Nothing Else on Earth" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    path, warns = compile_ly(parts, "Nothing Else on Earth - parts", cwd=OUT)
    print("parts:", [w for w in warns][:4], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
