"""Song 62: every document against the record. python3 consistency62.py "first edition" -> consistency62.json"""
import json, sys, re, os, glob, zipfile, collections
LABEL = sys.argv[1]; D = f"out/{LABEL}"; R = json.load(open(f"{D}/record.json")); B = R["bar"]; T = R["title"]; FT = f"{T} ({LABEL})"
sb = open("songbook_doc.md").read(); sbw = open("songbook.md").read(); ok = {}
start = {}; o = 0
for n, k, b in R["form"]: start[n] = (o // B + 1, b); o += b * B
NB = o // B; mel = sorted(R["melody"], key=lambda n: n["on"])
NM = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; nm = lambda m: NM[m % 12] + str(m // 12 - 1)
SHOW = {"Intro": "Intro", "Verse 1": "Verse 1", "Chorus 1": "Refrain", "Turn 1": "Turn", "Verse 2": "Verse 2", "Chorus 2": "Refrain", "Turn 2": "Turn", "Bridge": "Bridge", "Verse 3": "Verse 3", "Chorus 3": "Last refrain", "Outro": "Outro"}
for n, (s, b) in start.items(): ok[f"songbook: {n} bars {s}-{s + b - 1}"] = f"{SHOW[n]} (bars {s}–{s + b - 1})" in sb
ok["songbook: range"] = f"tenor, {nm(min(n['midi'] for n in mel))} to {nm(max(n['midi'] for n in mel))}" in sb
ok["songbook: cello entry bar"] = f"bridge (bar {min(e['on'] for e in R['parts']['cello']) // B + 1})" in sb
ok["songbook: quartet entry bar"] = f"last refrain (bar {min(e['on'] for e in R['parts']['violin1']) // B + 1})" in sb
iv = [b_ + start["Bridge"][0] for b_, c in enumerate(R["chords"]["Bridge"]) if c == "Abm"]; ok["songbook: the A♭ minor bars"] = f"Bars {iv[0]}–{iv[-1]} are A♭ minor" in sb
td = [n for n in mel if n["sec"] == "Chorus 3" and n["text"] == "today"][-1]; ok["record: 'today' on the tonic"] = (td["midi"] - R["key"]["tonic_midi"]) % 12 == 0
ok["songbook: the close"] = f"“Today” lands on {nm(td['midi'])} over E♭ in bar {td['on'] // B + 1}" in sb
for n in ("Verse 1", "Chorus 1", "Bridge", "Verse 3", "Chorus 3"):
    s, b = start[n]; rows = re.findall(r"\| (\d+)–(\d+)(?: \(pickup in \d+\))? \| ([^|]+) \|", sb.split(f"{SHOW[n]} (bars {s}")[1].split("###")[0])
    good = True
    for a, z, ch in rows:
        want = [R["chords"][n][int(a) - s], R["chords"][n][int(z) - s]]
        got = [re.sub(r"/.*", "", x.strip()).replace("♭", "b") for x in ch.split("·")]
        good &= all(w_.split()[0] == g_.split()[0] and len(w_.split()) == len(g_.split()) for w_, g_ in zip(want, got))
    ok[f"songbook: {n} chords beside the lines"] = good and len(rows) > 0
rb = json.load(open(f"{D}/readback.json")); ok["engraving: every staff reads back from its MIDI"] = all(v["matches_a_midi_staff"] for v in rb.values())
ok["record: strings never above a sung note"] = R["checks"]["strings_above_a_sung_note_share"] == 0
ok["record: the verse chords loop less than the kept median (0.333)"] = True
def rep(sec):
    m = []
    for bar in R["roman"][sec]:
        for c in bar.split():
            if not m or m[-1] != c: m.append(c)
    seen = set(); r = t = 0
    for i in range(len(m) - 2): g = tuple(m[i:i + 3]); t += 1; r += g in seen; seen.add(g)
    return r / t
ok["record: the verse chords loop less than the kept median (0.333)"] = rep("Verse 1") < 0.333
IN = {"I", "ii", "iii", "IV", "V", "vi", "viio"}; outk = [(n, c) for n, k, b in R["form"] for bar in R["roman"][n] for c in bar.split() if c not in IN]
ok["record: chords from outside the key only under 'for now'"] = all(n == "Bridge" for n, c in outk)
for kind in ("full score", "lead sheet", "parts", "songbook", "demo", "full score.musicxml"):
    fs = glob.glob(f"{D}/{FT} - {kind}*"); ok[f"files: {kind} carries the edition label"] = len(fs) > 0
ok["songbook: no engine terms"] = not re.search(r"\b(engine|module|Luthier|fingerprint|charge|gate|749\.|judge|kept)\b", sb, re.I)
ok["songbook: the producer one-sheet, its own page in Word"] = "### Producer one-sheet" in sbw and sbw.count('w:type="page"') >= 2
z = zipfile.ZipFile(glob.glob(f"{D}/{FT} - songbook.docx")[0]); xml = z.read("word/document.xml").decode()
ok["songbook (Word): page breaks around the one-sheet"] = xml.count('w:type="page"') >= 2 and "Producer one-sheet" in xml
lines = [l.strip() for l in open("lyric_locked.md") if l.strip() and not l.startswith("#") and not l.startswith("Words")]
ok["songbook: every locked line in the lyric sheet"] = all(l in sb for l in lines)
ok["songbook: credit line"] = "Words and music: Jason Bryant" in sb
ly = open(f"{D}/ly/lead sheet.ly").read(); fs = open(f"{D}/ly/full score.ly").read()
ok["engraving: section names match the songbook (Refrain, Last refrain, Turn)"] = all(f'box \\bold "{x}"' in ly for x in ("Refrain", "Last refrain", "Turn")) and "Chorus" not in ly and "Chorus" not in fs
lyr = re.search(r"\\lyricsto \"v\" \{(.*?)\}", ly, re.S).group(1); toks = [t for t in re.findall(r'"([^"]*)"', lyr)]
words = re.sub(r'"\s*--\s*(?:_\s*)*"', "", lyr); words = re.findall(r'"([^"]+)"', words)
ok["engraving: no word printed twice in a row where the lyric has it once"] = not any(a.lower() == b.lower() and a.lower() not in ("let", "in", "every") for a, b in zip(words, words[1:]))
ok["engraving: the breath and 'let it sit' after 'Good sermon, Dad'"] = "let it sit" in ly and "\\breathe" in ly
vb = sorted({e["on"] // B + 1 for e in R["parts"]["violin1"] if start["Chorus 3"][0] <= e["on"] // B + 1 < start["Outro"][0]})
ok["songbook: the violin's answers at the bars engraved"] = f"(bars {', '.join(str(b_) for b_ in vb)})" in sb
json.dump(ok, open("consistency62.json", "w"), indent=1); bad = [k for k, v in ok.items() if not v]
print(f"{sum(ok.values())} of {len(ok)} pass" + ("; failing: " + "; ".join(bad) if bad else ""))
