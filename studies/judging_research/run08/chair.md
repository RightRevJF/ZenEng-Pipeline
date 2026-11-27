# Run 08: the chair's picks

27 November 2026, the 02:17 ET pass. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. Tonight's outcome is y_cov, the standardised log of 1 + the number of distinct artist sets that recorded the song (Discogs-VI). Jason's rule applies: every idea that can be tested on the data at hand is tested this pass.

**No outcome was opened.** I did not read anything in `/home/claude/shape/` or `/home/claude/dl/discogs/`, or any covers, versions or HOLDOUT file. I did not call `common.load_outcomes` or `common.load_timelines`; every test that does is guarded. Everything below comes from the notes (`experiments/measures.py`), from the design file (clique ids, composer, genre, chart ids, no counts or years) and from fake outcomes (`experiments/power_run08.py`). The imaginers' scripts in `/home/claude/scripts/` were read and the code used was copied into `measures.py`. Song 59, songs/p69 and studies/holdout59 were not read. The McGill hold-out is excluded from the design and untouched.

## What changed tonight
- **New songs, never joined to an outcome.** ChoCo's iReal Pro and Wikifonia chord charts, matched to Discogs-VI cliques by title plus a writer's name. That gives **5,907 songs by 1,199 composers**, each composer with two or more songs. Songs already seen (Hooktheory, the fresh set, Lakh) are excluded.
- **Within composer.** Each composer's tunes are compared with each other, with genre held inside composer.
- **A count, not yes/no.** y_cov has more information per song than run 07's "taken up at all", where 98% of matched songs were already counted as taken up.
- **Bigger samples bring power.** Run 07's tests had power 0.00 to 0.02. Tonight's counted tests run from 0.21 to 0.65.
- **Two rulings now apply.** The 0.2 power floor (R06-5, ruled by the maintainer) and the range kill (R07-3, agreed by the maintainer; Jason may overrule). Neither is new tonight.
- **The measures are written down in one place.** `experiments/measures.py` holds every measure, copied from the imaginers' scripts. Its output is `/home/claude/dl/choco/measures_run08.json`, outside the repo; sha256 begins 04becd8c1d9f2870, and the script is deterministic.
  - 13,500 of the design's 13,599 charts are measured; 5,858 songs have at least one measured chart.
  - Each song's value is the plain mean over its charts. The number of charts is never a control.

## Tonight's tests: eight folders

Five are **counted**: they share **α = .05/5 = .01** (two-sided). Three are **estimates**: they are frozen and committed, but they pass nothing and kill nothing.

A counted test **passes** when four things hold:
1. p < .01;
2. the predicted sign;
3. the same sign in both composer halves (`common.halves`);
4. the same sign in a second model.

The second model is a Poisson pseudo-likelihood on the count of artist sets, with composer effects and the same columns (`models08.poisson_fe`). The timeline and heritability tests have their own second models.

A counted test is **killed** only if its prediction lies outside the estimate's 95% range. Anything else is **unsettled**.

| # | Folder | Idea | Measure | Prediction | Songs | Power at .01 (composer share 0.3 / 0.5) | Status |
|---|---|---|---|---|---|---|---|
| 1 | `chrep_confirm/` | **W01-J1**: the one seen pass, on fresh songs | ch_rep (chord repetition) | **−0.04** SD per SD | 5,858 | 0.487 / 0.687 | **counted** |
| 2 | `key_travel/` | R08-L1 + R08-I1, card 1: **the pass's mathematics** | TRAV5 (circular W1 on the fifths circle between 4-bar windows), holding TRAVL1 and size | **+0.05** | 5,829 | 0.213 / 0.323 | **counted** |
| 3 | `heritability/` | R08-I2, card 2: do chord-space neighbours by other composers share cover luck? | excess ρ_nb over a within-cell permutation null | **+0.06** | 5,852 | 0.65 (pseudo-decade cells) / 0.81 without decade | **counted** |
| 4 | `cover_timeline/` | R08-L2 + R08-G3, card 2: momentum or fitness? | Poisson slope β of late sets (L, years 10 to 29) on log(K10 + 1) | **β = 1.10** (neutral = 1) | about half the design | 0.25 (middle scale; 0.17 low, 0.305 high) | **counted** |
| 5 | `iiv_chunk/` | R08-L3: the ii-V chunk | IIV share of changes | **+0.04** | 5,858 | 0.387 / 0.553 | **counted** |
| 6 | `transport_economy/` | R08-G1, card 1 | econ = 1 − w̄/b | +0.03 | 5,858 | 0.223 / 0.323 | estimate (counted set full) |
| 7 | `tonic_resistance/` | R03-I2, now with written keys | H | −0.03 | 5,700 | 0.277 / 0.453 | estimate (counted set full) |
| 8 | `transposed_rep/` | R08-G2 | T = O − L | +0.05 | 5,858 | 0.790 / 0.940 | estimate (withdrawn from the count by its author) |

