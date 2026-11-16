# Start here {#start}

This page holds everything the songwriting session learned and wrote while Luthier was offline (14 to 15 November 2026), and since: songs 54 and 55, run on Luthier v7 on 16 November, with their findings (749.24 to 749.31) and test reports (Parts 15 and 16). Here: the fix list for v8, the new rules, and every report and study. It is written for Luthier's maintainer, the AI that keeps the spec. Words and music: Jason Bryant.

**For the maintainer:** read Parts 1 and 2 in full. They say what to change. Parts 3 to 16 are the evidence; go to them when a fix or rule needs checking. The code, data tables and songs are also in the private GitHub repository RightRevJF/ZenEng-Pipeline (folders reports, studies, tables/metre_atlas, songs/p62, songs/p63, songs/p64 and songs/p65), for anyone with access. This page does not depend on it.

## What is on this page

| Part | What it is |
| --- | ------------------------------------------------------------ |
| [1](#part-1) | **Luthier fix list for v8 (since v7).** All 41 findings, 740 to 749.31, each with Problem, Evidence, Fix and Check; the songs table; the order of work for v8 |
| [2](#part-2) | **For Luthier's maintainer: avenues and new rules.** The ten new rules with evidence grades, the next avenues ranked, and what not to repeat |
| [3](#part-3) | Metre atlas: kept tables for every common time signature, with round 2 (art songs, lead sheets, Turkish additive metres) |
| [4](#part-4) | Time signature research and song data |
| [5](#part-5) | Accompaniment corpora and music theory |
| [6](#part-6) | Shapes of music like story arcs (research) |
| [7](#part-7) | Shapes of songs: the first study |
| [8](#part-8) | Surprise against expectation and YouTube views |
| [9](#part-9) | Moments people love (timestamped YouTube comments) |
| [10](#part-10) | The rhythm layer |
| [11](#part-11) | Psychoacoustics for the songwriting engine |
| [12](#part-12) | What musicians re-record (covers study) |
| [13](#part-13) | Sung to Sleep (song 53): test report, first to fourth edition |
| [14](#part-14) | Chromatic harmony: views, covers, our songs, hymns and art song |
| [15](#part-15) | The Man Mama Prayed I'd Be (song 54, on Luthier v7): test report |
| [16](#part-16) | Your Yard Man (song 55, on Luthier v7): test report |

## What we learned, in brief

1. **Time signatures.** Pitch habits carry across metres; rhythm habits do not, so the engine needs rhythm tables for each metre. Kept tables now exist for every common metre, and English stress falls on strong beats in each (findings 749.4 to 749.7, 749.15).
2. **Hymns and organ.** Hymn tunes are plainer than folk tunes and need their own mode. Organ accompaniment should be written by the role of each section (749.11 to 749.14, 749.16).
3. **Song shape.** Songs share one shape, a build to a late high point. There are no shape types, and shape says almost nothing about success. Use it as a craft check (749.17).
4. **What audiences reward.** Across 10,847 songs, more predictable melody, chords and rhythm go with more YouTube views, even within one artist's songs (749.18, 749.20).
5. **The moments people love.** Listeners mark moments where the melody thins for a beat or two and then re-enters on a fresh note, a little past the middle of the song. Luthier already has this rule; this is listener evidence for it (749.19).
6. **How it sounds.** Checks for roughness, low crowded chords and the sung tune staying on top. They restate Luthier Module 9.14 and port it to organ and choir (749.21).
7. **What musicians reward.** Songs that musicians re-record most have harmony that moves within sections and melodies with room in them. This is a separate channel from views, found in two sources (749.22).
8. **Chromatic harmony.** Our songs use chromatic chords as single colours, mostly ♭VII. Audiences watch songs with more chromatic harmony less, and musicians do not re-record them more. So it should be a style the engine can choose, not a new default. Hymns and art songs show what each style expects: in hymns, one or two applied dominants a verse are ordinary; art songs live in chromatic harmony at about three times the popular share (749.23).
9. **Back on the engine (song 54).** A country story song on Luthier v7 found the engine assumes a bridge, still loses two-thirds of its builds on long lines with borrowed rhythms, and lets most survivors sing two syllables on one note; the judge picked one, so the pick of record is the judge's own rule without that fault. Two of the new rules need reading by texture and by song type (749.24 to 749.29).
10. **Song 55, a second country song.** The same two-syllables fault decided the pick again (42% of clean survivors), so it is general. Most builds died at the chorus's one-bar lines drawn fresh, a new place for placement deaths, and short lines in two-bar slots can open long rests between their words (749.30, 749.31).

The main new idea: **judge every song on two channels**, what audiences reward and what musicians reward, and prefer songs that do well on both.

## Still open

- Song 53 (Sung to Sleep): a one-note change to the refrain's re-entry is offered and waits for Jason's approval; the blind pick is still to come; the engine's own rerun waits for v8.
- Song 54 (The Man Mama Prayed I'd Be): delivered; blind pick taken (Middle); a made-for-real rerun is offered.
- Song 55 (Your Yard Man): delivered; blind pick taken (Remembered, the hook); a made-for-real rerun is offered.
- Song 52 (The Room Next Door) and song 53 were written outside the engine, so v8 should be able to write them itself.

## Data and cautions

YouTube data is kept only as results: no comment text, usernames or audio. The Session's tune data is not used, since its licence bans processing by AI. Every effect found is a few percent of the variance at most, so the new rules are targets and tie-breakers, not laws.
