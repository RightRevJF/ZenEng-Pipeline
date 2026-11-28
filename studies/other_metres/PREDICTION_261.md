# 749.261, a line that sings an earlier line again takes its second notes where its source has them: the form and the test, before any code or run

28 November 2026, 11:39 ET. From RESULT_count_first_rhythms.md (on the notes as made K6's rhythm line is met in 98 to 100 builds in 100; the melismas, placed line by line, break the repeats; the share drawn orders the six-mark share). Accepted and numbered by the songwriting session (11:34 ET); arms A, B and C of the earlier 749.261 are set aside.

**Read from the code before writing this:** the engine already does part of it. 919 and 942: a line the lyric marks as a copy, or as sung again **with the same number of syllables**, takes its source's melismas syllable for syllable. What is missing is (1) 818's lines (the line two above sung again inside a section: the repeats K6 reads), which the melisma step does not know about, and (2) the lyric's lines sung again with a syllable more or fewer.

**The form (`LUTHIER_MELISMA_FOLLOW=1`, unset by default):** every line that sings an earlier line again (the lyric's again, a copy, 818's) drops the second notes it drew for itself and takes its source's, in song order, so a source is settled before the lines that follow it.
- Where the lyric marks the line and the counts are the same: syllable for syllable, as 919 and 942 do now (unchanged).
- Otherwise (818's lines; a count that differs): **a note takes a second note where the source's note at the same place in the line has one** (the same onset counted from the line's own start), **and where the syllable allows.**
- *"Allows", settled:* by 848's own rule for where a melisma may sit: the syllable ends its word; the note is an eighth long or more; it is not an unstressed one-syllable word (875). Stress is not otherwise asked: 848 does not ask it.
- Lines drawn fresh draw their own, as now. The share drawn for the song is unchanged; the song's share as sung may differ from it (watched).
- *How the melisma step learns the source:* with the switch set, the engine marks each note with its place in its line and, for a line sung again, the line it sang; the planner keeps those two marks on the record's notes. With the switch unset no note carries them and nothing changes.

**The test (the songwriting session's):**
1. **Seen seeds 1 to 12, both lyrics, the package as it stands with the switch** (749.259 at 64 beneath), beside the same without it (RESULT_260_counts's runs): a read that decides nothing. If a figure mark breaks on any seen seed, it is said before the fresh seeds run.
2. **Fresh seeds 13 to 15, with 749.260, against the bar for ready as it stands:** both lyrics; every mark on the pool's median (notes a bar 2.38 to 3.85; onsets on a beat 0.508 or more; K3 off the beat 0.26 or under; range 12 or more; pitches 7 or more; K5 0.303 or under; K6 rhythm again 0.349 to 0.871 and figure again 0.667 or under; the share drawn fresh at most 0.076; the chord mark; source lines at least 0.40; late lines at most 0.15; the pool at least 10); the six-mark share at least 76.2 at each seed; no pick with a leap past an octave inside a line. **If both lyrics pass at all three seeds, pop 3/4 is ready and songs 68 and 69 run together** (when the songwriting session says so).
3. Watched: rhythm again within sections as made and as sung (the gap should close); different bar rhythms in 16 bars as sung against the clips' 6; the share of syllables on two notes as sung against the share drawn; the share of melismas that sit on a stressed syllable; K3's first beat (borrowed); 838 (flag over 450).
4. The switch acts only where set: the five 6/8 lyrics on song 69's package unset, and 54, 55, 52 and song 53's Essen arm unset, byte for byte; room files after.

No fit, so no fit file. A reading tool gains two figures before the run (not the engine): `pool_count.py` prints rhythm again on the notes as made, and the second notes' share.

## What I expect
- On the seen seeds the six-mark share rises at the seeds that drew 8.6 and 16.2 and is unchanged at 3.8; every seed of both lyrics clears 76.2, song 49's seed 10 (60.1) the least sure. The gap between as made and as sung closes to under 0.05.
- The song's share as sung rises a little above the share drawn where a section repeats a line that has a melisma (the copies multiply it); I do not expect K2 (notes a bar) to break.
- **Fresh seeds 13 to 15, both lyrics, with 749.260: I put a pass at two chances in three.** The ways to miss that I can name: a seed drawing 16.2 on song 49's words where fresh lines' own melismas are still enough to break the repeats; 749.260 thinning a pool; a figure mark I have not been watching.
