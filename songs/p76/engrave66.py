"""'They Did the Right Thing' (song 66) -- the lead sheet and the parts, written bar by bar from song_record.pkl (build66.py, from lyric66_d.hand.song.json).
In A minor (keyinfo66), q = 72, all 4/4; grid: twelfths of a beat. Chord symbols by the half-bar. The tenor written on the treble 8 clef, at sounding pitch
(an octave under the treble). Guitar strums as rhythm slashes under the chord names; drums on a drum staff, hands up and feet down.
Adapted from songs/p71/engrave61.py. Every pitched staff is read back from LilyPond's MIDI; slashes and drum hits are counted."""
import pickle, collections, os, sys, re, json
sys.path[:0] = ["/home/claude/carol", "/home/claude/p76"]
from lily import compile_ly, midi_readback
REC = pickle.load(open("/home/claude/p76/song_record.pkl", "rb"))
import keyinfo66 as KI
_NM = KI.NM; _ps = [n["midi"] for n in REC["lead"]]
OUT = "/home/claude/p76/out"; os.makedirs(OUT + "/check", exist_ok=True)
BARS = REC["bars"]; NB = len(BARS); TOT = REC["end"]
BST = [x["start"] for x in BARS]; BLEN = [x["len"] for x in BARS]
def bar_of(t):
    lo, hi = 0, NB - 1
    while lo < hi:
        m = (lo + hi + 1) // 2
        if BST[m] <= t: lo = m
        else: hi = m - 1
    return lo
SP = KI.SP             # the record's key
def pname(p, nxt=None):
    o = p // 12 - 4
    return KI.lily_dir(p, nxt) + KI.lily_octave(p, nxt)
DUR = {3: "16", 6: "8", 9: "8.", 12: "4", 18: "4.", 24: "2", 36: "2.", 48: "1"}
def split(pos, n, L):
    """a note of n twelfths at pos in a bar of L, written as tied values that keep the bar's beats (7/8: 2+2+3 eighths)."""
    groups = [0, 12, 24, 42] if L == 42 else list(range(0, L + 1, 12))
    out = []
    while n > 0:
        nxt_g = min(g for g in groups if g > pos) if any(g > pos for g in groups) else L
        if L == 48 and pos == 0 and n >= 48: Lx = 48
        elif L == 48 and pos == 0 and n >= 36: Lx = 36
        elif L == 48 and pos in (0, 24) and n >= 24: Lx = 24
        elif L == 48 and pos in (0, 24) and n >= 18: Lx = 18
        elif L == 42 and pos == 24 and n >= 18: Lx = 18
        elif pos % 12 == 0 and n >= 12 and pos + 12 <= nxt_g: Lx = 12
        elif pos % 12 == 0 and n >= 9: Lx = 9
        elif pos % 6 == 0 and n >= 6: Lx = 6
        else: Lx = 3
        if pos % 12: Lx = min(Lx, 12 - pos % 12)
        Lx = min(Lx, L - pos)
        while Lx not in DUR: Lx -= 3
        out.append((pos, Lx)); pos += Lx; n -= Lx
    return out
