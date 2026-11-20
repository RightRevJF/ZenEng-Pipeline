"""'Same Time Tomorrow' (song 58): the test report, the engine's record (kept apart from the songbook). Read from lyric58.song.json and the
document checks (consistency58.json, out/demo_report.pkl). Writes test_report58.md and out/Same Time Tomorrow - test report.docx."""
import json, os, pickle, subprocess, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import keyinfo58 as KI
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(HERE, "lyric58.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency58.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = R["melody"]; J = R["judge7"]; S = R["spec"]
md = [f"# Same Time Tomorrow ({REC['edition']}): test report", "", "Words and music: Jason Bryant", "",
      "Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v32 (main at 91db1a6). This report is the engine's record; the songbook is for musicians.", "",
      "## What a person typed", "",
      "The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: " +
      ", ".join(f"{k} {S.get(k, json.load(open(os.path.join(HERE, 'lyric58.json'))).get(k))}" for k in ("metre", "bpm")) + ", voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage19.md).", "",
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
       "- 899: line ends drawn with their rest (`studies/kept_checks/line_ends_engine.py`). Stressed line-final syllables an eighth or less 0.35, a half or more 0.19 (kept, ties read, pooled 0.18, 0.29); lines run on with under a beat of rest 0.29 (kept 0.295); rest median 15 twelfths.",
       "- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 1 of 14 line ends (kept 42 in 100, ties read; 6 of 14 under v31). 922 and 924, the page gate read as sung: plainness 0.353, plainer than 76 kept tunes in 100 (floor, the kept 10th, -0.64; all 76 builds read pass); four-note figures already sung 0.465 (kept quartiles 0.470, 0.560, 0.676), in the first 120 notes 0.293 (0.241, 0.362, 0.455).",
       "- Breaths: silences of a beat or more 8.9 per 100 beats (kept 7.1, 8.6, 10.4). Phrases split at half a beat: longest 12.75 beats (kept songs' longest, quartiles 8, 12, 15.5). A four-bar turn after chorus 1.",
       "- 920, 925 to 927, the aim: the song aims at the kept song Bird Dog. Range 10 (Bird Dog 9); longest run of one pitch 9 (9); repeated notes 0.363 (0.373); chorus over verse 2 semitones (its lift 0, the plan's gate allows two). It does not follow Bird Dog's repetition: bars on a figure already sung 0.184 (0.698), bars on a rhythm already sung 0.282 (0.774), distinct rhythms over bars 0.718 (0.226), all three beyond the kept 10th to 90th on the far side from Bird Dog (749.109).",
       f"- 900: the guitar under {R['band_checks'].get('sung notes with the chordal part sounding under them, share (892)')} of the sung notes.",
       f"- Length: {R['checks']['length in seconds (kept quartiles 165, 206, 243)']} s; 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).",
       "- 749.77 (closed): with ties read, kept stressed syllables a sixteenth long inside lines, first verse and chorus 0.109, later ones 0.108.", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else ('not met' if c['check'].startswith('READING') else 'FAIL')}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
md += ["", "## Findings", "",
       "Numbered from 749.105; each has Problem, Evidence, Fix and Check in the list for v33 (`songs/p68/fixlist_v33.md` and its Doc).", "",
       "- 749.105 (a fault) The hymn engine cannot run: 926's run cap is set only when a 4/4 engine is made, so song 53 stops with an error. The cap is also shared by every engine in one process.",
       "- 749.106 926 passes over two builds in three in song 54, mostly one note over the cap, and mostly where the draw does not check (a copied line's join, a melisma); the builds it passes over repeat their figures more.",
       "- 749.107 The page floor keeps range and leaps: without them it passes over 6 of 44 in song 55 instead of 7, and the pick is the same; the builds it passes over are surprising and repeat little.",
       "- 749.108 The steps do not follow the aim: one weight for every song, so song 58's builds step more than Bird Dog and song 54's less than its aim.",
       "- 749.109 The repeats and the rhythm do not follow the aim: song 58 aims at a kept song that repeats its bars more than nine kept songs in ten and repeats them less than nine in ten.",
       "- Answered: 924 to 927 hold as written (the floor reads as sung; the lift, the run, the range follow the aimed song). Carried: 749.103 (two-sided variety 1.18 against the kept 10.5), 749.104's fix, 749.101.",
       "- Carried open: 749.61 (6/8)."]
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report58.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report58.md"), "-o", os.path.join(OUT, REC["file_title"] + " - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
