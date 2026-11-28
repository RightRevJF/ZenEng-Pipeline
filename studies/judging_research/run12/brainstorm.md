# Run 12: the brainstorm

28 November 2026, the 10:17 ET pass. Round 1: three imaginers (fixed stances), each up to three new methods. Round 2: the Skeptic's critique, then each imaginer's answer. No imaginer or the Skeptic opened an outcome. Context: brief_for_agents.md; cards 1-2.


---

## Run 12, round 1: the Geometer

## R12-G1 FIFTHS: Parseval split of REP on Z12 (repo geometry: Amiot's DFT, R04-G1)
**Mechanism.** Concentration is a sum of six Fourier energies; only the fifths axis marks a well-formed scale, so learnability should live there.
**Measure** (`m_geometer.py`; no tonic, no settings). Let p be the duration-weighted melody pitch-class distribution and f_k = Σ p_j e^(−2πijk/12). Parseval gives C = 12Σp² − 1 = 2Σ_{k≤5}|f_k|² + |f_6|². Define E5 = 2|f5|² and REST = C − E5.
**Data.** Hooktheory 9,588 (seen); Lakh skyline.
**Prediction.**
- Hooktheory: E5 with REST held, **+0.025** (+0.015 to +0.035). REST with E5 held, 0 to +0.01.
- Lakh: E5, +0.02.

**Why** (extrapolation). Among k-note sets, |f5| peaks on the maximally even, fifth-generated ones, pentatonic and diatonic (Clough–Douthett). With Myhill's property, each note's place is audible, so the tune is easier to sing back.
**Kill.** +0.025 lies outside β ± 1.96 SE, or REST outweighs E5.

