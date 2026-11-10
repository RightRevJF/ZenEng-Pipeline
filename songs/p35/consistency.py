"""The First Wood -- every document against the song record."""
import pickle, re, sys, subprocess, collections
sys.path[:0] = ["/home/claude/p35", "/home/claude/carol", "/home/claude/pop"]
import mido
from lily import midi_readback
import lyric as L, intake as I, melody_p35 as M
REC = pickle.load(open("/home/claude/p35/song_record.pkl", "rb")); EV = REC["events"]; OUT = "/home/claude/p35/out"
MR = pickle.load(open("/home/claude/p35/melody_result.pkl", "rb")); VO = pickle.load(open("/home/claude/p35/voices.pkl", "rb")); RD = pickle.load(open("/home/claude/p35/readings.pkl", "rb"))
SB = open("/home/claude/p35/songbook.md").read(); TR = open("/home/claude/p35/test_report.md").read()
SC = open(f"{OUT}/The First Wood - score (choir and organ).ly").read(); LS = open(f"{OUT}/The First Wood - lead sheet.ly").read()
PT = open(f"{OUT}/The First Wood - parts (choir and organ).ly").read(); NC = open(f"{OUT}/nashville.html").read()
res = []
def chk(n, ok, info=""): res.append((n, bool(ok), info))
P = lambda part, st=None: [e for e in EV if e["part"] == part and (st is None or e.get("stanza") == st)]
PICK = MR["alive"][0]; tune = PICK["notes"]; ps = [n["p"] for n in tune]
chk("the record is the pick (no hand edits)", REC["fp"] == PICK["fp"] == VO["fp"] and REC["hand_edits"] == [])
chk("form: 104 bars, 3:23 (intro 8 + 4 x 24)", REC["nbars"] == 104 and round(REC["seconds"]) == 203 and "104 bars, about 3:23" in SB)
chk("summit: D5 once, on 'first' (165)", ps.count(74) == 1 and max(p for p in ps if p != 74) <= 72 and M.WORDS[0]["R1"][[n for n in tune if n["p"] == 74][0]["syl"]][0] == "first")
chk("tune range C4-D5", min(ps) == 60 and max(ps) == 74 and "C4–D5" in SB)
for st in (1, 2, 3, 4):
    chk(f"stanza {st}: the sopranos sing the tune", [e["pitch"] for e in sorted(P("S", st), key=lambda e: e["abs12"])] == ps)
chk("stanza 1 in unison (altos on the tune, tenors and basses an octave below)", [e["pitch"] for e in sorted(P("A", 1), key=lambda e: e["abs12"])] == ps and
    [e["pitch"] for e in sorted(P("T", 1), key=lambda e: e["abs12"])] == [p - 12 for p in ps] and [e["pitch"] for e in sorted(P("B", 1), key=lambda e: e["abs12"])] == [p - 12 for p in ps])
s3 = 8 + 24 * 2
chk("stanza 3 unaccompanied: no organ in bars 57-80 (the organ gives stanza 4's pickup on bar 80's beat 3)", not [e for e in EV if e["part"].startswith(("Organ", "Pedal")) and s3 <= e["bar"] < s3 + 24 and e.get("stanza") != 4]
    and all(e["slot"] == 24 and e["bar"] == s3 + 23 for e in EV if e["part"].startswith(("Organ", "Pedal")) and s3 <= e["bar"] < s3 + 24))
chk("stanza 4: the tune an octave higher in the organ", sorted(e["pitch"] for e in P("Organ 4ft")) == sorted(p + 12 for p in ps))
chk("introduction: the organ alone, bars 1-8 (the choir's pickup on bar 8's beat 3)", all(e["bar"] == 7 and e["slot"] == 24 for e in EV if e["bar"] < 8 and e["part"] in ("S", "A", "T", "B")) and [e for e in EV if e["bar"] < 8 and e["part"] == "Organ RH"])
# the closes (138)
fin = {ln: [n for n in tune if n["line"] == ln][-1] for ln in M.LINES}
ch = lambda t: [v for v in REC["voices"] if v["on"] <= t < v["end"]][0]
closes = {ln: ((fin[ln]["p"] - 5) % 12, ch(fin[ln]["on"])["chord"]) for ln in M.LINES}
chk("cadences: lines 1, 3 on G over V; line 2 and refrain 1 on A over I; line 4 and refrain 2 on F over I (138)",
    closes == {"L1": (2, "V"), "L2": (4, "I"), "L3": (2, "V"), "L4": (0, "I"), "R1": (4, "I"), "R2": (0, "I")}, closes)
ov = M.outer(tune, PICK["harm"])
chk("outer-voice gates hold on the pick (136)", ov["contrary"] + ov["oblique"] > ov["similar"] + ov["parallel"] and ov["parallel_perfect"] <= 0.10 and ov["imperfect"] >= 0.25)
chk("pitch and rhythm bands hold on the pick (153, 163)", M.PBAND["p05"] <= PICK["meas"]["pitch_bits"] <= M.PBAND["p95"] and M.RBAND["p05"] <= PICK["meas"]["rhythm_bits"] <= M.RBAND["p95"])
chk("rhythm floor and pushed notes (147, 159)", PICK["meas"]["repetition"]["rhythm_recurs"] >= 0.38 and PICK["meas"]["pushed"] == 0)
chk("declamation: every line's last stress on a downbeat (161)", PICK["meas"]["last_stress_strong"] == 1.0)
chk("sequences of two legs at most (148)", all(l <= 2 for l in PICK["meas"]["legs"]))
# the inner voices
V = VO["voices"]
def par(a, b):
    import itertools
    for i, j in itertools.combinations(range(4), 2):
        if None in (a[i], a[j], b[i], b[j]): continue
        if (a[i] - a[j]) % 12 == (b[i] - b[j]) % 12 and (b[i] - b[j]) % 12 in (0, 7) and a[i] != b[i] and a[j] != b[j] and (b[i] > a[i]) == (b[j] > a[j]): return True
    return False
