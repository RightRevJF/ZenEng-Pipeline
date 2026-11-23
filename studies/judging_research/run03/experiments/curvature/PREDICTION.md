# Ollivier curvature of the chord walk, beyond size, repetition and surprise: frozen before any outcome is joined

Run 03, 23 November 2026, written by the chair. No cover count, version, release, `first_year` or `discogs_versions_matched.json` has been opened. Figures marked "chair" come from a check on the notes only: 2,672 songs with at least 3 chords, before the first-year filter.

## Claim
This is L1 merged with G1, from Ollivier 2009, Props. 20 and 29.
- **Where κ(x,y) > 0:** chords x and y lead to overlapping next chords. They can stand in for each other, and the walk contracts.
- **Extrapolation:** songs whose moves sit on positively curved links give coverers stand-in chords. Those songs are covered more, beyond what size, within-section repetition (`ch_rep`) and chord surprise (`ch_ic_mean`) already predict.
- **What it builds on:** the one note finding that holds within artists (chords that move, −0.042), and chord surprise (−0.042, not stated in advance).

## Rows, chord graph and model
These are exactly as in `experiments/bridge/PREDICTION.md`:
- the same rows (at least 3 distinct chords, artists with two or more songs);
- the same token, merging and wrap rule;
- moves M pooled over all of the song's clips;
- data-pack measures weighted by `n_mel`;
- the same `within()` model, CR1 clustered SE and md5 halves.

Assert that every node has out-degree ≥ 1, so there are no dead ends.

## Measure
- **Walk:** P is M with each row normalised. Laziness is ½: m_x = ½δ_x + ½P(x,·).
- **Distance:** d is the unweighted shortest path on the undirected support (a link wherever M[a,b] + M[b,a] > 0).
- **Link curvature:** κ({x,y}) = 1 − W1(m_x, m_y), since d(x,y) = 1. W1 is solved exactly as a linear programme with `scipy.optimize.linprog(method="highs")`, using costs d between the two supports.
- **kbar** = Σ_{x≠y} M[x,y]·κ({x,y}) / Σ_{x≠y} M[x,y]. This is the move-weighted mean, wrap moves included.
- **Disconnected songs** (110; chair): κ is local, so it is computed within each piece. These songs are kept.
- **Size** is removed inside the model by holding three things: dummies for distinct chords (4, …, 11 and 12+, with 3 as the reference), the number of distinct links, and log(clips per song).

## Audit first (no outcome)
1. **Unit tests.** These are card 1's lazy values:

   | Graph | κ |
   |---|---|
   | Directed 3-cycle | 0.5 |
   | Directed 4-cycle | 0 |
   | Hub with 4 spokes | 0.25 |
   | K4 | 0.667 |

2. **Prop. 29.** In every piece with two or more nodes, g_lazy = 1 − |λ₂| of that piece's lazy matrix must be ≥ the smallest link κ in the piece − 1e-9 (chair: no violations). If this check or step 1 fails, the code is wrong and must be fixed.
3. **Print the measure's shape:**
   - kbar's distribution (chair: median 0.20; 10th to 90th percentile 0.00 to 0.50);
   - the share of songs with kmin > 0 (chair: 22%);
   - R² of standardised kbar on the size block plus a constant (chair: 0.46).
4. **Print correlations.** Take kbar_res, the residual of kbar after the size block. Print its Spearman correlation with: distinct chords, links, clips, merged moves, pooled lazy g (largest piece), kmin, the bridge indicator B, and all 17 data-pack measures. The chair found lazy g +0.35, ch_h_mean −0.24, B +0.22, ch_ic_mean −0.17 and ch_rep +0.02; every other |ρ| was 0.16 or less.
5. **Reproduce the chair's gate for g** (decides nothing). Take the non-lazy g of each clip by the McGill rule and average over clips, weighted by merged chord count. The chair found ρ = 0.26 with distinct chords, and 0.17 between clip 1 and clip 2.
6. **Stop rule.** Stop, join no outcome and record the test as stopped if either R² > 0.8 or |ρ| > 0.7 for kbar_res with anything listed in step 4.

## Outcome
**Primary:** log(1 + `covers`), all years.

**Secondary, deciding nothing:** covers within 5 years and more than 10 years after the first year, built exactly as in the bridge experiment.

## Model columns
- kbar
- `ch_rep`
- `ch_ic_mean`
- `first_year`
- log(clips per song)
- distinct links
- the nine distinct-chord dummies

**Surprise check:** refit the same model without `ch_ic_mean` and call that estimate β₀.

## Prediction
**β = +0.02 SD of log covers per SD of kbar.** This is the Listener's revised figure. A true effect of about +0.03 would show as about +0.02, because residual kbar agrees only 0.25 between two clips of the same song (chair).

## Power
The script prints the SE and the power before it prints β:

power = Φ(0.02/SE − 2.2414) + Φ(−0.02/SE − 2.2414)

The chair estimates SE ≈ 0.020, so **power ≈ 0.10**. This test will rarely pass. It can kill, though: if nothing is there, β ≤ 0 half the time.

## Rules
Tonight counts two tests, so each needs **p < .025**.
- **Pass:** all four of these hold:
  - β > 0;
  - p < .025;
  - β > 0 in both halves;
  - β ≥ 0.5·β₀.
- **Kill:** β ≤ 0.
- **Kill as surprise renamed:** β₀ > 0 and β < 0.5·β₀.
- **Unsettled:** anything else. A split between the halves does not kill, because each half has power of about 0.06.
- **Opposite sign** (β < 0, p < .025): a new hypothesis, not a pass.

## Reported, deciding nothing
- The secondary outcomes, and β₀.
- The model with the disconnected songs dropped.
- The unweighted mean link κ (chair: ρ 0.91 with kbar).
- The Geometer's shuffle-relative kbar and its ρ with `ch_rep` (Geometer: −0.62). To build it, permute each clip's merged sequence with `numpy.random.default_rng(0)`, merge repeats again, rebuild, and repeat 40 times (10 if 40 would pass 45 minutes; say which). The measure is kbar minus the mean of the shuffled values.

## What it cannot say
- **Low power:** a null or an unsettled result says almost nothing. Only a kill informs, and only weakly.
- **No cause:** a pass would not show that stand-in chords cause covers. All the songs are hits, and they differ in era.
- **Small graphs:** on 3 to 11 chords, κ mostly counts triangles and shared neighbours (Jost–Liu). It is a measure of local overlap, not a smooth geometry.
- **Fixed settings:** laziness ½ and hop distance are fixed choices. The Lin–Lu–Yau limit is not tested.
- **McGill:** the McGill hold-out is untouched.
