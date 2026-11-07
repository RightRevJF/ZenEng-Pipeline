"""v43 document consistency check for 'Make Do' (4/4, q = 72, G major; the instrumental lines, Module 27.21)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p21"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p21/song_record.pkl", "rb"))
O = "/home/claude/p21/out/Make Do - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p21/out/nashville.html").read(); sb = open("/home/claude/p21/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("Make Do" in d for d in (ly, nv, sb, docx)))
chk("credit (ZenEng v64, Jason Bryant)", all("v64" in d for d in (ly, nv, sb)) and all("Jason Bryant" in d for d in (ly, nv, sb, docx)))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre 4/4, q = 72 every section", set(tsig) == {"4/4"} and set(tmp) == {72} and "\\tempo 4 = 72" in ly and "♩ = 72" in nv and "♩ = 72" in sb)
chk("G major throughout", set(ks) == {"G"} and "\\key g \\major" in ly and "G major" in sb)
chk("68 bars", "68 bars" in nv and "68 bars" in sb and REC["nbars"] == 68 and sum(p[1] for p in plan) == 68)
chk("length 3:47", "3:47" in nv and "3:47" in sb and round(REC["seconds"]) == 227, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"g1:maj7": "Gmaj7", "c1:maj7": "Cmaj7", "d1": "D", "e1:m7": "Em7", "a1:m7": "Am7", "g1": "G"}
chk("chords: lead sheet = record", [LYC[c] for c in cm] == rec, f"{len(cm)} bars")
NUM = {"1maj7": "Gmaj7", "4maj7": "Cmaj7", "5": "D", "6m7": "Em7", "2m7": "Am7", "1": "G"}
cells = re.findall(r"<td>(1maj7|4maj7|6m7|2m7|5|1)(?:\s|<)", nv)
chk("chords: Nashville = record", [NUM[c] for c in cells] == rec, f"{len(cells)} bars")
rows = re.findall(r"^\| ([A-G][a-z0-9]*) · ([A-G][a-z0-9]*) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add((sb_[2 * i], sb_[2 * i + 1]))
chk("chords: songbook rows = record", rows and all((a, b) in want.get(l.replace("’", "'"), set()) for a, b, l in rows), f"{len(rows)} rows")
lyr = re.search(r"\\lyricsto \"mel\" \{ (.*?) \}\n", ly, re.S).group(1)
lw = norm(re.sub(r" -- ", "", lyr).replace(" __", "").replace(" _ ", " ").replace('"', ""))
chk("words: lead sheet = lyric", lw == norm(" ".join(L.SUNG)), f"{len(lw)} vs {len(norm(' '.join(L.SUNG)))} words")
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace('"', "").replace("“", "").replace("”", "").replace("’", "'")
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq),
    str([l for l in uniq if strip(l) not in strip(sb) or strip(l) not in strip(docx)][:3]))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung", not bad, str(bad))
chk("'cattywumpus' once, in a verse, not the chorus", sum("cattywumpus" in l for l in L.SUNG) == 1 and not any("cattywumpus" in l for _, l in L.CHORUS))
lead = REC["lead"]; ps = [n["midi"] for n in lead]
d4 = [n for n in lead if n["midi"] > 59]
chk("range B2-D4; D4 once, on the last DO", min(ps) >= 47 and len(d4) == 1 and d4[0]["midi"] == 62 and d4[0]["sec"] == "Chorus 3" and d4[0]["syl"][0] == "do")
chk("verses <= A3; chorus <= B3 but the last DO", all(n["midi"] <= 57 for n in lead if n["sec"].startswith("Verse")) and all(n["midi"] <= 59 for n in lead if n["sec"].startswith("Chorus") and n is not d4[0]))
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
for sec in ("Chorus 1", "Chorus 2"):
    ns = [n for n in lead if n["sec"] == sec and n["line"] == 3]; d = ns[-1]; b = bar_of(d["on"])
    chk(f"{sec}: DO on B3 over G, a downbeat, held, +4 from MAKE", d["midi"] == 59 and b["chord"] == "G" and d["on"] == b["start"] and d["dur"] >= 4 and d["midi"] - ns[-2]["midi"] == 4)
def cell(s, li):
    ns = [n for n in lead if n["sec"] == s and n["line"] == li]; b0 = [b for b in REC["bars"] if b["sec"] == s][0]["start"]
    return [(n["midi"], n["dur"] if k < len(ns) - 1 else None, n["syl"][0], n["on"] - b0) for k, n in enumerate(ns)]   # the last note's length is the join's
chk("chorus 2 = chorus 1; chorus 3 = chorus 1 but the last DO (a line's last length set by the join)", all(cell("Chorus 1", i) == cell("Chorus 2", i) for i in range(4))
    and all(cell("Chorus 1", i) == cell("Chorus 3", i) for i in range(3)) and cell("Chorus 1", 3)[:-1] == cell("Chorus 3", 3)[:-1])
chk("line 2 open (not on G)", all(cell(s, 1)[-1][0] % 12 != 7 for s in ("Verse 1", "Verse 2", "Verse 3", "Chorus 1")))
gt = REC["gtr"]
chk("27.21: a line in every instrumental section, floored (all rows pass but the one-phrase peak)", {n["sec"] for n in gt} == {"Intro", "Break", "Outro"}
    and all(all(v[1] for k, v in REC["gtr_floor"][s].items() if k != "peak_place") for s in REC["gtr_floor"]) and REC["gtr_floor"]["Break"]["peak_place"][1])
chk("27.21: the cue voice on the lead sheet, the instrument and clef named, grey", '\\new Voice = "gtr"' in ly and "cue: clean guitar" in ly and "8vb clef" in ly and "grey35" in ly)
lt = next(tr for tr in mid.tracks if any(m.type == "track_name" and m.name.startswith("Instrumental lead") for m in tr))
nlead = sum(1 for m in lt if m.type == "note_on" and m.velocity > 0)
chk("11.11 (v64): the lead track's notes in the MIDI = the record's", nlead == len(gt), f"{nlead} vs {len(gt)}")
chk("the cue never overlaps the voice", not any(a["on"] < g["on"] + g["dur"] and g["on"] < a["on"] + a["dur"] for g in gt for a in lead))
chk("record logs the forms and the certificates by construction", REC["plans"] and any(e[1] == "forms" for e in REC["cell_log"]) and len(REC["by_construction"]) == 4)
chk("songbook names the blind-pick slots from 10.20", all(x in sb for x in ("one corner gone cattywumpus in the dark", "the afternoon will have to make do", "I watch a blade of daylight find its way in")))
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
