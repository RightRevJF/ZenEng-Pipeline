# Run 10, round 1: the Inventor

27 November 2026. Notes only. I opened no outcome, called no outcome loader, and read no recordings, popularity, data/*.json or HOLDOUT file. Code is in `/home/claude/scripts/inventor/` (`measures_inventor.py` has `measure(t) -> dict`; the checks are in `checks.py`, `gapn.py` and `gapres.py`). Every measure is computed on `mel`, with no fitted settings.

## Proposals

**R10-I1. ARCH: the statue's arches (persistent entropy of the contour barcode; card 1's persistent entropy, card 1's lead 3, and the stability theorem of Cohen-Steiner, Edelsbrunner and Harer, 2007).**
- **Mechanism.** Treat the melody as a function: pitch against note order, with repeated pitches merged. Its sublevel and superlevel H0 barcode pairs every valley with a ridge, so each bar is one arch of the contour, of a given height.
- **Measure.** ARCH_PE is the persistent entropy of all finite bars, divided by log(number of bars).
- **What the mathematics predicts.** The stability theorem says a change of size e moves every bar by at most e. A step-sized ornament or variant therefore only adds or moves short bars, and the long bars are the part that survives transmission (card 2's skeleton). A low ARCH_PE means a few big arches carry the shape: a statue rather than a texture.
- **Prediction (extrapolation).** −0.03 SD of z(y_cov) per SD. y_love is also expected negative.
- **Kill.** −0.03 lies outside the 95% range.

**R10-I2. LOCK: the dancer's footfall (biomechanics; card 2's conservation gradient).**
- **Mechanism.** Where the melody turns, a dancer feels the step. If those turns sit on beats, which are the slots card 2 finds most conserved, the tune's shape lives where transmission protects it.
- **Measure.** LOCK = P(on a beat | contour turning point) − P(on a beat | any note-run start). A turning point is a strict local maximum or minimum after repeated pitches are merged. A note is on a beat when its beatpos is a whole number.
- **Prediction (extrapolation).** +0.03. y_love is also expected positive.
- **Kill.** +0.03 lies outside the 95% range.

**R10-I3. GAP: two rooms and a doorway (Jason's S = 1 + g/pi, never tested on melodies before; Cheeger's inequality).**
- **Mechanism.** Build the graph of transitions between octave-distinct pitches. It is cyclic (last note to first, because a dance tune goes round), symmetrised, and counts self-loops. Its gap g is λ2 of the normalised Laplacian.
- **What the theorem says.** Cheeger's inequality, g/2 ≤ h ≤ √(2g), means a small g forces a cut that the melody rarely crosses.
- **What the cut is.** In 88% of tunes the Fiedler vector orders the pitches by height, |ρ| ≥ 0.8. So the cut is a register cut: a low room and a high room, as in an Irish A part and its high B part.
- **Prediction (extrapolation, from architecture).** A legible two-room plan is remembered and taken up: −0.03 per SD of g (S is monotone in g). y_love is also expected negative. The test holds range, n_pitch and ln_notes as frozen extra controls.
- **Kill.** −0.03 lies outside the 95% range.

## Measure-side checks (split A)

Stability uses `common10.stability`: the first 3,000 tunes that have a second setting. Renaming uses `common10.renaming` on a random 3,000 tunes (seed 10). The checks took about 1.5 minutes of compute.

| measure | stability ρ (n = 3,000) | R² on the 13 baselines | largest baseline ρ | after removing baselines: stability |
|---|---|---|---|---|
| ARCH_PE | **0.80** | 0.35 | range −0.33, n_pitch −0.32, step_share −0.32 | 0.75 |
| LOCK | **0.74** | **0.01** | pc_entropy +0.08 | (≈0.74) |
| GAP (S) | **0.82** | 0.65 | range −0.59, n_pitch −0.54, leap_share +0.39 | 0.68 (0.77 after range, n_pitch, ln_notes only; R² 0.35) |

All three pass the 0.5 bar. The three measures are nearly independent of each other: ρ is −0.03 for LOCK with ARCH_PE, −0.02 for LOCK with GAP, and +0.43 for ARCH_PE with GAP.

## Notes

- **Rejected readings.** These were rejected on the notes alone; no outcome was seen.
  - ARCH_TOP, the share held by the longest bar: R² 0.79, mostly ln_notes.
  - GAP on pitch classes: stability 0.75, R² 0.55.
  - GAP divided by the gap of a k-node path: R² 0.63, which only moves the renaming from range onto n_int and int_entropy.
- **Canalisation, a descriptive check.** ARCH_PE on the on-beat skeleton agrees with ARCH_PE on the full surface only at ρ = 0.42. The stability theorem protects the long bars, not their entropy, because ornaments add many short bars. If ARCH dies, the next form to try is bottleneck distance on the long bars only.
- **LOCK by type.** LOCK is positive in every type, with a mean of about 0.04 to 0.09 (slides highest). Turning points favour beats everywhere, so the type fixed effect matters.
- **GAP renaming.** GAP is the most renamed of the three. It is worth a counted test only with its extra controls frozen; otherwise it is mostly range.