How power was computed:
- **y_cov tests:** `common.fake_power` on the real rows and frozen columns, 300 draws (`power_final_a.json`, `power_final_b.json`).
- **The composer share is an assumption.** The share of y_cov's variance that belongs to the composer is unknown before the outcome. Power is computed at 0.3, with 0.5 as a sensitivity check.
- **`cover_timeline` and `heritability`** have their own fake-outcome simulations (`power_other.json`, `power_herit_decade.json`). Their assumptions are written in their PREDICTION.md files.
- **Every test.py prints power again** before any outcome is loaded.

At least one counted test is mathematical: `key_travel` is card 1's circular optimal transport. Its closed form (W1 on the circle = Σ|D − median D|) is checked against card 1's table by `measures.unit_tests()`.

### How K was set (the K rule)
The brief asks for K = the number of counted tests, counting only tests with power of 0.2 or more at .05/K, recomputed until it is consistent. Tonight no single K is consistent:

| Power at .05/K (share 0.3) | K = 4 | K = 5 | K = 6 | K = 7 |
|---|---|---|---|---|
| chrep_confirm | 0.537 | 0.487 | 0.467 | 0.447 |
| heritability (pseudo-decade) | 0.68 | 0.65 | 0.59 | 0.58 |
| iiv_chunk | 0.397 | 0.387 | 0.377 | 0.350 |
| tonic_resistance | 0.320 | 0.277 | 0.257 | 0.240 |
| cover_timeline (middle) | 0.265 | 0.25 | 0.23 | 0.21 |
| transport_economy | 0.247 | 0.223 | 0.190 | 0.187 |
| key_travel | 0.237 | 0.213 | 0.190 | 0.167 |
| tests at or above 0.2 | 7 | 7 | 5 | 5 |

- **Why no K is consistent.** At K = 5, seven tests clear the floor. Counting all seven would mean K = 7, and at K = 7 only five clear it.
- **The rule I froze.** K is the largest number for which at least K tests clear 0.2 at .05/K. That is **K = 5**.
- **Which five.** The five are taken in the ranking order below: chrep_confirm, key_travel, heritability, cover_timeline, iiv_chunk.
- **The two left over.** transport_economy and tonic_resistance also clear the floor at .01. They are frozen as estimates because the counted set is full. Each folder says so, and each prints its reading against .01.
- **The cost.** Ranking by value rather than by power keeps a card-1 mathematics test in the count (key_travel, 0.213) and leaves tonic_resistance (0.277) out.
- **The margin is thin.** key_travel's and transport_economy's powers sit near the floor. With 300 draws, each carries a Monte Carlo error of about ±0.024.
- **The composer-share assumption decides some of this.** At a composer share of 0.5, more tests would clear the floor and K would be larger. The status was set at 0.3 and does not move.
- **Jason may overrule this rule.**

### Rulings applied
- **Power floor (R06-5, ruled by the maintainer, in the data pack README):** a test counts only if its power, reckoned before the outcome on fake outcomes on the real design, is 0.2 or more. Below the floor it is an estimate.
- **Range kill (R07-3, agreed by the maintainer; Jason may overrule):** a counted test is killed only when its prediction lies outside the estimate's 95% range. How often each kill fires is in each PREDICTION.md:
  - when the effect is zero, 44% to 75% for the y_cov tests and about 100% for heritability;
  - when the prediction is true, 2% to 4% for the y_cov tests, 6% to 10% for cover_timeline, and 11% to 61% for heritability. The decade cells shrink heritability's excess, so its kill is weak evidence; its PREDICTION.md says so.
