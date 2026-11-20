# Round two: the sceptic

## 1. The two strongest ideas from the others, and what method adds

**A. The evolutionist's breeding value (Idea 1).** Grade a song by how its covers fare in other hands, with the original dropped and the performer's pulling power controlled. This is my "same song, different records" idea done better: it gives every work a score and it yields the ceiling as a by-product. Three corrections.

- Covers are not fresh draws. Artists choose to cover what is already famous, and audiences reward a cover because they know the original. Controlling the original's chart peak does not remove fame acquired later. So u_w can still be biography. The clean sample is the era of rival simultaneous versions (before about 1960, several artists charting one new song in the same weeks), where no original had yet set the song's reputation. Estimate u_w there separately and see if the variance share holds.
- Charting covers are rare, so most works have O_w = 0 and u_w is mostly shrinkage. Report the reliability of u_w, Var(u) / (Var(u) + mean squared standard error), and use only works above a stated reliability. Otherwise a null against page features means nothing.
- The "heritability" from a logistic model is on a hidden scale and overstates what a rank correlation can reach. Convert it, or estimate the ceiling by the plain intraclass correlation as well.

**B. The cloud of versions: the physicist's stiff and sloppy directions (Idea 1) with the evolutionist's conserved core (Idea 3).** Five of us reached this separately, which makes it the room's main idea. It is also the one most at risk of being a tautology, so it needs the most discipline.

- "Much-covered songs have wide clouds" is the yardstick restated in other units. Only the predictive step is science: from the page and the original alone, predict which features later versions keep and how far they roam. Enforce it in time: fit on versions made before year t, test on versions after.
- Match the number of versions (rarefaction) and their mix of genres, or cloud volume just counts covers.
- The in-house stand-ins are contaminated. Lakh's multiple files are mostly transcriptions of the same record, and fans copy each other's files, so they are neither covers nor independent; near-duplicates will fake a rigid core. Agreement between transcription sources is worse for dense textures, so "agreement" will rediscover sparseness as a measurement artefact. Use real covers (Da-TACOS) or do not run it.

## 2. The weakest idea in the room, mine included

**Fitness from cover timing**: my own Idea 5(b) (a self-exciting model with a per-song baseline), the physicist's 3(b) and 3(c), and the evolutionist's 7(c). It will fail for two exact reasons. First, the brief says the cover lists hold each version's performer and title; it does not mention dates, and without dates none of these can be computed. Second, even with dates, each asks for one to three parameters per work, and most works have a handful of covers. Baseline rate and chain-reaction strength are hard to tell apart even with hundreds of events. With five, the estimate is the shrinkage prior plus the count, so the "fitness" will correlate above 0.95 with log cover count and we will have renamed the yardstick. Cover breadth with rarefaction (evolutionist Idea 4) does the same job and is estimable.

A warning of the same kind about the room's favourite cluster. About forty arrangement features from five papers are aimed at 1,400 fan-made MIDI files. On a hold-out of 700, inside year and tempo strata, the largest of forty null correlations is expected near 0.10, which is the size of effect the authors predict. Better-loved songs also attract fuller, more careful sequences, so measurement quality is tied to the yardstick. The producer's gate must come first, and the cluster needs one pre-declared combined score, not forty verdicts. The neuroscientist's advice to retest everything in three forms against two yardsticks multiplies the tests sixfold; it is right psychologically and needs a stated budget.

## 3. A new idea that exists only from reading the papers together: whose room is it?

The mathematician says the signal lives in the fibre (the sound), which the page throws away. The producer says the signal is room around the voice, made by the arranger. The physicist and evolutionist say a great song permits room. These cannot all be right, and nobody proposed the test that separates them: **decompose the sound feature itself, not the yardstick, across versions of the same work.**

For each feature f that held (spectral concentration, events per second, later lane clearance), over versions v of work w by performer a:

f_wv = mu + alpha_w + beta_a + era_t + e_wv, with alpha, beta random effects.

The work share Var(alpha) / Var(f) says how much of a record's sparseness travels with the song into other hands. Then regress the yardstick (better, the breeding value) on alpha_w and on the original's own deviation e_w,orig separately.

- Work share high and the yardstick follows alpha_w: the room belongs to the song. The recording finding was a page finding all along, read through a clean instrument, and the mathematician's "information is only lost" argument does not apply because the page determines its fibre. The next task is to find what on the page predicts alpha_w (the evolutionist's harmonic degeneracy is the first candidate). The owner's thesis survives in a new form: the page fixes how little a song needs.
- Work share low and the yardstick follows e: the room belongs to the producer. The engine's gains are in arranging, and the producer's nine rules are the deliverable.

Data: works with two or more charting versions among the 3,500 Essentia recordings (in hand, perhaps 100 to 200 works); Da-TACOS for scale.

## 4. Votes

**In hand:** re-test the surviving recording findings inside five-year, tempo and genre strata, against covers and lasting play separately (producer Idea 6 with the year control four of us asked for). Every theory in the room stands on the +0.25. If it is partly a dating of old slow ballads, we should know before building on it. One day's work.

**New data:** the no-recording laboratory, proposed independently by the songwriter, the evolutionist and me. Start with The Session's dump because it is on GitHub; pursue Hymnary counts for the crossed text-by-tune design. Caution: tunebook counts have their own rich-get-richer effect and need tune type and date controlled.

## 5. The theory the room is converging on, and whether I believe it

**A great song fixes a small, unmistakable core and leaves the rest open, so that the voice, the listener and later performers have room to complete it.**

I half believe it. For the "covered" half of the yardstick it is close to true by definition, since covers are a count of completions, and that is the problem: it becomes a discovery only if the openness can be predicted from the song before any cover exists. For the "still loved" half I doubt it, because dense, finished, uncoverable records are loved too. And the agreement of seven people is weak evidence: we all read the same four findings from one brief, so we are one observation, not seven. My odds: 40% that it survives as a predictor of cover reach after era is controlled, 15% that it explains lasting love.
