"""'The Ratios Hold' (song 48) -- the lead sheet and the parts, written bar by bar from the song record (the events the demo plays, before
any humanizing). q = 92; E major; the instrumentals in 7/8 (grouped 2+2+3) and 5/4 where the record has them; grid: twelfths of a beat.
Chord symbols by the half-bar (the 438 chart) on the sung sections. Every pitched staff read back from LilyPond's MIDI."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p58"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p58/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
OUT = "/home/claude/p58/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); TOT = REC["end"]
BST = [x["start"] for x in BARS]; BLEN = [x["len"] for x in BARS]
def bar_of(t):
    lo, hi = 0, NB - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if BST[m] <= t: lo = m
        else: hi = m - 1
    return lo
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}             # E major: sharps
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {3: "16", 6: "8", 9: "8.", 12: "4", 18: "4.", 24: "2", 36: "2.", 48: "1"}
def split(pos, n, L):
    """a note of n twelfths at pos in a bar of L, written as tied values that keep the bar's beats (7/8: 2+2+3 eighths)."""
    groups = [0, 12, 24, 42] if L == 42 else list(range(0, L + 1, 12))
    out = []
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
METER_TOK = {"4/4": "\\time 4/4", "7/8": "\\time 2,2,3 7/8", "5/4": "\\time 5/4"}
REST_UNIT = {"4/4": ("1", 1), "7/8": ("8", 7), "5/4": ("4", 5)}
TEMPO = '\\tempo "Symphonic prog" 4 = 92'
def body(bybar, marks, multirest=True):
    toks = [TEMPO, "\\key e \\major"]; bi = 0; rest_bars = set(); met = None
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
CHR = {"E": "e", "B": "b", "C#m": "cis", "A": "a", "F#m": "fis", "G#m": "gis", "D": "d"}
QUAL = {"C#m": ":m", "F#m": ":m", "G#m": ":m"}
BASSN = {"C#": "cis", "G#": "gis", "E": "e", "A": "a", "B": "b", "F#": "fis", "D#": "dis"}
def cho(c, d):
    base, _, bs = c.partition("/")
    return f"{CHR[base]}{d}{QUAL.get(base, '')}" + (f"/{BASSN[bs]}" if bs else "")
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
SHORT = {"Overture": "I. Overture", "Verse 1": "II. Verse 1", "Study": "III. Study", "Window": "IV. Window", "Last Chorus": "V. Last Chorus"}
VBODY, VREST = body(VOX, VMARKS)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
_hk = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 3]
_b5 = [n for n in REC["lead"] if n["sec"] == "Bridge" and n["line"] == 5]
_mm = int(REC["seconds"] // 60); _ss = int(round(REC["seconds"] % 60))
NOTE0 = f"The voice: a high tenor, {nm_(min(_ps))}–{nm_(max(_ps))}; the top, {nm_(max(_ps))}, only on the bridge's “ready.”"
NOTE1 = f"Chorus: “The ratios hold” steps up {' '.join(nm_(n['midi']) for n in _hk[-3:])} and holds “hold” two beats; a beat of silence after."
NOTE1a = "Harmony: three parts on “The ratios hold” in every chorus and the tag, and on every line of the last chorus."
NOTE1b = f"Bridge: the first pair low, the second a step higher; “The instrument is ready” lands on {nm_(max(n['midi'] for n in _b5))}, held."
NOTE2 = "Verses: the words race in sixteenths; keep them light and conversational over the bass."
FOOT = f"The Ratios Hold · Words and music: Jason Bryant · ♩ = 92 · E major · {_mm}:{_ss:02d}"
if __name__ == "__main__":
    lead_ly = HEAD % (17, FOOT, FOOT) + f'''\\header {{ title = "The Ratios Hold" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Symphonic prog · ♩ = 92" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(VREST)} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "v" {{ {VBODY} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "{NOTE0}" "{NOTE1}" "{NOTE1a}" "{NOTE1b}" "{NOTE2}" }}
'''
    path, warns = compile_ly(lead_ly, "The Ratios Hold - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = readback("voice", VOX, VWANT); print("  readback voice:", "matches" if ok[0] else "MISMATCH", ok[1:])
    P_ = REC["parts"]
    mell = [dict(e) for e in P_.get("strings", []) + P_.get("choir", [])]
    parts_src = [("harm_hi", "Harmony vocal (high)", [dict(n, p=[n["midi"]]) for n in REC["harm_hi"]], "\\clef \"treble_8\"", {"Chorus 1": "the hook", "Last Chorus": "every line"}),
                 ("harm_lo", "Harmony vocal (low)", [dict(n, p=[n["midi"]]) for n in REC["harm_lo"]], "\\clef \"treble_8\"", {"Chorus 1": "the hook", "Last Chorus": "every line"}),
                 ("moog", "Moog lead", P_.get("moog", []), "", {"Overture": "the pattern theme, 2+2+3", "Study": "the theme; then the exchange", "Coda": "in quarters"}),
                 ("hammond", "Hammond organ", P_.get("hammond", []), "", {}),
                 ("organ", "Church organ", P_.get("organ", []), "", {"Last Chorus": "the summit"}),
                 ("mellotron", "Mellotron (strings; choir in the choruses)", mell, "", {"Chorus 1": "choir"}),
                 ("piano", "Piano", P_.get("piano", []), "\\clef bass", {"Window": "alone, softer each bar", "Bridge": "with the voice"}),
                 ("guitar", "Electric guitar (clean)", P_.get("guitar", []), "\\clef \"treble_8\"", {"Overture": "the hook's figure, foreshadowed", "Verse 1": "arpeggios"}),
                 ("acoustic", "Acoustic guitar", P_.get("acoustic", []), "\\clef \"treble_8\"", {"Study": "the interlude, alone"}),
                 ("bass", "Bass (pick)", P_.get("bass", []), "\\clef bass", {"Verse 1": "lead the verse", "Bridge": "in on the last pair"})]
    books = []; checks = {}
    for k, name, src, clef, marks in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, marks)
        checks[k] = readback(k, by, want)
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}
  \\new Staff {{ {clef} {bd} }} >> \\layout {{ }} }} }}''')
    DN = {36: "bd", 38: "sn", 37: "ss", 42: "hh", 46: "hho", 49: "cymc", 51: "cymr", 48: "tomh", 45: "tommh", 41: "tomfl"}
    HITS = collections.defaultdict(set)
    for e in P_.get("drums", []):
        for p in e["p"]: HITS[e["on"]].add(DN[p])
    def drumbar(bi):
        toks = []; st, L = BST[bi], BLEN[bi]; step = 12 if L != 42 else 6
        for b0 in range(0, L, step):
            base = st + b0; hs = [x for x in range(0, step, 3) if HITS.get(base + x)]
            if not hs: toks.append("r" + DUR[step]); continue
            if hs[0] > 0: toks.append("r" + DUR[hs[0]])
            for j, x in enumerate(hs):
                ln = (hs[j + 1] if j + 1 < len(hs) else step) - x
                toks.append("<" + " ".join(sorted(HITS[base + x])) + ">" + DUR[ln])
        return toks
    dmarks = {"Overture": "7/8: kick 1 and the third group, snare 2", "Verse 1": "light: rim on 2 and 4", "Chorus 1": "full", "Study": "7/8, 5/4, then 4/4",
              "Window": "OUT", "Bridge": "in on the last pair", "Last Chorus": "ride", "Coda": "half-time"}
    dt = []; bi = 0; met = None
    while bi < NB:
        if BARS[bi]["meter"] != met: met = BARS[bi]["meter"]; dt.append(METER_TOK[met])
        if bi in starts:
            if bi > 0: dt.append('\\bar "||"')
            tx = dmarks.get(starts[bi], ""); dt.append(f'\\mark \\markup \\box \\bold "{starts[bi]}{(" · " + tx) if tx else ""}"')
        if not any(HITS.get(BST[bi] + x) for x in range(0, BLEN[bi], 3)):
            run = 1
            while bi + run < NB and (bi + run) not in starts and BARS[bi + run]["meter"] == met and not any(HITS.get(BST[bi + run] + x) for x in range(0, BLEN[bi + run], 3)): run += 1
            u, k = REST_UNIT[met]; dt.append(f"R{u}*{k * run}"); bi += run; continue
        dt += drumbar(bi); bi += 1
    dt.append('\\bar "|."')
    books.append(f'''\\bookpart {{ \\header {{ subtitle = "Drums" }}
\\score {{ \\new DrumStaff \\with {{ drumStyleTable = #drums-style }} \\drummode {{ {" ".join(dt)} }} \\layout {{ }} }} }}''')
    nh = sum(len(v) for v in HITS.values()); nd = len({(e["on"], p) for e in P_.get("drums", []) for p in e["p"]})
    parts = HEAD % (16, FOOT, FOOT) + '\\header { title = "The Ratios Hold" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    path, warns = compile_ly(parts, "The Ratios Hold - parts", cwd=OUT)
    print("parts:", [w for w in warns][:6], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
