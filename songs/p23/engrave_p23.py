"""Module 11.9 document 3: the engraved lead sheet of 'What Holds' (v64 port) from the song record -- one staff: the voice (treble 8vb),
and the riff (27.21) as a CUE VOICE (small grey notes, the riff guitar named on its first bar). Keys by section (E minor; G major for
the choruses and the bridge), 4/4 at q = 104; chord symbols, lyrics, boxed section labels. \\relative c' per voice with the Python
trace; LilyPond's MIDI read back per voice."""
import pickle, re, sys, collections, os
sys.path.insert(0, "/home/claude/carol")
import lily
lily.SPELL.update({1: ("c", "is"), 3: ("d", "is"), 6: ("f", "is"), 8: ("g", "is"), 10: ("a", "is")})
from lily import relative_chain, trace, compile_ly, midi_readback
sys.path[:0] = ["/home/claude/p23", "/home/claude/pop"]
import lyric as L
import engine_p23 as _E, phrasestress48 as _P; _P.install(_E); _E.install_patches()
REC = pickle.load(open("/home/claude/p23/song_record.pkl", "rb"))
OUT = "/home/claude/p23/out"
import pyphen
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"granite": ["gran", "ite"], "river": ["riv", "er"], "every": ["ev", "ery"], "toward": ["to", "ward"], "empty": ["emp", "ty"],
        "over": ["o", "ver"], "against": ["a", "gainst"], "rafters": ["raf", "ters"], "away": ["a", "way"], "rubble": ["rub", "ble"],
        "between": ["be", "tween"], "towers": ["tow", "ers"], "kitchen": ["kitch", "en"], "muscle": ["mus", "cle"],
        "straightens": ["straight", "ens"], "because": ["be", "cause"]}      # v60 fix 5: the table
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
VOC = sorted([dict(n) for n in REC["lead"]], key=lambda n: n["on"])
RIF = sorted([dict(n) for n in REC["riff"]], key=lambda n: n["on"])
texted(VOC)
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
def split(b, pos, n):
    out = []
    while n > 0:
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
PV, PR = pieces_of(VOC), pieces_of(RIF)
chains = {}
for nm_, P_ in (("voc", PV), ("rif", PR)):
    ps = [p[3]["midi"] for p in P_ if p[1] == "n"]; chains[nm_] = relative_chain(ps); trace(chains[nm_], ps)
CHR = {"Em": "e", "C": "c", "D": "d", "G": "g", "Am": "a"}
QUAL = {"Em": ":m", "Am": ":m"}
chords = [f"{CHR[b['chord']]}1{QUAL.get(b['chord'], '')}" for b in BARS]
by = {k: collections.defaultdict(list) for k in ("voc", "rif")}
for k, P_ in (("voc", PV), ("rif", PR)):
    for p in P_: by[k][p[0]].append(p)
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
KEYLY = {"E minor": "\\key e \\minor", "G major": "\\key g \\major"}
CUE = {"Intro": "cue: riff guitar (overdriven) -- the changes pushed an eighth early", "Riff": "cue: riff guitar", "Outro": "cue: riff guitar"}
SECNOTE = {"Chorus 3": "band out: clean guitar and organ only", "Bridge": "builds", "Chorus 4": "everything"}
def has(ps): return any(p[1] == "n" for p in ps)
toks = {"voc": [], "rif": []}; lyr = []; ci = {"voc": 0, "rif": 0}
last_key, labelled = None, set()
def ntok(p, k, rest):
    bar_, kind, Lh, n, first, tie = p
    if kind == "r": return rest + DUR[Lh]
    l, a, marks, o = chains[k][ci[k]]; ci[k] += 1
    mk = "'" * marks if marks > 0 else "," * (-marks)
    return f"{l}{a}{mk}{DUR[Lh]}" + ("~" if tie else "")
