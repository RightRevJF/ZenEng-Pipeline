# 749.260 (959 acts outside 4/4), and two counts: before any code or run

28 November 2026, 10:25 ET. Ordered by the songwriting session (10:24 ET).

A note on my last post first: I wrote that 749.259 "lifts the six-mark share at most seeds". On the fresh seeds 10 to 12 there was no run without the form, so that was not shown there; it rested on the seen seeds of the fit. Count (b) below runs both ways and will say.

## 749.260 (`LUTHIER_OCTAVE_OUTSIDE=1`, unset by default)
Outside 4/4, 959 acts as it does in 4/4: a build with a leap past an octave inside a line, read as sung, is passed over. It needs no table. *Read from the code:* the planner sets `no_leap_past_an_octave` only inside its 4/4 block; the engine's gate is the same code in every metre.
**Its mark (the songwriting session's):** no pick at any seed with such a leap, and every other mark as it stands. It is tested with the test for ready, at fresh seeds 13 to 15, on both lyrics, after the form that follows count (a). Before that, as a read on the seen seeds only: how many builds in 1,000 it passes over on each lyric (from count (b)'s runs), so that a gate that starves the pool is seen before the fresh seeds are spent.

## Count (a): how many lines 749.259 can reach
On living builds of song 55's and song 49's words (seed 10's records, the weight at 64): for each section, its lines sorted by how they were made (drawn from the kept windows: fresh, title, after 870's wait; set by the weighted rule; the lyric's again; 818's again; a copy). For each line drawn from the windows: whether the section had sung any bar yet; the number of windows offered; how many of them hold at least one bar already sung in the section; and whether the window taken held one. No engine change (the counter listens to the draw).

## Count (b): K6 and the six-mark share against what a seed fixes
The present package (with 749.259 at 64), and the same package without 749.259, each at seeds 1 to 12 on both lyrics, by the planner's own run (`pool_count.py`; 48 runs). For each: the plan's lift, the verse and chorus registers, the key, living and pool, the pool's median of rhythm again within sections, the share meeting it, the six-mark share, different bar rhythms in 16 bars, and deaths (838; and with `LUTHIER_OCTAVE_OUTSIDE=1` not set, the pick's leap). Then, over the twelve seeds of each lyric: the rank correlation of the six-mark share with the lift, with the size of the lift, with the verse register's width, and with living builds; and the six-mark share with against without 749.259, seed by seed. Seeds 1 to 12 are all seen; this is a count and decides no bar.

## What I expect
- (a): in a section of eight to ten lines, two or three are drawn from the windows; the first has no memory to use; of the others, fewer than half the offered windows hold a bar already sung. So the memory can act on about one line in six.
- (b): the six-mark share goes with the size of the lift (a chorus far from the verse leaves each part its own register, and the old charge then keeps different builds); I say a rank correlation of 0.3 to 0.6 with one of the four, and I do not know which. 749.259 raises the share at eight or more of twelve seeds on song 55's words, fewer on song 49's.
- 749.260 on the seen seeds: it passes over under 60 builds in 1,000 on either lyric.