starts = {}
for s, nb, st, mets, mv in REC["plan"]: starts[bar_of(st)] = s
def pitched(notes, namer=None, ties=True):
    """notes: dicts with on, dur, p (list), art. Returns tokens per bar, and the pitch list read in order."""
    notes = sorted(notes, key=lambda n: (n["on"], -len(n["p"]))); cur = 0; seq = []
    dedup = []
    for n in notes:
        if dedup and dedup[-1]["on"] == n["on"]: dedup[-1] = dict(dedup[-1], p=sorted(set(dedup[-1]["p"] + n["p"]))); continue
        dedup.append(dict(n))
    notes = dedup
    for i, n in enumerate(notes): n["nxt"] = notes[i + 1]["p"][0] if i + 1 < len(notes) and len(n["p"]) == 1 and len(notes[i + 1]["p"]) == 1 else None
    for i, n in enumerate(notes):
        nxt = notes[i + 1]["on"] if i + 1 < len(notes) else TOT
        n["dur"] = max(3, min(int(round(n["dur"] / 3)) * 3, nxt - n["on"]))
    for n in notes:
        assert n["on"] >= cur, (n, cur)
        if n["on"] > cur: seq.append(("r", cur, n["on"] - cur, None))
        seq.append(("n", n["on"], n["dur"], n)); cur = n["on"] + n["dur"]
    if cur < TOT: seq.append(("r", cur, TOT - cur, None))
    bybar = collections.defaultdict(list); want = []
    for kind, s, d, n in seq:
        first = True
        while d > 0:
            bi = bar_of(s); m = min(d, BST[bi] + BLEN[bi] - s)
            sp = split(s - BST[bi], m, BLEN[bi])
            for k, (pos, L) in enumerate(sp):
                tie = kind == "n" and not (k == len(sp) - 1 and m == d)
                if kind == "r": tok = "r" + DUR[L]
                else:
                    ps = n["p"]
                    if namer: nm = namer(ps[0]) if len(ps) == 1 else "<" + " ".join(namer(p) for p in ps) + ">"
                    else: nm = pname(ps[0], n.get("nxt")) if len(ps) == 1 else "<" + " ".join(pname(p) for p in ps) + ">"
                    tok = nm + DUR[L] + ("~" if tie and ties else "")
                    if n.get("slur_open") and first: tok += "("
                    if n.get("slur_close") and not tie and k == len(sp) - 1 and m == d: tok += ")"
                    if first: want += sorted(ps)
                bybar[bi].append(tok); first = False
            s += m; d -= m
    return bybar, want
METER_TOK = {"4/4": "\\time 4/4", "7/8": "\\time 2,2,3 7/8", "5/4": "\\time 5/4"}
REST_UNIT = {"4/4": ("1", 1), "7/8": ("8", 7), "5/4": ("4", 5)}
RAMP = {}
def tempo_tok(sec): return '\\tempo "Dark, steady" 4 = 72' if sec == "Intro" else ""
def body(bybar, marks, multirest=True):
    toks = [KI.LILY_KEY]; bi = 0; rest_bars = set(); met = None
    def has_(i): return any(t[0] != "r" for t in bybar.get(i, []))
    while bi < NB:
        if BARS[bi]["meter"] != met: met = BARS[bi]["meter"]; toks.append(METER_TOK[met])
        if bi in starts:
            if bi > 0: toks.append('\\bar "||"')
            txt = marks.get(starts[bi], ""); sec_ = starts[bi]
            if sec_ in RAMP: txt = (txt + "; " if txt else "") + ("accel." if RAMP[sec_][1] > RAMP[sec_][0] else "rit.") + f" to {RAMP[sec_][1]}"
            if bi == 0: toks.append(tempo_tok(sec_))
            toks.append(f'\\mark \\markup \\box \\bold "{SHORT.get(sec_, sec_)}{(" · " + txt) if txt else ""}"')
        if multirest and not has_(bi):
            run = 1
            while bi + run < NB and (bi + run) not in starts and BARS[bi + run]["meter"] == met and not has_(bi + run): run += 1
            u, k = REST_UNIT[met]; toks.append(f"R{u}*{k * run}"); rest_bars.update(range(bi, bi + run)); bi += run; continue
        toks += bybar[bi]; bi += 1
    toks.append('\\bar "|."')
    return " ".join(toks), rest_bars
ROOTN = {"C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "A": "a", "B": "b", "Bb": "bes", "Eb": "ees", "Ab": "aes", "F#": "fis"}
QUALN = {"": "", "7": ":7", "m": ":m", "m7": ":m7", "add9": ":9^7", "sus2": ":sus2", "sus4": ":sus4", "maj7": ":maj7", "dim7": ":dim7"}
def cho(c, d):
    base, _, bs = c.partition("/")
    rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]; q_ = base[len(rt_):]
    return f"{KI.lily_root(rt_)}{d}{QUALN[q_]}" + (f"/{KI.lily_root(bs)}" if bs else "")
