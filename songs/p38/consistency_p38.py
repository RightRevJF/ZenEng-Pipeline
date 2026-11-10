"""Song 38: every document against the song record: the demo, the engravings, the chart, the songbook, the readings and the report."""
import pickle, re, sys, mido
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p38"]
import melody_p38 as P
import lyric_p38 as L
M = P.M; H = "/home/claude/p38"; OUT = f"{H}/out"
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); Mn = pickle.load(open(f"{H}/melody_main.pkl", "rb")); pick = Mn["pick"]
T = pickle.load(open(f"{H}/readings.pkl", "rb")); RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
RF = pickle.load(open(f"{H}/riff_p38.pkl", "rb"))
SB = open(f"{H}/songbook.md").read(); TR = open(f"{H}/test_report.md").read()
lead = REC["lead"]; BAR = 48; ok = []; BEAT = 12
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
short = set(Mn["short"]); first_on_short = next(c for c in Mn["alive"] if c["fp"] in short)
chk("255: the record is the shortlist pick (the composite's first on the judge's upper half)", REC["fp"] == pick["fp"] == first_on_short["fp"])
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("114 bars, 3:27; every section a multiple of four but the last chorus's two-bar extension (228)", REC["nbars"] == 114 and round(REC["seconds"]) == 207 and all(nb % 4 == 0 or s == "Last Chorus" and nb == 18 for s, nb, _, _ in REC["plan"]))
chk("the lyric is draft 5, every syllable sung", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
chk("no never-say phrase in the lyric; no party or name", not any(p in " ".join(L.SUNG).lower() for p in L.NEVER_PHRASES))
ps = [n["midi"] for n in lead]
chk("range C#3 to A4 (inside the voice row A2-A4)", min(ps) == 49 and max(ps) == 69)
sm = [n for n in lead if n["midi"] == 69]
chk("the summit (the writer's A, 216, 244): A4 six times on 'tuned', beat 1, over A, bars 21, 29, 49, 57, 89, 97", len(sm) == 6 and all(n["text"].lower().startswith("tuned") and n["on"] % BAR == 0 and REC["bars"][n["on"] // BAR]["chord"] == "A" for n in sm) and [n["on"] // BAR + 1 for n in sm] == [21, 29, 49, 57, 89, 97])
chk("232: the title's stress held three beats, at least twice the median syllable", all(n["dur"] == 36 for n in sm))
c1 = [n for n in lead if n["sec"] == "Chorus 1"]
twice = [n for n in c1 if n["line"] == 1]
chk("said twice: 'tuned' in line 2 on G4 over G", twice[1]["midi"] == 67 and REC["bars"][twice[1]["on"] // BAR]["chord"] == "G")
on = {n["on"] for n in pick["notes"]}
chk("215: no sung note a tritone from its chord's root on a beat or held", not any(P.tri(n["p"], M.chord_for(n, on)) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in pick["notes"]))
chk("206: at most five note lengths in any 8 bars", all(len({n["dur"] for n in lead if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) <= 5 for b0 in range(REC["nbars"] - 7)))
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]
cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1 (pitches and onsets)", cc1 == cc2)
lc = [(n["on"] - P.BAR0["Last Chorus"] * BAR, n["midi"]) for n in lead if n["sec"] == "Last Chorus" and n["line"] < 6]
c6 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] < 6]
chk("228: the last chorus opens as chorus 1 (lines 1-6, onsets and pitches)", lc == c6)
tag = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 8]
chk("'Turn it off.': E4-C#4-A3 in the stop bars, nothing else sounding", [n["midi"] for n in tag] == [64, 61, 57] and all(n["on"] // BAR in REC["stop_bars"] for n in tag)
    and not any(e["on"] // BAR in REC["stop_bars"] or (e["on"] < REC["stop_bars"][0] * BAR < e["on"] + e["dur"] and e["art"] != "ring") for k in ("drums", "bass", "rgtr", "organ", "lgtr", "keys", "bvox", "counter") for e in REC[k]))
chk("one hit on the outro's first beat", any(e["on"] == P.BAR0["Outro"] * BAR and 49 in e["p"] for e in REC["drums"]) and not any(e["on"] > P.BAR0["Outro"] * BAR for k in ("drums", "bass", "rgtr", "organ", "lgtr", "keys", "bvox", "counter") for e in REC[k]))
chk("227: chorus opening unrelated to the verse's; median not below; floor above", not P.opening_rel(pick["notes"], "Chorus 1", "Verse 1")[0] and P.med(pick["notes"], "Chorus 1") >= P.med(pick["notes"], "Verse 1") and P.low(pick["notes"], "Chorus 1") > P.low(pick["notes"], "Verse 1"))
chk("208: bridge opening unrelated, above the verse, under the summit", not P.opening_rel(pick["notes"], "Bridge", "Verse 1")[0] and not P.opening_rel(pick["notes"], "Bridge", "Chorus 1")[0] and P.med(pick["notes"], "Bridge") > P.med(pick["notes"], "Verse 1") and P.top(pick["notes"], "Bridge") < 69)
er, _ = P.era_read(pick["notes"])
chk("242: the pick inside CLASSIC's five bands (median over V1, Ch1, Bridge)", all(P.ERA[k][0] <= er[k] <= P.ERA[k][2] for k in P.ERA_K))
chk("254: the pick above the judge's floor", pick["judge"]["combined"] >= -0.059)
chk("chords: one a bar, the plan's; N.C. in the stop bars", [b["chord"] for b in REC["bars"]] == [("N.C." if i in P.STOP_BARS else c) for i, c in enumerate(P.CHORD)])
voc_spans = [(n["on"], n["on"] + n["dur"]) for n in lead]
chk("235: no fill or intro tune over a sung note", not any(a < e["on"] + e["dur"] and e["on"] < b for e in REC["lgtr"] if not e["art"].startswith("solo") for a, b in voc_spans))
chk("235: fills 2-3 beats, 4-6 notes, start within a beat of the voice stopping, end on a chord tone", all(4 <= len(f["notes"]) <= 6 and 24 <= f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"] <= 36 and 6 <= f["notes"][0]["on"] - f["gap"]["stop"] <= 12
    and f["notes"][-1]["p"] % 12 in M.CH[M.chord_at(f["notes"][-1]["on"])][1] for f in RF["fills"]))
chk("235: the countermelody in the last chorus only, under half at unison or octave", all(P.BAR0["Last Chorus"] * BAR <= e["on"] < (P.BAR0["Last Chorus"] + 16) * BAR for e in REC["counter"]) and RF["counter_check"]["share"] < 0.5)
chk("233: the bass has the root on beat 1 of every bar it plays", all(e["p"][0] % 12 == M.CH[REC["bars"][e["on"] // BAR]["chord"]][0] for e in REC["bass"] if e["on"] % BAR == 0))
chk("Q12: four on the floor in the choruses, a rock beat in the verses", all(sum(1 for e in REC["drums"] if 36 in e["p"] and e["on"] // BAR == b and e["on"] % 12 == 0) >= 4 for b in range(P.BAR0["Chorus 1"], P.BAR0["Chorus 1"] + 15))
    and all(sorted(e["on"] % BAR for e in REC["drums"] if 36 in e["p"] and e["on"] // BAR == b) == [0, 24] for b in range(P.BAR0["Verse 1"], P.BAR0["Verse 1"] + 7)))
chk("238: intro at half the fullest or fewer; last chorus the fullest", T["238"]["Intro"] <= max(T["238"].values()) / 2 and T["238"]["Last Chorus"] == max(T["238"].values()))
# demo
mf = mido.MidiFile(f"{OUT}/Stay Tuned - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
voc = trk("Guide vocal")[0]
chk("demo guide vocal = the record's notes", [m.note for m in voc if m.type == "note_on" and m.velocity > 0] == ps)
for name, key in (("Lead guitar", "lgtr"), ("Organ (countermelody)", "counter"), ("Synth pulse", "keys")):
    t_ = trk(name); chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == sorted(p for e in REC[key] for p in e["p"]))
chk("demo tempo 132", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 132 for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Stay Tuned - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
# engravings
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
for f in ("Stay Tuned - lead sheet.ly", "Stay Tuned - parts.ly"):
    src = open(f"{OUT}/{f}").read(); chk(f"credit line, key, tempo and length in {f}", "Words and music: Jason Bryant" in src and "\\key a \\major" in src and "3:27" in src and "4 = 132" in src)
chk("lead sheet note: the summit bars are the record's", "(bars 21, 29, 49, 57, 89 and 97)" in open(f"{OUT}/Stay Tuned - lead sheet.ly").read())
# chart
html = open(f"{OUT}/nashville.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7", "": "N.C."}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line, 114 bars, tempo", "Words and music: Jason Bryant" in html and "114 bars" in html and "♩ = 132" in html)
# songbook
rows = re.findall(r"^\| (\d+)(?:–(\d+))? \| (.+?) \| (.+?) \| (\S+) – (\S+) \| (\S+) \((.*?)\) \|$", SB, re.M); bad = 0
CHN = {"A": "A", "E": "E", "F#m": "F♯m", "D": "D", "Bm": "Bm", "G": "G", "N.C.": "N.C."}
for b0, b1, text, chords, first, lastn, hi, hw in rows:
    cands = [(s, i) for s, ls in L.SECTIONS for i, (_, t) in enumerate(ls) if t == text]; good = False
    for s, i in cands:
        ns = [n for n in lead if n["sec"] == s and n["line"] == i]
        if ns and ns[0]["on"] // BAR + 1 == int(b0):
            good = ns[-1]["on"] // BAR + 1 == int(b1 or b0) and nm(ns[0]["midi"]) == first and nm(ns[-1]["midi"]) == lastn and nm(max(n["midi"] for n in ns)) == hi \
                   and chords == " – ".join(CHN[REC["bars"][b]["chord"]] for b in range(ns[0]["on"] // BAR, ns[-1]["on"] // BAR + 1))
            break
    bad += not good
chk(f"songbook: {len(rows)} line rows, bars, chords and pitches = the record", len(rows) == sum(len(ls) for _, ls in L.SECTIONS) and bad == 0)
chk("songbook: credit line", "Words and music: Jason Bryant" in SB)
ENGINE = ["module", "fix 2", "fix 1", "gates", "a gate", "composite", "table b", "table d", "v10", "zeneng", "bits", "fingerprint", "calibration", "corpus", "candidate", "rank of record", "discriminator", "judge", "axis", "shortlist", "kept window"]
chk("songbook: no engine terms or line labels", not any(w in SB.lower() for w in ENGINE) and not re.search(r"[A-Za-z] \d:\d", SB))
chk("songbook: three references, each with a link", len(re.findall(r"^- \*\*.+\(\d{4}\)\.\*\* .+\]\(https?://", SB, re.M)) == 3)
chk("songbook: the summit bars are the record's", all(f"bar {b}, beat 1" in SB for b in (21, 29, 49, 57, 89, 97)))
chk("songbook: 114 bars, 3:27, the stop bars and the last hit", "114 bars" in SB and "3:27" in SB and "bars 105–106" in SB and "bar 107" in SB)
# report
rr = Mn["rerun"]
chk("report: seed, calibration seed, code, order", str(rr["seed"]) in TR and str(rr["calibration_seed"]) in TR and rr["code_sha"] in TR and Mn["order_fp"] in TR)
chk("report: survivors, main and control", f"{Mn['survivors']} survivors" in TR and f"{T['run']['ctl']['survivors']} survivors" in TR)
chk("report: the three builds of 255", all(T["255"][k]["fp"] in TR for k in ("composite first", "shortlist pick", "judge first")))
chk("report: findings numbered from 257 to 268", all(f"**{n}." in TR for n in range(257, 269)))
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
