# iiv_dres08: the ii-V share holding resolved dominants (R09-L2's lead). SEEN SONGS: A LEAD, NOT IN K

Run 09, 27 November 2026. Frozen by the chair before this file's outcome fields are read. **Status: LEAD ON SEEN SONGS.** Run 08's
songs, whose outcomes were opened in run 08 (iiv_chunk +0.073 within composer; iiv_singletons +0.057); written after those results,
so never in K. Passes nothing, kills nothing.

## Songs
Run 08's 8,640 songs (`data/choco_songs_discogs_run08.json`, fields `clique` and `charts` only before the guard); the 8,565 with IIV,
DRES and the five columns.

## Measures (song value = unweighted mean over all its run 08 charts, run 08's rule; every run 08 chart is bar-timed)
- IIV as run 08.
- **DRES** (R09-L2, copied into `measures09.py`): resolved d7 tokens (bits 4 and 10, not 3, whose next change token's root is a
  fifth down or a semitone down) per bar, bars = ⌊last onset⌋ − ⌊first onset⌋ + 1.
- Controls: w_chr, ch_rep, V, ln_chg, ln_bars.

## Outcome and model
After `common09.guard(this folder)`: n_artist_sets, first_year, composer key and the run 08 `within` flag are read from the run 08 data
file. y_cov standardised over these songs. Plain OLS HC1 on z(IIV), z(DRES), the five controls, genre dummies (run 08's rule from the
charts) and decade dummies. Halves by `common09.halves(composer key)`. Second model: `posthoc08.poisson_plain`.

## Predictions (the Listener's, frozen)
- **b_IIV | DRES = +0.035** ("with DRES held, IIV should fall to half or less" of run 08's +0.07).
- **b_DRES | IIV = +0.04**.
- Frozen labels: "the ii carries it (writer's-signature reading)" if b_IIV | DRES ≥ +0.06 while DRES's 95% range covers 0;
  "the resolution carries it" if b_DRES > 0 with p < .05 and b_IIV | DRES ≤ half of b_IIV without DRES on the same songs;
  otherwise "neither rule met".

## Power at .05 (printed before the outcome; informational)
b_IIV at +0.035: 0.807 (N 8,565, fake SE 0.013). b_DRES at +0.04: 0.877 (fake SE 0.014). Seen songs give the power that unseen ones
cannot; that is why this lead is worth a slot, and also why it cannot count.

## Readings (deciding nothing)
1. IIV alone, same songs and columns (needed by the label rule).
2. DRES alone, same songs and columns.
3. IIV holding TR (the ii-collapsed resolution share) in place of DRES.
4. Within composer, run 08's iiv_chunk model (`common.ols_fe`, CR1 by composer; songs whose composer has 2+ songs): b_IIV and b_DRES.

## What it cannot say
ρ(IIV, DRES) is about 0.5, so the two coefficients share their information; chart writers may add resolutions as well as ii's.
