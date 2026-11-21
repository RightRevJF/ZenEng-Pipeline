# Luthier list for v43 (since v42)

21 November 2026. Luthier v42 (950 to 953) is reviewed (`lib/luthier/REVIEW_stage27.md`) and merged into main at 6df7ef6. Every kept table, all the music in the records, song 60's v42 record, `soundness.json`, `neighbour_v42.json` and the room files reproduce byte for byte. Four records name a table hash from before 952. Song 58's seventeenth edition is built from the v42 record. Next finding 749.139; next fix 954.

## In short

950, 952 and 953 hold. 951 is a fair use of the asking in kind, but in degree it is a judge. It holds every chosen tune within 2 semitones of a prediction whose own error is about 5. Kept songs land that near their asking only 35 times in 100. A floor does the work 951 was meant to do, at less cost: in a trial it keeps song 54's words' fit at 0.275 where 951 gives 0.163. Rhythm scaling is now the largest gap.

## Items

### 749.135 Make the range a floor, not a band
**Problem.** 951 picks the first build within 2 semitones of the range the words ask. The words predict range loosely, so this treats a loose prediction as exact. It also trades another reading away: song 54's words' fit falls from 0.282 to 0.163.
**Evidence.** `studies/review27_range_spread`. Held out by artist, the words-to-shape prediction misses kept songs' ranges by sd 4.99 semitones. 35 kept songs in 100 fall within 2 of their own asking; all five of Luthier's chosen tunes now do (spread sd 0.73 against kept songs' 5). Range less the asking in kept songs: 10th -6.5, 25th -3.36, middle -0.3, 75th +3.58, 90th +7.0. Under 872 alone the chosen tunes ran short (mean -2.9; song 58 at -8.9). That bias is the real fault.
A floor trial (one line changed, not committed) took the first build with range at least the asking less 3.36:
- song 54: 16 semitones, words' fit 0.275;
- songs 58 and 55: the same picks as 951;
- songs 60 and 59: unchanged by either rule;
- sound, with 11 checks outside the middle half against 951's 15.

**Fix.** Replace the band with a floor at the asking less the kept 25th of range less the asking (from the held-out residuals, written by the words-to-shape maker, not typed in). Above the floor, 872 decides.
**Check.**
- Each of songs 55, 54, 58 and 60: no chosen tune under the floor, and the pick is 872's whenever 872's first build clears it.
- No pick's words' fit is more than 0.02 under 872's pick unless 872's pick is under the floor.
- The soundness rule and the pool standard hold.
- Song 59 is read, not fitted to.

### 749.136 Stamp-check the song records, as 953 does the room files
**Problem.** Records 54, 55, 58 and 59 name `kept_words_to_shape.json` as `b243b89e5d`, the table before 952. The table now hashes `53edc7875f`. The notes are right, because only song 60's asking moved, but the record says it read a table it did not.
**Evidence.** Rerunning the four songs on v42 gives the same files except that one line. The records were written at d9b7493, and 39e385e changed the table after.
**Fix.** Rerun the four records so their stamps are current. Give `song_from_lyric.py` (or a small checker) a `--check` that compares each record's table hashes with the tables at hand, and run it in every window, as `lyric_room.py --check` is.
**Check.** The check passes on every record, and changing any kept table makes it fail.

### 749.137 Trace why the pools grew sounder
**Problem.** The neighbour choice fails the rule 1.5 times in 100 (Window 198: 3.0), and a random pool pick 2.7 (8.2). The paper says this is untraced.
**Evidence.** Under v41 the builds spanned 14 or 15, under the kept middle of 17, so range leaned low across the pools. 950 moves them to 17. That alone may explain most of the change.
**Fix.** Reread the pool figures with range left out of the soundness rule, and with the top-note share left out.
**Check.** If the figures return near Window 198's, the planted peak explains them; say so in the paper. If not, trace further before building more on the pools.

### 749.138 Rhythm scaling: act on the lyric's room in the engine
**Problem.** Rhythm scaling is the one check leaning past the quartiles, low in all three songs. Song 58 reads 0.557 against a kept 10th of 0.574. The rhythm-memory study found the cause: slow change in how busy the singing is (+0.68) and bars with nothing sung (+0.58). The lyric's room check measures both, and the engine does nothing with them.
**Evidence.** soundness.py on v42: `lean_beyond_25th_75th: rhythm scaling, low`. The builds' middle: 0.592, 0.576, 0.555, 0.682.
**Fix.** Rule first: give each section a busyness aim, from `tables/kept_rhythm_room.json`, so that sections differ as kept songs' do. Plan bars of rest where the lyric leaves room. Try it against the pool standard before building.
**Check.** Rhythm scaling within the kept quartiles in two of songs 55, 54 and 58. The soundness rule and the pool standard hold; no more than 7 in 10 as many builds lost.

## Notes on v42's other items

- **749.134 (the commonest pitch):** the study confirms the fault. Try the ceiling against the pool standard before building it, as proposed. A wider range did not spread song 58's verse (0.497 at 19 semitones), so range alone will not fix it.
- **Song 54 no wider in the middle:** the floor in 749.135 asks less of song 54 than 951 does, and keeps its words.

## Closed

749.111 (the peak: 950), 749.131 (952), 749.132 (953), 749.133 (952). 749.134 measured; the ceiling is to be tried.

## Carried

749.134 (the ceiling, to try), 749.125 (song 60 as a practice song), 749.127 (a "seen before writing" line: Window 199 kept it), 749.109, 749.116, 749.103, 749.101, 749.61.
