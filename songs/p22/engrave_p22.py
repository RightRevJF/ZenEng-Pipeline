"""Module 11.9 document 3: the engraved lead sheet of 'The Seam' (v64 port) from the song record -- a duet on two staves.
HER staff (treble): her verses and the chorus melody, and the instrumental lines as a CUE VOICE (small grey notes, the synth lead named
on its first bar). HIM staff (treble 8vb): his verses, his chorus harmony, his ending. Keys by section (E minor, F minor, C major), 4/4 at
q = 80 and the instrumental in 7/8 (2+2+3); chord symbols, lyrics under each staff, boxed section labels. \\relative c' per voice with the
Python trace; LilyPond's MIDI read back per voice."""
import pickle, re, sys, collections, os
sys.path.insert(0, "/home/claude/carol")
import lily
lily.SPELL.update({1: ("d", "es"), 3: ("e", "es"), 6: ("f", "is"), 8: ("a", "es"), 10: ("b", "es")})
from lily import relative_chain, trace, compile_ly, midi_readback
sys.path[:0] = ["/home/claude/p22", "/home/claude/pop"]
import lyric as L
import engine_p22 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p22/song_record.pkl", "rb"))
OUT = "/home/claude/p22/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"across": ["a", "cross"], "afraid": ["a", "fraid"], "against": ["a", "gainst"], "edges": ["edg", "es"], "nobody": ["no", "bod", "y"],
        "open": ["o", "pen"], "opens": ["o", "pens"], "record": ["rec", "ord"]}      # v60 fix 5: the table -- the dictionary's misses
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
BARS = REC["bars"]
HERN = sorted([dict(n) for n in REC["lead"] if n["singer"] == "her"], key=lambda n: n["on"])
HIMN = sorted([dict(n) for n in REC["lead"] if n["singer"] == "him"] + [dict(n) for n in REC["harm"]], key=lambda n: n["on"])
SYN = sorted([dict(n) for n in REC["gtr"]], key=lambda n: n["on"])
texted(HERN); texted([n for n in HIMN if not n["sec"].startswith("Chorus")]); texted([n for n in HIMN if n["sec"].startswith("Chorus")])
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
GROUPS = [(0, 2), (2, 4), (4, 7)]
def split(b, pos, n):
    out = []
    while n > 0:
        if b["meter"] == "4/4":
            if pos == 0 and n >= 8: Lh = 8
            elif pos == 0 and n >= 6: Lh = 6
            elif pos % 4 == 0 and n >= 4: Lh = 4
            elif pos % 4 == 0 and n >= 3: Lh = 3
            elif pos % 2 == 0 and n >= 2: Lh = 2
            else: Lh = 1
        else:
            g = next(g for g in GROUPS if g[0] <= pos < g[1]); room = g[1] - pos
            if pos == g[0] and room == 3 and n >= 3: Lh = 3
            elif room >= 2 and n >= 2: Lh = 2
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
            sp_ = split(b, s - b["start"], m)
            for k, (pos, Lh) in enumerate(sp_):
                lastp = k == len(sp_) - 1 and m == d
                out.append((bi, kind, Lh, n, first, kind == "n" and not lastp)); first = False
            s += m; d -= m
    return out
PH, PM, PS = pieces_of(HERN), pieces_of(HIMN), pieces_of(SYN)
chains = {}
for nm_, P_ in (("her", PH), ("him", PM), ("syn", PS)):
    ps = [p[3]["midi"] for p in P_ if p[1] == "n"]; chains[nm_] = relative_chain(ps); trace(chains[nm_], ps)
CHR = {"Em": "e", "C": "c", "Am": "a", "G": "g", "F": "f", "Fm": "f", "Db": "des", "Bbm": "bes"}
QUAL = {"Em": ":m", "Am": ":m", "Fm": ":m", "Bbm": ":m"}
BD = {"4/4": "1", "7/8": "8*7"}
chords = [f"{CHR[b['chord']]}{BD[b['meter']]}{QUAL.get(b['chord'], '')}" for b in BARS]
by = {k: collections.defaultdict(list) for k in ("her", "him", "syn")}
for k, P_ in (("her", PH), ("him", PM), ("syn", PS)):
    for p in P_: by[k][p[0]].append(p)
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
KEYLY = {"E minor": "\\key e \\minor", "F minor": "\\key f \\minor", "C major": "\\key c \\major"}
TIMELY = {"4/4": "\\time 4/4", "7/8": "\\time 2,2,3 7/8"}
FULLR = {"4/4": "R1", "7/8": "R8*7"}; FULLS = {"4/4": "s1", "7/8": "s8*7"}
CUE = {"Intro": REC["instrument"]["label"], "Interlude": "cue: synth lead", "Instrumental": "cue: synth lead (the city comes apart: a build)", "Outro": "cue: synth lead"}
def has(ps): return any(p[1] == "n" for p in ps)
toks = {"her": [], "him": [], "syn": []}; lyr = {"her": [], "him": []}; ci = {"her": 0, "him": 0, "syn": 0}
last_key, last_met, labelled = None, None, set()
def ntok(p, k, rest):
    bar_, kind, Lh, n, first, tie = p
    if kind == "r": return rest + DUR[Lh]
    l, a, marks, o = chains[k][ci[k]]; ci[k] += 1
    mk = "'" * marks if marks > 0 else "," * (-marks)
    return f"{l}{a}{mk}{DUR[Lh]}" + ("~" if tie else "")
