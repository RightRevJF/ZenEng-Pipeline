# Way 3 (the marriage of tune and words): predictions written before any fit was computed (18 Nov 2026)
The reading: for every sung syllable, the word's WEIGHT (0 for a one-syllable function word; for other syllables, 1 if stressed and 0.4 if not, plus up to 1 for a rare word)
against the note's SALIENCE (its length, its place in the bar, its height within its line, each standardised within the song). The fit is their rank correlation over the song.
The control: the same song with each line's words dealt out again in a random order over that line's notes (200 times).
M1. Kept songs' fit beats their own shuffled-words control in at least four songs in five (above the control's 95th percentile).
M2. The engine's builds fit their words less well than kept songs do (median fit lower), because the engine reads stress and nothing else of a word.
M3. Among STRESSED syllables only, kept songs still give the weightier (rarer, content) words more salience (median fit over 0), which is the part the engine does not do.
M4. Length carries more of the fit than height does.
M5. The fit will not rank kept songs by chart record beyond chance (|rho| under 0.15). I hope to be wrong.
