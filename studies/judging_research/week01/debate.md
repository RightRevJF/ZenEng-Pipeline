# Week 01 debate

Three agents with fixed stances, given the four cards (card_1 to card_4), the repo's earlier findings, and the week 0 report (week 0 had no ranked ideas, so this is the first debate).

## Round 1

### The Geometer: greatness as a coupling of two spaces, not a feature of one

The repo measured the tune's shape in one space and asked whether a level (curvature, S nearer 1) tracks G. All failed. Persistent homology on McGill chords (Fourier space of pitch-class sets) added nothing beyond counting distinct chords. Lesson: a one-space shape collapses onto plain counts. The shape may live in how a song couples two spaces.

**Space 1, voice-leading geometry.** Each chord is a point in Tymoczko's orbifold: distance is the smallest total semitone motion of the voices, in a folded, non-Euclidean space. A progression is a path; its length is how far the harmony travels, the geometric form of the one replicated finding, "chords that move."

**Space 2, the expectation plane.** Each chord also gets uncertainty before it and surprise at it [card 1], from IDyOM with long- and short-term models.

**The point a song makes** is the cloud of its chord changes on the plane (voice-leading step, surprise). Hypothesis, "far but expected": great songs travel far while surprise stays low, spending surprises after predictable stretches. It squares three facts that look opposed: movement goes with covers; Cheung's largest term says surprise lowers pleasure; folk phrases survive when expected and built of small steps [card 2]. Far by small, predictable steps lets all three hold.

**Metric.** Songs are compared as distributions on that plane by Wasserstein (earth-mover) distance, a metric on shapes. Score = distance to a frozen early-cover-rich template minus distance to a good-hit template. Speculatively, S = 1 + g/pi: g is the angle of the cloud's main axis from the "surprise grows with step" diagonal, so g/pi is a fraction of a half-turn. Separate from the failed DFA reading.

**Cards 3 and 4.** Social luck caps any notes measure [card 3]; covers feed fame [card 4]. So target early covers (within five years) and the tails, not full ranking.

**What kills it.** (1) Cheap: on Meertens folk phrases, "far but expected" must predict survival beyond length, surprisal and interval size; dead if beta is under 0.05. (2) Main: templates built on Hooktheory/SHS100K, frozen, judged on Discogs-VI and McGill Billboard. Dead if beta on early covers is under +0.05 in either store, signs disagree, it adds nothing beyond chord repetition and distinct-chord count, or it correlates above 0.7 with either. The regions map passed twice, then died on a third set; this needs one.

### The Listener

Lasting love is a different thing from first-hearing pleasure. Cheung's surface [card 1] measures strangers hearing unfamiliar chord loops once. Over most of that surface, surprise *lowers* pleasure. The pleasing corner ("surprise after a predictable stretch") is small. On the tenth hearing a listener's memory knows the song, so moment-to-moment surprise mostly drains away. What can survive is *schematic* surprise: a move that still feels slightly off against the listener's general sense of pop harmony, even when they know exactly what comes next (Huron's schematic vs veridical expectation). Familiarity also wears out. A loop satiates fastest, and that matters most to the people who cover songs, because they play a song hundreds of times.

So I think the apparent tension is a split between two scales, not a contradiction. The folk result [card 2] says plain, expected, short material is what others carry faithfully, though weakly (about 5% of variance). The repo found that covers go with "chords that move" (less repetition within a section, replicated) and, more weakly, with *conventional* chord choices (chord surprise −0.03 on Discogs-VI, p .06; negative on every channel). In plain terms: musicians cover songs made of common moves that don't keep repeating themselves. Each step is expected. The path is varied.

**Proposed pair of measures (chords, from the notes):**
1. *Vocabulary plainness*: mean long-term information content of each chord. Information content (IC) is −log probability under a model trained on a separate corpus, so it is "surprise against the style". Low IC means conventional moves.
2. *Path variety*: the repo's within-section chord repetition, reversed, so high means the chords move.

