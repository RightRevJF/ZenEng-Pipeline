# Luthier list for v44 (since v43)

21 November 2026. Luthier v43 (954 to 956) is reviewed (`lib/luthier/REVIEW_stage28.md`) and merged into main at 39166df. Every kept table, every record, song 60's v43 record, `soundness.json` and the neighbour figures reproduce byte for byte. Both checks pass, and the record check fails when a table changes. Song 58's eighteenth edition is built from the v43 record. Next finding 749.142; next fix 957.

## In short

954, 955 and 956 hold. The tag reading is right: kept songs' outros, fadeouts and codas are not pooled with their choruses either. But the kept table pools pre-choruses with choruses, and song 55's change of tune rests on that. 749.137 can be settled between gates and chance by reading the share per build. A new fault: the planted peak lets the song's top note fall on weak words. Song 58's highest note is held on "the", and the hold-out song 59 puts 11 of its 24 top notes on "to", "of" and "the". Rhythm scaling (749.138) is still the next window's main work.

## Items

### 749.139 The kept table pools pre-choruses with choruses
**Problem.** `make_kept_commonest_pitch.kind()` calls any part whose name contains "chorus" a chorus. Kept songs' "prechorus" sections (22 songs, 1,688 notes) are pooled with their choruses, and the engine reads Luthier's parts the same way. Luthier's choruses never hold a pre-chorus.
**Evidence.** Chorus ceiling as built 0.474; with pre-choruses left out 0.479. Song 55's tune before 956 read 0.476, so its change of tune turns on this. Bootstrapped, the ceilings run 0.405 to 0.498 (verse) and 0.451 to 0.501 (chorus).
**Fix.** Tell a part by its exact name in both places: a pre-chorus is neither verse nor chorus. Print each ceiling with its bootstrap range. Remake the table and rerun the songs.
**Check.** The maker rebuilds the table byte for byte. The record check passes. The paper says which picks change, and whether any changed inside the ceiling's range.

### 749.140 Settle 749.137 per build, not three at once
**Problem.** The result could not tell the gates from chance, because it reads the rate at which all three songs fail at once. That rate cubes the noise. The 43 and 28 in 100 it reports are worked back from that rate, not read.
**Evidence.** `studies/sounder_pools/RESULT.md`. Pools without and with the peak hold 167 and 152 builds. If the per-build shares under the kept 10th of rhythm scaling are near 43 and 28 in 100, that gap is about 2.8 standard errors.
**Fix.** Read, per build, the share under the kept 10th of rhythm scaling in each pool and among all living builds, with and without the peak. Test the pools' gap by permutation over builds.
**Check.** If the pools differ and the living builds do not, the gates explain it; say so. Either way, record the pool's spread of rhythm scaling against the kept spread (now 0.30) as the measure 749.138 must move.

### 749.141 The song's top note on weak words
**Problem.** 950 plants the peak until one stressed note reaches it, and does not stop other notes at the peak falling on weak syllables.**Evidence.** Top-note occurrences on weak syllables in the v43 records:
- song 55: 1 of 3 (livin');
- song 54: 2 of 8 (a, the);
- song 58: 4 of 12 (heaven twice, early, the), with the highest note held on "the" in "he climbs up to the top";
- song 59, the hold-out: 11 of 24 (to, of, the);
- song 60: 1 of 4 (me).

**Fix.** Rule first: read, in the kept songs, the share of a song's top-note occurrences that fall on weak syllables (word_weight's stress reading). If Luthier's builds stand over the kept 90th, plant the peak only on stressed syllables and redraw a planted line that puts a weak syllable at the peak. Try it against the pool standard first.
**Check.** No chosen tune over the kept 90th for weak top notes; the words' fit by height does not fall; builds and pools within the trial's floors; song 59 read only.

## Carried, next

749.138 (rhythm scaling in the engine, rule first). The pool's rhythm-scaling spread is 0.30 of the kept spread, and 93 pool builds in 100 sit under the kept 25th. That is the plainest measure of what it must move.

## Closed

749.135 (954), 749.136 (955), 749.134 (956), 749.137 (range ruled out; the rest goes on as 749.140).

## Carried

749.125 (song 60 as a practice song), 749.127 (the "seen before writing" line: kept), 749.109, 749.116, 749.103, 749.101, 749.61.
