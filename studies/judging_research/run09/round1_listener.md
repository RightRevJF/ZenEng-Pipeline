# Run 09, round 1: the Listener

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
