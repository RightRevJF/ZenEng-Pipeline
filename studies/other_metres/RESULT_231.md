# 749.231, a syllable's place by its weight in 3/4: result (27 Nov 2026). The living builds' first-beat stress clears the mark; the pick's does not; the commonest pitch misses on both. Not built.

Rule: `PREDICTION_231.md` (commit 5be2e5f, before any code or run). Figures: `package_231.json` (the chosen tune), `living_231.json` (318 living builds of 600 from the chosen record's fitted spec, beside form B's 322). Song 53's words, the lead-sheet table, padded, seed 1, 1,000 builds, the plan form, form B, the title's room, the copy's join, and `LUTHIER_STRESS_3_4=1`.

| | form B: pick; living median | with 749.231: pick; living median | the mark | |
|---|---|---|---|---|
| Living builds; pool | 530; 139 | 521; 165 | 30; 10 | **R1 met** |
| Notes a bar | 2.09; 2.09 | 2.09; 2.09 | 1.76 to 2.51 | **R2 met** |
| Onsets on a beat | 0.851; 0.817 | 0.772; 0.772 | 0.717 or more | **R3 met** |
| Stressed syllables on the first beat | 0.469; 0.541 | **0.561**; 0.607 | 0.583 or more, both | **R3 missed on the pick; met on the median** |
| Stressed syllables off the beat | 0; 0 | ; 0.071 | median 0.078 or under | **R3b met**, narrowly |
| Range | 17; 14 | 17; 14 | 13.75 or more | **R4 met** |
| Distinct pitches | 11; 9 | 11; 9 | 9 or more | **R4 met** |
| Commonest pitch | 0.269; **0.299** | **0.302; 0.302** | 0.275 or under, both | **R5 missed on both** |
| Bars on a figure already sung | 0.789; 0.817 | 0.793; 0.808 | 0.874 or under | **R6 met** |
| Bars on a rhythm already sung | 0.906; 0.892 | 0.879; 0.887 | 0.813 to 0.951 | **R6 met** |
| In the voice (59 to 76); a leap | yes; none | yes; none | | **R7 met** |
| Deaths on 780; 840 | 0; 0 | 0; 3 | under one in ten | **R8 met** |

Byte for byte, every switch unset: 54, 55, 52, both 3/4 trial records.

## What the form did
- **It moves what it was for.** The living builds' median first-beat stress goes from 0.541 to 0.607, over the lead sheets' 25th of 0.583; the builds at or over the mark go from 35 in 100 to 53. Their quartiles: 0.53, 0.61, 0.65 (form B: 0.46, 0.54, 0.62).
- **It costs a little on the beat:** onsets on a beat 0.817 to 0.772, and stressed syllables off the beat from none to 0.071 at the median (the lead sheets' 75th is 0.078). The table rewards an unstressed syllable off the beat, and stresses follow some of them there. R3b holds by 0.007.
- **The pick did not follow.** The chosen tune is at 0.561, between the 25th and the median of its own builds. The pick takes the first pool build at or over the range floor, and reads nothing of stress.

## R5, and a second pass that was the pick's luck
The commonest pitch misses on the median as well as the pick (0.302, 0.302), and **the living median was already 0.299 under form B**, whose pick happened to stand at 0.269. So the second reading's "R5 met" was the pick's again, not form B's. The centres moving into the room widened the range and raised the pitch count (medians 14 and 9, both at the marks); they did not bring the commonest pitch down. A build in three meets R5 (32 in 100; form B 37).

## Reported
- Living builds meeting R3's stress, R4 and R5 together: **10.1 in 100** (6.5 under form B). R4 and R5 together 20.4.
- The 6/8 table by the same rule is made (`trial_tables/6-8_leadsheet_sung.stress.json`, 99 lead sheets): stressed syllables 0.471 on the first beat, 0.273 on the second, 0.255 off; unstressed 0.086, 0.110, 0.804. Scores: stressed +0.57, +0.38, −0.76; unstressed −1.13, −0.53, +0.39.

## What I expected
The median over 0.583 at three chances in five: it is. R3b met: yes, barely. The whole at two in five: missed, on the pick and on R5, and I had not checked R5's median before.

## Not built. What the next form has to answer
1. **The pick.** With the median build now meeting R3's stress and R4, a pick that reads the like-length figures (first-beat stress, range, pitches, the commonest pitch) no longer hunts one build in fifteen; it chooses among one in ten that meet all, and one in two that meet stress. That is the songwriting session's candidate A, and after 749.231 it finishes a draw that is mostly right instead of standing in for one that is wrong.
2. **The commonest pitch is a fault of the draw**, untouched so far: a median of 0.30 against the like-length 75th of 0.275 and median of 0.24. One pitch carries three notes in ten. The 4/4 engine holds this with 956's ceiling, which my first reading found borrowable outside 4/4 and the stricter marks did not.
