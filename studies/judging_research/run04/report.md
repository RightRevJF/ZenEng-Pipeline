# Judging research, run 04

24 November 2026. Research only: nothing here goes into the Luthier engine or main. Song 59 and its folders were not read. The McGill hold-out was not touched.

## Tonight in three sentences

Tonight ran six tests: five frozen before any outcome was joined, and one more frozen after seeing those five. Two put each song's chords on a fixed map from geometry, the torus of Fourier phases, and tested them against cover counts. Three used a fresh outcome nobody had looked at: whether a song appears in the Discogs-VI covers database at all, across 9,588 songs compared only with the same artist's other songs.

All five frozen tests were killed by their own rules. The surprise was the opposite of the project's one replicated finding. Songs whose chords repeat more were *more* likely to have been recorded by someone else at all. Among songs that were recorded again, repeating chords still goes with fewer different coverers.

The sixth test checked whether that surprise was only the original artist's own credit variants. It was not, but the result is not strong enough to count. It is a lead for fresh songs, and it hints that "looping less" may help a song's reach in one way and hurt it in another.

## The experiments

Six hypotheses ran tonight, so each needed p < .05/6 = .0083 (the five frozen first were set at .01; none came near either bar). A pass also needed the same sign in both halves of the artists.

| Test | Prediction written first | Result | Verdict | Power |
|---|---|---|---|---|
| 1. Chords that move, on "versioned at all" (9,588 songs) | More repetition, less likely in Discogs-VI (−1.0 point per SD) | **+1.19** points (SE 0.50, p .018); both halves positive | Killed (wrong sign) | 0.28 |
| 2. Plain chords, same model | More chord surprise, less likely in (−1.0) | −0.10 (SE 0.41, p .81) | Killed | 0.45 |
| 3. Information rate (bits per beat far from the usual) | Further from usual, less likely in (−0.8) | −0.16 (SE 0.34, p .64); halves split | Killed | 0.40 |
| 4. P/L/R share on the torus, against covers (1,924 songs) | More smooth moves, more covers (+0.02 SD) | +0.0065 (SE 0.018, p .72) | Killed | 0.07 |
| 5. Thirds axis on the torus, against covers (two-sided) | High or low, either reading | +0.006 (SE 0.017, p .73), inside the "both die" band | Both killed | 0.08 |
| 6. Foreign versions (after seeing results) | Loop effect lives in versions by *other* artists (+0.9) | **+1.00** (SE 0.49, p .044); halves +0.45, +1.43 | Unsettled (a lead) | 0.21 |

**1 and 2. A new outcome, and a reversal.** Discogs-VI only lists a song when at least two different sets of performers have released it under the same title and writer. So "is the song in it at all" is a rough record of whether anyone took it up again. It had never been used, and it gives five times as many within-artist songs as before.

The guess was the replicated rule: chords that move win. The opposite came out. Within an artist, the songs that loop more were about 1.2 percentage points more likely to be in, against a base of 23%. It also showed in both halves of the artists and in a second model (conditional logit, p .009). By the rule it is a kill, not a discovery, because the "opposite sign" pass needed p < .01. Plain chords (low chord surprise) did nothing on this outcome.

**3. Information rate.** The Inventor borrowed from speech research the idea that listeners like a habitual rate of information. The measure was how far a song sits from that rate. It predicted nothing, and the artist halves disagreed.

**4 and 5. Geometry on the torus.** Both measures are new, stable between clips of a song (0.35 and 0.32), and unlike anything already measured (largest overlap 0.14 and 0.25). Both came out near zero. At power 0.07 to 0.08, these tests could only rule out a large effect (above about +0.04 SD).

**6. The check on the surprise.** One worry was that looping songs, often dance and pop singles, collect "Artist" and "Artist featuring Guest" credits. Those would count as two versions with no one else involved. That is the artefact story. But only 94 of the 2,224 matched songs had nothing except the original artist's own variants. Almost all of the effect (+1.00 of +1.19) sits in songs that another artist really recorded.

The test missed its bar (p .044 against .0083). It was designed after seeing test 1, on the same songs, so it is a lead and nothing more. The maintainer's list already notes that weeks on the chart lean the same way as tonight's sign (749.159).

