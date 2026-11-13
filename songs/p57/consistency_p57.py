"""The Singer Doesn't Stop (song 47): every document against song_record.pkl, the design gates and the writer's choices."""
import pickle, re, sys, mido, zipfile, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p57"]
import melody_v131_p57 as P
M = P.M; H = "/home/claude/p57"; OUT = f"{H}/out"; BAR = 48; T = "The Singer Doesn't Stop"
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake47", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p57 as L
D = pickle.load(open(f"{H}/run/melody_v131_p57_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/run/melody_v131_p57_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/run/melody_v131_p57_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/run/melody_v131_p57_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "bass", "guitar", "electric")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
LB = set(REC["lift"]["bars"])
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
chk(f"the record is the pick of record (the default path, 362/472), {REC['fp']}, with no hand edits", REC["fp"] == D["pick"]["fp"] == pick["fp"] and not REC["hand_edits"])
chk("record's sung notes = the melody, the second bridge's first fourteen bars a whole step up", [(n["on"], n["midi"], n["dur"]) for n in lead] == [(n["on"], n["p"] + (2 if n["on"] // BAR in LB else 0), n["dur"]) for n in pick["notes"]])
chk("the melody passes evaluate: every gate and both design gates", P.evaluate(pick)[0] is None and not P.design_fails(pick))
chk("the record's chart is the 438 chart the run drew (lifted where the record lifts)", REC["chords2_engine"] == list(D["chords2"]) == list(P.CHORD2))
chk(f"every writer's choice logged ({len(I.LOG)} entries; the lyric locked)", any(x.get("answer") == "Lock it!" for x in I.LOG) and all(x.get("answer") is not None for x in I.LOG))
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(by[(s, i)] for s in P.SUNG for i in range(len(P.LINES[s]))) and all(l in open(f"{H}/lyric_locked.md").read() for l in L.SUNG))
chk("the form (A): 88 bars, every line two bars; 527: no line flagged", REC["nbars"] == 88 and all(P.slot_len(s, i) == 2 for s in P.SUNG for i in range(len(P.LINES[s]))) and not P.FLAG527)
ps = [n["midi"] for n in lead]; top = [n for n in lead if n["midi"] == max(ps)]
chk(f"Q5 A: the tenor's row C3-A4 ({nm(min(ps))}-{nm(max(ps))}); A4 only on the second bridge's last 'do'", min(ps) >= 48 and max(ps) <= 69 and all(n["sec"] == "Bridge 2" and n["line"] == 6 for n in top))
rel = lambda s: [(n["on"] - P.BAR0[s] * BAR, n["midi"]) for n in lead if n["sec"] == s]
chk("chorus 2 = chorus 1; the last chorus's first three lines and fifth = chorus 1's; the tag's first line = the hook's", rel("Chorus 1") == rel("Chorus 2")
    and [x for x in rel("Last Chorus") if x[0] < 6 * BAR] == [x for x in rel("Chorus 1") if x[0] < 6 * BAR] and [x for x in rel("Tag") if x[0] < 2 * BAR] == [x for x in rel("Chorus 1") if x[0] < 2 * BAR])
h0, h1, h2 = by[("Chorus 1", 0)], by[("Chorus 1", 1)], by[("Chorus 1", 2)]
chk(f"the hook (A): 'The song can stop' falls {' '.join(nm(n['midi']) for n in h0[-3:])} to the tonic; a beat of silence", [n["midi"] for n in h0[-3:]] == sorted([n["midi"] for n in h0[-3:]], reverse=True)
    and h0[-1]["midi"] % 12 == 7 and h1[0]["on"] - (h0[-1]["on"] + h0[-1]["dur"]) >= 12)
chk(f"the hook (A): 'But the singer doesn't stop' the figure a step higher ({' '.join(nm(n['midi']) for n in h1[-3:])}), held into the next line", [n["midi"] for n in h1[-3:]] == [P.sstep(n["midi"], 1) for n in h0[-3:]]
    and [n["on"] - P.line_start("Chorus 1", 1) for n in h1[-3:]] == [n["on"] - P.line_start("Chorus 1", 0) for n in h0[-3:]] and h1[-1]["on"] + h1[-1]["dur"] == h2[0]["on"])
b1 = [(n["on"] - P.BAR0["Bridge"] * BAR, n["midi"]) for n in lead if n["sec"] == "Bridge" and n["line"] < 5]
b2 = [(n["on"] - P.BAR0["Bridge 2"] * BAR, n["midi"] - 2) for n in lead if n["sec"] == "Bridge 2" and n["line"] < 5]
b5, b6 = by[("Bridge 2", 5)], by[("Bridge 2", 6)]
chk(f"the bridge's build (A): the second bridge's first five lines the first's a whole step up; 'But You do / Yes You do' rising to {nm(b6[-1]['midi'])}, held", b1 == b2
    and all([n["midi"] for n in L_] == sorted(n["midi"] for n in L_) for L_ in (b5, b6)) and b6[0]["midi"] > b5[0]["midi"] and b6[-1]["midi"] == 69 and b6[-1]["dur"] >= 48)
chk(f"the song ends home: the last sung note {nm(lead[-1]['midi'])}, the tonic", lead[-1]["midi"] % 12 == 7 and lead[-1]["sec"] == "Tag")
secs_of = lambda e: REC["bars"][e["on"] // BAR]["sec"]
chk("the arrangement (A): guitar alone in the intro, verse 1, the first bridge and the tag", not any(secs_of(e) in ("Intro", "Verse 1", "Bridge", "Tag") for k in ("drums", "bass", "electric") for e in REC[k]))
chk("the arrangement (A): bass and brushes from chorus 1; the kick back at the second bridge's ninth bar; no pads", {secs_of(e) for e in REC["bass"]} == {"Chorus 1", "Verse 2", "Chorus 2", "Bridge 2", "Last Chorus"}
    and min(e["on"] for e in REC["drums"] if 36 in e["p"] and secs_of(e) == "Bridge 2") == (P.BAR0["Bridge 2"] + 8) * BAR and "pad" not in REC)
chk("the bass written by the routine (bass_v131.py) from the record", REC["bass_written_by"].startswith("bass_v131.py"))
RANGES = dict(bass=(28, 67), guitar=(40, 88), electric=(48, 84))
chk("319: every instrumental note inside its instrument's range", all(RANGES[k][0] <= p <= RANGES[k][1] for k in RANGES for e in REC[k] for p in e["p"]))
chk("one G chord on bar 88, nothing after it", all(e["on"] <= 87 * BAR for k in INSTR for e in REC[k]) and any(e["on"] == 87 * BAR for e in REC["guitar"]))
mf = mido.MidiFile(f"{OUT}/{T} - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
chk("demo: the voice track = the melody (as lifted)", sorted(m.note for m in trk("Voice")[0] if m.type == "note_on" and m.velocity > 0) == sorted(ps))
for name, key in (("Drums", "drums"), ("Bass", "bass"), ("Acoustic", "guitar"), ("Electric", "electric")):
    t_ = trk(name); want = sorted(p for e in REC[key] for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
chk(f"demo stems: the voice >= +3 dB over the band ({DR['stems_db']:+.1f})", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/{T} - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(c) < 128 for c in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: the voice reads back from LilyPond's MIDI", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/{T} - lead sheet.ly").read()
chk("lead sheet: credit, keys (G; A for the lift), tempo, length", "Words and music: Jason Bryant" in src and "\\key g \\major" in src and "\\key a \\major" in src and "4:11" in src and "4 = 84" in src)
html = open(f"{OUT}/nashville.html").read(); ROM = {"G": "I", "C": "IV", "D": "V", "Em": "vi", "Am": "ii", "Bm": "iii", "A": "I", "E": "V", "F#m": "vi", "C#m": "iii"}; NUM = {"I": "1", "IV": "4", "V": "5", "vi": "6m", "ii": "2m", "iii": "3m"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s == "Chorus 2": continue
    want += [NUM[ROM[REC["bars"][b]["chord"]]] if REC["bars"][b]["chord"] == REC["bars"][b]["chord2"] else NUM[ROM[REC["bars"][b]["chord"]]] + " " + NUM[ROM[REC["bars"][b]["chord2"]]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's half-bar chords (the lift in A); credit, tempo, key", cells == want and "Words and music: Jason Bryant" in html and "♩ = 84" in html and "KEY: G major" in html)
sb = open(f"{H}/songbook.md").read(); dx = zipfile.ZipFile(f"{OUT}/{T} - songbook.docx").read("word/document.xml").decode()
chk("songbook and its Word copy carry the producer one-sheet, on its own page", "Producer one-sheet" in sb and "Producer one-sheet" in dx and dx.count('w:type="page"') >= 2)
starts = {}
for (s, i), ns in by.items(): starts.setdefault(ns[0]["on"] // BAR + 1, []).append(dict(L.SECTIONS)[s][i][1])
rows = re.findall(r"^\| (\d+) \| (.+?) \|$", sb[sb.index("## Lyric sheet"):sb.index("## Producer one-sheet")], re.M)
chk("songbook lyric sheet: every bar number is the line's first sung bar", rows and all(t in starts.get(int(b), []) for b, t in rows))
chk(f"songbook: the voice {nm(min(ps))}-{nm(max(ps))}, read from the record", f"A tenor, {nm(min(ps))} to {nm(max(ps))}" in sb)
rng = lambda k: f"{nm(min(p for e in REC[k] for p in e['p']))}–{nm(max(p for e in REC[k] for p in e['p']))}"
chk(f"songbook session ranges = the record's (bass {rng('bass')}, electric {rng('electric')})", f"Bass {rng('bass')}" in sb and f"Electric {rng('electric')}" in sb)
banned = ["engine", "judge", "composite", "seed", "fix ", "design gate", "the search", "builds", "zeneng", "module", "window measure", "fingerprint", "524", "525", "527", "438"]
body = sb.lower()
chk("songbook: a musicians' document, no engine terms", not any(w in body for w in banned))
chk("songbook: the credit", "Words and music: Jason Bryant" in sb)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
