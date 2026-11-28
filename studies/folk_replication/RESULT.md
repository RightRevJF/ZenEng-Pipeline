# Folk replication: result

Printed by `python3 -I studies/folk_replication/run.py <clique_counts.json>` at 2026-11-27T20:55:03 (code at 21f0223), which wrote this file and `result.json`. The rule: `PREDICTION.md`.

Matched tunes with an outcome: 473. Artists per tune: median 4, mean 12.6, most 792.

K = 18 tests; pass level .05 / 18 = 0.00278 one-sided. Power is for a correlation of 0.15 (test half at the pass level, times the confirm half at .05).

## All matches (deciding)

Test half 231 tunes, confirm half 242. Power: form A 0.212, form B 0.217. Smallest correlation with power one half: A 0.195, B 0.194. **Power is under one half, so every test here is an estimate.**

| Test | Form | Predicted | Test half: size, p | Confirm half: size, p | Both halves: size | Verdict |
|---|---|---|---|---|---|---|
| Pitch-class entropy | as is | lower | -0.078, 0.1197 | -0.050, 0.220 | -0.062 | estimate |
| Pitch-class entropy | held | lower | +0.075, 0.8027 | +0.095, 0.901 | +0.088 | estimate |
| Next note easy to foresee | as is | lower | -0.057, 0.1959 | +0.031, 0.687 | -0.018 | estimate |
| Next note easy to foresee | held | lower | +0.045, 0.7039 | +0.008, 0.545 | +0.035 | estimate |
| Few different pitches | as is | lower | -0.099, 0.0659 | -0.109, 0.046 | -0.101 | estimate |
| Few different pitches | held | lower | -0.025, 0.4264 | +0.140, 0.858 | +0.069 | estimate |
| Time on the home note | as is | higher | +0.118, 0.0364 | -0.095, 0.929 | +0.010 | estimate |
| Time on the home note | held | higher | +0.053, 0.2396 | -0.075, 0.862 | -0.002 | estimate |
| Five-note scale | as is | higher | +0.004, 0.4747 | -0.027, 0.661 | -0.009 | estimate |
| Five-note scale | held | higher | -0.008, 0.5451 | -0.037, 0.725 | -0.024 | estimate |
| Six-note scale | as is | higher | +0.030, 0.3257 | +0.027, 0.339 | +0.036 | estimate |
| Six-note scale | held | higher | -0.004, 0.5225 | +0.019, 0.385 | +0.006 | estimate |
| Few leaps | as is | lower | -0.022, 0.3697 | -0.010, 0.437 | -0.021 | estimate |
| Few leaps | held | lower | +0.014, 0.5777 | -0.064, 0.177 | -0.028 | estimate |
| Short figures sung again | as is | higher | +0.092, 0.0820 | -0.035, 0.707 | +0.021 | estimate |
| Short figures sung again | held | higher | +0.231, 0.0038 | -0.008, 0.539 | +0.112 | estimate |
| The gate's whole plainness | as is | higher | +0.093, 0.0803 | +0.033, 0.305 | +0.061 | estimate |
| The gate's whole plainness | held | higher | -0.005, 0.5215 | -0.053, 0.730 | -0.031 | estimate |

Verdicts: estimate 18

Tests whose both-halves size has the predicted sign: 11 of 18.

## Exact-title matches only (reported, deciding nothing)

Test half 207 tunes, confirm half 212. Power: form A 0.170, form B 0.173. Smallest correlation with power one half: A 0.207, B 0.206. **Power is under one half, so every test here is an estimate.**

