# The sceptic's contribution: attack the framing, then rebuild it

## 1. Diagnosis

I do not think the day's testing showed that the page carries nothing. I think it showed that this particular experiment could not have seen the page even if the page mattered. Five things were stacked against it, and none of them is about music.

1. **The sample was pre-filtered on the answer.** Every song is already a Hot 100 hit. If the written tune works as a gate (a tune must be good enough to pass, and after that other things decide), then among songs that passed there is no gradient left to find. Selection can also create false zeros and reversals: a hit needs a good tune OR a famous performer OR a big push, so among hits those causes become negatively related to one another (collider bias, the same reason hospital patients show odd disease correlations).
2. **The yardstick measures a song's biography as much as the song.** Later love is moved by film placements, a death, one famous cover, a sample. Cover counts are moved by era (before about 1965 everyone recorded everyone's songs), by genre custom (jazz, country), and by how easy a song is to play. Sparse, slow, low-band recordings also describe old ballads, which have had the longest time and the friendliest culture for covers. The +0.25 may be partly a year-and-genre effect.
3. **Luck sets a ceiling nobody has measured.** If only a third of the yardstick is intrinsic to the song, a perfect musical predictor scores about 0.58, not 1.0. Without the ceiling, 0.25 cannot be called small or large.
4. **The page was measured badly and the recording was measured well.** Essentia numbers are computed from the audio itself. The tunes are automatic or crowd transcriptions, often of one section. Measurement error shrinks correlations. "Recording holds, page fails" is confounded with "clean instrument holds, noisy instrument fails".
5. **The tests were powered for big effects.** At 1,500 songs a single test detects a rank correlation of about 0.07 (0.10 after correcting for 40 tests). At 128 songs, the word-stress test detects only 0.25 or more. Twenty independent page effects of 0.05 each would add up to about 0.22 jointly and every one would have "failed".

There is a sixth possibility of a different kind: greatness may have no main effect on the page at all, only an interaction (this tune with these words, this voice, this year). That is still mathematics, but it needs a crossed design, which the Hot 100 does not supply.

**The ceiling arithmetic, for reference.** Write yardstick = intrinsic + history + luck, with intrinsic share s of the variance. A perfect predictor of the intrinsic part reaches r = sqrt(s). An observed r is also shrunk by measurement reliability of the feature, r_xx: r_obs = r_true * sqrt(r_xx). So:

| intrinsic share s | ceiling r | 0.25 is this fraction of what can be explained (0.0625 / s) |
|---|---|---|
| 0.10 | 0.32 | 62% |
| 0.20 | 0.45 | 31% |
| 0.35 | 0.59 | 18% |
| 0.50 | 0.71 | 12% |

Ideas 1 and 2 below estimate s. Until then the project does not know whether it is nearly finished or barely begun.

## 2. Ideas, most promising first

### Idea 1. Move the laboratory to where the page is all there is: hymn tunes, with texts and tunes crossed

**Plain words.** Hymnody is the one large tradition where tunes and words are routinely swapped. One tune carries many texts, one text is sung to rival tunes, and there is no recording, no star and no marketing budget. The filter has run for two to four centuries. So "how many hymnals print this tune" and "how many different texts has it been given" are a wordless, performer-free yardstick for the page, and the swapping gives a true crossed experiment for the interaction question.

**Mathematics.** Build the table n_ij = number of hymnals printing text i with tune j (many cells empty). Fit a Poisson model: log E[n_ij] = mu + a_i + b_j + g_ij, with a_i (text), b_j (tune), g_ij (pairing) as random effects, plus fixed terms for metre and century. Report the three variance shares. b_j is each tune's greatness with words averaged out. Then run every failed page measure against b_j, on full range, no hit filter. Rival-tune contests (one text, two tunes of the same metre, one won) give a paired test: sign test on feature difference between winner and loser.

**Data.** Hymn tunes are here, ungraded. The grades need Hymnary.org's instance counts (tune by text by hymnal). Hymnary offers data exports; I have not confirmed a GitHub or Zenodo mirror. A fallback with the same logic: The Session's Irish tune archive, whose data dump is on GitHub and includes how many members saved each tune and how many recordings include it.

**Proved wrong if.** Var(b) is near zero (tunes do not differ once text and metre are fixed), or Var(b) is solid and none of the page measures predicts it at 0.1 or better on thousands of tunes with full range.

**Implication.** Large Var(b), measures work: the Hot 100 was the wrong lab and the page thesis lives. Large Var(b), measures fail: tunes differ in greatness but we have not found the right mathematics, so keep inventing measures. Large Var(g): greatness is a marriage, and the engine must score pairings, never tunes alone.

