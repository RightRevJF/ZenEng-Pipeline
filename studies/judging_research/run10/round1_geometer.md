# Run 10, round 1: the Geometer

27 November 2026, the 18:17 ET pass. Notes only. I opened no outcome: I did not call `common10.load_outcomes`, and I did not open recordings.csv, tune_popularity.csv, data/*.json or any covers/versions/HOLDOUT file. All checks used split A, subsampled to 3,000 tunes (seed 10). Stability uses `common10.stability` on the first 3,000 split-A tunes that have a second setting. Code: `/home/claude/scripts/geometer/measures_geometer.py` (`measure(t) -> dict`, for the chair to freeze), with the checks in `checks_final.py`, `cand.py`, `cand2.py` and `fiedler.py` in the same folder. Total compute was about 4 minutes.

**Shared choice: the skeleton.** All three measures read the **beat skeleton**: the notes whose onset falls on a beat of the meter (beatpos an integer), taken in order. Card 2 found strong beats conserved across settings and variation piling up on weak beats. Using the skeleton changed stability little but cut renaming a lot. For the spectral gap, R² on the baselines fell from 0.56 (full surface) to 0.15; for tree reduction, from 0.19 to 0.07.

## G10-1: Weak links, the persistent entropy of the H0 barcode (card 1, M4)

1. **Mechanism.** H0 of the Vietoris-Rips filtration on a shortest-path metric is exactly the minimum spanning tree. Its finite bars are the lengths of the links that hold the tune's pitch vocabulary together, and their evenness says whether every pitch is bound to the tune by a habitual move or some hang by a rare thread.
2. **Measure.**
   - Nodes: the skeleton's distinct MIDI pitches. c(a,b) counts steps from a to b.
   - p_sym = (c + cᵀ)/total, with self-loops dropped.
   - Length = −ln p_sym, the transition's surprisal. I use this rather than card 1's 1/p because the card itself warns that 1/p is unbounded. 1/p is kept as the reading `pe_h0_inv`.
   - l_i = the MST edge lengths, which are the finite H0 bars; the infinite bar is dropped.
   - **pe_h0 = −Σ qᵢ ln qᵢ / ln(#bars)**, with qᵢ = lᵢ/Σl.
   - Nothing is fitted. It is invariant to transposition and to the overall count scale.
3. **Data.** TheSession split A (about 14,500 tunes), the first setting.
4. **Prediction.** **+0.03 SD of z(y_cov) per SD**, and positive for y_love.
   - What the mathematics says: a low-evenness tune has a few long bars, meaning pitches reached only by rare moves.
   - Card 2: rare pitches mutate most. So such a tune is the one that drifts or breaks when passed on.
   - *Extrapolation:* a uniformly knit skeleton travels intact between players, and intact travel is what lets a tune be learned and recorded.
5. **Kill.** +0.03 lies outside the 95% range (R07-3). The mechanism is also dead if the card's literal 1/p reading takes the opposite sign.

## G10-2: Retracing, the tree reduction of the skeleton walk (IRR revived on melody)

1. **Mechanism.** Free reduction deletes every back-track (x y x → x). A walk on a tree reduces to its geodesic, so what survives is the walk's word in the fundamental group of its own transition graph: how much the skeleton circulates round the graph's H1 loops instead of coming back the way it went. This is the same invariance as the path signature's uniqueness up to tree-like pieces.
2. **Measure.**
   - Take the skeleton and merge repeated pitches, giving length m.
   - Stack-reduce, giving length k.
   - **irr_skel = (k − 1)/(m − 1)**.
   - No parameters.
3. **Data.** As for G10-1.
4. **Prediction.** **−0.03 per SD** for y_cov, and negative for y_love.
   - Run 09 found the opposite of its prediction on chords: back-and-forth went with more covers (−0.060, a lead).
   - A melody whose way back is its way out (scale up then down, arpeggio up then down, neighbour notes) halves what must be remembered.
   - *Extrapolation:* that makes the tune easier to learn by ear.
5. **Kill.** −0.03 lies outside the 95% range. A positive estimate whose range excludes −0.03 would also show that run 09's chord lead does not transfer to melody.

## G10-3: Jason's S = 1 + g/π, a Cheeger bottleneck of the implied harmony

1. **Mechanism.** g = 1 − λ₂ of the random walk on the skeleton's pitch-class graph. Cheeger's inequality gives g/2 ≤ h ≤ √(2g), where h is the conductance of the best two-way cut.
   - The cut is mostly harmonic. On 1,000 major-mode tunes the Fiedler cut most often splits the tonic triad {1,3,5} from {2,4,6,7}, and the other common cuts are also chord regions.
   - So a small g means the skeleton dwells in one chord region before crossing: a slow, legible implied harmony.
2. **Measure.**
   - W = c + cᵀ on the skeleton's pitch classes, with self-loops kept.
   - λ₂ = the second-largest eigenvalue of D^−½ W D^−½.
   - **S_gap = 1 + (1 − λ₂)/π**.
   - No parameters.
3. **Data.** As for G10-1.
4. **Prediction.** **−0.03 per SD** of S for y_cov, and negative for y_love.
   - *Extrapolation:* a tune whose melody spells out a clear two-region harmony is easy for accompanists and learners to grasp.
   - Never powered before: run 07's chord version had power 0.01.
5. **Kill.** −0.03 lies outside the 95% range. If the sign is right but the effect vanishes once n_pc and pc_entropy are held (a reading), it was renaming.

## Measure-side checks (split A, 3,000 tunes)

| Measure | Stability (Spearman between two settings, n = 3,000) | Within reel / jig / polka / hornpipe | R² on the 13 baselines | R² on baselines plus type | Largest baseline ρ |
|---|---|---|---|---|---|
| pe_h0 (G10-1) | **0.679** | 0.66 / 0.66 / 0.69 / 0.71 | **0.141** | 0.145 | pc_entropy +0.25, n_pitch +0.20 |
| pe_h0_inv (card's 1/p reading) | 0.591 | 0.54 / 0.59 / 0.58 / 0.58 | 0.093 | 0.103 | ln_notes −0.13 |
| irr_skel (G10-2) | **0.762** | 0.72 / 0.81 / 0.78 / 0.75 | **0.071** | 0.091 | pc_entropy +0.17, n_pitch +0.14 |
| S_gap (G10-3) | **0.755** | 0.75 / 0.79 / 0.77 / 0.70 | **0.145** | 0.155 | pc_entropy −0.22, n_pc −0.19 |

The within-type columns used 600, 600, 466 and 444 tunes respectively.

**Overlap among the three measures (Spearman).**
- pe_h0 with irr_skel: 0.37.
- pe_h0 with S_gap: 0.01.
- irr_skel with S_gap: 0.05.

So the three are nearly separate. All pass the stability bar of 0.5 (R09-5) and stay well below renaming.

**Reserves I checked but did not propose:**
- **Rips H1 count on the skeleton (card 1, M2):** stability 0.62, R² 0.18. Its Spearman with the cycle rank is only 0.28, so here the topology is not just the count of cycles.
- **Circular transport on the fifths circle between the tune's first and second halves:** stability 0.67, R² 0.13.
- **Full-surface spectral gap:** stability 0.82, but R² 0.64 (range and n_pitch); it renames.
- **The 1/p metric (card 1's literal choice):** it is the least stable variant, as the card warned.
