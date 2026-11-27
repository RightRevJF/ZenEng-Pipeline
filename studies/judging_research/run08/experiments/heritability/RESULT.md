# heritability: result (R08-I2; card 2's neutral null)

**Verdict: PASS by the rule written first.**

## In plain words
**The neighbour statistic.** For each song, we found the 10 songs by *other* composers whose charts use the most similar three-chord moves. Siblings were excluded: shared names, shared titles, and near-copies of one tune. A song's *residual* is how much more or less it was covered than its composer, genre and era predict. ρ_nb is the correlation between a song's residual and the average residual of its neighbours.

**The permutation null.** Card 2's neutral copying says covers are luck, so neighbours' luck should be unrelated. We shuffled residuals 10,000 times, only among songs sharing a composer, genre and decade. A shuffle keeps the scene and era pattern but breaks any link carried by the chords. The test reads the *excess*: the real ρ_nb minus the shuffled average.

**Result.** Harmonically similar songs by other writers do share cover fortunes, beyond chance. The link is small: a correlation of about 0.05.

## Predicted (commit e624a7e, before any outcome)
Excess = +0.06. Pass needs p < .01, excess > 0, both composer halves > 0, and the excess with 5 neighbours > 0. Kill: +0.06 outside excess ± 1.96 SD(null).

## Came out (result.json; 5,852 songs)
- Power, printed before the estimate: 0.66 at K = 5 (frozen 0.65; composer share 0.3 is an assumption).
- Raw ρ_nb 0.060, null mean 0.009, **excess +0.051**, SE (null SD) 0.013, **p = .0002**, 95% range +0.026 to +0.076.
- Halves: +0.039 (p = .019) and +0.062 (p = .0004).
- 5 neighbours: +0.056 (p = .0001).

## How firm
The sign is firm. The p-value is far below .01 and below the final bar of .05/6 = .0083, and the halves and the second model agree. The size is less firm. +0.06 sits inside the range, but the first half alone would not pass. Raw ρ_nb equals 0.060 by coincidence: the prediction was for the excess.

## Renaming check
This does not apply. The test uses neighbour structure, not one song measure, so measure_gates.json has no gate for it. Nobody checked whether neighbour similarity tracks ch_rep or V.

## Reported, deciding nothing
- Shuffling within genre × decade only: excess +0.061.
- Songs first released in 1950 or later: excess +0.031, p = .021.

## The rival story: shared scene or idiom (jazz), not fitness
For the rival story:
- Neighbours share the coarse genre 31% of the time against 17% by chance. Swing songs (31% of the sample) have 53% swing neighbours (chord data only).
- The tags (swing, ballad, latin) do not separate jazz-canon tunes from the rest. Jazz re-records its canon, so jazz-like changes may mark a covering community rather than appeal.
- The signal halves after 1950, where that canon thins out. Finer cells shrank the excess from 0.061 to 0.051.
- iiv_chunk passed (ii-V-rich songs are covered more). Trigram neighbours share ii-Vs, so this may partly repeat that result.

For fitness: the residual already removes composer, genre and era, the shuffle holds composer × genre × decade, siblings are removed, and both halves agree.

The test cannot tell these apart. It says covers cluster in chord space, not why.

## What it cannot say
- **Genre within composer:** coarse tags only.
- **Chart writers:** iReal and Wikifonia spell chords differently. Genre (which includes "wikifonia") holds this only coarsely.
- **Name matching:** a missed shared writer lets a sibling in.
- **Tune selection:** jazz players choose which tunes to chart, and they also drive the cover counts.
