# formula_search: let the data propose the formula, with a sealed half (run 13; three counted confirmations)

**Candidates (a grammar, no hand choice).** From the features13 song values (mean over a song's 4/4 clips, weighted by notes): every base feature f; every difference of two z-scored base features z(f_i) − z(f_j); every product z(f_i)·z(f_j) (z over all rows, notes only).

**Gates (notes only, on half-0 songs, before any outcome).** Clip stability (clip 1 vs clip 2 of songs with two 4/4 clips, Spearman) ≥ 0.20; |Spearman| < 0.70 with pitch-class entropy (run 11's REP), the data pack's ch_rep and ln_notes (so a "discovery" is not a known measure renamed); at least 2,000 half-0 songs with a value.

**Discovery (half 0 only: artists with md5(artist) mod 2 = 0).** Only half-0 rows are passed to the outcome loader. For each gated candidate: OLS of z(y_foreign) on z(candidate), artist fixed effects, run 04's controls and ln_notes, CR1 SEs. Rank by p. Select the top three that are mutually |Spearman| < 0.70. Write `selected.json` (recipe, discovery β and SE) and commit and push it before half 1's outcome is read.

**Confirmation (half 1, opened once).** Each selected formula: same model on half-1 rows. Prediction = half the discovery β, same sign (shrunk for the winner's curse). Pass: p < .0125, the discovery's sign, both quarter-halves of half 1 (md5(artist + "b") mod 2) the same sign, conditional logit the same sign. Killed: the prediction outside β ± 1.96 SE. Else unsettled. Power, printed before the join: SE ≈ 0.011·√(9,588/N₁); counted only if ≥ 0.2 at α .0125, else an estimate.

**What a pass would mean.** A formula no one wrote, found by search on one half and confirmed on the other. Seen songs: a lead for unseen melodies, not a finding.
