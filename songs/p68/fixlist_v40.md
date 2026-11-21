# Luthier list for v40 (since v39)

20 November 2026. Luthier v39 (944, the shape from the song; no kept song drawn) is reviewed (`lib/luthier/REVIEW_stage25.md`) and merged into main at aaa2470. Every kept table (the new one included), all five song records, song 53's run, song 60's v39 record, `soundness.json` and `neighbour.json` reproduce byte for byte. Song 58's fifteenth edition is built from the v39 record. Next finding 749.128; next fix 945.

## In short

**944 stays.** It is the writer's ruling, its cost is stated, and the pools stay inside the standard's bar. Striking "verses step, choruses leap" on the evidence of the kept songs is the right use of the corpus.

**One measurement needs mending first (749.128).** The words-to-shape table reads kept songs' lines one way and Luthier's another. That inflates the repetition the words ask by 0.06 to 0.10 and understates the range by 1 to 2 semitones. Fix it before anything is aimed at the words' asks.

749.123 to 749.127 are carried. 749.130 adds to 749.123 a contrast that sharpens the next study.

## Items

### 749.128 Measure the words the same way on kept songs and on Luthier's
**Problem.** `make_kept_words_to_shape.py` splits a kept song's words into lines in proportion to each line's notes, since the corpus does not tie words to lines. `words_to_shape.from_sung` reads a Luthier lyric's real lines. "Lines said again word for word" suffers most: the proportional split misses most repeated lines in kept songs, so the table learns from a feature that Luthier's lyrics then show at full strength.
**Evidence.** Kept songs read 0.000, 0.025, 0.182 at the 10th, 50th and 90th percentiles. Songs 55, 54, 58, 59 and 60, from their real lines, read 0.232, 0.138, 0.193, 0.333, 0.275 (the kept 84th to 99th). The same proportional split applied to their lyrics gives 0.018, 0.017, 0.000, 0.190, 0.100. The asks move with it, measured the kept way against what the records hold:
- Bars on a figure already sung: 0.402, 0.399, 0.361, 0.479, 0.454 against 0.509, 0.461, 0.462, 0.551, 0.545.
- Bars on a rhythm already sung: 0.536, 0.550, 0.501, 0.595, 0.576 against 0.629, 0.603, 0.588, 0.658, 0.655.
- Range: 17.5, 18.4, 19.8, 17.2, 17.9 against 15.6, 17.3, 18.0, 15.9, 16.3.

Measured the kept way, the builds already sing bars on a figure at or above what the words ask in three songs of four. The segmentation-free feature agrees: by three-word runs already sung, Luthier's lyrics sit at the kept 10th to 29th percentiles.
**Fix.** Tie each kept song's words to its notes by syllable count (each word takes as many notes as it has syllables, a melisma's extra notes skipped), take each line's words from its notes, and refit the table. Test it again on songs held out by artist, rule first. Until then, read Luthier's lyrics the kept way.
**Check.** "Lines said again" reads alike in kept songs and in Luthier's lyrics measured both ways (within 0.03 for each song). The held-out prediction for range and the two repetition readings stays over the shuffled-chance line. The records' asks are rewritten.

### 749.129 Movement from the song's genre family, not the middle of all songs
**Problem.** With movement at the kept middle for every song, every song moves alike by design, and 749.103 (too like the middle) grows. The writer's override is built but has not been tried on a song.
**Evidence.** Table HF: the builds' steps 0.404 to 0.429 and leaps 0.097 to 0.119, all four songs within a quarter width of one point. The paper's own note: the songs are more alike than under the draw.
**Fix.** The ruling allows a style guide. Take the default movement from the kept songs of the song's own genre family (the genre tables in studies/genre), its middle and not one song's, with the writer's smooth, leaping and chant still overriding. Write the rule first: do kept songs' movement differ by genre family more than chance?
**Check.** If the genre families differ (the rule's test), each song's builds move to its family's middle within a quarter width, and the pools hold the standard with ranges. If they do not differ, the middle stays and the paper says so.

### 749.130 Rhythm scaling: use songs 59 and 60 as the contrast
**Problem.** Rhythm scaling is the one check the songs fail together. Two of Luthier's own songs do not fail it.
**Evidence.** v39's records: songs 59 and 60 at 0.668 and 0.717 (kept middle 0.656); songs 55, 54 and 58 at 0.578, 0.587 and 0.540. Song 60's share of repeats from far back (0.688) is at the kept 96th percentile, as song 54's is (0.742). So the far-back share alone (749.123) does not explain low rhythm scaling.
**Fix.** In the rhythm-scaling study, rule first, set songs 59 and 60 against 55, 54 and 58 on the rhythm's own readings: notes a bar, gaps, onsets on the beat, distance profile, line lengths and tempo. Then test what differs on the kept songs that repeat much.
**Check.** The study names a reading that separates 59 and 60 from 55, 54 and 58, and the same reading separates high from low rhythm scaling in kept songs, on songs held out.

## Carried from the list for v39

- 749.123 Where the repeats come from (now read with 749.130).
- 749.124 More inner draws for the neighbour range (v39's 0.5 to 5.5 at 1.5 in 100 is again mostly the inner draws).
- 749.125 Song 60 as a practice song (749.111's third trial no longer applies as written, now that no song is drawn; song 60 is still a sixth lyric to fit and read).
- 749.126 The join before a copy kills 805 of song 60's 1,000 builds under v39.
- 749.127 A "seen before writing" line in each PREDICTION file.

## Small things

- Song 58's fifteenth edition sings its top note, D4, 10 times, all in the bridge.
- The studies scripts that read a drawn song (studies/review19/aimpool.py, studies/holdout59) are retired.

## Carried

749.109, 749.111, 749.116, 749.103 (read as the outcome), 749.101, 749.61.
