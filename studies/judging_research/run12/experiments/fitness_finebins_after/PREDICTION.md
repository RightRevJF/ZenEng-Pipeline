# fitness_finebins_after (run 12, after seeing results; reads cover timing only, no notes)

Written 28 Nov 2026 ~12:15 ET, from first_principles.md section 5. Question: was "no rich-get-richer" (A -> infinity) an artefact of
seven coarse age bins (a rich-get-richer climb could hide inside a wide bin)? Refit fitness.py's model with one age bin per year for
ages 0-10, then 11-15, 16-31, 32+ (14 bins), everything else as frozen; profile A at 0.3, 1, 3, 10, 30, 100 and free.
**Prediction:** the likelihood still rises monotonically with A (free A > 1,000). **Killed** if any finite A of the profile beats
A = 100 by more than 2 log-likelihood units. No notes measure is read; nothing is counted in K (no notes test).
