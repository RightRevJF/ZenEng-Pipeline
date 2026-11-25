# Luthier list for v49 (since v48)

25 November 2026. Luthier v48 (three trials, all failed by their checks written first; nothing built; the engine writes v47's notes) is reviewed (`lib/luthier/REVIEW_stage33.md`) and merged into main. Song 54, the title-line reading, the drafted sections and the held-fit reading on song 55 reproduce; the check passes. Next finding 749.186; next fix 964.

## In short

Three honest failures, and one finding worth more than any of them: a gate changes the fits, so every gate trial is now read both ways (749.179). That reading shows why one leap would never help: a build that leaps past an octave leaps back.

Song 63 was rightly not run and stays sealed.

Next is the draw, as you proposed: why it leaps too far (749.182), why it holds weak title words long (749.183), then 749.171 and rhythm scaling. The loop gate with a chance waits behind them (749.185).

## Standing check, added

- 749.179 (yours, accepted): every gate trial is read both ways: the whole engine, fits and all (the test of record), and the record's fitted spec with only the gate changed (the clean reading, `held_fit.py`'s method).

## Items

### 749.182 Why the draw leaps past an octave
**Problem.** Builds leap past an octave inside a line about twice as often as kept songs (kept: 28 songs of 160 hold one; the kept 90th is 4.4 in a thousand notes), and nearly always out and back (749.180). The ban screens them at a cost of 66 to 111 living builds in a thousand.
**Evidence.** `studies/v48_trials/held_fit.json`; `studies/proposed_v47/RESULT.md`.
**Fix.** A reading first, rule committed before it, with the fitted spec held: for builds with no gate, where the leaps fall (inside a line, between a line's end and the next line's start carried inside the line by a pickup, at a section change), what move weights and register targets were in force, and how the out-and-back pairs sit (the far note's length and syllable). Set beside the kept songs' rare leaps read the same way. Then a change to the draw, not a gate.
**Check.** Written with the reading. The aim: builds' rate of such leaps at or near the kept rate with no gate, so the ban passes over few builds.

### 749.183 Why the draw holds weak title words long
**Problem.** With no gate, a quarter of song 49's living builds put a title line's longest note on a weak syllable before its last word (kept: 9 lines in 100). The judging mostly screens it (one chosen title line in 21), but the draw makes it.
**Evidence.** `studies/v48_trials/RESULT.md` section 2; `title_lines.json`.
**Fix.** A reading first, rule committed before it: in hook and title lines, how the word weights (`word_weight`) and the line-end rule share out length, against the kept title lines' own lengths by syllable kind.
**Check.** Written with the reading.

### 749.184 Two nits in the trial switches
**Problem.** `LUTHIER_LOOP` turns the loop gate on for any non-empty value ("off" and "0" included). The title form "inside" also passes over a weak syllable inside the last word that is not its last, where its comment says "before the last word" (kept share 0, so no cost).
**Fix.** Map `LUTHIER_LOOP` as the other switches are; make the comment say what the code does, or the code what the comment says.
**Check.** Song 54 byte for byte with every switch off.

### 749.185 The loop gate with a chance (waits)
**Problem.** Any redraw to a line empties the far side (749.181): the gentle gate left 0.1 verses in 100 over the kept 75th, where kept songs keep 25.
**Fix.** When loop-less chords are wanted again: redraw a verse over the kept 75th with a chance set so that about 25 in 100 stay over it, rule first, with the same three checks as 749.178 and song 63 as hold-out, its ledger line first.
**Check.** As 749.178's.

## Carried, open

- 749.171 what the engine does inside a line it gives one bar.
- Rhythm scaling leans low.
- 749.144 song 58's bars of rest; 749.147 a short line in a long slot; 749.148 to 749.152 the hymn items; 749.163.
- 749.165, 749.170: the region, as a change to the draw (fewer notes on three pitches).

## Closed

- 749.176 (the ban stands; the kept-shaped form gives nothing back), 749.177 (961 stays a setting; the judging screens it), 749.178 (failed; song 63 sealed), 749.179, 749.180, 749.181.
