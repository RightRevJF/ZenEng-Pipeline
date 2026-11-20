# The neuroscientist's contribution

## 1. Diagnosis

The tests asked what a model feels on the first hearing of the written tune. The yardstick asks what a person feels on the five-hundredth hearing of a recording. Those are different brains in different states. By the tenth hearing the listener's memory for the tune is close to perfect, so any surprise measured against "what note comes next" has been spent. What is left falls into three kinds, and none was in the tested measures:

- **Surprise that memory cannot switch off.** The brain runs two predictors at once: a memory of this song ("veridical") and a slow, general sense of how music goes ("schematic"), built over a lifetime and not updated by knowing the song. The second keeps being fooled even when the first knows what is coming. An n-gram model trained on the same hit corpus is neither of these.
- **Pleasure of anticipation.** In familiar music the reward moves from the event to the wait before it (Salimpoor's chills work used music people already knew by heart). What matters then is not how surprising a moment is, but whether the song has a few moments worth waiting for and a clear runway to them.
- **Detail that memory cannot store.** People remember a tune almost exactly and a timbre, a vocal grain, a micro-timing only roughly. So the tune wears out and the sound does not. That is the simplest reading of the central result: everything on the page failed, everything that held is in the recording.

Two further faults. First, most tests looked for "more is better", while the psychology of liking is full of inverted U's (too simple bores, too complex repels) and interactions (surprise is pleasant only when the listener was confident; syncopation moves the body only when the beat is firm). A rank correlation on a single measure sees none of that. Second, the yardstick mixes two things with opposite logic: "covered by many" says the page carries the value, "still loved" may be about one recording. They should be predicted separately.

Read together, the held findings describe one scene: a slow, sparse, low, not-cheerful sound with open space. That is the acoustic signature of one voice heard close, and of a mix with room for something to enter. I take that as the lead.

## 2. Ideas, most promising first

### Idea 1. Measure the wear-out curve directly (a sharper yardstick)

**Plain words.** "Still loved long after" is a crowd-level proxy for a per-person fact: this listener has not tired of this song. Measure that fact. For each song, take individual listening histories and ask how many of the people who played it five times went on to play it fifty, and two hundred. A song that is loved on the five-hundredth hearing has a flat wear-out curve; a merely good hit has a steep one. This separates durability from popularity, fame, radio rotation and the performer's career, which the present yardstick cannot.

**Mathematics.** For song s and user u let n(u,s) be total plays. Define the survival function S_s(k) = P(n ≥ k | n ≥ 5). Fit a discrete power law or stretched exponential tail; the score is the tail exponent (shallower = more durable), or simply D_s = log S_s(50) − mean of log S(50) over songs of the same year and genre. A second score: the median gap in days between a user's first and last play, corrected for how long the user is observed. A third: within-user rank stability, the probability a song in a user's top 100 one year is still there three years later.

**Data.** Not here. Candidates: Music Listening Histories Dataset (MLHD, about 27 billion Last.fm plays, 583k users); the Last.fm 1K-users dataset (full timestamped histories, about 19 million plays, small but enough for famous hits); ListenBrainz public dumps; the Spotify Sequential Skip Prediction set (skips within sessions, no long histories). Some of these have Zenodo or GitHub mirrors; that needs checking, I have not verified which are reachable from here.

**Proved wrong if.** The wear-out score is just popularity in disguise (correlation above 0.8 with total plays after the conditioning), or it does not correlate with the present yardstick at all (then one of the two is not measuring love).

**Odds.** 60% that it can be built for at least 1,000 graded songs and gives a cleaner target; 35% that the recording measures that held grow noticeably stronger against it.

### Idea 2. Arrival architecture: few peaks, long runways, something entering

**Plain words.** The measured triggers of chills are remarkably consistent across labs: a new voice or instrument entering, a sudden widening of loudness or register, a solo line emerging from a thin background, a harmonic turn after a long hold. All need emptiness beforehand, which is why sparse recordings can do it and a dense bright wall cannot. In a well-known song the pleasure is waiting for those arrivals. So a great song should have a small number of large arrivals, each preceded by a stretch where the listener can see it coming.

**Mathematics.** From the multi-track MIDI build three curves in one-bar steps: A(t) = number of sounding tracks; R(t) = pitch span in semitones between lowest and highest sounding note; L(t) = sum of note velocities (or note count where velocities are flat). Standardise each within song and take the first principal component, I(t), the "fullness" curve.
- Arrival events: bars where ΔI(t) = I(t) − mean(I(t−4..t−1)) exceeds 1.5 within-song standard deviations.
- Concentration: Gini coefficient of positive ΔI over the song (high = a few big arrivals rather than constant churn).
- Runway: for each arrival, the number of preceding bars in which I stayed below its song median, or rose monotonically. Score = sum over arrivals of ΔI × log(1 + runway).
- Headroom: I at the 95th percentile minus I at the 10th.
- Timing: position of the largest arrival as a fraction of song length (prediction: best around 0.55 to 0.8; test as an inverted U, not a slope).

**Data.** The 1,400 graded Lakh arrangements; have it. A coarse check on Essentia whole-recording numbers (dynamic complexity, loudness range if present).

**Proved wrong if.** Concentration, runway score and headroom all sit within ±0.03 of zero on the hold-out, or runway adds nothing over headroom alone.

**Odds.** 30%. It is the one idea here that explains why sparseness helps instead of merely restating it.

### Idea 3. Better than remembered: the part of the song memory cannot keep

**Plain words.** A reward signal fires when what arrives beats what was expected. On the five-hundredth hearing the expectation is the listener's memory of the song, and memory is a lossy copy pulled toward the average song. If the real thing is reliably richer than the remembered copy, every hearing delivers a small "better than I recalled", forever. So measure how much of a recording lies outside what a listener can carry in the head, which is roughly the tune, the words, the chords and the beat.

**Mathematics.** Let M be the memorable skeleton (melody plus chord sequence plus tempo) and X the full arrangement. Estimate the conditional information H(X | M): train one model on the 17,000 ungraded arrangements to predict each accompaniment track's notes (pitch class, octave, onset position in the bar, duration) given the melody and chords in that bar, and score each graded song by mean negative log-probability per bar of its actual arrangement. High = the arrangement says things the lead sheet does not imply. Refine by counting only what recurs within the song (bits that are unpredictable from the skeleton but repeated in the song are designed detail; bits that never recur are noise): score = H(X | M) − H(X | M, earlier bars of the same song). A recording-level stand-in from Essentia: the variance over time of timbre descriptors (MFCC variance, spectral flux variance, dynamic complexity) after regressing out tempo and event rate.

**Data.** Arrangements: have. Note Lakh files are mostly sequenced and quantised, so micro-timing and voice grain, likely the largest part of the effect, are absent; a real test needs audio or stems (MUSDB18, MedleyDB, and the Million Song Dataset timbre segments on mirrors, none graded in bulk).

**Proved wrong if.** Arrangement information given the skeleton is unrelated to the yardstick, or relates only through track count.

**Odds.** 25% on MIDI; I would put 45% on it with real audio.

### Idea 4. The voice against the grid: surprise across streams, weighted by certainty

**Plain words.** The tested measures asked how surprising each note is given the notes before it in the same line. The body does something else: it locks onto the band's pulse and harmony, and hears the voice as arriving early, late, or on a note that leans against the chord. That push and pull is felt only when the grid is firm; syncopation over a vague beat is just mess. This is the documented inverted U for groove, and it is an interaction between two streams, invisible in either alone and invisible on a lead sheet.

**Mathematics.** From multi-track MIDI:
- Grid certainty P: one minus the normalised entropy of drum and bass onsets over the 16 positions of the bar (1 = perfectly regular).
- Voice displacement V: mean metrical weight deficit of melody onsets (standard syncopation index), plus the share of melody notes that anticipate or delay the chord change, i.e. the melody reaches a tone of the next chord before the chord arrives, or holds a tone of the old chord after it.
- Lean: share of melody duration on non-chord tones that resolve by step within a beat (the appoggiatura, a known chills trigger), counted only on strong beats.
- Score: the product P × V, and a quadratic fit grade ~ V + V² within terciles of P. Prediction: positive effect of V only in the top tercile of P, turning down at the extreme.

**Data.** Have (Lakh graded). A weaker version is possible on Hooktheory, using chord change positions as the grid.

**Proved wrong if.** No interaction: V relates to the yardstick equally (that is, not at all) at every level of P, and the quadratic term is null.

**Odds.** 20%.

### Idea 5. Hindsight: surprising going forward, inevitable looking back

**Plain words.** Huron's account of musical pleasure is a fast alarm followed by a slower "that was fine, in fact that was right". A surprise that later context explains is the kind a listener can keep loving, because knowing the song deepens the explanation without removing the jolt in the fast system. A surprise never explained is a wrong note, and wears badly. Forward-only models measure the jolt and cannot tell the two apart.

**Mathematics.** Train two models on the ungraded tunes (and chords): a forward model giving IC_f(t) = −log p(x_t | past), and a two-sided model (masked prediction with context on both sides, same order or a small transformer) giving IC_b(t) = −log p(x_t | past and future). Hindsight gain G(t) = IC_f(t) − IC_b(t). Scores: mean of G over the top decile of IC_f (how well the song's biggest surprises are redeemed); count of events with IC_f in the top 10% and IC_b in the bottom 50%; and the ratio of that count to events with both high (unredeemed surprises), which should count against. Also compute at the level of bars and phrases (tokens = bar-level contour and chord), since the redeeming context is often a whole answering phrase.

**Data.** Have: note lists and Hooktheory, with 20,000 ungraded songs for training.

**Proved wrong if.** The redeemed-to-unredeemed ratio is null on the hold-out at note, bar and phrase level.

**Odds.** 15%. It is still a page measure, and the page has a poor record; it is the best-motivated repair of the surprise idea.

### Idea 6. Deep prior against fashion prior

**Plain words.** The listener's general sense of music is laid down early, from nursery songs, hymns, folk tunes and whatever was in the house, and changes little afterwards. The hit parade of a given year is a thin recent layer on top. A song that fits the deep layer while standing apart from its year would feel as if it had always existed and yet sound like nothing on the radio. The second half already held on recordings ("unlike other hits of its own years"); the first half has never been tested, because the models were trained on hits.

**Mathematics.** Train model D on the hymn and folk tune collections (pitch interval plus duration ratio tokens, key and tempo normalised) and model F_y on hits from the ten years before year y. For each song compute per-note log-likelihoods LL_D and LL_F. Score = LL_D − LL_F (the log-likelihood ratio), and separately test the 2×2 design: high LL_D with low LL_F should outrank the other three cells. Repeat with chords using jazz standards and hymns as the deep corpus.

**Data.** Have all of it.

**Proved wrong if.** The high-deep, low-fashion cell does not outrank the others, or LL_D alone carries any effect (then it is just simplicity).

**Odds.** 15%.

### Idea 7. The uncertainty-times-surprise surface, done as published

**Plain words.** Cheung and Koelsch found chord pleasure is not about surprise but about its combination with how sure the listener was beforehand: best when sure and then surprised, or unsure and then given what was most likely. Mean surprise and local surprise both discard the "how sure" half. If the tested measures did so, the idea was never tested.

**Mathematics.** For each chord (then each melody note) compute pre-event entropy H(t) = −Σ p log p over the model's predictive distribution, and surprise IC(t). Standardise both across the corpus. Score 1: −mean of z(H)·z(IC) per song (the negative interaction). Score 2: share of events in the two favoured quadrants (H low and IC high; H high and IC low) minus share in the other two. Score 3: the same, counting only events on phrase boundaries and section starts, where expectations are consulted most. Use a variable-order model with both a corpus-trained and a within-song component, as the original study did.

**Data.** Have: Hooktheory chords, 900 graded, 20,000 for training.

**Proved wrong if.** All three scores are null on the hold-out.

**Odds.** 12%. Cheap, and it closes the question properly.

### A note on method that applies to every idea
Retest the failed page measures in three forms the brain's known curves call for: as distance from the era's norm in any direction (the form in which the one recording result held), with a squared term, and as products of pairs the literature says interact (certainty with surprise, beat firmness with syncopation, sparseness with arrival size). And predict the two halves of the yardstick apart: cover count given love, love given cover count. My expectation is that page measures, if they ever speak, will speak to covers, and recording measures to love.

## 3. The wild idea: the song that breathes at the body's own slow rhythm

The cardiovascular system has a resonance near 0.1 Hz, one cycle every ten seconds: blood pressure and heart rate swing together at that rate, and breathing at six breaths a minute drives it hardest. Bernardi's group showed that sung or recited phrases about ten seconds long (the Ave Maria, some opera arias) pull breathing and heart rhythm into that resonance and raise heart-rate variability, which people feel as calm and fullness. A listener who sings along, or merely breathes with the singer, is being paced by the phrase length. So the conjecture: great songs have vocal phrases whose sing-and-breathe cycle sits near ten seconds, so that each hearing does something to the body that no amount of familiarity dulls, because it is physiology, not prediction. It would also explain "fewer events per second" and "slow, sparse".

Computable now: from the note lists and tempo, mark phrase boundaries at rests longer than a set fraction of a beat (or longer than 0.4 s), take the distribution of phrase-onset-to-phrase-onset times in seconds, and score each song by the share of phrase cycles between 8 and 12 seconds, or by the spectral power of the vocal on/off envelope at 0.08 to 0.12 Hz relative to total. Test as a peak, not a slope: songs at 5 s and at 20 s should both score below songs at 10 s. Wrong if the curve is flat or monotone. Odds perhaps 8%, and I would still run it first thing in the morning.
