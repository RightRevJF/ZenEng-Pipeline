"""Document consistency check for 'Either Or' (one tenor; two guitars, bass, organ, drums; D Dorian verses in 5/4,
F major refrains in 4/4, q = 132; the stop at bar 79; the songbook for musicians, with the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p27"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p27/song_record.pkl", "rb"))
O = "/home/claude/p27/out/Either Or - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p27/out/nashville.html").read(); sb = open("/home/claude/p27/songbook.md").read()
pt = open(O + "parts (guitars, bass, organ, drums).ly").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("Either Or" in d for d in (ly, nv, sb, docx, pt)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, nv, sb, docx, pt)))
ENG = r"zeneng|\bengine\b|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|search|fingerprint"
chk("songbook and chart for musicians: no engine terms", not re.search(ENG, sb.lower() + docx.lower() + nv.lower()),
    str(re.findall(ENG, sb.lower() + docx.lower() + nv.lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre per section: MIDI = record (5/4 verses, intro, break, build; 4/4 refrains, outro)", tsig == [p[3] for p in plan]
    and all(p[3] == ("4/4" if p[0].startswith(("Refrain", "Outro")) else "5/4") for p in plan))
chk("lead sheet: \\time 3,2 5/4 and 4/4 at each change", ly.count("\\time 3,2 5/4") == sum(1 for a, b in zip([None] + plan, plan) if b[3] == "5/4" and (a is None or a[3] != "5/4"))
    and ly.count("\\time 4/4") == sum(1 for a, b in zip([None] + plan, plan) if b[3] == "4/4" and (a is None or a[3] != "4/4")))
chk("q = 132 throughout", set(tmp) == {132} and "\\tempo 4 = 132" in ly and "♩ = 132" in nv and "♩ = 132" in sb)
keyof = {p[0]: REC["bars"][p[2]]["key"] for p in plan}
chk("keys: D Dorian verses (no signature), F major refrains", ks == [{"D Dorian": "C", "F major": "F"}[keyof[p[0]]] for p in plan]
    and "\\key d \\dorian" in ly and "\\key f \\major" in ly and all(keyof[p[0]] == ("F major" if p[0].startswith("Refrain") else "D Dorian") for p in plan))
chk("84 bars", "84 bars" in nv and "84 bars" in sb and REC["nbars"] == 84 and sum(p[1] for p in plan) == 84)
chk("length 2:55", "2:55" in nv and "2:55" in sb and abs(REC["seconds"] - 175) < 1 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
stop = REC["stop_at"]; bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
stopbars = [i + 1 for i, b in enumerate(REC["bars"]) if stop <= b["start"] < 81 * 0 + REC["bars"][80]["start"]]
chk("the stop: bars 79-80", stopbars == [79, 80], str(stopbars))
rec = ["N.C." if i + 1 in stopbars else b["chord"] for i, b in enumerate(REC["bars"])]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = lambda c: "N.C." if c.startswith("r") else {"d": "D", "g": "G", "f": "F", "a": "A", "c": "C", "bes": "Bb"}[re.match(r"[a-g](es)?", c).group(0)] + ("m" if c.endswith(":m") else "5" if c.endswith(":1.5") else "")
chk("chords: lead sheet = record (N.C. at the stop)", [LYC(c) for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"D Dorian": {"1m": "Dm", "4": "G", "♭3": "F", "5m": "Am", "♭7": "C", "1⁵": "D5"}, "F major": {"1": "F", "4": "Bb", "5": "C", "6m": "Dm"}}
cells = re.findall(r"<td>(1m|1⁵|♭3|♭7|5m|6m|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == 84 and all(NUMK[b["key"]][c] == b["chord"] for c, b in zip(cells, REC["bars"])), f"{len(cells)} bars")
chk("Nashville marks the stop and the B♭4", "STOP · voice alone" in nv and "SCORE: B♭4" in nv and "bars 79–80" in nv)
SBC = {"Dm": "Dm", "G": "G", "F": "F", "Am": "Am", "C": "C", "B♭": "Bb", "N.C.": "N.C."}
rows = re.findall(r"^\| ((?:(?:[A-G]♭?m?|N\.C\.) · )*(?:[A-G]♭?m?|N\.C\.)) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [rec[i] for i, b in enumerate(REC["bars"]) if b["sec"] == s]
    for i, (_, l) in enumerate(ls):
        pair = tuple(sb_[2 * i:2 * i + 2]); want.setdefault(l, set()).add(pair if len(set(pair)) > 1 else pair[:1])
def row_ok(a, l):
    return tuple(SBC[x] for x in a.split(" · ")) in want.get(re.sub(r"\*\*", "", l), set())
chk("chords: songbook rows = record", rows and all(row_ok(a, l) for a, l in rows), f"{len(rows)} rows; bad: {[l for a, l in rows if not row_ok(a, l)][:3]}")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
chk("words: the voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG))))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace("’", "'").replace("**", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq),
    str([l for l in uniq if strip(l) not in strip(sb)][:2]))
chk("the turn: the last line is 'and you were never either or'", L.SUNG[-1] == "and you were never either or" and L.SUNG.count("the wind was never either or") == 3)
lead = REC["lead"]
chk("voice F3-A4, B♭4 once on SCORE (refrain 4)", min(n["midi"] for n in lead) == 53 and [(n["syl"][0], n["sec"]) for n in lead if n["midi"] > 69] == [("score", "Refrain 4")])
h = [n for n in lead if n["midi"] == 70][0]
chk("SCORE on B♭4 over B♭ at the downbeat of bar 78", REC["bars"].index(bar_of(h["on"])) + 1 == 78 and bar_of(h["on"])["chord"] == "Bb" and h["on"] == bar_of(h["on"])["start"])
sc = [n for n in lead if n["syl"][0] == "score" and n["sec"] != "Refrain 4"]
chk("SCORE on F4 over B♭ in refrains 1-3", len(sc) == 3 and all(n["midi"] == 65 and bar_of(n["on"])["chord"] == "Bb" for n in sc))
ors = [n for n in lead if n["syl"][0] == "or" and n["line"] == 3]
chk("OR on C4 (a tone of C) at every refrain's end", len(ors) == 4 and all(n["midi"] == 60 for n in ors))
ref = lambda s: [(n["on"] - min(x["on"] for x in lead if x["sec"] == s), n["midi"]) for n in lead if n["sec"] == s]
r1 = ref("Refrain 1")
chk("refrains 2-3 copy refrain 1", ref("Refrain 2") == r1 and ref("Refrain 3") == r1)
r4 = ref("Refrain 4")
chk("refrain 4 = refrain 1 but SCORE raised; the turn on the title line's notes", [p for _, p in r4] == [70 if (n["syl"][0] == "score") else p for (_, p), n in zip(r1, [n for n in lead if n["sec"] == "Refrain 4"])]
    and [o for o, _ in r4] == [o for o, _ in r1])
band = REC["g1"] + REC["g2"] + REC["bass"] + REC["organ"] + REC["drums"]
chk("the stop: no band note sounds in bars 79-80", not [e for e in band if e["on"] < REC["bars"][80]["start"] and e["on"] + e["dur"] > stop], "")
lastline = [n for n in lead if n["sec"] == "Refrain 4" and n["line"] == 3]
chk("the last line sung inside the stop", all(stop - 2 <= n["on"] < REC["bars"][80]["start"] for n in lastline) and lastline[1]["on"] >= stop)
od = [e for e in band if bar_of(e["on"])["sec"] == "Outro"]
chk("outro: D and A only, no third, no drums", od and all(p % 12 in (2, 9) for e in od for p in e["p"]) and not [e for e in REC["drums"] if bar_of(e["on"])["sec"] == "Outro"])
vb = [n["midi"] % 12 for n in lead if n["sec"].startswith("Verse")]; rb = [n["midi"] % 12 for n in lead if n["sec"].startswith("Refrain")]
chk("B natural in the verses' melody, B♭ only in the refrains", 11 in vb and 10 not in vb and 11 not in rb)
gaps = sorted(lead, key=lambda n: n["on"])
chk("an eighth's breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 1 for a, b in zip(gaps, gaps[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
chk("guitar 2 tacet in verse 1 and the build", not [e for e in REC["g2"] if bar_of(e["on"])["sec"] in ("Verse 1", "Build")])
chk("organ drone F-C under every refrain", sorted(REC["bars"].index(bar_of(e["on"])) + 1 for e in REC["organ"] if e["p"] == [41, 48]) == [17, 33, 65, 73])
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
chk("MIDI notes per track = the record", tn.get("Guitar 1") == cnt("g1") and tn.get("Guitar 2") == cnt("g2") and tn.get("Bass (fretless)") == cnt("bass")
    and tn.get("Organ") == cnt("organ") and tn.get("Drums") == cnt("drums") and tn.get("Guide vocal (clarinet - reed fallback)") == len(lead), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
pcm = re.findall(r"\\chordmode \{ (.*?) \}", pt, re.S)
chk("parts: N.C. at the stop on every pitched part's chord line", len(pcm) >= 4 and all(" r4*8 " in c_ for c_ in pcm), str([" r4*8 " in c_ for c_ in pcm]))
chk("songbook carries the production notes", all(h_ in sb for h_ in ("## Lyric sheet", "## Production brief", "## Session notes", "## Score and parts")))
chk("songbook lists the band parts", "Band parts (9 pages)" in sb)
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
