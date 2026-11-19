"""'Same Time Tomorrow' (song 58): every document against the record (lyric58.song.json, through song_record.pkl). Run after build58, engrave58,
score58, musicxml58, nashville58, demo58 and songbook58. Prints each check and exits 1 if any fails."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo58 as KI
import pickle, json, os, re, subprocess, sys, collections
import mido
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out"); FT = None
SRC = json.load(open(os.path.join(HERE, "lyric58.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb")); FT = REC["file_title"]
C = []
def chk(name, ok, detail=""): C.append((name, bool(ok), detail))
# the record itself
chk("the document record is the song record: sung notes", [(n["on"], n["midi"]) for n in REC["lead"]] == [(n["on"], n["midi"]) for n in sorted(SRC["melody"]["notes"], key=lambda n: n["on"])])
chk("harmony notes", sorted((n["on"], n["midi"]) for n in REC["harm"]) == sorted((e["on"], e["p"][0]) for e in SRC["parts"]["harmony"]))
chk("band parts", all(REC["parts"][a] == [dict(e, art="") for e in SRC["parts"][b]] for a, b in (("guitar", "chords"), ("bass", "bass"), ("drums", "drums"))))
chk("bars and chords", [" ".join(x["beats4"]) if x.get("beats4") else (x["chord"] if x["chord"] == x["chord2"] else x["chord"] + " " + x["chord2"]) for x in REC["bars"]] == [c for s, _, _ in SRC["form"] for c in SRC["chords"][s]])
L = json.load(open(os.path.join(HERE, "lyric58.json"))); words = lambda s: re.sub(r"[^a-z' ]", "", s.lower().replace("’", "'")).split()
got = collections.OrderedDict()
for n in REC["lead"]:
    if n["first"]: got.setdefault((n["sec"], n["line"]), []).append(n["text"] + ("" if n["hyph"] else " "))
chk("every sung line spells its locked line", all(words("".join(v)) == words(dict(((s, i), t) for s, ls in L["sections"] for i, t in enumerate(ls))[k]) for k, v in got.items()), f"{len(got)} lines")
# engravings: LilyPond MIDI read back per staff (the scripts' own readbacks)
for f in ("readback.pkl", "readback_score.pkl"):
    rb = pickle.load(open(os.path.join(OUT, f), "rb"))
    for grp in ("voice", "parts"):
        for k, v in rb[grp].items(): chk(f"{f[:-4]}: {k} read back", v[0], f"{v[1]} of {v[2]}")
    chk(f"{f[:-4]}: drums counted", rb["drums"][0] == rb["drums"][1], f"{rb['drums'][0]} of {rb['drums'][1]}")
for doc in ("lead sheet", "full score", "parts", "Nashville chart"):
    p = os.path.join(OUT, f"{FT} - {doc}.pdf"); ok = os.path.exists(p)
    txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout if ok else ""
    chk(f"{doc}: PDF written, credit line", ok and "Words and music: Jason Bryant" in txt, f"{subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0] if ok else 0} pages")
    if doc != "Nashville chart": chk(f"{doc}: footer tempo and key", ("♩ = 84" in txt or "= 84" in txt) and KI.KEYSTR in txt, KI.KEYSTR)
    else: chk("Nashville chart: the record's key, 1 = its tonic", f"KEY: {KI.KEYSTR}" in txt.replace("\n", " ") or KI.KEYSTR in txt, KI.numbers_line())
    if doc != "Nashville chart":
        ly = os.path.join(OUT, f"{FT} - {doc}.ly"); chk(f"{doc}: key signature is the record's", os.path.exists(ly) and set(re.findall(r"\\key [a-z]+ \\major", open(ly).read())) == {KI.LILY_KEY}, KI.LILY_KEY)
# the number chart against the record
nv = open(os.path.join(OUT, "nashville.html")).read()
num = lambda c: KI.number(c[:2] if len(c) > 1 and c[1] in "#b" else c[0]) + ("m" if c.endswith("m") else "")
want = [" ".join(num(c) for c in (x["beats4"] or [])) if x.get("beats4") else (num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"])) for x in REC["bars"]]
cells = re.findall(r"<td>([^<]*)</td>", nv); chk("number chart: one cell a bar, as the record", cells == want, f"{len(cells)} cells")
# MusicXML: counted by the writer; re-read the lead sheet's pitches
from music21 import converter, harmony
for lab, n_want in (("lead sheet", len(REC["lead"])),):      # the record's count, not a number written in
    s = converter.parse(os.path.join(OUT, f"{FT} - {lab}.mxl"))
    ons = [x for x in s.parts[0].recurse().notes if not isinstance(x, harmony.ChordSymbol) and not (x.tie is not None and x.tie.type in ("stop", "continue"))]
    chk(f"MusicXML {lab}: onsets and pitches", len(ons) == n_want and [x.pitch.midi for x in ons] == [n["midi"] for n in REC["lead"]], f"{len(ons)}")
# the demo: notes per track against the record
m = mido.MidiFile(os.path.join(OUT, f"{FT} - demo (General MIDI).mid")); cnt = {t.name: sum(1 for x in t if x.type == "note_on" and x.velocity) for t in m.tracks}
chk("demo: voice notes", cnt.get("Voice (guide, tenor sax)") == len(REC["lead"]), str(cnt.get("Voice (guide, tenor sax)")))
chk("demo: harmony notes", cnt.get("Harmony voice (choir)") == len(REC["harm"]))
chk("demo: guitar notes", cnt.get("Acoustic guitar") == sum(len(e["p"]) for e in REC["parts"]["guitar"]))
chk("demo: bass notes", cnt.get("Bass") == len(REC["parts"]["bass"]))
chk("demo: drum hits", cnt.get("Drums") == sum(len(e["p"]) for e in REC["parts"]["drums"]))
chk("demo: track names ASCII", all(t.name.isascii() for t in m.tracks))
dr = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb")); chk("demo: voice at least 3 dB over the band", dr["stems_db"] >= 3, f"{dr['stems_db']:+.1f} dB")
chk("demo: MP3 written", os.path.exists(os.path.join(OUT, f"{FT} - demo.mp3")))
E = {r["sec"]: r["energy_read"] for r in dr["energy"]}
chk("energy arc: each chorus above its verse", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] > E["Verse 3"])
chk("READING, the engine's, not a document check: the last chorus or the bridge the top (9.12)", max(E["Last Chorus"], E["Bridge"]) >= max(E.values()) - 1e-9, f"last chorus {E['Last Chorus']:.2f}, top {max(E, key=E.get)} {max(E.values()):.2f} (749.75)")
# the songbook
sb = open(os.path.join(HERE, "songbook.md")).read()
chk("songbook: no engine terms", not re.search(r"\b(Luthier|module|fix \d|judge|fingerprint|charge|build[s]?\b|engine)\b", sb, re.I))
chk("songbook: credit line", "Words and music: Jason Bryant" in sb)
chk("songbook: every line on the lyric sheet", sum(1 for l in sb.split("### Lyric sheet")[1].split("### Producer")[0].splitlines() if re.match(r"^\d+( \(pickup in \d+\))?: ", l)) == len(got))
chk("songbook: producer one-sheet and its page breaks", "### Producer one-sheet" in sb and sb.count('w:type="page"') >= 2)
docx = os.path.join(OUT, f"{FT} - songbook.docx"); chk("songbook: Word copy written", os.path.exists(docx))
if os.path.exists(docx) and "--fast" not in sys.argv:
    tmp = "/tmp/sb_check"; os.makedirs(tmp, exist_ok=True); subprocess.run(["cp", docx, tmp + "/sb.docx"])
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, tmp + "/sb.docx"], capture_output=True, timeout=240)
    pages = [subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), tmp + "/sb.pdf", "-"], capture_output=True, text=True).stdout for p in range(1, 30)]
    one = [i for i, t in enumerate(pages) if "Producer one-sheet" in t]
    chk("songbook (Word): the one-sheet on one page", one and "Mix priorities" in pages[one[0]] and "Production brief" not in pages[one[0]], f"page {one[0] + 1 if one else '?'}")
fails = [c for c in C if not c[1] and not c[0].startswith("READING")]
for n, ok, d in C: print(("pass " if ok else ("not met " if n.startswith("READING") else "FAIL ")) + n + (f"  ({d})" if d else ""))
print(f"documents: {sum(1 for c in C if not c[0].startswith('READING') and c[1])} of {sum(1 for c in C if not c[0].startswith('READING'))} pass; readings not met: {sum(1 for c in C if c[0].startswith('READING') and not c[1])}")
json.dump([dict(check=n, ok=ok, detail=d) for n, ok, d in C], open(os.path.join(HERE, "consistency58.json"), "w"), indent=1)
sys.exit(1 if fails else 0)