**Prediction:** covers are highest in the "plain vocabulary, varied path" quadrant. The new claim is the interaction: the benefit of less repetition is larger among songs with low-IC vocabulary. Exotic *and* restless should not gain. Following [card 3], I expect this to show in the tails, not across the middle ranks. The test: are the top-decile covered songs over-represented in that quadrant (AUC > 0.6)?

**Data and safeguards:** Hooktheory chords joined to *early* covers only (within 5 years of release), so that fame feeding back into covers [card 4] doesn't produce the result. A fresh set is needed: both main effects were already found on SHS100K/Discogs-VI, so re-testing there is circular. LargeSHS, once published, or McGill Billboard joined to SecondHandSongs would do. Report a noise ceiling beside every result [card 3].

**Fails if:** the interaction's 95% CI includes zero, or path variety helps equally whatever the vocabulary, or the effect appears only in late covers.

**Honest status:** this is a reframing of two existing weak results, not new evidence. Notes have so far explained about 4% of covers. Even a pass would be a small effect, and nothing here touches love directly.

### The Skeptic

My test for every idea is simple. Would it pick out, on songs it has never seen, the ones people keep loving and other artists keep covering? Or does it only pick out what is popular, familiar or pleasing on first hearing?

**Card 1 (Cheung).** This is first-hearing pleasure. Strangers heard 30 synthetic chord loops, with no melody, no song rhythm and no repeat listens [card 1]. Lasting love is the opposite case. After years of listening, a song holds no surprises, so the paper's measure has nothing left to work on. We already tried a song-level version: it passed on SHS100K and then failed on Discogs-VI (+0.009). Verdict: a lab result, not a judge of songs.

**Card 2 (folk songs).** This measures how faithfully people copy a tune, not whether they choose to perform it. Plain, short, predictable phrases survive best [card 2]. That is memorability, and memorability is not the same thing as distinctiveness. It also runs against the one note result we have that repeated, "chords that move." And the song's tune family explained far more than the note features did (5% of the variance against 22% once family was added).

**Card 3 (MusicLab).** This is the main constraint. Once people can see what others chose, the winners depend partly on chance and history [card 3]. Knowing how appealing each song was cut the error in predicting success by only 16 to 38%. Card 4 adds a feedback loop: covers can send people back to the original, so the covers half of G partly causes the love half [card 4]. Card 4's evidence is weak, though: its counts do not add up, and about 44 of its hits would be expected by chance alone.

**Rough ceiling.** Path dependence probably takes half or more of G. Artist fame takes about 0.15. Recording, words and performance take part of what is left. That leaves a song-level note measure explaining at most about a tenth of G (r around 0.3). A realistic target is the 2 to 5% already seen. On that view, the failed tests of shape, S near 1, newness and the same-artist comparison are not surprising. Some of those failures come from the ceiling, not from bad ideas. But adding geometry does not raise the ceiling. More flexible representations just overfit: the codebook passed once, and then the frozen reader scored +0.008 on fresh songs.

**What would survive my scrutiny** is a narrow claim: one measure from the notes, fixed in advance, with a small effect, aimed at the tails rather than the full ranking. "Chords that move" is the model, since it repeated across two cover sources.

**A good test.** Card 4's early-cover design, made tougher:
1. Count only covers made within 5 years of release, before fame can feed back into covers.
2. Hold release year, genre and artist fixed.
3. Add the recording features, so the note measure cannot pass just by standing in for production.
4. Run it on two cover sources (SHS100K and Discogs-VI), and also check whether it separates the top and bottom songs (AUC of at least 0.6).

If the note measure keeps a beta of about −0.05 under all of that, it is real, though small. If it only holds on late covers, it was tracking fame, not the notes.

## Round 2

### The Geometer

**Concessions.** The Listener is right that "far but expected" and "plain vocabulary, varied path" are close to one claim. If voice-leading distance only re-measures repetition and chord IC, geometry adds nothing and the plainer pair wins. The Skeptic is right that my Wasserstein template was a flexible, fitted object, the same family as the codebook that scored +0.008 on fresh songs. I drop the templates, and I shelve the S-as-angle reading until a plain scalar passes.

