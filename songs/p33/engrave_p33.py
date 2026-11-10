"""Module 11.9 document 3: the engraved lead sheet of 'Sadie' (v74) from the song record -- the VOICE (a baritone, treble 8vb) with the
lyric and chord names, and the GANG's 'Sadie! Sadie!' as cue notes above it; 4/4 at q = 124; A major. The drop (bars 61-64: the band cut,
N.C.), the gang lines and the one F#4 marked. Absolute pitches; LilyPond's MIDI read back."""
import pickle, re, sys, collections, os
sys.path[:0] = ["/home/claude/p33", "/home/claude/carol", "/home/claude/pop"]
from lily import compile_ly, midi_readback
import lyric as L
import engine_p33 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p33/song_record.pkl", "rb"))
OUT = "/home/claude/p33/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"seconds": ["sec", "onds"], "bleachers": ["bleach", "ers"], "rumble": ["rum", "ble"], "under": ["un", "der"], "every": ["ev", "ery"],
        "coffee": ["cof", "fee"], "daughter": ["daugh", "ter"], "number": ["num", "ber"], "jacket": ["jack", "et"], "never": ["nev", "er"],
        "lettered": ["let", "tered"], "somebody": ["some", "bod", "y"], "behind": ["be", "hind"], "sadie": ["Sa", "die"],
        "pounding": ["pound", "ing"], "aluminum": ["a", "lu", "mi", "num"], "thousand": ["thou", "sand"], "hollering": ["hol", "ler", "ing"],
        "only": ["on", "ly"], "over": ["o", "ver"], "clothesline": ["clothes", "line"], "miller": ["Mil", "ler"], "holder": ["hold", "er"],
        "laces": ["lac", "es"], "quiet": ["qui", "et"], "moving": ["mov", "ing"], "gonna": ["gon", "na"]}
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
SP = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}   # sharps from the key (A major)
def pname(p):
    o = p // 12 - 4
    return SP[p % 12] + ("'" * o if o > 0 else "," * (-o))
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
def split(pos, n):
    """4/4 in eighths: a whole bar from the downbeat; a half from beat 1 or 3; nothing else crosses the middle of the bar"""
    out = []
    while n > 0:
        end = 8 if pos >= 4 or (pos == 0 and n >= 8) else 4
        room = min(n, end - pos)
        if pos == 0 and room >= 8: Lh = 8
        elif pos % 4 == 0 and room >= 6 and pos == 0: Lh = 6
        elif pos % 4 == 0 and room >= 4: Lh = 4
        elif pos % 2 == 0 and room >= 3: Lh = 3
        elif pos % 2 == 0 and room >= 2: Lh = 2
        else: Lh = 1
        out.append((pos, Lh)); pos += Lh; n -= Lh
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
def stream(notes, marks=None, texts=True):
    marks = marks or {}
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
                if kind == "r": tok = ("R1" if Lh == 8 else "r" + DUR[Lh])
                else:
                    tok = (pname(n["p"][0]) if len(n["p"]) == 1 else "<" + " ".join(pname(q) for q in sorted(n["p"])) + ">") + DUR[Lh] + ("~" if tie else "")
                    if first and n["on"] in marks: tok += '^\\markup \\italic \\small "' + marks[n["on"]] + '"'
                    if first and texts:
                        w = n["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                        lyr.append(q + (" --" if n.get("hy") else ""))
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, lyr
lead = REC["lead"]
NEV = next(n["on"] for n in lead if n["sec"] == "Chorus 4" and n["syl"][0] == "never" and n["syl"][2])
UP = next(n["on"] for n in lead if n["sec"] == "Drop" and n["syl"][0] == "it's")
MARKS = {NEV: "the one F♯4", UP: "the band cut: alone"}
for s_ in ("Chorus 1", "Chorus 2", "Chorus 3"):
    MARKS[next(n["on"] for n in lead if n["sec"] == s_)] = "with the gang"
MARKS[next(n["on"] for n in lead if n["sec"] == "Chorus 4")] = "everyone: the gang sings the whole chorus"
VB = {"voc": stream(VO["voc"], MARKS)}
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
TXT = {"Intro": "Intro · the riff", "Riff": "Riff", "Drop": "Drop · the band cut (N.C.)", "Chorus 4": "Last chorus · the crowd", "Outro": "Outro · the riff"}
def body(bybar, marks):
    toks = []
    for bi in range(NB):
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if bi == 0: toks += ["\\time 4/4", "\\tempo 4 = 124", "\\key a \\major"]
            if marks: toks.append(f'\\mark \\markup \\box \\bold "{TXT.get(s, s)}"')
        toks += bybar[bi]
    return " ".join(toks)
ROOTPC = {"A": 9, "D": 2, "E": 4, "F#m": 6, "Bm": 11, "C#m": 1}
LN = {0: "c", 1: "cis", 2: "d", 3: "dis", 4: "e", 5: "f", 6: "fis", 7: "g", 8: "gis", 9: "a", 10: "ais", 11: "b"}
def chord_tok(ch, dur="1"):
    if ch == "N.C.": return "r" + dur
    return f"{LN[ROOTPC[ch]]}{dur}" + (":m" if ch.endswith("m") else "")
chords = " ".join(chord_tok(b["chord"]) for b in BARS)
NM = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
vp = [n["p"][0] for n in VO["voc"]]
assert min(vp) >= 45 and max(vp) == 66 and sum(1 for x in vp if x >= 66) == 2     # NEV-er: both syllables of the one F#4
footer = f"Baritone (sounds an octave lower) · {nm(min(vp))}–{nm(max(vp))}, F♯4 once (“never”) · the gang: “Sadie! Sadie!” in every chorus, all of the last chorus"
footer2 = "Words and music: Jason Bryant · bars 61–64, the drop: the band cuts on beat 1; “It’s up.” alone; the kick’s heartbeat only"
if __name__ == "__main__":
    src = f"""\\version "2.24.3"
#(set-global-staff-size 19)
\\header {{ title = "Sadie" subtitle = "Lead sheet" composer = "Words and music: Jason Bryant" meter = "country-rock, 4/4" tagline = ##f }}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 24\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #f #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-0.8 \\override LyricHyphen.minimum-distance = #0.6 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {chords} }}
    \\new Staff = "vstaff" \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\compressMMRests {{ \\new Voice = "voc" {{ {body(VB["voc"][0], True)} \\bar "|." }} }} }}
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(VB["voc"][1])} }}
  >>
}}
"""
    src = src.replace("\\compressMMRests {", "{")
    path, warns = compile_ly(src, "Sadie - lead sheet", cwd=OUT)
    print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
    os.makedirs(OUT + "/check", exist_ok=True)
    toks = [t.split("^")[0] for bi in range(NB) for t in VB["voc"][0][bi] if t[0] not in "rR"]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, "check_voc", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_voc.midi")[0]
    want = [n["p"][0] for n in VO["voc"]]
    print("readback (voice):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
    print(footer)
