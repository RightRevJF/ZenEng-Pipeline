# Luthier fix list since v8

18 November 2026 · Jason Bryant. Live copy: the Doc https://claude.ai/artifact/RsLofQqXxtUqSMFu61sAyy

The songwriting session's findings since Luthier v8 stage 1 (Module 27.89, Window 165, fixes 750 to 755), for the maintainer. Stages 1 and 2a (Luthier v9, Module 27.90, fixes 760 to 766) are merged into main; 749.35 is closed; six new findings, 749.40 to 749.45. The maintainer's message of 18 November still had 749.35 open and new numbers from 749.40: both are settled here. Words and music on every song: Jason Bryant.

## Stage 1 review

Branch luthier-v8-stage1 (c1ce8e2) was reviewed and merged into main by fast-forward on 18 November. The code does what Window 165 says; the review is lib/luthier/REVIEW_stage1.md.

| Check | Result |
| --- | --- |
| Every .py in the branch compiles | yes |
| No .pkl, src/ or out/; no key | none |
| gen_l8.py on song 57's v7 file | gives the committed melody_l8_p67.py byte for byte |
| Song 49 main, 1,000, from the committed engine | order 00ab881be2a7, 671 survivors, 752's pick a4e59c5f298c, 69 eligible: Table FS exactly |
| Song 57 on v8, 40-build smoke | runs; 14 survivors; order 858e793a8e20 |
| 750 | keeps only rhythms whose onsets rise strictly inside the bar |
| 751 | evaluate's notes are in onset order, so the doubled-onset test is sound |
| 753 | sleepin', callin', nothin', 'n', 'cause, a.m. and p.m. read as meant (but see 749.41) |

The branch also commits the spec itself (reports/Luthier_v8.docx); no finding.

## Stage 2a review (Luthier v9)

Stage 2a (3850f18; Module 27.90, Window 166, fixes 760 to 766) was reviewed and merged into main on 18 November (a7447c2). The review is lib/luthier/REVIEW_stage2a.md.

| Check | Result |
|---|---|
| Every .py compiles; no .pkl, src/, out/ or key | yes; none |
| gen_l9.py on song 57's v7 file gives the committed melody_l9_p67.py | byte for byte |
| Song 55 main, 1,000, from the committed engine (songs/p65/runl9/review_main_v9.txt) | order 4f5d2cd5bbd8, 496 survivors, 53 placement deaths, pick a09b4cc4fd3a, 18 eligible: the log and Table FT |
| Song 54 main, 1,000 (songs/p64/runl9/review_main_v9.txt) | order 9a5743a02cde, 580 survivors, 0 placement deaths: the log and Table FT |
| slots.py, propose() | runs; song 57's lines at 112 bpm: two bars proposed for every line of 9 to 14 syllables, as written |

Why the two gates now take the most builds (766): song 55's join before a copy comes from 212 reading a copied pair more strictly than its source was read (749.42), plus one design collision (749.43); song 54's design fails at the same rate as on v8 and is decided by where the verse sings (749.44).

## Findings

### 749.35 (closed). Evaluate seemed to disagree with the run

