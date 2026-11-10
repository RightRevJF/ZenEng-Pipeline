"""Every document against the song record: the demo, the engravings, the chart, the songbook, the readings and the report."""
import pickle, re, sys, mido, json, subprocess
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p36", "/home/claude/carol"]
import melody_p36 as M
REC = pickle.load(open("/home/claude/p36/song_record.pkl", "rb")); OUT = "/home/claude/p36/out"
RD = pickle.load(open("/home/claude/p36/readings.pkl", "rb")); MR = pickle.load(open("/home/claude/p36/melody_main.pkl", "rb"))
VER2 = REC.get("version") == 2
if VER2:
    R2 = pickle.load(open("/home/claude/p36/melody_v2.pkl", "rb")); RD2 = pickle.load(open("/home/claude/p36/readings_v2.pkl", "rb"))
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
SB = open("/home/claude/p36/songbook.md").read(); TR = open("/home/claude/p36/test_report.md").read() if len(sys.argv) else ""
lead = REC["lead"]; BAR = 48; ok = []
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
pick = R2["pick"] if VER2 else MR["alive"][0]
chk("record from the frozen pick (#1 of the ranked survivors)", REC["fp"] == pick["fp"] == (RD2["fp"] if VER2 else RD["pick_fp"]))
if VER2:
    chk("v2: every section but the bridge and the three changed lines = version 1's", [(n["on"], n["p"]) for n in pick["notes"] if n["sec"] != "Bridge" and n["line"] not in ("Chorus 1:5", "Chorus 2:5", "Verse 2:2", "Pre 2:1")] == [(n["on"], n["p"]) for n in MR["alive"][0]["notes"] if n["sec"] != "Bridge" and n["line"] not in ("Chorus 1:5", "Chorus 2:5", "Verse 2:2", "Pre 2:1")])
    br = [n for n in lead if n["sec"] == "Bridge"]
    chk("v2: the bridge has no sixteenth gap and ends on a held B-flat 4", all(b["on"] - a["on"] >= 6 for a, b in zip(br, br[1:]) if a["line"] == b["line"]) and br[-1]["midi"] == 70)
    syn = REC["synth"]; held_bad = 0
    for s_ in syn:
        h = [n["midi"] for n in lead if n["on"] < s_["on"] + s_["dur"] and n["on"] + n["dur"] > s_["on"]]
        held_bad += any(abs((s_["p"][0] - x) % 12) in (1, 11) for x in h)
    chk("v2: the synth riff (31 statements) never a semitone from the sung note", len(syn) == 5 * 31 and held_bad == 0)
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("88 bars, 2:59", REC["nbars"] == 88 and round(REC["seconds"]) == 179)
chk("form bars sum to the plan", sum(nb for _, nb, _, _ in REC["plan"]) == 88)
ps = [n["midi"] for n in lead]
chk("range B-flat 3 to D5", min(ps) == 58 and max(ps) == 74)
chk("the D5 once (165), in the last chorus, bar 82", ps.count(74) == 1 and [n for n in lead if n["midi"] == 74][0]["on"] // BAR == 81)
chk("every other note C5 or lower", all(p <= 72 for p in ps if p != 74))
c1 = [(n["on"] - M.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]
c2 = [(n["on"] - M.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1", c1 == c2)
chk("each chorus's top not below its verse's (133)", not M.register_bad(pick["notes"]))
chk("the song ends on E-flat", sorted(lead, key=lambda n: n["on"])[-1]["midi"] % 12 == 3)
chk("chords: one a bar, the plan's", [b["chord"] for b in REC["bars"]] == M.CHORD)
# demo
SUF = " (version 2)" if REC.get("version") == 2 else ""
mf = mido.MidiFile(f"{OUT}/Dance Anyway{SUF} - demo (General MIDI).mid")
voc = [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith("Guide vocal") for m in t)][0]
vn = [m.note for m in voc if m.type == "note_on" and m.velocity > 0]
chk("demo guide vocal = the record's notes", vn == ps)
chk("demo tempo 118", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 118 for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Dance Anyway{SUF} - demo (GarageBand).mid")
chk("GarageBand MIDI: same notes, ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
# engravings
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
for f in (f"Dance Anyway{SUF} - lead sheet.ly", f"Dance Anyway{SUF} - parts.ly"):
    chk(f"credit line in {f}", "Words and music: Jason Bryant" in open(f"{OUT}/{f}").read())
# the chart
html = open(f"{OUT}/nashville.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "bVII": "♭7", "ii": "2m"}
cells = re.findall(r"<td>([^<]+)</td>", html)
want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line", "Words and music: Jason Bryant" in html)
# songbook: every table row read from the record
rows = re.findall(r"^\| (\d+) \| (.+?) \| (.+?) \| (\S+) – (\S+) \| (\S+) \((.*?)\) \|$", SB, re.M)
bad = 0
import lyric as L
if VER2: import lyric_v2 as L
for bar, text, chords, first, last, hi, hw in rows:
    sec = next(s for s, ls in L.SECTIONS if any(t == text for _, t in ls) and any(n["sec"] == s and n["on"] // BAR + 1 == int(bar) and n["line"] == [t for _, t in ls].index(text) for n in lead))
    i = [t for _, t in dict(L.SECTIONS)[sec]].index(text); ns = [n for n in lead if n["sec"] == sec and n["line"] == i]
    NMS = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
    if not (ns[0]["on"] // BAR + 1 == int(bar) and nm(ns[0]["midi"]) == first and nm(ns[-1]["midi"]) == last and nm(max(n["midi"] for n in ns)) == hi): bad += 1
chk(f"songbook: {len(rows)} line rows, bars and pitches = the record", len(rows) == 40 and bad == 0)
chk("songbook: credit line", "Words and music: Jason Bryant" in SB)
ENGINE = ["module", "fix ", "gate", "composite", "table b", "table c", "v91", "zeneng", "surprise", "bits", "fingerprint", "calibration", "corpus", "candidate", "search"]
chk("songbook: no engine terms", not any(w in SB.lower() for w in ENGINE))
chk("songbook: three references", len(re.findall(r"^- .+\(\d{4}\), \d+ BPM", SB, re.M)) == 3)
chk("songbook: the D5 bar is the record's", "bar 82" in SB)
# the report against the readings
if TR and VER2:
    chk("report v2: the song's pitch surprise", f"{RD2['pitch']:.2f}" in TR)
    chk("report v2: the bridge search's survivors and order", str(RD2["survivors"]) in TR and RD2["order"] in TR)
if TR:
    chk("report: the pick's pitch surprise", f"{RD['pick']['pitch_bits']:.2f}" in TR)
    chk("report: the control's pitch surprise", f"{RD['ctl']['pitch_bits']:.2f}" in TR)
    chk("report: survivors and frozen order", str(MR["survivors"]) in TR and MR["order_fp"] in TR)
    chk("report: exact bar repetition", f"{100 * RD['pick']['exact']:.0f}%" in TR)
    chk("report: stock design at 8 bars", f"{100 * RD['pick']['designs']['stock8']:.0f}%" in TR)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
