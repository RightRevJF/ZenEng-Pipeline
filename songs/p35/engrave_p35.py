"""The First Wood -- the score (choir and organ, hymnal layout), the lead sheet and the parts, from the song record.
One pass of the tune with the four stanzas beneath it; the voices of stanza 2 (stanzas 3 and 4 sing the same notes; stanza 1 is in
unison on the tune). Each staff read back from LilyPond's MIDI against the record."""
import pickle, re, sys, os, collections
sys.path[:0] = ["/home/claude/p35", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
from lily35 import stream, pname, DUR, esc, chord_tok, chord_text
import engine_p35 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
import pyphen, lyric as L
import melody_p35 as M
REC = pickle.load(open("/home/claude/p35/song_record.pkl", "rb")); EV = REC["events"]; OUT = "/home/claude/p35/out"
OFF = (8 + 24 * 1) * 36                    # stanza 2's first downbeat
START, END = OFF - 36, OFF + 23 * 36 + 24   # the pickup bar's bar line; the end of the tune before the next pickup
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"feed-trough": ["feed-", "trough"], "roughly": ["rough", "ly"], "along": ["a", "long"], "edges": ["ed", "ges"], "never": ["nev", "er"],
        "hundred": ["hun", "dred"], "other": ["oth", "er"], "fathers'": ["fa", "thers'"], "mortise": ["mor", "tise"], "father": ["fa", "ther"],
        "timber": ["tim", "ber"], "beyond": ["be", "yond"]}
def hyph(w, n):
    core = re.sub(r"[^A-Za-z'\-]", "", w).lower()
    parts = HFIX.get(core) or _PY.inserted(core).split("-")
    if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
    while len(parts) < n: parts.append("_")
    return parts
def line_syllables(text):
    out = []
    for w in text.split():
        n = len(_E.syllables(w.replace("-", " ")))
        if n <= 1: out.append((w, False)); continue
        ps = hyph(w, n); tail = re.search(r"[^A-Za-z']*$", w).group(0)
        lead = w[0] if not w[0].isalpha() else ""
        for j, p in enumerate(ps):
            t = (lead if j == 0 else "") + (p[0].upper() + p[1:] if j == 0 and w[len(lead)].isupper() else p) + (tail if j == n - 1 else "")
            out.append((t.rstrip("-"), j < n - 1))
    return out
TEXT = {}
for si in range(4):
    lines = L.STANZAS[si] + [L.REFRAIN1.rstrip(",") + L.REFRAIN1_PUNCT[si], L.REFRAIN2[si]]
    TEXT[si] = {ln: line_syllables(t) for ln, t in zip(M.LINES, lines)}
    for ln in M.LINES: assert len(TEXT[si][ln]) == M.NSYL[ln], (si, ln, TEXT[si][ln])

def part_ev(part, stanza):
    """a stanza's events for one part, moved onto stanza 2's bars (every stanza sings the same notes but stanza 1's lower voices)."""
    sh = (8 + 24 * stanza) * 36 - OFF
    return sorted([dict(e, on=e["abs12"] - sh) for e in EV if e["part"] == part and e.get("stanza") == stanza + 1 and START <= e["abs12"] - sh < END + 36], key=lambda e: e["on"])
def clip(es):
    out = []
    for e in es:
        e = dict(e); e["dur"] = min(e["dur"], END - e["on"])
        if e["dur"] > 0: out.append(e)
    return out
def voice_tokens(part, stanza=1, slurs=True):
    es = clip(part_ev(part, stanza))
    # slurs over a syllable's notes
    groups = []
    for e in es:
        if e["first"] or not groups: groups.append([e])
        else: groups[-1].append(e)
    opens = {g[0]["on"] for g in groups if len(g) > 1}; closes = {g[-1]["on"] for g in groups if len(g) > 1}
    def tok(e, Ln, tie, first):
        t = pname(e["pitch"]) + DUR[Ln] + ("~" if tie else "")
        if first and slurs and e["on"] in opens: t += "("
        if first and slurs and e["on"] in closes and not tie: t += ")"
        return t
    by = stream(es, START, END, tok)
    by[0] = [t for t in by[0] if not t.startswith("r")]          # the pickup bar: \partial 4
    return by, es
