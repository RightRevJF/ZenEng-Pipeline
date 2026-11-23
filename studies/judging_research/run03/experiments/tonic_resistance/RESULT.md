# Is home the electrical hub? Result

Run 03, 23 November 2026. The rule is `PREDICTION.md` (frozen and pushed in commit 09ce7bd before this script was written). `test.py` ran it once, as written. The numbers are in `result.json`.

## What was predicted
Treat a song's chords as an electrical circuit, with one wire per move and thicker wires for frequent moves. **H** compares how easily current flows from every chord back to the home chord with how easily it flows to an average chord. H below 1 means home is the hub, with many routes back.

The guess: an arranger can wander far from a central home without getting lost. So among one artist's own songs, a lower H means more covers. The predicted size was **−0.03 SD of log covers per SD of H**. Six tests ran tonight, so a pass needed p < .0083.

## Gate (run before any outcome was loaded): passed
- **Unit tests:** all three came out exact (1, 0.6 and 1.4).
- **Songs dropped:** 80 of 2,672, matching the chair. In 72 there was no chord on the home root; in 8, home's piece of the graph had fewer than 3 chords.
- **Clip-to-clip agreement, size removed:** 0.247 over 1,057 pairs. The rule needed at least 0.20.
- **Overlap:** the largest correlation was 0.083, with `length_variety`. The limit was 0.7. Size explains 10% of H; the limit was 80%.

## What came out
The model used 1,853 songs by 410 artists.

| | Songs | Estimate | SE | p |
|---|---|---|---|---|
| **All (decides)** | 1,853 | **−0.019** | 0.014 | 0.19 |
| Half 0 of artists | 900 | −0.010 | 0.022 | 0.66 |
| Half 1 of artists | 953 | −0.027 | 0.019 | 0.16 |

The 95% range runs from −0.046 to +0.009. The script printed the power before the estimate: **0.31**.

## Verdict: **unsettled**
- **Direction:** the estimate and both halves lean the predicted way.
- **Not a pass:** p is 0.19, far from the 0.0083 needed.
- **Not a kill:** the rule kills only above −0.01.
- **Bottom line:** no evidence for the effect, and none against it.

## Reported, deciding nothing
| Reading | Estimate | p |
|---|---|---|
| Covers within 5 years | −0.022 | 0.35 |
| Covers after 10 years | −0.010 | 0.46 |
| Chord surprise left out of the model | −0.026 | 0.07 |
| 74 songs dropped (home's piece is not the whole graph) | −0.023 | 0.11 |

- All four lean the same way, and none is significant.
- In the same model, chord repetition gave −0.061 (p 0.0003) and chord surprise −0.089 (p 0.0002).
- H overlaps with the obtuse-statue measure: ρ = +0.51.

## What it cannot say
- **Low power.** A null clears nothing. The clips agree only about 0.25, so a true −0.03 would show up nearer −0.015, close to what came out.
- **Frozen after other outcomes were known.** A pass would only have been a lead for unused songs.
- **No cause.** These are all hits, and era and singles still differ within an artist.
- **A simple graph.** It sees one step at a time and ignores direction. Home is taken from the clip's first key.
- **McGill.** The hold-out was not touched.

## Idea for later (not tried)
H could be confirmed on songs not used here. That would need its own frozen rule and enough songs for real power.

## Data credit
- **Notes and chords:** Hooktheory, via Sheet Sage (Donahue, Thickstun & Liang, 2022). CC BY-NC-SA 3.0.
- **Covers:** Discogs-VI 20240701 (Araz, Serra & Bogdanov, 2024). CC BY-SA 4.0.
