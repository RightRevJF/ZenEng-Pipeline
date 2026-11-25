# The certified loop margin M: a chord cycle a cover cannot break. Frozen before any outcome is joined

Run 05, 25 November 2026, by the chair. Ideas G1 (the Geometer), L1 (the Listener) and I1 (the Inventor), merged: all three are card 1's TopPT margin on chord chroma, normalised the same way. This is tonight's main mathematical test. No outcome has been opened by the chair or by any brainstorm agent: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, no covers or first-year field, not the McGill hold-out. Figures marked *chair* come from notes-only runs over every clip of the rows below (scratch scripts in /tmp/chair, not in the repo).

**Tonight counts seven tests** (`loop_margin`, `arrow_of_time`, `harmonic_freedom`, `melody_range`, `fifths_path`, `tonic_resistance`, `fame_vs_notes`). **Each needs p < .05/7 = .00714, two-sided (z = 2.690).** The threshold does not move if a test is stopped.

## Claim
Card 1 (Park, An, Kim & Kim, TopPT), Theorem 4.3 and Corollary 4.4: the sliding-window cloud of a periodic signal is an embedded circle whose H1 bar, born at 0, has persistence at least a ∝ √(m+1)·ε, where ε says how distinct the cycle's stations are. The subsampling radius c bounds the bottleneck error (Theorem 5.1), and the stability theorem says a perturbation smaller than half the margin keeps the circle. **Extrapolation (all three imaginers):** a cover is such a perturbation; a song whose chord loop has a large certified margin survives re-dressing, and others take it up. Exact passes beyond the first return add nothing to M, while `ch_rep` keeps rising, so M is the take-up face of looping without its repetition penalty.

## Measure M (frozen; every setting below is fixed)
Per clip, from `common.raw_clips()`:
1. **Grid:** h = ½ beat. T = ceil(num_beats / h − 1e−9) samples. X is T × 12, zeros. For each `harmony` event, set X[i, p] = 1 for every p in `common.chord_pcs(h)` and every i from max(floor(onset/h + 1e−9), 0) to min(ceil(offset/h − 1e−9), T) − 1. If X is all zero, the clip has no value.
2. **Smooth:** Xs = `scipy.ndimage.gaussian_filter1d(X, sigma=2, axis=0, mode="nearest")` (σ = 1 beat).
3. **Scale:** s = √(m+1) × √(mean over t of ‖Xs_t − mean_t Xs‖²) = 3 × the RMS spread of Xs (m = 8). If s < 1e−9, no value.
4. **Periods:** bars of `meters[0].beats_per_bar` beats (4 if missing or 0). For P_bars in (2, 4): P = P_bars × beats_per_bar / h samples; **skip this P if 2P > T.** (P = 8 bars is excluded: it would tie M to clip length.)
5. **Embedding:** m = 8, τ = P/9, span = 8τ. Anchors = `numpy.arange(0, T − 1 − span + 1e−9, 0.5)` (every ¼ beat). If there are more than 300, keep `anchors[numpy.round(numpy.linspace(0, len−1, 300)).astype(int)]`. **n_pre** = the number of anchors kept (after the cap, before deduplication). Each anchor t gives the 108-vector [Xs(t + kτ) for k = 0..8], each channel read by `numpy.interp` on the grid 0..T−1, ordered k-major (k = 0's 12 channels, then k = 1's, …).
6. **Deduplicate:** `numpy.unique(numpy.round(points, 6), axis=0)`; n = rows left. **If n < 10, skip this P.**
7. **Radius:** D = Euclidean distance matrix. b = min(ceil(0.99n), n − 1). A fresh `numpy.random.default_rng(0)` for each (clip, P). B = **200** times: keep = `rng.choice(n, b, replace=False)`; h_j = the largest, over points not kept, of the distance to the nearest kept point. c = 2 × `numpy.quantile(h, 0.95)`.
8. **Persistence:** `ripser(D, distance_matrix=True, maxdim=1, coeff=11)["dgms"][1] / 2` (ripser 0.6.15; full Rips, no threshold; radius scale). Drop bars with infinite death.
9. **Margin at P** = max(0, max over H1 bars with birth ≤ c of (death − birth − 2c)) / s.
10. **Clip M** = the largest margin over the computed P. No computed P: no value.

**Song value:** `common.song_measure` (mean over clips with a value, weighted by `n_mel`). **ln_anchors** (control) = `song_measure` of ln(n_pre at P = 2 bars) over the clips where P = 2 bars was computed. **cert** (reported) = `song_measure` of 1 if the clip's M > 0, else 0.

**Compute:** `multiprocessing.Pool(2)`, `imap_unordered(..., chunksize=25)` over the 16,563 clips. *Chair: 1,058 s (17.6 min) on this machine's 2 cores, no errors.*

**Unit values** (one chord per 4/4 bar, 16 bars, tonic C; must reproduce to 1e−6 before anything else): I–V–vi–IV ×4 → M = 0.242192 (n_pre 226, n after deduplication 96); I–IV ×8 → M = 0.015590 (a back-and-forth is nearly a segment, not a circle); 16 bars of I → no value (s = 0).

