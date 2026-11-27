# Run 09: the brainstorm

27 November 2026, the 10:17 ET pass. Three imaginers (round 1), the Skeptic (round 2), and each imaginer's reply. No outcome was opened by any of them. Scripts used for measure-side checks are in /home/claude/scripts/<name>/ (outside the repo); every recipe frozen by the chair is copied into experiments/measures09.py.

Yield given to the Skeptic and the replies (counted from clique titles, writers and performers only): 1,283 unseen songs.

---

## Run 09, round 1: the Geometer

27 November 2026. Notes only. I opened no outcome and called no outcome loader. I read only `charts_run08.json` and `charts_run09.json`.

## The check that shaped the proposals

Card 1's signed areas are stable between two charts from the same source, at 0.73 to 0.81. Between chart writers they are not. When a Real Book or BiaB chart is compared with the iReal chart of the same title, they agree only 0.28 to 0.36. That holds for M1, M3, M5, my tension engine, its wrapped form and its ii-collapsed form (table B).

The signature shape vector does worse. I used the level-3 log-signature of (τ, u, h). It finds the same tune within one source (median rank 0.1%), but across sources its median rank is 32%. A plain four-number size and vocabulary vector does better, at 9%. So I withdraw shape heritability by signature.

**Why.** Lévy area is S^{12} − S^{21}, the difference of two large terms, and on an open path it depends on where the chart starts and ends. The unwrapped fifths path also jumps by 6 whenever a writer swaps a dominant for its tritone substitute. Terms that are sums of squares do not cancel, and they survive a change of writer (TQ 0.50).

## G09-1: Tension breathing, TQ (card 1, lead-lag)

1. **Mechanism.** By the lead-lag theorem, a path's lead-lag Lévy area is half its quadratic variation. For the tension channel, that is how often the harmony switches between tritone and rest.
2. **Recipe.** h = 1 if the chord's pitch-class set holds a tritone. TQ = ½ · mean over changes of (Δh)², computed as \|A(lead, lag)\| / n_chg.
3. **Data.** charts_run09 (unseen).
4. **Prediction.** +0.03 SD per SD. Holding IIV, +0.01 (a reading only).
   - What the mathematics says: only even-order terms survive a change of chart writer, so any song shape upstream of the chart should show in them.
   - **Extrapolation:** a song that lasts runs an engine of expectation and release, switching often.
5. **Kill.** +0.03 lies outside the 95% range.

## G09-2: Tritone resolution on the ii-collapsed path, TR (voice-leading geometry; quotient by ii insertion)

1. **Mechanism.** A dominant's tritone resolves by two contrary semitones. G7→C and D♭7→C share that tritone and that motion. Deleting every "ii" before its V gives a measure that adding or dropping ii-Vs cannot move. That is exactly what the obstacle says chart writers do.
2. **Recipe.** Delete each m7 that is followed by a d7 a fourth up, then merge repeats. TR = (d7 → root down a fifth or down a semitone) / changes.
3. **Data.** charts_run09: charts plus recordings.
4. **Prediction.** If the ii-V lead is the song's goal-directed resolution, +0.04. If it is chart-writer decoration, about 0 while IIV stays positive; this contrast is a lead, not counted. Non-jazz reading +0.02.
5. **Kill.** +0.04 lies outside the 95% range.

## G09-3: Tension engine, TE (card 1, Lévy area and the shuffle identity; estimate only)

1. **Mechanism.** By the shuffle identity, S^{uh} + S^{hu} reads only the endpoints, so the order of events is carried by the area alone.
   - Tension built on the sharp side and held while roots fall by fifths gives a positive area (ii–V–I gives +1).
   - A jump up to V from IV gives a negative one (−½).
2. **Recipe.** Path (u, h), with u the unwrapped fifths position (shortest step −5..+6). TE = A / n_chg on the open path.
3. **Data.** charts_run09.
4. **Prediction.** +0.02. This is an estimate only, since the cross-writer agreement is 0.28.
5. **Kill.** None (estimate).

