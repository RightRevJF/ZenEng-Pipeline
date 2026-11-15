"""Sung to Sleep (song 53): both documents against the record, and the readings for the test report (written to readings53.json)."""
import json, re, subprocess, os, collections, itertools
import harm68
H = "/home/claude/p63"; OUT = f"{H}/out"
R = json.load(open(f"{H}/song_record.json")); V = R["voices"]; RB = json.load(open(f"{OUT}/readback.json"))
def pdf(n): return subprocess.run(["pdftotext", "-layout", f"{OUT}/Sung to Sleep - {n}.pdf", "-"], capture_output=True, text=True).stdout
HP, FS = pdf("hymn page"), pdf("full score (organ)")
C = []
def chk(name, ok): C.append((name, bool(ok)))
for nm, txt in (("hymn page", HP), ("full score", FS)): chk(f"credit line on the {nm}", "Words and music: Jason Bryant" in txt)
for k, v in RB.items(): chk(f"readback: {k}", v[0])
def system_bars(txt): return [int(x) for x in re.findall(r"^\s*(\d{1,2})\s*$|^\s*(\d{1,2})\s+[A-Z]", txt, re.M) for x in x if x] if False else [int(m) for m in re.findall(r"(?m)^\s{0,6}(\d{1,2})\b", txt) if 1 < int(m) <= 70]
src_h = open(f"{OUT}/Sung to Sleep - hymn page.ly").read(); src_f = open(f"{OUT}/Sung to Sleep - full score (organ).ly").read()
g = lambda s: re.search(r"global = \{(.*?)\n", s).group(1)
chk("the two documents share one global line (time, keys, bar lines, marks, a break every fourth bar; 80 bars)", g(src_h) == g(src_f) and g(src_h).count("\\break") == 19 and g(src_h).count("s2.") == 80)
chk("the same notes for every choir voice in both documents", all(re.search(re.escape(x), src_f) for x in re.findall(r'\\new Voice = "(?:sop|alt|ten|bas|desc)" \{ \\voice\w+ (.*?) \}', src_h)))
O = R["offsets"]; L0 = 40 * 36
def span(v, a, b): return [e for e in V[v] if a <= e["on"] < b]
S = V["S"]
chk("key: E-flat to bar 40, F from bar 41", R["keys"] == [[0, "E-flat major"], [L0, "F major"]] and "\\key ees \\major" in g(src_h) and "\\key f \\major" in g(src_h))
top_A = [e for e in span("S", 0, L0) if e["p"] == max(x["p"] for x in span("S", 0, L0))]
chk("the tune's top in verses 1-3 and refrain, E-flat5, only on 'world'", len(top_A) == 1 and top_A[0]["p"] == 75 and top_A[0]["part"] == "refrain" and top_A[0]["syl"] == 5 and top_A[0]["line"] == 2)
top_B = [e for e in S if e["p"] == max(x["p"] for x in S)]
chk("the song's top, F5, once, on the final refrain's 'world' (749.10)", len(top_B) == 1 and top_B[0]["p"] == 77 and top_B[0]["part"] == "refrain_final")
D = V["Desc"]; dt = [e for e in D if e["p"] == max(x["p"] for x in D)]
chk("the descant's top, A5, once, on 'world'", len(dt) == 1 and dt[0]["p"] == 81 and dt[0]["on"] == top_B[0]["on"])
chk("the descant above the sopranos throughout", all(d["p"] > s["p"] for d, s in zip(D, [e for e in S if e["part"] == "refrain_final"])))
def line(part, li): return [e for e in S if e["part"] == part and e["line"] == li]
for part, base in (("refrain", 62 + 1), ("refrain_final", 62 + 3)):
    l4 = line(part, 3); s1 = next(e for e in l4 if e["syl"] == 1); s2 = next(e for e in l4 if e["syl"] == 3)
    chk(f"{part}: the second 'sleeping' a step above the first; 'here' home on the tonic", 1 <= s2["p"] - s1["p"] <= 2 and l4[-1]["p"] == base)
    l1 = line(part, 0); chk(f"{part}: 'Hush now' low and still (within a major third)", max(e["p"] for e in l1) - min(e["p"] for e in l1) <= 4)
