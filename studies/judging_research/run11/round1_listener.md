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