- **Halves and a second model:** as above.
- **Withdrawals are respected (run 07).** "Estimate only" from an author is respected as a withdrawal from the count, not from the test.

## Merges
- **R08-L1 with R08-I1** (the Skeptic: within-composer ρ 0.76 here). TRAV5 is counted; E is its frozen second reading, at a prediction of +0.08.
- **R08-G3 with R08-L2.** One timeline test. G3's γ for the notes measures (TRAV5, econ, T, IIV, ch_rep) is reported beside it and decides nothing.

## The measure gates (written before any outcome)
A measure is stopped if:
- its two-chart stability is under 0.5; or
- its within-composer |ρ| with ch_rep or with V is over 0.8 (renamed).

Stability is the Spearman correlation between the first two **non-identical** charts of a design song (2,466 songs). Cross-source agreement (iReal against Wikifonia, 1,128 songs) is reported beside it and is not a gate. The full table, with residual stability and all within-composer overlaps, is in `experiments/measure_gates.json`.

| Measure | Two-chart | Residual on size | iReal vs Wikifonia | ρ ch_rep | ρ V | Gate |
|---|---|---|---|---|---|---|
| ch_rep | 0.597 | | 0.311 | | −0.149 | passes |
| TRAV5 | 0.738 | 0.619 | 0.515 | −0.285 | +0.208 | passes |
| E | 0.806 | 0.732 | 0.667 | −0.229 | +0.282 | passes |
| econ | 0.624 | 0.622 | 0.406 | −0.062 | +0.122 | passes |
| T_rep | 0.645 | 0.621 | 0.418 | −0.178 | +0.246 | passes |
| IIV | 0.772 | 0.708 | 0.584 | −0.021 | +0.217 | passes |
| H (tonic resistance) | 0.651 | 0.646 | 0.376 | −0.042 | −0.082 | passes |
| p_min (obtuse statue) | 0.628 | 0.521 | 0.394 | +0.086 | −0.598 | passes |
| lnP (loop period) | 0.672 | 0.673 | 0.465 | −0.003 | +0.011 | passes |
| B (burstiness) | 0.706 | 0.644 | 0.546 | −0.019 | +0.376 | passes |

- **Every proposal passed.** The weak spot is cross-source agreement: two different chart writers agree only 0.31 to 0.67. ch_rep is the worst at 0.31.
- **One identity was found.** The Geometer's L (literal 3-gram repetition) is exactly ch_rep on the change sequence (ρ 1.00). The T test therefore holds ch_rep as L.

## Ranking
Eleven qualified; eight run tonight.
1. `chrep_confirm`: the only idea that ever passed on seen songs (−0.042, p .009), now on fresh songs, at power 0.49. It runs W01-J1's own model (composer, genre, era; no size columns). The size-held version is reported, because chart length moves ch_rep (ρ +0.59).
2. `key_travel`: card 1's mathematics; the merged idea of two imaginers; geometry first, as Jason asks.
3. `heritability`: card 2's question asked of the notes without choosing a measure; strong power.
4. `cover_timeline`: card 2's direct test, with the urn ceiling, which tells how much room any content has.
5. `iiv_chunk`: music cognition; clean gates.
6. `transport_economy` (estimate): card 1's second reading.
7. `tonic_resistance` (estimate): newly testable because ChoCo has written keys. Ranked low because runs 05 to 07 recommended retiring it.
8. `transposed_rep` (estimate): withdrawn from the count by its author, but the most powerful reading tonight (0.79), so it runs as an estimate.
9. *(waits)* R03-G3 p_min, the obtuse statue: gate passes; power 0.033 at .01 for its −0.02.
10. *(waits)* R07-L2 loop period: power 0.040. Its +0.6 pp on y_foreign was translated to +0.012 SD by the outcome's SD, an assumption.
11. *(waits)* R07-I3 burstiness: power 0.007, at +0.006 SD translated the same way.

