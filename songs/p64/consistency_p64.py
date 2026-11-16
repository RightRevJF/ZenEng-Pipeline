"""The Man Mama Prayed I'd Be (song 54): every document against the record, the designs, the research checks and the files."""
import pickle, re, subprocess, collections, os, json
H = "/home/claude/p64"
R = pickle.load(open(f"{H}/song_record.pkl", "rb")); RB = pickle.load(open(f"{H}/out/readback.pkl", "rb")); RS = pickle.load(open(f"{H}/out/readback_score.pkl", "rb"))
DM = pickle.load(open(f"{H}/out/demo_report.pkl", "rb")); RX = json.load(open(f"{H}/research_p64.json"))
SB = open(f"{H}/songbook.md").read(); NV = open(f"{H}/out/nashville.html").read()
FT = R["file_title"]
def pdf(n): return subprocess.run(["pdftotext", f"{H}/out/{FT} - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts").replace("’", "'"), pdf("full score")
DOCX = subprocess.run(["pandoc", f"{H}/out/{FT} - songbook.docx", "-t", "plain"], capture_output=True, text=True).stdout
DOCXML = subprocess.run(["unzip", "-p", f"{H}/out/{FT} - songbook.docx", "word/document.xml"], capture_output=True, text=True).stdout
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p64.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; P_ = R["parts"]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
B0 = {}
for i, b in enumerate(R["bars"]): B0.setdefault(b["sec"], i)
H2 = R["chords2"]
def chord_on(n): return H2[n["on"] // 24]
for nm_, txt in (("songbook", SB), ("songbook (Word)", DOCX), ("lead sheet", LY), ("parts", PT), ("full score", SC), ("chart", NV)): chk(f"credit line on the {nm_}", "Words and music: Jason Bryant" in txt)
for k, v in RB["voice"].items(): chk(f"readback: {k} (lead sheet)", v[0])
for k, v in RS["voice"].items(): chk(f"readback: {k} (full score)", v[0])
for k, v in RB["parts"].items(): chk(f"readback: {k} (parts)", v[0])
for k, v in RS["parts"].items(): chk(f"readback: {k} (full score)", v[0])
chk("drums: every hit written (parts)", RB["drums"][0] == RB["drums"][1]); chk("drums: every hit written (score)", RS["drums"][0] == RS["drums"][1])
chk("parts: every instrument's notes written (the writer, 16 Nov)", all(k in RB["parts"] for k in ("acoustic", "tele", "fiddle", "steel", "piano", "bass")))
chk("parts: each part's role note", all(t in PT for t in ("the floor of the song", "short answers in the gaps", "plays the hook in the intro", "swells under the chords", "offbeat chords", "a two-step. On 1 and 3", "a two-step with sticks")))
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", all(E[f"Chorus {k}"] > E[f"Verse {k}"] for k in (1, 2, 3, 4)))
chk("9.12 / 749.17: each return above the one before", E["Chorus 1"] < E["Chorus 2"] < E["Chorus 3"] < E["Chorus 4"])
chk("9.12: the top at chorus 4 (her)", max(E, key=E.get) == "Chorus 4")
HOOK = [55, 59, 62, 59, 57, 54, 50]
chk("hook: G3 B3 D4 B3 A3 F#3 D3 in choruses 1-3", all([n["midi"] for n in by[(s, 5)]] == HOOK for s in ("Chorus 1", "Chorus 2", "Chorus 3")))
chk("hook: 'Ma-' on D4 over G; 'be' on D3 over D (open)", all(chord_on(by[(s, 5)][2]) == "G" and chord_on(by[(s, 5)][-1]) == "D" for s in ("Chorus 1", "Chorus 2", "Chorus 3")))
chk("hook: D4 his top, sung only on the title line", max(n["midi"] for n in lead if n["singer"] == "him") == 62 and all(by_r == 5 or s_ == "Tag" for s_, by_r in {(n["sec"], n["line"]) for n in lead if n["singer"] == "him" and n["midi"] == 62}))
c4 = by[("Chorus 4", 5)]
chk("chorus 4 (her): the same climb an octave up, F#4 up to G4 over G, home", [n["midi"] for n in c4] == [67, 71, 69, 74, 71, 69, 66, 67] and chord_on(c4[-1]) == "G" and chord_on(c4[-2]) == "D")
chk("chorus 4: every line hers, an octave above the engine's line", all(n["singer"] == "her" and n["midi"] == n["engine_midi"] + 12 for j in range(6) for n in by[("Chorus 4", j)]))
chk("tag: his line home on G3 over G, hers on G4 over G", by[("Tag", 0)][-1]["midi"] == 55 and by[("Tag", 1)][-1]["midi"] == 67 and chord_on(by[("Tag", 0)][-1]) == "G" and chord_on(by[("Tag", 1)][-1]) == "G")
chk("tag: her harmony over his line; him an octave under hers", any(n["singer"] == "her" and n["sec"] == "Tag" and n["line"] == 0 for n in R["harm"]) and all(n["midi"] == m["midi"] - 12 for n, m in zip([x for x in R["harm"] if x["sec"] == "Tag" and x["line"] == 1], by[("Tag", 1)])))
chk("chorus 4: him under her on the title line", sum(1 for n in R["harm"] if n["sec"] == "Chorus 4" and n["singer"] == "him") == len(c4))
st = R["breath"]["at"]
chk("the breath (749.19): nothing sounds from beat 3 of verse 4's last bar to her entry", not any(st <= e["on"] < st + 24 for evs in P_.values() for e in evs) and not any(n["on"] < st + 24 and n["on"] + n["dur"] > st for n in lead) and not any(e["on"] < st < e["on"] + e["dur"] - 1 for k in ("acoustic", "bass", "tele", "fiddle", "piano") for e in P_.get(k, [])))
chk("the breath: her first note after the stop", by[("Chorus 4", 0)][0]["on"] >= st + 24)
vm = sorted(n["midi"] for j in range(8) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in range(5) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("verses within B2-B3 (the key, A)", all(47 <= n["midi"] <= 59 for s in ("Verse 1", "Verse 2", "Verse 3", "Verse 4") for j in range(8) for n in by[(s, j)]))
chk("every sung line two bars", all(v == [2] * len(v) for v in R["design"]["slots"].values()))
chk("no two syllables on one onset, no note of no length (749.1)", len({n["on"] for n in lead}) == len(lead) and all(n["dur"] > 0 for n in lead))
chk("the voice in the key (G major)", all(n["midi"] % 12 in {7, 9, 11, 0, 2, 4, 6} for n in lead + R["harm"]))
chk("749.21: no low-interval breaks in the chordal parts", not RX["perception"]["low_interval_violations"])
chk("749.21: nothing in the band over her line more than a sixth of her notes", RX["perception"]["band_above_by_singer"]["her"] <= 1 / 6)
chk("749.21: no phrase over 8 seconds", RX["perception"]["phrases_over_8s"] == 0)
chk("749.23: no chord outside the key (the popular budget)", not RX["channels"]["chromatic_chords"])
chk("749.22: the harmony moves inside every sung section", all(v >= 0.5 for k, v in RX["channels"]["chord_changes_per_bar"].items() if k.startswith(("Verse", "Chorus", "Tag"))))
chk("research: every check read and written to research_p64.json", all(k in RX for k in ("surprise", "stress", "intensity", "breath", "perception", "channels")))
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier|Boundary|module|fingerprint)\b", SB, re.I))
chk("songbook: his range and hers", f"baritone, {nm(min(n['midi'] for n in lead if n['singer'] == 'him'))} to {nm(max(n['midi'] for n in lead if n['singer'] == 'him'))}" in SB and f"She sings {nm(min(n['midi'] for n in lead if n['singer'] == 'her'))} to" in SB)
chk("songbook: the hook's notes", ", ".join(nm(n["midi"]) for n in by[("Chorus 1", 5)]) in SB and ", ".join(nm(n["midi"]) for n in c4) in SB)
chk("songbook: bar count and the stop's bar", f"{R['nbars']} bars" in SB and f"bar {R['breath']['bar'] + 1}" in SB)
chk("songbook: every lyric line in the lyric sheet", all(t in SB for t in L.SUNG))
chk("songbook: the producer one-sheet, its five blocks", all(t in SB for t in ("## Producer one-sheet", "**The emotional target.**", "**The three references.**", "**The dynamic arc.**", "**The non-negotiables.**", "**The mix priorities.**")))
chk("songbook (Word): the one-sheet with a page break before and after", "Producer one-sheet" in DOCX and DOCXML.count('w:type="page"') >= 2)
chk("songbook: three references, checked by search", SB.count("checked by search") == 1 and all(t in SB for t in ("Check Yes or No", "I Never Lie", "Boots")))
chk("chart: every section", all(s.upper() in NV for s, *_ in R["plan"]))
chk("chart: the stop's bar", f"BAR {R['breath']['bar'] - B0['Verse 4'] + 1}" in NV)
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",").replace("'", "'") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("lead sheet: two vocal staves, him and her", "Him" in LY and "Her" in LY)
chk("meters: all 4/4, 126 bars, q = 120", all(b["meter"] == "4/4" and b["qbpm"] == 120 for b in R["bars"]) and len(R["bars"]) == 126)
chk("deliverables: no GarageBand MIDI (the writer)", not any("GarageBand" in f for f in os.listdir(f"{H}/out")))
chk("deliverables: every file named for the song", all(os.path.exists(f"{H}/out/{FT} - {x}") for x in ("lead sheet.pdf", "full score.pdf", "parts.pdf", "Nashville chart.pdf", "demo.mp3", "demo (General MIDI).mid", "songbook.docx", "lead sheet.mxl", "full score.mxl")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open(f"{H}/out/consistency.pkl", "wb"))
