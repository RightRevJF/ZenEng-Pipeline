"""'Before It's Done' (song 45) -- the lead sheet, the voice-and-guitar score (the whole song for one singer and one guitar: voice and
words, the guitar in notation and TAB, every note on its string and fret), and the parts (guitar, cello), written bar by bar from the song
record (the events the demo plays, before any humanizing). q = 72, 4/4; G major, the last chorus and the tag in A (sharps); grid: twelfths of
a beat. Rehearsal marks, bar numbers, chord symbols. Every pitched staff read back from LilyPond's MIDI."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/carol", "/home/claude/p49"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p49/song_record.pkl", "rb"))
_NM = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm_(p): return f"{_NM[p % 12]}{p // 12 - 1}"
_ps = [n["midi"] for n in REC["lead"]]; RANGE = f"{nm_(min(_ps))}–{nm_(max(_ps))}"
OUT = "/home/claude/p49/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); BAR = 48; TOT = NB * BAR
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}     # G and A major: sharps
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
LC0 = next(b0 for s, nb, b0, met in REC["plan"] if s == "Last Chorus")
def pitched(notes, rest="r", strings=False):
    """notes: dicts with on, dur, p (list), [sf]. Returns tokens per bar, and the pitch list read in order."""
    notes = sorted(notes, key=lambda n: n["on"]); cur = 0; seq = []
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
                if kind == "r": tok = rest + DUR[L]
                else:
                    ps = n["p"]
                    if strings: el = [f"{pname(p)}\\{st}" for p, (st, fr) in zip(ps, n["sf"])]
                    else: el = [pname(p) for p in ps]
                    nm = el[0] if len(el) == 1 and not strings else "<" + " ".join(el) + ">"
                    tok = nm + DUR[L] + ("~" if tie else "")
                    if n.get("slur_open") and first: tok += "("
                    if n.get("slur_close") and not tie and k == len(sp) - 1 and m == d: tok += ")"
                    if first: want += sorted(ps)
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, want
TEMPO = '\\tempo "Gently, fingerpicked" 4 = 72'
def body(bybar, marks, rehearsal=True, multirest=False, tempo=True, as_text=False, clefs=None, tacet=0):
    toks = ["\\time 4/4"] + ([TEMPO] if tempo else []) + ["\\key g \\major"]; bi = 0; clefs = clefs or {}; REST.clear()
    if tacet: toks += [f'\\mark \\markup \\box \\bold "Tacet: intro, verse 1, chorus 1"', f"R1*{tacet}"]; REST.update(range(tacet)); bi = tacet
    def has_(i): return any(t[0] not in "rs" for t in bybar.get(i, []))
    while bi < NB:
        if bi == LC0: toks.append("\\key a \\major")
        if bi in clefs: toks.append(f"\\clef {clefs[bi]}")
        if bi in starts and rehearsal:
            if bi > 0 and bi != LC0: toks.append('\\bar "||"')
            txt = marks.get(starts[bi], "")
            if as_text:
                if txt and bybar.get(bi):
                    bt = list(bybar[bi]); bt[0] += f'^\\markup \\italic \\small "{esc(txt)}"'; toks += bt; bi += 1; continue
            else: toks.append(f'\\mark \\markup \\box \\bold "{starts[bi]}{(" · " + txt) if txt else ""}"')
        if multirest and not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and (bi + run) != LC0 and not has_(bi + run): run += 1
            toks.append(f"R1*{run}"); REST.update(range(bi, bi + run)); bi += run; continue
        toks += bybar[bi]; bi += 1
    toks.append('\\bar "|."')
    return " ".join(toks)
# ---- chord names ----
CQ = {"G": "g", "Gsus4": "g:sus4", "Gres": "g", "D/F#": "d/fis", "Em7": "e:m7", "Cadd9": "c:9^7", "Am7": "a:m7", "Dsus4": "d:sus4", "D": "d", "E": "e",
      "A": "a", "Asus4": "a:sus4", "E/G#": "e/gis", "F#m7": "fis:m7", "Dadd9": "d:9^7", "Esus4": "e:sus4"}
CB = {"G": "g", "D": "d", "Em": "e:m", "C": "c", "Am": "a:m", "E": "e", "A": "a", "F#m": "fis:m"}
REST = set()
def chords_bars(rest=frozenset()):
    out, i = [], 0
    while i < NB:
        if i in rest:
            j = i
            while j + 1 < NB and (j + 1) in rest: j += 1
            out.append(f"s1*{j - i + 1}"); i = j + 1; continue
        r_, q_ = (CB[BARS[i]['chord']].split(":") + [""])[:2]; out.append(f"{r_}1" + (":" + q_ if q_ else "")); i += 1
    return " ".join(out)
def chords_shapes():
    out = []
    for bi in range(NB):
        sh = [REC["shape_at"][bi * 8 + e] for e in range(8)]; e = 0
        while e < 8:
            j = e
            while j + 1 < 8 and CQ[sh[j + 1]] == CQ[sh[e]]: j += 1
            for pos, L in split(e * 6, (j - e + 1) * 6): out.append(f"{CQ[sh[e]].split(':')[0].split('/')[0]}{DUR[L]}" + (":" + CQ[sh[e]].split(":")[1] if ":" in CQ[sh[e]] else "") + ("/" + CQ[sh[e]].split("/")[1] if "/" in CQ[sh[e]] else ""))
            e = j + 1
    return " ".join(out)
def esc(t): return t.replace('"', '\\"')
def readback(name, bybar, want, pre=""):
    toks = [re.sub(r"[()]", "", t) for b in sorted(bybar) for t in bybar[b] if not t.startswith(("r", "R", "s"))]
    toks = [re.sub(r"\\[1-6]", "", t) for t in toks]
    compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
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
VMARKS = {"Intro": "guitar alone", "Verse 1": "low and close", "Chorus 1": "fuller", "Verse 2": "cello enters", "Bridge": "lighter; building at the end",
          "Last Chorus": "up a step, to A; everything", "Tag": "let it go quiet"}
# ---- the guitar: two voices (the treble picking, the thumb's bass) ----
G_UP = [dict(e) for e in REC["gtr"] if e["voice"] == "up"]; G_BS = [dict(e) for e in REC["gtr"] if e["voice"] == "bass"]
GU, GUW = pitched(G_UP, strings=True); GB, GBW = pitched(G_BS, rest="s", strings=True)
GMARKS = {"Intro": "let ring; the last bar: the chorus's last four notes", "Verse 1": "thumb on 1 and 3; strings 3 2 1, then 3 2 3; let ring",
          "Chorus 1": "pinch the top string on 1; G-F♯-E-C in the bass", "Verse 2": "as verse 1", "Bridge": "quarters, let ring; strum the last two bars",
          "Last Chorus": "A: pinch on 1 and 3, fullest", "Tag": "quiet; end on D(add9), the last note with the voice"}
CMARKS = {"Verse 2": "long roots", "Chorus 2": "the high line", "Bridge": "low; swell into the lift", "Last Chorus": "half notes, singing", "Tag": "low; let the last D ring"}
CEL, CW = pitched([dict(e) for e in REC["cello"]])
CLEFS = {next(b0 for s, nb, b0, m in REC["plan"] if s == x): c for x, c in (("Chorus 2", "tenor"), ("Bridge", "bass"), ("Last Chorus", "tenor"), ("Tag", "bass"))}
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
chExceptionMusic = { <c e g d'>1-\markup { \super "add9" } }
chExceptions = #(append (sequential-music-to-chord-exceptions chExceptionMusic #t) ignatzekExceptions)
'''
FOOT = "Before It's Done · Words and music: Jason Bryant · ♩ = 72 · G major, the last chorus in A · 3:07"
_c0 = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0]; _c3 = [n for n in REC["lead"] if n["sec"] == "Chorus 1" and n["line"] == 3 and n["first"]]
_l3 = [n for n in REC["lead"] if n["sec"] == "Last Chorus" and n["line"] == 3 and n["first"]]; _end = REC["lead"][-1]
NOTE0 = f"The voice: a man's middle voice, {RANGE}. A fingerpicked ballad, ♩ = 72. G major; the last chorus and the tag a whole step up, in A."
NOTE1 = f"“Hold that thought”: “thought” is held two and a half beats on {nm_(_c0[2]['midi'])}; the guitar's sus4 resolves under it. In the last chorus “morning” is held on the same note, a step higher."
NOTE2 = f"“Before it’s done” steps down {' '.join(nm_(n['midi']) for n in _c3[-4:])} in the choruses, ending open on the 2nd; in the last chorus {' '.join(nm_(n['midi']) for n in _l3[-4:])}, home."
NOTE3 = f"The tag ends on {nm_(_end['midi'])}, the 2nd of A, over D: left open."
GSCORE_NOTE = ["Standard tuning, no capo. The TAB gives every note's string and fret; the stems-down notes are the thumb.",
               "Let everything ring: hold each chord shape for its half bar and lift only to change. Where the voice holds the fourth of a D (or of an E in A), the guitar plays the sus4 and resolves when the voice moves.",
               "The intro's last bar and the tag's last bar play the chorus's last four notes on the top strings; in the tag the last one arrives on the singer's note."]
def lead_sheet():
    src = HEAD % (18, FOOT, FOOT) + "\\paper { max-systems-per-page = 8 }\n" + f'''\\header {{ title = "Before It's Done" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "Ballad · ♩ = 72" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {chords_bars()} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "v" {{ {body(VOX, VMARKS)} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 {" ".join('\\wordwrap-string #"' + esc(t) + '"' for t in (NOTE0, NOTE1, NOTE2, NOTE3))} }}
'''
    return compile_ly(src, "Before It's Done - lead sheet", cwd=OUT)
def guitar_block(marks, tempo=True, as_text=False):
    up = body(GU, marks, tempo=tempo, as_text=as_text); bs = body(GB, {}, rehearsal=False, tempo=False)
    return up, bs
def voice_guitar_score():
    up, bs = guitar_block(GMARKS, tempo=False, as_text=True)
    src = HEAD % (16, FOOT, FOOT) + "\\paper { max-systems-per-page = 4 }\n" + f'''\\header {{ title = "Before It's Done" subtitle = "Voice and guitar: the whole song (notation and TAB)" composer = "Words and music: Jason Bryant" meter = "Ballad · ♩ = 72 · standard tuning, no capo" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {chords_shapes()} }}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "v" {{ {body(VOX, VMARKS)} }} }}
  \\new Lyrics \\lyricsto "v" {{ {" ".join(LYR)} }}
  \\new Staff \\with {{ instrumentName = "Guitar" \\omit StringNumber }} << \\clef "treble_8" \\new Voice {{ \\voiceOne {up} }} \\new Voice {{ \\voiceTwo {bs} }} >>
  \\new TabStaff \\with {{ instrumentName = "TAB" }} << \\new TabVoice {{ {strip_marks(up)} }} \\new TabVoice {{ {strip_marks(bs)} }} >>
>> \\layout {{ \\context {{ \\TabStaff \\remove "Bar_number_engraver" }} \\context {{ \\TabVoice \\omit Rest \\omit MultiMeasureRest \\omit Tie }} }} }}
\\markup \\small \\column {{ \\vspace #1 {" ".join('\\wordwrap-string #"' + esc(t) + '"' for t in GSCORE_NOTE)} }}
'''
    return compile_ly(src, "Before It's Done - voice and guitar score", cwd=OUT)
def strip_marks(t): return re.sub(r'\^\\markup \\italic \\small "[^"]*"', "", re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", re.sub(r'\\tempo "[^"]*" 4 = 72', "", t)))
def parts():
    up, bs = guitar_block(GMARKS)
    books = [f'''\\bookpart {{ \\header {{ subtitle = "Guitar (standard tuning, no capo): notation and TAB" }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {chords_shapes()} }}
  \\new Staff \\with {{ instrumentName = "Guitar" \\omit StringNumber }} << \\clef "treble_8" \\new Voice {{ \\voiceOne {up} }} \\new Voice {{ \\voiceTwo {bs} }} >>
  \\new TabStaff \\with {{ instrumentName = "TAB" }} << \\new TabVoice {{ {strip_marks(up)} }} \\new TabVoice {{ {strip_marks(bs)} }} >>
>> \\layout {{ \\context {{ \\TabStaff \\remove "Bar_number_engraver" }} \\context {{ \\TabVoice \\omit Rest \\omit MultiMeasureRest \\omit Tie }} }} }} }}''',
             (lambda cb: f'''\\bookpart {{ \\header {{ subtitle = "Cello" }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t chordNameExceptions = #chExceptions }} \\chordmode {{ {chords_bars(frozenset(REST))} }}
  \\new Staff \\with {{ instrumentName = "Cello" }} {{ \\clef bass {cb} }} >> \\layout {{ }} }} }}''')(body(CEL, CMARKS, multirest=True, clefs=CLEFS, tacet=next(b0 for s, nb, b0, m in REC['plan'] if s == 'Verse 2')))]
    src = HEAD % (16, FOOT, FOOT) + "\\paper { max-systems-per-page = 5 }\n" + '\\header { title = "Before It\'s Done" subtitle = "Parts" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + "\n".join(books)
    return compile_ly(src, "Before It's Done - parts", cwd=OUT)
if __name__ == "__main__":
    for nm, f in (("lead sheet", lead_sheet), ("voice and guitar score", voice_guitar_score), ("parts", parts)):
        path, warns = f(); print(nm + ":", len(warns), "warnings", warns[:3])
    checks = dict(voice=readback("voice", VOX, VWANT), guitar_treble=readback("gup", GU, GUW), guitar_thumb=readback("gbs", GB, GBW), cello=readback("vc", CEL, CW))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    # the TAB: every string and fret written is the record's
    tabw = [(p, st) for e in REC["gtr"] for p, (st, fr) in zip(e["p"], e["sf"])]
    tabok = all(0 <= p - REC["open"][st] <= 12 and (p - REC["open"][st]) == fr for e in REC["gtr"] for p, (st, fr) in zip(e["p"], e["sf"]))
    print("  TAB: strings and frets consistent with the pitches:", tabok, len(tabw), "notes")
    pickle.dump(dict(checks=checks, tab=(tabok, len(tabw))), open(f"{OUT}/readback.pkl", "wb"))
