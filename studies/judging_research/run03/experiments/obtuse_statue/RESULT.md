# The obtuse statue: result

Run 03, 23 November 2026. The rule is `PREDICTION.md` (frozen and pushed in commit 09ce7bd before this script was written). `test.py` ran it once. The numbers are in `result.json`.

## Verdict: **stopped**. The measure failed its gate, so no outcome was joined.

Before any cover data could be loaded, the measure had to pass a check. It failed, so the script stopped. It never opened the cover counts, the first years or the versions file.

- **What was checked:** whether p_min (how "obtuse" a song's chord graph is) belongs to the song or only to one clip. The script computed p_min on the song's first clip and on its second clip separately, removed size from both, and compared them.
- **The result:** the two clips agreed at **0.154**, over 1,166 pairs. The rule needed at least 0.20. The chair's notes-only check had found the same figure on the same number of pairs.
- **Before size was removed,** the clips agreed at 0.306. Most of what they share is simply how many chords they have.

## Other checks (before any outcome)
- **Unit tests:** all four came out exact (¼, 0, −½ and ¼).
- **Songs:** 2 of 2,672 were dropped, as the chair found, leaving 2,670.
- **Overlap (this part of the gate passed):**
  - With size removed, p_min's largest correlation with any listed measure was 0.075 (links). The limit was 0.7.
  - Size explains 65% of p_min. The limit was 80%.
- **Correlations printed, deciding nothing:** with distinct chords −0.83; with tonic resistance H +0.51; with the bridge flag −0.45.

## What this means
- **Too noisy to test:** with size removed, p_min varies too much from clip to clip to describe a whole song.
- **No estimate:** none exists for its link to covers, and none should be made from these songs.
- **Other tests unaffected:** each still needs p < .0083.
- **McGill:** the hold-out was not touched.

## Idea for later (not tried)
A weighted version, with move counts in place of plain links, might agree better from clip to clip. It would need its own frozen rule.

## Data credit
- **Notes and chords:** Hooktheory, via Sheet Sage (Donahue, Thickstun & Liang, 2022). CC BY-NC-SA 3.0.
- **Covers:** Discogs-VI 20240701 (Araz, Serra & Bogdanov, 2024). CC BY-SA 4.0. Not opened for this test.
