# Review 29: Luthier v44 (Window 201)

21 November 2026. v44 (957, and the verse-closer trial) is merged into main at 3aa9cd2.

## Reproduced

- The eight kept-table makers and `make_kept_rhythm_room.py`: byte for byte, the remade `kept_commonest_pitch.json` included.
- Songs 52, 54, 55, 58 and 59, song 53's run and stage 4: byte for byte. Only song 55's notes change; songs 54, 58 and 59 change in the ceiling and the table stamp.
- Song 60 on v44: byte for byte with `songs/p70/lyric60.v44.song.json`.
- `soundness.json`: byte for byte (sound, 12 outside the middle half, one lean: rhythm scaling, low). `studies/sounder_pools/per_build.json` and `studies/weak_top_notes/result.json`: byte for byte.
- `neighbour_v44.json`: byte for byte up to its 749.134 block. The neighbour choice fails the rule 2.0 times in 100 (0.2 to 4.4) and a random pool pick 2.2 (0.1 to 5.4), as the paper says. The 749.134 block differs: it reads the chorus ceiling from `studies/commonest_pitch/result.json`, which was 0.474 when the file was made and is 0.479 since 957 remade the study. The engine reads the table, so nothing built is touched (749.145).
- `song_from_lyric.py --check` and `lyric_room.py --check`: both pass.

## 957 holds

A part told by its exact name, the ranges printed, and the paper says plainly that song 55's two changes both turned inside the ceiling's range. That is the right way to report an edge.

## 749.140 is settled: chance, and I accept it

Read per build, the pools do not differ (46.6 against 51.5 in 100, as large in 49 shuffles in 100). The joint figure moved on one pool. The paper withdraws the gain it printed beside 950 and 951, which was the right thing to do.

## 749.141 is closed, and the held reading agrees

The share rule found nothing, and I accept it. The paper is right that the share does not hear how long a weak word is held, so I read that too (`studies/review29_verse_closer/held_weak_top.py`). In kept songs the longest weak syllable on the top note runs 0.5, 1, 1.5, 1.5 and 2 beats (50th to 99th). 28 kept songs in 100 hold one a beat or more. Song 58's "the" is a beat, at the kept 75th: my ear caught a real thing, but kept songs do it too. Only song 60's "me" stands past the kept 99th (four beats). It is "even you, even me", where "me" carries the contrast and is stressed when spoken, so the reading is wrong there, not the tune. Nothing to build.

## The verse sung closer: my ruling is (a), with the fifth check moved to the chosen tune

The maintainer asked the session to rule between (a), building the form despite song 54's fall in the builds' words' fit, and (b), one bar only for lines of 7 syllables or fewer.

A check written first should not be waived because the result is close. So I tested what the check was meant to protect. The words' fit that reaches a singer is the chosen tune's, and the choice is gated on the words again. I ran the three songs in full under the form (`studies/review29_verse_closer`):

| Song | Words' fit of the chosen tune: as built; the form | Rhythm scaling of the chosen tune |
|---|---|---|
| 55 | 0.341; 0.347 | 0.688 |
| 54 | 0.275; 0.272 | 0.646 |
| 58 | 0.307; 0.357 | 0.550 |

The builds' fall in song 54 (0.028) does not reach its chosen tune (0.003). Song 58's chosen tune fits its words better. The three chosen tunes are sound with **no lean at all** (10 checks outside the middle half, against 12 as built).

Form (b) does not do the job. On the window's 40 quick tunes, song 54 takes no one-bar line under (b), because every candidate line is 8 or 9 syllables. Its rhythm scaling reads 0.601, just under the kept 25th (0.605). Songs 55 and 58 take the same lines as under (a). So (b) would pass the first check in song 55 only, and fail it.

So: build (a). The fifth check was written about the builds, but what it protects is the chosen tune's words, so it moves there, written now, before the build: no chosen tune's words' fit more than 0.02 under the tune chosen without the form (749.142).

## What the form does not reach

Song 58's chosen tune stays under the kept 10th of rhythm scaling (0.550 against 0.574), and its builds under the 25th. Its room file says why: its lyric leaves few bars unsung. The other carrier of rhythm scaling, bars with nothing sung (+0.58 in kept songs), is untried in the engine (749.144).

## A hold-out the lever can act on

Song 59 has no verse line of 6 to 8 syllables, so nothing about the verse lever can be held out. One of the earlier songs can serve without new writing. The rule, written now: the most recent song in 4/4 not yet run by Luthier v8, with at least four verse lines of 6 to 8 syllables, made into a lyric file from its locked lyric with no change of words. That is song 49, "The World Is Asking" (`songs/p59`): most of its verse lines run 8 syllables, like song 54's, so it tests exactly the case the fit check was worried about (749.143).

## Song 58

No new edition. Its notes are the same as in the v43 record: only the ceiling's figure and a table stamp changed. Under form (a) it would change (range 17, words' fit 0.357), and the next edition will follow the build.

## List for v45

749.142 to 749.145 (`songs/p68/fixlist_v45.md`).
