"""'Same Time Tomorrow' (song 58): the test report, the engine's record (kept apart from the songbook). Read from lyric58.song.json and the
document checks (consistency58.json, out/demo_report.pkl). Writes test_report58.md and out/Same Time Tomorrow - test report.docx."""
import json, os, pickle, subprocess, collections
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
R = json.load(open(os.path.join(HERE, "lyric58.song.json"))); REC = pickle.load(open(os.path.join(HERE, "song_record.pkl"), "rb"))
CON = json.load(open(os.path.join(HERE, "consistency58.json"))); DR = pickle.load(open(os.path.join(OUT, "demo_report.pkl"), "rb"))
M = R["melody"]; J = R["judge7"]; S = R["spec"]
md = ["# Same Time Tomorrow: test report", "", "Words and music: Jason Bryant", "",
      "Song 58 (songs/p68), written end to end from its lyric with `lib/luthier/song_from_lyric.py` under Luthier v22 (main at 8dea87c). This report is the engine's record; the songbook is for musicians.", "",
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
       f"- Metre and stress: long notes on stressed syllables {R['checks']['long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65)']} (kept quartiles 0.43, 0.55, 0.65); the title's stressed syllables on a beat 0.75 (kept 0.73).",
       "- One song-wide intensity curve: section levels " + ", ".join(f"{k} {v}" for k, v in R["levels"].items()) + ". Read from the demo (band only): " + ", ".join(f"{r['sec']} {r['energy_read']:.2f}" for r in DR["energy"]) + ". Each chorus is above its verse; the last chorus is not above the first, and the turn reads highest (749.75).",
       "- A breath, then a fresh re-entry: real breaths (an onset gap of three beats or more) 6.1 a minute, inside the human range (median 7). The 0.55 to 0.65 return is not supported by the notes in 622 songs and is not checked here (749.65).",
       f"- Perception: accompaniment above a sung note {R['band_checks']['sung notes with accompaniment above them, share']}; sung phrases {R['band_checks']['sung phrases, seconds (median, longest)']} s, none over eight; the chord voicings inside the low-interval limits. But the guitar sounds under only 6 of 469 sung notes (749.73).",
       f"- Two channels and chromatic harmony: no chord from outside the key (share {R['chord_pick']['readings']['share from outside the key']}); the bass's chromatic notes are passing notes.",
       "", "## Readings the paper does not give", "",
       "- 869: sixteenths 5.3 in 100 of the sung notes (kept 15); no build died for want of a fit.",
       "- 870: the median rest between lines of a section 15 twelfths; 24 of 50 exactly a quarter (749.58 stays open).",
       "- 871: no two-syllable line-final word holds its weak syllable longer (0 of 13); one three-syllable word does, “completely” (749.71).",
       "- 875: no melisma on a function word (0 of 65).",
       "- 882: of the pick's 34 calls to refit a line, 23 are lines sung again and 11 are fresh lines that borrow an earlier line; 5 lines sung again keep their source note for note. Stressed syllables a sixteenth long in lines sung again: 3 of 75 (song 54: 19 of 134, 749.66).",
       f"- The harmony voice: {len(REC['harm'])} notes, lowest D2; 3 below E2 (749.74).",
       f"- Length: {R['checks']['length in seconds (kept quartiles 165, 206, 243)']} s in the checks, 337 s in the flag (749.69); 229 s under v20.", "",
       "## The documents", "",
       "Lead sheet, full score, parts, number chart, MusicXML (lead sheet and full score), demo (MP3 and General MIDI), songbook (Doc and Word). Each written from the record; the checks:", "",
       "| Check | Result |", "|---|---|"]
for c in CON: md.append(f"| {c['check']} | {'pass' if c['ok'] else ('not met' if c['check'].startswith('READING') else 'FAIL')}{(' (' + c['detail'] + ')') if c['detail'] else ''} |")
md += ["", "## Findings", "",
       "Numbered from 749.66; each has Problem, Evidence, Fix and Check in the fix list for v23 (`songs/p68/fixlist_v23.md` and its Doc).", "",
       "- 749.66 A split in a line sung again (882) halves the note it splits, chosen by place alone: a stressed syllable can be left a sixteenth long.",
       "- 749.67 Lines sung again keep less of their source, and no kept figure says how much they should.",
       "- 749.68 In 4/4 the joint gate and the words' gate pass nearly every build.",
       "- 749.69 One song, two lengths (343 s and 337 s), both past the kept 75th.",
       "- 749.70 The new kept tables and the stage 8 and 9 results have no maker that runs in the repo.",
       "- 749.71 871 reads only words stressed on their first syllable.",
       "- 749.72 Two fits printed for one pick; two sets of kept figures for the fit.",
       "- 749.73 Under a low voice the guitar drops out: 6 of 469 sung notes have it sounding.",
       "- 749.74 The harmony voice has no range of its own (D2).",
       "- 749.75 Every chorus is at level 1.0: the last chorus is not the song's top (9.12).",
       "- Carried open: 749.58 (rests), 749.61 (6/8)."]
text = "\n".join(md) + "\n"; open(os.path.join(HERE, "test_report58.md"), "w").write(text)
if __name__ == "__main__":
    subprocess.run(["pandoc", os.path.join(HERE, "test_report58.md"), "-o", os.path.join(OUT, "Same Time Tomorrow - test report.docx"), "--reference-doc=/home/claude/carol/songbook/ref.docx"], check=True)
    print("test report:", len(text.split()), "words")
