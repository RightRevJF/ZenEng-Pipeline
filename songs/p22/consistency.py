"""v43 document consistency check for 'The Seam' (a duet; keys by section; 4/4 and 7/8 at q = 80; the instrumental lines; the songbook for musicians)."""
import re, pickle, mido, subprocess, sys
sys.path[:0] = ["/home/claude/p22"]
import lyric as L, intake as I
REC = pickle.load(open("/home/claude/p22/song_record.pkl", "rb"))
O = "/home/claude/p22/out/The Seam - "
ly = open(O + "lead sheet.ly").read(); nv = open("/home/claude/p22/out/nashville.html").read(); sb = open("/home/claude/p22/songbook.md").read()
docx = subprocess.run(["pandoc", O + "Songbook.docx", "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout.replace("’", "'")
mid = mido.MidiFile(O + "demo (General MIDI).mid"); t0 = mid.tracks[0]
norm = lambda t: re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("—", " ").replace("-", " ")).split()
checks = []
def chk(n, ok, d=""): checks.append((n, ok, d))
chk("title in all", all("The Seam" in d for d in (ly, nv, sb, docx)))
chk("credit 'Words and music: Jason Bryant' in all", all("Jason Bryant" in d for d in (ly, nv, sb, docx)))
ENG = r"zeneng|\bengine\b|\bmodule\b|certificate|surviv|composite|table g|\bv\d\d\b|realness|10\.20|search|fingerprint"   # ("floor" is the lyric's own word)
chk("songbook and chart for musicians: no engine terms (the writer, 5 Nov)", not re.search(ENG, sb.lower()) and not re.search(ENG, docx.lower()) and not re.search(ENG, nv.lower()),
    str(re.findall(ENG, sb.lower() + docx.lower() + nv.lower())[:5]))
markers, tsig, tmp, ks = [], [], [], []
for m in t0:
    if m.type == "marker": markers.append(m.text)
    if m.type == "time_signature": tsig.append(f"{m.numerator}/{m.denominator}")
    if m.type == "set_tempo": tmp.append(round(mido.tempo2bpm(m.tempo)))
    if m.type == "key_signature": ks.append(m.key)
plan = REC["plan"]
chk("form (MIDI markers = record plan)", markers == [p[0] for p in plan])
chk("metre 4/4 and 7/8 (the instrumental), q = 80", tsig == [p[3] for p in plan] and set(tmp) == {80} and "\\time 2,2,3 7/8" in ly and "\\tempo 4 = 80" in ly and "♩ = 80" in nv and "♩ = 80" in sb)
KM = {"E minor": "Em", "F minor": "Fm", "C major": "C"}
chk("keys by section (MIDI = record = lead sheet)", ks == [KM[REC["bars"][p[2]]["key"]] for p in plan] and all(k in ly for k in ("\\key e \\minor", "\\key f \\minor", "\\key c \\major")))
chk("130 bars", "130 bars" in nv and "130 bars" in sb and REC["nbars"] == 130 and sum(p[1] for p in plan) == 130)
chk("length 6:12", "6:12" in nv and "6:12" in sb and round(REC["seconds"]) == 372, f"record {REC['seconds']:.1f}s, MIDI {mid.length:.1f}s")
rec = [b["chord"] for b in REC["bars"]]
cm = re.search(r"\\chordmode \{ (.*?) \}", ly, re.S).group(1).split()
CHR = {"e": "Em", "c": "C", "a": "Am", "g": "G", "f": None, "des": "Db", "bes": "Bbm"}
def lyc(t):
    root, rest = re.match(r"([a-g](?:es|is)?)(.*)", t).groups(); minor = ":m" in rest
    return {"e": "Em", "c": "C", "a": "Am", "g": "G", "des": "Db", "bes": "Bbm"}.get(root) if root != "f" else ("Fm" if minor else "F")
chk("chords: lead sheet = record", [lyc(c) for c in cm] == rec, f"{len(cm)} bars")
NUMK = {"E minor": {"1m": "Em", "♭6": "C", "4m": "Am"}, "F minor": {"1m": "Fm", "♭6": "Db", "4m": "Bbm", "5": "C", "1": "F"}, "C major": {"1": "C", "5": "G", "6m": "Am", "4": "F"}}
cells = re.findall(r"<td>(1m|♭6|4m|6m|1|4|5)(?:\s|<)", nv)
keys_by_bar = [b["key"] for b in REC["bars"]]
chk("chords: Nashville = record (numbers in each section's key)", len(cells) == len(rec) and all(NUMK[k][c] == r for c, k, r in zip(cells, keys_by_bar, rec)), f"{len(cells)} bars")
SB = {"Em": "Em", "C": "C", "Am": "Am", "G": "G", "F": "F", "Fm": "Fm", "D♭": "Db", "B♭m": "Bbm"}
rows = re.findall(r"^\| ([A-G][♭]?m?) · ([A-G][♭]?m?) \| (.+?) \|$", sb, re.M)
want = {}
for s, ls in L.SECTIONS:
    sb_ = [b["chord"] for b in REC["bars"] if b["sec"] == s]
    for i, (_, l) in enumerate(ls): want.setdefault(l, set()).add((sb_[2 * i], sb_[2 * i + 1]))
chk("chords: songbook rows = record", rows and all((SB[a], SB[b]) in want.get(l.replace("’", "'"), set()) for a, b, l in rows), f"{len(rows)} rows")
def words_of(name):
    m = re.search(r"\\lyricsto \"" + name + r"\" \{ (.*?) \}\n", ly, re.S).group(1)
    return norm(re.sub(r" -- ", "", m).replace(" __", "").replace(" _ ", " ").replace('"', ""))
her_lines = [l for s, ls in L.SECTIONS for _, l in ls if L.SINGER[s] in ("her", "both")]
him_lines = [l for s, ls in L.SECTIONS for _, l in ls if L.SINGER[s] in ("him", "both")]
def order_by_time(lines_secs):
    return lines_secs
him_seq = []
for s, ls in L.SECTIONS:
    if L.SINGER[s] in ("him", "both"): him_seq += [l for _, l in ls]
chk("words: her staff = her lines and the choruses", words_of("her") == norm(" ".join(her_lines)))
chk("words: his staff = his lines, the choruses (harmony) and the ending", words_of("him") == norm(" ".join(him_seq)))
uniq = list(dict.fromkeys(L.SUNG))
strip = lambda t: t.replace('"', "").replace("“", "").replace("”", "").replace("’", "'")
chk("words: songbook and Word carry every line", all(strip(l) in strip(sb) for l in uniq) and all(strip(l) in strip(docx) for l in uniq))
bad = [p for l in L.SUNG for p in I.NEVER_SAY + I.NEVER_PHRASES if re.search(r"\b" + re.escape(p) + r"\b", l.lower())]
chk("never-say: neither list sung; no names", not bad and not any(w in " ".join(L.SUNG).lower() for w in ("coda", "reed", "clef", "verse", "tacet")), str(bad))
lead, harm = REC["lead"], REC["harm"]
her = [n for n in lead if n["singer"] == "her"]; him = [n for n in lead if n["singer"] == "him"] + harm
chk("her A3-C5, C5 once on the last WE", min(n["midi"] for n in her) >= 57 and [n["syl"][0] for n in her if n["midi"] > 67] == ["we"] and max(n["midi"] for n in her) == 72)
chk("him E3-A4, A4 once (under her C5)", min(n["midi"] for n in him) >= 52 and [(n["sec"], n["syl"][0]) for n in him if n["midi"] > 67] == [("Chorus 3", "we")])
chk("singers by section: her verses 1 and 3, his 2 and 4, both choruses, his ending", {n["sec"] for n in lead if n["singer"] == "her"} == {"Verse 1", "Verse 3", "Chorus 1", "Chorus 2", "Chorus 3"}
    and {n["sec"] for n in lead if n["singer"] == "him"} == {"Verse 2", "Verse 4", "Ending"})
iv = {n["midi"] - h["midi"] for n, h in zip([x for x in lead if x["sec"].startswith("Chorus")], harm)}
chk("his harmony a third or a sixth under hers", iv <= {3, 4, 8, 9}, str(sorted(iv)))
bar_of = lambda o: next(b for b in REC["bars"] if b["start"] <= o < b["start"] + b["len"])
for sec in ("Chorus 1", "Chorus 2", "Chorus 3"):
    ns = [n for n in lead if n["sec"] == sec and n["line"] == 0]; s_ = ns[1]
    chk(f"{sec}: SEAM on G4 over C, the downbeat, held", s_["syl"][0] == "seam" and s_["midi"] == 67 and bar_of(s_["on"])["chord"] == "C" and s_["on"] == bar_of(s_["on"])["start"] and s_["dur"] >= 3)
we = [n for n in lead if n["syl"][0] == "we" and n["midi"] == 72][0]
chk("the last WE on C5 over F, a downbeat, held", bar_of(we["on"])["chord"] == "F" and we["on"] == bar_of(we["on"])["start"] and we["dur"] >= 4)
fr = [n for n in lead if n["sec"] == "Ending"][-1]
chk("the ending's -FRAID on A3 over F major, held", fr["midi"] == 57 and bar_of(fr["on"])["chord"] == "F" and fr["dur"] >= 4)
gt = REC["gtr"]
chk("the instrumental lines: in every instrumental section, floored", {n["sec"] for n in gt} == {"Intro", "Interlude", "Instrumental", "Outro"}
    and all(all(v[1] for v in REC["gtr_floor"][s].values()) for s in REC["gtr_floor"]))
chk("the cue on the lead sheet (grey, the synth lead named)", '\\new Voice = "syn"' in ly and "cue: synth lead" in ly and "grey35" in ly)
lt = next(tr for tr in mid.tracks if any(m.type == "track_name" and m.name.startswith("Instrumental lead") for m in tr))
nl = sum(1 for m in lt if m.type == "note_on" and m.velocity > 0)
chk("the lead track's notes in the MIDI = the record's", nl == len(gt), f"{nl} vs {len(gt)}")
chk("the cue never overlaps a voice", not any(a["on"] < g["on"] + g["dur"] and g["on"] < a["on"] + a["dur"] for g in gt for a in lead))
chk("the instrumental marked a build (record, chart)", all(b["build"] for b in REC["bars"] if b["sec"] == "Instrumental") and "BUILD" in nv)
for n, ok, d in checks: print(f"{'OK ' if ok else 'XX '} {n}  {d}")
print(f"{sum(ok for _, ok, _ in checks)}/{len(checks)} consistent")
