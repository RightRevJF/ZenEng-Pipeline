# A key the writer asks for, second form: the result (749.219)

27 November 2026. Marks in `PREDICTION_b.md`, committed before the run. `records_b.json`.

**The second form misses too: K1 on living builds, K2 in song 58, and K3. Two forms tried; neither is built. The setting is left in the code as a trial, off unless a lyric carries `"key"`, and it is not a fix.**

| | 66 own run | 66 Am, form 1 | 66 Am, form 2 | 55 v53 | 55 Db, form 2 | 54 v53 | 54 Ab, form 2 | 58 v53 | 58 Db, form 2 |
|---|---|---|---|---|---|---|---|---|---|
| Lowest to highest (the voice) | 50 to 69 (48 to 69) | 47 to 67 | 48 to 64 | 47 to 62 (43 to 64) | 48 to 63 | 49 to 69 (48 to 69) | 48 to 68 | 45 to 62 (43 to 64) | **42** to 63 |
| Living builds | 276 | 229 | **214** | 308 | 316 | 279 | 258 | 314 | 370 |
| The pool | 33 | 18 | 19 | 33 | 33 | 22 | 23 | 20 | 26 |
| Chosen tune's range (floor) | 19 (16.0) | 20 | 16 | 15 (14.6) | 15 | 20 (15.4) | 20 | 17 (16.6) | 21 |

- **K1 missed.** Song 66 in A minor: every note is now inside a tenor and the pool is 19, but living builds are 214 against 249 asked (0.78 of the engine's own run; the first form gave 0.83).
- **K2 missed in song 58.** Its chosen tune spans 21 semitones, the whole of a baritone's range and one more than the planned band, and its lowest note is a semitone under the voice. Songs 55 and 54 meet everything.
- **K3 missed.** The three asked-key tunes all sit at or under the kept 10th of rhythm scaling, the engine's standing lean, so the rule reads them not sound (the first form's three had no lean at all: three chosen tunes are three draws).
- K4 holds by construction (the code runs only where a lyric carries `"key"`); verified by run for the first form, not rerun for the second.

**What two forms have shown.**
1. **The key itself is never the trouble.** Both forms give the asked key in every record, a tritone from the engine's own in three songs.
2. **An asked key costs song 66 about a fifth of its living builds, both times** (229 and 214 of 276), with a pool of 18 and 19. That is far better than the design gate's 86 living of 4,000 and a pool of 9, and it is under the mark the list set (0.9).
3. **A tune can outgrow its planned band** (song 58: 21 semitones against 20), and when the key is fixed beforehand there is no key left to choose that would hold it. The engine's own way, choosing the key after the tune, never meets this.

**What I do not know.** Why living builds fall for song 66 and rise for songs 58 and 55 (form 2). Whether 0.9 is the right mark for a setting whose alternative is a design gate.

**Put to the songwriting session, before any third form.** Three ways on: (a) accept the setting as it is with its cost stated, and add a check that refuses a chosen tune outside the voice (take the next in the pool); (b) a third form that reads the kept songs' floors by degree, so the registers for an asked key are the kept ones for a tune whose floor is that degree, marks first; (c) leave 749.219 to the design gate and close it.
