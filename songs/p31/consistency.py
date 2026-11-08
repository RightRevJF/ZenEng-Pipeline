"""v43 document consistency check for 'Nothing On' (one female lead and a backing echo; a disco-funk band; F major signature, F only in
the bridge; 4/4 at q = 116 on sixteenths; the power cuts; the songbook for musicians, with the producer one-sheet and the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p31"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p31/song_record.pkl", "rb"))
O = "/home/claude/p31/out/Nothing On - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p31/out/nashville.html").read(); sb = open("/home/claude/p31/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
DEMO = pickle.load(open("/home/claude/p31/out/demo_report.pkl", "rb")); PARTS = pickle.load(open("/home/claude/p31/out/parts_report.pkl", "rb"))
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, bool(ok), d))
chk("title in all", all("Nothing On" in d for d in (ly, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, nv, sb, docx)))
ENG = r"zeneng|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|fingerprint|calibrat|corpus|percentile"
chk("songbook and chart for musicians: no engine terms", not re.search(ENG, (sb + docx + nv).lower()), str(re.findall(ENG, (sb + docx + nv).lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]; BARS = REC["bars"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre 4/4 at q = 116", set(tsig) == {"4/4"} and set(tmp) == {116} and "\\time 4/4" in ly and "\\tempo 4 = 116" in ly and "♩ = 116" in nv and "♩ = 116" in sb)
chk("key signature F major throughout", set(ks) == {"F"} and "\\key f \\major" in ly and all(b["key"] == "F major" for b in BARS))
chk("76 bars", "76 bars" in nv and "76 bars" in sb and REC["nbars"] == 76 and sum(p[1] for p in plan) == 76)
chk("length 2:37", "2:37" in nv and "2:37" in sb and round(REC["seconds"]) == 157 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in BARS]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"g1:m7": "Gm7", "a1:m7": "Am7", "bes1:maj7": "Bbmaj7", "c1": "C", "f1": "F", "a1:m": "Am", "bes1": "Bb"}
chk("chords: lead sheet = record", [LYC[c] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"2m7": "Gm7", "3m7": "Am7", "4maj7": "Bbmaj7", "5": "C", "1": "F", "3m": "Am", "4": "Bb"}
cells = re.findall(r"<td>(2m7|3m7|4maj7|3m|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == len(rec) and all(NUMK[c] == ch for c, ch in zip(cells, rec)), f"{len(cells)} bars")
SBC = {"Gm7": "Gm7", "Am7": "Am7", "B♭maj7": "Bbmaj7", "C": "C", "F": "F", "Am": "Am", "B♭": "Bb"}
rows = re.findall(r"^\| ((?:[A-G]♭?(?:m7|maj7|m)? · )[A-G]♭?(?:m7|maj7|m)?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in BARS if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add(tuple(sb_[2 * i:2 * i + 2]))
row_ok = lambda a, l: tuple(SBC[x] for x in a.split(" · ")) in want.get(l.replace("(nothing on) ", ""), set())   # the backing echo shown in the row
n_rows = sum(len(ls) for s, ls in L.SECTIONS if s not in ("Post 2",))
chk("chords: songbook rows = record", rows and all(row_ok(a, l) for a, l in rows) and len(rows) == n_rows, f"{len(rows)} rows (want {n_rows}); bad: {[l for a, l in rows if not row_ok(a, l)][:3]}")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', "").replace("“", "").replace("”", ""))
chk("words: the voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG))))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace("’", "'").replace("\\\n", " ").replace("\\", "").replace("**", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p.lower()) + r"\b", l.lower())]
chk("never-say: neither list sung", not bad, str(bad))
lead = REC["lead"]
bar_i = lambda o: next(i for i, b in enumerate(BARS) if b["start"] <= o < b["start"] + b["len"])
bar_of = lambda o: BARS[bar_i(o)]
chk("voice A3-C5, D5 once on OFF (chorus 3)", min(n["midi"] for n in lead) == 57 and [(n["syl"][0], n["sec"]) for n in lead if n["midi"] > 72] == [("off", "Chorus 3")])
h = [n for n in lead if n["midi"] == 74][0]
chk("D5 on the downbeat of bar 66, over Gm7", bar_i(h["on"]) + 1 == 66 and bar_of(h["on"])["chord"] == "Gm7" and h["on"] == bar_of(h["on"])["start"])
def line(s, i): return [n for n in lead if n["sec"] == s and n["line"] == i]
TT, CL = [69, 67, 72, 72, 69, 64], [69, 67, 72, 72, 70, 67]
ok = all([n["midi"] for n in line(s, 0)] == TT and [n["midi"] for n in line(s, 3)] == CL for s in ("Chorus 1", "Chorus 2", "Chorus 3"))
ok &= all(line(s, i)[0]["on"] - bar_of(line(s, i)[0]["on"])["start"] == 2 for s in ("Chorus 1", "Chorus 2", "Chorus 3") for i in (0, 3))
chk("the title tune on every title line (A G C | C A E; the close C Bb G), each starting on the and of 1", ok)
ok = all([n["midi"] for n in line(s, 0)] == [69, 67, 72, 70, 69, 67] for s in ("Post 1", "Post 2", "Post 3"))
ok &= all([n["midi"] for n in line(s, 1)] == [69, 67, 72, 70, 69] for s in ("Post 1", "Post 2")) and [n["midi"] for n in line("Post 3", 1)] == [69, 67, 72, 70, 69, 67]
chk("the post-chorus hook (C5 Bb4 A4 G4 on 'on but the moon')", ok)
fb = [i + 1 for i, b in enumerate(BARS) if b["chord"] == "F"]
chk("the home chord withheld: F only in the bridge (bars 53, 54, 57); the song ends on Bbmaj7", fb == [53, 54, 57] and all(BARS[i - 1]["sec"] == "Bridge" for i in fb) and BARS[-1]["chord"] == "Bbmaj7"
    and "1 = F" in nv and "F is played only in the bridge" in sb)
BAND = [e for k in ("drums", "bass", "gtr", "riff", "keys", "horns", "hum") for e in REC[k]]
cutbars = [i for i, b in enumerate(BARS) if b["sec"].startswith("Chorus") and b["k"] == 0]
ok = all(not [e for e in BAND if bar_i(e["on"]) == i] for i in cutbars)
for i, b in enumerate(BARS):
    if b["sec"].startswith("Pre") and b["k"] == 3: ok &= all(e["on"] + e["dur"] <= b["start"] + 12 for e in BAND if bar_i(e["on"]) == i)
    if b["sec"] == "Bridge" and b["k"] == 7: ok &= all(e["on"] + e["dur"] <= b["start"] + 4 for e in BAND if bar_i(e["on"]) == i)
chk("the power cuts: no band in bars 17, 41, 61; nothing past beat 3 of bars 16 and 40; only the hit in bar 60", ok and [i + 1 for i in cutbars] == [17, 41, 61] and len(REC["cuts"]) == 3)
br = [n for n in lead if n["syl"][0] == "breath"][0]
chk("BREATH on C5, the downbeat of bar 60, over C", br["midi"] == 72 and bar_i(br["on"]) + 1 == 60 and br["on"] == bar_of(br["on"])["start"] and bar_of(br["on"])["chord"] == "C")
gaps = sorted(lead, key=lambda n: n["on"])
chk("an eighth's breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 2 for a, b in zip(gaps, gaps[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
rf = REC["riff"]
chk("the riff = the title cell's opening (A4 G4 C5 on the and of 1, the a of 1, the and of 2)", [(e["on"] % 16, e["p"][0]) for e in rf[:3]] == [(2, 69), (5, 67), (6, 72)])
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
want_t = {"Drums and percussion": cnt("drums"), "Bass": cnt("bass"), "Funk guitar (muted)": cnt("gtr"), "Riff guitar (clean)": cnt("riff"), "Rhodes": cnt("keys"),
          "Horns": cnt("horns"), "Hum pad (bridge)": cnt("hum"), "Guide vocal (oboe - reed fallback)": len(lead), "Backing echo (oohs)": len(REC["harm"])}
chk("MIDI notes per track = the record", all(tn.get(k) == v for k, v in want_t.items()), str({k: (tn.get(k), v) for k, v in want_t.items() if tn.get(k) != v}))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("stems: the voice at least 3 dB over the band", DEMO["stems_db"] >= 3, f"{DEMO['stems_db']:+.1f} dB")
E_ = {r["sec"]: r["energy_read"] for r in DEMO["energy"]}
chk("energy: each chorus above its verse; the last chorus the top of the choruses and posts",
    E_["Chorus 1"] > E_["Verse 1"] and E_["Chorus 2"] > E_["Verse 2"] and E_["Chorus 3"] >= max(E_[k] for k in E_ if k.startswith(("Chorus", "Post"))), str({k: round(v, 2) for k, v in E_.items()}))
chk("parts: every part read back against the record; drum hits counted", all(PARTS["readback"].values()) and PARTS["drum_hits"] == PARTS["drum_want"])
chk("songbook carries the one-sheet and the production notes", all(h_ in sb for h_ in ("## Lyric sheet", "## Producer one-sheet", "## Production brief", "## Session notes", "## Score and parts")))
def at(word, sec):
    n = [x for x in lead if x["syl"][0] == word and x["sec"] == sec][0]; return bar_i(n["on"]) + 1, (n["on"] - bar_of(n["on"])["start"]) / 4 + 1, n["midi"]
chk("songbook melody notes read from the record (bar 66 D5, bar 60 C5, bar 15 Bb4 on beat 4, bar 46 G4)",
    at("off", "Chorus 3") == (66, 1.0, 74) and "**D5 on “off”**, the downbeat of bar 66" in sb and at("breath", "Bridge") == (60, 1.0, 72) and "C5 on “breath” on the downbeat of bar 60" in sb
    and at("breathe", "Pre 1") == (15, 4.0, 70) and "B♭4 on “breathe” on beat 4 of bar 15" in sb and at("off", "Chorus 2") == (46, 1.0, 67) and "held from the downbeat of bar 46" in sb)
for n, ok_, d in checks: print(f"{'OK ' if ok_ else 'XX '} {n}  {d}")
print(f"{sum(ok_ for _, ok_, _ in checks)}/{len(checks)} consistent")
pickle.dump(checks, open("/home/claude/p31/out/consistency.pkl", "wb"))
