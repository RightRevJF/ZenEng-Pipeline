# Chords that move, and plain chords, on a new outcome: is the song in Discogs-VI at all? Frozen before any outcome is joined

Run 04, 24 November 2026, by the chair. **Two hypotheses are counted here** (R04-L1 and R02-chordsurprise). Nothing on the outcome side has been opened: not `hooktheory_covers_discogs.json`, `discogs_versions_matched.json`, `/home/claude/scratch/covers.json` or any McGill cover file. No measure has been computed split by whether a song is matched. Figures marked "chair" come from notes-only checks on the rows below. **Run 04 does not touch the McGill hold-out.**

## Claims
- **H1 (R04-L1; J1 on a new outcome).** A musician records a song they can learn fast and not tire of. Within an artist's own songs, **more within-section chord repetition (`ch_rep`) goes with a lower chance that the song was versioned at all**, i.e. that it is in a Discogs-VI clique.
- **H2 (R02-chordsurprise, its first rule-first test).** In the same model, **higher chord surprise (`ch_ic_mean`) goes with a lower chance of being in Discogs-VI.** This was found on cover counts (−0.042, not pre-stated). The contrast between in and not in Discogs-VI has never been looked at, so this is its first fresh test. H2 is counted as its own hypothesis because it is untested and the outcome is new.

