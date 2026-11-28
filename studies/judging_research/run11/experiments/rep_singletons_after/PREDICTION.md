# rep_singletons_after: REP on the single-song artists (AFTER SEEING RESULTS; a lead, never in K)

Run 11, 28 November 2026. **Written after seeing the eight results of this pass** (rep_entropy passed, K = 5). Its outcome has not been joined. It is **not counted in K**: a pass here is a lead that needs songs not yet used, never a finding.

## Why
rep_entropy passed within artist on 9,588 seen songs. The cheapest further check with the data at hand: the same measure on the Hooktheory songs whose artist has only ONE song in the set (they cannot enter an artist fixed effect, so run 04's rows leave them out). Their outcome was joined once before, to one chord measure (run 05, `arrow_singletons`). They are seen songs too, said plainly; the measure is new to them.

## Measure (frozen)
`pc_entropy` exactly as `common11.baseline` (duration-weighted pitch-class entropy of each clip's melody, clips of 12+ notes; song = n_mel-weighted mean), the same key as rep_entropy's `REP`.

## Songs
Every song of `C5.load_rows()['allsongs']` whose artist slug has exactly one song there, with a value (about 3,600).

## Outcome, model
y_foreign (run 04's rule via `C5.load_outcomes`; nan dropped). OLS of z(y_foreign) on z(pc_entropy) + run 04's controls (`C5.controls`), **no artist effect** (one song per artist), HC1 robust SEs. Second model: logit of the binary outcome on the same columns, sign only. Halves: md5(artist slug) mod 2.

## Prediction
β = **−0.03** (fewer different pitch classes, more often taken up by another artist).

## Rule
Lead passes if p < .05, the sign is negative, both halves negative and the logit negative. Killed if −0.03 lies outside β ± 1.96 SE. Otherwise unsettled. Power is printed below before the join (fake outcomes, 300 draws, seed 11, α .05).

Readings (decide nothing): n_pitch, range, ln_notes and mel_ic_mean held; the across-artist confound (genre, era) is NOT held here, which is why this is a weak check.

## Power (before the join)
From power.json: **0.383** at α .05 for β = −0.03 (fake SE 0.0173, 3,610 songs, 300 draws, seed 11).

## How to run
`python3 test.py run` (after this file and common11.py are pushed; common11.load_outcomes refuses otherwise).
