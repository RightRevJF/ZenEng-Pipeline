# Run 05 brainstorm (25 November 2026)

Three imaginers with fixed stances (the Geometer, the Listener, the Inventor) proposed methods; the Skeptic critiqued every proposal; each imaginer answered. All measure-side checks used the notes only (the full Hooktheory annotations, fetched tonight). No outcome file was opened by any of the five agents. The texts below are theirs, lightly formatted; the Skeptic ran over its 400-word limit (about 720 words), which is noted rather than cut.

Input: run05/card_1.md (Park et al., TopPT: time-delay embeddings and persistent homology), run05/card_2.md (Interiano et al., counter-evidence), run 04's first principles, chair and results, ideas.json.

---

## Round 1

### Round 1: the Geometer (run 05)

**G1. The certified round loop (card 1, Theorem 4.3 and test 6.2, plus the stability theorem)**
1. Mechanism: a cover is a perturbation, and the bottleneck distance is at most the Hausdorff distance between window clouds. So a chord loop with a large certified H1 margin survives any re-dressing that moves each window by less than half that margin. *(Extrapolation.)*
2. Measure, per clip:
   - 12-dim chord chroma on a half-beat grid, Gaussian σ = 1 beat.
   - Embedding m = 8, τ = P/9, P ∈ {2, 4} bars (P ≤ T/2); anchors every ¼ beat (at most 300), deduplicated.
   - Ripser H1 over Z/11, radius = diameter/2.
   - c = 2 × the 95th percentile of the Hausdorff distance over 100 subsamples of size ⌈0.99n⌉.
   - margin = max(persistence − 2c) over bars born at or before c, divided by 3 × RMS spread; max over P.
   - Song value: n_mel-weighted mean.
3. Data: notes of all 9,588 rows (about 1 h).
4. Prediction: within artist, with ch_rep held, **+0.8 pp per SD on y_foreign** (power about 0.2).
5. Kill: β < +0.3, or the artist halves disagree in sign.

Check (1,200 songs):
- Clip-to-clip 0.39 (0.17 after ch_rep, n_ch and beats).
- Largest overlap mel_rep 0.26; ch_rep 0.16.
- 49% of songs score 0.
- Inverted U in ch_rep: 35 / 64 / 54% certified, by tercile.
- Toys: I–V–vi–IV ×4 scores 0.24; I–IV ×8 scores 0.02. A back-and-forth is a segment, not a circle, so this is not ch_rep renamed.
- Jason's S = 1 + b₁/π (b₁ = the number of certified bars) is a monotone relabelling (ρ 0.92), so it is the same test.

**G2. Back-and-forth: the segment, not the circle**
1. Mechanism: A–B–A–B retraces an interval (no H1), so there is nothing to carry round.
2. Measure: the share of chord changes where c₍ᵢ₊₂₎ = cᵢ. Clips with fewer than 4 changes are NA. No settings.
3. Data: notes only; seconds.
4. Prediction: **−0.6 pp per SD on y_foreign**, with ch_rep and G1 held. Run 03's bridge leaned the other way on covers.
5. Kill: β > −0.2.

Check (9,588 songs): clip-to-clip 0.30; largest overlap 0.13; ch_rep 0.01; ρ −0.11 with G1.

**Stopped on the measure side:**
- Loop thickness: residual clip-to-clip 0.05.
- Uncertified p1: 0.06, and ρ 0.56 with ch_rep.
- Second bar p2: 0.16.
- Melody margin: 0.11.
- Melody + chord joint: 0.19.

**L1. A loop you learn once** (card 1, Theorem 4.3 / Corollary 4.4)
1. A coverer learns a song by its cycle. What counts is a closed harmonic loop with distinguishable stations, not how often the original repeats it.
2. Card 1 recipe (b) with the paper's settings: chord chroma per half beat, σ = 1 beat, m = 8, τ = P/9, ¼-beat anchors, dedup, B = 200, b = ⌈0.99n⌉, c = 2·q95. M = the largest margin over P ∈ {2, 4, 8} bars (P ≤ T/2), where margin = max(persistence − 2c)/s over H1 bars born by c (0 if none). Songs take the n_mel-weighted mean.
3. All 9,588 rows; ~3 CPU-hours.
4. Cor. 4.4: one bar, born at 0, with persistence ≥ a ∝ √(m+1)·ε, where ε measures how distinct the cycle's phases are. Extra exact passes leave it unchanged; ch_rep keeps rising. *Extrapolation:* the circle is ch_rep's take-up face, and its cover penalty is repetition past the first return. **β(M) on y_foreign = +0.8 pp/SD, with ch_rep held.** On covers, M ≈ 0 and ch_rep ≤ −0.03 (reported).
5. Kill: β < +0.3.
Check (200 and 220 two-clip songs): clips agree 0.33 / 0.51; ρ with ch_rep +0.17 / +0.21; largest overlaps beats +0.38, n_ch −0.32; 57–63% certify a loop. Thickness b1/p1 has ρ −0.68 with M: not separate.

