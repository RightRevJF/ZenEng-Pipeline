"""Module 11.9 document 3: the engraved lead sheet of 'Make Do' (v64 port) from the song record. One staff, treble 8vb (baritone),
4/4 at q = 72 in G major, chord symbols, lyrics, boxed section labels -- and the INSTRUMENTAL LINES (Module 27.21) as a CUE VOICE
(11.9 as amended in v64): small grey notes on the vocal staff, no lyrics, the instrument and its clef named on the line's first bar,
the sung voice's bar rest giving way to it, the cue stepping aside where a sung pickup reaches into its bars. \\relative c' per voice
with the Python trace; LilyPond's MIDI read back after, per voice."""
import pickle, re, sys, collections, os
sys.path.insert(0, "/home/claude/carol")
import lily
lily.SPELL.update({1: ("c", "is"), 3: ("d", "is"), 6: ("f", "is"), 8: ("g", "is"), 10: ("a", "is")})
from lily import relative_chain, trace, compile_ly, midi_readback
sys.path[:0] = ["/home/claude/p21", "/home/claude/pop"]
import lyric as L
import engine_p21 as _E0, phrasestress48 as _P0; _P0.install(_E0); _E0.install_patches()
REC = pickle.load(open("/home/claude/p21/song_record.pkl", "rb"))
OUT = "/home/claude/p21/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
# v59 fix 10: printed breaks from the SPELLING (a hyphenation dictionary), the note count from the phones; more notes than breaks
# print as a melisma. The dictionary's misses, corrected by hand and logged: its two-letter margins leave short words whole (ver-y,
# man-y, var-y, e-lites, u-nit-ed), it misses a hiatus (vid-e-os) and a split (glut-ton-ous, dam-na-tion), and the made-up title is
# broken by the writer's own syllables (Q10 A).
HFIX = {"against": ["a", "gainst"], "footwell": ["foot", "well"], "leather": ["leath", "er"], "tremor": ["trem", "or"], "cattywumpus": ["cat", "ty", "wum", "pus"]}   # v60 fix 5: the table -- the dictionary's misses
class _H(dict):
    def get(self, w, default=None):
        w = w.lower()
        parts = HFIX.get(w) or _PY.inserted(w).split("-")
        return parts if len(parts) > 1 else default
HYPH = _H()
def hyph_for(w, nnotes):
    parts = HFIX.get(w.lower()) or _PY.inserted(w.lower()).split("-")
    if len(parts) > nnotes: parts = parts[:nnotes - 1] + ["".join(parts[nnotes - 1:])]
    if len(parts) < nnotes: parts = parts + ["_"] * (nnotes - len(parts))      # the melisma
    return parts
SEC = {s: items for s, items in L.SECTIONS}
SECMAP_OLD = {"I. Falling In": "I. Falling In", "Refrain 1": "Refrain 1", "II. England in the Carpet": "II. England in the Carpet",
          "Refrain 2": "Refrain 2", "III. The Faces": "III. The Faces", "Refrain 3": "Refrain 3", "IV. The Lamp": "IV. The Lamp",
          "Chorus 1": "Chorus 1", "Return": "Return", "Chorus 2": "Chorus 2", "Ending": "Ending"}
ev = sorted([dict(n) for n in REC["lead"]], key=lambda n: n["on"])
groups = collections.OrderedDict()
for n in ev: groups.setdefault((n["sec"], n["line"]), []).append(n)
for (sec, li), ns in groups.items():
    words = SEC[sec][li][1].split()
    import engine_p21 as _E
    runs = []
    for w in words:
        k = len(_E.syllables(w)); runs.append(ns[:k]); ns = ns[k:]
    assert not ns and all(runs), (sec, li, words)
    for w, r in zip(words, runs):
        parts = hyph_for(re.sub(r"[^A-Za-z']", "", w), len(r)) if len(r) > 1 else None
        tail = re.search(r"[^A-Za-z’']*$", w).group(0); cap = w[:1].isupper()
        for j, x in enumerate(r):
            if parts:
                t = parts[j]
                if j == 0: t = (t[0].upper() + t[1:]) if cap else (t[0].lower() + t[1:])
                if j == len(parts) - 1: t += tail
                x["text"] = t; x["hy"] = j < len(parts) - 1
            else:
                x["text"] = w; x["hy"] = False
        if parts and "_" in parts:                        # v59 fix 10: the extra notes print as a melisma
            j0 = parts.index("_"); r[j0 - 1]["text"] = r[j0 - 1]["text"].rstrip(re.search(r"[^A-Za-z’']*$", w).group(0)) + " __"; r[j0 - 1]["hy"] = False
            for x in r[j0:]: x["text"] = "_"; x["hy"] = False