for bi, b in enumerate(BARS):
    if bi in starts:
        s, met = starts[bi]
        if bi > 0: toks["her"].append('\\bar "||"'); toks["him"].append('\\bar "||"')
        if met != last_met:
            toks["her"].append(TIMELY[met]); last_met = met
            if bi == 0: toks["her"].append("\\tempo 4 = 80")
        if b["key"] != last_key:
            for k in ("her", "him", "syn"): toks[k].append(KEYLY[b["key"]])
            last_key = b["key"]
        toks["her"].append(f'\\mark \\markup \\box \\bold "{s}"')
    vh, vs, vm = by["her"][bi], by["syn"][bi], by["him"][bi]
    both = has(vh) and has(vs)
    for k, v, other in (("her", vh, vs), ("syn", vs, vh)):
        if has(v):
            for p in v:
                t = ntok(p, k, "s" if (both or k == "syn") else "r")
                if k == "syn" and p[1] == "n" and b["sec"] not in labelled:
                    t += f'^\\markup \\italic \\small "{CUE.get(b["sec"], "cue")}"'; labelled.add(b["sec"])
                toks[k].append(t)
                if k == "her" and p[1] == "n" and p[4]:
                    w = p[3]["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                    lyr["her"].append(q + (" --" if p[3].get("hy") else ""))
        else:
            toks[k].append(FULLS[b["meter"]] if (k == "syn" or has(other)) else FULLR[b["meter"]])
    if has(vm):
        for p in vm:
            toks["him"].append(ntok(p, "him", "r"))
            if p[1] == "n" and p[4]:
                w = p[3]["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                lyr["him"].append(q + (" --" if p[3].get("hy") else ""))
    else: toks["him"].append(FULLR[b["meter"]])
NM = ['C','D♭','D','E♭','E','F','F♯','G','A♭','A','B♭','B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
hp = [n["midi"] for n in HERN]; mp = [n["midi"] for n in HIMN]
assert min(hp) >= 57 and max(hp) == 72 and sum(1 for x in hp if x > 67) == 1 and min(mp) >= 52 and max(mp) <= 69
footer = f"Her {nm(min(hp))}–{nm(max(hp))} (C5 once, the last “we”) · Him {nm(min(mp))}–{nm(max(mp))} (A4 once, under her C5) · small grey notes = the synth lead"
footer2 = "Words and music: Jason Bryant · his staff is written in treble 8vb and sounds an octave lower · the instrumental in 7/8 (2+2+3), the quarter steady"
grey = " ".join(f"\\override {g}.color = #(x11-color 'grey35)" for g in ("NoteHead", "Stem", "Beam", "Flag", "Rest", "Tie", "Accidental", "Dots"))
src = f"""\\version "2.24.3"
\\header {{
  title = "The Seam"
  subtitle = "Lead sheet (duet)"
  composer = "Words and music: Jason Bryant"
  meter = "prog rock"
  tagline = ##f
}}
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 24\\mm
  oddFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  evenFooterMarkup = \\markup \\column {{ \\fill-line {{ \\tiny "{footer}" }} \\fill-line {{ \\tiny "{footer2}" }} }}
  system-system-spacing.basic-distance = #14 ragged-last-bottom = ##t }}
\\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT
  \\override RehearsalMark.font-size = #-1 }}
  \\context {{ \\Staff \\consists "Merge_rests_engraver" }}
  \\context {{ \\Lyrics \\override LyricText.font-size = #-1 \\override LyricHyphen.minimum-distance = #1.0 }} }}
\\score {{
  <<
    \\new ChordNames \\chordmode {{ {" ".join(chords)} }}
    \\new Staff \\with {{ instrumentName = "Her" }} <<
      \\clef "treble"
      \\new Voice = "her" {{ \\relative c' {{ {" ".join(toks["her"])} \\bar "|." }} }}
      \\new Voice = "syn" {{ \\relative c' {{ \\override NoteHead.font-size = #-1 {grey} {" ".join(toks["syn"])} }} }}
    >>
    \\new Lyrics \\lyricsto "her" {{ {" ".join(lyr["her"])} }}
    \\new Staff \\with {{ instrumentName = "Him" }} <<
      \\clef "treble_8"
      \\new Voice = "him" {{ \\relative c' {{ {" ".join(toks["him"])} }} }}
    >>
    \\new Lyrics \\lyricsto "him" {{ {" ".join(lyr["him"])} }}
  >>
}}
"""
path, warns = compile_ly(src, "The Seam - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, k, P_ in (("her", "her", PH), ("him", "him", PM), ("synth", "syn", PS)):
    notes = " ".join(t.split("^")[0] for t in toks[k] if not t.startswith("\\") and t[0] not in "Rs")
    chk = f'\\version "2.24.3"\n\\score {{ \\new Staff {{ \\relative c\' {{ \\time 4/4 {notes} }} }} \\midi {{ }} }}'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = [p[3]["midi"] for p in P_ if p[1] == "n" and p[4]]
    print(f"readback ({name}):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "sounded notes")
print(footer)
