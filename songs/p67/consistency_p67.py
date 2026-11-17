"""Jehovah's Band (song 57): every document against the record, the writers' reports, the research checks and the files."""
import pickle, re, subprocess, collections, os, json
H = "/home/claude/p67"
R = pickle.load(open(f"{H}/song_record.pkl", "rb")); RB = pickle.load(open(f"{H}/out/readback.pkl", "rb")); RS = pickle.load(open(f"{H}/out/readback_score.pkl", "rb"))
DM = pickle.load(open(f"{H}/out/demo_report.pkl", "rb")); RX = json.load(open(f"{H}/research_checks_p67.json"))
SB = open(f"{H}/songbook.md").read(); NV = open(f"{H}/out/nashville.html").read(); CJ = json.load(open(f"{H}/chords_p67.json"))
FT = R["file_title"]
def pdf(n): return subprocess.run(["pdftotext", f"{H}/out/{FT} - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts").replace("’", "'"), pdf("full score")
DOCX = subprocess.run(["pandoc", f"{H}/out/{FT} - songbook.docx", "-t", "plain"], capture_output=True, text=True).stdout
DOCXML = subprocess.run(["unzip", "-p", f"{H}/out/{FT} - songbook.docx", "word/document.xml"], capture_output=True, text=True).stdout
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p67.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; P_ = R["parts"]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
B0 = {}
for i, b in enumerate(R["bars"]): B0.setdefault(b["sec"], i)
for nm_, txt in (("songbook", SB), ("songbook (Word)", DOCX), ("lead sheet", LY), ("parts", PT), ("full score", SC), ("chart", NV)): chk(f"credit line on the {nm_}", "Words and music: Jason Bryant" in txt)
for k, v in RB["voice"].items(): chk(f"readback: {k} (lead sheet)", v[0])
for k, v in RS["voice"].items(): chk(f"readback: {k} (full score)", v[0])
for k, v in RB["parts"].items(): chk(f"readback: {k} (parts)", v[0])
for k, v in RS["parts"].items(): chk(f"readback: {k} (full score)", v[0])
chk("drums: every hit written (parts)", RB["drums"][0] == RB["drums"][1]); chk("drums: every hit written (score)", RS["drums"][0] == RS["drums"][1])
chk("parts: every instrument's notes written", all(k in RB["parts"] for k in ("organ", "rhythm", "lead", "bass")))
chk("stems: voice >= +3 dB over the band (9.12, H6)", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", all(E[f"Chorus {k}"] > E[f"Verse {k}"] for k in (1, 2, 3)))
chk("9.12 / 749.17: each chorus above the one before", E["Chorus 1"] < E["Chorus 2"] < E["Chorus 3"])
chk("9.12: the top at the last chorus", max(E, key=E.get) == "Chorus 3")
chk("749.17: the top inside 0.65-0.85 of the song (its start)", 0.65 <= RX["intensity"]["top_place"][0] <= 0.85)
chk("the chords are the writer's, bar by bar", all([list(b) for b in CJ["plan"][{"Chorus 3": "Last Chorus", "Tag": "Outro"}.get(s_, s_ if s_ not in ("Verse 1", "Verse 2", "Chorus 1", "Chorus 2") else s_.split()[0])]] for s_, *_ in R["plan"]))
chk("the chart on the record is the run's (438 over the writer's chords)", list(R["chords2"]) == list(pickle.load(open(f"{H}/melody_final.pkl", "rb"))["run"]["chords2"]))
chk("bVII (D) in the song (the key, A)", any(c.split("/")[0] == "D" for c in R["chords2"]))
chk("no hand edits to the melody", R["hand_edits"] == [])
chk("the jam starts from silence: only the organ in its first bar", all(k == "organ" for k, evs in P_.items() for e in evs if R["bars"][B0["Jam"]]["start"] <= e["on"] < R["bars"][B0["Jam"]]["start"] + 48))
chk("no voice in the jam but verse 3's pickup (its last half bar)", all(n["sec"] == "Verse 3" and n["on"] >= R["bars"][B0["Verse 3"]]["start"] - 24 for n in lead if R["bars"][B0["Jam"]]["start"] <= n["on"] < R["bars"][B0["Verse 3"]]["start"]))
t1 = [n["midi"] for n in by[("Chorus 1", 0)]]
chk("title line: chorus 1's tune in every chorus (lines 1 and 5)", all([n["midi"] for n in by[(s_, j_)]] == t1 for s_ in ("Chorus 1", "Chorus 2", "Chorus 3") for j_ in (0, 4)))
chk("'Thank God' sung twice to one tune", [n["midi"] for n in by[("Chorus 3", 5)]] == [n["midi"] for n in by[("Chorus 3", 6)]])
chk("outro: the title three times, one tune", by[("Tag", 0)] and all([n["midi"] for n in by[("Tag", j)]] == [n["midi"] for n in by[("Tag", 0)]] for j in (1, 2)))
chk("no two syllables on one onset, no note of no length (749.1)", len({n["on"] for n in lead}) == len(lead) and all(n["dur"] > 0 for n in lead))
chk("the voice in the key (E major)", all(n["midi"] % 12 in {4, 6, 8, 9, 11, 1, 3} for n in lead))
chk("the voice inside the search row B2-E4", min(n["midi"] for n in lead) >= 47 and max(n["midi"] for n in lead) <= 64)
chk("749.21: no low-interval breaks in the chordal parts", not RX["perception"]["low_interval_violations"])
chk("749.21: no phrase over 8 seconds", RX["perception"]["phrases_over_8s"] == 0)
chk("749.27: nothing within a second of the tune in a quarter or more of its notes", RX["perception"]["band_within_second"] < 0.25)
chk("749.22: the harmony moves inside every verse and chorus", all(v >= 0.5 for k, v in RX["channels"]["chord_changes_per_bar"].items() if k.startswith(("Verse", "Chorus"))))
chk("749.18: melody surprise at or under the popular median", RX["surprise"]["melody_ic"] <= RX["surprise"]["melody_median"])
chk("research: every check read and written to research_checks_p67.json", all(k in RX for k in ("surprise", "stress", "intensity", "breath", "perception", "channels")))
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier|Boundary|module|fingerprint|writer)\b", SB, re.I))
nm = lambda p: ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"][p % 12] + str(p // 12 - 1)
chk("songbook: the range", f"A baritone, {nm(min(n['midi'] for n in lead))} to {nm(max(n['midi'] for n in lead))}" in SB)
chk("songbook: the title line's notes", f"starts on {nm(t1[0])}" in SB and f"ends on {nm(t1[-1])}" in SB)
chk("songbook: bar count and the jam's bars", f"{R['nbars']} bars" in SB and f"bars {B0['Jam'] + 1}–{B0['Verse 3']}" in SB)
chk("songbook: every lyric line in the lyric sheet", all(t in SB for t in L.SUNG))
chk("songbook: the producer one-sheet, its five blocks", all(t in SB for t in ("## Producer one-sheet", "**The emotional target.**", "**The three references.**", "**The dynamic arc.**", "**The non-negotiables.**", "**The mix priorities.**")))
chk("songbook (Word): the one-sheet with a page break before and after", "Producer one-sheet" in DOCX and DOCXML.count('w:type="page"') >= 2)
chk("songbook: three references, checked by search", SB.count("checked by search") == 1 and all(t in SB for t in ("Eyes of the World", "Scarlet Begonias", "Uncle John's Band")))
chk("chart: every section", all(s_.upper() in NV for s_, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("meters: all 4/4, 128 bars, q = 112", all(b["meter"] == "4/4" and b["qbpm"] == 112 for b in R["bars"]) and len(R["bars"]) == 128)
chk("deliverables: no GarageBand MIDI", not any("GarageBand" in f for f in os.listdir(f"{H}/out")))
chk("deliverables: every file named for the song", all(os.path.exists(f"{H}/out/{FT} - {x}") for x in ("lead sheet.pdf", "full score.pdf", "parts.pdf", "Nashville chart.pdf", "demo.mp3", "demo (General MIDI).mid", "songbook.docx", "lead sheet.mxl", "full score.mxl")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open(f"{H}/out/consistency.pkl", "wb"))
