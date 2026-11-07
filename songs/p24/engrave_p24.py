"""Module 11.9 document 3: the engraved lead sheet of 'The Song You Sang Me' (v64 port) from the song record -- two staves: the VOICE
(tenor, treble 8vb) with the lyric, and the GUITAR (treble 8vb, concert pitch) in two voices: the lullaby's tune on top in the intro and
outro (27.21), the fingerpicking below. Chord names at concert pitch, with the capo-3 shapes beneath. 3/4 at q = 76, F major. Absolute
pitches; LilyPond's MIDI read back per voice."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p24", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p24 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p24/song_record.pkl", "rb"))
OUT = "/home/claude/p24/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"folding": ["fold", "ing"], "napkin": ["nap", "kin"], "window": ["win", "dow"], "pictures": ["pic", "tures"], "august": ["Au", "gust"],
        "anyone": ["an", "y", "one"], "folded": ["fold", "ed"], "brother's": ["broth", "er's"], "tuesday": ["Tues", "day"], "feeder": ["feed", "er"],
        "marker": ["mark", "er"], "underneath": ["un", "der", "neath"], "somewhere": ["some", "where"], "second": ["sec", "ond"],
        "didn't": ["did", "n't"], "along": ["a", "long"], "always": ["al", "ways"]}
def hyph_for(w, nnotes):
    parts = HFIX.get(w.lower()) or _PY.inserted(w.lower()).split("-")
    if len(parts) > nnotes: parts = parts[:nnotes - 1] + ["".join(parts[nnotes - 1:])]
    if len(parts) < nnotes: parts = parts + ["_"] * (nnotes - len(parts))
    return parts
SEC = {s: items for s, items in L.SECTIONS}
def texted(notes):
    groups = collections.OrderedDict()
    for n in notes: groups.setdefault((n["sec"], n["line"]), []).append(n)
    for (sec, li), ns in groups.items():
        words = SEC[sec][li][1].split(); runs = []
        for w in words:
            k = len(_E.syllables(w)); runs.append(ns[:k]); ns = ns[k:]
        assert not ns and all(runs), (sec, li, words)
        for w, r in zip(words, runs):
            disp = ("“" + w[1:]) if w.startswith('"') else w
            disp = (disp[:-1] + "”") if disp.endswith('"') else disp
            parts = hyph_for(re.sub(r"[^A-Za-z']", "", w), len(r)) if len(r) > 1 else None
            tail = re.search(r"[^A-Za-z’']*$", disp).group(0)
            for j, x in enumerate(r):
                if parts:
                    t = parts[j]
                    if j == len(parts) - 1: t += tail
                    x["text"] = t; x["hy"] = j < len(parts) - 1
                else:
                    x["text"] = disp; x["hy"] = False
BARS = REC["bars"]; TOT = REC["total_eighths"]; NB = len(BARS)
VOC = sorted([dict(n, p=[n["midi"]]) for n in REC["lead"]], key=lambda n: n["on"])
texted(VOC)
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2."}
def split(pos, n):
    out = []
    while n > 0:
        if pos == 0 and n >= 6: Lh = 6
        elif pos % 2 == 0 and n >= 4 and pos + 4 <= 6: Lh = 4
        elif pos % 2 == 0 and n >= 3 and pos + 3 <= 6: Lh = 3
        elif pos % 2 == 0 and n >= 2: Lh = 2
        else: Lh = 1
        out.append((pos, Lh)); pos += Lh; n -= Lh
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
def stream(notes, rest="r", lyric=False):
    notes = sorted(notes, key=lambda n: n["on"]); cur = 0; seq = []
    for n in notes:
        assert n["on"] >= cur, ("overlap", n)
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list); lyr = []
    for kind, s, d, n in seq:
        first = True
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; m = min(d, b["start"] + b["len"] - s)
            sp = split(s - b["start"], m)
            for k, (pos, Lh) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = rest + DUR[Lh]
                else:
                    ps = n["p"]; nm = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    tok = nm + DUR[Lh] + ("~" if tie else "")
                    if lyric and first:
                        w = n["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                        lyr.append(q + (" --" if n.get("hy") else ""))
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, lyr
VB, LYR = stream(VOC, "r", lyric=True)
MB, _ = stream(REC["gmel"], "s"); AB, _ = stream(REC["gtr"], "r")
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts and marks:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 3/4", "\\key f \\major", "\\tempo 4 = 76"]
            toks.append(f'\\mark \\markup \\box \\bold "{s}"')
        elif bi == 0: toks += ["\\time 3/4", "\\key f \\major"]
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"F": "f", "Bb": "bes", "C": "c", "Dm": "d", "Gm": "g", "Am": "a"}
QUAL = {"Dm": ":m", "Gm": ":m", "Am": ":m"}
chords = " ".join(f"{CHR[b['chord']]}2.{QUAL.get(b['chord'], '')}" for b in BARS)
vp = [n["midi"] for n in VOC]
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
assert min(vp) >= 50 and max(vp) == 70 and sum(1 for x in vp if x > 69) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (B♭4 once, the last “wake”) · guitar written at concert pitch; capo 3, play the shapes in brackets"
footer2 = "Words and music: Jason Bryant · voice and guitar written in treble 8vb, sounding an octave lower"
src = f"""\\version "2.24.3"
\\header {{ title = "The Song You Sang Me" subtitle = "Lead sheet: voice and guitar" composer = "Words and music: Jason Bryant" meter = "slow waltz, fingerpicked" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 24\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #13 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1 \\override LyricHyphen.minimum-distance = #1.0 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new ChordNames \\with {{ \\override ChordName.font-size = #-2 chordNameExceptions = #ignatzekExceptions }} \\transpose f d {{ \\chordmode {{ \\set chordNameFunction = #(lambda (in-pitches bass inversion context) (make-line-markup (list (make-simple-markup "(") (ignatzek-chord-names in-pitches bass inversion context) (make-simple-markup ")")))) {chords} }} }}
    \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "voc" {{ {body(VB, True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(LYR)} }}
    \\new Staff \\with {{ instrumentName = "Guitar" }} <<
      \\clef "treble_8"
      \\new Voice = "tune" {{ \\voiceOne {body(MB, False)} }}
      \\new Voice = "acc" {{ \\voiceTwo {body(AB, False)} }}
    >>
  >>
}}
"""
path, warns = compile_ly(src, "The Song You Sang Me - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, notes in (("voice", VB, VOC), ("tune", MB, REC["gmel"]), ("guitar", AB, REC["gtr"])):
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 3/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = []
    for n in sorted(notes, key=lambda n: n["on"]): want += sorted(n["p"])
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
