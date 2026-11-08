"""Module 11.9 document 3: the engraved lead sheet of 'Nothing On' (v64 port) from the song record -- the VOICE (female, treble) with
the lyric and chord names; beneath it the backing echo with its words (the posts' '(nothing on)', the last chorus's third under the
title lines) and a cue staff of the riff guitar (intro, verse 2, outro), each shown only where it sounds; the band's cuts marked over the
voice. 4/4 at q = 116 on a sixteenth grid; F major signature. Absolute pitches; LilyPond's MIDI read back per staff."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p31", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p31 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p31/song_record.pkl", "rb"))
OUT = "/home/claude/p31/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"tenfifteen": ["ten-", "fif", "teen"], "quiet": ["qui", "et"], "letting": ["let", "ting"], "only": ["on", "ly"], "glowing": ["glow", "ing"],
        "nothing": ["noth", "ing"], "everybody's": ["ev", "ery", "bod", "y's"], "waiting": ["wait", "ing"], "never": ["nev", "er"], "candle": ["can", "dle"],
        "birthday": ["birth", "day"], "kitchen": ["kitch", "en"], "funny": ["fun", "ny"], "every": ["ev", "ery"], "window": ["win", "dow"],
        "opens": ["o", "pens"], "microwave's": ["mi", "cro", "wave's"], "blinking": ["blink", "ing"], "am": ["a.", "m"]}
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
            if parts and parts[0].endswith("-"): parts = [parts[0][:-1]] + parts[1:]
            tail = re.search(r"[^A-Za-z’']*$", disp).group(0)
            for j, x in enumerate(r):
                if parts:
                    t = parts[j]
                    if j == len(parts) - 1: t += tail
                    x["text"] = t; x["hy"] = j < len(parts) - 1
                else:
                    x["text"] = disp; x["hy"] = False
BARS = REC["bars"]; TOT = REC["total_slots"]; NB = len(BARS)
VOC = sorted([dict(n, p=[n["midi"]]) for n in REC["lead"]], key=lambda n: n["on"])
texted(VOC)
for n in VOC:
    if n.get("text") == "a.": n["hy"] = False                     # 'two a. m.': the abbreviation, no hyphen
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}   # F major: flats (v65 fix 34)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "16", 2: "8", 3: "8.", 4: "4", 6: "4.", 8: "2", 12: "2.", 16: "1"}
def split(pos, n):
    """4/4 in sixteenths: a note crosses a quarter beat only as a half or dotted quarter from beat 1 or 3, a dotted half or whole from 1"""
    out = []
    while n > 0:
        if pos == 0 and n >= 16: Lh = 16
        elif pos == 0 and n >= 12: Lh = 12
        elif pos % 8 == 0 and n >= 8: Lh = 8
        elif pos % 8 == 0 and n >= 6: Lh = 6
        elif pos % 4 == 0 and n >= 4: Lh = 4
        elif pos % 4 in (0, 1) and n >= 3: Lh = 3
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
BV = sorted([dict(n, p=[n["midi"]]) for n in REC["harm"]], key=lambda n: n["on"])
byon = {n["on"]: n for n in VOC}
for n in BV:
    if n["sec"].startswith("Post"):
        k = [x["on"] for x in BV if x["sec"] == n["sec"]].index(n["on"])
        n["text"], n["hy"] = [("(noth", True), ("ing", False), ("on)", False)][k]
    else: n["text"], n["hy"] = byon[n["on"]]["text"], byon[n["on"]]["hy"]
BB, BLYR = stream(BV, "r", lyric=True)
CHANT = [dict(e) for e in REC["riff"]]
HB, _ = stream(CHANT, "r")
def blank(BY, evs):
    used = {bar_at[e["on"]] for e in evs} | {bar_at[min(TOT - 1, e["on"] + e["dur"] - 1)] for e in evs}
    for bi in range(NB):
        if bi not in used: BY[bi] = ["s1"]
blank(HB, CHANT); blank(BB, BV)
CUTMARK = {}
for cut in REC["cuts"]:
    CUTMARK[bar_at[cut["start"]]] = "tape stop: band out" if cut["kind"] == "tape stop" else "band hits 1, then out"
for b_ in range(NB):
    if BARS[b_]["sec"].startswith("Chorus") and BARS[b_]["k"] == 0: CUTMARK[b_] = "voice alone"
    if BARS[b_]["sec"].startswith("Chorus") and BARS[b_]["k"] == 1: CUTMARK[b_] = "band in"
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts and marks:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\key f \\major", "\\tempo 4 = 116"]
            toks.append(f'\\mark \\markup \\box \\bold "{s}"')
        elif bi == 0: toks += ["\\time 4/4", "\\key f \\major"]
        bt = list(bybar[bi])
        if marks and bi in CUTMARK and bt:
            bt[0] = bt[0] + f'^\\markup \\italic \\small "{CUTMARK[bi]}"'
        toks += bt
    return " ".join(toks)
CHR = {"Gm7": "g", "Am7": "a", "Bbmaj7": "bes", "C": "c", "F": "f", "Am": "a", "Bb": "bes"}
QUAL = {"Gm7": ":m7", "Am7": ":m7", "Bbmaj7": ":maj7", "Am": ":m"}
chords = " ".join(f"{CHR[b['chord']]}1{QUAL.get(b['chord'], '')}" for b in BARS)
vp = [n["midi"] for n in VOC]
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
assert min(vp) >= 55 and max(vp) == 74 and sum(1 for x in vp if x > 72) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (D5 once: “off” in the last chorus) · the backing echo and the riff guitar cued below · the band is silent in each chorus's first bar"
footer2 = "Words and music: Jason Bryant"
src = f"""\\version "2.24.3"
\\header {{ title = "Nothing On" subtitle = "Lead sheet: voice, with the backing echo and the riff cued" composer = "Words and music: Jason Bryant" meter = "disco-funk pop, straight sixteenths" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 22\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1.5 \\override LyricHyphen.minimum-distance = #0.6 }}
  \\context {{ \\Staff \\RemoveEmptyStaves }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff \\with {{ instrumentName = "Voice" \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble" \\new Voice = "voc" {{ {body(VB, True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(LYR)} }}
    \\new Staff \\with {{ instrumentName = \\markup \\small "Echo" shortInstrumentName = \\markup \\small "Echo" fontSize = #-3 \\override StaffSymbol.staff-space = #(magstep -3) \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "treble" \\new Voice = "bv" {{ {body(BB, False)} }} }}
    \\new Lyrics \\with {{ \\override LyricText.font-size = #-3 }} \\lyricsto "bv" {{ {" ".join(BLYR)} }}
    \\new Staff \\with {{ instrumentName = \\markup \\small "Riff" shortInstrumentName = \\markup \\small "Gtr." fontSize = #-3 \\override StaffSymbol.staff-space = #(magstep -3) \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "treble" {body(HB, False)} }}
  >>
}}
"""
path, warns = compile_ly(src, "Nothing On - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, notes in (("voice", VB, VOC), ("echo", BB, BV), ("riff guitar", HB, CHANT)):
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = []
    for n in sorted(notes, key=lambda n: n["on"]): want += sorted(n["p"])
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
