# Run 11: the chair's picks

28 November 2026, the 02:17 ET pass. Research only; nothing goes into the Luthier engine. Yardstick unchanged: lasting love plus covers by other artists. Data: the Hooktheory clip melodies of the 9,588 within-artist songs (1,741 artists; run 04's rows). **These songs are seen** (their outcome was joined to chord measures in runs 04-06 and to a few melody measures); every measure below is new to them. Run 10 is withdrawn (`run10/WITHDRAWN.md`): its ideas are re-tested fresh, and none of its figures is used here.

**No outcome was opened.** I did not call `common11.load_outcomes` or `C5.load_outcomes`, did not run `harness11.py run`, and read no covers, HOLDOUT or `data/*.json` file. Sources: the cache `/home/claude/dl/run11/measures_run11.json` (rebuilt from all five modules in `experiments/measures/`), the gates (`experiments/gates11.py` → `measure_gates11.json`) and fake outcomes on the real rows (each folder's `power.json`). A dry run of `do_run` in my scratch directory, on a synthetic outcome of random numbers, computed every frozen reading; the conditional logit failed there because **statsmodels is not installed**.

## Tonight's tests

**K = 5, α = .05/5 = 0.01.** Five tests are counted. Three more are frozen as uncounted estimates. That makes eight folders, which is within the cap.

| Rank | Folder | Idea | Key | Pred | Frozen extras | N | Power at .01 | Kill if true / if zero | Fake SE | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `gap_rooms/` | R11-G1 (= R10-I3) | `G_GAP` | −0.03 | range, n_pitch, ln_notes | 9,566 | **0.220** | 0.023 / 0.473 | 0.0154 | counted |
| 2 | `tie_rooms/` | R11-G3 (+ R11-I1) | `G_TIE` | +0.03 | ln_notes, density, n_pc | 9,576 | **0.330** | 0.027 / 0.603 | 0.0142 | counted |
| 3 | `rep_entropy/` | R11-L3 (= R10-S1) | `REP` | −0.03 | none | 9,588 | **0.220** | 0.017 / 0.547 | 0.0151 | counted |
| 4 | `typ11_typical/` | R11-L2 | `TYP11` | +0.03 | mel_ic_mean | 9,588 | **0.387** | 0.037 / 0.660 | 0.0133 | counted |
| 5 | `ant_push/` | R11-I2 | `ANT` | +0.03 | density | 9,363 | **0.280** | 0.027 / 0.610 | 0.0138 | counted |
| 6 | `slg_selflearn/` | R10-L1 | `R_SLG` | +0.03 | bar_rep, ln_notes | 8,879 | 0.227 | 0.023 / 0.487 | 0.0158 | ESTIMATE (set full) |
| 7 | `core_typical/` | R10-L2 | `R_CORE_IC` | −0.03 | pc_entropy, mel_ic_mean | 8,879 | 0.190 | 0.030 / 0.397 | 0.0178 | ESTIMATE (power) |
| 8 | `lockp_peaks/` | R11-I3 (+ R10-I2) | `LOCKP` | +0.02 | none | 9,379 | 0.133 | 0.033 / 0.300 | 0.0128 | ESTIMATE (gate) |

Power: 300 fake draws, seed 11, real rows, frozen model (Monte Carlo error about ±0.024). A counted test **passes** on p < 0.01, the predicted sign, both artist halves (md5 of the artist slug) and the conditional logit with that sign (`common11.verdict`); it is **killed** only if its prediction lies outside β̂ ± 1.96 SE (R07-3); otherwise **unsettled**. Estimates run with `counted: false`.

Every folder freezes the measure bare, **all 13 baselines plus mel_ic_mean held** (for REP, the other 12), and the **intensive** reading (among songs in Discogs-VI, z(log(1 + covers)), extras and **first year** held; first year cannot be held on the extensive margin, since unmatched songs have none). Round-2 readings: GAP with G_ROOMS, G_ROOMS holding G_GAP, SETTLE; TIE with CT held, Bergsma's corrected V² (`G_TIE_BC`, new in `m_chair_run10.py`), HB; REP with n_pitch, range and mel_ic_mean held, n_pc; TYP11 with pc_entropy held, tonic_share held, TYP_KK11, TYP; ANT with sync_per_note held, CT held. ANTC is in no module, so it is not frozen.

### How K was set
The rule is that K counts the tests whose power at .05/K is at least 0.2. Tonight no K satisfies it exactly. I applied the rule run 08 froze for this case: **K is the largest number for which at least K tests clear 0.2 at .05/K.** The tests are taken in ranking order. Power was computed from the same 300 fake draws at each α:

| Power at .05/K | GAP | TIE | REP | TYP11 | ANT | SLG | core_ic | clear 0.2 |
|---|---|---|---|---|---|---|---|---|
| K = 4 | 0.243 | 0.377 | 0.250 | 0.420 | 0.340 | 0.277 | 0.210 | 7 |
| **K = 5** | 0.220 | 0.330 | 0.220 | 0.387 | 0.280 | 0.227 | 0.190 | **6 (≥ 5)** |
| K = 6 | 0.193 | 0.293 | 0.203 | 0.340 | 0.267 | 0.210 | 0.160 | 5 (< 6) |
| K = 7 | 0.167 | 0.273 | 0.193 | 0.323 | 0.240 | 0.200 | 0.150 | 4 |

At K = 5 six clear the floor; the five counted are taken in ranking order. **SLG (0.227) ranks sixth**: its Hooktheory corpus (split by mode) is my wrap, not a recipe argued through this pass's rounds and the Skeptic, and its main renamer, mel_rep (ρ +0.44), is not held in the frozen form.

The cost: GAP (0.220) is in and SLG (0.227) out, a gap inside the Monte Carlo error. Jason may overrule the rule.

### Order
1. **GAP**: Jason's own S, and card 1's k = 2 case. It is this pass's mathematics focus.
2. **TIE**: card 1's theorem on the bipartite melody-harmony graph, the only test that uses melody and chords together.
3. **REP**: the replication anchor; if it is unsettled at this power, the other nulls say little.
4. **TYP11**: little renaming (R² 0.16) and the best powered.
5. **ANT**: not renamed, but tied to style and to how the transcriber places the chords.

## The gates (written before any outcome)

**Ruling.** The standing gate of runs 05-06 (clip-1 vs clip-2 Spearman ≥ 0.20; no single |Spearman| > 0.70 with a baseline or pack measure; REP, a baseline by design, exempt from the overlap part) applies to **the raw measure as frozen**. Runs 05-06 gated a residual only when the measure was itself defined as one (run 05's H). I add no residual gate; the Skeptic's stability with extras held is printed beside and decides nothing, and every test carries the all-13-baselines reading instead.

| Key | Role | Clip stability (pairs) | Largest overlap | R² on 13 | Stability, extras held | Stability, 13 held | Gate |
|---|---|---|---|---|---|---|---|
| G_GAP | test | **0.2004** (4,239) | n_pitch −0.61 | 0.57 | 0.158 | 0.089 | passes, narrowly |
| G_TIE | test | 0.265 (4,258) | ln_notes −0.34 | 0.34 | 0.216 | 0.207 | passes |
| REP | test | 0.389 (4,271) | (exempt; n_pc +0.88) | 1.00 | 0.389 (none) | 0.118 | passes |
| TYP11 | test | 0.212 (4,266) | n_int +0.25 | 0.16 | 0.207 | 0.183 | passes |
| ANT | test | 0.252 (3,981) | density +0.27 | 0.11 | 0.213 | 0.177 | passes |
| R_SLG | estimate | 0.247 (3,415) | mel_rep +0.44 | 0.47 | 0.217 | 0.153 | passes |
| R_CORE_IC | estimate | 0.386 (3,415) | mel_ic_mean +0.59 | 0.41 | 0.130 | 0.181 | passes |
| LOCKP | estimate | 0.143 (3,965) | ln_notes +0.07 | 0.02 | 0.143 | 0.136 | **stopped** |
| Run 10's ideas (readings) | reading | LOCK 0.112, pe_h0 0.182, IRR 0.152, skeleton S 0.080, ARCH 0.170, CUT_AB 0.095, TSG 0.155 | ≤ 0.44 | | | | stopped |
| R_CHEEGER (R10-C1) | reading | 0.245 (4,239) | **n_pitch −0.715** | 0.54 | 0.124 | | stopped (overlap) |
| G_ROOMS / SETTLE | readings | 0.218 / 0.212 | n_pitch +0.64 / +0.68 | 0.33 / 0.49 | 0.153 / 0.113 | | pass |
| HB / G_TIE_BC / CT | readings | 0.263 / 0.201 / 0.288 | ≤ 0.37 | | | | pass |
| TYP / TYP_KK11 | readings | 0.215 / 0.198 | tonic_share +0.41 / n_int +0.26 | | | | pass / under |

GAP clears the bar by 0.0004; as in run 05, it is not to be recomputed on more pairs. Among the eight frozen measures the largest overlaps are REP–core_ic +0.55, REP–GAP −0.47 and TYP11–SLG −0.41; every other pair |ρ| ≤ 0.33 (matrix in the json).

## Merges
- **GAP** absorbs G_ROOMS (R11-G2, ρ −0.79), SETTLE (R11-L1, −0.80), run 10's GAP (R10-I3, the same recipe), Cheeger sweep cut (R10-C1, +0.80) and CUT_AB (R10-L3), all readings in `gap_rooms`. S = 1 + g/π is G_GAP.
- **TIE** absorbs HB (R11-I1, ρ 0.96). **REP** (R11-L3) is R10-S1. **LOCKP** absorbs LOCK (R10-I2). **core_ic** carries TSG (R10-L2b).

## Left out, and why
- **Stopped at the gate (written before outcomes):** LOCKP and LOCK (the footfall belongs to the section, not the song; LOCKP runs as an estimate); R10-G1, R10-G2, R10-G3, R10-I1, R10-L3, R10-L2b on stability; R10-C1 on overlap. Under Jason's test-everything rule each is printed as an uncounted reading labelled "stopped; reads noise" (pe_h0, retracing, skeleton S and arches ride in `gap_rooms`). BIP (R11-X1, 0.11) stays stopped.
- **Over the counted set:** SLG (estimate). **Under the power floor:** core_ic (0.190, estimate).
- **Needs missing data:** R10-S2 (a TheSession poster field; that data may not be used); W01-J6c (MusicLab).
- **Withdrawn:** every run 10 figure; the ideas are re-tested, the numbers unused.

## What runs first next pass
Nothing waits over the cap. Next pass should first decide what to do with whatever passes here. The songs are seen, so a pass is a lead until confirmed on unseen melodies (none on hand). If Jason drops the run 08 K rule, SLG is the first estimate to promote, before its outcome is joined.

## Practical notes for the orchestrator
- **Install statsmodels before running.** `C5.cond_logit` imports it and it is missing on this machine (pip can reach it). Without it the second model returns an error, `second_ok` is false, and **no counted test can pass**.
- **Commit and push everything first, without running anything:**
  - `run11/chair.md`, `brainstorm.md` and the round files;
  - `experiments/common11.py`, `harness11.py`, `build_cache11.py`, `checks11.py`, `gates11.py`, `measure_gates11.json`;
  - `experiments/measures/*.py` (new: `m_chair_run10.py`);
  - the eight folders, each with `spec.json`, `power.json` and `PREDICTION.md`;
  - `ideas.json`.
  
  Do not commit `__pycache__/`. The guard in `common11.load_outcomes` refuses until PREDICTION.md and common11.py are committed, unmodified and pushed to origin/judging-research.
- **Then run each folder once**, in rank order: `cd run11/experiments && python3 harness11.py run <folder>`, for gap_rooms, tie_rooms, rep_entropy, typ11_typical, ant_push, slg_selflearn, core_typical, lockp_peaks. Each takes about 10 s plus the logit.
- **Do not rebuild the cache** between pushing and running. The tests read `/home/claude/dl/run11/measures_run11.json`, built at 02:55 ET tonight. If it must be rebuilt, `build_cache11.py` is deterministic; G_GAP's 0.2004 must reproduce exactly.
- **ideas.json** (run11 chair): "testing" for R11-G1, R10-I3, R11-G3, R11-L3, R10-S1, R11-L2, R11-I2, R10-L1, R10-L2; "stopped" for R11-I3, R10-I2, R10-G1, R10-G2, R10-G3, R10-I1, R10-L3, R10-C1, R10-L2b; notes on R10-S2, R11-G2, R11-L1, R11-I1.

## Credit
Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0. Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0. Card 1: Li, arXiv:2609.35369 (2026).
