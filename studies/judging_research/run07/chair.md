# Run 07: the chair's picks

26 November 2026, the 18:17 ET pass. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. The outcome tonight is y_foreign = 100 if Discogs-VI holds a version of the song by another artist. Jason's rule applies: every idea that can be tested tonight on the data at hand is tested, and every counted test shares one threshold.

**No outcome was opened before the rules were frozen.** I did not read anything in `/home/claude/shape/` or `/home/claude/dl/discogs/`, or any covers, versions or HOLDOUT file in the repo. I did not call `common.load_outcomes` or `common.run_test`. `/home/claude/dl/lakh/outcomes_run07.json` did not exist when I started (checked) and still does not. My checks used the notes only (`experiments/chair_gates.py`, `chair_gates_report.py` → `chair_gates.json`) and fake outcomes only (`experiments/power_fake.py` → `power_fake.json`, which calls `common.fake_power`). The Skeptic's and the imaginers' scripts in /home/claude/scripts were read after I checked that they open no outcome. **Run 07 does not touch the McGill hold-out:** its songs are removed from the Lakh list by `common.lakh_songs()`, and nothing reads its outcomes. Song 59, songs/p69 and studies/holdout59 were not read.

## What changed tonight
- **Whole songs, for the first time at scale.** The Lakh Pianoroll Dataset's cleansed songs (MIDI, 4/4) are named through the Million Song Dataset metadata. They give bar chroma and half-bar triad chords. None of their outcomes has ever been joined to anything.
- **The song list was cleaned twice before freezing, on metadata alone.** The first fix kept a file only if it belongs to one song, which left 5,373 songs. The Skeptic's fix then gave a file that carries one title under several artists to each of those artists, and a frozen name list drops cover-only acts. The result is **5,901 within-artist songs by 1,678 artists.** The brainstorm's figures came from the earlier lists. I recomputed every gate on the 5,901 songs.
- **One battery for every test** (`experiments/common.py`: `design()`, `fit()`, `fake_power()`, `run_test()`). It fits a within-artist LPM with CR1 errors by artist, controls for ln_chg, V, ln_bars and year bins, refits within each artist half, and adds a conditional logit. It also reports three readings: on y, with fame held, and first performers only.
- **Two new cards, both mathematics:** Gilbert & Yim on average four-point hyperbolicity (card 1) and Perea & Harer on sliding windows and persistence (card 2).

## Tonight's tests: eight folders

**Each test needs p < .05/8 = .00625 (two-sided, |z| > 2.734).** It also needs the predicted sign, the same sign in both artist halves (`common.half_of`), and a conditional logit of the same sign that converged. The threshold does not move if a test is stopped.

| # | Folder | Idea | Measure (`common.py`) | Extra columns | Prediction on y_foreign (pp per SD) | Kill | Rows | SE (pp) | Power at .00625 / at .05 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `lakh_repetition/` | R04-FV, R06-L3: chord repetition (the standing prediction) | `repetition` (ch_rep) | none | **+1.0** | β ≤ 0 | 5,901 | 1.03 | 0.007 / 0.08 |
| 2 | `tree_h4m/` | R07-L1 (+G1, I1 merged): average four-point hyperbolicity, **the pass's mathematics** | `song_shape` → H4m (`fp_stats`) | cv_w, ch_rep | **−0.5** | β ≥ 0 | 5,901 | 0.72 | 0.003 / 0.04 |
| 3 | `spectral_gap/` | R02-gap = R07-G3: Jason's S = 1 + g/π | `song_shape` → g | ch_rep | **−0.3** | β ≥ 0 | 5,901 | 0.67 | 0.007 / 0.03 |
| 4 | `lakh_chirality/` | R06-I1: harmonic chirality | `CH` | A, ch_rep | **−0.6** | β > −0.2 | 5,900 | 0.57 | 0.000 / 0.08 |
| 5 | `lakh_arrow/` | R05-A: the arrow of time | `A_arrow` (A) | none | **+0.6** | β ≤ 0 | 5,900 | 0.58 | 0.013 / 0.11 |
| 6 | `loop_period/` | R07-L2: loop period P\* | `song_shape` → lnP | ln_tempo | **+0.6** | β ≤ 0 | 5,759 | 0.60 | 0.023 / 0.12 |
| 7 | `burstiness/` | R07-I3: Kac burstiness B | `song_shape` → B | none (V, ln_chg, ln_bars are the controls) | **+0.3** | β ≤ 0 | 5,891 | 0.74 | 0.000 / 0.04 |
| 8 | `triad_fidelity/` | R07-I2: campfire fidelity F | `song_shape` → F | none | **+0.5** | β ≤ 0 | 5,901 | 0.80 | 0.003 / 0.04 |