def chords_for(rest_bars):
    out, i = [], 0
    while i < NB:
        met = BARS[i]["meter"]; u, k = REST_UNIT[met]
        if i in rest_bars:
            j = i
            while j + 1 < NB and (j + 1) in rest_bars and (j + 1) not in starts and BARS[j + 1]["meter"] == met: j += 1
            out.append(f"s{u}*{k * (j - i + 1)}"); i = j + 1; continue
        if BARS[i].get('beats4'): out.append(' '.join(cho(c_, '4') for c_ in BARS[i]['beats4'])); i += 1; continue
        a_, b_ = BARS[i]['chord'], BARS[i]['chord2']
        if met == "4/4" and a_ != b_: out.append(f"{cho(a_, '2')} {cho(b_, '2')}")
        else: out.append(cho(a_, f"{u}*{k}"))
        i += 1
    return " ".join(out)
def esc(t): return t.replace('"', '\\"')
def readback(name, bybar, want):
    toks = [re.sub(r"[()]", "", t) for b in sorted(bybar) for t in bybar[b] if not t.startswith(("r", "R"))]
    compile_ly('\\version "2.24.3"\n\\score { \\new Staff { \\time 4/4 ' + " ".join(toks) + ' } \\midi { } }', f"check_{name}", cwd=OUT + "/check")
    got = midi_readback(f"{OUT}/check/check_{name}.midi")[0]
    return sorted(got) == sorted(want) and len(got) == len(want), len(got), len(want)
def nm_(p): return f"{_NM[p % 12]}{p // 12 - 1}"
_TURNS = [x[0] for x in REC["plan"] if x[0].startswith("Turn")]
SHORT = {s_: ("Turn" if len(_TURNS) == 1 else f"Turn {i_ + 1}") for i_, s_ in enumerate(_TURNS)}; SHORT["Chorus 3"] = "Final chorus"      # a musician reads "Turn", not the record's count from the end
def staff_notes(who):
    """a vocal staff's notes: the lead and the other voices sung by who ('him', 'her', 'harmony')."""
    out = [dict(n) for n in REC["lead"] if n["singer"] == who] + [dict(n) for n in REC["harm"] if n["singer"] == who]
    out.sort(key=lambda n: n["on"])
    groups = collections.defaultdict(list)
    for n in out: groups[(n["sec"], n["line"], n["syl"], n["singer"])].append(n)
    for g in groups.values():
        g.sort(key=lambda n: n["on"])
        if len(g) > 1: g[0]["slur_open"] = True; g[-1]["slur_close"] = True
    return out
def lyr_of(ns):
    L_ = []
    for n in ns:
        if not n["first"]: continue
        w = n["text"].replace("'", "’"); q = '"' + esc(w) + '"' if re.search(r"[’?!,.;:\"—]", w) or w in ("_",) else w
        L_.append(q + (" --" if n["hyph"] else ""))
    return L_
HIM_N, HAR_N = staff_notes("him"), staff_notes("harmony")
HIM, HIM_W = pitched([dict(n, p=[n["midi"]]) for n in HIM_N]); HAR, HAR_W = pitched([dict(n, p=[n["midi"]]) for n in HAR_N])
HIM_L, HAR_L = lyr_of(HIM_N), lyr_of(HAR_N)
VMARKS = {}
HIM_B, HIM_R = body(HIM, VMARKS); HAR_B, _ = body(HAR, {})
HEAD = r'''\version "2.24.3"
#(set-global-staff-size %s)
\paper { #(set-paper-size "letter") left-margin = 15\mm right-margin = 15\mm top-margin = 12\mm bottom-margin = 14\mm ragged-last-bottom = ##t
  oddFooterMarkup = \markup \fill-line { \tiny "%s" } evenFooterMarkup = \markup \fill-line { \tiny "%s" } }
\layout { \context { \Score \override BarNumber.break-visibility = ##(#f #f #t) \compressEmptyMeasures }
  \context { \Staff \RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t \override MultiMeasureRest.minimum-length = #24 } \context { \Lyrics \override LyricText.font-size = #-0.5 } }
'''
def line_notes(sec, i): return [n for n in REC["lead"] if n["sec"] == sec and n["line"] == i]
def words_of(ns):
    out, cur = [], ""
    for n in ns:
        if not n["first"]: continue
        cur += n["text"]
        if not n["hyph"]: out.append(cur); cur = ""
    return out
