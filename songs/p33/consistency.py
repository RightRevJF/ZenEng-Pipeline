"""Document consistency check for 'Sadie' (a country-rock anthem: a baritone lead, a gang, a band; 4/4 at q = 124; A major; the drop in
bars 61-64; the songbook for musicians, with the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p33"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p33/song_record.pkl", "rb"))
O = "/home/claude/p33/out/Sadie - "
ly = open(O + "lead sheet.ly").read(); pt = open(O + "parts (band and gang).ly").read(); nv = open("/home/claude/p33/out/nashville.html").read()
sb = open("/home/claude/p33/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, bool(ok), d))
chk("title in all", all("Sadie" in d for d in (ly, pt, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, pt, nv, sb, docx)))
ENG = r"zeneng|\bengine\b|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|search|fingerprint|27\.22|register gate"
chk("songbook and chart for musicians: no engine terms", not re.search(ENG, sb.lower() + docx.lower() + nv.lower()), str(re.findall(ENG, sb.lower() + docx.lower() + nv.lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("4/4 at q = 124, A major, throughout", set(tsig) == {"4/4"} and set(tmp) == {124} and set(ks) == {"A"} and "\\tempo 4 = 124" in ly and "\\key a \\major" in ly and "♩ = 124" in sb and "♩ = 124" in nv)
chk("88 bars", "88 bars" in nv and "88 bars" in sb and REC["nbars"] == 88 and sum(p[1] for p in plan) == 88)
chk("length 2:50", "2:50" in nv and "2:50" in sb and round(REC["seconds"]) == 170 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
LYC = {"a1": "A", "d1": "D", "e1": "E", "fis1:m": "F#m", "b1:m": "Bm", "r1": "N.C."}
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
chk("chords: lead sheet = record", [LYC[c] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"1": "A", "4": "D", "5": "E", "6m": "F#m", "2m": "Bm", "N.C.": "N.C."}
cells = re.findall(r"<td>(6m|2m|N\.C\.|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == 88 and all(NUMK[c] == b for c, b in zip(cells, rec)), f"{len(cells)} bars")
SBC = {"A": "A", "D": "D", "E": "E", "F♯m": "F#m", "Bm": "Bm", "N.C.": "N.C."}
rows = re.findall(r"^\| ((?:(?:[A-G]♯?m?) · )+(?:[A-G]♯?m?)) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    bs = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add(tuple(bs[2 * i:2 * i + 2]) if s != "Drop" else tuple(bs))
lrows = [(a, l) for a, l in rows if l in want]
chk("chords: songbook rows = record", lrows and all(tuple(SBC[x] for x in a.split(" · ")) in want[l] for a, l in lrows), f"{len(lrows)} rows")
m = re.search(r'\\lyricsto "voc" \{ (.*?) \}\n', ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
chk("words: the voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG))))
uniq = list(dict.fromkeys(L.SUNG)); strip = lambda t: t.replace("’", "'").replace("*", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq), str([l for l in uniq if strip(l) not in strip(sb)][:2]))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: nothing from the list sung", not bad, str(bad))
lead = REC["lead"]; bno = lambda o: o // 8 + 1; chord_at = lambda o: REC["bars"][o // 8]["chord"]
top = [n for n in lead if n["midi"] >= 66]
chk("F#4 once, on NEV-er over F#m (bar 79)", [(n["syl"][0], bno(n["on"]), chord_at(n["on"])) for n in top] == [("never", 79, "F#m"), ("never", 79, "F#m")])
cell = [n["midi"] for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
chk("the title cell: E4 C#4 E4 C#4 A3 B3 A3 G#3 A3 B3 B3 B3; choruses 2-4 the same", cell == [64, 61, 64, 61, 57, 59, 57, 56, 57, 59, 59, 59] and all([n["midi"] for n in lead if n["sec"] == s and n["line"] == 0] == cell for s in ("Chorus 2", "Chorus 3", "Chorus 4")))
up = [n for n in lead if n["sec"] == "Drop"]
chk("the drop: it's UP, G#3 to B3 on beat 3 of bar 61", [(n["midi"], bno(n["on"]), n["on"] % 8) for n in up] == [(56, 61, 2), (59, 61, 4)])
SIL = [b["start"] for b in REC["bars"] if b.get("silence")]
who = {k: [e for e in REC[k] if any(s <= e["on"] < s + 8 for s in SIL)] for k in ("drums", "bass", "rhy", "ac", "organ", "riff", "gang")}
chk("fix 108: who plays in bars 62-64 = the kick only, as the songbook, chart and parts say", [b // 8 + 1 for b in SIL] == [62, 63, 64] and all(not v for k, v in who.items() if k != "drums")
    and {e["p"][0] for e in who["drums"]} == {36} and "heartbeat" in sb and "N.C." in nv and "only the heartbeat" in pt and not [n for n in lead if any(s <= n["on"] < s + 8 for s in SIL)])
ga = REC["gang"]
chk("the gang: 'Sadie! Sadie!' in choruses 1-3, all of chorus 4, two outro shouts", all(sum(1 for e in ga if REC["bars"][e["on"] // 8]["sec"] == s) == 4 for s in ("Chorus 1", "Chorus 2", "Chorus 3"))
    and sum(1 for e in ga if REC["bars"][e["on"] // 8]["sec"] == "Chorus 4") == len([n for n in lead if n["sec"] == "Chorus 4"])
    and sorted({bno(e["on"]) for e in ga if REC["bars"][e["on"] // 8]["sec"] == "Outro"}) == [83, 87])
ans = REC["answers"]
chk("the answers (fix 101): figures fitted to the room; bars 10, 12, 16 (two notes), 14 none; 34 (three), 36, 38, 40 (two)", [(bno(a["on"]), len(a["figure"])) for a in ans] == [(10, 2), (12, 2), (14, 0), (16, 2), (34, 3), (36, 2), (38, 2), (40, 2)]
    and all(a["room"] >= len(a["figure"]) for a in ans) and "bars 10, 12, 16" in sb)
rf = [e for e in REC["riff"] if e.get("art") == "riff" and e["on"] < 8]
chk("the riff (fix 22): bar 1 = the title cell's first six notes, an octave up", [e["p"][0] - 12 for e in rf][:6] == cell[:6])
gate = REC["meas"]["tops"]
chk("the register plan: verse < pre <= chorus < last line; bridge <= chorus", max(gate["Verse 1"], gate["Verse 2"]) < gate["Pre 1"] <= gate["Chorus 1"] < 66 and gate["Bridge"] <= gate["Chorus 1"])
chk("a breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 1 for a, b in zip(lead, lead[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
PR = pickle.load(open("/home/claude/p33/out/parts_report.pkl", "rb"))
chk("parts: every part reads back; drum hits = the demo's", all(PR["readback"].values()), str(PR["readback"]))
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
chk("MIDI notes per track = the record", tn.get("Drums") == cnt("drums") and tn.get("Bass") == cnt("bass") and tn.get("Rhythm guitar") == cnt("rhy") and tn.get("Gang (choir)") == cnt("gang")
    and tn.get("Lead guitar (riff and answers)") == cnt("riff") and tn.get("Guide vocal (trombone)") == len(lead), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn))
DR = pickle.load(open("/home/claude/p33/out/demo_report.pkl", "rb")); E_ = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("demo: stems >= +3 dB; each chorus above its verse; the last chorus the top; the drop below its neighbours", DR["stems_db"] >= 3 and E_["Chorus 1"] > E_["Verse 1"] and E_["Chorus 2"] > E_["Verse 2"]
    and E_["Chorus 4"] == max(E_.values()) and E_["Drop"] < min(E_["Bridge"], E_["Chorus 3"]), f"{DR['stems_db']:+.1f} dB")
chk("songbook carries the production notes and the one-sheet", all(h_ in sb for h_ in ("## Lyric sheet", "## Producer one-sheet", "## Production brief", "## Session notes", "## Score and parts")) and "Producer one-sheet" in docx)
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
