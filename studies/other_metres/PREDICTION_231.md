# 749.231, a syllable's place by its weight in 3/4: the rule file, before any code or run

27 November 2026, 15:45 ET. Form and marks accepted by the songwriting session (15:45 ET), with its two additions. The metres work is open by the writer's word (15:38 ET): a miss leads to the next form.

## The form (`LUTHIER_STRESS_3_4=1`, unset by default)
Fix 879's rule in 3/4, read from the lead sheets. Outside 4/4 the draw scores a stressed syllable +1.5 on any beat and −0.6 off it. With the switch, each syllable's place is scored by the natural log of the share of syllables of its weight sung there over the share of any syllable sung there, from `trial_tables/3-4_leadsheet_sung.stress.json` (538 lead sheets, 25,249 stressed and 26,576 unstressed syllables; made before the run):

| | the bar's first beat | another beat | off the beat |
|---|---|---|---|
| Stressed syllables, share | 0.652 | 0.277 | 0.072 |
| Unstressed, share | 0.136 | 0.587 | 0.277 |
| Any syllable, share | 0.387 | 0.436 | 0.177 |
| Score, stressed | +0.52 | −0.45 | −0.90 |
| Score, unstressed | −1.05 | +0.30 | +0.45 |

*Settled:* the scores are weighted as 4/4's are, by 879's own weight of 0.75 (`word_weight.place`), inside the draw's existing multipliers (1.4 a line, 2.8 a title line). The weak-ending term (871) stays. Two terms of the old score go with it, as they do in 4/4 under 879: the flat +1.5 and −0.6, and the −1.0 for a last stressed syllable off the beat. Stress has two weights here (stressed, unstressed), as the table has; function words are unstressed in it. Nothing else changes: 840 and 731 read "on a beat" as before.

## The trial
Song 53's words, the lead-sheet table, padded, seed 1, 1,000 builds: `LUTHIER_PLAN_3_4=1 LUTHIER_RANGE_3_4=centres LUTHIER_TITLE_ROOM=1 LUTHIER_COPY_JOIN=1` as the second reading stood, and `LUTHIER_STRESS_3_4=1`.

## Marks
R1 to R8 of `PREDICTION_package_3_4.md` against the same 52 like-length waltzes, **every moved figure on the living builds' median (600 builds from the chosen record's fitted spec) and on the chosen tune.** And:
- **R3's first-beat stress:** the living builds' median at or over 0.583, and the chosen tune's.
- **R3b (the songwriting session's):** the living builds' median for stressed syllables off the beat at or under the lead sheets' by-song 75th, **0.078** (504 songs: 10th 0, 25th 0, median 0.026, 75th 0.078, 90th 0.159).
- **Reported:** the share of living builds meeting R3, R4 and R5 together (6.5 in 100 at the second reading); the same rule's table for 6/8, made now for the form to come (`trial_tables/6-8_leadsheet_sung.stress.json`, 99 lead sheets: stressed 0.471 first beat, 0.273 second beat, 0.255 off; unstressed 0.086, 0.110, 0.804).
- **Byte for byte**, every switch unset: 54, 55, 52, both 3/4 trial records.

## What I expect
The first-beat stress rises: a stressed syllable now gains about a point over another beat where it gained nothing. Whether the median clears 0.583 from 0.54 I put at three chances in five. R3b likely met (off the beat is scored worst). The risks: the stress pull competes with the kept windows' own counts, and a draw that keeps the commonest waltz windows may not move much; and a stronger pull to beat one may lengthen runs of the same rhythm (R6's rhythm ceiling is 0.951, now 0.906). The whole at two chances in five.
