# Luthier fix list for v29 (since v28)

19 November 2026. Luthier v28 (fixes 913–915) is reviewed (`lib/luthier/REVIEW_stage15.md`) and merged into main at 88f4091. Every record reproduces byte for byte. Song 58 is rebuilt from its v28 record (sixth edition, B, guitar capo 2 with A shapes; 44 of 44 document checks pass). Two new findings (749.93, 749.94), one carried (749.61), and the fixed soundness checks. Next finding 749.95; next fix 916.

## The v28 list against the v28 records

| Finding | Fix | Closed? |
|---|---|---|
| 749.90 the beat | 913 | yes: stressed syllables on a beat 0.545 / 0.504 / 0.597; fit whole, by place and by height in the kept middle half |
| 749.91 the gate as sung | 914 | yes: the gate's melismas are the record's |
| 749.92 run-ons | 915 | yes: over 12 beats 0.041 / 0 / 0; song 55's 17-beat phrase is one line |
| 749.61 6/8 | none | carried |

Songs are given in the order 55 / 54 / 58.

## When is it finished

`studies/soundness/SOUNDNESS.md` sets out 23 fixed checks, each read the same way on the 160 kept songs and on the three 4/4 records:
- the words' placing and fit (5);
- rhythm (6);
- pitch (6);
- breath and line ends (4);
- the chorus's lift and rest share (2).

The test is a lean of the engine, not every check in every song's middle half. A kept song is outside its own middle half on about half the checks, so that bar would fail almost every real song.

**Sound** means:
- no check has all three songs beyond the kept 10th or 90th on the same side; and
- no more than two checks have all three beyond the 25th or 75th on the same side.

Three kept songs drawn at random fail this 6.8 times in 100. Under v28 one check fails: rhythm scaling (749.93). Once it closes and the rule holds on a rerun, findings are improvements, not faults.

## New findings

### 749.93 The voice never leaves for long, so rhythm scaling sits under the kept 10th
**Problem.** Rhythm scaling is the one check where all three songs lean past the kept 10th. In kept songs it follows how much the density of sung onsets changes across a song, most of all the stretches where the voice stops. The three songs keep the voice going: no silence of two bars or more in 54 and 58, one in 55. That is because 888 drops the turn whenever it would take a song past the kept 75th of lengths, and in all three it would.
**Evidence.**

| | 55 | 54 | 58 | Kept 25th / median / 75th |
|---|---|---|---|---|
| rhythm scaling | 0.546 | 0.547 | 0.532 | 0.608 / 0.656 / 0.721 (10th 0.574) |
| spread of onsets per 4-bar block | 0.236 | 0.137 | 0.250 | 0.353 / 0.438 / 0.554 |
| 4-bar blocks with no sung onset | 0 | 0 | 0 | 0 / 0.082 / 0.129 |
| silences of two bars or more | 1 | 0 | 0 | 1 / 2 / 3 |

Across the kept songs, rhythm scaling goes with the block spread (Spearman 0.65) and the empty blocks (0.56) (`studies/soundness/rhythm_scaling_why.py`). Chorus against verse density is kept-like (0.89 / 0.99 / 1.01 against 0.77 to 1.06), so the gap is in the stretches without the voice, not between sections. Borrowing an earlier line's rhythm moves it the wrong way: song 58's builds read 0.475, 0.463 and 0.436 at a rhythm borrow of 0, 0.2 and 0.4 (`rhythm_borrow_sweep.py`).
**Fix.** Keep 877's silences whatever the length: a turn of two bars between sections, as kept songs leave them (median two a song, three in five between sections). Let 888 shorten the intro and outro first, and drop a turn only when a song would pass the kept 90th of lengths, not the 75th.
**Check.** Each 4/4 song has at least one silence of two bars or more, and rhythm scaling no longer leans: not all three under the kept 10th. Rerun `studies/soundness/soundness.py`.

### 749.94 The songs sit nearer the kept middle than kept songs do (an improvement, not a fault)
**Problem.** Every gate the engine keeps pulls the pick toward the kept middle, so the three songs are more alike the median kept song than kept songs are to one another.
**Evidence.** On the 21 checks read on kept songs, 13 song-checks fall outside the middle half across the three songs. Three kept songs drawn at random have about 30, and about 21 at their 5th percentile.
**Fix.** None required for soundness. When the engine is sound, let one or two readings a song be drawn toward a kept tail on purpose, the way a writer leans a song one way.
**Check.** Over the three songs, song-checks outside the middle half come to at least the kept 5th percentile of three songs drawn at random (about 21), with the soundness rule still held.

## Carried
- **749.61** 6/8: song 52, no build past the joint gate; no kept pop corpus in 6/8.

## Known, not findings
- The chorus's lift leans high in all three songs (5 / 8 / 8 against a kept 75th of 4), the second of the two leans the rule allows. Song 58's title takes the top of any room (907 as asked).
- Pitch scaling follows the lift, as in kept songs (with a lift of 8 or more, kept median 1.115; song 58 1.20).
- Song 55's fit by length is past the kept 90th, one song.
- Songs 54 and 58 are past the kept lengths (the lyrics).

## Order of work
1. 749.93, then rerun the soundness checks. 2. 749.94, once the rule holds. 3. 749.61.

## Songs

| Song | Folder | Under v28 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 326 s; key B, capo 2, A shapes; stressed on a beat 0.597; sixth edition rebuilt from this record |
| 55, Your Yard Man | p65 | 240 s; key E; stressed on a beat 0.545 |
| 54, The Man Mama Prayed I'd Be | p64 | 298 s; key E; stressed on a beat 0.504 |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, and the six kept tables: byte for byte, or the fix says so and commits the new ones. From v29, `studies/soundness/soundness.py` on the three 4/4 records after every version.