sop = lambda t: (M.sounding(tune, t) or {"p": None})["p"]
rows = [(sop(v["on"]), v["alto"], v["tenor"], v["bass"]) for v in V]
chk("inner voices: no parallel fifths or octaves in any pair; no crossing", not any(par(a, b) for a, b in zip(rows, rows[1:])) and all((s is None or s >= a) and a >= t >= b for s, a, t, b in rows))
chk("inner voices: no voicing relaxed", VO["relaxed"] == [])
N = 'C D♭ D E♭ E F G♭ G A♭ A B♭ B'.split(); nm = lambda p: N[p % 12] + str(p // 12 - 1)
rng = {part: (nm(min(e["pitch"] for e in P(part, 2))), nm(max(e["pitch"] for e in P(part, 2)))) for part in ("A", "T", "B")}
chk("songbook: the voices' ranges as the record", f"B♭3–G4" in SB and "E3–E4" in SB and "F2–G3" in SB and rng == {"A": ("B♭3", "G4"), "T": ("E3", "E4"), "B": ("F2", "G3")}, rng)
# readback
for part, n in (("S", "sop"), ("A", "alto"), ("T", "ten"), ("B", "bas")):
    want = [e["pitch"] for e in sorted(P(part, 2), key=lambda e: e["abs12"])]
    got = midi_readback(f"{OUT}/check/check_{part}.midi")[0]
    chk(f"score readback ({part}, stanza 2)", got == want, (len(got), len(want)))
pages = lambda f: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
chk("pages: score 1, lead sheet 1, parts 5, chart 1 (as the songbook says)", (pages(f"{OUT}/The First Wood - score (choir and organ).pdf"), pages(f"{OUT}/The First Wood - lead sheet.pdf"),
    pages(f"{OUT}/The First Wood - parts (choir and organ).pdf"), pages(f"{OUT}/The First Wood - Nashville chart.pdf")) == (1, 1, 5, 1) and "(1 page)" in SB and "Parts (5 pages)" in SB)
mf = mido.MidiFile(f"{OUT}/The First Wood - demo (General MIDI).mid")
chk("demo MIDI: 3/4, q = 92, F", any(m.type == "time_signature" and m.numerator == 3 for m in mf.tracks[0]) and any(m.type == "set_tempo" and round(mido.tempo2bpm(m.tempo)) == 92 for m in mf.tracks[0]))
DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
chk("stems: the choir >= +3 dB over the organ", DR["stems_db"] >= 3.0, round(DR["stems_db"], 1))
EN = REC["energy"]
chk("energy: stanza 4 the top (141, 142)", EN["Stanza 4"]["E"] == max(v["E"] for v in EN.values()))
# songbook facts
for t in ("bar 18", "B♭3–G4", "Stanza 3 is unaccompanied", "\"Joseph Dearest, Joseph Mine\"", "\"Away in a Manger\"", "\"Once in Royal David's City\""): chk(f"songbook says: {t}", t in SB)
chords = {ln: [] for ln in M.LINES}
from lily35 import chord_text
bounds = dict(L1=(-12, 132), L2=(132, 276), L3=(276, 420), L4=(420, 576), R1=(576, 708), R2=(708, 864))
for v in REC["voices"]:
    for ln, (a, b) in bounds.items():
        if a <= v["on"] < b: chords[ln].append(chord_text(v["chord"], v["bass"]))
chk("songbook session chords as the record", "C7/B♭ · F/A B♭ · F/A E°/G · F/A B♭/D · C" in SB and chords["L1"] == ["C7/B♭", "F/A", "B♭", "F/A", "E°/G", "F/A", "B♭/D", "C"] and
    "Am/C · Dm C7/E F · Gm C · F" in SB and chords["R2"] == ["Am/C", "Dm", "C7/E", "F", "Gm", "C", "F"], chords["L1"])
eng = re.findall(r"\b(Module|fix(?:es)? \d|composite|realness|gate|v8\d|v7\d|engine|DEFAULT|bits)\b", SB)
chk("songbook: no engine terms", not eng, eng[:5])
cred = "Words and music: Jason Bryant"
chk("credit on every document", all(cred in x for x in (SB, SC, LS, PT, NC, TR)))
low = " ".join(L.SUNG).lower()
chk("never-say: none in the lyric", not [w for w in I.NEVER_SAY if re.search(rf"\b{w}\b", low)] and not [p for p in I.NEVER_PHRASES if p in low])
chk("the title words in every refrain", all("first wood" in ls[4][1].lower() for _, ls in L.SECTIONS))
chk("test report: findings 178-187; the gate table; the rule table; the blind pick pending", all(f"\n{n}. **" in TR for n in range(178, 188)) and "| outer voices: parallel perfects (136) | 0 | 0 | 209 |" in TR
    and "| 155 |" in TR and "Song 35: (pending)." in TR)
chk("test report: the search's counts as the record", f"Survivors:** {MR['survivors']} (17.2%)" in TR and MR["order_fp"] in TR and MR["deaths"]["sequence legs (148)"] == 7 and MR["would"]["sequence legs (148)"] == 14)
for n, ok, info in res: print(("PASS " if ok else "FAIL ") + n + (f"  {info}" if not ok and info != "" else ""))
print(f"{sum(ok for _, ok, _ in res)}/{len(res)} consistent")
