# The tune's tie to the chord, set by kept songs: the form and its marks, written before any run (749.198)

25 November 2026. The writer said yes to the test. Seen before writing: `studies/held_chord/RESULT.md`. Nothing has been run under the form. It is behind a switch that is off (`LUTHIER_CHORD_TIE`).

## The form

1. **In a line sung again** (fix 712's fit), a note on a beat that is not a chord tone is no longer moved to one. The clash rule (833) still moves a long note that sits a semitone from a chord tone, there as everywhere.
2. **In a fresh line,** the draw's hand-set favour for chord tones (2.6 to 0.3 on a beat, 1.3 to 0.8 off it) is replaced by two weights from the kept songs: a chord tone is favoured so that the odds of landing on one match the kept odds, on the beat (kept share 0.632) and off it (0.562).
3. Fix 833, the clash rule, is untouched.

**How the two weights are set (a fit of two constants to two kept figures, as 930 fits the move weights; said plainly, it is done on seen songs).** With no favour at all (both weights 1) and the rest of the form on, the builds of songs 55, 58 and 50 land on a chord tone some share of the time on the beat and off it: the draw's own base rates. Each weight is the kept odds over the base odds, averaged over the three songs: w = [k / (1 − k)] / [b / (1 − b)]. One pass; no search. If the builds' shares under the weights are not within 0.05 of the kept figures in those three songs, one correction by the same formula is allowed, and no more. The weights and the figures they came from go in `tables/kept_chord_tie.json`.

## The marks

The clean reading (each v50 record's fitted spec, only the form changed, a thousand builds):
1. Songs 50, 58, 49: living builds whose verses are over the pitch ceiling at or under 30 in 100 (now 65, 56, 56).
2. Every song read (55, 54, 58, 49, 50, 59): the builds' share of on-beat chord tones inside the kept 25th to 75th by song (0.53 to 0.73).

The whole engine, a thousand builds, songs 55, 54, 58, 49, 60, 59, 61, 62 and 50:
3. The chosen tune's on-beat chord-tone share (the record's own reading) inside the kept 10th to 90th (0.44 to 0.83).
4. No chosen tune holds a note a beat long or more a semitone from a chord tone (the record's own count; 833 must still do its work).
5. Living builds no fewer than nine tenths of v50's. (More builds is not what this form is for; it must not cost many.)
6. The builds' middle words' fit within 0.02 of v50's.
7. Every chosen tune at or over its floor.
8. Song 50's pool at 10 builds or more (now 5).
9. Songs 55, 54, 58: the three-song soundness rule; pools of 10 or more; a random pool pick fails the rule no more often than 6.5 in 100.

All nine on the seen songs, and it goes to the writer for a sealed song. Any miss and it is not built.

## What I expect

1 to hold (the switches together gave 13 to 19). 2 to hold by the fit, more or less; song by song it may stray. 3 the same. 4 to hold. 5 is a doubt: 712's snap also kept lines sung again inside other gates, and without it more may die. 6 I cannot call: the words' fit does not read chords, but the notes move. 8 to hold or come near (10 is twice what it has). 9 is the real test, as ever: the fits will move.

One thing I will listen for in the figures and cannot hear: 833 was asked for by ear. If the chosen tunes' long notes drift from the chord (kept 0.68 of long on-beat notes are chord tones), I report it even if every mark holds.
