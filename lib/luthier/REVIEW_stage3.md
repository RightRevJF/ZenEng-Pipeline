# Review of stage 3 (Luthier v12, fixes 790 to 796), 18 November 2026

Branch `luthier-v8-stage1` at e9427ea, merged into main (a merge commit: the branch did not carry main's review of 2b and 2c).
Stages 2b and 2c were reviewed and merged earlier today (REVIEW_stage2b_2c.md).

| Check | Result | Held? |
|---|---|---|
| metre_engine.py, mkspec52.py, mkspec53.py compile | yes | yes |
| `mkspec52.py`, `mkspec53.py` rebuild the committed specs | byte for byte | yes |
| `metre_engine.py songs/p62/spec52.json 3000` against spec52.run.txt and .run.json | identical: 1301 survivors, order 720051a188ac, pick af14d064785e, 1.981 | yes |
| `metre_engine.py songs/p63/spec53.json 3000` against spec53.run.txt and .run.json | identical: 2749 survivors, order 919d0a39d17b, pick ca6c64aa5425, 0.151 | yes |
| 794: gen34h.py's `readings` adds 12 to every onset | confirmed: the verse's pickup sits at -12, so +12 moves it to the downbeat and every bar line a beat late. The atlas reads its kept hymns with the pickup at beat 3 of bar 0 (atlas_build.notes_of), so the sketch was read on other bars than its table. First-beat share 0.419 as read, 0.452 on true bars | yes |
| 794's figure: the sketch's pick on true bars | 0.403 under the engine's charge (793's floor); 0.503 under the sketch's own charge. Either way far from 0.007 | yes, see 749.47 |
| Hymn.options against hymn practice (song 53's pick) | every stress on a downbeat, every pickup on beat 3, line ends held; 8 slurs over 56 syllables, all on one syllable, all by step; 7 of 8 on stressed syllables | yes, see 749.48 |

## 749.47 793's floor widens real widths, not only widths of nothing

**Problem.** 793 puts a floor under a kept width of nothing. The code applies `max(z - a, FLOOR(m))` to every reading, and FLOOR is a whole count wherever the median is above 1.5. "Notes a bar" is a rate, not a count, so its real kept width is widened.

**Evidence.** The hymn quartiles widened by it: notes a bar in 2/2, 2/4, 3/2, 3/4, 4/4, 6/8 (3/4: 0.542 to 1.0; 3/2: 0.137 to 1.0), notes a beat in 6/4 and 6/8 (0.526 and 0.374 to 1.0), and three 6/8 gap shares by under a point. Hymn mode charges every reading, so this changes song 53's pick: with the floor only under widths of nothing, the same 3000 builds pick df80b1c9ac90 (charge 0.213, notes a bar 2.129, inside the middle half), not ca6c64aa5425 (notes a bar 2.065, outside it). `review3_song53_no_floor.txt`. It is also why 794's true-bars figure is 0.403 (0.503 on the kept widths).

**Fix.** The floor only where the kept width is nothing (`(z - a) or FLOOR(m)`), or a floor scaled to the median for rates.

**Check.** No kept width above zero is changed; song 53's pick is read again and printed.

## 749.48 Two slurred bars a line, not two slurs

**Problem.** Module 27.93 says two slurred units a line at most. `rhythm_line` counts slurred bars, and one hymn bar can hold two slurs.

**Evidence.** Song 53's pick, verse line 1: three slurs (syllables 2, 6 and 7; the last two in one dotted-quarter, eighths bar). It is sung in every stanza.

**Fix.** Count slurs, or say bars in the text.

**Check.** No line of the pick holds more slurs than the rule allows.

## Still open

749.46 (the runl11 logs' code_sha) is not answered by stage 3.
