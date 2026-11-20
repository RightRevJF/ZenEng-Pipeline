# The borrows fitted to the aimed song: the rule, written before the trial

**How we got here.** Two ideas were tried and failed first (studies/bar_fit: keeping a returning line's bars costs the words; keeping them only where the words allow gains nothing). A third idea, that kept songs write later verses to the first verse's stresses, was measured and is wrong: Luthier's later verses match their first verses bar for bar as well as kept songs' do (`match.py`), and Luthier's songs sing a bar's rhythm again about as often as kept songs at large (`near.py`). The shortfall is only against each song's own aimed kept song. So this is the "too like the middle" fault under another name: where the aim does not reach, every song lands at the kept middle.

**The look (`reach.py`, before this rule was written).** One dial already in the engine moves these readings a long way: the share of fresh lines that sing an earlier line of their section again (the figure borrow), and the share that take its rhythm with new notes (the rhythm borrow). It is set the same for every song (0.8 and 0). Across its range a song's bars on a figure already sung move by about a tenth.

**The idea.** Fit the two borrows to the aimed song, as the step, leap and repeat weights are fitted: try five settings (0 and 0; 0.8 and 0; 1 and 0; 0.5 and 0.5; 0 and 1) on short trial runs and keep the one whose builds stand nearest the aimed song on bars on a figure already sung and bars on a rhythm already sung together (each gap in kept middle-half widths).

**Because the look came first,** the trial is on new draws: the fit on one seed (60 tries a setting), the reading on another (150 tries), the engine's fixed setting against the fitted one. And the hold-out, song 59, is the honest test: it was not in mind when the dial was found to matter, and it aims low where the three practice songs aim high.

**The check, on songs 55, 54 and 58.**

1. The summed gap to the aim on the two readings shrinks in at least two of the three songs and grows by more than 0.05 kept widths in none.
2. The words' fit, whole, falls by no more than 0.03 in any song.
3. At least eight tenths as many builds pass the gates.

**Prediction for the hold-out (read, not counted):** song 59's fit chooses less borrowing than the engine's 0.8, and its summed gap shrinks.

It passes if 1, 2 and 3 hold. If it passes and the hold-out's prediction fails, it is not built: a fix that works only on the songs it was found on is not a fix.
