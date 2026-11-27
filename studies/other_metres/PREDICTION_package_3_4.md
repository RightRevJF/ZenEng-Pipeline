# The 3/4 repair for v54 (749.226 to 749.229): the rule file, before any code or run

27 November 2026, 14:09 ET. Marks from the songwriting session (`coord/songwriting.md`, 14:08 ET), quoted where they are its words. Everything I settle to turn them into a form is said here, before any of it is written. Song 68 is reserved and is not run.

## The four parts, each behind its own switch, all unset by default
1. **749.226, bars from the table's density** (`LUTHIER_PLAN_3_4=1`, as tried). A line's sung bars are whichever of 2, 3 or 4 puts its syllables a bar nearest the table's median (a tie to the fewer). "Padding is used for popular style (the lead-sheet table), not for folk (Essen)": *settled:* the table says which it is (the lead-sheet table carries `"phrases": "padded"`); under a table without it a three-bar line takes three bars and no pad.
2. **749.227, a range floor and a register plan** (`LUTHIER_RANGE_3_4=1`). *Settled, after the two rules 4/4 already has:*
   - *The register plan (as 927):* the tops of the verse and chorus registers are set so that their span, floor to top, is the like-length waltzes' median range and one semitone over, held inside the voice; the bridge's top moves with them.
   - *The floor (as 954):* of the builds past the gates, the pick is the first whose range is at or over the like-length waltzes' 25th; where none is, the widest.
   - Like length is found by the plan from the bars it gives the song, by the band below, from a by-song list beside the table.
3. **749.229, a title line's own room** (`LUTHIER_TITLE_ROOM=1`). *Settled:* for a line that sings the title, the density rule's choice stands if, in the kept windows for that many bars, half or more of the line's stressed syllables fall on a beat in at least half the windows by kept count; if not, the line takes the next more bars (to four) at which that holds; if none does, the density choice stands.
4. **749.228, the join before a copy** (`LUTHIER_COPY_JOIN=1`). *Read before settling:* in the 6/8 trial every one of 780's deaths was one line (Last Chorus line 6, a two-bar copy of a line whose source came after a padded phrase and so began in a pickup; here it follows a full two-bar line). *Settled:* where a copy's first note would fall before the line ahead of it has ended, the line is sung again (its source's pitches, its rhythm fitted afresh, as 712 already does for a line sung again) and the build does not die.

## The trial
"Song 53's words (`lyric53.json`, mezzo, piano), popular style (the lead-sheet table, padded), seed 1, 1,000 builds, all four parts on."

## Like length, written before the run
The plan gives song 53 128 bars of sung phrases (P1). A waltz's length is its bars from its first sung note to its last. Within a quarter (96 to 160 bars) too few fall; **within a third (85 to 171 bars): 52 songs of 538**, still under the 60 asked. I do not widen further on my own: the marks are read against these 52, and the count is said wherever they are used. (Half the lead-sheet waltzes are 41 bars or shorter: padded to four-bar phrases, song 53 is a long waltz.) `like_length_3_4.json`, from `python3 studies/other_metres/like_length.py 128`.

| by song, the 52 | 10th | 25th | 50th | 75th | 90th |
|---|---|---|---|---|---|
| Notes a bar, over its bars first to last | 1.53 | 1.76 | 2.15 | 2.51 | 2.71 |
| Onsets on the beat | 0.595 | 0.717 | 0.818 | 0.933 | 0.979 |
| Range, semitones | 12 | 13.75 | 16 | 19 | 21 |
| Distinct pitches | 8 | 9 | 10.5 | 14 | 16.9 |
| Commonest pitch, whole tune | 0.181 | 0.203 | 0.242 | 0.275 | 0.317 |
| Bars on a figure already sung | 0.583 | 0.734 | 0.791 | 0.834 | 0.874 |
| Bars on a rhythm already sung | 0.813 | 0.876 | 0.905 | 0.934 | 0.951 |

(For scale, and seen already: the plan-form tune of this morning read 2.09, 0.893, 9, 6, 0.317, 0.858, 0.900.)

## Marks
- **R1.** Living builds 30 or more in 1,000; pool 10 or more.
- **R2.** Notes a bar, over the bars of sung phrases, inside 1.76 to 2.51.
- **R3.** Onsets on a beat at or over 0.717. Stressed syllables on the bar's first beat at or over 0.583.
- **R4.** Range at or over 13.75 semitones (so 14), and distinct pitches at or over 9.
- **R5.** The commonest pitch, whole tune, at or under 0.275.
- **R6.** Bars on a figure already sung at or under 0.874. Bars on a rhythm already sung inside 0.813 to 0.951.
- **R7.** Every note inside the voice (mezzo, 57 to 77), and no leap past an octave inside a line.
- **R8.** Deaths on 780 and on 840 each under one in ten builds made.
- **Reported only:** every other gate's deaths; each part's switch off one at a time, 200 builds each; the song's length against the kept 75th.
- **Byte for byte**, every switch unset: 54, 55, 52, and the two 3/4 trial records (the Essen arm, and the lead-sheet-table arm of the first trial).

All figures of the chosen tune are counted as the kept table counts them (`leadsheet_waltz_figures.figs`), notes a bar over the plan's bars of sung phrases.

## Stopping rule (the songwriting session's)
"One reading of the package, and at most one revised form if a mark misses for a reason the reading names. Then close for v54."

## What I expect
R1, R2, R3 met (this morning's form met them). R7 and R8 met (song 53 has no awkward copy and its title line had no death). **R4 and R5 are the question:** the registers will have the room, but the draw has its own pull to the centre and to chord tones, and a tune may not use room it is given; the floor in the pick helps the range, not the pitch count. R6's figure mark is close (0.858 against 0.874). I put the whole at two chances in five, R4's pitch count the likeliest miss.
