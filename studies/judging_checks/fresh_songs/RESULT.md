# Chords that move, on fresh songs (J6b): result

22 November 2026. Rule in `PREDICTION.md`, committed (f25209f) before any McGill song was joined to covers. Code `test.py`; figures `result.json`.

**Same direction, not settled.** On songs the finding was not found on, chord repetition within a section goes with fewer covers, weakly, and the range includes zero.

| | Songs | Chord repetition against covers | 95% range | p |
|---|---|---|---|---|
| Hooktheory songs, across artists (where it was found) | 2,360 | −0.071 | | < .001 |
| Hooktheory songs, within artists | 1,681 | −0.042 | −0.07 to −0.01 | .009 |
| **McGill songs, fresh** | 438 | **−0.028** | −0.11 to +0.05 | .50 |
| McGill, with chart peak held (sensitivity) | 438 | −0.049 | | .20 |

739 charts; 721 with the measure; 543 matched to a Discogs-VI group; 105 dropped because a Hooktheory song matched the same group; 438 fresh (middle song: 13.5 covers). Power to see −0.05 was 0.22, printed before the estimate: this test could confirm little and was never likely to. It does not contradict the finding (the fresh figure's range holds −0.042 and −0.071 comfortably), and it does not confirm it.

**Against what I expected:** I expected −0.03 to −0.08; it is −0.028, just outside.

**One thing I changed and put back.** My first run of the script matched artists loosely (one name inside the other), which the rule did not say; it gave −0.022 on 466 songs. The figures above are by the rule as written (the artist among the group's performers).

**What it cannot say.** The measure is not the covers study's: whole charts by section, a different chord alphabet, no views held. A real effect of −0.04 would be seen in a test this size about one time in six.

**The hold-out.** The 438 songs' cover counts are in `studies/judging_data/mcgill_covers_discogs_HOLDOUT.json`. They have now been read once. Anything else tried against them needs its rule committed first, and each such test counted.
