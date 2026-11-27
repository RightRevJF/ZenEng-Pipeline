# The 6/8 repair for v54, first reading: result (27 Nov 2026). Six marks met; 840 still takes four builds in ten. Not built.

Rule: `PREDICTION_package_6_8.md` (ef86dca, accepted with one addition at 793092f, both before any code or run). Figures: `package_6_8.json` (`python3 studies/other_metres/package_6_8_read.py NAME=DIR ...`). Song 52's lyric, Essen 6/8 table, seed 1, 1,000 builds, `LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=1 LUTHIER_COPY_JOIN=1`. "Living" = the 223 living builds of 600 from the chosen record's fitted spec.

**S1. The bars, before the draw.** Verses `[3, 3, 3, 3]` (verse 3 `[4, 3, 3, 3]`); choruses `[3, 3, 3, 3, 2]`; bridge `[3, 3, 4, 3]`; last chorus `[3, 3, 3, 3, 2, 2]`; no pad. The title's room moved the chorus title line from 2 bars to 3 and the bridge's from 3 to 4.

| | chosen tune | living builds' median | the mark | |
|---|---|---|---|---|
| Living builds; pool | 374; 36 | | 30; 10 | **S2 met** |
| Notes a bar, over 106 bars of sung phrases | 3.94 | 3.94 | 3.60 to 4.33 | **S3 met** |
| Onsets on the beat | 0.435 | 0.421 | 0.389 or more | **S4 met** |
| Onsets on the bar's first beat | 0.220 | 0.213 | 0.211 or more | **S4 met**, narrowly |
| Stressed syllables on a beat, every build made (median) | | 0.506 | 0.40 or more | **S5 met** |
| Deaths on 780, in ten builds made | 0 | | under one | **S6 met** |
| Deaths on 840, in ten builds made | **4.0** | | under one | **S6 missed** |
| Inside the voice (59 to 71 in an alto's 55 to 74); a leap past an octave | yes; none | | | **S7 met** |

Byte for byte, every switch unset: 54, 55, 52, and song 53's Essen arm.

## 840 and the title line, as asked: the window counts per bar count
By kept count, the share of Essen's windows in which half or more of the line's stressed syllables fall on a beat:

| title line | syllables; stressed | 2 bars | 3 bars | 4 bars | bars the rule gave | under half, in builds |
|---|---|---|---|---|---|---|
| "you're just in the room next door" (both choruses) | 7; 5 | 0.31 | 0.61 | 0.99 | 3 | 62 in 100 |
| "the room next door came as close a breath" (bridge) | 10; 6 | 0.04 | 0.23 | 0.91 | 4 | 50 in 100 |

So it is **not** a fault of the title line's words: at four bars nearly every kept window lands half its stresses. The rule I wrote stops at the first bar count where half the windows do, which gave the chorus line three bars, and the draw then lands it less often than the window count promised (38 builds in 100 at or over half, where the windows said 61). The threshold of half the windows is the weak point, and it was mine.

## Reported
- **One switch off at a time** (200 builds each):

| off | living; pool | deaths 780; 840 | notes a bar | on the beat |
|---|---|---|---|---|
| none (1,000 builds) | 374; 36 | 0; 404 | 3.94 | 0.435 |
| the plan | 7; 0 | 0; 131 | 5.76 | 0.304 |
| the title's room | 60; 27 | 0; 111 | 4.02 | 0.401 |
| the copy's join | 64; 3 | 39; 70 | 3.91 | 0.408 |

  The plan is what gives 6/8 a pool at all. **The copy's join is tested here and works:** with it, no build dies on 780 (203 copies were sung again instead in the 1,000 builds); without it 780 takes two builds in ten and the pool falls to 3. The title's room moves 840's deaths from 5.6 to 4.0 in ten: it helps and is not enough.
- **Other deaths:** 838 (the chorus's lift) 208; 731 14.
- **Stressed syllables on the bar's first beat** (the addition): chosen tune 0.261, living median 0.256. The lead sheets' 6/8 by song: 10th 0.324, 25th 0.390, median 0.509; the six hymns 0.515. So in 6/8 too the draw puts a stressed syllable on either beat as readily as on the first, and the figure is under the lead sheets' 10th. 6/8 shares 749.231.
- **Range and pitches:** chosen 12 and 8; living median 10 and 7. Essen's 10th 9 and 6, 25th 12 and 7; the lead sheets' 10th 12 and 8.
- **Length:** 271 seconds, past the kept 75th of 243 (the padded form ran 324).
- **Joint gate:** the pick stands 3.51 from the kept tunes (gate 3.57).

## What I expected
S2, S3, S5 met, S4 likely, S6 the doubt on 840. That is how it fell; the three-bar slots drew without fault.

## The one revised form the stopping rule allows, for the songwriting session to choose
The reading names the reason: the title's-room rule asks too little. **Proposed:** a title line takes the fewest bars (to four) at which **nine** kept windows in ten, by count, land half its stresses on a beat, in place of half the windows. For song 52 that gives both title lines four bars (0.99 and 0.91). Everything else as read. If no bar count reaches nine in ten, the most favourable is taken and the record says so.
