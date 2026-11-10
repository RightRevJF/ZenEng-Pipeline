"""Swallowed Up -- the lead sheet (9-M.9): the harsh voice on a three-line rhythm staff, cross noteheads at three heights (low,
mid, high), a boxed cue for the technique wherever it changes, the words beneath; power-chord names above; each section boxed
with its riff and its feel; the tempo at each change (q = 200; the slowdown q = 100). Read back from LilyPond's MIDI."""
import pickle, re, sys, os, collections
sys.path[:0] = ["/home/claude/p34", "/home/claude/carol"]
from lily import compile_ly, midi_readback
from lily34 import stream, esc
import pyphen
REC = pickle.load(open("/home/claude/p34/song_record.pkl", "rb"))
OUT = "/home/claude/p34/out"
BARS = REC["bars"]; NB = REC["nbars"]
FEELNAME = {None: "", 0.25: "quarter time", 0.5: "half time", 1: "normal time", 2: "double time", 4: "blast"}
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"november": ["No", "vem", "ber"], "drumming": ["drum", "ming"], "into": ["in", "to"], "over": ["o", "ver"], "father": ["fa", "ther"],
        "sunday": ["Sun", "day"], "bible": ["Bi", "ble"], "margins": ["mar", "gins"], "pencil": ["pen", "cil"], "every": ["ev", "ery"],
        "swallowed": ["Swal", "lowed"], "never": ["Nev", "er"], "enough": ["E", "nough"], "iron": ["i", "ron"], "heavy": ["heav", "y"],
        "ashes": ["Ash", "es"], "abel's": ["A", "bel's"], "mother": ["moth", "er"], "backhoe": ["back", "hoe"], "idles": ["i", "dles"],
        "quiet": ["qui", "et"], "everything": ["ev", "ery", "thing"], "victory": ["vic", "to", "ry"], "a.m.": ["a.", "m."]}
def hyph(w, n):
    parts = HFIX.get(w.lower()) or _PY.inserted(w.lower()).split("-")
    if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
    while len(parts) < n: parts.append("_")
    return parts

# ---- the words: each stroke gets its syllable text, from the lyric line ----
import lyric as L
SEC = dict(L.SECTIONS)
VOICE = sorted([e for e in REC["events"] if e["part"] == "Voice"], key=lambda e: (e["bar"], e["slot"]))
groups = collections.OrderedDict()
for e in VOICE: groups.setdefault(e["sec_line"], []).append(e)
import engine_p34 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
for (sec, li), es in groups.items():
    words = SEC[sec][li][1].split(); k = 0
    for w in words:
        nsyl = len(_E.syllables(w)); core = re.sub(r"[^A-Za-z'.]", "", w).strip(".") if w.lower() != "a.m.," else "a.m."
        parts = hyph(core, nsyl) if nsyl > 1 else [w]
        for j in range(nsyl):
            t = parts[j]
            if nsyl > 1 and j == nsyl - 1: t += re.search(r"[^A-Za-z'.]*$", w).group(0) if core != "a.m." else ","
            if nsyl > 1 and j == 0 and w[0] in "\"\u201c": t = w[0] + t
            if nsyl > 1 and core[:1].isupper() and j == 0: t = t[0].upper() + t[1:]
            es[k + j]["text"] = t; es[k + j]["hy"] = nsyl > 1 and j < nsyl - 1 and core != "a.m."
        k += nsyl
    assert k == len(es), (sec, li, k, len(es), words)

POS = {"low": "g'", "mid": "b'", "high": "d''"}                    # bottom line, middle line, top line
CUEN = {("growl", "low"): "growl · low", ("shout", "mid"): "shout · mid (to be understood)", ("scream", "high"): "fry scream · high"}
def voice_tokens():
    last = [None]
    def tok(e, Ln, tie, first):
        from lily34 import DUR
        t = POS[e["height"]] + DUR[Ln] + ("~" if tie else "")
        if first:
            fam = (e["family"], e["height"])
            if fam != last[0]: t += f'^\\markup \\box \\small "{CUEN[fam]}"'; last[0] = fam
            if e["stressed"] and e["family"] != "growl": t += "->"
        return t
    items = [dict(e, abs16=e["bar"] * 16 + e["slot"]) for e in VOICE]
    return stream(items, NB, tok)
def lyric_tokens():
    out = []
    for e in VOICE:
        w = e["text"].replace("'", "’"); q = '"' + esc(w) + '"' if re.search(r"[’?!,.;:\"“”]", w) else w
        out.append(q + (" --" if e["hy"] else ""))
    return out

