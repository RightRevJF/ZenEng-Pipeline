# Week 01: the chair's ranking

Week 0 ranked nothing, so every idea below is new this week or builds on an earlier repo study (named). Nothing goes into the engine.

## 1. Early covers: does "chords that move" survive the fame loop? (BUILDS ON the covers study, Discogs-VI replication)

**Idea.** Count only covers made within five years of a song's release, before fame can feed back into covers. If the one note finding that replicated (less chord repetition within a section) still predicts these early covers, it is a mark of the song and not of its fame.

**Support.** Card 4 (covers may cause love; time-order the halves of G), card 3 (path dependence). The Skeptic's tougher version; the Listener and Geometer both adopted early covers as the target.

**Prediction.** Chord repetition predicts early covers with a standardised beta of -0.05 or stronger (fewer repeats, more covers), holding release year, genre, views and artist clustering. Second leg: early covers predict the love half of G beyond year; late covers depend more on the original's popularity than early ones do.

**Test that could fail.** Discogs-VI (version groups with release years) on the 2,360 Hooktheory songs of the covers study, cross-checked with SecondHandSongs dates where matched. Report early, late, and love alone separately. **Fails** if the early-cover beta is weaker than -0.03 or p > .10 while it holds on late covers (the signal travels through fame), or if signs differ between Discogs-VI and SHS dates. Weakness: not fresh songs (the finding came from this set); this asks *when*, not *whether*. Early covers are fewer, so run a power check first.

**Decisions.** Re-fetch Discogs-VI and the Hooktheory notes (not committed). Accept early covers as the cleaner target for G's covers half. Decide if adding recording features as a control is worth needing audio.

## 2. Plain vocabulary, varied path, on fresh songs (BUILDS ON the covers study's two main effects; the interaction, the parsimony term and the McGill set are NEW)

**Idea.** Musicians may cover songs whose single chord moves are common but whose path does not loop. Where a song does surprise, the surprise may only pay when the voices reach it by small steps.

**Support.** Card 1 (surprise mostly lowers pleasure; uncertainty matters), card 2 (expected, small-step material is what others carry). The Listener's pair (style surprise of each chord, plus chord repetition) and their interaction. The Geometer's round-2 scalar (mean voice-leading step among the most surprising quarter of chord changes; no fitted parameters). The Skeptic rated this the best of the week. Wasserstein templates and "S as an angle" are dropped; the Geometer conceded both.

**Prediction.** (a) Chord repetition, beta -0.05 or stronger on covers within era (the replication on fresh songs). (b) Interaction: less repetition helps more when chord vocabulary is plain; beta 0.05 or more in that direction, and top-decile songs land in the plain-and-varied quadrant with AUC 0.6 or more. (c) Smaller voice-leading steps on surprising changes, beta -0.05 or stronger, with (a) and (b) held.

**Test that could fail.** McGill Billboard (about 740 songs, chord annotations with bass) joined to Discogs-VI and SHS100K cover counts. Drop any song already in the 2,360-song covers set. Freeze all measures before the join. Controls: year, chart peak and weeks, length, genre. **Fails:** for each term, if the 95% CI includes zero or the sign is reversed. The interaction also fails if repetition helps equally at every level of vocabulary plainness, or if the effect shows only in late covers. Cheung's frozen Table 1 index (card 1) can ride along at no cost, with the same rule.

**Decisions.** Fetch McGill Billboard. Face the power problem: with about 700 songs, a beta of 0.05 has only about 30% power. Either accept that the run is a lead, not a verdict, or wait for LargeSHS (arXiv 2511.15270) to become downloadable. Settle the voice-leading rule (pitch-class sets, minimal taxicab motion) before looking.

## 3. Measure the ceiling instead of guessing it (NEW)

**Idea.** If chance and social history decide much of who wins, no note measure can explain much of G, and earlier failures may partly reflect that limit. MusicLab ran eight parallel worlds of the same 48 songs, so the limit can be measured.

**Support.** Card 3. The Skeptic's ceiling ("a tenth of G at most", a guess); the Listener's round-2 demand to measure it; card 4's feedback loop.

**Prediction.** In Experiment 2 (strong social signal), independent-world appeal explains under half the variance of market share in a single social world (mean over eight worlds); in Experiment 1, under 0.7.

**Test that could fail.** MusicLab public data release (per-world downloads, listens, ratings). **Fails** if R² reaches 0.5 or more in Experiment 2. Then path dependence is small, and the "ceiling" excuse for weak note results is withdrawn. Optional notes leg: transcribe the 48 songs and test chord repetition against independent appeal (fails if |r| < 0.15 and tail AUC < 0.6). With n = 48, a pass is only a lead.

**Decisions.** Fetch the release. Ask Salganik about terms before publishing. Accept that first-session teen downloads are not decades of love: the number caps social success, not G, so it is a guide, not a bound.

## Not ranked
The folk-phrase test (card 2) measures faithful copying, not choosing to perform; it is shelved. The ListenBrainz repeat-listening outcome (Listener, round 2) is promising for the love half, but the joins are unproven. Revisit it after idea 1.

## The one check (prediction written into this file before running)

**Question.** In committed results, do G's two halves (love, covers) respond alike to the notes?

**Data.** Every notes-only measure in studies/shape/*/ results files that reports love and covers coefficients separately, with recording-feature files excluded. 61 entries (a duplicate S entry was removed).

**Prediction.** Spearman rho between love and covers coefficients below +0.30, with sign agreement of 60% or less.

**Disclosure.** I had seen the chord and S entries beforehand.

**Result: prediction failed.** Rho = +0.44, signs agree in 62% of entries, and among entries with a coefficient of 0.05 or more, 72% agree. **Honest reading:** both coefficients come from the same songs, and love and covers are correlated within those songs. That alone would produce agreement, so the check cannot show a shared note signal. I designed it poorly. It does show that the halves did not pull apart in past results. So the case for splitting G (idea 1) rests on time order, not on the halves disagreeing.
