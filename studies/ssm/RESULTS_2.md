# Held-out test of nesting: results (18 November 2026)

Predictions: PREDICTION_2.md (committed 9904b3e before measuring). Code: heldout_bimmuda.py (heldout_bimmuda.json). Melody alone throughout.
BiMMuDa: 290 Billboard year-end top-five songs in 4/4, 1950-2024, none also in CoCoPops (34 left out for that).

| Prediction | Result | Held? |
|---|---|---|
| N1 inside BiMMuDa, nest_fine rises with year-end position | rho -0.112 (one-sided p 0.97); nest_min -0.093 | no, slightly the other way |
| N2 BiMMuDa hits over CoCoPops songs that peaked below no. 20 | AUC 0.483 (p 0.68); nest_min 0.555 (p 0.17) | no |
| N3 the finer measure on the discovery sample, at least 0.18 | nest_fine 0.102 (p 0.14); nest_min 0.150 (p 0.028) | no: the count's 0.18 does not carry over |
| N4 Luthier below the BiMMuDa median | songs 54, 55, 58 at 0.60, 0.93, 0.25 against 1.17 (the 22nd, 36th and 11th percentiles of 504 human songs) | yes, mildly |

Reading: the lead from RESULTS.md does not hold on melodies it had not seen, nor with a finer measure on the songs it came from. "Repetition standing
out at every scale", read this way, does not mark the bigger hits. Luthier's songs have somewhat less of it than human songs, song 58 least.
Not tested: other readings of "the same order at every scale" (scaling of pitch and duration series, wavelets), and chills or moments as the outcome.
