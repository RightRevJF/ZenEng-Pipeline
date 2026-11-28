# Run 11, round 1: the Geometer

28 November 2026. Notes only: no outcome was opened. Module: `experiments/measures/m_geometer.py` (KEYS `G_GAP`, `G_ROOMS`, `G_TIE`). Figures come from `checks11.py` (all 9,588 rows, 100 fake draws; Monte Carlo error about ±0.05 on power).

## The proposals

**1. GAP, Jason's S on the melody (run 10's idea, adopted and sharpened; a fresh test).**
- *Mechanism.* Cheeger's inequality, the k = 2 case of card 1, gives φ2 ≤ √(2λ2). So a small gap means the melody lives in two pitch rooms joined by a thin doorway, a shape with parts that a singer can hold and carry.
- *Measure.* λ2 of the normalised Laplacian of the clip's octave-distinct pitch-transition graph (S = 1 + λ2/π is the same test). Range, n_pitch and ln_notes are frozen as extras.
- *Data.* Melody pitches only.
- *Prediction.* **−0.04** SD per SD, within artist.
- *Kill.* An estimate above about −0.010, which puts −0.04 outside the 95% range.

**2. ROOMS, the full room profile (card 1, Theorem 1.1).**
- *Mechanism.* The card adds a theorem for every k: λ_k/2 ≤ φ_k ≤ C√(λ_k log(k+1)), with the index exactly k. So each 1/λ_k sits between 1/(2φ_k) and C²log(k+1)/φ_k². Averaging 1/λ_k over the lower half of the spectrum therefore scores all of the melody's rooms (2, 3, 4 and more), not only the best single cut. It is the low half of Kemeny's constant: how long the melody keeps you somewhere before it takes you elsewhere.
- *Measure.* G_ROOMS. Size extras as in method 1.
- *Prediction.* **+0.03**.
- *Kill.* An estimate below +0.003, i.e. zero or negative.

**3. TIE, melody–harmony rooms (bipartite spectral geometry).**
- *Mechanism.* The beats-weighted graph that joins melody pitch classes to chords is exactly bipartite (2 − λmax = 0, the dual-Cheeger extreme), so its spectrum is the mirror image 1 ± s_k. When the low eigenvalues are small, each chord has its own room of melody notes. Such a tune carries its harmony inside it, so another artist can strip or re-arrange the backing and keep the song.
- *Measure.* G_TIE (it equals Cramér's V²). ln_notes is frozen as an extra.
- *Data.* Melody and chords.
- *Prediction.* **+0.03**.
- *Kill.* An estimate below +0.003.

**What the mathematics predicts (extrapolation).** A song that lasts and gets covered is a statue with a few distinct parts and narrow passages between them. The walk is expected inside a room, surprises at a doorway, and is remembered by its rooms. The theorem proves only the graph half of that sentence.

## Checks (checks11)

| Key | Songs | Stability (pairs) | Top overlaps | R² on 13 baselines | Power at prediction, α .05/6 (fake SE) |
|---|---|---|---|---|---|
| G_GAP | 9,566 | **0.200** (4,239), exactly at the gate | n_pitch −0.61, range −0.56, n_pc −0.50 | 0.571 | 0.47 at −0.04 (0.0154); at −0.03: 0.25 and 0.15 in two runs |
| G_ROOMS | 9,566 | 0.218 (4,239) | n_pitch +0.64, range +0.61, n_pc +0.49 | 0.329 | 0.35 at +0.03 (0.0138); 0.58 at 0.04 |
| G_TIE | 9,576 | 0.265 (4,258) | ln_notes −0.34, density −0.24, rhy_h_mean +0.23 | 0.342 | 0.32 at +0.03 with ln_notes (0.0139) |

Overlap among the three (Spearman, first 3,000 rows): GAP and ROOMS −0.79; TIE −0.18 with GAP and +0.17 with ROOMS. If the chair merges GAP and ROOMS, ROOMS has the better power and stability and is the card's own theorem; GAP is Jason's S. A suggested reading: ROOMS with G_GAP held, which isolates the rooms beyond two.

## Exact recipes (as coded)
- **Graph.** One node per distinct MIDI pitch; W = C + Cᵀ over consecutive notes, transitions across rests kept; L = I − D^-1/2 W D^-1/2; at least 3 nodes. Song value = the n_mel-weighted mean over clips.
- **G_GAP.** Repeated notes kept as self-loops; the last note is joined to the first (cyclic); the value is λ2 (identical to m00 `GAP`).
- **G_ROOMS.** Runs of repeated notes merged (no loops), no wrap; the eigenvalues sorted λ1 = 0 ≤ λ2 ≤ …; the value is mean(1/λ_k) for k = 2 … 1 + ⌊(n−1)/2⌋.
- **G_TIE.**
  - B[pc, chord] is the overlap in beats between each melody note's [onset, onset + dur] and each chord's [onset, offset]. A chord is identified by (root_pitch_class, root_position_intervals); inversion is ignored; chords with no root are skipped. At least 2 rows, 2 columns and 2 chords.
  - N = Dr^-1/2 B Dc^-1/2, with singular values s1 = 1 ≥ s2 ≥ ….
  - TIE = Σ_{k≥2} s_k² / (min(rows, cols) − 1).

## Dropped on the notes (first 3,000 rows)

**The dual-Cheeger measure.** 2 − λmax is unstable: 0.107 on the pitch graph and 0.135 on pitch classes. With loops kept it renames unison_share (ρ 0.72). Its idea survives only inside TIE.

**Unstable.** λ3/λ2 (0.05); k\* by the largest eigengap (0.07); the size-free positions of ln λ2 and ln K between the path and the complete graph (0.09 and 0.11).

**Renamed by n_pitch.** λ2 without loops (−0.77); λ3 (−0.88); the exact φ2 by brute force (−0.70, stability 0.22); the whole Kemeny constant K/(n−1) (+0.71, so I revised it to the low half).

**Not proposed.** The von Neumann ratio of the contour (stability 0.27, R² 0.61), because it overlaps GAP.

**What these checks show.** On these clips, the stable part of every pitch-graph spectral number is mostly its size, and the size-free shape is noise. That is why size is frozen in methods 1 and 2.
