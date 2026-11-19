# Producer / mixing engineer / psychoacoustician

## 1. Diagnosis

Every test on the page failed for a reason any session player would give you: among hits, the tune and chords have already been filtered. A song does not reach the Hot 100 with a weak tune, so the written-song variance that is left is small and mostly noise (range restriction). What still varies enormously between two hits is the *record*: who plays, how many play, where each part sits, and how much of the singer you can actually hear. The four surviving findings are, to my ear, four shadows of one object. "Concentrated spectrum" means few sound sources, each owning its own band, with the bright wash (cymbals, strings pads, stacked guitars, synth sheen) absent. "Few events per second" means nobody is doubling anybody and nobody is filling space for its own sake. "Unlike its years" means the record has a signature a listener identifies inside a second. "Less cheerful" means the record does not need to sell itself with brightness and bounce. The object casting these shadows is **figure and ground**: one human voice standing clear as the figure, and a ground made of a few parts that each do one job and otherwise stay out of the way. An exposed voice cannot hide, so the performance has to be true, and a sparse record also leaves the song itself *legible*, which is exactly what another artist needs before covering it. That last point matters: half the yardstick is cover count, and a record that shows the song's bones invites covers.

Two warnings before anyone gets excited. (a) A low, band-limited, sparse spectrum is also simply what a 1950s-60s tape recording and a slow ballad look like, and older songs and ballads have had more time and more reason to be covered. Every test below must be run inside narrow strata of release year (5 years or less) and tempo, or it will rediscover "old slow songs". (b) Our multi-track MIDI files are fan-made sequences, not the session. Their fidelity varies, so step zero is a calibration gate.

**Step zero, the gate.** For songs having both a MIDI arrangement and Essentia numbers, compute from the MIDI the predicted band-energy spread and the predicted onset rate (formulas in idea 1 and 2) and correlate them with Essentia's measured spectral numbers and onset rate. Also, Lakh contains several different MIDI versions of many songs: compute every feature below on each version and report the agreement across versions (intraclass correlation). If MIDI-predicted sparseness correlates below about 0.3 with measured sparseness, or versions of one song disagree, the MIDI stand-in is not good enough and ideas 1-5 need audio.

## 2. Ideas, most promising first

### Idea 1. Vocal exposure: how much of the voice the ear actually gets

**Plain words.** The ear analyses sound in "critical bands" (frequency slots, roughly a third of an octave wide above 500 Hz, within which a louder sound hides a quieter one; this hiding is "masking"). A voice is exposed when, in the bands where it has energy, nothing else is competing. My claim is that the concentrated spectrum is a by-product of arrangements that clear the voice's bands. Measure the clearing directly rather than the by-product.