## Checks

Recipes are frozen in `/home/claude/scripts/geometer/g09_measures.py` (TE, TR, ii_collapse, SIG, CH, base; unit tests reproduce card 1's Eq. 37–39 and time reversal) and in `g09_tq.py` (TQ). The checks are `g09_checks.py`, `g09_alt.py` and `g09_tq.py`, with outputs in `g09_*.json`. They took about 2.5 minutes of compute in total.

How to read the columns:
- **Stab** is over 3,796 run 08 pairs, grouped by normalised title plus artists, with identical chord lists skipped. Many pairs are near-duplicates (forum against playlist), so these values run above the chair's design-song figures (IIV here 0.916, against 0.772 in run 08).
- **Cross** compares a run 09 Real Book or BiaB chart with the first run 08 iReal chart of the same normalised title, for titles of two or more words (n = 2,475).
- **ρ** is pooled Spearman over run 08 charts, with run 09 in brackets.

**A. Proposals**

| | computable run 09 | Stab | Cross | ρ ch_rep | ρ V | ρ ln_chg | ρ IIV | ρ CH | Gate |
|---|---|---|---|---|---|---|---|---|---|
| TQ | 0.992 | 0.900 | 0.503 | −0.14 (−0.19) | 0.40 (0.20) | 0.11 (−0.10) | 0.57 (0.46) | −0.40 (−0.34) | passes |
| TR | 0.992 | 0.905 | 0.60 RB / 0.63 BiaB | −0.16 (−0.16) | 0.30 (0.10) | 0.02 (−0.16) | 0.48 (0.38; recordings 0.66) | −0.43 (−0.42) | passes |
| TE | 0.992 | 0.750 | 0.28 | 0.00 (0.04) | −0.09 (−0.13) | −0.06 (−0.08) | 0.06 (0.09) | −0.02 (−0.17) | passes; fails cross ≥ 0.5 |
| IIV (reference) | | 0.916 | 0.61 | | | | | | |

TQ against TR: ρ 0.74 (run 08), 0.56 (run 09).

**B. Card 1's areas, cross-writer (`g09_alt.py`)**

| Measure | Stab | Cross |
|---|---|---|
| TE | 0.75 | 0.28 |
| TE wrapped | 0.74 | 0.32 |
| M5 root–quality | 0.80 | 0.36 |
| M1 pitch-set fifths-plane | 0.81 | 0.36 |
| M3 arch (τ, u) | 0.75 | 0.29 |
| TE ii-collapsed | 0.73 | 0.29 |

M1 against chirality: ρ 0.48. SIG coordinates cross-writer: 0.14 to 0.39.

**C. Run 09 partition means (TR / IIV)**

| Partition | TR | IIV |
|---|---|---|
| Real Book | 0.28 | 0.09 |
| BiaB | 0.27 | 0.09 |
| weimar | 0.37 | 0.14 |
| jaah | 0.36 | 0.11 |
| isophonics | 0.05 | 0.003 |
| uspop2002 | 0.05 | 0.01 |
| rock-corpus | 0.03 | 0.003 |

Non-jazz TR is sparse, so its power will be low.

---

## Run 09, round 1: the Listener

27 November 2026. Notes side only. No outcome was opened: I read nothing under /home/claude/shape/ or /home/claude/dl/discogs/, no data/*.json, no covers, versions or HOLDOUT file, and I called no loader from common.py (only `nrm`). Scripts live outside the repo, in `/home/claude/scripts/listener/`: `checks_r09.py` (output `checks_r09_out.json`) and `checks_r09b.py` (output `checks_r09b_out.json`). Each runs in under a minute. Both use `measures.listener_measures` from run 08 for IIV, ch_rep, V and ln_chg.

## Proposals (about 400 words)

**R09-L1. The upstream ii-V, decomposed by writer (this targets the obstacle).**
1. *Mechanism:* if the song itself has the ii-V, a chart written outside the iReal community will carry it too and will predict covers. If iReal writers add the ii-V, only the iReal-minus-upstream gap will predict covers.
2. *Measure:* IIV_up is the mean IIV over the title's real-book and biab charts. GAP = IIV_iReal − IIV_up, where IIV_iReal is the mean over the iReal charts that share the most common artists string. Titles must match under nrm (brackets dropped, trailing ", The" moved to the front) and have at least two words. Both terms enter together, z-scored, in the iiv_singletons columns.
3. *Data:* 1,147 titles shared with real-book and 1,148 shared with biab. Most are run-08 songs that have already been seen, so this run is a lead. The counted version uses unseen cliques that have only real-book or biab charts and enters IIV_up alone.
4. *Prediction:* under the song story, b_up = +0.045 (that is +0.07 × the writer agreement of 0.64) and b_gap is about 0. Under the writer story, b_up ≤ +0.01 and b_gap ≥ +0.03.
5. *Kill (song story):* +0.045 lies outside b_up's 95% range.

**R09-L2. Fulfilled dominants (expectation kept; a test that adding a ii cannot fool).**
1. *Mechanism:* the strongest harmonic expectation a listener or improviser has learned is that a dominant seventh will resolve. A tune dense in kept promises is easy to hear, learn and improvise over. Putting a ii in front of a V leaves the count unchanged.
2. *Measure:* DRES = (pairs of change tokens in which a dom7 [bits 4 and 10 set, bit 3 clear] is followed by a root a fifth down (+5) or a semitone down (+11)) / bars. Bars = ⌊last onset⌋ − ⌊first onset⌋ + 1, on beats-timebase charts only. Second reading: FUL = resolved dom7s / all dom7 tokens, needing at least 2 dom7s.
3. *Data:* any chart partition.
4. *Prediction:* +0.04 SD per SD. With DRES held, IIV should fall to half or less.
5. *Kill:* +0.04 lies outside the range. As a lead on seen songs: if IIV stays at +0.06 or more with DRES held while DRES is about 0, the ii carries the effect, not the resolution (the writer's signature).

**R09-L3. Cadence arch (card 1: time augmentation, the area against time).**
1. *Mechanism:* a tune that saves its resolutions for the end of the form (the turnaround) pulls the band round again, chorus after chorus. A looping vehicle invites re-recording.
2. *Measure:* take X = (τ, N(τ)/N), with τ = normalised onset time and N counting resolution arrivals (the chord that DRES lands on). Its Lévy area is A = ½∫(τ dY − Y dτ) = mean τ of arrivals − ½, the card's "area against time relates to the mean". By Prop. 1, the time channel makes the signature determine the path. CARC = that area, needing at least 2 arrivals.
3. *Data:* any partition, including recordings timed in seconds.
4. *Prediction (extrapolation):* +0.02, a back-loaded form going with more covers. That is under the typical |b|.
5. *Kill:* +0.02 lies outside the range. Its writer agreement is already 0.35, under the 0.5 cross-source gate, so I expect it to run as an estimate only.

**Withdrawn before proposing: the tree-like lemma (M1 on roots).** By Chen's identity and the shoelace formula, a ii inserted over a held root (X | X7 → X | ii X7) is a back-tracked excursion. It is invisible to the signature exactly (checked: −0.25 = −0.25). A general insertion changes the area by the triangle (prev, ii, V). In practice FAc = chirality (ρ 0.985), which is a rename of the killed R06-I1, and simulated insertion moves it 0.34 SD. I keep it only as a diagnostic: across writers, ΔFA against ΔIIV is −0.33 (real-book) and −0.21 (biab). The lemma predicts that sign when the gap is made of inserted falling ii-Vs.

## Checks (notes only)

**Computable (charts measured / defined).** IIV and DRES are defined on 40,665 of 42,002 run-08 charts and 8,955 of 9,062 run-09 charts. DRES and FA need bars, so they are missing for recordings timed in seconds (isophonics, uspop2002, robbie-williams, jaah, weimar). FUL needs at least 2 dom7s: 31,073 run-08 and 8,118 run-09 charts. CARC needs at least 2 arrivals: 28,824 and 7,803.

**Stability and overlap (Spearman, chart level).**
- *Two-chart:* the first two non-identical charts of one nrm(title)+nrm(artists) group in run 08, 3,704 pairs.
- *Writer:* iReal against real-book (1,147 titles) and iReal against biab (1,148 titles), song means.

| measure | two-chart | writer: real-book | writer: biab | ρ ch_rep | ρ V | ρ ln_chg | ρ IIV | shift if a ii is put before every lone V (median, SD units) |
|---|---|---|---|---|---|---|---|---|
| IIV | 0.916 | 0.639 | 0.637 | −0.165 | +0.544 | +0.215 | 1 | 1.88 |
| DRES | 0.928 | 0.681 | 0.721 | −0.103 | +0.462 | +0.209 | +0.537 | 0.105 |
| FUL | 0.843 | 0.534 | 0.554 | +0.077 | −0.182 | −0.107 | −0.123 | 0.218 |
| CARC | 0.768 | 0.347 | 0.365 | −0.135 | −0.125 | −0.197 | −0.051 | 0.06 |
| FAc (area per root change) | 0.876 | 0.454 | 0.529 | +0.187 | −0.366 | −0.056 | −0.468 | 0.338 |
| ch_rep | 0.788 | 0.420 | 0.455 | | | | | |
| V | 0.917 | 0.649 | 0.727 | | | | | |

- **Caution on the two-chart column.** Pairs that cross partitions (forum against playlist against wikifonia, 1,219 pairs) agree at 0.95 to 0.99, so most of these pairs are near-copies. The writer columns are the honest stability.
- **Title collisions.** The writer columns include different songs that share a title. The subsets with one iReal artist give similar values; see the JSON.

**IIV by partition (chart level).**

| partition | n | mean | sd | median | share 0 |
|---|---|---|---|---|---|
| biab-internet-corpus | 4,965 | 0.093 | 0.101 | 0.059 | 0.35 |
| real-book | 2,802 | 0.088 | 0.095 | 0.059 | 0.33 |
| all recordings | 1,188 | 0.062 | 0.098 | 0 | 0.62 |
| weimar | 424 | 0.141 | 0.108 | 0.150 | 0.26 |
| jaah | 89 | 0.112 | 0.105 | 0.110 | 0.29 |
| isophonics | 225 | 0.003 | 0.014 | 0 | 0.92 |
| uspop2002 | 195 | 0.012 | 0.037 | 0 | 0.79 |
| rock-corpus | 193 | 0.003 | 0.017 | 0 | 0.95 |
| robbie-williams | 62 | 0.001 | 0.006 | 0 | 0.98 |
| (run 08) ireal-forum | 32,583 | 0.061 | 0.097 | 0 | 0.59 |
| (run 08) ireal-playlists | 2,031 | 0.120 | 0.112 | 0.100 | 0.29 |
| (run 08) wikifonia | 6,051 | 0.059 | 0.086 | 0 | 0.53 |

**Writer agreement on IIV (shared titles, song means; gap = iReal − other).**

| other source | titles | ρ | iReal mean | other mean | gap | p (Wilcoxon) | gap vs number of iReal charts |
|---|---|---|---|---|---|---|---|
| real-book (BiaB) | 1,147 | 0.639 | 0.119 | 0.103 | +0.016 | 7e-9 | +0.178 (+0.122 holding IIV level) |
| biab-internet | 1,148 | 0.637 | 0.105 | 0.105 | 0.000 | .39 | +0.058 (+0.007) |
| weimar (recorded solos) | 149 | 0.602 | 0.141 | 0.165 | −0.024 | .008 | −0.179 |
| jaah (recordings) | 45 | 0.738 | 0.153 | 0.141 | +0.013 | .44 | +0.009 |
| JSIR lead sheets | 31 | 0.356 | 0.175 | 0.227 | | | |
| uspop2002 / isophonics / rock-corpus | 84 / 94 / 118 | 0.72 / 0.27 / 0.45 | ~0.01 to 0.02 | ~0.00 to 0.02 | small | | |

**Reading.**
- *Real Book:* the real-book gap is +0.016, about 0.16 SD of IIV. It sits in the upper two IIV terciles (−0.005, +0.024, +0.028) and grows with how many iReal charts a title has (a notes-side stand-in for being played; it is not an outcome). That is the leakage pattern.
- *Other writers:* biab-internet shows no gap. Recordings of jazz solos (weimar) show *more* ii-Vs than iReal. So iReal is not uniformly the inflating writer.
- *Attenuation:* writer agreement of 0.64 means an upstream-only reading should shrink a true song effect by about a third.

---

## Run 09, round 1: the Inventor

27 November 2026. Notes only: no outcome, design count, covers, versions or HOLDOUT file was opened, and no outcome loader was called. Scripts are in `/home/claude/scripts/inventor/`, outside the repo.

## Proposals (about 400 words)

**R09-I1. The skeleton the signature sees (tree-like reduction; card 1, uniqueness: Hambly–Lyons).**
(1) The signature keeps everything about a path except retraced excursions. Embed each distinct chord as a generic point, and the tree-reduced chord walk is the free (stack) reduction of the change-token walk: A B A collapses to A, A B C A survives. The measure is the share of the harmony that the signature can see.
(2) IRR = (length of the stack-reduced walk − 1) / n_chg (recipe A).
(3) The new charts (yield songs) for the test; the run 08 charts for gates only.
(4) **Extrapolation:** if a song is remembered as a shape (Jason's statue), retracings are scaffolding and the irreducible walk is the statue. Songs that last should have a longer skeleton per change: **+0.03 SD per SD**, holding V, ch_rep and ln_chg.
(5) Killed if +0.03 lies outside the 95% range. Caveat: IRR ≈ 1 − 2·(local back-and-forth share), ρ −0.97. The theorem gives the name; the count is simple.

**R09-I2. Harmonic momentum: the variance ratio (card 1, lead-lag area = ½ quadratic variation; from finance, Lo–MacKinlay; from physics, Hurst).**
(1) Is the root walk on the fifths circle a random walk (VR = 1), a loop that keeps coming home (VR → 0), or a chain that keeps going (VR > 1)?
(2) VR4 = mean(4-step sum)² / (4 · mean step²) over the unwrapped fifths steps of root changes. This equals the lead-lag area of the path sampled every fourth root change, divided by 4 × the lead-lag area at every change (recipe B).
(3) As I1.
(4) **Extrapolation:** players carry tunes whose harmony travels, as in cycle chains and sequences. **+0.03**, holding IIV as well (ρ with IIV is 0.34 to 0.43).
(5) Killed if +0.03 lies outside the 95% range.

**R09-I3. Distance from the repertoire's expected signature (song-level reference shape; expected signature characterises a law, cited in card 1).**
(1) Make a song's chart a 4-channel path: time τ, fifths position u, tension h and third quality q. Take the path's six Lévy areas, and score how far the song sits from the centre of its own repertoire (its partition), with no outcome and no fitted weights.
(2) TYP = mean over the 6 areas of |2F(a) − 1|, where F is the partition's mid-rank CDF (recipe C). TYPM (Mahalanobis on normal scores) is the second reading.
(3) As I1. The reference is computed within each partition, leaving out nothing that matters at n ≥ 60.
(4) **Extrapolation, from evolution:** covering is selection on copies. Stabilising selection predicts that survivors sit near the type. Typical songs are covered more: **−0.02** per SD of TYP.
(5) Killed if −0.02 lies outside the 95% range. Renaming risk: ρ with V is 0.5 to 0.6, so V must be held.

**Power, honestly.** At |b| of 0.02 to 0.03 with an SE near 0.02, all three are likely to fall under the 0.2 floor unless the yield runs to several thousand songs. If so, they are estimates. I1 and I2 are the ones I would count.

## Check table (notes only; Spearman; `r09_out.json`)

Stability: the first two non-identical charts of one group (sorted ids). "Resid" = residual on [1, ch_rep, V, ln V, ln_chg]. The ρ values are chart-level, pooled.

| Measure | run 08 stab (3,704 pairs) | resid | run 09 stab (1,633) | weimar/jaah, same title, different recordings (115) | resid | ρ ch_rep 08 / 09 | ρ V 08 / 09 | ρ ln_chg 08 / 09 | ρ IIV 08 / 09 | Gate |
|---|---|---|---|---|---|---|---|---|---|---|
| IRR (I1) | 0.872 | 0.841 | 0.865 | 0.798 | 0.721 | −0.19 / −0.21 | 0.47 / 0.45 | 0.13 / 0.11 | 0.32 / 0.42 | passes |
| VR4 (I2) | 0.864 | 0.769 | 0.838 | 0.623 | 0.693 | −0.31 / −0.30 | 0.62 / 0.57 | 0.18 / 0.16 | 0.34 / 0.43 | passes |
| TYP (I3) | 0.779 | 0.685 | 0.728 | 0.623 | 0.401 | −0.12 / −0.16 | 0.60 / 0.51 | 0.33 / 0.24 | 0.40 / 0.37 | passes (weak upstream) |
| TYPM | 0.770 | | 0.733 | 0.703 | | −0.13 / −0.14 | 0.58 / 0.49 | 0.31 / 0.23 | 0.36 / 0.32 | passes |
| IIV (reference) | 0.886 | 0.861 | 0.830 | 0.713 | 0.709 | | | | | |
| ch_rep (reference) | 0.788 | | 0.853 | 0.543 | | | | | | |

Other notes:
- **Single areas** (stability 0.47 to 0.83): A_th is the weakest, at 0.47 on run 09. Every single area has |ρ| ≤ 0.29 with ch_rep, V, ln_chg and IIV.
- **Coverage.** 8,955 of 9,062 run 09 charts are measurable, and 8,857 have VR4 (at least 8 root changes).
- **Partition medians.** IRR is 0.60 in rock-corpus and 0.89 in weimar; VR4 is 0.22 in uspop and 0.57 in weimar. Like IIV, both mark jazz, so genre/partition must be held.
- **Duplicates.** Run 09's cross-partition title pairs (1,701, mostly biab-internet against real-book) include 294 with identical change tokens. Run 09's "stability" is inflated by these near-duplicates. The honest figures are run 08's column and the recordings column.
- **Unit tests in the script.** A vamp reduces to 0. Blues gives 0.6. A cycle gives 1. A fifths chain gives VR 4. The I-vi-ii-V loop gives VR 0. Card 1's shoelace example gives A = 2.

## Exact recipes (all read from the 12-bit chart format; chart filter as run 08: ≥ 8 events and ≥ 6 change tokens)

**Tokens.** (root, bitmap) with consecutive repeats collapsed, exactly as `measures.change_tokens`. n_chg = tokens − 1.

**A. IRR.**
- Stack = [t0]. For each later token t: if len(stack) ≥ 2 and stack[−2] = t, pop; else push t.
- IRR = (len(stack) − 1) / n_chg.
- The walk is open: no wrap from last to first.
- Song value = mean over its charts.

**B. VR4.**
- Roots of the change tokens, with consecutive equal roots collapsed.
- Each step s = (f(r2) − f(r1)) mod 12, where f(p) = 7p mod 12. Subtract 12 if the result is > 6, so steps run from −5 to +6.
- Need ≥ 8 steps.
- VR4 = mean over k of (s_k + … + s_{k+3})² / (4 · mean s_k²).

**C. TYP.**
- At each change token k, the channels are:
  - τ_k = cumulative duration before the token / total duration (uncollapsed events);
  - u_k = running sum of the B-steps over every token change (a quality-only change has step 0);
  - h_k = 1 − |Σ_{p∈set} e^{−2πi·5p/12}| / |set|, with the set relative to the root;
  - q_k = +1 if bit 4, else −1 if bit 3, else 0.
- Build the rectilinear path: hold (τ moves to the next onset, the others stay fixed), then jump. End at τ = 1.
- Translate the path to start at 0.
- For each of the 6 channel pairs (i < j): A_ij = ½ Σ (x̃ⁱ_{k−1} x̃ʲ_k − x̃ⁱ_k x̃ʲ_{k−1}). Divide the three areas without τ by n_chg.
- Within the chart's partition (run 08 partitions for run 08 charts), take F_j = (rank + 0.5)/n for each area. TYP = mean_j |2F_j − 1|.
- TYPM = √(zᵀ Σ⁻¹ z), with z = Φ⁻¹(F) and Σ the partition covariance of z.

## Scripts
- `/home/claude/scripts/inventor/r09_measures.py`: all measures, the unit tests, the gates and stability, written to `r09_out.json`. Runs in about 1 minute.
- `/home/claude/scripts/inventor/r09_dupcheck.py`: the near-duplicate count across run 09 partitions.

---

## Run 09, round 2: the Skeptic

No outcome opened. SE ≈ 0.029.

## For every test
- **"Upstream" mostly is not.** The Real Book came from canonical recordings. Weimar and JAAH transcribe jazz covers. Only about 110 pop transcriptions read an original, with IIV near 0. So a pass on RB or BiaB charts means "outside iReal", not "before covering".
- **Genre is partition.** Pop has almost no ii-Vs, so jazz, RB and BiaB carry the slopes (effective N about 950). Compute power with partition dummies in.
- **Title-only matches (985)** pull estimates toward 0. Check on the 298 title-plus-name songs.
- **Halves.** Hash the writer string (else performer); freeze now.

## Each proposal
- **Frozen ii-V confirmation.** Power is 0.43, under its own frozen 0.5. Count it under the 0.2 floor and state the relaxation. With writer agreement at 0.64, the song story expects about +0.035 on RB and BiaB charts, so +0.02 would be "unsettled". The non-jazz reading is an estimate.
- **L1.** Its counted form is the frozen test on RB and BiaB charts, so merge the two. Run GAP on the seen titles as a lead, holding log(number of iReal charts).
- **G09-2 TR = L2 DRES:** both count dominants resolving down a fifth or a semitone, so merge them. Make TR primary and DRES per bar the second reading. Predicted +0.04, so it counts only if fake-outcome power is at least 0.2 at .05/2. Run IIV holding DRES as a seen-song lead.
- **G09-1 TQ** is dominant density renamed (ρ IIV 0.57). Estimate, holding IIV and V.
- **G09-3 TE.** Cross-writer agreement is 0.28. Estimate, low priority.
- **L3 CARC.** Cross-writer agreement is 0.35, and BiaB intros and endings shift it. Compute it on one chorus. Estimate.
- **I1 IRR** is local A-B-A repetition renamed. Hold ch_rep, V and ln_chg. Estimate.
- **I2 VR4.** Fifth chains are mostly ii-V chains. Compute it on the ii-collapsed path and hold V. Estimate.
- **I3 TYP.** BiaB's genre mix sets what counts as "typical". Take the reference within coarse genre and hold V. Estimate.

## Ranking
**Counted (K ≤ 2):**
1. The frozen ii-V confirmation, on all 1,283 songs.
2. Merged TR/DRES, if fake-outcome power is at least 0.2 at .05/2. Otherwise K = 1.

**Unseen estimates:** IIV on RB and BiaB only, the non-jazz reading, TQ, IRR, VR4, TYP, CARC and TE.

**Seen-song leads:** GAP holding log(number of iReal charts), and IIV holding DRES.

---

## Run 09, round 2: the Geometer

No outcome opened. Recipes are frozen in `/home/claude/scripts/geometer/g09_measures.py` and `g09_tq.py`.

- **G09-2 TR (I accept the merge, with TR as the primary reading).** TR = dominant 7th → root a fifth or a semitone down, per change, on the ii-collapsed path (`TR()`).
  - Why TR leads: adding a ii cannot move it at all, whereas DRES per bar shifts 0.105 SD. TR is also defined on recordings timed in seconds.
  - DRES per bar is the second reading.
  - Prediction: shrunk to **+0.035**, for the title-only matches and a writer agreement of 0.60. Killed if +0.035 lies outside the 95% range.
  - It counts only if fake-outcome power is at least 0.2 at .05/2. Otherwise it is an estimate. I will not inflate the prediction to buy power.
- **G09-1 TQ: estimate.** I agree it largely tracks dominant density. Recipe as in `TQ()`, holding IIV and V. Prediction +0.01.
- **G09-3 TE: estimate, low priority.** Prediction +0.02. Cross-writer agreement is only 0.28, so it reads the chart writer as much as the song.
- **Signature shape heritability:** stays withdrawn.

---

## Run 09, round 2: the Listener

No outcome opened.

- **R09-L1: its counted form merges into the frozen ii-V confirmation.**
  - IIV read from RB and BiaB charts only is an unseen estimate, predicted at +0.035 (+0.07 × 0.64 writer agreement × title-only shrinkage).
  - The GAP lead on seen titles holds log(number of iReal charts). I also report it without that control, because chart count may sit on the path from covers to chart.
- **R09-L2: I accept the merge with G09-2.**
  - TR is primary. It cannot move when a ii is inserted, and it is defined on charts timed in seconds.
  - DRES per bar is the second reading.
  - Prediction +0.035; killed if +0.035 lies outside the 95% range.
  - It counts only if fake-outcome power is at least 0.2 at .05/2; otherwise it is an estimate.
  - IIV holding DRES stays a seen-song lead.
- **R09-L3 CARC: estimate only, low priority.**
  - Computed on arrivals after dropping the first 2 and last 2 bars (intros and endings), with at least 2 arrivals left.
  - Prediction +0.02.
- **Halves:** I accept the hash of the writer string, or of the performer string when there is no writer.

---

## Run 09, round 2: the Inventor

No outcome opened. I accept the Skeptic's points: all three are estimates, none counted.

**R09-I1, IRR: revised.** The recipe is unchanged (recipe A, open walk). I predict +0.02. Hold ch_rep, V, ln_chg, partition and decade. Its 95% range should show whether the skeleton adds anything beyond A-B-A repetition.

**R09-I2, VR4: revised to VR4c.** VR4c is recipe B with the min7 of each ii-V dropped. On run 08 charts its stability is 0.867, its ρ with VR4 is 0.96, its ρ with IIV falls from 0.34 to 0.31, and its ρ with V is 0.61. So the chains are not only ii-Vs. I predict +0.02. Hold IIV, V, ch_rep, ln_chg, partition and decade.

**R09-I3, TYP: revised.** The reference is taken within coarse genre (biab, jazz, pop, wikifonia, other), and V is held. I predict −0.02. Low priority.

The Skeptic's halves rule applies to all three. At SE 0.029, none of them can be killed.

Script: `/home/claude/scripts/inventor/r09_vr4c.py`.
