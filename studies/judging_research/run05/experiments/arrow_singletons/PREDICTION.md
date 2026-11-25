# The arrow of time on songs by single-song artists. Written AFTER SEEING RESULTS, frozen before this test's outcome is joined

Run 05, 25 November 2026, by the first-principles reviewer (`../../first_principles.md`, section 5). **This rule was written after seeing all seven of tonight's results**, including `arrow_of_time` (A within artist: +0.84 pp per SD, p .035, unsettled). It is the night's **8th test**.

**Threshold: p < .05/8 = .00625, two-sided (z = 2.734).** The seven earlier tests keep their frozen threshold of .00714. This rule changes none of their verdicts.

**What has been opened.** The reviewer read every RESULT.md and opened no outcome file. The figures marked *reviewer* come from a notes-only scratch script that never calls `load_outcomes`.
- No one in the judging research has computed y_foreign for these songs, or joined A to any of their outcomes.
- The covers study on main (15 November) did use cover counts for the matched songs among them, against the 17 measures, across artists. It never used A or y_foreign.

## Claim
`arrow_of_time`'s claim, carried to new songs: chord motion with a direction (one way round a cycle, far from detailed balance) goes with uptake by other artists.

These songs give no within-artist contrast, because each artist here has one song. So this is a cross-song test, with the style the notes carry held as well as the data allow.

## Songs
- **Source:** `common.load_rows()["allsongs"]`, keeping the songs whose `artist` has exactly one song among the 13,198. That gives 3,610 songs and 3,610 artists, none of them in run 04's or tonight's rows.
- **Halves:** half = `int(hashlib.md5(artist.encode()).hexdigest(), 16) % 2` (*reviewer:* 1,852 / 1,758 songs).
- **Model rows:** songs with an A value and all 17 data-pack measures finite (*reviewer:* 3,223; 8 songs have no rhythm row). Songs with y_foreign = NaN are dropped after the outcome is joined.

By construction this set holds none of the prolific game and library "artists" that broke tonight's fame proxy.

## Measure
A, exactly as in `../arrow_of_time/PREDICTION.md` (commit 1f6c36d):
- chord pitch-class sets in onset order, consecutive equal sets collapsed;
- clips with K < 6 changes have no value;
- A = 1 − Σ min(n_ij, n_ji) / Σ n_ij;
- the song value is the mean over the song's clips, weighted by K.

Reuse that test's `changes` and `clip_vals` unchanged. The script must first reproduce the unit values: I–V–vi–IV ×4 gives 1.0000, I–IV ×8 gives 0.0667, I–V–I–IV ×4 gives 0.0667.

*Reviewer:* 3,229 songs have A. Its 10th / 50th / 90th percentiles are 0.333 / 0.864 / 1.000, and 41.3% of songs score exactly 1. ρ(A, `ch_rep`) is +0.04.

## Gate (notes only, before `load_outcomes`)
`common.gate(singleton_rows, "A", extra={"ln_chg": ...})`. It needs clip-to-clip agreement ≥ 0.20 and |ρ| ≤ 0.7. A failure records "stopped".

*Reviewer:* agreement 0.339 on 896 pairs; largest overlap ln_chg −0.187. **Passes.**

## Outcome
**y_foreign**, set by `common.load_outcomes(rows, folder)` on these rows, unchanged (run 04's rule 4410a0e).

## Columns
- z(A) and z of each of the 17 data-pack measures (`common.FE`, which includes `ch_rep` and `ch_ic_mean`), all standardised over the model rows;
- ln_chg = ln(max(total K over all the song's clips, 1));
- run 04's block, `common.controls(model_rows)`;
- an intercept.

Drop any column with no variation in the model rows, and print which ones. Holding the 15 other measures is deliberate: tonight's fame test found that, across artists, the notes mostly carry style (rests, phrasing, sung against instrumental).

## Model
`common.lpm` cannot be used: demeaning by artist zeroes every column when each artist has one song. Instead:
- **Estimate:** OLS with an intercept.
- **SE:** HC1, V = N/(N−K) (X′X)⁻¹ X′ diag(u²) X (X′X)⁻¹. With one song per artist, this equals CR1 by artist.
- **Halves:** the same model within each half.
- **Sign check:** `statsmodels` `Logit` on y_foreign/100 with the same columns (`method="bfgs"`, `maxiter=2000`, then Newton from that point if needed). It counts as converged when max |score| / nobs < 1e−5.

## Prediction
**β(A) on y_foreign = +0.6 pp per SD.** This is tonight's original frozen size, not the +0.84 seen within artist.

## Rules
- **Pass (a lead only):** β > 0, p < .00625, β > 0 in both halves, and a converged logit coefficient > 0.
- **Kill:** β < +0.2.
- **Opposite sign** (β < 0, p < .00625): killed, and reported as a new hypothesis.
- **Unsettled:** anything else.

## Power (notes side)
SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²), where x̃ is z(A)'s residual after every other column.

*Reviewer:* the residual share is 0.921 on 3,223 songs, so **SE ≈ 0.76 pp**. Power at +0.6 is **0.03 at p < .00625** (0.12 at p < .05). The kill line fires 30% of the time if +0.6 is true and 60% if the effect is zero.

There is no fixed effect here, so the real SE should sit near the bound. Tonight's within-artist tests came in under theirs; this one probably will not. The script prints power from its own SE before any β.

## Reported, deciding nothing
- **β(`ch_rep`) in the same model.** This is the first look at chord repetition on y_foreign in songs outside run 04's rows. It is across artists and settles nothing about R04-FV.
- The model without the 15 other measures.
- β(A) on y.
- G2 in place of A.
- y_foreign with karaoke and tribute sets removed.

## Order
1. Unit values.
2. Singleton rows and A, from the notes.
3. Gate.
4. Notes-side power.
5. `load_outcomes`. It refuses unless this file is committed, and it is not yet committed.
6. Counts (N, y_foreign = 100, drops).
7. HC1 SE and power.
8. β, p and 95% range; halves; logit; verdict.
9. The reported items.
10. `result.json`.

## What it cannot say
- **Not a finding, even on a pass.** The rule was chosen after seeing A's result, the test compares across artists, and it is nearly blind.
- **A pass is a lead** that needs within-artist songs not yet used (the Discogs-VI re-match).
- **A kill may be style swamping a real song-level effect**, since nothing holds genre directly.
- **y_foreign is not lasting love.** Hits and non-hits are mixed, and the evidence is association only.
- **McGill hold-out:** untouched. Song 59, songs/p69 and studies/holdout59 were not read.
