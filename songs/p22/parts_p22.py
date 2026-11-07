"""The production parts pack for 'The Seam': four parts in one PDF -- SYNTH LEAD (every note of the intro, interlude, 48-bar 7/8
instrumental and outro lines), DRUMS, BASS and GUITAR -- each fully written out bar by bar from the same rules that play the demo
(demo_p22.py), without the demo's humanizing, so the charts and the demo agree. Keys and metres by section, rehearsal marks, bar
numbers, chord symbols. Absolute pitch, sounding (bass and guitar under 8vb clefs)."""
import pickle, collections, os, sys
sys.path.insert(0, "/home/claude/carol")
import lily
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p22/song_record.pkl", "rb"))
OUT = "/home/claude/p22/out"
BARS = REC["bars"]; NB = len(BARS); TOT = REC["total_eighths"]
SP = {0: ("c", ""), 1: ("d", "es"), 2: ("d", ""), 3: ("e", "es"), 4: ("e", ""), 5: ("f", ""), 6: ("f", "is"), 7: ("g", ""), 8: ("a", "es"),
      9: ("a", ""), 10: ("b", "es"), 11: ("b", "")}
def pname(p):
    l, a = SP[p % 12]; o = p // 12 - 4
    return l + a + ("'" * o if o > 0 else "," * (-o))
ROOT = {"Em": 4, "C": 0, "Am": 9, "G": 7, "F": 5, "Fm": 5, "Db": 1, "Bbm": 10}
TONES = {"Em": [4, 7, 11], "C": [0, 4, 7], "Am": [9, 0, 4], "G": [7, 11, 2], "F": [5, 9, 0], "Fm": [5, 8, 0], "Db": [1, 5, 8], "Bbm": [10, 1, 5]}
def voicing(ch, lo=52, n=4):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in TONES[ch]: out.append(p)
        p += 1
    return out
# ---- the band's rules (as the demo plays them) ----
bass, gtr, drums = [], [], collections.defaultdict(set)
for bi, b in enumerate(BARS):
    sec, ch, st, met = b["sec"], b["chord"], b["start"], b["meter"]
    k_in = bi - [x for x in range(NB) if BARS[x]["sec"] == sec][0]; nb_sec = sum(1 for x in BARS if x["sec"] == sec)
    first = k_in == 0; bld = b["build"]; quarter = (4 * k_in) // nb_sec if bld else 3
    r = 28 + ((ROOT[ch] - 28) % 12)
    cho = sec.startswith("Chorus"); verse = sec.startswith("Verse"); her = sec in ("Verse 1", "Verse 3")
    if sec == "Outro" and k_in == nb_sec - 1:
        bass.append(dict(on=st, dur=8, p=[r])); drums[st].add("cymc"); continue
    if sec in ("Intro", "Interlude", "Outro") and not (sec == "Intro" and k_in >= 4): continue
    if sec == "Ending":
        bass.append(dict(on=st, dur=8, p=[r])); continue
    if not bld or quarter >= 1:
        if met == "7/8":
            for e, d, p in ((0, 2, r), (2, 2, r), (4, 1, r), (5, 1, r + 7), (6, 1, r)): bass.append(dict(on=st + e, dur=d, p=[p]))
        elif verse:
            bass.append(dict(on=st, dur=4, p=[r])); bass.append(dict(on=st + 4, dur=2, p=[r]))
            if not her: bass.append(dict(on=st + 6, dur=2, p=[r + 7]))
        else:
            for e in range(0, 8, 2): bass.append(dict(on=st + e, dur=2, p=[r]))
    if verse and her:
        vo = voicing(ch, 55, 5)
        for e, i in enumerate([0, 2, 4, 3, 1, 3, 4, 2]): gtr.append(dict(on=st + e, dur=1, p=[vo[i]]))
    elif verse:
        for e in range(0, 8, 2): gtr.append(dict(on=st + e, dur=1, p=[r + 24], stacc=True))
    elif cho or (bld and quarter >= 3):
        for e in (range(8) if met == "4/4" else range(7)): gtr.append(dict(on=st + e, dur=1, p=[r + 12, r + 19, r + 24]))
    if met == "7/8":
        if quarter >= 2:
            for e in (0, 4): drums[st + e].add("bd")
            for e in (2, 5): drums[st + e].add("sn")
            for e in range(7): drums[st + e].add("hh" if quarter == 2 else "cymr")
            if k_in == nb_sec - 1:
                for i, t in enumerate(["tomh", "tommh", "tomml", "toml"]): drums[st + 3 + i].add(t)
    elif verse:
        drums[st].add("bd"); drums[st + 4].add("sn"); [drums[st + e].add("hh") for e in range(8)]
    elif cho:
        for e in (0, 3, 4): drums[st + e].add("bd")
        for e in (2, 6): drums[st + e].add("sn")
        for e in range(8): drums[st + e].add("cymr")
        if first: drums[st].add("cymc")
        if sec == "Chorus 3" and k_in == nb_sec - 1: drums[st].update({"cymc", "cymch"})
    elif sec == "Intro":
        drums[st].add("bd"); drums[st + 4].add("sn"); [drums[st + e].add("hh") for e in (0, 2, 4, 6)]
