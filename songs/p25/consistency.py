"""v43 document consistency check for 'Through Its Breaking' (one female voice; piano with the bell figure, cello, strings;
A minor / C major; 6/8 at dotted-q = 54; the songbook for musicians)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p25"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p25/song_record.pkl", "rb"))
O = "/home/claude/p25/out/Through Its Breaking - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p25/out/nashville.html").read(); sb = open("/home/claude/p25/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("Through Its Breaking" in d for d in (ly, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, nv, sb, docx)))
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
chk("form (MIDI markers = record plan = songbook form table)", markers == [p[0] for p in plan] and all(f"| {p[0]} |" in sb for p in plan))
chk("metre 6/8 at dotted-q = 54 (MIDI quarter 81)", set(tsig) == {"6/8"} and set(tmp) == {81} and "\\time 6/8" in ly and "\\tempo 4. = 54" in ly and "♩. = 54" in nv and "♩. = 54" in sb)
keyof = {p[0]: REC["bars"][p[2]]["key"] for p in plan}
chk("keys: A minor (intro, verses, interludes, bridge), C major (choruses, tag, outro); one signature", ks == [{"A minor": "Am", "C major": "C"}[keyof[p[0]]] for p in plan]
    and "\\key a \\minor" in ly and "A minor" in sb and "C major" in sb)
chk("88 bars", "88 bars" in nv and "88 bars" in sb and REC["nbars"] == 88 and sum(p[1] for p in plan) == 88)
chk("length 3:16", "3:16" in nv and "3:16" in sb and round(REC["seconds"]) == 196 and abs(mid.length - REC["seconds"]) < 3, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"f": "F", "c": "C", "g": "G", "e": "E", "e:m": "Em", "d:m": "Dm", "a:m": "Am"}
chk("chords: lead sheet = record", [LYC[re.sub(r"2\.", "", c)] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"A minor": {"1m": "Am", "♭3": "C", "4m": "Dm", "5": "E", "5m": "Em", "♭6": "F", "♭7": "G"},
        "C major": {"1": "C", "2m": "Dm", "3m": "Em", "3": "E", "4": "F", "5": "G", "6m": "Am"}}
cells = re.findall(r"<td>(1m|♭3|4m|5m|♭6|♭7|2m|3m|6m|1|3|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == len(rec) and all(NUMK[b["key"]][c] == b["chord"] for c, b in zip(cells, REC["bars"])), f"{len(cells)} bars")
rows = re.findall(r"^\| ((?:[A-G]m? · )+[A-G]m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls):
        n = 4 if (s == "Chorus 3" and i == 3) else 2
        want.setdefault(l, set()).add(tuple(sb_[2 * i:2 * i + n]))
chk("chords: songbook rows = record", rows and all(tuple(a.split(" · ")) in want.get(l.replace("’", "'"), set()) for a, l in rows), f"{len(rows)} rows")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', "").replace("“", "").replace("”", ""))
chk("words: the voice staff = every sung line in order", words == norm(" ".join(L.SUNG).replace('"', "")))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace('"', "").replace("“", "").replace("”", "").replace("’", "'")
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung", not bad, str(bad))
lead = REC["lead"]
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
chk("voice A3-B4, C5 once on THROUGH (chorus 3)", min(n["midi"] for n in lead) >= 57 and [(n["syl"][0], n["sec"]) for n in lead if n["midi"] > 71] == [("through", "Chorus 3")])
th = [n for n in lead if n["midi"] == 72][0]
chk("THROUGH on C5 over C, a downbeat, held", bar_of(th["on"])["chord"] == "C" and th["on"] == bar_of(th["on"])["start"] and th["dur"] >= 2)
chk("B4 only on REACHED, over G", [(n["syl"][0], bar_of(n["on"])["chord"]) for n in lead if n["midi"] == 71] == [("reached", "G")])
tr = [n for n in lead if n["syl"][0] == "true"]
chk("TRUE on A4 over F in every chorus", len(tr) == 3 and all(n["midi"] == 69 and bar_of(n["on"])["chord"] == "F" for n in tr))
rt = [n for n in lead if n["syl"][0] == "through" and n["sec"] in ("Chorus 1", "Chorus 2")]
chk("'rings it THROUGH' on G4 over G (choruses 1, 2)", len(rt) == 2 and all(n["midi"] == 67 and bar_of(n["on"])["chord"] == "G" for n in rt))
A4 = {(n["syl"][0] if n["sec"].startswith("Chorus") else n["sec"]) for n in lead if n["midi"] == 69}
chk("A4 only on TRUE (choruses) and in the bridge's climb", A4 == {"true", "Bridge"}, str(A4))
bb = {b["sec"] for b in REC["bars"] if b["bell"]}
chk("the bell: intro, interludes, bridge bars 61-68, chorus 3, tag, outro", bb == {"Intro", "Interlude 1", "Interlude 2", "Bridge", "Chorus 3", "Tag", "Outro"}
    and [i + 1 for i, b in enumerate(REC["bars"]) if b["sec"] == "Bridge" and b["bell"]] == list(range(61, 69)))
chk("the crack = root + the half step below", all(e["p"][1] - e["p"][0] == 1 and (e["p"][1] % 12 == {"Am": 9, "F": 5, "C": 0, "G": 7, "Dm": 2, "E": 4, "Em": 4}[bar_of(e["on"])["chord"]] or e is REC["bell"][-1])
                                                   for e in REC["bell"] if e["kind"] == "crack"))
last = REC["bell"][-1]
chk("the last bar: B4 against C5 left ringing over C", last["p"] == [71, 72] and bar_of(last["on"]) is REC["bars"][-1] and REC["bars"][-1]["chord"] == "C")
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
chk("MIDI notes per track = the record (piano, bell, cello, strings)", tn.get("Piano") == sum(len(e["p"]) for e in REC["pno"]) and tn.get("Piano - the bell (toll and crack)") == sum(len(e["p"]) for e in REC["bell"])
    and tn.get("Cello") == sum(len(e["p"]) for e in REC["cello"]) and tn.get("Strings") == sum(len(e["p"]) for e in REC["strings"]), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("tag: no strings, no left-hand figure", not any(bar_of(e["on"])["sec"] == "Tag" for e in REC["strings"]) and all(e["art"] == "ring" for e in REC["pno"] if bar_of(e["on"])["sec"] == "Tag"))
chk("lead sheet pages carry the credit footer", "Words and music: Jason Bryant" in ly)
fs = open(O + "full score.ly").read()
fcm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", fs, re.S).group(1).split()
fm = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", fs, re.S).group(1)
fwords = norm(re.sub(r" -- ", "", fm).replace(" __", "").replace(" _ ", " ").replace('"', "").replace("“", "").replace("”", ""))
chk("full score: chords and words = the lead sheet's", fcm == cm and fwords == words and "Through Its Breaking" in fs and "Words and music: Jason Bryant" in fs)
chk("songbook carries the production notes (lyric sheet, brief, session notes, score and parts)", all(h in sb for h in ("## Lyric sheet", "## Production brief", "## Session notes", "## Score and parts")))
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
