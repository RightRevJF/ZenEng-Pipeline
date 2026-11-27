# Chord repetition on whole songs: the standing prediction. Frozen before any outcome is joined

Run 07, 26 November 2026, by the chair. Idea: R04-FV and R06-L3 (the battery primary), carried as run 06's first-principles prediction for the next independent batch. Priority **1 of 8**.

**No outcome has been opened** by the chair or by any brainstorm agent: nothing in `/home/claude/shape/`, nothing in `/home/claude/dl/discogs/`, no covers, versions or hold-out file in the repo, and `/home/claude/dl/lakh/outcomes_run07.json` did not exist when this file was written (checked). Neither `common.load_outcomes` nor `common.run_test` has been called. Figures marked *chair* come from notes-only checks (`../chair_gates.py`, `../chair_gates_report.py`) and fake outcomes (`../power_fake.py`). The McGill hold-out and song 59 were not touched.

**This pass counts eight tests**, in priority order `lakh_repetition`, `tree_h4m`, `spectral_gap`, `lakh_chirality`, `lakh_arrow`, `loop_period`, `burstiness`, `triad_fidelity`. **Each needs p < .05/8 = .00625, two-sided (|z| > 2.734).** The threshold does not move if a test is stopped.

## Claim
Within artists, songs whose chords repeat more are more often released by another artist. Run 04 saw +1.00 pp per SD on seen Hooktheory songs (p .044) and run 06 +1.32 on fresh ones (SE 1.04, p .20); neither passed. Run 06's first principles wrote the prediction for the next independent batch: **+1.0 pp per SD, kill if β ≤ 0.** These 5,901 Lakh songs are that batch: no outcome of theirs has ever been joined to anything.

**The measure is a different construct here** (the Skeptic, design issue 5). MIDI ch_rep correlates only 0.32 with Hooktheory ch_rep on 1,487 shared songs, yet its split-half is 0.75 and two-file agreement 0.78: it is a stable reading of the arrangement's half-bar triads, not a noisy copy of a transcriber's chords. Through the shared part alone the Skeptic expects +0.3 to +0.5. The prediction stays +1.0 as written; **an estimate between 0 and +1.0 that is not significant is neither a pass nor a kill: it is unsettled** (stated here before the outcome, as the Skeptic asked).

## Measure (frozen)
`common.repetition(toks, 3)` via `common.track_measures`: the share of chord 3-grams already heard earlier in the track's chord sequence (half-bar triads, runs collapsed, `lakh_notes.py`); per song, the mean over its files. *Chair:* 5,901 values; 10th / 50th / 90th percentiles 0.357 / 0.639 / 0.825; mean 0.612, SD 0.183 (the z scale).