syn = [dict(on=n["on"], dur=n["dur"], p=[n["midi"]]) for n in REC["gtr"]]
# ---- notation ----
DUR = {1: "8", 2: "4", 3: "4.", 4: "2", 6: "2.", 8: "1"}
GROUPS = [(0, 2), (2, 4), (4, 7)]
def split(b, pos, n):
    out = []
    while n > 0:
        if b["meter"] == "4/4":
            if pos == 0 and n >= 8: L = 8
            elif pos == 0 and n >= 6: L = 6
            elif pos % 4 == 0 and n >= 4: L = 4
            elif pos % 4 == 0 and n >= 3: L = 3
            elif pos % 2 == 0 and n >= 2: L = 2
            else: L = 1
        else:
            g = next(g for g in GROUPS if g[0] <= pos < g[1]); room = g[1] - pos
            if pos == g[0] and room == 3 and n >= 3: L = 3
            elif room >= 2 and n >= 2: L = 2
            else: L = 1
        out.append((pos, L)); pos += L; n -= L
    return out
bar_at = []
for i, b in enumerate(BARS): bar_at += [i] * b["len"]
starts = {b0: (s, met) for s, nb, b0, met in REC["plan"]}
KEYLY = {"E minor": "\\key e \\minor", "F minor": "\\key f \\minor", "C major": "\\key c \\major"}
TIMELY = {"4/4": "\\time 4/4", "7/8": "\\time 2,2,3 7/8"}
FULLR = {"4/4": "R1", "7/8": "R8*7"}
def pitched(notes):
    notes = sorted(notes, key=lambda n: n["on"]); cur = 0; seq = []
    for n in notes:
        assert n["on"] >= cur, n
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list)
    for kind, s, d, n in seq:
        while d > 0:
            bi = bar_at[s]; b = BARS[bi]; m = min(d, b["start"] + b["len"] - s)
            sp = split(b, s - b["start"], m)
            for k, (pos, L) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = "r" + DUR[L]
                else:
                    ps = n["p"]; nm = pname(ps[0]) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    tok = nm + DUR[L] + ("~" if tie else "") + ("-." if n.get("stacc") else "")
                bybar[bi].append(tok)
            s += m; d -= m
    return bybar, sorted(notes, key=lambda n: n["on"])
def drumbar(bi):
    b = BARS[bi]; toks = []
    for e in range(b["len"]):
        s = drums.get(b["start"] + e)
        toks.append(("<" + " ".join(sorted(s)) + ">8") if s else "r8")
    return toks
RESTB = {}
def body(bybar, kind, cue_labels=None):
    RESTB[kind] = set(); toks = []; last_key = last_met = None; bi = 0
    while bi < NB:
        b = BARS[bi]
        if bi in starts:
            s, met = starts[bi]
            if bi > 0: toks.append('\\bar "||"')
            if met != last_met: toks.append(TIMELY[met]); last_met = met
            if bi == 0: toks.append("\\tempo 4 = 80")
            if kind != "drums" and b["key"] != last_key: toks.append(KEYLY[b["key"]]); last_key = b["key"]
            toks.append(f'\\mark \\markup \\box \\bold "{s}"')
        has = (any(t[0] != "r" for t in bybar.get(bi, [])) if kind != "drums" else bool([e for e in range(b["len"]) if drums.get(b["start"] + e)]))
        if not has:
            run = 1
            while bi + run < NB and (bi + run) not in starts and BARS[bi + run]["meter"] == b["meter"] and not (
                    any(t[0] != "r" for t in bybar.get(bi + run, [])) if kind != "drums" else any(drums.get(BARS[bi + run]["start"] + e) for e in range(BARS[bi + run]["len"]))):
                run += 1
            toks.append(f"{FULLR[b['meter']]}*{run}"); RESTB[kind].update(range(bi, bi + run)) if run > 1 else None; bi += run; continue
        bar = drumbar(bi) if kind == "drums" else bybar[bi]
        if cue_labels and b["sec"] in cue_labels and bi in starts:
            for j, t in enumerate(bar):
                if not t.startswith("r"): bar[j] = t + f'_\\markup \\italic \\small "{cue_labels[b["sec"]]}"'; break
        toks += bar; bi += 1
    return " ".join(toks)
CHR = {"Em": "e", "C": "c", "Am": "a", "G": "g", "F": "f", "Fm": "f", "Db": "des", "Bbm": "bes"}
QUAL = {"Em": ":m", "Am": ":m", "Fm": ":m", "Bbm": ":m"}
def chords_for(kind):
    out, i, rb = [], 0, RESTB.get(kind, set())
    while i < NB:
        b = BARS[i]
        if i in rb:
            j = i
            while j + 1 < NB and (j + 1) in rb and BARS[j + 1]["meter"] == b["meter"]: j += 1
            out.append(("s1" if b["meter"] == "4/4" else "s8*7") + f"*{j - i + 1}"); i = j + 1; continue
        out.append(f"{CHR[b['chord']]}{'1' if b['meter'] == '4/4' else '8*7'}{QUAL.get(b['chord'], '')}"); i += 1
    return " ".join(out)
