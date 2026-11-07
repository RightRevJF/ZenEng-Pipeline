"""v43 document consistency check for 'Five-Oh-One' (one tenor and a gang; a funk-pop band; Eb major -> F major; 4/4 at q = 112 on
sixteenths; the songbook for musicians, with the production notes)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p26"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p26/song_record.pkl", "rb"))
O = "/home/claude/p26/out/Five-Oh-One - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p26/out/nashville.html").read(); sb = open("/home/claude/p26/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook and production notes.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("Five-Oh-One" in d for d in (ly, nv, sb, docx)))
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
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre 4/4 at q = 112", set(tsig) == {"4/4"} and set(tmp) == {112} and "\\time 4/4" in ly and "\\tempo 4 = 112" in ly and "♩ = 112" in nv and "♩ = 112" in sb)
keyof = {p[0]: REC["bars"][p[2]]["key"] for p in plan}
chk("keys: Eb major to the lift, F major from chorus 3", ks == [{"Eb major": "Eb", "F major": "F"}[keyof[p[0]]] for p in plan] and "\\key ees \\major" in ly
    and "\\key f \\major" in ly and keyof["Chorus 3"] == "F major" and keyof["Lift"] == "Eb major")
chk("88 bars", "88 bars" in nv and "88 bars" in sb and REC["nbars"] == 88 and sum(p[1] for p in plan) == 88)
chk("length 3:09", "3:09" in nv and "3:09" in sb and round(REC["seconds"]) == 189 and abs(mid.length - REC["seconds"]) < 4, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\new ChordNames \\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
LYC = {"ees": "Eb", "aes": "Ab", "bes": "Bb", "c:m": "Cm", "g:m": "Gm", "c": "C", "f": "F", "d:m": "Dm"}
chk("chords: lead sheet = record", [LYC[c.replace("1", "")] for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"Eb major": {"1": "Eb", "4": "Ab", "5": "Bb", "6m": "Cm", "3m": "Gm", "6": "C"}, "F major": {"1": "F", "4": "Bb", "5": "C", "6m": "Dm"}}
cells = re.findall(r"<td>(6m|3m|1|4|5|6)(?:\s|<)", nv)
chk("chords: Nashville = record", len(cells) == len(rec) and all(NUMK[b["key"]][c] == b["chord"] for c, b in zip(cells, REC["bars"])), f"{len(cells)} bars")
SBC = {"E♭": "Eb", "A♭": "Ab", "B♭": "Bb", "Cm": "Cm", "C": "C", "F": "F", "Dm": "Dm"}
rows = re.findall(r"^\| ((?:[A-G]♭?m? · )+[A-G]♭?m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l.replace("'", "'"), set()).add(tuple(sb_[2 * i:2 * i + 2]))
def row_ok(a, l):
    l = re.sub(r"\*\*", "", l); l = re.sub(r" \((band|everybody)[^)]*\)", "", l).replace("(everybody) ", "")
    l2 = l.lower().replace("five-oh-one!", "five-oh-one") if "FIVE-OH-ONE" in l else l
    return tuple(SBC[x] for x in a.split(" · ")) in want.get(l2.replace("FIVE-OH-ONE!", "five-oh-one"), set())
chk("chords: songbook rows = record", rows and all(row_ok(a, l) for a, l in rows), f"{len(rows)} rows; bad: {[l for a, l in rows if not row_ok(a, l)][:3]}")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', "").replace("“", "").replace("”", ""))
chk("words: the voice staff = every sung line in order", "".join(words) == "".join(norm(" ".join(L.SUNG).replace('"', ""))))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace('"', "").replace("“", "").replace("”", "").replace("’", "'").replace("**", "").lower()
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung (the party never named)", not bad, str(bad))
lead = REC["lead"]
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
him = [n for n in lead if n["singer"] == "him"]
chk("voice Eb3-A4, Bb4 once on HERE (chorus 4)", min(n["midi"] for n in him) >= 50 and [(n["syl"][0], n["sec"]) for n in lead if n["midi"] > 69] == [("here", "Chorus 4")])
h = [n for n in lead if n["midi"] == 70][0]
chk("HERE on Bb4 over Bb, beat 4, held across the C bar", bar_of(h["on"])["chord"] == "Bb" and h["on"] - bar_of(h["on"])["start"] == 12 and h["on"] + h["dur"] > bar_of(h["on"])["start"] + 16)
cells_ok = True
for s in ("Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4"):
    for li in (0, 1, 3):
        ns = [n for n in lead if n["sec"] == s and n["line"] == li][:3]
        tr = 2 if s in ("Chorus 3", "Chorus 4") else 0
        st = ns[0]["on"]
        cells_ok &= [n["on"] - st for n in ns] == [0, 3, 4] and [n["midi"] for n in ns] == [58 + tr, 63 + tr, 67 + tr] and st == bar_of(st)["start"]
chk("the title cell on every 'five-oh-one' chorus line (downbeat; 0-3-4; Bb3-Eb4-G4 / C4-F4-A4)", cells_ok)
hk = [n for n in lead if n["sec"].startswith("Hook") or n["sec"] == "Outro"]
chk("the hook chant: tresillo 0-3-6-9-12-14-16 every line", all([n["on"] - ns_[0]["on"] for n in ns_] == [0, 3, 6, 9, 12, 14, 16]
    for ns_ in [[n for n in hk if (n["sec"], n["line"]) == k] for k in {(n["sec"], n["line"]) for n in hk}]))
sh = [n for n in lead if n["singer"] == "gang"]
chk("the gang's FIVE-OH-ONE over C in the lift (beats 1, 2, 3)", [n["syl"][0] for n in sh] == ["five", "oh", "one"] and all(bar_of(n["on"])["chord"] == "C" for n in sh)
    and [n["on"] - bar_of(n["on"])["start"] for n in sh] == [0, 4, 8])
gaps = sorted(lead, key=lambda n: n["on"])
chk("an eighth's breath before every line", all(b["on"] - (a["on"] + a["dur"]) >= 2 for a, b in zip(gaps, gaps[1:]) if (a["sec"], a["line"]) != (b["sec"], b["line"])))
bk = [n for n in lead if n["sec"] == "Breakdown" and n["syl"][0] == "clap"]
chk("breakdown: four CLAPs, each answered by three claps", len(bk) == 4 and all(sum(1 for c_ in REC["claps"] if n["on"] < c_["on"] <= n["on"] + 6) == 3 for n in bk))
chk("breakdown: the kit out (kick on 1 only)", all(d["p"] == [36] and d["on"] == bar_of(d["on"])["start"] for d in REC["drums"] if bar_of(d["on"])["sec"] == "Breakdown"))
tn = {next(mm.name for mm in t if mm.type == "track_name"): sum(1 for mm in t if mm.type == "note_on" and mm.velocity > 0) for t in mid.tracks[1:]}
chk("MIDI notes per track = the record", tn.get("Drums and claps") == sum(len(e["p"]) for e in REC["drums"] + REC["claps"]) and tn.get("Bass") == sum(len(e["p"]) for e in REC["bass"])
    and tn.get("Guitar (scratch)") == sum(len(e["p"]) for e in REC["gtr"]) and tn.get("Electric piano") == sum(len(e["p"]) for e in REC["keys"])
    and tn.get("Horns") == sum(len(e["p"]) for e in REC["horns"]), str(tn))
chk("MIDI track names ASCII", all(n.isascii() for n in tn) and REC["title"].isascii())
chk("songbook carries the production notes", all(h_ in sb for h_ in ("## Lyric sheet", "## Production brief", "## Session notes", "## Score and parts")))
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
