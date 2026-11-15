"""Sung to Sleep (song 53): the organ full score and the choir's hymn page, written from song_record.json. Both share one 'global' line (the
time, the keys, the bar lines, the section marks and a line break after every fourth bar), so every bar sits on the same system in both.
Sounding pitch throughout, spelled from the key (E-flat major to bar 36, F major from bar 37). After compiling, each staff's notes are read
back from LilyPond's MIDI and compared with the record."""
import json, subprocess, os, collections
import mido
import lyric_p63 as L
H = "/home/claude/p63"; OUT = f"{H}/out"; os.makedirs(OUT, exist_ok=True)
R = json.load(open(f"{H}/song_record.json")); V = R["voices"]; BAR = 36; L0 = 40 * BAR; END = R["end"]
ED = " (fourth edition)"
SP_EF = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}
SP_F = {0: "c", 1: "cis", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}
def pname(m, t):
    if isinstance(m, list): return "<" + " ".join(pname(q, t) for q in m) + ">"
    n = (SP_F if t >= L0 else SP_EF)[m % 12]; o = m // 12 - 1 - 3
    return n + ("'" * o if o > 0 else "," * (-o))
DUR = {6: "8", 12: "4", 18: "4.", 24: "2", 36: "2."}
def segs(t, d):
    """split at bar lines, then inside the bar into written lengths (dotted half, half, dotted quarter, quarter, eighth), longer ones
    only from a beat"""
    out = []
    while d > 0:
        nxt = (t // BAR + 1) * BAR; s = min(d, nxt - t)
        while s > 0:
            for L_ in (36, 24, 18, 12, 6):
                if L_ <= s and (L_ <= 6 or t % 12 == 0 or (L_ == 12 and t % 6 == 0 and False)):
                    break
            else: L_ = 6
            if L_ > s: L_ = s
            out.append((t, L_)); t += L_; s -= L_; d -= L_
    return out
def rest_toks(t, d, spacer=False):
    toks = []; r = "s" if spacer else "r"
    for a, s in segs(t, d):
        toks.append(("s2." if spacer else "R2.") if (s == 36 and a % BAR == 0) else (r + DUR[s]) if s in DUR else " ".join([r + "4"] * (s // 12)))
    return toks
def voice_ly(ev, dyn=None, fermata_last=True, slurs=False, spacer=False):
    toks = []; t = 0; dyn = dyn or {}
    for i, e in enumerate(ev):
        if e["on"] > t: toks += rest_toks(t, e["on"] - t, spacer)
        ss = segs(e["on"], e["dur"])
        for j, (a, s) in enumerate(ss):
            tk = pname(e["p"], a) + DUR[s]
            if j == 0 and e["on"] in dyn: tk += dyn[e["on"]]
            if j == len(ss) - 1 and i == len(ev) - 1 and fermata_last: tk += "\\fermata"
            if j < len(ss) - 1: tk += "~"
            if slurs and j == 0 and e.get("slur"): tk += "("
            if slurs and j == 0 and e.get("melisma"): tk += ")"
            toks.append(tk)
        t = e["on"] + e["dur"]
    if t < END: toks += rest_toks(t, END - t, spacer)
    return " ".join(toks)
def lyr_syls(line): return [(w.replace('"', '\\"'), j) for w, j in L.syls(line)]
def lyr_text(lines):
    out = []
    for ln in lines:
        for w, joins in lyr_syls(ln): out.append(w + (" --" if joins else ""))
    return " ".join(out)
# lyrics: line 1 carries verse 1, the refrain, then verse 4 and the final refrain; lines 2 and 3 verses 2 and 3
LY1 = ('\\set stanza = "1." ' + lyr_text(L.VERSES[0]) + " " + lyr_text(L.REFRAIN) + ' \\set stanza = "4." ' + lyr_text(L.VERSES[3]) + " " + lyr_text(L.REFRAIN))
LY2 = '\\set stanza = "2." ' + lyr_text(L.VERSES[1]); LY3 = '\\set stanza = "3." ' + lyr_text(L.VERSES[2]); LYD = lyr_text(L.REFRAIN)
O = R["offsets"]
DYN_S = {276: "\\mp", 864: "\\p", 1572: "\\mf", 2160: "\\f", O["B_refrain"] + 420: "\\p"}
DYN_O = {0: "\\p", 276: "\\mp", 864: "\\p", L0: "\\mf", 2160: "\\f", O["B_refrain"] + 420: "\\p", 76 * 36: "\\pp"}
DYN_D = {2160: "\\f"}
def glob():
    g = ['\\time 3/4', '\\key ees \\major', '\\tempo "Gently rocking" 4 = 88']
    marks = {1: "Organ: introduction", 9: "Verses 1–3", 25: "Refrain (after verses 1, 2 and 3)", 41: "Organ: to F major", 45: "Verse 4: unison (men an octave lower)", 61: "Final refrain: in parts, sopranos' descant", 77: "Organ: coda"}
    for b in range(1, 81):
        if b == 41: g.append('\\key f \\major')
        if b in marks: g.append(f'\\mark \\markup \\small \\bold "{marks[b]}"')
        g.append('s2.')
        if b in (8, 24, 40, 44, 60, 76): g.append('\\bar "||"')
        if b == 80: g.append('\\bar "|."')
        elif b % 4 == 0: g.append('\\break')
    return " ".join(g)
GLOB = glob()
NOTE36 = 's2.*39 s2 s4^\\markup \\italic \\small \\column { "Verses 2 and 3: back to bar 8, beat 3" "After verse 3: on to bar 41" } s2.*40'

FOOT = "Sung to Sleep (fourth edition) · Words and music: Jason Bryant · ♩ = 88 · E-flat major, verse 4 in F major"
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 14\mm right-margin = 14\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #14
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \override RehearsalMark.self-alignment-X = #LEFT }
          \context { \Staff \RemoveAllEmptyStaves } \context { \Lyrics \override LyricText.font-size = #-0.3 } }
'''
def music(v, dyn=None, slurs=False): return voice_ly(V[v], dyn, slurs=slurs)
SOP, ALT, TEN, BAS = music("S", DYN_S, True), music("A"), music("T"), music("B")
DES = music("Desc", DYN_D, True)
ORH, OLH, OPED = music("org_rh", DYN_O), music("org_lh"), music("org_ped")
ORHI = voice_ly(V.get("org_rh_in", []), fermata_last=False, spacer=True)
REG = {1: ["Sw. Flutes 8′ 4′", "Ped. Bourdon 16′, Sw. to Ped."], 9: ["v. 1: Sw. Flutes 8′ 4′", "v. 2: Gt. Open Diapason 8′", "v. 3: Gt. Diapasons 8′ 4′, Sw. to Gt."],
       25: ["1st time: Sw. Flutes 8′ 4′", "2nd: add Gt. Open Diapason 8′", "3rd: add Gt. Principal 4′"], 41: ["Gt. Diapasons 8′ 4′, Sw. to Gt."], 45: ["Gt. Diapasons 8′ 4′ 2′, Sw. Reed 8′, Sw. to Gt.", "Ped. 16′ 8′"],
       61: ["Full Sw. to Gt., Gt. Mixture", "Ped. 16′ 8′ 4′"], 77: ["Sw. Flutes 8′", "Ped. Bourdon 16′"]}
def reg_voice():
    out = []
    for b in range(1, 81):
        if b in REG: out.append('s2.^\\markup \\tiny \\italic \\column { ' + " ".join(f'"{x}"' for x in REG[b]) + ' }')
        else: out.append("s2.")
    return " ".join(out)
REGV = reg_voice()
KEEP = "\\with { \\override VerticalAxisGroup.remove-empty = ##f }"
def choir_block():
    return f'''
  \\new Staff = "desc" \\with {{ instrumentName = "Descant" shortInstrumentName = "D." }} <<
    \\new Voice = "glb_d" {{ \\global }} \\new Voice = "desc" {{ \\voiceOne \\oneVoice {DES} }} >>
  \\new Lyrics \\lyricsto "desc" {{ {LYD} }}
  \\new ChoirStaff <<
    \\new Staff = "sa" {KEEP[:-2]} instrumentName = "S A" shortInstrumentName = "S A" }} <<
      \\new Voice {{ \\global }} \\new Voice {{ {NOTE36} }} \\new Voice = "sop" {{ \\voiceOne {SOP} }} \\new Voice = "alt" {{ \\voiceTwo {ALT} }} >>
    \\new Lyrics \\lyricsto "sop" {{ {LY1} }}
    \\new Lyrics \\lyricsto "sop" {{ {LY2} }}
    \\new Lyrics \\lyricsto "sop" {{ {LY3} }}
    \\new Staff = "tb" {KEEP[:-2]} instrumentName = "T B" shortInstrumentName = "T B" }} <<
      \\clef bass \\new Voice {{ \\global }} \\new Voice = "ten" {{ \\voiceOne {TEN} }} \\new Voice = "bas" {{ \\voiceTwo {BAS} }} >>
  >>'''
def organ_block():
    return f'''
  \\new PianoStaff \\with {{ instrumentName = "Organ" shortInstrumentName = "Org." }} <<
    \\new Staff = "rh" {KEEP} << \\new Voice {{ \\global }} \\new Voice {{ {REGV} }} \\new Voice {{ \\voiceOne {ORH} }} \\new Voice {{ \\voiceTwo {ORHI} }} >>
    \\new Staff = "lh" {KEEP} << \\clef bass \\new Voice {{ \\global }} \\new Voice {{ {OLH} }} >>
  >>
  \\new Staff = "ped" \\with {{ instrumentName = "Pedal" shortInstrumentName = "Ped." \\override VerticalAxisGroup.remove-empty = ##f }} << \\clef bass \\new Voice {{ \\global }} \\new Voice {{ {OPED} }} >>'''
def doc(sub, organ, size):
    return HEAD % (size, FOOT, FOOT) + f'''global = {{ {GLOB} }}
\\header {{ title = "Sung to Sleep" subtitle = "{sub}" composer = "Words and music: Jason Bryant" poet = "Common Meter with refrain" tagline = ##f }}
\\score {{ << {choir_block()} {organ_block() if organ else ""} >> \\layout {{ }} }}
'''
def compile_ly(src, base):
    p = f"{OUT}/{base}.ly"; open(p, "w").write(src)
    r = subprocess.run(["lilypond", "-dno-point-and-click", "-o", f"{OUT}/{base}", p], capture_output=True, text=True)
    errs = [l for l in r.stderr.splitlines() if "error" in l.lower()]
    if r.returncode or errs: raise RuntimeError(r.stderr[-3000:])
    return [l for l in r.stderr.splitlines() if "warning" in l.lower()]
def readback():
    """every voice on its own staff, LilyPond's MIDI, notes compared with the record (sounding pitch, onset)"""
    names = ["S", "A", "T", "B", "Desc", "org_rh", "org_rh_in", "org_lh", "org_ped"]
    staves = " ".join(f'\\new Staff {{ \\new Voice {{ \\global {{}} }} }} ' for _ in [])
    body = " ".join(f'\\new Staff << \\new Voice {{ \\global }} \\new Voice {{ {voice_ly(V[n], fermata_last=False)} }} >>' for n in names)
    src = f'\\version "2.24.3"\nglobal = {{ {GLOB.replace(chr(92) + "break", "")} }}\n\\score {{ << {body} >> \\midi {{ \\tempo 4 = 88 }} }}\n'
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
        # tied segments sound once; a note's onset is its first segment
        res[n] = (g == want, len(g), len(want))
    return res
if __name__ == "__main__":
    w1 = compile_ly(doc("Hymn page (choir) · fourth edition", False, 17), f"Sung to Sleep{ED} - hymn page")
    w2 = compile_ly(doc("Full score (organ) · fourth edition", True, 15), f"Sung to Sleep{ED} - full score (organ)")
    print("hymn page warnings", w1[:5], len(w1)); print("full score warnings", w2[:5], len(w2))
    rb = readback(); print({k: v for k, v in rb.items()})
    json.dump({k: list(v) for k, v in rb.items()}, open(f"{OUT}/readback.json", "w"))
