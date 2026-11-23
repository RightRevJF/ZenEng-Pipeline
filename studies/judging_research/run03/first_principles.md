# Run 03: first principles

23 November 2026. Research only. Recommendations; nothing is dropped without Jason.

## 1. Bedrock
**Facts added tonight.**
- Bridges in the chord map do not go with fewer covers within artist: +0.021 (range −0.011 to +0.053) against a predicted −0.025.
- Ollivier curvature adds nothing beyond size, repetition and surprise: −0.0002 (SE 0.029). At power 0.06 this says only that the effect is not large.
- The mathematics was computed right: networkx, Foster's theorem, Prop. 29 and a second solver all agreed on every song.
- On Hooktheory maps, size explains 46% of curvature; the gap g agrees only 0.17 between two clips of one song.
- Chords that move (−0.042 within artist) is untouched.

**Assumptions still carrying weight.** That a few user-chosen clips stand for the song; that one-step chord succession holds what coverers hear; that a low-power null means "small".

**Unplanned, not a test.** In the curvature model, chord repetition came out −0.061 and chord surprise −0.089, against the maintainer's −0.042. My notes-only check: repetition and surprise correlate −0.29 across songs, and surprise +0.52 with chord count (2,769 matched songs; rechecked by the run). Songs that loop less surprise more, and the two pull covers opposite ways, so each may mask the other. Same songs, a model built for another question: a forking path, a lead, not evidence.

## 2. Question every requirement
- **Yardstick (love + covers).** Every test since run 02 uses covers alone. Flag: say so, or bring love back.
- **Covers sample.** 13,198 Hooktheory songs have chord measures; 2,769 are matched to Discogs-VI, and only 2% of those have no cover. The corpus is selected on having been versioned at all. Flag.
- **Notes only; hits only.** Kept; hits-only is a data habit.
- **The clip-pooled Hooktheory graph as the unit.** This killed the geometry: 3 to 11 chords, bridges rising from 25% to 40% with clips per song. Flag strongly: no geometry built from these maps again.
- **Within artist.** Right, though it costs 28% of rows. Keep.
- **The low-power habit.** Powers 0.24 and 0.06. The curvature kill rule would have killed a true +0.02 one time in four; each look spends the corpus. Flag: a power floor (0.5) before joining outcomes.
- **J1 gate.** Nothing tonight moves it. An engine rule ("move, but plainly") must never come from an unplanned observation.

## 3. Delete (recommended)
- **Bridge indicator (G2):** killed; wrong sign, 2.8 SE from the prediction.
- **Traffic on bridges (L2):** +0.029, p .19; same failure.
- **kbar (L1/G1):** killed; zero, and the little seen without surprise was surprise.
- **Shuffle-relative curvature:** repetition renamed (ρ −0.52); null.
- **g on Hooktheory, and S = 1 + g/π as its own test:** g failed stability; S only rescales g. S is Jason's call.
- **Curvature variants on these songs:** chosen after seeing tonight.

## 4. Simplify
Chords that move, simplest honest form: log covers, artist held, first year, chord count, and two terms only, chord repetition and chord surprise, because each seems to mask the other. No geometry.

## 5. Speed the loop
**No fresh songs are on disk.** Cheapest new data: re-match the ~10,400 Hooktheory songs with chord measures but no Discogs-VI link, by a title rule fixed in advance, blind to covers, de-duplicated against the 2,769. Commit the list, freeze the rule, join once.

**Prediction, written now.** Fresh songs, within artist, both terms held together: repetition −0.04 (not the inflated −0.061), surprise −0.04; each needs p < .025 and the same sign in both artist halves. **Kill:** repetition weaker than −0.02. Surprise weaker than −0.02 kills "plainly", not J1.

**Power** at −0.04, p < .025, scaled from tonight's SE (0.017 on 1,924): about 0.29 with 1,000 within-artist songs, 0.56 with 2,000, 0.76 with 3,000. Under 2,000, wait.

## 6. The obstacle and the way through
**Obstacle.** The one signal is small (about 0.04 SD), every song on disk has been looked at, and geometry built from a dozen moves measures size and repetition.

**What the mathematics taught.** The theorems held exactly; the objects were too small. Curvature on a five-chord map counts triangles; a loop's gap is zero; a bridge depends on how many sections were transcribed.

**Way through (speculation).** Put geometry where the space is fixed and not built from the song: Tymoczko's voice-leading space, or the phases of a chord's Fourier coefficients (the fifths and thirds circles). Each song is a path in one shared space; a short song gives a noisier reading, not a different geometry. Voice-leading distance per move, or the arc covered on the fifths circle, can be checked for stability before any outcome. Second, McGill's whole-song maps, where g is stable (0.58), touched only by a frozen rule. Third, fresh songs in bulk: the re-match, or a large chord corpus such as Chordonomicon (unverified).
