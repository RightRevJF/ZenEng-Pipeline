# The metre-free reading, second run: result (27 Nov 2026). By the marks as written, no check is free in both references. Nothing built.

Rule: `PREDICTION_b.md` (commit 7c93010, before this run; the pop side had been seen, the other two not). Figures: `metre_free_b.json`, from `python3 studies/other_metres/metre_free_b.py`.

## The three checks that are gates
"Median" = inside the same-source 4/4 middle half. "Tail" = the gated tail (plainness 10th; commonest pitch 90th) inside the 4/4 tail's bootstrap range; for the leap, the share of tunes against the 4/4 share's range.

| reference | metre | tunes | plainness 10th; 50th (4/4: 10th's range; 50th) | commonest pitch 50th; 90th (4/4: 50th; 90th's range) | tunes in 100 with the leap (4/4 range) |
|---|---|---|---|---|---|
| Essen sung | 3/4 | 943 | -1.03; -0.29 (-0.95 to -0.87; -0.31) **tail out** | 0.256; 0.328 (0.261; 0.328 to 0.339) free | 2.5 (0.7 to 1.7) **out** |
| Essen sung | 6/8 | 593 | -0.86; -0.25 (same) **tail out, on the plain side** | 0.267; 0.350 **tail out** | 0.5 **out** |
| Lead sheets | 3/4 | 66 | -1.61; -0.75 (-1.48 to -1.28; -0.70) **tail out** | 0.207; 0.295 (0.223; 0.297 to 0.331) **tail out, on the safe side** | 4.5 (1.2 to 4.7) free |
| Lead sheets | 6/8 | 10 | -1.28; -0.77 **tail out** (ten songs) | 0.240; 0.298 free | 30.0 **out** (three songs of ten) |
| Pop, against Rolling Stone 4/4 | compound | 41 | -1.36; -0.23 (-0.78 to -0.63; -0.02) **tail out** | 0.273; 0.437 (0.268; 0.388 to 0.460) free | 19.5 (13.6 to 23.5) free |
| Pop, against the kept 4/4 | compound | 41 | **median and tail out** | 0.437 against 0.373 to 0.400 **tail out** | 19.5 (11.6 to 21.3) free |

## By the marks
- **Every median is inside the 4/4 middle half**, in every reference and metre, on all three (the one exception is pop plainness against the kept songs read in-sample). The middles do not move with the metre. That agrees with atlas Finding 1.
- **The tails mostly fall outside the 4/4 tail's range.** So by "free in both references", **none of the three is metre-free**: plainness is out everywhere; the commonest pitch is free in Essen 3/4 and in pop against its own source, out in Essen 6/8 and against the kept table; the leap is free in pop and out in Essen.
- How far out matters and the mark does not weigh it, so I set it down: with 1,397 Essen tunes the 90th's range is 0.011 wide, and Essen 6/8 misses it by 0.011. The leap in Essen is 0.5 to 2.5 tunes in 100: folk tunes hardly have it at all. The plainness tail is the one large and steady difference: lower in Essen 3/4, in lead-sheet 3/4, and by 0.6 in compound pop.

## Against my first run
My rule (the share of kept songs a 4/4 gate would turn away) called 956 and 959 borrowable in compound pop and 922 not. The songwriting session's marks agree on 922 and are stricter on the other two. Both are on the record; I have not rewritten either. Whether a trial of 956 in 6/8 is still licensed is the songwriting session's to say.

## The other parts, in brief (`metre_free_b.json` holds every figure)
Not free in most references: surprise, different pitches, different intervals, repeated notes, figures sung again. So the page gate's parts differ in their tails by metre and by genre, and its sum, plainness, with them.

## A source for 3/4 found on the way
OpenEWLD (already in `tables/metre_atlas/ewld_mxl.json`): 66 lead sheets in 3/4 with 60 notes or more (80 in all, 72 with English words), 89 in 2/2, 10 in 6/8. Public-domain Tin Pan Alley songs with melody, chords and words, MIT licence on the collection. Against four pop songs in 3/4, it is the first set from which 3/4 tables with words could be made. They are older songs than the kept pop set, which is a genre gap to state, not hide.

## What I expected
Essen pitch checks free: wrong by the tail test, right for the medians. Lead-sheet 3/4 free on the commonest pitch and the leap: the leap yes; the commonest pitch out, on the side that cannot hurt.
