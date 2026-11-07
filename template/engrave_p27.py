"""Module 11.9 document 3: the engraved lead sheet of 'Either Or' (v64 port) from the song record -- the VOICE (tenor, treble 8vb) with the
lyric and chord names. Verses in 5/4 (beamed 3+2), refrains in 4/4, q = 132; D Dorian (no key signature) and F major. The stop before the
last line and the outro's drone marked. Absolute pitches; LilyPond's MIDI read back."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p27", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p27 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p27/song_record.pkl", "rb"))
OUT = "/home/claude/p27/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"aristotle": ["Ar", "is", "tot", "le"], "across": ["a", "cross"], "other": ["oth", "er"], "ever": ["ev", "er"], "calling": ["call", "ing"], "tower": ["tow", "er"], "systematizing": ["sys", "tem", "a", "tiz", "ing"], "weighing": ["weigh", "ing"], "sprinkled": ["sprin", "kled"], "holy": ["ho", "ly"], "water": ["wa", "ter"], "amen": ["a", "men"], "keepers": ["keep", "ers"], "handing": ["hand", "ing"], "fathers'": ["fa", "thers'"], "turning": ["turn", "ing"], "into": ["in", "to"], "never": ["nev", "er"], "either": ["ei", "ther"], "doesn't": ["does", "n't"], "fiveohone": ["five", "oh", "one"], "fiveoh": ["five", "oh"], "borrowing": ["bor", "row", "ing"], "second": ["sec", "ond"], "money": ["mon", "ey"], "minute": ["min", "ute"], "somebody's": ["some", "bod", "y's"], "loading": ["load", "ing"], "speakers": ["speak", "ers"], "sending": ["send", "ing"], "address": ["ad", "dress"], "little": ["lit", "tle"], "loosens": ["loos", "ens"], "avenue's": ["av", "e", "nue's"], "sixty": ["six", "ty"], "single": ["sin", "gle"], "finding": ["find", "ing"], "radio's": ["ra", "di", "o's"], "playing": ["play", "ing"], "pretended": ["pre", "tend", "ed"], "hated": ["hat", "ed"], "singing": ["sing", "ing"], "already": ["al", "read", "y"], "rattling": ["rat", "tling"], "dancing": ["danc", "ing"], "driveway": ["drive", "way"], "before": ["be", "fore"], "even": ["e", "ven"], "neighbor": ["neigh", "bor"], "wasn't": ["was", "n't"], "coming": ["com", "ing"], "grandmother's": ["grand", "moth", "er's"], "middle": ["mid", "dle"], "winning": ["win", "ning"], "monday": ["Mon", "day"], "tuesday": ["Tues", "day"], "wednesday": ["Wednes", "day"], "thursday": ["Thurs", "day"], "bury": ["bur", "y"], "shovel": ["shov", "el"], "wouldn't": ["would", "n't"], "over": ["o", "ver"], "thumbnail": ["thumb", "nail"], "tower": ["tow", "er"], "over": ["o", "ver"], "brilliance": ["bril", "liance"], "valley": ["val", "ley"],
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
BARS = REC["bars"]; TOT = REC["total_eighths"]; NB = len(BARS)
VOC = sorted([dict(n, p=[n["midi"]]) for n in REC["lead"]], key=lambda n: n["on"])
texted(VOC)
SP = {0: "c", 1: "cis", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}   # D Dorian / F major (v65 fix 34)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
def split(pos, n, blen=8):
    """eighths. 4/4: a note crosses beat 3 only from beat 1. 5/4 (3+2): never across the group line at the fourth beat"""
    out = []
    while n > 0:
        if blen == 10:
            end = 6 if pos < 6 else 10
            room = min(n, end - pos)
            if pos == 0 and room >= 6: Lh = 6
            elif pos % 2 == 0 and room >= 4 and pos in (0, 2, 6): Lh = 4
            elif pos % 2 == 0 and room >= 3: Lh = 3
            elif pos % 2 == 0 and room >= 2: Lh = 2
            else: Lh = 1
        else:
            if pos == 0 and n >= 8: Lh = 8
            elif pos == 0 and n >= 6: Lh = 6
            elif pos % 4 == 0 and n >= 4: Lh = 4
            elif pos % 4 == 0 and n >= 3: Lh = 3
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
            sp = split(s - b["start"], m, b["len"])
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
    if n["sec"] == "Refrain 4" and n["line"] == 3 and n["syl"][0] == "and": GANG_MARK[(bar_at[n["on"]], n["on"])] = "(the band stops: alone, almost spoken)"
VB, LYR = stream(VOC, "r", lyric=True)
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
TXT = {"Outro": "Outro · D–A drone, let ring", "Break": "Break · the guitars interlock", "Build": "Build", "Intro": "Intro · guitar 1 alone, then guitar 2"}
def body(bybar, marks):
    toks = []; cur = None
    for bi in range(NB):
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if met != cur: toks.append("\\time 3,2 5/4" if met == "5/4" else "\\time 4/4"); cur = met
            if bi == 0: toks.append("\\tempo 4 = 132")
            k = BARS[bi]["key"]
            if bi == 0 or k != BARS[bi - 1]["key"]: toks.append("\\key d \\dorian" if k == "D Dorian" else "\\key f \\major")
            if marks: toks.append(f'\\mark \\markup \\box \\bold "{TXT.get(s, s)}"')
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"Dm": "d", "G": "g", "F": "f", "Am": "a", "C": "c", "Bb": "bes", "Gm": "g", "D5": "d", "Em": "e"}
QUAL = {"Dm": ":m", "Am": ":m", "Gm": ":m", "Em": ":m", "D5": ":1.5"}
chords = " ".join(("r1" if (b["sec"] == "Refrain 4" and b["start"] >= REC["stop_at"]) else f"{CHR[b['chord']]}{'4*5' if b['len'] == 10 else '1'}{QUAL.get(b['chord'], '')}") for b in BARS)   # N.C. where the band stops
vp = [n["midi"] for n in VOC]
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
assert min(vp) >= 50 and max(vp) == 70 and sum(1 for x in vp if x > 69) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (B♭4 once: “score”, the last refrain) · treble 8vb, sounding an octave lower · verses 5/4 felt 3+2, refrains 4/4"
footer2 = "Words and music: Jason Bryant"
src = f"""\\version "2.24.3"
#(set-global-staff-size 18)
\\header {{ title = "Either Or" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "angular art rock" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 28\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t page-count = 3 }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1.5 \\override LyricHyphen.minimum-distance = #0.6 }}
  \\context {{ \\Staff \\RemoveEmptyStaves }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff \\with {{ instrumentName = "Voice" \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble_8" \\new Voice = "voc" {{ {body(VB, True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(LYR)} }}
  >>
}}
"""
path, warns = compile_ly(src, "Either Or - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, notes in (("voice", VB, VOC),):
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = []
    for n in sorted(notes, key=lambda n: n["on"]): want += sorted(n["p"])
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
