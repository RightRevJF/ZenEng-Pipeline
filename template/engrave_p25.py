"""Module 11.9 document 3: the engraved lead sheet of 'Through Its Breaking' (v64 port) from the song record -- the VOICE (treble) with the
lyric, and beneath it a cue of the piano's bell figure (a piano grand staff: the crack above, the toll below), shown only where the bell
plays (intro, interludes, bridge bars 9-16, chorus 3, tag, outro). Chord names above. 6/8 at dotted-q = 54, A minor / C major (one key
signature). Absolute pitches; LilyPond's MIDI read back per voice."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p25", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p25 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p25/song_record.pkl", "rb"))
OUT = "/home/claude/p25/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"thumbnail": ["thumb", "nail"], "tower": ["tow", "er"], "over": ["o", "ver"], "brilliance": ["bril", "liance"], "valley": ["val", "ley"],
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
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}   # A minor: the leading tones sharp
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 6: "2."}
def split(pos, n):
    """6/8: never across the bar's second dotted-quarter beat"""
    out = []
    while n > 0:
        if pos == 0 and n >= 6: Lh = 6
        elif pos in (0, 3) and n >= 3: Lh = 3
        elif pos % 3 in (0, 1) and n >= 2: Lh = 2
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
CRACK = [dict(e) for e in REC["bell"] if e["kind"] == "crack"]; TOLL = [dict(e) for e in REC["bell"] if e["kind"] == "toll"]
CB, _ = stream(CRACK, "r"); TB, _ = stream(TOLL, "r")
BELLBAR = {i for i, b in enumerate(BARS) if b["bell"]}
for BYB in (CB, TB):
    for bi in range(NB):
        if bi not in BELLBAR: BYB[bi] = ["s2."]
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts and marks:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 6/8", "\\key a \\minor", "\\tempo 4. = 54"]
            toks.append(f'\\mark \\markup \\box \\bold "{s}"')
        elif bi == 0: toks += ["\\time 6/8", "\\key a \\minor"]
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"F": "f", "C": "c", "G": "g", "E": "e", "Em": "e", "Dm": "d", "Am": "a"}
QUAL = {"Dm": ":m", "Em": ":m", "Am": ":m"}
chords = " ".join(f"{CHR[b['chord']]}2.{QUAL.get(b['chord'], '')}" for b in BARS)
vp = [n["midi"] for n in VOC]
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
assert min(vp) >= 57 and max(vp) == 72 and sum(1 for x in vp if x > 71) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (C5 once: “through”, chorus 3) · Bell cue: low toll; the crack = root + half step below"
footer2 = "Words and music: Jason Bryant"
src = f"""\\version "2.24.3"
\\header {{ title = "Through Its Breaking" subtitle = "Lead sheet: voice, with the piano’s bell cue" composer = "Words and music: Jason Bryant" meter = "slow 6/8, felt in two" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 24\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #13 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1 \\override LyricHyphen.minimum-distance = #1.0 }}
  \\context {{ \\Staff \\RemoveEmptyStaves }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff \\with {{ instrumentName = "Voice" \\override VerticalAxisGroup.remove-empty = ##f }} {{ \\clef "treble" \\new Voice = "voc" {{ {body(VB, True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(LYR)} }}
    \\new PianoStaff \\with {{ instrumentName = \\markup \\small "Bell (pno)" shortInstrumentName = \\markup \\small "Bell" }} <<
      \\new Staff \\with {{ fontSize = #-3 \\override StaffSymbol.staff-space = #(magstep -3) \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "treble" {body(CB, False)} }}
      \\new Staff \\with {{ fontSize = #-3 \\override StaffSymbol.staff-space = #(magstep -3) \\override VerticalAxisGroup.remove-first = ##t }} {{ \\clef "bass" {body(TB, False)} }}
    >>
  >>
}}
"""
path, warns = compile_ly(src, "Through Its Breaking - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, notes in (("voice", VB, VOC), ("crack", CB, CRACK), ("toll", TB, TOLL)):
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rs" and not t.startswith("s2.")]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = []
    for n in sorted(notes, key=lambda n: n["on"]): want += sorted(n["p"])
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