ROOT = {"B5": "b", "C5": "c", "D5": "d", "E5": "e", "F5": "f", "F#5": "fis", "G5": "g", "A5": "a"}
def chord_bar(k):
    names = BARS[k]["chords"]; riff = BARS[k]["riff"]
    if riff == "C" and len(names) == 3: d = ["2", "4", "4"]
    elif riff == "C" and len(names) == 2 and names == ["F5", "E5"]: d = ["2", "2"]
    elif len(names) == 3: d = ["4", "4", "2"]
    elif len(names) == 2: d = ["2", "2"]
    else: d = ["1"]
    if riff == "C" and names == ["F5", "E5", "C5"]: d = ["4", "4", "2"]
    return " ".join(f"{ROOT[n]}{x}:5" for n, x in zip(names, d))
def section_marks():
    m = {}
    for k, bb in enumerate(BARS):
        if k == 0 or bb["sec"] != BARS[k - 1]["sec"]:
            f = FEELNAME.get(bb["feel"]["feel"], "")
            label = bb["sec"] + f" · riff {bb['riff']}" + (f" · {f}" if f else "")
            if bb["sec"] == "Intro": label = "Intro · riff A · guitar 1 alone, then the band in layers (bar 9)"
            if bb["sec"] == "Slowdown": label = "Slowdown · riff E · half time"
            m[k] = label
        elif bb["riff"] != BARS[k - 1]["riff"] or (bb["feel"]["feel"] != BARS[k - 1]["feel"]["feel"] and bb["sec"] not in ("Intro", "Outro")):
            if bb["sec"] == "Slowdown" and bb["riff"] == "F": m[k] = "the breakdown · riff F · quarter time, the cymbal thinning"
            elif bb["sec"] == "Verse 3" and bb["riff"] == "B": m[k] = "riff B (home on B)"
            elif bb["sec"] == "Outro" and bb["riff"] == "G": m[k] = "the strokes · riff G"
            elif bb["sec"] == "Riff 2": m[k] = "double time"
    return m

def body(bybar, marks=True, part_marks=None):
    toks = []; M = section_marks()
    for k in range(NB):
        bb = BARS[k]
        if k == 0: toks += ["\\time 4/4", "\\tempo 4 = 200"]
        if k > 0 and bb["sec"] != BARS[k - 1]["sec"]: toks.append('\\bar "||"')
        if k > 0 and bb["q"] != BARS[k - 1]["q"]: toks.append(f"\\tempo \"{'the slowdown' if bb['q'] == 100 else 'a tempo'}\" 4 = {bb['q']}")
        if marks and k in M: toks.append(f'\\mark \\markup \\box \\bold "{esc(M[k])}"')
        if part_marks and k in part_marks: toks.append(part_marks[k])
        toks += bybar[k]
    return " ".join(toks)

CHORDS = " ".join(chord_bar(k) for k in range(NB))
footer = "Harsh voice: no pitch. Cross noteheads: bottom line low (growl), middle line mid (shout), top line high (fry scream). Accents: the shouted stresses."
footer2 = "Tuning B E A D F♯ B (low string B) · ♩ = 200; the slowdown ♩ = 100 · Words and music: Jason Bryant"
if __name__ == "__main__":
    vb = voice_tokens(); ly = lyric_tokens()
    src = f"""\\version "2.24.3"
#(set-global-staff-size 19)
\\header {{ title = "Swallowed Up" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "death metal, 4/4" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 22\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #13 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1.5 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-0.8 \\override LyricHyphen.minimum-distance = #0.6 }} }}
\\score {{
  <<
    \\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {CHORDS} }}
    \\new Staff = "vstaff" \\with {{ instrumentName = "Voice" \\override StaffSymbol.line-count = #3 \\override NoteHead.style = #'cross \\override Clef.stencil = ##f
       \\override KeySignature.stencil = ##f \\remove "Accidental_engraver" }}
      {{ \\compressMMRests {{ \\new Voice = "voc" {{ \\stemUp {body(vb)} \\bar "|." }} }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(ly)} }}
  >>
}}
"""
    path, warns = compile_ly(src, "Swallowed Up - lead sheet", cwd=OUT)
    print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
    os.makedirs(OUT + "/check", exist_ok=True)
    toks = [re.sub(r"[\^-].*$", "", t) for k in range(NB) for t in vb[k] if t[0] not in "rR"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, "check_voc", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_voc.midi")[0]
    H = {"low": 67, "mid": 71, "high": 74}
    want = [H[e["height"]] for e in VOICE]
    print("readback (voice):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "strokes")
