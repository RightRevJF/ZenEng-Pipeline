# Review 17: Luthier v30 (fixes 918–921)

Branch `luthier-v8-stage1` at e408ae6, main merged in at 7b33e96.

## Byte for byte

The song reruns reproduce every committed record. `soundness.py` writes `soundness.json` as committed. `neighbour.py` rerun gives every field of the committed `neighbour.json` unchanged; I added three readings, below. So:
- the pools pass the rule 93 times in 100;
- a random pick has 19 song-checks outside the middle half (16 without the aim);
- rhythm scaling falls past the kept 10th 2 times in 100;
- the first picks pass.

Sound by the amended rule.

## 918

As written. Turns are drawn at the kept split, with at least one of four bars. Song 58 has a four-bar turn after chorus 1 and runs 337 seconds.

## 919, checked hardest: a copy takes its source's melismas

`melisma_notes(how=...)` replaces a copied line's draw with its source's, syllable for syllable, where the line counts match and the note is an eighth or more. In all three records every copied line now carries exactly its source's melismas (13, 8 and 11 copies; none differ).

Copies are processed in note order, so a copy of a copy follows its source. The words' gate reads the same draw (`as_sung` passes `how`). Holds.

One side effect: the song's melisma share now falls a little under the share drawn (0.036 / 0.071 / 0.139 against 0.038 / 0.086 / 0.162). A copy takes its source's choices rather than its own, and loses any that land on a note shorter than an eighth. That is still inside the kept quartiles (3.8, 8.6, 16.2 in 100).

`FIGURE_BORROW` 0.8 moves the builds' bars on a figure already sung toward the kept median (0.42 / 0.587 / 0.444 against 0.474), as `stage17_results.json` shows.

## 920, checked hardest: the aim at a kept song

The kept song is drawn from the title's seed. The row maps to the kept list as `kept_corpus.kept_songs()` orders it: song 58's row 130 is The Everly Brothers' "Bird Dog" (range 9, repeated notes 0.373), as the target's readings say.

The tilt (repeats, steps, leaps, clamped to 0.4–2.5) and the recentred charge bounds act as written. The leap band (5 semitones or more) matches the atlas's. But the aim reaches its targets only in part, and in song 58 it is pulled against itself:

| Song 58 | Target ("Bird Dog") | The pick | Kept median |
|---|---|---|---|
| moves by step | 0.398 | 0.566 (past the kept 90th) | 0.396 |
| moves by leap | 0.057 | 0.033 (under the kept 10th) | 0.102 |
| repeated notes | 0.373 | 0.272 | 0.312 |
| range | 9 | 15 | 17 |
| the chorus's lift | 0 ("Bird Dog") | 10 (plan 9) | 1 |
| pitch scaling | n/a | 1.311 | 0.905 (90th 1.107) |

The aim narrows the tops to a range near 9, while the plan's lift, drawn from another song, puts the chorus 9 semitones over the verse. Each section is squeezed into about six semitones, apart from the other. The melody has room only to step, and the pitch line jumps between two plateaus (749.98).

The repeats cannot reach 0.373, whatever the tilt. The draw never takes a pitch three times running inside a line (`ps[-1] == ps[-2] == p`), and `runs_ok` refuses four. Every song's longest run is 4 (kept median 6, 10th 3; 749.99).

Choosing the pool build nearest each song's own target, rather than the first, brings the targets closer (song 54's steps 0.542 against 0.595; its figures 0.519 against 0.525). But it narrows the songs overall: a random pick among the ten nearest has a median of 16 song-checks outside the middle half (the first picks' pools: 19). So the choice is not the lever (749.100).

## Where the pools sit, check by check

New in `neighbour.json`: the share of all pool builds outside the kept middle half on each check, low and high. A kept song is outside 25 times in 100 on each side.

| Lean: most builds on one side | low | high |
|---|---|---|
| rhythm scaling | 0.90 | 0 |
| pitch scaling | 0.02 | 0.78 |
| moves by step | 0.01 | 0.50 |
| moves by leap | 0.49 | 0.06 |
| range | 0.42 | 0 |
| bars on a figure already sung | 0.49 | 0 |
| bars on a rhythm already sung | 0.47 | 0 |
| distinct rhythms over bars | 0 | 0.47 |

| Too central: few builds outside on either side | outside, total |
|---|---|
| notes a bar | 0.01 |
| longest phrase | 0.02 |
| stressed line ends held a half note | 0.06 |
| onsets on the beat; lines run on | 0.09 each |
| fit by height | 0.11 |
| repeated notes (all low) | 0.13 |

The rule reads leans only when all three songs fall on one side together. These are the engine's tendencies underneath it:
- a melody that steps more, leaps less and spans less than kept songs;
- less repetition;
- pitch scaling high, following the large lifts;
- rhythm scaling low;
- and a set of rhythm and phrase readings that hardly leave the kept middle.

749.94's shortfall (19 against 21) sits there.

## Merged

`origin/luthier-v8-stage1` into main at 7b33e96, no fast-forward. Song 58 rebuilt from the v30 record (eighth edition, D major, a four-bar turn). The consistency check's count of lead-sheet notes was a number written in; it is now read from the record.