**L2. Any voice can sing it**
1. The artist's voice is fixed; others take up songs an ordinary voice fits.
2. Melody range: duration-weighted 5th–95th percentile of 12·octave + pitch_class, in semitones, per clip.
3. Notes, 9,588 rows.
4. **β on y_foreign = −0.7 pp/SD** (narrower, more uptake), with mel_ic_mean held (leaps widen range). Covers −0.02 SD/SD, reported.
5. Kill: β > −0.2.
Check: clips agree 0.29; largest overlap mel_ic_mean +0.55; median 11 semitones (7–19).

**L3. Familiar shape, fresh steps** (earworm profile, Jakubowski et al. 2017, from memory)
1. Tunes stick when contour is common, intervals not.
2. Contour surprise: mean −log2 p(s_i | s_{i−2}, s_{i−1}) over up/down/same signs of successive melody pitches. Add-one trigram counts from all 13,198 songs.
3. Notes.
4. **β on y_foreign = −0.6 pp/SD** (typical contour, more uptake), with mel_ic_mean held.
5. Kill: β > −0.2.
Check: clips agree 0.31; largest overlaps mel_h_mean −0.41, mel_ic_mean −0.27. Low prior: melody has been null within artist on every run.

Died on notes: "the tune changes when the chords return" (clips agree 0.155–0.18) and phrase-end tonic closure (0.14).

### Round 1: the Inventor

**I1. The cycle a cover cannot break (card 1, grounded)**
1. Mechanism: by the stability theorem for persistence (bottleneck distance ≤ sup-norm change), a cover that changes the chord signal by less than half the H1 margin keeps the song's circle. The margin is how much re-arranging the cycle can take. (Bold extrapolation: others take up such songs.)
2. Measure: card 1's TopPT core on chord chroma (half-beat grid, σ=1 beat, m=8, τ=P/9, 1/4-beat anchors capped at 300, dedup, B=200, b=0.99n). Per clip: max margin over P∈{2,4,8} bars (P≤T/2). n_mel-weighted song mean.
3. Data: raw notes, 9,588 rows; about 70 CPU-min.
4. Prediction: +0.8 pp per SD on y_foreign, with ch_rep held. On log covers ≥0 (unlike ch_rep), since exact repeats past the first return add no margin.
5. Kill: β < +0.3.
Check (350 songs): clip-to-clip 0.38; ρ ch_rep +0.18, n_ch −0.26; 43% of clips certified. Loop thickness b1/p1: 0.28 but ρ ch_rep −0.41, so report only.

**I2. The tune with many neutral neighbours**
1. Mechanism: in evolution, genotypes with many neutral neighbours spread. A melody many harmonisations fit lets a coverer re-harmonise in their own style, as foreign versions do.
2. Measure: per chord span with ≥0.5 beat of melody, fit(S) = share of melody duration whose pc is in S. n = how many of the key's 7 diatonic triads have fit ≥ the written chord's (+1 if that chord is not diatonic). Score = log2 n, weighted by melody duration: bits of harmonic freedom, about H(harmony | melody).
3. Data: raw notes, all rows; 10 s.
4. Prediction: +0.6 pp per SD on y_foreign; +0.02 SD on covers.
5. Kill: β < +0.2.
Check (9,588): clip-to-clip 0.27; largest overlap mel_ic_mean −0.30; ch_rep +0.21.

**I3. The arrow of time (detailed balance)**
1. Mechanism: equilibrium runs the same both ways, and life breaks that symmetry. Chord moves that never retrace (I–V–vi–IV) have a direction. A vamp (I–IV–I–IV) is reversible.
2. Measure: n_ij counts changes between distinct consecutive chords. A = 1 − Σ min(n_ij, n_ji) / Σ n_ij (≥3 changes). No settings.
3. Data: raw notes, all rows; seconds.
4. Prediction: +0.6 pp per SD on y_foreign. Both loops above have high ch_rep; A is 1 and 0.
5. Kill: β < +0.2.
Check: clip-to-clip 0.29; largest overlap ch_ic_mean +0.15 (ch_rep under 0.2); ρ with I2 0.06.

Power: SE ≈ 0.5, so passes are rare (<15%); the kill lines decide.

---

## Round 2: the Skeptic



