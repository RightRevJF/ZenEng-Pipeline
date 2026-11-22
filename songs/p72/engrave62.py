"""Song 62: the full score (voice, string quartet, piano), the lead sheet and the parts, engraved with LilyPond from out/<label>/record.json.
Everything is read from the record; durations sit on a sixteenth grid (the piano's and strings' held lengths are snapped to it).
  python3 engrave62.py "first edition"  -> out/<label>/<title> (<label>) - full score.pdf, - lead sheet.pdf, - parts.pdf; readback.json"""
import json, sys, os, re, subprocess, collections
import pyphen, mido
LABEL = sys.argv[1]; D = f"out/{LABEL}"; R = json.load(open(f"{D}/record.json")); B = R["bar"]; U = 3      # a sixteenth = 3 units
NB = sum(b for _, _, b in R["form"]); TITLE = R["title"]; FT = f"{TITLE} ({LABEL})"
NAMES = ["c", "des", "d", "ees", "e", "f", "ges", "g", "aes", "a", "bes", "b"]
def pn(m): o = m // 12 - 4; return NAMES[m % 12] + ("'" * o if o > 0 else "," * (-o))
def q(x): return int(round(x / U))
def events(part, mono=True):
    """[(start16, end16, pitches)] on the sixteenth grid, no overlaps"""
    ev = []
    for e in sorted(part, key=lambda e: e["on"]):
        ps = e["p"] if isinstance(e["p"], list) else [e["p"]]; s = q(e["on"]); t = max(s + 1, q(e["on"] + e["dur"]))
        if ev and ev[-1][0] == s: ev[-1] = (s, max(t, ev[-1][1]), sorted(set(ev[-1][2]) | set(ps))); continue
        ev.append((s, t, sorted(ps)))
    out = []
    for i, (s, t, ps) in enumerate(ev):
        nxt = ev[i + 1][0] if i + 1 < len(ev) else NB * 16
        if t > nxt: t = nxt
        if t - s >= 1: out.append((s, t, ps))
        if i + 1 < len(ev) and 0 < nxt - t <= 1 and not mono: out[-1] = (s, nxt, ps)
    return out
def pieces(s, e):
    """split [s, e) inside one bar (positions 0..16) into engraved lengths"""
    res = []
    while s < e:
        for v in (16, 12, 8, 6, 4, 3, 2, 1):
            if s + v > e: continue
            if v == 16 and s != 0: continue
            if v == 12 and s not in (0, 4): continue
            if v == 8 and s % 8: continue
            if v == 6 and (s % 4 or (s < 8 < s + 6)): continue
            if v == 4 and s % 4: continue
            if v == 3 and s % 4 not in (0,): continue
            if v == 2 and s % 2: continue
            res.append(v); s += v; break
    return res
