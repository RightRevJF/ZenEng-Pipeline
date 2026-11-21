# Card 4: dos Santos & Figueiredo 2024, borrowings and the original's popularity

## Citation and link
dos Santos, G. S. S., & Figueiredo, F. (2024). Assessing the Impact of Sampling, Remixes, and Covers on Original Song
Popularity. *Proc. 1st Latin American Music Information Retrieval Workshop (LAMIR)*, Rio de Janeiro. arXiv:2411.01242.
Universidade Federal de Minas Gerais. Data: github.com/uai-ufmg/whosampleddata.

- Full text: https://arxiv.org/html/2411.01242v1
- What I read: the whole v1 HTML (abstract, sections 1-5, three figures and captions, footnotes 1-7, all 12 references).
  It is a short workshop paper with no appendix or supplement beyond the data repo. Read through a text-extraction tool
  in several passes, section by section, so figure values (the ATE histogram) were not visible to me.
- Version caveat: the abs page (arxiv.org/abs/2411.01242) was blocked in this session, so I could not confirm whether a
  v2 exists. Everything below is v1.

## The claim, and the data it rests on
Claim: when a new track samples, remixes or covers an older one, search interest in the older song sometimes rises at
the new track's release, and in many cases the new track's interest series predicts the original's later interest.

- **Borrowing graph:** WhoSampled, crawled 2019, about 700,000 songs (samples, covers, remixes, community-moderated).
- **Linking:** Wikidata lookups for Freebase IDs (needed for Google Trends topic queries). 699k songs -> 111k musical
  works -> 44,857 with a Freebase ID -> 4,477 borrowing pairs after fuzzy title/artist matching (difflib, cutoff 0.55)
  -> 4,360 songs with Trends data.
- **Window:** monthly global Google Trends, 12 months before and 12 after the borrowing's release; all-zero series
  dropped. Final set: **884 borrowing pairs**. Because Trends starts in 2004, every borrowing here is from 2005 or later.
- **Success:** Google Trends search interest in the original (each series scaled to peak at 100). Not sales, streams,
  chart runs, or years of listening.
- No split of the 884 by type: we are not told how many are covers versus samples versus remixes. WhoSampled is
  sample-heavy, so covers are probably a minority.

## The measure: from the notes or not?
Not from the notes. No score, chord or audio feature appears. The paper is about a social channel: how a later
recording changes attention to an earlier one. It bears on the yardstick (covers and longevity), not on the notes.

## How big the effect is and how it was checked
- **Short term (regression discontinuity in time):** per pair, interest regressed on time, a post-release step, and a
  slope change, with the borrowing's release month as the cutoff. The step is the effect, reported in relative terms.
  82 of 884 pairs (9.3%) had p < .05. No numeric median or range is given, only a log-scale histogram. Extreme
  effects (often originals with no prior search interest, e.g. Etta James sampled by Flo Rida) were inspected by hand
  and dropped, a post hoc rule. One named negative case (Lana Del Rey, about -152%). The split of positive versus
  negative effects among the 82 is not reported.
- **Long term (Granger causality):** borrowing's Trends series as predictor of the original's, up to 10 monthly
  lags, SSR F-test, p < .05. 117 pairs "significant", given as 64% with an unclear base (117 of 182 is 64%; 117 of 884
  is 13%). No reverse-direction test, no stationarity check, no rule for which lag counts.
- **Counts do not reconcile:** the introduction says 182 pairs (20%) show any causal evidence and 82 of them (45%)
  show RDD effects; section 4 gives 82 as 9.3% of 884; 117 Granger hits cannot be a subset of 82.
- **What is missing:** no control series, no placebo cutoffs, no comparison with unborrowed songs, no correction
  for 884 separate tests (at p < .05 about 44 false hits are expected by chance, so 82 is only about twice the noise
  floor), no seasonal adjustment, no handling of repeated borrowings of the same original. Granger on two Trends
  series that share search seasonality and news cycles will flag many pairs without any causal link.
- **No breakdown by borrowing type**, so nothing here is specific to covers. The positive examples shown are mostly
  samples reviving late-1970s to 1980s tracks (Dead or Alive, The Cure via Kid Rock, LMFAO via Natalie La Rose).

