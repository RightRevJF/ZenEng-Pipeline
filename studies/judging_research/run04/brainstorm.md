# Run 04 brainstorm (24 November 2026)

Three imaginers with fixed stances (the Geometer leading, per the mathematics focus), then the Skeptic, then each imaginer's answer. All measure-side checks used the notes only; no outcome, cover count, first year or match status was opened by any imaginer or the Skeptic. Scratch scripts stayed outside the repo. Saved verbatim from the agents' files.

## Round 1

### The Geometer


Common recipe: each chord is a pc set (root plus cumulative intervals), with repeats merged and durations in beats; a_k = Σ_x e^{-2πikx/12}; a song's value is its clip mean. Lemma 2 makes all three key-free, and none has a fitted setting. They need the notes, so they can be tested only on the ~1,924 matched songs within artist against log(1+covers), not on the extensive margin.

**G1. Diatonicity, |a₅|/a₀**
- (a) Harmony held in one diatonic region travels: a cover can re-key, revoice or invert it, and Theorem 1 with Lemma 2 keeps the value exactly.
- (b) D5 = |Σ v_x e^{-2πi5x/12}| / Σ v_x, where v is the duration-weighted chord profile. By linearity and the triangle inequality, D5 = the chord's own |a₅|/a₀ × the concentration of the chords' φ₅.
- (c) clips.json harmony.
- (d) **+0.025 SD per SD**, holding ch_rep, ch_ic_mean, size, log clips and first year. *Extrapolation:* a song that lasts loops little but stays near home.
- (e) Killed if β < +0.005, or if β halves when ch_ic_mean or FP is added.

**G2. P/L/R share on the 2-D torus**
- (a) Amiot's table: a triad's three nearest neighbours (≤1.229; the next is 1.656) are exactly P, L and R, the two-common-tone moves any arranger can revoice.
- (b) The share of chord changes, clip looped, with sqrt(w(Δφ₃)²+w(Δφ₅)²) < 1.25. Any cut in (1.229, 1.656) gives the same result on triads.
- (c) As G1.
- (d) **+0.02**.
- (e) Killed if β < +0.005.
- Not the fifths path: FP used φ₅ alone, so V→vi scored 0 and IV→V one notch. On the torus they are 2.50 and 3.31, and I→vi, at 1.065, is the shortest move. ρ(PLR, FP) = −0.19.

**G3. Thirds axis, |a₃|/a₀**
- (a) Lemma 2 exactly: transposing by t multiplies a₃ by e^{-iπt/2}. Chords a major third apart add; chords a whole step apart (IV–V, ♭VII–I), which share no tone, cancel.
- (b) As G1 with k = 3. Examples: IV–V 0; ii–V–I 0.11; I–IV–V 0.25; I–V–vi–IV 0.33; I–vi 0.67.
- (c) As G1.
- (d) **+0.02**. *Extrapolation:* with shared tones, the tune fits either chord, so covers can reharmonise.
- (e) Killed if β < +0.005.

**Power:** about 0.2 to 0.3 each at p < .05 (SE ≈ 0.018), so a kill is the likeliest informative result.

---

## Notes-side checks (no outcome opened; `torus.py`, `extra.py`, `size.py` in this folder)
5,561 clips; 118 have fewer than 2 chord runs. That leaves 3,047 songs, and 1,498 of them have at least 2 clips.

| Measure | Clip to clip (pairs) | After chord-count dummies | ρ ch_rep | ρ ch_ic_mean | ρ n_ch | ρ distinct chords | ρ FP | Largest other \|ρ\| |
|---|---|---|---|---|---|---|---|---|
| G1 D5 | **0.432** (1,498) | 0.377 | +0.20 | −0.36 | −0.10 | −0.40 | **−0.65** | ch_ic_sd −0.41 |
| G2 PLR | **0.316** (1,495) | 0.306 | −0.02 | +0.11 | +0.02 | +0.12 | −0.19 | ch_ic_mean +0.11 |
| G3 D3 | **0.322** (1,498) | 0.316 | +0.08 | −0.26 | −0.16 | −0.27 | −0.02 | ch_ic_mean −0.26 |
| *FP (run 03, reproduced)* | 0.342 | | −0.10 | +0.24 | +0.03 | | 1 | ch_ic_sd +0.28 |

