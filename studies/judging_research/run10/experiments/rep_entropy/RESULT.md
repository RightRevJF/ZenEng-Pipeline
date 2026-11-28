# rep_entropy: result (plain language)

**Verdict by the rule written first: PASSED (split A).** The effect is real in direction but much larger than predicted, so the predicted size (−0.03) lies outside the 95% range. The rule checks the pass before the kill, so the verdict is "passed". The test was run once, after the rules were committed. The finding for this measure is the split C confirmation (`../rep_entropy_C/`), not this result.

## What was predicted (written first)
Predictions commit 641f966 (one of the eight split-A tests run this pass; K = 9 counted tests, α = .05/9 = 0.00556). Results commit 629b8da. The question: do simpler tunes spread further? "Simpler" here is McBride & Leroi's pitch-class entropy: how evenly a tune's time is spread over the twelve pitch classes (low entropy = a few notes carry most of the tune). This is the replication baseline, a known effect on this same site. It was checked on 14,511 split-A tunes from TheSession.org, melody only.

Prediction: **−0.03** standard deviations of y_cov (log of 1 + distinct recording artists) per standard deviation of pitch-class entropy. Pass needed p < 0.00556, a negative estimate, both halves negative, and a negative second-model (Poisson) coefficient. Kill: −0.03 outside the 95% range. Power, printed before the outcome was joined: **0.713** (chance of killing a true −0.03: 0.017; chance of killing if the truth is zero: 0.92).

## What came out
- Estimate **−0.083**, standard error 0.0073, p = 5 × 10⁻³⁰. 95% range **−0.097 to −0.069**. N 14,511 (mean 5.45 recording artists; 69% of tunes recorded at least once).
- Halves: −0.083 (N 7,128) and −0.085 (N 7,383). Both negative, nearly identical.
- Second model (Poisson): −0.154, SE 0.016, p = 1 × 10⁻²². Negative.
- Love reading (log tunebooks, tunes in 10 or more tunebooks; decides nothing): −0.117, SE 0.0095, p = 2 × 10⁻³⁴, range −0.135 to −0.098, N 7,449. Halves −0.122 (N 3,607) and −0.115 (N 3,842). Same direction, a little stronger.

**About the verdict.** Every pass condition is met. The kill condition is also met, because the range (−0.097 to −0.069) does not reach −0.03. `common10.verdict` checks the pass first, so the label is "passed". Said plainly: the direction was right and the size was wrong. The effect is close to three times the predicted size. A pass here means "simpler tunes have more recording artists", not "the effect is −0.03".

## How firm
Firm on split A. The p-value is far below the bar, both halves agree almost exactly, the Poisson model agrees, and the love reading agrees. The known effect shows up on this design, so the design can see effects of this size. It is still one split; the counted finding is the split C rerun.

## Renaming check
Pitch-class entropy is itself one of the 13 renaming baselines, so the renaming gate does not apply. In `../measure_gates10.json` it is stable across two settings of the same tune (Spearman 0.83, n 4,000) and is largely explained by the other baselines (R² 0.732; closest: number of pitch classes +0.72, number of pitches +0.48, tonic share −0.40). The question is whether it just repeats "fewer pitch classes". The readings answer it: with all 12 other baselines held, the estimate is still −0.064 (p = 6 × 10⁻⁷), nearly four fifths of the main estimate.

## Frozen readings (estimates only; none passes or kills anything)
1. **Notes per bar (density)**, predicted −: **−0.038**, SE 0.011, p = 0.0003, range −0.059 to −0.018.
2. **Number of pitch classes (n_pc)**, predicted −: **−0.072**, SE 0.0070, p = 1 × 10⁻²⁴, range −0.086 to −0.058.
3. **Log number of notes (ln_notes; McBride & Leroi's "fewer notes")**, predicted −: **−0.042**, SE 0.0077, p = 4 × 10⁻⁸, range −0.057 to −0.027.
4. **Pitch-class entropy holding density**, predicted −: **−0.081**, SE 0.0073, p = 1 × 10⁻²⁸, range −0.095 to −0.067.
5. **Pitch-class entropy with all 12 other baselines held (all_13_baselines_held)**, predicted −: **−0.064**, SE 0.013, p = 6 × 10⁻⁷, range −0.090 to −0.039.

All five are negative, as predicted. All N 14,511.

## What it cannot say
- It compares tunes, not changes to a tune. It cannot say simplicity causes spread; simpler tunes may be older, more often taught to beginners, or more often chosen for sessions for other reasons.
- The first poster of a tune is not held fixed (the design carries no username), so a poster who posts simple, popular tunes could produce part of this.
- The measure uses the first setting posted. If popular tunes tend to be posted in plainer versions, the link could run partly from popularity to the notes.
- The love reading covers only tunes in 10 or more tunebooks, a truncated sample.
- It says nothing about the predicted size being right; it was too small.
