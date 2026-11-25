# Any voice can sing it: folded melody range. Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. Idea L2 (the Listener), in the revised (folded) form agreed after the Skeptic's round. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only checks (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided (z = 2.690).** The threshold does not move if a test is stopped.

## Claim
The original artist's voice is fixed; other singers take up songs an ordinary voice fits. **Extrapolation:** within an artist's own songs, a narrower melody range goes with more uptake by another artist. Melody has been null within artist on every run so far, so the prior is low.

## Measure L2 (frozen)
Per clip:
1. Notes = `common.melody_midi(a)` (onset, offset, pitch = 12·octave + pitch_class; notes with no pitch class or zero length are already dropped), sorted with Python's `sorted()` (by onset, then offset, then pitch). **Fewer than 4 notes: no value.**
2. **Fold octave errors:** q₀ = p₀. For k ≥ 1, i = p_k − p_{k−1} (raw written interval); while |i| > 12, i ← i − 12·sign(i); q_k = q_{k−1} + i. (An interval of exactly 12 is kept.)
3. Weights w_k = offset − onset. Order the q_k ascending (stable sort); cw = cumulative w / Σ w.
4. **Clip value** = q at index `searchsorted(cw, 0.95)` minus q at index `searchsorted(cw, 0.05)` (numpy, left side), in semitones.

**Song value:** `common.song_measure` (mean over clips with a value, weighted by `n_mel`).

**Unit values** (one beat per note; must reproduce): pitches 0, 4, 7, 12 → 12; pitches 0, 4, 19, 12 (the G written an octave high) → 7; a C-major scale 0, 2, 4, 5, 7, 9, 11, 12, 14, 16 → 16.

*Chair:* all 9,588 songs have a value; 10th / 50th / 90th percentiles 7 / 11 / 21 semitones. The folded and unfolded ranges agree at ρ +0.94 (the Listener).

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists; halves `r['half']`.

## Outcome
**Primary: y_foreign** exactly as `common.load_outcomes()` sets it (run 04 rule 4410a0e). Songs with y_foreign = NaN are dropped from every model.

## Columns
- z(L2) over the songs with a value (population SD).
- z(`mel_ic_mean`) (leaps widen range; agreed with the Skeptic), z(`ch_rep`), z(`ch_ic_mean`): standardised over the 9,588 rows.
- Run 04's control block, `common.controls(rows)`, which already holds ln beats (the Skeptic's length control) and the clips-per-song dummies (the section count: each Hooktheory clip is one section, and range is taken within a clip).
- Artist fixed effect.

## Model
LPM via `common.lpm`; the same within each artist half; conditional logit via `common.cond_logit` with the same columns, not demeaned (install statsmodels or maximise the exact likelihood with scipy; print drops and convergence; no convergence, no pass).

## Gate (notes only; before `load_outcomes`; failing records "stopped")
`common.gate(rows, "L2")`:
1. Clip 1 vs clip 2 Spearman **≥ 0.20**. *Chair: 0.290 on 4,271 pairs.*
2. |Spearman| **≤ 0.7** with the 17 data-pack measures, `n_ch`, `beats` and clips per song. *Chair: largest mel_ic_mean +0.555; beats +0.227.*

Chair's verdict: passes (the overlap with mel_ic_mean is the closest of tonight's measures to the 0.7 line, which is why mel_ic_mean is a column).

## Prediction
**β(L2) on y_foreign = −0.7 percentage points per SD** (narrower range, more uptake), within artist, holding mel_ic_mean and the columns above.

## Rules
- **Pass:** β < 0, p < .00714, β < 0 in both halves, conditional logit < 0 and converged.
- **Kill:** β > −0.2 (wrong sign, or weaker than −0.2).
- **Opposite sign** (β > 0, p < .00714): killed; reported as a new hypothesis ("wide-range showpieces are what others take up"), not a pass.
- **Unsettled:** anything else.

## Power (notes side; the script prints power again from its own SE before any β)
SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²). *Chair:* residual share 0.748 on 9,588 songs, **SE ≈ 0.49 pp; power at −0.7 and p < .00714 = 0.10** (0.30 at p < .05). The kill line fires about 15% of the time if −0.7 is true, 66% if zero.

## Reported, deciding nothing
- The unfolded range in place of L2.
- The model without mel_ic_mean.
- β(L2) on y; intensive margin (z(log(1 + covers)) among songs with y = 100, non-null covers and a first_year, same columns plus `first_year`; the Listener predicted −0.02 SD per SD); y_foreign with "karaoke"/"tribute" sets removed.

## Order
1. Unit values. 2. Rows and L2. 3. Gate; stop if it fails. 4. Notes-side power. 5. `load_outcomes`. 6. Counts. 7. Clustered SE and power. 8. β, halves, conditional logit, verdict. 9. Reported items. 10. `result.json`.

## What it cannot say
- Hooktheory's octave field is the transcriber's choice; folding removes jumps over an octave, not a whole clip written an octave off (which does not change the range).
- A clip is one section, so a song whose verse and chorus sit in different registers is scored per section, not across the song.
- y_foreign is not lasting love; the songs were used in run 04. Low power. Hits only. The McGill hold-out is untouched.
