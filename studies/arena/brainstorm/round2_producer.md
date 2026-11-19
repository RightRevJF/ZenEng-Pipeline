# Round two: the producer answers the room

A warning that applies to half the room, me included: the multi-track MIDI files are made by fans, and loved songs attract more and more careful sequencers. Track count, detail and number of versions can therefore leak the yardstick into any MIDI measure. Every MIDI test should control for number of tracks and notes, and where a song has several files, use the median.

## 1. The two strongest ideas from the others

**Sceptic, Idea 2: same song, different hit records.** The best design in the room, because it holds the page exactly fixed and asks whether the recording findings still work. It also gives the ceiling without needing any musical feature.
*What my field corrects.* Two hit versions of one song are usually years apart, and a 1962 and a 1987 recording differ in tape, track count and mastering before anyone plays a note. Raw differences in spectrum will just measure the calendar. So score each version against its own cohort first: z_v(f) = (f_v - mean of hits within +/- 2 years) / (their standard deviation), then take the within-work difference of z, not of f. Also record which version came first: a remake is made by people who knew the earlier record and deliberately moved away from it, so the two are not independent draws.
*What my field adds.* A directional prediction: within a work, the version that is sparser and less like its own year is the one still loved. Sign test over works.

**Neuroscientist, Idea 2: arrival architecture (few big arrivals, long runways).** Better than my own density arc, because it says why sparseness helps instead of restating it.
*What my field adds.* Loudness and fullness are logarithmic. Adding one part to n equal parts raises level by 10*log10((n+1)/n) dB: about 3 dB for the second part, 0.5 dB for the ninth. A dense record cannot have a big arrival; a sparse one always can. So measure arrival size as G(t) = 10*log10(n(t)/n(t-1)) + w * (number of frequency bands newly occupied at bar t that were empty over the previous 4 bars), not as a raw change in note count. An entrance into an empty band is heard; an entrance into an occupied band is masked.
*What my field corrects.* Drop the velocity term: fan MIDI velocities are arbitrary. And count subtraction as an arrival too. The bar where the band drops out and the voice is left alone is often the largest event on a record, and it has negative delta-I.

## 2. The weakest idea in the room

**Neuroscientist, Idea 3 as run on MIDI ("better than remembered": information in the arrangement beyond the lead sheet).** The idea is right and the test will fail or, worse, falsely pass. What memory cannot store is grain: the vocal timbre, timing, breath, the room. A fan MIDI file contains none of it. What H(arrangement | skeleton) will measure on these files is how diligent the sequencer was and how far the genre sits from the training pile, and diligence rises with how loved the song is. The same fault kills the physicist's "cheap first look" at microtiming in unquantised Lakh files: that timing belongs to a hobbyist's keyboard, not the session.
My own Idea 1 shares the disease in its fancy form: the synthesised-spectrum masking model rests on velocities and instrument numbers that are not trustworthy. I withdraw it down to the velocity-free "lane clearance" count, which the songwriter and mathematician proposed independently.

## 3. A new idea from reading the papers together: the promoted part

The physicist, evolutionist and sceptic all converge on a rigid core plus a free shell, and all three quietly assume the core is the page: tune and chords. The songwriter splits Song from Record. Put those beside my signature idea and something neither says appears: on many lasting records, a piece of the *arrangement* has been promoted into the song. Later artists keep a bass line, a guitar figure, a drum pattern or an intro that no lead sheet contains, as if it were melody. That would explain the central puzzle, why recording measures predict a yardstick that is half cover count: the record wrote part of the song, and a sparse record is the only kind in which such a part is audible enough to be promoted.

**Mathematics.** For a work with K versions by different artists (use fixed K, say 4, so cover count cannot leak in):
- From the original, take each non-vocal track's most repeated one- or two-bar figure, coded as (rhythm slots on a sixteenth grid, pitch intervals) so key does not matter.
- Promotion of figure g: pi_g = fraction of the other versions in which the code appears in any track for at least 4 bars, allowing one slot of timing tolerance and a halving or doubling of tempo.
- Baseline: the same fraction computed against versions of *other* works with the same chord loop and tempo band. Promotion score Pi_w = max over g of (pi_g - baseline).
- Record share of the core: rho_w = conserved non-melody events / all conserved events, using the evolutionist's conservation count c_i extended to every track.
- Predictions: Pi_w is higher for great songs; Pi_w rises with the original's sparseness and vocal exposure; and in the physicist's "identity space", adding the presence of the promoted figure sharpens the distance that predicts the yardstick.

**Data.** Different-artist arrangements of the same title inside Lakh (in hand, but few true covers). Properly: cover features from Da-TACOS, where bass-register chroma could carry a bass line; that needs fetching and checking.
**Wrong if** promotion is no more common than baseline, or is unrelated to grade and to sparseness.
**Odds.** 35% that promotion is real and measurable; 25% that it grades songs.

## 4. Votes

**First test with data in hand:** Sceptic's Idea 2, same work in two charting versions, with every sound number scored against its own year cohort as above. One run gives the page ceiling and tells us whether sparseness survives with the page fixed and the era removed. If the +0.25 dies there, most of this room's theory dies with it.

**First test needing new data:** fetch Da-TACOS and measure version clouds of real covers (physicist Idea 1, evolutionist Idea 3), adding the promoted-part count. I expect the hymn laboratory to get the other votes, and it deserves them for the page question; but every finding that has held is in the sound, and this is the only new dataset that carries sound for many versions of one song without needing audio.

## 5. Where the room is converging, and whether I believe it

**The theory:** a great song is a small, rigid, unmistakable core surrounded by deliberate open space, and the yardstick counts how many listeners and performers have stepped into that space.

**Do I believe it?** Half. I believe it for the covers half, with the amendment that the core is not only the page. For the "still loved record" half, open space is a precondition and nothing more: people do not love a gap, they love the one voice that was exposed in it, and nobody in this room, me included, can measure that performance without raw audio. And until the era-controlled test is run, "space" may still be a polite name for "old ballad".
