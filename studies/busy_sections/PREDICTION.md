# Rhythm scaling in the engine (749.138): the rule, written before anything is run

**Seen before writing.** `studies/rhythm_memory/RESULT.md`: slow change in how busy the singing is (+0.68) and bars with nothing sung (+0.58) carry rhythm scaling. Review 28: the pools' spread of rhythm scaling is 0.30 of the kept spread and 93 pool builds in 100 sit under the kept 25th. Read today, before this rule, on the kept songs: notes per sung bar stand at 3.9, 4.6, 5.4 in verses and 3.5, 4.0, 4.9 in choruses (quartiles); the verse is the busier part in 66 songs in 100; the busier part is 1.21 times the sparser at the middle (1.11, 1.37 at the quartiles). Luthier's songs 55, 54 and 58 give nearly every line of 6 to 8 syllables two bars, verse and chorus alike (about 3.7 notes a bar); fix 869 gives a line one bar only where half of kept lines that long take one bar, and kept lines of 6 to 8 syllables take one bar 22 times in 100 at a middle tempo and 36 at a slow one. The engine already sings a two-bar line in one bar and rests the other 9 times in 100 (876, 911), set from kept songs.

**What the engine can move.** How busy a stretch is, in notes a bar, is the lyric's syllables over the bars the engine gives them. The engine cannot add or drop words. It can give a part's lines fewer bars, and it can plan bars of rest. Two changes are tried, alone and together:

- **A, the verse sung closer.** In verses, lines of 6 to 8 syllables take one bar as often as kept lines that long do at the song's tempo (22 or 36 in 100), the shortest lines first, an even count in each verse so the verse keeps whole pairs of bars. The chorus is left as it is. (The verse, because it is the busier part in two kept songs in three.)
- **B, a break where A leaves room.** The planner's own rule (830, 842) adds an eight-bar break only while the song stays inside the kept 75th of lengths. Nothing is changed in that rule; A shortens the song, and the break comes in or does not.
- **A at its limit**, read only to see how far the lever reaches: every verse line of 6 to 8 syllables in one bar.

**Trial, outside the engine's records** (`trial.py`): 40 quick tunes a song as `lyric_room.py` draws them, songs 55, 54, 58; song 59 read only; then, for a form that passes the first check, the pools by `neighbour.py`.

**The check** (Review 28's): rhythm scaling, the builds' middle, inside the kept quartiles (0.605 to 0.721) in two of songs 55, 54 and 58; the soundness rule and the pool standard hold; at least 7 in 10 as many builds live; the words' fit, the builds' middle, down by no more than 0.02.

**What I expect.** A moves two or three lines of eight in a verse, so the verse runs about 4.3 notes a bar against the chorus's 3.6: a ratio near 1.2, the kept middle. That is a small change in the four-bar windows, and I expect rhythm scaling to rise by 0.01 or 0.02 and the check to fail. A at its limit may reach the kept 25th in song 55 and not in 54 or 58, whose lyrics leave no room for rest (their room files already say so). If so the finding is that the engine's side is nearly spent and the remedy for these three is the lyric's.

## Added after the first step, before the next is run

**Seen:** `trial_as_built.json`, `trial_kept.json`, `trial_all.json`. A as written moves rhythm scaling to 0.605, 0.574, 0.589 (songs 55, 54, 58; as built 0.590, 0.574, 0.559); in song 54 it moves no line, because rounding to an even count leaves none. A at its limit reaches 0.730, 0.674, 0.674, well inside the kept quartiles, but songs 55 and 54 all but stop building (2 tunes in 100 tries) and the words' fit falls by 0.035 to 0.07; and a verse at twice the chorus's notes a bar is outside anything kept songs do (the busier part is 1.48 times the sparser at the kept 90th).

**Two doses between, with a guard.** *Aim:* each verse takes as many one-bar lines (shortest first, an even count) as bring its notes a bar nearest the kept middle for verses (4.59). *Half:* half the verse's lines of 6 to 8 syllables. **Guard, for any form:** the verse's notes a bar over the chorus's must stay inside the kept 10th to 90th (0.83 to 1.48); a form outside it is not built whatever its rhythm scaling.

The check is unchanged. **What I expect:** aim lands near A as written (0.60, 0.58, 0.59) and fails; half passes the scaling check in song 58 only and breaks the guard there.

## Added after the second step, before the third is run

**Seen:** `trial_aim.json`, `trial_half.json`, and aim read on a thousand builds a song by `neighbour.py` (`neighbour_v44_trial_verse_closer.json`): the builds' middle rhythm scaling 0.676, 0.618, 0.609 (all inside the kept quartiles, against my expectation); the pools fail the soundness rule 0.1 times in 100; the verse stands at 1.11 to 1.14 times the chorus's notes a bar (the kept middle is 1.15). But builds live 244, 241, 197 against 342, 309, 419: song 58 keeps 47 in 100, under the 7 in 10 written first. So aim, as it stands, fails on builds in song 58. Read where they die (300 tries): "the syllables cannot fit the window", 152 tries in song 58 and 85 in song 55, none as built. In song 58's third verse aim had put three one-bar lines side by side.

**One change, from that:** no two one-bar lines stand side by side in a verse (each keeps a two-bar neighbour, whose rest gives it room to begin early), and no line already next to a one-bar line is taken. The shortest lines are still taken first, the count is still even and still the count nearest the kept middle for verses that this allows. Called *aim, apart*.

**The check is unchanged,** read on a thousand builds a song: rhythm scaling, the builds' middle, inside the kept quartiles in two of songs 55, 54, 58; at least 7 in 10 as many builds live in each; the words' fit, the builds' middle, down by no more than 0.02 in each; the soundness rule and the pool standard hold; the guard (verse over chorus inside 0.83 to 1.48). Song 59 has no line of 6 to 8 syllables in its verses and is unchanged by any form.

**What I expect:** fewer deaths at the window; song 58 keeps about 6 in 10 of its builds and still fails the builds check, narrowly. If it does, nothing is built and the result says how far it is.