chords = " ".join(f"{CHR[b['chord']]}{'1' if b['meter'] == '4/4' else '8*7'}{QUAL.get(b['chord'], '')}" for b in BARS)
SB, SN = pitched(syn); BB, BN = pitched(bass); GB, GN = pitched(gtr)
LAB = {"Intro": "warm saw lead", "Interlude": "", "Instrumental": "long notes (61-76) · quarters (77-92) · running eighths to C6 (93-108)", "Outro": "ends on A"}
NOTES = {
 "synth": "Synth lead -- every note, sounds as written. The motif is the chorus's opening ('a SEAM a-cross': up a third into a held note, a drop, a step up). Instrumental: 48 bars of 7/8 (2+2+3), the quarter steady at 80; plays the whole time.",
 "drums": "Drums -- verses half-time (kick 1, snare 3, eighth hats); choruses full time (kick 1, &2, 3; snare 2 and 4; ride; crash on each chorus's first bar); instrumental out until bar 85, then 2+2+3 (kick on groups 1 and 3, snare on group 2 and the middle of group 3; hats 85-96, ride 97-108; tom fill in 108); crash and china on the last 'we' (bar 116); out in the ending; one crash on the final F.",
 "bass": "Bass (sounds an octave below the written bass-clef notes) -- her verses: root on 1 (half) and 3; his verses: root on 1 and 3, the fifth on 4; choruses and intro 5-8: root quarters; instrumental from bar 73: 2+2+3 figure (root, root, root-fifth-root eighths); ending: one note a bar; final F.",
 "gtr": "Guitar (sounds an octave below the written treble notes) -- her verses: clean eighth arpeggios, let ring; his verses: a muted note on each quarter; choruses and instrumental 97-108: overdriven root-fifth-octave in eighths.",
}
def part(title, kind, music, clef, extra=""):
    staff = "DrumStaff" if kind == "drums" else "Staff"
    mode = "\\drummode" if kind == "drums" else ""
    cl = "" if kind == "drums" else f'\\clef "{clef}"'
    return f"""\\bookpart {{
  \\header {{ title = "The Seam" subtitle = "{title}" composer = "Words and music: Jason Bryant" tagline = ##f }}
  \\markup \\small \\wordwrap {{ {NOTES[kind]} }}
  \\score {{
    <<
      \\new ChordNames \\chordmode {{ {chords_for(kind)} }}
      \\new {staff} {{ {cl} \\compressMMRests {mode} {{ {extra} {music} \\bar "|." }} }}
    >>
    \\layout {{ \\context {{ \\Score \\override BarNumber.break-visibility = ##(#f #t #t) \\override RehearsalMark.self-alignment-X = #LEFT \\override RehearsalMark.font-size = #-1 }}
               \\context {{ \\Staff \\consists "Merge_rests_engraver" }} }}
  }}
}}
"""
MUS = dict(synth=body(SB, "synth", LAB), drums=body(None, "drums"), bass=body(BB, "bass"), gtr=body(GB, "gtr"))
src = f"""\\version "2.24.3"
\\paper {{ #(set-paper-size "letter") left-margin = 14\\mm right-margin = 14\\mm top-margin = 12\\mm bottom-margin = 14\\mm ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #12 }}
{part("Synth lead", "synth", MUS["synth"], "treble")}
{part("Drums", "drums", MUS["drums"], "")}
{part("Bass", "bass", MUS["bass"], "bass_8")}
{part("Guitar", "gtr", MUS["gtr"], "treble_8")}
"""
src = src.replace("Part(", "part(")
path, warns = compile_ly(src, "The Seam - parts (synth, drums, bass, guitar)", cwd=OUT)
print("compiled", path, "warnings:", warns[:6], f"({len(warns)} total)")
# readback: each pitched part against its notes; the synth against the record (and the demo's lead track)
os.makedirs(OUT + "/check", exist_ok=True)
for name, BYB, notes in (("synth", SB, SN), ("bass", BB, BN), ("guitar", GB, GN)):
    toks = [t.split("_\\markup")[0] for bi in range(NB) for t in BYB.get(bi, []) if not t.startswith("r")]
    chk = '\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }'
    compile_ly(chk, f"check_part_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_part_{name}.midi")[0]
    want = []
    for n in notes:
        b = BARS[bar_at[n["on"]]]
        want += sorted(n["p"]) if len(n["p"]) > 1 else n["p"]
    print(f"readback ({name}):", "matches" if sorted(got) == sorted(want) and len(got) == len(want) else f"MISMATCH ({len(got)} vs {len(want)})", len(got), "notes")
print("drum hits:", sum(len(v) for v in drums.values()), "· synth notes:", len(SN), "· bass notes:", len(BN), "· guitar events:", len(GN))
pickle.dump(dict(bass=BN, gtr=GN, drums={k: sorted(v) for k, v in drums.items()}, syn=SN), open(OUT + "/parts_events.pkl", "wb"))
