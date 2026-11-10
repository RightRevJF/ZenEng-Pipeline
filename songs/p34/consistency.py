"""Swallowed Up -- every document against the song record. Everything must pass before delivery."""
import pickle, re, os, sys, subprocess, collections
sys.path[:0] = ["/home/claude/p34", "/home/claude/carol"]
import mido
from lily import midi_readback
import lyric as L, intake as I, riffs_p34 as R
REC = pickle.load(open("/home/claude/p34/song_record.pkl", "rb")); EV = REC["events"]; OUT = "/home/claude/p34/out"
RF = pickle.load(open("/home/claude/p34/riffs_frozen.pkl", "rb")); VO = pickle.load(open("/home/claude/p34/voice.pkl", "rb"))
SB = open("/home/claude/p34/songbook.md").read(); TR = open("/home/claude/p34/test_report.md").read()
LS = open(f"{OUT}/Swallowed Up - lead sheet.ly").read(); PT = open(f"{OUT}/Swallowed Up - parts (band and voice).ly").read()
NC = open(f"{OUT}/nashville.html").read()
res = []
def chk(name, ok, info=""): res.append((name, bool(ok), info))
a16 = lambda e: e["bar"] * 16 + e["slot"]
P = lambda part: [e for e in EV if e["part"] == part]

chk("form: 152 bars, 3:22, summed (fix 139)", REC["nbars"] == 152 and round(REC["seconds"]) == 202 and sum(b for _, b, _ in R.FORM) == 152)
chk("the riffs were frozen before the voice and the solo (9-M.4)", REC["riffs_sha"] == RF["sha"] == VO["riffs_sha"] == REC["solo"]["rerun"]["riffs_sha"])
chk("eight riffs (a long song: 9-M.4)", sorted({b["riff"] for b in REC["bars"]}) == ["A", "B", "B'", "C", "D", "E", "F", "G"])
term = all((R.BARS[k]["strokes"] is R.BT) == (R.BARS[k]["i"] % 4 == 3) for k in range(152) if R.BARS[k]["sec"] in ("Riff", "Verse 1", "Verse 2"))
chk("riff B's fourth bar changed, every time (terminal modification)", term)
g1 = sorted((a16(e), e["pitch"]) for e in P("Gtr 1") if e["bar"] >= 8); g2 = sorted((a16(e), e["pitch"]) for e in P("Gtr 2"))
chk("two guitars, the same riff; guitar 1 alone in bars 1-8", g1 == g2 and not [e for e in P("Gtr 2") if e["bar"] < 8] and [e for e in P("Gtr 1") if e["bar"] < 8])
low = collections.defaultdict(lambda: 999)
for e in P("Gtr 1"): low[a16(e)] = min(low[a16(e)], e["pitch"])
chk("bass: the guitar's lowest note an octave below, same rhythm", all(low[a16(e)] - 12 == e["pitch"] for e in P("Bass")) and len({a16(e) for e in P("Bass")}) == len({k for k in low if k >= 8 * 16}))
b120 = R.SEC_FIRST["Slowdown"] + 7
chk("bar 120: beat 4 silent (the gap)", not [e for e in EV if e["bar"] == b120 and e["slot"] >= 12 and e["part"] != "Voice"] and not [e for e in EV if e["bar"] == b120 and e["part"] != "Voice" and e["slot"] + e["dur"] > 12 and e["part"] != "Drums"])
bk = range(R.SEC_FIRST["Slowdown"] + 8, R.SEC_FIRST["Slowdown"] + 16)
uni = all({a16(e) for e in P("Gtr 1") if e["bar"] == b} == {a16(e) for e in P("Bass") if e["bar"] == b} == {a16(e) for e in P("Drums") if e["bar"] == b and e["pitch"] == 36} for b in bk)
chk("the breakdown: guitar, bass and kick in unison", uni)
chk("the breakdown: silence between the strokes", all(e["dur"] <= 2 for e in P("Gtr 1") if e["bar"] in bk))
qmap = {b["q"] for b in REC["bars"][112:128]} == {100} and {b["q"] for b in REC["bars"][:112] + REC["bars"][128:]} == {200}
mf = mido.MidiFile(f"{OUT}/Swallowed Up - demo (General MIDI).mid")
tempos = [(m.time, round(mido.tempo2bpm(m.tempo))) for m in mf.tracks[0] if m.type == "set_tempo"]
chk("tempo map: 200, 100 at bar 113, 200 at bar 129 (record and MIDI)", qmap and [t for _, t in tempos] == [200, 100, 200], tempos)
V = sorted(P("Voice"), key=a16)
acc = lambda b: {s + 16 * k for k in (0, 1) if b + k < 152 for s, d, o, pm in R.BARS[b + k]["strokes"] if not pm}
lockok = all(e["slot"] % 4 == 0 or e["slot"] in acc(e["bar"]) for e in V if e["stressed"])
chk("the voice: every stressed stroke on a beat or an open accent (9-M.7)", lockok and VO["lock"] == 1.0)
chk("the voice: each line ends with a breath before its two-bar cycle ends", all(l["end"] <= 30 for l in REC["voice_lines"]))
fam = {(e["sec_line"][0], e["family"], e["height"]) for e in V}
chk("the voice: verses growl low, choruses and the taunt shout mid, one high scream", all((f == "growl") == s.startswith("Verse") for s, f, h in fam) and
    [e["word"] for e in V if e["height"] == "high"] == ["swallowed", "swallowed", "up"])
