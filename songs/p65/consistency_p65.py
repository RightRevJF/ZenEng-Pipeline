"""Your Yard Man (song 55): every document against the record, the designs, the research checks and the files."""
import pickle, re, subprocess, collections, os, json
H = "/home/claude/p65"
R = pickle.load(open(f"{H}/song_record.pkl", "rb")); RB = pickle.load(open(f"{H}/out/readback.pkl", "rb")); RS = pickle.load(open(f"{H}/out/readback_score.pkl", "rb"))
DM = pickle.load(open(f"{H}/out/demo_report.pkl", "rb")); RX = json.load(open(f"{H}/research_p65.json"))
SB = open(f"{H}/songbook.md").read(); NV = open(f"{H}/out/nashville.html").read()
FT = R["file_title"]
def pdf(n): return subprocess.run(["pdftotext", f"{H}/out/{FT} - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts").replace("’", "'"), pdf("full score")
DOCX = subprocess.run(["pandoc", f"{H}/out/{FT} - songbook.docx", "-t", "plain"], capture_output=True, text=True).stdout
DOCXML = subprocess.run(["unzip", "-p", f"{H}/out/{FT} - songbook.docx", "word/document.xml"], capture_output=True, text=True).stdout
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p65.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
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
chk("parts: each part's role note", all(t in PT for t in ("the floor of the song", "short answers in the gaps", "plays the call and the answer", "swells under the choruses", "offbeat chords", "a two-step. On 1 and 3", "a two-step with sticks")))
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", all(E[f"Chorus {k}"] > E[f"Verse {k}"] for k in (1, 2, 3)))
chk("9.12 / 749.17: each return above the one before", E["Chorus 1"] < E["Chorus 2"] < E["Chorus 3"])
chk("9.12: the top at chorus 3", max(E, key=E.get) == "Chorus 3")
chk("verse 2 (his daddy) the quietest verse", E["Verse 2"] < E["Verse 1"] and E["Verse 2"] < E["Verse 3"])
CALL, ANSWER = [57, 61, 64, 61], [64, 61, 59, 61, 57]
chk("hook: the call A3 C#4 E4 C#4 on chorus lines 1 and 9, every chorus", all([n["midi"] for n in by[(s_, j_)]] == CALL for s_ in ("Chorus 1", "Chorus 2", "Chorus 3") for j_ in (0, 8)))
chk("hook: the answer E4 C#4 B3 C#4 A3, home on A over A, every chorus", all([n["midi"] for n in by[(s_, 9)]] == ANSWER and chord_on(by[(s_, 9)][-1]) == "A" for s_ in ("Chorus 1", "Chorus 2", "Chorus 3")))
chk("hook: 'yard' on E4 over A, on beat 3", all(by[(s_, 0)][2]["midi"] == 64 and chord_on(by[(s_, 0)][2]) == "A" and by[(s_, 0)][2]["on"] % 48 == 24 for s_ in ("Chorus 1", "Chorus 2", "Chorus 3")))
hl = {(s_, j_) for s_ in ("Chorus 1", "Chorus 2", "Chorus 3") for j_ in (0, 8, 9)} | {("Tag", 0), ("Tag", 1)}
chk("E4 the song's top, sung only on the hook", max(n["midi"] for n in lead) == 64 and all((n["sec"], n["line"]) in hl for n in lead if n["midi"] >= 64))
chk("tag: the call, then the answer home on A3", [n["midi"] for n in by[("Tag", 0)]] == CALL and [n["midi"] for n in by[("Tag", 1)]] == ANSWER)
t0 = R["bars"][B0["Tag"]]["start"]
chk("tag: the call over a stop (only a kick and crash under it)", all(k == "drums" for k, evs in P_.items() for e in evs if t0 <= e["on"] < t0 + 48))
st = R["breath"]["at"]
chk("the breath (749.19): the break's last bar the acoustic alone", all(k == "acoustic" for k, evs in P_.items() for e in evs if st <= e["on"] < st + 48) and not any(n["on"] < st + 48 and n["on"] + n["dur"] > st for n in lead))
chk("harmony on the call and the answer in every chorus and the tag", all(any(h["sec"] == s_ and h["line"] == j_ for h in R["harm"]) for s_, j_ in hl))
vm = sorted(n["midi"] for j in range(8) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in range(1, 8) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("slots: verse lines two bars; the chorus 1,1,1,1,2,2,2,2,1,1; the tag 1,1", all(R["design"]["slots"][s_] == [2] * 8 for s_ in ("Verse 1", "Verse 2", "Verse 3")) and all(R["design"]["slots"][s_] == [1, 1, 1, 1, 2, 2, 2, 2, 1, 1] for s_ in ("Chorus 1", "Chorus 2", "Chorus 3")) and R["design"]["slots"]["Tag"] == [1, 1])
chk("no two syllables on one onset, no note of no length (749.1)", len({n["on"] for n in lead}) == len(lead) and all(n["dur"] > 0 for n in lead))
chk("the voice in the key (A major)", all(n["midi"] % 12 in {9, 11, 1, 2, 4, 6, 8} for n in lead + R["harm"]))
chk("749.21: no low-interval breaks in the chordal parts", not RX["perception"]["low_interval_violations"])
chk("749.21: no phrase over 8 seconds", RX["perception"]["phrases_over_8s"] == 0)
chk("749.23: no chord outside the key (the popular budget)", not RX["channels"]["chromatic_chords"])
chk("749.22: the harmony moves inside every verse and chorus", all(v >= 0.5 for k, v in RX["channels"]["chord_changes_per_bar"].items() if k.startswith(("Verse", "Chorus"))))
chk("research: every check read and written to research_p65.json", all(k in RX for k in ("surprise", "stress", "intensity", "breath", "perception", "channels")))
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier|Boundary|module|fingerprint)\b", SB, re.I))
chk("songbook: the range", f"A baritone, {nm(min(n['midi'] for n in lead))} to {nm(max(n['midi'] for n in lead))}" in SB)
chk("songbook: the hook's notes", ", ".join(nm(n["midi"]) for n in by[("Chorus 1", 9)]) in SB)
chk("songbook: bar count and the breath's bar", f"{R['nbars']} bars" in SB and f"bar {R['breath']['bar'] + 1}" in SB)
chk("songbook: every lyric line in the lyric sheet", all(t in SB for t in L.SUNG))
chk("songbook: the producer one-sheet, its five blocks", all(t in SB for t in ("## Producer one-sheet", "**The emotional target.**", "**The three references.**", "**The dynamic arc.**", "**The non-negotiables.**", "**The mix priorities.**")))
chk("songbook (Word): the one-sheet with a page break before and after", "Producer one-sheet" in DOCX and DOCXML.count('w:type="page"') >= 2)
chk("songbook: three references, checked by search", SB.count("checked by search") == 1 and all(t in SB for t in ("Little Man", "I Never Lie", "Check Yes or No")))
chk("chart: every section", all(s_.upper() in NV for s_, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("meters: all 4/4, 102 bars, q = 120", all(b["meter"] == "4/4" and b["qbpm"] == 120 for b in R["bars"]) and len(R["bars"]) == 102)
chk("deliverables: no GarageBand MIDI", not any("GarageBand" in f for f in os.listdir(f"{H}/out")))
chk("deliverables: every file named for the song", all(os.path.exists(f"{H}/out/{FT} - {x}") for x in ("lead sheet.pdf", "full score.pdf", "parts.pdf", "Nashville chart.pdf", "demo.mp3", "demo (General MIDI).mid", "songbook.docx", "lead sheet.mxl", "full score.mxl")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open(f"{H}/out/consistency.pkl", "wb"))
