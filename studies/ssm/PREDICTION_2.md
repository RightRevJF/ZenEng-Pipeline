# Predictions for the held-out test of nesting, written before measuring (18 November 2026, 18:10)

The lead (RESULTS.md): in the CoCoPops Billboard sample, songs whose repetition stands out at more of the scales 2, 4, 8, 16 and 32 bars charted higher
(0.18 with peak, 0.17 with weeks). The finer measure, fixed now: `ssm_lib.nest_fine` = the mean, over 2, 4, 8 and 16 bars, of how far repetition at that
distance stands above repetition one bar nearer and one bar further, in the song's own spread (and its least value, "every scale").

Held-out melodies: BiMMuDa (Billboard year-end top five, 1950-2024; full-song melodies, melody only, no chords), songs in 4/4, read with melody alone.
Songs that are also in CoCoPops are left out of every held-out test.

N1. Inside BiMMuDa, nest_fine relates to year-end position (1 best): Spearman with minus the position over 0, one-sided p under 0.05.
N2. BiMMuDa's top-five hits show more nest_fine than the CoCoPops Billboard songs that peaked below no. 20 (AUC over 0.55). Caution: two encodings.
N3. On the discovery sample, nest_fine (melody alone) relates to Billboard peak at least as strongly as the count did (0.18).
N4. Luthier's songs 54, 55, 58 sit below the BiMMuDa median on nest_fine.
What I expect: N3 holds (it is the same sample); N1 is too small to see in a top-five range and fails; N2 is the real test and could go either way.
