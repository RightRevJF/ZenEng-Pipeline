"""Dry Ground (song 46): every document against song_record.pkl, the design gate and the writer's choices (Q1-Q13)."""
import pickle, re, sys, mido, zipfile, collections
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p56"]
import melody_v130_p56 as P
M = P.M; H = "/home/claude/p56"; OUT = f"{H}/out"; BAR = 48
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake46", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p56 as L
D = pickle.load(open(f"{H}/run/melody_v130_p56_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/run/melody_v130_p56_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/run/melody_v130_p56_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/run/melody_v130_p56_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "bass", "pad", "arp", "rain", "hum")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
chk(f"the record is the pick of record (the default path, 362/472), {REC['fp']}, with no hand edits", REC["fp"] == D["pick"]["fp"] == pick["fp"] and not REC["hand_edits"])
chk("record's sung notes = the melody", [(n["on"], n["midi"], n["dur"]) for n in lead] == [(n["on"], n["p"], n["dur"]) for n in pick["notes"]])
chk("the melody passes evaluate: every gate and the design gate", P.evaluate(pick)[0] is None and not P.design_fails(pick))
chk("the record's chart is the 438 chart the run drew", list(REC["chords2"]) == list(D["chords2"]) == list(P.CHORD2))
qs = [x["q"] for x in I.LOG]
chk(f"every writer's choice logged ({len(qs)} entries; the lyric locked)", len(qs) >= 18 and any(x.get("answer") == "Lock it!" for x in I.LOG) and all("answer" in x for x in I.LOG[1:]))
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(by[(s, i)] for s in P.SUNG for i in range(len(P.LINES[s]))) and all(l in open(f"{H}/lyric_locked.md").read() for l in L.SUNG))
low = " ".join(L.SUNG).lower()
chk("Q9 C: no never-say word; Noah named once", not (set(re.findall(r"[a-z']+", low)) & set(I.NEVER_SAY)) and low.count("noah") == 1)
chk("Q11 A (524): 120 bars; every line of nine syllables or more has three bars or more", REC["nbars"] == 120 and all(P.slot_len(s, i) >= 3 for s in P.SUNG for i in range(len(P.LINES[s])) if len(P.LINES[s][i]) >= 9))
ps = [n["midi"] for n in lead if not n.get("falsetto")]; g = REC["registers"]; fal = [n for n in lead if n.get("falsetto")]
chk(f"Q5 A: the voice inside the tenor's row C3-A4 ({nm(min(ps))}-{nm(max(ps))}), one falsetto B4", min(ps) >= 48 and max(ps) <= 69 and len(fal) == 1 and fal[0]["midi"] == 71)
rel = lambda s: [(n["on"] - P.BAR0[s] * BAR, n["midi"]) for n in lead if n["sec"] == s]
lc = rel("Last Chorus"); c1 = rel("Chorus 1")
chk("chorus 2 = chorus 1; the last chorus = chorus 1 but for its fourth line's words and the last 'flood'", rel("Chorus 1") == rel("Chorus 2") and lc[:-1] == c1[:-1] and lc[-1][0] == c1[-1][0])
ch1 = [n for n in lead if n["sec"] == "Chorus 1"]; wa = [n for n in by[("Chorus 1", 4)] if n["syl"] in (4, 5)]; f1 = by[("Chorus 1", 5)][-1]; f3 = by[("Last Chorus", 5)][-1]
chk(f"Q12 A: 'water' on the chorus's high note ({nm(max(n['midi'] for n in wa))} = {nm(max(n['midi'] for n in ch1))})", max(n["midi"] for n in wa) == max(n["midi"] for n in ch1))
chk(f"Q12 A: choruses 1 and 2, 'flood' falls to the tonic ({nm(f1['midi'])}) and holds ({f1['dur'] / 48:g} bars)", (f1["midi"] - 9) % 12 == 0 and f1["midi"] < max(n["midi"] for n in wa) and f1["dur"] >= 48
    and by[("Chorus 2", 5)][-1]["midi"] == f1["midi"] and by[("Chorus 2", 5)][-1]["dur"] >= 48)
chk(f"Q12 A: the last 'flood' leaps to the falsetto B4 ({nm(by[('Last Chorus', 5)][-2]['midi'])} to {nm(f3['midi'])}) and holds ({f3['dur'] / 48:g} bars)", f3["midi"] == 71 and f3["midi"] - by[("Last Chorus", 5)][-2]["midi"] >= 5 and f3["dur"] >= 48 and f3.get("falsetto"))
chk(f"the song ends home: the last sung note {nm(lead[-1]['midi'])}, the tonic", (lead[-1]["midi"] - 9) % 12 == 0 and lead[-1]["sec"] == "Outro")
kicks = {e["on"] for e in REC["drums"] if 36 in e["p"]}
br = range(P.BAR0["Bridge"] * BAR, (P.BAR0["Bridge"] + 10) * BAR); ou = range((P.BAR0["Outro"] + 4) * BAR, 120 * BAR)
chk("Q13 A: the kick on every beat from bar 5, out for the bridge but its last two bars, and out after the outro's first four",
    not any(t in kicks for t in br) and not any(t in kicks for t in ou) and all(t in kicks for t in range(4 * BAR, 108 * BAR + 4 * BAR, 12) if t not in br and t not in ou))
chk("Q13 A: rain in the intro and outro only; the hum at both ends", {REC["bars"][e["on"] // BAR]["kind"] for e in REC["rain"]} == {"Intro", "Outro"} and {REC["bars"][e["on"] // BAR]["kind"] for e in REC["hum"]} == {"Intro", "Outro"})
chk("Q13 A: the verses filtered (pad and arpeggio marked), opening at the chorus", all("filtered" in e["art"] for e in REC["pad"] if REC["bars"][e["on"] // BAR]["kind"] == "Verse")
    and not any("filtered" in e["art"] for e in REC["pad"] + REC["arp"] if REC["bars"][e["on"] // BAR]["kind"] == "Chorus"))
chk("the bass written by the routine (bass_v130.py, 538) from the record", REC["bass_written_by"].startswith("bass_v130.py"))
RANGES = dict(bass=(28, 67), pad=(36, 96), arp=(48, 96), hum=(36, 72), rain=(36, 96))
chk("319: every instrumental note inside its instrument's range", all(RANGES[k][0] <= p <= RANGES[k][1] for k in RANGES for e in REC[k] for p in e["p"]))
chk("one A minor chord on bar 120, nothing after it", all(e["on"] <= 119 * BAR for k in INSTR for e in REC[k]) and any(e["on"] == 119 * BAR for e in REC["pad"]))
mf = mido.MidiFile(f"{OUT}/Dry Ground - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
chk("demo: the voice track = the melody", sorted(m.note for m in trk("Voice")[0] if m.type == "note_on" and m.velocity > 0) == sorted(n["midi"] for n in lead))
for name, key in (("Drums", "drums"), ("Synth bass", "bass"), ("Pad", "pad"), ("Synth arpeggio", "arp"), ("Rain", "rain"), ("Hum", "hum")):
    t_ = trk(name); want = sorted(p for e in REC[key] for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
chk(f"demo stems: the voice >= +3 dB over the band ({DR['stems_db']:+.1f})", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Dry Ground - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(c) < 128 for c in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: the voice reads back from LilyPond's MIDI", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Dry Ground - lead sheet.ly").read()
chk("lead sheet: credit, key, tempo, length", "Words and music: Jason Bryant" in src and "\\key a \\minor" in src and "4:04" in src and "4 = 118" in src)
html = open(f"{OUT}/nashville.html").read(); NUM = {"Am": "1m", "F": "♭6", "C": "♭3", "G": "♭7", "Dm": "4m", "Em": "5m", "E": "5"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s == "Chorus 2": continue
    want += [NUM[REC["bars"][b]["chord"]] if REC["bars"][b]["chord"] == REC["bars"][b]["chord2"] else NUM[REC["bars"][b]["chord"]] + " " + NUM[REC["bars"][b]["chord2"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's half-bar chords; credit, tempo, key", cells == want and "Words and music: Jason Bryant" in html and "♩ = 118" in html and "KEY: A minor" in html)
sb = open(f"{H}/songbook.md").read(); dx = zipfile.ZipFile(f"{OUT}/Dry Ground - songbook.docx").read("word/document.xml").decode()
chk("songbook and its Word copy carry the producer one-sheet, on its own page", "Producer one-sheet" in sb and "Producer one-sheet" in dx and dx.count('w:type="page"') >= 2)
starts = {}
for (s, i), ns in by.items(): starts.setdefault(ns[0]["on"] // BAR + 1, []).append(dict(L.SECTIONS)[s][i][1])
rows = re.findall(r"^\| (\d+) \| (.+?) \|$", sb[sb.index("## Lyric sheet"):sb.index("## Producer one-sheet")], re.M)
chk("songbook lyric sheet: every bar number is the line's first sung bar", rows and all(t in starts.get(int(b), []) for b, t in rows))
chk(f"songbook: the voice {nm(min(ps))}-{nm(max(ps))} and the falsetto B4, read from the record", f"A tenor, {nm(min(ps))} to {nm(max(ps))}" in sb and "falsetto B4" in sb)
rng = lambda k: f"{nm(min(p for e in REC[k] for p in e['p']))}–{nm(max(p for e in REC[k] for p in e['p']))}"
chk(f"songbook session ranges = the record's (bass {rng('bass')}, arpeggio {rng('arp')}, pad {rng('pad')})", f"Bass {rng('bass')}" in sb and f"Arpeggio {rng('arp')}" in sb and f"Pad {rng('pad')}" in sb)
banned = ["engine", "judge", "composite", "seed", "fix ", "design gate", "the search", "builds", "zeneng", "module", "window measure", "fingerprint", "524", "438"]
body = sb.lower()
chk("songbook: a musicians' document, no engine terms", not any(w in body for w in banned))
chk("songbook: the credit", "Words and music: Jason Bryant" in sb)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
