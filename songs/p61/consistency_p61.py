"""A Wire Pulled Tight (song 51): every document against the record."""
import pickle, re, subprocess, collections, os
H = "/home/claude/p61"
R = pickle.load(open(f"{H}/song_record.pkl", "rb")); RB = pickle.load(open(f"{H}/out/readback.pkl", "rb")); RS = pickle.load(open(f"{H}/out/readback_score.pkl", "rb"))
DM = pickle.load(open(f"{H}/out/demo_report.pkl", "rb"))
SB = open(f"{H}/songbook.md").read(); NV = open(f"{H}/out/nashville.html").read()
FT = R["file_title"]
def pdf(n): return subprocess.run(["pdftotext", f"{H}/out/{FT} - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts"), pdf("full score")
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", f"{H}/lyric_p61.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; ps = [n["midi"] for n in lead]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
B0 = {}
for i, b in enumerate(R["bars"]): B0.setdefault(b["sec"], i)
def chord_on(n): return R["bars"][n["on"] // 48]["chord"]
for nm_, txt in (("songbook", SB), ("lead sheet", LY), ("parts", PT), ("full score", SC), ("chart", NV)): chk(f"credit line on the {nm_}", "Words and music: Jason Bryant" in txt)
chk("readback: voice (lead sheet)", RB["voice"][0]); chk("readback: voice (full score)", RS["voice"][0])
for k, v in RB["parts"].items(): chk(f"readback: {k} (parts)", v[0])
for k, v in RS["parts"].items(): chk(f"readback: {k} (full score)", v[0])
chk("drums: every hit written (parts)", RB["drums"][0] == RB["drums"][1]); chk("drums: every hit written (score)", RS["drums"][0] == RS["drums"][1])
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", all(E[f"Chorus {k}"] > E[f"Verse {k}"] for k in (1, 2, 3)))
chk("9.12: the choruses climb", E["Chorus 1"] < E["Chorus 2"] < E["Chorus 3"])
chk("9.12: the peak at verse 4, the bridge or a chorus", max(E, key=E.get) in ("Verse 4", "Bridge", "Chorus 3", "Last Chorus"))
h = [n["midi"] for n in by[("Chorus 1", 7)]]
chk("hook: 'time is breaking through' G#3 A3 B3 B3, C#4 held, in choruses 1-3", all([n["midi"] for n in by[(s, 7)]] == [56, 57, 59, 59, 61] and by[(s, 7)][-1]["dur"] >= 192 for s in ("Chorus 1", "Chorus 2", "Chorus 3")))
chk("hook: 'through' over Dmaj7 in choruses 1-3", all(chord_on(by[(s, 7)][-1]) == "Dmaj7" for s in ("Chorus 1", "Chorus 2", "Chorus 3")))
chk("hook: choruses 1-3 top C#4", all(max(n["midi"] for j in range(8) for n in by[(s, j)]) == 61 for s in ("Chorus 1", "Chorus 2", "Chorus 3")))
lc = by[("Last Chorus", 7)]
chk("final chorus: B3 C#4 D4 D4, E4 held over Asus4 into A", [n["midi"] for n in lc] == [59, 61, 62, 62, 64] and chord_on(lc[-1]) == "Asus4" and R["bars"][(lc[-1]["on"] + lc[-1]["dur"] - 1) // 48]["chord"] == "A")
chk("E4 the song's top, sung only in the final chorus's last line", max(ps) == 64 and all((n["sec"], n["line"]) == ("Last Chorus", 7) for n in lead if n["midi"] >= 64))
chk("no full A on a downbeat before the final chorus's release", all(b["chord"] != "A" for b in R["bars"] if not (b["sec"] in ("Last Chorus", "Tag"))))
chk("bridge: the first pass within A2-A3", all(45 <= n["midi"] <= 57 for j in range(4) for n in by[("Bridge", j)]))
bd = by[("Bridge", 6)]
chk("bridge: 'none of it was ever lost' presses to D4 over Bm", max(n["midi"] for n in bd) == 62 and chord_on(next(n for n in bd if n["midi"] == 62)) == "Bm")
chk("bridge: nothing over D4", all(n["midi"] <= 62 for j in range(8) for n in by[("Bridge", j)]))
A0 = R["bars"][B0["Approach"]]["start"]
chk("approach: a bar of silence, voice and band", not any(n["on"] < A0 + 48 and n["on"] + n["dur"] > A0 for n in lead) and not any(A0 <= e["on"] < A0 + 48 for evs in R["parts"].values() for e in evs))
chk("approach: the acoustic guitar alone after the silence", all(k == "acoustic" for k, evs in R["parts"].items() for e in evs if A0 + 48 <= e["on"] < A0 + 8 * 48))
chk("tag: the opening line as verse 1 sang it", [(n["on"] - by[("Tag", 0)][0]["on"], n["midi"]) for n in by[("Tag", 0)]] == [(n["on"] - by[("Verse 1", 0)][0]["on"], n["midi"]) for n in by[("Verse 1", 0)]])
chk("tag: 'grace' home on A2 over A", by[("Tag", 1)][-1]["midi"] == 45 and chord_on(by[("Tag", 1)][-1]) == "A")
vm = sorted(n["midi"] for j in range(4) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in range(7) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("choruses 2, 3 and the final chorus: lines 1-4 and 7 as chorus 1 (the final chorus's line 7 over G: F#3 to G3)", all([n["midi"] for n in by[(s, j)]] == [n["midi"] for n in by[("Chorus 1", j)]] for s in ("Chorus 2", "Chorus 3", "Last Chorus") for j in (0, 1, 2, 3, 6) if (s, j) != ("Last Chorus", 6))
    and [n["midi"] + (1 if n["midi"] % 12 == 6 else 0) for n in by[("Chorus 1", 6)]] == [n["midi"] for n in by[("Last Chorus", 6)]])
chk("verse lines four bars, the rest two (the hook's and the tag's last lines held)", all(R["design"]["slots"][s] == [4] * 4 for s in ("Verse 1", "Verse 2", "Verse 3", "Verse 4")) and R["design"]["slots"]["Chorus 1"] == [2] * 7 + [6])
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier|Boundary)\b", SB, re.I))
chk("songbook: the range", f"{nm(min(ps))} to {nm(max(ps))}" in SB)
chk("songbook: the hook's notes", ", ".join(nm(n["midi"]) for n in by[("Chorus 1", 7)]) in SB and ", ".join(nm(n["midi"]) for n in lc) in SB)
chk("songbook: bar count", f"{R['nbars']} bars" in SB)
chk("songbook: every tempo of the plan", all(f"♩ = {a}" in SB for a, z in R["tempo"].values()))
chk("chart: every section", all(s.upper() in NV for s, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("lead sheet: half-time feel and the felt tempo marked", "Half-time feel" in LY and "felt" in LY)
chk("meters: all 4/4, 194 bars", all(b["meter"] == "4/4" for b in R["bars"]) and len(R["bars"]) == 194)
chk("songbook: three references", SB.count("checked by search") == 1)
chk("files: named (v6), apart from the writer's v5", all("(v6)" in f for f in os.listdir(f"{H}/out") if f.startswith("A Wire Pulled Tight")))
chk("deliverables: no GarageBand MIDI (the writer, 14 Nov)", not any("GarageBand" in f for f in os.listdir(f"{H}/out")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open(f"{H}/out/consistency.pkl", "wb"))
