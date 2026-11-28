# rep_entropy_C: result (plain language)

**Verdict by the rule written first: PASSED (counted confirmation on split C).** This is the finding for pitch-class entropy in run 10: simpler tunes have more recording artists, on tunes never before joined to an outcome. As on split A, the predicted size (−0.03) lies just outside the 95% range because the effect is larger; the rule checks the pass before the kill. The test was run once, after its rule and power were committed.

## What was predicted (written first)
The confirmation rule was frozen with the split-A predictions (commit 641f966): a counted test that passes on A is rerun once on split C with the identical spec, the same predicted sign and size, at α = .05 divided by the number of tests that passed on A. Three passed (rep_entropy, irr_skel_retrace, core_typical), so α = .05/3 = 0.0167. This folder's rule and power were committed in 629b8da, before the C outcome was joined. Results commit d823e98.

The measure is McBride & Leroi's pitch-class entropy (how evenly a tune's time is spread over the twelve pitch classes). Split C: 4,261 tunes from TheSession.org, melody only, never before joined to any outcome. Prediction: **−0.03** standard deviations of y_cov (log of 1 + distinct recording artists) per standard deviation of entropy, the frozen size from A, not A's estimate. Pass needed p < 0.0167, a negative estimate, both halves negative, and a negative Poisson coefficient. Kill: −0.03 outside the 95% range. Power on C, printed before the outcome: **0.277** (chance of killing a true −0.03: 0.027; chance of killing if the truth is zero: 0.43). Counted, since power is above 0.2.

## What came out
- Estimate **−0.062**, standard error 0.014, p = 6 × 10⁻⁶. 95% range **−0.089 to −0.035**. N 4,261 (mean 5.26 recording artists; 68% recorded at least once).
- Halves: −0.056 (N 2,106, p = 0.004) and −0.067 (N 2,155, p = 0.0008). Both negative.
- Second model (Poisson): −0.094, SE 0.030, p = 0.002. Negative.
- Love reading (log tunebooks, tunes in 10 or more tunebooks; decides nothing): −0.091, SE 0.017, p = 1.5 × 10⁻⁷, range −0.125 to −0.057, N 2,180. Halves −0.100 (N 1,060) and −0.080 (N 1,120).

**About the verdict.** All pass conditions are met. The top of the range (−0.035) also sits just below −0.03, so the kill condition is met too; the pass is checked first. Plainly: the direction replicated, and the size is again larger than predicted (about twice). The estimate is smaller than A's −0.083, which is the usual pull-back on new data.

## How firm
Firm. Power was only 0.277 for a true −0.03, but the true effect is about twice that, and the estimate cleared the bar by a wide margin (p = 6 × 10⁻⁶ against 0.0167). Both halves, the Poisson model and the love reading agree, and A and C agree. This is the one run-10 replication of a known effect; it shows the design can see a real effect of this size.

## Renaming check
Pitch-class entropy is one of the 13 renaming baselines, so the renaming gate does not apply. From `../measure_gates10.json` (split A, notes only): two-setting stability 0.83; R² 0.732 on the other baselines; closest are number of pitch classes (+0.72), number of pitches (+0.48) and tonic share (−0.40). On C the effect does not shrink when the other 12 baselines are held: **all_13_baselines_held** gives −0.082 (p = 0.002), the same size as the main estimate. So it is not just "fewer pitch classes" under another name.

## Frozen readings (estimates only; none passes or kills anything)
1. **Notes per bar (density)**, predicted −: **−0.038**, SE 0.020, p = 0.060, range −0.078 to +0.002.
2. **Number of pitch classes (n_pc)**, predicted −: **−0.035**, SE 0.013, p = 0.008, range −0.061 to −0.009.
3. **Log number of notes (ln_notes)**, predicted −: **−0.033**, SE 0.015, p = 0.025, range −0.062 to −0.004.
4. **Pitch-class entropy holding density**, predicted −: **−0.060**, SE 0.014, p = 1.6 × 10⁻⁵, range −0.087 to −0.033.
5. **Pitch-class entropy with all 12 other baselines held (all_13_baselines_held)**, predicted −: **−0.082**, SE 0.026, p = 0.002, range −0.133 to −0.031.

All five are negative. Density is the only one whose range touches zero. All N 4,261.

## What it cannot say
- It compares tunes, not changes to a tune, so it cannot say simplicity causes spread. Older, beginner-friendly or session-standard tunes may be simpler for other reasons.
- The first poster is not held fixed (no username in the design).
- The first posted setting is measured; popular tunes may be posted in plainer versions, which would run the link partly backwards.
- The love reading is on a truncated sample (10 or more tunebooks).
- The size is still uncertain: the range runs from about −0.035 to −0.089. The prediction of −0.03 was too small on both splits.
- Split H stays sealed; this result does not use it.
