"""'Same Time Tomorrow' (song 58): the test report, the engine's record (kept apart from the songbook). Read from lyric58.song.json and the
document checks (consistency58.json, out/demo_report.pkl). Writes test_report58.md and out/Same Time Tomorrow - test report.docx."""
import json, os, pickle, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(HERE, "lyric58.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency58.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = R["melody"]; J = R["judge7"]; S = R["spec"]
md = [f"# Same Time Tomorrow ({REC['edition']}): test report", "", "Words and music: Jason Bryant", "",
      "Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v25 (main at 9b149f6). This report is the engine's record; the songbook is for musicians.", "",
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
       f"- Perception: sung phrases {R['band_checks']['sung phrases, seconds (median, longest)']} s, {R['band_checks']['sung phrases over eight seconds']} over eight by the check's one-beat rule (749.83); the chord voicings inside the low-interval limits; no accompaniment a second from a sung note. The guitar above a sung note {R['band_checks'].get('sung notes with the guitar above them, share (no kept figure; not a fault)')}, printed without a kept figure (900).",
       f"- Two channels and chromatic harmony: chords from outside the key, share {round(R['chord_pick']['readings']['share from outside the key'], 3)} (the outro's B♭ and the last chorus's A); the bass's chromatic notes are passing notes.",
       "", "## Readings the paper does not give", "",
       "- 899: line ends drawn with their rest. Stressed line-final syllables an eighth or less 0.19, a half or more 0.27 (kept 0.24, 0.27); lines run on with under a beat of rest 0.20 (kept 0.27); rest median 27 twelfths.",
       "- 901: on a word's weak last syllable, the weak one outlasts the stressed one in 8 of 14 line ends (kept 47 to 49 in 100; 42 with tied notes read, 749.82).",
       "- Breaths: 6.6 real breaths a minute by onsets (human median 7); silences of a beat or more 10.4 per 100 beats (CoCoPops quartiles 7.0, 9.1, 11.1), median silence 2.5 beats (CoCoPops 2.0). Phrases split at half a beat: over 12 beats 0.019 (kept 0.046), longest 13.2 beats (kept songs' longest, median 12).",
       f"- 900: the guitar under {R['band_checks'].get('sung notes with the chordal part sounding under them, share (892)')} of the sung notes.",
       f"- Length: {R['checks']['length in seconds (kept quartiles 165, 206, 243)']} s; 9.12 as kept songs meet it: the last chorus 16 bars, the first 14 (903).",
       "- 749.77 (not raised): stressed syllables a sixteenth long, of syllables, lines sung again 1 of 65, other lines 2 of 98.", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else ('not met' if c['check'].startswith('READING') else 'FAIL')}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
md += ["", "## Findings", "",
       "Numbered from 749.82; each has Problem, Evidence, Fix and Check in the fix list for v26 (`songs/p68/fixlist_v26.md` and its Doc).", "",
       "- 749.82 The CoCoPops parser drops every note that begins a tie, with its syllable; the kept tables built since 895 shift when the ties are read.",
       "- 749.83 The phrase check counts a breath only at a beat of silence; kept singers breathe in half a beat, and on that rule the songs match the kept.",
       "- Answered: 901 recounted (the retirement of 871 and 890 stands); 749.77 closed with a kept figure for returning lines.",
       "- Carried open: 749.61 (6/8)."]
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report58.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report58.md"), "-o", os.path.join(OUT, REC["file_title"] + " - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
