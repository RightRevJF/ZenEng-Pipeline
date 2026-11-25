# The flagged patches for v47, tested one at a time: rules written before the runs

25 November 2026. The songwriting session wrote six fixes from song 62 as flagged patches (`lib/luthier/proposed_v47.py`) and asked that each be tested and kept or dropped. Its first readings had every flag on at once, which left 7 to 10 builds of 3,000. Here each flag is read alone.

**Seen before writing:** the session's table of first readings on songs 61 and 62 (list for v46); its step-one reading of the chord writer (`studies/loop_less_reading`); its note that the `loop_less` patch filters kept templates by their chords while the writer draws new chords into them, so a song can still loop (song 61's verse, 0.64). Nothing of any run of mine under any flag.

**Songs.** 58, 60, 61 and 62, as the session named. Never 59, 50 or 63: the runner refuses them.

**Runs** (`run.py`; the real engine with the flag applied, so the engine's own fits see the gate). 1,000 builds a song with the flag off, and for `octave`, `title_stress`, `no_blue` and each form of `loop_less`; 3,000 for `region`, which kills most builds. The session's survivor bar (20 in 9,000) is read in proportion: 3 in 1,000, 7 in 3,000.

**The keep rule (the session's), for each flag:**
- its own reading moves as stated;
- the words' fit of the chosen tune stays at or over the kept 25th (0.248) on the songs run;
- survivors stay over the bar;
- and, mine, added now: the chosen tune's words' fit is no more than 0.02 under the flag-off tune in at least three of the four songs. A gate that passes its own reading by trading away the words is not kept as a default; it may stay as a setting.

**Each flag's own reading.**
- `octave` (749.160): no chosen tune holds a leap past an octave inside a line. Also read: how many flag-off chosen tunes hold one (if none of four, the gate guards against a rare thing, and is kept only if it costs nothing).
- `title_stress` (749.162): on every title line of the chosen tune the longest note is on a stressed syllable; read against the flag-off tunes.
- `no_blue` (749.168): no lowered third in the chosen tune. Run only on songs the engine draws as blue-note songs. It is a writer's setting by nature, never a default.
- `region` (749.165, 749.170): the chosen tune inside the region (surprise at most the kept median, pitch DFA at least 0.95 and 1.05, three commonest pitches at most 69% of the sung notes). Also read: how many flag-off chosen tunes are already inside.
- `vary_returns` (749.167): on each flag-off record, a section returning note for note has at least one line changed; the count of changes; the words' fit after.

**`loop_less` (749.159), three forms.**
- *Templates* (the session's patch): verse and bridge structures drawn only from kept sections at or below the kept median of chord repetition.
- *Structure* (the session's first repair): templates filtered by their own repeat structure: the share of a kept section's bars that return, at or below the kept median of that share for the kind.
- *Gate* (its second repair): a written verse or bridge is drawn again, up to 30 times, until its own chord repetition is at or below the kept median for its kind and mode; the least-looping draw is taken if none passes.

The session's checks for the trial, read for each form:
1. Verse and bridge chord repetition of the chosen plan at or below the kept median (verse 0.333; bridge 0.0 major) in at least three of the four songs.
2. Chorus repetition within 0.02 of the flag-off plan.
3. The stage 4 held-out readings (first, last, chords, bigrams, bars) for verse and bridge no further from the held-out kept sections than the unpatched writer's by more than 0.02.
4. The chosen tune's words' fit no more than 0.02 under the flag-off tune (the guard of 749.155), in at least three songs.
5. A fresh hold-out (song 63) must pass the same guard: **not run here.** It waits for the session's word, and for a form that has passed 1 to 4.

A form that passes 1 to 4 is a candidate, not a build. Whether it is on by default is a ruling for the session and the writer; my own view, written now, is that it should be a setting until fresh songs settle the covers finding.

**What I expect.**
- `octave`: kills 10 to 15 in 100 builds (the session's count); no cost to the words; kept.
- `title_stress`: kills about 3 in 100; kept.
- `region`: leaves under 3 builds in 100; the chosen tune's words' fit falls by more than 0.02 in at least two songs; not kept as a default.
- `loop_less`: *templates* fails check 1 in at least two songs (the session saw why); *gate* passes check 1 in all four and fails check 3 on bars or bigrams, since refusing loops moves the writer away from kept sections; *structure* lands between.