Two tests are mathematics in the strict sense:
- **`tree_h4m`** comes from card 1. fp is exactly 0 on tree metrics (Buneman), and moving each distance by at most ε moves each fp by at most 2ε.
- **`spectral_gap`** is Jason's S. Cheeger's inequality links a small gap to a bottleneck. It is proved only for reversible chains, so here it is a guide.

`lakh_chirality` carries run 06's Green's-theorem measure onto new songs. `burstiness` rests on Kac's lemma.

Each folder holds a `PREDICTION.md` (the frozen measure, columns, songs, outcome, rules as numbers, power) and a `test.py`. `test.py` calls `C.run_test(folder, S, meas, extra, pred, sign, alpha, kill=…)`, applies the logit-convergence rule, adds the readings named in PREDICTION.md and writes `result.json`. **No test.py has been run.**

## Merges and rulings
- **All eight are counted.** The Skeptic wanted two counted tests (ch_rep and H4m) and the rest reported as estimates. Jason's rule says every testable idea is tested and shares the threshold, so .05 is split eight ways. The cost is plain in the power column. The rule's purpose is that every look at an outcome is paid for in the shared threshold.
- **The "report only" authors did not withdraw, so their ideas are counted.** This covers L2 P\*, I2 F and I3 B ("secondary at most"). Each passes both written gates, and under Jason's rule an idea leaves the count only by needing data not on hand, failing a gate written before any outcome, or being withdrawn. "Report only" is a statement of the author's confidence, not a withdrawal. Printing an outcome coefficient outside the count would be an unpaid look that the next pass could fish on. Their doubts are printed in their PREDICTION.md files: F may read the arranger, and B is mostly vocabulary and length.
- **Withdrawals are respected.** G1 Ht and I1 Hm were merged into H4m and withdrawn by their authors. G2's ring R was "withdrawn as a test (report only)": its author used the word *withdrawn*, so it is out, and I attach it to no test. L3 Nfr was withdrawn (it is ch_rep inverted).
- **A gate failed on clips is re-read once on whole songs, and the same holds for every idea.** R02-gap failed only its clip-to-clip stability gate (0.17), on Hooktheory clips too short to hold two harmonic rooms. Whole songs are the first different unit it has met, and the Skeptic admitted it. Run 06 ruled that re-running a failed gate on new songs "until it clears" would make the gate a fishing step. A new *unit* is different from new *songs of the same unit*, so I allow one re-read per unit, for every idea alike:
  - **R03-G3, the obtuse statue,** also qualifies on that ground. Its p_min is computed from chord tokens, with run 03's code adapted to Lakh tokens in `chair_gates.py`. On the 5,901 songs its split-half is 0.530 and its residual on the size block is 0.311. Its largest renaming overlap is V −0.656 and its R² on the size block is 0.615. It passes both gates. It ranks ninth (see below), so it does not run tonight.
  - **R03-I1 (melody transport)** needs a melody, and LPD-5 has no lead track. It stays out on data, not on the gate.
  - If an idea fails again on whole songs, it stays stopped for good.
