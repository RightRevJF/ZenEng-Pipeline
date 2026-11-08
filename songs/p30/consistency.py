"""v43 document consistency check for 'She Left the Light On' (one male voice; a country band; D major, G minor borrowed under THUMB;
4/4 at q = 84 on sixteenths; the songbook for musicians, with the producer one-sheet and the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p30"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p30/song_record.pkl", "rb"))
O = "/home/claude/p30/out/She Left the Light On - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p30/out/nashville.html").read(); sb = open("/home/claude/p30/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("She Left the Light On" in d for d in (ly, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, nv, sb, docx)))
ENG = r"zeneng|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|fingerprint|calibrat"
chk("songbook and chart for musicians: no engine terms", not re.search(ENG, (sb + docx + nv).lower()), str(re.findall(ENG, (sb + docx + nv).lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre 4/4 at q = 84", set(tsig) == {"4/4"} and set(tmp) == {84} and "\\time 4/4" in ly and "\\tempo 4 = 84" in ly and "♩ = 84" in nv and "♩ = 84" in sb)
chk("key: D major throughout", set(ks) == {"D"} and "\\key d \\major" in ly and all(b["key"] == "D major" for b in REC["bars"]))
chk("60 bars", "60 bars" in nv and "60 bars" in sb and REC["nbars"] == 60 and sum(p[1] for p in plan) == 60)
chk("length 2:51", "2:51" in nv and "2:51" in sb and round(REC["seconds"]) == 171 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"d": "D", "g": "G", "a": "A", "b:m": "Bm", "e:m": "Em", "g:m": "Gm"}
chk("chords: lead sheet = record", [LYC[c.replace("1", "")] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"1": "D", "4": "G", "5": "A", "6m": "Bm", "2m": "Em", "4m": "Gm"}
cells = re.findall(r"<td>(6m|4m|2m|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == len(rec) and all(NUMK[c] == ch for c, ch in zip(cells, rec)), f"{len(cells)} bars")
rows = re.findall(r"^\| ((?:[A-G]m? · )+[A-G]m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add(tuple(sb_[2 * i:2 * i + 2]))
row_ok = lambda a, l: tuple(a.split(" · ")) in want.get(l, set())
chk("chords: songbook rows = record", rows and all(row_ok(a, l) for a, l in rows) and len(rows) == sum(len(ls) for s, ls in L.SECTIONS if s != "Chorus 2"), f"{len(rows)} rows; bad: {[l for a, l in rows if not row_ok(a, l)][:3]}")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', "").replace("“", "").replace("”", ""))
chk("words: the voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG))))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace("’", "'").replace("\\\n", " ").replace("\\", "").replace("**", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p.lower()) + r"\b", l.lower())]
chk("never-say: neither list sung", not bad, str(bad))
lead = REC["lead"]
bar_i = lambda o: next(i for i, b in enumerate(REC["bars"]) if b["start"] <= o < b["start"] + b["len"])
bar_of = lambda o: REC["bars"][bar_i(o)]
chk("voice D3-E4, F#4 once on LIGHT (chorus 3)", min(n["midi"] for n in lead) >= 50 and [(n["syl"][0], n["sec"]) for n in lead if n["midi"] > 64] == [("light", "Chorus 3")])
h = [n for n in lead if n["midi"] == 66][0]
chk("F#4 on beat 3 of bar 49, over D", bar_i(h["on"]) + 1 == 49 and bar_of(h["on"])["chord"] == "D" and h["on"] - bar_of(h["on"])["start"] == 8)
def line(s, i): return [n for n in lead if n["sec"] == s and n["line"] == i]
CELL1, CELL4, FLIP = [57, 62, 59, 62, 57], [57, 62, 61, 64, 62], [57, 59, 62, 64, 66, 62]
ok = all([n["midi"] for n in line(s, 0)] == CELL1 and [n["midi"] for n in line(s, 3)] == CELL4 for s in ("Chorus 1", "Chorus 2"))
ok &= [n["midi"] for n in line("Chorus 3", 1)] == FLIP and [n["midi"] for n in line("Chorus 3", 4)] == CELL4
ok &= [n["midi"] for n in line("Verse 1", 3)][-5:] == CELL1
ok &= all(line(s, i)[[x["syl"][0] for x in line(s, i)].index(w)]["on"] == bar_of(line(s, i)[[x["syl"][0] for x in line(s, i)].index(w)]["on"])["start"]
          for s, i, w in (("Chorus 1", 0, "left"), ("Chorus 1", 3, "left"), ("Chorus 3", 1, "leave"), ("Chorus 3", 4, "leave")))
chk("the title tune on every title line (A D B D A; the close A D C# E D; the flip; LEFT/LEAVE on the downbeat)", ok)
th = [n for n in lead if n["syl"][0] == "thumb"][0]
chk("THUMB on Bb3 over G minor; G minor only in bars 45-46", th["midi"] == 58 and bar_of(th["on"])["chord"] == "Gm"
    and [i + 1 for i, b in enumerate(REC["bars"]) if b["chord"] == "Gm"] == [45, 46])
gaps = sorted(lead, key=lambda n: n["on"])
chk("an eighth's breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 2 for a, b in zip(gaps, gaps[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
d47 = [e for e in REC["drums"] + REC["bass"] if bar_i(e["on"]) + 1 == 47]; d48 = [e for e in REC["drums"] if bar_i(e["on"]) + 1 == 48]
chk("the drop: bar 47 no kit or bass; bar 48 toms only; one acoustic strum", not d47 and d48 and all(e["p"][0] in (45, 47, 50) for e in d48)
    and not [e for e in REC["bass"] if bar_i(e["on"]) + 1 == 48] and len([e for e in REC["ac"] if bar_i(e["on"]) + 1 in (47, 48)]) == 1)
lk = REC["lick"]
chk("the lick = the title tune up an octave; it ends on B4 over G", [e["p"][0] for e in lk[:4]] == [p + 12 for p in CELL1[:4]] and lk[-1]["p"] == [71]
    and REC["bars"][-1]["chord"] == "G" and lk[-1]["on"] + lk[-1]["dur"] == REC["total_slots"])
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
chk("MIDI notes per track = the record", tn.get("Drums") == cnt("drums") and tn.get("Bass") == cnt("bass") and tn.get("Acoustic guitar (strummed)") == cnt("ac")
    and tn.get("Electric guitar (the lick)") == cnt("lick") and tn.get("Pedal steel (approximated)") == cnt("steel") and tn.get("Organ") == cnt("organ")
    and tn.get("Guide vocal (clarinet - reed fallback)") == len(lead), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("songbook carries the one-sheet and the production notes", all(h_ in sb for h_ in ("## Lyric sheet", "## Producer one-sheet", "## Production brief", "## Session notes", "## Score and parts")))
chk("songbook melody notes read from the record (bar 49 F♯4, bar 46 B♭3, bar 15 E4)", "F♯4, beat 3, over D" in sb and "“Thumb” lands on B♭3 (bar 46)" in sb
    and bar_i([n for n in line("Chorus 1", 1) if n["syl"][0] == "asked"][0]["on"]) + 1 == 15 and "E4 on “asked” (bar 15)" in sb)
for n, ok_, d in checks: print(f"{'OK ' if ok_ else 'XX '} {n}  {d}")
print(f"{sum(ok_ for _, ok_, _ in checks)}/{len(checks)} consistent")
