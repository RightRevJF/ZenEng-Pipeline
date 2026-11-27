# tr_resolve: dominants that resolve, read on the ii-collapsed path (G09-2 merged with R09-L2). ESTIMATE

Run 09, 27 November 2026. Frozen by the chair before any outcome is joined. **Status: ESTIMATE** (fake-outcome power 0.193 at
α .05/K with K = 1, under the 0.2 floor by 0.007; it passes nothing and kills nothing). K = 1, α = .05, for reference.

## Measure (the Geometer's recipe, copied into `measures09.py`: `tokens_with_dur`, `ii_collapse`, `TR`)
- Tokens: chart events with a non-empty bitmap, (root, bitmap) with consecutive repeats merged.
- **ii-collapse** (the quotient by ii insertion): delete every m7 token (bits 3, 10, not 4) that is immediately followed by a d7 token
  (bits 4, 10, not 3) a fourth up ((r2 − r1) mod 12 = 5); merge repeats again. Inserting or deleting such a ii cannot move the measure.
- **TR** = (changes on the collapsed path where a d7 moves to a root a fifth down, (r2 − r1) mod 12 = 5, or a semitone down,
  (r2 − r1) mod 12 = 11, the tritone substitute: same tritone, same two contrary semitones) / (changes on the collapsed path);
  nan if the collapsed path has fewer than 6 tokens. Defined on both timebases. Song value = mean over measured charts.
- Unit tests in `measures09.unit_tests()` (C Dm7 G7 C equals C G7 C after the collapse; a worked chain gives 3/6).

## Merge
The Skeptic ruled G09-2 (TR) and R09-L2 (DRES) one idea: both count dominants that resolve down a fifth or a semitone. Both authors
agreed, with TR primary (a ii cannot move it; DRES per bar shifts 0.105 SD when one is inserted; TR is defined on recordings timed
in seconds). On this design ρ(TR, DRES) = 0.87. DRES is the second reading.

## Songs, outcome, model
As `iiv_confirm09` (the 1,270 design songs with TR and every column; y_cov; plain OLS HC1 on z(TR), z(w_chr), z(ch_rep), z(V),
z(ln_chg), z(ln_bars), z(no_bars), genre and decade dummies; the timebase rule; halves by the composer key; `posthoc08.poisson_plain`
second model; CR1 by composer reported).

## Prediction
**β = +0.035 SD per SD of TR** (both authors: +0.04 shrunk for title-only matches and a writer agreement of 0.60; the Geometer
declined to inflate it to buy power).

## Rules, were it counted (it is not)
Pass: p < .05, β > 0, both halves > 0, Poisson > 0. Kill: +0.035 outside β ± 1.96 SE. As an estimate the verdict is
"estimate: passes nothing, kills nothing", and the range is reported.

## Power (printed again by test.py before the outcome)
`harness09.fake_power`, β +0.035, 300 draws: **0.193 at .05** (N 1,270, fake SE 0.033; Monte Carlo error about ±0.023). Range kill
fires in 5% of draws if the prediction is true, 16% if the effect is zero. The margin under the floor is inside the Monte Carlo error;
the chair froze the 300-draw rule before seeing this number (as run 08) and does not re-draw.

## Frozen readings (deciding nothing)
1. **DRES per bar** (R09-L2: resolved d7 tokens, next root a fifth or a semitone down, on the uncollapsed change tokens, per bar,
   bars = ⌊last onset⌋ − ⌊first onset⌋ + 1; bar-timed charts only, so N 1,097), predicted **+0.035**; power 0.16.
2. **TR holding IIV** (no prediction): the Geometer's contrast. TR near 0 while IIV stays positive would read the ii-V as chart-writer
   decoration; this is a lead.
3. **TR, non-jazz genres** (N 831), predicted **+0.02** (G09-2's non-jazz reading); power 0.057.
4. TR, chart provenance only (N 1,074), no prediction.
