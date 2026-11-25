# Card 1: Park, An, Kim & Kim, "Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings"

This card replaces Perea & Harer (arXiv 1307.6188), which could not be read in full tonight.

## 1. Citation and copy read
Donghyun Park, Junhyun An, Taehyoung Kim and Jisu Kim (Department of Statistics, Seoul National University), "Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings." arXiv:2512.06324, math.ST / stat.TH. First submitted 6 Dec 2025; current version v4, dated 25 Sep 2026 (from the abs page). The HTML author block lists the two Kims in the opposite order from the abs page. An earlier version (v2) carried a different title, "Subsampling Confidence Bound for Persistent Diagram via Time-delay Embedding."

Copy read: https://arxiv.org/html/2512.06324v4. The page itself shows no version string. I covered every section (1 to 8), all appendices (A to I), the figure captions and the full bibliography (23 entries). Caveats:
- The fetch tool hands back a close paraphrase made by a helper model, not the raw page. I read the paper in six passes (Sections 1 to 3, 4 to 5, 6 to 8, Appendices A to E, Appendices F to I plus references, and the abs page). Formulas came back consistent across passes, but treat exact constants as "check against the PDF before quoting".
- The source's Table 1 is garbled in the HTML. One robust-test entry (0.437 false rejections for the linear trend h1) contradicts the prose, which says the robust test also has zero false rejections.

Why not the first choices: Gakhar & Perea (arXiv 2103.04540) was tried at https://arxiv.org/html/2103.04540, then /html/2103.04540v2 and /html/2103.04540v3. All three requests were blocked by the permission system before going out (not answered in time). I did not try v4. The abs page did load: it shows v3 (2 Aug 2023) as current and lists no HTML full text, so even unblocked it would probably have been PDF-only. I did not use it for anything below except the lead in Section 7.

## 2. Construction and results
**The embedding.** For a function f and an integer m and delay τ, SW_{m,τ}f(t) = (f(t), f(t+τ), ..., f(t+mτ)), a point in R^{m+1}. Running t over the observed times gives a point cloud. The window length is mτ. Unlike Perea & Harer's SW1PerS, the paper uses **raw** windows: no per-window centring or normalising. (On real data each analysis segment is linearly detrended and standardised first.)

**Signal classes (Section 3).**
- f is Ξ-periodic if f(t+Ξ) = f(t) for all t.
- f is non-periodic on an interval if the phase map t ↦ (f(t), f′(t)) never revisits a point.
- Quantitative versions: (Ξ, d, ε)-periodic means periodic, and any two times at least d apart on the circle of length Ξ differ by at least ε in value or in slope. (d, ε)-non-periodic is the same without the wrap-around.
- These classes deliberately exclude near-constant signals and signals with partial recurrence (a pattern that comes back sometimes but not always). They are disjoint but do not cover everything.

**Regularity (Appendix A).** f is C² with Lipschitz f″; at every time |f′| ≥ δ or |f″| ≥ δ (never flat in both); |f′|, |f″| ≤ L. Derived constant ν = (δ/16)·min(1, δ/(8L)). The separation scale d must be smaller than d_{δ,L} = πν²/(2L²). Times are sampled i.i.d. from a density bounded above and below. In the periodic case the observation span must cover at least one full period Ξ.

**Theorem 4.1 (non-periodic case).** If f is (d, ε)-non-periodic and the window satisfies mτ > max(δ/(2L), ε/(4L)) and τ < min(δ/(8L), ε/(16L)), then the sliding-window curve is an embedded interval with reach at least
a_{m,τ} = √(m+1) · min{ (ε/32)·min(1, ε/(16L)), ν²/(2L) }.
**Corollary 4.2:** the H1 persistence diagram has no point born before a_{m,τ}. No loops at small scale.

**Theorem 4.3 (periodic case).** Same window conditions, f (Ξ, d, ε)-periodic: the curve is an embedded circle with the same reach bound. **Corollary 4.4:** the only H1 point born before a_{m,τ} is (0, D) with D ≥ a_{m,τ}. So one loop, born at zero, with persistence at least a_{m,τ}. This is the paper's lower bound on persistence. It grows like √(m+1) and with the separation ε.

The proofs (Appendix E) bound the speed of the curve from below, its curvature from above, and the distance between windows that are far apart in time, then use a reach criterion for curves. Two geometric lemmas are cited rather than proved. Notably, **the window mτ does not have to cover a full period**; only the observation span does.