**Odds.** 70% that tune variance is substantial; 40% that at least one already-failed page measure clears 0.1 against it.

### Idea 2. Same song, different records: how much of the yardstick belongs to the work at all

**Plain words.** Many works charted more than once in different artists' hands. If the page matters, two different hit recordings of the same work should resemble each other in later love more than two unrelated hits do. That resemblance is the share of the yardstick the page can ever explain. It needs no musical feature, so it cannot fail for lack of the right feature.

**Mathematics.** Take works with two or more charting versions (link Hot 100 entries through SecondHandSongs). Use only the "still loved" half of the yardstick per recording, residualised on release year, genre and chart peak, because the cover count is shared within a work by construction. Model y_wk = work_w + e_wk. Intraclass correlation ICC = Var(work) / (Var(work) + Var(e)), by REML, with a bootstrap interval. Then the mirror: same performer, different works, giving the performer share (already known, about 15%). A within-work regression (subtract the work mean from y and from each sound feature) tests the recording findings with the page held exactly fixed.

**Data.** All here: chart histories, cover lists, Spotify readings, Essentia numbers. Expect a few hundred works; an ICC of 0.2 is detectable at 300 pairs.

**Proved wrong if.** ICC is below about 0.05 after a check that the second version is not simply riding the first (compare cases where the later version is the bigger one).

**Implication.** ICC near 0: on this yardstick the page explains nothing among hits and no cleverness will change that; change the yardstick or the population. ICC of 0.3 or more: the page ceiling is about 0.55 and forty failures mean wrong measures or bad transcriptions, not a wrong thesis.

**Odds.** 60% that ICC lands between 0.15 and 0.4.

### Idea 3. Total page variance without naming any feature (the heritability trick)

**Plain words.** Geneticists estimate how heritable height is without finding a single gene: they ask whether people with more similar genomes have more similar heights. Do the same with songs. Ask whether songs with more similar pages have more similar fates, using a generic similarity that presupposes no theory. This replaces forty separate verdicts with one number, and it can include an explicit interaction term.

**Mathematics.** Build an n by n similarity matrix K_page (for example a kernel on interval-and-duration n-gram counts, or exp(-NCD) where NCD is normalised compression distance: how much better two tunes compress together than apart). Build K_sound from the 127 Essentia numbers. Fit y ~ N(X*beta, s_p^2 K_page + s_s^2 K_sound + s_ps^2 (K_page ∘ K_sound) + s_e^2 I) by REML, where X holds year and genre and ∘ is the entrywise product (two songs are alike in the interaction term only if alike on both page and sound). Report each share with a likelihood-ratio test. Control: permute song labels within year to get the null distribution of each share.

**Data.** All here. About 1,400 to 3,000 songs have both page and sound.

**Proved wrong if.** s_p^2 share is indistinguishable from the permutation null with a kernel that demonstrably recovers known structure (it should recover composer or genre well above chance; if it cannot, the kernel is at fault, not the page).

**Implication.** Page share near 0 and sound share modest: among hits, stop on the page. Page share of 5 to 15%: many small effects, so build a combined score, not a single shape. Interaction share bigger than both: the plotted "shape" lives in the joint space of tune and sound.

**Odds.** 35% that the page share is clearly above null among hits; 50% that the interaction term is at least as large as the page term.

### Idea 4. Measure the instruments before trusting the verdicts

**Plain words.** Three transcription sources overlap. Compute every page measure on the same song from two sources and see whether the two answers agree. If they agree poorly, the measure was never tested, only its noise was. This is a week of checking that reprices every failure in the brief.

**Mathematics.** For each feature f, reliability r_xx(f) = correlation of f across two sources on shared songs. Corrected effect r_true = r_obs / sqrt(r_xx * r_yy), where r_yy is the yardstick's reliability (lower bound from the correlation c between its two halves, loved and covered: r_yy = 2c / (1 + c)). Detectable effect at 80% power is 2.8 / sqrt(n): 0.25 at n = 128, 0.09 at 900, 0.07 at 1,500, 0.05 at 3,100. Publish for each failed test the largest true effect it could have missed: (0.07 or as applicable) / sqrt(r_xx * r_yy). Reverse check: add noise to the Essentia numbers until their reliability matches the transcriptions and see whether the recording findings survive.

**Data.** All here.

**Proved wrong if.** Reliabilities are 0.8 or higher across the board. Then the failures stand as measured.

**Implication.** Low reliability (0.3 to 0.5): the page was not refuted; rerun the best ideas on the cleanest human-entered source only, or on hymn scores, which are exact. High reliability: the page failures are real for this population and Ideas 1 and 5 become the only route.

**Odds.** 65% that at least a third of the page measures have reliability under 0.5.

