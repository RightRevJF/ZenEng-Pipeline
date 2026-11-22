# Run 02: first principles

## 1. Bedrock
Week 01 stands (a cover keeps the notes, drops the recording). New:
- **Fact (card 2).** Where only musicians choose, among non-hits, choice is real selection, not herding. Yet melody adds 3 points of explained variance against 16 for recordings' prestige.
- **Fact (card 1; repo).** Covers pile onto famous artists (top 0.1% take 41%). But among our hits the artist accounts for only 0.14 of the differences in covers: most variation lies between songs of the same artist.
- **Fact (card 1).** Covering stays in-genre for jazz (73%), not country (43%) or blues (37%). Week 01's "against the pull" case for breadth holds only in some genres.
- **Fact (card 3, 15 listeners).** Hearing raises liking at every complexity. Love partly records exposure.
- **Fact (repo).** Chords that move predict covers on two sources (−0.124, −0.071), not views.
- **Assumption.** That this is the song, not the performer. No test held the artist fixed; year was held as a straight line, and harmony, era, genre and covering culture travel together. Mechanism (room to arrange) assumed.

## 2. Question every requirement
- **G = love + covers** (Jason). Stays. Covers suit a notes judge better (love tracks exposure). Flagged.
- **Covers as Discogs artist counts** (data habit). Likely includes budget "hits of the year" cover albums made within months of a chart run.
- **Early covers only** (week 01, by analogy). Those budget albums make early covers among the most fame-driven; covers ten years on are the lasting ones. Report both; decide nothing on the contrast.
- **Hot 100 weeks and peak as controls** (debate). Chart success is partly caused by the notes, so holding it can remove the effect sought. Sensitivity only.
- **Performer's covers on other songs** (card 1). Artist fixed effects hold it by design, nothing fitted.
- **"First performer or not"** (chair). Set to 1 for every song in the Discogs script: inert.
- **Notes only** (Jason): kept. **Hits only**: data habit; narrows the range.
- **J1 gate on the structure draw (800)**: between-artist evidence only; wait for section 5. **Song 59 seal**: law of the experiment.

## 3. Delete (recommended; Jason decides)
- J3, earn the surprise: failed on Discogs-VI (+0.009, p .54).
- J4, smooth approach: untested; one more term in weak tests.
- J2, plain-chords interaction: folded out; its base term was p .06.
- J5, hook readings: folk memory, not covering; the tune failed five runs.
- Pitch-class entropy as a secondary term: a sixth try at the tune.
- Card 3's love-by-exposure interaction (reverse causation); card 4's E and R as tests.
- Chart controls in the primary model.

Park: the spectral gap g. It passed the renaming check, but its stability is unknown and Hooktheory clips make tiny graphs.

## 4. Simplify
One term (within-section chord repetition), one outcome (log covers, all years), one design control (artist fixed effects), plus year and views. Holds fame, voice, genre and most of era at once.

## 5. Speed the loop
**Kill test.** Within-artist chord repetition against covers: the 2,360 Discogs-VI songs, artists with two or more, artists halved by name. Never run.
**Prediction, written now.** Beta −0.04 or stronger, pooled p < .05, same sign in both halves. Killed if weaker than −0.02 (under 30% of the between-artist −0.071): the finding then belongs to performers, eras or genres. Between: unsettled. Compute power first.
**Loop.** The download and per-song tables are gone from disk. Re-stream once, keeping each version's year, artists and release id; commit a small derived per-song table. Then each test runs in seconds.

## 6. The obstacle and the way through
**Obstacle.** The notes have never been varied while the performer is held still. No note finding that holds has held the artist fixed. The one within-artist test (21 measures against G) found nothing.
**Way through.** A cover is a natural experiment: notes held, performer changed. Mirror it: performer held, notes changed (section 5). If chord motion survives, add the outcome made of notes: cross-genre breadth, judged against the original's genre. *Speculation:* if it dies, the hits-only note signal is mostly the performer; look next at songs by the same writers that never charted.

## The one check
**Prediction (written first).** Committed scripts read only artists, title and year per version, with no genre field; probably a release id (60%). Fails if any reads `genres` or `styles`.
**Result: held.** `discogs_cliques.py` reads title, artists, release date, release id and writers per track; no committed file mentions genre or style. It keeps only counts and the earliest year, discarding release ids and per-version years, so neither breadth nor early covers can be computed from it. Release ids mean the CC0 Discogs dump can supply genres. (Beyond committed data: the download is gone from disk.)
