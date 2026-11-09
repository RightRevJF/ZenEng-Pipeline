"""Document consistency check for 'I Took Him for the Gardener' (an Easter concert solo: one high voice, piano, cello, strings; 6/8 at
dotted quarter = 52, the last refrain 48 and the coda 44; D minor, D major from MARY; soprano and mezzo editions; the songbook for
musicians, with the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p32"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p32/song_record.pkl", "rb"))
O = "/home/claude/p32/out/I Took Him for the Gardener - "
ly = open(O + "lead sheet (soprano).ly").read(); lym = open(O + "lead sheet (mezzo).ly").read(); sc = open(O + "full score.ly").read()
nv = open("/home/claude/p32/out/nashville.html").read(); sb = open("/home/claude/p32/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, bool(ok), d))
T = "I Took Him for the Gardener"
chk("title in all", all(T in d for d in (ly, lym, sc, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Words and music: Jason Bryant" in d for d in (ly, lym, sc, nv, sb, docx)))
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
chk("6/8 throughout", set(tsig) == {"6/8"} and "\\time 6/8" in ly and "\\time 6/8" in sc)
chk("tempo: MIDI in quarters 78, 72 from refrain 3, 66 in the coda; written dotted-quarter 52/48/44", tmp == [72 if p[0] == "Refrain 3" else (66 if p[0] == "Coda" else 78) for p in plan]
    and "\\tempo 4. = 52" in ly and "4. = 48" in ly and "4. = 44" in ly and "♩. = 52" in sb and "♩. = 48" in sb and "♩. = 52" in nv)
mb = REC["mary"]["bar"]
chk("keys: D minor to bar 54, D major from bar 55 (MARY); mezzo B minor / B major", ks[:len(plan)] == ["Dm" if p[0] not in ("Verse 4", "Refrain 3", "Coda") else "D" for p in plan] and ks[-1] == "D"
    and mb == 55 and REC["bars"][53]["key"] == "D minor" and REC["bars"][54]["key"] == "D major"
    and "\\key d \\minor" in ly and "\\key d \\major" in ly and "\\key b \\minor" in lym and "\\key b \\major" in lym and "bar 55" in sb)
chk("82 bars", "82 bars" in nv and "82 bars" in sb and REC["nbars"] == 82 and sum(p[1] for p in plan) == 82)
chk("length 3:13", "3:13" in nv and "3:13" in sb and round(REC["seconds"]) == 193 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
LYC = {"d2.:m": "Dm", "g2.:m": "Gm", "bes2.": "Bb", "f2.": "F", "c2.": "C", "a2.": "A", "d2.": "D", "g2.": "G", "b2.:m": "Bm", "e2.:m": "Em", "r2.": "N.C."}
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
chk("chords: lead sheet = record", [LYC[c] for c in cm] == rec, f"{len(cm)} bars")
MZ = {"b2.:m": "Dm", "e2.:m": "Gm", "g2.": "Bb", "d2.": "F", "a2.": "C", "fis2.": "A", "b2.": "D", "e2.": "G", "gis2.:m": "Bm", "cis2.:m": "Em", "r2.": "N.C."}
cmz = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", lym, re.S).group(1).split()
chk("chords: mezzo lead sheet = record a minor third lower", [MZ[c] for c in cmz] == rec)
NUMK = {"D minor": {"1m": "Dm", "4m": "Gm", "♭6": "Bb", "♭3": "F", "♭7": "C", "5": "A", "N.C.": "N.C."}, "D major": {"1": "D", "4": "G", "5": "A", "6m": "Bm", "2m": "Em"}}
cells = re.findall(r"<td>(1m|4m|♭6|♭3|♭7|N\.C\.|6m|2m|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == 82 and all(NUMK[b["key"]][c] == b["chord"] for c, b in zip(cells, REC["bars"])), f"{len(cells)} bars")
SBC = {"Dm": "Dm", "Gm": "Gm", "B♭": "Bb", "F": "F", "C": "C", "A": "A", "D": "D", "G": "G", "Bm": "Bm", "Em": "Em", "N.C.": "N.C."}
rows = re.findall(r"^\| ((?:(?:[A-G]♭?m?|N\.C\.) · )+(?:[A-G]♭?m?|N\.C\.)) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    bs = [b["chord"] for b in REC["bars"] if b["sec"] == s]; at = 0
    for i, (_, l) in enumerate(ls):
        nb = 4 if (s, i) in (("The Name", 3), ("Refrain 3", 4)) else 2
        want.setdefault(re.sub(r"\*", "", l), set()).add(tuple(bs[at:at + nb])); at += nb
def row_ok(a, l): return tuple(SBC[x] for x in a.split(" · ")) in want.get(re.sub(r"\*", "", l), set())
lyric_rows = [(a, l) for a, l in rows if re.sub(r"\*", "", l) in want]
chk("chords: songbook rows = record", len(lyric_rows) == 29 and all(row_ok(a, l) for a, l in lyric_rows), f"{len(lyric_rows)} rows; bad: {[l for a, l in lyric_rows if not row_ok(a, l)][:3]}")
for nm_, src_ in (("soprano", ly), ("mezzo", lym)):
    m = re.search(r'\\lyricsto "voc" \{ (.*?) \}\n', src_, re.S).group(1)
    words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
    chk(f"words: the {nm_} voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG))))
uniq = list(dict.fromkeys(L.SUNG)); strip = lambda t: t.replace("’", "'").replace("*", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq), str([l for l in uniq if strip(l) not in strip(sb)][:2]))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: no Easter cliché sung", not bad, str(bad))
lead = REC["lead"]
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
bno = lambda o: REC["bars"].index(bar_of(o)) + 1
top = [n for n in lead if n["midi"] >= 81]
chk("A5 once, on EARTH over D at the downbeat of bar 72", [(n["syl"][0], n["midi"], bno(n["on"]), bar_of(n["on"])["chord"], n["on"] == bar_of(n["on"])["start"]) for n in top] == [("earth", 81, 72, "D", True)])
chk("voice D4 and up; nothing above G5 but the one A5", min(n["midi"] for n in lead) == 62 and max(n["midi"] for n in lead if n["midi"] != 81) == 79)
cell = [n["midi"] for n in lead if n["sec"] == "Refrain 1" and n["line"] == 0]
g = [n for n in lead if n["sec"] == "Refrain 1" and n["line"] == 0 and n["syl"][2]][-1]
chk("the title cell: F4 A4 G4 A4 C5 D5 D5 D5; GAR on D5 over Bb at bar 14's downbeat; refrain 2 the same", cell == [65, 69, 67, 69, 72, 74, 74, 74] and bno(g["on"]) == 14 and bar_of(g["on"])["chord"] == "Bb"
    and g["on"] == bar_of(g["on"])["start"] and [n["midi"] for n in lead if n["sec"] == "Refrain 2" and n["line"] == 0] == cell)
r1 = [(n["on"] - REC["bars"][12]["start"], n["midi"], n["dur"]) for n in lead if n["sec"] == "Refrain 1"]; r2 = [(n["on"] - REC["bars"][28]["start"], n["midi"], n["dur"]) for n in lead if n["sec"] == "Refrain 2"]
chk("refrain 2 = refrain 1 (but the held last note)", [x[:2] for x in r1] == [x[:2] for x in r2] and [x[2] for x in r1[:-1]] == [x[2] for x in r2[:-1]])
ok = True
for s_ in ("Verse 1", "Verse 2", "Verse 3"):
    l0 = [n["midi"] for n in lead if n["sec"] == s_ and n["line"] == 0]
    ok &= [65, 69, 67] == ([x for x in l0 if x >= 65][:3]) and l0[-1] == 65 and max(l0) == 70
chk("the seed: verses 1-3 open F A G (A) and fall to F4 after B-flat4", ok)
dawn = [n for n in lead if n["sec"] in ("Refrain 1", "Refrain 2") and n["line"] == 1 and n["syl"][0] == "dawn"]
gone = [n for n in lead if n["sec"] in ("Refrain 1", "Refrain 2") and n["line"] == 3 and n["syl"][0] == "gone"]
chk("DAWN on A4 over F; GONE on A4 over A (refrains 1-2)", all(n["midi"] == 69 and bar_of(n["on"])["chord"] == "F" for n in dawn) and all(n["midi"] == 69 and bar_of(n["on"])["chord"] == "A" for n in gone) and len(dawn) == len(gone) == 2)
nc = REC["nc_bar"]; name = next(n for n in lead if n["sec"] == "The Name" and n["syl"][0] == "name")
chk("NAME (bar 54): A4, the ensemble silent, N.C. in every chart", bno(name["on"]) == 54 and name["midi"] == 69 and bno(nc) == 54 and not [e for e in REC["pno"] + REC["cello"] + REC["strings"] if nc <= e["on"] < nc + 6]
    and REC["bars"][53]["chord"] == "N.C." and "r2." in cm and "N.C." in nv and "Gm · N.C." in sb)
mary = [n for n in lead if n["syl"][0] == "mary"]
fs_before = [n for n in lead if n["midi"] % 12 == 6 and n["on"] < mary[0]["on"]]
fs_acc = [e for e in REC["pno"] + REC["cello"] + REC["strings"] if e["on"] < mary[0]["on"] and any(p % 12 == 6 for p in e["p"])]
chk("MARY: F#5 over D at bar 55's downbeat, the first F# anywhere; D major arrives with everyone", [n["midi"] for n in mary] == [78, 78] and bno(mary[0]["on"]) == 55 and bar_of(mary[0]["on"])["chord"] == "D"
    and not fs_before and not fs_acc and all(any(e["on"] == mary[0]["on"] for e in REC[k]) for k in ("pno", "cello", "strings")))
rb = [n for n in lead if n["syl"][0] == "rabboni"]
chk("RABBONI: A4 to E5 over A (bar 58)", [n["midi"] for n in rb] == [69, 76, 76] and bno(rb[1]["on"]) == 58 and bar_of(rb[1]["on"])["chord"] == "A")
was = [n for n in lead if n["sec"] == "Refrain 3" and n["line"] == 4][-1]
hush = REC["hush_bar"]
chk("the close: WAS on D5 over D (bar 78), after bar 77 where the strings alone hold A", was["syl"][0] == "was" and was["midi"] == 74 and bno(was["on"]) == 78 and bar_of(was["on"])["chord"] == "D"
    and bno(hush) == 77 and not [n for n in lead if hush <= n["on"] < hush + 4] and not [e for e in REC["cello"] if hush <= e["on"] < hush + 6]
    and not [e for e in REC["pno"] if hush <= e["on"] < hush + 6] and [e for e in REC["strings"] if e["on"] == hush])
v4 = max(n["midi"] for n in lead if n["sec"] == "Verse 4")
chk("verse 4 climbs to F#5 (ANSWERED, bar 65)", v4 == 78 and bno(next(n for n in lead if n["sec"] == "Verse 4" and n["midi"] == 78)["on"]) == 65)
il = [e for e in REC["cello"] if e.get("art") == "interlude"]
r1n = [n for n in lead if n["sec"] == "Refrain 1" and n["line"] in (0, 1)]; d = REC["bars"][36]["start"] - REC["bars"][12]["start"]
diff = [e for e in il if not any(e["on"] == n["on"] + d and e["p"] == [n["midi"] - 12] for n in r1n)]
chk("the interlude: refrain lines 1-2 an octave lower, ONE note changed (DAWN C#4 for A3, bar 40, over A)", il and len(diff) == 1 and diff[0]["p"] == [61] and bno(diff[0]["on"]) == 40
    and bar_of(diff[0]["on"])["chord"] == "A" and REC["varied"]["was"] == 57 and "C♯4" in sb)
ans = REC["answers"]; lines_ = {}
for n in lead: lines_.setdefault((n["sec"], n["line"]), []).append(n)
ok = len(ans) == 4 and all([e["p"][0] for e in REC["cello"] if e.get("art") == "answer" and a["on"] <= e["on"] < a["on"] + 3] == [x["midi"] - 12 for x in lines_[(a["sec"], a["line"])][-3:]] for a in ans)
ok &= sorted(bno(a["on"]) for a in ans) == [24, 26, 28, 44] and "bars 24, 26, 28, 44" in sb
chk("the cello answers (4): each line's last three notes an octave below; bars 24, 26, 28, 44 as the songbook says", ok, f"{len(ans)} answers")
CP = [e for e in REC["pno"] if e.get("art") == "coda"]
r3t = [n["midi"] for n in lead if n["sec"] == "Refrain 3" and n["line"] == 0]
lastc = max(REC["pno"], key=lambda e: e["on"])
chk("the coda: the piano states refrain 3's title notes; the last chord D add E with A4 on top", [e["p"][0] for e in CP] == r3t == [66, 69, 67, 69, 73, 74, 74, 74] and max(lastc["p"]) == 69
    and sorted({p % 12 for p in lastc["p"]}) == [2, 4, 6, 9] and CP[0]["on"] >= max(n["on"] + n["dur"] for n in lead))
chk("the ossia: F#5 over EARTH (soprano), D#5 (mezzo); both editions present", 'alignAboveContext = #"vstaff"' in ly and "fis''" in ly.split("alignAboveContext")[1][:500]
    and 'alignAboveContext = #"vstaff"' in lym and "dis''" in lym.split("alignAboveContext")[1][:500] and "mezzo edition" in lym and "F♯5 ossia" in sb)
chk("spelling from the key: C# (not D-flat) in D minor; A# in the mezzo's B minor", "des" not in re.sub(r"\\[a-z]+", "", ly.split("\\new Voice")[1].split("}")[0]) and "ais" in lym)
PR = pickle.load(open("/home/claude/p32/out/parts_report.pkl", "rb"))
chk("parts: piano, cello, strings read back against the record", all(PR["readback"].values()), str(PR["readback"]))
gaps = sorted(lead, key=lambda n: n["on"])
chk("a breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 1 for a, b in zip(gaps, gaps[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
chk("MIDI notes per track = the record", tn.get("Piano") == cnt("pno") and tn.get("Cello") == cnt("cello") and tn.get("Strings") == cnt("strings") and tn.get("Guide vocal (flute)") == len(lead), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("full score: every staff present", all(x in sc for x in ('instrumentName = "Voice"', 'instrumentName = "Piano"', 'instrumentName = "Cello"', 'instrumentName = "Strings"')))
chk("songbook carries the production notes and the one-sheet", all(h_ in sb for h_ in ("## Lyric sheet", "## Producer one-sheet", "## Production brief", "## Session notes", "## Score and parts")) and "Producer one-sheet" in docx)
DR = pickle.load(open("/home/claude/p32/out/demo_report.pkl", "rb")); E_ = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("demo: stems >= +3 dB; each refrain above its verse; the last refrain the top", DR["stems_db"] >= 3 and E_["Refrain 1"] > E_["Verse 1"] and E_["Refrain 2"] > E_["Verse 2"] and E_["Refrain 3"] > E_["Verse 4"]
    and E_["Refrain 3"] == max(E_.values()), f"{DR['stems_db']:+.1f} dB")
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
