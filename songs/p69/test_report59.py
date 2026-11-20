"""'Before the Bread Goes Cold' (song 59): the test report, the engine's record (kept apart from the songbook). Read from lyric59.song.json and the
document checks (consistency59.json, out/demo_report.pkl). Writes test_report59.md and out/Same Time Tomorrow - test report.docx."""
import json, os, pickle, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import keyinfo59 as KI
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(HERE, "lyric59.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency59.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = R["melody"]; J = R["judge7"]; S = R["spec"]
md = [f"# {REC['title']} ({REC['edition']}): test report", "", "Words and music: Jason Bryant", "",
      "Song 59 (songs/p69), the hold-out test of Luthier v34 as merged (main at b6bf0e9): written end to end from a new lyric with `lib/luthier/song_from_lyric.py`, with no change to the engine during the song and the pick taken as drawn. This report is the engine's record; the songbook is for musicians.", "",
      "## What a person typed", "",
      "The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: " +
      ", ".join(f"{k} {S.get(k, json.load(open(os.path.join(HERE, 'lyric59.json'))).get(k))}" for k in ("metre", "bpm")) + ", voice baritone, lead guitar, mode major, genre rock, seed 1. Nothing else was typed or chosen by hand. The record was written once, on main at b6bf0e9, and not changed.", "",
      "## The run", "",
      f"- Key {R['key']['key']} ({R['key']['lowest']} to {R['key']['highest']}); other keys offered: " + ", ".join(k["key"] for k in R["other_keys"]) + ".",
      f"- Chords: draft {R['chord_pick']['draft']} of {R['chord_pick']['drafts']}, charge {R['chord_pick']['charge']}.",
      f"- Melody: {M['survivors']} of {M['made']} builds survive; deaths " + ", ".join(f"{k} {v}" for k, v in M["deaths"].items()) + ".",
      f"- The pick: {M['pick']}, the first build past the gates in the order built (traced: build 0). Gates: old charge's least half {J['gates_passed']['old_charge_least_half']}, joint gate {J['gates_passed']['joint_gate']}, words' gate {J['words_gate']['pass_after_the_other_gates']} (at least {J['words_gate']['at_least']}; builds' fit quartiles {J['words_gate']['builds_fit_quartiles']}).",
      f"- Distance {J['pick_distance']} (gate {J['gate']}); directed readings, printed only: " + ", ".join(f"{k} {round(v, 3)}" for k, v in J["pick_directed"].items()) + ".",
      f"- Flags: " + "; ".join(R["flags"]) + ".", "",
      "## The record's checks", "", "| Check | Reading |", "|---|---|"]
for k, v in R["checks"].items(): md.append(f"| {k} | {v} |")
md += ["", "## The band's checks", "", "| Check | Reading |", "|---|---|"]
for k, v in R["band_checks"].items(): md.append(f"| {k} | {v} |")
md += ["", "## Research checks (the offline rules)", "",
       f"- Metre and stress: long notes on stressed syllables {R['checks']['long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65)']} (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat {R['checks'][next(k for k in R['checks'] if k.startswith('the title'))]} (kept 0.73).",
       "- One song-wide intensity curve: section levels " + ", ".join(f"{k} {v}" for k, v in R["levels"].items()) + ". Read from the demo (band only): " + ", ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR["energy"]) + ". Each chorus is above its verse and the last chorus reads highest: 9.12 met.",
       "- A breath, then a fresh re-entry: the 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65). Breaths are read below.",
       f"- Perception: sung phrases {R['band_checks']['sung phrases, seconds (median, longest)']} s, over 12 beats, share and longest in beats, {R['band_checks'][next(k for k in R['band_checks'] if k.startswith('sung phrases over 12 beats'))]} by the half-beat rule (906; kept 0.042); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note {R['band_checks'].get('sung notes with the guitar above them, share (no kept figure; not a fault)')}, printed without a kept figure (900).",
       f"- Two channels and chromatic harmony: chords from outside the key, share {round(R['chord_pick']['readings']['share from outside the key'], 3)} (" + "; ".join(sorted({f"{c} in the {sec.lower()}" for sec, bars_ in R['chords'].items() for b_ in bars_ for c in b_.split() if KI.nashville(c) not in ('1', '2m', '3m', '4', '5', '6m')})) + "); the bass's chromatic notes are passing notes.",
       "", "## Readings the paper does not give", "",
       "- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.21, a half or more 0.10 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.37 (kept 0.295); rest median 12 twelfths.",
       "- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 5 of 5 line ends (kept 42 in 100, ties read). 922 and 924, the page gate read as sung: plainness -0.084, plainer than 46 kept tunes in 100 (floor -0.64; 19 of 20 builds read pass); four-note figures already sung 0.434 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.172 (0.241, 0.362, 0.455).",
       "- Breaths: silences of a beat or more 6.2 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 14 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1; an eight-bar break after chorus 2, the lead guitar on verse 1's tune.",
       "- 920, 925 to 933, the aim: the song aims at the kept song Two Hearts (Phil Collins, 1989). Melismas drawn at its share, 7.1 syllables in 100 (932). The step fit kept round 2 of 6 (step 1.208, leap 0.717); its rounds read 9 to 17 builds of 80, for half the trial builds died in the rhythm draw. Range: the aim is 24, past the baritone's span; the tops were set for 22; the builds span 17 at the median, the pick 20.",
       f"- 900: the guitar under {R['band_checks'].get('sung notes with the chordal part sounding under them, share (892)')} of the sung notes.",
       f"- Length: {R['checks']['length in seconds (kept quartiles 165, 206, 243)']} s. Deaths: half the thousand builds died before a pitch was drawn, the syllables not fitting the window (the verse lines run 11 to 14 syllables at 120 beats a minute, set in three-bar slots).", "",
       "## The hold-out readings", "",
       "Read after the song was built (`studies/holdout59/`). soundness.py on the record alone: no check past the kept 10th to 90th; three of the 21 checks read on kept songs outside the kept middle half (fit by place high, moves by step low, silences low). A single kept song stands outside the middle half on a median of 10 (quartiles 9, 12); 1 kept song in 147 stands outside on 3 or fewer. Songs 55, 54 and 58 stand outside on 6, 6 and 5. The three-song rule passes on every three of songs 55, 54, 58 and 59; with song 59 in, no check leans past the kept quartiles.",
       "Against its aimed song (every living build's median, aimpool readings): it sits within a fifth of the kept middle half's width of Two Hearts on most checks, nearer than songs 55, 54 and 58 sit to theirs, because Two Hearts sits near the kept middle. Where Two Hearts leaves the middle, the builds do not follow: range 17 against 24, repeated notes 0.336 against 0.21, rhythm scaling 0.676 against 0.593.", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else ('not met' if c['check'].startswith('READING') else 'FAIL')}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
md += ["", "## Findings", "",
       "For the next list (from 749.113).", "",
       "- Out of sample, the songs sit nearer the kept middle than almost any kept song (749.103 holds on a new lyric).",
       "- Where the aim leaves the middle, the builds stay in it: range, repeated notes and rhythm scaling did not follow Two Hearts (749.111 and 749.109 hold on a new lyric).",
       "- Long lines at a quick tempo kill half the builds in the rhythm draw, and the step fit then reads too few builds a round to be trusted.",
       "- The break's lead guitar makes the break read as the demo's loudest section, above the last chorus (9.12 not met as a reading)."]
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report59.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report59.md"), "-o", os.path.join(OUT, REC["file_title"] + " - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
