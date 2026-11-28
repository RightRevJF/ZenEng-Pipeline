# windows_lakh_after: chord repetition and LATE covers, on Lakh songs (run 12, AFTER SEEING RESULTS)

Written 28 November 2026, about 11:45 ET, by the orchestrator, **after** the eight frozen tests' results (folder results written 11:20-11:40 ET; none yet committed) and **before** any Lakh song is joined to cover timing. Label: **after seeing results**. A pass here is a lead that needs songs not yet used; it is never a finding.

## Why
The Hooktheory WINDOWS estimate (an uncounted estimate, power 0.06) gave, for chord repetition (ch_rep): β early (covers at ages 0-3) +0.06 (SE 0.07), β late (ages 8+) −0.18 (SE 0.05), Δ = β_L − β_E = −0.24 with analytic SE 0.072 (p .0007). Its frozen bootstrap failed (NaN replicates), so its frozen range flag is void. If the chord finding ("chords that move go with covers") lives in the late window, it is about lasting, not launch: the yardstick's "longevity" half. This tests that on other songs.

## Songs
Run 07's within-artist Lakh songs (notes side `lakh_notes_side.json`; near-duplicate MIDI files counted once, `common12.lakh_rows()`), with a Discogs-VI clique, an own set, t0 ≤ 2005, and artists with 2+ such songs. **Seen**: joined in run 07 to y_foreign and eight chord measures including ch_rep, and in run 11 to the bass coupling; **never joined to cover timing or windows**.

## Measure (frozen)
ch_rep = run 07's MIDI chord repetition (share of chord 3-grams heard earlier in the file), as carried in the notes-side list. Reading: REP_L (skyline pitch-class entropy, this pass's cache).

## Outcome
Covers by fitness.py's rule (a version whose performer set shares no normalised name with the song's own artist sets), from Discogs-VI 20240701 main.zip streamed by cliques_versions.py's reduction (per artist set, the earliest track year); t0 = the clique's earliest year; N_E = covers at ages 0-3; N_L = covers at ages 8+; exposures from the frozen fit's g and h (common12.exposure). Code: `test.py` in this folder.

## Model
Per window, FE Poisson (artist groups; conditional likelihood; cluster sandwich) of N_w on z(ch_rep), z of the Lakh controls (ln_chg, V, ln_bars, LNEV, NPB, ACT, NFILES) and five-year t0 dummies, offset log exposure. Δ = β_L − β_E with the analytic joint sandwich SE. Halves: md5(artist) mod 2.

## Prediction
**Δ = −0.12** (Hooktheory's −0.24 halved for the winner's curse): chord repetition goes with fewer LATE covers more than with fewer early ones.

## Rules
- Counts toward this pass's total: **K = 4, α = .05/4 = 0.0125** (the three counted tests do not change verdict: none had p under .0125 or .0167).
- **Pass (a lead):** Δ < 0, p < 0.0125, both halves Δ < 0.
- **Killed:** −0.12 lies outside Δ ± 1.96 SE.
- **Unsettled:** otherwise.
- Power, before the join, from the Hooktheory analytic SE scaled to about 2,000 songs (my approximation; no fake run): SE ≈ 0.060, power ≈ 0.31 at α .0125 (0.21 at the unscaled SE). Under R06-5 the floor is met only on the scaled figure; if the real SE exceeds 0.072 this is an estimate and passes nothing.
- Readings (decide nothing): REP_L windows; ch_rep on t0 ≥ 1970.

Credit: Lakh MIDI / LPD (CC BY 4.0); Discogs-VI 20240701 (CC BY-SA 4.0).
