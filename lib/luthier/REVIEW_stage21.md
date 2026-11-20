# Review 21: Luthier v35 (fixes 934–936)

Branch `luthier-v8-stage1` at 2508db0, merged into main at 78f8ee4. Answers the list for v35 (749.113 to 749.116); 749.116 was not reached.

## Byte for byte

- The six makers write every kept table byte for byte.
- All five song records (52, 54, 55, 58 and the hold-out 59), song 52's and song 53's run files, and `stage4_results.json` reproduce.
- `soundness.py` reproduces `soundness.json`: sound; 6, 7, 5 checks outside the middle half; one lean past the quartiles (rhythm scaling, low).
- `neighbour.py` reproduces every field of `neighbour_v35.json`.

## The fixes

- **934** holds. Every round reads 40 builds; song 59's fit under a second seed lands at 0.72, 0.349, 0.261 against 0.78, 0.37, 0.231.
- **935** holds for song 59: rhythm deaths fall from 500 to 52 in 1,000, and survivors rise from 138 to 325. My list blamed the long verse lines; the trace showed the one short bridge line at fault. The trace was the right call. But the rule acts in every build of songs 55 and 54 too (the stat counts 1,000 of 1,000), and it is gated on the song having an aim, which a rhythm rule should not depend on (749.119).
- **936** meets its check in two songs of four. The builds' repeated notes are 0.382 against 0.373 (58) and 0.225 against 0.210 (59), but 0.222 against 0.158 (55) and 0.215 against 0.110 (54). A quarter of the kept width is 0.045 (749.118).

## Question 1: pools fail the rule 2.5 in 100 (0.5 in v34). Is 936 the cause?

No. First, the figure: 2.5 in 100 is the **neighbour choice** (the pool build nearest a randomly drawn kept song). **A random pick from the engine's pool** fails 2.6 in 100, against 2.5 in v34. The papers have quoted the neighbour figure under the random-pick label since v32 (749.117).

Second, the test. v35 was run with 936's repeat weight taken out and everything else kept (`studies/review21/`):

| | v34 | v35 | v35 without 936 |
|---|---|---|---|
| Neighbour choice fails, in 100 | 0.5 | 2.5 | 4.8 |
| Random pool pick fails, in 100 | 2.5 | 2.6 | 5.4 |
| Pool builds' repeated notes under the 25th / over the 75th | 0.16 / 0.32 | 0.21 / 0.20 | 0.16 / 0.34 |

936 lowers both rates and evens out the repeated-note lean. The rise came with 934 and 935, which change songs 55 and 54 in every build. Which of the two did it is not yet measured (749.119). At 400 draws, 0.5 against 2.5 is 2 against 10 failures. That is likely more than chance, but not by much.

## Question 2: song 59 is outside the kept middle half on 2 of 21 checks (3 before)

That is a step the wrong way. Song 59 is now more central than every one of the 147 kept songs; a kept song stands outside on a median of 10. Its two (steps, pitch scaling) are only small leans.

The reason is not a fault in 936. Two Hearts sits near the kept middle, so closing on the aim moves the song inward. And the checks the aim does not set (rhythm scaling, the words' fit, onsets) stay in the middle anyway. 749.103 holds on the hold-out, more strongly than before.

## What else the review found

- **Why 936 falls short in songs 55 and 54 (749.118).** Two causes:
  - **The refit's fixed shares.** The trace after the fix shows repeats in fresh lines of 0.17 and 0.179, but in returning lines 0.289 and 0.247 (55, 54). A refitted line (`again`, 882) gives a split note the pitch before it 4 times in 10, and leads into a note on the same pitch 32 times in 100. Both are fixed shares that the repeat weight never reaches.
  - **The fit walks back to its start.** In song 54, round 2 met the aim on repeats (0.152) and steps (0.592), but its fresh lines left the kept band. Each later round went halfway back toward round 1, the last round inside the band, and the kept round (6: repeat 0.92, step 1.268) is nearly where the fit began.
- **749.111, the second trial.** The pattern is clear: plant only where the aim is wider than the kept middle. In song 59 the planted peak sat near the top of the voice and only 11 builds in 100 survived. The peak should sit a step under the voice's top.
- **Song 58, twelfth edition.** A major, G♯2 to F♯3, 337 seconds, built from the v35 record. It goes up from the eleventh (v33): there was no edition from v34, the hold-out cycle. Bars on a figure already sung rose to 0.505 (0.253 at v33). Rhythm scaling is 0.507, under the kept 10th. The chorus sits where the verse does (lift 0, as Bird Dog's), so the songbook's voice note now says so rather than "about 0 semitones higher". 44 of 44 document checks pass.

## Findings

749.117 to 749.119, in `songs/p68/fixlist_v36.md`. Next finding 749.120; next fix 937.
