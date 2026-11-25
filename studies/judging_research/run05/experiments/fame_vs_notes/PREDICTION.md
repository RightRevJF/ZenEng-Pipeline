# Fame against the notes: does uptake by other artists follow the artist, not the song? Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. The Skeptic's test, motivated by card 2 (Interiano et al. 2018, the counter-evidence paper: success is predicted far better by a superstar flag than by song features). The Skeptic's three parts and several pass/kill clauses are cleaned up here into **one rule**; the other parts are reported, deciding nothing. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Power below comes from synthetic outcomes on the real predictors (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided.** Here that level is applied as a (1 − .00714) artist-bootstrap interval. The threshold does not move if a test is stopped.

## What this tests, and why it is different
Every other test tonight compares songs **within** an artist, so the artist's fame is removed by design. This one compares **across** artists on purpose. It partly tests the yardstick and the project's premise: if "taken up by another artist" (y_foreign) is predicted across artists by crude fame proxies and not at all by the notes, then the outcome records mainly who the artist is, and any notes effect must live in small within-artist differences. If the notes add prediction beyond fame, the outcome carries something about songs that fame proxies miss.

## Claim (the Skeptic's)
Across artists, fame proxies predict y_foreign better than the notes do, and the notes add almost nothing once fame is known.

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists. Songs with y_foreign = NaN are dropped.

## Outcome
**y_foreign** exactly as `common.load_outcomes()` sets it (run 04 rule 4410a0e), as 0/1 (y_foreign / 100).

## Predictor blocks (all on hand; no outside data)
- **(a) Fame:** ln(the artist's number of songs among all 13,198 songs of the surprise file, i.e. `load_rows()["allsongs"]` counted by `artist`), and ln(clips per song). Both are popularity traces on Hooktheory: users transcribe more songs, and more sections, of artists and songs they care about.
- **(b) Notes:** the 17 data-pack measures (`common.FE`), song values from `load_rows()`. *Chair:* 14 songs have no rhythm row (NaN in the 9 rhythm measures).
- **(c) Both:** (a) and (b) together.

## Model (frozen)
- **Folds:** fold = `int(hashlib.md5(artist.encode()).hexdigest(), 16) % 5`, so every artist's songs sit in one fold. *Chair: 2,069 / 2,072 / 1,739 / 1,772 / 1,936 songs.*
- For each fold k: standardise every predictor with the mean and population SD of the other four folds; after standardising, set NaN to 0 (the training mean); fit `sklearn.linear_model.LogisticRegression(C=1.0, max_iter=5000)` (sklearn 1.9.1 defaults otherwise: L2, lbfgs, intercept) on the other four folds; predict probabilities for fold k.
- **AUC** = `sklearn.metrics.roc_auc_score` over all songs' out-of-fold predictions pooled, for each block: AUC(a), AUC(b), AUC(c).
- **D = AUC(a) − AUC(b)** (fame against notes) and **Δ = AUC(c) − AUC(a)** (what the notes add to fame).
- **Interval:** artist bootstrap on the fixed out-of-fold predictions (no refitting). G = number of artists; `rng = numpy.random.default_rng(0)`; 2,000 times draw `rng.integers(0, G, G)`, take all songs of each drawn artist (with repeats), recompute D and Δ. The interval is the 0.357th to 99.643th percentile (level 1 − .05/7).

## The rule
- **Pass (the Skeptic's claim holds):** the lower end of D's interval is above 0 **and** Δ < 0.01.
- **Kill (the notes carry what fame does not):** Δ ≥ 0.01 with the lower end of Δ's interval above 0, **or** D ≤ 0 (the notes predict at least as well as fame).
- **Unsettled:** anything else.
The two outcomes cannot both hold.

## Prediction (the Skeptic's)
AUC(a) about 0.62 or more, AUC(b) 0.56 or less, so D about +0.06; Δ below 0.01.

## Power (synthetic outcomes on the real predictors; no outcome read)
Synthetic y from a logistic model on the real fame and notes columns, with an artist random intercept (SD 1 on the logit scale), base rate 0.19 to 0.23. Bootstrap SEs: about 0.02 for D and 0.005 for Δ.
- A fame-only world (AUC(a) 0.58 to 0.64, notes add nothing): **pass 6 of 6**.
- Notes add about 0.045 AUC: **kill 6 of 6**.
- Notes add about 0.01 AUC (the boundary): pass 4, kill 1, unsettled 3 of 8.
So the rule decides at the extremes and is honestly unsettled at the boundary.

## Reported, deciding nothing
- AUC(a), AUC(b), AUC(c) with 95% artist-bootstrap intervals; log-loss of each; D and Δ within each artist half (`r['half']`).
- The same rule run on y (in Discogs-VI at all).
- **Within artist (the Skeptic's part 2):** LPM with artist demeaning on y_foreign (points), columns z of the 17 measures plus run 04's block (`common.controls`). Partial R² of the clips-per-song dummies (song-level fame) and of the 17-measure block, each = (RSS without the block − RSS full) / RSS without the block. The Skeptic predicted fame's at least 5 times the notes'.
- **Interaction (part 3):** run 04's model (z `ch_rep`, z `ch_ic_mean`, run 04's block, artist demeaning, CR1) plus z(`ch_rep`) × z(ln artist songs), z over the 9,588 rows (the main effect of ln artist songs is absorbed by the artist effect). Also `ch_rep`'s slope in the same model among songs of artists at or below the artist-level median of ln artist songs. The Skeptic predicted the interaction > 0 (the loop lead carried by prolific artists, so it behaves like familiarity).
- **Placebo:** the 17 notes columns permuted within artist (`numpy.random.default_rng(s)`, s = 0..199), Δ recomputed each time; the mean and 95th percentile. This shows how much of any Δ is artist-level notes (style, genre, era) rather than song-level.

## Order
1. Rows and predictor blocks from the notes. 2. Folds and their sizes. 3. `load_outcomes` (refuses unless this file is committed). 4. Counts: N, artists, y_foreign = 1, drops. 5. Out-of-fold predictions, AUCs, D and Δ with intervals; verdict. 6. Reported items. 7. `result.json`.

## What it cannot say
- **Not a test of within-artist effects.** A pass does not touch tonight's other six tests or run 04's findings; it says only that, across artists, this outcome is mostly fame.
- **Fame proxies are Hooktheory traces,** not chart or streaming data; they also carry genre and era (who Hooktheory users transcribe).
- **Notes across artists also carry genre and era.** A kill could mean "the notes carry style, and style predicts uptake", not "good songs are taken up".
- y_foreign is not lasting love. The songs were used in run 04. Hits only. The McGill hold-out is untouched.
