# Run 12, round 1: the Geometer

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
