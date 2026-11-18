# Review of Luthier v9 stage 2a (branch luthier-v8-stage1, 3850f18), by the songwriting session, 18 November 2026

Merged into main (merge commit; stage 1 was already merged on 18 November) at the writer's instruction ("Please review and merge both").

## What was checked

| Check | Result |
|---|---|
| Every .py compiles; no .pkl, src/, out/ or key | yes; none |
| gen_l9.py on song 57's v7 file gives the committed melody_l9_p67.py | byte for byte |
| Song 55 main, 1,000, from the committed engine (songs/p65/runl9/review_main_v9.txt) | order 4f5d2cd5bbd8, 496 survivors, 53 placement deaths, pick a09b4cc4fd3a, 18 eligible: the log and Table FT |
| Song 54 main, 1,000 (songs/p64/runl9/review_main_v9.txt) | order 9a5743a02cde, 580 survivors, 0 placement deaths: the log and Table FT |
| slots.py, propose() | runs; song 57's lines at 112 bpm: two bars proposed for every line of 9 to 14 syllables, as written |

## Why the two gates now take the most builds (766, as asked)

**Song 55, the join before a copy (212): 310 of 1,000.** A trace of 300 builds (songs/p65/melody_l9_p65_trace212.py; 428 such deaths
logged with the line, its source and its neighbour) puts them in four places: chorus 2's lines 2 to 4, each a copy before a copy
(273 of 428); chorus 3's line 3, sung again (89); the hook's last line before verse 2 (58); verse 1 (8). The cause is one rule read two
ways. The join *before a line* lets the line enter after the breath 631 drew for the line before (as little as 3 twelfths in a dense
one-bar cell). The join *before a copy* asks GAP_MIN (18 twelfths) when the line before is itself a copy or a design, and that line's
own freshly drawn breath when it is fresh or sung again. So chorus 1's lines 2 and 3 can join legally a beat apart (the last onset at 36,
the next line on the downbeat: 12 twelfths), and chorus 2, copying both, dies on the same notes. Chorus 3's line sung again carries
chorus 1's rhythm but draws its own breath (24 to 30) for a join the source made in 12. The hook ends on beat 4 and verse 2, sung again,
enters a sixteenth after the downbeat: 15 twelfths against 18. Placement hid this: in v8 most of these builds died earlier.

**Song 54, the chorus above the verse (the writer's design: chorus 1's median, the hook aside, two semitones over verse 1's): 346 of
1,000.** It is not new. It took 124 of the 348 builds that reached it on v8 (36%) and takes 346 of 1,000 now (35%). It is decided by the
verse, not by the drawn lift. The chorus's lines under the hook sit at a median of 54 or 55 in nearly every build (spread 1.8 semitones),
because the hook's D4 is the chorus's top and the song's; the register draw asks a lift of about 8 semitones that the chorus cannot take.
The verse's sung median follows its drawn centre only loosely (r = 0.31) and spreads more (2.2). Builds whose verse sings at or under
52 die 3% of the time; 52 to 54, 19%; 54 and over, 78%.

## Findings (from 749.42; 749.35 was closed and 749.40 and 749.41 numbered in the fix list since v8)

**749.42. The join before a copy asks more than the source's join.** *Problem:* 212 reads a copied pair with GAP_MIN or a fresh breath,
where the pair it copies was joined under 631's drawn breath. *Evidence:* above; 273 + 89 of 428 traced deaths on song 55. *Fix:* a line
before a copy keeps the join its source kept (when both lines are copies or sung-again of a pair that joined legally, the copy's join
is the source's), and 765's least breath applies to the copy's join as to the line's. *Check:* song 55's deaths at 212 fall to the
hook-to-verse case or below; no copied pair dies on notes its source sang.

**749.43. The hook-to-verse join on song 55 is a design collision.** *Problem:* the designed answer ends on beat 4 and verse 2 enters
a sixteenth after the downbeat (15 twelfths against 18). *Evidence:* 58 of 428 traced deaths. *Fix:* either let verse 2's entry move
to the downbeat or later when the line before is designed, or read the join at the least breath the kept songs allow after a held
note. *Check:* no build dies at Chorus 1 line 10 before Verse 2.

**749.44. The chorus-above-the-verse design is decided by where the verse sings.** *Problem:* on song 54 the chorus is held under the
hook's top and barely moves; the design passes or fails on the verse's median, which the register draw does not hold. *Evidence:*
above. *Fix:* draw the verse's centre from the chorus's reachable median (at or under the chorus median less the design's lift), or
hold the verse's walk near its centre; or check the design at intake as a constraint on the verse. *Check:* design deaths on song 54
under one build in ten.

**749.45. Small things.** The stage-2a logs record code hashes the committed engines do not give (song 55: 745cf9220e7c against
276d01acc0ce), though both songs rerun to the logged results; and `slots.py`'s command line reads the bars given as syllables
(`slots.py 112 13 10 7 2 2 1` proposes slots for lines of 2, 2 and 1 syllables). *Fix:* commit logs from the committed engines; parse
the given bars after a separator. *Check:* hashes match; the command line flags a short slot.
