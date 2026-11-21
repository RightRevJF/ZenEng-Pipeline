# Card 3 (skeptic): Salganik, Dodds & Watts 2006, the MusicLab experiment

## Citation and link
Salganik, M. J., Dodds, P. S., & Watts, D. J. (2006). Experimental study of inequality and unpredictability in an
artificial cultural market. *Science* 311(5762), 854-856. doi:10.1126/science.1121066

- Author copy (article): https://pdodds.w3.uvm.edu/research/papers/years/2006/salganik2006a.pdf
- Supporting Online Material (SOM): https://pdodds.w3.uvm.edu/research/papers/years/2006/salganik2006a_supp.pdf
- Also read for context: Salganik & Watts 2009 (Topics in Cognitive Science), author copy at princeton.edu/~mjs3, and
  the MusicLab public data-release notes (oprdata.princeton.edu/Archive/cm/data_release.pdf).

What I actually read: the whole article (text, three figure captions, notes 1-24) and the whole SOM (design, subject
experience, recruitment, song selection, analysis, data-quality checks, robustness, Tables S1-S4, Figs S1-S10 captions,
its one reference). Both were read through a text-extraction tool, so the bar heights in Figs 1-2 (exact Gini and U values)
were not visible to me; the text itself reports only significance levels, not the values.

## The claim, and the data it rests on
Claim: letting people see what others chose makes success both more unequal and less predictable, and "quality" only
partly sets the outcome.

- **Participants:** 14,341 people on a website (MusicLab), mostly recruited from bolt.com, a teen and young-adult site.
  Experiment 1 (Oct-Dec 2004) n = 7,149; Experiment 2 (Dec 2004-Mar 2005) n = 7,192. About 80% in the US; most aged
  15-24; 36% female in Exp 1 vs 74% in Exp 2 (recruitment sources differed). Each person took part once.
- **Songs:** 48 previously unknown songs by 48 unknown bands, sampled from premium-member bands on purevolume.com and
  screened to drop anything with real popularity (touring, Warped Tour, many page hits). 51 of 133 contacted bands agreed;
  48 used. Two music experts recognized none. Genre is not stated (in practice indie rock/pop-punk era bands).
- **Task:** browse a menu, listen, give 1-5 stars, then optionally download free.
- **Worlds:** 20% of arrivals went to an *independent* world (song names only, about 1,400 people); 80% were split evenly
  across eight *social-influence* worlds (about 700 each) that also showed each song's download count within that world.
  All worlds started at zero downloads, so the eight are eight parallel histories of the same market.
- **Experiment 1:** 16 x 3 grid, positions shuffled for each person, counts shown (weak social signal).
- **Experiment 2:** one column sorted by current download count in the social worlds (strong social signal).
- **Success:** a song's market share, i.e. its downloads divided by all downloads in that world.
- **Quality:** a song's market share (or rank) in the independent world. The authors note it mixes the song's own appeal
  with the tastes of this subject pool. As a check, average star rating tracked the chance that a listen led to a download
  (r = 0.87 in Exp 1; Exp 2 reported as near identical but not shown).
- Totals: about 27,000 listens and 8,200 downloads (Exp 1); 25,900 listens and 10,300 downloads (Exp 2). Median person
  listened to 1 song and downloaded 0.

## The measure: from the notes or not?
Not from the notes. "Quality" here is a listener measure: how often this crowd, choosing without social cues, downloaded a
song. No score, transcription or audio feature enters anywhere. It also is not Jason's yardstick: it is a one-session,
first-hearing choice by teens about free downloads, not years of love or other musicians choosing to cover a song.

## How big the effect is and how it was checked
- **Inequality (Gini of market shares):** every one of the 8 social worlds was more unequal than the independent world in
  both experiments, and the gap was larger under the stronger signal of Exp 2 (p < .01 Exp 1, p < .001 Exp 2 per SOM). The
  independent baseline was computed on 1,000 random half-splits so its sample size matched a social world.
- **Unpredictability (U):** for each song, the average absolute difference in its market share across all 28 pairs of
  social worlds; U averages that over songs. Baseline: the same measure between random halves of the independent world
  (1,000 splits). Social worlds were more unpredictable than the baseline in both experiments, more so in Exp 2
  (same significance levels).
- **Stability:** Gini and U curves over arrivals (Figs S9-S10) flattened, so the authors argue more subjects would not
  change the picture. Contaminated records (people told about a band by friends or the band) were flagged out; the authors
  argue leftover contamination would shrink, not inflate, the effects.
- **Replication:** 8 worlds x 2 experiments, all pointing the same way. No independent lab replication in this paper.
- **Quality vs success (Fig 3):** success rises with quality, convexly, and more convexly in Exp 2. But the spread is wide:
  "the best songs rarely did poorly, and the worst rarely did well"; nearly any outcome was possible in between. By
  market share the top songs were the most unpredictable; by rank, the middle songs were. The authors argue part of the
  convex "superstar" shape is made by social influence itself, not by preexisting taste.
