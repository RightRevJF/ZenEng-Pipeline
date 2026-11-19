# Round two: the neuroscientist replies

## 1. The two strongest ideas from the others

**A. The hymn laboratory with tunes and texts crossed (sceptic 1; also songwriter 2, evolutionist 2).**
It is the only design in the room that removes the recording, the star, the chart luck and the words at once, and it yields a tune score with full range instead of a thin slice of survivors.

What my field adds:
- A hymn is not listened to, it is sung, weekly, for a lifetime, by untrained people. That makes it the wear-out curve in the wild with the body included: the closest thing we have to "still loved on the five-hundredth hearing".
- It is the right place to test the things a listening model cannot see: phrase length against the breath (my ten-second conjecture), and the songwriter's open vowels on long high notes.

What it corrects:
- Hymnal counts grade what a congregation can produce in unison (narrow range, steps, regular phrases), which is a motor filter. A page measure that works there has shown it predicts singability under group constraints, and may not carry to songs loved by listening. Expect the hymn result to transfer to the "covered" half of the hit yardstick and not to the "loved" half; say so in advance.
- Hymn tunes are also the material many listeners' general sense of music was built from. So "probable under a hymn model" (my idea 6, the mathematician's wild idea, the evolutionist's idea 5) is partly circular in that repertoire. Train the prior on folk tunes when grading hymns, and the reverse.
- Test every measure there as a peak as well as a slope. The liking curves are inverted U's and the hymn data has the range to show one.

**B. The stiff core and the free shell, measured on real versions (physicist 1, evolutionist 3, sceptic's wild idea).**
Three people reached it independently, and it turns "robustness" from one number into a shape.

What my field adds:
- It is a description of auditory memory. People keep contour, rhythm ratios and the placement of a few anchor notes almost exactly, and keep timbre, voicing and micro-timing only roughly. The core is what memory holds; the shell is what it cannot. My "better than remembered" idea is the same object seen from the listener's side: the shell is where each hearing can still exceed the memory.
- So the core should be predictable from memory salience, not just from covers: notes that are long, metrically strong, at contour turning points, repeated, and heard in the clear.

What it corrects:
- Conservation will look two-peaked in every song for a dull reason: strong-beat notes are kept and passing notes are not. The grading quantity must be conservation beyond what metrical position and duration predict.
- Covers of a famous original are constrained by the audience's memory of it, so fame alone stiffens the core. Match on the original's popularity as well as on number of versions.
- Fan MIDI versions of one song are often copies of one another. Check independence before treating them as separate draws.

## 2. The weakest idea in the room

**Irreversibility and entropy production on the page** (physicist 5, mathematician 6: proposed twice, so it risks being run).

It will fail for three exact reasons:
1. Estimation. A 20-state chain has 400 transition cells; a tune supplies a few hundred transitions. The entropy-production estimate is then dominated by positive bias of order (cells / transitions), and that bias falls with song length and with repetition. The measure will mostly re-read length and repetition, both already tested and null. Shuffled-phrase z-scores do not cure it, since shuffling phrases preserves almost all within-phrase transitions.
2. Universality, by the physicist's own argument. All tonal music is irreversible in the same way (dominant goes to tonic, leaps recover by step). It marks membership of the class and cannot rank members.
3. Perception. Listeners do not carry transition tables; they carry events at particular places. The songwriter's point stands: averages over the whole song were the failed family, and this is another average.

In fairness, my own idea 7 (uncertainty times surprise) is second weakest, and by my own diagnosis: it is a first-hearing measure, the published effect was on bare chord sequences rated moment by moment, and averaged over a song against a forty-year social outcome it has little chance. I would run it only because it is nearly free.

## 3. A new idea that exists only because the papers are read together: the exposed core

Sources: the evolutionist's per-note conservation, the producer's vocal exposure, the songwriter's appointment, my memory account.

**Claim.** A culture's memory of a song is built from what individual ears could encode. The ear encodes what is unmasked, isolated in time, long and metrically strong. So the notes every later version keeps should be the notes the original arrangement left in the clear, and a great song is one whose identity sits exactly where the ear can take it, with its freedom placed where the band is busy or the voice rests.

**Causal chain, each link testable:** exposure in the original → encoding → conservation across versions → covers and lasting love.

**Mathematics.**
- For each original note i: conservation c_i (evolutionist 3), exposure x_i = lane clearance at that note (producer 1: no accompaniment note within 4 semitones while it sounds, plus no accompaniment onset in the same sixteenth slot), and appointment a_i (songwriter 3).
- Link test, needs no yardstick: within each song, logistic regression of c_i on x_i, controlling duration, metrical weight and repetition count. Pooled over hundreds of songs and tens of thousands of notes, so power is enormous and chart luck is irrelevant.
- Song-level score: E_s = partial correlation of c_i with x_i within the song, compared with a baseline where the accompaniment is shifted against the melody by random whole bars (the songwriter's shuffle). Where versions are lacking, replace c_i by the evolutionist's predicted conservation.
- Mirror score: across versions, the share of arrangement variance falling in vocal rests (the producer's "hole") against that falling under the voice.

**Data.** In hand: Lakh songs with several arrangements, the three transcription sources.

**Wrong if** exposure does not predict which notes are conserved once duration and metre are controlled, or E_s is flat across grades within year bands.

**Odds.** 55% for the note-level link; 25% that E_s grades songs.

## 4. Votes

**First test with data in hand:** the sceptic's idea 2, same work in different charting records, intraclass correlation of later love. It needs no musical feature, takes days, and tells us whether love follows the work or the record, which decides where everyone else should look. (Run the year-and-tempo stratified recheck of the sparse-spectrum finding alongside; if that result is a dating effect, half the room's ideas lose their footing.)

**First test needing new data:** the crossed hymn tune-by-text table from Hymnary, with the caveat above that it grades singing, so its transfer to the "loved" half must be predicted in advance. My own per-listener wear-out curve is my second choice; it is the right target for hits, but I have not verified that the listening histories are reachable.

## 5. Where the room is converging, and whether I believe it

**The theory:** a great song fixes a few things rigidly and memorably, sets them in the clear, and leaves a large open space that every performer and listener fills differently.

**Do I believe it?** About 40%. I believe it as an account of why songs are covered. I am not persuaded it explains why one person does not tire of one record, which needs something positive in the shell (detail memory cannot hold, and arrivals worth waiting for), not merely room. And the agreement is weaker than it looks: seven people have read one unstratified +0.25 result seven ways, which is one piece of evidence, not seven.
