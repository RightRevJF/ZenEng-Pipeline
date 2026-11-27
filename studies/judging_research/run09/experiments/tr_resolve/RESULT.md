# tr_resolve: result (run 09, 27 November 2026)

**Verdict: ESTIMATE. It passes nothing and kills nothing.** The test had too little power to count (0.193, under the 0.2 floor, K = 1). The estimate came out slightly negative, not positive as predicted.

## What was predicted (written first)
Songs whose dominant chords more often resolve down a fifth or a semitone should be covered by more distinct artists: **+0.035 SD of covers per SD of the measure (TR)**, after holding fixed the other chord and length measures. Power was computed on fake outcomes before the real outcome was joined, and printed again by test.py: **0.193** (N 1,270).

## What the measure counts
TR is the share of chord changes where a dominant-seventh chord moves down a fifth (for example G7 to C) or down a semitone (the tritone substitute, for example Db7 to C). Before counting, every minor-seventh chord that leads straight into a dominant a fourth above it (the ii before the V) is deleted. A chart writer adding or removing a ii therefore cannot move the score.

## What came out (1,270 unseen songs)
| | Estimate | SE | p | 95% range |
|---|---|---|---|---|
| Main model | -0.041 | 0.027 | 0.130 | -0.094 to +0.012 |

- Halves (split by composer key): -0.024 (SE 0.037, N 718) and -0.081 (SE 0.041, N 552). Both negative.
- Second model (Poisson count of artist sets): -0.052 (SE 0.068, p 0.444).
- Clustered by composer: SE 0.029, p 0.157.
- Power printed beforehand: 0.193 (kill rule would fire 5% if the prediction were true, 16% if the effect were zero).

## Verdict by the rule written first
Under the power floor, so the test is an estimate: nothing passes, nothing is killed. For the record, the prediction (+0.035) sits **above the top of the 95% range** (+0.012), so had this test counted, the kill rule would have fired. The pass rule (p < .05, positive, both halves positive, Poisson positive) would have failed on every clause.

## Frozen readings (decide nothing)
1. **DRES per bar** (bar-timed charts, N 1,097; predicted +0.035; power 0.16): -0.030, SE 0.028, p 0.291, range -0.084 to +0.025. Halves +0.014 and -0.111. Poisson -0.100 (p 0.048, the only nominal p under .05 in this folder; it is one of several readings and the main model there is not significant).
2. **TR holding IIV** (no prediction): -0.046, SE 0.028, p 0.104, range -0.101 to +0.009. TR is not near zero in a way that isolates it; it stays slightly negative once the ii-V measure is held. This does not support the "ii-V as chart-writer decoration" lead.
3. **Non-jazz** (N 831; predicted +0.02; power 0.057): -0.023, SE 0.037, p 0.546, range -0.096 to +0.051. The prediction falls inside this range, which is wide enough to hold almost anything.
4. **Chart provenance only** (N 1,074; no prediction): -0.030, SE 0.029, p 0.296, range -0.087 to +0.026. Halves +0.019 and -0.107.

## Renaming check (measure_gates.json)
TR is not a relabelled version of the controls. Song-level rank correlation: ch_rep -0.27, V +0.26 (within genre -0.17 and +0.13), and with IIV +0.50 (+0.33 within genre). With DRES it is +0.87, which is why the two were merged. All under the 0.8 stopping line.

## What the sign means musically
Songs with a larger share of dominants resolving down a fifth or semitone (after the ii before each V is deleted) were, if anything, covered by slightly fewer distinct artist sets. The estimate is small (about four hundredths of an SD) and the range includes zero and small positive values, so this is a faint lean, not a finding.

## What it cannot say
- It cannot confirm or refute the idea: power was under the floor, and the range runs from a modest negative to a tiny positive.
- The two halves disagree in size (the second is about three times the first), and in the DRES and provenance readings the first half is positive, so the result is not stable.
- Two chart writers agree on TR only about 0.60 to 0.63 across sources, so any true effect is diluted.
- Most songs were matched by title alone and charts are not guaranteed to predate the covers. Only a correlation can be read.
- The four readings are not independent tests; they share songs and the same measure.
