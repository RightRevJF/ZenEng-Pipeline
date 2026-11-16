"""'The Man Mama Prayed I'd Be' (song 54) -- the lead sheet and the parts, written bar by bar from the song record (the events the demo plays,
before any humanizing). G major, q = 120, all 4/4; grid: twelfths of a beat. Chord symbols by the half-bar (the chart 438 drew). Two vocal
staves: him (treble_8, sounding an octave lower) and her (treble). Every pitched staff is read back from LilyPond's MIDI; the drums counted."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p64"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p64/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
OUT = "/home/claude/p64/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); TOT = REC["end"]
BST = [x["start"] for x in BARS]; BLEN = [x["len"] for x in BARS]
def bar_of(t):
    lo, hi = 0, NB - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if BST[m] <= t: lo = m
        else: hi = m - 1
    return lo
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}             # G major: F sharp
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
RAMP = {}
def tempo_tok(sec): return '\\tempo "Two-step" 4 = 120' if sec == "Intro" else ""
def body(bybar, marks, multirest=True):
    toks = ["\\key g \\major"]; bi = 0; rest_bars = set(); met = None
    def has_(i): return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        if BARS[bi]["meter"] != met: met = BARS[bi]["meter"]; toks.append(METER_TOK[met])
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            txt = marks.get(starts[bi], ""); sec_ = starts[bi]
            if sec_ in RAMP: txt = (txt + "; " if txt else "") + ("accel." if RAMP[sec_][1] > RAMP[sec_][0] else "rit.") + f" to {RAMP[sec_][1]}"
            if bi == 0: toks.append(tempo_tok(sec_))
            toks.append(f'\\mark \\markup \\box \\bold "{SHORT.get(sec_, sec_)}{(" · " + txt) if txt else ""}"')
        if multirest and not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and BARS[bi + run]["meter"] == met and not has_(bi + run): run += 1
            u, k = REST_UNIT[met]; toks.append(f"R{u}*{k * run}"); rest_bars.update(range(bi, bi + run)); bi += run; continue
        toks += bybar[bi]; bi += 1
    toks.append('\\bar "|."')
    return " ".join(toks), rest_bars
ROOTN = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F#": "fis", "G": "g"}
QUALN = {"": "", "m": ":m", "m7": ":m7", "add9": ":9^7", "sus2": ":sus2", "sus4": ":sus4", "maj7": ":maj7", "dim7": ":dim7"}
def cho(c, d):
    base, _, bs = c.partition("/")
    rt_ = base[:2] if len(base) > 1 and base[1] == "#" else base[:1]; q_ = base[len(rt_):]
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
SHORT = {}
def staff_notes(who):
    """a vocal staff's notes: the lead and the other voices sung by who ('him', 'her', 'harmony')."""
    out = [dict(n) for n in REC["lead"] if n["singer"] == who] + [dict(n) for n in REC["harm"] if n["singer"] == who]
    out.sort(key=lambda n: n["on"])
    groups = collections.defaultdict(list)
    for n in out: groups[(n["sec"], n["line"], n["syl"], n["singer"])].append(n)
    for g in groups.values():
        g.sort(key=lambda n: n["on"])
        if len(g) > 1: g[0]["slur_open"] = True; g[-1]["slur_close"] = True
    return out
def lyr_of(ns):
    L_ = []
    for n in ns:
        if not n["first"]: continue
        w = n["text"].replace("'", "’"); q = '"' + esc(w) + '"' if re.search(r"[’?!,.;:\"—]", w) or w in ("_",) else w
        L_.append(q + (" --" if n["hyph"] else ""))
    return L_
HIM_N, HER_N, HAR_N = staff_notes("him"), staff_notes("her"), staff_notes("harmony")
HIM, HIM_W = pitched([dict(n, p=[n["midi"]]) for n in HIM_N]); HER, HER_W = pitched([dict(n, p=[n["midi"]]) for n in HER_N])
HAR, HAR_W = pitched([dict(n, p=[n["midi"]]) for n in HAR_N])
HIM_L, HER_L, HAR_L = lyr_of(HIM_N), lyr_of(HER_N), lyr_of(HAR_N)
VMARKS = {}
HIM_B, HIM_R = body(HIM, VMARKS); HER_B, HER_R = body(HER, {}); HAR_B, _ = body(HAR, {})
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures }
  \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t \override MultiMeasureRest.minimum-length = #24 } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def line_notes(sec, i): return [n for n in REC["lead"] if n["sec"] == sec and n["line"] == i]
