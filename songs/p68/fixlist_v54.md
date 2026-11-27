# Luthier list for v54 (since v53)

Started 27 November 2026. Findings from 749.226. The settled items up to v53 are on `fixlist_v53.md`.

## Songs
| Song | Folder | State |
|---|---|---|
| 67, A Door in the Coral | p77 | locked, banked, unrun; made for real once the drafting fix lands |
| 68, Save Me from My Muse | p78 | locked, banked, unrun; a 3/4 punk waltz for high tenor; made for real once the 3/4 draw reads well |

## 749.226. In 3/4 the plan gives every line two bars
- **Problem:** a 3/4 lyric's plan (`spec.slots`) gives every line two bars, whatever table the draw reads. So a line's density is fixed before the draw begins: eight syllables in two bars of 3/4 is four notes a bar, and seven is three and a half.
- **Evidence:** the 3/4 trial on song 53's words (`studies/other_metres/PREDICTION_trial_3_4.md` at 9deaabc, before the run; `RESULT_trial_3_4.md`, `trial_3_4.json` at dfc493d). Against Wikifonia's middle half (2.06 to 2.70 notes a bar; onsets on a beat 0.731 to 0.939; first-beat stress by song 0.583 at the 25th), the lead-sheet arm made 3.29, 0.571 and 0.306, and the Essen arm 3.5, 0.576 and 0.306. The arms are nearly the same, so the table isn't the cause. Living builds aren't the problem (610 and 566 of 1,000), unlike 6/8.
- **Fix (proposed, to be tried rule first):** in 3/4 a line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest the table's median. A line of three sung bars is padded to a four-bar phrase with a held last note or a rest, and the draw reads a four-bar line as two windows. The maintainer's first version rounded to 2 or 4 only. That would leave 6- and 7-syllable lines, every line of song 68, in two bars.
- **Check:** marks P1 to P7 in `coord/songwriting.md` (27 Nov, 10:58 ET); byte for byte on 54, 55 and 52 with the switch unset. One form only. If it misses, the 3/4 draw closes for v54, and song 68's path goes to the writer.
