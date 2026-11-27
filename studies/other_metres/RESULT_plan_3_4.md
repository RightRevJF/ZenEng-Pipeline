# The 3/4 plan form on song 53's words (749.226): result (27 Nov 2026). The density marks are met; P6 is missed. Not built.

Marks: `PREDICTION_plan_3_4.md` (commit 740bb4e, before the run). Figures: `plan_3_4.json` (`trial_3_4_read.py` on the two arms' records, with three counts of notes a bar added; the records are outside the repository). `LUTHIER_PLAN_3_4=1`, 1,000 builds an arm, seed 1.

**P1. The bars, per line, before the draw.** Lead-sheet arm: every line of every section three sung bars in a four-bar phrase (`[3, 3, 3, 3]` eight times; slots all 4). Essen arm: every line two bars, as the rule gives under a median of 3.44, so that arm is v53's Essen arm to the last figure.

| | Essen arm, plan form | Lead-sheet arm, plan form | the mark |
|---|---|---|---|
| Living builds; pool | 566; 15 | **731; 268** | 30; 10 |
| Notes a bar, over the bars of sung phrases (128) | 4.19 (64 bars) | **2.09** | 2.06 to 2.70 |
| the same, as the kept table counts (bars with a note) | 4.19 | 2.23 | |
| the same, the engine's own reading (turns counted) | 3.50 | 2.00 | |
| Onsets on a beat | 0.576 | **0.893** | 0.731 to 0.939 |
| Stressed syllables on the first beat | 0.306 | **0.622** | 0.583 or more |
| Commonest pitch, verses; refrains | 0.287; 0.280 | **0.424; 0.390** | no higher than Essen's by more than 0.02 |
| Range; a leap past an octave | 9; none | 9; none | |
| Bars on a rhythm already sung; distinct rhythms | 0.766; 0.234 | 0.946; 0.054 | reported |
| Distance from the lead sheets' kept tunes (gate 3.69) | 2.78 | 3.40 | reported |
| Deaths | 838: 372; 840: 61; 731: 1 | 838: 269 only | reported |
| Notes held a bar or longer | 0 | 15 | reported |

## By the marks
- **P1 met.**
- **P2 met.** 731 living builds and a pool of 268; no build dies on the title's stresses or the stress floor.
- **P3 met by the count the mark names**, "over every bar sung, padded bars included": 268 notes over 128 bars, 2.09. It is narrow, and I set the other two counts beside it so nothing hides: counted as the kept table counts its own songs it is 2.23 (inside); by the engine's own reading, which also counts the instrumental turns, 2.00 (outside by 0.06). The songwriting session wrote the mark and may say which count it meant.
- **P4 met.** 0.893.
- **P5 met.** 0.622: stressed syllables fall on the first beat about as a lead-sheet waltz has them.
- **P6 missed.** The verses put 0.424 of their notes on one pitch and the refrains 0.390, against the Essen arm's 0.287 and 0.280: over by 0.14 and 0.11, the margin being 0.02. The range is the same and neither has the leap.
- **Byte for byte met:** switch unset, 54, 55 and 52 are v53's records.

So the form does what it was made to do (a waltz's density, beats and stresses) and misses on the one mark that guards the tune.

## What bears on P6, for the songwriting session to weigh (I change no mark)
- 956's own 4/4 lines are 0.44 for verses and 0.479 for choruses; this tune is under both (0.424, 0.390). The mark set was "no worse than the Essen arm", and the Essen arm is a tune of twice the notes a bar.
- The lead sheets themselves: the commonest pitch over a whole 3/4 tune has a median of 0.21 and a 90th of 0.30 (`metre_free_b.json`; whole tune, not by section, so not like for like). By that the tune does sit on one pitch more than a kept waltz.
- P7 shows where it comes from: bars on a rhythm already sung 0.946 and distinct rhythms 0.054. Thirty-two lines of two syllable counts, each drawn as the same window pair, with 818 and the copies on top. The tune is square to a fault, and its range of 9 semitones over 268 notes leaves it few pitches.

## What I expected
P1 to P3 met, P4 likely, P5 and P6 in doubt; one chance in three for the whole. P5 held; P6 missed.

## Not built
The switch stays in, unset. By the stopping rule written before the run this was the one form, and the 3/4 draw closes for the version unless the songwriting session rules otherwise on P6.
