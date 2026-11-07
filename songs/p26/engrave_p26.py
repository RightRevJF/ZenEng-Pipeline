"""Module 11.9 document 3: the engraved lead sheet of 'Five-Oh-One' (v64 port) from the song record -- the VOICE (tenor, treble 8vb)
with the lyric and chord names, and beneath it a cue staff of the horns' chant (the intro, the hooks, the outro; 27.21's quote kind),
shown only where the horns play it. 4/4 at q = 112 on a sixteenth grid; Eb major, F major from chorus 3. Absolute pitches; LilyPond's MIDI
read back per staff."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p26", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p26 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p26/song_record.pkl", "rb"))
OUT = "/home/claude/p26/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"fiveohone": ["five", "oh", "one"], "fiveoh": ["five", "oh"], "borrowing": ["bor", "row", "ing"], "second": ["sec", "ond"], "money": ["mon", "ey"], "minute": ["min", "ute"], "somebody's": ["some", "bod", "y's"], "loading": ["load", "ing"], "speakers": ["speak", "ers"], "sending": ["send", "ing"], "address": ["ad", "dress"], "little": ["lit", "tle"], "loosens": ["loos", "ens"], "avenue's": ["av", "e", "nue's"], "sixty": ["six", "ty"], "single": ["sin", "gle"], "finding": ["find", "ing"], "radio's": ["ra", "di", "o's"], "playing": ["play", "ing"], "pretended": ["pre", "tend", "ed"], "hated": ["hat", "ed"], "singing": ["sing", "ing"], "already": ["al", "read", "y"], "rattling": ["rat", "tling"], "dancing": ["danc", "ing"], "driveway": ["drive", "way"], "before": ["be", "fore"], "even": ["e", "ven"], "neighbor": ["neigh", "bor"], "wasn't": ["was", "n't"], "coming": ["com", "ing"], "grandmother's": ["grand", "moth", "er's"], "middle": ["mid", "dle"], "winning": ["win", "ning"], "monday": ["Mon", "day"], "tuesday": ["Tues", "day"], "wednesday": ["Wednes", "day"], "thursday": ["Thurs", "day"], "bury": ["bur", "y"], "shovel": ["shov", "el"], "wouldn't": ["would", "n't"], "over": ["o", "ver"], "thumbnail": ["thumb", "nail"], "tower": ["tow", "er"], "over": ["o", "ver"], "brilliance": ["bril", "liance"], "valley": ["val", "ley"],
        "winter": ["win", "ter"], "farther": ["far", "ther"], "frozen": ["fro", "zen"], "open": ["o", "pen"], "again": ["a", "gain"],
        "breaking": ["break", "ing"], "every": ["ev", "ery"], "enough": ["e", "nough"], "stranger's": ["strang", "er's"], "couldn't": ["could", "n't"],
        "never": ["nev", "er"], "carries": ["car", "ries"], "only": ["on", "ly"], "ever": ["ev", "er"], "folding": ["fold", "ing"], "napkin": ["nap", "kin"], "window": ["win", "dow"], "pictures": ["pic", "tures"], "august": ["Au", "gust"],
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
BARS = REC["bars"]; TOT = REC["total_slots"]; NB = len(BARS)
VOC = sorted([dict(n, p=[n["midi"]]) for n in REC["lead"]], key=lambda n: n["on"])
texted(VOC)
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}   # Eb and F major: flats (v65 fix 34)
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
                    if first and lyric and (bi, n["on"]) in GANG_MARK: tok += '^\\markup \\italic \\small "' + GANG_MARK[(bi, n["on"])] + '"' 
                    if lyric and first:
                        w = n["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                        lyr.append(q + (" --" if n.get("hy") else ""))
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, lyr
# the gang: (everybody) on the lift's shout; the band's answers after each hook line
GANG_MARK = {}
for n in VOC:
    if n["singer"] == "gang" and n["syl"][0] == "five": GANG_MARK[(bar_at[n["on"]], n["on"])] = "(everybody)"
for g in REC["gang"]:
    if g.get("word") in ("hey", "go"):
        ln_end = max(n["on"] for n in VOC if n["on"] <= g["on"])
        GANG_MARK[(bar_at[ln_end], ln_end)] = f"(band: {g['word']}!)"
VB, LYR = stream(VOC, "r", lyric=True)
CHANT = [dict(e) for e in REC["horns"] if e.get("src") == "chant"]
HB, _ = stream(CHANT, "r")
CHANTBAR = {bar_at[e["on"]] for e in CHANT} | {bar_at[min(TOT - 1, e["on"] + e["dur"] - 1)] for e in CHANT}
for bi in range(NB):
    if bi not in CHANTBAR: HB[bi] = ["s1"]

starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts and marks:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\key ees \\major", "\\tempo 4 = 112"]
            if s == "Chorus 3": toks.append("\\key f \\major")
            toks.append(f'\\mark \\markup \\box \\bold "{s}"')
        elif bi == 0: toks += ["\\time 4/4", "\\key ees \\major"]
        if not marks and bi in starts and starts[bi][0] == "Chorus 3": toks.append("\\key f \\major")
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"Eb": "ees", "Ab": "aes", "Bb": "bes", "Cm": "c", "Gm": "g", "C": "c", "F": "f", "Dm": "d"}
QUAL = {"Cm": ":m", "Gm": ":m", "Dm": ":m"}
chords = " ".join(f"{CHR[b['chord']]}1{QUAL.get(b['chord'], '')}" for b in BARS)
vp = [n["midi"] for n in VOC]
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
assert min(vp) >= 50 and max(vp) == 70 and sum(1 for x in vp if x > 69) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (B♭4 once: “here”, the last chorus) · sung in treble 8vb, sounding an octave lower · horns’ chant cued below"
footer2 = "Words and music: Jason Bryant"
src = f"""\\version "2.24.3"
\\header {{ title = "Five-Oh-One" subtitle = "Lead sheet: voice, with the horns’ chant cued" composer = "Words and music: Jason Bryant" meter = "funk-pop, straight sixteenths" tagline = ##f }}
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
    \\new Staff \\with {{ instrumentName = "Voice" \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble_8" \\new Voice = "voc" {{ {body(VB, True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(LYR)} }}
    \\new Staff \\with {{ instrumentName = \\markup \\small "Horns" shortInstrumentName = \\markup \\small "Hn." fontSize = #-3 \\override StaffSymbol.staff-space = #(magstep -3) \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "treble" {body(HB, False)} }}
  >>
}}
"""
path, warns = compile_ly(src, "Five-Oh-One - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, notes in (("voice", VB, VOC), ("horns chant", HB, CHANT)):
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = []
    for n in sorted(notes, key=lambda n: n["on"]): want += sorted(n["p"])
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
