# Run 06: the chair's picks

26 November 2026. Research only; nothing goes into the Luthier engine. The yardstick is unchanged: lasting love plus covers by other artists. Jason's rule applies: every idea that can be tested tonight on the data at hand is tested, and every counted test shares one threshold.

No outcome was opened before the rules were frozen: not `hooktheory_covers_discogs.json`, not `discogs_versions_matched.json`, nothing in `/home/claude/shape/` (the reduced Discogs-VI files were listed by name, never read), no covers, versions or first years, and no fresh song was matched to Discogs. My checks used the notes only (`experiments/common.py`, `experiments/power_fake.py`; scratch in /tmp/claude-0/r6/chair). **Run 06 does not touch the McGill hold-out.** Song 59, songs/p69 and studies/holdout59 were not read.

## What changed tonight
- **Fresh songs.** The raw Hooktheory file holds 1,946 songs that are not in the data pack, mostly clips with chords but no melody. Their outcomes have never been joined to anything. 1,295 of them are by 601 artists with another song, so they can enter a within-artist model.
- **The fresh outcome can be built.** Discogs-VI's `main.zip` is on disk and has been reduced by the maintainer's own script, so the fresh songs can be matched by the maintainer's own rule once the tests are frozen.
- **statsmodels 0.15 is installed**, so the conditional logit runs as written.

## Tonight's tests: six folders

**Each test needs p < .05/6 = .00833 (two-sided, z 2.638)**, plus the predicted sign, the same sign in both artist halves (md5 of the artist slug) and a converged conditional logit of the same sign. The threshold does not move if a test is stopped.