**Confidence bound (Section 5, Algorithm 1).** Draw B random subsamples of size b from the cloud, compute each one's Hausdorff distance to the full cloud, take the (1−α) quantile, and double it: c_α. **Theorem 5.1:** with b → ∞ and b = o(n/log n), the bottleneck distance between the sample diagram and the true diagram exceeds c_α with probability at most α + O((b/n)^{1/4}). Lemma 5.2: c_α → 0. With noisy, linearly interpolated data, the radius is inflated by 5ζ, where ζ = √(m+1)·(noise bound + grid spacing²·L_int/8) (Theorem 5.3). This extends Fasy et al. (2014) from closed manifolds to curves with endpoints (Proposition D.2, argued by adjusting constants).

**The test (Section 6).** Reject "non-periodic" if the diagram has an H1 point with birth ≤ c_α and persistence > 2c_α. **Theorem 6.2:** both error rates are at most α + O((b/n)^{1/4}) plus the chance that a_{m,τ} ≤ 4c_α. Corollary 6.3: asymptotic level α and power. Corollary 6.4: over a grid of K (m, τ) pairs, run each at α/K (Bonferroni) and declare periodic if any rejects.

**Persistence pictures.**
- Periodic: one long H1 bar born at 0 (a circle). Non-periodic: no early H1 bar (an interval).
- **Quasiperiodic: not covered.** The paper has no torus result, no H2 and no second H1 bar. Section 8 lists quasi-periodic and almost-periodic signals as open directions. The "two long H1 bars plus one H2 bar" picture belongs to Gakhar & Perea, which I could not read, so I state nothing about it from tonight's reading.

**Parameter rules actually used.** Delay τ = (period)/(m+1), so the window just under one period. m = 20 on synthetic data, m = 8 on real data. Candidate periods from autocorrelation and Welch peaks, each tried at 0.9×, 1× and 1.1×, with Bonferroni over the candidates. Subsample b = 0.99n with 300 subsamples on real data, which the authors call a practical calibration and not the regime of the theorem. Clouds capped at 300 anchor points.

## 3. Is the measure from the notes?
Yes, once a signal is chosen. The test takes any sampled series. The theory is for a scalar f, so a 12-dim chord vector is an extension. My guess is the arguments carry over to vector signals, but the paper does not say so. The theory also assumes a smooth signal with no flat stretches. Note grids are step functions with held notes, so they break Assumption A.1; Gaussian smoothing and linear interpolation (which the paper itself uses) soften this but do not remove it. No audio, listener or popularity data enters.

## 4. Effect size and how checked
- **Proved:** topology (circle vs interval) and the reach lower bound, under the smoothness and separation assumptions; the subsampling confidence bound; the test's asymptotic error control. The constants (δ, L, ε, d) are never computed for a real signal, so on data the guarantee is qualitative.
- **Synthetic (Table 1):** two periodic signals of period 2π/5 and four trend-like non-periodic ones; N = 400 points, m = 20, n = 336 anchors, α = 0.05, 100 seeds, seven noise settings. Raw TopPT: detection 1.000 on both periodic signals, false rejection 0.000 on all four non-periodic ones. Robust TopPT: detection 0.699 and 0.457. Lomb–Scargle, Fisher's g and a permutation test rejected all six, including all the non-periodic trends.
- **Stress tests (Table 3):** phase drift sin(5t + 0.18t²) rejected 0.791 (raw) / 0.137 (robust); amplitude modulation 1.000 / 0.714. So a cycle that slowly bends or swells is still read as a loop by the raw test.
- **Real data (Table 2):** respiration. Fantasia: 35/40 records, 142/280 windows. BIDMC: 51/53 records, 249/318 windows. Baselines rejected everything. There are no null labels, so these are detection counts only.
- **Music or audio application:** none.

## 5. What it says about lasting love and covers
Nothing. **Extrapolation (mine):** the paper's main contrast is "closed loop vs open path". In a song, that is "the music returns to where it was" vs "it keeps going somewhere new". The project's existing finding (more exact 3-gram repetition, fewer covers) suggests looping alone will not be the useful part. The paper's birth condition, though, separates loops that retrace themselves exactly from loops that come back each time a little different (its phase-drift case). Whether varied return predicts covers is a hypothesis, not something this paper supports.

## 6. Methods or measures it suggests for tonight's experiments
All numbers below are my own toy runs (Python, ripser, numpy, scipy; scripts in /tmp/reader_scratch, not in the repo), not the paper's.

