# Review 25: Luthier v39 (Window 196)

20 November 2026. v39 (944, the shape from the song; no kept song drawn) is merged into main at aaa2470.

## Reproduced

- The seven kept-table makers, the new `make_kept_words_to_shape.py` included: byte for byte.
- Songs 52, 54, 55, 58 and 59, song 53's run, and stage 4: byte for byte as v39 wrote them.
- Song 60 rerun on main's v39: byte for byte with `songs/p70/lyric60.v39.song.json`. The delivered record is untouched.
- `soundness.json` and `neighbour.json` (ranges included): byte for byte.
- Not rerun: the held-out study in `studies/words_to_shape` (500 shuffles) and `sections.py`.

## 944

**The ruling stands, and keeping 944 despite its failed check is right.** The check was the writer's own design question, not a figure to optimise. The cost is stated plainly: the random pool pick is 7.8 in 100 (range 4.1 to 11.4) against v37's 3.2 (1.2 to 6.1), with the ranges just touching, still inside the standard's bar. The cause is named: rhythm scaling, low in songs 55, 54 and 58 together. Striking "verses step, choruses leap" from the theory, on the evidence of 137 kept songs, is the right use of the corpus.

**749.128: the words-to-shape features are measured two ways.** `make_kept_words_to_shape.py` splits a kept song's words into lines in proportion to each line's notes, because the corpus does not tie words to lines. `words_to_shape.from_sung` reads a Luthier lyric's real lines.

The feature that suffers most is "lines said again word for word". Kept songs read 0.000, 0.025, 0.182 at the 10th, 50th and 90th percentiles; real choruses repeat far more than that, so the proportional split is missing most repeated lines. Songs 55, 54, 58, 59 and 60, read from their real lines, give 0.232, 0.138, 0.193, 0.333, 0.275, at the kept 84th to 99th percentiles. Read the kept way (the same proportional split applied to their lyrics), they give 0.018, 0.017, 0.000, 0.190, 0.100.

The asks move with it, measured the kept way against what the records hold:

| | Range | Bars on a figure already sung | Bars on a rhythm already sung |
|---|---|---|---|
| Song 55 | 17.5 (15.6) | 0.402 (0.509) | 0.536 (0.629) |
| Song 54 | 18.4 (17.3) | 0.399 (0.461) | 0.550 (0.603) |
| Song 58 | 19.8 (18.0) | 0.361 (0.462) | 0.501 (0.588) |
| Song 59 | 17.2 (15.9) | 0.479 (0.551) | 0.595 (0.658) |
| Song 60 | 17.9 (16.3) | 0.454 (0.545) | 0.576 (0.655) |

So the repetition asks are inflated by 0.06 to 0.10, and the range asks are understated by 1 to 2 semitones. The window's two motivating examples lean on it: song 59 "asks 0.608" and the borrows-from-the-words trial was aimed at the inflated asks. Measured the kept way, the builds' bars on a figure already sung (0.384, 0.491, 0.412, 0.400) sit at or above what the words ask in three songs of four.

The segmentation-free feature agrees. Words in a three-word run already sung puts Luthier's lyrics at the kept 10th to 29th percentiles: by that measure they repeat less than kept lyrics, not more. "Unevenness of the lines" is at the kept 0th to 12th percentiles both ways. That may be real (Luthier's lines are even), or another sign that a kept "line" is not a lyric line.

**749.129: movement at the kept middle makes every song alike by design.** The paper says so and accepts it. Jason's ruling forbids taking a song's shape from one kept song. It does not forbid a style guide, and the paper already holds genre tables (studies/genre). Movement from the song's own genre family's middle, overridden by the writer, would be the engine's theory and still let a lane differ.

**749.130: rhythm scaling, with a contrast inside Luthier.** v39's records split: songs 59 and 60 read rhythm scaling 0.668 and 0.717 (kept middle 0.656); songs 55, 54 and 58 read 0.578, 0.587 and 0.540. Yet song 60's share of repeats from far back (0.688) stands at the kept 96th percentile, as song 54's does (0.742). Far-back repeating alone does not explain low rhythm scaling, which weakens my 749.123 as a cause. It remains a fault of shape: the far-back share still sits at the kept 70th to 96th percentiles in all five songs. The rhythm-scaling study now has a free contrast: what songs 59 and 60 have that 55, 54 and 58 lack.

**Small.** In song 58's fifteenth edition the top note, D4, comes 10 times, all in the bridge. The studies scripts that read a drawn song (studies/review19/aimpool.py, studies/holdout59) are retired, as the paper says.

## Song 58, fifteenth edition

From the v39 record: D major, C♯3 to D4 (13 semitones as sung; its words ask 18.0). Steps 0.355, leaps 0.119, repeated notes 0.377 against the kept middle's 0.396, 0.102, 0.312. Rhythm scaling 0.540. All 44 document checks pass. The fourteenth edition is kept in `songs/p68/out/fourteenth_edition_v37/`.
