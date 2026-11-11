"""Blue Movie (song 43): every document against song_record.pkl, the design gate and the writer's choices (Q1-Q18)."""
import pickle, re, sys, mido, zipfile, collections
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p45", "/home/claude/p40"]
import melody_p43 as P
M = P.M; H = "/home/claude/p45"; OUT = f"{H}/out"; BAR = 48
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake43", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p43 as L
D = pickle.load(open(f"{H}/melody_p43_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/melody_p43_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/melody_p43_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/melody_p43_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "bass", "pad", "pluck")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
chk(f"the record is the pick of record (Q18 A: the judge's first), {REC['fp']}, with no hand edits", REC["fp"] == D["judge_first"]["fp"] == pick["fp"] == "dc24946f27cb" and not REC["hand_edits"])
chk("record's sung notes = the melody", [(n["on"], n["midi"], n["dur"]) for n in lead] == [(n["on"], n["p"], n["dur"]) for n in pick["notes"]])
chk("the melody passes evaluate: every gate and the design gate", P.evaluate(pick)[0] is None and not P.design_fails(pick))
chk("every writer's choice logged (Q1-Q18)", [str(x["q"]).split(" ")[0] for x in I.LOG] == [str(k) for k in range(1, 19) if k != 17] + ["17"] or
    sorted(int(str(x["q"]).split(" ")[0]) for x in I.LOG) == list(range(1, 19)))
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(by[(s, i)] for s in P.SUNG for i in range(len(P.LINES[s]))) and all(l in open(f"{H}/lyric_locked.md").read() for l in L.SUNG))
low = " ".join(L.SUNG).lower()
chk("no never-say word", not (set(re.findall(r"[a-z']+", low)) & set(I.NEVER_SAY)))
chk(f"Q9: {REC['nbars']} bars (80, 2:43); every line two bars", REC["nbars"] == 80 and all(P.slot_len(s, i) == 2 for s in P.SUNG for i in range(len(P.LINES[s]))))
ps = [n["midi"] for n in lead]; g = REC["registers"]
chk(f"Q10: the voice inside the tenor's row C3-A4 ({nm(min(ps))}-{nm(max(ps))}); the range drawn centred (unused below {g['song_lo'] - 48}, above {69 - g['song_hi']})",
    min(ps) >= 48 and max(ps) <= 69 and abs((g["song_lo"] - 48) - (69 - g["song_hi"])) <= 1)
rel = lambda s: [(n["on"] - P.BAR0[s] * BAR, n["midi"]) for n in lead if n["sec"] == s]
chk("chorus 2 = chorus 1; post-chorus 2 = post-chorus 1; the last chorus's first three lines = chorus 1's",
    rel("Chorus 1") == rel("Chorus 2") and rel("Post 1") == rel("Post 2") and [x for x in rel("Last Chorus") if x[0] < 6 * BAR] == [x for x in rel("Chorus 1") if x[0] < 6 * BAR])
fl = by[("Chorus 1", 2)]; U = P.line_start("Chorus 1", 2); l3 = by[("Chorus 1", 3)]; ch = [n for n in lead if n["sec"] == "Chorus 1"]
seq = [n["on"] - U for n in fl[:3]] == [n["on"] - U - BAR for n in fl[3:]] and all(P.sstep(a["midi"], -1) == b["midi"] for a, b in zip(fl[:3], fl[3:]))
chk(f"Q15 A: 'blue movie' one figure twice, the second a step lower ({' '.join(nm(n['midi']) for n in fl)}), from the chorus's top ({nm(max(n['midi'] for n in ch))})",
    seq and fl[0]["midi"] == max(n["midi"] for n in ch))
chk(f"Q15 A: 'starring nobody but you' lifts back to the top ({nm(max(n['midi'] for n in l3))})", max(n["midi"] for n in l3) == max(n["midi"] for n in ch))
p0, p1 = by[("Post 1", 0)], by[("Post 1", 1)]
chk("Q15 A: the post-chorus chants: one pitch each line, then the figure", [n["midi"] for n in p0[-3:]] == [n["midi"] for n in fl[:3]] and [n["midi"] for n in p1[-3:]] == [n["midi"] for n in fl[3:]]
    and len({n["midi"] for n in p0[:-3]}) == 1 and len({n["midi"] for n in p1[:-3]}) == 1)
chk(f"the song ends home: the last sung note {nm(lead[-1]['midi'])}, the tonic", (lead[-1]["midi"] - 9) % 12 == 0 and lead[-1]["sec"] == "Post 3")
FIGP = {n["midi"] + 12 for n in fl}; secs_of = lambda e: REC["bars"][e["on"] // BAR]["sec"]
chk("Q16 A: the pluck plays only the figure, an octave up, in the intro, post-choruses 1-2, the last chorus and the outro",
    all(p in FIGP for e in REC["pluck"] for p in e["p"]) and {secs_of(e) for e in REC["pluck"]} == {"Intro", "Post 1", "Post 2", "Last Chorus", "Outro"})
bridge = range(P.BAR0["Bridge"] * BAR, (P.BAR0["Bridge"] + 6) * BAR); p3 = range(P.BAR0["Post 3"] * BAR, (P.BAR0["Post 3"] + 2) * BAR)
kicks = {e["on"] for e in REC["drums"] if 36 in e["p"]}
chk("Q16 A: drums out for the bridge (bars 57-62) and the last post-chorus's first two bars; kick on every beat elsewhere from bar 5",
    not any(e["on"] in bridge or e["on"] in p3 for e in REC["drums"]) and all(t in kicks for t in range(4 * BAR, 79 * BAR, 12) if t not in bridge and t not in p3))
RANGES = dict(bass=(28, 67), pad=(36, 96), pluck=(48, 96))
chk("319: every instrumental note inside its instrument's range", all(RANGES[k][0] <= p <= RANGES[k][1] for k in RANGES for e in REC[k] for p in e["p"]))
chk("one A minor chord on bar 80, nothing after it", all(e["on"] <= 79 * BAR for k in INSTR for e in REC[k]) and REC["bars"][79]["chord"] == "Am" and any(e["on"] == 79 * BAR for e in REC["pad"]))
mf = mido.MidiFile(f"{OUT}/Blue Movie - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
chk("demo: the voice track = the melody", sorted(m.note for m in trk("Voice")[0] if m.type == "note_on" and m.velocity > 0) == sorted(ps))
for name, key in (("Drums", "drums"), ("Synth bass", "bass"), ("Pad", "pad"), ("Pluck", "pluck")):
    t_ = trk(name); want = sorted(p for e in REC[key] for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
chk(f"demo stems: the voice >= +3 dB over the band ({DR['stems_db']:+.1f})", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Blue Movie - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(c) < 128 for c in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: the voice reads back from LilyPond's MIDI", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Blue Movie - lead sheet.ly").read()
chk("lead sheet: credit, key, tempo, length", "Words and music: Jason Bryant" in src and "\\key a \\minor" in src and "2:43" in src and "4 = 118" in src)
html = open(f"{OUT}/nashville.html").read(); NUM = {"i": "1m", "VI": "♭6", "III": "♭3", "VII": "♭7", "iv": "4m", "v": "5m", "V": "5"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Chorus 2", "Post 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords; credit, tempo, key", cells == want and "Words and music: Jason Bryant" in html and "♩ = 118" in html and "KEY: A minor" in html)
sb = open(f"{H}/songbook.md").read(); dx = zipfile.ZipFile(f"{OUT}/Blue Movie - songbook.docx").read("word/document.xml").decode()
chk("songbook and its Word copy carry the producer one-sheet, on its own page", "Producer one-sheet" in sb and "Producer one-sheet" in dx and dx.count('w:type="page"') >= 2)
starts = {}
for (s, i), ns in by.items(): starts.setdefault(ns[0]["on"] // BAR + 1, []).append(L.SECTIONS[[x for x, _ in L.SECTIONS].index(s)][1][i][1])
rows = re.findall(r"^\| (\d+) \| (.+?) \|$", sb[sb.index("## Lyric sheet"):sb.index("## Producer one-sheet")], re.M)
chk("songbook lyric sheet: every bar number is the line's first sung bar", rows and all(t in starts.get(int(b), []) for b, t in rows))
chk(f"songbook: the voice D3-G4, the figure {' '.join(nm(n['midi']) for n in fl[:3])} / {' '.join(nm(n['midi']) for n in fl[3:])}, read from the record",
    nm(min(ps)) == "D3" and nm(max(ps)) == "G4" and "G4, F4, E4" in sb and "F4, E4, D4" in sb and [nm(n["midi"]) for n in fl] == ["G4", "F4", "E4", "F4", "E4", "D4"])
rng = lambda k: f"{nm(min(p for e in REC[k] for p in e['p']))}–{nm(max(p for e in REC[k] for p in e['p']))}"
chk(f"songbook session ranges = the record's (bass {rng('bass')}, pluck {rng('pluck')}, pad {rng('pad')})", f"Synth bass {rng('bass')}" in sb and f"Pluck {rng('pluck')}" in sb and f"Pad {rng('pad')}" in sb)
banned = ["engine", "judge", "composite", "seed", "fix ", "design gate", "the search", "builds", "ZenEng", "module", "window", "fingerprint"]
body = sb.lower()
chk("songbook: a musicians' document, no engine terms", not any(w.lower() in body for w in banned))
chk("Q14 A (342): the lyric's density printed at intake and logged", any(str(x["q"]).startswith("14") and x["answer"] == "A" for x in I.LOG) and I.DENSITY_342["song"] == 3.94)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
