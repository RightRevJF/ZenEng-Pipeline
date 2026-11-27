# Luthier list for v54 (since v53)

Started 27 November 2026. Findings from 749.226. The settled items up to v53 are on `fixlist_v53.md`.

## Songs
| Song | Folder | State |
|---|---|---|
| 67, A Door in the Coral | p77 | locked, banked, unrun; made for real once the drafting fix lands |
| 68, Save Me from My Muse | p78 | locked, banked, unrun; a 3/4 punk waltz for high tenor; made for real once the 3/4 draw reads well; the writer chooses its path now that the v54 draw has closed (27 Nov) |

## 749.226. In 3/4 the plan gives every line two bars
- **Problem:** a 3/4 lyric's plan (`spec.slots`) gives every line two bars, whatever table the draw reads. So a line's density is fixed before the draw begins: eight syllables in two bars of 3/4 is four notes a bar, and seven is three and a half.
- **Evidence:** the 3/4 trial on song 53's words (`studies/other_metres/PREDICTION_trial_3_4.md` at 9deaabc, before the run; `RESULT_trial_3_4.md`, `trial_3_4.json` at dfc493d). Against Wikifonia's middle half (2.06 to 2.70 notes a bar; onsets on a beat 0.731 to 0.939; first-beat stress by song 0.583 at the 25th), the lead-sheet arm made 3.29, 0.571 and 0.306, and the Essen arm 3.5, 0.576 and 0.306. The arms are nearly the same, so the table isn't the cause. Living builds aren't the problem (610 and 566 of 1,000), unlike 6/8.
- **Fix (proposed, to be tried rule first):** in 3/4 a line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest the table's median. A line of three sung bars is padded to a four-bar phrase with a held last note or a rest, and the draw reads a four-bar line as two windows. The maintainer's first version rounded to 2 or 4 only. That would leave 6- and 7-syllable lines, every line of song 68, in two bars.
- **Check:** marks P1 to P7 in `coord/songwriting.md` (27 Nov, 10:58 ET); byte for byte on 54, 55 and 52 with the switch unset. One form only.
- **Read (27 Nov):** marks 740bb4e, result 02e75c3 (`RESULT_plan_3_4.md`, `plan_3_4.json`). P1 to P5 met: every line three sung bars in a four-bar phrase; 731 living, pool 268; 2.09 notes a bar over the sung phrases; onsets on a beat 0.893; first-beat stress 0.622. P6 missed: the commonest pitch 0.424 and 0.390, against 0.287 and 0.280 for the Essen arm. By the stopping rule the 3/4 draw closes for this version; the form stays a switch (`LUTHIER_PLAN_3_4`), unset. The density part of the fix works; 749.227 is what's left.

## 749.227. In 3/4, the four-bar phrase repeats one rhythm and the tune narrows
- **Problem:** under the plan form (749.226), the draw reads a four-bar phrase as two windows and keeps reusing one rhythm, and the tune sits on one pitch.
- **Evidence:** `plan_3_4.json` (02e75c3). Bars on a rhythm already sung 0.946 and distinct rhythms over bars 0.054, against v53's Essen arm at 0.766 and 0.234. The commonest pitch is 0.424 in the verses and 0.390 in the refrains, against the lead sheets' whole-tune 90th of 0.30.
- **Fix (to be specified rule first):** first compute the lead sheets' own figures, by song, for repeated bar rhythms and the commonest pitch. Then draw the phrase's two windows so that a section's repeated bar rhythms and its commonest pitch fall inside the kept waltzes' middle half.
- **Check:** marks read against kept waltzes, not against another arm, on song 53's words. Song 68 is the real test after it.
