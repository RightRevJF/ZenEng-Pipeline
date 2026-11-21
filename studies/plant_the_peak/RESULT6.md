# The peak to whichever chorus line reaches it: result of the sixth trial

**Passes.** (`trial6.py`, 100 tries a song; `trial6.json`.) By the rule written first, it is built.

| Check (songs of 4, 3 needed) | Met in |
|---|---|
| 1 The range follows the words | 3 (55, 58, 60) |
| 2 The peak is a peak | 3 (55, 54, 60) |
| 3 Builds survive | 4 |
| 4 The words still sit | 3 (not 60: 0.326 to 0.294) |

| Song | Middle range, as built → planted | Builds within 2 of the asking | Top-note share inside the kept band | Peak planted, tries in 100 | Builds |
|---|---|---|---|---|---|
| 55 | 14 → 17 | 0.24 → 0.61 | 0.83 → 0.90 | 85 | 29 → 41 |
| 54 | 14 → 15 | 0.24 → 0.40 | 0.68 → 0.88 | 62 | 34 → 42 |
| 58 | 14 → 19 | 0.10 → 0.56 | 0.77 → 0.78 | 86 | 48 → 41 |
| 60 | 17 → 17 | 0.52 → 0.64 | 0.67 → 0.92 | 90 | 27 → 25 |
| 59 (read only) | 15 → 19 | 0.29 → 0.78 | 0.80 → 0.81 | 70 | 41 → 27 |

**Against what I expected:** the range and the builds went as expected; check 2 I expected to stay unmet and it is met (a planted peak is sung once or twice, so the share of notes on the top falls into the kept band).

**Not settled:** song 54 still reaches the range in only 40 builds in 100; song 60's words' fit falls by 0.03; the hold-out keeps 27 builds of 41 (under the 7 in 10 asked of the fitted songs). A trial outside the engine passed once before (943) and failed inside it, so the build is checked against the soundness and pool standards before it stands.