**Extra columns held:** none (the battery's own controls only).

## Gates (notes only, written before any outcome; Jason's rules: split-half Spearman ≥ 0.20; |ρ| ≤ 0.7 with ch_rep, V, ln_chg and ln_bars)
ch_rep is the battery's primary and needs no gate; for the record, *chair* split-half (first half of the chords against the second, first file) **0.742** on 5,901 songs (brainstorm 0.75), residual after V, ln_chg, ln_bars 0.313; largest within-artist overlap V −0.598.

## Songs
The **5,901 within-artist Lakh songs by 1,678 artists** of `common.lakh_songs()` with `common.add_shapes()`: from LPD-5 cleansed's 21,425 tracks, dropping 8,607 tracks on files that carry more than one clean title, 395 tracks by cover-only artists (`common.COVER_ARTISTS`), 1,247 tracks of songs already seen on Hooktheory, 131 tracks of McGill hold-out songs and 25 short or blank tracks; 9,549 songs, of which 5,901 are by artists with two or more. Songs with a missing column are dropped by `common.lpm` (rows for this model: **5,901** by 1,678 artists). **Halves:** md5 of the artist key mod 2 (`common.half_of`): 2,961 and 2,940 songs; 842 and 836 artists.

## Outcome
**y_foreign** exactly as `common.load_outcomes` builds it, after this file and `../common.py` are committed (its guard refuses otherwise): Discogs-VI 20240701 reduced by the maintainer's `cliques_versions.py`; a song matches the clique whose title equals its clean normalised title and whose artists include its artist (most artist sets on ties); y_foreign = 100 if some version's performer set shares no name with the artist's own sets, 0 if not or if unmatched, NaN (dropped) if matched with no own set. **Reported, deciding nothing:** y (in Discogs-VI at all).

## Model (`common.run_test`, one design for every test)
`common.design` columns: z(ch_rep), z(ln_chg), z(V), z(ln_bars), and MSD year in five-year bins as dummies (unknown, 39.8% of songs, is its own bin; a precision control, not a first-year control). **Linear probability model within artist** (`common.lpm`: artist-demeaned, CR1 standard errors clustered by artist). The same model within each artist half. **Conditional logit** (`common.cond_logit`, grouped by artist, same columns) as a sign check. Fame (Billboard flag, hotttnesss) is **not held** in the primary: it is partly downstream of the outcome.

## Prediction
**β(ch_rep) on y_foreign = +1.0 percentage points per SD**, within artist.

- **Between 0 and +1.0** (the Skeptic's request, written before the outcome): if not significant at .00625, the test is **unsettled**, neither a pass nor a kill. If significant with both halves and the logit positive, it **passes the direction** and is reported as smaller than predicted.
- **Run 06's first principles attached a condition** to this prediction: "one counted test at .05 … run only with fake-outcome power of 0.5 or more". Neither holds: Jason's standing rule shares .05 among the eight tests run tonight, and power is far below 0.5 (table below). That condition was a recommendation Jason has not adopted, so the chair runs and counts the test under his rule and flags the conflict in chair.md.

## Rules (as numbers)
- **Pass:** β > 0 and two-sided p < .00625; β > 0 in both artist halves; conditional-logit coefficient > 0. `test.py` also requires the logit to have converged (run 06's rule): a PASS with a non-converged logit is recorded UNSETTLED.
- **Kill:** **β ≤ 0**. `kill=lambda b: b <= 0`.
- **Opposite sign with p < .00625:** killed, and reported as a new hypothesis, not a pass.
- **Unsettled:** anything else, including split halves or a logit of the other sign.

## Power (fake outcomes on these rows and columns, `common.fake_power`, before any outcome)
Artist baselines Beta(0.25, 1.0) (base rate 0.20, precision 1.25, run 06's calibration), y ~ Bernoulli(baseline + β/100 · z); a pass needs p < α, the predicted sign and the same sign in both halves (the logit is not simulated). 300 draws under the prediction, 150 under zero, seed 7. Kill rates are normal approximations from the mean SE.

| True β (pp per SD) | SE (pp) | Pass rate at .00625 | at .05 | False pass if 0 (.00625 / .05) | Kill fires if true | Kill fires if 0 |
|---|---|---|---|---|---|---|
| +1.0 (the prediction) | 1.03 | **0.007** | 0.077 | 0.000 / 0.013 | 17% | 50% |
| +0.4 (the Skeptic's expected size) | 1.03 | **0.000** | 0.033 | | | |

**Nearly blind.** Even if the prediction is exactly true, a pass at .00625 is a rare event; a kill is weak evidence. `run_test` prints its own power (400 draws) before the estimate; small Monte Carlo differences from this table are expected.

## Reported, deciding nothing (in `result.json`)
- β on **y**; β with **fame held** (Billboard flag, hotttnesss with a missing flag); β on **first performers only** (`common.first_performer_mask`, R02-3's rule).
- **W01-J6a, early and late uptake** (run 02's ruling: printed, nothing decided on their contrast): y_early = 100 if a foreign version set has a year ≤ the clique's first year + 5; y_late = 100 if > first year + 10; 0 if unmatched; NaN if y_foreign is NaN or the first year is unknown. Same columns.
- The Skeptic's expected size: power is also printed at +0.4 (below).

## What it cannot say
- **Power** (above): a null clears nothing.
- **MIDI is not the record.** The notes are an arranger's MIDI file matched to the recording by audio; chords are half-bar triad templates.
- **y_foreign is uptake, not love.** No love measure is used (run 06 first principles: flag it in every result).
- **Within artist only; no cause.** Lakh songs lean to well-known artists; Discogs-VI coverage is uneven.

## Order the script follows (`test.py`, `common.run_test`)
guard → power (printed first) → outcome → estimate → halves → logit → readings → verdict → `result.json`.
