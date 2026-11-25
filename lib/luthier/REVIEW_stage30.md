# Review 30: Luthier v45 (Window 202)

22 November 2026. v45 (958, song 49 as a second hold-out, 749.145, 749.146) is merged into main at 06829b1.

## Reproduced

- The eight kept-table makers and `make_kept_rhythm_room.py`: byte for byte.
- Songs 52, 54, 55, 58 and 59, song 53's run and stage 4: byte for byte.
- Song 49 with the form and without it (`lyric49.song.json`, `lyric49.without_958.song.json`): byte for byte.
- Song 60 on v45: byte for byte with `songs/p70/lyric60.v45.song.json`.
- `soundness.json`: byte for byte (sound, no lean, 10 checks outside the middle half).
- `neighbour_v45.json`: byte for byte. 749.145 is mended: the block reads the table.
- `studies/lever_range/result.json`: byte for byte from the committed `studies/metre/cocopops_lines.json`.
- `song_from_lyric.py --check` and `lyric_room.py --check`: both pass.
- Not rerun: the within-artist covers test. Its views and cover counts are not committed (size, YouTube's terms), so it cannot be rebuilt from the repository alone.

## 958 does what it was built to do on the songs it was fitted to

Every check written before the build is met on songs 55, 54 and 58, and every figure is the one my own run gave. The checks were committed before the run, as they should be.

## The hold-out disagrees, and I turn the form off

Song 49 was chosen as the hold-out so that this window could find out whether the form works on a song nothing was fitted to. On rhythm it does: rhythm scaling rises into the kept middle half and bars with nothing sung into the kept range. On the words it does not:

- The chosen tune's words' fit falls 0.116, against the 0.02 the fitted songs were allowed.
- The builds' middle falls 0.040. That is not one noisy draw, and it is larger than song 54's 0.028, the fall that made the maintainer ask for a check in Window 201.

The maintainer raised this case in Window 201, and I set it aside because song 54's chosen tune did not show it. The hold-out shows it, so he was right. A hold-out that fails the check it was meant to guard tells us the form was tuned to the three songs, not to songs in general.

**My ruling: 958 off by default from v46, with its code kept behind the switch.** Turning it off costs nothing against the soundness rule: v44 was sound with one lean, rhythm scaling low, and the rule allows two. Keeping it on costs words on songs nothing was fitted to, and words are what a singer has to sing. The form comes back only as the trial below, if it passes.

## Where song 49's fit fell: in the verses, and more in the lines the form did not touch

I read the engine's own fit line by line on the two chosen tunes (`studies/review30_holdout49/per_line.py`). On the record's notes the whole-song fit reads 0.350 and 0.224; the records print 0.326 and 0.210, from the same notes counted slightly differently. Each line's fit is a rank correlation over eight or nine notes, so only the means are worth reading.

| Mean words' fit of a line | Without the form | With it |
|---|---|---|
| The four verse lines given one bar | 0.269 | −0.034 |
| The twelve other verse lines (still two bars) | 0.536 | 0.068 |
| The rest of the song (30 lines) | 0.370 | 0.502 |
| Parts of the whole fit: length, place, height | 0.278, 0.254, 0.206 | 0.254, 0.200, 0.066 |

Two things follow:
- **The named lines fit worse, as the maintainer said.** Eight syllables in one bar leave little to choose between.
- **The larger fall is in the verse lines the form did not touch,** and in height more than length. That is not explained by "no long note in an 8-syllable bar". Either the draw changed, or a verse that mixes one-bar and two-bar lines draws a worse tune for its two-bar lines.

One chosen tune cannot tell these apart. So the trial must read the untouched verse lines in the builds, where the draw averages out (749.154).

## 749.146 is settled: the range does not widen

The study reads the transcribers' lyric lines, and I reproduced it byte for byte. Kept verse lines of 9 to 11 syllables take one bar 4, 5 and 4 times in 100, against the 8's 9. By the rule written first, the range stays at 6 to 8.

The slow-tempo rise at 10 and 11 syllables (29 and 35 in 100) rests on 24 and 17 lines. Those are about 7 of 24 and 6 of 17, and the 95% ranges of both overlap the slow 8's 21. Too thin to build on, as the maintainer says.

Song 61's remedy is bars with nothing sung (749.144) or the lyric, not this lever. Catching the line-index fault before reporting, and saying so, is the right practice.

## The maintainer's proposed trial: yes, with a fresh hold-out

Taking lines by how often kept lines of that length take one bar at the song's tempo answers what the table showed. The form took 8-syllable lines as readily as 6-syllable ones, and kept songs do not (28, 18 and 9 in 100 at 6, 7 and 8 syllables; 1 in 100 for 8-syllable lines at a fast tempo).

Song 49 can no longer judge it, because it has been seen and the trial is aimed at what it showed. By the same rule as before (the most recent 4/4 song not yet run by this engine, with at least four verse lines of 6 to 8 syllables), the next hold-out is song 50, "The Small Things" (`songs/p60`). It is a swung 4/4 with 14 of its 16 verse lines at 6 to 8 syllables. Songs 51 to 53 do not qualify: 51 has one such verse line, and 52 and 53 are not in 4/4.

The checks are written now, before the trial (749.153).

## From the judging research: holds, narrowly, and I agree with how it is read

The within-artist figure (−0.042, p .009) passes the rule written first by 0.002, and one half of the artists carries it alone (p .16 in the other). The paper says both. I accept "holds" and its reading: it rules out zero and not a small effect.

Two cautions for what follows:
- The chord-writer trial should state its fresh-songs leg and its rule before anything is built.
- Chord surprise, which passed among sixteen measures where about one would by chance, needs its own rule-first test before it is used anywhere (749.157).

## Song 58

No new edition. v45 gave it a new tune, but this review turns the form off, so its next record returns to the v44 tune unless 959 passes and changes it again. The next edition will follow whichever form stands after the trial.

## List for v46

749.153 to 749.157 (`songs/p68/fixlist_v46.md`).
