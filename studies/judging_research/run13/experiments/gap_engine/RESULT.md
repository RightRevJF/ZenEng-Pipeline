# gap_engine: result (no outcome read)

**Data.** 14,747 real 4/4 Hooktheory clips (within-artist rows) against 8,400 sections from the metre engine's survivors on eight spent or seen songs (50, 54, 55, 58, 60, 61, 62, 66; 150 builds each), first 8 bars each; plus the 56 sections of those songs' actual picks.

**The engine's melodies are easy to tell from real songs by their notes alone.** Out-of-fold AUC **0.969** (each engine song held out once). Every held-out engine song's sections score below the real median; the actual picks score −2.5 log-odds on average, against +4.7 for real clips and −3.3 for builds.

**Numeric predictions (written first, PREDICTION.md):** P1 AUC ≥ 0.90: **true**. P2 the engine leans on one pitch more (commonest pitch-class share 0.455 against 0.340): **true**. P3 rhythm-minus-pitch repetition by bar higher in real songs: **false** (0.143 both). P4 in real clips bar rhythms repeat more than bar intervals (0.400 against 0.286): **true**. P5 a real phrase spans 7 to 11 semitones: **true** (9, the world-music branch's folk figure exactly).

**The gap list** (|AUC − 0.5| ≥ 0.15, the same way in at least 7 of 8 songs). Real median against engine median (picks):

| What | Real | Engine | Picks |
|---|---|---|---|
| Repeated notes (unisons), share of steps | 0.18 | 0.39 | 0.27 |
| Commonest pitch class, share of time | 0.34 | 0.46 | 0.39 |
| Pitch-class entropy (bits) | 2.28 | 1.88 | 2.08 |
| Note lengths used (distinct) | 4 | 6 | 5.5 |
| Rhythm 3-grams heard before in the window | 0.54 | 0.36 | 0.36 |
| Phrase range (semitones) | 9 | 5.7 | 6.2 |
| Notes a phrase | 18 | 9 | 9.5 |
| Phrases in 8 bars | 2 | 4 | 4 |
| Rest share | 0.09 | 0.18 | 0.22 |
| Pitch line's echo one bar later (autocorrelation) | +0.08 | −0.10 | −0.08 |
| Turns of direction, share | 0.56 | 0.70 | 0.67 |
| Whole range (semitones) | 12 | 8 | 9 |

In one sentence: real songs reuse a few rhythms and move the pitch over long, wide phrases that echo bar to bar; the engine varies its rhythms, stops often, and sits on one pitch, repeating notes.

**What it cannot say.** It tells "real pop" from "engine", not "great" from "ordinary" (realness_covers tests that, and it went the other way). Hooktheory clips are mostly choruses and verses chosen by transcribers; the engine's sections include tags and intros. The engine sets words syllable by syllable, which raises repeated notes by design; real pop does too, so the gap is still the engine's. Credit: Hooktheory via Sheet Sage (CC BY-NC-SA 3.0); the Luthier engine.
