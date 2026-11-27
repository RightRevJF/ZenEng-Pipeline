# Card 2: Perea and Harer, "Sliding Windows and Persistence" (2015)

## 1. Citation and copy read
Jose A. Perea and John Harer, "Sliding Windows and Persistence: An Application of Topological Methods to Signal Analysis", *Foundations of Computational Mathematics* 15 (2015); arXiv:1307.6188. Copy read: arXiv HTML (https://arxiv.org/html/1307.6188), v2 of 25 Nov 2013 (v1 23 Jul 2013); not the journal version. Four WebFetch passes over the HTML (whole paper; experiments and discussion; score definition and Thm 6.8 hypotheses; r̃_n and bibliography), plus one of the abs page for versions. WebFetch returns a paraphrase, so the theorems below are right in substance, not copied symbol by symbol.

## 2. Main construction and theorems
- **Sliding window.** For a function f on the circle, SW_{M,τ}f(t) = (f(t), f(t+τ), …, f(t+Mτ)) in R^{M+1}. The window length is Mτ. For periodic f the windows trace a closed curve. Periodicity shows up as roundness, measured by the longest-lived H1 hole in the Rips filtration.
- **Window vs period.** For cos(Lt) the curve is an ellipse. It is roundest exactly when L(M+1)τ is a multiple of π. The choice τ = 2π/(L(M+1)) makes Mτ = (M/(M+1)) × period, just under one period. Section 1.2 says maximum persistence occurs "when the window size corresponds to the natural frequency of the signal". This is proved only for cosines; for general f it is a stated conjecture.
- **Embedding dimension (Prop 5.1).** With Mτ < 2π, the window vectors of the first N harmonics are linearly independent if and only if M ≥ 2N. This is a Nyquist/Takens-style rule, and the standing choice is M = 2N.
- **Fourier truncation (Prop 4.2, Thm 4.5).** SW is a bounded linear map with norm at most √(M+1). For f in C^k, the window cloud of f and that of its N-term Fourier truncation S_N f differ in Hausdorff distance by O(√(M+1)/(N+1)^{k−1/2}). By diagram stability, the bottleneck distance and the change in max persistence obey the same bound. The paper also covers Sobolev and Hölder variants.
- **Structure (Thm 5.6).** If f is L-periodic and τ = 2π/(L(M+1)), the centred and normalised curve lies on a torus, with mutually orthogonal harmonic planes. Its radii are r̃_n = 2|f̂(n)| / ‖S_N f − f̂(0)‖₂ for n a multiple of L, and the squared radii sum to 1.
- **Convergence (Thms 6.6, 6.7).** As N grows, the diagrams of the centred, normalised clouds form a Cauchy sequence in bottleneck distance. A limit diagram therefore exists, and it depends continuously on the sampling set.
- **Lower bound (Thm 6.8).** The hypotheses are: f is C¹ and L-periodic, M ≥ 2N, L(M+1)τ = 2π, the sample times are δ-dense, δ is small relative to √3·max r̃_n/κ_N, and the coefficients are F_p with p > N prime. Then max persistence ≥ √3·max_n r̃_n − δκ_N. Here κ_N is a ratio of the derivative's norm to the signal's norm, so jagged signals need denser sampling. - **Coefficients (Sec 6.3).** For cos t + cos 2t the cloud bounds a Möbius strip, so H1 over F_2 differs from F_3; hence a prime field such as F_11.
- **Score.** Spline-interpolate, centre each window (subtract its own coordinate mean), divide by its norm; Score = mp(H1 Rips diagram)/√3, higher = more periodic. The √3 is the Rips death of a sampled circle. No proof that the score lies in [0,1]; examples ran about 0.4 to 0.95.

## 3. Is the measure from the notes?
Yes, entirely: a functional of the signal alone. A song must become a time series; for us, bar-indexed 12-dim chroma, so a window of W bars is a point in R^{12W}. The paper is scalar-only; the multichannel extension is ours, though SW stays linear and stability carries over.

## 4. Proved vs assumed; empirical checks
- **Proved:** the approximation, dimension, structure, convergence and lower-bound results above, all for one smooth periodic scalar signal with a known period L.
- **Assumed or conjectured:** that the period-matched window maximises persistence (conjecture); a known L; smoothness. Quasiperiodicity and multiple incommensurate periods are mentioned in the introduction but not developed. H2 is never used.
- **Empirical:** synthetic only, no real gene data. Shape test: 10 shapes at 50 points, best of L ∈ {2,3,4}; unlike JTK_CYCLE, Lomb–Scargle and total persistence, no shape bias. Classification: 600 profiles (4 periodic, 2 aperiodic shapes × 100 phases) at 0/25/50% noise, ROC/AUC; comparable to Lomb–Scargle, better on peaked and damped shapes at high noise. N = 10, F_11. Preprocessing (spline, 7-point moving average, one mean-shift step) mattered a lot. No confidence intervals.

## 5. Lasting love and covers
Nothing. The paper never mentions music, listeners or popularity. All it offers is a shape-independent number for how cyclically a signal returns to itself.

## 6. Methods and measures for this pass
**Recommended recipe (no fitted settings):**
1. Bar chroma from the pitched tracks (no drums): duration × velocity per pitch class, L1-normalised; silent bars zero.
2. Windows of W bars, step 1 bar, flattened to R^{12W}. The paper's rule is window ≈ one period; the usual 4/4 pop phrase is 8 bars, so **W = 8** is primary. As in Sec 7.1 (best of a fixed set of periods), also report max over W ∈ {4, 8, 16}. Both are fixed in advance. No spline step, since bars are discrete.
3. Centre each window by subtracting each pitch class's mean over the W bars (our f̂(0) removal, so key/drone drops out), then L2-normalise. Drop windows with norm < 1e-6.
4. `ripser(X, maxdim=1, coeff=11)`, Euclidean. Score = max H1 (death − birth)/√3.
5. Cost: about 90 points per 100-bar song, milliseconds each; the whole corpus in under 30 minutes on one core.

**Not just "how repetitive":** report partial correlations with the chord-repetition measure and with the number of distinct windows; keep the residual. **Shuffled-bar null:** permute bars 50 times and report z = (score − null mean)/null sd. This keeps the bar vocabulary but destroys cyclic order. A **4-bar block shuffle** separates phrase cycles from bar loops.

**Pitfalls:**
- Length: score fixed 64-bar segments and take the median.
- Identical bars: a strict 8-bar loop is just 8 points, a polygon that scores high from repetition alone; constant music centres to zero. Deduplicate and log the unique-window count.
- Verse vs chorus: two loops, but mp sees one. Also log the second H1 bar.
- Quasiperiodicity (a 4-bar loop inside a 16-bar form) gives a torus: two H1 bars plus H2. This is unproved; try maxdim = 2 on a subsample.
- Use F_11, not F_2 (the Möbius effect).

## 7. Leads
1. J. A. Perea, A. Deckard, S. B. Haase, J. Harer, "SW1PerS: Sliding Windows and 1-Persistence Scoring; Discovering Periodicity in Gene Expression Time Series Data", BMC Bioinformatics 2015 (cited as a 2013 preprint).
2. V. de Silva, D. Morozov, M. Vejdemo-Johansson, "Persistent Cohomology and Circular Coordinates", Discrete Comput. Geom. 45(4), 2011. Gives a phase per bar, i.e. where in the cycle each bar sits.
3. D. Cohen-Steiner, H. Edelsbrunner, J. Harer, "Stability of Persistence Diagrams", Discrete Comput. Geom. 37(1), 2007.
4. V. de Silva, P. Skraba, M. Vejdemo-Johansson, "Topological Analysis of Recurrent Systems", NIPS 2012 workshop on algebraic topology and machine learning.
5. F. Takens, "Detecting Strange Attractors in Turbulence", Lecture Notes in Math. 898, Springer, 1981.