for bi, b in enumerate(BARS):
    if bi in starts:
        s, met = starts[bi]
        if bi > 0: toks["voc"].append('\\bar "||"')
        if bi == 0: toks["voc"] += ["\\time 4/4", "\\tempo 4 = 104"]
        if b["key"] != last_key:
            for k in ("voc", "rif"): toks[k].append(KEYLY[b["key"]])
            last_key = b["key"]
        lab = s + (f" ({SECNOTE[s]})" if s in SECNOTE else "")
        toks["voc"].append(f'\\mark \\markup \\box \\bold "{lab}"')
    vv, vr = by["voc"][bi], by["rif"][bi]
    both = has(vv) and has(vr)
    for k, v, other in (("voc", vv, vr), ("rif", vr, vv)):
        if has(v):
            for p in v:
                t = ntok(p, k, "s" if (both or k == "rif") else "r")
                if k == "rif" and p[1] == "n" and b["sec"] in CUE and b["sec"] not in labelled:
                    t += f'^\\markup \\italic \\small "{CUE.get(b["sec"], "cue")}"'; labelled.add(b["sec"])
                toks[k].append(t)
                if k == "voc" and p[1] == "n" and p[4]:
                    w = p[3]["text"].replace("'", "’"); q = '"' + w + '"' if re.search(r"[’?!,.;:—]", w) else w
                    lyr.append(q + (" --" if p[3].get("hy") else ""))
        else:
            toks[k].append("s1" if (k == "rif" or has(other)) else "R1")
NM = ['C', 'C♯', 'D', 'D♯', 'E', 'F', 'F♯', 'G', 'G♯', 'A', 'A♯', 'B']; nm = lambda p: NM[p % 12] + str(p // 12 - 1)
vp = [n["midi"] for n in VOC]
assert min(vp) >= 52 and max(vp) == 69 and sum(1 for x in vp if x > 67) == 1
footer = f"Voice {nm(min(vp))}–{nm(max(vp))} (A4 once, the last “stand”) · small grey notes = the riff guitar"
footer2 = "Words and music: Jason Bryant · written in treble 8vb, sounding an octave lower · every chord change pushed an eighth early in the band"
grey = " ".join(f"\\override {g}.color = #(x11-color 'grey35)" for g in ("NoteHead", "Stem", "Beam", "Flag", "Rest", "Tie", "Accidental", "Dots"))
src = f"""\\version "2.24.3"
\\header {{
  title = "What Holds"
  subtitle = "Lead sheet"
  composer = "Words and music: Jason Bryant"
  meter = "driving rock"
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
    \\new Staff \\with {{ instrumentName = "Voice" }} <<
      \\clef "treble_8"
      \\new Voice = "voc" {{ \\relative c' {{ {" ".join(toks["voc"])} \\bar "|." }} }}
      \\new Voice = "rif" {{ \\relative c' {{ \\override NoteHead.font-size = #-1 {grey} {" ".join(toks["rif"])} }} }}
    >>
    \\new Lyrics \\lyricsto "voc" {{ {" ".join(lyr)} }}
  >>
}}
"""
path, warns = compile_ly(src, "What Holds - lead sheet", cwd=OUT)
print("compiled", path, "warnings:", [w for w in warns if "clashing" not in w][:6], f"({len(warns)} total)")
os.makedirs(OUT + "/check", exist_ok=True)
for name, k, P_ in (("voice", "voc", PV), ("riff", "rif", PR)):
    notes = " ".join(t.split("^")[0] for t in toks[k] if not t.startswith("\\") and t[0] not in "Rs")
    chk = f'\\version "2.24.3"\n\\score {{ \\new Staff {{ \\relative c\' {{ \\time 4/4 {notes} }} }} \\midi {{ }} }}'
    compile_ly(chk, f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    want = [p[3]["midi"] for p in P_ if p[1] == "n" and p[4]]
    print(f"readback ({name}):", "matches" if got == want else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "sounded notes")
print(footer)
