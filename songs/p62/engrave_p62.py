"""'The Room Next Door' (song 52) -- the lead sheet and the parts, written bar by bar from the song record (the events the demo plays, before
any humanizing). 6/8, dotted quarter = 54; D major; grid: twelfths of a quarter (a 6/8 bar of 36, its beats at 0 and 18). One chord a bar,
the writer's. Every pitched staff read back from LilyPond's MIDI."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p62"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p62/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
OUT = "/home/claude/p62/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); TOT = REC["end"]
BST = [x["start"] for x in BARS]; BLEN = [x["len"] for x in BARS]
def bar_of(t):
    lo, hi = 0, NB - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if BST[m] <= t: lo = m
        else: hi = m - 1
    return lo
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}             # D major: F and C sharp; B flat (B-flat major 7), C natural (Cadd9)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {3: "16", 6: "8", 9: "8.", 12: "4", 18: "4.", 24: "2", 36: "2.", 48: "1"}
def split(pos, n, L):
    """a note of n twelfths at pos in a bar of L, written as tied values that keep the bar's beats (7/8: 2+2+3 eighths)."""
    groups = [0, 12, 24, 42] if L == 42 else ([0, 18, 36] if L == 36 else list(range(0, L + 1, 12)))
    out = []
    while n > 0 and L == 36:                                                               # 6/8: nothing crosses the bar's middle beat but a whole bar's dotted half
        nxt_g = 18 if pos < 18 else 36
        if pos == 0 and n >= 36: Lx = 36
        elif pos in (0, 18) and n >= 18: Lx = 18
        elif pos % 6 == 0 and n >= 12 and pos + 12 <= nxt_g: Lx = 12
        elif pos % 6 == 0 and n >= 9 and pos + 9 <= nxt_g: Lx = 9
        elif pos % 6 == 0 and n >= 6: Lx = 6
        else: Lx = 3
        Lx = min(Lx, nxt_g - pos, L - pos)
        while Lx not in DUR: Lx -= 3
        out.append((pos, Lx)); pos += Lx; n -= Lx
    if L == 36: return out
    while n > 0:
        nxt_g = min(g for g in groups if g > pos) if any(g > pos for g in groups) else L
        if L == 48 and pos == 0 and n >= 48: Lx = 48
        elif L == 48 and pos == 0 and n >= 36: Lx = 36
        elif L == 48 and pos in (0, 24) and n >= 24: Lx = 24
        elif L == 48 and pos in (0, 24) and n >= 18: Lx = 18
        elif L == 42 and pos == 24 and n >= 18: Lx = 18
        elif pos % 12 == 0 and n >= 12 and pos + 12 <= nxt_g: Lx = 12
        elif pos % 12 == 0 and n >= 9: Lx = 9
        elif pos % 6 == 0 and n >= 6: Lx = 6
        else: Lx = 3
        if pos % 12: Lx = min(Lx, 12 - pos % 12)
        Lx = min(Lx, L - pos)
        while Lx not in DUR: Lx -= 3
        out.append((pos, Lx)); pos += Lx; n -= Lx
    return out
starts = {}
for s, nb, st, mets, mv in REC["plan"]: starts[bar_of(st)] = s
def pitched(notes):
    """notes: dicts with on, dur, p (list), art. Returns tokens per bar, and the pitch list read in order."""
    notes = sorted(notes, key=lambda n: (n["on"], -len(n["p"]))); cur = 0; seq = []
    dedup = []
    for n in notes:
        if dedup and dedup[-1]["on"] == n["on"]: dedup[-1] = dict(dedup[-1], p=sorted(set(dedup[-1]["p"] + n["p"]))); continue
        dedup.append(dict(n))
    notes = dedup
    for i, n in enumerate(notes):
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
            bi = bar_of(s); m = min(d, BST[bi] + BLEN[bi] - s)
            sp = split(s - BST[bi], m, BLEN[bi])
            for k, (pos, L) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = "r" + DUR[L]
                else:
                    ps = n["p"]; nm = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    tok = nm + DUR[L] + ("~" if tie else "")
                    if n.get("slur_open") and first: tok += "("
                    if n.get("slur_close") and not tie and k == len(sp) - 1 and m == d: tok += ")"
                    if first: want += sorted(ps)
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, want
METER_TOK = {"4/4": "\\time 4/4", "7/8": "\\time 2,2,3 7/8", "5/4": "\\time 5/4", "6/8": "\\time 6/8"}
REST_UNIT = {"4/4": ("1", 1), "7/8": ("8", 7), "5/4": ("4", 5), "6/8": ("2.", 1)}
TEMPO = '\\tempo "Gently rocking" 4. = 54'
def body(bybar, marks, multirest=True):
    toks = [TEMPO, "\\key d \\major"]; bi = 0; rest_bars = set(); met = None
    def has_(i): return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        if BARS[bi]["meter"] != met: met = BARS[bi]["meter"]; toks.append(METER_TOK[met])
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            txt = marks.get(starts[bi], ""); toks.append(f'\\mark \\markup \\box \\bold "{SHORT.get(starts[bi], starts[bi])}{(" · " + txt) if txt else ""}"')
        if multirest and not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and BARS[bi + run]["meter"] == met and not has_(bi + run): run += 1
            u, k = REST_UNIT[met]; toks.append(f"R{u}*{k * run}"); rest_bars.update(range(bi, bi + run)); bi += run; continue
        toks += bybar[bi]; bi += 1
    toks.append('\\bar "|."')
    return " ".join(toks), rest_bars
