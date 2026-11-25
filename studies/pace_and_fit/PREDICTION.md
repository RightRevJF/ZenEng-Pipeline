# Pace and the words' fit (749.154's reading, proposed in Luthier v46): the rule, written before any reading

25 November 2026, by the writer's side, in Review 31, at the maintainer's proposal. Nothing below has been computed on the kept songs before this file was committed.

**The question.** Window 203 read that the whole words' fit (one rank correlation over every note of a song, of each syllable's weight against its note's salience, with note length ranked across the song) may count a busy line against the song even when each of its weighty syllables stands out within its own line. If so, kept songs whose sections change pace more should have a lower whole fit at the same line-by-line fit.

**Songs.** The kept 4/4 pop songs (`lib/luthier/kept_corpus.py`) whose words the lexicon reads, with 40 weighted notes or more, as `lib/luthier/make_kept_word_weight.py` reads them (weights 0, 0.4, 1 from the lexicon; words it cannot read left out).

**Measures (per song).**
- Whole fit: `word_weight.salience` (length, place, height, as the engine reads them) against the weights, Spearman over the song's weighted notes (the engine's fit, kept form).
- Line fit: the same correlation inside each sung line with 4 or more weighted notes and some spread in both, averaged over the song's lines.
- Change of pace: the spread of notes a sung bar across the song's sections (by the corpus's section labels): the standard deviation of log notes a sung bar over sections with 2 or more sung bars, weighted by bars.

**The model.** Whole fit on line fit and change of pace, all standardised; ordinary least squares, robust errors (HC1).

**The rule.**
- **The reading holds** if the coefficient on change of pace is -0.15 or stronger with p < .05.
- **It does not hold** if the coefficient is above -0.05, or positive.
- **Unsettled** between.
- Also reported, deciding nothing: the same with length taken out of salience (place and height only), where the reading predicts the pace effect should vanish; and the kept songs' whole fit against line fit alone (how much of the whole fit the lines carry).

**What I expect.** The reading holds weakly: about -0.10 to -0.20, and near zero without length. Held loosely.

**What it cannot say.** Kept songs are 4/4 chart hits, transcribed by ear; section labels are the corpus's; a negative coefficient would say the whole fit marks pace down in kept songs too, not which fit is the truer.