DUR = {16: "1", 12: "2.", 8: "2", 6: "4.", 4: "4", 3: "8.", 2: "8", 1: "16"}
MARKS = {}; o = 0
for n, k, b in R["form"]:
    MARKS[o // B * 1] = n; o += b * B
def bar_starts(): return {o_: n for o_, n in MARKS.items()}
def music(part, mono=True, marks=True, rest="r"):
    """LilyPond notes for a part, bar by bar, with ties across beats and bars; returns (text, notes in order for lyrics)"""
    ev = events(part, mono); out = []; seq = []; i = 0; cur = 0
    starts = dict(MARKS)
    for bar in range(NB):
        b0, b1 = bar * 16, bar * 16 + 16; toks = []
        if marks and bar in starts: toks.append(f'\\mark \\markup \\box \\bold "{starts[bar]}"')
        pos = b0
        for (s, t, ps) in [x for x in ev if x[1] > b0 and x[0] < b1]:
            if s > pos: toks += [rest + DUR[v] for v in pieces(pos - b0, s - b0)]
            a, z = max(s, b0), min(t, b1); pp = pieces(a - b0, z - b0); first = s >= b0
            name = pn(ps[0]) if len(ps) == 1 else "<" + " ".join(pn(p) for p in ps) + ">"
            for j, v in enumerate(pp):
                tie = "~" if (j < len(pp) - 1 or t > b1) else ""
                toks.append(name + DUR[v] + tie)
            if first: seq.append((s, ps))
            pos = z
        if pos < b1: toks += [rest + DUR[v] for v in pieces(pos - b0, 16)]
        out.append(" ".join(toks) + " |")
    return "\n".join(out), seq
# lyrics: syllables per sung note, melisma notes extended
H = pyphen.Pyphen(lang="en_US"); mel = sorted(R["melody"], key=lambda n: n["on"])
OVR = {w_.replace("-", ""): w_.split("-") for w_ in "a-cross ev-ery re-mem-bered morn-ing morn-ings sat-ur-day fa-ther out-grew noth-ing coun-ter de-cem-ber cof-fee doc-tor mid-night on-ly ser-mon door-way nod-ded clos-et to-mor-row to-mor-row's him-self moth-er moth-er's wid-ow thir-ty de-cide be-fore o-pen go-ing to-day sun-day want-ed did-n't af-ter ev-ery".split()}
def syll(word, k):
    w = re.sub(r"[^A-Za-z']", "", word); p = list(OVR[w.lower()]) if w.lower() in OVR else (H.inserted(w).split("-") if w else [w])
    while len(p) > k: p[-2:] = [p[-2] + p[-1]]
    while len(p) < k: i_ = max(range(len(p)), key=lambda j: len(p[j])); s_ = p[i_]; c_ = max(1, len(s_) // 2); p[i_:i_ + 1] = [s_[:c_], s_[c_:] or s_[-1:]]
    return p
lyr = []; i = 0
while i < len(mel):
    w = mel[i]["text"]
    if not w: lyr.append("_"); i += 1; continue
    j = i
    while j < len(mel) and mel[j]["text"] == w and (j == i or mel[j]["line"] == mel[i]["line"]): j += 1
    k = j - i; ss = syll(w, k)
    for x, s_ in enumerate(ss):
        s_ = s_.replace("'", "’")
        lyr.append(('"' + s_ + '"') + (" --" if x < k - 1 else ""))
    i = j
LYR = " ".join(lyr)
def chordname(c):
    m = re.match(r"([A-G])(b|#)?(m|dim)?$", c); root = m.group(1).lower() + {"b": "es", "#": "is", None: ""}[m.group(2)]
    if root in ("ees",): root = "ees"
    if root == "aes" or root == "ees": pass
    return root, {"m": ":m", "dim": ":dim", None: ""}[m.group(3)]
NOTE = {"c": 0, "des": 1, "d": 2, "ees": 3, "e": 4, "f": 5, "ges": 6, "g": 7, "aes": 8, "a": 9, "bes": 10, "b": 11, "cis": 1, "dis": 3, "fis": 6, "gis": 8, "ais": 10}
BASSAT = {}
for e in R["parts"]["bass"]:
    if e["on"] % B == 0: BASSAT.setdefault(e["on"] // B, e["p"] if isinstance(e["p"], int) else e["p"][0])
def chords():
    out = []; bar_ = 0
    for n, k, b in R["form"]:
        for bar in R["chords"][n]:
            cs = bar.split(); ds = {1: ["1"], 2: ["2", "2"], 3: ["2", "4", "4"], 4: ["4"] * 4}[len(cs)]
            for x, (c, d_) in enumerate(zip(cs, ds)):
                r, qq = chordname(c); sl = ""
                if R.get("design") and k == "verse" and x == 0 and bar_ in BASSAT and BASSAT[bar_] % 12 != NOTE[r]:
                    sl = "/" + NAMES[BASSAT[bar_] % 12]
                out.append(f"{r}{d_}{qq}{sl}")
            bar_ += 1
    return " ".join(out)
voice, vseq = music([dict(on=n["on"], dur=n["dur"], p=n["midi"]) for n in mel])
parts = {k: music(R["parts"][k], mono=(k != "piano"), marks=False) for k in ("violin1", "violin2", "viola", "cello", "piano", "bass")}
KEY = "\\key ees \\major"; TIME = "\\time 4/4"; TEMPO = '\\tempo "Gently, with space" 4 = 72'
HEAD = f'''\\version "2.24.0"
\\paper {{ #(set-paper-size "letter") indent = 0 ragged-last-bottom = ##t }}
'''
def header(sub): return f'''\\header {{ title = "{TITLE}" subtitle = "{sub} ({LABEL})" composer = "Words and music: Jason Bryant" tagline = "{TITLE} ({LABEL}) · Words and music: Jason Bryant" }}'''
VOICE = f'\\new Staff \\with {{ instrumentName = "Voice" shortInstrumentName = "V." midiInstrument = "clarinet" }} {{ \\clef "treble_8" {KEY} {TIME} {TEMPO} \\new Voice = "v" {{ {voice} }} }}\n\\new Lyrics \\lyricsto "v" {{ {LYR} }}'
CH = f"\\new ChordNames {{ \\chordmode {{ {chords()} }} }}"
def staff(name, short, clef, mus, inst): return f'\\new Staff \\with {{ instrumentName = "{name}" shortInstrumentName = "{short}" midiInstrument = "{inst}" }} {{ \\clef "{clef}" {KEY} {TIME} {mus} }}'
PIANO = f'\\new PianoStaff \\with {{ instrumentName = "Piano" shortInstrumentName = "Pno." }} << {staff("", "", "treble", parts["piano"][0], "acoustic grand")} {staff("", "", "bass", parts["bass"][0], "acoustic grand")} >>'
STR = "\n".join([staff("Violin I", "Vln. I", "treble", parts["violin1"][0], "violin"), staff("Violin II", "Vln. II", "treble", parts["violin2"][0], "violin"), staff("Viola", "Vla.", "alto", parts["viola"][0], "viola"), staff("Cello", "Vc.", "bass", parts["cello"][0], "cello")])
score = HEAD + header("Full score: voice, string quartet and piano") + f'''
\\score {{ << {CH} {VOICE} \\new StaffGroup << {STR} >> {PIANO} >>
  \\layout {{ #(layout-set-staff-size 15) \\context {{ \\Staff \\RemoveAllEmptyStaves }} \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) }} }}
  \\midi {{ }} }}
'''
lead = HEAD + header("Lead sheet") + f'''
\\score {{ << {CH} {VOICE} >> \\layout {{ #(layout-set-staff-size 18) }} }}
'''
def part(name, short, clef, key):
    return f'''\\bookpart {{ \\header {{ title = "{TITLE}" subtitle = "{name} ({LABEL})" composer = "Words and music: Jason Bryant" tagline = "{TITLE} ({LABEL}) · {name}" }}
\\score {{ << {CH} \\new Staff {{ \\compressEmptyMeasures \\clef "{clef}" {KEY} {TIME} {TEMPO} {music(R["parts"][key], mono=(key != "piano"), marks=True)[0]} }} >> \\layout {{ #(layout-set-staff-size 18) }} }} }}
'''
pianopart = f'''\\bookpart {{ \\header {{ title = "{TITLE}" subtitle = "Piano ({LABEL})" composer = "Words and music: Jason Bryant" tagline = "{TITLE} ({LABEL}) · Piano" }}
\\score {{ << {CH} \\new Staff \\with {{ instrumentName = "Voice (cue)" }} {{ \\clef "treble_8" {KEY} {TIME} \\new Voice = "c" {{ \\teeny {voice} }} }} \\new PianoStaff << \\new Staff {{ \\clef treble {KEY} {TIME} {TEMPO} {music(R["parts"]["piano"], mono=False, marks=True)[0]} }} \\new Staff {{ \\clef bass {KEY} {TIME} {parts["bass"][0]} }} >> >> \\layout {{ #(layout-set-staff-size 16) }} }} }}
'''
parts_ly = HEAD + "\\book {\n" + pianopart + part("Violin I", "Vln. I", "treble", "violin1") + part("Violin II", "Vln. II", "treble", "violin2") + part("Viola", "Vla.", "alto", "viola") + part("Cello", "Vc.", "bass", "cello") + "}\n"
os.makedirs(f"{D}/ly", exist_ok=True)
for nm_, txt in (("full score", score), ("lead sheet", lead), ("parts", parts_ly)):
    p_ = f"{D}/ly/{nm_}.ly"; open(p_, "w").write(txt)
    r_ = subprocess.run(["lilypond", "-s", "-o", f"{D}/ly/{nm_}", p_], capture_output=True, text=True)
    if r_.returncode: print(nm_, r_.stderr[-2500:]); sys.exit(1)
    os.replace(f"{D}/ly/{nm_}.pdf", f"{D}/{FT} - {nm_}.pdf")
# readback: the full score's MIDI against the record, staff by staff (pitches in order, onsets on the grid)
mf = mido.MidiFile(f"{D}/ly/full score.midi"); tpb = mf.ticks_per_beat; got = []
for tr in mf.tracks:
    t = 0; ns = []
    for m in tr:
        t += m.time
        if m.type == "note_on" and m.velocity > 0: ns.append((round(t * 4 / tpb), m.note))
    if ns: got.append(sorted(ns))
want = {"voice": [(s, p) for s, ps in vseq for p in ps]} | {k: [(s, p) for s, ps in parts[k][1] for p in ps] for k in parts}
rb = {}
for k, w in want.items():
    w = sorted(w); match = any(g == w for g in got); rb[k] = dict(notes=len(w), matches_a_midi_staff=match)
json.dump(rb, open(f"{D}/readback.json", "w"), indent=1); print(rb)
