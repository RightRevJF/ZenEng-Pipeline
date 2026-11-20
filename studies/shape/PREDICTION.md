# Song as a shape — predictions, written 19 Nov 2026 before any measure was run

Yardstick (Jason, 18 Nov): great = still loved long after release + covered by many. G = mean of
 love  (Spotify 2021 popularity ranked against Hot 100 songs released within 3 years) and
 covers (SecondHandSongs versions, 0 if not in the 10,000-work list, ranked against set songs within 5 years).
Set: songs of 2005 or earlier with love known and >= 48 notes, one entry per title (whole songs preferred): 1,102.

The path. Each sung note is a point with six coordinates: scale degree on the circle of fifths (2), height from the
song's median in octaves (1), place in the bar on a circle (2), log2 of time to the next note (1). Tonic by
Krumhansl-Schmuckler. The shape is the cloud of windows of 8 successive notes (48 dimensions).

Predicted direction with G (partial Spearman, holding year, log note count and source):
 M1 return        share of window pairs within a fixed radius                         +
 M2 varied return of the returning pairs, the share that are near but not identical     +
 M3 curvature     mean turning angle of the six-coordinate path                       -
 M4 persistence   Hurst exponent of the path's displacement over lags 1-16            +
 M5 room used     participation ratio of the window cloud                             -
 M6 loops         total H1 persistence of the window cloud over its diameter          +
 M7 word and tune (kept songs with words only) canonical correlation of word windows
                  with tune windows, over the same with words shuffled within lines   +

Pass, for each: predicted sign in both halves (split by hash of title) with p < .05 in each, and pooled p < .007
(seven measures). Anything else is a fail. A pass must also survive adding chart peak as a control, and show the
same sign on the whole-song sources alone. Nothing goes into the engine on this study.