BARS = REC["bars"]
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
def split(pos, n):
    out = []
    while n > 0:
        if pos == 0 and n >= 8: Lh = 8
        elif pos % 4 == 0 and n >= 6 and pos == 0: Lh = 6
        elif pos % 4 == 0 and n >= 4: Lh = 4
        elif pos % 4 == 0 and n >= 3: Lh = 3
        elif pos % 2 == 0 and n >= 2: Lh = 2
        else: Lh = 1
        out.append((pos, Lh)); pos += Lh; n -= Lh
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
TOT = REC["total_eighths"]
def pieces_of(notes):
    cur, seq = 0, []
    for n in notes:
        s, d = int(n["on"]), int(n["dur"])
        assert s >= cur, ("overlap", n)
        if s > cur: seq.append(("r", cur, s - cur, None))
        seq.append(("n", s, d, n)); cur = s + d
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    out = []
    for kind, s, d, n in seq:
        first = True
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; be = b["start"] + b["len"]; m = min(d, be - s)
            sp_ = split(s - b["start"], m)
            for k, (pos, Lh) in enumerate(sp_):
                lastp = k == len(sp_) - 1 and m == d
                out.append((bi, kind, Lh, n, first, kind == "n" and not lastp)); first = False
            s += m; d -= m
    return out
GT = sorted([dict(n) for n in REC["gtr"]], key=lambda n: n["on"])
PV, PG = pieces_of(ev), pieces_of(GT)
chainV = relative_chain([p[3]["midi"] for p in PV if p[1] == "n"]); trace(chainV, [p[3]["midi"] for p in PV if p[1] == "n"])
chainG = relative_chain([p[3]["midi"] for p in PG if p[1] == "n"]); trace(chainG, [p[3]["midi"] for p in PG if p[1] == "n"])
CHR = {"Gmaj7": "g", "Cmaj7": "c", "D": "d", "Em7": "e", "Am7": "a", "G": "g"}
QUAL = {"Gmaj7": ":maj7", "Cmaj7": ":maj7", "Em7": ":m7", "Am7": ":m7"}
chords = [f"{CHR[b['chord']]}1{QUAL.get(b['chord'], '')}" for b in BARS]
byV, byG = collections.defaultdict(list), collections.defaultdict(list)
for p in PV: byV[p[0]].append(p)
for p in PG: byG[p[0]].append(p)
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
KEYLY = {"G major": "\\key g \\major"}
GLAB = {"Intro": REC["instrument"]["label"], "Break": "cue: clean guitar (the light comes in)", "Outro": "cue: clean guitar"}
def has_notes(ps): return any(p[1] == "n" for p in ps)
toksV, toksG, lyr = [], [], []
ci = {"V": 0, "G": 0}; last_key = None; labelled = set()
def note_tok(p, chain, which, rest_tok):
    bar_, kind, Lh, n, first, tie = p
    if kind == "r": return rest_tok + DUR[Lh]
    l, a, marks, o = chain[ci[which]]; ci[which] += 1
    mk = "'" * marks if marks > 0 else "," * (-marks)
    return f"{l}{a}{mk}{DUR[Lh]}" + ("~" if tie else "")
