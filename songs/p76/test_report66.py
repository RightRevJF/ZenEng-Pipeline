"""'They Did the Right Thing' (song 66): the test report, the engine's record (kept apart from the songbook). Read from run/engine.log and
lyric66.song.json (the engine's own run), run_d/lyric66_d.song.json (the design run in A minor), lyric66_d.hand.song.json (the design notes laid on),
consistency66.json and out/demo_report.pkl. Writes test_report66.md and out/They Did the Right Thing (first edition) - test report.docx."""
import json, os, pickle, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import keyinfo66 as KI
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
E0 = json.load(open(os.path.join(HERE, "lyric66.song.json"))); D = json.load(open(os.path.join(HERE, "run_d", "lyric66_d.song.json")))
H = json.load(open(os.path.join(HERE, "lyric66_d.hand.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency66.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = D["melody"]; J = D["judge7"]; HE = H["hand_edits"]
ns = sorted(REC["lead"], key=lambda n: n["on"]); run = best = 1
for a, b in zip(ns, ns[1:]):
    run = run + 1 if a["midi"] == b["midi"] else 1; best = max(best, run)
def first8(s):
    st = next(st for s_, nb, st, _, _ in REC["plan"] if s_ == s); v = [n["midi"] for n in ns if n["sec"] == s and n["on"] < st + 8 * 48]
    return v
br = first8("Bridge"); brc = collections.Counter(br).most_common(1)[0]
SH = {}
for s_, nb_, st_, _, _ in REC["plan"]:
    v = first8(s_)
    if v: c_ = collections.Counter(v).most_common(1)[0]; SH[s_] = (KI.pitch_name(c_[0]), c_[1], len(v))
OVER = [f"{s_} {p_} {k_} of {n_}" for s_, (p_, k_, n_) in SH.items() if k_ / n_ > 0.44]
E = {r["sec"]: r["energy_read"] for r in DR["energy"]}
top = max(E, key=E.get); tot = REC["end"]; c3 = next(st for s, nb, st, _, _ in REC["plan"] if s == "Chorus 3"); c3e = c3 + next(nb for s, nb, st, _, _ in REC["plan"] if s == "Chorus 3") * 48
md = [f"# They Did the Right Thing ({REC['edition']}): test report", "", "Words and music: Jason Bryant", "",
      "Song 66 (songs/p76). The engine is Luthier v52 (main at 5dd5ba8), every trial switch off. This report is the engine's record; the songbook is for musicians.", "",
      "## Intake", "",
      "The writer's older lyric, revised with him and locked; the mouth tests read before any music (`mouth_readings.txt`). Settings: 4/4, ♩ = 72, tenor, guitar lead, minor, genre rock (dark indie folk-rock). "
      "His production notes are kept in `intake.py` (DESIGN_NOTES_FROM_THE_WRITER). Song 66 was first spent as the sealed test of the pair (749.217, `studies/borrow_kept`); those test records are not this song. "
      "The writer chose A minor for it (intake LOG).", "",
      "## The runs", "",
      f"- **The engine as it is** (`lyric66.song.json`, `run/engine.log`): key {E0['key']['key']} ({E0['key']['lowest']} to {E0['key']['highest']}), {E0['melody']['survivors']} of {E0['melody']['made']} builds living. The tune sat 2 to 19 semitones over its written tonic, so in A minor it could only be B2 to E4 or B3 to E5 for a tenor.",
      f"- **The design run** (`design66.py`, `run_d/lyric66_d.song.json`): one design gate, the whole tune inside a tenor (C3 to A4) over an A3 tonic, and the key set to A minor. 4,000 builds: {M['survivors']} living; deaths " + ", ".join(f"{k} {v}" for k, v in M["deaths"].items()) + f". Chord draft {D['chord_pick']['draft']} of {D['chord_pick']['drafts']}. The pick {M['pick']}, the first past both gates; {J['pass_the_gate']} builds passed the joint gate (the standard asks 10). Melody {D['key']['lowest']} to {D['key']['highest']} (G3 to A4).",
      f"- Flags: " + "; ".join(D["flags"]) + ".", "",
      "## The writer's design notes, laid by hand (`hand66.py`)", ""]
for e in HE["edits"]:
    if "word" in e: md.append(f"- {e['what']}: “{e['word']}” bar {e['before'][1]:g}, {e['before'][2]:g} beats on MIDI {e['before'][3]} to {e['after'][2]:g} beats on {e['after'][3]}.")
    else: md.append(f"- {e['what']}: " + ", ".join(f"bar {c['bar']} {c['was'] or '(added)'} to {c['now']}" for c in e["chords"]) + ".")
md += [f"- Parts taken out: " + "; ".join(f"{r['part']} {r['removed']} ({r['why']})" for r in HE["removed"] if r["removed"]) + ".",
       f"- The stop: bar {HE['stop']['bar']}, beats {HE['stop']['beats']}. Levels: the bridge 0.55, the tag 0.62, the outro 0.5; the final chorus's band 1.12 times as loud, with a crash on its downbeat.",
       f"- Two harmony notes over the lead (“Still”, bars 36 and 102: G4 over B3) set an octave down.",
       f"- Words' fit: the pick {HE['words_fit_engine']['all']}, after the notes {HE['words_fit_after']['all']}.", "",
       "## The record's checks (the design run)", "", "| Check | Reading |", "|---|---|"]
for k, v in D["checks"].items(): md.append(f"| {k} | {v} |")
md += ["", "## The band's checks", "", "| Check | Reading |", "|---|---|"]
for k, v in D["band_checks"].items(): md.append(f"| {k} | {v} |")
md += ["", "## Research checks (the offline rules)", "",
       f"- Chant: the longest run of one pitch is {best} notes (kept median 6, 90th percentile 9.5). Each section's first eight bars, the commonest pitch: " + "; ".join(f"{s_} {p_} {k_}/{n_}" for s_, (p_, k_, n_) in SH.items()) + ". Over the 0.44 that 956 holds verses to: " + "; ".join(OVER) + ". The verses are under it; the pre-choruses (D4) and the bridge (E4) sit on one note like speech.",
       "- One song-wide intensity curve, read from the demo (band only): " + ", ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR["energy"]) + f". Each chorus above its verse; the top is the final chorus ({E['Chorus 3']:.2f}), bars {c3 // 48 + 1} to {c3e // 48}, {c3 / tot:.2f} to {c3e / tot:.2f} of the song (749.17 asks the high point at 0.65 to 0.85); the bridge the lowest sung section before it, and the tag the release.",
       f"- A breath, then a fresh re-entry: the stop in bar {HE['stop']['bar']} is two beats of silence before the final chorus enters together, at {c3 / tot:.2f} of the song.",
       f"- Perception: sung phrases {D['band_checks']['sung phrases, seconds (median, longest)']} seconds (median, longest; the longest are the designed holds); chord voicings inside the low-interval limits; no accompaniment a second from a sung note.",
       f"- Surprise: the page gate's plainness {D['checks']['the page gate: plainness (floor: the kept 10th percentile, -0.64; kept middle -0.0456)']}.",
       "- Chromatic harmony: the descent's chords (E/D♯, E7/D, A/C♯) are the writer's, under held notes; the engine's own plan uses E (V) as the minor key's dominant.", "",
       "## Findings (for the next list, from 749.219)", "",
       f"- **749.219 A writer's key cannot be asked for.** The engine draws the tune against a written tonic and chooses the key afterwards by range. Its own run put the tonic at the bottom of the tune (D minor for a tenor). To honour the writer's A minor, a design gate kept only tunes inside a tenor over an A3 tonic: {M['deaths'].get('design: the tune inside a tenor over an A3 tonic (the writer' + chr(39) + 's A minor)', 0)} of 4,000 builds died at it, and the joint gate passed {J['pass_the_gate']} (the standard asks 10). Fix: a lyric `key` setting that places the draw's register against that tonic before drawing, so the asked key costs no builds.",
       f"- **749.220 The pitch ceiling reads verses only.** Here the verses are under 0.44, but the pre-choruses put D4 on 20 of 38 notes and the bridge E4 on {brc[1]} of {len(br)} ({brc[1] / len(br):.2f}). It suits a quiet bridge and a pre-chorus that builds on one note, but 956 never read them. Check: read 956 on every sung section and report it; decide by kind whether it holds.",
       "- **749.221 Arrangement the writer designs has no lever.** Every design note here (a held note of set length at a section's end, a bass line under it, an instrument's entry and exit by section, a stop, an added stretch of bars) was laid by hand. Fix: a design file the engine reads, naming these by section, so the record carries them and the checks read them.",
       "- **749.222 The harmony voice sits over the lead.** Twice (“Still”, bars 36 and 102) the engine's harmony note was G4 over the lead's B3, and it reaches A2. Fix: the harmony a third to a sixth under the lead, never over it, inside a stated range.",
       f"- Length: {REC['seconds']:.0f} seconds, past the kept 75th (243): the lyric is long for its tempo (the engine's flag).", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else 'FAIL'}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report66.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report66.md"), "-o", os.path.join(OUT, REC["file_title"] + " - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
