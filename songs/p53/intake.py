"""The writer's choices in the v127 Run 2 session (songs/p53). No new song; the songs' own intakes stand (songs p40-p49)."""
LOG = [
    dict(q="(instruction)", asked="v127 Run 2 of 3",
         answer_text="Run 2 of 3, on top of Run 1. The spec is now ZenEng v127 (Modules 27.69-27.71). Kept figures are in the tables page files named below. "
                     "Numbering: your Run 1 findings 450-454 are 464-468 in the paper (450->464, 451->465, 452->466, 453->467, 454->468); 455-463 stand. New findings number from 480. "
                     "Rulings on Run 1's findings. Adopted as you proposed: 464, 465, 467, 468, 455, 456, 457, 458, 459, 461. Readings: 460, 462, 463, 466. "
                     "The judge, from this run on (zeneng_v126_judge.json): 470: content scores come from the refit; the order judge is unchanged. "
                     "471: 254's floor stays on the v108 judge. Print the share of complete builds under the refit's kept fifth percentile (-0.51). "
                     "472: the pick is the refit's first among survivors with no soft break. Print the old judge's pick and each one's rank under the other. "
                     "473: the judge does not read a second verse. Do the four parts in order, with a rerun of all five songs (main and control, same seeds) after each of Parts 1, 2 and 3. "
                     "Part 0: repairs, no rerun of their own: 464: 267 reads song 45's bridge G before its raise. 459: read verse 2's bars where syllable counts differ by one or less. "
                     "Part 1: the second verse (zeneng_v122_whole_song.json): 434 (amends 228): in sing-again, remove the move of stressed on-beat notes to chord tones, and do not repeat a note the source line did not repeat. "
                     "Verse 2's chord tones come from 398's knobs, as verse 1's do. 435: where both verses strike the same place in the bar, keep verse 1's pitch about 75% of the time. "
                     "Test: verse 2 less verse 1 under 0.15 kept sd on at least 20 of the 27 measures (now 14); chord tones on the beat in verse 2 within five points of verse 1's (now 87% against 68%). "
                     "Part 2: rhythm (zeneng_v125_port_reread.json): 452: aim gaps equal to the gap before at 38% (now 51%); the longest run of equal gaps at the kept figure for the section's notes a bar; three moves that zigzag at 32%. "
                     "455: the sixteenth-gap weight by band. 406: draw the landing jointly with the kept table. 465: a line's span ends in the bar of its slot where kept lines of its length end. Empty bars stay unaimed. "
                     "457, 458: unit-return lines drawn strictly on the unit's onsets first; span bounds from kept lines' syllables a second across the sung span. "
                     "Part 3: pitch: 408 with 468: aim 257's contour shapes at the kept turns; hold 400's knob at 0.5 or above. 467: 392's chorus floor no higher than the chorus top less eight; "
                     "aim the window's range at the kept mean by the register's widening. Print song 44's range against its intake. 461 with 450: read 398's first-beat knob by section; "
                     "the chorus's first-beat notes on the chord's third at 27% (now 16%); notes a second or seventh from the bass at 19% (now 23%). 456: read the last-note test on windows whose last note the walk chose. "
                     "After each rerun: predictions written and pushed first; compare every reading with the run before and say which moved toward kept songs and which away; give separation on the agreed measures, "
                     "and again without each family you aimed (454). Check: separation at or under Run 1's 0.719 on songs 40, 42 and 43. If a test can't be passed by kept songs themselves, flag it. "
                     "Push everything and give me the test report and fix-list link."),
    dict(q="Q1", asked="Part 2 is blocked on two fixes, so I'll stop before its run. 465 (where a line's span ends in its slot, by the kept share for its length) and 458 "
                       "(span bounds from kept lines' syllables a second across the sung span) both need kept-line figures. Neither figure is in the tables page or the paper, "
                       "and I have no access to the corpora. Part 1 is running now and doesn't depend on them. How should I handle 465 and 458?",
         options={"A": "Run without them (Recommended): run Part 2 with 452, 455, 406 and 457 now; add 465 and 458 in Part 3 once the paper side sends the two kept tables.",
                  "B": "Wait for the tables: hold Part 2 until the paper side posts both kept figures, then run all six rhythm fixes together.",
                  "C": "Use stand-ins: approximate both from 378's span table and Window 124's line ends, flagged as stand-ins in the report."},
         recommended="A", answer="A", answer_text="Run without them (Recommended)"),
]
