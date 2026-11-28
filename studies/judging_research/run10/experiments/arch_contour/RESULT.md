# arch_contour: result (plain language)

**Verdict by the rule written first: UNSETTLED.** No pass, and no kill. The test was run once, after the rules were committed.

## What was predicted (written first)
Predictions commit 641f966; results commit 629b8da. The question: is a tune whose contour is a few big arches (a "statue") recorded by more distinct artists than one made of many equal bumps (a "texture")? The measure, ARCH_PE, reads every rise and fall of the melody as a bar of a persistence barcode and asks how evenly sized those arches are (high = many equal bumps). Checked on 14,511 split-A tunes, with range and number of distinct pitches held fixed. Prediction: **-0.03** standard deviations of cover-count (y_cov) per standard deviation of ARCH_PE. Pass needed p < .05/9 = 0.00556, a negative effect in both halves, and a negative Poisson coefficient. Kill: -0.03 outside the 95% range. Power was printed before the outcome was joined: **0.643**.

## What came out
- Estimate **-0.018**, standard error 0.0074, p = 0.015. 95% range **-0.032 to -0.003**.
- Halves: -0.011 (N 7,128, p 0.31) and -0.024 (N 7,383, p 0.019). Both negative.
- Second model (Poisson): -0.016, SE 0.017, p = 0.34. Negative, weak.
- Love reading (y_love, log tunebooks, N 7,449; predicted -): -0.002, SE 0.0096, p = 0.84, range -0.021 to +0.017. Halves -0.003 (N 3,607) and +0.001 (N 3,842). Nothing.

Sign, halves and Poisson have the predicted sign; only p falls short (0.015 against 0.0056). The prediction (-0.03) lies inside the range, near its lower edge, so no kill.

## How firm
Weak. The main model leans the predicted way, but the love reading is flat, and the effect disappears once all 13 baselines are held (it even turns slightly positive; reading 2). Fairly read: what signal there is may belong to simpler features of the melody, not to the arches themselves.

## Renaming check
Does this measure just repeat others? From `measure_gates10.json`: two-setting stability 0.806 (n 4,000; bar 0.5); R² on the 13 baselines **0.345**, the most renamed of the counted measures; the largest baseline correlations are range -0.32, n_pitch -0.32, step_share -0.31. Among the counted measures, its largest overlaps are pe_h0 (-0.20) and irr_skel (-0.20). No single baseline exceeds the 0.8 gate, so it was tested, but this is the folder where renaming matters most: holding step_share too barely changes the estimate (-0.016), while holding all 13 baselines removes it (+0.005).

## Frozen readings (estimates only; none passes or kills anything)
1. **Holding step_share as well** (predicted -; N 14,511): **-0.016**, SE 0.0077, p = 0.032, range -0.031 to -0.001.
2. **All 13 baselines held** (predicted -; N 14,511): **+0.005**, SE 0.0082, p = 0.54, range -0.011 to +0.021. Wrong sign, near zero.

## What it cannot say
- It cannot separate the arches from the baselines that predict a third of the measure; once they are all held, nothing is left.
- The outcome counts artists in TheSession.org's recordings list, which members submit; it reflects what that community logs.
- Most tunes are traditional, so there is no composer to hold fixed.
- The measure reads only the first setting of each tune; transcriber differences add noise.
- The first-poster effect could not be held (the design carries no username).
- Low power for a true effect smaller than -0.03 means a small real effect could look like this.