The three that wait would be estimates with power under 0.05, so they would say almost nothing tonight. The cost: once tonight's outcomes are opened, these songs are seen, and those three need another unseen batch. Their frozen forms are already in `measures.py` (`pmin_of`, `loop_period`, `burstiness`). Their power at other K values is in `power_scan_b.json`.

## Left out, and why
- **Withdrawn by its author:**
  - R08-I3, inherited template F. It also fails the stability gate: 0.45 in the Inventor's check, cross-source 0.23, and 94% of charts score zero.
  - R08-G2 is withdrawn from the *count* only, so it runs as an estimate.
- **Stopped by their authors on the notes:**
  - the Geometer's two circles (ρ 0.82 with the fifths step: R03-F1 renamed);
  - local straightness (ρ 0.76 with the killed arrow);
  - the Inventor's copying fidelity (stability 0.13).
- **Data not on hand this pass:**
  - R03-I1, melody transport: Wikifonia's MusicXML melodies are in the zip but not parsed.
  - R02-breadth: needs genres per version.
  - W01-J6c: needs MusicLab.
- **Reported, not tested:**
  - W01-J6a, early covers: cover_timeline's K10 and L are its early and late counts, reported there.
  - Run 02's ruling stands: nothing is decided on early against late.
- **Merged into a killed idea or retired:** R03-G1 (repetition renamed) and W01-J4.
- **Untouched:** W01-J6b, the McGill hold-out.
- **Failed earlier and not reopened:** every idea marked `failed` in `ideas.json`.
  - That includes ch_rep at +1.0 on y_foreign (R04-FV).
  - chrep_confirm is a different idea: W01-J1 on cover *counts*, and its status is "passed".

## What a reader should keep in mind
- **Lead sheets, not recordings.** A chart is one writer's reading of a tune. Two writers agree only modestly, so every effect is diluted.
- **Within composer is not within performer.** Fame of the first recording still varies between one composer's tunes.
- **Hits only.** Every song has a Discogs-VI clique.
- **The timeline test's power rests on an assumed outcome scale** (the middle of three). If the counts run low, its true power is nearer 0.17.

## Practical notes for the experimenters
- **Commit and push first, without running anything.** The guard refuses an outcome until each folder's PREDICTION.md and `common.py` are committed, unmodified and pushed to origin/judging-research. The commit should include:
  - this file;
  - `experiments/measures.py`, `models08.py`, `harness08.py`, `power_run08.py`;
  - `measure_gates.json` and the `power_*.json` files;
  - the eight folders, each with `PREDICTION.md` and `test.py`.
- **Check the table.** If `/home/claude/dl/choco/measures_run08.json` is missing or its sha256 differs, rerun `python3 -I measures.py` (about one minute).
- **Then run each test once.** `cd experiments/<folder> && python3 -I test.py`. Each prints power first, then the estimate, then writes `result.json`.
  - A y_cov test takes about two minutes, most of it the power reprint.
  - `heritability` takes about four minutes (10,000 permutations).
  - `cover_timeline` takes about one minute, plus the scan of the versions file.
- **No test.py has been run on a real outcome.** The code paths were exercised once on synthetic outcomes (common.load_outcomes replaced by a random generator in a scratch script, outside the repo), and the synthetic results were discarded.
- **`ideas.json` has no R08 entries yet.** They need adding with these statuses:
  - testing: G1, L1 (+I1), L3, I2, L2 (+G3);
  - estimate: G2;
  - withdrawn: I3, and I1 and G3 as merged.
  - Record R03-I2, R03-G3, R07-L2 and R07-I3 as above, and W01-J1 as "fresh confirmation frozen (run08/chrep_confirm)".

## Data and credit
- **The new notes:** ChoCo, the Chord Corpus (de Berardinis, Meroño-Peñuela, Poltronieri & Presutti 2023; Zenodo 7706751; CC BY 4.0). Its iReal Pro charts are user contributions; its Wikifonia lead sheets were CC-licensed.
- **The outcome, joined only after the commit:** Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024; CC BY-SA 4.0).
- **Cards:** Rabin, Delon & Gousseau, "Transportation Distances on the Circle" (JMIV 2011; arXiv:0906.5499), and Evans & Giometto, "Turnover Rate of Popularity Charts in Neutral Models" (arXiv:1105.4044).
