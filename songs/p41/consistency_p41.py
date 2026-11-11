"""The Water Used to Sing (song 41): every document against song_record.pkl, the design gates and the writer's choices (Q1-Q20)."""
import pickle, re, sys, mido
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p41"]
import melody_p41 as P
import riff_p41 as RV
M = P.M; H = "/home/claude/p41"; OUT = f"{H}/out"; BAR = 48
REC = pickle.load(open(f"{H}/song_record.pkl", "rb")); F = pickle.load(open(f"{H}/melody_final.pkl", "rb")); pick = F["pick"]
RB = pickle.load(open(f"{OUT}/readback.pkl", "rb")); DR = pickle.load(open(f"{OUT}/demo_report.pkl", "rb")); RF = pickle.load(open(f"{H}/riff_p41.pkl", "rb"))
import importlib.util as _u; _sp = _u.spec_from_file_location("intake41", f"{H}/intake.py"); I = _u.module_from_spec(_sp); _sp.loader.exec_module(I)
import lyric_p41 as L
D = pickle.load(open(f"{H}/melody_p41_main.pkl", "rb")); DRr = pickle.load(open(f"{H}/melody_p41_main_r.pkl", "rb"))
C = pickle.load(open(f"{H}/melody_p41_ctl.pkl", "rb")); Cr = pickle.load(open(f"{H}/melody_p41_ctl_r.pkl", "rb"))
lead = REC["lead"]; ok = []
NMS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]; nm = lambda p: f"{NMS[p % 12]}{p // 12 - 1}"
INSTR = ("drums", "bass", "acou", "egtr", "organ", "counter")
def chk(name, cond): ok.append((name, bool(cond))); print(("PASS " if cond else "FAIL ") + name)
SL = lambda s: dict((a, n) for a, n, _, _ in REC["plan"])[s]
chk(f"both runs made twice give the same order (main {D['order_fp']}, control {C['order_fp']})", D["order_fp"] == DRr["order_fp"] and C["order_fp"] == Cr["order_fp"])
short = [c["fp"] for c in D["alive"] if c["fp"] in set(D["short"])]
chk(f"the record is the pick of record (255), {REC['fp']}, with no hand edits", REC["fp"] == D["pick"]["fp"] == pick["fp"] and not REC["hand_edits"])
sung = [(n["on"], n["midi"]) for n in lead]; mel = [(n["on"], n["p"]) for n in pick["notes"]]
chk("record's sung notes = the melody (only the tag's hold lengthened, the writer's note)", sung == mel and all(a["dur"] == b["dur"] for a, b in zip(lead[:-1], pick["notes"][:-1])))
chk("the melody passes evaluate: every gate and the design gate", P.evaluate(pick)[0] is None)
chk(f"Q16 B: the bridge median under the verse's ({P.med(pick['notes'], 'Bridge') - P.med(pick['notes'], 'Verse 1'):+.1f})", P.med(pick["notes"], "Bridge") < P.med(pick["notes"], "Verse 1"))
chk("every writer's choice logged (Q1-Q20)", [str(x["q"]).split(" ")[0] for x in I.LOG] == [str(k) for k in range(1, 21)])
chk("the locked lyric is the lyric sung, every syllable", all(len(REC["text"][s][i]) == len(P.LINES[s][i]) for s in P.SUNG for i in range(len(P.LINES[s])))
    and all(any(n["sec"] == s and n["line"] == i for n in lead) for s in P.SUNG for i in range(len(P.LINES[s]))))
low = " ".join(L.SUNG).lower()
chk("Q10 B: no never-say word or phrase; 'living water' once", not (set(re.findall(r"[a-z']+", low)) & set(I.NEVER_SAY)) and not any(p in low for p in I.NEVER_PHRASES) and low.count("living water") == 1)
chk(f"Q20 A: form of {REC['nbars']} bars (bridge and verse 3 twelve bars), every 9+ syllable line in two bars", REC["nbars"] == 104 and SL("Bridge") == 12 and SL("Verse 3") == 12
    and all(P.slot_len(s, i) == 2 for s in P.SUNG for i in range(len(P.LINES[s])) if len(P.LINES[s][i]) >= 9))
