# Run 12: the chair's picks

28 November 2026, the 10:17 ET pass (chair 10:55 to 11:30 ET). Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. Physics vector 1 (fitness, not luck) starts here. Vector 2 (predictive information) runs on Lakh and Hooktheory. P11-4 (roughness) and P11-5 (invariants across arrangements) each get a pass.

**No outcome was opened.** Specifically:
- I called neither `C5.load_outcomes` nor `common12.load_hook`/`load_lakh`.
- I read neither `/home/claude/dl/run12/fitness.json`, `data/*.json`, a covers file nor a HOLDOUT file.
- I ran `harness12.py run` only on `canal_pilot`, which is notes-only.

**Sources.**
- The notes-side caches: `DATA.md` lists them, with hashes.
- The gates (`experiments/gates12.py` → `measure_gates12.json`).
- Fake outcomes on the real rows, **with the within-artist variance share** (`outcome_side_shares.json`; run 11's lesson). These are in each folder's `power.json`.
- A dry run of every `run` path on a synthetic outcome (random numbers), in my scratch directory. Every path ran, including the conditional logit (statsmodels 0.15.0 is installed) and the 500-resample bootstrap in `windows`.

## Tonight's tests

**K = 3, α = .05/3 = 0.0167.** Three tests are counted. Five more are frozen as uncounted estimates, and one is a notes-side pilot.

| Rank | Folder | Idea | Key | Prediction | N (songs / artists) | Power at .0167 | Kill if zero | Fake SE | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `v1_rep/` | V1 (Jason's vector 1) | REP → D = z(FIT) − z(log1p N) | β_D −0.01 | ~1,845 rows (matched; model-based) | **0.293** | 0.42 | 0.0055 | **counted** |
| 2 | `pi3c_lakh/` | R12-L1 (+ R12-G2 reading) | PI3c (H1, REPBAR + Lakh controls held) | +0.03 | 5,093 / 1,481 | **0.243** | 0.46 | 0.0168 | **counted** |
| 3 | `pic_hook/` | R12-L2 | PIC (step_share, mel_ic_mean, ln_notes, pc_entropy held) | +0.03 | 9,544 / 1,741 | **0.587** | 0.81 | 0.0113 | **counted** |
| 4 | `v1_chrep/` | V1 (Jason's vector 1) | ch_rep → D | β_D −0.01 | ~1,845 rows | 0.193 | 0.36 | 0.0059 | ESTIMATE (power) |
| 5 | `rep_lakh/` | REP replication | REP_L (Lakh controls) | −0.02 | 5,848 / 1,661 | 0.070 | 0.17 | 0.0182 | ESTIMATE (power) |
| 6 | `fifths_lakh/` | R12-G1 | E5_L (REST_L, TOP_L held) + Wald b_E5 vs b_REST | +0.02 | 5,848 / 1,661 | 0.070 | 0.12 | 0.0193 | ESTIMATE (stopped at gate: ρ −0.708 with REP_L) |
| 7 | `windows/` | merge of G3, L3, I1 | Δ = β_L − β_E, REP and ch_rep | REP −0.02 (Listener); ch_rep 0 (Inventor) | ~1,450 rows (t0 ≤ 2005) | 0.060 (REP) | — | 0.022 (Δ) | ESTIMATE (power) |
| 8 | `roughx_lakh/` | R12-I2 | ROUGH_X (register, octaves, chord measures held) | −0.01 | 5,699 / 1,627 | 0.013 | 0.04 | 0.0210 | ESTIMATE (power; the gate passes) |
| 9 | `canal_pilot/` | R12-I3 | CANAL (notes only) | P1-P4 | 159 pairs | — | — | — | PILOT (run: P1, P2, P4 true; P3 false) |

**Power methods** (300 fake draws, seed 12, Monte Carlo error about ±0.025):
- **Lakh:** within-artist share 0.46 (Lakh y_foreign).
- **Hooktheory y_foreign:** share 0.38, y's share. y_foreign's own share is not in the file. Run 11's realised REP SE of 0.011 against its no-share fake SE of 0.0151 implies about 0.5, so PIC stays far above the floor either way (0.173 even with no share).
- **FIT tests (V1, WINDOWS):** model-based, from fit.json's r, A, g and h:
  - matched rows come from an artist-clustered probit tuned to 2,091 rows and to y's share 0.38;
  - η ~ Gamma(r, r) has artist correlation tuned to log-covers' share 0.427;
  - first years are fake, in two scenarios ("artist" era 1960-2012; "recent" 1985-2012), and the lower power is used;
  - N ~ Poisson(η·E).
  The simulated sd(D) is 0.39, against 0.38 implied by the real FIT–log1p N Pearson of 0.927.

**Verdicts.** A counted test **passes** on p < 0.0167, the predicted sign, both artist halves (md5 of the artist), and, for the binary outcomes (pi3c_lakh, pic_hook), the conditional logit with that sign. It is **killed** only if its prediction lies outside β̂ ± 1.96 SE (R07-3). V1's kill is Jason's: the range rule on −0.01 **and** β̂_D ≥ 0. Otherwise it is **unsettled**. Estimates run with `counted: false`.

### How K was set (run 08's rule: K = the largest number for which at least K tests clear 0.2 at .05/K, taken in ranking order)

| Power at .05/K | v1_rep | v1_chrep | pi3c | pic | rep_lakh | fifths | windows REP | rough_x | clear 0.2 |
|---|---|---|---|---|---|---|---|---|---|
| K = 1 (.05) | 0.443 | 0.370 | 0.397 | 0.767 | 0.170 | 0.137 | 0.147 | 0.030 | 4 |
| K = 2 (.025) | 0.337 | 0.250 | 0.297 | 0.650 | 0.093 | 0.083 | 0.090 | 0.017 | 4 |
| **K = 3 (.0167)** | 0.293 | 0.193 | 0.243 | 0.587 | 0.070 | 0.070 | 0.060 | 0.013 | **3 (≥ 3)** |
| K = 4 (.0125) | 0.277 | 0.167 | 0.220 | 0.543 | 0.053 | 0.053 | 0.047 | 0.013 | 3 (< 4) |
| K = 5 (.01) | 0.227 | 0.157 | 0.203 | 0.527 | 0.047 | 0.040 | 0.040 | 0.013 | 3 |

**The cost.**
- **v1_chrep (0.193)** misses the floor at K = 3 by less than the Monte Carlo error. Its "artist" scenario gives 0.193 and its "recent" scenario 0.240; the frozen rule takes the lower.
- **If PIC were left uncounted, as the orchestrator's reading proposed,** K would be 2. The two counted would be v1_rep and v1_chrep, and pi3c would drop to an estimate although it clears 0.2. Counting PIC gives three counted tests instead of two, and it carries vector 2 on both sources.
- Jason may overrule either choice. It must be done before any join.

### Order (and why)
1. **v1_rep.** Jason's mandated vector-1 test, on the one melody measure that has passed before (REP, run 11). It is the only counted test whose outcome is new: FIT has never met a notes measure.
2. **v1_chrep.** The same mandate, on chord repetition.
3. **pi3c_lakh.** Vector 2 on whole songs. It is not renamed: its largest overlap is |ρ| 0.17, and it is stable between arrangers (0.47 on non-duplicate pairs). These are the Lakh songs no melody measure has met.
4. **pic_hook.** Vector 2 on clips. It is well powered but re-spent, and it is tied to mel_ic_mean (ρ −0.63, held).
5. **rep_lakh.** The replication. It is under the floor because REP_L shares variance with run 07's V (ρ 0.63) and the other controls.
6. **fifths_lakh.** Stopped at the overlap gate.
7. **windows.** It sees launch luck, which the Skeptic called the only test that can, but its power is about 0.06 until pooled.
8. **roughx_lakh.** The gate passes, but the prediction is tiny (−0.01).

## The gates (written before any outcome; `measure_gates12.json`)
- **Lakh:** two-file Spearman on non-duplicate kept pairs ≥ 0.20, and no |Spearman| > 0.70 with an existing measure. Existing measures are run 07's 13, the Skeptic's LNEV, NPB, ACT and NFILES, and REP's skyline twins REP_L and H1. REP_L and H1 are exempt, as REP was in run 11.
- **ROUGH_X** also has the Inventor's own gate: stability with register held ≥ 0.20.
- **Hooktheory:** the run 05-06 clip gate.

| Key | Role | Stability (pairs) | Largest overlap | Within-artist share | Gate |
|---|---|---|---|---|---|
| PI3c | test | 0.471 (135) | cv_w −0.17 | 0.64 | passes |
| PIC | test | 0.273 (4,219 clip pairs) | mel_ic_mean −0.63 | — | passes |
| REP (Hooktheory) | V1 | 0.389 (4,271) | exempt | — | passes (run 11) |
| ch_rep | V1 | pack measure (runs 04-06) | — | — | existing |
| REP_L | estimate | 0.596 (159) | V +0.63 (H1 +0.885, exempt twin) | 0.57 | passes |
| H1 | reading / held | 0.691 (135) | V +0.67 | 0.55 | passes |
| E5_L | estimate | 0.566 (159) | **REP_L −0.708** | 0.61 | **stopped** (overlap) |
| REST_L / TOP_L / C_L | held / readings | 0.43 / 0.43 / 0.53 | REP_L −0.81 / −0.81 / −0.96 | | fail (held only) |
| PI8 (G2) | reading | 0.527 (154) | ch_rep +0.34 | 0.63 | passes |
| ROUGH_X | estimate | 0.299 (159); **0.354 with register held** | NPB −0.13 | 0.55 | passes |
| REPBAR / EVLEN / H8 | held | 0.54 / 0.51 / 0.37 | ch_rep +0.52 / LNEV −0.67 / LNEV +0.48 | | pass |
| G_E5 (Hooktheory reading) | reading | 0.311 (4,271) | pc_entropy −0.61 | | passes |

**Near-duplicate rule (frozen).** Within a song, a MIDI file whose tracks-1-2-4 pitch-class profile has a min-over-rotations JSD below 1e-4 against an earlier kept file is dropped. This dropped 81 files in 77 songs, so 159 non-duplicate pairs remain. The song value is the mean over the kept files. NFILES (the fame proxy) counts the files listed.

## Merges
- **WINDOWS** is G3 THIN + L12-3 Late wins + I-1 PROP, the Skeptic's Merge 1, accepted by all three authors. FE Poisson per window with a five-year first-year design and a paired bootstrap. The REP prediction is the Listener's; ch_rep's is the Inventor's.
- **PI3c** absorbs G2 PRED, the Skeptic's Merge 2. PI8 and its shrink run as readings.
- **V1** is the brief's design with the Skeptic's margin argument. The kill is written as Jason's words.

## Left out, and why
- **G3 THIN (binomial late share):** withdrawn into WINDOWS by the Geometer.
- **PI1C, PI2c, E3c, PI4c, KEFF, grid PIs:** dropped by the Listener on the notes (renamed or saturated).
- **ROUGH (round 1, octaves kept) and ROUGH_BEAT:** replaced by ROUGH_X. ROUGH_BEAT has ρ 0.92 with NPB.
- **G_PI on clips:** stability 0.16, stopped by the Geometer.
- **WINDOWS pooled with Lakh:** next pass (`DATA.md`). Discogs-VI main.zip is DONE, but the Lakh clique link is an outcome, and the pooled design needs rules of its own.
- **P11-3 (the performer's field):** no aligned recordings.

## CANAL pilot (run; notes only)
There are 159 non-duplicate pairs. CANAL's median is 0.988 (10th to 90th percentile 0.930 to 0.998), and 86% of pairs are in the same key. Spearman between CANAL and the files' agreement:

| Measure | ρ with CANAL |
|---|---|
| H1 | +0.52 |
| REP_L | +0.41 |
| E5_L | +0.50 |
| PI3c | +0.30 |
| ROUGH_X | +0.34 |
| NPB | +0.23 |

ρ with mean PCE_ALL is +0.19.

- **P1, P2 and P4 hold.**
- **P3 fails.** Agreement on roughness also tracks CANAL, so well-canalised pairs agree on voicing too. They may share a source arrangement.

The two-file stability ranking (PCE_ALL 0.74 > H1 0.69 > REP_L 0.60 > E5_L 0.57 > PI3c 0.47 > ROUGH_X 0.30) was seen in the gates before the pilot's prediction was written. It is description, not a test.

## Practical notes for the orchestrator
- **Commit and push first, without running anything:**
  - `run12/chair.md`, `run12/DATA.md`, and the brainstorm and round files;
  - `run12/experiments/common12.py`, `harness12.py`, `build_lakh12.py`, `build_hook12.py`, `gates12.py`, `measure_gates12.json`;
  - `run12/experiments/measures/*.py` (unchanged);
  - the nine folders, each with `spec.json`, `power.json` and `PREDICTION.md` (and `canal_pilot/result.json`).

  Do not commit `__pycache__/`. **The guard in `common12.guard` refuses unless the folder's PREDICTION.md and spec.json, common12.py and harness12.py are committed, unmodified and pushed to origin/judging-research.** `C5.load_outcomes` also checks that PREDICTION.md is committed. The guard reads run 11's `common11.py` and run 05's `common.py`, which are already committed.
- **Then run each folder once, in rank order** (`cd run12/experiments` first). The counted tests come first:
  - `python3 harness12.py run v1_rep` (seconds)
  - `python3 harness12.py run pi3c_lakh` (about 20 s with the logit)
  - `python3 harness12.py run pic_hook` (about 30 s with the logit)

  Then the estimates:
  - `python3 harness12.py run v1_chrep`
  - `python3 harness12.py run rep_lakh`
  - `python3 harness12.py run fifths_lakh`
  - `python3 harness12.py run windows` (about 1 to 2 min: 500 bootstrap refits per measure)
  - `python3 harness12.py run roughx_lakh`

  `canal_pilot` is already run (notes only).
- **Do not rebuild the caches between pushing and running.** The tests read `/home/claude/dl/run12/lakh_measures12.json`, `/home/claude/dl/run12/hook_measures12.json` and `/home/claude/dl/run11/measures_run11.json` (hashes in DATA.md). The builders are deterministic; the Lakh `songs` block reproduced exactly.
- **The v1 and windows loaders print two checks:** `window_N_mismatch_vs_fitness_json`, which should be 0 (the windows' cover rule is fitness.py's), and `rows_with_FIT`, which should be about 2,091.
- **ideas.json (suggested; I did not edit it):**
  - **"testing":** V1 (P11-1), R12-L1, R12-L2;
  - **"estimate":** R12-G1 (stopped at the overlap gate), R12-G3/R12-L3/R12-I1 (as WINDOWS), R12-I2, the REP Lakh replication;
  - **"pilot":** R12-I3;
  - **"merged into R12-L1":** R12-G2.

## Credit
- Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0.
- Lakh MIDI Dataset (Raffel 2016) / Lakh Pianoroll Dataset (Dong et al. 2018), CC BY 4.0.
- Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
- Cards: Freeman & Jordan, arXiv:1812.06946; Gaeta, Garetto, Ruffo & Flammini (2022), DOI 10.1145/3530790.

## Addendum (orchestrator, after the results)
- One test written after seeing results joined the pass's total: `windows_lakh_after` (rule 2d64143), so **K = 4, α = .05/4 = 0.0125** for the pass. None of the three counted tests had p under .0167, so no verdict changed. Its code read the wrong Discogs-VI member on a first run; fixed to the written rule and rerun (3f22888, NOTE_rerun.md); both runs reported.
- `fitness_finebins_after` (cover timing only, no notes; not counted): the no-attachment finding holds with yearly age bins.
- The windows estimate's frozen bootstrap failed for ch_rep (NaN replicates), so its frozen range flag is void; its RESULT.md reports the analytic SE.
