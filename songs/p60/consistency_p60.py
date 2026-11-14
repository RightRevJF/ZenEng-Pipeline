"""The Small Things (song 50): every document against the record."""
import pickle, re, subprocess, collections
R = pickle.load(open("/home/claude/p60/song_record.pkl", "rb")); RB = pickle.load(open("/home/claude/p60/out/readback.pkl", "rb")); RS = pickle.load(open("/home/claude/p60/out/readback_score.pkl", "rb"))
DM = pickle.load(open("/home/claude/p60/out/demo_report.pkl", "rb"))
SB = open("/home/claude/p60/songbook.md").read(); NV = open("/home/claude/p60/out/nashville.html").read()
def pdf(n): return subprocess.run(["pdftotext", f"/home/claude/p60/out/The Small Things - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts"), pdf("full score")
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", "/home/claude/p60/lyric_p60.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
_i = _u.spec_from_file_location("intk", "/home/claude/p60/intake.py"); I = _u.module_from_spec(_i); _i.loader.exec_module(I)
PN = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; ps = [n["midi"] for n in lead]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
hk, hw, b3 = by[("Chorus 1", 6)], by[("Chorus 1", 7)], by[("Bridge", 3)]
for nm_, txt in (("songbook", SB), ("lead sheet", LY), ("parts", PT), ("full score", SC), ("chart", NV)): chk(f"credit line on the {nm_}", "Words and music: Jason Bryant" in txt)
chk("readback: voice (lead sheet)", RB["voice"][0]); chk("readback: voice (full score)", RS["voice"][0])
for k, v in RB["parts"].items(): chk(f"readback: {k} (parts)", v[0])
for k, v in RS["parts"].items(): chk(f"readback: {k} (full score)", v[0])
chk("drums: every hit written (parts)", RB["drums"][0] == RB["drums"][1]); chk("drums: every hit written (score)", RS["drums"][0] == RS["drums"][1])
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"])
chk("9.12: the last chorus the top", E["Last Chorus"] >= max(E.values()) - 1e-9)
chk("hook: 'I think God likes the small things' climbs to D4 on 'small', held", [n["midi"] for n in hk] == [55, 57, 59, 57, 59, 62, 59] and hk[5]["dur"] >= 18)
chk("hook: 'I think He always will' lands home on D3 over D", [n["midi"] for n in hw] == [57, 55, 54, 52, 49, 50] and R["bars"][hw[-1]["on"] // 48]["chord"] == "D")
chk("hook: D4 the song's top", max(ps) == 62)
for s in ("Chorus 2", "Last Chorus"): chk(f"every chorus the same: {s}", all([n["midi"] for n in by[(s, j)]] == [n["midi"] for n in by[("Chorus 1", j)]] for j in range(8)))
chk("bridge: lines 1-3 within A2-F#3", all(45 <= n["midi"] <= 54 for j in range(3) for n in by[("Bridge", j)]))
L3 = R["bars"][next(i for i, b in enumerate(R["bars"]) if b["sec"] == "Bridge") + 6]["start"]
chk("bridge: the beat of silence (voice and band)", not any(n["on"] < L3 + 12 and n["on"] + n["dur"] > L3 for n in lead) and not any(L3 <= e["on"] < L3 + 12 for evs in R["parts"].values() for e in evs))
chk("bridge: 'and the holy showed up clear' rises to A3, held", [n["midi"] for n in b3] == [50, 52, 54, 55, 57, 55, 57] and b3[-1]["dur"] >= 18)
vm = sorted(n["midi"] for j in range(8) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in range(6) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("never-say: no word of the list in the lyric", not any(re.search(rf"\b{re.escape(w)}\b", " ".join(L.SUNG), re.I) for w in I.NEVER_SAY))
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier)\b", SB, re.I))
chk("songbook: the range", f"{nm(min(ps))} to {nm(max(ps))}" in SB)
chk("songbook: the hook's notes", ", ".join(nm(n["midi"]) for n in hk) in SB and ", ".join(nm(n["midi"]) for n in hw) in SB)
chk("songbook: bar count", f"{R['nbars']} bars" in SB)
chk("chart: every section", all(s.upper() in NV for s, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("meters: all 4/4", all(b["meter"] == "4/4" for b in R["bars"]) and len(R["bars"]) == 96)
chk("songbook: three references", SB.count("checked by search") == 1 and all(x in SB for x in ("Morning Has Broken", "Feelin' Groovy", "Naked as We Came")))
chk("swing: marked on the lead sheet and in the songbook", "swung" in LY and "swung" in SB)
chk("deliverables: no GarageBand MIDI (the writer, 14 Nov)", not any("GarageBand" in f for f in __import__("os").listdir("/home/claude/p60/out")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open("/home/claude/p60/out/consistency.pkl", "wb"))