- **More than eight qualified (nine), so only the first eight run.** The ninth is R03-G3 p_min, ranked last for four reasons. Its gate was re-read on a new unit after failing. Its prediction (−0.02 SD of log covers) would have to be translated to pp on another outcome. Its renaming overlap (V −0.656) is the closest to the 0.7 line. And no author was present this pass to answer the Skeptic. The cost is that once tonight's outcomes are opened these songs are seen, so p_min must wait for an independent batch. Its frozen form for that batch is run 03's `pmin_of` on the half-bar triad tokens (largest connected piece, at least 3 chords, wrap move added), residualised on V dummies (4 to 19, 20+) and distinct links. The prediction would be negative, the kill β ≥ 0.
- **R03-I2, tonic resistance, is left out: it needs an annotated key, and these songs have none.** Its hub is the tonic, and the measure is defined from it. A key-finder would add a fitted step, and the result would be a different measure, not this idea on new data. Run 05 and run 06 recommended retirement; that remains Jason's call.
- **The standing ch_rep prediction runs as written: +1.0, kill β ≤ 0.** As the Skeptic asked, this is stated before the outcome: an estimate between 0 and +1.0 that is not significant is **unsettled**, neither pass nor kill. **A conflict is flagged:** run 06's first principles wrote this prediction as "one counted test at .05 … run only with fake-outcome power of 0.5 or more". Its power is 0.007 at .00625, and still only 0.08 at .05. Those conditions were recommendations Jason has not adopted, so I run and count the test under his standing rule. By its own first-principles condition it would not have run.
- **H4m's prediction is the median of its three authors:** −0.6 (Listener), −0.5 (Geometer) and −0.5 (Inventor), so −0.5. It uses the Skeptic's frozen form (sliding 4-bar windows ÷ 2, 4,000 quadruples seeded by md5 of the track id) and holds cv_w and ch_rep.
- **g holds ch_rep.** V, the other column the Geometer named, is already a battery control.
- **CH keeps its author's run 06 kill line (β > −0.2).** It was frozen in the same units (pp of y_foreign per SD), so it stands. Run 06's ch_ic_mean column does not exist for MIDI songs, so CH holds A and ch_rep only. |CH| is reported.
- **A runs in run 06's fresh_arrow form** (no extra columns); A with ch_rep held is reported.
- **P\* holds ln tempo** (the Skeptic's half-time and double-time point). Two readings are reported: the seconds form (without ln tempo, since holding it would turn the seconds form back into lnP) and the categorical form (2, 8, 16, other against 4).
- **F carries the Skeptic's warning,** and F with ln tempo held is reported. A pass would need a voicing-free version before it said anything about songs.
- **Fame is reported, not held.** The Billboard flag and hotttnesss are partly downstream of the outcome, so the fame-held fit is a reading. **Year is a precision control:** five-year bins, with unknown (39.8%) as its own bin. Discogs first_year is never used as a control, since it exists only for matched songs. **The first-performer reading** (R02-3's rule) is in `run_test`.
- **The logit must converge.** `run_test` checks the logit's sign but not its convergence, so each `test.py` records a PASS whose logit did not converge as UNSETTLED, as run 06 ruled.
- **W01-J6a, early covers, is reported only,** as run 02 ruled. Early and late uptake appear beside `lakh_repetition`, and nothing is decided on their contrast.

## Left out, and why
- **Withdrawn by their authors:**
  - R07-G1 Ht: merged into H4m; it reads voicing, ρ −0.56 with its own CV.
  - R07-I1 Hm: merged into H4m; 59% of its variance remains once its CV is held.
  - R07-G2 ring R: withdrawn as a test; median −0.004 against its own shuffles.
  - R07-L3 Nfr: ch_rep inverted, ρ −0.54.
  - R05-L3 contour surprise: withdrawn in run 05.
- **Stopped by the Listener on the notes:** first-minute novelty (residual 0.19), time to first return (0.15), bar of the first chorus (0.088), card 2's κ loop span (lag-1 autocorrelation renamed) and return depth (R05-M renamed).
- **Data not on hand:**
  - R03-I2 tonic resistance: no annotated key (ruling above).
  - R03-I1 melody transport, and R05-L2 melody range (already killed): no melody track.
  - W01-J6c: needs MusicLab.
  - R02-breadth: needs genres per version.
- **Qualified but not run (ninth of nine):** R03-G3 p_min (ruling above).
- **Merged into a killed test:** R03-G1, shuffle-relative curvature, was merged into R03-L1 (killed in run 03) and is repetition renamed. Run 05 and run 06 left it out, and so do I.
- **Retired or waiting:** W01-J4 is retired. W01-J6b, the McGill hold-out, waits and is untouched.
- **Failed earlier and not reopened:** every idea marked `failed` in `ideas.json`.

## Gates, checked on the notes alone
Split-half compares the first half of the first file's bars and chords with the second half (Spearman). The residual is each half's measure after that half's ch_rep, V, ln_chg and ln_bars. Overlaps are within-artist rank correlations on the 5,901 songs. The thresholds are written before any outcome: stability ≥ 0.20, renaming |ρ| ≤ 0.7 with ch_rep, V, ln_chg and ln_bars.

| Measure | Brainstorm split-half / residual | Chair split-half / residual (5,901) | Largest renaming overlap, brainstorm | Chair (within artist) | Verdict |
|---|---|---|---|---|---|
| ch_rep | 0.75 (two files 0.78) | 0.742 / 0.313 | | V −0.598 | the battery primary (no gate) |
| H4m | 0.52 (Skeptic's form), 0.615 (Listener's) / 0.56 | 0.582 / 0.504 | V −0.28 | V −0.263 (cv_w −0.205) | passes |
| g | 0.53 / 0.44 | 0.447 / 0.371 | ch_rep −0.35 (Skeptic −0.27) | ch_rep −0.279 | passes |
| CH | not in the brainstorm | 0.619 / 0.610 | | ch_rep +0.071 | passes |
| A | not in the brainstorm | 0.704 / 0.666 | | V +0.159 | passes |
| lnP | 0.454 / 0.417 | 0.457 / 0.409 (4,832 pairs) | ln_chg −0.275 | ln_chg −0.154 | passes |
| F | 0.897 / 0.81 | 0.888 / 0.785 | ln_chg −0.35 | ln_chg −0.339 | passes |
| B | 0.626 / 0.386 | 0.631 / 0.436 | V +0.59 (Skeptic +0.48) | V +0.466 | passes |
| p_min (R03-G3) | clips: 0.154 residual (failed, run 03) | 0.530 / 0.311 (on the size block) | | V −0.656; R² on the size block 0.615 | passes; ninth, not run |
| Ht (G1) | 0.70 / 0.59 | | ch_rep −0.39 | | withdrawn |
| R (G2) | 0.28 / 0.27 | | ≤ 0.11 | | withdrawn |
| Hm (I1) | 0.307 / 0.256 | | ch_rep −0.23 | | withdrawn |
| Nfr (L3) | 0.485 / 0.24 | | ch_rep −0.63 | | withdrawn |

Fame, era and genre (the Skeptic): every measure has |ρ| ≤ 0.07 within artist with hotttnesss, the Billboard flag, year, year-known and the number of files.

## Power, plainly
`power_fake.py` runs `common.fake_power` on each test's real rows and columns:
- **Fake outcomes:** artist baselines Beta(0.25, 1.0), which is base rate 0.20 with run 06's calibrated precision of 1.25, and y ~ Bernoulli(baseline + β/100 · z).
- **What counts as a pass:** p < α, the predicted sign, and the same sign in both halves. The logit is not simulated.
- **Draws:** 300 under the prediction and 150 under zero. With 300 draws, a power of 0.01 is uncertain by about ±0.006.

| Test | SE (pp) | Pass rate if the prediction is true, at .00625 | at .05 | Kill fires if true | Kill fires if 0 |
|---|---|---|---|---|---|
| lakh_repetition (+1.0) | 1.03 | 0.007 | 0.077 | 17% | 50% |
| lakh_repetition at the Skeptic's +0.4 | 1.03 | 0.000 | 0.033 | | |
| tree_h4m (−0.5) | 0.72 | 0.003 | 0.043 | 24% | 50% |
| spectral_gap (−0.3) | 0.67 | 0.007 | 0.033 | 33% | 50% |
| lakh_chirality (−0.6) | 0.57 | 0.000 | 0.083 | 24% | 64% |
| lakh_arrow (+0.6) | 0.58 | 0.013 | 0.107 | 15% | 50% |
| loop_period (+0.6) | 0.60 | 0.023 | 0.123 | 16% | 50% |
| burstiness (+0.3) | 0.74 | 0.000 | 0.043 | 34% | 50% |
| triad_fidelity (+0.5) | 0.80 | 0.003 | 0.043 | 27% | 50% |

- **Tonight's battery is blind.** Even if every prediction is exactly true, the chance that any one of the eight passes is about 6%. Splitting .05 eight ways costs about ten-fold: the pass rate at .05 is 0.03 to 0.12, at .00625 it is 0.00 to 0.02.
- **ch_rep's SE is 1.03 pp**, because ch_rep is collinear with V (−0.60 within artist). That SE is about what run 06's 1,295 fresh songs gave, not the 0.4 hoped for from 5,901 songs. Its +1.0 needs about five times as many songs for a pass at .05 to become likely (an SE near 0.45).
- **Kills are weak evidence.** A "wrong side of zero" kill fires half the time when the effect is zero and 15% to 34% of the time when the prediction is true, so it moves the odds by a factor of 1.5 to 3. Chirality's −0.2 line fires 64% of the time under zero and 24% when the prediction is true.
- **Against the floor:** every test is below run 03's proposed 0.5 power floor. That floor is Jason's undecided proposal, so power is printed and does not block. The run 06 first-principles flag (count only tests with power ≥ 0.2) would count none of them tonight.
- **The real base rate is unknown.** Run 06's fresh uptake was 17%. A lower rate lowers power further.

## Practical notes for the experimenters
- **Commit first, without running anything:**
  - the eight `PREDICTION.md` files and their `test.py` files;
  - `experiments/common.py` and `lakh_notes.py`;
  - `power_fake.py`, `power_fake.json`, `chair_gates.py`, `chair_gates_report.py`, `chair_gates.json`;
  - this file.
  
  The guard refuses unless the folder's PREDICTION.md and `common.py` are committed and unmodified.
- **Then run each `python3 -I <folder>/test.py`** (about a minute each, plus a minute of power). The first guarded call builds `/home/claude/dl/lakh/outcomes_run07.json` from the reduced Discogs-VI files, and later tests read that cache.
- **`ideas.json` has no R07 entries yet.** The brainstorm says they were added, but they are not there. Add R07-G1 to R07-I3 with their statuses (G1, G2, I1 and L3 withdrawn; L1, G3, L2, I2 and I3 testing), set R02-gap and R03-G3 to the rulings above, and record R03-I2 as "not testable on Lakh (no key)".

## Ranking
Nine qualified; the first eight run tonight.
1. `lakh_repetition`: the standing prediction and the longest-running lean (runs 04 and 06 both positive).
2. `tree_h4m`: the pass's mathematics, the merged idea of all three imaginers, and nearly orthogonal to repetition (ρ −0.04).
3. `spectral_gap`: Jason's S, the second mathematics; parked since run 02 and never yet tested on an outcome.
4. `lakh_chirality`: run 06's new mathematics, unsettled; the first whole-song reading.
5. `lakh_arrow`: run 05's lead, which faded on run 06's fresh songs.
6. `loop_period`: new, with clean gates; its author says report only.
7. `burstiness`: new; mostly vocabulary and length even after controls.
8. `triad_fidelity`: the strongest gate, but likely reads the arranger.
9. *(not run)* R03-G3 p_min: qualified, but waits for an independent batch.

## Data and credit
- Lakh MIDI Dataset (Raffel 2016) and the Lakh Pianoroll Dataset (Dong et al. 2018; Zenodo 5646574), CC BY 4.0.
- Million Song Dataset metadata (Bertin-Mahieux et al. 2011) via Gold-Caps LMD-matched (Jonason, Casini & Sturm 2023; Zenodo 10178563), CC BY 4.0.
- Billboard flags from Hit Song Prediction (Zangerle et al. 2019; Zenodo 3258042).
- Hooktheory via Sheet Sage, CC BY-NC-SA 3.0, used only to exclude songs already seen.
- Discogs-VI (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0, the outcome, to be joined only after commit.
- Cards: Gilbert & Yim, arXiv:2412.05746; Perea & Harer, FoCM 2015, arXiv:1307.6188.
