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

## Built as fix 950, and read inside the engine (1,000 builds a song)

| | v41 | with 950 |
|---|---|---|
| Builds' middle range, songs 55 / 54 / 58 / hold-out 59 (asked 18.0 / 18.8 / 19.9 / 18.8) | 14 / 15 / 15 / 15 | 17 / 15 / 17 / 17 |
| The chosen tune's range, songs 55 / 54 / 58 / 59 / 60 | 13 / 15 / 12 / 14 / 17 | 18 / 14 / 12 / 19 / 15 |
| Soundness, three songs | sound | sound (one lean past the quartiles: rhythm scaling, low) |
| Neighbour choice fails the rule, in 100 | 3.0 (1.3 to 5.6) | 1.5 (0.1 to 2.9) |
| A random pick from the engine's pool fails, in 100 | 8.2 (3.7 to 11.4) | 2.7 (0.6 to 5.0) |
| Builds that live, 55 / 54 / 58 / 59 | 398 / 337 / 508 / 420 | 342 / 309 / 419 / 376 |

Song 52 (6/8) and the hymn are unchanged.

**What 950 does not do.** The builds are wider, but the tune the engine *chooses* is wider in only two songs of five (55 and 59). The choice does not read the range (range is printed, not charged), so a wide build is chosen only by chance. Song 54's builds are not wider at all. Paper not yet written: the choice is looked at first.