## Data (read only)
`studies/judging_data/` on `origin/main`: `hooktheory_surprise.json.gz` and `hooktheory_rhythm.json.gz` (the rhythm file is used only for the gate's overlap list). The copies in `/home/claude/scratch/` are byte-identical (md5 ff7b9d37… and 1d6e0405…; chair). The outcome is the **key set** of `hooktheory_covers_discogs.json`, and nothing else in that file is read.

## Rows
- **Clips:** every record of the surprise file, in file order.
- **A song** is a `vid`. Its clips are all surprise records with that `vid`.
- **Artist** = the `artist` slug of the song's first clip. **Slug** = the `song` slug of the song's first clip.
- **Keep** every song whose artist has 2 or more songs. *Chair: 9,588 songs, 1,741 artists, out of 13,198 songs and 5,351 artists.*
- **Song value of any surprise-file field** = mean over the song's clips weighted by `n_mel`, as the data-pack README says. If the weights sum to 0, use the plain mean. *Chair: no such song.*
- **Artist halves:** `int(hashlib.md5(artist.encode()).hexdigest(), 16) % 2`, fixed on the full rows. *Chair: 886 and 855 artists.*

## Measures (tested)
- `ch_rep` and `ch_ic_mean`: song values as above, each standardised (z, population SD) over the 9,588 rows. Coefficients are per SD.

## Controls (fixed now)
1. **Chord count:** song `n_ch`, binned by `numpy.digitize(n_ch, [5, 7, 9, 11, 13, 16, 20, 25, 32])` into 10 bins. Dummies for bins 1–9; bin 0 (`n_ch` < 5) is the reference. *Chair bin counts: 341, 672, 1,553, 1,160, 1,174, 1,429, 1,597, 811, 464, 387.*
2. **Clips per song:** dummies for 2, 3 and 4+; 1 is the reference. *Chair: 5,317 / 2,533 / 1,123 / 615.*
3. **Length:** ln(song `beats`).
4. **Title genericness** (from the slug only):
   - u = `urllib.parse.unquote(slug).lower()`; b = `re.sub(r"\([^)]*\)", " ", u)`; tokens = `[t for t in re.split(r"[^a-z0-9]+", b) if t]`, or the same split of u if that list is empty.
   - Word-count dummies for 1, 2, 3 and 4 tokens; 5+ is the reference. The 1-token dummy is the one-word flag. *Chair: 1,931 / 2,454 / 1,907 / 1,396 / 1,900.*
   - Parentheses flag: "(" in u. *Chair: 109.*
   - Repeated-title flag: `"-".join(tokens)` is shared by songs of at least two distinct artist slugs among all 13,198 songs of the surprise file. *Chair: 960.*
- **No first year.** Unmatched songs have none, so era enters only through the artist fixed effect. Drift across a career is not held.

## Outcome
y = 1 if the song's `vid` is a key of `hooktheory_covers_discogs.json`, else 0. The script prints the number of y = 1 rows and the number of keys that are not among the 13,198 surprise songs (diagnostic only).

## Gate (notes only, run before the key set is read; failing it records "stopped" and no outcome is joined)
These are existing data-pack measures, so the gate checks stability and that the two do not collapse into each other or into another of the covers study's measures.
1. **Clip-to-clip:** among model songs with 2+ clips, clip 1 vs clip 2 (surprise-file order), Spearman **≥ 0.20** for each of `ch_rep` and `ch_ic_mean`. *Chair: 0.324 and 0.496 (4,271 pairs).*
2. **Overlap:** |Spearman| **≤ 0.7** between each tested measure and every other column of this model, the other 16 of run 03's 17 data-pack measures (the `FE` list; rhythm fields weighted by `n_mel` over the clips that have a rhythm row), song `n_ch`, `beats` and clips per song. *Chair: `ch_rep` largest −0.44 (`ch_h_mean`); `ch_ic_mean` largest +0.48 (`ch_h_mean`); the two together −0.33.*
   Printed, deciding nothing: `ch_ic_mean` against `ch_ic_sd` +0.78. That field is outside the 17 and outside the model, and it is the spread of the same surprise values.

## Model
- **Primary: a linear probability model (LPM).** y is in percentage points (0 or 100). The columns are z(`ch_rep`), z(`ch_ic_mean`) and every control above. Demean every column and y within artist; fit OLS with no constant.
- **SE:** CR1 clustered by artist, G/(G−1) · (N−1)/(N−K) · (X′X)⁻¹ Σ_g X_g′u_g u_g′X_g (X′X)⁻¹, where K counts the demeaned columns. P-values are normal and two-sided. statsmodels' `cov_type="cluster"` with `df_correction=True` gives the same result. statsmodels is not installed on this machine, so code CR1 directly.
- **All artists with 2+ songs stay in**, including those with no song in Discogs-VI. In an LPM such artists are not weightless (Skeptic). This was decided before the join.
- **Conditional logit (sign check).** Use the same columns, not demeaned, grouped by artist, with the exact conditional likelihood. Use statsmodels `ConditionalLogit` if it is installed. Otherwise maximise the same likelihood with scipy (BFGS, then Newton if needed), computing each artist's denominator by the standard recursion over subsets with that artist's number of y = 1. Artists whose songs are all 0 or all 1 drop out. **Print how many artists and songs it drops.** If the optimiser does not converge, print that, and neither hypothesis can pass.
- **Halves:** the same LPM within each artist half.

## Predictions
- **H1:** β(`ch_rep`) = **−1.0 pp per SD** of P(in Discogs-VI).
- **H2:** β(`ch_ic_mean`) = **−1.0 pp per SD**.

## Power (notes-side; printed again by the script, from its own clustered SE, before any β)
SE ≤ √(0.21·0.79 / Σx̃²), where x̃ is the residual of the standardised measure after the artist fixed effect and every other column. The outcome variance 0.21·0.79 is an upper bound. Clustering could raise the SE.

| Hypothesis | Within-artist residual share of x | SE | Power at prediction, p < .01 | (at p < .05) |
|---|---|---|---|---|
| H1 `ch_rep` | 0.412 | 0.65 pp | **0.15** | 0.34 |
| H2 `ch_ic_mean` | 0.530 | 0.57 pp | **0.20** | 0.42 |

Power = Φ(1.0/SE − 2.5758) + Φ(−1.0/SE − 2.5758). Both are below run 03's proposed 0.5 floor (R03-4). That floor is Jason's undecided proposal, so it is printed here and does not block the test.

## Rules
**Tonight counts five hypotheses (two here, `info_rate`, `plr_share`, `thirds_axis`), so each needs p < .05/5 = .01, two-sided.** The threshold does not move if any test is stopped.
For each of H1 and H2 separately:
- **Pass:** β < 0, p < .01, β < 0 in both artist halves, and the conditional-logit coefficient < 0.
- **Opposite sign:** β > 0 and p < .01. The prediction is killed. This is reported as a new hypothesis, not a pass.
- **Kill:** β > −0.3 pp (wrong sign, or weaker than −0.3 pp).
- **Unsettled:** anything else, including split halves or a conditional logit that disagrees in sign.
- **What a kill means:** a kill of H2 kills "plainly" (chord surprise as its own claim), not J1. A kill of H1 says chords that move do not predict being versioned at all. It leaves the within-artist cover-count result (−0.042) as it stands.

## Order the script must follow
1. Build the rows and measures from the notes.
2. Run the gate, and stop if it fails.
3. Only then read the key set of `hooktheory_covers_discogs.json`.
4. Print N, the artists and the y = 1 count.
5. Print the SE and power for both hypotheses.
6. Print β, p and the 95% range; then the halves; then the conditional logit with its drop counts; then the verdicts.
7. Write `result.json`.

## Reported, deciding nothing
- Each term with the other left out.
- The model without the title flags.
- log(clips) entered linearly in place of the clip dummies.
- The LPM on the conditional-logit sample (artists with at least one y = 1 and one y = 0).
- The share of y = 1 by clips-per-song class.
- Songs and artists per half.

## What it cannot say
- **What the outcome measures:** documented re-release by two performer sets under the same normalised title and a shared writer (card 2). That is not lasting love.
- **False non-matches:** non-matches mix "never covered" with missing writer credits, retitles and failed matches. Noise unrelated to the notes only attenuates the effect, so a pass is conservative and a null is weak.
- **Noise that tracks the notes:** compilation "versions" of singles (held only partly by clips per song) and translated covers of international hits can create an effect. False versions from featured artists or remixes favour loops (high `ch_rep`), so an H1 pass survives that one.
- **Era:** not held beyond the artist fixed effect.
- **Low power:** a null clears nothing.
- **No cause:** hits only.
- **McGill:** the hold-out is untouched.
