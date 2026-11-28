# gap_full_C: result (plain language)

**Verdict by the rule written after seeing results: PASSED, as a lead.** It is not a counted finding. It is not in K = 9, its rule was written after the split-A results were seen, and it needs confirmation on the sealed split H. The test was run once, after its rule and power were committed.

## What was predicted (written after seeing results)
Rule and power commit d823e98. The rule was written **after** the eight split-A results (629b8da) and the three split-C confirmations were seen. On split A the counted skeleton version of Jason's S (`../s_gap_skeleton/`) was killed (−0.005), while one of its frozen readings, the full-melody spectral gap GAP, came out strong (−0.065). This test asks whether that reading holds on split C. GAP had never been compared with split C's outcomes, but C's outcomes had already been joined for three other measures. The results of this run are in this folder and are not yet committed.

The measure: GAP, the spectral gap g of the graph of moves between notes over the whole melody (every note; octave-distinct pitches as nodes; the melody closed into a loop, last note to first). S = 1 + g/π rises with g, so a test of g is a test of S. A small gap means the melody has two pitch regions that it rarely crosses between. Controls held: range, number of pitches and log number of notes, as in the A reading. Split C: 4,261 tunes from TheSession.org, melody only.

Prediction: **−0.04** standard deviations of y_cov (log of 1 + distinct recording artists) per standard deviation of GAP, shrunk from A's −0.065. Pass at α = .05 needed p < .05, a negative estimate, both halves negative, and a negative Poisson coefficient. Kill: −0.04 outside the 95% range. Power on C, printed before the outcome: **0.423** (chance of killing a true −0.04: 0.037; chance of killing if the truth is zero: 0.497).

## What came out
- Estimate **−0.067**, standard error 0.016, p = 2 × 10⁻⁵. 95% range **−0.098 to −0.036**. N 4,261 (mean 5.26 recording artists; 68% recorded at least once).
- Halves: −0.086 (N 2,106, p = 0.0002) and −0.051 (N 2,155, p = 0.021). Both negative.
- Second model (Poisson): −0.172, SE 0.040, p = 2 × 10⁻⁵. Negative.
- Love reading (log tunebooks, tunes in 10 or more tunebooks; decides nothing): −0.070, SE 0.021, p = 0.0008, range −0.112 to −0.029, N 2,180. Halves −0.083 (N 1,060) and −0.059 (N 1,120, p = 0.056).

All pass conditions are met. The predicted −0.04 lies inside the range, so there is no kill. The estimate (−0.067) is almost exactly A's (−0.065).

## How firm
Strong as a lead, not yet a finding. On C the estimate matches A, clears p < .05 by a wide margin, and both halves, the Poisson model and the love reading agree. But the choice to test GAP came from looking at the A results: it was the strongest of several readings in a test that failed. Nothing about C itself was chosen after seeing C's GAP outcome, so the C result is a fair out-of-sample check of a lead picked on A. To count, it must be confirmed on the sealed split H with a rule written beforehand.

## Renaming check
From `../measure_gates10.json` (split A, notes only): GAP is stable across two settings of a tune (Spearman 0.823, n 3,999), but it leans heavily on the baselines (R² 0.63; range −0.58, number of pitches −0.53, leap share +0.37). No single baseline passes the 0.8 renaming bar, so it was not stopped. The readings on C test the worry directly: with **all 13 baselines held** the estimate is −0.052 (p = 0.011), about four fifths of the main estimate. Holding pitch-class entropy (the run-10 replication finding) changes almost nothing (−0.066), and holding core_ic changes little (−0.060). So it is not just range, number of pitches or simplicity under another name, though part of it overlaps with the baselines.

## Frozen readings (estimates only; none passes or kills anything)
1. **All 13 baselines held (all_13_baselines_held)**, predicted −: **−0.052**, SE 0.021, p = 0.011, range −0.092 to −0.012. N 4,261.
2. **Holding pitch-class entropy too**, predicted −: **−0.066**, SE 0.016, p = 3 × 10⁻⁵, range −0.096 to −0.035. N 4,261.
3. **Holding core_ic too**, predicted −: **−0.060**, SE 0.016, p = 0.0002, range −0.091 to −0.029. N 4,234.

All three are negative and their ranges exclude zero.

## What it cannot say
- It is a lead, picked after seeing results. It does not count toward run 10's K = 9 and needs a confirmation on split H.
- It says this works for the full melody, not the beat skeleton; why the two differ is not known. Part of the full-melody gap may come from leaps between registers, which the skeleton version (pitch classes only) cannot see.
- It compares tunes, not changes to a tune, so it cannot say the shape causes spread. The first poster is not held fixed (no username in the design).
- About a fifth of the estimate goes away when all baselines are held, so the size of the part that is new is nearer −0.05 than −0.07.
- The love reading is on a truncated sample (10 or more tunebooks).
