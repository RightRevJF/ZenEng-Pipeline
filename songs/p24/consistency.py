"""v43 document consistency check for 'The Song You Sang Me' (one tenor and one guitar; F major; 3/4 at q = 76; the songbook for musicians)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p24"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p24/song_record.pkl", "rb"))
O = "/home/claude/p24/out/The Song You Sang Me - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p24/out/nashville.html").read(); sb = open("/home/claude/p24/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("The Song You Sang Me" in d for d in (ly, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Jason Bryant" in d for d in (ly, nv, sb, docx)))
ENG = r"zeneng|\bengine\b|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|search|fingerprint"
chk("songbook and chart for musicians: no engine terms", not re.search(ENG, sb.lower()) and not re.search(ENG, docx.lower()) and not re.search(ENG, nv.lower()),
    str(re.findall(ENG, sb.lower() + docx.lower() + nv.lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre 3/4 at q = 76", set(tsig) == {"3/4"} and set(tmp) == {76} and "\\time 3/4" in ly and "\\tempo 4 = 76" in ly and "♩ = 76" in nv and "♩ = 76" in sb)
chk("key F major (MIDI, lead sheet, chart, songbook); capo 3", set(ks) == {"F"} and "\\key f \\major" in ly and "capo 3" in nv.lower() and "capo 3" in sb.lower())
chk("112 bars", "112 bars" in nv and "112 bars" in sb and REC["nbars"] == 112 and sum(p[1] for p in plan) == 112)
chk("length 4:25", "4:25" in nv and "4:25" in sb and round(REC["seconds"]) == 265, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"f": "F", "bes": "Bb", "c": "C", "d:m": "Dm", "g:m": "Gm", "a:m": "Am"}
chk("chords: lead sheet = record", [LYC[re.sub(r"2\.", "", c)] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"1": "F", "4": "Bb", "5": "C", "6m": "Dm", "2m": "Gm", "3m": "Am"}
cells = re.findall(r"<td>(6m|2m|3m|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == len(rec) and all(NUMK[c] == r for c, r in zip(cells, rec)), f"{len(cells)} bars")
SBC = {"F": "F", "B♭": "Bb", "C": "C", "Dm": "Dm", "Gm": "Gm", "Am": "Am"}
rows = re.findall(r"^\| ((?:[A-G]♭?m? · )+[A-G]♭?m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add(tuple(sb_[4 * i:4 * i + 4]))
chk("chords: songbook rows = record", rows and all(tuple(SBC[x] for x in a.split(" · ")) in want.get(l.replace("’", "'"), set()) for a, l in rows), f"{len(rows)} rows")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', "").replace("“", "").replace("”", ""))
chk("words: the voice staff = every sung line in order", words == norm(" ".join(L.SUNG).replace('"', "")))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace('"', "").replace("“", "").replace("”", "").replace("’", "'")
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung; the parent never gendered", not bad and not re.search(r"\b(mother|father|mom|dad|mama|daddy)\b", " ".join(L.SUNG).lower()), str(bad))
lead = REC["lead"]
chk("voice E3-A4, Bb4 once on the last WAKE", min(n["midi"] for n in lead) >= 50 and [n["syl"][0] for n in lead if n["midi"] > 69] == ["wake"] and max(n["midi"] for n in lead) == 70)
chk("A4 only on DARK", {n["syl"][0] for n in lead if n["midi"] == 69} == {"dark"})
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
for sec in ("Verse 1", "Verse 2", "Verse 3", "Verse 4"):
    rf = [n for n in lead if n["sec"] == sec and n["line"] == 3]
    chk(f"{sec}: the refrain (ME C4 over C, SON/SONG F3 over F, both downbeats)", [n["midi"] for n in rf] == [57, 60, 57, 55, 53] and bar_of(rf[1]["on"])["chord"] == "C"
        and rf[1]["on"] == bar_of(rf[1]["on"])["start"] and bar_of(rf[4]["on"])["chord"] == "F" and rf[4]["on"] == bar_of(rf[4]["on"])["start"]
        and rf[4]["syl"][0] == ("song" if sec == "Verse 4" else "son"))
for sec in ("Chorus 1", "Chorus 2"):
    dk = [n for n in lead if n["sec"] == sec and n["syl"][0] == "dark"][0]
    chk(f"{sec}: DARK on A4 over F, a downbeat, held", dk["midi"] == 69 and bar_of(dk["on"])["chord"] == "F" and dk["on"] == bar_of(dk["on"])["start"] and dk["dur"] >= 8)
wk = [n for n in lead if n["syl"][0] == "wake"]
chk("WAKE on F4 (chorus 1), on Bb4 (chorus 2), over Bb, downbeats", [n["midi"] for n in wk] == [65, 70] and all(bar_of(n["on"])["chord"] == "Bb" and n["on"] == bar_of(n["on"])["start"] for n in wk))
gm = REC["gmel"]
chk("the lullaby's tune on the guitar in the intro and outro only, on chord tones", {bar_of(n["on"])["sec"] for n in gm} == {"Intro", "Outro"}
    and all(REC["gmel_floor"][s]["chord_tones_on_strong"][1] and REC["gmel_floor"][s]["distinct_pitches"][1] for s in REC["gmel_floor"]))
chk("the tune never overlaps the voice", not any(a["on"] < g["on"] + g["dur"] and g["on"] < a["on"] + a["dur"] for g in gm for a in lead))
tr = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
chk("the guitar's notes in the MIDI = the record's (tune and fingerpicking)", tr.get("Instrumental lead - guitar (the lullaby)") == sum(len(e["p"]) for e in gm)
    and tr.get("Guitar") == sum(len(e["p"]) for e in REC["gtr"]), str(tr))
chk("verse 4 thinned: one chord a bar", all(len([e for e in REC["gtr"] if bar_of(e["on"])["sec"] == "Verse 4" and bar_of(e["on"])["start"] == b["start"]]) == 1 for b in REC["bars"] if b["sec"] == "Verse 4"))
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
