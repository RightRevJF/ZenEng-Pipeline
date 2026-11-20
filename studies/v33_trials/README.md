# Trials for Luthier v33 that were not adopted

**AIM_REPEATS again (749.109).** With 929 in, the figure borrow and rhythm borrow were set from the aimed song (`AIM_REPEATS = True`), songs rerun at 1000 12.

- `aimpool_with_aim_repeats.json`: every living build's medians against the aim. Song 58, bars on a figure already sung 0.307 (0.280 before; aim 0.698); bars on a rhythm already sung 0.439 (0.406; aim 0.774). Song 54, 0.398 (0.411; aim 0.525) and 0.571 (0.534; aim 0.775). The check is not met.
- `neighbour_with_aim_repeats.json`: a random pool pick fails the soundness rule 7.0 times in 100 (1.0 in v32); range and rhythm scaling lean low in all three picks.
- Why it tops out: song 58's figure borrow is already 1.0. A borrowed line is refitted to new words with a different syllable count, so its bars are seldom the same bars. That is the split-and-merge fitting 749.104 names.

**Register spread in the fit (749.108).** The spread was scaled each round toward the aimed range. From 62 to 400 in song 55 the builds span 15 to 17 semitones throughout: spread does not set range. Not adopted.
