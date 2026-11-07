"""v43 document consistency check for 'What Holds' (one voice; E minor / G major; 4/4 at q = 104; the riff; the songbook for musicians)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p23"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p23/song_record.pkl", "rb"))
O = "/home/claude/p23/out/What Holds - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p23/out/nashville.html").read(); sb = open("/home/claude/p23/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("What Holds" in d for d in (ly, nv, sb, docx)))
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
chk("metre 4/4 at q = 104", set(tsig) == {"4/4"} and set(tmp) == {104} and "\\tempo 4 = 104" in ly and "♩ = 104" in nv and "♩ = 104" in sb)
KM = {"E minor": "Em", "G major": "G"}
chk("keys by section (MIDI = record = lead sheet)", ks == [KM[REC["bars"][p[2]]["key"]] for p in plan] and all(k in ly for k in ("\\key e \\minor", "\\key g \\major")))
chk("78 bars", "78 bars" in nv and "78 bars" in sb and REC["nbars"] == 78 and sum(p[1] for p in plan) == 78)
chk("length 3:00", "3:00" in nv and "3:00" in sb and round(REC["seconds"]) == 180, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
def lyc(t):
    root, rest = re.match(r"([a-g](?:es|is)?)\d+(.*)", t).groups(); minor = ":m" in rest
    return {"e": "Em", "c": "C", "d": "D", "g": "G", "a": "Am"}[root] if (minor or root in "cdg") else None
chk("chords: lead sheet = record", [lyc(c) for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"E minor": {"1m": "Em", "♭6": "C", "♭7": "D"}, "G major": {"1": "G", "5": "D", "6m": "Em", "4": "C", "2m": "Am"}}
cells = re.findall(r"<td>(1m|♭6|♭7|6m|2m|1|4|5)(?:\s|<)", nv)
keys_by_bar = [b["key"] for b in REC["bars"]]
chk("chords: Nashville = record (numbers in each section's key)", len(cells) == len(rec) and all(NUMK[k][c] == r for c, k, r in zip(cells, keys_by_bar, rec)), f"{len(cells)} bars")
rows = re.findall(r"^\| ((?:[A-G]m? · )+[A-G]m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]; k = 0
    for i, (_, l) in enumerate(ls):
        n = 4 if (s == "Chorus 4" and i == 3) else 2
        want.setdefault(l, set()).add(tuple(sb_[k:k + n])); k += n
chk("chords: songbook rows = record", rows and all(tuple(a.split(" · ")) in want.get(l.replace("’", "'"), set()) for a, l in rows), f"{len(rows)} rows")
m = re.search(r"\\lyricsto \"voc\" \{ (.*?) \}\n", ly, re.S).group(1)
words = norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
chk("words: the staff = every sung line in order", words == norm(" ".join(L.SUNG)))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace('"', "").replace("“", "").replace("”", "").replace("’", "'")
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung", not bad, str(bad))
lead = REC["lead"]
chk("voice E3-A4, A4 once on the last STAND", min(n["midi"] for n in lead) >= 52 and [n["syl"][0] for n in lead if n["midi"] > 67] == ["stand"] and max(n["midi"] for n in lead) == 69)
chk("G4 only on HOLDS and STAND", {n["syl"][0] for n in lead if n["midi"] == 67} <= {"holds", "stand"})
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
for sec in ("Chorus 1", "Chorus 2", "Chorus 3", "Chorus 4"):
    ns = [n for n in lead if n["sec"] == sec and n["line"] == 0]; h = ns[1]
    chk(f"{sec}: HOLDS on G4 over G, the downbeat, held", h["syl"][0] == "holds" and h["midi"] == 67 and bar_of(h["on"])["chord"] == "G" and h["on"] == bar_of(h["on"])["start"] and h["dur"] >= 3)
for sec in ("Chorus 1", "Chorus 2", "Chorus 3"):
    st = [n for n in lead if n["sec"] == sec and n["line"] == 3 and n["syl"][0] == "stand"][0]
    chk(f"{sec}: STAND on G4 over G, a downbeat", st["midi"] == 67 and bar_of(st["on"])["chord"] == "G" and st["on"] == bar_of(st["on"])["start"])
st4 = [n for n in lead if n["sec"] == "Chorus 4" and n["syl"][0] == "stand"][0]; h4 = [n for n in lead if n["sec"] == "Chorus 4" and n["syl"][0] == "holds"][-1]
chk("the turn: STAND on A4 over D, HOLDS on G4 over G, both downbeats, held", st4["midi"] == 69 and bar_of(st4["on"])["chord"] == "D" and st4["on"] == bar_of(st4["on"])["start"]
    and h4["midi"] == 67 and bar_of(h4["on"])["chord"] == "G" and h4["on"] == bar_of(h4["on"])["start"] and h4["dur"] >= 8)
br = [n for n in lead if n["sec"] == "Bridge" and n["syl"][0] == "stand"][0]
chk("the bridge's STAND on F#4 over D, a downbeat", br["midi"] == 66 and bar_of(br["on"])["chord"] == "D" and br["on"] == bar_of(br["on"])["start"])
rf = REC["riff"]
chk("the riff: in the intro, the riff break and the outro, floored", {bar_of(max(0, n["on"] + 1))["sec"] for n in rf} == {"Intro", "Riff", "Outro"}
    and all(v[1] for s in REC["riff_floor"] for v in REC["riff_floor"][s].values()))
chk("the cue on the lead sheet (grey, the riff guitar named)", '\\new Voice = "rif"' in ly and "cue: riff guitar" in ly and "grey35" in ly)
lt = next(tr for tr in mid.tracks if any(mm.type == "track_name" and mm.name.startswith("Instrumental lead") for mm in tr))
nl = sum(1 for mm in lt if mm.type == "note_on" and mm.velocity > 0)
chk("the riff track's notes in the MIDI = the record's", nl == len(rf), f"{nl} vs {len(rf)}")
chk("the riff never overlaps the voice", not any(a["on"] < g["on"] + g["dur"] and g["on"] < a["on"] + a["dur"] for g in rf for a in lead))
chk("the bridge marked a build (record, chart)", all(b["build"] for b in REC["bars"] if b["sec"] == "Bridge") and "BUILD" in nv)
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
