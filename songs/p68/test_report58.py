"""'Same Time Tomorrow' (song 58): the test report, the engine's record (kept apart from the songbook). Read from lyric58.song.json and the
document checks (consistency58.json, out/demo_report.pkl). Writes test_report58.md and out/Same Time Tomorrow - test report.docx."""
import json, os, pickle, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(HERE, "lyric58.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency58.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = R["melody"]; J = R["judge7"]; S = R["spec"]
md = [f"# Same Time Tomorrow ({REC['edition']}): test report", "", "Words and music: Jason Bryant", "",
      "Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v24 (main at cc03065). This report is the engine's record; the songbook is for musicians.", "",
      "## What a person typed", "",
      "The title; the words by section, with section names marking returns (the second chorus typed out); seven settings: " +
      ", ".join(f"{k} {S.get(k, json.load(open(os.path.join(HERE, 'lyric58.json'))).get(k))}" for k in ("metre", "bpm")) + ", voice baritone, lead guitar, mode major, genre folk, seed 1. Nothing else was typed or chosen by hand. The record reproduces byte for byte (REVIEW_stage8.md).", "",
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
       f"- Perception: sung phrases {R['band_checks']['sung phrases, seconds (median, longest)']} s, none over eight; the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. Accompaniment above a sung note {R['band_checks']['sung notes with accompaniment above them, share']}: the guitar now plays in its own register (892), and the 2-in-100 rule was measured on piano (749.79).",
       f"- Two channels and chromatic harmony: chords from outside the key, share {R['chord_pick']['readings']['share from outside the key']} (the outro's B♭ and the last chorus's A); the bass's chromatic notes are passing notes.",
       "", "## Readings the paper does not give", "",
       "- 887: rests between lines of a section, median 24 twelfths, 11 of 50 exactly a quarter (749.58 closed in 4/4). But stressed line-final notes an eighth or less 0.44 (kept 0.22), a half or more 0.11 (kept 0.31); weak line-final syllables an eighth or less 0.85 (kept 0.40) (749.76).",
       "- 890: no line-final word holds its weak syllable longer (0 of 14; “completely” mended).",
       "- 891: stressed syllables a sixteenth long in lines sung again 6 of 72, against 9 of 111 in the other lines.",
       f"- 892: the guitar sounds under {R['band_checks'].get('sung notes with the chordal part sounding under them, share (892)')} of the sung notes; none a second away.",
       f"- 893: the harmony voice {min(e['p'][0] for e in R['parts']['harmony'])} to {max(e['p'][0] for e in R['parts']['harmony'])} (E2 is 40).",
       "- Breaths: 7.6 real breaths a minute by onsets (human median 7); by durations 13.0 silences of a beat or more per 100 beats (CoCoPops quartiles 7.0, 9.1, 11.1), median silence 2 beats (CoCoPops 2.0) (749.80).",
       f"- Length: {R['checks']['length in seconds (kept quartiles 165, 206, 243)']} s, the flag and the check agreeing (894); 2 bars in, 4 out, no turn (888).",
       "- The pick's fit by length -0.035 (kept median 0.132) (749.81).", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else ('not met' if c['check'].startswith('READING') else 'FAIL')}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
md += ["", "## Findings", "",
       "Numbered from 749.76; each has Problem, Evidence, Fix and Check in the fix list for v25 (`songs/p68/fixlist_v25.md` and its Doc).", "",
       "- 749.76 887 gives the rest its kept length by cutting the line's last note below the kept lengths.",
       "- 749.77 891 is not enough in song 54: stressed syllables a sixteenth long in lines sung again 14 of 131, against 5 of 82 in its other lines.",
       "- 749.78 871 is a weight, not a rule: song 55's “summers” holds its weak syllable twice as long as the stressed one.",
       "- 749.79 892 leaves a third of song 54's sung notes with no guitar; the old above-the-tune check still prints against guitars.",
       "- 749.80 The voice now breathes after nearly every line: silences of a beat or more above the kept 75th in all three 4/4 songs.",
       "- 749.81 Song 58's pick: fit by length -0.035; song 55's flags print one line twice.",
       "- 749.75 answered with kept evidence (last choruses are longer, a little louder, sometimes higher; rarely denser or in a new key); song 58 meets 9.12 under v24.",
       "- Carried open: 749.61 (6/8)."]
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report58.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report58.md"), "-o", os.path.join(OUT, REC["file_title"] + " - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
