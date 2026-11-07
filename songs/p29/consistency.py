"""Document consistency check for 'The Word Without a Word' (a concert carol: one high voice, piano, cello, strings; 3/4 at q = 66, the
last refrain and coda at q = 56; D-flat, E-flat from verse 4; the songbook for musicians, with the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p29"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p29/song_record.pkl", "rb"))
O = "/home/claude/p29/out/The Word Without a Word - "
ly = open(O + "lead sheet.ly").read(); sc = open(O + "full score.ly").read(); nv = open("/home/claude/p29/out/nashville.html").read()
sb = open("/home/claude/p29/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("The Word Without a Word" in d for d in (ly, sc, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, sc, nv, sb, docx)))
ENG = r"zeneng|\bengine\b|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|search|fingerprint"
chk("songbook and chart for musicians: no engine terms", not re.search(ENG, sb.lower() + docx.lower() + nv.lower()), str(re.findall(ENG, sb.lower() + docx.lower() + nv.lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("3/4 throughout", set(tsig) == {"3/4"} and "\\time 3/4" in ly)
chk("tempo: q = 66, then q = 56 from refrain 3", tmp == [56 if p[0] in ("Refrain 3", "Coda") else 66 for p in plan] and "\\tempo 4 = 66" in ly and "4 = 56" in ly and "♩ = 66" in sb and "♩ = 56" in sb and "♩ = 56" in nv)
chk("keys: D-flat to bar 60, E-flat from verse 4", ks == [("Eb" if p[0] in ("Verse 4", "Refrain 3", "Coda") else "Db") for p in plan] and "\\key des \\major" in ly and "\\key ees \\major" in ly
    and REC["bars"][59]["key"] == "Db major" and REC["bars"][60]["key"] == "Eb major")
chk("80 bars", "80 bars" in nv and "80 bars" in sb and REC["nbars"] == 80 and sum(p[1] for p in plan) == 80)
chk("length 3:44", "3:44" in nv and "3:44" in sb and round(REC["seconds"]) == 224 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"des2.": "Db", "ges2.": "Gb", "aes2.": "Ab", "bes2.:m": "Bbm", "f2.:m": "Fm", "ees2.:m": "Ebm", "bes2.": "Bb", "ees2.": "Eb", "c2.:m": "Cm", "g2.:m": "Gm", "f2.": "F"}
chk("chords: lead sheet = record", [LYC[c] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"Db major": {"1": "Db", "2m": "Ebm", "3m": "Fm", "4": "Gb", "5": "Ab", "6m": "Bbm", "3": "F", "6": "Bb"}, "Eb major": {"1": "Eb", "2m": "Fm", "3m": "Gm", "4": "Ab", "5": "Bb", "6m": "Cm"}}
cells = re.findall(r"<td>(2m|3m|6m|1|3|4|5|6)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == 80 and all(NUMK[b["key"]][c] == b["chord"] for c, b in zip(cells, REC["bars"])), f"{len(cells)} bars")
SBC = {"D♭": "Db", "G♭": "Gb", "A♭": "Ab", "B♭m": "Bbm", "Fm": "Fm", "E♭m": "Ebm", "B♭": "Bb", "E♭": "Eb", "Cm": "Cm", "Gm": "Gm"}
rows = re.findall(r"^\| ((?:[A-G]♭?m? · )+[A-G]♭?m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    cs = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(re.sub(r"\*", "", l), set()).add(tuple(cs[2 * i:2 * i + 2]))
def row_ok(a, l): return tuple(SBC[x] for x in a.split(" · ")) in want.get(re.sub(r"\*", "", l), set())
chk("chords: songbook rows = record", rows and all(row_ok(a, l) for a, l in rows), f"{len(rows)} rows; bad: {[l for a, l in rows if not row_ok(a, l)][:3]}")
m = re.search(r'\\lyricsto "voc" \{ (.*?) \}\n', ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
chk("words: the voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG))))
uniq = list(dict.fromkeys(L.SUNG)); strip = lambda t: t.replace("’", "'").replace("*", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq), str([l for l in uniq if strip(l) not in strip(sb)][:2]))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: no carol cliché sung", not bad, str(bad))
lead = REC["lead"]
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
bno = lambda o: REC["bars"].index(bar_of(o)) + 1
top = [n for n in lead if n["midi"] > 80]
chk("B-flat5 once, on WORLD over E-flat at the downbeat of bar 74", [(n["syl"][0], n["midi"], bno(n["on"]), bar_of(n["on"])["chord"], n["on"] == bar_of(n["on"])["start"]) for n in top] == [("world", 82, 74, "Eb", True)])
chk("voice D-flat4 and up; nothing above A-flat5 but the one B-flat5", min(n["midi"] for n in lead) == 61 and max(n["midi"] for n in lead if n["midi"] != 82) == 80)
tw = [n for n in lead if n["sec"] in ("Refrain 1", "Refrain 2") and n["line"] == 0][-1]
chk("the title's last WORD on E-flat5 over A-flat (refrains 1-2)", all([n for n in lead if n["sec"] == s and n["line"] == 0][-1]["midi"] == 75 and bar_of([n for n in lead if n["sec"] == s and n["line"] == 0][-1]["on"])["chord"] == "Ab" for s in ("Refrain 1", "Refrain 2")))
rs = [[n for n in lead if n["sec"] == s and n["line"] == 3][-1] for s in ("Refrain 1", "Refrain 2")]
chk("RESTS on A-flat4 over A-flat (the half cadence)", all(n["syl"][0] == "rests" and n["midi"] == 68 and bar_of(n["on"])["chord"] == "Ab" for n in rs))
last = [n for n in lead if n["sec"] == "Refrain 3" and n["line"] == 3][-1]
chk("the last IN on B-flat4 over B-flat, open", last["syl"][0] == "in" and last["midi"] == 70 and bar_of(last["on"])["chord"] == "Bb")
ma = REC["ma"]
chk("MA held two beats or more, and nothing in piano or cello starts under it", ma["dur"] >= 4 and not [e for e in REC["pno"] + REC["cello"] if ma["on"] < e["on"] < ma["on"] + ma["dur"]])
ab = REC["abba_bar"]
chk("ABBA's bar (59): the ensemble silent; the voice sings Ab4-F4", bno(ab) == 59 and not [e for e in REC["pno"] + REC["cello"] + REC["strings"] if ab <= e["on"] < ab + 6]
    and [n["midi"] for n in lead if n["syl"][0] == "abba"] == [68, 65])
jt = [n for n in lead if n["sec"] == "Bridge" and n["line"] == 3][-1]
chk("TURNS on D5 over B-flat, bar 60 (the pivot into E-flat)", jt["syl"][0] == "turns" and jt["midi"] == 74 and bno(jt["on"]) == 60 and bar_of(jt["on"])["chord"] == "Bb")
r1 = [(n["on"] - REC["bars"][12]["start"], n["midi"]) for n in lead if n["sec"] == "Refrain 1"]; r2 = [(n["on"] - REC["bars"][28]["start"], n["midi"]) for n in lead if n["sec"] == "Refrain 2"]
chk("refrain 2 = refrain 1", r1 == r2)
il = [e for e in REC["cello"] if e.get("art") == "lullaby"]
r1n = [n for n in lead if n["sec"] == "Refrain 1"]; d = REC["bars"][36]["start"] - REC["bars"][12]["start"]
chk("the interlude: the cello sings refrain 1's tune an octave lower", il and all(any(e["on"] == n["on"] + d and e["p"] == [n["midi"] - 12] for n in r1n) for e in il))
gaps = sorted(lead, key=lambda n: n["on"])
chk("a breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 1 for a, b in zip(gaps, gaps[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
chk("MIDI notes per track = the record", tn.get("Piano") == cnt("pno") and tn.get("Cello") == cnt("cello") and tn.get("Strings") == cnt("strings") and tn.get("Guide vocal (flute)") == len(lead), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("full score: every staff present", all(x in sc for x in ('instrumentName = "Voice"', 'instrumentName = "Piano"', 'instrumentName = "Cello"', 'instrumentName = "Strings"')))
chk("songbook carries the production notes and the one-sheet", all(h_ in sb for h_ in ("## Lyric sheet", "## Producer one-sheet", "## Production brief", "## Session notes", "## Score and parts")) and "Producer one-sheet" in docx)
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
