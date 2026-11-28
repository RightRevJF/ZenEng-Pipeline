# Run 12, round 1: the Inventor (carrying vector 1)

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
