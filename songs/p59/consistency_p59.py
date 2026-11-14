"""The World Is Asking (song 49): every document against the record."""
import pickle, re, subprocess, collections
R = pickle.load(open("/home/claude/p59/song_record.pkl", "rb")); RB = pickle.load(open("/home/claude/p59/out/readback.pkl", "rb")); RS = pickle.load(open("/home/claude/p59/out/readback_score.pkl", "rb"))
DM = pickle.load(open("/home/claude/p59/out/demo_report.pkl", "rb"))
SB = open("/home/claude/p59/songbook.md").read(); NV = open("/home/claude/p59/out/nashville.html").read()
def pdf(n): return subprocess.run(["pdftotext", f"/home/claude/p59/out/The World Is Asking - {n}.pdf", "-"], capture_output=True, text=True).stdout
LY, PT, SC = pdf("lead sheet").replace("’", "'"), pdf("parts"), pdf("full score")
import importlib.util as _u
_s = _u.spec_from_file_location("lyr", "/home/claude/p59/lyric_p59.py"); L = _u.module_from_spec(_s); _s.loader.exec_module(L)
_i = _u.spec_from_file_location("intk", "/home/claude/p59/intake.py"); I = _u.module_from_spec(_i); _i.loader.exec_module(I)
PN = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "G♯", "A", "B♭", "B"]
def nm(p): return f"{PN[p % 12]}{p // 12 - 1}"
C = []
def chk(name, ok): C.append((name, bool(ok)))
lead = R["lead"]; ps = [n["midi"] for n in lead]
by = collections.defaultdict(list)
for n in lead: by[(n["sec"], n["line"])].append(n)
hk, h7, lc7, b4, b5 = by[("Chorus 1", 0)], by[("Chorus 1", 6)], by[("Last Chorus", 7)], by[("Bridge", 4)], by[("Bridge", 5)]
for nm_, txt in (("songbook", SB), ("lead sheet", LY), ("parts", PT), ("full score", SC), ("chart", NV)): chk(f"credit line on the {nm_}", "Words and music: Jason Bryant" in txt)
chk("readback: voice (lead sheet)", RB["voice"][0]); chk("readback: voice (full score)", RS["voice"][0])
for k, v in RB["parts"].items(): chk(f"readback: {k} (parts)", v[0])
for k, v in RS["parts"].items(): chk(f"readback: {k} (full score)", v[0])
chk("drums: every hit written (parts)", RB["drums"][0] == RB["drums"][1]); chk("drums: every hit written (score)", RS["drums"][0] == RS["drums"][1])
chk("stems: voice >= +3 dB over the band", DM["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DM["energy"]}
chk("9.12: each chorus above its verse", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"])
chk("9.12: the last chorus the top", E["Last Chorus"] >= max(E.values()) - 1e-9)
chk("hook: climbs to D4 on 'ask-', '-ing' held on D4", [n["midi"] for n in hk] == [55, 57, 59, 60, 62, 62] and hk[-1]["dur"] >= 36)
chk("hook: line 7 the same figure", [n["midi"] for n in h7] == [57, 59, 60, 62, 62])
for s in ("Chorus 2",): chk(f"hooks copied in {s}", [n["midi"] for n in by[(s, 0)]] == [n["midi"] for n in hk] and [n["midi"] for n in by[(s, 6)]] == [n["midi"] for n in h7])
chk("last chorus: line 1 the hook", [n["midi"] for n in by[("Last Chorus", 0)]] == [n["midi"] for n in hk])
chk("last chorus: 'Speak, I'm listening' lands on G3 over G", lc7[-1]["midi"] == 55 and R["bars"][(lc7[-1]["on"]) // 48]["chord"] == "G")
chk("bridge: lines 1-4 within B2-G3", all(47 <= n["midi"] <= 55 for j in range(4) for n in by[("Bridge", j)]))
bsil = R["bars"][next(i for i, b in enumerate(R["bars"]) if b["sec"] == "Bridge") + 8]["start"]
chk("bridge: the silent bar (voice and band)", not any(bsil <= n["on"] < bsil + 48 for n in lead) and not any(bsil <= e["on"] < bsil + 48 for evs in R["parts"].values() for e in evs))
chk("bridge: 'Speak, I'm listening' held on D3", b5[-1]["midi"] == 50 and b5[-1]["dur"] >= 36)
vm = sorted(n["midi"] for j in range(8) for n in by[("Verse 1", j)]); cm = sorted(n["midi"] for j in (1, 2, 3, 4, 5, 7) for n in by[("Chorus 1", j)])
chk("the chorus above the verse (median two or more)", cm[len(cm) // 2] - vm[len(vm) // 2] >= 2)
chk("never-say: no word of the list in the lyric", not any(re.search(rf"\b{re.escape(w)}\b", " ".join(L.SUNG), re.I) for w in I.NEVER_SAY))
chk("songbook: no engine terms", not re.search(r"\b(engine|judge|survivor|gate|calibrat|fix \d|ZenEng|Luthier)\b", SB, re.I))
chk("songbook: the range", f"{nm(min(ps))} to {nm(max(ps))}" in SB)
chk("songbook: the hook's notes", ", ".join(nm(n["midi"]) for n in hk) in SB)
chk("songbook: bar count", f"{R['nbars']} bars" in SB)
chk("chart: every section", all(s.upper() in NV for s, *_ in R["plan"]))
chk("lead sheet: every lyric line's first syllable", all(R["text"][sec][i][0][0].strip(",") in LY for sec in R["text"] for i in range(len(R["text"][sec]))))
chk("meters: all 4/4", all(b["meter"] == "4/4" for b in R["bars"]) and len(R["bars"]) == 100)
chk("songbook: three references", SB.count("checked by search") == 1 and all(x in SB for x in ("The Stable Song", "Farther Along", "Mystery of Love")))
chk("deliverables: no GarageBand MIDI (the writer, 14 Nov)", not any("GarageBand" in f for f in __import__("os").listdir("/home/claude/p59/out")))
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
pickle.dump(C, open("/home/claude/p59/out/consistency.pkl", "wb"))
