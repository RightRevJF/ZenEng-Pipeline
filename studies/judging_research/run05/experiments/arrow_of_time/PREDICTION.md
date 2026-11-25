# The arrow of time: do chord changes that never retrace go with uptake by other artists? Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. Idea I3 (the Inventor), which absorbed G2 (the Geometer's back-and-forth share). No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only checks on the rows below (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided (z = 2.690).** The threshold does not move if a test is stopped.

## Claim
Equilibrium runs the same forwards and backwards; a Markov chain is reversible when every move i→j is as common as j→i (detailed balance). A vamp (I–IV–I–IV) is reversible. A loop such as I–V–vi–IV only ever moves one way round, so it has a direction. **Extrapolation:** chord motion with a direction carries a listener somewhere, and within an artist's own songs such songs are more often taken up by another artist.

## Measure A (frozen)
Per clip, from the raw Hooktheory annotations (`common.raw_clips()`):
1. Take the `harmony` events sorted by `onset` (Python's stable sort). Map each to `common.chord_pcs(h)` (absolute pitch-class set; inversions ignored; sevenths and other extensions kept, so C and C7 are different chords).
2. Collapse consecutive equal sets. Call the result s₀, s₁, …, s_K. K is the number of chord changes.
3. **If K < 6 the clip has no value.**
4. n_ij = the number of t in 0..K−1 with s_t = i and s_{t+1} = j. No wrap from the last chord to the first.
5. **A = 1 − Σ_(i,j) min(n_ij, n_ji) / Σ_(i,j) n_ij**, both sums over ordered pairs (so each unordered pair enters the numerator twice).

**Song value:** the mean of the clip values over the song's clips that have one, **weighted by each clip's K** (not by `n_mel`). A song with no clip value has no A and drops out of every model of this test.

**Unit values** (one chord per beat, tonic C; the script must reproduce them before reading anything else):
| Progression | Changes | A | G2 |
|---|---|---|---|
| I–V–vi–IV ×4 | 15 | 1.0000 | 0.0000 |
| I–IV ×8 | 15 | 0.0667 | 0.9333 |
| I–V–I–IV ×4 | 15 | 0.0667 | 0.4667 |

*Chair:* 8,774 of the 9,588 songs have a value; 10th / 50th / 90th percentiles 0.333 / 0.833 / 1.000; 33% of songs score exactly 1.

## The merge with G2 (reported only)
G2 = (number of t in 0..K−2 with s_{t+2} = s_t) / K, clips with K < 6 have no value, song value weighted by K as for A. On the notes, ρ(A, G2) = −0.96 (*chair*, 8,774 songs; the Geometer and the Inventor found −0.96 and −0.94). They are one contrast. A runs because it is graded and has a theorem behind it; G2 is printed, deciding nothing, and is **not** in the model or in the overlap list of the gate.

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists with two or more songs; artist = the first clip's `artist` slug; halves `r['half']` = md5 of the artist slug mod 2 (886 / 855 artists). Songs with no A drop; artists are not re-filtered (an artist left with one song is demeaned to zero and adds nothing).

## Outcome
**Primary: y_foreign**, exactly as `common.load_outcomes()` sets it (run 04's rule, commit 4410a0e): 100 if the song's Discogs-VI group holds a non-empty performer set sharing no normalised name with the original artist's own sets, else 0 (0 for every song not in Discogs-VI). Songs with y_foreign = NaN (clique missing or no own set) are dropped from every model of this test.

## Columns
- z(A): standardised over the songs with a value (population SD). Coefficients are per SD.
- z(`ch_rep`) and z(`ch_ic_mean`): song values from `load_rows()`, standardised over the 9,588 rows.
- **ln_chg** = ln(max(total chord changes K summed over all the song's clips, 1)). The chair adds it because A is biased towards 1 when changes are few (Skeptic). *Chair:* ρ(A, ln_chg) −0.15.
- Run 04's control block, `common.controls(rows)`: chord-count bins, clips-per-song dummies (2, 3, 4+), ln beats, title flags (word-count dummies 1–4, parentheses, shared title).
- Artist fixed effect (demeaning inside `common.lpm`).

## Model
- **LPM:** `common.lpm(X, y_foreign, artist)`: demean every column and y within artist, OLS with no constant, CR1 SE clustered by artist, normal two-sided p.
- **Halves:** the same LPM within half 0 and within half 1.
- **Conditional logit (sign check):** `common.cond_logit(X, y_foreign/100, artist)` with the same columns, not demeaned. statsmodels is not installed on this machine tonight (*chair*: import fails); install it before running, or maximise the exact conditional likelihood with scipy (BFGS, then Newton) as run 04 allowed. Print the artists and songs it drops and whether it converged. If it does not converge, the test cannot pass.

## Gate (notes only; run before `load_outcomes`; failing it records "stopped" and no outcome is joined)
`common.gate(rows, "A", extra={"ln_chg": ...})`:
1. **Stability:** clip 1 vs clip 2 (load_rows order), both with a value, Spearman **≥ 0.20**. *Chair: 0.302 on 3,294 pairs.*
2. **Overlap:** |Spearman| **≤ 0.7** with each of the 17 data-pack measures, `n_ch`, `beats`, clips per song and ln_chg. *Chair: largest ch_ic_mean +0.152; ln_chg −0.154; ch_rep under 0.1.*

Chair's verdict: passes.

## Prediction
**β(A) on y_foreign = +0.6 percentage points per SD**, within artist, with the columns above.

## Rules
- **Pass:** β > 0, p < .00714, β > 0 in both artist halves, and the conditional-logit coefficient > 0 with convergence.
- **Kill:** β < +0.2 (wrong sign, or weaker than +0.2).
- **Opposite sign** (β < 0 and p < .00714): killed, and reported as a new hypothesis ("reversible vamps are what others take up"), not a pass.
- **Unsettled:** anything else, including split halves or a conditional logit that disagrees in sign.

## Power (notes side; the script prints power again from its own clustered SE before any β)
Binary-outcome bound: SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²), where x̃ is the residual of z(A) after the artist fixed effect and every other column. *Chair:* residual share 0.667 on 8,774 songs, **SE ≈ 0.54 pp; power at +0.6 and p < .00714 = 0.06** (0.20 at p < .05). Below run 03's proposed 0.5 floor, which is Jason's undecided proposal, so it is printed and does not block. The kill line decides most outcomes: it fires about 23% of the time if +0.6 is true and about 64% of the time if the true effect is zero.

## Reported, deciding nothing
- G2 in place of A (same columns), and ρ(A, G2).
- β(A) on y (in Discogs-VI at all), same columns.
- Intensive margin: among songs with y = 100, a non-null `covers` and a `first_year`, z(log(1 + covers)) on the same columns plus `first_year` (linear), artist demeaning, CR1. In SD per SD.
- y_foreign with performer sets naming "karaoke" or "tribute" (case-insensitive, any name in the set) removed before deciding whether a foreign set exists (from `r['versions']`).
- The model without ln_chg; the unweighted (plain-mean) song value of A.
- Songs and artists per half.

## Order the script must follow
1. Unit values (must reproduce). 2. Rows and A from the notes. 3. Gate; stop if it fails. 4. Notes-side power. 5. `load_outcomes` (refuses unless this file is committed). 6. Counts: N, artists, y_foreign = 100, drops. 7. Clustered SE and power at +0.6, p < .00714. 8. β, p, 95% range; halves; conditional logit; verdict. 9. Reported items. 10. `result.json`.

## What it cannot say
- y_foreign is not lasting love. It is "some performer set with no shared name released a version under the same title and writer".
- The same 9,588 songs were used in run 04 (for `ch_rep` and `ch_ic_mean` on y and y_foreign). A is new on them, but the songs are not unseen.
- Vamps are a genre habit (funk, hip-hop); within artist mostly absorbs genre, not entirely.
- Low power: a null clears nothing. Hits only; no cause. The McGill hold-out is untouched.
