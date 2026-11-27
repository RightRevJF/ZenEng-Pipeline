# Repeat-and-contrast (cv_w) on songs by single-song artists. WRITTEN AFTER SEEING RESULTS; frozen before this test's outcome is joined

Run 07, 26 November 2026, by the first-principles reviewer (`../../first_principles.md`, section 5). **This rule was written after seeing all eight of tonight's results**, including the uncounted reading that suggested it: cv_w's own coefficient in the `tree_h4m` model, **+3.11 pp per SD (SE 1.10, p .0047)**. That reading was not predicted and not counted. **A pass here is a lead, never a finding.** It is the night's **9th test**.

**Threshold: p < .05/9 = .00556, two-sided (|z| > 2.77).** The eight frozen tests keep .00625; this rule changes none of their verdicts. (Run 05's precedent: `run05/experiments/arrow_singletons`.)

**What has been opened.** The reviewer read every RESULT.md and result.json of the eight tests. No outcome of these songs has been computed by anyone: `/home/claude/dl/lakh/outcomes_run07_singletons.json` does not exist, and none of these songs' keys is in the within-artist cache `outcomes_run07.json` (checked, keys only). Figures marked *reviewer* come from `notes_check.py` (notes and fake outcomes only; `notes_check.json`). The maintainer's shape study on main used 1,388 Lakh clean-MIDI songs against a different yardstick (love plus SHS covers); some of these songs may be among them, but none has been joined to y_foreign or to cv_w. The McGill hold-out and song 59 were not touched. **test.py has not been run.**

## Claim
Within artist, songs whose 4-bar stretches are *unevenly* far apart (some near-repeats, some strong contrasts: verse and chorus that differ clearly) were more often taken up by other artists, with chord repetition and tree-likeness held. The claim tested here: **the same holds across songs by different artists**, on songs no one has looked at.

The reviewer expects it to fail. It is most likely a winner's curse: the largest of many readings printed tonight, and cv_w correlates +0.55 with ch_rep, which was killed. This test is the cheapest way to kill it.

## Songs
- `test.singleton_songs()`: the songs of `common.lakh_songs()`'s own list (same exclusions, same per-song means; `all_songs()` copies it step for step and asserts that its within-artist part equals `common.lakh_songs()` exactly) whose artist has **one** song. That gives 3,648 songs; **212 that share a MIDI file with a within-artist song are dropped** (same notes as a seen song). *Reviewer:* **3,436 songs by 3,436 artists; 3,435 model rows; halves (md5 of the artist key, `common.half_of`) 1,727 and 1,708.**
- After the join, songs whose matched Discogs-VI clique is also matched by any of the 5,901 seen songs are dropped (their outcome has been seen). The count is printed; a reading keeps them.

## Measure (frozen)
`common.song_shape(...)["cv_w"]` via `common.add_shapes(S, cache=shapes_run07_singletons.json)`: the SD ÷ mean of the pairwise distances between a song's distinct sliding 4-bar chroma windows (the same call as H4m), mean over the song's files. *Reviewer:* percentiles 0.181 / 0.245 / 0.366, SD 0.086.

## Gates (notes only; split-half ≥ 0.20, |ρ| ≤ 0.7 with ch_rep, V, ln_chg, ln_bars)
*Reviewer, across songs:* split-half **0.700** (3,412 pairs), residual after each half's ch_rep, V, ln_chg, ln_bars **0.542**. Overlaps (Spearman): ch_rep **+0.609** (largest), V −0.548, ln_chg −0.023, ln_bars +0.019; H4m −0.247, g −0.417, F +0.089; hotttnesss +0.038, Billboard −0.001, year +0.051. Passes both gates. (Within artist on the seen songs the chair had 0.691 / 0.530, ch_rep +0.551.)

## Outcome
**y_foreign** exactly as `common.load_outcomes` builds it, with `common.OUT_CACHE` pointed at a new file (`outcomes_run07_singletons.json`), because the existing cache holds only the 5,901 seen songs and would give every song here y = 0. The guard refuses unless this file and `../common.py` are committed.

## Model (`test.py`)
Across songs: **OLS with an intercept, HC1 errors** (one song per artist, so HC1 equals CR1 by artist). Columns: z(cv_w), z(H4m), z(ch_rep), z(ln_chg), z(V), z(ln_bars), five-year year bins (the `tree_h4m` model, without artist demeaning). The same model in each half. **Sign check:** statsmodels `Logit` on y_foreign > 0, same columns; it must converge.

## Prediction
**β(cv_w) on y_foreign = +1.5 pp per SD**: the within-artist reading halved for selection and for the move across artists.

## Rules (as numbers)
- **Pass (a lead only):** β > 0, two-sided p < .00556, β > 0 in both halves, logit > 0 and converged.
- **Kill:** **β ≤ 0.**
- **Opposite sign with p < .00556:** killed; reported as a hypothesis, not a finding.
- **Unsettled:** anything else.

## Power (fake outcomes on these rows and columns, `test.fake_power`, 300 draws)
| True β | Base rate | SE (pp) | Pass at .00556 | at .05 |
|---|---|---|---|---|
| +1.5 (the prediction) | 0.40 | 1.24 | **0.07** | 0.23 |
| +3.1 (the within-artist reading) | 0.40 | 1.24 | 0.41 | 0.73 |
| +1.5 | 0.25 | 1.11 | 0.07 | 0.25 |
| 0 | 0.40 | 1.23 | 0.003 | 0.03 |

The base rate 0.40 is the realised rate on the seen songs; songs by single-song artists may sit lower. **Below the proposed 0.2 floor at .00556** (R06-5, Jason's call). It is run as a kill test: **the kill fires 11% of the time if +1.5 is true and 50% if the effect is zero**, a likelihood ratio of about 4.4, stronger than any kill tonight (1.5 to 3).

## Reported, deciding nothing (`result.json`)
On y; fame held (Billboard flag, hotttnesss, missing flag); style held (F, ln_tempo with a missing flag); first performers only; bare cv_w (H4m, ch_rep not held); shared cliques kept.

## What it cannot say
- **Written after seeing results.** At best a lead for a batch no one has seen.
- **Across artists, not within.** Genre and artist style are not held; run 05's arrow flipped sign across single-song artists.
- **MIDI is not the record:** an arranger's file; cv_w reads that arrangement's chroma.
- **y_foreign is uptake, not love.**
- **It spends the last unseen Lakh outcomes** (the ambiguous-file tracks aside).
