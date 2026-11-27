# The harmony under the lead, third and last form: the result (749.222)

27 November 2026. Form, marks and stopping rule in `PREDICTION_c.md`, the songwriting session's, committed before the run. `records_c.json`.

**Five marks of six, and H3 missed in song 59 by one part in a thousand. By the stopping rule written first, 749.222 is closed for this version. Not built.**

| | 55 | 54 | 58 | 49 | 50 | 59 | 61 | 66 own | 66 A minor |
|---|---|---|---|---|---|---|---|---|---|
| H1. Notes over the lead, now; the form | 0; 0 | 1; 0 | 0; 0 | 0; 0 | 0; 0 | 2; 0 | 0; 0 | 0; 0 | 2; 0 |
| H2. Outside the stated range | 0; 0 | 0; 0 | 0; 0 | 0; 0 | 0; 0 | 0; 0 | 1; 0 | 0; 0 | 0; 0 |
| H3. Fit to kept interval shares (miss) | 0.108; 0.076 | 0.146; 0.130 | 0.077; 0.054 | 0.126; 0.118 | 0.037; 0.037 | 0.084; **0.115** | 0.133; 0.040 | 0.107; 0.086 | 0.072; 0.076 |
| H4. Syllables sung; share kept | 186; 1.00 | 189 of 193; 0.98 | 168; 1.00 | 161; 1.00 | 203; 1.00 | 106 of 112; 0.95 | 119; 1.00 | 231; 1.00 | 231 of 234; 0.99 |
| Syllables that rest, by chorus | | one in each of four | | | | two in each of three | | | one in each of three |

- **H1, H2, H4, H5, H6 met.** The harmony rests on 13 syllables in all, in three records, the same one or two in each chorus of a song (song 59: the syllable before "with" and "with" itself, in every chorus). No song loses more than one syllable in eighteen.
- **H3: eight records as good or better; song 59 misses by 0.0012.** Unrounded, its miss goes from 0.0842 to 0.1154, a rise of 0.0312 where 0.03 was allowed. Under form 1 the rise was 0.074, under (a) 0.093. Resting the six syllables where nothing fits under the lead takes back most of what the first two forms lost, and not quite all.

**It is a miss.** The mark was written before the run, a rise of more than 0.03 is a rise of more than 0.03, and the stopping rule says no fourth form. I record it without softening and close the item for the version.

**What stands on the list, for a later version.**
- The engine's harmony goes over the lead in three records of nine (once in song 54, twice in song 59, twice in song 66's A minor run), always where no kept interval under the lead lands on a chord tone.
- A form that never crosses, keeps a stated range, rests on those few syllables and starts its fit from the present weights fits kept interval shares better in seven records and within the margin in an eighth; song 59, whose choruses put the lead at the bottom of the range, is 0.0012 over the margin.
- The code for all three forms is in `band.arrange()` behind the `voice` argument, which nothing passes. With it not passed a record re-arranged is itself.
