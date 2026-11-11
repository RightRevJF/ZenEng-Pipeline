"""Nothing Important (song 42): every document against song_record.pkl, the design gate and the writer's choices (Q1-Q15)."""
import pickle, re, sys, mido
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p42", "/home/claude/p40"]
import melody_p42 as P
import riff_p42 as RV
M = P.M; H = "/home/claude/p42"; OUT = f"{H}/out"; BAR = 48
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb")); RF = pickle.load(open(f"{H}/riff_p42.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake42", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p42 as L
D = pickle.load(open(f"{H}/melody_p42_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/melody_p42_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/melody_p42_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/melody_p42_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []
NMS = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("piano_rh", "piano_lh", "cello", "bass", "drums", "gtr")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
SL = lambda s: dict((a, n) for a, n, _, _ in REC["plan"])[s]
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
chk(f"the record is the pick of record (255), {REC['fp']}, with no hand edits", REC["fp"] == D["pick"]["fp"] == pick["fp"] and not REC["hand_edits"])
chk("record's sung notes = the melody (only the last note held to the chorus's end)", [(n["on"], n["midi"]) for n in lead] == [(n["on"], n["p"]) for n in pick["notes"]]
    and all(a["dur"] == b["dur"] for a, b in zip(lead[:-1], pick["notes"][:-1])))
chk("the melody passes evaluate: every gate and the design gate", P.evaluate(pick)[0] is None and not P.design_fails(pick))
chk("every writer's choice logged (Q1-Q15)", [str(x["q"]).split(" ")[0] for x in I.LOG] == ["1", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"])
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
low = " ".join(L.SUNG).lower()
chk("Q9 B: no never-say word or phrase; 'the third morning' once, never explained", not (set(re.findall(r"[a-z']+", low)) & set(I.NEVER_SAY)) and not any(p in low for p in I.NEVER_PHRASES) and low.count("third morning") == 1)
chk("Q4: the title is his message's words, sung in the hook and the last chorus", sum("nothing important" in l.lower() for l in L.SUNG) == 4)
chk("Q9 turn: the last line is 'I'll call you back', the only changed line of his message", L.SUNG[-1] == "I'll call you back." and L.SUNG.count("Call me back.") == 2)
chk(f"Q6/Q13: {REC['nbars']} bars; every line two bars", REC["nbars"] == 68 and all(P.slot_len(s, i) == 2 for s in P.SUNG for i in range(len(P.LINES[s]))))
ps = [n["midi"] for n in lead]; g = REC["registers"]
chk(f"Q7/Q8: the voice inside the alto's row F3-D5 ({nm(min(ps))}-{nm(max(ps))}); the song's range drawn centred (unused below {g['song_lo'] - 53}, above {74 - g['song_hi']})",
    min(ps) >= 53 and max(ps) <= 74 and abs((g["song_lo"] - 53) - (74 - g["song_hi"])) <= 1)
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]; cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1", cc1 == cc2)
h0 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; h2 = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 2]
chk("Q10 A: 'hey, it's me' sung again in the chorus on the same notes", [n["midi"] for n in h0[:3]] == [n["midi"] for n in h2[:3]] and [n["on"] - h0[0]["on"] for n in h0[:3]] == [n["on"] - h2[0]["on"] for n in h2[:3]])
lc4 = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 4]; lc5 = [n for n in lead if n["sec"] == "Last Chorus" and n["line"] == 5]; tl = [n for n in h0 if n["syl"] >= 3]
chk(f"Q11 note 4: 'Nothing important' held longer (span {(lc4[-1]['on'] - lc4[0]['on']) / 12:g} beats against {(tl[-1]['on'] - tl[0]['on']) / 12:g}); 'I'll call you back' falls to {nm(lc5[-1]['midi'])}, the tonic, under it",
    lc4[-1]["on"] - lc4[0]["on"] >= 1.5 * (tl[-1]["on"] - tl[0]["on"]) and [n["midi"] for n in lc4] == [n["midi"] for n in tl] and (lc5[-1]["midi"] - M.TONIC) % 12 == 0 and lc5[-1]["midi"] < lc4[-1]["midi"])
q = [b for b in range(P.BAR0["Last Chorus"] + 10, P.BAR0["Last Chorus"] + 12)]
chk("Q11 note 4: the band out under 'I'll call you back' (the piano alone, bars 63-64)", not any(e["on"] // BAR in q for k in ("bass", "drums", "gtr") for e in REC[k]))
chk("Q5: the band only in the last chorus, bars 53-62; the cello from verse 2", {e["on"] // BAR for k in ("bass", "drums", "gtr") for e in REC[k]} <= set(range(52, 62))
    and min(e["on"] for e in REC["cello"]) >= P.BAR0["Verse 2"] * BAR)
# Q7: the piano is a complete song: it plays in every bar, under every sung note, with a chord tone on every bar's first beat
pb = {e["on"] // BAR for e in REC["piano_rh"] + REC["piano_lh"]} | {b for e in REC["piano_rh"] + REC["piano_lh"] for b in range(e["on"] // BAR, (e["on"] + e["dur"] - 1) // BAR + 1)}
cov = all(any(e["on"] <= n["on"] < e["on"] + e["dur"] for e in REC["piano_lh"]) for n in lead)
first = all(any(e["on"] == b * BAR and any(p % 12 == M.CH[REC["bars"][b]["chord"]][0] for p in e["p"]) for e in REC["piano_lh"]) for b in range(REC["nbars"]))
chk("Q7: the piano alone is the whole song: it sounds in every bar, under every sung note, the chord's root on every bar's first beat", pb >= set(range(REC["nbars"])) and cov and first)
chk("Q14 A: the cello holds in verse 2 and chorus 2; its countermelody only in the bridge and the last chorus, under the voice, no semitone or tritone",
    all(e["art"] in ("held", "ring") for e in REC["cello"] if REC["bars"][e["on"] // BAR]["sec"] in ("Verse 2", "Chorus 2"))
    and {REC["bars"][e["on"] // BAR]["sec"] for e in REC["cello"] if e["art"] == "counter"} <= {"Bridge", "Last Chorus"} and RF["counter_check"]["below"] and RF["counter_check"]["semitones"] == 0 and RF["counter_check"]["tritones"] == 0)
chk("235: the piano's intro figure unrelated to every sung line's opening (27.31)", not RV.related_any([dict(on=t, p=p) for t, p in zip(RF["pick"]["ons"], RV.pitches(RF["pick"]["steps"], "Bb"))])[0])
RANGES = dict(piano_rh=(21, 108), piano_lh=(21, 108), cello=(36, 76), bass=(28, 67), gtr=(40, 88))
chk("319: every instrumental note inside its instrument's range", all(RANGES[k][0] <= p <= RANGES[k][1] for k in RANGES for e in REC[k] for p in e["p"]))
chk("one B-flat chord on bar 68, nothing after it", all(e["on"] <= 67 * BAR for k in INSTR for e in REC[k]) and REC["bars"][67]["chord"] == "Bb" and any(e["on"] == 67 * BAR for e in REC["piano_rh"]))
mf = mido.MidiFile(f"{OUT}/Nothing Important - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
chk("demo: the voice track = the melody", sorted(m.note for m in trk("Voice")[0] if m.type == "note_on" and m.velocity > 0) == sorted(ps))
for name, keys in (("Piano", ("piano_rh", "piano_lh")), ("Cello", ("cello",)), ("Bass", ("bass",)), ("Guitar", ("gtr",)), ("Drums", ("drums",))):
    t_ = trk(name); want = sorted(p for k in keys for e in REC[k] for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
chk("demo stems: the voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk("9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/Nothing Important - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("lead sheet: the voice reads back from LilyPond's MIDI", RB["voice"][0])
chk("piano-vocal score: both hands read back from LilyPond's MIDI", RB["piano_rh"][0] and RB["piano_lh"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/Nothing Important - piano-vocal score.ly").read()
chk("score: credit, key, tempo, length, the piano staff", "Words and music: Jason Bryant" in src and "\\key bes \\major" in src and "3:35" in src and "4 = 76" in src and "PianoStaff" in src)
html = open(f"{OUT}/nashville.html").read(); NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "iii": "3m"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s == "Chorus 2": continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords; credit, tempo, key", cells == want and "Words and music: Jason Bryant" in html and "♩ = 76" in html and "KEY: B♭" in html)
import zipfile
_sb = open(f"{H}/songbook.md").read(); _dx = zipfile.ZipFile(f"{OUT}/Nothing Important - songbook.docx").read("word/document.xml").decode()
chk("songbook and its Word copy carry the producer one-sheet, on its own page", "Producer one-sheet" in _sb and "Producer one-sheet" in _dx and _dx.count('w:type="page"') >= 2)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
