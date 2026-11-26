"""'They Did the Right Thing' (song 66): every document against the record (lyric66_d.hand.song.json, through song_record.pkl), and each of the
writer's design notes checked where it was built. Run after build66, engrave66, score66, musicxml66, nashville66, demo66 and songbook66.
Prints each check and exits 1 if any fails."""
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import keyinfo66 as KI
import pickle, json, os, re, subprocess, sys, collections
import mido
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
SRC = json.load(open(os.path.join(HERE, "lyric66_d.hand.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb")); FT = REC["file_title"]
C = []
def chk(name, ok, detail=""): C.append((name, bool(ok), detail))
P = REC["parts"]; B1 = {s: st // 48 for s, nb, st, _, _ in REC["plan"]}; NB = {s: nb for s, nb, _, _, _ in REC["plan"]}
def span(s): return B1[s] * 48, (B1[s] + NB[s]) * 48
chk("the document record is the song record: sung notes", [(n["on"], n["midi"]) for n in REC["lead"]] == [(n["on"], n["midi"]) for n in sorted(SRC["melody"]["notes"], key=lambda n: n["on"])])
chk("harmony notes are the engine's (two set an octave down, where the engine's sat over the lead)", all((n["on"], n["midi"] + (12 if n.get("recast") else 0)) in {(e["on"], e["p"][0]) for e in SRC["parts"]["harmony"]} for n in REC["harm"]), f"{len(REC['harm'])}; {sum(1 for n in REC['harm'] if n.get('recast'))} recast")
chk("harmony: never above the lead", all(n["midi"] <= max([x["midi"] for x in REC["lead"] if x["on"] <= n["on"] < x["on"] + x["dur"]] or [127]) for n in REC["harm"]))
for k, src in (("guitar", "chords"), ("bass", "bass"), ("drums", "drums")):
    chk(f"{k}: the engine's part (with the design notes), note for note", [(e["on"], e["p"]) for e in P[k] if not (k == "drums" and e["p"] == [49] and e["on"] == span("Chorus 3")[0])] == [(e["on"], e["p"]) for e in SRC["parts"][src]], f"{len(P[k])}")
_bc = lambda t: REC["bars"][t // 48]["beatchords"][(t % 48) // 12]
chk("guitar: every strummed note a tone of its beat's chord", all(all(p % 12 in SRC["chord_tones"][_bc(e["on"])[1]] for p in e["p"]) for e in P["guitar"]))
_dd = lambda xs: [c for i_, c in enumerate(xs) if i_ == 0 or xs[i_ - 1] != c]
chk("bars and chords", [(x["chord"] if x["chord"] == x["chord2"] else x["chord"] + " " + x["chord2"]) for x in REC["bars"]] == [c for s, _, _ in SRC["form"] for c in SRC["chords"][s]])
# the design notes
holds = [n for n in REC["lead"] if n["midi"] == 64 and n["dur"] >= 96]; hb = {n["sec"]: n for n in holds}
chk("design 1: each chorus ends on E4 held at least two bars", all(s in hb and hb[s]["text"] == "gone" for s in ("Chorus 1", "Chorus 2")) and hb["Chorus 3"]["dur"] >= 144, ", ".join(f"{s} bar {n['on'] // 48 + 1}, {n['dur'] // 48} bars" for s, n in hb.items()))
def bass_under(n): return [e["p"][0] % 12 for e in P["bass"] if n["on"] <= e["on"] < n["on"] + n["dur"]]
def walk(pcs): return [p for i, p in enumerate(pcs) if i == 0 or pcs[i - 1] != p]
chk("design 1: under the first two holds the bass begins a chromatic descent from E", all(walk(bass_under(hb[s]))[-2:] == [4, 3] for s in ("Chorus 1", "Chorus 2")), str([walk(bass_under(hb[s])) for s in ("Chorus 1", "Chorus 2")]))
b0, b1 = span("Bridge")
chk("design 2: the bridge is voice, guitar and bass only", not any(b0 <= e["on"] < b1 for e in P["drums"]) and not any(b0 <= n["on"] < b1 for n in REC["harm"]) and any(b0 <= e["on"] < b1 for e in P["guitar"]) and any(b0 <= e["on"] < b1 for e in P["bass"]))
dr = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb")); E = {r["sec"]: r["energy_read"] for r in dr["energy"]}
chk("design 2: the bridge the lowest level of the song's sung sections", E["Bridge"] < min(v for s, v in E.items() if s not in ("Bridge", "Intro", "Tag", "Outro") and not s.startswith("Turn")), f"bridge {E['Bridge']:.2f}")
stop0 = b1 - 24
chk("design 3: all stop on the bridge's last two beats, every instrument", not any(e["on"] < b1 and e["on"] + e["dur"] > stop0 for k in ("guitar", "bass", "drums") for e in P[k]), f"bar {b1 // 48}")
c0 = span("Chorus 3")[0]
chk("design 4: the final chorus all in on its downbeat, nothing in the bar before", all(any(e["on"] == c0 for e in P[k]) for k in ("guitar", "bass", "drums")) and not any(stop0 <= e["on"] < c0 for k in P for e in P[k]))
chk("design 4: the final chorus's hold three bars over the bass E, D♯, D, C♯, C", hb["Chorus 3"]["dur"] == 144 and walk([e["p"][0] % 12 for e in P["bass"] if hb["Chorus 3"]["on"] <= e["on"] < hb["Chorus 3"]["on"] + hb["Chorus 3"]["dur"] + 2 * 48])[-5:] == [4, 3, 2, 1, 0], str(walk([e["p"][0] % 12 for e in P["bass"] if hb["Chorus 3"]["on"] <= e["on"] < hb["Chorus 3"]["on"] + 240])))
t0 = span("Tag")[0]
chk("design 5: the tag and outro voice and guitar only", not any(e["on"] >= t0 for k in ("bass", "drums") for e in P[k]) and not any(n["on"] >= t0 for n in REC["harm"]))
last = max(n["on"] for n in REC["lead"]); ln = next(n for n in REC["lead"] if n["on"] == last)
chk("design 5: the tag's last word held on E4; the song ends on A minor", ln["midi"] == 64 and REC["bars"][-1]["chord"] == "Am", f"“{ln['text']}”, last chord {REC['bars'][-1]['chord']}")
chk("design 5: the tag fades", sum(e["vel"] for e in P["guitar"] if e["on"] >= REC["end"] - 96) / max(1, sum(1 for e in P["guitar"] if e["on"] >= REC["end"] - 96)) < sum(e["vel"] for e in P["guitar"] if t0 <= e["on"] < t0 + 96) / max(1, sum(1 for e in P["guitar"] if t0 <= e["on"] < t0 + 96)))
chk("the key: A minor, the writer's", SRC["key"]["key"] == "Am" and KI.LILY_KEY == "\\key a \\minor")
chk("the voice inside a tenor (C3 to A4)", 48 <= min(n["midi"] for n in REC["lead"]) and max(n["midi"] for n in REC["lead"]) <= 69, f"{min(n['midi'] for n in REC['lead'])}–{max(n['midi'] for n in REC['lead'])}")
L = json.load(open(os.path.join(HERE, "lyric66.json"))); words = lambda s: re.sub(r"[^a-z' ]", "", s.lower().replace("’", "'").replace("-", " ")).split()
got = collections.OrderedDict()
for n in REC["lead"]:
    if n["first"]: got.setdefault((n["sec"], n["line"]), []).append(n["text"] + ("" if n["hyph"] else " "))
chk("every sung line spells its locked line", all(words("".join(v)) == words(dict(((s, i), t) for s, ls in L["sections"] for i, t in enumerate(ls))[k]) for k, v in got.items()), f"{len(got)} lines")
for f in ("readback.pkl", "readback_score.pkl"):
    rb = pickle.load(open(os.path.join(OUT, f), "rb"))
    for grp in ("voice", "parts"):
        for k, v in rb[grp].items(): chk(f"{f[:-4]}: {k} read back", v[0], f"{v[1]} of {v[2]}")
    chk(f"{f[:-4]}: drum hits written", rb["drums"][0] == rb["drums"][1], f"{rb['drums'][0]} of {rb['drums'][1]}")
for doc in ("lead sheet", "full score", "parts", "Nashville chart"):
    p = os.path.join(OUT, f"{FT} - {doc}.pdf"); ok = os.path.exists(p)
    txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout if ok else ""
    chk(f"{doc}: PDF written, credit line", ok and "Words and music: Jason Bryant" in txt, f"{subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout.split('Pages:')[1].split()[0] if ok else 0} pages")
    if doc != "Nashville chart":
        chk(f"{doc}: footer tempo and key", "= 72" in txt and KI.KEYSTR in txt, KI.KEYSTR)
        ly = os.path.join(OUT, f"{FT} - {doc}.ly"); chk(f"{doc}: key signature is the record's", os.path.exists(ly) and set(re.findall(r"\\key [a-z]+ \\(?:major|minor)", open(ly).read())) == {KI.LILY_KEY}, KI.LILY_KEY)
    else: chk("Nashville chart: the record's key, 1 = its tonic", KI.KEYSTR in txt, KI.numbers_line())
nv = open(os.path.join(OUT, "nashville.html")).read()
QN = {"": "", "m": "m", "7": "⁷"}
def num(c):
    base, _, bs = c.partition("/"); rt_ = base[:2] if len(base) > 1 and base[1] in "#b" else base[:1]
    return KI.number(rt_) + QN[base[len(rt_):]] + (f"/{KI.number(bs)}" if bs else "")
want = [num(x["chord"]) if x["chord"] == x["chord2"] else num(x["chord"]) + " " + num(x["chord2"]) for x in REC["bars"]]
cells = re.findall(r"<td>([^<]*)</td>", nv); chk("number chart: one cell a bar, as the record", cells == want, f"{len(cells)} cells")
from music21 import converter, harmony
s = converter.parse(os.path.join(OUT, f"{FT} - lead sheet.mxl"))
ons = [x for x in s.parts[0].recurse().notes if not isinstance(x, harmony.ChordSymbol) and not (x.tie is not None and x.tie.type in ("stop", "continue"))]
chk("MusicXML lead sheet: onsets and pitches", len(ons) == len(REC["lead"]) and [x.pitch.midi for x in ons] == [n["midi"] for n in REC["lead"]], f"{len(ons)}")
m = mido.MidiFile(os.path.join(OUT, f"{FT} - demo (General MIDI).mid")); cnt = {t.name: sum(1 for x in t if x.type == "note_on" and x.velocity) for t in m.tracks}
chk("demo: voice notes", cnt.get("Voice (guide, tenor sax)") == len(REC["lead"]), str(cnt.get("Voice (guide, tenor sax)")))
chk("demo: harmony notes", cnt.get("Harmony voice (choir)") == len(REC["harm"]))
chk("demo: guitar notes", cnt.get("Acoustic guitar") == sum(len(e["p"]) for e in P["guitar"]))
chk("demo: bass notes", cnt.get("Bass") == len(P["bass"]))
chk("demo: drum hits", cnt.get("Drums") == sum(len(e["p"]) for e in P["drums"]))
chk("demo: track names ASCII", all(t.name.isascii() for t in m.tracks))
chk("demo: voice at least 3 dB over the band", dr["stems_db"] >= 3, f"{dr['stems_db']:+.1f} dB")
chk("demo: MP3 written", os.path.exists(os.path.join(OUT, f"{FT} - demo.mp3")))
chk("energy arc: each chorus above its verse", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Chorus 3"] > E["Verse 2"])
chk("energy arc: the final chorus the top", E["Chorus 3"] >= max(E.values()) - 1e-9, f"final chorus {E['Chorus 3']:.2f}")
sb = open(os.path.join(HERE, "songbook.md")).read()
chk("songbook: no engine terms", not re.search(r"\b(Luthier|module|fix \d|judge|fingerprint|charge|build[s]?\b|engine)\b", sb, re.I))
chk("songbook: credit line", "Words and music: Jason Bryant" in sb)
chk("songbook: every line on the lyric sheet", sum(1 for l in sb.split("### Lyric sheet")[1].split("### Producer")[0].splitlines() if re.match(r"^\d+( \(pickup in \d+\))?: ", l)) == len(got))
chk("songbook: producer one-sheet and its page breaks", "### Producer one-sheet" in sb and sb.count('w:type="page"') >= 2)
chk("songbook: the held E4s and the stop named at their bars", all(f"bar {n['on'] // 48 + 1}" in sb for n in holds) and f"bar {b1 // 48}" in sb)
docx = os.path.join(OUT, f"{FT} - songbook.docx"); chk("songbook: Word copy written", os.path.exists(docx))
if os.path.exists(docx) and "--fast" not in sys.argv:
    tmp = "/tmp/sb_check66"; os.makedirs(tmp, exist_ok=True); subprocess.run(["cp", docx, tmp + "/sb.docx"])
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, tmp + "/sb.docx"], capture_output=True, timeout=240)
    pages = [subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), tmp + "/sb.pdf", "-"], capture_output=True, text=True).stdout for p in range(1, 40)]
    one = [i for i, t in enumerate(pages) if "Producer one-sheet" in t]
    chk("songbook (Word): the one-sheet on one page", one and "Mix priorities" in pages[one[0]] and "Production brief" not in pages[one[0]], f"page {one[0] + 1 if one else '?'}")
fails = [c for c in C if not c[1]]
for n, ok, d in C: print(("pass " if ok else "FAIL ") + n + (f"  ({d})" if d else ""))
print(f"documents: {sum(1 for c in C if c[1])} of {len(C)} pass")
json.dump([dict(check=n, ok=ok, detail=d) for n, ok, d in C], open(os.path.join(HERE, "consistency66.json"), "w"), indent=1)
sys.exit(1 if fails else 0)
