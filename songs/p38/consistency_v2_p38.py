"""Song 38 rerun under v107 (v2): every document against the v2 song record: the demo, the lead sheet, the parts, the number
chart and the test report; the pick's design gates and the v107 readings that decide the record."""
import pickle, re, sys, mido, collections
import numpy as np
sys.argv = ["x", "1", "B"]; sys.path[:0] = ["/home/claude/p38"]
import melody_v2_p38 as P
import lyric_p38 as L
M = P.M; H = "/home/claude/p38"; OUT = f"{H}/out_v2"
REC = pickle.load(open(f"{H}/song_record_v2.pkl", "rb")); Mn = pickle.load(open(f"{H}/melody_v2_B.pkl", "rb")); pick = Mn["pick"]
RD = pickle.load(open(f"{H}/readings_v2.pkl", "rb")); RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
RF = pickle.load(open(f"{H}/riff_v2_p38.pkl", "rb"))
TR = open(f"{H}/test_report_v2.md").read()
lead = REC["lead"]; BAR = 48; ok = []; BEAT = 12
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
short = set(Mn["short"]); first_on_short = next(c for c in Mn["alive"] if c["fp"] in short)
chk("255: the record is Run B's shortlist pick (the composite's first on the judge's upper half)", REC["fp"] == pick["fp"] == first_on_short["fp"])
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("274: 114 bars, 3:27; every section a multiple of four but the last chorus's named extension", REC["nbars"] == 114 and round(REC["seconds"]) == 207 and all(nb % 4 == 0 or s == "Last Chorus" and nb == 18 for s, nb, _, _ in REC["plan"]))
chk("the locked lyric, every syllable sung", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
chk("no never-say phrase in the lyric", not any(p in " ".join(L.SUNG).lower() for p in L.NEVER_PHRASES))
ps = [n["midi"] for n in lead]
chk(f"range {nm(min(ps))} to {nm(max(ps))}, inside the voice row", min(ps) >= M.LO and max(ps) == 69)
sm = [n for n in lead if n["midi"] == 69]
chk("design gate (216, 244): A4 six times on 'tuned', beat 1, over A, bars 21, 29, 49, 57, 89, 97", len(sm) == 6 and all(n["text"].lower().startswith("tuned") and n["on"] % BAR == 0 and REC["bars"][n["on"] // BAR]["chord"] == "A" for n in sm) and [n["on"] // BAR + 1 for n in sm] == [21, 29, 49, 57, 89, 97])
chk("232: the title's stress held three beats", all(n["dur"] == 36 for n in sm))
c1 = [n for n in lead if n["sec"] == "Chorus 1"]; l0 = [n for n in c1 if n["line"] == 0]; l1 = [n for n in c1 if n["line"] == 1]
moved = sum(1 for a, b in zip(l0, l1) if b["midi"] - a["midi"] != -2)
chk(f"282: the said-twice line is line 1 moved whole a whole step down ({moved} note(s) changed, each for 276's tritone reading)",
    len(l0) == len(l1) and [b["on"] - a["on"] for a, b in zip(l0, l1)] == [96] * len(l0) and moved == pick["meta"]["twice_changed"])
chk("said twice: 'tuned' in line 2 on G4 over G", l1[1]["midi"] == 67 and REC["bars"][l1[1]["on"] // BAR]["chord"] == "G")
info = pick["info"]
chk(f"276/277: the pick breaks no hard limit and {len(info['soft'])} soft limit(s) {info['soft']}", not info["hard"] and len(info["soft"]) < 3)
lr = P.limit_readings(pick["notes"]); s_, h_ = P.limit_breaks(lr)
chk("276: the limits read again on the record agree with the search", s_ == info["soft"] and h_ == info["hard"])
ends = {s: (max((n for n in lead if n["sec"] == s), key=lambda n: n["on"])["midi"] - M.TONIC) % 12 for s in ("Verse 1", "Verse 2", "Chorus 1", "Chorus 2", "Last Chorus")}
chk(f"262: the last chorus ends on the tonic, chorus 1 on a note of the tonic triad, the verse off the tonic ({ends})", ends["Last Chorus"] == 0 and ends["Chorus 1"] in (0, 4, 7) and ends["Verse 1"] != 0)
er, _ = P.era_read(pick["notes"]); ins = P.era_inside(er)
chk(f"264: the pick inside CLASSIC's 5th-95th on {len(ins)} of five bands (four needed)", len(ins) >= 4)
chk("267: every built return related", all(x[1] for x in P.return_267(pick)))
chk("design gate (208): bridge above the verse, under the summit", P.med(pick["notes"], "Bridge") > P.med(pick["notes"], "Verse 1") and P.top(pick["notes"], "Bridge") < 69)
chk("279: chorus opening and bridge opening unrelated", not P.opening_rel(pick["notes"], "Chorus 1", "Verse 1")[0] and not P.opening_rel(pick["notes"], "Bridge", "Verse 1")[0] and not P.opening_rel(pick["notes"], "Bridge", "Chorus 1")[0])
chk("254: the pick above the judge's floor", pick["judge"]["combined"] >= -0.059)
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]
cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1 (pitches and onsets)", cc1 == cc2)
lc = [(n["on"] - P.BAR0["Last Chorus"] * BAR, n["midi"]) for n in lead if n["sec"] == "Last Chorus" and n["line"] < 6]
c6 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] < 6]
chk("228: the last chorus opens as chorus 1 (lines 1-6)", lc == c6)
tag = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 8]
chk("'Turn it off.': E4-C#4-A3 in the stop bars, nothing else sounding", [n["midi"] for n in tag] == [64, 61, 57] and all(n["on"] // BAR in REC["stop_bars"] for n in tag)
    and not any(e["on"] // BAR in REC["stop_bars"] or (e["on"] < REC["stop_bars"][0] * BAR < e["on"] + e["dur"] and e["art"] != "ring") for k in ("drums", "bass", "rgtr", "organ", "lgtr", "keys", "bvox", "counter") for e in REC[k]))
chk("one hit on the outro's first beat", any(e["on"] == P.BAR0["Outro"] * BAR and 49 in e["p"] for e in REC["drums"]) and not any(e["on"] > P.BAR0["Outro"] * BAR for k in ("drums", "bass", "rgtr", "organ", "lgtr", "keys", "bvox", "counter") for e in REC[k]))
chk("chords: one a bar, the plan's; N.C. in the stop bars", [b["chord"] for b in REC["bars"]] == [("N.C." if i in P.STOP_BARS else c) for i, c in enumerate(P.CHORD)])
voc_spans = [(n["on"], n["on"] + n["dur"]) for n in lead]
chk("235: no fill or intro tune over a sung note", not any(a < e["on"] + e["dur"] and e["on"] < b for e in REC["lgtr"] if not e["art"].startswith("solo") for a, b in voc_spans))
okf = all(4 <= len(f["notes"]) <= 6 and f["notes"][-1]["p"] % 12 in M.CH[M.chord_at(f["notes"][-1]["on"])][1] and
          ((18 == f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"] and f["gap"]["beats"] < 2.75) or (24 <= f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"] <= 36)) for f in RF["fills"])
chk("235/272: fills of 2-3 beats, or a beat and a half in a gap under 2.75 beats; 4-6 notes; ending on a chord tone", okf)
chk("235: the countermelody in the last chorus only", all(P.BAR0["Last Chorus"] * BAR <= e["on"] < (P.BAR0["Last Chorus"] + 16) * BAR for e in REC["counter"]))
chk("233: the bass has the root on beat 1 of every bar it plays", all(e["p"][0] % 12 == M.CH[REC["bars"][e["on"] // BAR]["chord"]][0] for e in REC["bass"] if e["on"] % BAR == 0))
bon = {e["on"] for e in REC["bass"]}; wb = float(np.mean([e["on"] in bon for e in REC["organ"]]))
chk(f"273: chord strikes with a bass note {wb:.0%} (floor 16%; bass cell in eighths)", wb >= 0.16)
parts = {}
for s, nb, b0, _ in REC["plan"]:
    a, z = b0 * BAR, (b0 + nb) * BAR
    parts[s] = sum(any(a <= e["on"] < z for e in REC[k]) for k in ("drums", "bass", "rgtr", "organ", "lgtr", "keys", "bvox", "counter", "lead"))
chk(f"238: intro at half the fullest or fewer; last chorus the fullest ({parts})", parts["Intro"] <= max(parts.values()) / 2 and parts["Last Chorus"] == max(parts.values()))
mf = mido.MidiFile(f"{OUT}/Stay Tuned v2 - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
voc = trk("Guide vocal")[0]
chk("demo guide vocal = the record's notes", [m.note for m in voc if m.type == "note_on" and m.velocity > 0] == ps)
for name, key in (("Lead guitar", "lgtr"), ("Organ (countermelody)", "counter"), ("Synth pulse", "keys")):
    t_ = trk(name); chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == sorted(p for e in REC[key] for p in e["p"]))
chk("demo tempo 132", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 132 for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Stay Tuned v2 - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Stay Tuned v2 - lead sheet.ly").read()
chk("credit line, key, tempo and length on the lead sheet", "Words and music: Jason Bryant" in src and "\\key a \\major" in src and "3:27" in src and "4 = 132" in src)
html = open(f"{OUT}/nashville.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7", "": "N.C."}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line, 114 bars, tempo", "Words and music: Jason Bryant" in html and "114 bars" in html and "♩ = 132" in html)
rr = Mn["rerun"]
chk("report: seed, calibration seed, code, order", str(rr["seed"]) in TR and str(rr["calibration_seed"]) in TR and rr["code_sha"] in TR and Mn["order_fp"] in TR)
chk("report: survivors and frozen orders of all three runs, each reproduced", all(f"{RD['1'][v]['survivors']} of 3,000" in TR and RD["1"][v]["order"] in TR and RD["1"][v]["reproduced"] for v in "ABC"))
chk("report: the three builds of 255 for Run B", all(RD["6"]["B"][k]["fp"] in TR for k in ("composite first", "shortlist pick", "judge first")))
chk("report: findings numbered from 286", "**286." in TR and "**285." not in TR)
chk("report: the readings the paper did not spell out are listed", "Readings the paper did not spell out" in TR)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
