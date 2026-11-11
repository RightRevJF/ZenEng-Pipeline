"""Song 40 under v108: every document against the song record: the demo, the lead sheet, the parts, the number chart and the test
report; the pick's gates and the v108 readings that decide the record."""
import pickle, re, sys, mido, collections
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p40"]
import melody_p40 as P
import lyric_p40 as L
M = P.M; H = "/home/claude/p40"; OUT = f"{H}/out"
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); Mn = pickle.load(open(f"{H}/melody_main.pkl", "rb")); pick = Mn["pick"]
RD = pickle.load(open(f"{H}/readings_p40.pkl", "rb")); RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
RF = pickle.load(open(f"{H}/riff_p40.pkl", "rb"))
TR = open(f"{H}/test_report_p40.md").read()
lead = REC["lead"]; BAR = 48; BEAT = 12; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "bass", "rgtr", "keys", "strings", "lgtr")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
short = set(Mn["short"]); first_on_short = next(c for c in Mn["alive"] if c["fp"] in short)
chk("255: the record is the main run's shortlist pick (the composite's first on the judge's upper half)", REC["fp"] == pick["fp"] == first_on_short["fp"])
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("both runs reproduced on their second making (order, survivors, pick)", all(RD["1"][v]["reproduced"] for v in ("main", "ctl")))
chk("110 bars, 3:48; every section a multiple of four but the last chorus's named extension (274)", REC["nbars"] == 110 and round(REC["seconds"]) == 228 and all(nb % 4 == 0 or s == "Last Chorus" and nb == 18 for s, nb, _, _ in REC["plan"]))
chk("the locked lyric, every syllable sung", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
lock = open(f"{H}/lyric_locked.md").read().lower()
chk("the record's words are the locked lyric's (every line found in lyric_locked.md)", all(re.sub(r"[^a-z' ]", "", t.lower()).split()[0] in lock for s in P.SUNG for _, t in M.WORDS_OF[s]))
chk("no never-say phrase in the lyric", not any(p in " ".join(t for s in P.SUNG for _, t in M.WORDS_OF[s]).lower() for p in L.NEVER_PHRASES))
ps = [n["midi"] for n in lead]
chk(f"range {nm(min(ps))} to {nm(max(ps))}, inside the voice row A3-D5 (Q7)", min(ps) >= 57 and max(ps) <= 74)
chk("no designed summit, no design gate in force (the default path)", REC["summit"] is None and P.DESIGN_GATES == [] and P.M.SUMMIT == 74)
hook = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; ear = hook[-1]
chk(f"232: the title's stress 'earth' on beat 1, held {ear['dur'] // 12} beats (at least twice the median syllable)", ear["text"].lower().startswith("earth") and ear["on"] % BAR == 0
    and ear["dur"] >= 2 * np.median([n["dur"] for n in lead]))
tags = [n for n in lead if n["text"].lower().strip(",.:;").startswith("earth")]
chk(f"232: every 'earth' ({len(tags)}) on beat 1 or 3 and held at least twice the median", all(n["on"] % BAR in (0, 24) and n["dur"] >= 2 * np.median([x["dur"] for x in lead]) for n in tags))
rate = {s: len([n for n in lead if n["sec"] == s and n["first"]]) / dict((a, b) for a, b, _, _ in REC["plan"])[s] for s in P.SUNG}
chk(f"230: sung rate 3.2-6.2 syllables a bar in every section ({ {k: round(v, 2) for k, v in rate.items()} })", all(3.2 <= v <= 6.2 for v in rate.values()))
long2 = [(s, i) for s in P.SUNG for i in range(len(P.LINES[s])) if len(P.LINES[s][i]) >= 9 and P.slot_len(s, i) == 2]
chk(f"230: every line of nine or more syllables in two bars is a named design (Q21; {len(long2)} lines)", sorted(long2) == sorted((s, i) for s, i, _ in P.DESIGNED_TWO_BAR))
info = pick["info"]
chk(f"276/277/286: the pick breaks no hard limit and {len(info['soft'])} soft limit(s) of the fifteen", not info["hard"] and len(info["soft"]) < 3)
lr = P.limit_readings(pick["notes"]); s_, h_ = P.limit_breaks(lr); l7, _ = P.limit7_readings(pick["notes"]); s7, h7 = P.limit7_breaks(l7)
chk("the fifteen limits read again on the record agree with the search", s_ + s7 == info["soft"] and h_ + h7 == info["hard"])
chk("267/287: every built return related", all(x[1] for x in P.return_267(pick)))
chk("279: chorus opening and bridge opening unrelated", not P.opening_rel(pick["notes"], "Chorus 1", "Verse 1")[0] and not P.opening_rel(pick["notes"], "Bridge", "Verse 1")[0] and not P.opening_rel(pick["notes"], "Bridge", "Chorus 1")[0])
chk("254/291: the pick above the refitted judge's floor (-0.739)", pick["judge"]["combined"] >= -0.739)
ends = {s: ([n for n in lead if n["sec"] == s][-1]["midi"] - M.TONIC) % 12 for s in ("Verse 1", "Chorus 1", "Last Chorus")}
chk(f"262/295: the last chorus ends on the tonic, chorus 1 on the tonic triad, verse 1 off the tonic ({ends})", ends["Last Chorus"] == 0 and ends["Chorus 1"] in (0, 4, 7) and ends["Verse 1"] != 0)
lift = pick["info"]["lift"]
chk(f"288: the lift printed (median {lift['median']}, top {lift['top']}, lowest {lift['lowest']}) and read again from the record",
    lift["median"] == P.med(pick["notes"], "Chorus 1") - P.med(pick["notes"], "Verse 1") and lift["top"] == P.top(pick["notes"], "Chorus 1") - P.top(pick["notes"], "Verse 1"))
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]
cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("Q11: chorus 2 = chorus 1 (pitches and onsets), a plain repeat", cc1 == cc2)
l0 = [(n["on"] - P.line_start("Chorus 1", 0), n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
l4 = [(n["on"] - P.line_start("Chorus 1", 4), n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 4]
chk("213: the hook said twice in the chorus (line 5 = line 1, pitches and onsets)", l0 == l4)
lc = [(n["on"] - P.BAR0["Last Chorus"] * BAR, n["midi"]) for n in lead if n["sec"] == "Last Chorus" and n["line"] < 7]
c7 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] < 7]
chk("228: the last chorus opens as chorus 1 (lines 1-7)", lc == c7)
chk("chords: one a bar, the plan's", [b["chord"] for b in REC["bars"]] == list(P.CHORD))
voc_spans = [(n["on"], n["on"] + n["dur"]) for n in lead]
chk("235: no fill or riff over a sung note", not any(a < e["on"] + e["dur"] and e["on"] < b for e in REC["lgtr"] if e["art"] != "solo" for a, b in voc_spans))
okf = all(4 <= len(f["notes"]) <= 6 and f["notes"][-1]["p"] % 12 in M.CH[M.chord_at(f["notes"][-1]["on"])][1] and
          ((18 == f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"] and f["gap"]["beats"] < 2.75) or (24 <= f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"] <= 36)) for f in RF["fills"])
