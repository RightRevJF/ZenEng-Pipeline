# Luthier v47, the kept patches built: checks written before the build is run

25 November 2026. From `RESULT.md` here: three patches are kept as defaults, two as settings a lyric may ask for, one is dropped. Review 31 (read after the tests were run) rules that `loop_less` stays a setting.

**Seen before writing:** `RESULT.md`; Review 31 and the list for v47. Nothing of songs 55, 54, 49 or 59 under any patch.

**The build.**
- **959 (749.160), on in 4/4:** a build with a leap past an octave between two sung notes of one line is passed over (read as sung).
- **961 (749.162), on in 4/4:** a build whose title line's longest note falls on an unstressed syllable is passed over.
- **962 (749.167), on:** in the chosen tune, a section whose every line returns note for note has each line after its first lift its longest held note (a beat or more) a scale step onto a chord tone, leaps kept within a fifth; and, mine, never above the tune's highest note, so the planted peak stays the peak.
- **960 (749.159), a setting, off:** `"chords": "loop_less"` in a lyric: a written verse or bridge is drawn again, 30 times at most, until its chord repetition is at or under the kept median for its kind and mode.
- **963 (749.168), a setting:** `"blue_notes": false` in a lyric: no blue-note draw for the song.
- The region gate (749.165, 749.170) is not built.

**The checks.** A thousand builds a song.
1. No chosen tune of songs 55, 54, 58, 60 holds a leap past an octave in a line; every title line's longest note is on a stressed syllable; no section of a chosen tune returns note for note in every line.
2. The three-song soundness rule holds on songs 55, 54 and 58.
3. The pool standard holds (a random pool pick and the neighbour choice pass the rule 90 times in 100), and each pool keeps at least 10 builds.
4. The builds' middle words' fit is no more than 0.02 under v46's in each of songs 55, 54 and 58 (0.265, 0.221, 0.306).
5. The chosen tunes keep the floor (954) and the ceiling (956).
6. Songs 52 and 53 are byte for byte as they were (the gates are 4/4's; 962 changes them only if a section of theirs returns whole, and that is reported).
7. Song 59, the hold-out, is read and decides nothing. Songs 50 and 63 are not run.

**The settings** are checked on song 61 only (a seen song): with `"blue_notes": false` no lowered third; with `"chords": "loop_less"` its verse at or under 0.333.

**Song 63 is not run for 960.** Review 31 names it the hold-out for the loop-less trial. The gate form did not pass my third check, and it is built only as a setting no song gets unless its writer asks. A hold-out is spent when a default is at stake; this one is kept for that.

**What I expect.** Checks 1, 2, 5 and 6 hold. Builds that live fall by about 3 in 10 (the octave gate), so the pools shrink to about 15 to 28; check 3's floor of 10 is the one at risk, in song 54 (its pool is 25 now).
