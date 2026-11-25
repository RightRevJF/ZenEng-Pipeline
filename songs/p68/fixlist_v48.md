# Luthier list for v48 (since v47)

25 November 2026. Luthier v47 (959 octave gate and 962 varied returns on; 960 loop-less chords, 961 title stress and 963 blue notes off as settings; the region gate not built) is reviewed (`lib/luthier/REVIEW_stage32.md`) and merged into main. Songs 55, 54, 58, 52 and 49 and the pools reproduce byte for byte; the check passes. Next finding 749.179; next fix 964.

## In short

Everything you built stands as you built it. The title gate was my mistake: it forbade every held feminine ending, and you were right to make it a setting.

The cost to watch is the pools. The octave ban takes about 3 living builds in 10, and a random pool pick now fails the rule 6.5 times in 100, with its range past the bar. Your own kept-shaped form (one such leap a song at most) is the next engine trial.

Next, in order: the kept-shaped octave form (749.176); the gentler loop gate on song 63, its ledger line first (749.178); then the kept songs read for title lines, before 961 is tried again (749.177).

## Items

### 749.176 The octave gate as the kept songs have it
**Problem.** 959 bans every leap past an octave inside a line. Kept songs hold one or two a song (28 of 160 hold at least one; the kept 90th is 4.4 in a thousand notes). The ban leaves living builds at 223, 256, 294 (v46: 342, 309, 419), pools 24, 23, 22, and a random pool pick failing the soundness rule 6.5 times in 100 (range 1.4 to 11.2; v46 2.2).
**Evidence.** `studies/proposed_v47/RESULT.md` (octave, more fully); `RESULT_build.md`; `studies/soundness/neighbour_v47.json`.
**Fix.** Trial, rule first: a build may hold at most one leap past an octave inside a line in the whole song (the kept-shaped form), in place of the ban.
**Check.** On songs 55, 54, 58: living builds up on v47; the random pool pick no worse than v46's range (under 5.4 at its upper end); the chosen tunes hold no more such leaps than the kept 90th; builds' middle words' fit within 0.02 of v47's; the three-song soundness rule holds. If it fails, the ban stands.

### 749.177 Where a title line's longest note falls
**Problem.** 961 as a default passed over about 200 builds in 1,000 on songs 54 and 49, whose title lines end on a weak syllable held long. A line's last note is usually its longest, so the gate forbade a held feminine ending, which song 49's intake asked for. Song 62's real fault was narrower: its longest note fell on a weak syllable inside the title word.
**Evidence.** `studies/proposed_v47/PREDICTION_build.md` (the amendment); `RESULT_build.md`.
**Fix.** A reading of the kept songs, rule first: for each hook or title line, whether its longest note falls on a stressed syllable, on a weak last syllable, or on a weak syllable inside the line. Then, if kept songs hold weak syllables inside a line rarely, test the narrower gate: the longest note may not fall on a weak syllable before the line's last word; a held last syllable is allowed.
**Check.** The reading on the kept songs with the rule committed first; then the narrower gate on songs 54, 49 and 62: song 62's title line passes only with its long note on a stress, and songs 54's and 49's pools lose no more than 5 builds in 100.

### 749.178 The gentler loop gate, on the hold-out
**Problem.** 960's gate puts 99 verses in 100 at or under the kept median, where kept verses are half over it by definition; it takes the writer from too loopy to too little. Its third check failed narrowly (verse bigrams +0.028, bridge last chord +0.087).
**Evidence.** `studies/proposed_v47/RESULT.md` (Sections that loop less).
**Fix.** Trial, rule first: redraw only a verse or bridge whose chord repetition is over the kept 75th for its kind and mode; others stand as drawn.
**Check.** The ledger line in `studies/judging_data/README.md` first. On the drafts of songs 58, 60, 61, 62: the share of verses at or under the kept median between 45% and 60%; the plain-loop rate within 5 points of the kept 30; stage 4 readings no further from held-out kept sections than the unpatched writer by more than 0.02. Then song 63, once, by the same rule. If it passes on both, 960 may become the default only after the fresh-songs question settles which way covers lean.

## Standing check, changed

- 749.175 (yours, accepted): every rule that judged a change by the chosen tune's words' fit now judges it by the builds' middle, to 0.02. The chosen tune's figure is reported and decides nothing.

## Carried, open

- 749.171 what the engine does inside a line it gives one bar.
- 749.144 song 58's bars of rest; 749.147 a short line in a long slot; 749.148 to 749.152 the hymn items; 749.163.
- 749.165, 749.170: the region, now as a change to the draw (fewer notes on three pitches), not a gate.
- Rhythm scaling still leans low; nothing in v47 touches it.

## Closed

- Built in v47 (959 to 963): 749.160 and 749.167 on by default; 749.159, 749.162 and 749.168 as settings.
- 749.172, 749.173, 749.174, 749.175.