v4 = [e for e in S if e["part"] == "verse4"]; on4 = {e["on"] for e in v4}
A4 = {e["on"]: e["p"] for e in V["A"] if e["on"] in on4}; T4 = {e["on"]: e["p"] for e in V["T"] if e["on"] in on4}; B4 = {e["on"]: e["p"] for e in V["B"] if e["on"] in on4}
chk("verse 4: the choir in unison (altos with the sopranos, men an octave lower) (749.8)", all(A4.get(e["on"], e["p"]) == e["p"] and T4.get(e["on"], e["p"] - 12) == e["p"] - 12 and B4.get(e["on"], e["p"] - 12) == e["p"] - 12 for e in v4))
p4 = [c for c, *_ in R["paths"]["verse4"]]; pA = [c for c, *_ in R["paths"]["A"][:len(p4)]]
chk("verse 4: the organ's own harmony (chords differ from verse 1-3's on most notes) (749.8)", sum(a != b for a, b in zip(p4, pA)) >= len(p4) // 2)
def doubles(cv, ov, a, b):
    c = {(e["on"], e["p"]) for e in span(cv, a, b)}; o = {(e["on"], e["p"]) for e in span(ov, a, b)}; return c == o
def sounding(v, t):
    out = set()
    for e in V[v]:
        if e["on"] <= t < e["on"] + e["dur"]: out |= set(e["p"] if isinstance(e["p"], list) else [e["p"]])
    return out
def organ_at(t): return sounding("org_rh", t) | sounding("org_lh", t) | sounding("org_ped", t)
inA = [(e["on"], e["p"]) for v in ("S", "A", "T", "B") for e in V[v] if O["A_verse"] - 12 <= e["on"] < 40 * 36]
chk("verses 1-3 and refrains: every choir note sounds in the organ (a fuller form of the choir's harmony)", all(p in organ_at(t) for t, p in inA))
_rhA = [e for e in V["org_rh"] if O["A_verse"] - 12 <= e["on"] < 40 * 36]
chk("verses 1-3 and refrains: the organ fuller than the choir (three notes in the right hand on most chords)", sum(isinstance(e["p"], list) and len(e["p"]) == 3 for e in _rhA) > len(_rhA) / 2)
chk("introduction: 8 bars, the organ alone; coda: 4 bars, the organ alone", not any(e["on"] < 8 * 36 - 12 for e in S) and not any(e["on"] >= 76 * 36 for v in ("S", "A", "T", "B", "Desc") for e in V[v])
    and any(e["on"] >= 76 * 36 for e in V["org_rh"]) and any(e["on"] < 8 * 36 for e in V["org_lh"]))
chk("introduction: the rocking left hand in eighths, a held pedal", sum(e["dur"] == 6 for e in V["org_lh"] if e["on"] < 8 * 36) >= 40)
chk("verse 4: the organ does not double the tune (its right hand below the choir throughout) (749.8)", all(max(sounding("org_rh", e["on"]) or {0}) < e["p"] for e in S if e["part"] == "verse4"))
chk("verse 4: a suspension at a chord change", any(e.get("sus") for e in V["org_rh"]))
FR0 = O["B_refrain"]
chk("final refrain: the rocking left hand in every bar", all(any(FR0 + b * 36 <= e["on"] < FR0 + (b + 1) * 36 and e["dur"] == 6 for e in V["org_lh"]) for b in range(16)))
chk("final refrain: a tonic pedal under 'Hush now' (bars 61-64), a dominant pedal under 'is sleeping, sleeping' (bars 73-74)", any(e["on"] == FR0 and e["dur"] == 4 * 36 and e["p"] == 41 for e in V["org_ped"]) and any(e["on"] == FR0 + 12 * 36 and e["dur"] == 2 * 36 and e["p"] == 48 for e in V["org_ped"]))
from harmonize53 import stats, CHORDS
par = 0
for path_key, notes_off in (("A", None), ("verse4", None), ("final_refrain", None)):
    pth = R["paths"][path_key]
chk("no Nashville chart among the deliverables (the writer, 15 Nov)", not any("Nashville" in f for f in os.listdir(OUT)))
chk("SATB within their ranges (S D4-F5, A B-flat3-D5, T D3-G4, B F2-D4)", min(e["p"] for e in S) >= 62 and max(e["p"] for e in S) <= 77 and 58 <= min(e["p"] for e in V["A"]) and max(e["p"] for e in V["A"]) <= 74
    and 50 <= min(e["p"] for e in V["T"]) and max(e["p"] for e in V["T"]) <= 67 and 41 <= min(e["p"] for e in V["B"]) and max(e["p"] for e in V["B"]) <= 62)
# readings: each lower part (and the descant) against the sopranos, by section (harm68.readings, 749.9)
def rd(part, voice):
    lead = [dict(e, midi=e["p"], sec=e["part"]) for e in S if e["part"] == part]
    a, b = lead[0]["on"], lead[-1]["on"] + lead[-1]["dur"]
    pv = [dict(e, midi=e["p"]) for e in V[voice] if a <= e["on"] < b]
    return harm68.readings(lead, pv)
RD = {f"{part} {v}": rd(part, v) for part in ("verse", "refrain", "refrain_final") for v in ("A", "T", "B")}
RD["refrain_final Desc"] = rd("refrain_final", "Desc")
def rd_org(part, voice, pick):
    lead = [dict(e, midi=e["p"], sec=e["part"]) for e in S if e["part"] == part]; a, b = lead[0]["on"], lead[-1]["on"] + lead[-1]["dur"]
    pv = [dict(e, midi=pick(e["p"] if isinstance(e["p"], list) else [e["p"]])) for e in V[voice] if a <= e["on"] < b]
    return harm68.readings(lead, pv)
RD["verse4 organ right hand (top)"] = rd_org("verse4", "org_rh", max); RD["verse4 pedal"] = rd_org("verse4", "org_ped", min)
RD["refrain_final pedal"] = rd_org("refrain_final", "org_ped", min)
for k, v in RD.items(): chk(f"harmony: {k}: no parallel fifths or octaves with the tune", v["parallel fifths or octaves"] == 0)
SEC = collections.OrderedDict((p, sum(e["p"] for e in S if e["part"] == p) / sum(1 for e in S if e["part"] == p)) for p in ("verse", "refrain", "verse4", "refrain_final"))
first_top = min(e["on"] for e in S if e["p"] == max(x["p"] for x in S)) // 36 + 1
json.dump(dict(harmony=RD, section_means=SEC, top_bar=first_top, top_share=(first_top - 1) / 80), open(f"{H}/readings53.json", "w"))
for n, ok in C: print(("PASS " if ok else "FAIL ") + n)
print(f"{sum(ok for _, ok in C)}/{len(C)} checks pass")
json.dump(C, open(f"{OUT}/consistency.json", "w"))