def title_desc(REC_):
    """where the title falls against the chorus's first bar, read from the record"""
    b0 = next(st for s, nb, st, _, _ in REC_["plan"] if s == "Chorus 1"); ns = [n for n in REC_["lead"] if n["sec"] == "Chorus 1" and n["line"] == 0 and n["first"]]
    if ns[0]["on"] >= b0: return "on the chorus's downbeat", "Title on the downbeat."
    beat = (ns[0]["on"] % 48) // 12 + 1; land = next((n for n in ns if n["on"] >= b0), None); w = land["text"].strip(",.") if land else ""
    return (f"“{ns[0]['text']}” on beat {beat} of the bar before the chorus and “{w}” on its downbeat",
            f"The title picks up on beat {beat} of the bar before; “{w}” lands on the downbeat.")
def top_desc(REC_, nm_f):
    """where the song's top note falls, read from the record"""
    lead = REC_["lead"]; top = max(n["midi"] for n in lead); b1 = {s: st // 48 + 1 for s, nb, st, _, _ in REC_["plan"]}
    hits = [n for n in lead if n["midi"] == top and n["first"]] or [n for n in lead if n["midi"] == top]
    ch = [s for s in b1 if s.startswith(("Chorus", "Last Chorus"))]; rel = {s: sorted({n["on"] // 48 + 1 - b1[s] + 1 for n in hits if n["sec"] == s}) for s in ch}
    if all(rel[s] and rel[s] == rel[ch[0]] for s in ch) and all(n["sec"] in ch for n in hits):
        return f"The song’s top note, {nm_f(top)}, comes in bar{'s' if len(rel[ch[0]]) > 1 else ''} " + " and ".join(map(str, rel[ch[0]])) + " of each chorus."
    where = "; ".join(f"on “{n['text']}” in {n['sec'].lower() if n['sec'][-1].isdigit() else 'the ' + n['sec'].lower()} (bar {n['on'] // 48 + 1})" for n in hits[:3])
    return f"The song’s top note, {nm_f(top)}, comes {'once' if len(hits) == 1 else str(len(hits)) + ' times'}: {where}."
# ---- song 66: what the notes say, read from the record
_mm = int(REC["seconds"] // 60); _ss = int(round(REC["seconds"] % 60))
_him = [n["midi"] for n in REC["lead"]]; _top = max(_him)
B1 = {s: st // 48 + 1 for s, nb, st, mets, mv in REC["plan"]}
def line_notes(sec, i): return [n for n in REC["lead"] if n["sec"] == sec and n["line"] == i]
def bar1(t): return t // 48 + 1
HOLDS = [n for n in REC["lead"] if n["midi"] == 64 and n["dur"] >= 96]                    # the designed E4 holds (hand66.py)
STOP_BAR = REC["hand"]["stop"]["bar"]                                                      # the bridge's last bar: all stop on beats 3 and 4
_hold_txt = "; ".join(f"“{n['text']}” bar {bar1(n['on'])}, {n['dur'] // 48} bars" for n in HOLDS)
NOTE0 = f"Voice: a tenor, {nm_(min(_him))}–{nm_(max(_him))}, written on the treble 8 clef (sounding an octave lower than the treble)."
NOTE1 = (f"“They did the right thing” opens every chorus (bars {B1['Chorus 1']}, {B1['Chorus 2']}, {B1['Chorus 3']}); “And still be gone” closes it, held on E4: {_hold_txt}. "
         f"Under each hold the bass walks down by half steps from E.")
NOTE2 = f"The bridge (bar {B1['Bridge']}) is voice, guitar and bass only, the quietest part of the song. On beats 3 and 4 of bar {STOP_BAR} everything stops; the final chorus comes in together on the downbeat of bar {B1['Chorus 3']}."
NOTE3 = f"Dark indie folk-rock, ♩ = 72: strummed guitar, bass and drums; a harmony voice in the choruses. The tag is voice and guitar only, fading; the song ends on A minor."
TITLE = REC["title"]; FT = REC["file_title"]
FOOT = f"{TITLE} ({REC['edition']}) · Words and music: Jason Bryant · ♩ = 72, dark indie folk-rock · {KI.KEYSTR} · {_mm}:{_ss:02d}"
CHN = lambda rest: f'\\new ChordNames \\with {{ chordChanges = ##t }} \\chordmode {{ {chords_for(rest)} }}'
_g = REC["parts"]["guitar"]; _b = REC["parts"]["bass"]; _d = REC["parts"]["drums"]
_rng = lambda evs: f"{nm_(min(min(e['p']) for e in evs))}–{nm_(max(max(e['p']) for e in evs))}"
# guitar strums as rhythm slashes (one slash a strum) on the middle line
SLASH = [dict(on=e["on"], dur=e["dur"], p=[71], art="") for e in _g]
# drums: hands up (hi-hat, snare, toms, crash), feet down (kick); each hit lasts to the next in its voice, inside its beat
DN = {36: "bd", 38: "sn", 42: "hh", 49: "cymc", 48: "tommh", 45: "toml", 41: "tomfl"}
def drum_voice(evs):
    evs = sorted(evs, key=lambda e: e["on"]); out = []
    for i, e in enumerate(evs):
        nxt = next((x["on"] for x in evs[i + 1:] if x["on"] > e["on"]), e["on"] + 12); d = min(12, nxt - e["on"]) or 3
        if e["on"] % 12 + d > 12: d = 12 - e["on"] % 12
        out.append(dict(on=e["on"], dur=d, p=list(e["p"]), art=""))
    return out
D_UP = drum_voice([e for e in _d if e["p"][0] != 36]); D_DN = drum_voice([e for e in _d if e["p"][0] == 36])
def drum_count(bybar): return sum(len(re.findall(r"(?<![a-z])(bd|sn|hh|cymc|tommh|toml|tomfl)(?![a-z])", t)) for b in bybar for t in bybar[b])
def drums_staff(marks=None, multirest=True):
    bu, _ = pitched(D_UP, namer=lambda p: DN[p], ties=False); bdn, _ = pitched(D_DN, namer=lambda p: DN[p], ties=False)
    up, _ = body(bu, marks or {}, multirest=False); dn, _ = body(bdn, {}, multirest=False)
    strip = lambda x: re.sub(r'\\key \S+ \\minor', "", x)
    nomark = lambda x: re.sub(r'\\tempo "[^"]*" 4 = 72', "", re.sub(r'\\mark \\markup \\box \\bold "[^"]*"', "", x))
    return ('\\new DrumStaff \\with { instrumentName = "Drums" shortInstrumentName = "Dr." } \\drummode { << { \\voiceOne ' + strip(up)
            + ' } \\\\ { \\voiceTwo ' + strip(nomark(dn)) + ' } >> }'), drum_count(bu) + drum_count(bdn)
_LIFT = next((v for k, v in json.load(open('/home/claude/p76/lyric66_d.hand.song.json'))['checks'].items() if k.startswith("the chorus's median over the verse's")), None)
ROLE = {"him": "Voice: the story is told plainly in the verses, no push; the pre-choruses lean in. Each chorus ends “And still be gone” held long on E4: steady, no vibrato swell, let the band move under it. The bridge is sung quiet and close; the final chorus full.",
        "harmony": f"Harmony voice: with the lead in the choruses, in its rhythm and words, a third or so under it (range {_rng([dict(p=[n['midi']]) for n in REC['harm']])}). It drops out on the held E4s, the bridge and the tag.",
        "guitar": f"Guitar: steady eighth-note strums from the chord names, through the whole song. The bridge (bar {B1['Bridge']}) quieter; stop dead on beat 3 of bar {STOP_BAR} and come back on the downbeat of bar {B1['Chorus 3']}. Under each held E4 the chords walk down from E to E/D♯, and on after the first and last choruses. The tag is the guitar alone with the voice, fading; end on A minor, let it ring.",
        "bass": f"Bass: quarter notes on the roots, as written. Under each held E4 walk down by half steps from E (E, D♯, D, then C♯ and C after the final chorus). In the bridge play softly; stop on beat 3 of bar {STOP_BAR}; out for the tag and outro. Range {_rng(_b)}.",
        "drums": f"Drums: kick, snare and eighth-note hi-hat as written. Out for the whole bridge (bars {B1['Bridge']}–{B1['Chorus 3'] - 1}): no fill into the final chorus; come back with a crash on the downbeat of bar {B1['Chorus 3']}. Out for the tag and outro."}
VMARKS_P = {"guitar": {"Intro": "strum eighths throughout", "Bridge": "softer", "Tag": "alone with the voice, fading"}, "bass": {"Bridge": "softly", "Tag": "tacet"},
            "drums": {"Bridge": "tacet", "Chorus 3": "crash, all in", "Tag": "tacet"}, "him": {}, "harmony": {}}
if __name__ == "__main__":
    lead_ly = HEAD % (17, FOOT, FOOT) + f'''\\header {{ title = "{TITLE}" subtitle = "Lead sheet ({REC['edition']})" composer = "Words and music: Jason Bryant" tagline = ##f }}
\\score {{ <<
  {CHN(HIM_R)}
  \\new Staff \\with {{ instrumentName = "Voice" }} {{ \\clef "treble_8" \\new Voice = "him" {{ {HIM_B} }} }}
  \\new Lyrics \\lyricsto "him" {{ {" ".join(HIM_L)} }}
>> \\layout {{ }} }}
\\markup \\small \\column {{ \\vspace #1 \\wordwrap-string "{NOTE0}" \\vspace #0.3 \\wordwrap-string "{NOTE1}" \\vspace #0.3 \\wordwrap-string "{NOTE2}" \\vspace #0.3 \\wordwrap-string "{NOTE3}" }}
'''
    path, warns = compile_ly(lead_ly, f"{FT} - lead sheet", cwd=OUT)
    print("lead sheet:", [w for w in warns][:4], len(warns))
    ok = {k: readback(k, b_, w_) for k, b_, w_ in (("him", HIM, HIM_W),)}
    for k, v in ok.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    P_ = REC["parts"]
    parts_src = [("him", "Voice", [dict(n, p=[n["midi"]]) for n in HIM_N], '\\clef "treble_8"', HIM_L),
                 ("harmony", "Harmony vocal", [dict(n, p=[n["midi"]]) for n in HAR_N], '\\clef "treble_8"', HAR_L),
                 ("guitar", "Guitar", SLASH, '\\clef "treble"', None),
                 ("bass", "Bass", P_["bass"], '\\clef "bass_8"', None)]
    books = []; checks = {}
    for k, name, src, clef, lyr in parts_src:
        ev = [dict(e) for e in src]
        by, want = pitched(ev); bd, rest = body(by, VMARKS_P.get(k, {}))
        checks[k] = readback("part_" + k, by, want)
        if k == "guitar": bd = "\\improvisationOn " + bd
        vo = f'\\new Voice = "pv{k}" {{ {bd} }}' if lyr else bd
        ly = f'\\new Lyrics \\lyricsto "pv{k}" {{ {" ".join(lyr)} }}' if lyr else ""
        books.append(f'''\\bookpart {{ \\header {{ subtitle = "{name}" }}
\\markup \\small \\wordwrap {{ {esc(ROLE[k])} }}
\\score {{ << {CHN(rest)}
  \\new Staff {{ {clef} {vo} }} {ly} >> \\layout {{ }} }} }}''')
    dstaff, nh = drums_staff(VMARKS_P["drums"]); nd = len({(e["on"], p) for e in _d for p in e["p"]})      # distinct hits (the record doubles six)
    books.append(f'''\\bookpart {{ \\header {{ subtitle = "Drums" }}
\\markup \\small \\wordwrap {{ {esc(ROLE["drums"])} }}
\\score {{ << {CHN(set())} {dstaff} >> \\layout {{ }} }} }}''')
    HEAD_P = HEAD.replace(r'\RemoveEmptyStaves \override VerticalAxisGroup.remove-first = ##t ', '')
    assert HEAD_P != HEAD
    parts = HEAD_P % (16, FOOT, FOOT) + f'\\header {{ title = "{TITLE}" subtitle = "Parts ({REC['edition']})" composer = "Words and music: Jason Bryant" tagline = ##f }}\n' + "\n".join(books)
    path, warns = compile_ly(parts, f"{FT} - parts", cwd=OUT)
    print("parts:", [w for w in warns][:6], len(warns))
    for k, v in checks.items(): print(f"  readback {k}:", "matches" if v[0] else "MISMATCH", v[1:])
    print(f"  drums: {nh} hits written of {nd} in the record")
    pickle.dump(dict(voice=ok, parts=checks, drums=(nh, nd)), open(f"{OUT}/readback.pkl", "wb"))
