# Steps around the circle of fifths, on the extensive margin (R03-F1, with R04-G1 diatonicity merged). Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. Backlog idea R03-F1 (status testing: unsettled on covers in run 03, β −0.017, p .36), now testable on all 9,588 within-artist songs because tonight's full Hooktheory notes cover the songs not in Discogs-VI. R04-G1 (diatonicity |a₅|/a₀, parked for fresh songs) is merged in as a reported item. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only checks (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided (z = 2.690).** The threshold does not move if a test is stopped.

## Claim (run 03, unchanged in direction)
Each chord is a point on the circle of fifths (the phase of its 5th Fourier coefficient, Amiot); a song is a path, and FP is its mean step. Plainer motion round the circle, a cover can carry. **Prediction direction from run 03: smaller steps, more uptake.** On covers among versioned songs it leaned that way (unsettled). Whether another artist took the song up at all has never been looked at for FP.

## Measure FP (frozen; run 03's rules, read from the raw annotations)
Per clip (`common.raw_clips()`):
1. Tonic = `keys[0].tonic_pitch_class` (0 if the clip has no keys).
2. Harmony events sorted by `onset`. Token t = ((root_pitch_class − tonic) mod 12)·9 + qual(root_position_intervals), with run 03's table qual: (4,3)→0, (3,4)→1, (3,3)→2, (4,4)→3, (4,3,3)→4, (4,3,4)→5, (3,4,3)→6, (3,3,4)→2, (3,3,3)→2, (5,2)→7, (2,5)→7, anything else (including none) → 8.
3. Merge consecutive equal tokens into runs; each run keeps its first event.
4. Run pitch-class set, relative to the tonic: r = (root − tonic) mod 12; S = {r} ∪ {(r + cumulative sums of root_position_intervals) mod 12}.
5. Phase θ = `numpy.angle(Σ_{k∈S} exp(−2πi·5k/12))`; if the modulus < 1e−6 (augmented triad, diminished seventh, tritone) the run has no phase.
6. Moves: run i → run i+1, plus the wrap last → first when their tokens differ. Skip a move if either run has no phase.
7. Step = shortest arc |θ_x − θ_y| on the circle, in [0, π] radians.

**Song value FP** = the plain mean of the step over every kept move of all the song's clips pooled. No kept move: no value. **Clip value** (for the gate only) = the mean over that clip's kept moves.

**Unit values** (must reproduce, as in run 03): I→V, I→IV, I→vi, ii→V = π/6; I→iii, I→♭VII, I→i, IV→V = π/3; I→♭VI = 2π/3; I→♭II = 5π/6; V→vi = 0; I→ii = 0; V7 has the phase of I; augmented triad and diminished seventh have none. Worked examples (with the wrap): I–V–vi–IV has steps 0.524, 0, 1.047, 0.524, so FP = 0.524 rad; I–IV–V has 0.524, 1.047, 0.524, so FP = 0.698 rad.

*Chair:* all 9,588 songs have a value; 10th / 50th / 90th percentiles 0.449 / 0.714 / 1.197 rad.

## The merge with R04-G1 diatonicity (reported only)
D5 per clip = |Σ_x v_x e^{−2πi·5x/12}| / Σ_x v_x, where v_x = Σ (offset − onset) over harmony events whose `common.chord_pcs` contains pc x; song value by `common.song_measure` (n_mel-weighted). *Chair:* clip-to-clip 0.503, but **ρ(FP, D5) = −0.73** on the 9,588 songs (run 04 found −0.65 on the matched songs), over the 0.7 renaming line. Its author withdrew it in run 04 because its sign was set after FP leaned. So FP decides and D5 is printed in place of FP, deciding nothing. D5 is not in the model or in FP's overlap list.

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists; halves `r['half']`.

## Outcome
**Primary: y_foreign** exactly as `common.load_outcomes()` sets it (run 04 rule 4410a0e). Songs with y_foreign = NaN are dropped from every model.

## Columns
- z(FP) over the songs with a value (population SD).
- z(`ch_rep`), z(`ch_ic_mean`) over the 9,588 rows (run 03 held both: the test asks whether a fixed-space distance carries plainness beyond corpus surprise).
- Run 04's control block, `common.controls(rows)`. FP is size-free (run 03: R² 0.02 on the size block), so run 03's distinct-chord and link columns are replaced by run 04's chord-count bins.
- Artist fixed effect.

## Model
LPM via `common.lpm`; the same within each artist half; conditional logit via `common.cond_logit` with the same columns, not demeaned (install statsmodels or maximise the exact likelihood with scipy; print drops and convergence; no convergence, no pass).

## Gate (notes only; before `load_outcomes`; failing records "stopped")
`common.gate(rows, "FP", extra={"distinct_chords": ..., "links": ...})`, where distinct chords = number of distinct tokens pooled over the song's clips and links = number of distinct unordered token pairs joined by a move (wrap included), as in run 03:
1. Clip 1 vs clip 2 Spearman **≥ 0.20**. *Chair: 0.407 on 4,268 pairs.*
2. |Spearman| **≤ 0.7** with the 17 data-pack measures, `n_ch`, `beats`, clips per song, distinct chords and links. *Chair: largest ch_ic_mean +0.286; distinct chords +0.231.*

Chair's verdict: passes.

## Prediction
**β(FP) on y_foreign = −0.6 percentage points per SD** (smaller steps, more uptake by another artist), within artist.

## Rules
- **Pass:** β < 0, p < .00714, β < 0 in both halves, conditional logit < 0 and converged.
- **Kill:** β > −0.2.
- **Opposite sign** (β > 0, p < .00714): killed; reported as a new hypothesis ("bold steps are what others take up"), not a pass.
- **Unsettled:** anything else.
- A kill here would also close R03-F1 (it stays "testing" only while unsettled).

## Power (notes side; the script prints power again from its own SE before any β)
SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²). *Chair:* residual share 0.670 on 9,588 songs, **SE ≈ 0.52 pp; power at −0.6 and p < .00714 = 0.06** (0.21 at p < .05). The kill line fires about 22% of the time if −0.6 is true, 65% if zero.

## Reported, deciding nothing
- D5 in place of FP (predicted positive by its author: more diatonic, more uptake), and ρ(FP, D5).
- FP without z(`ch_ic_mean`).
- β(FP) on y; intensive margin (z(log(1 + covers)) among songs with y = 100, non-null covers and a first_year, same columns plus `first_year`); y_foreign with "karaoke"/"tribute" sets removed.
- The share of zero steps.

## Order
1. Unit values and the worked example. 2. Rows, FP, D5, distinct chords, links. 3. Gate; stop if it fails. 4. Notes-side power. 5. `load_outcomes`. 6. Counts. 7. Clustered SE and power. 8. β, halves, conditional logit, verdict. 9. Reported items. 10. `result.json`.

## What it cannot say
- f5 phase is a chord's centre on the fifths circle, not its function: I, ii and V7 share a phase, as do V and vi.
- Modulations inside a clip are not followed (tonic from `keys[0]`).
- The matched songs' FP was already tested on covers in run 03; the extensive contrast is new but the songs are not unseen. y_foreign is not lasting love. Low power. Hits only. The McGill hold-out is untouched.
