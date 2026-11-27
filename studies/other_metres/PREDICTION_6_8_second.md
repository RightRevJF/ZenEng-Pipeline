# The 6/8 package on a second lyric: the lyric chosen by rule, the marks, before any run

27 November 2026, 18:17 ET. Asked by the songwriting session (18:03 ET): nobody calls 6/8 working on one lyric.

## The lyric, by the songwriting session's rule
A spent lyric, genre folk, not 52, 53 or 55, nor 65, 67 or 68, with the median line length nearest song 52's; ties by the number of title lines. Counted from the records' own syllables:

| Song | Median syllables a line | Lines | Title lines |
|---|---|---|---|
| 52 (the first lyric) | 11 | 36 | 3 |
| 49 | 7 | 46 | 5 |
| 50 | 7.5 | 44 | 3 |
| 58 | 7 | 57 | 6 |
| **61, "This Side of the Door"** | **8** | 39 | 2 |

**Song 61 is the nearest, with no tie.** It is three syllables a line shorter than song 52, so this is a harder test than a like lyric would be: the bars-from-density rule has to choose differently, and the marks must hold where it does.

*Settled:* the lyric's words, sections, voice (alto), lead (guitar), mode and seed as they stand in `songs/p71/lyric61.json`; metre set to 6/8, genre folk; **54 beats a minute, song 52's**, since no mark here reads tempo and ours has one 6/8 tempo on record. The file is a trial copy outside `songs/`; song 61's own record is untouched.

## The form
Every 6/8 switch as the last trial stood: `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.9 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=1 LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1`. Seed 1, 1,000 builds. No code changes, so no byte check is owed.

## Marks (S1 to S7 and U1 to U4, as they stand), on the living median and the pick
- Bars per line printed before the draw, lines ahead of title lines marked.
- Living builds 30 or more; pool 10 or more.
- Notes a bar over the bars of sung phrases 3.60 to 4.33.
- Onsets on the beat 0.389 or more; on the bar's first beat 0.211 or more.
- 731: the median build's stressed syllables on a beat 0.40 or more.
- Deaths on 780 and on 840 each under one in ten of builds made.
- Every note in the voice; no leap past an octave inside a line.
- Each title line on its bar line or before it in three builds of four, among builds made from the fitted spec.

Reported: builds never made, by reason; stressed syllables on the first beat (no mark).

## What I expect
The title-line marks and 840 are met (the form is general). **Notes a bar is the doubt:** at eight syllables the rule gives two bars (four a bar, inside) or three (2.7, outside), and a song of mixed choices could land under 3.60. Living builds and beat marks likely. One chance in two for every mark on both readings.
