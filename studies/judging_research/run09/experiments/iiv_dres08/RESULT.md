# iiv_dres08: does the ii chord or the dominant's resolution carry the ii-V effect? (LEAD on seen songs, not counted)

## The question
Run 08 found that tunes with a higher share of ii-V moves have more artists covering them (+0.073 within composer on seen songs, +0.057 on unseen ones). A ii-V has two parts: the ii chord and a dominant (V) that resolves down a fifth or semitone. DRES counts resolved dominants per bar. If the resolution does the work, holding DRES should shrink the ii-V effect; if the ii chord (a chart writer's signature) does, it should stay. Songs: run 08's 8,565 with all measures. Their outcomes were opened in run 08, so this is a lead only. Units are standard deviations of covers per standard deviation of the measure.

## Predictions, written first
- Both parts count: ii-V +0.035 and DRES +0.04 with both in the model.
- "The ii carries it": ii-V stays at +0.06 or more while DRES's range covers 0.
- "The resolution carries it": DRES positive with p under .05 and ii-V at half or less of its value without DRES.

## What came out
Across-composer main model (frozen):
- ii-V: +0.056 (95% range +0.035 to +0.077, p about 1e-7).
- DRES: -0.046 (range -0.068 to -0.024, p .00004).
- Neither prediction's value (+0.035, +0.040) falls inside its range. Frozen label: neither rule met. The ii rule fails because ii-V is 0.056, below 0.06, and DRES's range excludes 0; the resolution rule fails because DRES is negative.

Readings (decide nothing):
- ii-V alone, same songs: +0.055. Holding DRES barely moves it (0.055 to 0.056), so it is not halved.
- DRES alone: -0.044 (range -0.066 to -0.022).
- ii-V holding TR (the resolution share with ii chords collapsed): ii-V +0.060, TR -0.038 (p .0005).
- Within composer, run 08's model (5,858 songs, 1,199 composers with two or more songs): ii-V +0.073 (p .00004), DRES +0.034 (p .054).

## Plain reading
The ii-V coefficient is stable at about +0.055 to +0.073 whatever resolution measure is held, so the ii-V effect does not look like a resolution effect. That fits the ii chord (or something travelling with it) carrying it, though it misses the frozen "ii carries it" cut by 0.004, and the label says neither rule was met. DRES itself flips sign: negative across composers, mildly positive within composer. So across composers, tunes with many resolved dominants are covered less, perhaps because they come from different kinds of composer; within one composer's catalogue the sign reverses, though it is borderline. DRES's sign is not stable enough to be a claim. The ii-V and DRES correlate about 0.5, so they share information. The Poisson second model gives ii-V about +0.126 and DRES -0.010 (p .67), so the DRES result is weaker under that model. The halves agree for ii-V (+0.070, +0.041) but DRES differs (-0.023, -0.069).

Power was good here (0.81 and 0.88), which is why the lead was worth a slot, and also why it cannot count: these songs were already read.

## What it cannot say
- Seen songs only; a pattern is a lead for unseen ones.
- Jazz-heavy material.
- Chart writers may add resolutions as well as ii chords, so "the ii" is not separated from "the writer".
- No timing or recording-order information: charts are not shown to precede covers.

Source: result.json in this folder (labels: ii_carries false, resolution_carries false, "neither rule met").
