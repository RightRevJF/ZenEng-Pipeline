# Chords that move, within each artist's own songs (R02-1): result

22 November 2026. Rule in `PREDICTION.md`, committed (d5f30d0) before any cover count was on this machine. Code `test.py`; figures `result.json`.

**It holds, by the rule written first, and narrowly.** With the performer held still, songs whose chords repeat less within a section are still covered more.

| | Songs | Artists | Chord repetition against covers | p |
|---|---|---|---|---|
| Across artists (the covers study, reproduced today) | 2,360 | | −0.071 | < .001 |
| **Within each artist's own songs** | 1,681 | 365 | **−0.042** | .009 |
| Half A of the artists | 810 | 173 | −0.051 | .02 |
| Half B of the artists | 871 | 192 | −0.034 | .16 |

The rule: −0.04 or stronger, pooled p < .05, the same sign in both halves. All three are met. Power to see −0.04 was 0.69, printed before the estimate.

**How firmly.** The figure is 0.002 past the line, with a standard error of 0.016, so the honest range is about −0.07 to −0.01. It rules out zero. It does not rule out the "belongs to performers" band (weaker than −0.02). About six tenths of the across-artist effect is left once the artist is held; the rest was the artist's, as the judging research suspected. One half of the artists carries it alone at .05 and the other does not.

**Step 0.** The covers study's script, unchanged, on data fetched again today (Hooktheory notes from Sheet Sage; Discogs-VI from Zenodo; YouTube views fetched today): 2,360 songs, chord repetition −0.071, covers and views unrelated (r −0.00). The same rows as the committed result.

**Read beside it, deciding nothing.**

| | Chord repetition | p |
|---|---|---|
| The covers study's full controls, artist held | −0.043 | .007 |
| All seventeen note measures together, full controls, artist held | −0.061 | .005 |
| Artists with five or more songs only | −0.051 | .01 |
| Covers within five years of the first release (middle song: 1) | −0.028 | .15 |
| Covers more than ten years after (middle song: 3) | −0.030 | .04 |

- **Early against late covers:** alike in size. Nothing here says the effect travels through fame, and nothing says early covers are the cleaner target. Night two's advice (report both, decide nothing) stands.
- **The other sixteen measures, one at a time, artist held:** three more pass .05 where about one would by chance: chord surprise (−0.042, p .03: plainer chords, more covers), syncopation (+0.037, p .02) and variety of note lengths (+0.033, p .047). None was the stated test. Chord surprise stays at −0.065 (p .002) with everything else held, and is worth its own test, rule first.
- **The tune:** nothing. Melody surprise, uncertainty and repetition are all near zero within artists, as in every earlier run.

**Against what I expected.** I expected −0.03 to −0.04 and the unsettled band. It came out a little stronger, just inside "holds".

**What follows.**
- The one note finding the project has is not only a habit of certain performers. It survives the test the judging research named as the main obstacle.
- It is small: about 0.04 of a standard deviation of covers for one of chord repetition.
- J1's reading stands, and J1's proposed change to the engine's structure draw is no longer blocked by this test. It still needs its own trial before anything is built, and the fresh-songs leg (McGill, J6b) has not been run.
- R02-2 is done here: `discogs_versions_matched.json` keeps, for each matched song, every version's artists, year and release ids, so breadth across genres can be joined later from the Discogs dump.

**What this cannot say.** All songs are hits with a Hooktheory transcription. An artist's own songs still differ in era and in which were singles. Within-artist does not prove the notes cause covers. Views are today's, not those of the first study. The raw downloads and the views are not committed (size and YouTube's terms); the scripts rebuild them.