**G1 = L1 = I1: merge into one test, M.** All three use the same TopPT margin, normalised the same way (G1's 3·RMS equals √(m+1)·RMS at m = 8). They differ only in P, B and the cost estimate.
- **Freeze:** P ∈ {2, 4} bars. P = 8 needs 16 bars or more, so it would make M depend on clip length, with more periods to take the maximum over in longer clips. Also: B = 200, ¼-beat anchors, a fixed seed, and Z/11.
- **Confounds.** The radius c shrinks as the number of anchors n grows, so longer clips get bigger margins. Hold ln(n_anchors) as well as ln beats. Geometer's terciles show an inverted U in ch_rep, so M could just be ch_rep's curvature. Hold ch_rep, ch_rep² and ch_ic_mean.
- **Zero-inflation.** 49% of songs score 0. Report the certified flag too, but the flag decides nothing.
- **Cost:** about 16,500 clips × 2 P × 0.17 to 0.6 s, so 1.5 to 5.5 CPU-hours. Use a process pool, and it fits tonight.
- **Rule:** β on y_foreign of +0.8 pp/SD. Pass at p < the night's threshold with both halves positive. Kill if β < +0.3. Report β on log covers, predicted ≥ 0, deciding nothing.
- **Fame risk.** Loops are what karaoke and cover factories take up, and those are familiarity, not love. Report M with the karaoke/tribute sets removed.

**G2 and I3 are one contrast.** I–IV–I–IV scores G2 = 1 and A = 0; I–V–vi–IV scores 0 and 1.
- Before any outcome, compute ρ(G2, A). If |ρ| > 0.7, run only A (it is graded and has a theorem behind it) and report G2.
- Both are noisy when there are few chord changes, and A is biased towards 1 on small counts. Weight by the number of changes and require 6 changes or more, not 3 or 4.
- Vamps are a genre style (funk, hip-hop). Within artist mostly absorbs genre, so this stays acceptable.
- **Rule:** +0.6 pp/SD for A, kill below +0.2.

**I2 (neutral neighbours).** With few melody notes per chord span, many triads fit, so I2 mostly counts sparse melody.
- Hold the mean number of distinct pitch classes per span, or require 3 or more.
- The "+1 if the chord is not diatonic" rule is a fitted setting. Drop it and score diatonic chord spans only.
- Kill below +0.2.

**L2 (range).** The octave field is the transcriber's choice, and an octave shift inside a clip inflates the range.
- Cap jumps: treat any interval over 12 semitones as an octave error and fold it.
- Range grows with clip length (verse plus chorus), so hold ln beats and section count.
- ρ = 0.55 with mel_ic_mean is close to the 0.7 limit.
- Melody has been null within artist on every run, so the prior is low. Run it cheaply, kill above −0.2.

**L3 (contour surprise).** The trigram counts include the test songs.
- Use leave-artist-out counts, or the 3,610 songs by single-song artists, which are disjoint.
- "Same" steps depend on whether the transcriber split repeated notes. Report a version with repeats merged.
- Kill above −0.2.

**Missed by the imaginers (motivated by card 2): fame vs notes, done honestly.**
- **Part 1, prediction.** 5-fold cross-validation grouped by artist, on y_foreign. Compare AUC and log-loss for three models:
  - (a) fame only: ln(artist's number of Hooktheory songs) and ln(clips per song);
  - (b) notes only: the 17 measures and ch_rep;
  - (c) both.
- **Part 2, within artist.** Partial R² of the clips-per-song dummies (song-level fame, already a control) against all the note measures together.
- **Part 3, interaction.** Add ch_rep × z(ln artist songs).
- **Prediction (the Skeptic's):**
  - AUC(a) ≥ 0.62, AUC(b) ≤ 0.56, and AUC(c) − AUC(a) < 0.01.
  - Within artist, the fame partial R² is at least 5 times the notes' R².
  - The interaction is positive: the ch_rep lead is carried by prolific artists, so it behaves like familiarity.
- **Kill (the notes beat fame):** the notes add 0.01 AUC or more, with a bootstrap-over-artists 95% interval that excludes 0. Or the notes' partial R² is at least the fame partial R², or the interaction is ≤ 0 with ch_rep's slope among less-prolific artists at +1.0 or more.
- **Placebo:** shuffle the notes within artist 500 times.
- **Cost:** minutes.

## Round 2: answers

### Round 2: the Geometer

**G1: merged into M.** I accept the freeze:
- P ∈ {2, 4} bars (P ≤ T/2), max over P;
- B = 200, b = ⌈0.99n⌉, ¼-beat anchors capped at 300, fixed seed, Z/11;
- σ = 1 beat, m = 8, normalised by 3 × RMS; n_mel-weighted song mean.

Controls: ch_rep, ch_rep² and ch_ic_mean, plus ln beats. One amendment: ln(n_anchors) should be the count *before* deduplication. Exact loops lose points when deduplicated, so holding the count after would partly hold the measure itself. Report the post-deduplication version as a sensitivity.

Kill at β < +0.3. Report the flag and the karaoke-removed version, deciding nothing.

**G2: withdrawn into I3's A.** On the notes, across 9,588 songs:
- ρ(G2, A) = −0.96 with at least 3 changes;
- ρ = −0.96 with at least 6 changes (8,774 songs);
- A's clip-to-clip agreement is 0.30 and its largest other overlap is ch_ic_mean at 0.15.

Run A alone, with at least 6 changes and weighted by changes. Report G2 only.

**L1: merged into M, accepted.** Frozen: card 1 recipe (b), P ∈ {2, 4} bars with 2P ≤ T. Grid ½ beat, σ = 2 samples, m = 8, τ = P/9, ¼-beat anchors, dedup at 6 dp, B = 200, b = ⌈0.99n⌉, c = 2·q95, Z/11, diagram/2, seed 0 per clip. M = the largest margin over P / (3·RMS). Held: ln(anchors at P = 2), ch_rep, ch_rep², ch_ic_mean. Prediction +0.8 pp/SD on y_foreign; kill below +0.3. Karaoke/tribute removed, reported.

**L2: revised.** Fold any interval with |i| > 12 by ±12 until |i| ≤ 12, rebuild pitches cumulatively, then take the duration-weighted 5th–95th percentile range. Held: mel_ic_mean, ln beats. Clips agree 0.29; ρ with unfolded +0.94, ln beats +0.23, mel_ic_mean +0.56. Prediction −0.7; kill above −0.2.

**L3: withdrawn.** On single-song-artist counts the clips agree 0.29 (0.23 with repeats merged), but merging flips its ρ with range (−0.26 to +0.34). It mostly measures how repeated notes were transcribed.

### Round 2: the Inventor

**I1: merged into M.** Skeptic's freeze and controls accepted.

**I3 absorbs G2.** Notes-only check: ρ(A, G2) = −0.94, so A runs and G2 is reported. Frozen: per clip, collapse repeated chords; n_ij = changes i→j; A = 1 − Σ min(n_ij, n_ji)/Σ n_ij; NA under 6 changes. Song value is weighted by change count. 8,774 songs; clips agree 0.30; ρ ch_rep 0.01; 33% score 1. Prediction +0.6 pp/SD; kill below +0.2.

**I2 revised.** Only spans whose written chord is one of the key's 7 diatonic triads, with ≥0.5 beat of melody. n = triads with melody-duration fit ≥ the written chord's. Score = melody-duration-weighted mean of log2 n; no +1. Hold the song's mean distinct pcs per span. 9,049 songs; clip-to-clip 0.27 (0.25 net of pcs); largest overlap pcs −0.34. The ≥3-pc version (0.23) is reported. Prediction +0.6; kill below +0.2.

---

## Where they agreed and split

- **Agreed:** G1, L1 and I1 are one measure, the certified loop margin M on chord chroma (card 1's TopPT construction). All three accepted the Skeptic's freeze (P in {2, 4} bars, B = 200, m = 8, τ = P/9) and controls (ch_rep, ch_rep², ch_ic_mean, ln anchors). The Geometer asked that ln anchors be counted before deduplication; the Listener wrote it as anchors at P = 2. The chair settles it.
- **Agreed:** G2 (back-and-forth share) and I3 (the arrow of time, A) are one contrast (ρ −0.96 on the notes); A runs, G2 is reported.
- **Agreed:** card 1's own recommended "loop thickness" is not a separate measure (residual clip-to-clip 0.05; ρ −0.68 with M).
- **Withdrawn:** L3 (contour surprise: it measures how repeated notes were transcribed). Stopped by its authors on the notes: the melody margin (clip-to-clip 0.11), melody plus chords (0.19), the second H1 bar (0.16), "the tune changes when the chords return" (0.155 to 0.18), phrase-end tonic closure (0.14).
- **Split:** the Skeptic predicts that fame (the artist's number of Hooktheory songs, clips per song) explains far more of y_foreign than the notes do, and that the chord-repetition lead is carried by prolific artists. The imaginers did not take a stand on it. It runs as its own test.
- **Split:** M's authors read the margin as robustness that invites re-recording (two-part story, take-up face). The Skeptic warns it may be cover-factory familiarity, not love; the karaoke-removed outcome is reported.