## The mathematics, plainly

**A map that does not depend on the song.** Run 03 learned that shapes built from a song's own handful of chords mostly measure how many chords it has. So tonight used a map fixed in advance. It comes from Amiot's "torus of phases" [1].

Take any chord, say C major (C, E, G), and ask two questions:
- How well does it line up with a cycle of major thirds? The angle of the answer is φ₃.
- How well does it line up with the circle of fifths? Its angle is φ₅.

Two angles make a point on a doughnut (a torus), since each angle wraps around. Every major and minor chord gets its own point. Change key, and every point slides by the same amount. That is the paper's proved lemma, so any shape measured on the doughnut is the same in every key.

**Worked example.**

| Chord | φ₃ | φ₅ |
|---|---|---|
| C | 0.46 | 0.79 |
| G | 2.03 | 1.31 |
| A minor | −0.46 | 1.31 |

On the doughnut, C to A minor is 1.07 and C to G is 1.66. The closest neighbours of any triad turn out to be exactly the three chords that keep two of its notes and move one by a small step. Music theory calls these the P, L and R moves. A cover artist can re-voice them easily, which is why test 4 counted them.

In the loop C → G → A minor → F, only one move of four (A minor to F) is such a step, so its share is 0.25.

**The thirds axis.** Test 5 asked how strongly a song's chords, weighted by time, point one way on the thirds circle. Chords a major third apart (C and E major) add up; chords a whole step apart (F and G) cancel out.

| Progression | Thirds-axis value |
|---|---|
| IV–V alone | 0 |
| I–vi–IV–V | 0.33 |
| I–IV–V–I | 0.37 |

**What the mathematics also taught.** The paper suggests counting how many times a song's path winds round the doughnut, and the area it sweeps. All three imaginers found, independently, that this fails on pop songs. A whole-step move between two chords of the same kind (IV to V, or I to ♭VII) lands exactly half-way round the thirds circle. Whether it went "left" or "right" is then arbitrary, so winding and area have no fixed answer. The paper names only the tritone; tonight's finding corrects the card.

**What it showed.** The fixed map worked as hoped as a measuring tool: stable, key-free and new. It found nothing about covers that these songs could detect. These songs are now spent for geometry, and the map needs fresh songs or a larger outcome.

## The brainstorm

| Idea | Stance | Status |
|---|---|---|
| G1 Diatonicity (how tightly chords sit on the fifths circle) | Geometer | Withdrawn; parked for fresh songs |
| G2 + L2 Share of smooth (P/L/R) moves on the torus | Geometer, Listener | Tested: killed |
| G3 vs I1 Thirds axis, high or low | Geometer, Inventor | Tested (two-sided): both killed |
| L1 Chords that move on "versioned at all" | Listener | Tested: killed (opposite sign) |
| Chord surprise as its own test (from run 02) | earlier backlog | Tested: killed |
| I3 Information-rate deviation | Inventor | Tested: killed |
| L3 The one chord you remember | Listener | Withdrawn (no power) |
| I2 The harmonic ratchet | Inventor | Withdrawn |
| Winding and swept area | all three | Stopped: undefined on pop loops |
| Foreign versions (two-part story) | first principles | Tested after seeing results: unsettled |

**Agreed:**
- Winding and area are unusable.
- Phase concentration on the fifths circle is the fifths path renamed.
- Duplicates had to be merged.

**Split:** the Geometer and the Inventor read the same number, the thirds axis, in opposite directions. The Skeptic showed the Inventor's reading was flawed (IV–V alone scores as "balanced" with no home chord). Both readings were then kept in one two-sided test, and the data supported neither.

**The Skeptic's sharpest catch:** in the linear model, artists with no song in Discogs-VI still pull the estimate. So that rule had to be fixed before the outcome was joined.

## First principles

**The obstacle.** Every outcome so far is a by-product of a credit database, and its noise is as large as the notes signal (about 0.04 SD). Tonight it also showed two faces. The same feature, chords that loop, went with *more* chance of being taken up and with *fewer* distinct coverers once taken up. Every song with notes on disk has now been looked at.