| Test | Form | Predicted | Test half: size, p | Confirm half: size, p | Both halves: size | Verdict |
|---|---|---|---|---|---|---|
| Pitch-class entropy | as is | lower | -0.059, 0.1989 | -0.047, 0.249 | -0.053 | estimate |
| Pitch-class entropy | held | lower | +0.084, 0.8165 | +0.093, 0.881 | +0.093 | estimate |
| Next note easy to foresee | as is | lower | -0.059, 0.1976 | +0.044, 0.737 | -0.015 | estimate |
| Next note easy to foresee | held | lower | +0.034, 0.6469 | +0.036, 0.680 | +0.046 | estimate |
| Few different pitches | as is | lower | -0.072, 0.1516 | -0.089, 0.099 | -0.079 | estimate |
| Few different pitches | held | lower | -0.026, 0.4277 | +0.123, 0.814 | +0.057 | estimate |
| Time on the home note | as is | higher | +0.123, 0.0391 | -0.097, 0.919 | +0.013 | estimate |
| Time on the home note | held | higher | +0.047, 0.2790 | -0.067, 0.814 | -0.001 | estimate |
| Five-note scale | as is | higher | +0.023, 0.3723 | -0.031, 0.675 | -0.002 | estimate |
| Five-note scale | held | higher | +0.011, 0.4437 | -0.050, 0.772 | -0.023 | estimate |
| Six-note scale | as is | higher | +0.046, 0.2531 | +0.053, 0.220 | +0.057 | estimate |
| Six-note scale | held | higher | +0.028, 0.3727 | +0.033, 0.310 | +0.027 | estimate |
| Few leaps | as is | lower | -0.011, 0.4376 | +0.021, 0.620 | +0.000 | estimate |
| Few leaps | held | lower | +0.019, 0.6020 | -0.042, 0.281 | -0.015 | estimate |
| Short figures sung again | as is | higher | +0.091, 0.0973 | +0.015, 0.416 | +0.049 | estimate |
| Short figures sung again | held | higher | +0.232, 0.0069 | +0.053, 0.263 | +0.145 | estimate |
| The gate's whole plainness | as is | higher | +0.086, 0.1092 | +0.032, 0.322 | +0.059 | estimate |
| The gate's whole plainness | held | higher | +0.005, 0.4797 | -0.057, 0.737 | -0.028 | estimate |

Verdicts: estimate 18

Tests whose both-halves size has the predicted sign: 10 of 18.

## Essen tunes only (reported, deciding nothing)

Test half 96 tunes, confirm half 89. Power: form A 0.034, form B 0.033. Smallest correlation with power one half: A 0.304, B 0.306. **Power is under one half, so every test here is an estimate.**

| Test | Form | Predicted | Test half: size, p | Confirm half: size, p | Both halves: size | Verdict |
|---|---|---|---|---|---|---|
| Pitch-class entropy | as is | lower | +0.072, 0.7579 | -0.047, 0.332 | +0.016 | estimate |
| Pitch-class entropy | held | lower | +0.200, 0.9127 | +0.078, 0.722 | +0.127 | estimate |
| Next note easy to foresee | as is | lower | -0.030, 0.3841 | -0.011, 0.460 | -0.031 | estimate |
| Next note easy to foresee | held | lower | +0.079, 0.6988 | -0.134, 0.135 | -0.003 | estimate |
| Few different pitches | as is | lower | -0.007, 0.4738 | +0.019, 0.570 | -0.005 | estimate |
| Few different pitches | held | lower | +0.042, 0.5994 | +0.146, 0.782 | +0.066 | estimate |
| Time on the home note | as is | higher | +0.026, 0.3995 | -0.222, 0.982 | -0.096 | estimate |
| Time on the home note | held | higher | -0.052, 0.6447 | -0.157, 0.886 | -0.088 | estimate |
| Five-note scale | as is | higher | -0.134, 0.9029 | +0.037, 0.367 | -0.048 | estimate |
| Five-note scale | held | higher | -0.154, 0.8774 | -0.060, 0.712 | -0.070 | estimate |
| Six-note scale | as is | higher | -0.053, 0.6969 | +0.162, 0.065 | +0.066 | estimate |
| Six-note scale | held | higher | -0.052, 0.6401 | +0.044, 0.351 | +0.028 | estimate |
| Few leaps | as is | lower | -0.010, 0.4631 | -0.062, 0.281 | -0.032 | estimate |
| Few leaps | held | lower | +0.025, 0.5814 | -0.196, 0.071 | -0.101 | estimate |
| Short figures sung again | as is | higher | +0.107, 0.1488 | -0.017, 0.562 | +0.042 | estimate |
| Short figures sung again | held | higher | +0.218, 0.0483 | -0.167, 0.829 | +0.060 | estimate |
| The gate's whole plainness | as is | higher | +0.012, 0.4523 | +0.019, 0.429 | +0.019 | estimate |
| The gate's whole plainness | held | higher | -0.116, 0.7717 | -0.046, 0.630 | -0.065 | estimate |

Verdicts: estimate 18

Tests whose both-halves size has the predicted sign: 10 of 18.

Sizes: form A is Spearman's correlation with the number of artists; form B is the change in log(artists) per standard deviation of the measure, with log length, range, metre and collection held. p is one-sided, in the predicted direction.
