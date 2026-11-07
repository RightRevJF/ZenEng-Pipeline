"""Document consistency check for 'Tinted Glass' (a duet that never sings together; slow-burn soul; Eb major throughout, no key change;
6/8 at dotted-q = 54; the songbook for musicians, with the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p28"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p28/song_record.pkl", "rb"))
O = "/home/claude/p28/out/Tinted Glass - "
ly = open(O + "lead sheet.ly").read(); sc = open(O + "full score.ly").read(); nv = open("/home/claude/p28/out/nashville.html").read()
sb = open("/home/claude/p28/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("Tinted Glass" in d for d in (ly, sc, nv, sb, docx)))
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
chk("6/8 throughout, MIDI q = 81 (dotted-q = 54)", set(tsig) == {"6/8"} and set(tmp) == {81} and "\\time 6/8" in ly and "\\tempo 4. = 54" in ly and "♩. = 54" in nv and "♩. = 54" in sb)
chk("Eb major throughout: no key change anywhere", set(ks) == {"Eb"} and ly.count("\\key") == 2 and "\\key ees \\major" in ly and {b["key"] for b in REC["bars"]} == {"Eb major"})
chk("152 bars", "152 bars" in nv and "152 bars" in sb and REC["nbars"] == 152 and sum(p[1] for p in plan) == 152)
chk("length 5:38", "5:38" in nv and "5:38" in sb and round(REC["seconds"]) == 338 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"ees2.": "Eb", "aes2.": "Ab", "bes2.": "Bb", "c2.:m": "Cm", "f2.:m": "Fm", "g2.:m": "Gm"}
chk("chords: lead sheet = record", [LYC[c] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"1": "Eb", "2m": "Fm", "3m": "Gm", "4": "Ab", "5": "Bb", "6m": "Cm"}
cells = re.findall(r"<td>(2m|3m|6m|1|4|5)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == 152 and [NUMK[c] for c in cells] == rec, f"{len(cells)} bars")
SBC = {"E♭": "Eb", "A♭": "Ab", "B♭": "Bb", "Cm": "Cm", "Fm": "Fm", "Gm": "Gm"}
rows = re.findall(r"^\| ((?:[A-G]♭?m? · )+[A-G]♭?m?) \|(?: (?:Her|Him) \|)? (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    cs = [b["chord"] for b in REC["bars"] if b["sec"] == s]; per = len(cs) // len(ls)
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add(tuple(cs[per * i:per * i + per]))
def row_ok(a, l): return tuple(SBC[x] for x in a.split(" · ")) in want.get(re.sub(r"\*\*", "", l), set())
chk("chords: songbook rows = record", rows and all(row_ok(a, l) for a, l in rows), f"{len(rows)} rows; bad: {[l for a, l in rows if not row_ok(a, l)][:3]}")
for k in ("her", "him"):
    m = re.search(r'\\lyricsto "' + k + r'" \{ (.*?) \}\n', ly, re.S).group(1)
    words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
    sung = [l for s, ls in L.SECTIONS for i, (_, l) in enumerate(ls) if (L.SINGER[s][i] if isinstance(L.SINGER[s], list) else L.SINGER[s]) == k]
    chk(f"words: {k}'s staff = every line {k} sings, in order", "".join(words) == "".join(norm(" ".join(sung))))
uniq = list(dict.fromkeys(L.SUNG)); strip = lambda t: t.replace("’", "'").replace("**", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq), str([l for l in uniq if strip(l) not in strip(sb)][:2]))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung (no job named, no affair cliché)", not bad, str(bad))
lead = REC["lead"]
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
bno = lambda o: REC["bars"].index(bar_of(o)) + 1
him = [n for n in lead if n["singer"] == "him"]; her = [n for n in lead if n["singer"] == "her"]
chk("him C3-Bb3, C4 once on FOG (bar 137, downbeat)", min(n["midi"] for n in him) == 48 and [(n["syl"][0], bno(n["on"]), n["on"] == bar_of(n["on"])["start"]) for n in him if n["midi"] > 58] == [("fog", 137, True)])
chk("her Bb3-Bb4, C5 once on FOG (bar 145, downbeat)", min(n["midi"] for n in her) == 58 and [(n["syl"][0], bno(n["on"]), n["on"] == bar_of(n["on"])["start"]) for n in her if n["midi"] > 70] == [("fog", 145, True)])
srt = sorted(lead, key=lambda n: n["on"])
chk("they never sing at the same time", all(b["on"] >= a["on"] + a["dur"] for a, b in zip(srt, srt[1:]) if a["singer"] != b["singer"]))
chk("singers by section = the lyric's", all(n["singer"] == (L.SINGER[n["sec"]][n["line"]] if isinstance(L.SINGER[n["sec"]], list) else L.SINGER[n["sec"]]) for n in lead))
gl = [n for n in lead if n["syl"][0] == "glass" and n["sec"].startswith("Chorus")]
chk("GLASS on Ab over Ab, each chorus line 1's second downbeat (Ab3 him, Ab4 her)", len(gl) == 4 and all(n["midi"] % 12 == 8 and bar_of(n["on"])["chord"] == "Ab" and n["on"] == bar_of(n["on"])["start"] for n in gl)
    and [n["midi"] for n in gl] == [56, 68, 56, 68])
ends = [[n for n in lead if n["sec"] == s and n["line"] == 3][-1] for s in ("Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4")]
chk("each chorus ends on F over Bb (the half cadence)", all(n["midi"] % 12 == 5 and bar_of(n["on"])["chord"] == "Bb" for n in ends), str([(n["syl"][0], n["midi"]) for n in ends]))
c1 = [n["midi"] for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; c2 = [n["midi"] for n in lead if n["sec"] == "Chorus 2" and n["line"] == 0]
c3 = [(n["on"] - REC["bars"][132]["start"], n["midi"]) for n in lead if n["sec"] == "Chorus 3"]
c4 = [(n["on"] - REC["bars"][140]["start"], n["midi"] - 12) for n in lead if n["sec"] == "Chorus 4"]
chk("her choruses are his tune an octave up (chorus 2's title line; chorus 4 = chorus 3 + 12)", c2 == [p + 12 for p in c1] and c3 == c4)
vl = [n for n in lead if n["sec"].startswith("Verse") or n["sec"] == "Bridge"]
from collections import defaultdict
lines_ = defaultdict(list)
for n in vl: lines_[(n["sec"], n["line"])].append(n)
def line_bar4_free(k):
    s, i = k; st = [b for b in REC["bars"] if b["sec"] == s][4 * i + 3]["start"]
    return all(n["on"] < st for n in lines_[k])
chk("bar 4 of every verse and bridge line: no new sung note (the piano's answer)", all(line_bar4_free(k) for k in lines_))
ans = [e for e in REC["keys"] if e.get("art") == "answer"]
chk("the piano answers in bar 4 of every verse and bridge line", len({bno(e["on"]) for e in ans}) == len(lines_))
chk("no drums in the intro, verse 1 or the outro", not [d for d in REC["drums"] if bar_of(d["on"])["sec"] in ("Intro", "Verse 1", "Outro")])
chk("the outro: electric piano alone", {k for k in ("bass", "organ", "drums") if any(bar_of(e["on"])["sec"] == "Outro" for e in REC[k])} == set())
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
cnt = lambda k: sum(len(e["p"]) for e in REC[k])
chk("MIDI notes per track = the record", tn.get("Electric piano") == cnt("keys") and tn.get("Bass") == cnt("bass") and tn.get("Organ") == cnt("organ")
    and tn.get("Drums (brushes)") == cnt("drums") and tn.get("Guide vocal - him (clarinet)") == len(him) and tn.get("Guide vocal - her (flute)") == len(her), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("full score: every staff present", all(x in sc for x in ('instrumentName = "Her"', 'instrumentName = "Him"', "Electric piano", 'instrumentName = "Bass"', 'instrumentName = "Organ"', "DrumStaff")))
chk("songbook carries the production notes", all(h_ in sb for h_ in ("## Lyric sheet", "## Production brief", "## Session notes", "## Score and parts")))
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
