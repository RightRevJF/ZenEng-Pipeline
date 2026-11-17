# Start here {#start}

This page holds everything the songwriting session learned and wrote while Luthier was offline (14 to 15 November 2026), and since: songs 54 and 55, run on Luthier v7 on 16 November, with their findings (749.24 to 749.31) and test reports (Parts 15 and 16), and an audit of what the engine itself writes, with five research studies for the harmony, band, tension, metre and melody writers v8 needs (Parts 17 to 22). Here: the fix list for v8, the new rules, and every report and study. It is written for Luthier's maintainer, the AI that keeps the spec. Words and music: Jason Bryant.

**For the maintainer:** read Parts 1, 2 and 17 in full. They say what to change. Parts 18 to 22 are the research for the new writers; Parts 3 to 16 are the evidence; go to them when a fix or rule needs checking. The code, data tables and songs are also in the private GitHub repository RightRevJF/ZenEng-Pipeline (folders reports, studies, tables/metre_atlas, songs/p62, songs/p63, songs/p64, songs/p65 and songs/p66; the harmony and arrangement studies are in studies/harmony, studies/arrangement, studies/tension, studies/metre and studies/genre), for anyone with access. This page does not depend on it.

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
| [17](#part-17) | **Luthier audit: harmony and arrangement.** What the engine writes and what an AI has written, item by item and song by song; the gaps; the order of work for v8 and the no-hand-input test |
| [18](#part-18) | Harmony research for Luthier v8: what follows what (the McGill Billboard songs, a prototype chord writer, tested) |
| [19](#part-19) | Arrangement research for Luthier v8: what the band does (the academic record, POP909, the Lakh band by genre) |
| [20](#part-20) | Tension research for Luthier v8: building and releasing tension (models tested against listeners, structure, pop theory, 214 Billboard songs measured) |
| [21](#part-21) | Metre research for Luthier v8: bars, phrases and hypermeter (why lines would not fit in songs 54 to 56; slots in seconds; phrase expansion; weighted text-setting) |
| [22](#part-22) | Melody by genre for Luthier v8: scales, blue notes and the divorce (five-note scales, flat 3 and flat 7 by style, what fix 200 and tri() forbid, songs 54 and 55 against the corpus) |

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

11. **Who writes what (the audit).** In every song since v7 the engine wrote the sung melody and its rhythm, and the bass routine wrote the bass; an AI wrote each song's chord plan and every other band part by hand, and songs 52 and 53 entirely. The goal is an engine that writes everything and uses AI only lightly, so v8 needs two new writers, harmony and arrangement, drawn from measured tables and tested, and a test that fails any song with a hand-typed chord or band note (Part 17).
12. **Harmony (Part 18).** On 739 Billboard songs each section kind has a sharp job (verses open on I three times in four, bridges end on V nearly half the time). A simple model of what follows what, trained on 592 songs, already passes as real on major-key verses and choruses; minor keys, bridges and pre-choruses need more data, and the writer needs a loop step, since real sections repeat a two- or four-bar cell.
13. **The band (Part 19).** Real intros carry about 70% of the fullest band; the chorus lifts by playing more notes (busier than the verse in 88% of 909 songs), not by moving higher; the bass plays about once a beat at any tempo; every genre's commonest snare bar is 2 and 4, and genre shows in kick patterns, bass syncopation and piano voicing. The best published systems draw real phrases and fit them to new chords, which is how v8's band writer should work.

14. **Tension (Part 20).** Harmonic tension and energy are two curves. In 214 Billboard hits the chords are most tense in the pre-chorus and bridge, with V just before each chorus and I on its first bar, while listeners' energy peaks in the chorus; both build late (about 0.68 and 0.74 of the song). v7's 1-to-3 chord value predicts nothing; models that fit listeners read trends and give harmony a memory of 20 to 30 seconds. v8 should plan both curves before writing and gate its writers by them.

15. **Metre above the bar (Part 21).** All four placement failures of songs 54 to 56 come from fixing a line's length in bars before the words are known. In 9,313 lines of 198 Billboard songs, lines are timed in seconds: slow songs give a line fewer bars (6 to 8 syllables in one bar 36% of the time, against 6% in fast songs). v8 should set slots in seconds, choose the felt tempo at intake, let phrases expand, overlap or shrink at kept rates, and place words by weighted rules (Hayes) instead of failing. This closes 749.25, 749.30 and 749.31.

16. **Melody by genre (Part 22).** v7 writes every melody from the 7-note scale and forbids the flat third against a major chord (fix 200) and the flat fifth (tri()). In 165 major-key Billboard songs the typical melody puts 85% of its notes on one five-note scale, notes fix 200 forbids appear in 63% of songs (69% of soul songs), and tri() mostly blocks plain diatonic notes. Songs 54 and 55 have no flat 3 or flat 7, and song 54 sings the leading tone at three and a half times the country rate. v8 should take its pitch table from the style, place flat 3, flat 7 and flat 5 where soul and blues put them, narrow tri(), and treat the leading tone as a moving note.

The main new idea: **judge every song on two channels**, what audiences reward and what musicians reward, and prefer songs that do well on both.

## Still open

- Song 53 (Sung to Sleep): a one-note change to the refrain's re-entry is offered and waits for Jason's approval; the blind pick is still to come; the engine's own rerun waits for v8.
- Song 54 (The Man Mama Prayed I'd Be): delivered; blind pick taken (Middle); a made-for-real rerun is offered.
- Song 55 (Your Yard Man): delivered; blind pick taken (Remembered, the hook); a made-for-real rerun is offered.
- Song 52 (The Room Next Door) and song 53 were written outside the engine, so v8 should be able to write them itself.
- Song 56 (Terpsichore, a soul ballad): lyric locked and mouth-tested, and the engine's melody runs are done; the song waits for v8's harmony and band writers, so that the engine writes all of it.

## Data and cautions

YouTube data is kept only as results: no comment text, usernames or audio. The Session's tune data is not used, since its licence bans processing by AI. Every effect found is a few percent of the variance at most, so the new rules are targets and tie-breakers, not laws.
