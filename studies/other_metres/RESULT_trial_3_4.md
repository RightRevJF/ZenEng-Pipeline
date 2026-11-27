# The 3/4 draw on the lead-sheet tables, song 53's words: result (27 Nov 2026). Missed. Not built. The cause is in the plan, not the table.

Marks: `PREDICTION_trial_3_4.md` (commit 9deaabc, before the run). Figures: `trial_3_4.json` (`python3 studies/other_metres/trial_3_4_read.py ESSEN WIKI`; the written records are outside the repository). 1,000 builds an arm, seed 1.

| | Essen arm (the engine as it is) | Wikifonia arm (the switch) | the mark |
|---|---|---|---|
| Living builds | 566 | 610 | 30 or more |
| Pool (past the joint gate) | 15 | 128 | 10 or more |
| Notes a bar, chosen tune | 3.50 | **3.29** | 2.06 to 2.70 |
| Onsets on a beat | 0.576 | **0.571** | 0.731 to 0.939 |
| Stressed syllables on the first beat | 0.306 | **0.306** | 0.583 or more |
| Words' fit | not read | not read | (the fit is read in 4/4 only) |
| Commonest pitch, verses; refrains | 0.287; 0.280 | **0.438**; 0.314 | no higher than Essen's by more than 0.02 |
| Range (semitones) | 9 | 7 | |
| A leap past an octave in a line | none | none | |
| Distance from Essen's kept tunes (gate 3.53) | 3.33 | 4.25 | reported |
| Distance from Wikifonia's kept tunes (gate 3.69) | 2.78 | 3.63 | reported |
| Deaths: 838 the refrain's lift; 840 the title's stresses; 731 | 372; 61; 1 | 331; 57; 2 | reported |

## By the marks
- **T1 met.** 610 living, pool 128. 3/4 does not die as 6/8 does.
- **T2, T3, T4 missed.** The chosen tune is as busy under the lead-sheet table as under Essen's (3.3 notes a bar against a waltz's 2.1 to 2.7), half its notes off the beat, and three stressed syllables in ten on the first beat against the lead sheets' six or seven.
- **T5 cannot be read:** the words' fit has no table outside 4/4, and the record carries none.
- **T6 missed on the commonest pitch:** the verses put 0.438 of their notes on one pitch against the Essen arm's 0.287. The range also narrowed, 9 to 7 semitones.
- **Byte for byte met:** switch unset, songs 54, 55 and 52 are v53's records.

## Why, as far as this run shows
The table changed and the density did not, because **the plan gives every line two bars whatever the table says** (`spec.slots`: every line of song 53 is `2`). An eight-syllable line in two bars of 3/4 is four notes a bar, mostly eighths, before any table is read; the draw can only choose among two-bar windows of eight notes. The popular waltz spends about four bars on such a line (2.3 notes a bar). The same rule fixes where stresses can fall: with eighths filling the bar, most stressed syllables cannot be on the first beat.

The one odd thing: the Essen arm's tune is nearer the lead sheets (2.78) than the lead-sheet arm's own (3.63), though the lead-sheet arm's pool is far larger. With few eight-note windows in the lead-sheet table, the draw repeats the same bar rhythm (bars on a rhythm already sung 0.90; distinct rhythms 0.10), and the tune comes out narrow and stuck.

## What I expected
T2 and T3 met, T1 in doubt. Wrong both ways: the builds live, and the density marks miss.

## Not built
The switch stays in, unset. The tables stand as steady tables; the fault is that the plan does not ask them how many bars a line wants.

## A form this points to (nothing built; marks first if tried)
In 3/4, the plan takes a line's bars from the kept table's notes a bar: bars = the line's syllables over the table's median notes a bar, rounded to the nearest of 2 or 4 (an eight-syllable line gets four bars under the lead-sheet table, two under Essen's). Then the draw reads four-bar spans as two windows. It is a change to the plan in 3/4 only and would be tried on song 53's words again, the same marks.
