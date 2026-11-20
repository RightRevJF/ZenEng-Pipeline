# The songwriter's contribution

## 1. Diagnosis

Almost everything that failed was either a property of a part (a leap, a high note, a chord) or an average over the whole song (mean surprise, overall repetition, a scaling exponent). In fifty years I have never once judged a song that way. What I listen for is a small number of appointments: the one bar where the title lands, the one bar where the chorus opens, the one bar where the last chorus comes back changed. A great song and a good song can have identical averages and differ only in whether four or five things happen in the same bar or two bars apart. Averages cannot see that; a coincidence in time can.

Second, a lead sheet is the song with three things removed: the words in the mouth, the singer's body (where in the voice the notes sit), and the room left around the voice. All three are relations, and the tests that held (sparse, uncrowded, few events per second) are exactly what "room around the voice" looks like when measured crudely.

Third, the yardstick mixes two different objects. "Still loved" is mostly about a record. "Covered by many" is about a song that can leave its record. Those are different crafts, and I suspect they have been cancelling each other. A wall-of-sound record nobody dares cover and a plain tune everybody covers both score "half great".

Fourth, every test song is already a hit. A hit has already passed the tests for hook, pace and singability. You are grading among survivors, where those features have little spread left.

## 2. Ideas, most promising first

### Idea 1. Split the yardstick: the Song and the Record

**Plain words.** Separate greatness into two scores. Song-greatness is how far the tune travels without its record: covered by artists of other genres, other sexes, other decades. Record-greatness is love for the original that covers do not explain. I expect the page to predict the first and the recording to predict the second, and that this is why page features scored zero on the blend.

