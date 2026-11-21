"""Wood and Cloth (second edition): every document against the record."""
import json, re, subprocess, itertools
import lyric_p12 as L
H = "/home/claude/zeneng-pipeline/songs/p12"; OUT = f"{H}/out"; ED = L.EDITION; T = L.TITLE
R = json.load(open(f"{H}/song_record.json")); V = R["voices"]; N = R["tune"]; BAR = 36; ST = {int(k): v for k, v in R["stanza_offsets"].items()}
C = []
def chk(name, ok): C.append((name, bool(ok)))
def pdf(n): return subprocess.run(["pdftotext", "-layout", f"{OUT}/{T}{ED} - {n}.pdf", "-"], capture_output=True, text=True).stdout
rb = json.load(open(f"{OUT}/readback.json"))
for k, (ok, a, b) in rb.items(): chk(f"MIDI readback {k} ({a}/{b})", ok)
hp, os_, ls = pdf("hymnal page"), pdf("organ score with choir"), pdf("lead sheet")
sb = open(f"{H}/songbook.md").read()
for name, txt in (("hymnal page", hp), ("organ score", os_), ("lead sheet", ls), ("songbook", sb)):
    chk(f"{name}: no engine terms", not re.search(r"\b(PASS|Module|engine|Luthier|ZenEng|Elias Cord|DU)\b", txt))
    chk(f"{name}: credit line", "Jason Bryant" in txt)
    chk(f"{name}: edition label", ED.strip(" ()") in txt.lower() or name == "hymnal page")
for s in range(5):
    first = L.syls(L.STANZAS[s][0])[0][0]
    chk(f"hymnal page carries stanza {s + 1}", first in hp and f"{s + 1}." in hp)
chk("hymnal page: scripture under stanza 2", "Matthew 27:57" in hp and "Arimathea" in hp)
chk("hymnal page: stanza 4 marked choir alone", "choir alone" in hp)
chk("organ score: stanza 4 marked choir alone", "choir alone" in os_)
chk("organ score: registrations printed", "Diapasons" in os_ and "Full organ" in os_)
l1 = [(x["on"] - 0, x["dur"], x["p"]) for x in N if x["line"] == 0]; l3 = [(x["on"] - 8 * BAR, x["dur"], x["p"]) for x in N if x["line"] == 2]
chk("line 3 repeats line 1 exactly", l1 == l3)
chk("E5 once a stanza, bar 14", [x["on"] // BAR + 1 for x in N if x["p"] == 76] == [14])
chk("final cadence C#5 to D5", (N[-2]["p"], N[-1]["p"]) == (73, 74))
chk("tune range D4-E5", min(x["p"] for x in N) == 62 and max(x["p"] for x in N) == 76)
chk("descant above the tune throughout", all(d - x["p"] >= 3 for d, x in zip(R["descant"], N)))
chk("descant top G5 only in bars 13-14", all(x["on"] // BAR in (12, 13) for d, x in zip(R["descant"], N) if d == 79))
chk("organ silent in stanza 4", not any(ST[4] <= e["on"] < ST[4] + 16 * BAR for v in ("org_rh", "org_lh", "org_ped") for e in V[v]))
chk("no pedal in stanza 3", not any(ST[3] <= e["on"] < ST[3] + 16 * BAR for e in V["org_ped"]))
chk("held D in the pedal under stanza 5 line 4", any(e["on"] == ST[5] + 12 * BAR and e["p"] == 38 and e["dur"] == 4 * BAR for e in V["org_ped"]))
for name in ("hymnal", "stanza4", "stanza5"):
    P = R["paths"][name]; bad = 0
    for k in range(1, len(P)):
        v0 = [N[k - 1]["p"]] + P[k - 1][1:]; v1 = [N[k]["p"]] + P[k][1:]
        for i, j in itertools.combinations(range(4), 2):
            i0 = (v0[i] - v0[j]) % 12; i1 = (v1[i] - v1[j]) % 12
            if i0 == i1 and i0 in (0, 7) and v0[i] != v1[i] and v0[j] != v1[j]: bad += 1
    chk(f"{name}: no parallel fifths or octaves", bad == 0)
    downs = [P[k][0] for k, x in enumerate(N) if x["on"] % BAR == 0]
    chk(f"{name}: downbeat chords follow the plan", downs == R["chords"][name])
chk("hymnal: E7 bar 7, F#7 bar 10", R["chords"]["hymnal"][6] == "E7" and R["chords"]["hymnal"][9] == "F#7")
chk("stanza 4: one borrowed chord (G minor 6) in bar 14 only", [i + 1 for i, c in enumerate(R["chords"]["stanza4"]) if c == "Gm6"] == [14])
chk("songbook: bar claims read from the record", "E7 in bar 7" in sb and "F#7 in bar 10" in sb and "organ score bar 66" in sb and "bars 85 and 86" in sb and "Bars 1, 5, 7, 9 and 13" in sb)
chk("songbook: producer one-sheet", "Producer one-sheet" in sb and "Non-negotiables" in sb and "Mix priorities" in sb)
for name, txt in (("hymnal page", hp), ("organ score", os_), ("lead sheet", ls), ("songbook", sb)):
    chk(f"{name}: felt in one, no 'one to the bar'", "felt in one" in txt and "one to the bar" not in txt)
chk("organ score: hold at the end of stanza 3", "release as the choir breathes" in os_)
chk("organ score: Joseph of Arimathea note", "Arimathea" in os_)
chk("link starts on D (pedal D3, right hand D4 and F-sharp4)", any(e["on"] == R["link"] and e["p"] == 50 for e in V["org_ped"]) and any(e["on"] == R["link"] and e["p"] == [62, 66] for e in V["org_rh"]))
sl = {}
for x in N: sl[(x["line"], x["syl"])] = sl.get((x["line"], x["syl"]), 0) + x["dur"]
chk("no weak syllable as long as or longer than the strong one before it (every stanza)", all(sl[(li, k)] < sl[(li, k - 1)] for li, n in enumerate([8, 7, 8, 7]) for k in range(1, n - 1, 2)))
chk("songbook Word copy exists", subprocess.run(["test", "-s", f"{OUT}/{T}{ED} - songbook.docx"]).returncode == 0)
for f in ("demo.mp3", "demo.mid", "hymnal setting.musicxml", "organ score with choir.musicxml"):
    chk(f"file: {f}", subprocess.run(["test", "-s", f"{OUT}/{T}{ED} - {f}"]).returncode == 0)
for n_, ok in C: print(("PASS " if ok else "FAIL ") + n_)
print(f"{sum(ok for _, ok in C)} of {len(C)} checks pass")
json.dump(C, open(f"{OUT}/consistency.json", "w"))
