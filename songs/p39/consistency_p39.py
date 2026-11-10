"""Song 39: every document against the song record: the demo, the engravings, the chart, the songbook, the readings and the report."""
import pickle, re, sys, mido
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p39"]
import melody_p39 as P
import lyric_p39 as L
M = P.M; H = "/home/claude/p39"; OUT = f"{H}/out"
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); Mn = pickle.load(open(f"{H}/melody_main.pkl", "rb")); pick = Mn["pick"]
T = pickle.load(open(f"{H}/readings.pkl", "rb")); RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
RF = pickle.load(open(f"{H}/riff_p39.pkl", "rb"))
SB = open(f"{H}/songbook.md").read(); TR = open(f"{H}/test_report.md").read()
lead = REC["lead"]; BAR = 48; ok = []; BEAT = 12
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
short = set(Mn["short"]); first_on_short = next(c for c in Mn["alive"] if c["fp"] in short)
chk("255: the record is the shortlist pick (the composite's first on the judge's upper half)", REC["fp"] == pick["fp"] == first_on_short["fp"])
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("90 bars, 3:20; every section a multiple of four but the last chorus's two-bar tag (228)", REC["nbars"] == 90 and round(REC["seconds"]) == 200 and all(nb % 4 == 0 or s == "Last Chorus" and nb == 18 for s, nb, _, _ in REC["plan"]))
chk("the lyric is the locked draft, every syllable sung", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
chk("no never-say word in the lyric (no party, colour, side or name)", not any(re.search(r"\b" + p + r"\b", " ".join(L.SUNG).lower()) for p in L.NEVER_PHRASES))
ps = [n["midi"] for n in lead]
chk("range A2 to E4 (the voice row)", min(ps) == 45 and max(ps) == 64)
sm = [n for n in lead if n["midi"] == 64]
chk("the summit (the writer's A, 216, 244): E4 four times on 'Vote', beat 1, over E, bars 21, 45, 69, 77", len(sm) == 4 and all(n["text"].lower().startswith("vote") and n["on"] % BAR == 0 and REC["bars"][n["on"] // BAR]["chord"] == "E" for n in sm) and [n["on"] // BAR + 1 for n in sm] == [21, 45, 69, 77])
tw = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 1]
chk("said twice: line 2's 'vote' on D4 over D", tw[0]["midi"] == 62 and REC["bars"][tw[0]["on"] // BAR]["chord"] == "D")
fx = [n for n in lead if n["text"].lower().startswith("fixed")]
chk("232: the title's stress on beat 1 or 3, held at least twice the median syllable", all(n["on"] % 24 == 0 for n in fx) and all(n["dur"] >= 12 for n in fx))
on = {n["on"] for n in pick["notes"]}
chk("215: no sung note a tritone from its chord's root on a beat or held", not any(P.tri(n["p"], M.chord_for(n, on)) and (n["on"] % BEAT == 0 or n["dur"] >= 12) for n in pick["notes"]))
chk("206: at most five note lengths in any 8 bars", all(len({n["dur"] for n in lead if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) <= 5 for b0 in range(REC["nbars"] - 7)))
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] < 3]
cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2" and n["line"] < 3]
lc = [(n["on"] - P.BAR0["Last Chorus"] * BAR, n["midi"]) for n in lead if n["sec"] == "Last Chorus" and n["line"] < 3]
chk("chorus 2 and the last chorus open as chorus 1 (lines 1-3, onsets and pitches)", cc1 == cc2 == lc)
tag = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 8]
chk("the tag 'Fixed by fall.': G#3-F#3-E3", [n["midi"] for n in tag] == [56, 54, 52])
chk("the duet: voice 2 sings line 2 alone, lines 3-4 a third under, lines 5-9 with voice 1; chorus 2 doubled", 
    sorted(e["on"] for e in REC["voice2"] if e["art"].startswith("two:")) == sorted(n["on"] for n in lead if n["sec"] == "Last Chorus" and n["line"] == 1)
    and all(e["p"][0] in [n["midi"] for n in lead if n["on"] == e["on"]] for e in REC["voice2"] if e["art"].startswith(("unison:", "double:")))
    and all(3 <= min(n["midi"] for n in lead if n["on"] == e["on"]) - e["p"][0] <= 4 for e in REC["voice2"] if e["art"].startswith("third:")))
chk("one hit on the last bar", any(e["on"] == (REC["nbars"] - 1) * BAR and 49 in e["p"] for e in REC["drums"]) and not any(e["on"] > (REC["nbars"] - 1) * BAR for k in ("drums", "bass", "rgtr", "piano", "lgtr", "voice2") for e in REC[k]))
chk("227: chorus opening unrelated to the verse's; median not below; floor above", not P.opening_rel(pick["notes"], "Chorus 1", "Verse 1")[0] and P.med(pick["notes"], "Chorus 1") >= P.med(pick["notes"], "Verse 1") and P.low(pick["notes"], "Chorus 1") > P.low(pick["notes"], "Verse 1"))
chk("208: bridge opening unrelated, above the verse, under the summit", not P.opening_rel(pick["notes"], "Bridge", "Verse 1")[0] and not P.opening_rel(pick["notes"], "Bridge", "Chorus 1")[0] and P.med(pick["notes"], "Bridge") > P.med(pick["notes"], "Verse 1") and P.top(pick["notes"], "Bridge") < 64)
chk("254: the pick above the judge's floor", pick["judge"]["combined"] >= -0.059)
chk("chords: one a bar, the plan's", [b["chord"] for b in REC["bars"]] == P.CHORD)
chk("Q12: shuffle sections swung in the record, the choruses straight", all(b["swing"] == (b["kind"] != "Chorus") for b in REC["bars"]))
voc_spans = [(n["on"], n["on"] + n["dur"]) for n in lead]
chk("235: no fill or intro tune over a sung note", not any(a < e["on"] + e["dur"] and e["on"] < b for e in REC["lgtr"] if not e["art"].startswith("solo") for a, b in voc_spans))
chk("235: fills 2-3 beats, 4-6 notes, start within a beat of the voice stopping, end on a chord tone", all(4 <= len(f["notes"]) <= 6 and 24 <= f["notes"][-1]["on"] + f["notes"][-1]["dur"] - f["notes"][0]["on"] <= 36 and 6 <= f["notes"][0]["on"] - f["gap"]["stop"] <= 12
    and f["notes"][-1]["p"] % 12 in M.CH[M.chord_at(f["notes"][-1]["on"])][1] for f in RF["fills"]))
chk("233: the bass has the root on beat 1 of every bar it plays", all(e["p"][0] % 12 == M.CH[REC["bars"][e["on"] // BAR]["chord"]][0] for e in REC["bass"] if e["on"] % BAR == 0))
chk("Q12: kick on every beat in the choruses; kick 1 and 3 in the verses", all(sum(1 for e in REC["drums"] if 36 in e["p"] and e["on"] // BAR == b and e["on"] % 12 == 0) >= 4 for b in range(P.BAR0["Chorus 1"], P.BAR0["Chorus 1"] + 7))
    and all(sorted(e["on"] % BAR for e in REC["drums"] if 36 in e["p"] and e["on"] // BAR == b) == [0, 24] for b in range(P.BAR0["Verse 1"], P.BAR0["Verse 1"] + 15)))
chk("238: intro at half the fullest or fewer; last chorus the fullest; no verse fuller than its chorus", T["238"]["Intro"] <= max(T["238"].values()) / 2 and T["238"]["Last Chorus"] == max(T["238"].values()) and T["238"]["Verse 1"] <= T["238"]["Chorus 1"] and T["238"]["Verse 2"] <= T["238"]["Chorus 2"])
# demo
mf = mido.MidiFile(f"{OUT}/Fixed by Fall - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
voc = [t for t in mf.tracks if any(m.type == "track_name" and m.name == "Guide vocal (clarinet - reed fallback)" for m in t)][0]
chk("demo guide vocal = the record's notes (voice two's solo line on its own track)", [m.note for m in voc if m.type == "note_on" and m.velocity > 0] == [n["midi"] for n in lead if n["voice"] != "two"])
for name, key in (("Lead guitar", "lgtr"), ("Guide vocal 2", "voice2"), ("Piano", "piano")):
    t_ = trk(name); chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == sorted(p for e in REC[key] for p in e["p"]))
chk("demo tempo 108", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 108 for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Fixed by Fall - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
# engravings
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
for f in ("Fixed by Fall - lead sheet.ly", "Fixed by Fall - parts.ly"):
    src = open(f"{OUT}/{f}").read(); chk(f"credit line, key, tempo and length in {f}", "Words and music: Jason Bryant" in src and "\\key e \\major" in src and "3:20" in src and "4 = 108" in src)
chk("lead sheet note: the summit bars are the record's", "(bars 21, 45, 69 and 77)" in open(f"{OUT}/Fixed by Fall - lead sheet.ly").read())
# chart
html = open(f"{OUT}/nashville.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line, 90 bars, tempo", "Words and music: Jason Bryant" in html and "90 bars" in html and "♩ = 108" in html)
# songbook
rows = re.findall(r"^\| (\d+)(?:–(\d+))? \| (.+?) \| (.+?) \| (\S+) – (\S+) \| (\S+) \((.*?)\) \|$", SB, re.M); bad = 0
CHN = {"A": "A", "E": "E", "F#m": "F♯m", "D": "D", "B": "B", "C#m": "C♯m"}
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
ENGINE = ["module", "fix 2", "fix 1", "gates", "a gate", "composite", "table b", "table d", "v10", "zeneng", "bits", "fingerprint", "calibration", "corpus", "rank of record", "discriminator", "judge", "axis", "shortlist", "kept window"]
chk("songbook: no engine terms or line labels ('candidate' is the song's word)", not any(w in SB.lower() for w in ENGINE) and not re.search(r"(Verse|Chorus|Bridge) \d:\d", SB))
chk("songbook: three references, each with a link", len(re.findall(r"^- \*\*.+\(\d{4}\)\.\*\* .+\]\(https?://", SB, re.M)) == 3)
chk("songbook: the summit bars are the record's", all(f"bar {b}, beat 1" in SB for b in (21, 45, 69, 77)))
chk("songbook: 90 bars, 3:20, the two feels and the last hit", "90 bars" in SB and "3:20" in SB and "shuffle" in SB and "straight" in SB and "bar 90" in SB)
# report
rr = Mn["rerun"]
chk("report: seed, calibration seed, code, order", str(rr["seed"]) in TR and str(rr["calibration_seed"]) in TR and rr["code_sha"] in TR and Mn["order_fp"] in TR)
chk("report: survivors, main and control", f"{Mn['survivors']} survivors" in TR and f"{T['run']['ctl']['survivors']} survivors" in TR)
chk("report: the three builds of 255", all(T["255"][k]["fp"] in TR for k in ("composite first", "shortlist pick", "judge first")))
chk("report: findings numbered from 269 to 273", all(f"**{n}." in TR for n in range(269, 274)))
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