## R12-G2 PRED: Gaussian predictive information (vector 2)
**Mechanism.** What the past tells about the future beyond the last note.
**Measure.** For a stationary Gaussian process, I(past; future) = −½ Σ k ln(1 − α_k²), where α_k are the partial autocorrelations (Ibragimov–Rozanov). Apply it to the Lakh skyline, the highest pitch of tracks 1, 2 and 4 per eighth (run 11's `lines`). Compute α_k by Levinson–Durbin with K = 32 (4 bars) and subtract the noise bias K(K+1)/4n.
**Data.** Lakh, 5,901 songs.
**Prediction.** **+0.02**, holding skyline entropy, innovation variance and length. ρ(PI, entropy) = −0.23, so "fewer notes" is mostly not learnability: entropy's β should shrink by under 10% when PI enters.
**Kill.** +0.02 lies outside the range. Separately, a shrink of 25% or more kills the "mostly not" answer.

## R12-G3 THIN: lasting beyond fitness (card 1, Freeman–Jordan §6; vector 1)
**Theorem.** Affine attachment condenses only if E[R] > 2 + α. With A → 2×10⁶, nothing condenses: there are no waves, and covers follow Poisson(η·g·h). Derived from the brief's summary:
1. FIT = ψ(r + n) − ln(r + Λ(first year)). For any notes measure, |β_FIT − β_logcovers| < 0.005; "no better" limits the estimator, not the notes.
2. Given n, the late share (covers after age 15) is Binomial(n, Λ_late/Λ), with η absent.

**Test.** Use E5 and REP. Fit a binomial GLM of the late share, with offset logit(Λ_late/Λ) from the frozen g and h, artist effects, and songs with n ≥ 2 (compare R08-G3).
**Prediction.** 0 ± 0.05 log-odds per SD. Waves would give E5 +, REP −.
**Kill** (of the no-waves reading). 0 lies outside β ± 1.96 SE.

## Checks (notes only; about 1 minute of compute)
**Hooktheory clips.** Stability is clip 1 vs clip 2; R² is on the 13 baselines.

| Measure | Stability | Main overlap | R² |
|---|---|---|---|
| C | 0.33 | pc_entropy −0.97 | 0.95 |
| E5 | 0.31 | pc_entropy −0.61 | 0.45 |
| REST | 0.27 | pc_entropy −0.85 | 0.86 |

- E5 with entropy and n_pc held: stability 0.20.
- Power for E5 (REST held, +0.025, α .05/6): 0.21. The fake outcomes have no artist share, so the real power is higher.
- Predictive information on clips: stability 0.16, stopped.

**Lakh** (`lakh_geometer_check.py` → `/home/claude/dl/run12/geometer_lakh_check.json`). Stability across 155 arrangement pairs, near-duplicates removed:

| Measure | Pair stability |
|---|---|
| Skyline entropy | 0.59 |
| E5 | 0.56 (0.50 with entropy held) |
| PI | 0.50 (with controls held) |
| Texture E5 | 0.75 (P11-5's best invariant) |

Overlaps: E5–entropy −0.71; PI–ch_rep +0.34.

---

## Run 12, round 1: the Listener

28 November 2026. Stance: expectation, surprise, memory, exposure; what makes a musician want to learn a song by ear. **No outcome was opened** (no `load_outcomes`, no covers, FIT, HOLDOUT or `data/*.json` file; `fitness/fit.json` not opened). Notes-side checks only, about 2.5 minutes of compute. Code: `run12/experiments/measures/m_listener.py` (clips), `run12/experiments/measures/lakh_listener_pi.py` (Lakh; writes only `/home/claude/dl/run12/listener_pi_lakh.json`).

## Proposals (about 400 words)

**L12-1 PI3: the past tells the future (physics vector 2; Lakh whole songs).**
- *Mechanism.* Worth learning when the first minute pays for the rest: the hook returns.
- *Mathematics (Bialek, Nemenman & Tishby 2001; prediction is extrapolation).* S(N) ≈ hN + E: h is paid on every note, E is learned once. Subadditivity gives I(past_L; future_L) ≤ H(L) ≤ L·H1, so few pitch classes cap both: REP is a confounded read. Lasting songs should have high E at a given h.
- *Measure.* PI3c = 2H(3) − H(6) on skyline pitch-class events, minus its 10-shuffle mean. *Data:* 5,275 of run 07's Lakh songs (seen; no melody measure joined).
- *Prediction.* **+0.03** SD of y_foreign per SD, within artist, H1 and lnN held. Subsumption: the notes say **no** (within-artist r with H1 −0.29, R² on H1 + lnN 0.06), so H1 keeps at least two thirds of its coefficient with PI3c held.
- *Kill.* +0.03 lies outside β ± 1.96 SE.

**L12-2 PIC: the exposure-trained ear's context gain (vector 2; Hooktheory clips).**
- *Mechanism.* Clips are too short for block entropies; the corpus-trained ear stands in: how much do the last two notes tell about the next?
- *Measure.* Mean log2 p(d_t | d_t−2, d_t−1) − log2 p(d_t); Witten-Bell trigram on scale degrees, song left out. *Data:* 9,544 Hooktheory songs.
- *Prediction.* **+0.03**, ln_notes and pc_entropy held (reading: mel_ic_mean too).
- *Kill.* As L12-1.

**L12-3 Late wins (vector 1; card 1 Thm 2.6, card 2 Prop. 3.1).**
- *Mathematics (extrapolation).* The frozen fit finds no rich-get-richer (A → ∞): card 2's α = 0 case, where with K ≥ 2 popularity order converges almost surely to quality order; card 1's leaders fall only to fitter newcomers. So quality should show more in late covers than early ones.
- *Not FIT vs counts:* they correlate 0.985.
- *Which notes property.* One a coverer judges by ear, surviving re-arrangement: PI3c and H1 are stable between arrangers (0.65, 0.78); MIDI chord repetition agrees with Hooktheory's only 0.32.
- *Measure.* REP, PIC and PI3c. The outcome is z log(1 + covers at age ≥ 15), with covers at age ≤ 5 and first year held, on songs released by 2005.
- *Prediction.* REP **−0.03**, PIC and PI3c **+0.03**. On early covers alone, |β| ≤ 0.02.
- *Kill.* Prediction outside the range; "exposure, not quality" if |β_early| exceeds |β_late| by over 1.96 SE (artist bootstrap).
- *Power.* About 0.1 on ~1,700 Hooktheory songs (SE ~0.03): an estimate, unless frozen `fitness.py` (settings fixed) is applied to Lakh's Discogs groups and pooled.

## Check numbers (notes only)

| Key | Data | Songs | Stability | Largest overlaps | R² | Power (checks11) |
|---|---|---|---|---|---|---|
| **PI3c** | Lakh | 5,275 | **0.646** between two MIDI files (196 songs) | within artist: H1 −0.29, ch_rep −0.11, lnN +0.15 | 0.06 on H1 + lnN | — (Lakh SE about 0.017 in run 11; power about 0.2 at +0.03, α .01, my arithmetic) |
| **PIC** | clips | 9,544 | **0.273** clip 1 vs 2 (4,219) | mel_ic_mean −0.63, leap_share −0.59, step_share +0.41, int_entropy −0.38 | 0.47 on 13 | 0.29 at +0.03, ln_notes and pc_entropy held (fake SE 0.0135) |
| PIC_REL | clips | 9,544 | 0.293 | mel_ic_mean −0.68, leap_share −0.60 | 0.50 | 0.24 |

Power in the last column used 100 draws at α .05/6, without an artist share, so it is understated (run 11's lesson).

For reference, on Lakh: H1 has arrangement stability 0.781 and lnN 0.698.

**Dropped on the notes.** Each was tried in this pass.

| Key | Why dropped | Figures |
|---|---|---|
| PI1C (own-clip adjacent MI, shuffle-corrected) | unstable, and renames mel_rep | stability 0.184; mel_rep +0.66; R² 0.54 |
| Lakh PI2c | renamed by note count | lnN +0.54 within; R² 0.63 |
| Lakh E3c (finite-L excess entropy) | renamed by note count | lnN +0.49; R² 0.43 |
| Lakh PI4c and KEFF (PI4c − PI1c, read as the theorem's (K/2)·log-growth "parameter count") | stable (0.65), but bias-driven | correlation with H1 flips from −0.29 at L = 3 to +0.23 at L = 4 (8-grams saturate at log N) |
| Grid readings PIg4c / PIg8c (eighth grid with holds) | renamed: they carry duration | stability 0.59 / 0.68; PIg8c within-artist +0.33 with H1, −0.30 with ch_rep |

So L = 3 is the one window that is neither renamed nor saturated.

## Exact recipes

**PI3c (Lakh, `lakh_listener_pi.py`)**
1. *Skyline.* At every 12th step (an eighth note), take the highest pitch sounding on tracks 1, 2 and 4. Trim to the span from the first sounding step to the last.
2. *Events.* Drop rests and merge consecutive equal pitches. Map each event to pitch class mod 12. Block entropies are invariant to relabelling, so no key is needed.
3. *Block entropy.* H(L) is the plug-in entropy, in bits, of the overlapping L-blocks.
4. *PI3c.* Compute 2H(3) − H(6), then subtract the mean of the same quantity over 10 permutations of the events. The RNG seed is int(md5[:8], 16).
5. *Bounds.* A file needs at least 128 events. The song value is the mean over its files.
6. *Fixed choices, none fitted.* Skyline tracks, eighth grid, L = 3, 10 shuffles.

**PIC (clips, `m_listener.py`)**
1. *Sequence.* Scale degree (pitch − tonic) mod 12, repeat-free.
2. *Corpus.* Counts from every raw clip with a melody, minus all clips of the scored song.
3. *Model.* Unigram with add-one smoothing. Bigram and trigram use Witten-Bell interpolation: p = (c(h,x) + T(h)·p_lower)/(c(h) + T(h)).
4. *Score.* Mean over t ≥ 3. PIC_REL = PIC divided by the mean unigram surprisal.
5. *Song value.* As `C.song_values`.

**Commands run**
- `python3 lakh_listener_pi.py` (39 s)
- `cd run11/experiments && python3 checks11.py ../../run12/experiments/measures/m_listener.py 0.03 ln_notes,pc_entropy` (48 s, run twice)

## Against my own sign (labelled)
High PI3c is also the signature of copy-pasted choruses in a MIDI file. Arrangement stability of 0.65 says it is mostly the song's property, but not wholly. If covers reward "room to move", the sign could be negative. +0.03 is written down so that it can be killed.

---

## Run 12, round 1: the Inventor (carrying vector 1)

No outcome was opened. Check scripts are in `run12/experiments/measures/inventor_*_check.py`, and their output is in `/home/claude/dl/run12/inventor_*_check.json`.

**Two facts first, both read from fitness.py and fit.json. They rule out the obvious test.**
- With A = 2×10⁶, E_i depends on first year alone. So within a year, FIT is a strictly increasing function of N, and z(FIT) − z(log1p N) given year is only digamma(r+N) versus log(1+N) curvature. It contains no luck. I drop it as an outcome.
- At about 30 covers per song (78,008 / 2,627), the model's only remaining luck, Poisson noise, leaves trigamma(r+N)/trigamma(r) of the variance in log η. That is 0.011 at N = 30 and 0.062 at N = 5. Counts are already the fitness, so a "notes beat counts" horse race has almost no power.

The luck the model cannot see is a boost that does not scale with fitness: the original's launch.

## I-1 PROP: fitness is proportional; luck is front-loaded
**Grounding.** A → ∞ makes the frozen model a gamma-mixed Poisson process. That is card 2's α = 0 urn with a uniform menu, where Prop 3.1 gives counts converging to quality order. Given η, covers in disjoint age windows are independent Poisson processes with rate η·g·h.
- A fitness effect therefore multiplies every window equally.
- A launch or fame effect sits only at age 0 to 3, where g peaks at 1.5.

**Extrapolation.** Read through Freeman–Jordan with uniform sampling, a song at quality quantile q wins with probability ∝ q^(R−1). The fitted shape r = 0.66 then implies R ≈ 2.5, or 2.8 if matched on var log η instead. In words, each cover is the best of two or three songs the coverer weighed.

**Recipe.**
- Songs with t0 ≤ 2005.
- N_E = covers at ages 0 to 3; N_L = covers at age 8 and over.
- Offset log Σ_w g·h, taken from fit.json. No new settings.
- Artist fixed-effect Poisson regression per window, on z(REP) and, separately, z(ch_rep), with five-year first-year dummies.
- Statistic: Δ = β_L − β_E. A second reading gives β_L with log(r + N_E) held.

**Prediction.** REP: β_L = β_E ≈ −0.05 log-rate per SD, so Δ ≈ 0. ch_rep: the same size, with its run 04-06 sign.

**Kill.** Killed if −0.05 lies outside β_L ± 1.96 SE. The measure "reads launch, not fitness" if Δ < 0 at p < .05 against the predicted sign.

## I-2 ROUGH (P11-4)
**Mechanism.** Overtones beating within a critical band are a physical cost, and voicings that beat less travel further.

**Recipe** (Sethares 2005 code):
- Tracks 1 to 4, sampled every beat, distinct pitches only.
- Partials n = 1 to 6 at n·f₀, amplitude 0.88^(n−1).
- For each pair of partials: d = min(a, a′) · 5 · (e^(−3.51 s Δf) − e^(−5.75 s Δf)), with s = 0.24 / (0.0207 f_low + 18.96).
- ROUGH = Σ_beats Σ_pairs d / Σ_beats C(n, 2), i.e. roughness per sounding pair.

**Data.** Lakh, 5,901 songs, within artist.

**Prediction.** −0.02 SD per SD on y_foreign, measure bare. Range kill.

**Check.**
- Two-file stability 0.53, or 0.43 after dropping 31 near-duplicate pairs.
- Within-artist variance share 0.44.
- Overlap with ch_rep, ln_bars, notes per beat and PCE: |ρ| ≤ 0.12.
- The density-kept version, ROUGH_BEAT, has ρ = 0.92 with notes per beat, so it is rejected.

## I-3 CANAL (P11-5): Waddington canalization
**Mechanism.** A fit genotype keeps its phenotype across environments. In the same way, a song that survives two arrangers survives forty coverers.

**Recipe.** CANAL = 1 − min over 12 rotations of JSD(bits) between the two files' duration-weighted pitch-class profiles (tracks 1, 2 and 4). No settings.

**Pilot results** (156 non-duplicate pairs):
- Median 0.988 (10th to 90th percentile: 0.929 to 0.998).
- 85% of pairs are in the same key.
- ρ with PCE is +0.19, so this is not simplicity under another name.

**Prediction.** Within artist, +0.03 SD on y_foreign. This waits for more pairs: 156 is too few, so for now it is a pilot only.

**Kill.** Range kill. On the notes side, it fails if two-file stability against a third file falls below 0.2.

**Lakh arranger stability (notes side).** PCE over all tracks 0.78 (non-duplicate pairs), skyline PCE 0.67. PCE has ρ = −0.54 with ch_rep, so REP and ch_rep partly overlap.

---

## Run 12, round 2: the Skeptic

No outcome opened. The Inventor's fit.json is aggregates only: no breach.

**All Lakh tests** hold ln events, notes per beat, active tracks and the number of MIDI files (a fame proxy); near-duplicates count once.

**V1: FIT vs log covers.**
- *Arithmetic.* With A → ∞, E depends on t0 alone. Within a first year, FIT is monotone in N, differing by digamma curvature (the gap from 0 to 1 cover weighs about 2×).
- *Run.* Same rows, exact first-year dummies for both outcomes (coarse bins give FIT free age adjustment). Estimate Δ = |β_FIT| − |β_log| by paired artist bootstrap.
- *Margin.* SE(Δ) is tiny, so "better" needs Δ ≥ 0.01 at p < .05/K.
- *Shows* whether the effect sits at 0 covers versus a few; *cannot show* fitness beyond luck. A kill indicts the estimator, not the notes.

**Merge 1: G3, L12-3 and I-1 are one test.**
- *Design.* Early window ages 0-3, late window 8+. Songs with t0 ≤ 2005; Poisson with artist effects and offset log Σg·h. The statistic is Δ = β_L − β_E, on REP and ch_rep.
- *Settles.* G3 and I-1 predict Δ = 0; L12-3 predicts a stronger late window. This is the only test that sees launch luck.
- *Confounds.* Rival versions in the 1950s-60s and Discogs' undercounted late self-releases. Hold decade × window.
- *Power.* About 0.1: an estimate, unless Lakh groups pool under the frozen fit.

**G1 FIFTHS.** C = E5 + REST, so equal raw coefficients mean C renamed. Wald-test it; z-scores hide it. Hold tonic_share, since dwelling on 1 and 5 inflates |f5|. Stability is 0.20. Hooktheory is re-spent, so Lakh is the honest count (power about 0.1).

**Merge 2: G2 and L12-1 are one family.**
- PI3c is primary (stability 0.65); G2 is a reading.
- G2's grid carries duration: hold mean event length.
- H(6) saturates near log n, so PI3c mostly counts literal repeats (MIDI copy-paste?). Hold the repeated-bar share.
- Shrinkage counts only if H1 alone is nonzero on Lakh. Power about 0.2.

**L12-2 PIC.** Typicality means familiarity, and it rewards scalar steps (mel_ic_mean −0.63). Hold step_share and mel_ic_mean in the counted test.

**I-2 ROUGH.** Reads the arranger's voicing (stability 0.43): octave doublings read smooth, low register rough. Hold tracks, octave-pair share, register and the chord measures. Power about 0.1.

**I-3 CANAL.** 156 pairs, median 0.988, and it tracks transcription care, which follows fame. Pilot only; no K slot.

---

## Run 12, round 2: the Geometer

**G1 FIFTHS: revised.**
- *Counted test:* Lakh, on the skyline, with the Skeptic's Lakh controls held. Hooktheory becomes an uncounted reading.
- *Controls:* add the largest pitch-class share. Lakh has no tonic; on clips, hold tonic_share.
- *Statistic:* E5 and REST enter one model on raw scale, and a Wald test asks whether b_E5 = b_REST, i.e. whether this is just C renamed.
- *Prediction:* b_E5 > b_REST. On the z scale, E5 is +0.02 (+0.01 to +0.03).
- *Kill:* +0.02 lies outside β ± 1.96 SE, or b_E5 ≤ b_REST.
- *Check (clips):* ρ(E5, tonic_share) is +0.23. With REST and tonic_share held, stability is 0.28, up from 0.20.

**G2 PRED: merged** under PI3c as a reading. Add mean event length and the repeated-bar share to the held set. Shrinkage counts only if the no-PI entropy β is nonzero.

**G3 THIN: withdrawn** into Merge 1. My binomial thinning is the conditional form of its Poisson pair. The prediction is unchanged: Δ = β_L − β_E = 0 ± 0.03.

---

## Run 12, round 2: the Listener

No outcome opened. New checks were notes-only (about 1 minute).

**L12-1 PI3c: revise.**
- *Controls.* I accept all of the Skeptic's Lakh controls, plus H1 and the repeated-bar share. The repeated-bar share is the share of non-empty 8-eighth skyline bars that equal an earlier bar exactly.
- *Copy-paste worry.* The check does not bear it out. Within artist, PI3c correlates −0.25 with the repeated-bar share, +0.19 with notes per beat and −0.01 with the number of MIDI files. All five controls together give R² 0.25 (5,275 songs).
- *Prediction.* Unchanged at **+0.03**. G2 becomes a reading. The subsumption reading counts only if H1 alone is nonzero on Lakh.

**L12-2 PIC: withdrawn as a counted test.**
- With step_share and mel_ic_mean held, power is 0.18 at +0.03 (fake SE 0.0184), below the 0.2 floor.
- It stays an uncounted estimate on re-spent songs.

**L12-3: merged into the Skeptic's design** (early window 0-3, late window 8+, decade × window held).
- *Prediction.* Δ = β_L − β_E = **−0.02** for REP, and **+0.02** for PI3c if the Lakh groups are pooled.
- *Kill.* The prediction lies outside Δ ± 1.96 SE.
- *Status.* An estimate.

---

## Run 12, round 2: the Inventor

No outcome was opened. New check: `measures/inventor_roughx_check.py`, written to `/home/claude/dl/run12/inventor_roughx_check.json`.

**I-1 PROP: revised, and I accept the merge (G3 / L12-3 / I-1).**
- Fit each window separately, with its own five-year first-year dummies (this gives decade × window).
- Add a reading on 1970+ songs only, to deal with the rival 1950s-60s versions.
- Prediction unchanged: REP β_E = β_L ≈ −0.05, Δ = 0.
- This becomes an estimate (power about 0.1) unless pooling raises it to the 0.2 floor.

**I-2 ROUGH: revised to an uncounted estimate.**
- New measure ROUGH_X: drop octave-multiple pairs from both the sum and the count.
- Check on 156 non-duplicate pairs: stability falls to 0.285, and ρ with mean sounding pitch is −0.63. Most of the roughness is register.
- Controls: register, octave-pair share, active tracks, ln events, notes per beat, number of files and run 07's chord measures.
- Prediction: −0.01.
- Stopped if its two-file stability with register held falls below 0.20.

**I-3 CANAL: withdrawn as a test.** It stays a notes-side pilot until there are more than 156 independent pairs.
