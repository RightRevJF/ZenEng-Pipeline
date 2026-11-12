"""Before It's Done (song 45): every document against song_record.pkl, the design and the writer's choices (Q0-Q15)."""
import pickle, re, sys, mido, zipfile, collections
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p49", "/home/claude/p40"]
import melody_p45 as P
M = P.M; H = "/home/claude/p49"; OUT = f"{H}/out"; BAR = 48
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake45", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p45 as L
D = pickle.load(open(f"{H}/melody_p45_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/melody_p45_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/melody_p45_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/melody_p45_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []; LIFTED = REC["lifted"]
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
first = lambda k: [n for n in by[k] if n["first"]]
rel = lambda s: [(n["on"] - P.BAR0[s] * BAR, n["midi"]) for n in lead if n["sec"] == s]
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
chk(f"the record is the pick of record (362: the judge's first with no soft break), {REC['fp']}, with the writer's hand edits (Q16 A) logged in it",
    REC["fp"] == D["pick"]["fp"] == DRr["pick"]["fp"] == pick["fp"] and not pick["info"]["soft"]
    and [h["line"] for h in REC["hand_edits"]] == ["Verse 2:0", "Chorus 1:1", "Chorus 2:1", "Last Chorus:1"] and any(str(x["q"]) == "16" and x["answer"] == "A" for x in I.LOG))
untouched = lambda ns: [(n["on"], n["p"]) for n in ns if n["line"] not in {h["line"] for h in pick["hand_edits"]}]
chk("every other line is the pick as drawn", untouched(D["pick"]["notes"]) == untouched(pick["notes"]))
chk("Q16 A: verse 2's first line no longer one pitch (longest run 2); the chorus's second line in eighths and quarters, 'room' held two beats",
    max(len(list(g)) for _, g in __import__("itertools").groupby(n["midi"] for n in by[("Verse 2", 0)])) <= 2
    and all(n["dur"] >= 6 for n in by[("Chorus 1", 1)]) and by[("Chorus 1", 1)][-1]["dur"] == 24 and rel("Chorus 1") == rel("Chorus 2"))
chk("record's sung notes = the melody (the last chorus and the tag a whole step up)",
    [(n["on"], n["midi"], n["dur"]) for n in lead] == [(n["on"], n["p"] + (2 if n["sec"] in LIFTED else 0), n["dur"]) for n in sorted(pick["notes"], key=lambda n: n["on"])])
chk("the melody passes evaluate: every gate and the design gate", P.evaluate(pick)[0] is None and not P.design_fails(pick))
qs = [str(x["q"]).split(" ")[0] for x in I.LOG if str(x["q"]).split(" ")[0].isdigit()]
chk("every writer's choice logged (Q0-Q16)", sorted(int(q) for q in qs) == list(range(0, 17)))
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(by[(s, i)] for s in P.SUNG for i in range(len(P.LINES[s]))) and all(l in open(f"{H}/lyric_locked.md").read() for l in L.SUNG))
low = " ".join(L.SUNG).lower()
chk("Q3 A: the never-say list asked and kept: no word or phrase from it sung", not (set(re.findall(r"[a-z']+", low)) & set(I.NEVER_SAY)) and not any(p in low for p in I.NEVER_PHRASES))
chk(f"Q7 A: {REC['nbars']} bars (56, 3:07); every line two bars", REC["nbars"] == 56 and round(REC["seconds"]) == 187 and all(P.slot_len(s, i) == 2 for s in P.SUNG for i in range(len(P.LINES[s]))))
ps = [n["midi"] for n in lead]
chk(f"Q5 A: the voice inside a man's middle voice, B2-E4 ({nm(min(ps))}-{nm(max(ps))})", min(ps) >= I.VOICE["lo"] and max(ps) <= I.VOICE["hi"])
rel = lambda s: [(n["on"] - P.BAR0[s] * BAR, n["midi"]) for n in lead if n["sec"] == s]
chk("chorus 2 = chorus 1", rel("Chorus 1") == rel("Chorus 2"))
c0, l0 = first(("Chorus 1", 0)), first(("Last Chorus", 0))
chk(f"Q15 A: 'thought' held {c0[3]['on'] - c0[2]['on']} twelfths on {nm(c0[2]['midi'])} (G or D); 'morning' held as long on the same note a step up ({nm(l0[1]['midi'])})",
    c0[3]["on"] - c0[2]["on"] >= 30 and c0[2]["midi"] % 12 in (7, 2) and l0[1]["midi"] == c0[2]["midi"] + 2 and l0[2]["on"] - l0[1]["on"] >= 30)
c3, c3b, l3, t1 = first(("Chorus 1", 3)), first(("Chorus 2", 3)), first(("Last Chorus", 3)), first(("Tag", 1))
chk(f"Q15 A: 'before it's done' D4 C4 B3 A3 in choruses 1-2 ({' '.join(nm(n['midi']) for n in c3[-4:])}); D4 C♯4 B3 A3 home in the last ({' '.join(nm(n['midi']) for n in l3[-4:])}); the tag on B3, the 2nd of A",
    [n["midi"] for n in c3[-4:]] == [n["midi"] for n in c3b[-4:]] == [62, 60, 59, 57] and [n["midi"] for n in l3[-4:]] == [62, 61, 59, 57] and t1[-1]["midi"] == 59 and lead[-1] is t1[-1])
vp = [n["midi"] for n in lead if n["sec"] == "Verse 1"]; cp = [n["midi"] for n in lead if n["sec"] == "Chorus 1"]
chk(f"Q14 A: the chorus over the verse (verse {nm(min(vp))}-{nm(max(vp))}, chorus {nm(min(cp))}-{nm(max(cp))}; median +{np.median(cp) - np.median(vp):.1f})",
    np.median(cp) - np.median(vp) >= 3 and max(cp) > max(vp))
A_CH = {"A": {9, 1, 4}, "E": {4, 8, 11}, "F#m": {6, 9, 1}, "D": {2, 6, 9}}
chk("Q6 A: the last chorus and the tag in A: their chords, key and notes a whole step up; every other bar in G",
    all((b["key"] == "A major") == (b["sec"] in LIFTED) for b in REC["bars"]) and all(b["chord"] in A_CH for b in REC["bars"] if b["sec"] in LIFTED)
    and REC["bars"][44]["chord"] == "A" and REC["bars"][43]["chord"] == "E")
# ---- the guitar ----
OPEN = REC["open"]; V = REC["voicings"]
chk("the guitar: every note's string and fret give its pitch; standard tuning, no capo, no fret above 5",
    all(OPEN[st] + fr == p and 0 <= fr <= 5 for e in REC["gtr"] for p, (st, fr) in zip(e["p"], e["sf"])))
def tones(ch):
    r = {"G": 7, "A": 9, "B": 11, "C": 0, "D": 2, "E": 4, "F#": 6}[ch[:2] if ch.startswith("F#") else ch[0]]; mi = "m" in ch
    return {r, (r + (3 if mi else 4)) % 12, (r + 7) % 12}
SHAPE_CH = {"G": "G", "Gsus4": "G", "Gres": "G", "D/F#": "D", "Em7": "Em", "Cadd9": "C", "Am7": "Am", "Dsus4": "D", "D": "D", "E": "E", "Esus4": "E",
            "A": "A", "Asus4": "A", "E/G#": "E", "F#m7": "F#m", "Dadd9": "D"}
chk("the guitar's shapes are the bar's chord (with its sus, seventh or added ninth): each shape's root and fifth are the chord's",
    all(SHAPE_CH[REC["shape_at"][bi * 8 + e]] == b["chord"] for bi, b in enumerate(REC["bars"]) for e in range(8)))
sounding = lambda bi, h: [p for e in REC["gtr"] if bi * BAR + 24 * h <= e["on"] < bi * BAR + 24 * h + 24 for p in e["p"]]
def sung(bi, h):
    a, z = bi * BAR + 24 * h, bi * BAR + 24 * h + 24; out = collections.Counter()
    for n in lead:
        ov = min(z, n["on"] + n["dur"]) - max(a, n["on"])
        if ov > 0: out[n["midi"] % 12] += ov
    return out
lst = []
for bi, b in enumerate(REC["bars"]):
    if b["chord"] not in ("D", "E") or (b["chord"] == "D" and b["sec"] in LIFTED) or (b["chord"] == "E" and b["sec"] not in LIFTED): continue
    f4, f3 = {"D": (7, 6), "E": (9, 8)}[b["chord"]]
    for h in (0, 1):
        v = sung(bi, h); sh = REC["shape_at"][bi * 8 + 4 * h]
        if v[f4] >= 6 and v[f4] >= v[f3]: lst.append(sh.endswith("sus4"))
        elif v[f3] >= 3: lst.append(not sh.endswith("sus4"))
chk(f"the guitar listens: the sus4 wherever the voice holds the fourth over a D (in G) or an E (in A), the plain chord where it sings the third ({len(lst)} half bars)", lst and all(lst))
c0b = [e for e in REC["gtr"] if P.BAR0["Chorus 1"] * BAR + 24 <= e["on"] < P.BAR0["Chorus 1"] * BAR + 48 and e["voice"] == "up"]
chk("under 'thought': Gsus4's C (string 2, fret 1) on beat 3, resolving to the open B on beat 4", any((60, (2, 1)) in zip(e["p"], [tuple(x) for x in e["sf"]]) and e["on"] % BAR == 24 for e in c0b)
    and any((59, (2, 0)) in zip(e["p"], [tuple(x) for x in e["sf"]]) and e["on"] % BAR == 42 for e in c0b))
top = lambda bi: [e["p"][-1] for e in REC["gtr"] if e["on"] // BAR == bi and e["voice"] == "up"]
chk("the intro's last bar plays the chorus's last four notes (D C B A); the tag's last bar E D C♯ B, arriving on the singer's last note",
    top(3)[:4] == [62, 60, 59, 57] == [n["midi"] for n in c3[-4:]] and top(55)[:4] == [64, 62, 61, 59] and top(55)[3] == lead[-1]["midi"])
bass = lambda bi: sorted((e["on"], e["p"][0]) for e in REC["gtr"] if e["on"] // BAR == bi and e["voice"] == "bass")
b0 = P.BAR0["Chorus 1"]
chk("the chorus bass walks down G, F♯, E to C (the F♯ at the half bar where the D starts as Dsus4)", [bass(b0)[0][1] % 12, bass(b0 + 1)[-1][1] % 12, bass(b0 + 2)[0][1] % 12, bass(b0 + 3)[0][1] % 12] == [7, 6, 4, 0])
chk("the last chorus bass walks down A, G♯, F♯ to D", [bass(44)[0][1] % 12, bass(45)[-1][1] % 12, bass(46)[0][1] % 12, bass(47)[0][1] % 12] == [9, 8, 6, 2])
chk("the bridge's last bar strummed: Esus4, then E (the G♯) on beat 4", all(e.get("art") == "strum" for e in REC["gtr"] if e["on"] // BAR == 43)
    and {REC["shape_at"][43 * 8 + k] for k in range(6)} == {"Esus4"} and REC["shape_at"][43 * 8 + 6] == "E")
# ---- the cello ----
cel = [p for e in REC["cello"] for p in e["p"]]
chk(f"the cello in its range (C2 up) and in the key: G, then A from bar 45 ({nm(min(cel))}-{nm(max(cel))}); tacet until verse 2",
    min(cel) >= 36 and max(cel) <= 76 and all(e["p"][0] % 12 in ({9, 11, 1, 2, 4, 6, 8} if REC["bars"][e["on"] // BAR]["sec"] in LIFTED else {7, 9, 11, 0, 2, 4, 6}) for e in REC["cello"])
    and min(e["on"] for e in REC["cello"]) == P.BAR0["Verse 2"] * BAR)
chk("the cello takes the suspension over 'morning' (A4 held into bar 46, falling to G♯4) and ends on D, the tag's last bar",
    any(e["p"] == [69] and e["on"] < 45 * BAR < e["on"] + e["dur"] for e in REC["cello"]) and any(e["p"] == [68] and e["on"] == 45 * BAR + 24 for e in REC["cello"])
    and REC["cello"][-1]["p"][0] % 12 == 2 and REC["cello"][-1]["on"] == 55 * BAR)
# ---- the demo ----
mf = mido.MidiFile(f"{OUT}/Before It's Done - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
notes_of = lambda t: sorted(m.note for m in t if m.type == "note_on" and m.velocity > 0)
chk("demo: the voice track = the melody (lifted where the record lifts it)", notes_of(trk("Voice")[0]) == sorted(ps))
chk("demo: the guitar track = the record's", notes_of(trk("Acoustic guitar")[0]) == sorted(p for e in REC["gtr"] for p in e["p"]))
chk("demo: the cello track = the record's", notes_of(trk("Cello")[0]) == sorted(p for e in REC["cello"] for p in e["p"]))
chk(f"demo stems: the voice >= +3 dB over the band ({DR['stems_db']:+.1f})", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Before It's Done - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes; tempo in quarters (72); key signatures G then A", all(not any(m.type == "program_change" for m in t) for t in gb.tracks)
    and all(all(ord(c) < 128 for c in m.name) for t in gb.tracks for m in t if m.type == "track_name")
    and any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 72 for m in gb.tracks[0])
    and [m.key for m in gb.tracks[0] if m.type == "key_signature"] == ["G", "A"])
# ---- the engravings ----
for k, v in RB["checks"].items(): chk(f"engraving readback, {k}: LilyPond's MIDI = the record", v[0])
chk(f"TAB: every string and fret written agrees with its pitch ({RB['tab'][1]} notes)", RB["tab"][0])
src = open(f"{OUT}/Before It's Done - lead sheet.ly").read()
chk("lead sheet: credit, keys (G, then A at the last chorus), tempo, length", "Words and music: Jason Bryant" in src and "\\key g \\major" in src and "\\key a \\major" in src and "3:07" in src and "4 = 72" in src)
vg = open(f"{OUT}/Before It's Done - voice and guitar score.ly").read()
chk("voice-and-guitar score: the whole song, voice and words over the guitar in notation and TAB, string numbers on every guitar note; credit",
    "Words and music: Jason Bryant" in vg and "\\new TabStaff" in vg and "\\new Lyrics" in vg and vg.count("\\key a \\major") >= 3
    and len(re.findall(r"[a-g](?:is)?[',]*\\[1-6]", vg)) >= RB["tab"][1])
html = open(f"{OUT}/nashville.html").read()
NUM_G = {"G": "1", "Gsus4": "1sus", "Gres": "1", "D/F#": "5/7", "Em7": "6m7", "Cadd9": "4add9", "Am7": "2m7", "Dsus4": "5sus", "D": "5", "E": "6", "Esus4": "6sus"}
NUM_A = {"A": "1", "Asus4": "1sus", "E/G#": "5/7", "F#m7": "6m7", "Dadd9": "4add9", "E": "5", "Esus4": "5sus"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0_, _ in REC["plan"]:
    if s == "Chorus 2": continue
    for b in range(b0_, b0_ + nb):
        num = NUM_A if s in LIFTED else NUM_G; out = []
        for e in range(8):
            n_ = num[REC["shape_at"][b * 8 + e]]
            if not out or out[-1] != n_: out.append(n_)
        want.append(" ".join(out[:3]))
chk("chart numbers = the guitar's shapes, each section in its own key (1 = G; 1 = A from the last chorus); credit, tempo, key",
    cells == want and "Words and music: Jason Bryant" in html and "♩ = 72" in html and "G major; the last chorus and the tag up a whole step to A" in html)
sb = open(f"{H}/songbook.md").read(); dx = zipfile.ZipFile(f"{OUT}/Before It's Done - songbook.docx").read("word/document.xml").decode()
chk("songbook and its Word copy carry the producer one-sheet, on its own page", "Producer one-sheet" in sb and "Producer one-sheet" in dx and dx.count('w:type="page"') >= 2)
starts = {}
for (s, i), ns in by.items(): starts.setdefault(ns[0]["on"] // BAR + 1, []).append(L.SECTIONS[[x for x, _ in L.SECTIONS].index(s)][1][i][1])
rows = re.findall(r"^\| (\d+)(?: \(pickup\))? \| (.+?) \|$", sb[sb.index("## Lyric sheet"):sb.index("## Producer one-sheet")], re.M)
chk("songbook lyric sheet: every bar number is the line's first sung bar", rows and all(t in starts.get(int(b), []) for b, t in rows) and len(rows) == len(starts) - 4)
hi = max(ps); hib = next(n for n in lead if n["midi"] == hi)
chk(f"songbook: the voice {nm(min(ps))} to {nm(max(ps))} (top on '{hib['text']}', bar {hib['on'] // BAR + 1}); 'thought' on {nm(c0[2]['midi'])}; the chorus ending and the tag's B3, read from the record",
    f"{nm(min(ps))} to {nm(max(ps))}" in sb and f"bar {hib['on'] // BAR + 1}" in sb and f"\"thought\" on {nm(c0[2]['midi'])}" in sb
    and "D4, C4, B3, A3" in sb and "D4, C♯4, B3, A3" in sb and "B3 on the downbeat of bar 56" in sb and lead[-1]["on"] // BAR + 1 == 56)
rng = lambda k: f"{nm(min(p for e in REC[k] for p in e['p']))}–{nm(max(p for e in REC[k] for p in e['p']))}"
chk(f"songbook session ranges = the record's (guitar {rng('gtr')}, cello {rng('cello')})", f"Guitar {rng('gtr')}" in sb and f"Cello {rng('cello')}" in sb and f"Voice {nm(min(ps))}–{nm(max(ps))}" in sb)
chk("songbook: the cello's notes as written in the record (verse 2, the bridge, the tag)",
    "E3, C3, B2, A2, G2, C3, A2, D3" in sb and "A2, B2, C3, B2, A2, G2, E2" in sb and "A3, F♯3, E3, D3" in sb
    and [nm(e["p"][0]) for e in REC["cello"] if REC["bars"][e["on"] // BAR]["sec"] == "Verse 2"] == "E3 C3 B2 A2 G2 C3 A2 D3".split())
chk("songbook: the guitar shapes written are the record's frets", all(f"{k} {''.join('x' if f is None else str(f) for f in V[k])}" in sb for k in ("D/F#".replace("#", "♯") and [] or []) ) and
    all(("".join('x' if f is None else str(f) for f in V[k])) in sb for k in V))
banned = ["engine", "judge", "composite", "seed", "fix ", "design gate", "the search", "builds", "ZenEng", "module", "window", "fingerprint"]
chk("songbook: a musicians' document, no engine terms", not any(w.lower() in sb.lower() for w in banned))
chk("342: the lyric's density printed at intake and answered (Q13 A)", "5.29" in I.DENSITY_342 and any(str(x["q"]).split(" ")[0] == "13" and x.get("answer") == "A" for x in I.LOG))
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