ROOTN = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F#": "fis", "G": "g", "Bb": "bes"}
QUALN = {"": "", "m": ":m", "m7": ":m7", "add9": ":9^7", "sus4": ":sus4", "maj7": ":maj7", "m9": ":m9", "7sus4": ":7sus4"}
def cho(c, d):
    base, _, bs = c.partition("/")
    rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]; q_ = base[len(rt_):]
    return f"{ROOTN[rt_]}{d}{QUALN[q_]}" + (f"/{ROOTN[bs]}" if bs else "")
def chords_for(rest_bars):
    out, i = [], 0
    while i < NB:
        met = BARS[i]["meter"]; u, k = REST_UNIT[met]
        if i in rest_bars:
            j = i
            while j + 1 < NB and (j + 1) in rest_bars and (j + 1) not in starts and BARS[j + 1]["meter"] == met: j += 1
            out.append(f"s{u}*{k * (j - i + 1)}"); i = j + 1; continue
        a_, b_ = BARS[i]['chord'], BARS[i]['chord2']
        if met == "4/4" and a_ != b_: out.append(f"{cho(a_, '2')} {cho(b_, '2')}")
        elif met == "6/8": out.append(cho(a_, "2."))
        else: out.append(cho(a_, f"{u}*{k}"))
        i += 1
    return " ".join(out)
def esc(t): return t.replace('"', '\\"')
def readback(name, bybar, want):
    toks = [re.sub(r"[()]", "", t) for b in sorted(bybar) for t in bybar[b] if not t.startswith(("r", "R"))]
    compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    return sorted(got) == sorted(want) and len(got) == len(want), len(got), len(want)
def nm_(p): return f"{_NM[p % 12]}{p // 12 - 1}"
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
VMARKS = {}
SHORT = {}
VBODY, VREST = body(VOX, VMARKS)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
chExceptionMusic = { <c e g d'>1-\markup { \super "add9" } }
chExceptions = #(append (sequential-music-to-chord-exceptions chExceptionMusic #t) ignatzekExceptions)
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def line_notes(sec, i): return [n for n in REC["lead"] if n["sec"] == sec and n["line"] == i]
_d = line_notes("Chorus 1", 4); _h2 = line_notes("Last Chorus", 5); _th = line_notes("Bridge", 3)
_mm = int(REC["seconds"] // 60); _ss = int(round(REC["seconds"] % 60))
NOTE0 = f"The voice: an alto, {nm_(min(_ps))}–{nm_(max(_ps))}. Count it in two: two dotted-quarter beats a bar, gently rocking."
NOTE1 = f"Chorus: “there's a door in the wall” lifts to {nm_(max(n['midi'] for n in _d))} on “door” ({nm_(max(_ps))} in the last chorus, the song's top), and leaves “wall” open on {nm_(_d[-1]['midi'])}."
NOTE1a = f"Final chorus: the hook twice; the second time “door” on {nm_(_h2[2]['midi'])} and “wall” home on {nm_(_h2[-1]['midi'])}, held into the outro. Harmony on every line."
NOTE1b = f"Bridge: a hush, piano and cello; “and you were there” lifts to {nm_(max(n['midi'] for n in _th))}, and “gone” holds open into the last verse."
NOTE2 = "Verses: close and plain, as if talking to him through the wall."
TITLE = REC["title"]; FT = REC["file_title"]
FOOT = f"{TITLE} (third edition) · Words and music: Jason Bryant · ♩. = 54, 6/8 · D major · {_mm}:{_ss:02d}"
if __name__ == "__main__":
    lead_ly = HEAD % (17, FOOT, FOOT) + f'''\\header {{ title = "{TITLE}" subtitle = "Lead sheet · third edition" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {chords_for(VREST)} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "{NOTE0}" "{NOTE1}" "{NOTE1a}" "{NOTE1b}" "{NOTE2}" }}
'''
    path, warns = compile_ly(lead_ly, f"{FT} - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    P_ = REC["parts"]
    HM = {"Chorus 1": "the hook", "Last Chorus": "every line"}
    parts_src = [("harm_hi", "Harmony vocal (high)", [dict(n, p=[n["midi"]]) for n in REC["harm_hi"]], "", {"Chorus 1": "with the words: the hook", "Last Chorus": "with the words: every line"}),
                 ("harm_lo", "Harmony vocal (low)", [dict(n, p=[n["midi"]]) for n in REC["harm_lo"]], "", {"Chorus 1": "ooh: the hook", "Last Chorus": "ooh: every line"}),
                 ("guitar", "Acoustic guitar", P_.get("guitar", []), "\\clef \"treble_8\"", {"Intro": "fingerpicked, alone; bass note on 1 and 4", "Bridge": "OUT", "Verse 4": "back in"}),
                 ("piano", "Piano", P_.get("piano", []), "", {"Chorus 1": "on the beats, soft", "Verse 2": "answers at the line ends", "Bridge": "held chords, very soft"}),
                 ("cello", "Cello", P_.get("cello", []), "\\clef bass", {"Chorus 2": "in: long notes", "Interlude": "the hook's tune", "Bridge": "with the piano"}),
                 ("bass", "Acoustic bass", P_.get("bass", []), "\\clef bass", {"Chorus 1": "in", "Bridge": "OUT", "Verse 4": "back in"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    nh = nd = 0
    parts = HEAD % (16, FOOT, FOOT) + f'\\header {{ title = "{TITLE}" subtitle = "Parts · third edition" composer = "Words and music: Jason Bryant" tagline = ##f }}\n' + "\n".join(books)
    path, warns = compile_ly(parts, f"{FT} - parts", cwd=OUT)
    print("parts:", [w for w in warns][:6], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print("  drums: none in this song")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