bi = 0
while bi < len(BARS):
    b = BARS[bi]
    if bi in starts:
        s, met = starts[bi]
        if bi > 0: toksV.append('\\bar "||"')
        if bi == 0: toksV += ["\\time 4/4", "\\tempo 4 = 72"]
        if b["key"] != last_key: toksV.append(KEYLY[b["key"]]); toksG.append(KEYLY[b["key"]]); last_key = b["key"]
        toksV.append(f'\\mark \\markup \\box \\bold "{s}"')
    v, g = byV[bi], byG[bi]
    hv, hg = has_notes(v), has_notes(g)
    if not hv and not hg:                                  # nobody: the voice rests the bar, the guitar a spacer
        run = 1
        while bi + run < len(BARS) and (bi + run) not in starts and not has_notes(byV[bi + run]) and not has_notes(byG[bi + run]): run += 1
        toksV.append(f"R1*{run}"); toksG.append(f"s1*{run}"); bi += run; continue
    both = hv and hg
    if hv:
        for p in v:
            toksV.append(note_tok(p, chainV, "V", "s" if both else "r"))
            if p[1] == "n" and p[4]:
                w = p[3]["text"].replace("'", "’")
                q = '"' + w + '"' if re.search(r"[’?!,.;—]", w) else w
                lyr.append(q + (" --" if p[3].get("hy") else ""))
    else: toksV.append("s1")
    if hg:
        sec = b["sec"]
        for k, p in enumerate(g):
            t = note_tok(p, chainG, "G", "s" if both else "r")
            if p[1] == "n" and sec not in labelled:
                t += f'^\\markup \\italic \\small "{GLAB.get(sec, "cue")}"'; labelled.add(sec)
            toksG.append(t)
    else: toksG.append("s1")
    bi += 1
NM = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
pitches = [n["midi"] for n in ev]
lo, hi = min(pitches), max(pitches)
assert lo >= 47 and hi <= 62 and sum(1 for n in ev if n["midi"] == 62) == 1
footer = f"Voice {nm(lo)}–{nm(hi)}: the verses to A3, the chorus B3 on “do” · D4 once, the last “do” · small grey notes = the cue (clean guitar)"
footer2 = "Words and music: Jason Bryant · ZenEng v64 · 2026 · treble 8vb sounds an octave lower (voice and guitar)"
src = f"""\\version "2.24.3"
\\header {{
  title = "Make Do"
  subtitle = "Lead sheet"
  composer = "Words and music: Jason Bryant"
  meter = "dream-pop"
  tagline = ##f
}}
\\paper {{ #(set-paper-size "letter") left-margin = 15\\mm right-margin = 15\\mm top-margin = 12\\mm bottom-margin = 26\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #15 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT
  \\override RehearsalMark.font-size = #-1 \\compressEmptyMeasures }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-0.5 \\override LyricHyphen.minimum-distance = #1.0 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {" ".join(chords)} }}
    \\new Staff \\with {{ \\consists "Merge_rests_engraver" }} <<
      \\clef "treble_8"
      \\new Voice = "mel" {{ \\relative c' {{ {" ".join(toksV)} \\bar "|." }} }}
      \\new Voice = "gtr" {{ \\relative c' {{ \\override NoteHead.font-size = #-1 \\override NoteHead.color = #(x11-color 'grey35) \\override Stem.color = #(x11-color 'grey35) \\override Beam.color = #(x11-color 'grey35) \\override Flag.color = #(x11-color 'grey35) \\override Rest.color = #(x11-color 'grey35) \\override Tie.color = #(x11-color 'grey35) {" ".join(toksG)} }} }}
    >>
    \\new Lyrics \\lyricsto "mel" {{ {" ".join(lyr)} }}
  >>
}}
"""
path, warns = compile_ly(src, "Make Do - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, toks, P in (("voice", toksV, PV), ("guitar", toksG, PG)):
    notes = " ".join(t.split("^")[0] for t in toks if not t.startswith("\\") and not t[0] in "Rs")
    notes = " ".join(x for x in notes.split() if not x.startswith("s"))
    chk = f'\\version "2.24.3"\n\\score {{ \\new Staff {{ \\relative c\' {{ \\time 4/4 {notes} }} }} \\midi {{ }} }}'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = [p[3]["midi"] for p in P if p[1] == "n" and p[4]]
    print(f"readback ({name}):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "sounded notes")
print(footer)