_h = line_notes("Chorus 1", 5); _h4 = line_notes("Chorus 4", 5)
_mm = int(REC["seconds"] // 60); _ss = int(round(REC["seconds"] % 60))
_him = [n["midi"] for n in REC["lead"] if n["singer"] == "him"]; _her = [n["midi"] for n in REC["lead"] if n["singer"] == "her"]
NOTE0 = f"Him: a baritone, {nm_(min(_him))}–{nm_(max(_him))}, written an octave above where he sings (treble clef with the 8 below). Her: {nm_(min(_her))}–{nm_(max(_her))}, as written."
NOTE1 = f"The hook, choruses 1–3: “The man Mama prayed he’d (I’d) be” climbs to {nm_(max(n['midi'] for n in _h))} on “Ma-” and stops on {nm_(_h[-1]['midi'])} over D: open. He isn’t that man yet."
NOTE2 = f"Chorus 4 (her): the same climb, and “be” comes home to {nm_(_h4[-1]['midi'])} over G. He joins under her on the title line. Tag: he sings his line with her above, then she sings hers with him an octave below, both home on G."
NOTE3 = "Verse 4’s last bar: the band stops on beat 3 after “kiss”; she comes in on her own. Two-step feel: the bass on 1 and 3, the snare on 2 and 4."
TITLE = REC["title"]; FT = REC["file_title"]
FOOT = f"{TITLE} · Words and music: Jason Bryant · ♩ = 120, country two-step · G major · {_mm}:{_ss:02d}"
CHN = lambda rest: f'\\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}'
ROLE = {"him": "Him: the lead. He tells the story (verses 1–4) and sings choruses 1–3; under her hook in chorus 4; the tag’s first line.",
        "her": "Her: chorus 4 is hers alone. In the tag she sings above his line, then her own line, home on G.",
        "harmony": "Harmony voice: a third above him on the hook in choruses 1–3, and on chorus 3’s middle lines. Blend under him; never over.",
        "acoustic": "Acoustic guitar: the floor of the song. Boom-chick in the verses (the root on 1, the fifth on 3, the chord on 2 and 4); straight eighths in the choruses. Stops on beat 3 of verse 4’s last bar.",
        "tele": "Telecaster: short answers in the gaps, never under a sung word. Clean, a little twang, double-stops on the first note of a fill.",
        "fiddle": "Fiddle: plays the hook in the intro, the turnaround and the ending (the last time home to G). Long notes under choruses 3 and 4 and the tag.",
        "steel": "Pedal steel: swells under the chords; answers in the verse gaps (a bend from the note above). It carries the turnaround’s second half.",
        "piano": "Piano: light, offbeat chords (2 and 4) from chorus 2 on; the last G rings.",
        "bass": "Bass: a two-step. On 1 and 3 with the kick; roots and fifths with walks between chords. Stops with the band on beat 3 of verse 4’s last bar.",
        "drums": "Drums: a two-step with sticks. Kick 1 and 3, snare 2 and 4, hat eighths; cross-stick in verse 1, the intro and the early verse 4; ride in choruses 3 and 4. The stop before chorus 4."}
VMARKS_P = {
    "acoustic": {"Verse 1": "boom-chick", "Chorus 1": "straight eighths", "Verse 4": "stop on beat 3 of the last bar"},
    "tele": {"Verse 2": "fills in the gaps", "Chorus 1": "short fills"},
    "fiddle": {"Intro": "the hook", "Chorus 3": "long notes", "Turnaround": "the hook", "Ending": "the hook, home"},
    "steel": {"Intro": "swell", "Verse 1": "answers", "Chorus 1": "swells", "Turnaround": "bars 3–4"},
    "piano": {"Chorus 2": "in: offbeats"},
    "bass": {"Intro": "root–five", "Verse 1": "two-step", "Verse 4": "stop on beat 3 of the last bar"},
    "him": {}, "her": {"Chorus 4": "her chorus"}, "harmony": {"Chorus 1": "on the hook"}}
if __name__ == "__main__":
    lead_ly = HEAD % (17, FOOT, FOOT) + f'''\\header {{ title = "{TITLE}" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\score {{ <<
  {CHN(HIM_R & HER_R)}
  \\new Staff \\with {{ instrumentName = "Him" }} {{ \\clef "treble_8" \\new Voice = "him" {{ {HIM_B} }} }}
  \\new Lyrics \\lyricsto "him" {{ {" ".join(HIM_L)} }}
  \\new Staff \\with {{ instrumentName = "Her" }} {{ \\clef "treble" \\new Voice = "her" {{ {HER_B} }} }}
  \\new Lyrics \\lyricsto "her" {{ {" ".join(HER_L)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 \\wordwrap-string "{NOTE0}" \\vspace #0.3 \\wordwrap-string "{NOTE1}" \\vspace #0.3 \\wordwrap-string "{NOTE2}" \\vspace #0.3 \\wordwrap-string "{NOTE3}" }}
'''
    path, warns = compile_ly(lead_ly, f"{FT} - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = {k: readback(k, b_, w_) for k, b_, w_ in (("him", HIM, HIM_W), ("her", HER, HER_W))}
    for k, v in ok.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    P_ = REC["parts"]
    parts_src = [("him", "Him (lead vocal)", [dict(n, p=[n["midi"]]) for n in HIM_N], '\\clef "treble_8"', HIM_L),
                 ("her", "Her (vocal)", [dict(n, p=[n["midi"]]) for n in HER_N], '\\clef "treble"', HER_L),
                 ("harmony", "Harmony vocal", [dict(n, p=[n["midi"]]) for n in HAR_N], '\\clef "treble_8"', HAR_L),
                 ("acoustic", "Acoustic guitar", P_.get("acoustic", []), '\\clef "treble_8"', None),
                 ("tele", "Telecaster", P_.get("tele", []), '\\clef "treble_8"', None),
                 ("fiddle", "Fiddle", P_.get("fiddle", []), '\\clef "treble"', None),
                 ("steel", "Pedal steel", P_.get("steel", []), '\\clef "treble_8"', None),
                 ("piano", "Piano", P_.get("piano", []), '\\clef "treble"', None),
                 ("bass", "Bass", P_.get("bass", []), '\\clef "bass_8"', None)]
    books = []; checks = {}
    for k, name, src, clef, lyr in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, VMARKS_P.get(k, {}))
        checks[k] = readback("part_" + k, by, want)
        vo = f'\\new Voice = "pv{k}" {{ {bd} }}' if lyr else bd
        ly = f'\\new Lyrics \\lyricsto "pv{k}" {{ {" ".join(lyr)} }}' if lyr else ""
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\markup \\small \\wordwrap {{ {esc(ROLE[k])} }}
\\score {{ << {CHN(rest)}
  \\new Staff {{ {clef} {vo} }} {ly} >> \\layout {{ }} }} }}''')
    DN = {36: "bd", 38: "sn", 37: "ss", 42: "hh", 46: "hho", 49: "cymc", 51: "cymr", 48: "tomh", 45: "tommh", 41: "tomfl"}
    HITS = collections.defaultdict(set)
    for e in P_.get("drums", []):
        for p in e["p"]: HITS[e["on"]].add(DN[p])
    def drumbar(bi):
        toks = []; st, L = BST[bi], BLEN[bi]; step = 12
        for b0 in range(0, L, step):
            base = st + b0; hs = [x for x in range(0, step, 3) if HITS.get(base + x)]
            if not hs: toks.append("r" + DUR[step]); continue
            if hs[0] > 0: toks.append("r" + DUR[hs[0]])
            for j, x in enumerate(hs):
                ln = (hs[j + 1] if j + 1 < len(hs) else step) - x
                toks.append("<" + " ".join(sorted(HITS[base + x])) + ">" + DUR[ln])
        return toks
    dmarks = {"Intro": "cross-stick", "Verse 1": "cross-stick", "Chorus 1": "snare 2 and 4; crash", "Verse 2": "sticks", "Chorus 3": "ride", "Turnaround": "fill in bar 4",
              "Verse 4": "cross-stick, then sticks from bar 9; STOP on beat 3 of bar 16", "Chorus 4": "ride; crash on each line", "Tag": "easing; cross-stick from bar 3", "Ending": "kick and crash on the last G"}
    dt = []; bi = 0
    dt.append("\\time 4/4")
    while bi < NB:
        if bi in starts:
            if bi > 0: dt.append('\\bar "||"')
            tx = dmarks.get(starts[bi], "")
            if bi == 0: dt.append(tempo_tok("Intro"))
            dt.append(f'\\mark \\markup \\box \\bold "{starts[bi]}{(" · " + tx) if tx else ""}"')
        if not any(HITS.get(BST[bi] + x) for x in range(0, BLEN[bi], 3)):
            run = 1
            while bi + run < NB and (bi + run) not in starts and not any(HITS.get(BST[bi + run] + x) for x in range(0, BLEN[bi + run], 3)): run += 1
            dt.append(f"R1*{run}"); bi += run; continue
        dt += drumbar(bi); bi += 1
    dt.append('\\bar "|."')
    books.append(f'''\\bookpart {{ \\header {{ subtitle = "Drums" }}
\\markup \\small \\wordwrap {{ {esc(ROLE["drums"])} }}
\\score {{ \\new DrumStaff \\with {{ drumStyleTable = #drums-style }} \\drummode {{ {" ".join(dt)} }} \\layout {{ }} }} }}''')
    nh = sum(len(v) for v in HITS.values()); nd = len({(e["on"], p) for e in P_.get("drums", []) for p in e["p"]})
    parts = HEAD % (16, FOOT, FOOT) + f'\\header {{ title = "{TITLE}" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }}\n' + "\n".join(books)
    path, warns = compile_ly(parts, f"{FT} - parts", cwd=OUT)
    print("parts:", [w for w in warns][:6], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
