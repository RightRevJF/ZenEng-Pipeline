# Fresh songs, test 1: is chord repetition taken up by other artists on songs whose outcome has never been seen? Frozen before any outcome is joined

Run 06, 26 November 2026, by the chair. Ideas R04-FV (the two-part story, unsettled in run 04: +1.00 pp per SD, p .044) and R06-L3 (the Listener's fresh-song confirmation, in the Skeptic's design). No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, nothing in `/home/claude/shape/`, no covers, versions or first years, and no fresh song has been matched to Discogs. Figures marked *chair* come from notes-only checks (`../common.py`, `../power_fake.py`; scratch in /tmp/claude-0/r6/chair).

**This file also freezes the rules shared by all five fresh tests** (`fresh_repetition`, `fresh_arrow`, `fresh_range`, `fresh_tonic`, `fresh_diatonic`): the fresh songs, the outcome, the validation step and the model. The code is `../common.py`. The outcome loaders refuse to run unless this file, the test's own PREDICTION.md and `../common.py` are committed and unmodified.

**Tonight counts six tests** (`chirality`, `fresh_repetition`, `fresh_arrow`, `fresh_range`, `fresh_tonic`, `fresh_diatonic`). **Each needs p < .05/6 = .00833, two-sided (z = 2.638).** The threshold does not move if a test is stopped.