def lyric_tokens(part, stanza):
    es = clip(part_ev(part, stanza)); out = []; ln_prev = None; k = 0
    for e in es:
        if not e["first"]: continue                       # a slurred or tied note is a melisma by itself (lyricsto)
        t, hy = TEXT[stanza][e["line"]][e["syl_i"]]
        w = t.replace("'", "’"); q = '"' + esc(w) + '"' if re.search(r"[’?!,.;:\"]", w) else w
        out.append(q + (" --" if hy else ""))
    return out
def chords_tokens():
    sl = []
    for v in REC["voices"]:
        on, end = OFF + v["on"], OFF + min(v["end"], 23 * 36 + 24)
        if end > on: sl.append(dict(on=on, dur=end - on, chord=v["chord"], bass=v["bass"]))
    def tok(it, Ln, tie, first): return chord_tok(it["chord"], it["bass"], Ln) if first else "s" + DUR[Ln]
    by = stream(sl, START, END, tok, mm=False)
    by[0] = [t for t in by[0] if not t.startswith("r")]
    return " ".join(t for b in by for t in b)
MARKS = {0: "Stanza", 4: "", 8: "", 12: "", 16: "Refrain", 20: ""}
def body(by):
    toks = ["\\key f \\major", "\\time 3/4", "\\partial 4"]
    for k, b in enumerate(by):
        if k == 17: toks.append('\\mark \\markup \\small \\bold "Refrain"')
        toks += b
    toks.append('\\bar "|."')
    return " ".join(toks)
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 16\mm right-margin = 16\mm top-margin = 12\mm bottom-margin = 16\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
FOOT = "The First Wood · Words and music: Jason Bryant · ♩ = 92 · F major · Common Metre with refrain"
ARRNOTE = ('\\markup \\small \\column { "Introduction: the organ plays the refrain (bars 17–24)." '
           '"Stanza 1: everyone in unison on the tune (tenors and basses an octave below), the organ in four parts." '
           '"Stanza 2: four parts with the organ.  Stanza 3: four parts, unaccompanied." '
           '"Stanza 4: four parts, full organ, the tune doubled an octave higher." }')
def lyrics_block(voice, part, stanzas):
    return " ".join(f'\\new Lyrics \\lyricsto "{voice}" {{ \\set stanza = "{s + 1}." {" ".join(lyric_tokens(part, s))} }}' for s in stanzas)
def readback(name, by, want):
    toks = [re.sub(r"[()]", "", t) for b in by for t in b if not t.startswith(("r", "R"))]
    compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 3/4 \\partial 4 ' + " ".join(toks) + ' } \\midi { } }', f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    return got == want, len(got)