**The way through (partly speculation):**
- Use outcomes the original artist cannot produce: versions by other artists only. Weight covers by how independent the coverer is, with karaoke factories out and later covers in.
- If loops draw cover factories, the audience's taste is leaking into the covers count.
- Fresh songs are needed: the notes of all 13,198 Hooktheory songs, not only the matched ones.

**Deleted (recommended; Jason decides):**
- chords that move, predicted negative on "versioned at all" (wrong sign)
- chord surprise as its own claim (killed twice; kept as a control)
- information-rate deviation
- P/L/R share and mean torus step
- the thirds axis in both readings
- torus winding and area (undefined)
- geometry on run 03's songs, as a family (five kills now)

**Simplified:** chord repetition, within artist, on one versions file read two ways:
1. Did anyone outside the original artist release the song?
2. How many did?

**Flagged:**
- The loop-less trial in the engine (749.159) rests only on cover counts among songs that were already versioned. If tonight's sign holds, looping less could cost a song its chance of being taken up at all, so the trial is best kept as a reading until fresh songs settle it.
- The cover count itself includes the original artist's own "featuring" variants. It should be recomputed (fix list R04-2).

## The papers

1. **Amiot (2013), "The Torii of Phases"** [1], Mathematics and Computation in Music (LNCS 7937); read in full from arXiv 1208.4774. Each chord becomes a point on a doughnut given by the phases of its third and fifth Fourier coefficients. One lemma is proved: changing key slides every point equally, and turning the chord upside down mirrors it. The layout of the Tonnetz (the classic chord network) is shown by numbers, not proved. Chords with a missing coefficient, like the augmented triad, become whole circles. There are no statistics; Amiot himself asks for larger tests, and tonight was one.
2. **Araz, Serra & Bogdanov (2024), "Discogs-VI"** [2], ISMIR 2024; read in full from arXiv 2410.17400. It is the dataset behind every cover count in this project. A group of versions is formed by exact title and a shared writer credit, and needs at least two different performer sets. A song released only once is never in. There is no audit of errors. Retitled covers and songs missing writer credits fall out, so "not in" is a noisy "never covered".

## Ideas for coming nights (not testable tonight)

- **Tonic resistance, the fifths path, diatonicity and every torus measure on fresh songs.** They need the notes of the 10,429 unmatched Hooktheory songs. Those are in Sheet Sage's `Hooktheory.json.gz`, which is not on this machine, or in the gated Hugging Face copy `m-a-p/HookTheory`, which needs a login. This is data request R04-1.
- **The two-part story, confirmed.** "Taken up by another artist" against "how many took it up", on songs not yet used. This needs the same fresh notes, or the re-match of R03-1.
- **Measure the ceiling with MusicLab:** the data is not on hand. **Cover breadth across genres:** it needs the Discogs releases dump, and the choice of yardstick is Jason's.
- **Counter-evidence for the Skeptic:** none was read tonight, so run 05 must include it.

## Paywalled papers for the inbox

None tonight: both papers were open.

## The proposed fix list

See the separate Doc "Proposed fix list: judging research, run 04". The same text is in `run04/proposed_fixlist.md`.

## References

1. Amiot, E. (2013). The Torii of Phases. In *Mathematics and Computation in Music*, LNCS 7937. https://arxiv.org/abs/1208.4774
2. Araz, R. O., Serra, X. & Bogdanov, D. (2024). Discogs-VI: A Musical Version Identification Dataset Based on Public Editorial Metadata. ISMIR 2024. https://arxiv.org/abs/2410.17400
3. The maintainer's within-artist test: `studies/judging_checks/within_artist/RESULT.md` on main (−0.042, p .009).
4. Run 04 commits on judging-research: 00ab557 (predictions), 5c8be4b (results), 4410a0e (sixth prediction).
5. Data: Hooktheory TheoryTab annotations via Sheet Sage (Donahue, Thickstun & Liang 2022), CC BY-NC-SA 3.0; Discogs-VI 20240701 (Araz, Serra & Bogdanov 2024), CC BY-SA 4.0.
