"""Version 3: every document against the song record: the demo, the engravings, the chart, the songbook, the readings and the report."""
import pickle, re, sys, mido
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p36", "/home/claude/carol"]
import melody_v3_p36 as V
import lyric_v2 as L
M = V.M; H = "/home/claude/p36"; OUT = f"{H}/out"; SUF = " (version 3)"
REC = pickle.load(open(f"{H}/song_record_v3.pkl", "rb")); Mn = pickle.load(open(f"{H}/melody_v3_main.pkl", "rb")); pick = Mn["alive"][0]
R = pickle.load(open(f"{H}/readings_v3.pkl", "rb")); T = pickle.load(open(f"{H}/tests_v3.pkl", "rb"))
RB = pickle.load(open(f"{OUT}/readback_v3.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report_v3.pkl", "rb"))
SB = open(f"{H}/songbook_v3.md").read(); TR = open(f"{H}/test_report.md").read(); TR3 = TR[TR.index("## Version 3"):]
lead = REC["lead"]; BAR = 48; ok = []
NMS = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
chk("record from the pick, first by the rank of record", REC["fp"] == pick["fp"] == R["pick"] and REC["version"] == 3)
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("99 bars, 3:21 (201's form)", REC["nbars"] == 99 and round(REC["seconds"]) == 201 and sum(nb for _, nb, _, _ in REC["plan"]) == 99)
chk("spans: verse 2-3-2-3, chorus lines 4 and 8 three bars, bridge line 2 three bars", REC["spans"] == {"Verse": [2, 3, 2, 3], "Pre": [2, 2], "Chorus": [2, 2, 2, 3, 2, 2, 2, 3], "Bridge": [2, 3, 2, 2]})
chk("the lyric is draft 5, every syllable sung", all(len(REC["text"][s][i]) == len(V.LINES[s][i]) for s in V.SUNG for i in range(len(V.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in V.SUNG for i in range(len(V.LINES[s]))))
ps = [n["midi"] for n in lead]
chk("range B-flat 3 to D5", min(ps) == 58 and max(ps) == 74)
sm = [n for n in lead if n["midi"] == 74]
chk("the summit (writer's A): D5 three times, chorus line 6's last stressed word, on a beat, over B-flat", len(sm) == 3 and all(n["line"] == 5 and n["sec"] in ("Chorus 1", "Chorus 2", "Last Chorus") and n["on"] % 12 == 0 and REC["bars"][n["on"] // BAR]["chord"] == "Bb" for n in sm) and [n["on"] // BAR + 1 for n in sm] == [31, 63, 90])
chk("every other note C5 or lower", all(p <= 72 for p in ps if p != 74))
chk("206: no sixteenth gap in a line; at most five lengths in any 8 bars", all(b["on"] - a["on"] >= 6 for a, b in zip(lead, lead[1:]) if a["line"] == b["line"] and a["sec"] == b["sec"]) and T["206"]["max_lengths_any_span"] <= 5)
ends = {n["dur"] for i, n in enumerate(lead) if i + 1 == len(lead) or (lead[i + 1]["line"], lead[i + 1]["sec"]) != (n["line"], n["sec"])}
chk("206: line ends held one of two lengths (a half, a dotted quarter)", ends <= {24, 18})
c1 = [(n["on"] - V.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]
c2 = [(n["on"] - V.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1", c1 == c2)
chk("each chorus's top not below its verse's (133)", not V.register_bad(pick["notes"]))
chk("208: the bridge's median above the verse's; its opening related to neither", R["rows"][14]["pick"] > 0 and not pick["read"]["bridge_rel_verse"][0] and not pick["read"]["bridge_rel_chorus"][0])
chk("no sung note a tritone from its chord's root", T["200"]["tritone_root_pick"] == 0)
chk("the song ends on E-flat", sorted(lead, key=lambda n: n["on"])[-1]["midi"] % 12 == 3)
chk("chords: one a bar, the plan's", [b["chord"] for b in REC["bars"]] == V.CHORD)
sung_on = sorted(n["on"] for n in lead)
chk("209: the synth never sounds over a sung onset", T["209"]["over_sung_onset"] == 0 and T["209"]["on_sung_onset"] == 0)
held_bad = sum(any(abs((s_["p"][0] - n["midi"]) % 12) in (1, 11) for n in lead if n["on"] < s_["on"] + s_["dur"] and n["on"] + n["dur"] > s_["on"]) for s_ in REC["synth"])
chk("209: the synth never a semitone from a sung note", held_bad == 0)
chk("209: in the intro, the choruses and the outro", set(T["209"]["where"]) == {"intro", "outro", "Chorus 1", "Chorus 2", "Last Chorus"})
# demo
mf = mido.MidiFile(f"{OUT}/Dance Anyway{SUF} - demo (General MIDI).mid")
voc = [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith("Guide vocal") for m in t)][0]
chk("demo guide vocal = the record's notes", [m.note for m in voc if m.type == "note_on" and m.velocity > 0] == ps)
syn = [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith("Synth (instrumental hook)") for m in t)]
chk("demo synth track named for the instrumental hook, its notes = the record's", len(syn) == 1 and [m.note for m in syn[0] if m.type == "note_on" and m.velocity > 0] == [e["p"][0] for e in REC["synth"]])
chk("demo tempo 118", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 118 for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Dance Anyway{SUF} - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
# engravings
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
for f in (f"Dance Anyway{SUF} - lead sheet.ly", f"Dance Anyway{SUF} - parts.ly"):
    src = open(f"{OUT}/{f}").read()
    chk(f"credit line and version label in {f}", "Words and music: Jason Bryant" in src and "(version 3)" in src and "3:21" in src)
# chart
html = open(f"{OUT}/nashville_v3.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "bVII": "♭7", "ii": "2m"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line and version label", "Words and music: Jason Bryant" in html and "(version 3)" in html and "99 bars" in html)
# songbook
rows = re.findall(r"^\| (\d+)(?:–(\d+))? \| (.+?) \| (.+?) \| (\S+) – (\S+) \| (\S+) \((.*?)\) \|$", SB, re.M); bad = 0
for b0, b1, text, chords, first, last, hi, hw in rows:
    sec = next(s for s, ls in L.SECTIONS if any(t == text for _, t in ls) and any(n["sec"] == s and n["on"] // BAR + 1 == int(b0) and n["line"] == [t for _, t in ls].index(text) for n in lead))
    i = [t for _, t in dict(L.SECTIONS)[sec]].index(text); ns = [n for n in lead if n["sec"] == sec and n["line"] == i]
    good = ns[0]["on"] // BAR + 1 == int(b0) and (ns[-1]["on"] // BAR + 1 == int(b1 or b0)) and nm(ns[0]["midi"]) == first and nm(ns[-1]["midi"]) == last and nm(max(n["midi"] for n in ns)) == hi
    good = good and chords == " – ".join({"Eb": "E♭", "Bb": "B♭", "Cm": "Cm", "Ab": "A♭", "Db": "D♭", "Fm": "Fm"}[REC["bars"][b]["chord"]] for b in range(ns[0]["on"] // BAR, ns[-1]["on"] // BAR + 1))
    bad += not good
chk(f"songbook: {len(rows)} line rows, bars, chords and pitches = the record", len(rows) == 40 and bad == 0)
chk("songbook: credit line and version label", "Words and music: Jason Bryant" in SB and "(version 3)" in SB)
ENGINE = ["module", "fix ", "gate", "composite", "table b", "table c", "v95", "zeneng", "surprise", "bits", "fingerprint", "calibration", "corpus", "candidate", "search", "rank of record"]
chk("songbook: no engine terms", not any(w in SB.lower() for w in ENGINE))
chk("songbook: three references", len(re.findall(r"^- .+\(\d{4}\), \d+ BPM", SB, re.M)) == 3)
chk("songbook: the summit bars are the record's", all(f"bar {b}, beat 2" in SB for b in (31, 63, 90)))
chk("songbook: 99 bars, 3:21", "99 bars" in SB and "3:21" in SB)
# the report against the runs
rr = Mn["rerun"]
chk("report v3: seed, N, code and order", str(rr["seed"]) in TR3 and rr["code_sha"] in TR3 and Mn["order_fp"] in TR3 and f"N {rr['N']}" in TR3)
chk("report v3: survivors, run and control", f"{Mn['survivors']} survivors" in TR3 and f"{R['ctl']['survivors']} survivors" in TR3)
chk("report v3: the readings table", R["md"] in TR3 and R["deaths_md"] in TR3)
chk("report v3: the distance and its flag", f"{R['distance'][0]:.3f}" in TR3 and R["distance"][1] in TR3)
chk("report v3: the composite called the rank of record", "rank of record" in TR3)
chk("report v3: 209 says it has no corpus figure", "no kept figure behind it" in TR3)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency_v3.pkl", "wb"))
