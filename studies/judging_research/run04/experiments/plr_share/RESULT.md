# Share of P/L/R moves on the torus of phases: result

Run 04, 24 November 2026. The rule was frozen before any outcome was opened (`PREDICTION.md`, commit 00ab557). `test.py` follows it in order: first the measure on the notes, then the gate, then the overlap check, and only then the covers. It ran as written, and the numbers are in `result.json`. The script reads the data straight from `origin/main:studies/judging_data/`. The whole run takes about 6 seconds.

## What was predicted
Every major or minor chord has three "closest cousins": the chords you reach by keeping two of its three notes and moving the third by a semitone or a whole tone. Music theorists call these the **P**, **L** and **R** moves. On Amiot's map of chords (a flat torus with two angles per chord, φ₃ and φ₅), these three cousins are exactly the three nearest chords. **PLR** is the share of a song's chord changes that are such moves.

**The guess:** within one artist's own songs, a song with **more P/L/R moves gets more covers**, at **+0.02 SD** of log(1 + covers) per SD of PLR. The model holds chord repetition (`ch_rep`), chord surprise (`ch_ic_mean`), first year, clips, links and chord count fixed. Five hypotheses were tested tonight, so a pass needed **p < .01**, two-sided, and a positive estimate in both artist halves. The authors themselves called the case for it weak before any data were seen: the plainest progression, I–IV–V–I, has no P/L/R move at all.

## Worked example: the four-chord loop
Take the "four chords of pop", I–V–vi–IV, in C: **C → G → Am → F**, then back to C.
- **C → G:** C (C-E-G) and G (G-B-D) share only one note, G. Not a P/L/R move (distance 1.656).
- **G → Am:** G (G-B-D) and Am (A-C-E) share no notes. Not a P/L/R move (2.498).
- **Am → F:** Am (A-C-E) and F (F-A-C) share two notes, A and C. Only E moves, down to F. **This is a P/L/R move** (an "L" move; distance 1.229, under the 1.25 cut).
- **F → C:** F and C share only C. Not a P/L/R move (1.656).

So one of the four changes is a P/L/R move, and the loop's **PLR is 0.25**. Its average step on the map (TS) is 1.760. For comparison:
- C → Am → C (I–vi) is all P/L/R moves: PLR 1.
- I–IV–V has none: PLR 0.

## Checks and gate (before any outcome was read): **passed**
**Unit values.** All reproduced:
- d(C,Am) 1.065;
- d(C,Cm) = d(C,Em) 1.229;
- d(C,F) = d(C,G) 1.656;
- d(C,Fm) 1.824;
- d(Cm,D) 3.26.

Exactly 36 of the 276 pairs of triads fall under 1.25. They are exactly the P/L/R pairs, and they are the same 36 when φ₅ is stretched by 0.7365. All five loops on the card matched.

**Shape.** Matched the chair to the digit:
- 2,672 songs;
- 1,801 of 60,579 moves skipped because a phase is undefined, and 37 skipped as zero steps;
- PLR at the 10th / 50th / 90th percentile: 0.00 / 0.22 / 0.50.

**Gate 1, two clips of a song agree:** Spearman **0.349**, 1,279 songs (needs ≥ 0.20; chair 0.349).

**Gate 2, not an existing measure renamed:** the largest |ρ| with the 17 data-pack measures, distinct chords, links and clips is **+0.14**, with links (needs ≤ 0.7). With `ch_rep` it is +0.01, and with chord surprise +0.12.
- *Printed, deciding nothing:* TS −0.70, FP −0.19, D3 +0.26 (all as the chair found).

## What came out
All 2,672 songs had a first year. After keeping only artists with two or more songs, the model ran on 1,924 songs by 420 artists, the same as run 03.

Printed **before** the estimate: **SE 0.018** (chair ~0.0176) and **power 0.07** (chair 0.075) to see +0.02 at p < .01.

| | Songs | Artists | β | SE | p |
|---|---|---|---|---|---|
| **All (decides)** | 1,924 | 420 | **+0.0065** | 0.018 | 0.72 |
| Half 0 | 932 | 205 | +0.015 | 0.024 | 0.55 |
| Half 1 | 992 | 215 | −0.004 | 0.024 | 0.86 |

**95% range:** −0.029 to +0.042.

The CR1 clustered SE was computed by hand, as the rule requires. statsmodels' clustered SE agrees with it to within 1e-14.

## Verdict, by the rule written first: **kill**
The estimate is positive but small: +0.0065, below the kill line of +0.01. The halves also split. The prediction is killed.

**How firm:** weak. This is a kill by the rule, not proof that the effect is zero. The power was 0.07, and the 95% range (−0.029 to +0.042) still holds the predicted +0.02. What the data can say is that a share of P/L/R moves worth more than about +0.04 SD of covers, within artist, is unlikely. The prediction's authors expected a kill to be the likeliest informative result, and it is.

## Reported, deciding nothing

| Reading | β | SE | p |
|---|---|---|---|
| TS (mean torus step) in place of PLR | −0.002 | 0.018 | 0.92 |
| Covers within 5 years of first year | +0.005 | 0.026 | 0.84 |
| Covers more than 10 years after | +0.008 | 0.016 | 0.61 |
| PLR without chord surprise (`ch_ic_mean`) | +0.001 | 0.019 | 0.96 |

- **Skipped moves:** 1,801 of 60,579 had an undefined phase (augmented triads, diminished sevenths and bare tritones have no angle on one of the two circles). 37 were zero steps.
- **Songs with PLR = 0:** 18.2% of all 2,672 songs, and 17.4% of the 1,924 in the model.
- **TS:** its Spearman correlation with PLR is −0.69 on the model songs. TS is flat as well.
- In the same model, chord repetition (−0.062, p .0002) and chord surprise (−0.090, p < .0001) behave as in earlier runs.

## What it cannot say
- **Not fresh:** these are run 03's songs, and their covers have been looked at many times. Only the measure was new.
- **Triad-based cut:** the 1.25 cut is exact for major and minor triads only. For seventh chords and other sets it is a convention.
- **Low power:** a null clears nothing for small effects.
- **No cause:** even a pass would not show that P/L/R moves cause covers.
- **Hits only:** these are all songs popular enough to be transcribed on Hooktheory.
- **McGill:** the hold-out was not touched.

## Data credit
- **Notes and chords:** Hooktheory, via Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022). CC BY-NC-SA 3.0.
- **Covers and versions:** Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024). CC BY-SA 4.0.
