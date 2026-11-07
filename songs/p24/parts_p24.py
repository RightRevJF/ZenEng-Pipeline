"""The production parts pack for 'The Song You Sang Me': the GUITAR part as played -- capo 3, written in the D shapes (sounding a minor
third higher), standard notation over TAB with the strings fixed from the shapes (the bass on its string, the top three strings, the
lullaby's tune on the top strings), the shape names over the staff and the concert chords beneath. Written from the same events the
demo plays and the lead sheet shows (the song record), so all three agree."""
import pickle, collections, os, sys, re
sys.path[:0] = ["/home/claude/p24", "/home/claude/carol"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p24/song_record.pkl", "rb"))
OUT = "/home/claude/p24/out"; CAPO = REC["capo"]
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_eighths"]
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
OPEN = {1: 64, 2: 59, 3: 55, 4: 50, 5: 45, 6: 40}
def tune_string(p):
    for s in (1, 2, 3):
        if 0 <= p - OPEN[s] <= 5: return s
    return min((s for s in OPEN if p - OPEN[s] >= 0), key=lambda s: p - OPEN[s])
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
def k_in(bi): b = BARS[bi]; return bi - next(i for i, x in enumerate(BARS) if x["sec"] == b["sec"])
def strings_acc(e):
    ps = [p - CAPO for p in e["p"]]; bi = bar_at[e["on"]]; sh = REC["shape_of"][BARS[bi]["chord"]]
    out = []
    for p in ps:
        if p < 52 and len([q for q in ps if q < 52]) == 1 and p == min(ps):
            role = "bass_root" if (k_in(bi) % 2 == 0 or bi == NB - 1) else "bass_fifth"; s = REC["shape_strings"][role][sh]
            if p - OPEN[s] < 0 or p - OPEN[s] > 5: s = min((x for x in OPEN if p - OPEN[x] >= 0), key=lambda x: p - OPEN[x])
        else: s = 3 if p < 59 else (2 if p < 64 else 1)
        while p - OPEN[s] < 0: s += 1
        out.append((p, s))
    return out
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
def stream(events, rest, strfn):
    events = sorted(events, key=lambda e: e["on"]); cur = 0; seq = []
    for e in events:
        assert e["on"] >= cur, e
        if e["on"] > cur: seq.append(("r", cur, e["on"] - cur, None))
        seq.append(("n", e["on"], e["dur"], e)); cur = e["on"] + e["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list)
    for kind, s, d, e in seq:
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; m = min(d, b["start"] + b["len"] - s)
            sp = split(s - b["start"], m)
            for k, (pos, Lh) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": bybar[bi].append(rest + DUR[Lh])
                else:
                    ps = strfn(e)
                    bybar[bi].append("<" + " ".join(f"{pname(p)}\\{st}" for p, st in ps) + ">" + DUR[Lh] + ("~" if tie else "") + ("\\laissezVibrer" if (e.get("art") == "ring" and not tie and Lh == 6) else ""))
            s += m; d -= m
    return bybar
MB = stream(REC["gmel"], "s", lambda e: [(p - CAPO, tune_string(p - CAPO)) for p in e["p"]])
AB = stream(REC["gtr"], "r", strings_acc)
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
TXT = {"Intro": "the lullaby's tune on top", "Verse 1": "fingerpicked", "Chorus 1": "pinch on 1", "Verse 4": "one chord a bar, let ring", "Chorus 2": "pinch on 1 and 3", "Outro": "the tune; let the last chord ring"}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi == 0: toks += ["\\time 3/4", "\\key d \\major"] + (["\\tempo 4 = 76"] if marks else [])
        if bi in starts and marks:
            s, _ = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            toks.append(f'\\mark \\markup \\box \\bold "{s}{(" · " + TXT[s]) if s in TXT else ""}"')
        toks += bybar[bi]
    return " ".join(toks)
CHR = {"F": "f", "Bb": "bes", "C": "c", "Dm": "d", "Gm": "g", "Am": "a"}; QUAL = {"Dm": ":m", "Gm": ":m", "Am": ":m"}
chords = " ".join(f"{CHR[b['chord']]}2.{QUAL.get(b['chord'], '')}" for b in BARS)
tune, acc = body(MB, True), body(AB, False)
note = ("Guitar -- capo 3. Written as played, in D shapes; it sounds a minor third higher (F major). The TAB is counted from the capo. "
        "Verses 1-3: bass on 1 (the root, then the fifth the next bar), then the top three strings up and back, 1-2-3-2-1. Chorus 1: pinch the top string with the bass on 1; "
        "the last chorus: pinch on 1 and 3. Verse 4: one chord a bar, let it ring. Intro and outro: the lullaby's tune on the top strings over bass and chord.")
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #14 }}
\\header {{ title = "The Song You Sang Me" subtitle = "Guitar (capo 3, D shapes): notation and TAB" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\markup \\vspace #0.8
\\markup \\small \\wordwrap {{ {note} }}
\\markup \\vspace #1.2
\\score {{
  <<
    \\new ChordNames \\transpose f d {{ \\chordmode {{ {chords} }} }}
    \\new ChordNames \\with {{ \\override ChordName.font-size = #-2 }} {{ \\chordmode {{ \\set chordNameFunction = #(lambda (in-pitches bass inversion context) (make-line-markup (list (make-simple-markup "(") (ignatzek-chord-names in-pitches bass inversion context) (make-simple-markup ")")))) {chords} }} }}
    \\new Staff \\with {{ instrumentName = "Guitar" \\omit StringNumber }} <<
      \\clef "treble_8"
      \\new Voice {{ \\voiceOne {tune} \\bar "|." }}
      \\new Voice {{ \\voiceTwo {acc} }}
    >>
    \\new TabStaff \\with {{ instrumentName = "TAB" }} <<
      \\new TabVoice {{ {tune.replace(chr(92) + 'tempo 4 = 76', '')} }}
      \\new TabVoice {{ {acc} }}
    >>
  >>
  \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
             \\context {{ \\TabStaff \\remove "Bar_number_engraver" }} \\context {{ \\TabVoice \\omit Rest \\omit MultiMeasureRest \\omit Tie }} }}
}}
"""
src = re.sub(r'(\\new TabVoice \{\{? ?[^}]*?)\\mark \\markup \\box \\bold "[^"]*"', r'\1', src)
path, warns = compile_ly(src, "The Song You Sang Me - guitar part (capo 3, TAB)", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns][:5], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, events in (("tune", MB, REC["gmel"]), ("acc", AB, REC["gtr"])):
    toks = [re.sub(r"\\\\laissezVibrer", "", t) for bi in range(NB) for t in BYB[bi] if t[0] not in "rs"]
    toks = [re.sub(r"\\laissezVibrer", "", t) for t in toks]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 3/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_gpart_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_gpart_{name}.midi")[0]
    want = []
    for e in sorted(events, key=lambda e: e["on"]): want += sorted(p - CAPO for p in e["p"])
    print(f"readback ({name}, as played):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
