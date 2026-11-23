# Curvature of the chord walk against covers: result

Run 03, 23 November 2026. The rule is `PREDICTION.md` in this folder, committed and pushed (ad201ad) before this script was written. The script is `test.py` and the numbers are in `result.json`.

## What was predicted
Each song's chords make a small map of which chord moves to which. Where two neighbouring chords lead on to the same next chords, they can stand in for each other. Ollivier curvature scores this overlap link by link, and **kbar** averages it over the song's moves. The prediction was that a song with more of these stand-in chords is covered a little more than the artist's other songs: **+0.02 SD of log covers per SD of kbar**. The model holds size, chord repetition, chord surprise and first year. It needed p < .025, because two tests were run tonight.

## What came out
1,924 songs by 420 artists, each artist with two or more songs.

| | Estimate | SE | p |
|---|---|---|---|
| **kbar (the test)** | **−0.0002** | 0.029 | 0.995 |
| kbar without chord surprise (β₀) | +0.020 | 0.028 | 0.48 |
| Artist half 0 (932 songs) | +0.001 | | 0.98 |
| Artist half 1 (992 songs) | −0.001 | | 0.97 |
| Chord repetition, same model | −0.061 | 0.017 | 0.0003 |
| Chord surprise, same model | −0.089 | 0.023 | 0.0001 |

**Verdict by the rule: kill.** The rule says β ≤ 0 kills, and the estimate is −0.0002. The second kill condition also holds: β₀ is above zero and β is below half of β₀. Most of the little that kbar shows without chord surprise in the model is chord surprise under another name.

## How firm
- **Precision:** the 95% range is −0.058 to +0.057.
- **Power:** the script printed it before the estimate. It was **0.06**, against the chair's guess of 0.10. The SE came out at 0.029, not the expected 0.020. After the size dummies and the artist are held, there is less left of kbar to work with than the chair thought.
- **What that means:** a kill at this power is weak evidence. But the estimate is almost exactly zero and both halves agree, so nothing hints at a hidden effect.

## Audit (run before any outcome was loaded)
- **Unit tests:** all four of card 1's values were reproduced: 3-cycle 0.5, 4-cycle 0, hub 0.25, K4 0.667.
- **Prop. 29 held on every song:** 0 violations. In every connected piece, the lazy spectral gap was at least the smallest link curvature.
- **Cross-checks:** the curvature values match a second exact solver (POT) to 9×10⁻¹⁶. B matched networkx's bridges, and Foster's theorem held, on all 2,672 songs.
- **Shape (2,672 songs), all matching the chair:**
  - kbar 10th / 50th / 90th percentile: 0.00 / 0.20 / 0.50;
  - share with kmin > 0: 22.1%;
  - R² on the size block: 0.456;
  - disconnected songs: 110.
- **Correlations of residual kbar:**

  | Measure | Spearman ρ |
  |---|---|
  | Lazy g | +0.35 |
  | Chord uncertainty | −0.24 |
  | B | +0.22 |
  | Chord surprise | −0.17 |
  | Chord repetition | +0.02 |

  Every other |ρ| was 0.16 or less. All match the chair.
- **The g gate:** ρ with chord count 0.25 (chair 0.26); clip 1 against clip 2 0.17 (chair 0.17, 1,267 pairs); 37% of songs have g < 0.01 (chair 37%).
- **Stop rule:** not triggered. The largest R² was 0.46 and the largest |ρ| was 0.35.

## Reported, deciding nothing
- **Covers within 5 years:** +0.008 (p 0.84). **More than 10 years after:** −0.012 (p 0.64).
- **Disconnected songs dropped:** +0.002 (p 0.95, 1,843 songs).
- **Unweighted mean link curvature:** ρ 0.91 with kbar, as the chair found. In the model in place of kbar it gives +0.013 (p 0.63).
- **Shuffle-relative kbar (40 shuffles):**
  - ρ with chord repetition: −0.52 (Geometer: −0.62);
  - in the model in place of kbar: −0.011 (p 0.63).

## What it cannot say
- **Low power (0.06):** a true +0.02 would usually look like this too. The effect is not large; it is not shown to be absent.
- **No cause:** all hits, from different eras. A kill does not show that stand-in chords never matter.
- **Small graphs:** on 3 to 11 chords, curvature mostly counts shared neighbours and triangles, not a smooth geometry.
- **Fixed settings:** laziness ½ and hop distance were fixed in advance. Others were not tried, and should not be tried on these songs now.
- **McGill:** the hold-out was not touched.

## Ideas for a later night (not run)
Curvature with move-count weights in the distance too, or on the directed walk. Each needs its own frozen rule and fresh songs; run here, either would be a variant chosen after seeing this result.

## Notes on the run
The first full run crashed while writing `result.json` (a number-format error). The fix touched only the file writing, and the deterministic rerun was identical. All 2,672 songs had a first year. Runtime: about 3 minutes.

## Data credit
Hooktheory TheoryTab annotations, as released with Sheet Sage (Donahue, Thickstun & Liang, 2022), CC BY-NC-SA 3.0. Discogs-VI 20240701 (Araz, Serra & Bogdanov, 2024), CC BY-SA 4.0.
