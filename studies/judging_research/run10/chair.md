# Run 10: the chair's picks

27 November 2026, the 18:17 ET pass. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus
covers by other artists. The data are new this pass: TheSession.org traditional tunes, melody only (`common10.tunes()`, 23,089 tunes;
split A 14,511 for tonight's tests, split C about 4,260 for confirmation, split H sealed). The primary outcome is y_cov, the standardised
log of 1 + the number of distinct recording artists of the tune; y_love (log tunebooks, tunes with 10 or more) is a reading beside it.

**No outcome was opened.** I did not open recordings.csv or tune_popularity.csv, did not call `common10.load_outcomes`, and did not run
`harness10.py run`. Everything below comes from the notes (the measure cache `/home/claude/dl/thesession/measures_run10.json`, built from
`experiments/measures/` for splits A and C), from my own stability and renaming checks on split A (`experiments/measure_gates10.json`)
and from fake outcomes on the real rows (`harness10.py power`, each folder's `power.json`). The one synthetic-outcome dry run of the
readings code (random Poisson counts, in my scratch directory, to check that every frozen reading computes) read no outcome.

## Tonight's tests

**Nine counted tests are frozen, all at α = .05/9 = 0.00556: K = 9.** Eight run tonight. The ninth, `lock_turns`, is frozen in the same
family at the same α and runs first in the next pass (the standing cap of eight; see "Order"). The estimates (GAP, g, TSG and the other
companions) are frozen as uncounted readings inside the related folders, not as folders of their own.

A counted test **passes** when p < .05/9, the sign is the predicted one, both halves (md5 of the composer key, or of 'trad:<tune_id>'
for traditional tunes) have that sign, and the Poisson model on the artist count has it too (`common10.verdict`). It is **killed** only if
its prediction lies outside the estimate's 95% range (R07-3); otherwise it is **unsettled**.

| Rank | Folder | Idea | Measure (cache key) | Prediction (y_cov, SD per SD) | Frozen extras | N | Power at .05/9 | kill if true | kill if zero | fake SE |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `rep_entropy/` | REP (Skeptic; McBride & Leroi) | `pc_entropy` | **−0.03** | none | 14,511 | **0.713** | 0.017 | 0.920 | 0.0093 |
| 2 | `s_gap_skeleton/` | G10-3, Jason's S (the one S) | `S_gap` | **−0.03** | n_pc | 14,511 | **0.673** | 0.047 | 0.923 | 0.0092 |
| 3 | `pe_h0_links/` | G10-1, card 1 M4 | `pe_h0` | **+0.03** | pc_entropy | 14,511 | **0.723** | 0.057 | 0.880 | 0.0092 |
| 4 | `irr_skel_retrace/` | G10-2, IRR on melody | `irr_skel` | **−0.03** | n_pc | 14,511 | **0.753** | 0.050 | 0.917 | 0.0090 |
| 5 | `core_typical/` | L2 as core_ic (Skeptic's form) | `core_ic` | **−0.03** | pc_entropy | 14,413 | **0.510** | 0.043 | 0.810 | 0.0112 |
| 6 | `cut_ab_parts/` | L3 | `cut_ab` | **+0.03** | n_bars, ln_notes | 14,413 | **0.700** | 0.050 | 0.920 | 0.0092 |
| 7 | `arch_contour/` | R10-I1 | `ARCH_PE` | **−0.03** | range, n_pitch | 14,511 | **0.643** | 0.047 | 0.877 | 0.0095 |
| 8 | `slg_selflearn/` | L1 | `slg` | **+0.03** | bar_rep, ln_notes | 14,413 | **0.413** | 0.070 | 0.727 | 0.0113 |
| 9 | `lock_turns/` (WAITS: runs first next pass) | R10-I2 | `LOCK` | **+0.03** | none | 14,511 | **0.740** | 0.043 | 0.910 | 0.0089 |

y_love signs are the same as the y_cov signs in every folder (`love_sign` in spec.json). Power: 300 fake draws, seed 10, the real rows,
the frozen model and extras; Monte Carlo error about ±0.03 near these values.

### How K was set
K is the number of counted tests with power ≥ 0.2 at .05/K. I computed every candidate at .05/9 first: all nine clear 0.2 (the lowest is
`slg_selflearn`, 0.413), so **K = 9** is consistent and no recompute was needed. I kept K = 9 although only eight run tonight, because the
ninth is frozen tonight in the same family and keeps its α when it runs; Bonferroni over nine is conservative for the eight (it costs them
about 0.02 to 0.03 of power against .05/8). The next pass does not count `lock_turns` in its own K.

| Power at α = .05/9 | rep | S_gap | pe_h0 | irr_skel | core_ic | cut_ab | ARCH_PE | slg | LOCK | at or above 0.2 |
|---|---|---|---|---|---|---|---|---|---|---|
| K = 9 | 0.713 | 0.673 | 0.723 | 0.753 | 0.510 | 0.700 | 0.643 | 0.413 | 0.740 | **9 of 9** |

`core_ic` and `slg` have the larger fake SE (0.011) because their type-specific corpus models make them partly explained by the type
fixed effect, and slg's two frozen extras take more of it.

## Why each was selected (all nine candidates qualify; none merged away)
- **REP (pc_entropy, −0.03).** McBride & Leroi's own measure on this very site, the replication baseline the Skeptic asked for. If it is
  unsettled at power 0.71, every null below means little; if it passes, any measure leaning on pc_entropy must beat it with pc_entropy
  frozen (`pe_h0_links` and `core_typical` freeze it). density, n_pc and ln_notes run as readings.
- **S_gap (−0.03, n_pc frozen).** Jason's S = 1 + g/π, never powered before (run 07's chord version, power 0.01). The Skeptic's merge is
  applied: the Inventor's GAP and the Listener's g are one measure (ρ 0.97, both mostly range, R² 0.63 and 0.64) and run as estimates
  inside this folder with range, n_pitch and ln_notes frozen; the Geometer's skeleton form is distinct (ρ with GAP −0.01) and is the one
  counted S.
- **pe_h0 (+0.03, pc_entropy frozen).** Card 1's construction (H0 bars = MST of the shortest-path metric; persistent entropy). The
  round-1 "1/p opposite sign" kill is dropped (ρ 0.87, one test); pe_h0_inv is a reading.
- **irr_skel (−0.03, n_pc frozen).** The backlog's IRR revived on melody; it asks whether run 09's chord sign (back-and-forth with more
  covers) carries to melody.
- **core_ic (−0.03, pc_entropy frozen).** The Skeptic's form of L2 and card 2's typicality test. TSG was mostly −surf_ic (ρ −0.73 here)
  and reads the weak beats where transcribers differ, so TSG is an estimate inside the folder, with surf_ic alone as a reading.
- **cut_ab (+0.03, n_bars and ln_notes frozen).** Cheeger geometry asked as a question about time. The strict-AABB reels and jigs
  (aabb == 1, 1,444 tunes) are a frozen subset reading; cheeger and h0_max (the card 1 H0 check) are readings.
- **ARCH_PE (−0.03, range and n_pitch frozen).** Sublevel persistence of the contour. The most renamed counted measure (R² 0.35);
  the frozen controls run against its prediction, so they can only make it harder. step_share held as a reading.
- **slg (+0.03, bar_rep and ln_notes frozen).** The closest to "learning it"; counted only with both renamers frozen (the Skeptic, accepted).
- **LOCK (+0.03, none).** The cleanest measure (R² 0.011). Counted as written.

Every folder also carries an "all 13 baselines held" reading, so a reader can see what survives full renaming.

## The measure gates (written now, before any outcome)
Recomputed by me on split A, notes only, for every key a test or reading uses: stability is the Spearman between a tune's first and second
ok settings over the first 4,000 split-A tunes that have a second setting (the same pairs as `common10.stability`, which I ran directly
for irr_skel, 0.767, and LOCK, 0.741, as a cross-check). Renaming is `common10.renaming` on all of split A.
A measure is **stopped** if (1) its stability is under 0.5 on 100 or more pairs (R09-5), (2) its |Spearman| with any one of the 13
baselines exceeds 0.8 (run 09's first gate, adapted; not applied to REP, which is a baseline), or (3) it is defined on under 90% of split A.

| Key | Role | Stability (n) | R² on baselines | Largest baseline ρ | Coverage of split A | Gate |
|---|---|---|---|---|---|---|
| pc_entropy | REP | 0.830 (4,000) | (0.73; baseline) | n_pc +0.72 | 100% | passes |
| S_gap | counted | 0.750 (3,999) | 0.155 | pc_entropy −0.22 | 100% | passes |
| pe_h0 | counted | 0.676 (3,999) | 0.152 | pc_entropy +0.26 | 100% | passes |
| irr_skel | counted | 0.767 (4,000) | 0.074 | pc_entropy +0.18 | 100% | passes |
| core_ic | counted | 0.569 (4,000) | 0.209 | pc_entropy +0.36 | 99.3% | passes |
| cut_ab | counted | 0.773 (4,000) | 0.178 | range +0.26 | 99.3% | passes |
| ARCH_PE | counted | 0.806 (4,000) | 0.345 | range −0.32 | 100% | passes |
| slg | counted | 0.548 (4,000) | 0.273 | ln_notes +0.34 | 99.3% | passes (nearest the bar) |
| LOCK | counted | 0.741 (4,000) | 0.011 | unison_share −0.08 | 100% | passes |
| GAP / gap | estimates | 0.823 / 0.823 | 0.63 / 0.64 | range −0.58 / −0.62 | 100% / 99.3% | passes (renamed: estimate only, extras frozen) |
| tsg | estimate | 0.601 | 0.159 | step_share +0.38 | 99.3% | passes |
| pe_h0_inv, slg_win, surf_ic, cheeger, h0_max | readings | 0.586, 0.585, 0.554, 0.806, 0.553 | | | | pass |
| density, n_pc, ln_notes | REP readings | 0.874, 0.701, 0.762 | | | | pass |

**No measure is stopped.** Overlap among the nine counted measures is low (split A, 14,413 tunes): the largest |ρ| is 0.40 (slg with
core_ic), then 0.38 (pe_h0 with irr_skel) and 0.36 (core_ic with pc_entropy); so there are no duplicates left to merge.

## Order, and the one that waits
Nine qualify; the standing cap is eight a pass, so the rest (one) runs first next pass. The order:
1. **REP**: the replication anchor; it decides how every null below is read.
2. **S_gap**: Jason's own S, never powered before.
3. **pe_h0**: this pass's card 1 construction.
4. **irr_skel**: the backlog's IRR, and a direct check of run 09's chord sign on melody.
5. **core_ic**: card 2's skeptical reading (typicality) made testable, held against REP.
6. **cut_ab**: Cheeger geometry and form.
7. **ARCH_PE**: sublevel persistence; the most renamed counted measure.
8. **slg**: power 0.41 (lowest) and stability 0.55 (nearest the bar), renamed in part by repetition and length.
9. **LOCK, waits.** Three reasons. This pass's focus is geometry and topology, and LOCK is the one counted idea not grounded in a theorem
   or construction (it rests on card 2's empirical gradient). The Skeptic rated its mechanism the weakest. And it is nearly orthogonal to
   every measure that runs tonight (|ρ| ≤ 0.06 with each of the other eight; R² 0.011 on the baselines), so tonight's results tell nobody
   anything about it, and its frozen prediction stays clean while it waits. slg was the alternative (lowest power), but slg shares ρ 0.40 with
   core_ic, so deferring it would let tonight's core_ic result leak into it.
   **The cost, stated plainly:** next pass LOCK runs on split A tunes whose y_cov has by then been joined to eight other measures. Its
   measure, spec, prediction and α are frozen tonight and committed with this file, so it remains a test written before its own outcome;
   if the orchestrator would rather run all nine tonight, drop the cap for this pass and run `lock_turns` last; the α is already .05/9.

## The confirmation rule for split C (written now, before any outcome)
Any counted test that **passes** on split A is re-run once on split C (about 4,260 tunes, never joined to an outcome), with the identical
spec except `"split": "C"`: the same measure (C values are already in the cache), extras, readings, predicted sign and size, at
**α = .05 / m**, where m is the number of tonight's tests that passed on A. It runs from a sibling folder `<name>_C/` (the A PREDICTION.md
copied, spec.json changed only in split and α); its power is computed on C with `harness10.py power <name>_C` at that α and committed and
pushed before the C outcome is joined. The C verdict is `common10.verdict` on C (counted only if the C power is ≥ 0.2; otherwise an estimate,
and the A pass stays a lead). **The C verdict is the finding.** A test that does not pass on A is not run on C. If `lock_turns` passes on A
next pass, its C confirmation uses α = .05 / (m + 1). For slg and core_ic, the corpus models are trained on split A, so C tunes are scored
against all of split A (nothing to leave out). Split H stays sealed for later passes.

Notes-side preview (fake outcomes on split C at α = .05, i.e. m = 1; in my scratch directory, not committed; the binding C power is the one
computed at the final α): REP 0.453, S_gap 0.453, pe_h0 0.340, irr_skel 0.383, core_ic 0.283, cut_ab 0.390, ARCH_PE 0.347, slg 0.270,
LOCK 0.477 (fake SE 0.017 to 0.022). With two or more confirmations slg and core_ic may fall under the 0.2 floor on C; a reader should
expect a true +0.03 to be confirmed less than half the time.

## Left out, and why
- **Estimates, not separate tests:** GAP (R10-I3) and g (L3's companion; duplicate of GAP) inside `s_gap_skeleton`; TSG (L2's original)
  and surf_ic inside `core_typical`; pe_h0_inv, slg_win, cheeger, h0_max as readings. All uncounted.
- **Rejected by their authors on the notes alone:** ARCH_TOP (R² 0.79, mostly ln_notes), GAP_PC (R² 0.55), GAP over a path's gap
  (R² 0.63), the full-surface spectral gap (R² 0.64), FIED_REG (descriptive only).
- **The Geometer's reserves, not proposed:** Rips H1 count on the skeleton (stability 0.62, R² 0.18) and circular transport between the
  tune's halves (0.67, 0.13). Nobody wrote a prediction, so they are not tests.
- **The first-poster fixed effect** (the Skeptic's round-2 reading for surface measures, accepted by all three authors): `harness10.py`'s
  design carries no username, so it cannot be frozen as written. I did not change the frozen harness. If the orchestrator wants it, it must
  be added (as an uncounted reading) before any PREDICTION.md is pushed; otherwise it waits.
- **Card 2's tune variability and setting dispersion (card 1's M5, card 2's M1):** they need several settings per tune, and the settings
  count is downstream of popularity (never a measure or control in this design).
- **Backlog items named in the brief with no measure written this pass:** R08-G2 transposed repetition, R05-L3 contour-trigram surprise,
  W01-J4 smooth approach, R07-I3 burstiness, R07-L2 loop period, chirality / Lévy area on a melodic path. Nobody proposed a frozen recipe and
  prediction, so they are not testable tonight. Note for the next pass: once tonight's outcomes are joined, split A is seen; a new idea
  written then should be tested on split H when it is unsealed, not on A.
- **A cache quirk, harmless:** the Listener's and the Inventor's `measure()` both return a key `S`; in the cache the Inventor's overwrites
  the Listener's (build order). No test or reading uses `S`.

## Practical notes for the orchestrator
- **Commit and push first, without running anything:** this file, `brainstorm.md`, `experiments/measure_gates10.json`, the nine folders
  (each with `spec.json`, `power.json`, `PREDICTION.md`), and `common10.py`, `harness10.py`, `abcparse.py`, `build_cache10.py` and
  `experiments/measures/*.py` if not already committed; not `__pycache__/`. The guard in `common10.load_outcomes` refuses until each
  folder's PREDICTION.md is committed, unmodified and pushed to origin/judging-research.
- **Then run each of the eight once,** in rank order: `cd run10/experiments && python3 harness10.py run <folder>` for rep_entropy,
  s_gap_skeleton, pe_h0_links, irr_skel_retrace, core_typical, cut_ab_parts, arch_contour, slg_selflearn. Not lock_turns.
- **Then apply the C rule** to whatever passed, power first.
- `ideas.json` was not touched: counted tonight REP, G10-1, G10-2, G10-3, L2 (as core_ic), L3, R10-I1, L1; counted, waits R10-I2;
  estimates R10-I3 (GAP), L2's TSG, L3's g.

## Data and credit
TheSession.org data (Jeremy Keith and the members of thesession.org; github.com/adactio/TheSession-data, fetched 27 Nov 2026). Cards:
Mijangos, Bravetti & Padilla, arXiv:2204.11139 (card 1); McBride & Fitch, arXiv:2607.12673 (card 2); McBride & Leroi (run 02, card 2).
