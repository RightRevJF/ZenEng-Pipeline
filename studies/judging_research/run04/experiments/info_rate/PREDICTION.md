# Information rate: does a song far from the habitual surprise-per-beat get versioned less? Frozen before any outcome is joined

Run 04, 24 November 2026, by the chair. **One hypothesis (R04-I3).** Nothing on the outcome side has been opened. No measure has been computed split by match status. "Chair" = notes-only checks on the rows below. **Run 04 does not touch the McGill hold-out.**

## Claim (Inventor, I3, revised in round 2)
- **The analogy:** languages are said to converge on one information rate (the Inventor's recollection of Coupé et al. 2019, not checked).
- **Extrapolation:** a song far from the habitual rate either bores or overloads, so within an artist's own songs, **a larger deviation D goes with a lower chance of being in Discogs-VI.**

## Data and rows
- **Data:** as `../move_extensive/PREDICTION.md` (surprise and rhythm files on `origin/main`, identical to the scratch copies; outcome = key set of `hooktheory_covers_discogs.json`).
- **Rows:** exactly move_extensive's rows (songs = `vid`; artist and slug from the first clip; artists with 2+ songs), less the songs with no clip in the rhythm file. Those songs are dropped after the artist rule. An artist left with one song carries no weight under the fixed effect. *Chair: 9,574 songs, 1,741 artists (14 songs have no rhythm row).*

## Measure (frozen)
- **Per clip:** r = (`n_mel`·`mel_ic_mean` + `n_ch`·`ch_ic_mean`) / `beats`, in bits per beat.
- **Clip D** = |ln r − ln 4.32|. 4.32 is fixed: it is the median of r over all 21,998 clips (chair: 4.323). A clip with `beats` ≤ 0 or r ≤ 0 has no D (chair: none).
- **Song D** = the mean of clip D over all of the song's surprise clips, weighted by `n_mel` (plain mean if the weights sum to 0). It is standardised over the rows.

## Controls
- **All of move_extensive's controls:** chord-count bin dummies with the same cuts, clips-per-song dummies, ln beats, word-count dummies, the parentheses flag and the repeated-title flag.
- **Density:** song `density`, weighted by `n_mel` over the clips that have a rhythm row with a non-null value.
- **Beats-per-bar dummies:** song bpb = the mean of `bpb` over the song's rhythm clips, weighted by `n_mel`. Dummies for bpb = 3, bpb = 6, and any other value not equal to 4 (all compared with `numpy.isclose`); 4 is the reference. *Chair: 354 / 456 / 167.*
- **Why density and beats-per-bar:** a per-beat rate depends on whether the transcriber chose half or double time (Skeptic).
- **Left out:** `ch_rep` and `ch_ic_mean` are not held (a run with them added is reported, deciding nothing). There is no first year (era only through the artist fixed effect).

## Outcome
y = 1 if the `vid` is a key of `hooktheory_covers_discogs.json`, else 0. Nothing else in that file is read.

## Gate (notes only, before the key set is read; failing it records "stopped" and no outcome is joined)
1. **Clip-to-clip:** among model songs with 2+ clips, clip D of clip 1 vs clip 2 (surprise-file order), Spearman **≥ 0.20**. *Chair: 0.279 (4,271 pairs).* Also printed: 0.290 at clip level after regressing on density, bpb and ln beats (all songs).
2. **Overlap:** |Spearman| of song D **≤ 0.7** with each of the 17 data-pack measures (`FE` of run 03), song `n_ch`, `beats`, clips per song and bpb. *Chair: largest +0.17 (`mel_ic_mean`); `ch_ic_mean` +0.07, `ch_rep` −0.03, density +0.05.*

## Model
- **Primary:** the LPM of move_extensive (y in pp; columns z(D) plus the controls; demeaned within artist; OLS with no constant; CR1 clustered by artist; normal two-sided p).
- **Conditional logit:** the same columns, with the same exact-likelihood rule and non-convergence rule. Print the artists and songs dropped.
- **Halves:** md5 artist halves as in run 03.

## Prediction
**β = −0.8 pp per SD of D** (farther from the habitual rate, less often in Discogs-VI).

## Power (notes-side; printed again from the script's own clustered SE before β)
- **Within-artist residual share of z(D) after the controls:** 0.646.
- **SE** ≤ √(0.21·0.79 / Σx̃²) = **0.52 pp**.
- **Power at −0.8 pp, p < .01 two-sided: 0.15.** Power = Φ(0.8/SE − 2.5758) + Φ(−0.8/SE − 2.5758).
- **Power floor:** below the proposed 0.5 floor (R03-4, undecided). Printed, not blocking.

## Rules
**Tonight counts five hypotheses, so p < .05/5 = .01, two-sided.** The threshold does not move if a test is stopped.
- **Pass:** β < 0, p < .01, β < 0 in both halves, and the conditional-logit coefficient < 0.
- **Opposite sign:** β > 0 and p < .01. The prediction is killed. This is reported as a new hypothesis, not a pass.
- **Kill:** β > −0.3 pp.
- **Unsettled:** anything else.

## Order the script must follow
1. Notes, then the gate (stop if it fails).
2. Only then read the key set.
3. Print N and the y = 1 count.
4. Print SE and power, then β, then the halves, then the conditional logit, then the verdict.
5. Write `result.json`.

## Reported, deciding nothing
- β with `ch_rep` and `ch_ic_mean` added.
- β of signed ln r − ln 4.32 in place of D, to show which side carries any effect.
- D built from the melody term alone and from the chord term alone.

## What it cannot say
- **Not a measured rate:** 4.32 is a Hooktheory corpus median, not a measured human rate. The rate is per beat, not per second, because there is no tempo.
- **Built from surprise:** D is built from two surprise means, so a result could come from the surprise terms, not the rate. The run with `ch_rep` and `ch_ic_mean` added is printed for that reason.
- **The outcome's limits:** the same as move_extensive. It is documented versioning, not lasting love, and a non-match is not a true negative.
- **Low power; no cause; hits only.**
- **McGill:** the hold-out is untouched.