bk_voice = [e for e in V if e["bar"] in bk and e["stressed"]]
chk("the breakdown lines: stressed strokes on the unison hits", all(e["slot"] in {s for s, d, o, pm in R.BARS[e["bar"]]["strokes"]} for e in bk_voice))
solo = [e for e in P("Lead") if e.get("src") == "solo"]; top = max(e["pitch"] for e in solo)
chk("the solo: the summit once, B5 in bar 110 (the declared clause)", [e["bar"] + 1 for e in solo if e["pitch"] == top] == [110] and top == 83)
chk("the solo: ends on A# in bar 112", solo[-1]["pitch"] % 12 == 10 and solo[-1]["bar"] + 1 == 112)
chk("the solo: no hand edits", REC["hand_edits"] == [])
EN = REC["energy"]
chk("energy: each chorus above its verse; the last chorus the top (from the record, 141/142)", all(EN[c]["E"] > EN[v]["E"] for v, c in (("Verse 1", "Chorus 1"), ("Verse 2", "Chorus 2"), ("Verse 3", "Chorus 3")))
    and EN["Last Chorus"]["E"] == max(x["E"] for x in EN.values()))
sn = [e for e in P("Drums") if e["pitch"] == 38]
blast = [e["vel"] for e in sn if "Chorus" in REC["bars"][e["bar"]]["sec"]]; back = [e["vel"] for e in sn if "Chorus" not in REC["bars"][e["bar"]]["sec"]]
chk("snare: backbeats 115-120, blasts 125-127, never every stroke at 127 (9-M.9)", min(back) >= 115 and max(back) <= 120 and min(blast) >= 125 and max(blast) <= 127 and 0 < blast.count(127) < len(blast))
DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb"))
chk("stems: the voice >= +3 dB over the band", DR["stems_db"] >= 3.0, round(DR["stems_db"], 1))
# readback files against the record
H = {"low": 67, "mid": 71, "high": 74}
chk("lead sheet readback (voice)", midi_readback(f"{OUT}/check/check_voc.midi")[0] == [H[e["height"]] for e in V])
for nm, part in (("gtr", "Gtr 1"), ("lead", "Lead"), ("bass", "Bass")):
    chk(f"parts readback ({part})", sorted(sum(midi_readback(f"{OUT}/check/check_{nm}.midi"), [])) == sorted(e["pitch"] for e in P(part)))
chk("parts readback (drums)", sorted(sum(midi_readback(f"{OUT}/check/check_dup.midi"), []) + sum(midi_readback(f"{OUT}/check/check_ddown.midi"), [])) == sorted(e["pitch"] for e in P("Drums")))
pages = lambda f: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
chk("pages: lead sheet 2, parts 21, chart 1 (as the songbook says)", (pages(f"{OUT}/Swallowed Up - lead sheet.pdf"), pages(f"{OUT}/Swallowed Up - parts (band and voice).pdf"), pages(f"{OUT}/Swallowed Up - Nashville chart.pdf")) == (2, 21, 1)
    and "Lead sheet (2 pages)" in SB and "Parts (21 pages)" in SB and "Number chart (1 page)" in SB)