**Mathematics.** For each work, from the cover list compute (a) log(1 + number of covers), (b) cover breadth B = Shannon entropy of the genre distribution of covering performers (genre taken from the performers' own charting records where available, otherwise from tags), (c) cover reach T = median years between release and cover. Song score S = first principal component of (a, b, T). Regress current love (streams or popularity) on S plus release year; the residual is Record score R. Then rerun the cheapest existing page features against S alone and the 127 sound numbers against R alone. Also compute S within songwriter, not within performer, where writer credits exist.

**Data.** Cover lists with performer per version: have. Performer genres: have for charting performers, partial otherwise. Writer credits: SecondHandSongs works carry them; check the dump.

**Proved wrong if** page features stay at zero against S, and sound features predict S as well as they predict R.

**Odds.** 35% that at least one family of page features rises above 0.10 against S on the hold-out.

### Idea 2. A yardstick with no record in it: hymnals and standards

**Plain words.** There are two repertoires where the page is all that was ever transmitted. A hymn tune survives by being reprinted in hymnal after hymnal for centuries, sung by untrained people with no recording to imitate. A jazz standard survives by being re-recorded by hundreds of players from a lead sheet. If mathematics on the page can grade greatness anywhere, it will be here first. If it cannot do it here, the page hypothesis is in real trouble, and that would be worth knowing.

**Mathematics.** Hymn tunes: greatness = log(number of distinct hymnals printing the tune), controlled for year of first publication and denomination; a sharper version is survival, the fraction of hymnals published more than 100 years after the tune that still include it. Standards: greatness = log(number of distinct recorded versions), controlled for year. Run the entire failed battery plus Ideas 3 and 6 below, unchanged, with a locked hold-out.

**Data.** Tunes: have (ungraded). Grades: need Hymnary.org instance counts (dumps and scrapes exist on GitHub; needs checking) and a standards recording count (SecondHandSongs works already cover many standards; the jazzstandards ranking list is mirrored in several GitHub repositories). Uncertain until someone looks.

**Proved wrong if** nothing on the page grades hymn tunes or standards either, at sample sizes of a thousand or more.

**Odds.** 45% that something on the page holds in at least one of the two repertoires. This is the cleanest experiment on the list.

### Idea 3. The appointment: how many things arrive in the same bar

**Plain words.** In a lasting song the title line feels inevitable because several independent arrivals are booked for the same moment: the tune reaches its goal note, the harmony comes home, the note is long, it sits on a strong beat, and it is the first time all of those have happened together. A good song has the same ingredients spread over neighbouring bars. This is not mutual information across the whole song (which failed); it is a coincidence at one place.

**Mathematics.** For every note n compute five standardised streams within the song: p(n) = pitch height z-score; d(n) = log duration z-score; m(n) = metric weight (4 for bar downbeat, 3 half-bar, 2 beat, 1 off-beat) z-score; h(n) = harmonic arrival, 1 if the chord is tonic and the previous chord was dominant or subdominant, else 0, z-scored; s(n) = stability, 1 if the note is scale degree 1, 3 or 5 and a chord tone. Appointment score A(n) = product of the positive parts of the five, or more robustly the minimum of the five. Then: (i) A_max = the maximum over the song; (ii) concentration = A_max divided by the 90th percentile of A; (iii) first-arrival time = position of the first note with A above a threshold, as a fraction of the first verse-plus-chorus cycle; (iv) a shuffle baseline: shift each stream by a random whole number of bars against the others 1,000 times and report where the real A_max sits in that distribution. The claim is about (iv): great songs have more coincidence than their own ingredients would give by chance.

**Data.** Hooktheory melody plus chords, about 900 graded: have. Lakh multi-track for full-song span: have. With aligned lyrics (Idea 6 data) add a sixth stream: is this the title word.

**Proved wrong if** the shuffle percentile does not differ between graded tiers, or differs only through song length.

**Odds.** 20%.

### Idea 4. Room for the voice: the answer in the gaps

**Plain words.** The oldest rule in arranging is that nothing plays in the singer's register while the singer is singing, and something answers when the singer breathes. The measures that held (few bands, few events per second) are a blurred photograph of this. Measure the relation directly: does the band step back when the voice enters and step forward when it rests, and is the voice's register left empty?

**Mathematics.** From multi-track MIDI, identify the lead line (track labelled melody or vocal, else the monophonic track with highest pitch-entropy in the vocal range). Let V(t) = 1 where the lead sounds, on a sixteenth-note grid. Let O(t) = count of accompaniment onsets, excluding drums, in the grid cell. (a) Call-and-answer C = minus the correlation of V(t) and O(t), and separately the mean of O in the two beats after each vocal phrase end divided by the mean of O during phrases. (b) Register clearance K = fraction of vocal-sounding time in which no accompaniment note lies within a fifth (7 semitones) of the sung pitch. (c) Bass independence = share of bass onsets that fall in vocal rests. Report each per section and overall.

**Data.** Lakh clean, about 1,400 graded: have. MIDI files are fan transcriptions, so noisy, but this noise is not biased toward the yardstick.

**Proved wrong if** C and K show nothing on the hold-out, or vanish once note density is controlled (meaning it was only "fewer events" again).

**Odds.** 30% for a correlation of 0.10 or better surviving the density control.

### Idea 5. The withheld close: where the song first lets you rest

**Plain words.** A verse that closes fully has nowhere to go. In the songs that last, phrase after phrase ends open (on the fifth, on the second degree, over a chord that is not home), and the first complete close is saved for the title line. Average tension and resolution failed because the average is the same either way. The schedule is what matters: open, open, open, shut.

**Mathematics.** Segment the melody into phrases (rest longer than a beat, or a long note followed by a new start). For phrase k, closure c_k in [0,1] = mean of four indicators at its final note: note is the tonic; chord is the tonic; final note is on a strong beat; final note is at least twice the phrase's median duration. Then (a) Gini coefficient of c over phrases (closure concentrated in few phrases scores high); (b) rank position of the first phrase with c at least 0.75, as a fraction of the first full verse-chorus cycle; (c) whether the highest-closure phrase is also the most-repeated phrase in the song (a stand-in for the title line when lyrics are absent); (d) the open run: the longest run of consecutive phrases with c under 0.5 before the first full close.

**Data.** Hooktheory graded 900: have, though Hooktheory entries are often a section rather than a whole song, so use the Lakh files for (b) and (d).

**Proved wrong if** none of (a) to (d) separates tiers; in particular if songs that close fully in every verse phrase grade just as well.

**Odds.** 15 to 20%.

### Idea 6. The word in the mouth, tested properly

**Plain words.** The only page result that leaned positive was word stress against melodic accent, and it was never finished. A singer knows more than stress: high and long notes want open vowels (ah, oh, ay), tight vowels and clustered consonants on a top note strangle it, and the important word must be the one the tune leans on. This is a relation between two parts, the text and the tune, and it is why some songs are a pleasure to sing for fifty years.

**Mathematics.** With note-aligned lyrics, for each sung syllable take pitch z-score p, log-duration z-score d, metric weight m, lexical stress s (0, 1, 2 from the CMU pronouncing dictionary), vowel openness v (first formant rank of the vowel, a fixed table: "ah" highest, "ee" and "oo" lowest), consonant load q (number of consonants closing the syllable). Scores: (a) stress fit = correlation of s with m plus d; (b) open-vowel fit = correlation of v with p plus d, and specifically mean v over the top decile of p plus d; (c) choke rate = mean q on the top decile of p plus d; (d) title fit = percentile of (p + d + m) for the syllables of the title words among all syllables; (e) content-word fit = mean (d + m) on nouns and verbs minus the same on articles and prepositions.

**Data.** Need note-aligned lyrics. The DALI dataset (several thousand songs, word and note level alignment, annotations distributed through GitHub and Zenodo without audio) is the obvious source; overlap with the graded hits must be checked. MIDI karaoke files (.kar) in the Lakh collection also carry syllable-timed lyrics and are already here if the lyric events were kept.

**Proved wrong if** on 500 or more graded songs none of (a) to (e) reaches 0.08 on the hold-out.

**Odds.** 30%. Also the one most useful to a working writer if it holds.

### Idea 7. Same tune, new ground: the reframe

**Plain words.** The bridge and the last chorus work by making you hear the same line as a different thing. On the page this shows as a melodic phrase that returns with the notes unchanged but the chords, the bass or the bar position changed underneath. Varied repetition of the melody failed; this is repetition of the melody with variation of everything else.

**Mathematics.** Find all pairs of melodic segments of 2 bars or more with identical interval and rhythm sequences (allow transposition). For each pair compute the context distance D = fraction of beats on which the scale-degree function of the melody note against the chord root differs (for example the same G heard as the fifth of C, then as the third of E minor). Song score = share of repeated-melody time with D above 0.25, and its position: mean normalised time of the high-D returns (the claim is that they come late). From MIDI add an arrangement version: for each repeat of the chorus, cosine distance between the vectors of which tracks are active, and whether the last chorus differs most from the first.

**Data.** Hooktheory and Lakh: have.

**Proved wrong if** the share of reharmonised returns, and their lateness, are flat across tiers.

**Odds.** 15%.

## 3. The wild idea: the song as the crowd sings it

A great song is one that ordinary people sing wrong in the same way and it is still the song. I suspect a great tune is an attractor: give a thousand untrained singers the melody and their errors pull toward a simpler shape that is still unmistakably it, whereas a merely good tune dissolves into a thousand different mistakes. Greatness would then be measurable as the narrowness of the cloud of amateur renditions around its own centre, relative to its distance from every other song's cloud. That is a shape in a space, as the owner wants, but the space is not the score; it is the space of everything people do to the score. Hymn tunes have been through four centuries of exactly this filter, which is why I trust them as a test bed. Data: the Smule DAMP sets on Zenodo hold tens of thousands of amateur performances of a few hundred songs (access is by request, and it is audio, so pitch tracks would have to be extracted). A no-audio stand-in already here: the three independent transcription sources of the same tune are three "singers"; where they agree is the attractor, and the agreement rate per bar could be computed tomorrow. I would not defend it in public because it defines greatness by what survives carelessness, and every teacher's instinct says the opposite. I cannot put it down because every song I have seen last is one a room full of people can sing after two hearings.
