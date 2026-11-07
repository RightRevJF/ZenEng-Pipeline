"""Module 11.9 document 3: the engraved lead sheet of 'Tinted Glass' (v64 port) from the song record -- a duet on two staves that never
sound together: HER (treble) and HIM (treble 8vb), each with its own lyric; a staff hides where its singer rests. 6/8 at dotted-q = 54,
Eb major throughout (no key change), chord names, boxed section labels. Absolute pitches; LilyPond's MIDI read back per staff."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p28", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p28 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p28/song_record.pkl", "rb"))
OUT = "/home/claude/p28/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"visiting": ["vis", "it", "ing"], "furniture": ["fur", "ni", "ture"], "company": ["com", "pa", "ny"], "vinyl": ["vi", "nyl"],
        "over": ["o", "ver"], "every": ["ev", "ery"], "window": ["win", "dow"], "twenty": ["twen", "ty"], "shaking": ["shak", "ing"],
        "glasses": ["glass", "es"], "together": ["to", "geth", "er"], "county": ["coun", "ty"], "dollars": ["dol", "lars"],
        "fourteen": ["four", "teen"], "about": ["a", "bout"], "strangers": ["strang", "ers"], "giggles": ["gig", "gles"],
        "memorizing": ["mem", "o", "riz", "ing"], "enough": ["e", "nough"], "behind": ["be", "hind"], "tinted": ["tint", "ed"],
        "breathing": ["breath", "ing"], "people": ["peo", "ple"], "someday": ["some", "day"], "sunday": ["Sun", "day"],
        "sundays": ["Sun", "days"], "waiting": ["wait", "ing"], "second": ["sec", "ond"], "never": ["nev", "er"], "again": ["a", "gain"],
        "coffee": ["cof", "fee"], "before": ["be", "fore"], "traded": ["trad", "ed"], "couldn't": ["could", "n't"], "away": ["a", "way"]}
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
VO = {k: sorted([dict(n, p=[n["midi"]]) for n in REC["lead"] if n["singer"] == k], key=lambda n: n["on"]) for k in ("her", "him")}
texted(VO["her"]); texted(VO["him"])
SP = {0: "c", 1: "des", 2: "d", 3: "ees", 4: "e", 5: "f", 6: "ges", 7: "g", 8: "aes", 9: "a", 10: "bes", 11: "b"}   # Eb major (v65 fix 34)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 6: "2."}
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
                    if first:
                        w = n["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                        lyr.append(q + (" --" if n.get("hy") else ""))
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, lyr
VB = {k: stream(VO[k]) for k in ("her", "him")}
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
TXT = {"Intro": "Intro · electric piano", "Outro": "Outro · electric piano alone, let it ring", "Bridge": "Bridge · the lines traded",
       "Chorus 3": "Chorus 3 · him", "Chorus 4": "Chorus 4 · her (never together)"}
WHO = {"Verse 1": "him", "Verse 2": "her", "Chorus 1": "him", "Verse 3": "him", "Verse 4": "her", "Chorus 2": "her", "Verse 5": "him", "Verse 6": "her"}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 6/8", "\\tempo 4. = 54", "\\key ees \\major"]
            if marks:
                lab = TXT.get(s, f"{s} · {WHO[s]}" if s in WHO else s)
                toks.append(f'\\mark \\markup \\box \\bold "{lab}"')
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"Eb": "ees", "Ab": "aes", "Bb": "bes", "Cm": "c", "Fm": "f", "Gm": "g"}
QUAL = {"Cm": ":m", "Fm": ":m", "Gm": ":m"}
chords = " ".join(f"{CHR[b['chord']]}2.{QUAL.get(b['chord'], '')}" for b in BARS)
NM = ['C', 'D♭', 'D', 'E♭', 'E', 'F', 'F♯', 'G', 'A♭', 'A', 'B♭', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
hp = [n["midi"] for n in VO["her"]]; mp = [n["midi"] for n in VO["him"]]
assert max(hp) == 72 and sum(1 for x in hp if x > 70) == 1 and max(mp) == 60 and sum(1 for x in mp if x > 58) == 1
footer = f"Her {nm(min(hp))}–{nm(max(hp))} (C5 once: “fog”, her last chorus) · Him {nm(min(mp))}–{nm(max(mp))} (C4 once: “fog”, his last chorus) · they never sing at once"
footer2 = "Words and music: Jason Bryant · his staff is written in treble 8vb and sounds an octave lower · 6/8, felt in two"
src = f"""\\version "2.24.3"
#(set-global-staff-size 18)
\\header {{ title = "Tinted Glass" subtitle = "Lead sheet (duet)" composer = "Words and music: Jason Bryant" meter = "slow-burn soul" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 13\\mm right-margin = 13\\mm top-margin = 12\\mm bottom-margin = 26\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #13 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1.2 \\override LyricHyphen.minimum-distance = #0.6 }}
  \\context {{ \\Staff \\RemoveEmptyStaves \\override VerticalAxisGroup.remove-first = ##t }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff = "her" \\with {{ instrumentName = "Her" shortInstrumentName = "Her" }} {{ \\clef "treble" \\new Voice = "her" {{ {body(VB["her"][0], True)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "her" {{ {" ".join(VB["her"][1])} }}
    \\new Staff = "him" \\with {{ instrumentName = "Him" shortInstrumentName = "Him" }} {{ \\clef "treble_8" \\new Voice = "him" {{ {body(VB["him"][0], False)} \\bar "|." }} }}
    \\new Lyrics \\lyricsto "him" {{ {" ".join(VB["him"][1])} }}
  >>
}}
"""
path, warns = compile_ly(src, "Tinted Glass - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name in ("her", "him"):
    BYB = VB[name][0]
    toks = [t for bi in range(NB) for t in BYB[bi] if t[0] not in "rRs"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 6/8 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = [n["midi"] for n in VO[name]]
    print(f"readback ({name}):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print(footer)
