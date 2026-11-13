"""The writer's choices in the v128 Run 3 session (songs/p54). No new song; the songs' own intakes stand (songs p40-p49)."""
LOG = [
    dict(q="(instruction)", asked="v128 Run 3 of 3",
         answer_text="Run 3 of 3. The spec is now ZenEng v128 (Module 27.72). New findings number from 500. Start from Part 3's code with the withdrawals below. Do the three parts in order. "
                     "Rulings on 480-496. 480: the two kept tables are posted as zeneng_v128_kept_lines.json. 481, 482: both were the paper's faults. Use zeneng_v128_judge.json for content scores "
                     "from now on (476); it was fitted with every song in its own key. The pick's score is the mean of content and order, as you have it (477). 483, 491: withdraw 467's knob on the "
                     "walk's spread and 408's on the contour's width. Song 45's chorus floor falls only as far as its lift allows. Keep 461 with 450, and 456. Adopted as you proposed: 484, 485, 486, "
                     "489, 490, 494, 496. Readings: 487, 488, 492, 493, 495. "
                     "Part 1: clean-up, then rerun all five songs, main and control. The withdrawals above (491). 465 and 458, from the posted tables. 484: aim 435's rate so the pitch kept reads "
                     "72-79% (now 84%). 478 (amends 434): a line sung again repeats a note and steps at verse 1's rates; lift the bar on repeats the source did not have. Test: verse 2's repeats and "
                     "steps within five points of verse 1's; the paired test at 20 of 27 or more. 486: read 389's rates on the sections the judge reads. 489, 490: the stream's knobs by band of "
                     "density; a weight on a sixteenth that follows a sixteenth. 494: 457 falls back as soon as no entry and landing fit; make the side runs for song 45's joins. 485, 479: read every "
                     "check on main and control together; call a change real only beyond twice their difference. 496: print each test's kept pass rate beside it. "
                     "Part 2: the chart, then rerun songs 40, 42 and 43, main and control (zeneng_v123_bass_at_the_chord.json). 438: charts are not one chord in every bar. Draw the share of bars "
                     "with two or more changes, and the share holding the last bar's chord, inside the kept middle half. A song with no two-change bar is allowed at the kept rate. 440: root in the "
                     "bass at a chord change is the norm. A third or fifth only as a step between neighbours, at most one chord in twelve. Every chord reading takes the chord at the note, not the bar's. "
                     "Part 3: the bass, no melody rerun (zeneng_v124_bass_between_the_chords.json). 439 (amends 233-235): the song record's bass is written by an engine routine from the chart, the "
                     "kick and the vocal's rests, not typed per section. 445: a two- or four-bar figure, varied, never one bar repeated. In eight bars: two or more bar rhythms; a bar repeats the bar "
                     "before in under half of bars. 446: 2 to 4 different notes a bar; 38-73% of a bar's notes on the note the bar started with. 447: repeats 20-61% of moves, steps 9-32%, octaves "
                     "under 29%. No alternating octaves through a section. 448: a bass note on 70% or more of kicks; 35-59% of bass notes on a kick; the last note of a bar a step from the next bar's "
                     "first in a quarter to a half of bars where they differ. 444: read the bass against the Lucerne quartiles for the song's style. 449: nothing takes a listener rating as its target. "
                     "Rebuild the song records for songs 40, 43 and 44 and report the bass readings beside the old hand-written ones. "
                     "For every part: predictions written and pushed first; compare with the part before on both draws; report failures and anything the code can't do as numbered findings. "
                     "Push everything and give me the test report and fix-list link."),
    dict(q="Q1", asked="465 can't be ported as written; it conflicts with the slot ends (310/327) and 260's entry shares. Its class 0 is a line's last onset in the bar where the next line "
                       "begins: 26-38% of kept lines, against 15-20% of builds now. A line has to end inside its slot, so the only way to reach class 0 is for the next line to start with a pickup. "
                       "Pickups now come up 17% of the time. Everything else in Part 1 is coded and smoke-tested, and Part 0 reproduces Run 2's song 45 exactly. How should 465 reach class 0?",
         options={"A": "Via pickups (Recommended): class 0 asks the next line to start with a pickup, and classes 1-3 ask it not to. Kept shares are held, but pickups after drawn lines rise to about 30%.",
                  "B": "Classes 1-3 only: draw the class among 1-3 inside the slot and leave 260's entries alone. Class 0 then comes only from the next line's own pickups (about 15%).",
                  "C": "Land past the slot: let a class-0 line land in the next slot's first bar. That changes 310/327's slot end; not yet coded."},
         recommended="A", answer="A", answer_text="Via pickups (Recommended)"),
]
