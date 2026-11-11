"""Nothing Else on Earth, made for real (the Evermore version): every document against song_record_d.pkl, the design gates, the
hand edits and the arrangement the writer chose (Q22-Q27)."""
import pickle, re, sys, mido
import numpy as np
sys.argv = ["x", "1", "design"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40d as P
M = P.M; H = "/home/claude/p40"; OUT = f"{H}/out_d"; BAR = 48
REC = pickle.load(open(f"{H}/song_record_d.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final_d.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb")); RF = pickle.load(open(f"{H}/riff_p40d.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location('intake40', f'{H}/intake.py'); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
lead, harm = REC["lead"], REC["harm"]; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "perc", "bass", "rgtr", "strings", "lgtr", "mando", "acou")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
D = pickle.load(open(f"{H}/melody_design.pkl", "rb")); short = [c["fp"] for c in D["alive"] if c["fp"] in set(D["short"])]
chk(f"the record is the design run's pick by ear, {REC['fp']} (shortlist rank {short.index(REC['fp']) + 1}), logged in pick_p40d.py", REC["fp"] == pick["fp"] and REC["fp"] in short)
chk(f"record's sung notes = the final melody ({len(REC['hand_edits'])} hand edits, each logged with its reason)", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]] and all(e["why"] is not None for e in REC["hand_edits"]))
chk("the edited melody passes evaluate: every gate and both design gates", P.evaluate(pick)[0] is None and not P.design_fails(pick))
chk("every writer's choice logged (Q22-Q27)", [x["q"].split(" ")[0] for x in I.LOG[-6:]] == ["22", "23", "24", "25", "26", "27"])
chk("the locked lyric, every syllable sung", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
h = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; noth = next(n for n in h if n["syl"] == 5); earth = next(n for n in h if n["syl"] == 9)
chk(f"Q23: the hook climbs to B4 on 'noth-' (its top) and lands 'earth' on A4, beat 1 of bar {earth['on'] // BAR + 1}, over A, held {earth['dur'] // 12} beats",
    noth["midi"] == 71 and max(n["midi"] for n in h) == 71 and earth["midi"] == 69 and earth["on"] % BAR == 0 and REC["bars"][earth["on"] // BAR]["chord"] == "A" and earth["dur"] >= 24)
tag = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 8]
chk(f"the tag comes home to D ({' '.join(nm(n['midi']) for n in tag)})", tag[-1]["midi"] % 12 == 2 and REC["bars"][tag[-1]["on"] // BAR]["chord"] == "D")
L_ = [n["midi"] for n in lead if n["singer"] == "Lark"]; B_ = [n["midi"] for n in lead if n["singer"] == "Briar"]
vt = max(n["midi"] for n in lead if n["sec"] in ("Verse 1", "Verse 2"))
chk(f"Q26 plan: the verses low (top {nm(vt)}, F#4 asked); Briar's chorus {nm(min(B_))}-{nm(max(B_))}, top B4", vt <= 66 and max(B_) == 71)
chk(f"Lark's harmony a third above Briar, inside her row (A3-D5): {nm(min(h_['midi'] for h_ in harm))}-{nm(max(h_['midi'] for h_ in harm))}",
    all(3 <= x["midi"] - y["midi"] <= 4 or x["midi"] == y["midi"] for x in harm for y in lead if y["on"] == x["on"]) and max(x["midi"] for x in harm) <= 74 and min(L_) >= 57)
chk("Q25: chorus 1 Briar alone; chorus 2 Briar with Lark's harmony; the last chorus both, Lark alone on line 7",
    not any(x["sec"] == "Chorus 1" for x in harm) and all(n["singer"] == "Briar" for n in lead if n["sec"] in ("Chorus 1", "Chorus 2"))
    and {x["sec"] for x in harm} == {"Chorus 2", "Last Chorus"} and all(n["singer"] == "Lark" for n in lead if n["sec"] == "Last Chorus" and n["line"] == 6)
    and not any(x["sec"] == "Last Chorus" and x["line"] == 6 for x in harm) and all(n["singer"] == "Lark" for n in lead if n["sec"] in ("Verse 1", "Verse 2", "Pre 1", "Pre 2", "Bridge")))
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]; cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1 (the hand edits applied to both)", cc1 == cc2)
l0 = [(n["on"] - P.line_start("Chorus 1", 0), n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
l4 = [(n["on"] - P.line_start("Chorus 1", 4), n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 4]
chk("the hook said twice in the chorus (pitches and onsets)", l0 == l4)
band = {b for s in ("Chorus 1", "Chorus 2", "Last Chorus", "Riff break") for b in range(P.BAR0[s], P.BAR0[s] + dict((a, n) for a, n, _, _ in REC["plan"])[s])}
folk = {b for s in ("Verse 1", "Verse 2", "Bridge") for b in range(P.BAR0[s], P.BAR0[s] + dict((a, n) for a, n, _, _ in REC["plan"])[s])}
fillbars = {b - 1 for b in band if b - 1 not in band}                                  # the bar before the storm carries its fill
kit_bars = {e["on"] // BAR for e in REC["drums"]} - fillbars
chk("Q24 B: the kit (bar a fill in the bar before), the electric guitar and the chorus bass only in the band's sections; the verses and bridge have none",
    kit_bars <= band and {e["on"] // BAR for e in REC["rgtr"]} <= band and not any(e["on"] // BAR in folk for e in REC["rgtr"]) and not any(e["on"] // BAR in (set(range(P.BAR0["Verse 1"], P.BAR0["Verse 1"] + 12)) | set(range(P.BAR0["Verse 2"], P.BAR0["Verse 2"] + 12))) for e in REC["bass"]))
chk("Q27: the mandolin riff in intro bars 1-8 (alone for four), verse bars 1-8, the break's edges, outro bars 1-3",
    sorted({e["on"] // BAR for e in REC["mando"] if e["art"].startswith("riff")}) == sorted({b for _, b in RF["bars"]}) and not any(e["on"] < 4 * BAR for k in INSTR if k != "mando" for e in REC[k]))
chk("Q27: every riff eighth has an open-string drone (D4 or A4) under it", all((62 in e["p"]) or (69 in e["p"]) for e in REC["mando"] if e["art"].startswith("riff")))
chk("235: the riff's top line unrelated to every sung line's opening (27.31)", not __import__("riff_p40").related_any([dict(on=t, p=p) for t, p in zip(RF["pick"]["ons"], __import__("riff_p40d").pitches(RF["pick"]["steps"], "D"))])[0])
chk("235/272: chorus fills only in the voice's gaps, 4-6 notes, ending on a chord tone", all(4 <= len(f["notes"]) <= 6 and f["notes"][-1]["p"] % 12 in M.CH[M.chord_at(f["notes"][-1]["on"])][1] for f in RF["fills"])
    and not any(a < e["on"] + e["dur"] and e["on"] < b for e in REC["lgtr"] if e["art"] != "solo" for a, b in [(n["on"], n["on"] + n["dur"]) for n in lead]))
chk("233: the bass has the root on beat 1 of every bar it plays", all(e["p"][0] % 12 == M.CH[REC["bars"][e["on"] // BAR]["chord"]][0] for e in REC["bass"] if e["on"] % BAR == 0))
chk("one D chord on bar 110, nothing after it", all(e["on"] <= 109 * BAR for k in INSTR for e in REC[k]) and REC["bars"][109]["chord"] == "D" and any(e["on"] == 109 * BAR for e in REC["mando"]))
mf = mido.MidiFile(f"{OUT}/Nothing Else on Earth (Evermore version) - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
lk = sorted(m.note for m in trk("Lark")[0] if m.type == "note_on" and m.velocity > 0); bk = sorted(m.note for m in trk("Briar")[0] if m.type == "note_on" and m.velocity > 0)
chk("demo: Lark's track = her melody and harmony; Briar's = his melody", lk == sorted(L_ + [x["midi"] for x in harm]) and bk == sorted(B_))
for name, key in (("Mandolin", "mando"), ("Acoustic", "acou"), ("Strings", "strings"), ("Bass", "bass"), ("Rhythm guitar", "rgtr"), ("Lead guitar", "lgtr"), ("Drums", None)):
    t_ = trk(name); want = sorted(p for e in (REC["drums"] + REC["perc"] if key is None else REC[key]) for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
chk("demo stems: the voices >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk(f"9.12 energy arc: each chorus above its verse; the last chorus the top ({ {k: round(v, 2) for k, v in E.items()} })", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Nothing Else on Earth (Evermore version) - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: melody and harmony read back from LilyPond's MIDI", RB["voice"][0] and RB["harmony"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums and percussion: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Nothing Else on Earth (Evermore version) - lead sheet.ly").read()
chk("lead sheet: credit, key, tempo, length; who sings each section", "Words and music: Jason Bryant" in src and "\\key d \\major" in src and "3:48" in src and "4 = 116" in src and "Briar" in src and "Lark" in src)
html = open(f"{OUT}/nashville.html").read(); NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords; credit, tempo, key", cells == want and "Words and music: Jason Bryant" in html and "♩ = 116" in html and "KEY: D" in html)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
