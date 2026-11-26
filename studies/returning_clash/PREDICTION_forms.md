# Two forms for the clashes of 749.212: marks written first (749.223, 749.224)

26 November 2026. Agreed on the thread (`coord/songwriting.md`, 16:40): two forms, each read on its own, clean and whole, on the seen songs; a form that misses its own marks drops out; what passes goes together to sealed song 64 as one version against v52, its marks posted before anything runs on it; if that fails neither is built. Seen before writing: `RESULT.md` here. Neither form has been run.

(Findings 749.219 to 749.222 are the songwriting session's, from song 66; these are the next two.)

**Form 1, the copy (749.223).** A copied line's note that is long in the draw's sense (the last of its line, or a beat or more to the next onset), where the chord under it differs from the chord under the same place of its source, and it is off the chord and a semitone from a chord tone: moved to the nearest chord tone within four semitones, in the scale and in the line's register, as `again()` does (833); left where there is none. Blue notes (846) are left. `LUTHIER_COPY_CLASH=1`; spec key `copy_clash`. Off.

**Form 2, the melisma's second note (749.224).** A syllable is not a candidate for a melisma if its second note would clash both ways: the scale step below and the scale step above each either off the chord and a semitone from a chord tone while a beat long or more, or shut out by the rules already there (the run cap, the range). Where the step below would clash and the step above is clear, the second note is the step above. A returning line takes its source's melismas as before, except on a syllable that is shut out under its own chord. The song's share of melismas is drawn as before, from the candidates left. `LUTHIER_MELISMA_CLEAR=1`; spec key `melisma_clear`. Off.

With both off, songs 54 and 55 byte for byte.

## Clean reading: each v52 record's fitted spec, 1,000 builds, songs 55, 54, 58, 49, 50, 59; v52, form 1 alone, form 2 alone

Clashes are counted as since 12:10 today: a sung note a beat long or more, off its chord, a semitone from a chord tone, other than a blue note.

What each form is for:
- **F1.** Clashes in copied lines over another chord, per 100 notes of the song: at most half of v52's in every song where v52 has 0.1 or more.
- **F2.** Clashes on a melisma's second note, anywhere in the song, per 100 notes: at most a quarter of v52's in every song.

What neither may break (each form alone against v52):
- **a.** All clashes per 100 notes no more than v52's in any song.
- **b.** Living builds no fewer than 0.9 of v52's in every song.
- **c.** The builds' middle bars on a figure already sung no lower than v52's by more than 0.03 in any song.
- **d.** The builds' middle pitch scaling no further from the kept middle (0.905) than v52's by more than 0.03, and the builds' middle surprise no further over the kept middle (3.18) than v52's by more than 0.05, each in at least five songs of six.
- **e, form 2 only.** The melismas drawn, syllables in 100, within one point of v52's in every song; the share of them on a line's last syllable within 5 points of v52's in every song. (A melisma sits on a word's last syllable by construction, before and after.)

## Whole engine: the six songs written through, each form alone

- **W1.** Soundness of the three holds; a random pool pick fails the rule 6.5 times in 100 or fewer; pools no smaller than 0.8 of v52's in songs 55, 54, 58 and no pool under 10 that was 10 or more.
- **W2.** The builds' middle words' fit no lower than v52's by more than 0.02 in any song; every chosen tune at or over its floor.
- **W3.** Marks F, a and d again on each written record's fitted spec (300 builds).

## What I expect

Form 1: F1 met (most such notes have a chord tone within reach; `again()`'s rule never failed where it looked). a, b met. **c is its risk:** a moved note in a copy breaks a figure that was sung before, and song 55, with most to mend, may lose 0.02 to 0.04 of its figure share. d met.

Form 2: F2 met, near nil. e met (the candidates shut out are few). a to d met; it moves one note in a hundred or fewer. I expect form 2 to pass everything and form 1 to pass unless c catches it in song 55.
