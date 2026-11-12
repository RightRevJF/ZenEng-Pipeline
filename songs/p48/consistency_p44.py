"""Keeping Time (song 44): every document against song_record.pkl, the design and the writer's choices (Q1-Q17)."""
import pickle, re, sys, mido, zipfile, collections
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p48", "/home/claude/p40"]
import melody_p44 as P
M = P.M; H = "/home/claude/p48"; OUT = f"{H}/out"; BAR = 48
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake44", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p44 as L
D = pickle.load(open(f"{H}/melody_p44_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/melody_p44_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/melody_p44_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/melody_p44_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []
NMS = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "bass", "pad", "pulse")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
chk(f"the record is the pick of record (362: the judge's first with no soft break), {REC['fp']}, with no hand edits",
    REC["fp"] == D["pick"]["fp"] == pick["fp"] == "e8dc84c25324" and not REC["hand_edits"] and not pick["info"]["soft"])
chk("record's sung notes = the melody", [(n["on"], n["midi"], n["dur"]) for n in lead] == [(n["on"], n["p"], n["dur"]) for n in pick["notes"]])
chk("the melody passes evaluate: every gate and the design gate", P.evaluate(pick)[0] is None and not P.design_fails(pick))
qs = [str(x["q"]).split(" ")[0] for x in I.LOG if str(x["q"]).split(" ")[0].isdigit()]
chk("every writer's choice logged (Q0-Q17)", sorted(int(q) for q in qs) == list(range(0, 18)))
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(by[(s, i)] for s in P.SUNG for i in range(len(P.LINES[s]))) and all(l in open(f"{H}/lyric_locked.md").read() for l in L.SUNG))
low = " ".join(L.SUNG).lower()
chk("Q2 B: no never-say word or phrase; one faint echo ('hear')", not (set(re.findall(r"[a-z']+", low)) & set(I.NEVER_SAY)) and not any(p in low for p in I.NEVER_PHRASES)
    and sum(low.count(w) for w in (" hear", "heard", "touched")) == 1)
chk(f"Q7 A: {REC['nbars']} bars (80, 2:51); every line two bars", REC["nbars"] == 80 and round(REC["seconds"]) == 171 and all(P.slot_len(s, i) == 2 for s in P.SUNG for i in range(len(P.LINES[s]))))
ps = [n["midi"] for n in lead]
chk(f"Q6 A: the voice inside the mezzo's row G3-D5 ({nm(min(ps))}-{nm(max(ps))})", min(ps) >= 55 and max(ps) <= 74)
rel = lambda s: [(n["on"] - P.BAR0[s] * BAR, n["midi"]) for n in lead if n["sec"] == s]
chk("chorus 2 = chorus 1; post-chorus 2 = post-chorus 1; the last chorus = chorus 1 but its third line",
    rel("Chorus 1") == rel("Chorus 2") and rel("Post 1") == rel("Post 2") and [x for x in rel("Last Chorus") if not 4 * BAR <= x[0] < 6 * BAR - 24] == [x for x in rel("Chorus 1") if not 4 * BAR <= x[0] < 6 * BAR - 24])
rk, lc, cl = by[("Chorus 1", 2)], by[("Last Chorus", 2)], by[("Chorus 1", 3)]
rocks = lambda ns: len({n["midi"] for n in ns}) == 2 and all(a["midi"] != b["midi"] for a, b in zip(ns, ns[1:]))
chk(f"Q16 A: 'Two clocks on the same wall' rocks on two notes a step apart ({' '.join(nm(n['midi']) for n in rk)}); 'It was always the same wall' on the same two",
    rocks(rk) and rocks(lc) and {n["midi"] for n in rk} == {n["midi"] for n in lc} == set(REC["design"]["clocks"]) and P.sstep(max(n["midi"] for n in rk), -1) == min(n["midi"] for n in rk))
a3, b3 = cl[2:5], cl[5:8]
chk(f"Q16 A: 'keeping time' twice, the second a step higher ({' '.join(nm(n['midi']) for n in a3)} / {' '.join(nm(n['midi']) for n in b3)})",
    [n["on"] + BAR for n in a3] == [n["on"] for n in b3] and all(P.sstep(m["midi"], 1) == n["midi"] for m, n in zip(a3, b3)))
