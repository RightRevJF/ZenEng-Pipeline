"""'Everything That Moves' (song 60): the test report, the engine's record (kept apart from the songbook). Read from lyric60.song.json and the
document checks (consistency60.json, out/demo_report.pkl). Writes test_report60.md and out/<file title> - test report.docx."""
import json, os, pickle, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import keyinfo60 as KI
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(HERE, "lyric60.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency60.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = R["melody"]; J = R["judge7"]; S = R["spec"]
CK = R["checks"]; BC = R["band_checks"]; TG = S["target"]; PG = CK["the page gate: each part, and the share of kept tunes the song is plainer than"]
ck = lambda p: CK[next(k for k in CK if k.startswith(p))]
md = [f"# {REC['title']} ({REC['edition']}): test report", "", "Words and music: Jason Bryant", "",
      "Song 60 (songs/p70), from the writer's paper on near-1/f scaling in animal sound across two phyla (CrossPhylum v2) and the C. elegans crawling check: written end to end from a new lyric with `lib/luthier/song_from_lyric.py` on main at 14f7eeb (v36 merged), with no change to the engine during the song. The pick chanted, so the method's re-pick was offered (below); the writer kept the engine's pick. Song 59 stays the hold-out; nothing here was fitted to it. This report is the engine's record; the songbook is for musicians.", "",
      "## What a person typed", "",
      "The title; the words by section (the second chorus typed out); settings: metre 4/4, bpm 116, voice baritone, lead guitar, mode major, genre soul / r&b (the engine has no funk or disco tables; the writer's lane is funk-disco), seed 1. The record was written once and not changed; the documents add an arrangement read from it (below).", "",
      "## The run", "",
      f"- Key {R['key']['key']} ({R['key']['lowest']} to {R['key']['highest']}); other keys offered: " + ", ".join(k["key"] for k in R["other_keys"]) + ".",
      f"- Chords: draft {R['chord_pick']['draft']} of {R['chord_pick']['drafts']}, charge {R['chord_pick']['charge']}.",
      f"- Melody: {M['survivors']} of {M['made']} builds survive; deaths " + ", ".join(f"{k} {v}" for k, v in M["deaths"].items()) + ".",
      f"- The pick: {M['pick']}, the judge's. Gates: old charge's least half {J['gates_passed']['old_charge_least_half']}, joint gate {J['gates_passed']['joint_gate']}, words' gate {J['words_gate']['pass_after_the_other_gates']} (at least {J['words_gate']['at_least']}).",
      f"- Distance {J['pick_distance']} (gate {J['gate']}); directed readings, printed only: " + ", ".join(f"{k} {round(v, 3)}" for k, v in J["pick_directed"].items()) + ".",
      f"- Flags: " + "; ".join(R["flags"]) + ".", "",
      "## The record's checks", "", "| Check | Reading |", "|---|---|"]
for k, v in CK.items(): md.append(f"| {k} | {v} |")
md += ["", "## The band's checks", "", "| Check | Reading |", "|---|---|"]
for k, v in BC.items(): md.append(f"| {k} | {v} |")
md += ["", "## Research checks (the offline rules)", "",
       f"- Metre and stress: long notes on stressed syllables {ck('long notes on stressed')} (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat {ck('the title')} (kept 0.73).",
       "- One song-wide intensity curve: section levels " + ", ".join(f"{k} {v}" for k, v in R["levels"].items()) + ". Read from the demo (band only): " + ", ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR["energy"]) + ". Each chorus above its verse; the last chorus reads highest, the break below it (the horn stabs lift the choruses).",
       f"- Perception: sung phrases {BC['sung phrases, seconds (median, longest)']} s; over 12 beats, share and longest in beats, {BC[next(k for k in BC if k.startswith('sung phrases over 12 beats'))]} (kept 0.042); chord voicings inside the low-interval limits; no accompaniment a second from a sung note.",
       f"- Two channels and chromatic harmony: chords from outside the key, share {round(R['chord_pick']['readings']['share from outside the key'], 3)}.",
       "", "## Readings the paper does not give", "",
       f"- The aim: the kept song {TG['kept_song'].replace('_', ' ')}. Its readings: " + ", ".join(f"{k} {v}" for k, v in TG['readings'].items()) + f". The run cap {TG['run']} (its own longest run, 17, capped); melismas at its share, {TG['melisma_share']} syllables in 100 (932); the step fit kept round {TG['moves_fit_kept_round']} of {len(TG['moves_fit']['rounds'])}.",
       f"- The page gate, as sung: plainness {PG['plainness'][0]}, plainer than {PG['plainness'][1]} kept tunes in 100; time on the tonic plainer than {PG['time_on_tonic'][1]} in 100. Four-note figures already sung, first 120 notes, {ck('four-note figures already sung')} (kept quartiles 0.241, 0.362, 0.455).",
       f"- The chorus's median over the verse's: {ck(chr(34) + 'x')[0] if False else ck('the chorus' + chr(39) + 's median over')} semitones, the plan's lift {CK['the plan' + chr(39) + 's lift']} (838 passes within two). The chorus climbs inside itself: its top, A3, on “groove” in every chorus.",
       f"- Breaths: silences of a beat or more per 100 beats and their median, {ck('silences of a beat')} (kept 7.0, 9.1, 11.1). Lines run on with under a beat of rest {ck('lines that run on')} (kept quartiles 0.095, 0.253, 0.426).",
       f"- Length: {ck('length in seconds')} s.", "",
       "## The chant and the re-pick", "",
       "The pick chants: the verses sit on E3 for 70 notes in 100, a run of 10 of one pitch as sung (kept 90th percentile 9.5). The aimed song's own longest run is 17, capped at 10, so the gate let it through by design. The method's re-pick (`songs/p70/repick60.py`): the judge's own rule over the same run's builds with no run over 9 (52 of the 88 set aside). It drew 7205d09f0ede in B (capo 2): verses that move (commonest note 36 in 100), but a chorus on D♯3 for 53 notes in 100 that never climbs (B2 to F♯3). Both demos went to the writer; he kept the engine's pick. The re-pick's record is kept as `lyric60.nochant.song.json`.", "",
       "## The arrangement added to the record", "",
       "The writer chose a funk-disco lane: a busy bass line, sixteenth-note hi-hat, rhythm guitar, horns on the chorus. The engine's soul / r&b band gives four on the floor, eighth hats, eighth guitar, quarter-note bass. `build60.py` adds, read from the engine's parts and nothing invented: the bass's quarters split into eighths, root then octave (the octave kept only where it stays two semitones under every sung note then); the hats split into sixteenths; horn stabs on 1 and the and of 2 in every chorus from the guitar's top two notes; the break's tune given to the horns. The document checks test each against the engine's parts.", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else ('not met' if c['check'].startswith('READING') else 'FAIL')}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
md += ["", "## Findings", "",
       "For the next list (from 749.123).", "",
       "- An aim that chants lets the pick chant: the run cap is the aimed song's own longest run (capped at 10), so a pick can sit on one note for 70 in 100 verse notes. The method's chant check then offers a re-pick, and here the re-pick lost the chorus's climb. The cap and the chant check disagree on what a kept song allows.",
       "- 784 of 1,000 builds die at the join before a copy (780).",
       "- The chorus's median sits where the verse's does (0 against a plan of 2), yet the chorus plainly climbs to the song's chorus top: the median reading misses a climb inside the chorus.",
       "- One harmony note crosses the lead by more than an octave (bar 95, G♯4 over G♯3).",
       "- No funk or disco tables: the soul / r&b band is plainer than the lane, and the documents had to add the bass octaves and sixteenth hats."]
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report60.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report60.md"), "-o", os.path.join(OUT, REC["file_title"] + " - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