**Mathematics (from MIDI).**
- Identify the vocal track: track name contains melody/vocal/lead, else the track whose note sequence best matches the tune we already hold for that song (best alignment score), else the most monophonic mid-range track.
- Give every note a crude spectrum. Note with MIDI pitch p, velocity v: fundamental f0 = 440 * 2^((p-69)/12); partials at k*f0 for k = 1..10 with amplitude a_k = (v/127) * k^(-rho), rho set by instrument family (bass 1.5, piano 1.2, clean guitar and voice 1.0, strings 0.8, brass 0.7, distorted guitar 0.5). Plucked or struck notes decay as exp(-(t - onset)/0.4 s); sustained ones stay flat. Drums get fixed band templates (kick 40-100 Hz, snare 150-250 Hz plus 2-8 kHz, hi-hat and cymbals 6-12 kHz).
- Map frequency to band number with the ERB scale: E(f) = 21.4 * log10(4.37*f/1000 + 1), rounded to integer bands b.
- In 50 ms frames t, let V_b(t) be vocal energy (sum of a_k^2 in band b) and A_b(t) the energy of everything else.
- Spread the maskers across neighbouring bands: M_b(t) = sum over b' of A_b'(t) * 10^(-S(b - b')/10), with S(d) = 10*d dB when the masker lies below the target band (d > 0, masking spreads strongly upward) and S(d) = 25*|d| dB when it lies above.
- Exposure at frame t: X(t) = sum_b [V_b / sum_b V_b] * [V_b / (V_b + M_b)]. It is 1 when the voice is alone and tends to 0 when it is buried.
- Song features: mean X over vocal frames; the fraction of vocal frames with X > 0.5; X at phrase ends (last 25% of each phrase), where long notes hang in the air.
- A velocity-free version, because MIDI velocities are unreliable: **lane clearance** = 1 - (fraction of vocal frames during which any non-bass accompaniment note sounds within +/- 4 semitones of the sung pitch).

**Data.** Multi-track MIDI for ~1,400 graded songs: we have it. True version needs audio (separate the vocal with Demucs, then the same formula on real band energies).

**Proved wrong if** exposure and lane clearance show no relation to the yardstick within year and tempo strata, or if they add nothing once total track count is controlled (then it is just "fewer instruments", not "room for the voice").

**Odds.** 35% from MIDI; 55% if we had audio.

### Idea 2. One player per event: redundancy and interlock

**Plain words.** "Fewer events per second" could mean a lazy record or a disciplined one. In a Motown or Muscle Shoals rhythm section the combined rhythm is complete, yet each musician plays little, because nobody doubles anybody: the bass fills the hole the kick leaves, the guitar chops only on the backbeat, the tambourine owns the top. A dense wall is the opposite: five parts hitting the same slots. Measure doubling, not just count.

**Mathematics.** Quantise onsets to a sixteenth-note grid. For each track i, S_i = set of slots where it starts a note.
- Union events U = |union of S_i|; total events T = sum_i |S_i|.
- **Redundancy** R = T / U (1.0 means every event is played by exactly one part). Compute per bar, take the median.
- **Interlock.** For each pair of tracks compute the phi coefficient (ordinary correlation of two yes/no series) of their slot-occupancy vectors, excluding beat 1 of each bar. Interlock I = minus the mean phi over pairs. Positive I means parts avoid each other's slots.
- **Pitch doubling** P = fraction of sounding time during which two non-bass tracks hold the same pitch in the same octave.
- **Registral lanes.** For each track, p_i = its distribution of sounding time over pitch. Overlap of two tracks = sum over pitch of sqrt(p_i * p_j) (1 = same register, 0 = disjoint). Lane separation L = 1 - energy-weighted mean overlap across pairs.
- **Effective number of parts** N_eff(t) = exp(-sum_i s_i ln s_i), where s_i is track i's share of sounding notes in bar t. This is the count of parts that actually matter, not the count on the track sheet.

**Data.** MIDI: we have it. No audio needed for a first test.

**Proved wrong if** great hits are sparse in U but no lower in R, P, or overlap than good hits: then sparseness is plain emptiness and my "discipline" reading is wrong.

**Odds.** 35%.

### Idea 3. The shape of the build: density arc and drop-outs

**Plain words.** A record that averages sparse may do so because it only goes full where it counts. Producers think in layers over time: start nearly bare, add one thing per section, pull everything out before the last chorus. The page-level "section contrast" test failed, but that measured the tune; this measures how many players are in the room bar by bar. The mean hides this; the trajectory shows it.

**Mathematics.** Per bar t = 1..B: n(t) = number of tracks sounding; d(t) = union onsets per second; N_eff(t) from idea 2.
- Contrast: Q90(d) / Q10(d), and max n - min n over bars containing vocal.
- **Drop-outs:** count of bars where n(t) <= mean(n(t-4..t-1)) - 2 and t > B/4. Also record whether the voice continues through the drop (voice left alone is the most exposed moment in a record).
- **Build position:** c = sum_t t*d(t) / (B * sum_t d(t)); c > 0.5 means density arrives late.
- **Entry stagger:** number of bars until 80% of all tracks have made their first entrance.
- **Opening bareness:** mean n(t) over the first 4 bars, and over the first verse.
- **Does the band lift the singer or crowd the singer?** Correlation over bars between d(t) of the accompaniment and the mean sung pitch in that bar.

**Data.** MIDI: we have it. A cross-check exists in the Essentia set if it includes loudness range or dynamic complexity (two standard Essentia outputs).

**Proved wrong if** arc features carry nothing beyond mean density in the same strata.

**Odds.** 30%.

### Idea 4. Answering the voice: what happens in the silences

**Plain words.** Great arrangements treat the vocal phrase and the gap after it as two different spaces. During the phrase the band holds still; in the gap one instrument answers (the guitar lick, the horn stab, the piano fill) or nothing does and the silence is left to ring. Poor arrangements play the same pattern through both. This is the relationship between voice and band the crude event count cannot see.

**Mathematics.** v(t) = 1 if the voice sounds in sixteenth-slot t, else 0. Fill tracks F = everything except voice, bass and drums. d_F(t) = onsets in F at slot t.
- **Complementarity** g = correlation of v(t) with d_F(t) over the song. Negative means the band plays in the gaps.
- **Answer ratio** AR = [mean d_F in the 2 beats after each phrase end] / [mean d_F during phrases]. A phrase end is a vocal rest of at least one beat.
- **Single answerer:** in each gap, the share of fill onsets coming from the busiest fill track, averaged over gaps (1 = one voice answers; low = everyone piles in).
- **Breath:** fraction of song time the voice is silent, and the mean and variance of gap lengths in beats.
- **Air:** fraction of sixteenth slots with no onset in any track; and fraction of time with the voice silent and N_eff <= 2.
- **Rhythm-section steadiness under the voice:** bar-to-bar change in bass and drum patterns (Hamming distance between consecutive bars' slot vectors, divided by slots) during vocal bars versus non-vocal bars. A good section changes less while the singer sings.

**Data.** MIDI: we have it.

**Proved wrong if** g, AR and single-answerer are unrelated to the yardstick, or if busy-through-the-vocal arrangements grade as well as answering ones.

**Odds.** 25%.

### Idea 5. The signature: an arrangement unlike its year, and one part that carries it

**Plain words.** Recording-level unlikeness held (+0.09) while tune-level unlikeness scored zero. On most enduring records the unlikeness lives in one identifiable thing: a bass line, a guitar figure, a drum pattern, an odd instrument, stated almost alone at the top. I would test whether unlikeness is concentrated in one part and announced in the intro.

**Mathematics.**
- Arrangement vector a = (features from ideas 1-4, share of sounding time per instrument family, register centre of each role, onset rate of each role). Standardise within the cohort of hits released within +/- 2 years. **Unlikeness** D = mean Euclidean distance from the song to its 20 nearest cohort neighbours. Report D for the whole vector and separately for each role's sub-vector, to see which role is the odd one.
- **Riff concentration.** For each non-vocal track, cut it into 1-bar and 2-bar windows, code each window as (rhythm slots, pitch intervals) so transposition does not matter, and find the most repeated code. q_i = bars occupied by that code / bars the track plays.
- **Riff rarity.** r_i = 1 - (fraction of the ~17,000 ungraded MIDI songs in which the same code appears in any track). The ungraded pile is the background of what everybody plays.
- **Signature strength** Sig = max over tracks of q_i * r_i. **Announced** = 1 if that track sounds in the first 4 bars with n(t) <= 2.
- **First-seconds test:** recompute D using only the first 4 bars of each song. If the opening alone carries the unlikeness, the record has a calling card.

**Data.** MIDI graded and ungraded: we have it. The audio version (timbre unlike its year, first five seconds only) needs raw audio or frame-level features.

**Proved wrong if** D in arrangement space is unrelated to the yardstick, or if unlikeness spread evenly across parts does as well as unlikeness concentrated in one.

**Odds.** 30% for D (it mirrors a finding that already held); 20% for the concentration claim.

### Idea 6. Split the yardstick: is the sparse record loved, or merely legible?

**Plain words.** The yardstick mixes two things: people still play the record, and musicians remake the song. My practitioner's reading predicts something specific: sparseness should predict *covers* more strongly than *lasting play*, because a bare record hands the next artist a song with room left in it, while a dense, finished production leaves nothing to add and little to see. If instead sparseness predicts lasting play just as well, then the space around the voice is doing its work on listeners, which is the stronger and more interesting result. No new data is needed and either answer redirects the whole project.

**Mathematics.** y_cov = log(1 + number of covers), residualised on release year. y_play = present-day popularity, residualised on release year and peak chart position. Compute the rank correlation of each sparseness measure (Essentia spectral concentration, onset rate, and MIDI R, X, N_eff) with y_cov and with y_play separately; test the difference with a bootstrap over songs. Add **cover spread**: the entropy H = -sum_g p_g ln p_g of genres among the cover performers (genre attached from our genre table by performer name where possible); a song that travels across genres has survived being stripped and rebuilt.

**Data.** We have all of it (cover lists with performers, Essentia, Spotify, genres).

**Proved wrong if** sparseness predicts lasting play but not covers.

**Odds.** 45% that covers carry more of the sparseness effect than lasting play does.

### Idea 7. The truth of the performance (needs raw audio)

**Plain words.** Exposure matters only because of what it exposes. A vocal sounds true when pitch and timing move with the meaning: scooping into a note, vibrato arriving late on a held note rather than being switched on throughout, lines laid behind the beat in the verse and pushed in the chorus, a band whose tempo breathes together. None of this is in a MIDI sequence, where timing is often snapped to a grid and velocities are arbitrary. Of everything here it is the thing I would bet on most and can test least.

**Mathematics (audio).** Separate the vocal (Demucs). Track pitch f0(t) with pYIN or CREPE; track beats with a beat tracker.
- **Vocal level:** 10*log10(E_vocal / E_rest), overall and in the 1-4 kHz band where the ear is most sensitive.
- **Scoop:** for each note, 1200*log2(f0 at onset / median f0 of the note's settled middle), in cents (hundredths of a semitone); mean and spread.
- **Vibrato:** energy of f0 fluctuation in the 4-8 Hz band; extent in cents; **delay** = time from note onset to vibrato onset divided by note length.
- **Pitch freedom:** standard deviation of f0 around the nearest semitone during settled portions (tuned-flat singing scores near 0).
- **Lay-back:** vocal note onset minus nearest sixteenth of the tracked beat, in ms; signed mean and standard deviation, by section; and the verse-to-chorus change.
- **Band breathing:** inter-beat intervals IBI_k; tempo drift = slope and spread of the tempo curve; and the fluctuation exponent alpha from detrended fluctuation analysis of the IBI deviations. Published work on human drumming (Hennig and colleagues, 2011) found long-memory fluctuations (alpha between 0.5 and 1) and that listeners preferred them to random jitter; click-track and quantised records give alpha near 0.5 or no fluctuation at all. This is where the owner's 1/f belongs: the written tune sat near the critical point for every song and graded none of them, but the *playing* may differ between records in a way the page cannot.
- **Dynamic arc:** loudness range (EBU R128 LRA), crest factor (peak over average level), and the short-term loudness curve's build position as in idea 3.

**What can be done without audio.** Check the 127 Essentia numbers for: dynamic complexity, loudness range, the spread of the first tempo-histogram peak (a steadiness proxy), and "danceability", which in Essentia is itself computed from a detrended fluctuation exponent of the loudness envelope. That last one is a ready-made scaling measure on the recording that may already be sitting in the table.

**Where audio might come from.** We have none. The cheapest powerful design is small: because 85% of the variation is between songs by the same artist, take about 100 matched pairs (same artist, within three years, one great and one merely good hit) from recordings the owner lawfully owns, and run the measures above. Time-resolved Echo Nest features (per-event loudness, timbre and pitch vectors) exist for the Million Song Dataset and are linked to the Lakh "matched" MIDI subset; I am not certain a copy sits on GitHub or Zenodo, so that needs checking before it is counted on.

**Proved wrong if** in matched pairs the great hit shows no more scoop variety, vibrato delay, lay-back or timing memory than its sibling.

**Odds.** 40%, untestable today.

## What an arrangement engine should do differently if these findings are true

For an engine writing voice, guitar, bass, harmony vocals and drums, each rule below is one of the measures turned into a constraint.

1. **Clear the voice's lane.** While the voice sustains, no guitar or harmony note within +/- 4 semitones of the sung pitch. Voice the guitar below the melody or well above it; use two- and three-note voicings, and do not double the bass's root.
2. **One player per event.** Hold redundancy R at or below about 1.3 in verses. If two parts land on the same slot away from beat 1, delete one.
3. **The mute test.** For each part compute what the arrangement loses without it: change in union onsets U, in harmonic completeness (are root, third and seventh still stated somewhere), and in vocal exposure X. A part whose removal changes none of these is deleted. This is how a producer works: mute it, and if nobody misses it, it goes.
4. **Hold still under the phrase, answer in the gap.** Fills only where the voice rests for a beat or more, from one instrument at a time, and not in every gap. Leave some silences empty.
5. **One signature figure.** Give one instrument a repeated one- or two-bar figure that the engine checks is rare against its own corpus, and state it alone or nearly alone in the intro.
6. **Plan the layers.** Open with at most two parts. Change the layer count by one per section. Put peak density past the 60% point. Schedule one drop-out, ideally leaving the voice alone, before the final chorus.
7. **Harmony vocals are an event, not a texture.** Choruses and phrase ends only, so that their entrance is heard.
8. **Leave the top open.** Keep hi-hat and cymbal activity low and avoid bright sustained pads; the surviving spectrum finding says the open upper bands are part of the sound.
9. **Report the numbers.** Print X, R, I, N_eff per section, the drop-out count and the build position with every arrangement, so each song can be compared with whatever the tests above establish.

## 3. The wild idea: the hole the shape of the listener

A great record is unfinished on purpose. The bands left open and the slots left silent are the space where the listener sings along, taps, and imagines; the record is completed in the person hearing it, and a cover is that same completion done by a musician. A wall of sound is a closed object you admire from outside; a sparse record has a door. If so, greatness is not a property of what is on the record but of the *complement*: the shape of what was left out. Measure the complement itself. Take the band-by-time grid of energy (ERB bands by 50 ms frames, from idea 1), mark the empty cells, and ask whether the emptiness is structured: is the empty region large, connected, and located where a human voice lives (roughly 150-1,000 Hz for the sung note and up to 3 kHz for its vowel colour) in the moments when the lead voice rests? Compute H = the share of vocal-range band-time cells that are empty while the lead is silent, and the size of the largest connected empty region as a share of the grid. Then test the prediction that covers of high-H songs differ *more* from one another than covers of low-H songs (spread of tempo, duration and key across cover versions, if the cover lists or matched MIDI versions carry them), because each artist fills the hole differently. I cannot defend the metaphysics. But "the statue is what remains after the stone is removed" is, I notice, also how the owner framed his hunch about shape.
