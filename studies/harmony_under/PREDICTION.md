# The harmony voice under the lead, in a stated range: the form and its marks, written first (749.222)

27 November 2026. The item is the songwriting session's, from song 66 (`songs/p68/fixlist_v53.md`): twice in the A minor run the harmony note was G4 over the lead's B3, and the voice reaches A2. Seen before writing: that entry; `band.arrange()` (829, 889, 893: the harmony below the lead, above it only where below has no room, between E2 and A5 whatever the singer); and that re-arranging a finished record reproduces its parts exactly (tried on songs 55 and 66), so the form can be read on the records without writing any song again. How often the present harmony crosses the lead, record by record, has been read for three records only: 0 in song 55, 0 in song 66's own run, 2 in song 66's A minor run.

**The form.**
1. **Never over the lead.** The candidates above the lead are dropped. Where no note under the lead fits, the harmony voice does not sing that syllable (the code already rests it where it has no candidate).
2. **A stated range.** The harmony is sung by the voice next below the lead's (soprano: mezzo; mezzo: alto; alto: tenor; tenor: baritone; baritone and bass: bass), from that voice's floor to the lead voice's top, by `chord_writer.VOICES`. The record states it. For song 66, a tenor: G2 to A4, that is 43 to 69.
3. **The interval classes stay the kept ones** (PDMX, a voice below the lead: thirds, fifths, octaves, unisons, fourths, sixths). The list's wording is "a third to a sixth under the lead"; kept second voices sing a unison or an octave under the lead 30 times in 100, and I have not dropped them. For the songwriting session to amend before the run if it means the narrower thing.

A default (every 4/4 and 6/8 song's harmony part is written by it). It changes the harmony part and nothing else.

**Marks, on the records re-arranged** (songs 55, 54, 58, 49, 50, 59, 61 as v53 has them; song 66's own run; song 66's A minor run under the design gate, `songs/p76/run_d/lyric66_d.song.json`, where the fault was seen):
- **H1.** No harmony note over the lead, in any record.
- **H2.** Every harmony note inside the stated range.
- **H3.** The harmony's fit to the kept interval shares (the record's `harmony_fit.miss`) no worse than the record's present one by more than 0.03.
- **H4.** The harmony sings no fewer than 0.9 of the syllables it sings now, in every record (it is not thinned away).
- **H5.** Everything in the record but the harmony part, its fit and the band checks that read it is unchanged: melody, chords, bass, chordal part, drums.
- **H6.** The band checks that are true stay true; "a second from the lead" stays nil.

**What I expect.** H1 and H5 by construction. H2 met. H3 met: the above-the-lead notes are rare (2 of 234 in the record that has them). H4 met, with the A minor run losing a handful of syllables where the lead sits at the bottom of its range. If the stated range's floor (a fifth under the lead's) is still lower than the songwriting session wants, that is a number to set before the run, not after.