**Pushback.** The repo's shape and persistent-homology failures had no fitted parameters, so overfitting did not kill them; redundancy and weak signal did. Voice-leading distance also has zero fitted parameters. Geometry does not raise the Skeptic's ceiling; it splits a term the plain pair lumps together.

**What geometry adds.** IC and voice-leading step come apart exactly where it matters. A chromatic mediant (C major to A-flat major) is surprising against the style yet reached by two semitone moves, one tone held; an expected chord can still be reached clumsily. The Listener's pair cannot tell those apart. My sharpened claim: surprise is tolerated, and covered, when it is *parsimonious*.

**One frozen scalar.** Among a song's top-quartile-IC chord changes, the mean voice-leading step (Tymoczko's taxicab distance). Predicted: smaller step, more early covers (within five years), beta at most −0.05.

**Kill.** On McGill Billboard joined to SecondHandSongs (fresh), holding year, genre, artist, recording features, and the Listener's two measures and their interaction: |beta| under 0.05, or the CI crosses zero, or it holds only on late covers.

### The Listener

**To the Geometer.** "Far but expected" is close to my idea but not the same. Voice-leading distance measures how far the voices travel. Repetition measures whether the path keeps coming back. A two-chord loop between distant chords (I to bVI) travels far but repeats, so it scores well on your measure and badly on mine. A varied path by small steps is the reverse. Those two kinds of song are where we can tell the ideas apart. You are right that pairing each change with its own surprise captures timing ("surprise after a predictable stretch") better than my song averages do. But Wasserstein distances to templates are flexible, and flexible readers have died on fresh songs before: the codebook passed once, then scored +0.008. So my two plain numbers, fixed in advance, should be the baseline your template has to beat.

**To the Skeptic.** I accept the ceiling as a rough guide. I add the recording features as a control, and I target tails and early covers. But "half or more" for path dependence is a guess. Card 3 shows how to measure the ceiling instead [card 3]. I push back on "nothing left to work on": schematic expectation outlasts knowing the song (a known deceptive cadence still lands). I admit the evidence for that on real songs over years is thin.

**What lasting love needs beyond covers** is resistance to satiation. The measure: the repeat-listening rate of each listener across years, from the open ListenBrainz dumps, joined to Hooktheory. Prediction: songs with plain vocabulary and a varied path keep a higher repeat rate per listener. This is untested, the joins lose songs, and it gives a second outcome that the covers loop cannot produce.

### The Skeptic

**Geometer.** The idea is clever, but it has many free settings: the IDyOM settings, the voice-leading model, which songs go into the two templates, and the Wasserstein distance itself. That is exactly how the codebook failed: it passed twice, then scored +0.008 on fresh songs. It is also probably not distinct from what already worked. Voice-leading path length is close to "less chord repetition" under another name. Requiring a correlation below 0.7 with chord repetition is too weak; I want the new measure's partial beta to hold with chord repetition in the model. Discogs-VI is not fresh either, because chords that move was found there. McGill Billboard is the only real test set. The folk-song test is cheap and worth running, but a pass there says the tune is easy to copy, not that musicians choose to cover it. Reading S = 1 + g/pi as an angle is unconstrained, so I would drop it. I do concede that the kill rules are explicit and that it aims at early covers and the tails.

**Listener.** This meets my bar best. It rests on two existing results, it is honest about being a reframing, it demands a fresh set, and the interaction is falsifiable. Two worries:
1. Testing an interaction needs far more songs than testing a main effect. With about 700 McGill songs it could easily come out null for lack of data.
2. Conventional chords track genre and era, and they also track how easy a song is to play. That would be playability, not greatness.

**Tests I'd accept.** For both proposals: freeze every measure and template before looking at McGill joined to SecondHandSongs; count early covers only (within 5 years of release); hold year, genre, artist and the recording features fixed; run a power check first; run the love half of G separately. A beta of at least 0.05 beyond chord repetition is a pass.
