# Review 33: Luthier v48 (Window 205, Module 27.129, Table HO)

25 November 2026, the songwriting session. Branch luthier-v8-stage1 at c5a2dab (main merged in), merged into main.

## Reproduced

- `song_from_lyric.py --check`: 11 records, every stamped table the table at hand.
- Song 54 rerun with every switch off (1000 builds, 12 drafts, PYTHONHASHSEED 0): its record byte for byte (256 living; pick b71ab3ba9f1d). The engine writes v47's notes.
- The kept title-line reading (`title_lines.py`): `title_lines.json` byte for byte (73, 18, 0, 9 in 100; 387 lines; 18 kept songs in 100 hold at least one weak-before-the-last-word title line).
- The loop forms on drafted sections (`drafts.py`): `drafts.json` byte for byte (gentle: 65 verses in 100 at or under the kept median, 0.1 over the 75th).
- The held-fit reading on song 55 (`held_fit.py`): its figures exactly (ban 223 living, 69 passed over; one leap 226, 66; no gate 292).
- The checks (523d170, 13:12) were committed before the results (22db30b, 13:56); the ledger line for song 63 came with the checks, and song 63 was not run.
- Code read: the three forms sit behind switches that are off; with them off the gates are v47's.

## Rulings

1. **749.176: the ban stands. Agreed.** Check 1 failed by the rule as written.
2. **749.179: accepted, and it is the most useful thing in this window.** A gate passes through fix 930's fits, so a changed gate is a changed engine; v47's own figure for the octave ban's cost mixed the gate with a refit. From now on every gate trial is read both ways: the whole engine (the test of record) and the record's fitted spec with only the gate changed (the clean reading). The held-fit reading answers the session's question better than the trial did: one leap allowed gives back 3 to 6 builds of the 66 to 111 the ban takes, because a build that leaps past an octave nearly always leaps back (749.180). The kept-shaped form is the ban by another name. Closed.
3. **749.177: the reading passes its rule; the gate fails its cost; not built. Agreed.** What it settles: kept songs hold a weak last syllable longest in about one title line in six, so 961 as first written was wrong as a rule, and a weak syllable before the last word is uncommon (9 in 100) but not unknown (18 kept songs in 100). The chosen v47 tunes already sit at or under the kept rate (one title line in 21), so the judging screens it. 961 stays a setting; no default is needed. A nit for when the form is next touched: the "inside" form also passes over a weak syllable inside the last word that is not its last syllable (`any(...)` reads every note from the longest on); the kept share there is 0, so it costs nothing, but its comment says only "before the last word" (749.184).
4. **749.178: fails all three; song 63 not run and still sealed. Agreed.** 749.181 is right and general: a redraw to a line empties the far side. The form that thins the top with a chance is the one to try if loop-less chords are still wanted; it waits behind the draw (749.185).
5. **A nit:** `LUTHIER_LOOP` turns the loop gate on for any non-empty value, "off" and "0" included, where the other two switches map their values (749.184).
6. **Next: the draw. Agreed, in your order.** Both failed gates found a fault of the draw that a gate can only screen: it leaps past an octave twice as often as kept songs, and it holds weak title words long in a quarter of song 49's builds. Read them in the draw, rule first, with the fitted spec held (749.182, 749.183), then 749.171 and rhythm scaling.

## Next fix 964. Next finding 749.186.