- **Size in prediction terms (from the 2009 follow-up, not this paper):** knowing the independent-world shares cut error in
  predicting an Exp 2 social world by only about 16%; about 38% in a third experiment with a different pool.
- **Limits stated by the authors:** small catalogue, one visit per person, no word of mouth, no marketing, critics or radio;
  they think real markets have *stronger* social influence than this.

## What it says about Jason's yardstick
Against note-based prediction of greatness:
- If a market is path-dependent, a large share of who ends up on top is not in the song at all, so any predictor built on
  intrinsic features (notes included) has a hard ceiling well below perfect, even with perfect measurement. This fits what
  the repo already found: notes explain about 4% of covers, and the shape and S tests failed. Some of that failure may be
  ceiling, not bad features.
- Covers are themselves social choices: musicians cover what they and their audiences already know, which is a textbook
  cumulative-advantage channel. Long-run love is partly familiarity, which also compounds.
- The repo finding that covers and views are uncorrelated once release year is held (r = 0.00) is what you would expect if
  each channel is largely its own history with only a weak common quality factor beneath both.

In fairness to the yardstick:
- The experiment measures first-session downloads of unknown songs, over weeks, by one demographic. It says nothing directly
  about decades. Later work (van de Rijt 2019) finds that, given enough time and choices, better options often win back the
  lead; long-run love may self-correct more than early downloads do.
- Covers are a choice by skilled listeners who play the song, which may weigh musical material more than a teen's click.
- Even here, quality was not irrelevant: the extremes were fairly safe. A notes measure could still flag the bottom or the
  top tail without predicting rank in the middle. That is a narrower, testable goal than "predict greatness".
- Its "quality" is itself only a crowd's taste, so the paper cannot say how much of that taste lives in the notes.

Net: it does not show that the notes do not matter; it shows that the yardstick has a large non-musical component, so tests
should report a ceiling and aim for tail detection, not full ranking.

## One test Luthier could run
**MusicLab ceiling-and-notes test (public corpus: MusicLab data release, 48 mp3s plus per-world downloads, ratings,
listens; terms of use unstated, so ask Salganik before publishing results).**
1. Ceiling: for each song compute mean market share across the 8 social worlds and its between-world variance in Exp 1 and
   Exp 2. Reliability = share of variance that is between songs rather than between worlds. That is the most any
   song-intrinsic predictor can explain of social success here; report it alongside every later note-model R2 on G.
2. Notes: transcribe chords and melody for the 48 songs (hand or chord recognizer checked by ear), compute the one note
   measure that replicated in the repo (chord repetition within a section) plus the Cheung-style surprise term, frozen
   before looking at outcomes.
3. Prediction: less chord repetition goes with higher independent-world appeal (download-per-listen rate and mean
   rating), and the effect is mainly in the tails (top and bottom 10 songs separated better than chance).
4. Failure condition: |r| < 0.15 with independent appeal and with mean rating, and no tail separation (AUC < 0.6), in both
   experiments' independent worlds. With n = 48, only |r| above about 0.28 can pass p < .05, so treat a pass as a lead to
   re-test on SHS100K/Discogs-VI, not proof.

## Leads
1. Salganik & Watts (2008). Leading the herd astray: an experimental study of self-fulfilling prophecies in an artificial
   cultural market. *Social Psychology Quarterly* 71(4), 338-355. doi:10.1177/019027250807100404. Inverts the download
   counts: shows how far false popularity can push bad songs and whether good ones recover.
2. Salganik & Watts (2009). Web-based experiments for the study of collective social dynamics in cultural markets.
   *Topics in Cognitive Science* 1(3), 439-468. doi:10.1111/j.1756-8765.2009.01030.x. Adds a new subject pool and the
   prediction-error numbers; best source for how much "appeal" predicts success.
3. van de Rijt (2019). Self-correcting dynamics in social influence processes. *American Journal of Sociology* 124(5),
   1468-1495. doi:10.1086/702899. The strongest counter: given time, better options tend to regain the lead, which bears on
   long-run love.
4. Abeliuk, Berbeglia, Cebrian & Van Hentenryck (2015). The benefits of social influence in optimized cultural markets.
   *PLoS ONE* 10(4), e0121934. doi:10.1371/journal.pone.0121934. Models the MusicLab data and shows which displays let
   quality surface; separates position effects from popularity effects.
5. Krumme, Cebrian, Pickard & Pentland (2012). Quantifying social influence in an online cultural market. *PLoS ONE* 7(5),
   e33785. doi:10.1371/journal.pone.0033785. Splits a choice into "listen" (socially driven) and "download given listen"
   (more song-driven), a useful template for separating song from history in G.