**Problem:** on song 57, 102 of the 277 builds the session took as clean survivors failed evaluate when it ran again on their stored notes, all but a few on 267 (the bridge's line 5 returning line 1).

**Evidence:** two causes, neither the engine's judgement.

- The session's pick script read the run's record of builds (`all`) as its survivors. The record holds every build that reached evaluate, and 32 of the 277 had been killed there (key word on a chord tone, the chorus or bridge opening another tune, limits).
- The run stores each note without `moved386`, the pitch 386 leaves on a note it moves, and 267 reads a return before 386's moves. Evaluate run again on a stored build therefore fails 267 wherever a return line had a 386 move: 72 true survivors.
- A run of song 57 on v8 that stores every note field (songs/p67/melody_l8_p67_trace.py; the same order, 39364f77a34e, and 295 survivors as without them): all 242 of its clean survivors pass evaluate again with `moved386` restored, 179 with it dropped. Every other note field changes nothing.
- Read on the correct 247 survivors, song 57's pick is unchanged (be9dba1f3d5c). The session's pick script now reads survivors as builds with no cause.

**Fix (proposed):** the run stores `moved386` with each note in its record (`notes=[(on, dur, p, sec, line, stress, syl, moved386)]`), and every reader of the record takes survivors as builds whose cause is empty.

**Check:** every clean survivor of a run re-evaluates clean from the stored record.

### 749.40. The committed stage-1 run logs predate 752

**Problem:** songs/p59, p60, p61, p64 and p65's runl8/run_*.txt were made before the pick moved to luthier_judge6.

**Evidence:** song 49's log records code e545ed727af5 where the committed engine reads 68e55733a5b0, and prints 730's pick (3ef101ca2544) and 447 eligible where 752 gives a4e59c5f298c and 69. Songs 51 and 54 differ the same way; songs 50 and 55 happen to agree. The orders are unaffected. The review run from the committed engine (songs/p59/runl8/review_main_v8.txt) gives Table FS exactly.

**Fix (proposed):** make the five runs again from the repository, or mark the logs as made before 752.

**Check:** every log's recorded code matches its engine.

### 749.41. 753's a.m. rule catches a sentence's last 'a'

**Problem:** lib/carol/lyricsearch.py's words() rewrites any "a." followed by a word beginning with m, and the same for "p.".

**Evidence:** "it was plan a. make it work" reads it, was, plan, ayem, ake, it, work.

**Fix (proposed):** match a.m. and p.m. only when the m is followed by a full stop or ends the word, and the next character is not a letter.

**Check:** "plan a. make" reads plan, a, make; "up at 5 a.m." reads ayem.

### 749.42. The join before a copy asks more than the source's join

 *Problem:* 212 reads a copied pair with GAP_MIN or a fresh breath,
where the pair it copies was joined under 631's drawn breath. *Evidence:* above; 273 + 89 of 428 traced deaths on song 55. *Fix:* a line
before a copy keeps the join its source kept (when both lines are copies or sung-again of a pair that joined legally, the copy's join
is the source's), and 765's least breath applies to the copy's join as to the line's. *Check:* song 55's deaths at 212 fall to the
hook-to-verse case or below; no copied pair dies on notes its source sang.


### 749.43. Song 55's hook-to-verse join is a design collision

 *Problem:* the designed answer ends on beat 4 and verse 2 enters
a sixteenth after the downbeat (15 twelfths against 18). *Evidence:* 58 of 428 traced deaths. *Fix:* either let verse 2's entry move
to the downbeat or later when the line before is designed, or read the join at the least breath the kept songs allow after a held
note. *Check:* no build dies at Chorus 1 line 10 before Verse 2.


### 749.44. The chorus-above-the-verse design is decided by where the verse sings

 *Problem:* on song 54 the chorus is held under the
hook's top and barely moves; the design passes or fails on the verse's median, which the register draw does not hold. *Evidence:*
above. *Fix:* draw the verse's centre from the chorus's reachable median (at or under the chorus median less the design's lift), or
hold the verse's walk near its centre; or check the design at intake as a constraint on the verse. *Check:* design deaths on song 54
under one build in ten.


### 749.45. Stage 2a's logs and slots.py's command line

 The stage-2a logs record code hashes the committed engines do not give (song 55: 745cf9220e7c against
276d01acc0ce), though both songs rerun to the logged results; and `slots.py`'s command line reads the bars given as syllables
(`slots.py 112 13 10 7 2 2 1` proposes slots for lines of 2, 2 and 1 syllables). *Fix:* commit logs from the committed engines; parse
the given bars after a separator. *Check:* hashes match; the command line flags a short slot.

## Carried from the final report

Song 57's findings came in Part 33 of the final report (songs/p67/test_report_p67.md) and are open, for the maintainer to stage under 755. Their numbers are unchanged since the report except 749.32's and 749.34's counts, now read on the correct 247 survivors.

| Finding | In one line |
| --- | --- |
| 749.32 | No build reaches Part 31's long-note band: 0 of 247 clean survivors, best 0.74 against 0.75 |
| 749.33 | The title line has no hook gates: low and narrow, its stresses on a beat 38% of the time, held no longer than the median note |
| 749.34 | The chorus barely lifts: the pick +0.34 semitones over its verse; 51 of 247 at or under it |
| 749.35 | Closed above |
| 749.36 | 749.21's limit empties the band under a low lead; 749.27's reading used instead |
| 749.37 | The band's level curve does not read the lyric: the bridge, the song's low, sits above both verses |
| 749.38 | Two-bar slots leave long rests: rest share 0.48 against 0.125 (Part 21's slots in seconds, stage 2) |
| 749.39 | The three prototype writers (writers/chords.py, band.py, solo.py) are ready to port at stages 4 and 5 |

## Regression line

The v8 stage-1 orders (main / control), from the maintainer's runs; picks from Table FS. The orders do not depend on 752, so 749.40 leaves them standing; song 49's main order and pick were reproduced here.

| Song | Orders, main / control | 752's picks, main / control |
| --- | --- | --- |
| 49, The World Is Asking | 00ab881be2a7 / 7195086ea1e2 (main reproduced) | a4e59c5f298c / 3e054366b0ae |
| 50, The Small Things | 7ab47c58826d / 5273c53556de | 4f51e116a9ad / 1065fb53dfd7 |
| 51, A Wire Pulled Tight | cd18f4df32dd / d0509fe1a54d | 453713f5add8 / 793cb5781833 |
| 54, The Man Mama Prayed I'd Be | 7857816fc633 / f4d6ecc1ef4d | a7b011847a5b / b22dcad87e05 |
| 55, Your Yard Man | b5f29da59adf / d8cea6f59772 | 31f951208a8d / 6c0ba31f9476 |
| 57, Jehovah's Band (v8, main only, the trace file) | 39364f77a34e, 295 survivors | not taken; the pick of record stays v7's, be9dba1f3d5c |

## Running total

- **Findings since v8:** 7 (749.35 closed; 749.40 to 749.45 open). Next new finding: 749.46; the paper's next fix: 770. Closed by v9 stage 2a: 741, 747, 749.3, 749.25, 749.30, 749.31.
- **Carried open from the final report:** 7 (749.32 to 749.34, 749.36 to 749.39).
- **Songs on v8:** none written yet. Song 58 starts from an l9 file (lib/luthier/gen_l9.py), its slots proposed by lib/luthier/slots.py with the flags printed.
- **Ported by the session since v8:** nothing, as asked; stage 2b, then stage 3 (metre and hymns), come next from the maintainer.
