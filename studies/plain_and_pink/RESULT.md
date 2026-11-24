# Plain and pink: result (24 November 2026)

Rule committed first (c6301aa); `study.py`; `result.json`.

**Verdict by the rule: they do not trade.** Across the 167 kept songs, melody surprise and the pitches' DFA-1 are unrelated (Spearman rho -0.05, p .51; DFA-2 -0.04). The same on syllable attacks (-0.05, -0.02).

**A region where both hold exists.** 47 of 167 kept songs (28%) are at or under the kept median of surprise (3.18 bits) and at or over the kept median of DFA-1 (0.906). Their quartiles: DFA-1 0.95, 1.03, 1.08; DFA-2 1.05, 1.12, 1.18; three-pitch share 0.55, 0.63, 0.69; surprise 2.61, 2.84, 3.09.

**What drives song 62's problem.** The share of notes on three pitches goes with both: more concentrated tunes are plainer (rho -0.45 with surprise) and whiter (-0.45 with DFA-1, -0.40 with DFA-2). That is the cheap road to plainness, and it whitens. The kept songs in the region get their plainness without it: their three-pitch share is the kept median (0.63), not the 0.79 of song 62's first edition.

**Song 62 among the kept (every note).**

| | Surprise (pct) | DFA-1 (pct) | DFA-2 (pct) | Three pitches (pct) | In the region |
|---|---|---|---|---|---|
| The engine's draw | 2.85 (28) | 0.97 (64) | 1.04 (54) | 0.60 (37) | yes |
| First edition | 3.02 (36) | 0.88 (43) | 0.94 (30) | 0.76 (85) | no |
| Pink survivor | 3.63 (77) | 0.98 (66) | 1.10 (71) | 0.59 (34) | no |

The engine's own draw was already plain and pink; the design's gates moved the first edition out of the region by concentrating its pitches.

**For the gates (749.165, 749.166).** Read together, not one at a time: surprise at or under the kept median, DFA-1 at least 0.95 and DFA-2 at least 1.05 (the region's lower quartiles), three-pitch share at most 0.69 (the region's upper quartile).

**What it cannot say.** Kept songs are 4/4 chart hits transcribed by ear; DFA on a few hundred notes is noisy; the region is defined by medians, not by any outcome.