The "Largest other |ρ|" column covers all chord and melody surprise fields, six rhythm fields and clips per song. Between my own measures: D5–D3 +0.12, D5–PLR +0.12, D3–PLR +0.28.

Unit checks reproduce card 1: d(C,G) = d(C,F) = 1.656, d(C,Am) = 1.065, d(C,Cm) = d(C,Em) = 1.229.

**Considered and dropped on the notes side:**
- **R5** (circular concentration of φ₅): ρ −0.81 with FP. It is the fifths path in another form, so I used D5 instead.
- **Winding numbers and signed area (recipes 3 and 4).** Lemma 2 says a whole-step move between chords of the same quality is an exact half-turn in φ₃ (t = 2, 6 and 10, not only the tritone as card 1 says). This happens on 7,624 steps, so a lift convention decides the result. With Lemma 2's smallest-root-motion lift, 53% of clip loops wind around φ₃; I–IV–V–I already winds once. The area is then defined for only 1,754 songs, and which songs those are depends on the harmony. It is also stable only on 430 pairs (0.44).
- **Mean 2-D step (TS):** clip to clip 0.368, but ρ +0.60 with the half-turn share. It mostly counts IV–V moves.
- **Melody-weighted D5:** clip to clip 0.241, a weak tune measure.
- **Extensive margin:** none of these measures can be built from the surprise or rhythm fields. Testing them on the 9,588 songs would need the pitch-class notes for every Hooktheory song, computed for all 13,198 alike and never split by match status.

### The Listener


