# Harmonic chirality on whole songs. Frozen before any outcome is joined

Run 07, 26 November 2026, by the chair. Idea: R06-I1 (the Inventor; unsettled in run 06 on seen Hooktheory songs, −0.30 against −0.6). Priority **4 of 8**.

**No outcome has been opened** by the chair or by any brainstorm agent: nothing in `/home/claude/shape/`, nothing in `/home/claude/dl/discogs/`, no covers, versions or hold-out file in the repo, and `/home/claude/dl/lakh/outcomes_run07.json` did not exist when this file was written (checked). Neither `common.load_outcomes` nor `common.run_test` has been called. Figures marked *chair* come from notes-only checks (`../chair_gates.py`, `../chair_gates_report.py`) and fake outcomes (`../power_fake.py`). The McGill hold-out and song 59 were not touched.

**This pass counts eight tests**, in priority order `lakh_repetition`, `tree_h4m`, `spectral_gap`, `lakh_chirality`, `lakh_arrow`, `loop_period`, `burstiness`, `triad_fidelity`. **Each needs p < .05/8 = .00625, two-sided (|z| > 2.734).** The threshold does not move if a test is stopped.

## Claim
**The mathematics (run 06; Green's theorem on the Hodge cycle part).** Put each chord's root on the circle of fifths; the progression sweeps a signed area. Moves that go and come back add exactly 0, so CH reads only the loop part of the flow, and it is the one measure that changes sign when a song is played backwards. Falling fifths (ii–V–I) turn clockwise (negative); I–V–vi–IV turns counterclockwise.

**The claim (the Inventor's extrapolation).** The most re-recorded repertoire, the standards, turns clockwise; so within an artist, **songs that turn clockwise (negative CH) are more often taken up by another artist: −0.6 pp per SD.** Unchanged from run 06 in direction, size and kill line.

**What is new.** The songs are whole and fresh, and the chords are read from MIDI (half-bar triad templates, roots only), not from a transcriber. Run 06's first principles noted that |CH| was as large as signed CH; |CH| is reported here, deciding nothing.

## Measure (frozen)
`common.CH(toks)` via `common.track_measures`: θ_t = 2π · ((7 · root_t) mod 12)/12 with root = token mod 12; **CH = (1/K) Σ ½ sin(θ_{t+1} − θ_t)** over the open walk (no wrap); K < 6: no value; mean over the song's files. *Chair:* 5,900 values; percentiles −0.041 / 0.000 / +0.046; mean +0.0017, SD 0.0376; 49.9% above 0, 0.9% exactly 0.

**Extra columns held:** **z(A)** and **z(ch_rep)**, as in run 06's chirality model (run 06's ch_ic_mean is a Hooktheory corpus score and does not exist for these songs).

## Gates (notes only, written before any outcome; Jason's rules: split-half Spearman ≥ 0.20; |ρ| ≤ 0.7 with ch_rep, V, ln_chg and ln_bars)
*Chair:* split-half **0.619**, residual 0.610; within-artist overlaps ch_rep **+0.071** (largest renaming), V −0.067, ln_chg +0.048, ln_bars +0.046; A +0.003. Passes (run 06: 0.252 seen, 0.238 fresh clips).

## Songs
The **5,901 within-artist Lakh songs by 1,678 artists** of `common.lakh_songs()` with `common.add_shapes()`: from LPD-5 cleansed's 21,425 tracks, dropping 8,607 tracks on files that carry more than one clean title, 395 tracks by cover-only artists (`common.COVER_ARTISTS`), 1,247 tracks of songs already seen on Hooktheory, 131 tracks of McGill hold-out songs and 25 short or blank tracks; 9,549 songs, of which 5,901 are by artists with two or more. Songs with a missing column are dropped by `common.lpm` (rows for this model: **5,900** by 1,678 artists). **Halves:** md5 of the artist key mod 2 (`common.half_of`): 2,961 and 2,940 songs; 842 and 836 artists.

## Outcome
**y_foreign** exactly as `common.load_outcomes` builds it, after this file and `../common.py` are committed (its guard refuses otherwise): Discogs-VI 20240701 reduced by the maintainer's `cliques_versions.py`; a song matches the clique whose title equals its clean normalised title and whose artists include its artist (most artist sets on ties); y_foreign = 100 if some version's performer set shares no name with the artist's own sets, 0 if not or if unmatched, NaN (dropped) if matched with no own set. **Reported, deciding nothing:** y (in Discogs-VI at all).

## Model (`common.run_test`, one design for every test)
`common.design` columns: z(CH), z(A), z(ch_rep), z(ln_chg), z(V), z(ln_bars), and MSD year in five-year bins as dummies (unknown, 39.8% of songs, is its own bin; a precision control, not a first-year control). **Linear probability model within artist** (`common.lpm`: artist-demeaned, CR1 standard errors clustered by artist). The same model within each artist half. **Conditional logit** (`common.cond_logit`, grouped by artist, same columns) as a sign check. Fame (Billboard flag, hotttnesss) is **not held** in the primary: it is partly downstream of the outcome.

## Prediction
**β(CH) on y_foreign = −0.6 percentage points per SD**, within artist.

## Rules (as numbers)
- **Pass:** β < 0 and two-sided p < .00625; β < 0 in both artist halves; conditional-logit coefficient < 0. `test.py` also requires the logit to have converged (run 06's rule): a PASS with a non-converged logit is recorded UNSETTLED.
- **Kill:** **β > −0.2** (wrong sign, or weaker than −0.2; the Inventor's line, frozen in run 06). `kill=lambda b: b > -0.2`.
- **Opposite sign with p < .00625:** killed, and reported as a new hypothesis, not a pass.
- **Unsettled:** anything else, including split halves or a logit of the other sign.

## Power (fake outcomes on these rows and columns, `common.fake_power`, before any outcome)
Artist baselines Beta(0.25, 1.0) (base rate 0.20, precision 1.25, run 06's calibration), y ~ Bernoulli(baseline + β/100 · z); a pass needs p < α, the predicted sign and the same sign in both halves (the logit is not simulated). 300 draws under the prediction, 150 under zero, seed 7. Kill rates are normal approximations from the mean SE.

| True β (pp per SD) | SE (pp) | Pass rate at .00625 | at .05 | False pass if 0 (.00625 / .05) | Kill fires if true | Kill fires if 0 |
|---|---|---|---|---|---|---|
| −0.6 (the prediction) | 0.57 | **0.000** | 0.083 | 0.000 / 0.000 | 24% | 64% |

**Nearly blind.** Even if the prediction is exactly true, a pass at .00625 is a rare event; a kill is weak evidence. `run_test` prints its own power (400 draws) before the estimate; small Monte Carlo differences from this table are expected.

## Reported, deciding nothing (in `result.json`)
- β on **y**; β with **fame held** (Billboard flag, hotttnesss with a missing flag); β on **first performers only** (`common.first_performer_mask`, R02-3's rule).
- |CH| in place of CH (run 06 first principles: any lean may be how much a song turns, not which way), same columns.

## What it cannot say
- **Power** (above): a null clears nothing.
- **MIDI is not the record.** The notes are an arranger's MIDI file matched to the recording by audio; chords are half-bar triad templates.
- **y_foreign is uptake, not love.** No love measure is used (run 06 first principles: flag it in every result).
- **Within artist only; no cause.** Lakh songs lean to well-known artists; Discogs-VI coverage is uneven.

## Order the script follows (`test.py`, `common.run_test`)
guard → power (printed first) → outcome → estimate → halves → logit → readings → verdict → `result.json`.