### Idea 5. Split the yardstick in two, and clean each half of biography

**Plain words.** "Loved" attaches to a record; "covered" attaches to a song. Averaging them hides two kinds of greatness: songs great on the page (standards, covered by everyone, no single version dominant) and records great as records (rarely covered well). A feature can help one kind and hurt the other and average to zero. Also, covers breed covers: one famous version triggers twenty more, which is history, not the song. Separate the song's own pull from the chain reaction, and count instrumental covers separately, since that is the owner's "moves people without words" in countable form.

**Mathematics.** (a) Concentration H_w = sum over versions of (share of the work's total streams)^2. Low H marks page-great, high H record-great. Fit a two-class mixture of regressions and test whether feature slopes differ by class. (b) Cover arrivals as a self-exciting process: rate_w(t) = m_w * g(t - release) + sum over earlier covers of a * phi(t - t_k), with a shared kernel phi and a per-song baseline m_w, fitted by maximum likelihood with shrinkage on m_w. m_w is the rate of independent discoveries, the cleaned yardstick. (c) Simpler stand-ins: number of distinct genres and decades among coverers (entropy), number of instrumental versions, all standardised within release year and genre. (d) Negative control: any feature that predicts release year as well as it predicts the yardstick is suspect; re-test inside five-year, single-genre strata.

**Data.** Cover lists with performers are here; dates and instrumental flags exist on SecondHandSongs and need confirming in our copy. Biography flags (film use, sampling) are not here.

**Proved wrong if.** Page measures score zero against m_w and against instrumental cover counts as well, and slopes do not differ between the two classes.

**Implication.** If the page predicts the cover half only, the engine should aim at "covered", which is the right target for a songwriter without a star's voice. If the +0.25 shrinks inside strata, the recording result is partly a dating effect.

**Odds.** 55% that the recording findings shrink by a third or more within strata; 40% that some page measure reaches 0.1 against instrumental covers.

### Idea 6. Ask the engine's real question: competent versus chosen, not good hit versus great hit

**Plain words.** A song engine's output lands among all competent songs, not among hits. What it needs is a filter that separates the keepers from the heap, which is the bottom and middle of the range, exactly what the Hot 100 sample cut away. Test whether the page separates singles from album tracks by the same artist in the same year, hits from never-charted songs, and standards from the rest of their repertory.

**Mathematics.** Matched pairs (same artist, same year, one charted, one not). For each feature, d = feature(charted) - feature(not); sign test and paired effect size. Jointly: conditional logistic regression, reported as AUC (chance that the model ranks the charted song above its twin). Range check for each feature: U = SD(all songs) / SD(hits). If U is well above 1, correct the hit-only result by r_full = r*U / sqrt(1 + r^2 (U^2 - 1)). If U is about 1 and AUC is about 0.5, the feature is not a gate either. Final out-of-time test: freeze the score, grade songs from 2006 to 2015 by their standing today.

**Data.** The 17,000 ungraded MIDI arrangements and 20,000 Hooktheory songs can be marked charted or not from the chart histories. Caution: both collections were made by fans, so "ungraded" is not "unloved"; album tracks by charting artists are the cleanest contrast.

**Proved wrong if.** Paired AUC for the full page model is under 0.55 on thousands of pairs.

**Implication.** AUC of 0.65 or more: the page is a gate. The engine gets a working filter, and "great" becomes "passes the gate, then gets the sound and the pairing right". AUC near 0.5: the page does not even gate, and the project should move its mathematics to the sound and the marriage.

**Odds.** 60% for AUC above 0.6 on singles versus album tracks.

## 3. The wild idea

**A great song is an unfinished one.** The yardstick counts covers, which is to say it counts how many different people found room to finish the song their own way. The recording findings say the same thing from the other side: few events, sparse spectrum, space left open. So perhaps greatness is not a shape the song has but the size of the family of shapes it permits: a small fixed core and a very large space of realisations that are all still recognisably it. Measured: for works with several independent MIDI arrangements in Lakh, take fixed-size sets of versions (so cover count cannot leak in), align them, and compute the core (the fraction of melodic and harmonic events all versions share) and the spread (mean pairwise distance in everything else). Greatness would be high spread per unit of core: much freedom bought with little constraint. If true, the engine should write less, and the statue comparison is the wrong picture. The right one is the block of marble that a hundred sculptors each want to carve.

## What I would do first

Ideas 4 and 2 use only data on hand and take days. Between them they fix the ceiling and tell us whether the page was ever tested. Idea 1 is the one I expect to change the project, because it is the only design where the owner's claim, music without words, is tested with the words, the voice and the luck of the charts actually removed.
