# s_gap_skeleton: result (plain language)

**Verdict by the rule written first: KILLED.** The predicted −0.03 lies outside the 95% range (−0.019 to +0.009). The test was run once, after the rules were committed. It is not run on split C.

## What was predicted (written first)
Predictions commit 641f966 (one of the eight split-A tests run this pass; K = 9 counted tests, α = .05/9 = 0.00556). Results commit 629b8da. The question: Jason's S = 1 + g/π, where g is the spectral gap of a graph of how a melody moves between its notes. A small g means the melody has two regions it rarely crosses between, for example the tonic triad and the other scale degrees; the idea is that this clear two-region shape, like an implied harmony, makes a tune spread. Here S is measured on the **beat skeleton**: only the notes that start on a beat, with pitch classes as the nodes. That choice was made so S would not just repeat the tune's range. Checked on 14,511 split-A tunes from TheSession.org, melody only, holding the number of pitch classes fixed.

Prediction: **−0.03** standard deviations of y_cov (log of 1 + distinct recording artists) per standard deviation of S (smaller gap, more covers). Pass needed p < 0.00556, a negative estimate, both halves negative, and a negative Poisson coefficient. Kill: −0.03 outside the 95% range. Power, printed before the outcome: **0.673** (chance of killing a true −0.03: 0.047; chance of killing if the truth is zero: 0.923).

## What came out
- Estimate **−0.005**, standard error 0.0070, p = 0.48. 95% range **−0.019 to +0.009**. N 14,511 (mean 5.45 recording artists; 69% recorded at least once).
- Halves: +0.004 (N 7,128) and −0.013 (N 7,383). Not both negative.
- Second model (Poisson): **+0.039**, SE 0.016, p = 0.015. The wrong sign.
- Love reading (log tunebooks, tunes in 10 or more tunebooks; decides nothing): −0.004, SE 0.0092, p = 0.66, range −0.022 to +0.014, N 7,449. Halves +0.015 (N 3,607) and −0.018 (N 3,842).

The estimate is close to zero. It fails the pass rule on p, on the halves and on the Poisson sign, and the range excludes −0.03, so it is killed.

## How firm
Firm as a kill of this measure at this size. Power was 0.67, and a true −0.03 would have been killed only about 5% of the time; the data put the effect between about −0.02 and +0.01. A smaller true effect (around −0.01 or −0.02) is not ruled out. The Poisson model leans the other way (p = 0.015), which also argues against the predicted direction.

## Renaming check
From `../measure_gates10.json` (split A, notes only): S_gap is stable across two settings of a tune (Spearman 0.75, n 3,999; bar 0.5) and is not a rename of the baselines (R² 0.155; closest: pitch-class entropy −0.22, number of pitch classes −0.19, range +0.13). Its rank correlations with the other counted measures are all 0.22 or less in size. The readings that hold more baselines (below) stay near zero, so nothing is being hidden by the controls.

## Frozen readings (estimates only; none passes or kills anything)
1. **S_gap holding pitch-class entropy too**, predicted −: **−0.011**, SE 0.0071, p = 0.12, range −0.025 to +0.003. N 14,511.
2. **GAP, the Inventor's full-melody version (R10-I3)**: the same spectral gap on the whole melody, every note, octave-distinct pitches as nodes, the melody closed into a loop; holding range, number of pitches and log number of notes; predicted −0.03, uncounted: **−0.065**, SE 0.0083, p = 4 × 10⁻¹⁵, range −0.081 to −0.049. N 14,511.
3. **g, the Listener's version (L3; a near-duplicate of GAP, ρ 0.97)**, same controls, predicted −: **−0.064**, SE 0.0086, p = 7 × 10⁻¹⁴, range −0.081 to −0.048. N 14,413.
4. **S_gap with all 13 baselines held (all_13_baselines_held; number of pitch classes was already held)**, predicted −: **−0.012**, SE 0.0072, p = 0.10, range −0.026 to +0.002. N 14,511.

The full-melody GAP reading is strong, while the skeleton version is not. That contrast was noticed only after the results were seen. GAP was one of four readings, and it leans heavily on range and number of pitches (R² 0.63 on the baselines; range −0.58, number of pitches −0.53, leap share +0.37; stability 0.823). Its reading here held range, number of pitches and number of notes, but not all 13 baselines. So it is a lead, not a finding. It was then tested on split C after seeing these results (`../gap_full_C/`).

## What it cannot say
- It kills S on the beat skeleton with pitch classes as nodes, at the size −0.03. It does not kill S in every form: the full-melody version behaves very differently (reading 2).
- Effects smaller than about −0.02 are not ruled out.
- It compares tunes, not changes to a tune, and the first poster is not held fixed (no username in the design).
- The beat skeleton depends on how the transcriber placed notes on beats; transcription habits add noise, which pulls any effect toward zero.
- The love reading is on a truncated sample (10 or more tunebooks).
