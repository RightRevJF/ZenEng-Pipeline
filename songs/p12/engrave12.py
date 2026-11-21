"""Wood and Cloth (second edition): the hymnal page, the organ score and the lead sheet, written from song_record.json in sounding pitch,
spelled from D major (A-sharp in the F#7, B-flat only in stanza 4's G minor 6). After compiling, each staff is read back from LilyPond's
MIDI and compared with the record. No engine terms on any page."""
import json, subprocess, os
import mido
import lyric_p12 as L
H = "/home/claude/zeneng-pipeline/songs/p12"; OUT = f"{H}/out"; os.makedirs(OUT, exist_ok=True)
R = json.load(open(f"{H}/song_record.json")); V = R["voices"]; BAR = 36; END = R["end"]; ST = {int(k): v for k, v in R["stanza_offsets"].items()}
ED = L.EDITION; TITLE = L.TITLE
GM6 = (ST[4] + 13 * BAR, ST[4] + 14 * BAR)
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}
def pname(m, t, flat_bes=False):
    if isinstance(m, list): return "<" + " ".join(pname(q, t, flat_bes) for q in m) + ">"
    n = SP[m % 12]
    if m % 12 == 10 and (flat_bes or GM6[0] <= t < GM6[1]): n = "bes"
    o = m // 12 - 1 - 3
    return n + ("'" * o if o > 0 else "," * (-o))