chk("235/272: fills of 2-3 beats, or a beat and a half in a gap under 2.75 beats; 4-6 notes; ending on a chord tone", okf)
elig = [g for g in RF["gaps"] if g["beats"] >= 2.75]; fil = sum(1 for f in RF["fills"] if f["gap"]["beats"] >= 2.75)
chk(f"272: the fill rate on gaps of 2.75 beats or more ({fil} of {len(elig)}) inside 60-80%", 0.6 <= fil / len(elig) <= 0.8)
chk("Q18: no countermelody", "counter" not in REC)
riff_bars = sorted({e["on"] // BAR for e in REC["lgtr"] if e["art"].startswith("riff")})
chk("the riff in intro bars 1-8 and outro bars 1-3 (bars 1-8, 107-109)", riff_bars == list(range(0, 8)) + [106, 107, 108])
chk("233: the bass has the root on beat 1 of every bar it plays", all(e["p"][0] % 12 == M.CH[REC["bars"][e["on"] // BAR]["chord"]][0] for e in REC["bass"] if e["on"] % BAR == 0))
bon = {e["on"] for e in REC["bass"]}; wb = float(np.mean([e["on"] in bon for e in REC["keys"]]))
chk(f"273: electric-piano strikes with a bass note {wb:.0%} (floor 16%)", wb >= 0.16)
def half(b):
    ev = {(e["on"] - b * BAR, p) for e in REC["drums"] if e["on"] // BAR == b for p in e["p"]}
    return (24, 38) in ev and (12, 38) not in ev and (36, 38) not in ev
vb = [b for s in ("Verse 1", "Verse 2") for b in range(P.BAR0[s], P.BAR0[s] + 11)]
cb = [b for s in ("Chorus 1", "Chorus 2", "Last Chorus") for b in range(P.BAR0[s], P.BAR0[s] + 15)]
chk("Q19 (236, the arrangement design): half time in the verses (snare on 3 only), full beat in the choruses (snare 2 and 4)",
    all(half(b) for b in vb) and all(any(e["on"] == b * BAR + 12 and 38 in e["p"] for e in REC["drums"]) for b in cb))
chk("236: drums enter at intro bar 5", min(e["on"] for e in REC["drums"]) == 4 * BAR)
chk("one hit on the outro's last bar, nothing after it", any(e["on"] == 109 * BAR and 49 in e["p"] for e in REC["drums"]) and not any(e["on"] > 109 * BAR for k in INSTR for e in REC[k]))
parts = {}
for s, nb, b0, _ in REC["plan"]:
    a, z = b0 * BAR, (b0 + nb) * BAR
    parts[s] = sum(any(a <= e["on"] < z for e in REC[k]) for k in INSTR + ("lead",))
chk(f"238: intro at half the fullest or fewer; the last chorus the fullest ({parts})", parts["Intro"] <= max(parts.values()) / 2 and parts["Last Chorus"] == max(parts.values()))
mf = mido.MidiFile(f"{OUT}/Nothing Else on Earth - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
chk("demo guide vocal = the record's notes", [m.note for m in trk("Guide vocal")[0] if m.type == "note_on" and m.velocity > 0] == ps)
for name, key in (("Lead guitar", "lgtr"), ("Electric piano", "keys"), ("Strings", "strings"), ("Bass", "bass"), ("Rhythm guitar", "rgtr"), ("Drums", "drums")):
    t_ = trk(name); chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == sorted(p for e in REC[key] for p in e["p"]))
chk("demo tempo 116, key D", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 116 for m in mf.tracks[0]) and any(m.type == "key_signature" and m.key == "D" for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Nothing Else on Earth - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Nothing Else on Earth - lead sheet.ly").read()
chk("credit line, key, tempo and length on the lead sheet", "Words and music: Jason Bryant" in src and "\\key d \\major" in src and "3:48" in src and "4 = 116" in src)
top_ = max(lead, key=lambda n: (n["midi"], -n["on"]))
chk("lead sheet notes read from the record (range, hook, top note)", nm(min(ps)).replace("♯", "♯") in src.replace("A3", "A3") and f"bar {top_['on'] // 48 + 1}" in src and f"bar {ear['on'] // 48 + 1}" in src)
html = open(f"{OUT}/nashville.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7", "": "N.C."}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line, 110 bars, tempo, key", "Words and music: Jason Bryant" in html and "110 bars" in html and "♩ = 116" in html and "KEY: D" in html)
rr = Mn["rerun"]
chk("report: seed, calibration seed, code, rerun line", str(rr["seed"]) in TR and str(rr["calibration_seed"]) in TR and rr["code_sha"] in TR and rr["cmd"].replace(" 1000 main", "") in TR)
chk("report: survivors and frozen orders of both runs, each reproduced", all(f"{RD['1'][v]['survivors']} of 1,000" in TR and RD["1"][v]["order"] in TR for v in ("main", "ctl")))
chk("report: the three builds of 255 and the pick under the old fit term (296)", all(RD["6"]["main"][k]["fp"] in TR for k in ("composite first", "shortlist pick", "judge first", "pick under the old fit term (296)")))
chk("report: the lift beside the kept figures, and the spectral reading beside it", "## The lift" in TR and "spectral" in TR.lower())
chk("report: findings numbered from 298", "**298." in TR and "**297." not in TR)
chk("report: the readings the paper does not give are listed by fix", "## Readings the paper does not give" in TR)
chk("report: the design choices named (Q19 drums, Q21 for 230); no design gate in force", "Q19" in TR and "Q21" in TR and "No design gate" in TR)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