**L1. Did anyone want to learn it? Move plainly, on the extensive margin.**
(a) A musician records a song they can learn fast and not tire of: chords that move (low `ch_rep`), plainly (low `ch_ic_mean`). "A second act released it" is where one musician's wish shows, before fame piles up counts.
(b) MP = −(z`ch_rep` + z`ch_ic_mean`); song = clip mean; z over the 9,588 songs; equal weights, fixed now. One test; each half reported, deciding nothing.
(c) `surprise.json`; in Discogs-VI (0/1); 9,588 songs, 1,741 artists; linear, artist fixed effects, holding mean `n_ch`, log mean beats, log clips per song (fame; also transcribers' wish to learn, so holding it is conservative); SE clustered by artist.
(d) **+1.2 pp** of P(in Discogs-VI) per SD of MP (≈ −1.0 pp per term-SD; 6% of the 21% base). Proxy SE 0.56 pp, power 0.58 (α .05).
(e) Killed if β < +0.4 pp. "Plainly" alone is killed if the `ch_ic_mean` half is weaker than −0.3 pp.

**L2. Pitch proximity on Amiot's torus.**
(a) On Amiot's torus a triad's nearest neighbours are exactly its P, L, R relatives (two notes kept, one moves by step). Short steps are harmony obeying pitch proximity, listeners' most robust expectation, so inner lines stay hearable and singable.
(b) TS: per clip, merged chord runs (fifths-path token and wrap rule); chord at (φ₃, φ₅) of its 0/1 pc-set; mean flat-torus geodesic step, both differences wrapped; steps with an undefined phase dropped, counted; song = n_mel-weighted mean of clips. No settings.
(c) `clips.json`; covers within artist (~1,924 songs); run 03's within() holding `ch_rep`, `ch_ic_mean`, size block, log clips, first year.
(d) **Extrapolation:** −0.025 SD of log(1+covers) per SD (shorter steps, more covers). Unlike the fifths path, it scores V→vi (2.50) and IV→V (3.31) long: every voice moves. It barely overlaps surprise (ρ −0.06): a pass would mean plainness is acoustic, not learned. Power about 0.2.
(e) Killed if β ≥ 0.

**L3. The one chord you remember.**
(a) Memory keeps the odd event in a plain field (isolation effect): surprise packed into a few chords hands the learner "that chord".
(b) CV = `ch_ic_sd`/`ch_ic_mean` per clip, mean over clips.
(c) `surprise.json`; L1's model plus MP's two terms.
(d) +0.6 pp per SD. Power about 0.2. Kin to failed J3 (Cheung), which asked where surprise falls against uncertainty, not how concentrated it is.
(e) Killed if β ≤ 0.

---

## Measure-side numbers (notes only; no outcome or match status opened)

Scripts: `/home/claude/scratch/listener/check_a.py`, `check_b.py`, `check_c.py`.

**Extensive-margin rows (`surprise.json`):** 13,198 songs; 1,741 artists with 2+ songs, 9,588 songs. Clips per song in those: 1: 5,317; 2: 2,533; 3: 1,123; 4+: 615.

| Measure | Clip-to-clip ρ (5,436 songs) | Largest \|ρ\| with ch_rep / ch_ic_mean / n_ch (song level, 9,588) | Gate |
|---|---|---|---|
| MP (L1) | 0.318 | n_ch −0.45 (beats −0.22, clips +0.01) | passes |
| ch_rep | 0.328 | ch_ic_mean −0.33 (within artist −0.24) | (existing) |
| ch_ic_mean | 0.513 | | (existing) |
| CV (L3) | 0.269 | n_ch +0.29; ch_rep +0.01; ch_ic_mean 0.00; ch_ic_sd +0.59 | passes |
| ch_ic_sd (rejected for L3) | 0.459 | ch_ic_mean **+0.78** | fails |

Power proxies (LPM with artist fixed effects, homoskedastic, y variance taken as 0.21 × 0.79, an upper bound; clustering would raise the SE, dropping artists with no matched song would change N):
- MP: within-artist residual variance share 0.56; SE 0.56 pp; power 0.58 at +1.2 pp (α .05), 0.30 at +0.8 pp.
- Two terms separately: ch_rep SE 0.60 pp, ch_ic_mean SE 0.57 pp; power at −1.2 pp each (α .025) 0.40 and 0.45.
- CV: SE 0.50 pp; power 0.26 at +0.8 pp (α .025), about 0.2 at +0.6 pp.

**Torus (`clips.json`, 2,769 songs with notes, 4,775 clips).** Unit checks reproduce card 1: d(C,Am) 1.065, d(C,Cm) = d(C,Em) 1.229, d(C,F) = d(C,G) 1.656, d(C,Fm) 1.824, d(Cm,D) 3.26. Worked: I–V–vi–IV has TS 1.760, I–IV–V 2.208, I–bVII–IV 2.208.

| Torus measure | Clip-to-clip ρ (1,295 songs) | Overlaps (song level) | Verdict |
|---|---|---|---|
| **TS, mean step (L2)** | **0.367** | ch_rep +0.03, ch_ic_mean −0.06, n_ch 0.00, distinct chords −0.03, clips +0.01, fifths path +0.35 | passes; a new axis |
| PLR share (steps < 1.25) | 0.363 | TS −0.67 | TS's complement; not proposed |
| R5, phase concentration (DFT linearity) | 0.408 | fifths path **−0.80** | fails (fifths path renamed) |
| Isolation (max − mean step) | 0.264 | distinct chords +0.37, n_ch +0.32 | passes; not proposed |
| Signed area (recipe 4) | 0.205 (800 closed clips) | ≤ 0.07 | **not usable**: see below |

**Winding and area warning.** φ₃ moves by exactly ±π on every whole-step root move between same-quality chords (IV→V, I→bVII, bVI→bVII), not only on tritones as the card says (transposing by t shifts φ₃ by −πt/2, so t = 2, 6 and 10 all land on ±π). These moves are everywhere in pop, so W₃ and the signed area depend on an arbitrary wrap: 49% of the 3,560 closed clips get W₃ ≠ 0 (W₅ ≠ 0 only 2%), and I–IV–V gets W₃ = −1. Step length is unaffected. Do not build tests on winding or area from these clips.

Power for TS is borrowed from the fifths path's SE (0.018; it has similar stability): about 0.20 at −0.025 (α .025), 0.28 at α .05.

### The Inventor


## I1. Balance on the thirds circle (Amiot, Lemma 2 + Theorem 1)
(a) Lemma 2 puts triads a major third apart at the same φ3 and spreads the diatonic triads round φ3 in the chain of thirds (I, iii, V, ii, IV, vi). |a3|/a0 is then the centre of mass of chord time on that circle: low means the tonic, subdominant and dominant regions are spanned evenly.
(b) B3. For each clip, v[pc] = Σ (offset − onset) over chords, counting each pc of root + cumsum(intervals) once. B3 = |Σ v[x]·e^{−2πi·3x/12}| / Σ v; song value = mean over clips. Reference values: one triad 0.745; I–V–vi–IV 0.333; I–IV–V 0.248; I–vi–ii–V 0.167.
(c) clips.json.gz, about 1,924 songs in 420 artists.
(d) Theorem 1 makes B3 invariant under transposition and major/minor inversion, so it survives re-keying. *Extrapolation:* a balanced song holds a full cadence and stands alone with voice and guitar. Prediction: **−0.025 SD** of log(1+covers) per SD within artist, holding ch_rep, ch_ic_mean, size, log clips and first year.
(e) Killed if β > −0.01.

## I2. The harmonic ratchet
(a) Closed loops have zero net fifths drift, so the third moment is the lowest-order step statistic that is transposition-invariant but odd under inversion (Lemma 2) and under retrograde. Negative means the harmony creeps sharpward and falls flatward in one leap: stick-slip.
(b) K5 = mean(s³)/mean(s²)^{3/2}. Here s is the wrapped φ5 step between distinct chords, including each clip's wrap, with undefined phases dropped and steps pooled over the song's clips. Reference values: I–V–vi–IV −0.82; I–IV–V +0.71.
(c) As I1.
(d) *Extrapolation:* listeners keep the build-then-release shape. Prediction: **−0.02 SD** per SD (more negative, more covers), with I1's controls.
(e) Killed if β > −0.01.

## I3. Information rate (speech analogy, extensive margin)
(a) Languages converge on one information rate (my recollection of Coupé et al. 2019, not checked). A song far from the habitual rate either bores or overloads the listener.
(b) For each clip, r = (n_mel·mel_ic_mean + n_ch·ch_ic_mean)/beats. D = |ln r − ln 4.32|, where 4.32 is the median over all 21,998 clips; song value = mean of D.
(c) surprise.json.gz; 9,588 songs in 1,741 artists.
(d) Prediction: **−0.8 pp** of P(in Discogs-VI) per SD within artist, holding log clips, n_ch and beats. Power is roughly 0.4. The rate is per beat because there is no tempo.
(e) Killed if the estimate is above −0.3 pp.

---
## Appendix: measure-side numbers (notes only; no outcome or match status opened)
Clip-to-clip is the Spearman correlation between clip 1 and clip 2 of the same song. "Largest overlap" is the largest |ρ| with ch_rep, ch_ic_mean, n_ch, the 17 data-pack fields, clips per song and the fifths path (FP).

| ID | Songs | Clip-to-clip (pairs) | Largest overlap | Gate |
|---|---|---|---|---|
| I1 B3 | 2,763 | 0.332 (1,297) | ch_ic_mean −0.27; ch_ic_sd −0.26; ch_rep +0.08; n_ch −0.17; FP 0.00 | passes |
| I2 K5 | 2,750 | 0.237 (1,281) | all ≤ 0.06 | passes (narrowly) |
| I3 D | 13,198 | 0.282 (5,436) | mel_ic_mean +0.16; ch_ic_mean +0.08; ch_rep −0.01; n_ch −0.02 | passes |

Invariance: B3 came out identical under transposition and inversion on random clips.

Stopped or dropped at the measure stage:
- **Signed area and winding on the torus.** A whole-step move between triads of the same quality (IV→V, ♭VII→I) is exactly ±π on φ3. As a result, 53% of clips wind on φ3, depending on how that tie is broken. The area of a loop that winds depends on where it starts, and it failed the retrograde check (I–IV–V gives 0 forwards and 0.548 backwards).
- **Kuramoto R5.** ρ −0.81 with FP.
- **Raw information rate r.** ρ +0.75 with density.
- **Melody–harmony φ5 lag.** Clip-to-clip 0.06 (|lag|) and 0.19 (signed).
- **Diatonicity |a5|/a0.** Clip-to-clip 0.465, but ρ −0.65 with FP and −0.36 with ch_ic_mean: plainness under a new name. Kept as a backup.
- **P/L/R share.** Clip-to-clip 0.362, but ρ −0.63 with torus step length.
- **Free-connector time share.** Zero in 86% of songs.

## Round 2: the Skeptic


**Shared.** All clips.json tests reuse run 03's ~1,924 songs: not fresh, and every one is below the 0.5 power floor (only L1 clears it). Bonferroni over all frozen tests, stopped ones included. One kill form: wrong sign or weaker than 0.01 SD / 0.3 pp.

**G1.** FP renamed (rho -0.65) plus chord quality; its sign was set after FP leaned. Hold FP and non-triad share, or drop it.

**G2/L2.** Merge into one test with PLR share primary: it holds for any cut in (1.229, 1.656) and under the stretched metric. TS mostly counts IV-V half-turns (rho +0.60). The a-priori case is weak: I-IV-V-I has zero PLR moves.

**G3/I1.** Same number, opposite signs. I1 misreads it: IV-V alone scores 0 ("balanced"), with no tonic. G3's shared-tone story fits the measure. One two-sided test, counted once: > +0.005 G3 passes and I1 dies; < -0.01 the reverse; between, both die. Hold distinct-chord dummies.

**I2.** Skew of about 4 steps is the sign of the largest step. Tritone steps on phi5 sit at exactly +-pi and their sign is arbitrary: drop them and count them. It is inversion-odd, so hold the minor share.

**L1.** The composite mixes ch_rep (replicated) with surprise (unplanned). Use run 03's frozen two-term form; kill if ch_rep is weaker than -0.3 pp. n_ch as dummies (rho -0.45).

**L3.** The SD of a few surprises tracks n_ch: dummies.

**I3.** A per-beat rate rides on the transcriber's half- or double-time choice: hold density, bpb, beats.

**Extensive margin.**
- **Hold:** dummies for clips per song and n_ch, log beats, and title genericness from the Hooktheory title only (one word; repeated title; parentheses). Era comes only through the artist FE; drift across a career is unheld, stated as such.
- **Model:** LPM with artist FE is fine, SE clustered. Correction: in an LPM, all-zero artists are NOT weightless. They enter the x-variance and pull beta toward zero. Only conditional logit drops them. Rule, frozen before the join: keep every artist with >=2 songs; LPM primary; conditional logit must agree in sign; report how many artists it drops.
- **Meaning:** a pass means documented re-release by two performer sets under the same title and writer, within artist. It is not lasting love. Noise unrelated to the notes only attenuates: a pass is conservative, a null weak. Noise that tracks the notes can create a result: singles get compilation "versions" and credits (clips per song holds fame only partly), and translated covers miss international hits. Feat./remix false versions favour loops (high ch_rep), so an L1 pass survives that one.

## Round 2: the answers

### The Geometer


**G1: withdrawn to the backlog.**
- Its sign was set after the fifths path (FP) leaned, and each extra test raises the bar for every test.
- Holding FP and non-triad share, D5 stays stable (0.394 clip to clip; rank R² 0.44), so it is worth testing on fresh songs.

**G2: merged with L2, PLR share primary.**
- **Controls:** run 03's within() (ch_rep, ch_ic_mean, distinct-chord dummies, links, log clips, first year).
- **Robust:** any cut in (1.229, 1.656), and the stretched metric, give the same 36 P/L/R pairs (≤1.004 vs ≥1.483).
- **Prediction:** +0.02 SD. **Kill:** β < +0.01.
- TS is reported only. The a-priori case is weak, I concede.

**G3 = I1: one two-sided test of D3, counted once, same controls.**
- **Prediction:** +0.02 SD.
- **Rule:** β ≥ +0.01, G3 survives and I1 dies; β ≤ −0.01, the reverse; otherwise both die.

### The Listener


**L1: revised.** I drop the composite for run 03's frozen two-term form: `ch_rep` decides, `ch_ic_mean` is held and reported.
- **Model.** LPM, artist fixed effects, every artist with 2+ songs (9,588 songs), SE clustered by artist. Conditional logit must agree in sign; report how many artists it drops.
- **Controls.** Dummies for n_ch and clips per song, log beats, title-genericness flags from the Hooktheory title (one word, repeated, parentheses).
- **Prediction.** `ch_rep` −1.0 pp per SD, `ch_ic_mean` −1.0 pp.
- **Kill.** `ch_rep` positive or weaker than −0.3 pp.
- **Power.** About 0.4 at α .05, below the 0.5 floor.

**L2: merged into G2.** PLR share is primary, with distinct-chord dummies. TS mostly counts IV–V half-turns (ρ −0.67 with PLR). Prediction +0.02 SD per SD; kill if wrong sign or weaker than +0.01.

**L3: withdrawn.** Power about 0.2, and it tracks n_ch. It would spend α on the one fresh outcome.

### The Inventor


**I1: withdrawn; merged into G3.** The Skeptic is right: IV–V scores 0 with no tonic, so B3 measures whole-step cancellation, not balance. I accept the one two-sided test, counted once, with distinct-chord dummies: above +0.005, G3 passes and I1 dies; below −0.01, the reverse; in between, both die.

**I2: withdrawn.** On about 4 steps the skew is the sign of the largest step. It is odd under inversion, so tied to mode. At clip-to-clip 0.237 and power about 0.1, it only spends Bonferroni budget.

**I3: revised.** D = |ln r − ln 4.32|, unchanged. After density, bpb and log beats are removed (R² 0.07), clip-to-clip is still 0.290 (5,422 pairs).
- **Controls:** those three; dummies for clips per song and n_ch; the title flags.
- **Model:** LPM with artist FE, SE clustered; conditional logit must agree in sign.
- **Prediction:** −0.8 pp per SD.
- **Kill:** wrong sign or weaker than −0.3 pp.

## Where they agreed and split

- **Agreed:** winding numbers and signed area on the torus are not usable on pop loops. Any whole-step move between chords of the same quality (IV to V, I to bVII) lands exactly on a half-turn in phi_3, so the sign is arbitrary. All three found this independently; it corrects card 1, which named only the tritone.
- **Agreed:** phase concentration on the fifths circle (R5) is the fifths path renamed (rho about -0.8), and so stopped.
- **Merged:** G2 (share of P/L/R moves) and L2 (mean torus step) became one test, with the P/L/R share as the measure. G3 and I1 are the same number, |a3|/a0, with opposite predicted signs. They became one two-sided test, counted once.
- **Split:** the Geometer reads a high |a3| as shared tones that invite reharmonising. The Inventor first read a low |a3| as balance among tonic, subdominant and dominant. The Skeptic showed that IV to V alone scores 0 with no tonic at all. The Inventor then withdrew his reading, but the test keeps both outcomes open.
- **Withdrawn:**
  - G1, diatonicity: its sign was set after the fifths path leaned. It goes back to the backlog for fresh songs.
  - L3, the one chord you remember.
  - I2, the harmonic ratchet.
- **New outcome:** the Listener and the Inventor moved two proposals onto the first fresh outcome in weeks: whether a song is in Discogs-VI at all, within artist, across about 9,588 songs. The Skeptic corrected one claim. In a linear model, artists with no matched song are not weightless, so the rule must be frozen before the join.