p0, p1, p3 = by[("Post 1", 0)], by[("Post 1", 1)], by[("Post 3", 1)]
chk("Q16 A: every post-chorus phrase lands on a downbeat; the two 'one's on the clocks' notes",
    all(n["on"] % BAR == 0 for n in (p0[3], p0[7], p1[-1], p3[-1])) and {p0[3]["midi"], p0[7]["midi"]} == set(REC["design"]["clocks"]))
vp = [n["midi"] for n in lead if n["sec"] == "Verse 1"]; cp = [n["midi"] for n in lead if n["sec"] == "Chorus 1"]
chk(f"Q17 C: a narrow verse ({nm(min(vp))}-{nm(max(vp))}), the chorus over it and wider ({nm(min(cp))}-{nm(max(cp))}; median +{np.median(cp) - np.median(vp):.1f})",
    max(vp) - min(vp) <= 7 and np.median(cp) - np.median(vp) >= 3 and max(cp) - min(cp) > max(vp) - min(vp))
chk(f"Q9 A: the verse closes on C ({nm(by[('Verse 1', 3)][-1]['midi'])}); the song ends on E-flat ({nm(lead[-1]['midi'])})", by[("Verse 1", 3)][-1]["midi"] % 12 == 0 and lead[-1]["midi"] % 12 == 3 and lead[-1]["sec"] == "Post 3")
CB = set(REC["design"]["clock_bars"])
chk("Q16 A: in each chorus's fifth bar only the pulse plays, ticking the clocks' two notes an octave up",
    all(not any(e["on"] // BAR in CB for e in REC[k]) for k in ("drums", "bass", "pad")) and {p for e in REC["pulse"] if e["on"] // BAR in CB for p in e["p"]} == {p + 12 for p in REC["design"]["clocks"]}
    and len(CB) == 3)
drift = lambda s: [e["on"] % BAR for e in REC["pulse"] if REC["bars"][e["on"] // BAR]["sec"] == s and e.get("art") == "drift"]
lock = lambda s: [e["on"] % BAR for e in REC["pulse"] if REC["bars"][e["on"] // BAR]["sec"] == s and e.get("art") == "lock"]
chk("Q5 A: the pulse drifts in dotted eighths in the intro and the verses, and locks to eighths in the choruses and post-choruses",
    all(t % 9 == 0 for s in ("Intro", "Verse 1", "Verse 2", "Outro") for t in drift(s)) and drift("Verse 1") and not lock("Verse 1")
    and all(t % 6 == 0 for s in ("Chorus 1", "Post 1", "Last Chorus") for t in lock(s)) and lock("Chorus 1") and not drift("Chorus 1"))
bridge = range(P.BAR0["Bridge"] * BAR, (P.BAR0["Bridge"] + 6) * BAR); kicks = {e["on"] for e in REC["drums"] if 36 in e["p"]}
chk("the writer's note to draft 3: no kick for the bridge's first six bars; the kick back for its last two",
    not any(t in bridge for t in kicks) and all(t in kicks for t in range((P.BAR0["Bridge"] + 6) * BAR, (P.BAR0["Bridge"] + 8) * BAR, 12)))
RANGES = dict(bass=(28, 67), pad=(36, 96), pulse=(48, 96))
chk("319: every instrumental note inside its instrument's range", all(RANGES[k][0] <= p <= RANGES[k][1] for k in RANGES for e in REC[k] for p in e["p"]))
chk("one E-flat chord on bar 80, nothing after it", all(e["on"] <= 79 * BAR for k in INSTR for e in REC[k]) and REC["bars"][79]["chord"] == "Eb" and any(e["on"] == 79 * BAR for e in REC["pad"]))
mf = mido.MidiFile(f"{OUT}/Keeping Time - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
chk("demo: the voice track = the melody", sorted(m.note for m in trk("Voice")[0] if m.type == "note_on" and m.velocity > 0) == sorted(ps))
for name, key in (("Drums", "drums"), ("Synth bass", "bass"), ("Pad", "pad"), ("Pulse", "pulse")):
    t_ = trk(name); want = sorted(p for e in REC[key] for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
chk(f"demo stems: the voice >= +3 dB over the band ({DR['stems_db']:+.1f})", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Keeping Time - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes; tempo in quarters (112)", all(not any(m.type == "program_change" for m in t) for t in gb.tracks)
    and all(all(ord(c) < 128 for c in m.name) for t in gb.tracks for m in t if m.type == "track_name")
    and any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 112 for m in gb.tracks[0]))
chk("lead sheet: the voice reads back from LilyPond's MIDI", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Keeping Time - lead sheet.ly").read()
chk("lead sheet: credit, key, tempo, length", "Words and music: Jason Bryant" in src and "\\key ees \\major" in src and "2:51" in src and "4 = 112" in src)
html = open(f"{OUT}/nashville.html").read()
NCM = {"Cm": "1m", "Fm": "4m", "Gm": "5m", "G": "5", "Ab": "♭6", "Eb": "♭3", "Bb": "♭7"}; NEB = {"Eb": "1", "Fm": "2m", "Gm": "3m", "Ab": "4", "Bb": "5", "Cm": "6m", "G": "3"}
MINOR = ("Intro", "Verse 1", "Pre 1", "Verse 2", "Pre 2", "Outro")
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Chorus 2", "Post 2"): continue
    want += [(NCM if s in MINOR else NEB)[REC["bars"][b]["chord"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords, each section in its own key; credit, tempo, key", cells == want and "Words and music: Jason Bryant" in html and "♩ = 112" in html and "C minor (verses) / E♭ major (chorus)" in html)
sb = open(f"{H}/songbook.md").read(); dx = zipfile.ZipFile(f"{OUT}/Keeping Time - songbook.docx").read("word/document.xml").decode()
chk("songbook and its Word copy carry the producer one-sheet, on its own page", "Producer one-sheet" in sb and "Producer one-sheet" in dx and dx.count('w:type="page"') >= 2)
starts = {}
for (s, i), ns in by.items(): starts.setdefault(ns[0]["on"] // BAR + 1, []).append(L.SECTIONS[[x for x, _ in L.SECTIONS].index(s)][1][i][1])
rows = re.findall(r"^\| (\d+)(?: \(pickup\))? \| (.+?) \|$", sb[sb.index("## Lyric sheet"):sb.index("## Producer one-sheet")], re.M)
chk("songbook lyric sheet: every bar number is the line's first sung bar", rows and all(t in starts.get(int(b), []) for b, t in rows))
chk(f"songbook: the voice {nm(min(ps))}-{nm(max(ps))}, the clocks {' and '.join(nm(p) for p in sorted(REC['design']['clocks'], reverse=True))}, the figure {' '.join(nm(n['midi']) for n in a3)} / {' '.join(nm(n['midi']) for n in b3)}, read from the record",
    f"{nm(min(ps))} to {nm(max(ps))}" in sb and "between G4 and F4" in sb and f"{' '.join(nm(n['midi']) for n in a3)}" in sb and f"{' '.join(nm(n['midi']) for n in b3)}" in sb
    and f"E♭4 on the downbeat of bar 76" in sb and nm(lead[-1]["midi"]) == "E♭4" and lead[-1]["on"] // BAR + 1 == 76)
rng = lambda k: f"{nm(min(p for e in REC[k] for p in e['p']))}–{nm(max(p for e in REC[k] for p in e['p']))}"
chk(f"songbook session ranges = the record's (bass {rng('bass')}, pulse {rng('pulse')}, pad {rng('pad')})", f"Synth bass {rng('bass')}" in sb and f"Pulse {rng('pulse')}" in sb and f"Pad {rng('pad')}" in sb)
banned = ["engine", "judge", "composite", "seed", "fix ", "design gate", "the search", "builds", "ZenEng", "module", "window", "fingerprint"]
chk("songbook: a musicians' document, no engine terms", not any(w.lower() in sb.lower() for w in banned))
chk("342: the lyric's density inside the kept range, printed at intake (no question needed)", "3.93" in I.DENSITY_342)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