| Folder | Idea | Rows (fresh) | Prediction on y_foreign | Kill | Power at .00833 |
|---|---|---|---|---|---|
| `chirality/` | R06-I1, harmonic chirality CH (the Inventor; Green's theorem on the Hodge cycle part) | 8,774 seen | **−0.6 pp per SD** | above −0.2 | 0.15 |
| `fresh_repetition/` | R04-FV and R06-L3, chord repetition on fresh songs (battery primary) | 5,768 (1,295) | **+1.0** | ≤ 0 | 0.035 |
| `fresh_arrow/` | R05-A, the arrow of time on fresh songs | 4,920 (888) | **+0.6** | ≤ 0 | 0.02 |
| `fresh_tonic/` | R03-I2, tonic resistance on fresh songs | 5,144 (997) | **−0.6** | ≥ 0 | 0.03 |
| `fresh_range/` | R05-L2, melody range (capped at three octaves) on fresh songs | 4,746 (404) | **−0.7** | ≥ 0 | 0.014 |
| `fresh_diatonic/` | R04-G1, diatonicity holding the fifths path, on fresh songs | 5,707 (1,235) | **+0.5** | ≤ 0 | 0.015 |

One test is mathematical in the strict sense and new: `chirality`, the signed area a progression sweeps on the circle of fifths. It is the only proposal tonight that survived its own author, the Skeptic and the gates, and the only one that can tell a song from the same song played backwards. `fresh_tonic` (effective resistance) and `fresh_diatonic` (a Fourier coefficient) carry older mathematics onto new songs.

### The shared models
- **`chirality`:** run 04's 9,588 within-artist seen rows (`run05 common.load_rows()`); y_foreign by run 05's `load_outcomes`; columns z(CH), z(A), z(ch_rep), z(ch_ic_mean), V, ln_chg, run 04's block, artist fixed effect; LPM with CR1 by artist; the same in each half; conditional logit as a sign check.
- **The five fresh tests** (frozen once, in `experiments/fresh_repetition/PREDICTION.md`; code in `experiments/common.py`): one LPM with artist fixed effects on seen and fresh songs together, restricted to artists with at least one fresh song and two songs in all. The measure enters twice, z × fresh and z × seen, so **the tested slope comes from fresh outcomes only**. A fresh main effect is in. z uses the mean and SD of the 9,588 seen rows. Controls are only those computed identically for seen and fresh songs: run 04's block, ln_chg, V, has_mel.
- **The fresh outcome:** the maintainer's match (title and artist), keyed by (artist slug, song slug), on the maintainer's reduction of Discogs-VI; y_foreign by run 05's rule on the clique's version sets. Seen rows take their outcomes from the data pack. **A validation step runs first** and must reproduce the data pack's keys, cliques, version sets and seen y_foreign for 99% or more; if it fails, the five fresh tests stop.

## Merges and rulings
- **The Skeptic's merges stand.** λ, P, D and β₁ are one idea ("one loop, not many"), mostly the number of distinct chords. Its last form, λ, was withdrawn by its author. β₁ʰ was withdrawn. A\* is A renamed. The tonic downhill H is the clip boundary.
- **CH runs in the open-walk form** the Inventor froze in round 2. It adds no boundary edge, which answers the Skeptic's warning that the wrap move is new in 35% of clips. The wrapped form (ρ 0.92) is reported only. Unit values were reproduced, including the Inventor's wrapped +0.133 for I–V–vi–IV.
- **One threshold for all six.** The Listener and the Skeptic wanted the ch_rep fresh test one-sided at .05. Jason's rule shares the threshold among counted tests, so it is two-sided at .00833 like the rest. Its kill line stays theirs (β ≤ 0).
- **The fresh kill lines are "wrong side of zero".** With SEs of 0.85 to 1.8 pp, a +0.2 line would mean nothing. The cost is plain in the power table: such a kill fires about half the time when the true effect is zero and a quarter to a third of the time when the prediction is true. So a fresh kill is weak evidence, a factor of about two.
- **Counted or reported.** A, melody range, tonic resistance and diatonicity have each been read on the seen songs before; tonight's fresh songs are new data for them, so each is tested and counted. **CH on the fresh songs is reported only**, with its sign frozen: CH's counted test tonight is the seen one, and a second counted look at the same idea on the same night would only lower the bar for everyone. **W01-J6a, early covers**, is reported only (early and late uptake beside every fresh test), as run 02 ruled: both are printed and nothing is decided on their contrast.
- **R03-I2 (tonic resistance): tested.** Run 05's first principles recommended retiring it, but retirement is Jason's call and he has not made it. His standing rule says a testable idea is tested, and the fresh songs are data it has never met. It is ranked low. If Jason retires it, the test is moot and the threshold stays as frozen.
- **R04-G1 (diatonicity): tested.** It was parked in run 04 for exactly this, "kept for fresh songs, holding the fifths path and the non-triad share". The fifths path was killed in run 05 and deletion of the pair was recommended; Jason has not ruled. It runs in its author's form, ranked last. The non-triad share had never been defined, so I froze it: the share of chord duration on events that are not plain major or minor triads.
- **ch_ic_mean and mel_ic_mean are left out of every fresh model.** They are scores from the pack's corpus models, trained on the seen clips, so a fresh song cannot be scored identically. They are left out of seen and fresh rows alike, so the columns match. They stay in `chirality`, which uses seen songs only.
- **Melody range is capped at 36 semitones for its fresh test.** L2 has transcription artefacts (a seen maximum of 1,030 semitones; SD 17.5 against a median of 11). On about 400 fresh songs, a fake null run on the uncapped measure came out significant 14% of the time at .00833. Rows above three octaves are dropped, seen and fresh alike (3.0% of seen rows, 9 fresh rows), and z uses the capped SD (5.45). This was decided on the notes alone. Run 05's uncapped form is reported.
- **The fresh rows.** A fresh clip counts only if it has chords (every pack clip has chords and melody). One fresh song duplicated a seen song under another slug and was dropped. The 530 fresh songs whose artist has no other song are not used: the design is within artist, and last night's across-artist reading of A was what reversed.
- **Do not use `studies/judging_data/hooktheory_clips.json.gz`.** Its clip set is the set of matched videos, so it is an outcome. (The pack's covers file was built over every raw video, so it may already list some fresh videos; the validation counts them and nothing else reads them.)

## Left out, and why
- **Withdrawn by their authors tonight:** G1 holes β₁ʰ (residual stability 0.18 seen, 0.15 fresh, once loops, distinct chords and length are held); G2 cycle rank β₁ (mostly the number of distinct chords; merged into λ); G3 A\* (A renamed, ρ +0.78; fresh stability 0.18); L1 one-loop share λ (residual stability 0.146; its author allowed it to be reported only, and I attach it to no test, since a printed outcome coefficient on a measure that fails its gate reads noise); L2 tonic downhill H (67% clip boundary; residual 0.16); I2 orbit purity P (λ again, ρ −0.90 with β₁).
- **Stopped on the notes (no outcome joined):**
  - the Hodge gradient share g: all three imaginers proved independently that for one walk it is the unit current from the first chord to the last, ‖G‖² = R_eff(first, last), so it reads only where the clip starts and ends (stability 0.19 seen, 0.10 fresh);
  - entropy production σ: raw σ is A renamed (+0.89); the debiased form is A plus repetition; the two-way-edge form has stability 0.17;
  - the heat engine (Lévy area of melody height against home-ness): stability 0.06;
  - melodic holonomy η: 0.152;
  - the harmonic energy share h (its stable part is β₁ʰ), the dominant-cycle share D (β₁ renamed, ρ −0.86) and the curl dimension (0.20, borderline; not proposed).
- **Stopped at a gate in earlier runs (kept stopped):** R02-gap (0.17), R03-G3 the obtuse statue (0.154), R03-I1 melody transport (0.195). Rerunning a failed gate on new songs until it clears would make the gate a fishing step.
- **R03-G1, shuffle-relative curvature:** repetition renamed (ρ −0.62 with ch_rep); left out as in run 05.
- **R05-L3, contour surprise:** withdrawn in run 05 (it measures how repeated notes were transcribed).
- **Retired earlier:** W01-J4. **Waiting on a pass:** W01-J6b, the McGill hold-out (`experiments/HOLDOUT_LOG.md`).
- **Data not on hand** (`DATA.md`): W01-J6c MusicLab; R02-breadth (genres per version); a real fame measure; enough fresh songs for a powered confirmation.

## Gates, checked on the notes alone

| Measure | Two clips agree (≥ 0.20), seen | Fresh (reported) | Largest overlap (≤ 0.7) | Verdict |
|---|---|---|---|---|
| CH (open walk) | 0.252 (3,294 pairs) | 0.246 (253) | ch_ic_mean −0.141 (A +0.07, V −0.12) | passes |
| ch_rep | the pack's measure; no gate | 0.395 (432) | | |
| A | 0.302 (3,294) | 0.244 (253) | ln_chg −0.154 | passes (run 05) |
| H (run 03's residualised gate) | 0.203 (3,512) | 0.182 (243) | beats −0.081; size R² 0.16 | passes, narrowly (run 05) |
| L2 | 0.290 (4,271) | 0.396 (52) | mel_ic_mean +0.555 | passes (run 05) |
| D5 given FP and NT (new form) | 0.342 residual (4,268); raw 0.503 | raw 0.395 (432) | ch_ic_mean −0.423 (FP −0.73, held as a column) | passes |

Every measure was recomputed tonight from the raw notes by `experiments/common.py` and reproduces run 05's counts and percentiles exactly (A 8,774; H 9,009, 0.624 / 0.818 / 1.143; FP 0.449 / 0.714 / 1.197; L2 7 / 11 / 21). The fresh-song chord tokens reproduce the pack's ch_rep, n_ch, n_mel and beats on all 21,998 pack clips with no difference.

## Power, plainly
**How it was computed** (run 05's first principles asked for fake outcomes, since the notes-side bound overstated SE by a third): `experiments/power_fake.py` simulates y ~ Bernoulli on each test's real rows and columns, 1,000 draws with the predicted effect and 1,000 with none. "Homogeneous" gives every song 22%. "Calibrated" spreads artist baselines (Beta, precision 1.25) so that run 05's arrow design yields the SE run 05 actually observed (0.40 pp). The pass rate includes the halves rule, not the logit.

| Test | SE, calibrated / homogeneous (pp) | Pass rate if true (calibrated) | Power at .00833 / at .05 (calibrated) | Kill fires if true | Kill fires if 0 |
|---|---|---|---|---|---|
| chirality | 0.38 / 0.51 | 0.135 | 0.15 / 0.35 | 15% | 71% |
| fresh_repetition | 1.21 / 1.63 | 0.034 | 0.035 / 0.13 | 22% | 48% |
| fresh_arrow | 1.06 / 1.43 | 0.022 | 0.02 / 0.09 | 28% | 48% |
| fresh_tonic | 0.85 / 1.12 | 0.042 | 0.03 / 0.11 | 26% | 48% |
| fresh_range | 1.78 / 2.45 | 0.021 | 0.014 / 0.07 | 35% | 52% |
| fresh_diatonic | 1.12 / 1.50 | 0.019 | 0.015 / 0.07 | 33% | 49% |
| CH on fresh (reported) | 1.06 / 1.44 | | 0.02 / 0.09 | | |

- **The fresh tests are nearly blind.** The brief warned of this (SE 1.3 to 1.7 pp). The fresh y_foreign rate is unknown and may be below 22%, which would lower power further.
- **Against the floor:** every test is below run 03's proposed 0.5 floor, which is Jason's undecided proposal; power is printed and does not block.
- **What to expect:** a pass is unlikely even if every prediction is true. `chirality` is the only test whose kill line is informative (it fires 71% of the time under no effect, 15% under the prediction).

## Practical notes for the experimenters
- **Commit first:** the six PREDICTION.md files, `experiments/common.py`, `experiments/power_fake.py` and `power_fake.json`. The loaders refuse unless the test's PREDICTION.md, `fresh_repetition/PREDICTION.md` (for fresh tests) and `common.py` are committed and unmodified.
- **Run the validation once, first** (`common.validate_match`, called by `common.load_battery_outcomes`; it caches `experiments/match_validation.json`). If it fails, the five fresh tests record "stopped (validation failed)" and `chirality` runs without its fresh reading.
- **The fresh list is rebuilt from the notes** by `common.fresh_songs()` (it asserts 1,946 songs and 2,570 clips), so /tmp/claude-0/r6/fresh_songs.json is not needed.
- **Runtime:** measures for all 13,198 seen and 1,825 fresh songs take about 25 seconds; the power script about 45 seconds. The validation reads the 100 MB clique file and the 114 MB versions file once.
- **Each PREDICTION.md gives unit values** the script must reproduce before anything else.

## Ranking
Six qualified, fewer than eight, so all run tonight. If an order is wanted, by power and novelty:
1. `chirality` (new mathematics, the only test with real power)
2. `fresh_repetition` (the battery's primary; the longest-standing lean)
3. `fresh_arrow` (run 05's best lead)
4. `fresh_tonic`
5. `fresh_range`
6. `fresh_diatonic`
