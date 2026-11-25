# Review 34: Luthier v49 (Window 206, Module 27.130, Table HP)

25 November 2026, the songwriting session. Branch luthier-v8-stage1 at cab7ac3 (main merged in), merged into main.

## Reproduced

- `song_from_lyric.py --check`: 11 records, every stamped table the table at hand.
- Song 54 rerun with every switch off (1000 builds, 12 drafts, PYTHONHASHSEED 0): its record byte for byte (256 living; pick b71ab3ba9f1d).
- The reading of the draw on song 55 (`read_builds.py`): `builds_lyric55.json` byte for byte (23.6 builds in 100 holding a leap; 0.54 with the planted top as the far note).
- Every rule was committed before its run: the readings (0094229, 14:28) before their result (feb72fd, 14:32); the first form's checks (feb72fd) before its result (9390bd4, 14:56); the second test's (9390bd4) before its result (98e708e, 15:04); the form with a way back (76362ab, 16:02) before its result (cab7ac3, 16:42).
- The break in `write()` (0094229 to f2e884d) could not have made a wrong record: with `drafts` undefined every call to `write()` stops with an error, and no record or result was committed from that span; the readings run the engine on the records' fitted specs and do not call `write()`.
- Code read: the two forms sit behind `LUTHIER_PEAK_CLIMB`, off; 749.184's switch now maps its values. **My nit on the "inside" title form was wrong:** a note's `text` is the whole word, so the code already passed over only a weak syllable with another word after it, as the new comment says. The comment change is right; the code needed nothing.

## Rulings

1. **749.186: accepted. The best finding in some windows.** The planted peak (950) makes the leaps: half to two thirds of them have the planted top as their far note, and they come a dozen at a time because the carrying line is copied into every later chorus. With the plant out the builds leap less than kept songs, and the range falls to 13 or 14. So the plant stays and the line that carries it is what to mend. It also corrects 749.180: the leaps are not out and back so much as copied.
2. **749.187: accepted; 749.177 and 749.183 close.** By title line the draw is at the kept rate and its cases are the kept kind (a small word before a breath, a stressed note a sixteenth shorter beside it). The gate was dear because it judged a build by its worst of five title lines. 961 stays a setting for a writer who asks.
3. **The first form, failed twice by one build and by the hold-out's plant share: not built. Agreed**, and the writer's "hold it" stands. Keeping the line at a half when the miss was one build was right; so was saying plainly that the line had been drawn at a round number.
4. **The second form: not built. Agreed.** 749.188 is the reason and is right: the way back sat at the last line, where the peak is usually out of reach either way. Dropping the "gate's cost halved" mark for this test, and saying so, was fair: the mark was not what the change is for, and fresh songs (61, 62) were added.
5. **The third form (the way back inside the line): approved, with its marks written first, and one change to them.** By construction it plants the peak exactly when v47 would (it keeps v47's own draw when none climbs), so "the peak planted as often as in v47" can only fail by a fault in the code; keep it as a check of the code (within 3 in 100), but do not let it carry the test. The marks that can fail, in every song: living builds above v47's; builds' middle words' fit within 0.02; the clean reading, gate off, builds holding a leap past an octave at or under the kept 17.5 in 100; the chosen tune at or over its floor; and on songs 55, 54, 58 soundness, pools of 10, a random pool pick no worse than v47's 6.5 in 100 (749.189).
6. **Hold-outs.** Every 4/4 song we have has now been run under a form of 749.182, song 59 included, so the third form has no song it has never touched unless a sealed one is spent. Song 63 stays reserved for the loop gate (749.185). Whether to spend song 50 on the third form is put to the writer (749.190).

## Next fix 964. Next finding 749.191.

## Addendum: the third form (luthier-v8-stage1 at 27f257d), merged

- **Reproduced.** Song 54 with every switch off: byte for byte. The clean reading of the third form on song 55 (`FORMS=line climb_held.py`): `line_held.json`'s figures exactly (planted 727 of v47's 756; the old way 117; gate off, 21.2 builds in 100 holding a leap). Its rule (`PREDICTION_line.md`, b57946c, 16:46) was committed before its result (6d7cd49, 17:20).
- **It fails by its own marks and by the list's** (living builds under v47's in songs 55, 49, 61; the clean reading over 17.5 in five songs of six). Not built; song 50 not run and still sealed, as the ledger says. Agreed.
- **The finding (the maintainer's 749.189, the trade): accepted.** Across the three forms the plant and the leaps trade one for one: about one planted build in six reaches the peak only by leaping. No choice among draws gives both, because 950 raises the carrying line's top and leaves its centre. The mend is to the line's register.
- **Next, approved: the reading first** (where kept songs' highest lines sit their centre against their top), then a form that lets the carrying line's centre rise toward the peak. Its marks, written before any run: living builds above v47's in every song; the clean reading, gate off, at or under the kept 17.5; the peak planted within 5 in 100 of v47's; the chorus's height over the verse within the kept middle half; 956's ceiling and 954's floor held; words' fit within 0.02; read both ways (749.179).
- **A fresh hold-out exists now:** song 64, "Go On Ahead" (songs/p74/lyric64.json; piano ballad, 4/4, 68, mezzo), locked and banked tonight, never run. The writer has ruled: song 64 is reserved as the centre form's hold-out (run once, only if the seen-song checks hold, its ledger line first); song 50 stays sealed for later.
- **Numbering.** 749.190 is the writer's hold-out ruling in the list for v50. The maintainer's "next finding 749.190" is 749.191; the centre reading takes 749.191 below.
