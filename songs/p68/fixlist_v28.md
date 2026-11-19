# Luthier fix list for v28 (since v27)

19 November 2026. Luthier v27 (fixes 907–912) is reviewed (`lib/luthier/REVIEW_stage14.md`) and merged into main at 82551f7. All five makers now run from the repo and write their tables byte for byte, and every song record reproduces. Song 58 is rebuilt from its v27 record in B, guitar capo 2 with A shapes (fifth edition; 44 of 44 document checks pass). Three new findings (749.90 to 749.92), one carried (749.61). Next finding 749.93; next fix 913.

## The v27 list against the v27 records

| Finding | Fix | Closed? |
|---|---|---|
| 749.84 lift and key | 907 | yes: drawn within the voice's room; verse centres 0.5 / 0.5 / 2.5 from the voice's middle as `choose_key` reads them (song 58: 3.5 as sung, after melismas) |
| 749.85 words' fit | 908 | yes on what it asked: picks' fit 0.429 / 0.303 / 0.377, by length 0.336 / 0.218 / 0.191. It brings 749.90 and 749.91 with it |
| 749.86 register plan | 910 | yes: byte for byte from the repo; `kept6a.json` gone |
| 749.87 surprise quartiles | none | noted in the README; agreed |
| 749.88 long phrases | 909 | partly: over 12 beats 0.019 / 0.074 / 0.036 (kept 0.042); song 54 still over (749.92) |
| 749.89 constants | 911 | yes |
| (the paper's own) every kept rhythm | 912 | yes: builds' onsets on the beat 0.50 / 0.47 / 0.51 (kept quartiles 0.38, 0.45, 0.53). It exposes 749.90 |
| 749.61 6/8 | none | carried |

Songs are given in the order 55 / 54 / 58 throughout.

## The question: gate on length and height, leaving place out?

Yes, together with halving the place weight. Leaving place out alone moves the pool's median of stressed syllables on a beat by only 0.01, because the builds are already square. The numbers are under 749.90 and in `REVIEW_stage14.md`.

## New findings

### 749.90 After 912 the place weight makes the builds square, and 908 adds to it
**Problem.** Each kept window's score carries 879's place weight on every syllable (WORD_PLACE 1.5, times 1.4 in the window score; 2.8 on a title line). The weight was fitted when twelve windows were on offer. With every kept rhythm on offer (912), it picks the most stress-aligned windows out of hundreds. The builds' stressed syllables land on beats far more often than kept songs', and their fit by place runs over the kept. 908 then gates the whole fit, which is a third place, at the builds' median, and pushes further the same way.
**Evidence.** `studies/kept_checks/place_in_gate.py` (each song's 1,000 builds; the engine's three picks reproduced) and `place_weight_sweep.py` (300 builds a setting). Kept, stressed syllables on a beat by song: 25th, median, 75th 0.446, 0.542, 0.661. Fit by place: 0.115, 0.242, 0.333.

| | 55 | 54 | 58 |
|---|---|---|---|
| builds' stressed on a beat, median | 0.658 | 0.585 | 0.706 |
| builds in the kept middle half | 0.51 | 0.87 | 0.27 |
| builds' fit by place, median | 0.294 | 0.233 | 0.356 |
| correlation, place with stressed on a beat | 0.60 | 0.71 | 0.85 |
| pool past 908: median; share in the kept middle half | 0.663; 0.48 | 0.603; 0.87 | 0.726; 0.10 |
| pool past length and height: median; share | 0.652; 0.54 | 0.585; 0.91 | 0.711; 0.16 |
| pick (v27): stressed on a beat; by place | 0.722; 0.393 | 0.581; 0.269 | 0.821; 0.499 |

The place weight, swept on 58 and 55: at 1.5 the builds' stressed syllables on a beat run 0.704 and 0.652, fit by place 0.349 and 0.294. At 0.75: 0.642 and 0.588, fit by place 0.268 and 0.209, the whole fit 0.337 and 0.308 (kept median 0.318). At 0 the fit by place falls under the kept 25th (0.082, 0.111). With 0.75 and the gate on length and height, the picks read: stressed on a beat 0.545 / 0.504 / 0.597; fit 0.366 / 0.317 / 0.383; by place 0.150 / 0.208 / 0.291; by height 0.081 / 0.131 / 0.171. Every one is inside the kept middle half.
**Fix.** Set WORD_PLACE to 0.75, refitted after 912 so the builds' fit by place meets the kept median. Gate on the fit by length and by height at the builds' medians, with the whole fit held only to the kept floor (0.152).
**Check.** Each 4/4 pick's stressed syllables on a beat, and its fit whole, by place and by height, sit in the kept middle half. The builds' median fit by place is within 0.05 of the kept 0.242.

### 749.91 908 gates on the builds' notes; the melismas come after
**Problem.** The gate reads each build's fit before 848 adds melismas to the pick. A melisma halves its syllable's note, as kept melismas do (the first note is 0.44 of the span at the median). So the pick's fit by length as sung lands below what passed the gate.
**Evidence.** Song 58: fit by length 0.324 at the gate, 0.191 as sung (kept median 0.209; the builds' median at the gate was 0.288). Whole fit 0.430 at the gate, 0.377 as sung.
**Fix.** Draw each build's melismas before the words' gate (848's draw is seeded by the title and cheap), so the gate reads the notes as sung. Or measure the gate's medians on the notes as sung.
**Check.** The pick's fit by length as sung is at or above the builds' median as sung, and at or above the kept median.

### 749.92 909 reads a phrase at its last note's onset, so two lines still run together
**Problem.** 909 makes a line end in at least half a beat of rest once the phrase is past eight beats, measured at the onset of the line's last note. A line of 8 to 11 beats whose last note starts before beat 8 runs on into the next line, and the two make one phrase past 12 beats.
**Evidence.** Every phrase over 12 beats in the three songs is two lines run together with no rest, or a sixteenth: song 54 has four (13.0 to 15.5 beats; lines of 7.8 to 9.0 beats, then 4.0 to 7.0); song 58 two (13.2, 15.0); song 55 one (16.0, past the kept 75th of each song's longest, 15.5). Share over 12 beats: 54, 0.074 (kept 0.042).
**Fix.** Before drawing a line's last length, look ahead. If the phrase from its start to the end of the next line would pass 12 beats, end this line in at least half a beat of rest.
**Check.** Each 4/4 pick's share over 12 beats is at or under 0.06, and its longest phrase is at or under 15.5 beats.

## Carried
- **749.61** 6/8: song 52, no build past the joint gate; no kept pop corpus in 6/8.

## Known, not findings
Song 58's title draws at about 0.99 of any sorted list, so it takes the top of whatever room it is given: lift 9, the chorus to E4, the top of the baritone. That is 907 working as asked. Rest share low in 55 and 54 (0.148, 0.136; kept 25th 0.14). Songs 54 and 58 past the kept lengths (the lyrics).

## Order of work
1. 749.90 (what a listener hears first: stressed syllables on the beat four times in five in song 58). 2. 749.91. 3. 749.92. 4. 749.61.

## Songs

| Song | Folder | Under v27 |
|---|---|---|
| 58, Same Time Tomorrow | p68 | 326 s; key B, capo 2, A shapes; lift 9; stressed on a beat 0.821; fifth edition rebuilt from this record |
| 55, Your Yard Man | p65 | 240 s; key D; lift 4; stressed on a beat 0.722 |
| 54, The Man Mama Prayed I'd Be | p64 | 298 s; key G; lift 6; stressed on a beat 0.581 |
| 53, Sung to Sleep | p63 | unchanged |
| 52, The Room Next Door | p62 | no build past the joint gate |

## Regression line
The four `lyricNN.song.json` records (with `.song.txt`), `spec52.run.json`, `spec52.written_chords.json`, `spec53.json`, `spec53.run.json`, `spec53.parts.json`, `stage4_results.json`, and the six kept tables: byte for byte, or the fix says so and commits the new ones (749.90 to 749.92 will change the 4/4 records).
