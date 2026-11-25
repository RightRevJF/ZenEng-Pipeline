# Harmonic freedom: a tune with many neutral neighbours. Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. Idea I2 (the Inventor), in the revised form agreed after the Skeptic's round. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only checks (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided (z = 2.690).** The threshold does not move if a test is stopped.

## Claim
In evolution, genotypes with many neutral neighbours spread. A melody that many harmonisations fit lets a coverer re-harmonise it in their own style. **Extrapolation:** within an artist's own songs, tunes with more harmonic freedom are more often taken up by another artist.

## Measure I2 (frozen)
Per clip, from the raw annotations (`common.raw_clips()`):
1. **Melody notes:** every `melody` note with a non-null `pitch_class` and `offset > onset`, as (onset, offset, pitch_class mod 12).
2. **Spans:** each `harmony` event h, in file order, is a span [onset, offset). w[pc] = total overlap in beats, max(0, min(note offset, span offset) − max(note onset, span onset)), summed over notes of that pitch class. W = Σ w. **Skip the span if W < 0.5 beat.**
3. **Scale:** the key active at the span's onset: the last entry of `keys` with `beat ≤ onset` (the first entry if none). Scale pcs = tonic, then tonic + cumulative sums of `scale_degree_intervals`, mod 12. **Skip the span if the clip has no keys or the scale does not have exactly 7 pcs.**
4. **Diatonic triads:** T_i = {sc[i], sc[(i+2) mod 7], sc[(i+4) mod 7]} for i = 0..6.
5. **Only diatonic spans:** skip the span unless frozenset(`common.chord_pcs(h)`) equals one of the seven T_i. (So sevenths, borrowed and altered chords are skipped. There is no "+1 for a non-diatonic chord".)
6. fit(S) = Σ_{pc ∈ S} w[pc] / W. n = the number of T_i with fit(T_i) ≥ fit(written chord) − 1e−9 (the written chord counts itself, so n ≥ 1).
7. **Clip value** = Σ W·log₂(n) / Σ W over the kept spans: bits of harmonic freedom. No kept span: no value.

**Song value:** `common.song_measure` (mean over the song's clips with a value, weighted by `n_mel`). A song with no value drops out of every model of this test.

**Control pcs_span** (agreed with the Skeptic: sparse melody lets many triads fit): per clip, Σ W·(number of distinct pcs with w > 0) / Σ W over the same kept spans; song value by `song_measure`.

**Unit values** (key C major, tonic 0, intervals [2,2,1,2,2,2]; must reproduce): one beat of C over a C chord → 1.585 (C, F and A minor fit); a C–E–G melody over a C chord in one beat → 0.000 (only C fits; pcs_span 3).

*Chair:* 9,049 songs have a value; 10th / 50th / 90th percentiles 0.81 / 1.49 / 2.02 bits.

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists; halves `r['half']` (md5 of the artist slug mod 2). Songs with no I2 or no pcs_span drop; artists are not re-filtered.

## Outcome
**Primary: y_foreign** exactly as `common.load_outcomes()` sets it (run 04 rule 4410a0e). Songs with y_foreign = NaN are dropped from every model of this test.

## Columns
- z(I2), z(pcs_span): each standardised over the songs with a value (population SD).
- z(`ch_rep`), z(`ch_ic_mean`): standardised over the 9,588 rows.
- Run 04's control block, `common.controls(rows)`.
- Artist fixed effect (demeaning in `common.lpm`).

## Model
LPM via `common.lpm` (artist demeaning, CR1 by artist, normal two-sided p); the same LPM within each artist half; conditional logit via `common.cond_logit` with the same columns, not demeaned (statsmodels is not installed tonight: install it, or maximise the exact conditional likelihood with scipy as run 04 allowed; print drops and convergence; no convergence, no pass).

## Gate (notes only; before `load_outcomes`; failing records "stopped", no outcome joined)
`common.gate(rows, "I2", extra={"pcs_span": ...})`:
1. Clip 1 vs clip 2 Spearman **≥ 0.20**. *Chair: 0.267 on 3,796 pairs* (0.25 net of pcs_span, the Inventor).
2. |Spearman| **≤ 0.7** with the 17 data-pack measures, `n_ch`, `beats`, clips per song and pcs_span. *Chair: largest pcs_span −0.343; mel_ic_mean −0.255; ch_rep +0.203.*

Chair's verdict: passes.

## Prediction
**β(I2) on y_foreign = +0.6 percentage points per SD**, within artist, holding pcs_span and the columns above.

## Rules
- **Pass:** β > 0, p < .00714, β > 0 in both halves, conditional logit > 0 and converged.
- **Kill:** β < +0.2.
- **Opposite sign** (β < 0, p < .00714): killed; reported as a new hypothesis, not a pass.
- **Unsettled:** anything else.

## Power (notes side; the script prints power again from its own SE before any β)
SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²), x̃ = residual of z(I2) after the artist fixed effect and every other column. *Chair:* residual share 0.601 on 9,049 songs, **SE ≈ 0.56 pp; power at +0.6 and p < .00714 = 0.05** (0.19 at p < .05). The kill line fires about 24% of the time if +0.6 is true, 64% if zero.

## Reported, deciding nothing
- The version that keeps only spans with 3 or more distinct melody pcs (*Inventor:* clip-to-clip 0.23).
- The model without pcs_span.
- β(I2) on y; intensive margin (z(log(1 + covers)) among songs with y = 100, non-null covers and a first_year, same columns plus `first_year`); y_foreign with "karaoke"/"tribute" sets removed (as in `arrow_of_time`).
- The share of spans kept, per half.

## Order
1. Unit values. 2. Rows, I2 and pcs_span. 3. Gate; stop if it fails. 4. Notes-side power. 5. `load_outcomes`. 6. Counts. 7. Clustered SE and power. 8. β, halves, conditional logit, verdict. 9. Reported items. 10. `result.json`.

## What it cannot say
- Fit uses pitch classes and duration only, not metre or chord tones on strong beats; a passing tone counts as much as a held note.
- Only plain diatonic triads are scored; songs built on sevenths or modal mixture are scored on their remaining spans.
- y_foreign is not lasting love. The songs were used in run 04 for other measures. Low power: a null clears nothing. Hits only. The McGill hold-out is untouched.
