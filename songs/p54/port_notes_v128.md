Every fix is a whole-statement patch in gen_v128.py (Part 1) or gen_v128_parts23.py (Part 2), gated on its part by ON8(). ZE_PART=0 reproduces Run 2's Part 3: song 45 main, order daaa5c98509f, 537 survivors, matched. Part 3's bass is bass_v128.py.

**Part 1**
- **491.** 467's knob on the walk's spread (rg467) and 408's on the contour's width (sh408) are withdrawn (ON7 returns false for both). 468 (400's knob at a half or above) stays.
  - Song 45's chorus floor is the lower of the verse's median plus three and the chorus top less three, as before 467. It may fall to the top less eight, but no lower than keeps the register's centre one semitone over the verse's median plus three: max(top − 8, 2(vm + 3) − top + 2).
  - 461 with 450, and 456, are kept.
- **476.** The content judge of record is zeneng_v128_judge.json (the same 37 measures). The pick's score is the mean over the windows of (content + order) / 2 (477), as in Run 2.
- **465.** For a drawn line whose next line is in the same section, a class is drawn by the kept share for the line's notes: the last onset 0, 1, 2 or 3+ bars back from the bar where the next line begins.
  - Only classes the slot can reach are drawn: the line's unweighted lattice (the cap, the palette, the grid) must have a last onset in that bar.
  - The next line's bar is known when the next line is a copy, return or sung-again line (prefitted). Otherwise it is the next slot's first bar.
  - Q1 A: class 0 asks the next drawn line to take a pickup (when its first syllable is unstressed), and classes 1–3 ask it not to. The ask holds for half the next line's tries.
  - The class holds for half the line's tries: a weight of 0 on last onsets outside the bar, and the span's share (378) drawn again inside the bar's reach. After that it is given up and counted.
  - The final melisma stays in the bar.
- **458.** 414's density bound uses the kept 25th–75th of notes a second across the sung span (first onset to the end of the last note), by notes in the line, in place of 423's whole-song 1.4–2.3.
- **484.** 435's rate (K435) is aimed in the calibration, on unaimed builds, toward a pitch kept of 0.755, with Window 142's pair() on the first eight bars of each verse. It starts at 0.75.
- **478.** In the sing-again walk, the repeat and step categories carry knobs (rep478, stp478), aimed on unaimed builds at verse 1's own repeat and step shares in the same builds. 434's bar on repeats the source did not sing is lifted.
- **486.** 389's run rate for a band read in Verse 1 or Chorus 1 is read on those two sections alone. A band they lack is read on its own sections, as before.
- **489.** 452's three knobs (equal gap, run of equal gaps, zigzag) are kept by the section's band of density and aimed on the judged windows at the kept figure for the window's own notes a bar (zeneng_v125_port_reread.json). The song-wide knobs stay at one.
- **490.** A weight on an onset in a run is kept by band (a sixteenth position with sixteenth gaps on both sides, chosen in the backward draw). It moves with 389's reading of drawable runs.
  - 455's sixteenth-gap weight no longer moves with that reading. 490 takes its place, so 455 is inert (see 509).
- **494.** When the strict copy of a unit-return line (457) leaves no entry and landing, the line falls back at once to the weighted copy for the rest of its tries.
- **485, 479.** Separation and the reread are read on the main and control runs alike (sep_v128.py on the control runs; RR_MODE=ctl). A change counts as real beyond twice the larger main–control difference.
- **496.** kept_pass_v128.py reads 170 CoCoPops songs the way each test reads a song (the mean of its windows) and prints the share that pass. A test of the engine's own rule, a count, or a reading is marked as having no kept rate.

**Part 2**
- **438.** draw_chart() works on each section's chord list, so sections of one kind keep one chart. The song's own seed is "438 chart <song>", so main and control share it.
  - No two-change bar is drawn at the kept rate (the mean of 25.1% and 36.6%). Otherwise a target share of two-change bars is drawn in the kept middle half, and so is a share of held bars.
  - Holds come first: a bar takes the chord of the bar before. Then two-change bars: a bar takes, on its third beat, the chord a fifth above the next bar's root where the song has one, else the next bar's chord.
  - A section's first and last bars are not edited.
- **440.** At the kept rate of songs with inversions (46%), up to one chord in twelve is written over its third or fifth, where that makes a step to a neighbour (a step on both sides weighted three to one). The bass's pitch class is kept with the chord, and 450's second-or-seventh weight reads it.
- **The chord at the note.** M.chord_at reads the half-bar the note falls in. Every reading in the engine, readings_v128.py and reread_v128.py takes the chord at the note.

**Part 3**
- **439.** bass_v128.py writes each section's bass from the record's chart (the chord at each half-bar), its kicks (drum note 36) and its lead (the half-bars the voice leaves empty).
- **445.** The figure is A B A C A B A D over eight bars: two cells, with fills C and D at bars 4 and 8. A bar whose second half the voice leaves empty takes a fill at a rate of 0.35.
- **446, 447.** The root falls on beat 1 and at every change. The other notes are drawn among the root, octave, fifth, third, the scale's seventh and notes of passage, with no more than one octave a bar and never two running.
  - The intervals of an A bar are kept for the other A bars four times in five.
- **448.** The bass takes every kick on the eighth grid, and the notes are made dense enough that about half fall on kicks. The bar's last note steps into the next bar's root at a rate of 0.45 where the roots differ.
- **444.** Each eight bars is read with Window 144's measures() against the pop-and-rock quartiles. A draw that breaks a test is drawn again, up to 60 times a section.
- **449.** No rating is read.
- The records are the songs' own (songs 40, 43, 44): only the bass is replaced, and the hand-written one is kept in the record beside it.