## Claim
Run 04 found, within artists, that songs whose chords repeat more were more often released by another artist (y_foreign, +1.00 pp per SD, p .044, not enough to pass). Every one of those songs had been seen. **The claim tested tonight:** the same holds on songs whose outcome nobody has looked at. A pass confirms "taken up by others", not "loved long" (the Skeptic: loop-based styles may collect remixes under other performers' names).

## The fresh songs (notes only; `common.fresh_songs()`, `common.fresh_rows()`)
1. **Source:** the raw Hooktheory file (`Hooktheory.json.gz`, sha256 917b7cd5…e0c, checked), clips in file order.
2. **Fresh clip:** its clip id is not a data-pack clip (`hooktheory_surprise.json.gz`), its YouTube id (if any) is not a pack video, and its (artist slug, song slug) pair is not a pack pair. Grouped by (artist slug, song slug). *Chair:* **1,946 songs, 2,570 clips, 1,765 songs with a video id** (the same list as /tmp/claude-0/r6/fresh_songs.json).
3. **A fresh clip counts only if it has at least one harmony event** (every one of the pack's 21,998 clips has chords and melody). Songs with no such clip drop: 120. A song whose normalised artist and title (the maintainer's `norm`) equal a seen song's drops as a duplicate: 1. *Chair:* **1,825 fresh rows.**
4. **Per clip, the pack's own definitions:** n_mel = number of melody notes, n_ch = number of pack chord tokens, beats = `num_beats`, ch_rep = `repetition(pack chord tokens, 3)` (the pack's tokens: root relative to the first key's tonic × 9 + quality, consecutive equal tokens merged; `common.pack_tokens`, copied from /tmp/claude-0/r6/surp.py). *Chair:* on all 21,998 pack clips these reproduce the pack's ch_rep (max difference 0), n_ch, n_mel and beats exactly.
5. **Song values:** means over the song's counted clips weighted by n_mel, or the plain mean if every n_mel is 0 (as `run05 common.load_rows` does). 32 fresh songs mix clips with and without a melody; their no-melody clips get weight 0, as the rule says.
6. **Title flags** as run 04 (`toks` of the song slug: word count, parentheses); the shared-title flag is recomputed over all seen and fresh songs together.

## The rows of every fresh model (`common.battery()`)
Every song, seen (the pack's 13,198) or fresh, **by an artist with at least one fresh row and at least two rows in total.** *Chair:* **5,768 rows = 4,473 seen + 1,295 fresh, by 601 artists.** Of the fresh rows, 1,210 have a video id and 85 do not; 1,160 are by 550 artists who also have seen songs; 932 are by 238 artists with two or more fresh rows. The 530 fresh rows by artists with no other song are not used (a within-artist design needs two songs). Halves: md5 of the artist slug mod 2 (`common.half_of`).

## The outcome (built only after this file is committed)
**Discogs-VI 20240701**, reduced exactly as the maintainer's `studies/judging_checks/within_artist/cliques_versions.py` (origin/main) into `/home/claude/shape/discogs_cliques.json` (348,796 cliques, per the reduction's log) and `/home/claude/shape/discogs_versions.jsonl`. The chair did not open either file.

- **Match (the maintainer's `studies/covers/covers_match_discogs.py`):** norm(s) = lower case, "&" → "and", drop everything but a–z and 0–9. A fresh song matches a clique when norm(song slug) equals the clique's `title` and norm(artist slug) is among the clique's `artists`; among several, the one with the most artist sets (`max`, so the first in file order on ties). **Fresh songs are keyed by (artist slug, song slug)**, so the 85 without a video id can match too.
- **y** = 100 if matched, else 0.
- **y_foreign** (run 05's rule, `common.y_foreign_of`): the clique's version sets from `discogs_versions.jsonl`; own sets = those holding a name equal to norm(artist slug); y_foreign = 100 if some non-empty set shares no name with any own set, else 0; 0 if unmatched; NaN (dropped) if matched but no own set.
- **Seen rows** take y, y_foreign, versions and first year from the data pack exactly as `run05 common.load_outcomes()` does.
- **Never use `studies/judging_data/hooktheory_clips.json.gz`**: its clip set is the set of matched videos, so it is an outcome.

## Validation (must run first after commit; `common.validate_match`)
Before any fresh outcome is used, the match is rebuilt over every YouTube id in the raw file exactly as `covers_match_discogs.py` does (one entry per video, the last clip's slugs winning) and compared with the data pack:
1. keys: |pack ∩ rebuilt| / |pack ∪ rebuilt| ≥ 0.99;
2. cliques equal on ≥ 99% of the common keys;
3. for ≥ 99% of the pack's matched cliques (`discogs_versions_matched.json`), the set of normalised performer sets equals the rebuilt one;
4. y_foreign of all 13,198 seen songs, the pack's route against the rebuilt route: equal for ≥ 99%.

It writes `../match_validation.json` (with up to 50 differences of each kind, and the sha256 of both reduced files). **If any of the four fails, every fresh test stops: no fresh outcome is used, and each records "stopped (validation failed)".** The chirality test does not depend on it, except for its reported fresh reading. Printed, deciding nothing: how many pack keys are fresh songs' videos; for fresh songs with a video id, agreement between the slug-keyed match and the vid-keyed one.

## The model (all five fresh tests)
- **LPM with artist fixed effects** (`run05 common.lpm`: demeaning, no constant, CR1 by artist), on seen and fresh rows together.
- **Tested column, z_fresh = z(x) × fresh**, and beside it **z_seen = z(x) × (1 − fresh)**: the measure's slope is separate for fresh and seen rows, so **the tested slope is identified by fresh outcomes only.** z(x) = (x − mean) / SD, both over the 9,588 within-artist seen rows that have a value (run 04 and 05's per-SD scale).
- **Controls, computed identically for seen and fresh rows** (`common.battery_controls`): run 04's block (chord-count bins, clips-per-song dummies 2, 3, 4+, ln beats, word-count dummies 1–4, parentheses, shared title), **ln_chg** = ln(max(total chord changes over the song's counted clips, 1)), **V** = distinct chord pitch-class sets per clip (mean weighted by each clip's changes K; plain mean if all K are 0), **has_mel** (any counted clip with a melody), and the **fresh** main effect.
- **ch_ic_mean and mel_ic_mean are left out of every fresh model.** They are scores from the pack's corpus models (studies/surprise), trained on the seen clips, so a fresh song cannot be scored identically. Leaving them out of both seen and fresh rows keeps the columns identical.
- **Halves:** the same model within each artist half; the tested slope is z_fresh's.
- **Conditional logit** (`run05 common.cond_logit`, statsmodels 0.15 is installed): y_foreign / 100 on the same columns, not demeaned, grouped by artist. Print drops and convergence. No convergence, no pass.

## Measure (this test): ch_rep
The share of chord 3-grams heard earlier in the clip (pack tokens), as above. *Chair:* seen mean 0.2933, **SD 0.2295** (the z scale); fresh rows' mean 0.247 (more chords-only clips). Fresh clip 1 vs clip 2 agreement 0.395 on 432 pairs (reported; ch_rep is the pack's own measure and needs no gate). No extra columns.

## Prediction
**β(z_fresh) on y_foreign = +1.0 percentage points per SD of ch_rep**, within artist.

## Rules
- **Pass:** β > 0 and two-sided p < .00833; β > 0 in both artist halves; conditional-logit coefficient on z_fresh > 0 and converged.
- **Kill:** β ≤ 0 (the Listener's and the Skeptic's line for a fresh test this small). A kill says the fresh songs did not lean the predicted way; it is weak evidence (see power).
- **Opposite sign** (β < 0 and p < .00833): killed, and reported as a new hypothesis, not a pass.
- **Unsettled:** anything else, including split halves or a logit that disagrees.

## Power (from fake outcomes on these rows and columns, `../power_fake.py`, before any outcome)
Two worlds, 1,000 draws each: homogeneous (every song 22%) and calibrated (artist baselines spread so that run 05's arrow design gives the SE run 05 actually saw, 0.40 pp).

| | SE (pp) | Pass rate if +1.0 is true | Kill fires if true | Kill fires if 0 | Power at p < .05 |
|---|---|---|---|---|---|
| calibrated | 1.21 | 0.034 | 22% | 48% | 0.13 |
| homogeneous | 1.63 | 0.023 | 28% | 51% | 0.09 |

Nearly blind. The base rate of y_foreign on fresh songs is unknown (fresh clips are mostly chords-only transcriptions, perhaps of less-known songs); a lower rate lowers power further. A null clears nothing.

## Reported, deciding nothing
- z_seen's coefficient (a seen-song reading, already spent).
- β on **y** (in Discogs-VI at all), same columns.
- **W01-J6a, early and late uptake** (`common.early_late`): y_early = 100 if a foreign set's earliest year ≤ the clique's first year + 5; y_late = 100 if > first year + 10; same columns. As run 02 ruled, both are printed and nothing is decided on their contrast.
- Fresh rows whose clique is also matched by a seen song dropped (`clique_seen`); fresh rows with a video id only.
- y_foreign with performer sets naming "karaoke" or "tribute" removed (as run 05).
- The fresh-only within-artist model: fresh rows of the 238 artists with two or more fresh rows, same columns less z_seen and fresh.
- The model without has_mel; counts of fresh y = 100 and y_foreign = 100.

## Order the script must follow
1. Reproduction checks: ch_rep, n_ch, n_mel, beats on every pack clip (exact); 1,946 / 2,570 / 1,825 / 5,768 / 1,295 / 601. 2. Columns. 3. Notes-side power (bound 1.66 pp). 4. `common.validate_match` (stop if it fails). 5. `common.load_battery_outcomes`. 6. Counts: N, artists, y_foreign = 100 among fresh and seen rows, drops. 7. Clustered SE and power at +1.0, p < .00833. 8. β, p, 95% range; halves; conditional logit; verdict. 9. Reported items. 10. `result.json`.

## What it cannot say
- y_foreign is not lasting love. The match is by title and artist name; Hooktheory slugs that differ from the Discogs title (subtitles, "feat.") do not match, as for the seen songs.
- Fresh songs are those the data pack left out, mostly because their clips had no melody. They are not a random sample of songs.
- Within artist absorbs most genre, not all. Low power. Hits only; no cause. The McGill hold-out is untouched.
