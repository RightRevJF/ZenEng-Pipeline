# The loop gate with a chance: the form, its rule and marks, written first (749.185)

26 November 2026. Seen before writing: `studies/v48_trials/RESULT.md` section 3 and `drafts.json` (the writer with no gate: 45 major verses in 100 at or under the kept median of chord repetition, 34 over the kept 75th, plain loops 32 against the kept 30; the median gate, 960 as built, leaves 99 under the median and none over the 75th; the gentle gate 65 and none). Any gate that redraws to a line empties the far side of the line. This form has not been run.

**The form.** Where a lyric asks for chords that loop less (`"chords": "loop_less"`), a verse or bridge whose chord repetition is over the kept 75th for its kind and mode is drawn again **with a chance**, and then until it is at or under the 75th (30 times at most; the least-looping draw where none is); otherwise it stands as drawn. The chance is set so that about 25 sections in 100 stay over the kept 75th, as kept songs have by definition: for each kind and mode, 1 less 0.25 over the unpatched writer's own share over the 75th (nothing where that share is 0.25 or under). The shares are measured once on a thousand unpatched drafts a kind with their own seed, not the checks' seed: `lib/luthier/make_loop_chance.py`, `tables/loop_chance.json`. `LUTHIER_LOOP=chance`; `loop_less == "chance"` in the writer. Off unless asked; with it off nothing changes.

**Judged on the kept songs' rate alone** (R06-2: the two cover margins lean opposite ways and neither is settled).

**Marks, on a thousand drafted sections a kind, major, as `studies/v48_trials/drafts.py` drew them (the same seed as the earlier forms, so the four forms are read on the same draws up to the gate):**
1. Verses at or under the kept median between 45 and 60 in 100.
2. Verses that are plain loops within 5 points of the kept share (30 in 100; the stage 4 reading `loops`).
3. The stage 4 readings (first, last, chords, bigrams, bars; verse and bridge) no further from held-out kept sections than the unpatched writer's by more than 0.02.
4. Verses over the kept 75th between 20 and 30 in 100 (what the form is for).

Minor is reported and decides nothing (35 kept bridges).

**Then song 63, once, only if all four hold,** its ledger row first, and after the songwriting session has seen the marks' result on the thread: `songs/p73/lyric63.json` written through by v50 with the form on. A single song cannot check a share. What it can check, as written for 749.178: its chosen plan's verse and bridge are drawn by the form without fault (each either at or under the kept 75th, or stood as drawn by the chance: both are the form working, so this is read as "the plan is one the form could have made" and reported); **its pool is 10 builds or more; its builds' middle words' fit is at or over the words gate's floor.**

**Whatever happens, 960 stays a setting, not a default.** If the form passes on both it replaces the median form as what `"chords": "loop_less"` means.

**What I expect.** 4 met by construction, near 25. 1 met, 50 to 53 (the redrawn ninth of verses lands mostly under the median). 2 met: plain loops sit at the top of repetition, and a quarter of the top is thinned, not all of it; I guess 26 to 29. **3 is the doubt**, as before: the gentle gate missed it by 0.002 on verse bigrams and by 0.015 on the bridge's last chord, and this form redraws about a quarter as many sections, so I expect it inside, with the bridge's last chord (a small held-out sample) the one that could still miss.