**Shared core ("TopPT score"), about 25 lines.**
1. Grid: h = 1/2 beat. Build a series X of shape (T, d).
2. Smooth: `gaussian_filter1d(X, sigma=2, axis=0, mode='nearest')` (σ = 1 beat). This stands in for the paper's smoothness assumption.
3. Embed: m = 8 (the paper's real-data value), τ = P/(m+1) samples for a candidate period P. Anchors every 1/4 beat (0.5 samples) from 0 to T−1−mτ; read X at t + kτ, k = 0..m, by linear interpolation (`np.interp` per channel); concatenate into one vector per anchor.
4. **Deduplicate** (`np.unique` on rounded points). Exact loops produce identical windows, and duplicates make every subsample look perfect (c_α = 0), which wrecks the birth condition. This is the fix for exact repeats.
5. Radius: B = 200 subsamples of size b = ceil(0.99n) (capped at n−1); h_j = max over all points of the distance to the nearest subsample point; c = 2·quantile(h, 0.95).
6. `ripser(D, distance_matrix=True, maxdim=1, coeff=11)`. Ripser reports Rips diameters; divide by 2 to put them on the paper's radius scale before comparing with c.
7. Normalise by s = √(m+1)·RMS distance of X from its mean, so scores are comparable across songs. Outputs: p1 and p2 (longest and second-longest H1 persistence)/s, b1 (birth of the longest bar)/s, c/s, reject flag (some bar with birth ≤ c and persistence > 2c), and **margin** = max(persistence − 2c)/s over bars born by c (0 if none). The margin is the paper's Figure 4 diagnostic.
8. Periods: P ∈ {2, 4, 8} bars for chords, {1, 2, 4} for melody, using bar length from the meter. Only use P ≤ T/2 (clip must hold window plus one full period, Assumption 3.4); otherwise NA. Report the max margin over P and the argmax P*. If you want a yes/no, use α/K per P (Corollary 6.4).
9. Cost: about 0.15 s per (clip, P) at 1/4-beat anchors on 16 bars. Halving the anchor step to 1/8 beat costs about 8× more and roughly halves c, so pick one step and keep it fixed across the corpus; scores at different steps are not comparable.

**(a) Melody periodicity.** Signal: pitch in semitones (scale degree → major or minor scale semitone, plus 12 × octave), held through rests, linearly detrended over the clip and divided by its SD (the paper's preprocessing). Toy results (16 bars, margin at P = 1 / 2 / 4 bars):
- 2-bar motif ×8: 0.39 / 0.51 / 0 (at 4 bars the birth condition fails narrowly: b1 0.10 vs c 0.07).
- Same motif, one note varied per repeat: 0.27 / 0.18 / 0.
- 4-bar phrase ×4: 0 / 0.50 / 0.51.
- Random-walk melody: 0 / 0 / 0.31. **Warning:** across 40 random walks the reject rate was 0 / 0.30 / 0.10 at P = 1 / 2 / 4. Pitch-only melodies revisit states, which breaks the paper's non-periodic assumption, so the test leaks on melody. Calibrate against a per-song surrogate (shuffle the notes, keep the rhythm, 20 draws) and report margin minus surrogate mean.

**(b) Chord periodicity.** Signal: 12-dim 0/1 pitch-class vector of the sounding chord per half beat (root + type; ignore inversion). Toy results, 16 bars, one chord per bar, b = 0.99n, anchors every 1/8 beat:

| Progression | 3-gram share | margin at P = 2 / 4 / 8 bars | p2 at 4 bars | b1 at 4 bars |
|---|---|---|---|---|
| A: I–V–vi–IV looped ×4 | 0.71 | 0.51 / **0.53** / 0.53 | 0.01 | 0.04 |
| B: that loop 8 bars, then ii–V–I–vi 8 bars | 0.29 | 0.38 / **0.44** / 0 | **0.48** | 0.07 |
| C: 8-bar progression played twice | 0.43 | 0.52 / 0.53 / 0.55 | 0.03 | 0.03 |
| D: the loop with 3 substitutions | 0.21 | 0.42 / **0** / 0 | 0.17 | **0.28** |
| E: 16 random diatonic chords | 0.00 | 0 / 0 / 0 | 0.05 | 0.49 |
| F: I–IV ×8 | 0.86 | 0.42 / 0.43 / 0.42 | 0.00 | 0.05 |

With anchors every 1/4 beat (the cheaper setting) at P = 4: A 0.24, B 0.21, D 0; 40 random 16-chord progressions rejected 3% of the time (7% at 1/8 beat), mostly where chance produced a repeated stretch.

**Worked example (the one asked for).** The four-chord loop (A) and the progression that changes at bar 8 (B) both score high at a 4-bar period (0.53 vs 0.44). They part ways in two places: B collapses at the 8-bar period (0 vs 0.53), because its first and second halves do not trace the same cycle, and B has a second long H1 bar (0.48 vs 0.01), one loop per section. The 3-gram share sees only that B repeats less (0.29 vs 0.71).

**(c) Second-cycle / quasiperiodicity score (extrapolation; the paper gives no theory for this).**
- Joint signal: [melody series as in (a), chord chroma / √3] stacked per half beat. Run the core with maxdim = 2 at P = the chord period. Report p2 (second H1 bar) and the longest H2 bar, both / s.
- Toy: a 3-bar melody over a 4-bar loop (24 bars): p2 0.08 to 0.16, H2 0.03 to 0.06. A 5-bar melody over the same loop (40 bars): p2 0.14 to 0.15, H2 0.07. The same melody locked to the 4-bar loop: p2 0.01, H2 0.002. So the two-cycle case is an order of magnitude above the locked case, but every value stayed below 2c, so nothing is certified. Cost rises fast (9 to 70 s per clip with maxdim 2), so run it on a subsample or only on songs where the melody's P* and the chord P* differ.
- Caution: in symbolic music both periods are whole numbers of bars, so the joint signal is exactly periodic at their lcm. The trajectory is a closed curve winding on a torus, not a dense torus. Also, two sections with different loops (case B) give two H1 bars without any torus: that is two circles joined, not a product. Lead 5 is about telling these apart.
- Cheaper proxy that follows the paper's own tools: compute P*_mel and P*_chord from (a) and (b); "cycle mismatch" = P*_mel ≠ P*_chord (or their ratio), and check whether the joint signal still rejects at lcm(P*_mel, P*_chord).

**Overlap with "share of chord 3-grams heard earlier".**
- Both reward loops. On clean loops they will correlate, and a looped four-chord pattern maxes out both. An exact loop's TopPT score is set by the loop's shape once one full return happens; more repeats do not raise it, while the 3-gram share keeps rising (A 0.71 vs F 0.86, margins 0.53 vs 0.43).
- TopPT is graded and time-aware: it uses durations and the period scale, and it tolerates a few exact mismatches at short periods (D still scores 0.42 at 2 bars with 3-gram share 0.21).
- It reads a single 8-bar progression played twice as fully periodic (C: 0.53), while the 3-gram share gives it 0.43.

**One measure that is not repetition renamed: loop thickness.** T = b1/p1 for the longest H1 bar at the chord period P* (or simply b1/s). It measures how far each pass around the cycle departs from the last, given that there is a cycle: near 0 when the loop retraces itself exactly, large when it comes back varied. Toy: A 0.05, B 0.10, C 0.04, D 0.61, E 2.6 (no real loop). B and D have almost the same 3-gram share (0.29 vs 0.21) but very different thickness, because B repeats exactly and then changes section, while D keeps one cycle and varies it. Pair it with **section count** = number of H1 bars with persistence > 2c (A: 1, B: 2), which counts distinct cycles rather than repeats. Partial out the 3-gram share before reading either against the yardstick, and report thickness only where p1 is clearly above the random-progression range (p1/s > 0.55 at P = 4 was the 95th percentile for random chords).

**For tonight I would run:** (b) chord margin at P ∈ {2, 4, 8} bars with P*, thickness and section count; and (a) melody margin at P ∈ {1, 2, 4} bars minus its shuffle-surrogate mean. Treat (c) as exploratory.

## 7. Leads
1. **Gakhar, H. & Perea, J. A.** "Sliding Window Persistence of Quasiperiodic Functions." arXiv:2103.04540 (v3, 2023); J. Appl. Comput. Topology. https://arxiv.org/abs/2103.04540. The torus theory and window rules that recipe (c) needs; abstract mentions a music-audio dissonance application. Needs a readable PDF route.
2. **Suarez Salas, L. et al.** "Estimation of Persistence Diagrams Via the Three Gap Theorem." arXiv:2603.04570. https://arxiv.org/html/2603.04570. Quasiperiodic sliding windows with an HTML full text, so readable next run.
3. **Fasy, B. T., Lecci, F., Rinaldo, A., Wasserman, L., Balakrishnan, S. & Singh, A.** (2014). "Confidence sets for persistence diagrams." Annals of Statistics 42(6). The subsampling radius TopPT is built on; worth checking for finite-sample advice on b.
4. **Perea, J. A. & Harer, J.** (2015). "Sliding windows and persistence." Foundations of Computational Mathematics 15(3):799–838. arXiv:1307.6188. Still unread; its window-equals-period and normalisation results complement TopPT's raw-window test.
5. **"Doughnut or Mickey Mouse? Detecting Toroidal Structure in Data through Persistent Cup-Length."** arXiv:2507.11151. https://arxiv.org/html/2507.11151. Separates a true torus from two circles joined at a point, which is exactly the B-vs-quasiperiodic confusion in recipe (c).