if __name__ == "__main__":
    os.makedirs(OUT + "/check", exist_ok=True)
    V = {p: voice_tokens(p) for p in ("S", "A", "T", "B")}
    CH = chords_tokens()
    # ---- the score: choir and organ, hymnal layout ----
    score = HEAD % (18, FOOT, FOOT) + f'''\\header {{ title = "The First Wood" subtitle = "Score: choir (SATB) and organ" composer = "Words and music: Jason Bryant" meter = "C.M. with refrain · ♩ = 92" tagline = ##f }}
{ARRNOTE}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ \\partial 4 {CH} }}
  \\new ChoirStaff <<
    \\new Staff \\with {{ instrumentName = \\markup \\center-column {{ "S" "A" }} }} << \\new Voice = "sop" {{ \\voiceOne {body(V["S"][0])} }} \\new Voice = "alto" {{ \\voiceTwo {body(V["A"][0])} }} >>
    {lyrics_block("sop", "S", range(4))}
    \\new Staff \\with {{ instrumentName = \\markup \\center-column {{ "T" "B" }} }} << \\clef bass \\new Voice = "ten" {{ \\voiceOne {body(V["T"][0])} }} \\new Voice = "bas" {{ \\voiceTwo {body(V["B"][0])} }} >>
  >> >> \\layout {{ }} }}
'''
    path, warns = compile_ly(score, "The First Wood - score (choir and organ)", cwd=OUT)
    print("score:", [w for w in warns if "clashing" not in w][:4], len(warns))
    for p in ("S", "A", "T", "B"):
        ok, n = readback(p, V[p][0], [e["pitch"] for e in V[p][1]]); print(f"  readback {p}: {'matches' if ok else 'MISMATCH'} ({n})")
    # ---- the lead sheet ----
    lead = HEAD % (20, FOOT, FOOT) + f'''\\header {{ title = "The First Wood" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "C.M. with refrain · ♩ = 92" tagline = ##f }}
\\score {{ <<
  \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ \\partial 4 {CH} }}
  \\new Staff {{ \\new Voice = "sop" {{ {body(V["S"][0])} }} }}
  {lyrics_block("sop", "S", range(4))}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 "The refrain's first line is the same in every stanza; its second line changes, and in stanza 4 it turns: “it will not be the last.”" "The one D5 falls on “first.”" }}
'''
    compile_ly(lead, "The First Wood - lead sheet", cwd=OUT); print("lead sheet compiled")
    # ---- the parts ----
    def part_book(p, name, clef, stanzas, note):
        vname = {"S": "sop", "A": "alto", "T": "ten", "B": "bas"}[p]
        return f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\markup \\small "{note}"
\\score {{ << \\new Staff {{ {clef} \\new Voice = "{vname}" {{ {body(V[p][0])} }} }} {lyrics_block(vname, p, stanzas)} >> \\layout {{ }} }} }}
'''
    st1 = "Stanza 1: everyone sings the tune in unison"
    parts = HEAD % (19, FOOT, FOOT) + '\\header { title = "The First Wood" composer = "Words and music: Jason Bryant" tagline = ##f }\n' + \
        part_book("S", "Soprano", "", range(4), "All four stanzas. Stanza 3 unaccompanied.") + \
        part_book("A", "Alto", "", range(1, 4), st1 + " (the soprano line); the harmony below is for stanzas 2–4. Stanza 3 unaccompanied.") + \
        part_book("T", "Tenor", '\\clef "treble_8"', range(1, 4), st1 + " an octave below; the harmony below is for stanzas 2–4. Stanza 3 unaccompanied.") + \
        part_book("B", "Bass", "\\clef bass", range(1, 4), st1 + " an octave below; the harmony below is for stanzas 2–4. Stanza 3 unaccompanied.") + \
        f'''\\bookpart {{ \\header {{ subtitle = "Organ" }}
\\markup \\small \\column {{ "The organ plays the four choir parts as written; the pedal doubles the bass, an octave lower where it lies above C3." "Introduction: the refrain (bars 17–24), then give the pickup to stanza 1." "Stanza 1: four parts under the unison choir.  Stanza 2: four parts.  Stanza 3: tacet (the choir alone)." "Stanza 4: full organ, the tune doubled an octave higher in the right hand." }}
\\score {{ << \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ \\partial 4 {CH} }}
  \\new PianoStaff << \\new Staff << \\new Voice {{ \\voiceOne {body(V["S"][0])} }} \\new Voice {{ \\voiceTwo {body(V["A"][0])} }} >>
  \\new Staff << \\clef bass \\new Voice {{ \\voiceOne {body(V["T"][0])} }} \\new Voice {{ \\voiceTwo {body(V["B"][0])} }} >> >> >> \\layout {{ }} }} }}
'''
    compile_ly(parts, "The First Wood - parts (choir and organ)", cwd=OUT); print("parts compiled")