*Chair:* 9,576 songs have M (44 clips of 16,563 give none); 48% of songs score 0; 41% of clips certify a loop; 10th / 50th / 75th / 90th percentiles 0 / 0.006 / 0.124 / 0.242. Share of songs with M > 0 by `ch_rep` tercile: 36% / 65% / 54% (the inverted U the Skeptic flagged; hence ch_rep²).

## Songs
Run 04's rows from `common.load_rows()`: 9,588 songs by 1,741 artists; halves `r['half']`. Songs with no M drop; artists are not re-filtered.

## Outcome
**Primary: y_foreign** exactly as `common.load_outcomes()` sets it (run 04 rule 4410a0e). Songs with y_foreign = NaN are dropped from every model.

## Columns
- z(M) over the songs with a value (population SD).
- z(`ch_rep`), **z(`ch_rep`)²** (the square of the standardised value), z(`ch_ic_mean`): standardised over the 9,588 rows.
- **ln_anchors, counted before deduplication** (the chair's ruling on the Geometer–Listener split). The radius c shrinks as the cloud grows, so the anchor count is held. Counting after deduplication would partly hold M itself, because an exact loop loses its repeated windows in deduplication (*chair:* ρ(M, ln anchors before) +0.25, after +0.12). The after-deduplication count is reported as a sensitivity. Both counts are taken at P = 2 bars, which every clip with a value has.
- Run 04's control block, `common.controls(rows)` (holds ln beats).
- Artist fixed effect.

## Model
LPM via `common.lpm`; the same within each artist half; conditional logit via `common.cond_logit` with the same columns, not demeaned (statsmodels is not installed tonight: install it, or maximise the exact conditional likelihood with scipy as run 04 allowed; print drops and convergence; no convergence, no pass).

## Gate (notes only; before `load_outcomes`; failing records "stopped")
`common.gate(rows, "M", extra={"ch_rep_sq": ..., "ln_anchors": ...})`:
1. Clip 1 vs clip 2 Spearman **≥ 0.20**. *Chair: 0.369 on 4,247 pairs* (the Geometer: 0.17 after residualising on ch_rep, n_ch and beats; the gate uses the raw value, as every test tonight).
2. |Spearman| **≤ 0.7** with the 17 data-pack measures, `n_ch`, `beats`, clips per song, ch_rep² and ln_anchors. *Chair: largest n_ch −0.254; beats +0.249; ln_anchors +0.247; ch_rep² −0.224; ch_rep under 0.19.*

Chair's verdict: passes. Also printed, deciding nothing: ρ(M, A) = +0.19 (`arrow_of_time`).

## Prediction
**β(M) on y_foreign = +0.8 percentage points per SD**, within artist, holding ch_rep, ch_rep², ch_ic_mean, ln_anchors and run 04's block.

## Rules
- **Pass:** β > 0, p < .00714, β > 0 in both halves, conditional logit > 0 and converged.
- **Kill:** β < +0.3 (wrong sign, or weaker than +0.3).
- **Opposite sign** (β < 0, p < .00714): killed; reported as a new hypothesis, not a pass.
- **Unsettled:** anything else.

## Power (notes side; the script prints power again from its own clustered SE before any β)
SE ≤ √(0.22 × 0.78) × 100 / √(Σ x̃²), x̃ = residual of z(M) after the artist fixed effect and every other column. *Chair:* residual share 0.459 on 9,576 songs (M shares variance with ch_rep, its square and the anchor count), **SE ≈ 0.63 pp; power at +0.8 and p < .00714 = 0.08** (0.25 at p < .05). The kill line fires about 21% of the time if +0.8 is true and 68% if zero.

## Reported, deciding nothing
- cert (the certified flag) in place of M (49% of songs score 0, so the flag is the natural split).
- ln_anchors counted after deduplication in place of before; the model without ch_rep².
- y_foreign with performer sets naming "karaoke" or "tribute" (case-insensitive, any name in the set) removed before deciding whether a foreign set exists, from `r['versions']` (the Skeptic's fame risk: loops may draw cover factories).
- β(M) on y.
- Intensive margin: among songs with y = 100, a non-null `covers` and a `first_year`, z(log(1 + covers)) on the same columns plus `first_year` (linear), artist demeaning, CR1, in SD per SD. **The imaginers predict ≥ 0 there, unlike ch_rep's −0.042.**

## Order
1. Unit values (must reproduce). 2. Rows and M over every clip (Pool(2)). 3. Gate; stop if it fails. 4. Notes-side power. 5. `load_outcomes` (refuses unless this file is committed). 6. Counts: N, artists, y_foreign = 100, drops. 7. Clustered SE and power at +0.8, p < .00714. 8. β, p, 95% range; halves; conditional logit; verdict. 9. Reported items. 10. `result.json`, with per-clip M cached outside the repo if wanted.

## What it cannot say
- Card 1's theory is for a smooth scalar signal; chord chroma is a 12-dim step function, smoothed. The guarantee is qualitative on these data, and the paper has no music application.
- B = 200 and b = 0.99n are the paper's practical calibration, not the regime of its theorem.
- M is one clip's loop, not the song's; clips are the sections users transcribed.
- y_foreign is not lasting love. The songs were used in run 04 (for ch_rep and ch_ic_mean). Low power: a null clears nothing. Hits only. The McGill hold-out is untouched.
