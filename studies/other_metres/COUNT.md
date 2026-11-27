# Kept songs outside 4/4: a count (27 Nov 2026). Nothing built, nothing tested.

The writer's direction, 27 Nov 07:41 ET: the engine should in the end write every metre as well as it writes 4/4. This is the first step, a count of what the kept collection holds. Counted from `corpora/CoCoPops` (each melody file's metre taken as the one most of its bars are in).

| metre | Billboard (melody, words, sections) | Rolling Stone (melody, no words) | together |
|---|---|---|---|
| 4/4 | 198 | 168 | 366 |
| 12/8 | 10 | 24 | 34 |
| 6/8 | 2 | 6 | 8 |
| 3/4 | 3 | 1 | 4 |
| 9/8, 7/4 | 1 | 1 | 2 |

- Compound time (12/8 and 6/8 together): 42 melodies, 12 of them with words and sections.
- 3/4: four songs. No kept table can be made from four.
- The 4/4 tables stand on 160 songs. A 90th percentile from 12 songs is not a line anyone should gate on.

## What follows
1. **The collection cannot carry other metres by itself.** A second source of well-loved songs with melody (and, for the words' checks, words) in 3/4 and compound time is needed. None is found yet.
2. **A route that needs no new songs, to be tested and not assumed:** some checks may not depend on the metre (the commonest pitch's share, plainness, range, pitch scaling, the octave leap). A reading, rule first: do the 42 compound-time kept melodies fall inside the 4/4 kept songs' ranges on each such check? Where they do, the 4/4 table may stand in outside 4/4, to be tried one check at a time. Checks that read the bar (the words' weight by place in the bar, line ends, rhythm scaling, the closer verse) cannot be borrowed.

## A second count, the same day: Wikifonia lead sheets (through ChoCo)
`github.com/smashub/choco`, `partitions/wikifonia/raw`: 6,391 MusicXML lead sheets read (melody, chord symbols, words). Named by the songwriting session; counted with `wikifonia_count.py` (`wikifonia_count.json`). Each filed under the metre most of its bars are in; "usable" = 60 notes or more, words under at least half the notes, eight chord symbols or more.

| metre | lead sheets | usable (melody, words, chords) |
|---|---|---|
| 4/4 | 4,398 | 3,128 |
| 3/4 | 818 | 571 |
| 2/2 | 750 | 667 |
| 6/8 | 153 | 99 |
| 2/4 | 213 | 61 |
| 12/8 | 34 | 23 |
| 5/4, 9/8, 6/4, 3/8, 7/4, 9/4, 3/2 | 25 | 7 |

- **3/4 can be learned from 571 songs with words, and compound time from 122.** That changes `COUNT.md`'s first conclusion.
- Odd metres (5/4, 7/4, 9/8) hold a handful: no tables.
- What these are not: no section names, no chart record. They are published popular songs someone cared to transcribe, from standards to the 1990s; OpenEWLD is the public-domain part of the same collection.
- **Licence, to be settled before any public use:** ChoCo is CC BY 4.0, but the songs themselves are in copyright and Wikifonia closed over licensing. The raw files are kept outside the repository, as CoCoPops is. Tables of counts made from them are a different thing from the songs, but that is a judgment for the writer before a public app, not mine to assume.