DUR = {6: "8", 12: "4", 18: "4.", 24: "2", 36: "2."}
def segs(t, d):
    out = []
    while d > 0:
        nxt = (t // BAR + 1) * BAR; s = min(d, nxt - t)
        while s > 0:
            for L_ in (36, 24, 18, 12, 6):
                if L_ <= s and (L_ <= 6 or t % 12 == 0 or (L_ == 18 and t % BAR == 18)): break
            else: L_ = 6
            out.append((t, L_)); t += L_; s -= L_; d -= L_
    return out
def rest_toks(t, d, spacer=False):
    toks = []; r = "s" if spacer else "r"
    for a, s in segs(t, d):
        toks.append(("s2." if spacer else "R2.") if (s == 36 and a % BAR == 0) else (r + DUR[s]))
    return toks
def gap(t, d, hide):
    """rests, or spacers inside the ranges where another voice on the staff carries the music"""
    out = []
    while d > 0:
        h = next(((a, b) for a, b in hide if a <= t < b), None)
        nxt = min([b for a, b in hide if a <= t < b] + [a for a, b in hide if a > t] + [t + d])
        out += rest_toks(t, nxt - t, spacer=bool(h)); d -= nxt - t; t = nxt
    return out
def voice_ly(ev, end, dyn=None, fermata_last=True, slurs=False, t0=0, marks=None, hide=(), holds=()):
    toks = []; t = t0; dyn = dyn or {}; marks = marks or {}
    for i, e in enumerate(ev):
        if e["on"] > t: toks += gap(t, e["on"] - t, hide)
        ss = segs(e["on"], e["dur"])
        for j, (a, s) in enumerate(ss):
            tk = pname(e["p"], a) + DUR[s]
            if j == 0 and e["on"] in dyn: tk += dyn[e["on"]]
            if j == 0 and e["on"] in marks: tk += marks[e["on"]]
            if j == len(ss) - 1 and fermata_last and ((i == len(ev) - 1 and e["on"] + e["dur"] == end) or e["on"] + e["dur"] in holds): tk += "\\fermata"
            if j < len(ss) - 1: tk += "~"
            if slurs and j == 0 and e.get("slur"): tk += "("
            if slurs and j == len(ss) - 1 and e.get("melisma"): tk += ")"
            toks.append(tk)
        t = e["on"] + e["dur"]
    if t < end: toks += gap(t, end - t, hide)
    return " ".join(toks)
def lyr(line):
    return " ".join(w.replace('"', '\\"') + (" --" if joins else "") for w, _, joins in L.syls(line))
def stanza_text(i): return " ".join(lyr(l) for l in L.STANZAS[i])
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #%s
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
'''
FOOT = f"{TITLE}{ED} · Words and music: Jason Bryant · D major · 3/4, felt in one (dotted half = c. 33; quarter = 100)"
TEMPO = '\\tempo \\markup { "Flowing, felt in one" \\normal-text { "(" \\note {2.} #UP "= c. 33;" \\note {4} #UP "= 100)" } }'
def compile_ly(src, base):
    p = f"{OUT}/{base}.ly"; open(p, "w").write(src)
    r = subprocess.run(["lilypond", "-dno-point-and-click", "-o", f"{OUT}/{base}", p], capture_output=True, text=True)
    errs = [l for l in r.stderr.splitlines() if "error" in l.lower()]
    if r.returncode or errs: raise RuntimeError(r.stderr[-3000:])
    return [l for l in r.stderr.splitlines() if "warning" in l.lower()]
# ---------------- the hymnal page: stanza 1's events (bars 5-20) moved to bar 1 ----------------
def stanza_events(v, s):
    a, b = ST[s], ST[s] + 16 * BAR
    return [dict(e, on=e["on"] - a) for e in V[v] if a <= e["on"] < b]
def hymnal():
    g = "\\time 3/4 \\key d \\major " + TEMPO + " " + " ".join(("s2. \\break" if b in (4, 8, 12) else "s2.") for b in range(1, 17)) + ' \\bar "|."'
    sop = voice_ly(stanza_events("S", 1), 16 * BAR, slurs=True); alt = voice_ly(stanza_events("A", 1), 16 * BAR)
    ten = voice_ly(stanza_events("T", 1), 16 * BAR); bas = voice_ly(stanza_events("B", 1), 16 * BAR)
    lys = "\n".join(f'    \\new Lyrics \\lyricsto "sop" {{ \\set stanza = "{i + 1}." {stanza_text(i)} }}' for i in range(5))
    src = HEAD % (16, 9, FOOT, FOOT) + "\\paper { page-count = 1 print-page-number = ##f }\n" + f'''\\layout {{ \\context {{ \\Score \\remove "Bar_number_engraver" }} \\context {{ \\Lyrics \\override LyricText.font-size = #-0.5 \\override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #0.6 }} }}
\\header {{ title = "{TITLE}" subtitle = \\markup \\italic \\small "She wrapped him in swaddling clothes, and laid him in a manger. Luke 2:7" tagline = ##f }}
\\markup \\fill-line {{ \\bold \\large "1" \\smallCaps "Christmas" }}
\\score {{
  \\new ChoirStaff <<
    \\new Staff = "sa" << \\new Voice {{ {g} }} \\new Voice = "sop" {{ \\voiceOne {sop} }} \\new Voice = "alt" {{ \\voiceTwo {alt} }} >>
{lys}
    \\new Staff = "tb" << \\clef bass \\new Voice {{ {g} }} \\new Voice = "ten" {{ \\voiceOne {ten} }} \\new Voice = "bas" {{ \\voiceTwo {bas} }} >>
  >>
  \\layout {{ }}
}}
\\markup \\vspace #1
\\markup \\fill-line {{ \\column {{ \\small "WORDS AND MUSIC: Jason Bryant, 2026" }} \\column {{ \\right-align \\small \\smallCaps "Arimathea" \\right-align \\small "87 87" }} }}
\\markup \\vspace #0.6
\\markup \\small \\italic \\wordwrap {{ Stanza 2: Luke 2:7; Matthew 27:57–60. The second Joseph is Joseph of Arimathea, who wrapped Jesus' body in linen for burial. }}
\\markup \\small \\italic \\wordwrap {{ Stanza 4 is sung by the choir alone, unaccompanied, in its own setting (printed in the organ score); the congregation rejoins at stanza 5. }}
'''
    return src
# ---------------- the organ score (full score): 88 bars ----------------
MARKS = {1: "Organ: introduction (the last line)", 5: "Stanza 1", 21: "Stanza 2", 37: "Stanza 3", 53: "Stanza 4: choir alone, unaccompanied",
         69: "Organ: link (from the choir's D)", 73: "Stanza 5: all on the tune (men an octave lower), sopranos' descant"}
REG = {1: ["Gt. Diapasons 8′ 4′, Sw. to Gt.", "Ped. Bourdon 16′, Principal 8′"], 21: ["add Gt. Fifteenth 2′"],
       37: ["Sw. Flutes 8′ 4′ (manuals only)"], 52: ["Hold; release as the choir breathes"], 53: ["Organ silent"], 69: ["Gt. Diapasons 8′ 4′ 2′, Mixture, Sw. Reeds to Gt.", "Ped. 16′ 8′ 4′, Gt. to Ped."],
       73: ["Full organ"]}
def organ_global():
    g = ['\\time 3/4', '\\key d \\major', TEMPO]
    for b in range(1, 89):
        if b in MARKS: g.append(f'\\mark \\markup \\small \\bold "{MARKS[b]}"')
        g.append('s2.')
        if b in (4, 20, 36, 52, 68, 72): g.append('\\bar "||"')
        if b == 88: g.append('\\bar "|."')
        elif b % 4 == 0: g.append('\\break')
    return " ".join(g)
def reg_voice():
    out = []
    for b in range(1, 89):
        out.append('s2.^\\markup \\tiny \\italic \\column { ' + " ".join(f'"{x}"' for x in REG[b]) + ' }' if b in REG else 's2.^\\markup \\italic "broaden"' if b == 87 else "s2.")
    return " ".join(out)
DYN_S = {ST[1]: "\\mf", ST[3]: "\\p", ST[4]: "\\mp", ST[5]: "\\f"}
DYN_O = {0: "\\mf", ST[3]: "\\p", R["link"]: "\\mf\\<", ST[5]: "\\f"}
def organ_score():
    G = organ_global()
    HOLD = (ST[4],)
    sop = voice_ly(V["S"], END, DYN_S, slurs=True, holds=HOLD); alt = voice_ly(V["A"], END, hide=[(ST[5], END)], holds=HOLD); ten = voice_ly(V["T"], END, holds=HOLD, marks={ST[5]: "^\\markup \\tiny \\italic \"men, on the tune\""}); bas = voice_ly(V["B"], END, hide=[(ST[5], END)], holds=HOLD)
    des = voice_ly(V["Desc"], END, {ST[5]: "\\f"}, slurs=True, marks={ST[5] + 14 * BAR: "^\\markup \\italic \"broaden\""})
    orh = voice_ly(V["org_rh"], END, DYN_O, holds=HOLD); olh = voice_ly(V["org_lh"], END, holds=HOLD); oped = voice_ly(V["org_ped"], END, holds=HOLD)
    ly_all = " ".join(f'\\set stanza = "{i + 1}." {stanza_text(i)}' for i in range(5))
    KEEP = "\\with { \\override VerticalAxisGroup.remove-empty = ##f }"
    src = HEAD % (14, 13, FOOT, FOOT) + f'''\\layout {{ \\context {{ \\Score \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
          \\context {{ \\Staff \\RemoveAllEmptyStaves }} \\context {{ \\Lyrics \\override LyricText.font-size = #-0.6 }} }}
global = {{ {G} }}
\\header {{ title = "{TITLE}" subtitle = "Organ score with choir{ED}" composer = "Words and music: Jason Bryant" poet = "Tune: ARIMATHEA, 87 87" tagline = ##f }}
\\score {{ <<
  \\new Staff = "desc" \\with {{ instrumentName = "Descant" shortInstrumentName = "Desc." }} << \\new Voice {{ \\global }} \\new Voice = "desc" {{ {des} }} >>
  \\new Lyrics \\lyricsto "desc" {{ {stanza_text(4)} }}
  \\new ChoirStaff <<
    \\new Staff = "sa" \\with {{ instrumentName = "S A" shortInstrumentName = "S A" }} << \\new Voice {{ \\global }} \\new Voice = "sop" {{ \\voiceOne {sop} }} \\new Voice = "alt" {{ \\voiceTwo {alt} }} >>
    \\new Lyrics \\lyricsto "sop" {{ {ly_all} }}
    \\new Staff = "tb" \\with {{ instrumentName = "T B" shortInstrumentName = "T B" }} << \\clef bass \\new Voice {{ \\global }} \\new Voice = "ten" {{ \\voiceOne {ten} }} \\new Voice = "bas" {{ \\voiceTwo {bas} }} >>
  >>
  \\new PianoStaff \\with {{ instrumentName = "Organ" shortInstrumentName = "Org." }} <<
    \\new Staff = "rh" {KEEP} << \\new Voice {{ \\global }} \\new Voice {{ {reg_voice()} }} \\new Voice {{ {orh} }} >>
    \\new Staff = "lh" {KEEP} << \\clef bass \\new Voice {{ \\global }} \\new Voice {{ {olh} }} >>
  >>
  \\new Staff = "ped" \\with {{ instrumentName = "Pedal" shortInstrumentName = "Ped." \\override VerticalAxisGroup.remove-empty = ##f }} << \\clef bass \\new Voice {{ \\global }} \\new Voice {{ {oped} }} >>
>> \\layout {{ }} }}
\\markup \\vspace #1
\\markup \\small \\italic \\wordwrap {{ Stanza 2: the second Joseph is Joseph of Arimathea, who wrapped Jesus' body in linen for burial (Luke 2:7; Matthew 27:57–60). }}
\\markup \\small \\italic \\wordwrap {{ Into stanza 4: the organ holds stanza 3's last chord (D major) and releases as the choir breathes; the choir's first chord, B minor, shares its D and F-sharp. Out of stanza 4: the link begins on D, the chord the choir ends on. }}
'''
    return src
# ---------------- the lead sheet: the tune, the chords as the hymnal sings them, five stanzas ----------------
CHN = {"D": "d", "Bm": "b:m", "G": "g", "A": "a", "E7": "e:7", "F#7": "fis:7", "Em7": "e:m7", "A7": "a:7", "Bm7": "b:m7", "Em": "e:m", "F#m": "fis:m", "Gm6": "g:m6"}
def chord_line():
    """one chord per change, as the four-part setting sings it (the downbeat chords are the hymn's plan; changes inside a bar shown)"""
    toks = []; t = 0; prev = None
    tune = R["tune"]; path = R["paths"]["hymnal"]
    ch_at = []
    for k, n in enumerate(tune): ch_at.append((n["on"], path[k][0]))
    marks = []
    for on, c in ch_at:
        if c != prev: marks.append((on, c)); prev = c
    for i, (on, c) in enumerate(marks):
        nxt = marks[i + 1][0] if i + 1 < len(marks) else 16 * BAR
        for a, s in segs(on, nxt - on):
            r, _, q = CHN[c].partition(":"); toks.append((r + DUR[s] + (":" + q if q else "")) if a == on else "s" + DUR[s])
    return " ".join(toks), marks
def lead_sheet():
    chs, _ = chord_line()
    g = "\\time 3/4 \\key d \\major " + TEMPO + " " + " ".join(("s2. \\break" if b in (4, 8, 12) else "s2.") for b in range(1, 17)) + ' \\bar "|."'
    sop = voice_ly(stanza_events("S", 1), 16 * BAR, slurs=True)
    lys = "\n".join(f'  \\new Lyrics \\lyricsto "mel" {{ \\set stanza = "{i + 1}." {stanza_text(i)} }}' for i in range(5))
    src = HEAD % (19, 12, FOOT, FOOT) + f'''\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) }} \\context {{ \\Lyrics \\override LyricText.font-size = #-0.4 }} }}
\\header {{ title = "{TITLE}" subtitle = "Lead sheet{ED} · a Christmas hymn, 87 87, five stanzas" composer = "Words and music: Jason Bryant" poet = "D major · tune ARIMATHEA" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\chordmode {{ \\set chordChanges = ##t {chs} }}
  \\new Staff << \\new Voice {{ {g} }} \\new Voice = "mel" {{ {sop} }} >>
{lys}
>> \\layout {{ }} }}
\\markup \\vspace #1
\\markup \\small \\wordwrap {{ Range D4 to E5; women at pitch, men an octave lower. "Cloth" (stanzas 1 and 5) is the hymn's one high note, E5. Chords as the four-part setting sings them. Stanza 4 has its own setting (choir alone) and stanza 5 the organ's own harmony with a descant: see the organ score. }}
\\markup \\small \\italic \\wordwrap {{ Stanza 2: Luke 2:7; Matthew 27:57–60. The second Joseph is Joseph of Arimathea. }}
'''
    return src
def readback():
    names = ["S", "A", "T", "B", "Desc", "org_rh", "org_lh", "org_ped"]
    G = organ_global().replace("\\break", "")
    body = " ".join(f'\\new Staff << \\new Voice {{ {G} }} \\new Voice {{ {voice_ly(V[n], END, fermata_last=False)} }} >>' for n in names)
    src = f'\\version "2.24.3"\n\\score {{ << {body} >> \\midi {{ \\tempo 4 = 100 }} }}\n'
    compile_ly(src, "readback")
    mf = mido.MidiFile(f"{OUT}/readback.midi"); tpq = mf.ticks_per_beat; got = []
    for tr in mf.tracks:
        t = 0; ns = []
        for m in tr:
            t += m.time
            if m.type == "note_on" and m.velocity > 0: ns.append((round(t * 12 / tpq), m.note))
        if ns: got.append(sorted(ns))
    res = {}
    for n, g in zip(names, got):
        want = sorted((e["on"], q) for e in V[n] for q in (e["p"] if isinstance(e["p"], list) else [e["p"]]))
        res[n] = (g == want, len(g), len(want))
    return res
if __name__ == "__main__":
    out = {}
    out["hymnal page"] = compile_ly(hymnal(), f"{TITLE}{ED} - hymnal page")
    out["organ score"] = compile_ly(organ_score(), f"{TITLE}{ED} - organ score with choir")
    out["lead sheet"] = compile_ly(lead_sheet(), f"{TITLE}{ED} - lead sheet")
    for k, w in out.items(): print(k, "warnings", len(w), w[:3])
    rb = readback(); print(rb); json.dump({k: list(v) for k, v in rb.items()}, open(f"{OUT}/readback.json", "w"))
