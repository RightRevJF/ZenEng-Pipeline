# Does the chord graph have a bridge? Result

Run 03, 23 November 2026. The rule was committed before any outcome was opened (`PREDICTION.md`, commit ad201ad). `test.py` ran it once, as written. The numbers are in `result.json`.

## What was predicted
Draw each song as a map. The chords are the places, and a road joins two chords whenever the song moves between them. A **bridge** is a road you cannot avoid: remove it and the map splits in two.

The guess: a cover artist cannot route around such a move, so **among one artist's own songs, a song with a bridge is covered less**. The predicted size was −0.025 SD of log covers per SD of the bridge flag. Because two tests ran tonight, a pass needed p < .025.

## What came out

| | Songs | Artists | Estimate | SE | p |
|---|---|---|---|---|---|
| **All (decides)** | 1,924 | 420 | **+0.021** | 0.016 | 0.21 |
| Half 0 of artists | 932 | 205 | +0.034 | 0.024 | 0.16 |
| Half 1 of artists | 992 | 215 | +0.008 | 0.025 | 0.76 |

The 95% range runs from −0.011 to +0.053, so it leaves out the predicted −0.025. Both halves lean the same way, and it is the opposite way to the guess.

## Verdict: **kill**
The rule kills the test if the estimate is above −0.01. It came out at +0.021.

The "opposite sign" reading ("the bridge is the move people remember") applies only when p < .025. Here p is 0.21, so it does not apply.

## How firm
- **SE: 0.016.** The chair expected 0.015.
- **Power: 0.24.** The script printed this before the estimate. Even if the guess were exactly right, the test would pass only about one time in four.
- **Why the kill still means something.** A true −0.025 would rarely land at +0.021. That is 2.8 SEs away.

## The audit (before any outcome was read)
- **Code checks passed.**
  - Bridges found from electrical resistance matched networkx's bridge finder on all 2,672 songs, down to the exact roads.
  - Foster's theorem held to within 2e-14.
  - No chord was a dead end.
  - The chair's "2,764 of 2,764" probably also counted songs with fewer than 3 chords.
- **Shape.**
  - 2,672 songs, 110 of them with maps in more than one piece. Both counts match the chair's.
  - 30.5% have a bridge: 25% of songs with one clip, 34% with two, 40% with three or more.
  - 31.2% of the final rows have a bridge.
- **Overlap with other measures.**
  - The largest correlation was with the number of distinct chords: 0.18, and 0.20 on the final rows.
  - Every other listed measure, including kbar (+0.12) and the 17 covers-study measures, was at 0.13 or below.
- **Stop rule: not met.**
- **Order.** `first_year` is on the outcome side. So the audit ran first, then `first_year` was read and the audit printed again, and only then were cover counts read. Every kept song had a first year. The rows shrank only through the rule of two or more songs per artist.

## Reported, deciding nothing

| Reading | Estimate | p |
|---|---|---|
| Covers within 5 years | +0.017 | 0.40 |
| Covers after 10 years | +0.014 | 0.34 |
| Without the 81 songs whose map is in pieces | +0.022 | 0.21 |
| Share of chord traffic on bridges, in place of the flag | +0.029 | 0.19 |

All four are small, positive and not significant. Median counts per song:
- 7 covers in all;
- 1 within five years;
- 3 after ten years;
- 0 undated versions.

## What it cannot say
- **Low power.** The test cannot clear bridges entirely. It shows only that an effect as large as −0.025 is unlikely here.
- **Not causal.** An artist's songs still differ in era and in which were singles. YouTube views are not in the data pack, so they are not held.
- **The map is simple.** It sees one step at a time and ignores direction, rhythm and melody.
- **Clips.** The result depends on which sections Hooktheory users transcribed.
- **Scope.** Hits only. The McGill hold-out was not touched.

## Idea for a later night (not tried)
The positive lean may be noise. Testing "the bridge is the move people remember" needs its own rule, frozen first. It must not be read into tonight's numbers.

## Data credit
- **Notes and chords:** Hooktheory, via Sheet Sage (Donahue, Thickstun & Liang, ISMIR 2022). CC BY-NC-SA 3.0.
- **Covers and versions:** Discogs-VI 20240701 (Araz, Serra & Bogdanov, ISMIR 2024). CC BY-SA 4.0.
