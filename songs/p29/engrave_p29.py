"""Module 11.9 document 3: the engraved lead sheet of 'The Word Without a Word' (v64 port) from the song record -- the VOICE (written for
soprano; a tenor sings it an octave lower) with the lyric and chord names; 3/4 at q = 66, broadening to q = 56 for the final refrain;
D-flat major, E-flat from verse 4. The anchors (MA, ABBA) marked. Absolute pitches; LilyPond's MIDI read back."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p29", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p29 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p29/song_record.pkl", "rb"))
OUT = "/home/claude/p29/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"running": ["run", "ning"], "lying": ["ly", "ing"], "feeding": ["feed", "ing"], "single": ["sin", "gle"], "without": ["with", "out"],
        "sleeping": ["sleep", "ing"], "soften": ["sof", "ten"], "against": ["a", "gainst"], "thundered": ["thun", "dered"], "loses": ["los", "es"],
        "again": ["a", "gain"], "until": ["un", "til"], "reaches": ["reach", "es"], "abba": ["Ab", "ba"], "joseph": ["Jo", "seph"],
        "crying": ["cry", "ing"], "mother": ["moth", "er"]}
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
            parts = hyph_for(re.sub(r"[^A-Za-z']", "", w), len(r)) if len(r) > 1 else None
            tail = re.search(r"[^A-Za-z’']*$", w).group(0)
            for j, x in enumerate(r):
                if parts:
                    t = parts[j]
                    if j == len(parts) - 1: t += tail
                    x["text"] = t; x["hy"] = j < len(parts) - 1
                else:
                    x["text"] = w; x["hy"] = False
BARS = REC["bars"]; TOT = REC["total_eighths"]; NB = len(BARS)
VO = {"voc": sorted([dict(n, p=[n["midi"]]) for n in REC["lead"]], key=lambda n: n["on"])}
texted(VO["voc"])
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}   # D-flat / E-flat major (v65 fix 34)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2."}
def split(pos, n):
    """3/4 in eighths: a whole bar from the downbeat; a half note from beat 1 or 2; otherwise quarters and eighths on the beat"""
    out = []
    while n > 0:
        room = min(n, 6 - pos)
        if pos == 0 and room >= 6: Lh = 6
        elif pos in (0, 2) and room >= 4: Lh = 4
        elif pos % 2 == 0 and room >= 3: Lh = 3
        elif pos % 2 == 0 and room >= 2: Lh = 2
        else: Lh = 1
        out.append((pos, Lh)); pos += Lh; n -= Lh
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
def stream(notes):
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
                if kind == "r": tok = ("R2." if Lh == 6 else "r" + DUR[Lh])
                else:
                    tok = pname(n["p"][0]) + DUR[Lh] + ("~" if tie else "")
                    if first and n["on"] in MARKS: tok += '^\\markup \\italic \\small "' + MARKS[n["on"]] + '"'
                    if first:
                        w = n["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                        lyr.append(q + (" --" if n.get("hy") else ""))
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, lyr
MA = REC["ma"]["on"]; NOW = next(n["on"] for n in REC["lead"] if n["sec"] == "Bridge" and n["line"] == 3)
TURN = next(n["on"] for n in REC["lead"] if n["sec"] == "Bridge" and n["line"] == 3 and n["syl"][0] == "and")
WORLD = next(n["on"] for n in REC["lead"] if n["midi"] == 82)
MARKS = {MA: "held: nothing moves", NOW + 2: "the band silent", TURN: "everyone back", WORLD: "the one B♭"}
VB = {"voc": stream(VO["voc"])}
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
TXT = {"Intro": "Intro · piano", "Interlude": "Interlude · the cello sings her lullaby", "Bridge": "Bridge",
       "Verse 4": "Verse 4 · a step higher", "Refrain 3": "Refrain 3 · broadening", "Coda": "Coda · piano alone"}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 3/4", "\\tempo 4 = 66", "\\key des \\major"]
            if s == "Verse 4": toks.append("\\key ees \\major")
            if s == "Refrain 3": toks.append('\\tempo "Broadening" 4 = 56')
            if marks: toks.append(f'\\mark \\markup \\box \\bold "{TXT.get(s, s)}"')
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"Db": "des", "Gb": "ges", "Ab": "aes", "Bbm": "bes", "Fm": "f", "Ebm": "ees", "Bb": "bes", "Eb": "ees", "Cm": "c", "Gm": "g", "F": "f"}
QUAL = {"Bbm": ":m", "Fm": ":m", "Ebm": ":m", "Cm": ":m", "Gm": ":m"}
chords = " ".join(f"{CHR[b['chord']]}2.{QUAL.get(b['chord'], '')}" for b in BARS)
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
vp = [n["midi"] for n in VO["voc"]]
assert min(vp) >= 60 and max(vp) == 82 and sum(1 for x in vp if x > 81) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (B♭5 once: “world”, the last refrain) · written for soprano; a tenor sings it an octave lower"
footer2 = "Words and music: Jason Bryant · “ma” and “Abba” are the song’s anchors: hold them, and let nothing move under them"
src = f"""\\version "2.24.3"
#(set-global-staff-size 19)
\\header {{ title = "The Word Without a Word" subtitle = "Lead sheet · voice (soprano or tenor)" composer = "Words and music: Jason Bryant" meter = "a concert carol" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 24\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t page-count = 3 }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-0.8 \\override LyricHyphen.minimum-distance = #0.6 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble" \\new Voice = "voc" {{ {body(VB["voc"][0], True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(VB["voc"][1])} }}
  >>
}}
"""
path, warns = compile_ly(src, "The Word Without a Word - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name in ("voc",):
    BYB = VB[name][0]
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rRs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 3/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = [n["midi"] for n in VO[name]]
    print(f"readback ({name}):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
