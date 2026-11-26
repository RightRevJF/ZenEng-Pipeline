# Shorter lines, or the chorus? Sung transcriptions against WASABI: result

26 November 2026, the songwriting session. Read against `PREDICTION.md` (commit 62e0f7c, before any sung lyric met WASABI or a cover count). Scripts `build.py`, `analyze.py`; numbers in `result.json`. No lyric text stored.

**Repetition is not a typing habit. WASABI's lyrics repeat their lines exactly as the sung transcriptions do, and short lines go with returning lines in sung lyrics too. Shorter lines on their own could not be tested here (too little power).**

## The data
355 BiMMuDa singles with sung lyrics (Billboard year-end top five, 1950 to 2022); 295 of them found in WASABI; 125 matched to a Discogs-VI clique (117 of those also in WASABI).

## The answers
| Question | Result | Verdict |
|---|---|---|
| 1. WASABI's repeat share less the sung one | mean −0.002, median 0.000; against log recording artists ρ −0.04 (one-sided p .68, n 117) | **not named**: no typing habit |
| 2. Do the sources agree? | repeat share ρ 0.74 (means 0.352 sung, 0.350 WASABI); syllables a line ρ 0.53 (8.26, 8.08) | described: they agree, repetition closely |
| 3. Shorter lines on their own, sung, across songs | power 0.09 with 125 songs, under the floor of 0.2; estimate −0.003 a SD (p .48) | **estimate only**, counts for nothing |
| 4. Syllables a line against repeat share, sung | ρ −0.20 (p .0001, n 355); WASABI's was −0.24 | described: the same tie |

## What it means for Design B
- The worry was that famous songs are typed out in full, so that "more repetition" and "shorter lines" in WASABI were fans' habits. They are not: hand transcriptions from the recordings show the same repetition, song by song, and no extra repetition in the more-covered songs.
- So Design B's leads are the songs' own. Within a writer, the more-covered song has more lines that come back (`repeat_share`, +0.077 a SD in the session's join and +0.070 in the maintainer's) and shorter lines, and the shorter lines are mostly those returning lines.
- `repeat_share` was described only in Design B, never predicted, so it is a lead, not a passed test. It now stands free of the typing worry; it would need its own rule and a fresh outcome to pass.

## For the writing
Not "write shorter lines". The trait that travels with covers is a song whose lines come back, and the lines that come back are short: a short-lined hook or chorus that returns. That is advice, not a rule, and it sits with the round-two finding that repetition helps up to a point.
