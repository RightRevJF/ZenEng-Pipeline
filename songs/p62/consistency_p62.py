"""The Room Next Door (song 52): every document against the record."""
import pickle, re, subprocess, collections, os, json
H = "/home/claude/p62"
R = pickle.load(open(f"{H}/song_record.pkl", "rb")); RB = pickle.load(open(f"{H}/out/readback.pkl", "rb")); RS = pickle.load(open(f"{H}/out/readback_score.pkl", "rb"))
DM = pickle.load(open(f"{H}/out/demo_report.pkl", "rb"))
SB = open(f"{H}/songbook.md").read(); NV = open(f"{H}/out/nashville.html").read()
def pdf(n): return subprocess.run(["pdftotext", f"{H}/out/The Room Next Door - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts"), pdf("full score")
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; ps = [n["midi"] for n in lead]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
B0 = {}
for i, b in enumerate(R["bars"]): B0.setdefault(b["sec"], i)
def chord_on(n): return R["bars"][n["on"] // 36]["chord"]
for nm_, txt in (("songbook", SB), ("lead sheet", LY), ("parts", PT), ("full score", SC), ("chart", NV)): chk(f"credit line on the {nm_}", "Words and music: Jason Bryant" in txt)
chk("readback: voice (lead sheet)", RB["voice"][0]); chk("readback: voice (full score)", RS["voice"][0])
for k, v in RB["parts"].items(): chk(f"readback: {k} (parts)", v[0])
for k, v in RS["parts"].items(): chk(f"readback: {k} (full score)", v[0])
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"])
chk("9.12: the last chorus the top", E["Last Chorus"] >= max(E.values()) - 1e-9)
chk("9.12: the bridge the hush", E["Bridge"] == min(v for k, v in E.items() if k not in ("Intro", "Outro")))
chk("metre: 6/8 throughout, 84 bars of 36 ticks", all(b["meter"] == "6/8" and b["len"] == 36 for b in R["bars"]) and len(R["bars"]) == 84)
chk("hook: 'door' on D5 in every first hook, 'wall' open on A4 over Asus4", all([n["midi"] for n in by[(s, 4)]] == [69, 71, 74, 71, 69, 69] and chord_on(by[(s, 4)][-1]) == "Asus4" for s in ("Chorus 1", "Chorus 2", "Last Chorus")))
chk("hook: D5 the top, sung only on 'door'", max(ps) == 74 and all(n["text"].lower().startswith("door") for n in lead if n["midi"] == 74))
chk("hook: the second time home on D4 over Dadd9", by[("Last Chorus", 5)][-1]["midi"] == 62 and chord_on(by[("Last Chorus", 5)][-1]) == "Dadd9")
chk("bridge: first three lines B3-F#4 or lower, guitar and bass out", all(n["midi"] <= 66 for j in range(3) for n in by[("Bridge", j)]) and not any(B0["Bridge"] * 36 <= e["on"] < B0["Verse 4"] * 36 for k in ("guitar", "bass") for e in R["parts"][k]))
th = by[("Bridge", 3)]
chk("bridge: 'and you were there' lifts to B4; 'gone' held on E4 over A7sus4", max(n["midi"] for n in th) == 71 and th[-1]["midi"] == 64 and chord_on(th[-1]) == "A7sus4" and th[-1]["dur"] >= 18)
chk("B-flat maj7 under 'and some morning it opens'", R["bars"][B0["Last Chorus"] + 5]["chord"] == "Bbmaj7" and B0["Last Chorus"] + 4 <= by[("Last Chorus", 2)][0]["on"] // 36 <= B0["Last Chorus"] + 5)
chk("voice in the scale (D major)", all(p % 12 in {2, 4, 6, 7, 9, 11, 1} for p in ps))
chk("no run of four of one pitch in a line (749.2)", all(not any(v[k]["midi"] == v[k + 1]["midi"] == v[k + 2]["midi"] == v[k + 3]["midi"] for k in range(len(v) - 3)) for v in by.values()))
chk("no note of no length, no two onsets alike in a line (749.1)", all(n["dur"] > 0 for n in lead) and all(len({n["on"] for n in v}) == len(v) for v in by.values()))
chk("chorus 2 sung exactly as chorus 1", all([(n["on"] - B0["Chorus 2"] * 36, n["midi"]) for n in by[("Chorus 2", j)]] == [(n["on"] - B0["Chorus 1"] * 36, n["midi"]) for n in by[("Chorus 1", j)]] for j in range(5)))
vm = sorted(n["midi"] for j in range(4) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in range(4) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier|Essen|sketch)\b", SB, re.I))
chk("songbook: the range", f"{nm(min(ps))} to {nm(max(ps))}" in SB)
chk("songbook: the hook's notes", ", ".join(nm(n["midi"]) for n in by[("Chorus 1", 4)]) in SB and ", ".join(nm(n["midi"]) for n in by[("Last Chorus", 5)]) in SB)
chk("songbook: bar count", f"{R['nbars']} bars" in SB)
chk("songbook: three references", SB.count("checked by search") == 1)
chk("chart: every section", all(s.upper() in NV for s, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("lead sheet: 6/8 tempo marked", "Gently rocking" in LY)
chk("deliverables: no GarageBand MIDI (the writer, 14 Nov)", not any("GarageBand" in f for f in os.listdir(f"{H}/out")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open(f"{H}/out/consistency.pkl", "wb"))
