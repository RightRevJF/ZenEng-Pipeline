"""The Ratios Hold (song 48): every document against the record."""
import pickle, re, subprocess, json, collections
R = pickle.load(open("/home/claude/p58/song_record.pkl", "rb")); RB = pickle.load(open("/home/claude/p58/out/readback.pkl", "rb"))
DM = pickle.load(open("/home/claude/p58/out/demo_report.pkl", "rb"))
SB = open("/home/claude/p58/songbook.md").read(); NV = open("/home/claude/p58/out/nashville.html").read()
LY = subprocess.run(["pdftotext", "/home/claude/p58/out/The Ratios Hold - lead sheet.pdf", "-"], capture_output=True, text=True).stdout
PT = subprocess.run(["pdftotext", "/home/claude/p58/out/The Ratios Hold - parts.pdf", "-"], capture_output=True, text=True).stdout
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", "/home/claude/p58/lyric_p58.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
_i = _u.spec_from_file_location("intk", "/home/claude/p58/intake.py"); I = _u.module_from_spec(_i); _i.loader.exec_module(I)
PN = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; ps = [n["midi"] for n in lead]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
hook = by[("Chorus 1", 3)]
chk("credit line in the songbook", "Words and music: Jason Bryant" in SB)
chk("credit line on the lead sheet", "Words and music: Jason Bryant" in LY)
chk("credit line on the parts", "Words and music: Jason Bryant" in PT)
chk("credit line on the chart", "Words and music: Jason Bryant" in NV)
chk("readback: voice", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"readback: {k}", v[0])
chk("drums: every hit written", RB["drums"][0] == RB["drums"][1])
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"])
chk("9.12: the last chorus the top", E["Last Chorus"] >= max(E.values()) - 1e-9 or E["Last Chorus"] >= max(v for k, v in E.items() if k != "Last Chorus"))
chk("hook: three notes stepping up to B4 on 'hold'", [n["midi"] for n in hook[2:]] == [68, 69, 71])
for s in ("Chorus 2", "Last Chorus"): chk(f"hook copied in {s}", [n["midi"] for n in by[(s, 3)]] == [n["midi"] for n in hook])
chk("tag: the hook twice", all([n["midi"] for n in by[("Tag", j)]] == [n["midi"] for n in hook] for j in (0, 1)))
chk("hook: 'hold' two beats", hook[-1]["dur"] >= 24)
b5 = by[("Bridge", 5)]; chk("bridge: 'ready' on C#5, the song's top", b5[5]["midi"] == 73 == max(ps))
chk("bridge: second pair over the first", sorted(n["midi"] for j in (2, 3) for n in by[("Bridge", j)])[len([1 for j in (2, 3) for n in by[("Bridge", j)]]) // 2] > sorted(n["midi"] for j in (0, 1) for n in by[("Bridge", j)])[len([1 for j in (0, 1) for n in by[("Bridge", j)]]) // 2])
vm = sorted(n["midi"] for j in range(4) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in (0, 1, 2, 4, 5) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("never-say: no word of the list in the lyric", not any(re.search(rf"\b{re.escape(w)}\b", " ".join(L.SUNG), re.I) for w in I.NEVER_SAY))
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng)\b", SB, re.I))
chk("songbook: the range", f"{nm(min(ps))} to {nm(max(ps))}" in SB)
chk("songbook: the hook's notes", f"{nm(hook[2]['midi'])}, {nm(hook[3]['midi'])}, {nm(hook[4]['midi'])}" in SB)
chk("songbook: bar count", f"{R['nbars']} bars" in SB)
chk("chart: bar count", f"{R['nbars']} bars" in NV)
chk("chart: every section", all(s.upper() in NV for s, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("meters: 7/8 and 5/4 bars in the record", collections.Counter(b["meter"] for b in R["bars"]) == collections.Counter({"4/4": 126, "7/8": 40, "5/4": 8}))
chk("songbook: three references", SB.count("checked by search") == 1 and "Close to the Edge" in SB and "Awaken" in SB and "Similitude" in SB)
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open("/home/claude/p58/out/consistency.pkl", "wb"))
