# 749.252, a line that will be sung again is drawn for every set of words it will carry: the form and marks, before any code or run

28 November 2026, 04:42 ET. From RESULT_counts_251.md (mending same-count lines alone reaches 0.438; every line sung again as good as fresh, 0.481). Accepted and numbered by the songwriting session (04:34 ET), with its marks.

**The form (`LUTHIER_SOURCE_WORDS=1`, unset by default; it acts only where the table has a stress file and 749.231 is on):** when a line is drawn that later lines will sing again, its rhythm is chosen by the table's stress score summed over every set of words it will carry. Its own words weigh as now. Each later set adds its score as the refit would set it: the same count, the score of the rhythm as it stands; one to three apart, the best score 749.251 would find; more than three apart, nothing.

*Settled, mine to answer for:*
- **How the sum is drawn.** The line is drawn twelve times by today's rule (so the kept windows' counts, the entry, and its own words weigh exactly as now), and one of the twelve is taken with chance in proportion to e to the power of 1.4 times the later sets' summed score, 1.4 being the weight the draw gives the stress score now. This is the same on every path of the draw (one window, two windows, the weighted rule), which is why it is done this way and not inside one path.
- **Which later sets.** The lyric's marked lines that sing this line again or copy it, each counted whole; and 818's: the line two below it in its section (and the second line, for a section's first), with whatever those would carry in turn, each weighed by 818's chance of singing it again (the record's figure, 0.8 here), multiplied down the chain.
- It acts on the line's main draw only; a line set after 870's wait is as now.
- 749.251 stays on beneath it.

## Trials
- **Pop 3/4:** song 55's words, RESULT_251.md's package (with `LUTHIER_AGAIN_WORDS=1`) and the new switch; seed 1, 1,000 builds.
- **The five 6/8 lyrics:** song 69's settled package with both switches set. No stress file there, so nothing to act by.

## Marks, pick and living median
1. **Pop 3/4, K1 to K8,** with K3 at 0.45 or more on the first beat and 0.26 or under off it, K5 0.303 or under, the share of marked lines drawn fresh at most 0.076, 749.247's chord mark.
2. **K6 holds:** rhythm again within sections 0.349 to 0.871; figure again 0.667 or under.
3. **The source lines' own words do not pay for it:** the first-beat stress of the drawn lines that are later sung again, read on their first singing, at least 0.40. **Read on the present package before this file was written (count_sources.py, 231 living builds of 400): 0.458 on the first beat, 0.179 off the beat, over 4215 stressed syllables.** (Drawn lines no later line sings again: 0.764, over 148.)
4. **The five 6/8 lyrics come out byte for byte the same.**

Watched: K3 by sort as in count (a); the share of living builds meeting K3's first beat (24.1 in 100 now); every figure mark (11.2 in 100 now).

Byte for byte, every switch unset: 54, 55, 52, song 53's Essen arm. Room files after.

## What I expect
- Lines sung again rise on the first beat from 0.358 to between 0.40 and 0.46; the same-count lines most.
- The source lines' own figure falls a little from 0.458, to 0.41 to 0.45: mark 3 met.
- **K3 on the median: 0.42 to 0.47 on the first beat. An even chance it is met.** Off the beat stays met on the median.
- The risk I can name: the sum over many sets is a strong pull, so of twelve draws nearly always the same one wins. Rhythm sung again may rise (inside K6's band, I think), and fewer builds may differ. I do not expect a new death.
- The pick is still one draw from the pool; if under half the pool meets every mark, the pick can miss by chance even where the median passes.
