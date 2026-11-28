# Run 11 brainstorm

28 November 2026, the 02:17 ET pass. Three imaginers (Round 1), the Skeptic (Round 2), then each imaginer's answer. Notes-side checks only; no outcome was opened by any of the four. Data: Hooktheory clip melodies, 9,588 within-artist songs (seen songs; new measures). Run 10's data is withdrawn (licence), so its figures are cited nowhere as evidence.


---

<!-- round1_geometer.md -->
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

---

<!-- round1_listener.md -->
# Run 11, round 1: the Listener

28 November 2026. Stance: expectation, surprise, memory, exposure. What makes a musician want to learn a song by ear. No outcome was opened. Only notes-side checks were run (`checks11.py`, 100 fake draws, α .05/6). Module: `run11/experiments/measures/m_listener.py`.

## Proposal (about 400 words)

**L11-1 SETTLE: rooms where the ear settles (card 1, Cheeger and sweep cut).**
- *Mechanism.* Inside a room of the pitch graph the listener's short-term expectations keep coming true, and a crossing through the thin doorway is the rare event of surprise. A melody that stays in its rooms can be learned in chunks.
- *Measure.* 1 − crossings / (2·nA·nB/n), counted on the sweep cut of the Fiedler vector. The denominator is the number of crossings expected if the same notes came in random order.
- *Mathematics (extrapolation).* 1 − SETTLE is the cut's sparsity, which lies between φ and 2φ of the sweep cut. Cheeger gives λ2/2 ≤ φ2 ≤ φ_sweep ≤ √(2λ2). A walker escapes a room in about 1/φ steps but learns the room's moves faster than that. So a high SETTLE means long runs of confirmed expectation. The melody can be chunked, so it should be easier to learn and so covered more.
- *Data.* Clip melodies only.
- *Prediction.* **+0.03** SD per SD within artist, with **n_pitch and range frozen** (otherwise it is partly "how far apart the registers are").
- *Kill.* +0.03 falls outside the 95% range, i.e. the estimate is about 0 or below.

**L11-2 TYP11: a typical melody by exposure, not by sequence.**
- *Mechanism.* Listeners carry a long-memory schema of how much time a pop melody spends on each scale degree. A melody that matches it is heard as "already known" on first exposure and is easy to hold.
- *Measure.* Pearson r between the clip's duration-weighted scale-degree profile and the corpus profile (major and minor kept separate), with the tonic bin dropped so that it is not tonic_share.
- *Why it is not mel_ic_mean.* mel_ic_mean is sequential surprisal (which note comes next). TYP11 is zeroth-order (where the time goes), and |ρ| with mel_ic_mean is below 0.19. mel_ic_mean is frozen as an extra anyway.
- *Prediction.* **+0.03**.
- *Kill.* The estimate is below about +0.004.

**L11-3 REP, run fresh: fewer pitch classes.** I endorse it as a counted test.
- *Mechanism.* Each extra pitch class is one more thing to hold. A narrow spread is learned and sung back sooner.
- *Measure.* pc_entropy, exactly as in the baseline (REP is that baseline by design).
- *Prediction.* **−0.03**, no extras. Run 10's sizes are withdrawn and not evidence, so −0.03 is a prior, not a replication target.
- *Kill.* The estimate is about 0 or above.

**On core_ic.** I do not propose it as a separate test here. The pack's mel_ic_mean already measures corpus surprisal of the melody on these songs, so a skeleton version would mostly rename it. TYP11 is the "typical melody" test that does not rename it. If someone builds core_ic, it should be an estimate with mel_ic_mean frozen.

## checks11 figures (notes only)

| Key | Role | Songs | Stability (clip pairs) | Largest overlaps (ρ) | R² on 13 | Power at pred, extras | fake SE |
|---|---|---|---|---|---|---|---|
| SETTLE | L11-1 | 9,528 | 0.212 (4,199) | n_pitch 0.68, range 0.64, n_pc 0.55 | 0.492 | **0.21** at +0.03, n_pitch+range (0.39 with none; 0.56 at 0.04 with none) | 0.0162 |
| TYP11 | L11-2 | 9,588 | 0.212 (4,266) | n_int 0.25, int_entropy 0.23, pc_entropy 0.21 | 0.163 | **0.27** at +0.03, mel_ic_mean (0.29 with none; 0.70 at 0.04) | 0.0133 |
| REP | L11-3 | 9,588 | 0.389 (4,271) | pc_entropy 1.0 (by design), n_pc 0.88 | 1.0 | **0.25** at −0.03, none (0.49 at −0.04; 0.18 with mel_ic_mean; 0.12 with n_pitch+range) | 0.0151 |
| TYP | reading (all 12 bins) | 9,588 | 0.215 | tonic_share 0.41 | 0.345 | 0.32 at +0.03, mel_ic_mean | 0.0134 |
| TYP_KK11 | reading (Krumhansl–Kessler profile) | 9,588 | 0.198 | n_int 0.26 | 0.133 | 0.30 at +0.03, mel_ic_mean | 0.0131 |

