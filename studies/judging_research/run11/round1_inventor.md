# Run 11, round 1: the Inventor

28 November 2026. Notes-side only: no outcome opened. Module: `run11/experiments/measures/m_inventor.py`. Effects are SD of y_foreign per SD of the measure, within artist.

## Proposals (the proposal text)

**I11-1 HB, bound rooms (Li 2026, Theorem 1.1, applied to the melody–harmony graph).**
- Mechanism: join each melody pitch class to the chords it sounds over. The graph is exactly bipartite (spectrum 1 ± σ_i), so a small λ_k (σ_k near 1) means k chords each own a room of melody notes, with thin doorways between.
- Measure: HB = mean σ_i², i = 2..min(r, c) (Cramér's V² of the pc × chord duration table).
- Data: melody and chords.
- Prediction (label extrapolation): +0.03, with ln_notes frozen. The theorem makes a high HB mean genuine rooms (λ_k/2 ≤ φ_k ≤ C√(λ_k log(k+1))). Sung alone, such a song still spells its progression, so it should survive being stripped back and re-arranged.
- Kill: estimate below about 0.00, which puts +0.03 outside the 95% range.

**I11-2 ANT, the push (phase lead between coupled oscillators).**
- Mechanism: of two coupled oscillators, the leader drives. A melody that reaches the next chord's new tone early carries the harmonic rhythm itself.
- Measure: the share of chord changes where a melody note starts in the half beat before the change, on a pitch class that is in the new chord and not in the old one.
- Data: melody and chords.
- Prediction: +0.03, with density frozen. A cover artist with another groove still gets the changes from the tune.
- Kill: estimate below about 0.00.
- Note: ANT runs against chord-tone share CT (ρ −0.38) and HB (−0.28); read it with CT held.

**I11-3 LOCKP, the footfall sharpened (run 10's R10-I2, a fresh test on pop).**
- Mechanism: the dancer lifts on the strong beat. Contour peaks land at high metrical weight.
- Measure: the mean metrical weight (1 to 5) of contour peaks, minus the mean over all pitch-change onsets.
- Data: melody only.
- Prediction: +0.03, no extras.
- Kill: estimate below about 0.00.
- **Verdict: it fails the stability gate in every form.** Seven forms: binary (run 10 recipe, 0.11), graded (0.101), curvature-weighted (0.116), correlation (0.100), agogic (0.09), at chord changes (0.109), peaks only (**0.143**). None reaches 0.2: the footfall belongs to the section, not the song. Run LOCKP as an uncounted estimate only; not in K.

**Dropped: BIP, Trevisan's dual Cheeger bound.**
- 2 − λ_max of the transition graph (small = a pendulum, two-strand melody). Unstable, 0.108 (pitch classes 0.159): one triadic leap closes an odd cycle and moves λ_max. Kept in the module as a record.

## checks11 figures

These come from `python3 checks11.py measures/m_inventor.py 0.03`, plus a scratch rerun of `C.power` (200 draws) with each measure's frozen extras. α = .05/6.

| Key | Songs | Stability (pairs) | R² on 13 | Largest \|ρ\| (baselines/pack) | Power +0.03 (frozen extras) | Power +0.04 | fake SE |
|---|---|---|---|---|---|---|---|
| HB | 9,570 | **0.263** (4,250) | 0.358 | ln_notes −0.37, density −0.27, rhy_h_mean +0.25 | 0.215 (ln_notes) | 0.48 | 0.014 |
| ANT | 9,363 | **0.252** (3,981) | 0.109 | density +0.27, sync_per_note +0.22 | 0.245 (density) | 0.53 | 0.014 |
| LOCKP | 9,379 | 0.143 (3,965) | 0.016 | ln_notes +0.07 | 0.445 (none) | n/a | 0.013 |
| BIP (dropped) | 9,566 | 0.108 | 0.234 | n_int +0.28 | 0.38 | n/a | 0.013 |
| CT (reading) | 9,557 | 0.288 | 0.145 | phrase_on_downbeat +0.21 | 0.22 | n/a | 0.014 |

Overlap, Spearman, songs with every measure:
- HB vs CT: +0.49
- HB vs ANT: −0.28
- ANT vs CT: −0.38
- HB vs GAP (m00): −0.16
- LOCKP vs m00 LOCK: +0.42
- Every other pair: |ρ| ≤ 0.17

Neither of the two proposed tests is a renamed baseline. Power at +0.03 sits just above the 0.2 floor; Monte Carlo error is about ±0.03.

## Exact recipes (per clip; song value = n_mel-weighted mean)

- **Common settings.** Notes come from `C.melody(a)`. A chord is "active" at time t if onset ≤ t < offset. A chord's pitch classes are the root plus the cumulative `root_position_intervals`, mod 12.
- **HB.**
  1. For every note, add its duration to the cell (pc, chord label) of the chord active at the note's onset. The chord label is (root pc, the interval tuple).
  2. This gives an r × c table A. It needs r ≥ 2 and c ≥ 2.
  3. Set N = D_r^-1/2 A D_c^-1/2 and take its singular values σ1 = 1 ≥ σ2 ≥ ….
  4. HB = the mean of σ_i² for i = 2..min(r, c).
- **ANT.**
  1. Count every consecutive pair of chord spans (h0, h1). This needs 4 or more pairs.
  2. Mark a pair as a hit if any melody note has onset in [t − 0.5, t), where t is h1's onset, and its pc is in pcs(h1) \ pcs(h0).
  3. ANT = hits / pairs.
- **LOCKP.**
  1. Merge repeated pitches into their first onset.
  2. Metrical weight w = 1 + [b on the half-beat grid] + [b an integer] + [b on the half-bar, if bpb is even] + [b = 0], where b = onset mod bpb.
  3. A peak is a run higher than both of its neighbours. This needs 3 or more peaks.
  4. LOCKP = the mean w at the peaks minus the mean w over all runs.
- **BIP.** Merge repeats. Build W = C + Cᵀ from the transitions between consecutive octave-distinct pitches (no wrap-around). BIP = 2 − λ_max of I − D^-1/2 W D^-1/2. This needs 3 or more pitches.

## Readings to freeze with the tests (uncounted)

- HB with CT held.
- ANT with CT held.
- Each test with all 13 baselines held.
- A variant of ANT that keeps only the chord changes with some melody onset in the window (ANTC): stability 0.223, 7,657 songs.
