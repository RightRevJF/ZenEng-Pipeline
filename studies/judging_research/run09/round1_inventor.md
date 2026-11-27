# Run 09, round 1: the Inventor

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
