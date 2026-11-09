"""Module 11.9 document 3: the engraved lead sheet of 'I Took Him for the Gardener' (v64 port) from the song record -- the VOICE with
the lyric and chord names; 6/8 at dotted quarter = 52, broadening for the last refrain; D minor, D major from MARY. The anchors (NAME,
MARY) and the summit marked; EARTH's A5 carries an F#5 ossia. Two co-equal editions (fix 92), chosen with ZVOICE=soprano|mezzo:
SOPRANO (D minor / D major, as written) and MEZZO (a minor third lower: B minor / B major). Absolute pitches; LilyPond's MIDI read back."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p32", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p32 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p32/song_record.pkl", "rb"))
OUT = "/home/claude/p32/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"spices": ["spi", "ces"], "gardener": ["gar", "den", "er"], "linen": ["lin", "en"], "lying": ["ly", "ing"], "folded": ["fold", "ed"],
        "itself": ["it", "self"], "either": ["ei", "ther"], "between": ["be", "tween"], "someone": ["some", "one"], "among": ["a", "mong"],
        "only": ["on", "ly"], "body": ["bod", "y"], "mary": ["Ma", "ry"], "rabboni": ["Rab", "bo", "ni"], "garden": ["gar", "den"],
        "evening": ["eve", "ning"], "answered": ["an", "swered"], "again": ["a", "gain"], "carried": ["car", "ried"], "instead": ["in", "stead"]}
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
VERSION = os.environ.get("ZVOICE", "soprano"); SHIFT = -3 if VERSION == "mezzo" else 0; VCLEF = "treble"
KEYS = {"soprano": ("d", "D"), "mezzo": ("b", "B")}[VERSION]
VO = {"voc": sorted([dict(n, p=[n["midi"] + SHIFT]) for n in REC["lead"]], key=lambda n: n["on"])}
texted(VO["voc"])
SP = ({0: "c", 1: "cis", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"} if VERSION == "soprano" else
      {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"})   # sharps from the key: C# (D minor), A# (B minor)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2."}
def split(pos, n):
    """6/8: two dotted quarters; nothing crosses the middle of the bar except a whole bar from its downbeat"""
    out = []
    while n > 0:
        if pos == 0 and n >= 6: Lh = 6
        else:
            end = 3 if pos < 3 else 6; room = min(n, end - pos)
            Lh = 3 if (pos % 3 == 0 and room >= 3) else (2 if room >= 2 else 1)
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
NAME = next(n["on"] for n in REC["lead"] if n["sec"] == "The Name" and n["line"] == 2 and n["syl"][0] == "name")
MARYON = REC["mary"]["on"]
EARTH = next(n["on"] for n in REC["lead"] if n["midi"] == 81)
WAS = next(n["on"] for n in REC["lead"] if n["sec"] == "Refrain 3" and n["line"] == 4 and n["syl"][0] == "was")
MARKS = {NAME: "the band silent", MARYON: KEYS[1] + " major: everyone back, softly", EARTH: "the one " + ("A5" if VERSION == "soprano" else "F♯5"), WAS: "closed"}
VB = {"voc": stream(VO["voc"])}
OSS_BI = bar_at[EARTH]                                    # the ossia bar (F#5 for A5; the mezzo's D#5 for F#5)
def ossia_tokens(toks):
    out, done = [], False
    for t in toks:
        t = t.split("^")[0]
        if not done and t.startswith(pname(81 + SHIFT)): t = pname(78 + SHIFT) + t[len(pname(81 + SHIFT)):]; done = True
        out.append(t)
    assert done
    return out
OSS_STAFF = ('\\new Staff \\with { alignAboveContext = #"vstaff" fontSize = #-3 \\override StaffSymbol.staff-space = #(magstep -3) '
             '\\remove "Time_signature_engraver" firstClef = ##f \\override KeySignature.stencil = ##f } '
             '{ \\clef "' + VCLEF + '" \\key ' + KEYS[0] + ' \\major ')
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
TXT = {"Intro": "Intro · piano", "Interlude": "Interlude · the cello sings the refrain", "The Name": "The Name",
       "Verse 4": "Verse 4 · the garden", "Coda": "Coda · piano alone: the refrain returns"}
MARY_BI = bar_at[MARYON]
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 6/8", "\\tempo 4. = 52", f"\\key {KEYS[0]} \\minor"]
            if s == "Refrain 3": toks.append('\\tempo "Broadening" 4. = 48')
            if s == "Coda": toks.append('\\tempo "Slower" 4. = 44')
            if marks: toks.append(f'\\mark \\markup \\box \\bold "{TXT.get(s, s)}"')
        if bi == MARY_BI: toks += ['\\bar "||"', f"\\key {KEYS[0]} \\major"]
        if marks and bi == OSS_BI:
            toks += ["<<", "{", *bybar[bi], "}", OSS_STAFF, '\\once \\override TextScript.font-size = #-2', ossia_tokens(bybar[bi])[0] + '^"ossia"', *ossia_tokens(bybar[bi])[1:], "}", ">>"]
        else: toks += bybar[bi]
    return " ".join(toks)
ROOTPC = {"Dm": 2, "Gm": 7, "Bb": 10, "F": 5, "C": 0, "A": 9, "Am": 9, "D": 2, "G": 7, "Bm": 11, "Em": 4, "F#m": 6}
LN = {0: "c", 1: "cis", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "bes", 11: "b"}
def chord_tok(ch):
    if ch == "N.C.": return "r2."
    r = (ROOTPC[ch] + SHIFT) % 12
    return f"{LN[r]}2." + (":m" if ch.endswith("m") else "")
def chord_name(ch):
    if ch == "N.C.": return ch
    r = (ROOTPC[ch] + SHIFT) % 12
    return {0: "C", 1: "C♯", 2: "D", 3: "E♭", 4: "E", 5: "F", 6: "F♯", 7: "G", 8: "G♯", 9: "A", 10: "B♭", 11: "B"}[r] + ("m" if ch.endswith("m") else "")
chords = " ".join(chord_tok(b["chord"]) for b in BARS)
NM = (['C', 'C♯', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'B♭', 'B'] if VERSION == "soprano" else ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B'])
nm = lambda p: NM[p % 12] + str(p // 12 - 1)
vp = [n["p"][0] for n in VO["voc"]]
assert min(vp) >= 62 + SHIFT and max(vp) == 81 + SHIFT and sum(1 for x in vp if x >= 81 + SHIFT) == 1
footer = (f"Soprano edition · D minor, D major from “Mary” · {nm(min(vp))}–{nm(max(vp))} (A5 once: “earth”, the last refrain; F♯5 ossia) · the mezzo edition is a minor third lower"
          if VERSION == "soprano" else
          f"Mezzo edition · B minor, B major from “Mary” · {nm(min(vp))}–{nm(max(vp))} (F♯5 once: “earth”, the last refrain; D♯5 ossia) · the soprano edition is a minor third higher")
footer2 = "Words and music: Jason Bryant · “name” is sung alone; “Mary” brings the major: sing it quietly, as he would say it"
src = f"""\\version "2.24.3"
#(set-global-staff-size 19)
\\header {{ title = "I Took Him for the Gardener" subtitle = "Lead sheet · {VERSION} edition" composer = "Words and music: Jason Bryant" meter = "an Easter solo · John 20" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 24\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-0.8 \\override LyricHyphen.minimum-distance = #0.6 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff = "vstaff" \\with {{ instrumentName = "{VERSION.capitalize()}" }} {{ \\clef "{VCLEF}" \\new Voice = "voc" {{ {body(VB["voc"][0], True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(VB["voc"][1])} }}
  >>
}}
"""
path, warns = compile_ly(src, f"I Took Him for the Gardener - lead sheet ({VERSION})", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name in ("voc",):
    BYB = VB[name][0]
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rRs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}_{VERSION}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}_{VERSION}.midi")[0]
    want = [n["p"][0] for n in VO[name]]
    print(f"readback ({name}):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