With 100 draws, each power figure carries a Monte Carlo error of about ±0.045. SETTLE sits on the floor. To clear it more safely, freeze range only, or predict +0.04. That is the chair's call, and it must be made before the join.

### Dropped on the notes (each tried in this pass)
- **DOOR** (crossings that fall on a downbeat or after a rest, minus the base rate of such moves): stability 0.056. Too few crossings per clip.
- **DOOR_T** (crossings through the tonic): 0.011.
- **BIP** (2 − λmax, Trevisan's dual Cheeger): 0.108.
- **SETTLE on pitch classes**: 0.122. Folding the octaves loses the register rooms.
- **SETTLE3** (three rooms by a recursive sweep, the case Li's theorem covers): renamed, n_pitch ρ 0.79, R² 0.61. On clips of about 47 notes, a third room mostly means "more pitches".
- **TIGHT2** (φ_sweep/√λ2, the tightness from card 1 M2): 0.14.
- **TYP_KK with the tonic bin**: tonic_share ρ 0.64, R² 0.51. Kept only as the TYP11 family.

## Exact recipes (`m_listener.py`)

- **Melody.** `C.melody(a)` (12 or more notes).
- **Repeat-free sequence P.** Drop every note whose pitch equals the previous note's. Rests are ignored, so transitions across rests are kept.
- **SETTLE**
  1. Build one node per distinct MIDI-like pitch in P. For each consecutive pair add 1 to W[a,b] and to W[b,a]. The walk is not cyclic.
  2. Compute L = I − D^−½ W D^−½ (numpy `eigh`). Take f = v2/√d. Sort the nodes by (f rounded to 12 decimals, node index).
  3. Room A is the prefix with the least cut/min(vol A, vol B); on ties, the first prefix found wins.
  4. Count the crossings c = #{i : room(P_i) ≠ room(P_i+1)}. SETTLE = 1 − c/(2·nA·nB/n), where n = |P| and nA, nB count the notes of P in each room.
  5. No value if P has fewer than 3 distinct pitches or fewer than 8 notes.
- **TYP11**
  1. Build the clip's profile: prof[(pitch − tonic_pc) mod 12] += dur, over all notes.
  2. Build the corpus profile: the sum of the same profiles over every raw Hooktheory clip with a melody, iterated in sorted key order. Keep one sum for major (first key's scale intervals [0] + [1] = 4) and one for the rest.
  3. TYP11 = Pearson r of prof[1:12] with corpus[1:12] for the clip's mode. TYP uses all 12 bins. TYP_KK11 uses the Krumhansl–Kessler major or minor profile in place of the corpus.
- **REP.** `C.baseline(mel)['pc_entropy']`: the duration-weighted pitch-class entropy in bits.
- **Song value.** The n_mel-weighted mean over the song's clips (`C.song_values`).
- **Checks run:**
  - `checks11.py measures/m_listener.py 0.03`
  - `checks11.py measures/m_listener.py 0.03 n_pitch,range`
  - `checks11.py measures/m_listener.py 0.03 mel_ic_mean`
  - `checks11.py measures/m_listener.py -0.04`
  - The variants were checked from scratch modules that are not in the repo.
  - Total compute was about 3.5 minutes.

## Note against my own sign (labelled)
Earlier Hooktheory lessons (the brief) say musicians lean toward "room in the melody" and chords that move, and that chord repetition goes with fewer covers (about −0.04). If "moving" is what covers reward, SETTLE could come out negative. The +0.03 is a prediction, written down so that it can be killed.

---

<!-- round1_inventor.md -->
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

---

<!-- round2_skeptic.md -->
# Run 11, round 2: the Skeptic

Notes only; no outcome opened. Scratch checks (1 minute): within-artist ρ with ch_rep and the pack; clip-pair stability after each test's own frozen extras.

**Across all.** None renames chord repetition: within-artist |ρ| with ch_rep ≤ 0.06 everywhere, so the seen ch_rep result (about −0.04) leaks at most about 0.002 SD. Seen-ness enters through mel_ic_mean instead (within ρ: REP 0.34, TYP11 −0.18, SETTLE 0.13, HB 0.12). Fame: hits get more clips and transcribed choruses, so keep clips per song in the controls. Nothing holds era drift within a career.

**GAP (= G_GAP = S), G_ROOMS, SETTLE.** One idea three times (SETTLE–ROOMS +0.90, SETTLE–GAP −0.80, GAP–ROOMS −0.79). Count GAP once and make the other two readings. Their stable part is size: with their own extras held, stability falls to 0.158, 0.153 and 0.113, all under the 0.20 gate. −0.04 echoes run 10's withdrawn figures. Predict −0.03 as an estimate (power 0.15–0.25), unless the chair rules that the gate applies to the residual. Separating reading: all 13 baselines plus mel_ic_mean held. If it lives only without range held, it is range.

**G_TIE / HB.** Duplicates (ρ 0.96): merge them. Cramér's V² is biased upward in sparse tables, so few notes per chord (chords that move) can drive it. Hold ln_notes, density and n_pc (residual stability 0.212). Readings: CT held (ρ 0.49), and bias-corrected V². The kill at +0.003 is sharp.

**TYP11.** Clean: not mel_ic_mean, and stability 0.218 with pc_entropy and tonic_share held. Risk: "typical" means the corpus's dominant style, and artist effects absorb only 26% of its variance. Freeze mel_ic_mean, and read it with pc_entropy held (it leans against REP, +0.21).

**REP.** A baseline. Bare, it is partly n_pitch (within 0.63) and the seen mel_ic_mean (0.34). It is also the most between-artist measure (42%), so the most genre-laden. Count it bare. If it survives with n_pitch, range and mel_ic_mean held (residual stability 0.175), the effect is "fewer pitch classes", not "plain songs". State now that power is 0.25 bare and 0.12 held.

**ANT.** Not renamed (within-artist R² 0.12 on all 30 measures). The push is style-coded and depends on where the transcriber places the chord change. Hold density (0.213); read it with sync_per_note and CT held.

**LOCKP.** Fails the gate (best 0.143): uncounted. +0.03 is unrealistic on a measure this noisy.

**Power.** SETTLE (0.21) and HB (0.215) are at the floor within Monte Carlo error. Rerun them at 300 draws and freeze before the join.

---

<!-- round2_geometer.md -->
# Run 11, round 2: the Geometer answers

Notes only. No outcome opened, no new compute.

**GAP, ROOMS and SETTLE: accepted, counted once.** They are one idea, so they count as one test.

**−0.04: withdrawn.** Nothing from first principles picked it out of the 0.02 to 0.06 band, and choosing it for power is anchoring.

**Stability: conceded.** With size held, the residual is under the gate, so GAP runs as an estimate unless the chair rules that the gate applies to the raw measure.

- **Frozen:** `G_GAP` (= m00 GAP; S = 1 + g/π is the same test), **−0.03**. Extras: range, n_pitch, ln_notes.
- **Readings:**
  - bare;
  - all 13 baselines plus mel_ic_mean held;
  - `G_ROOMS` (prediction +0.03) and SETTLE;
  - ROOMS with `G_GAP` held, for the rooms beyond two.

**ROOMS: withdrawn as a test** (kept as a reading).

**TIE: withdrawn, merged into the Inventor's HB** (ρ 0.96). Same mathematics; HB was written first.

- **Frozen:** HB, **+0.03**. Extras: ln_notes, density, n_pc.
- **Readings:**
  - CT held;
  - bias-corrected V² (Bergsma 2013) on note counts. If HB lives only uncorrected, it is sparse-table bias from chords that move.
- **Power:** at 300 draws before the join.

---

<!-- round2_listener.md -->
# Run 11, round 2: the Listener answers the Skeptic

No outcome was opened, and nothing was committed.

**SETTLE is withdrawn as a counted test.** I accept that it is the same idea as GAP and ROOMS: ρ +0.90 with ROOMS and −0.80 with GAP. Its residual stability is 0.113, so with its extras held, what is left is only size. It goes into the GAP folder as an uncounted reading, `SETTLE`, predicted **+0.03** (the same direction as GAP's minus sign), with n_pitch and range held.

**TYP11 is kept as counted.**
- Key `TYP11`, predicted **+0.03**, with **mel_ic_mean** frozen. Power 0.27.
- Readings:
  - pc_entropy held
  - tonic_share held
  - all 13 baselines plus mel_ic_mean held
  - `TYP_KK11` (the listener profile from Krumhansl and Kessler, not from the corpus)
  - `TYP` (all 12 scale degrees)
- Style check: if TYP11 survives but TYP_KK11 is zero, it measures the corpus's main style, not the listener's schema.

**REP is counted bare.**
- Key `REP` (pc_entropy), predicted **−0.03**, no extras. Power 0.25, stated now.
- Reading: n_pitch, range and mel_ic_mean held (power 0.12, residual stability 0.175), so it is an estimate only. If REP survives with these held, the effect is "fewer pitch classes", not "plain songs".

---

<!-- round2_inventor.md -->
# Run 11, round 2: the Inventor

No outcome was opened. Power is from fake outcomes (300 draws, α .05/6).

**HB, merged into G_TIE.**
- I accept the duplicate (ρ 0.96) and drop my HB. The chair uses the Geometer's recipe, because it weights a held note under every chord it overlaps.
- Measure: `G_TIE`.
- Prediction: **+0.03**.
- Extras: **ln_notes, density, n_pc** (residual stability 0.212).
- Power: **0.29** (SE 0.0142).
- Kill: an estimate below +0.003.
- Readings: chord-tone share (CT) held, and Bergsma's bias-corrected V².

**ANT, kept as written.**
- Measure: `ANT`.
- Prediction: **+0.03**.
- Extras: **density**.
- Power: **0.27** (SE 0.0138).
- Kill: an estimate below 0.00.
- Readings: sync_per_note held, CT held, and all 13 baselines held.
- I accept that ANT is tied to style and to where the transcriber places the chord change. Artist fixed effects absorb only part of that.

**LOCKP, withdrawn as a test.** It is an uncounted estimate at +0.02 with no extras. It is not in K, because its best stability, 0.143, is under the 0.2 gate.
