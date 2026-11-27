# Run 09: the chair's picks

27 November 2026, the 10:17 ET pass. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus
covers by other artists. The outcome is y_cov, the standardised log of 1 + the number of distinct artist sets that recorded the song
(Discogs-VI). Jason's rule applies: every idea that can be tested on the data at hand is tested this pass, within the orchestrator's
cap of eight tests.

**No outcome was opened.** I read nothing in `/home/claude/shape/` or `/home/claude/dl/discogs/`, no covers, versions or HOLDOUT file,
and no outcome field of `data/*.json`. From `data/choco_songs_discogs_run08.json` I read only the `clique` and `charts` fields (in
`measures09.py`), and the list of field names once, to write the seen-song test.py files; no value other than clique and chart ids was
read. I did not call `common09.load_outcomes` or run 08's `common.load_outcomes`. Everything below comes from the notes
(`experiments/measures09.py`), from the design (`common09.load_design()`: clique ids, composer key, genre, chart ids, match, provenance;
no counts or years) and from fake outcomes (`experiments/power_run09.py`). Song 59, songs/p69 and studies/holdout59 were not read. The
imaginers' scripts in `/home/claude/scripts/` were read and their recipes copied into `measures09.py`.

## What changed tonight
- **New songs, never joined to an outcome: 1,283** (common09's design; 1,271 with a measurable chart). 985 are matched by a unique
  title alone and 298 by title plus a name, so nearly all comparisons are ACROSS composers (925 composer keys; 482 songs share a key,
  'traditional' alone holds 89).
- **Charts from outside the iReal community.** Real Book and BiaB files (Band-in-a-Box), and 191 songs known only from a transcription
  of one recording. This is the first pass that can read a song's harmony from a writer other than the iReal players whose recordings
  make the outcome (the obstacle of run 08), though "outside iReal" is not "before covering" (see below).
- **Small N, low power.** The iiv_singletons model on 1,271 songs has a fake SE of 0.032 per SD; typical predictions are 0.01 to 0.05.
  Only one test clears the power floor. Everything else is an estimate or a seen-song lead.
- **A timebase rule.** Recordings are timed in seconds, so bar-based measures (ln_bars, DRES, CARC) are missing on them. In the models
  a song with no bar-timed chart gets the mean ln_bars and an indicator column `no_bars` = 1 (`harness09.py`). This is the only change
  to run 08's frozen iiv_singletons model, and it is stated in each PREDICTION.md.
- **The measures are in one place.** `experiments/measures09.py` writes `/home/claude/dl/choco/measures_run09.json` (outside the repo;
  sha256 begins a67802bb1db04112; deterministic: two runs gave the same file) and `experiments/measure_gates.json`. It measures
  31,515 charts (every chart of `common09.load_charts()`, needed for TYP's reference), the 1,283 design songs, and the run 08 songs for
  the two seen-song leads.

## Tonight's tests: eight folders

**One is counted: K = 1, α = .05 (two-sided).** Five are estimates on unseen songs (frozen and committed; they pass nothing and kill
nothing). Two are leads on seen songs (re-spending run 08's outcomes; never in K).

A counted test **passes** when p < α, the sign is the predicted one, both composer halves (`common09.halves` of the design's composer
key) have that sign, and the second model (`posthoc08.poisson_plain` on n_sets, same columns) has it too. It is **killed** only if its
prediction lies outside the estimate's 95% range; otherwise it is **unsettled**.

| # | Folder | Idea | Measure | Prediction | Songs | Power at .05 | Status |
|---|---|---|---|---|---|---|---|
| 1 | `iiv_confirm09/` | run 08 first principles §5: the ii-V share on unseen songs (with L1's counted form and the frozen non-jazz reading as readings) | IIV | **+0.05** | 1,271 | **0.367** | **counted** |
| 2 | `tr_resolve/` | G09-2 merged with R09-L2: dominants that resolve, on the ii-collapsed path (voice-leading geometry; quotient by ii insertion) | TR (DRES per bar second) | +0.035 | 1,270 | 0.193 | estimate (under the floor) |
| 3 | `tq_tension/` | G09-1, card 1: lead-lag area = ½ quadratic variation of the tritone channel | TQ, holding IIV | +0.01 | 1,271 | 0.037 | estimate |
| 4 | `irr_skeleton/` | R09-I1, card 1: the tree-reduced walk (signature uniqueness up to tree-like paths) | IRR | +0.02 | 1,271 | 0.067 | estimate (withdrawn from count) |
| 5 | `vr4c_momentum/` | R09-I2 revised, card 1: variance ratio of the fifths root walk, ii dropped | VR4c, holding IIV | +0.02 | 1,245 | 0.120 | estimate (withdrawn from count) |
| 6 | `typ_typical/` | R09-I3 revised, card 1: distance from the coarse genre's expected Lévy areas | TYP | −0.02 | 1,271 | 0.067 | estimate (withdrawn from count) |
| 7 | `gap_writer08/` | R09-L1's lead: IIV read upstream and the iReal gap, together, holding log(iReal charts) | IIV_up, GAP | song story b_up +0.045, b_gap 0; writer story b_up ≤ +0.01, b_gap ≥ +0.03 | 1,181 seen | b_up 0.207; b_gap 0.117 | **lead, seen songs** |
| 8 | `iiv_dres08/` | R09-L2's lead: IIV holding DRES | IIV and DRES | b_IIV +0.035, b_DRES +0.04 | 8,565 seen | 0.807 / 0.877 | **lead, seen songs** |

How power was computed:
- `harness09.fake_power` (posthoc08.fake_power_ols style): y = β·z(measure) + N(0, 1 − β²) on the real rows, plain OLS HC1 with the
  frozen columns and genre dummies (no decade dummies: first_year comes with the outcome), 300 draws, seed 11. All numbers are in
  `experiments/power_run09.json`, which also gives the share of draws where the range kill fires if the prediction is true (3 to 6%)
  and if the effect is zero (5 to 35%).
- With 300 draws the Monte Carlo error on a power near 0.2 to 0.35 is about ±0.023 to ±0.028.
- Every test.py prints its power again before any outcome is joined.

The mathematics this pass: every unseen estimate except the confirmation is grounded in card 1 (lead-lag theorem: TQ, VR4c;
tree-like uniqueness: IRR; level-2 Lévy areas and the expected signature: TYP) or in voice-leading geometry (TR's ii-collapse is
a quotient that a ii insertion cannot move; unit-tested in `measures09.unit_tests()`). None of them reached the floor, so the counted
test is not a mathematical one. I would not inflate a prediction to change that, and neither would the Geometer.

### How K was set (the K rule)
Run 08's rule, applied again: K is the largest number for which at least K candidate tests clear 0.2 at .05/K; then take the top K
by the ranking.

| Power at .05/K | K = 1 | K = 2 | K = 3 |
|---|---|---|---|
| iiv_confirm09 (IIV, +0.05) | **0.367** | 0.277 | 0.240 |
| tr_resolve (TR, +0.035) | 0.193 | 0.127 | 0.097 |
| reading: IIV non-jazz (+0.04) | 0.190 | 0.113 | 0.090 |
| reading: DRES per bar (+0.035) | 0.160 | 0.097 | 0.053 |
| vr4c_momentum (+0.02) | 0.120 | 0.063 | 0.047 |
| TE (+0.02; waits) | 0.120 | 0.077 | 0.057 |
| reading: IIV on RB/BiaB charts (+0.035) | 0.113 | 0.063 | 0.040 |
| CARC (+0.02; waits) | 0.110 | 0.050 | 0.037 |
| irr_skeleton (+0.02) | 0.067 | 0.037 | 0.027 |
| typ_typical (−0.02) | 0.067 | 0.030 | 0.027 |
| tq_tension (+0.01) | 0.037 | 0.033 | 0.023 |
| tests at or above 0.2 | **1** | 1 | 1 |

- **K = 1** is consistent: at .05 exactly one test (the confirmation) clears the floor, and at K = 2 still only one does.
- **TR misses the floor by 0.007**, inside the Monte Carlo error. The 300-draw rule was frozen before its number was seen (as in run
  08), and I did not re-draw. TR is therefore an estimate; the Skeptic's condition ("counted only if power ≥ 0.2 at .05/2") would have
  needed 0.2 at .025, where it has 0.127, so it fails under either reading.
- **The non-jazz reading misses at 0.19.** Run 08 froze it to "count only at power 0.2", so it stays an estimate inside
  `iiv_confirm09`.
- The seen-song leads have high power (0.81 and 0.88 for iiv_dres08) but are never in K: they were written after run 08's results on the same songs.

## Rulings applied
- **Power floor (R06-5):** a test counts only at fake-outcome power ≥ 0.2 at .05/K on the real design. Under it, an estimate.
- **Run 08's "power 0.5" condition is relaxed, stated plainly.** Run 08 wrote that its confirmation should run only at power 0.5 or more.
  Its power here is 0.367. I count it under the ruling floor of 0.2, because 0.5 was run 08's recommendation and the floor is the
  maintainer's ruling. A non-pass at 0.367 will be weak evidence; a pass or a range kill would say something.
- **Range kill (R07-3).** For the confirmation the kill fires in 4% of draws if +0.05 is true and in 35% if the effect is zero.
- **The maintainer's correction (run 08):** the two seen-song leads were written after seeing run 08's results and are not in K.
- **Withdrawals are respected (run 07):** the Inventor withdrew I1 to I3 from the count; the Geometer froze TQ and TE as estimates;
  the Listener froze CARC as an estimate.
- **Halves (frozen here, for every test):** `common09.halves(composer key)`, where the key is the design's: the name-matched person
  key, else nrm(the clique's first Discogs-VI writer), else 'solo:<clique>'. This is the Skeptic's "writer string, else performer"
  in the form the design stores. (The design never needs the performer fallback: every song has a writer key or a person key.)
  For the seen leads the key is run 08's composer key, read after the guard.
- **Controls:** the iiv_singletons columns (w_chr, ch_rep, V, ln_chg, ln_bars) plus `no_bars` (the timebase rule), partition-based genre
  dummies, first-year decade dummies. Plain OLS HC1, as iiv_singletons; CR1 SEs clustered by composer key are reported beside each
  estimate, deciding nothing.

## Merges
- **G09-2 TR with R09-L2 DRES** (the Skeptic; both authors agreed). TR is primary; DRES per bar is the second reading. On this
  design ρ(TR, DRES) = 0.87 (pooled), 0.83 within genre.
- **R09-L1's counted form into the confirmation** (the Skeptic). IIV read from Real Book and BiaB charts only is a frozen reading
  of `iiv_confirm09` at +0.035 (power 0.113). Its seen-song form is `gap_writer08`.
- **The non-jazz reading** stays where run 08 froze it, inside the confirmation (+0.04; labelled "jazz repertoire" if its range
  excludes +0.04).
- Folding these two readings into the confirmation's folder keeps them frozen, powered and reported without using up two of the
  eight slots. They are estimates exactly as they would be in folders of their own.

## The measure gates (written before any outcome)
A measure is stopped if its song-level Spearman with ch_rep or with V exceeds 0.8 in absolute value (pooled over the 1,283 songs, or
within genre), or if its two-chart stability is under 0.5 on 100 or more pairs (run 08's second gate). Stability is the Spearman
between the first two non-identical charts (sorted ids) of a design song: 317 pairs, 190 of them a BiaB internet file against a Real
Book file of the same title. These two collections overlap heavily (the Inventor found 294 run 09 title pairs with identical change
tokens), so stability runs high. The stricter column needs the change tokens to differ too. Full table: `experiments/measure_gates.json`.

| Measure | Songs | Two-chart (n) | Tokens differ | ρ ch_rep | ρ V | ρ IIV | ρ TR | Cross-writer (imaginers) | Gate |
|---|---|---|---|---|---|---|---|---|---|
| IIV | 1,271 | 0.824 (317) | 0.867 | −0.28 | +0.50 | 1 | +0.50 | 0.64 | passes |
| TR | 1,270 | 0.896 (317) | 0.866 | −0.27 | +0.26 | +0.50 | 1 | 0.60 to 0.63 | passes |
| DRES | 1,097 | 0.882 (283) | 0.850 | −0.22 | +0.44 | +0.48 | +0.87 | 0.68 to 0.72 | passes |
| TQ | 1,271 | 0.874 (317) | 0.840 | −0.29 | +0.36 | +0.55 | +0.76 | 0.50 | passes |
| IRR | 1,271 | 0.877 (317) | 0.831 | −0.29 | +0.53 | +0.35 | +0.19 | (resid. 0.72 on recordings) | passes |
| VR4c | 1,245 | 0.848 (308) | 0.810 | −0.35 | +0.58 | +0.35 | +0.30 | (VR4 0.62 on recordings) | passes |
| TYP | 1,271 | 0.692 (317) | 0.654 | −0.17 | +0.58 (0.62 within genre) | +0.31 | +0.09 | weak | passes |
| CARC | 773 | 0.783 (218) | 0.750 | −0.05 | +0.03 | −0.05 | −0.06 | 0.35 | passes (waits) |
| TE | 1,271 | 0.748 (317) | 0.699 | −0.06 | −0.01 | +0.15 | +0.14 | 0.28 | passes (waits) |

The ρ columns are pooled song-level values; the within-genre values (in the JSON) are close to them, and the largest is TYP with
V (0.62). Every measure passes. The weak spot is the one run 08 found: two chart writers agree only 0.28 to 0.72 (the imaginers'
cross-writer column, iReal against Real Book or BiaB on shared titles), so every effect is diluted.

## Ranking
Ten qualified; eight run tonight.
1. `iiv_confirm09`: the frozen confirmation of run 08's one standing lead, on songs no session has seen; the only test with power.
2. `tr_resolve`: the obstacle's direct probe on unseen songs. A ii insertion cannot move TR, so a TR effect cannot be a chart writer's
   added ii's; geometry (voice-leading quotient). Power 0.193.
3. `gap_writer08` (seen lead): the obstacle asked straight: does the upstream reading or the iReal excess carry the ii-V's effect?
4. `iiv_dres08` (seen lead): does the ii, or the resolution, carry it? Power 0.81 / 0.88 on seen songs.
5. `vr4c_momentum`: card 1 lead-lag; held against IIV.
6. `tq_tension`: card 1 lead-lag; held against IIV (largely dominant density).
7. `irr_skeleton`: card 1 tree-like uniqueness; A-B-A repetition renamed in part.
8. `typ_typical`: card 1 expected signature; ρ 0.58 with V.
9. *(waits)* R09-L3 CARC, the cadence arch: power 0.11 at .05; cross-writer agreement 0.35; its author ranked it low.
10. *(waits)* G09-3 TE, the tension engine: power 0.12; cross-writer agreement 0.28; its author called it low priority.

The Skeptic ranked the estimates IIV on RB/BiaB, non-jazz, TQ, IRR, VR4c, TYP, CARC, TE. I kept that order for what runs and what
waits, and placed the two seen leads above the weaker unseen estimates because they bear on the obstacle and have the power to say
something.

## What waits for the next pass, and why
- **CARC** and **TE.** Both pass the gates and their frozen recipes and values are already in `measures09.py` and
  `measures_run09.json`. They wait because the pass is capped at eight and they are the two lowest-ranked ideas: each reads the
  chart writer as much as the song (cross-writer 0.35 and 0.28, under the 0.5 the Geometer and the Skeptic used), and each has power
  near 0.11 here.
- **The cost, stated plainly:** once tonight's outcomes are opened, these 1,283 songs are seen. CARC and TE then need another unseen
  batch. If the orchestrator would rather spend the slots on them, swap them for the two seen-song leads (which can run in any later
  pass, because their songs are already seen); the folders would need writing in the same form as `irr_skeleton`.
- **The next unseen batch.** Tonight's confirmation is the last fresh chance for the ii-V on this design, at power 0.37. ChoCo has
  no further usable partition (Billboard and Chordify are the McGill hold-out's source), so more power needs a new source of charts
  for songs no session has joined to an outcome.

## Left out, and why
- **Withdrawn by its author:** the Geometer's signature shape vector (SIG) for shape heritability: across chart writers its median
  retrieval rank is 32%, worse than a four-number size vector (9%).
- **Card 1's other areas (M1 pitch-set fifths-plane area, M3 arch, M5 root-quality lead-lag, TE wrapped, TE ii-collapsed):** cross-writer
  agreement 0.29 to 0.36 (the Geometer's table B). Not proposed for testing by anyone.
- **The Listener's FA / FAc (the tree-like lemma on roots):** withdrawn before proposing; ρ 0.985 with chirality, a rename of the
  killed R06-I1. Kept as a diagnostic only.
- **FUL** (share of dominants that resolve): R09-L2's round-1 second reading, superseded by the merge (TR primary, DRES second). It is
  computed in `measures09.py` but not tested.
- **TYPM, VR4 uncollapsed, TQ without IIV, DRES:** run as frozen readings inside their folders, not as tests.
- **JSIR (card 2):** 44 standards; its recordings were chosen for prominence and canonical changes, which is selection on the outcome,
  and its lead sheets are a consensus of those recordings. No test.

## What a reader should keep in mind
- **"Upstream" mostly is not.** The Real Book was compiled from canonical recordings; Weimar and JAAH transcribe jazz covers; BiaB files
  are user-made. A pass on Real Book or BiaB charts means "outside iReal", not "before covering". Only about 110 pop transcriptions read
  an original recording, and their IIV is near 0.
- **Genre is the partition.** Pop has almost no ii-Vs (Isophonics 92% zero), so jazz, Real Book and BiaB carry the slopes.
- **Title-only matches (985 of 1,283)** can attach the wrong song and pull every estimate toward 0. The name-matched subset (297) is
  reported in `iiv_confirm09`.
- **Across composers.** A famous writer's tune is compared with an obscure one's; fame is not held. Some composer keys group many
  songs ('traditional' 89), so CR1-by-composer SEs are reported beside the HC1 ones.
- **The confirmation's power is 0.37.** A non-pass will most likely be "unsettled"; that would not be evidence against the ii-V.

## Practical notes for the experimenters
- **Commit and push first, without running anything.** The guard refuses an outcome until the folder's PREDICTION.md and
  `common09.py` are committed, unmodified and pushed to origin/judging-research. Commit:
  - this file (`run09/chair.md`);
  - `run09/experiments/measures09.py`, `harness09.py`, `power_run09.py`, `measure_gates.json`, `power_run09.json`, and `common09.py`
    (with `parse09.py` and `jsir_iiv_check.py` if the orchestrator keeps them);
  - the eight folders, each with `PREDICTION.md` and `test.py`;
  - not `__pycache__/`.
- **Check the measures table.** If `/home/claude/dl/choco/measures_run09.json` is missing or its sha256 does not begin a67802bb1db04112,
  rerun `python3 -I measures09.py` (about 2 minutes, 7 GB machine fine).
- **Then run each test once:** `cd run09/experiments/<folder> && python3 -I test.py`. Each prints power first, then the estimate, then
  writes `result.json`. Order: `iiv_confirm09` first (the counted test), then `tr_resolve`, `tq_tension`, `irr_skeleton`,
  `vr4c_momentum`, `typ_typical`, then the seen leads `gap_writer08` and `iiv_dres08`.
- **Runtime:** in the synthetic run each unseen test took 1 to 2 seconds, plus the time to read `$SHAPE/discogs_cliques.json` once
  per test; `gap_writer08` about 2 seconds; `iiv_dres08` about 10 seconds (the clustered SEs on 8,565 songs). The whole set should run
  in a few minutes on 2 cores.
- **No test.py has been run on a real outcome.** Every test.py was exercised once on synthetic outcomes (common09.load_outcomes,
  common09.guard and harness09.load_seen_outcomes replaced by random generators in a scratch script outside the repo); the synthetic
  result.json files were deleted.
- **`ideas.json` was not touched** (the orchestrator updates it): testing G09-2 (+L2 merged; estimate), the confirmation (counted);
  estimates G09-1, R09-I1, R09-I2, R09-I3; leads R09-L1 (gap_writer08), R09-L2 (iiv_dres08); waits R09-L3 and G09-3; withdrawn SIG.

## Data and credit
- **The notes:** ChoCo, the Chord Corpus (de Berardinis, Meroño-Peñuela, Poltronieri & Presutti 2023; Zenodo 7706751; CC BY 4.0): its
  iReal Pro and Band-in-a-Box charts are user contributions; Wikifonia lead sheets were CC-licensed; Isophonics, uspop2002, the rock
  corpus, Robbie Williams, JAAH and the Weimar Jazz Database annotations are credited as in ChoCo.
- **The outcome, joined only after the commit:** Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024; CC BY-SA 4.0).
- **Cards:** Chevyrev & Kormilitzin, "A Primer on the Signature Method in Machine Learning" (arXiv:1603.03788); Lee & Jeong, "JSIR"
  (arXiv:2610.15356; annotations CC BY-SA 4.0).
