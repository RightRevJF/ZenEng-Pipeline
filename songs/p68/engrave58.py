"""'Same Time Tomorrow' (song 58) -- the lead sheet and the parts, written bar by bar from song_record.pkl (build58.py, from lyric58.song.json).
C major, q = 84, all 4/4; grid: twelfths of a beat. Chord symbols by the half-bar. The voices on treble_8 (sounding an octave lower).
Adapted from songs/p65/engrave_p65.py. Every pitched staff is read back from LilyPond's MIDI; the drums counted."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p68"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p68/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"]; _ps = [n["midi"] for n in REC["lead"]]
OUT = "/home/claude/p68/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); TOT = REC["end"]
BST = [x["start"] for x in BARS]; BLEN = [x["len"] for x in BARS]
def bar_of(t):
    lo, hi = 0, NB - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if BST[m] <= t: lo = m
        else: hi = m - 1
    return lo
SP = {0: "c", 1: "cis", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}             # C major
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
def tempo_tok(sec): return '\\tempo "Gently" 4 = 84' if sec == "Intro" else ""
def body(bybar, marks, multirest=True):
    toks = ["\\key c \\major"]; bi = 0; rest_bars = set(); met = None
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
ROOTN = {"C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "A": "a", "B": "b", "Bb": "bes", "Eb": "ees", "Ab": "aes", "F#": "fis"}
QUALN = {"": "", "m": ":m", "m7": ":m7", "add9": ":9^7", "sus2": ":sus2", "sus4": ":sus4", "maj7": ":maj7", "dim7": ":dim7"}
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
        if BARS[i].get('beats4'): out.append(' '.join(cho(c_, '4') for c_ in BARS[i]['beats4'])); i += 1; continue
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
HIM_N, HAR_N = staff_notes("him"), staff_notes("harmony")
HIM, HIM_W = pitched([dict(n, p=[n["midi"]]) for n in HIM_N]); HAR, HAR_W = pitched([dict(n, p=[n["midi"]]) for n in HAR_N])
HIM_L, HAR_L = lyr_of(HIM_N), lyr_of(HAR_N)
VMARKS = {}
HIM_B, HIM_R = body(HIM, VMARKS); HAR_B, _ = body(HAR, {})
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures }
  \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t \override MultiMeasureRest.minimum-length = #24 } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def line_notes(sec, i): return [n for n in REC["lead"] if n["sec"] == sec and n["line"] == i]
def words_of(ns):
    out, cur = [], ""
    for n in ns:
        if not n["first"]: continue
        cur += n["text"]
        if not n["hyph"]: out.append(cur); cur = ""
    return out
def title_desc(REC_):
    """where the title falls against the chorus's first bar, read from the record"""
    b0 = next(st for s, nb, st, _, _ in REC_["plan"] if s == "Chorus 1"); ns = [n for n in REC_["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0 and n["first"]]
    if ns[0]["on"] >= b0: return "on the chorus's downbeat", "Title on the downbeat."
    beat = (ns[0]["on"] % 48) // 12 + 1; land = next((n for n in ns if n["on"] >= b0), None); w = land["text"].strip(",.") if land else ""
    return (f"“{ns[0]['text']}” on beat {beat} of the bar before the chorus and “{w}” on its downbeat",
            f"The title picks up on beat {beat} of the bar before; “{w}” lands on the downbeat.")
_TD = title_desc(REC)
_mm = int(REC["seconds"] // 60); _ss = int(round(REC["seconds"] % 60))
_him = [n["midi"] for n in REC["lead"]]; _top = max(_him)
B1 = {s: st // 48 + 1 for s, nb, st, mets, mv in REC["plan"]}
_t = line_notes("Chorus 1", 0); _tw = [n for n in _t if n["first"]]
_tops = []
for s_ in ("Chorus 1", "Last Chorus"):
    for li in range(8):
        ns = line_notes(s_, li)
        if any(n["midi"] == _top for n in ns): _tops.append((s_, li + 1, ns[0]["on"] // 48 + 1))
NOTE0 = f"Voice: a baritone, {nm_(min(_him))}–{nm_(max(_him))}, written an octave above where he sings (treble clef with the 8 below)."
_topbars = sorted({n["on"] // 48 + 1 - B1["Chorus 1"] + 1 for n in REC["lead"] if n["sec"] == "Chorus 1" and n["midi"] == _top})
NOTE1 = (f"The title opens every chorus (bars {B1['Chorus 1']}, {B1['Chorus 2']} and {B1['Last Chorus']}): " + " ".join(nm_(n['midi']) for n in _tw) +
         f". The song’s top note, {nm_(_top)}, comes in bar{'s' if len(_topbars) > 1 else ''} " + " and ".join(map(str, _topbars)) + " of each chorus.")
NOTE2 = "A harmony voice sings under him in all three choruses, in his rhythm and words, mostly a third to a fifth below."
NOTE3 = "A folk ballad, ♩ = 84: the guitar strums eighths under him from bar 1 to the end; the bass on every beat; kick on 1 and 3, snare on 2 and 4, hat eighths."
TITLE = REC["title"]; FT = REC["file_title"]
FOOT = f"{TITLE} ({REC['edition']}) · Words and music: Jason Bryant · ♩ = 84, folk ballad · C major · {_mm}:{_ss:02d}"
CHN = lambda rest: f'\\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}'
_g = REC["parts"]["guitar"]; _b = REC["parts"]["bass"]
ROLE = {"him": "Voice: he tells it. Plain in the verses, a little more open in the choruses, which sit about three semitones higher. Sing the title as written: " + _TD[0] + ".",
        "harmony": f"Harmony voice: under him in the three choruses, in his rhythm and words, mostly a third to a fifth below (lowest {nm_(min(n['midi'] for n in REC['harm']))}). Keep it soft; he leads.",
        "guitar": f"Acoustic guitar: steady eighth-note strums from bar 1 to the end, under his voice. Where a chord tone would sit a step from the note he sings, it is left out. Range {nm_(min(min(e['p']) for e in _g))}–{nm_(max(max(e['p']) for e in _g))}.",
        "bass": f"Bass: quarter notes on every beat, roots and fifths, with chromatic passing notes a half step from the next root. {nm_(min(e['p'][0] for e in _b))}–{nm_(max(e['p'][0] for e in _b))}. Lock with the kick on 1 and 3.",
        "drums": f"Drums: kick 1 and 3, snare 2 and 4, hat eighths, from bar {min(x['on'] for x in REC['parts']['drums']) // 48 + 1} to the end. A tom fill in the bar before each chorus that follows a verse (bars {', '.join(str(b_) for b_ in sorted({x['on'] // 48 + 1 for x in REC['parts']['drums'] if x['p'][0] in (45, 48)}))})."}
VMARKS_P = {"guitar": {"Intro": "strum eighths throughout"},
            "bass": {"Intro": "quarters, roots and fifths"}, "him": {}, "harmony": {"Chorus 1": "under the lead"}}
DMARKS = {"Intro": "kick, snare, hats", "Chorus 1": "as before", "Bridge": "as before", "Outro": "to the end"}
if __name__ == "__main__":
    lead_ly = HEAD % (17, FOOT, FOOT) + f'''\\header {{ title = "{TITLE}" subtitle = "Lead sheet ({REC['edition']})" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\score {{ <<
  {CHN(HIM_R)}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "him" {{ {HIM_B} }} }}
  \\new Lyrics \\lyricsto "him" {{ {" ".join(HIM_L)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 \\wordwrap-string "{NOTE0}" \\vspace #0.3 \\wordwrap-string "{NOTE1}" \\vspace #0.3 \\wordwrap-string "{NOTE2}" \\vspace #0.3 \\wordwrap-string "{NOTE3}" }}
'''
    path, warns = compile_ly(lead_ly, f"{FT} - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = {k: readback(k, b_, w_) for k, b_, w_ in (("him", HIM, HIM_W),)}
    for k, v in ok.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    P_ = REC["parts"]
    parts_src = [("him", "Voice", [dict(n, p=[n["midi"]]) for n in HIM_N], '\\clef "treble_8"', HIM_L),
                 ("harmony", "Harmony vocal", [dict(n, p=[n["midi"]]) for n in HAR_N], '\\clef "treble_8"', HAR_L),
                 ("guitar", "Acoustic guitar", P_.get("guitar", []), '\\clef "treble_8"', None),
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
    dmarks = DMARKS
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
    parts = HEAD % (16, FOOT, FOOT) + f'\\header {{ title = "{TITLE}" subtitle = "Parts ({REC['edition']})" composer = "Words and music: Jason Bryant" tagline = ##f }}\n' + "\n".join(books)
    path, warns = compile_ly(parts, f"{FT} - parts", cwd=OUT)
    print("parts:", [w for w in warns][:6], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
