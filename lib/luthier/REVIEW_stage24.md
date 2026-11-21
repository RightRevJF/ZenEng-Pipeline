# Review 24: Luthier v37 and v38 (Windows 194 and 195)

20 November 2026. v37 (fixes 940 to 942) was not relayed separately, so it is reviewed here with v38 (943, built in and withdrawn, now off). Both are merged into main at 0fe5991.

## Reproduced

- The six kept-table makers (kept_plan, make_kept_4_4_tables, make_kept_line_ends, make_kept_page_gate, make_kept_returns, make_kept_word_weight): byte for byte.
- Songs 52, 54, 55, 58 and 59, song 53's run, and stage 4: byte for byte as v37 left them (PYTHONHASHSEED=0, /tmp/rerun/run15.sh).
- `soundness.py` on songs 55, 54 and 58: `soundness.json` byte for byte.
- `neighbour.py` (OUT_SUFFIX=_v38_check): byte for byte with `neighbour.json`, ranges included.
- With BORROW_FIT = None the engine is v37's. 943's code was read; the in-engine run with it on was not repeated.

## v37

**940 (the ranges) holds**, with one weakness (749.124). The neighbour choice's range is read on 200 inner draws per resample. At a rate of 1.5 in 100, 200 draws alone give a binomial 90% range of 0.5 to 3.0, nearly the whole published range (0.0 to 3.5). So most of that range is the inner draws' noise, not the pools'. It did not mislead the 943 decision, since 943's range (4.0 to 18.5) sits clear of it, but a smaller effect would hide inside it. The random pool pick uses 1,000 inner draws and is less affected.

**941 (each weight on its own) holds.** Song 54's fit keeps round 5 (step 1.343, leap 1.797, repeat 0.603). Its fresh lines step 0.570 against the band's edge of 0.558, inside the 0.03 allowance, and its builds' repeated notes are 0.191 against the kept 25th of 0.210.

Song 60 confirms it out of sample. Under v36 its fit kept round 1, the weights were never fitted, and the pick chanted (verses on one note 70 in 100, a run of 10). Rerun under v38, its fit keeps round 6 (repeat weight 0.368), and the pick no longer chants: its commonest verse note is 30 in 100, its longest run 7, and it is in key G. The v38 record is kept as `songs/p70/lyric60.v38.song.json`; the delivered first edition stays on the v36 pick, which the writer chose by ear.

**942 (the melismas carried) holds.** The gain is small and costs nothing, as the paper says.

## v38

**Is withdrawing 943 right? Yes.** The standard is the soundness rule read on the pools, and both pool figures with 943 on sit clear of v37's ranges (neighbour choice 10.2, range 4.0 to 18.5, against 1.5, range 0.0 to 3.5). The cause is named and measured: one check, rhythm scaling, with all three songs under the kept 10th together. A fit that passes its trial outside the engine but breaks the pools inside it should not stay in.

One door is worth leaving open, though not opening now. The failure comes from more borrowing; the hold-out gained from less (its fit chose no figure borrow, its gap halved, and 35 in 100 more builds passed the gates). A one-sided 943, allowed to lower the borrows but never to raise them, cannot make the failure the paper measured. But it is a rule written after seeing the results, so if it is ever tried, it needs its own rule first and new draws.

**The method caution.** Looking at reach.py before writing the rule is a real fork, but a small one here. reach.py shows how far the dial can move the readings, not which setting wins, and the safeguard taken was the right one: a directional prediction on the hold-out, against the grain of the practice songs, written before the trial. The amendment after the first trial tightened the rule (the fit may not buy bars with the words) and was read on new draws, which is the acceptable way to amend. And the in-engine standard failed anyway, so nothing rests on the fork. For the future: write in each PREDICTION file what was looked at before it was written. When a dial has been looked at, read the result on a song nobody looked at.

**"There was no fault of repetition" is stated too strongly.** The amount is near the kept middle but leans low. Bars on a rhythm sung before, in songs 55, 54, 58, 59 and 60 (v36, v38): 0.416, 0.557, 0.629, 0.478, 0.443, 0.486 against kept quartiles of 0.454, 0.588, 0.685. Four songs of five sit under the kept median and two under the 25th.

The clearer finding is in near.py's own rows: **where the repeats come from** (749.123). Of the bars sung on an earlier rhythm, the share whose source lies more than 16 bars back is 0.595, 0.656, 0.455, 0.545 and 0.645 (0.611 under v38). That is more than 90, 94, 66, 85 and 94 kept songs in 100; the kept median is 0.378. Repeats from within 8 bars sit at the kept 19th, 24th, 64th, 28th and 21st percentiles. The hold-out and song 60 show it as plainly as the practice songs.

Luthier repeats by whole sections returning. Its verse 2 matches verse 1 on rhythm more closely than 72 to 81 kept songs in 100 (match.py). Kept songs repeat more nearby, a bar answered a few bars later. This is not a proof of the rhythm-scaling cause, but it is the shape the next study (how kept songs that repeat much keep a high rhythm scaling) should start from. Those readings are from v38's own outputs and records; no dial was turned for this review.

## Song 58, fourteenth edition

From the v37 record (v38 leaves it byte for byte): A major, A2 to A3, its top note 5 times (25 in the thirteenth edition; Bird Dog twice). Bars on a figure already sung 0.543, on a rhythm already sung 0.638 (Bird Dog 0.698, 0.774). Rhythm scaling 0.507, under the kept 10th. Length 337 seconds, past the kept 75th (243). All 44 document checks pass. The thirteenth edition is kept in `songs/p68/out/thirteenth_edition_v36/`.