# the songbook against the record
ls_bars = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"^- (\d+): (.+)$", SB, re.M)}
want = {l["first_bar"]: dict(L.SECTIONS)[l["sec"]][l["line"]][1] for l in REC["voice_lines"] if l["sec"] in ("Verse 1", "Chorus 1", "Verse 2", "Verse 3", "Slowdown", "Last Chorus")}
chk("songbook lyric sheet: every line at the bar the record puts it", all(ls_bars.get(b, "").startswith(t[:20]) for b, t in want.items()), [b for b, t in want.items() if not ls_bars.get(b, "").startswith(t[:20])])
chk("songbook: the section bars match the form", all(f"| {R.SEC_FIRST[s] + 1}–{R.SEC_FIRST[s] + n} |" in SB or s in ("Slowdown",) for s, n, q in R.FORM) and "| 113–120 | Slowdown |" in SB and "| 121–128 | Breakdown |" in SB)
chk("songbook: the summit (bar 110), the solo's end (A♯4, bar 112), the scream (bar 143), bar 120's silent beat", all(x in SB for x in ("bar 110", "A♯4 over F♯5 in bar 112", "bar 143", "beat 4 silent")))
CH = REC["bars"]
chk("songbook: chorus chords as the record (B5 C5 D5 · F5 E5; last bar F5 E5 C5)", CH[40]["chords"] == ["B5", "C5", "D5"] and CH[41]["chords"] == ["F5", "E5"] and CH[47]["chords"] == ["F5", "E5", "C5"] and "B5 C5 D5 · F5 E5" in SB)
chk("songbook: the solo loop and the slowdown chords as the record", [CH[k]["chords"][0] for k in range(96, 112, 2)] == ["B5", "A5", "G5", "F#5"] * 2 and CH[113]["chords"] == ["C5", "F5"] and CH[117]["chords"] == ["C5", "F5"] and CH[119]["chords"] == ["F5", "C5"]
    and "| E: B5 · C5 F5 (117–118) |" in SB)
chk("songbook: verse 3's half-step move (bars 73-80 on C)", all(CH[k]["riff"] == "B'" for k in range(72, 80)) and CH[80]["riff"] == "B" and "73–80" in SB)
eng = re.findall(r"\b(Module|fix(?:es)? \d|composite|realness|IC\b|CMP|9-M|v7\d|v6\d|preset|engine|DEFAULT)", SB)
chk("songbook: no engine terms (musicians only)", not eng, eng[:5])
chk("songbook: three references, each searched", all(x in SB for x in ('"Pull the Plug"', '"Infecting the Crypts"', '"Scrolls of the Megilloth"')))
chk("songbook: the demo is a reference, not a tone", "not for tone" in SB)
chk("songbook: the producers' four targets", all(f"| {x} |" in SB for x in ("Impact", "Energy", "Precision", "Extremity")))
cred = "Words and music: Jason Bryant"
chk("credit line on every document", all(cred in x for x in (SB, LS, PT, NC, TR)))
low_lyr = " ".join(L.SUNG).lower()
chk("never-say: none in the lyric (v77: a death)", not [w for w in I.NEVER_SAY if re.search(rf"\b{w}\b", low_lyr)] and not [p for p in I.NEVER_PHRASES if p in low_lyr])
chk("the title in every chorus", all("swallowed" in ls[0][1].lower() for s, ls in L.SECTIONS if "Chorus" in s))
chk("every intro bar sounds (fix 144)", all([e for e in P("Gtr 1") if e["bar"] == k] for k in range(16)))
chk("test report: findings 146-154, blind pick pending", all(f"\n{n}. **" in TR for n in range(146, 155)) and "Song 34: (pending)." in TR)
for n, ok, info in res: print(("PASS " if ok else "FAIL ") + n + (f"  {info}" if info not in ("", None) and not ok else ""))
print(f"{sum(ok for _, ok, _ in res)}/{len(res)} consistent")
