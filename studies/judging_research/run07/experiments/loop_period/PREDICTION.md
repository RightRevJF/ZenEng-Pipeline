# The phrase a guitarist must learn: loop period P*. Frozen before any outcome is joined

Run 07, 26 November 2026, by the chair. Idea: R07-L2 (the Listener; revised in round 2 and called "report only" by its author: counted here under Jason's rule, see chair.md). Priority **6 of 8**.

**No outcome has been opened** by the chair or by any brainstorm agent: nothing in `/home/claude/shape/`, nothing in `/home/claude/dl/discogs/`, no covers, versions or hold-out file in the repo, and `/home/claude/dl/lakh/outcomes_run07.json` did not exist when this file was written (checked). Neither `common.load_outcomes` nor `common.run_test` has been called. Figures marked *chair* come from notes-only checks (`../chair_gates.py`, `../chair_gates_report.py`) and fake outcomes (`../power_fake.py`). The McGill hold-out and song 59 were not touched.

**This pass counts eight tests**, in priority order `lakh_repetition`, `tree_h4m`, `spectral_gap`, `lakh_chirality`, `lakh_arrow`, `loop_period`, `burstiness`, `triad_fidelity`. **Each needs p < .05/8 = .00625, two-sided (|z| > 2.734).** The threshold does not move if a test is stopped.

## Claim
**The idea (card 2's window-equals-period rule, Perea & Harer 2015).** You learn a song by learning one cycle. The lag at which the song best repeats itself is its loop period; a 2-bar vamp gives another musician little to carry over, a 4- to 16-bar sentence that returns is worth covering. So within an artist, **longer loop periods go with more uptake by others: +0.6 pp per SD of ln P*, with ln tempo held** (the Skeptic: P* in bars depends on whether the arranger wrote the song in half or double time).

## Measure (frozen)
`common.song_shape(...)["lnP"]`: sounding bars' L1 chroma; D(ℓ) = mean ‖x_{t+ℓ} − x_t‖² for ℓ = 2 … 16; **P* = argmin** (ties to the smaller lag); lnP = ln P*; needs at least 34 sounding bars; mean over the song's files. ln_tempo = ln(tempo) from LPD's midi_info_v2.json (`common.add_shapes`). *Chair:* 5,759 values; P* is 4 bars for 2,039 songs (first file), 8 for 1,240, 2 for 1,097, 16 for 562, another lag for 818; lnP mean 1.653, SD 0.655.

**Extra columns held:** **z(ln_tempo)**.

## Gates (notes only, written before any outcome; Jason's rules: split-half Spearman ≥ 0.20; |ρ| ≤ 0.7 with ch_rep, V, ln_chg and ln_bars)
*Chair:* split-half **0.457** (4,832 pairs; brainstorm 0.454), residual 0.409 (0.417); within-artist overlaps ln_chg **−0.154** (largest renaming), ch_rep −0.073, V −0.030, ln_bars +0.022; ln_tempo +0.054. Passes.

## Songs
The **5,901 within-artist Lakh songs by 1,678 artists** of `common.lakh_songs()` with `common.add_shapes()`: from LPD-5 cleansed's 21,425 tracks, dropping 8,607 tracks on files that carry more than one clean title, 395 tracks by cover-only artists (`common.COVER_ARTISTS`), 1,247 tracks of songs already seen on Hooktheory, 131 tracks of McGill hold-out songs and 25 short or blank tracks; 9,549 songs, of which 5,901 are by artists with two or more. Songs with a missing column are dropped by `common.lpm` (rows for this model: **5,759** by 1,676 artists). **Halves:** md5 of the artist key mod 2 (`common.half_of`): 2,961 and 2,940 songs; 842 and 836 artists.

## Outcome
**y_foreign** exactly as `common.load_outcomes` builds it, after this file and `../common.py` are committed (its guard refuses otherwise): Discogs-VI 20240701 reduced by the maintainer's `cliques_versions.py`; a song matches the clique whose title equals its clean normalised title and whose artists include its artist (most artist sets on ties); y_foreign = 100 if some version's performer set shares no name with the artist's own sets, 0 if not or if unmatched, NaN (dropped) if matched with no own set. **Reported, deciding nothing:** y (in Discogs-VI at all).

## Model (`common.run_test`, one design for every test)
`common.design` columns: z(lnP), z(ln_tempo), z(ln_chg), z(V), z(ln_bars), and MSD year in five-year bins as dummies (unknown, 39.8% of songs, is its own bin; a precision control, not a first-year control). **Linear probability model within artist** (`common.lpm`: artist-demeaned, CR1 standard errors clustered by artist). The same model within each artist half. **Conditional logit** (`common.cond_logit`, grouped by artist, same columns) as a sign check. Fame (Billboard flag, hotttnesss) is **not held** in the primary: it is partly downstream of the outcome.

## Prediction
**β(lnP) on y_foreign = +0.6 percentage points per SD**, within artist.

## Rules (as numbers)
- **Pass:** β > 0 and two-sided p < .00625; β > 0 in both artist halves; conditional-logit coefficient > 0. `test.py` also requires the logit to have converged (run 06's rule): a PASS with a non-converged logit is recorded UNSETTLED.
- **Kill:** **β ≤ 0**. `kill=lambda b: b <= 0`.
- **Opposite sign with p < .00625:** killed, and reported as a new hypothesis, not a pass.
- **Unsettled:** anything else, including split halves or a logit of the other sign.

## Power (fake outcomes on these rows and columns, `common.fake_power`, before any outcome)
Artist baselines Beta(0.25, 1.0) (base rate 0.20, precision 1.25, run 06's calibration), y ~ Bernoulli(baseline + β/100 · z); a pass needs p < α, the predicted sign and the same sign in both halves (the logit is not simulated). 300 draws under the prediction, 150 under zero, seed 7. Kill rates are normal approximations from the mean SE.

| True β (pp per SD) | SE (pp) | Pass rate at .00625 | at .05 | False pass if 0 (.00625 / .05) | Kill fires if true | Kill fires if 0 |
|---|---|---|---|---|---|---|
| +0.6 (the prediction) | 0.60 | **0.023** | 0.123 | 0.000 / 0.020 | 16% | 50% |

**Nearly blind.** Even if the prediction is exactly true, a pass at .00625 is a rare event; a kill is weak evidence. `run_test` prints its own power (400 draws) before the estimate; small Monte Carlo differences from this table are expected.

## Reported, deciding nothing (in `result.json`)
- β on **y**; β with **fame held** (Billboard flag, hotttnesss with a missing flag); β on **first performers only** (`common.first_performer_mask`, R02-3's rule).
- **The seconds form**, lnPsec = ln(P* × 4 × 60 / tempo), which half- or double-time writing cannot move, without ln_tempo (holding ln_tempo would make it lnP again).
- **The categorical form** (86% of P* are powers of two): dummies for P* = 2, 8, 16 and "other" against P* = 4 (first file's P*), ln_tempo and the battery's controls held; the Listener's predicted order 2 < 4 < 8 ≤ 16 is printed, deciding nothing.

## What it cannot say
- **Power** (above): a null clears nothing.
- **MIDI is not the record.** The notes are an arranger's MIDI file matched to the recording by audio; chords are half-bar triad templates.
- **y_foreign is uptake, not love.** No love measure is used (run 06 first principles: flag it in every result).
- **Within artist only; no cause.** Lakh songs lean to well-known artists; Discogs-VI coverage is uneven.

## Order the script follows (`test.py`, `common.run_test`)
guard → power (printed first) → outcome → estimate → halves → logit → readings → verdict → `result.json`.