ps = [n["midi"] for n in lead]
chk(f"Q7: the voice inside the baritone row G2-E4 ({nm(min(ps))}-{nm(max(ps))})", min(ps) >= 43 and max(ps) <= 64)
h0 = [(n["on"] - P.line_start("Chorus 1", 0), n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
h2 = [(n["on"] - P.line_start("Chorus 1", 2), n["midi"]) for n in lead if n["sec"] == "Chorus 1" and n["line"] == 2]
chk("Q11 A: the hook said twice in the chorus (pitches and onsets)", h0 == h2)
cc1 = [(n["on"] - P.BAR0["Chorus 1"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 1"]; cc2 = [(n["on"] - P.BAR0["Chorus 2"] * BAR, n["midi"]) for n in lead if n["sec"] == "Chorus 2"]
chk("chorus 2 = chorus 1", cc1 == cc2)
tag = lead[-1]
chk(f"the song ends on 'It sings.' on the tonic ({nm(tag['midi'])}), held into the outro", tag["sec"] == "Last Chorus" and tag["line"] == 7 and tag["midi"] % 12 == 7 and tag["on"] + tag["dur"] > P.BAR0["Outro"] * BAR)
hook_end = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0][-1]
chk(f"the hook ends on the tonic ({nm(hook_end['midi'])})", hook_end["midi"] % 12 == 7)
sticks = {b["start"] // BAR for b in REC["bars"] if b["kit"] == "sticks"}
want_st = {b for s in ("Chorus 1", "Chorus 2", "Break", "Last Chorus", "Outro") for b in range(P.BAR0[s], P.BAR0[s] + SL(s))} | set(range(P.BAR0["Verse 3"] + 4, P.BAR0["Verse 3"] + 12))
chk("Q19 A: sticks in the choruses, the break, verse 3 from its fifth bar and the outro; brushes elsewhere", sticks == want_st)
chk("Q18 B: the countermelody only in the last chorus, above the voice, no semitone or tritone", REC["counter"] and all(P.BAR0["Last Chorus"] * BAR <= e["on"] < P.BAR0["Outro"] * BAR for e in REC["counter"])
    and RF["counter_check"]["above"] and RF["counter_check"]["semitones"] == 0 and RF["counter_check"]["tritones"] == 0)
chk("235: the lick unrelated to every sung line's opening (27.31)", not RV.related_any([dict(on=t, p=p) for t, p in zip(RF["pick"]["ons"], RV.pitches(RF["pick"]["steps"], "G"))])[0])
chk("235/272: fills only in the voice's gaps, 4-6 notes, ending on a chord tone", all(4 <= len(f["notes"]) <= 6 and f["notes"][-1]["p"] % 12 in M.CH[M.chord_at(f["notes"][-1]["on"])][1] for f in RF["fills"])
    and not any(a < e["on"] + e["dur"] and e["on"] < b for e in REC["egtr"] if e["art"].startswith("fill") for a, b in [(n["on"], n["on"] + n["dur"]) for n in lead]))
chk("233: the bass has the root on beat 1 of every bar it plays", all(e["p"][0] % 12 == M.CH[REC["bars"][e["on"] // BAR]["chord"]][0] for e in REC["bass"] if e["on"] % BAR == 0))
chk(f"the break solo inside the guitar's reach (E4-C6): {nm(min(e['p'][0] for e in REC['egtr'] if e['art'] == 'solo'))}-{nm(max(e['p'][0] for e in REC['egtr'] if e['art'] == 'solo'))}", all(52 <= e["p"][0] <= 84 for e in REC["egtr"] if e["art"] == "solo"))
chk("the bridge has no electric guitar; the bass enters at bar 5", not any(P.BAR0["Bridge"] * BAR <= e["on"] < P.BAR0["Break"] * BAR for e in REC["egtr"]) and min(e["on"] for e in REC["bass"]) == 4 * BAR)
chk("one G chord on bar 104, nothing after it", all(e["on"] <= 103 * BAR for k in INSTR for e in REC[k]) and REC["bars"][103]["chord"] == "G" and any(e["on"] == 103 * BAR for e in REC["acou"]))
mf = mido.MidiFile(f"{OUT}/The Water Used to Sing - demo (General MIDI).mid")
def trk(name): return [t for t in mf.tracks if any(m.type == "track_name" and m.name.startswith(name) for m in t)]
vk = sorted(m.note for m in trk("Voice")[0] if m.type == "note_on" and m.velocity > 0)
chk("demo: the voice track = the melody", vk == sorted(ps))
for name, key in (("Acoustic", "acou"), ("Electric", "egtr"), ("Organ - counter", "counter"), ("Bass", "bass"), ("Drums", "drums")):
    t_ = trk(name); want = sorted(p for e in REC[key] for p in e["p"])
    chk(f"demo {name.lower()} = the record's", len(t_) == 1 and sorted(m.note for m in t_[0] if m.type == "note_on" and m.velocity > 0) == want)
org = [t for t in mf.tracks if any(m.type == "track_name" and m.name == "Organ" for m in t)]
chk("demo organ = the record's", len(org) == 1 and sorted(m.note for m in org[0] if m.type == "note_on" and m.velocity > 0) == sorted(p for e in REC["organ"] for p in e["p"]))
progs = [m.program for m in trk("Drums")[0] if m.type == "program_change"]
chk(f"demo: the drum kit changes with the record (brush 40, standard 0): {progs}", progs[0] == 40 and set(progs) == {0, 40})
chk("demo stems: the voice >= +3 dB over the band", DR["stems_db"] >= 3.0)
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
chk(f"9.12 energy arc: each chorus above its verse; the last chorus the top", E["Chorus 1"] > E["Verse 1"] and E["Chorus 2"] > E["Verse 2"] and E["Last Chorus"] == max(E.values()))
gb = mido.MidiFile(f"{OUT}/The Water Used to Sing - demo (GarageBand).mid")
chk("GarageBand MIDI: ASCII names, no program changes", all(not any(m.type == "program_change" for m in t) for t in gb.tracks) and all(all(ord(ch) < 128 for ch in m.name) for t in gb.tracks for m in t if m.type == "track_name"))
chk("GarageBand MIDI: same notes and times as General MIDI", [sorted((m.note) for m in t if m.type == "note_on") for t in gb.tracks] == [sorted((m.note) for m in t if m.type == "note_on") for t in mf.tracks])
chk("lead sheet: the voice reads back from LilyPond's MIDI", RB["voice"][0])
for k, v in RB["parts"].items(): chk(f"parts, {k}: MIDI readback matches", v[0])
chk("parts, drums: every hit written", RB["drums"][0] == RB["drums"][1])
src = open(f"{OUT}/The Water Used to Sing - lead sheet.ly").read()
chk("lead sheet: credit, key, swing mark, tempo, length, treble-8 clef", "Words and music: Jason Bryant" in src and "\\key g \\major" in src and "4:20" in src and "4 = 96" in src and "Shuffle" in src and 'treble_8' in src)
html = open(f"{OUT}/nashville.html").read(); NUM = {"I": "1", "V": "5", "vi": "6m", "IV": "4", "ii": "2m", "bVII": "♭7"}
cells = re.findall(r"<td>([^<]+)</td>", html); want = []
for s, nb, b0, _ in REC["plan"]:
    if s == "Chorus 2": continue
    want += [NUM[REC["bars"][b]["roman"]] for b in range(b0, b0 + nb)]
chk("chart numbers = the record's chords; credit, tempo, key, shuffle", cells == want and "Words and music: Jason Bryant" in html and "♩ = 96" in html and "KEY: G" in html and "SHUFFLE" in html)
n_pass = sum(1 for _, v in ok if v); print(f"\n{n_pass}/{len(ok)} checks pass")
pickle.dump(ok, open(f"{OUT}/consistency.pkl", "wb"))
