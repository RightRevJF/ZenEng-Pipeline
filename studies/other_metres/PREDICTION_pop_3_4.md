# A pop-style trial in 3/4: the rule file, before any code or run

27 November 2026, 16:13 ET. Ordered by the songwriting session (16:08 ET) after the writer's word that metre must be kept apart from style. Nothing here has been run.

## The pop tables, rebuilt as asked
`hooktheory_filter.json` was committed first (590d678): the word list and named soundtrack, game and library sources, extended from artist names only, with classical composers added by me. Then the tables were rebuilt from **all** Hooktheory songs outside the filter: **3/4: 267 songs, 6,208 bars** (53 of them in the Discogs join); **6/4 read as 6/8: 342 songs, 5,712 bars** (71 in the join). The test set beforehand: is each figure's median for the joined songs inside the full table's middle half? **Yes for every figure, in both metres.** The full tables stand (`trial_tables/3-4_pop_sung.json`, `6-8_pop_sung.json`, `hooktheory_by_song.json`).

Pop 3/4 by song (267), 10th / 25th / 50th / 75th / 90th:
| | | | | | |
|---|---|---|---|---|---|
| Notes a bar | 2.00 | 2.38 | 2.94 | 3.85 | 5.16 |
| Onsets on a beat | 0.418 | 0.508 | 0.643 | 0.800 | 0.940 |
| Range (a song's clips pooled) | 9 | 12 | 15 | 20 | 26 |
| Distinct pitches | 6 | 7 | 10 | 13 | 17 |
| Commonest pitch | 0.145 | 0.190 | 0.248 | 0.303 | 0.377 |
| Bars on a rhythm already sung | 0.349 | 0.465 | 0.625 | 0.787 | 0.871 |
| Bars on a figure already sung | 0.116 | 0.209 | 0.375 | 0.562 | 0.667 |
A bar lasts 1.44 seconds at the median. These are sections (median 16 bars), not whole songs: range, pitches and repetition are not like for like with a whole song, and a whole song will repeat more than a section does.

## The lyric, by the rule given
"The spent lyric whose median line length is nearest song 68's (7 syllables, lines of 6 and 7)", among our pop and rock lyrics; 65, 67, 68 not candidates. Median syllables a line: song 55 6, song 54 8, song 62 8, song 64 9, song 66 8 (songs 58 and 49 have 7 but are folk). Songs 55, 54, 62 and 66 tie at one syllable off; *settled:* the tie goes to the largest share of lines of 6 or 7 syllables (55: 0.43; 62: 0.42; 66: 0.23; 54: 0.21). **The lyric is song 55's** ("I'm Your Yard Man", 56 lines, baritone), set in 3/4 with genre rock, at 133 quarters a minute (the pop table's median bar). A seen song; nothing sealed is spent.

## The form
The metre-level forms as read, the style from the pop table:
- the plan form (bars from the pop table's median of 2.94 notes a bar; padded phrases, popular style);
- form B (tops and centres), *settled for a table of sections:* no like-length band exists, so the range asked is the pop table's median over all songs (15) and the pick's floor its 25th (12);
- the title's room (0.9) and the copy's join;
- 749.231's rule with **the lead sheets' stress table borrowed** (Hooktheory has no words; said in the record).

## Marks (the songwriting session's K1 to K8), every moved figure on the living builds' median and on the pick
- **K1.** Living 30 or more; pool 10 or more.
- **K2.** Notes a bar inside 2.38 to 3.85.
- **K3.** Onsets on a beat at or over 0.508. Stressed syllables on the first beat at or over **0.471** (the 3/4 lead sheets' by-song 10th, 504 songs). Stressed syllables off the beat at or under **0.159** (their 90th).
- **K4.** Range at or over 12 and distinct pitches at or over 7.
- **K5.** Commonest pitch at or under 0.303.
- **K6.** Bars on a rhythm already sung inside 0.349 to 0.871; bars on a figure already sung at or under 0.667.
- **K7.** In the voice; no leap past an octave in a line. **K8.** Deaths on 780 and 840 each under one in ten.
- **Reported:** each switch off in turn (200 builds); the share of living builds meeting every mark.
- **Byte for byte**, every switch unset: 54, 55, 52, both 3/4 trial records.

(The middle half in K2 is the full table's; your post gave the joined songs' 2.34 to 3.30 before the rebuild you ordered.)

## What I expect
K1 to K5, K7 met: the pop marks are wider than the lead sheets'. **K6 is the question, as you say:** the engine sings lines again (818, the copies) and draws from the commonest windows, and a whole song of 56 lines repeats more than a 16-bar section; I expect rhythm again near 0.85 to 0.9, at or past the mark's top of 0.871, and figures again past 0.667. One chance in four for the whole.
