# Luthier list for v39 (since v38)

20 November 2026. Luthier v37 (fixes 940 to 942) and v38 (943, withdrawn and off) are reviewed together (`lib/luthier/REVIEW_stage24.md`) and merged into main at 0fe5991. Every kept table, all five song records, song 53's run, `soundness.json` and `neighbour.json` reproduce byte for byte. 940, 941 and 942 hold. Song 58's fourteenth edition is built from the v37 record. Next finding 749.123; next fix 944.

## The questions, in short

**Withdrawing 943 is right.** The standard is the soundness rule on the pools, both pool figures with 943 on sit clear of v37's ranges, and the cause is measured: one check, rhythm scaling, with all three songs low together. One door is worth leaving open, though not opening now: a one-sided 943 that may lower the borrows but never raise them cannot make that failure, and the hold-out gained from less borrowing. It would be a rule written after seeing the results, so it needs its own rule first and new draws.

**The method caution.** Looking at reach.py first was a fork, but a small one. reach.py shows how far the dial reaches, not which setting wins. The hold-out prediction written against the grain was the right safeguard, and the amendment tightened the rule on new draws. Nothing rests on it, since the in-engine standard failed. Going forward, see 749.127.

**One correction to the paper.** "There was no fault of repetition" is too strong. The amount leans low: four songs of five under the kept median, two under the 25th. The clearer fault is where the repeats come from (749.123), and that is where the next study should start.

## Items

### 749.123 Where the repeats come from: far back, not near
**Problem.** Luthier's songs repeat by whole sections returning. Kept songs repeat more nearby, a bar's rhythm answered a few bars later. This is the likeliest shape behind the rhythm-scaling fault that withdrew 943, and the paper's next study (how kept songs that repeat much keep a high rhythm scaling) should start from it.
**Evidence.** From `studies/verse_match/near.py`'s own rows, read as shares of the bars sung on an earlier rhythm. Source more than 16 bars back: songs 55, 54, 58, 59, 60 at 0.595, 0.656, 0.455, 0.545, 0.645 (song 60 under v38: 0.611), more than 90, 94, 66, 85 and 94 kept songs in 100 (kept median 0.378). Repeats within 8 bars: the kept 19th, 24th, 64th, 28th and 21st percentiles. match.py agrees: Luthier's verse 2 matches verse 1 on rhythm more closely than 72 to 81 kept songs in 100. The hold-out and song 60 show it as plainly as the practice songs.
**Fix.** In the next study, write the rule first. Read the distance profile (near.py's rows) of the kept songs that repeat most, against their rhythm scaling, and against the builds with 943's settings. If the near repeats carry the high rhythm scaling, the mechanism to try is a bar-level answer within a section (a bar's rhythm taken up two to four bars later), not a whole-line copy.
**Check.** In the study's trial: the share of repeats from within 8 bars moves into the kept middle half in at least two of songs 55, 54 and 58; rhythm scaling does not fall in any; and the pools hold the soundness standard read with ranges. Song 59 read, not fitted.

### 749.124 Give the neighbour range more inner draws
**Problem.** 940's neighbour-choice range is read on 200 inner draws per resample. At 1.5 failures in 100, 200 draws alone give a binomial 90% range of 0.5 to 3.0, nearly the whole published range (0.0 to 3.5). The range is mostly the inner draws' noise, not the pools'.
**Evidence.** Binomial 5th and 95th percentiles: 200 draws at 1.5% give 0.5 to 3.0; 1,000 draws at 3.2% (the random pool pick) give 2.3 to 4.1, against a published 1.2 to 6.1, so that figure's range is mostly the pools'. 943's decision is unaffected (4.0 to 18.5 sits clear).
**Fix.** Raise the neighbour range's inner draws to 1,000, or report the two sources apart: the pool resampling with many inner draws, and the inner draws' own binomial range.
**Check.** v38's neighbour range is recomputed and narrower. The paper says which part of each range is the pools'.

### 749.125 Song 60: the second wide-aim practice song, and an out-of-sample check of 941
**Problem.** 749.111's third trial waits on a second practice song with a wide aim, and the paper asks for more practice songs. Song 60 is one.
**Evidence.** "Everything That Moves" (songs/p70/lyric60.json): 4/4, 116 bpm, baritone, major, soul / r&b (the writer's lane is funk-disco). It aims at It's Raining Men (range 24, a wide aim). Under v36 its fit kept round 1, the weights were never fitted, and the pick chanted (verses on one note 70 in 100, a run of 10). Under v38 the fit keeps round 6, and the pick's range is 19, its longest run 7. The writer kept the v36 pick by ear for the delivered first edition; the v38 record is `songs/p70/lyric60.v38.song.json`.
**Fix.** Add song 60 to the practice songs (fitted to, with 55, 54 and 58) for 749.111's third trial and the soundness rule's pools. Song 59 stays the one hold-out.
**Check.** Song 60's record is in the rerun set and reproduces. 749.111's third trial is read on songs 55 and 60, the two wide aims.

### 749.126 The join before a copy kills most of song 60's builds
**Problem.** 788 of song 60's 1,000 builds die at the join before a copy (780). Its chorus opens with a short line whose words begin the next line ("Everything that moves" / "Everything that moves got the groove").
**Evidence.** `songs/p70/lyric60.v38.song.json` deaths: join before a copy 788, the plan's lift 110, the title's stresses 12. 86 survive. Under v36: 784 at the join, 88 survive.
**Fix.** Trace which join fails (the line, the carried run, the copied line's first note) before choosing a fix. If the short title line's run into a copy is the cause, let the join move the copy's first note a step, as 929 does for a returning line.
**Check.** Song 60's survivors rise by at least half with no other song's record changing, or the trace shows the deaths are right and says why.

### 749.127 Write in each PREDICTION file what was looked at first
**Problem.** v38 looked at the dial before writing its first rule. The safeguard it took (a hold-out prediction) was right, but what was seen beforehand is recorded only in prose.
**Evidence.** `studies/verse_match/PREDICTION.md` and the paper's Window 195.
**Fix.** Each PREDICTION file opens with a "seen before writing" line: which outputs were looked at, and when. When a dial has been looked at, the result is also read on a song nobody looked at.
**Check.** The next study's PREDICTION file carries the line.

## Small things

- Song 60's harmony voice crosses the lead once under v36, by more than an octave (bar 95, G♯4 over G♯3). It is gone under v38 (0 crossings).
- The engine has no funk or disco tables. Song 60 used the soul / r&b family, and its documents added the disco octave bass, sixteenth hats and horn stabs, read from the engine's parts.
- Song 58 runs 337 seconds, past the kept 75th (243); the record's 888 flag notes it.

## Carried

749.109, 749.111 (third trial: see 749.125), 749.116, 749.103 (read as the outcome), 749.101, 749.61.
