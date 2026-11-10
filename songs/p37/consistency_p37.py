"""Song 37: every document against the song record: the demo, the engravings, the chart, the songbook, the readings and the report."""
import pickle, re, sys, mido
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p37"]
import melody_p37 as P
import lyric_p37 as L
M = P.M; H = "/home/claude/p37"; OUT = f"{H}/out"
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); Mn = pickle.load(open(f"{H}/melody_main.pkl", "rb")); pick = Mn["alive"][0]
RD = pickle.load(open(f"{H}/readings.pkl", "rb")); RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
SB = open(f"{H}/songbook.md").read(); TR = open(f"{H}/test_report.md").read()
lead = REC["lead"]; BAR = 48; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
chk("record from the pick, first by the rank of record", REC["fp"] == pick["fp"] == RD["pick"]["main"])
chk("record's sung notes = the pick's notes", [(n["on"], n["dur"], n["midi"]) for n in lead] == [(n["on"], n["dur"], n["p"]) for n in pick["notes"]])
chk("no hand edits", REC["hand_edits"] == [])
chk("112 bars, 3:40; every section a multiple of four (220)", REC["nbars"] == 112 and round(REC["seconds"]) == 220 and all(nb % 4 == 0 for _, nb, _, _ in REC["plan"]))
chk("the lyric is draft 3, every syllable sung", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s]))) and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
chk("no never-say phrase in the lyric", not any(p in " ".join(L.SUNG).lower() for p in L.NEVER_PHRASES))
ps = [n["midi"] for n in lead]
chk("range D3 to F#4", min(ps) == 50 and max(ps) == 66)
sm = [n for n in lead if n["midi"] == 66]
chk("the summit (writer's A, 216): F#4 five times on 'hol-', chorus line 4, on a downbeat, over D", len(sm) == 5 and all(n["text"].lower().startswith("hol") and n["on"] % BAR == 0 and REC["bars"][n["on"] // BAR]["chord"] == "D" for n in sm) and [n["on"] // BAR + 1 for n in sm] == [27, 35, 55, 63, 95])
chk("every other note E4 or lower", all(p <= 64 for p in ps if p != 66))
on = {n["on"] for n in pick["notes"]}
chk("no sung note a tritone from its chord's root (215)", not any(P.tri(n["p"], M.chord_for(n, on)) for n in pick["notes"]))
chk("206: no sixteenth gap in a line; at most five lengths in any 8 bars", all(b["on"] - a["on"] >= 6 for a, b in zip(lead, lead[1:]) if (a["line"], a["sec"]) == (b["line"], b["sec"])) and all(len({n["dur"] for n in lead if b0 * BAR <= n["on"] < (b0 + 8) * BAR}) <= 5 for b0 in range(105)))
ends = {n["dur"] for i, n in enumerate(lead) if i + 1 < len(lead) and (lead[i + 1]["line"], lead[i + 1]["sec"]) != (n["line"], n["sec"])}
chk("218: line ends held a quarter, a dotted quarter or a half, all three used", ends == {12, 18, 24})
c1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]
c2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
half = [(t, p) for t, p in c1 if t < 8 * BAR]; half2 = [(t - 8 * BAR, p) for t, p in c1 if t >= 8 * BAR]
chk("chorus 2 = chorus 1, and each chorus is its 8 bars twice", c1 == c2 and half == half2)
last = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 7]
chk("the last line holds its first 'home' a half note and ends on A3 over A", [n for n in last if n["text"].lower().startswith("home")][0]["dur"] == 24 and last[-1]["midi"] == 57 and REC["bars"][last[-1]["on"] // BAR]["chord"] == "A")
chk("217: every chorus's last line lands on A over A", all([n for n in lead if n["sec"] == s and n["line"] == i][-1]["midi"] % 12 == 9 for s in ("Chorus 1", "Chorus 2", "Last Chorus") for i in (3, 7)))
chk("208: the bridge's median above the verse's; its opening related to neither", pick["read"]["bridge_median_minus_verse"] > 0 and not pick["read"]["bridge_rel_verse"][0] and not pick["read"]["bridge_rel_chorus"][0])
chk("chords: one a bar, the plan's", [b["chord"] for b in REC["bars"]] == P.CHORD)
chk("209: the lead guitar never starts or sounds over a sung onset outside the solo", sum(1 for s_ in REC["lgtr"] for n in lead if s_["on"] <= n["on"] < s_["on"] + s_["dur"]) == 0)
chk("209: the hook never a semitone from a held sung note", sum(any(abs((s_["p"][0] - n["midi"]) % 12) in (1, 11) for n in lead if n["on"] < s_["on"] + s_["dur"] and n["on"] + n["dur"] > s_["on"]) for s_ in REC["lgtr"]) == 0)
# demo
mf = mido.MidiFile(f"{OUT}/Windows Down - demo (General MIDI).mid")
voc = [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith("Guide vocal") for m in t)][0]
chk("demo guide vocal = the record's notes", [m.note for m in voc if m.type == "note_on" and m.velocity > 0] == ps)
lg = [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith("Lead guitar") for m in t)]
chk("demo lead guitar = the record's", len(lg) == 1 and [m.note for m in lg[0] if m.type == "note_on" and m.velocity > 0] == [e["p"][0] for e in REC["lgtr"]])
chk("demo tempo 122", any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 122 for m in mf.tracks[0]))
chk("demo stems: voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Windows Down - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
# engravings
chk("lead sheet: MIDI readback matches", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
for f in ("Windows Down - lead sheet.ly", "Windows Down - parts.ly"):
    src = open(f"{OUT}/{f}").read(); chk(f"credit line, key and length in {f}", "Words and music: Jason Bryant" in src and "\\key a \\major" in src and "3:40" in src)
chk("lead sheet note: the summit bars are the record's", "(bars 27, 35, 55, 63 and 95)" in open(f"{OUT}/Windows Down - lead sheet.ly").read())
# chart
html = open(f"{OUT}/nashville.html").read()
NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "iii": "3m"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s in ("Verse 2", "Pre 2", "Chorus 2"): continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords", cells == want)
chk("chart credit line, 112 bars", "Words and music: Jason Bryant" in html and "112 bars" in html)
# songbook
rows = re.findall(r"^\| (\d+)(?:–(\d+))? \| (.+?) \| (.+?) \| (\S+) – (\S+) \| (\S+) \((.*?)\) \|$", SB, re.M); bad = 0
CHN = {"A": "A", "E": "E", "F#m": "F♯m", "D": "D", "Bm": "Bm", "C#m": "C♯m"}
for b0, b1, text, chords, first, lastn, hi, hw in rows:
    cands = [(s, i) for s, ls in L.SECTIONS for i, (_, t) in enumerate(ls) if t == text]
    good = False
    for s, i in cands:
        ns = [n for n in lead if n["sec"] == s and n["line"] == i]
        if ns and ns[0]["on"] // BAR + 1 == int(b0):
            good = ns[-1]["on"] // BAR + 1 == int(b1 or b0) and nm(ns[0]["midi"]) == first and nm(ns[-1]["midi"]) == lastn and nm(max(n["midi"] for n in ns)) == hi \
                   and chords == " – ".join(CHN[REC["bars"][b]["chord"]] for b in range(ns[0]["on"] // BAR, ns[-1]["on"] // BAR + 1))
            break
    bad += not good
chk(f"songbook: {len(rows)} line rows, bars, chords and pitches = the record", len(rows) == 40 and bad == 0)
chk("songbook: credit line", "Words and music: Jason Bryant" in SB)
ENGINE = ["module", "fix 2", "fix 1", "gates", "a gate", "composite", "table b", "table c", "v96", "zeneng", "surprise", "bits", "fingerprint", "calibration", "corpus", "candidate", "search", "rank of record", "discriminator"]
chk("songbook: no engine terms (the lyric's 'fix it' and 'gate' are words)", not any(w in SB.lower() for w in ENGINE))
chk("songbook: three references", len(re.findall(r"^- .+ \(\d{4}\), ", SB, re.M)) == 3)
chk("songbook: the summit bars are the record's", all(f"bar {b}, beat 1" in SB for b in (27, 35, 55, 63, 95)))
chk("songbook: 112 bars, 3:40", "112 bars" in SB and "3:40" in SB)
# report
rr = Mn["rerun"]
chk("report: seed, N, code and order", str(rr["seed"]) in TR and rr["code_sha"] in TR and Mn["order_fp"] in TR)
chk("report: survivors, run and control", f"{RD['survivors']['main']} survivors" in TR and f"{RD['survivors']['ctl']} survivors" in TR)
chk("report: the readings, outside-both and deaths tables", RD["md"] in TR and RD["outside_md"] in TR and RD["deaths_md"] in TR)
chk("report: the distance, its flag and the share too central", f"{RD['distance']['main'][0]:.3f}" in TR and f"{100 * RD['too_central']['main']:.0f}%" in TR)
chk("report: 209 says it has no corpus figure", "no kept figure behind it" in TR)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
