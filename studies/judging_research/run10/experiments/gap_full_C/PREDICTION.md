# gap_full_C: Jason's S = 1 + g/π on the whole melody, on split C (AFTER SEEING RESULTS; a lead, never in K)

Run 10, 27 November 2026, written by the orchestrator after the eight split-A results (629b8da) and the three split-C confirmations were seen. **Label: after seeing results.** It is not in K = 9; a pass is a lead that needs confirmation on tunes not yet used (split H, sealed).

## Why

On split A, the full-surface spectral gap (the Inventor's GAP, R10-I3, merged into `s_gap_skeleton` as an uncounted estimate) came out at −0.065 (SE 0.008) holding range, n_pitch and ln_notes, while the counted skeleton version (S_gap) was killed (−0.005). The estimate was frozen before the outcome (its reading is in `../s_gap_skeleton/spec.json`), but it was one of several readings and the counted test failed, so it is only a lead. Split C's outcomes have been joined for three other measures (rep_entropy_C, irr_skel_retrace_C, core_typical_C), but GAP has never been compared with C's outcomes.

## The measure (frozen; unchanged)

`measures/measures_inventor.py`, `measure(t)`, key `GAP`: g = λ2 of the normalised Laplacian of the transition graph between octave-distinct pitches of the expanded first setting, closed into a loop (last note to first) and symmetrised (W = c + cᵀ). S = 1 + g/π is a monotone function of g, so the test of g is the test of S. Cache key `GAP` in `/home/claude/dl/thesession/measures_run10.json`.

## Tunes, outcome, model

Split C, every tune with GAP and the extras defined: 4,261. y_cov primary (log 1 + distinct recording artists), y_love a reading. Model, fixed effects, clusters, halves and Poisson exactly as `common10.py`. **Frozen extra controls: range, n_pitch, ln_notes** (as in the A reading).

## Prediction

**β = −0.04 SD of z(y_cov) per SD of GAP** (shrunk from A's −0.065): a small gap, a melody with a bottleneck between two pitch regions that it rarely crosses, goes with more recording artists. y_love: negative.

## Rules

α = .05 (a lead, not in K). Pass = p < .05, negative, both halves negative, Poisson negative. Killed if −0.04 lies outside the 95% range. Otherwise unsettled.

## Power (power.json, fake outcomes on the real C rows, before the outcome)

| power | kill_if_true | kill_if_zero | median fake SE | n |
|---|---|---|---|---|
| **0.423** | 0.037 | 0.497 | 0.0209 | 4,261 |

## Readings (uncounted)

All 13 baselines held; pc_entropy held too; core_ic held too.