Net: a plausible direction (borrowing can lift the original) on a small, linked sample, with weak checks. Treat it as
suggestive evidence of feedback, not a measured effect size.

## What it says about Jason's yardstick (lasting love plus covers)
- **Covers may partly cause lasting love.** The paper's point, and the older Schuster et al. 2019 sales study it
  cites, is that a new version can send listeners back to the original. If so, a song's cover count and its later
  "still loved" score are not two independent readings of its quality: some of the second is produced by the first,
  and fame feeds covers in turn (musicians cover what audiences know). That is a feedback loop, the cumulative-
  advantage picture from card 3 (MusicLab), now with a second channel.
- **Consequence for G:** adding covers and longevity into one target double-counts whatever the loop amplifies,
  including luck and marketing, and inflates G's apparent reliability. It also means a note feature could predict G
  only through the loop (an early cover starts it), or be swamped by it.
- **Fit with the repo:** the covers study found covers and views unrelated once release year is held (r = 0.00).
  That argues against a strong, general feedback from covers to present-day streaming, at least on that sample. The
  two can be reconciled: this paper finds effects in a minority of pairs (9-20%, before chance is subtracted),
  mostly short bursts in search interest; a few big revivals would barely move a cross-song correlation. So the
  feedback looks real but patchy, not the main driver of G.
- **Practical upshot:** keep the two parts of G apart and time-ordered. Use covers that came before the original's
  long-run measure (or early covers, within a few years of release) as the cleaner quality signal, and treat late
  covers as partly an effect of fame. Report results on each part separately as well as on the sum.

## One test Luthier could run
**Early-cover test (does the one note measure that held survive the feedback loop?).**
- Data: Discogs-VI (versions with Discogs release years) for the 2,360 songs already used in the covers study,
  cross-checked with SecondHandSongs dates where available; release year and Spotify 2021 popularity as in G.
- Split each song's covers into early (within 5 years of the original's release) and late (after 5 years).
- Measure: chord repetition within a section (the term that replicated, beta -0.07 on all covers), frozen as before.
- Predictions: (1) less repetition predicts more early covers, with a standardized beta at least -0.05 holding year
  and genre; (2) early covers predict later still-loved popularity beyond year, while late covers depend more on the
  original's prior popularity than early covers do (the feedback signature).
- Failure: the note term on early covers is near zero (|beta| < 0.03 or p > .10) while it holds on late covers. That
  would say the "chords that move" signal travels through fame, not through cover-worthiness at the start, and that
  the covers half of G is not a clean mark of the notes.
- Optional second leg: an event study on Wikipedia pageviews (2015 onward) for originals that got a charting cover,
  each matched to another song by the same artist with no new cover that month; a real feedback effect shows as a
  lift in the original versus its match that outlasts 12 months.

## Leads
1. Ortega, J. L. (2021). Cover versions as an impact indicator in popular music: A quantitative network analysis.
   *PLoS ONE* 16(4), e0250212. doi:10.1371/journal.pone.0250212. SecondHandSongs network of 855k covers; directly
   about whether cover counts measure impact, which is the covers half of G.
2. Schuster, M., Mitchell, D., & Brown, K. (2019). Sampling increases music sales: An empirical copyright study.
   *American Business Law Journal* 56(1), 177-229. doi:10.1111/ablj.12137. Sales-based evidence that borrowing lifts
   the original; the stronger source for the feedback claim.
3. Bryan, N. J., & Wang, G. (2011). Musical influence network analysis and rank of sample-based music. *Proc. ISMIR*,
   329-334. No DOI. WhoSampled network with centrality ranks: a ready "influence" score to compare against G.
4. Shalit, U., Weinshall, D., & Chechik, G. (2013). Modeling musical influence with topic models. *Proc. ICML*, PMLR
   28(2), 244-252. No DOI (proceedings.mlr.press/v28/shalit13). Audio-based influence and novelty over 24k songs;
   a route to test whether influential songs are the long-loved ones.
5. Hausman, C., & Rapson, D. S. (2018). Regression discontinuity in time: Considerations for empirical applications.
   *Annual Review of Resource Economics* 10, 533-552. doi:10.1146/annurev-resource-121517-033306. The pitfalls this
   paper skips (seasonality, autocorrelation, bandwidth); a checklist for any cover-event study we run.
