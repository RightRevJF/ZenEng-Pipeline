# Run 05 searches (25 November 2026)

The Drive folder "Judging research inbox" (id 1g3VCdZ216otpRPKGPUc2sDb1anIvVWi6) was checked first: it is empty, so there are no inbox papers this run.

origin/main was read without checking it out (head edbb6e0). New since run 04: `studies/plain_and_pink/` (PREDICTION.md, RESULT.md: melody surprise and pitch DFA do not trade among kept songs, rho −0.05), `studies/loop_less_reading/reading_v47.*`, `lib/luthier/proposed_v47*.py`, and the latest fix list is still `songs/p68/fixlist_v46.md` (updated). Nothing new under `studies/judging_checks`, `studies/fresh_songs` or `studies/judging_data`. The latest review is `lib/luthier/REVIEW_stage30.md`.

## A data unlock, found before the searches

Run 04's data request R04-1 asked for the notes of every Hooktheory song (Sheet Sage's `Hooktheory.json.gz`). Tonight it was found to be downloadable from `raw.githubusercontent.com/chrisdonahue/sheetsage-data/main/hooktheory/Hooktheory.json.gz` (20,075,896 bytes; sha256 917b7cd5…e0c). It is the file `studies/judging_data/make.py` reads. It holds 26,175 clips; every one of the 16,563 clips behind run 04's 9,588 within-artist rows is in it. It is CC BY-NC-SA 3.0 (Hooktheory via Sheet Sage), kept outside the repo, never committed. Hugging Face holds only gated copies (`m-a-p/HookTheory`, `hidude562/hooktheory-music-midi`), which were not touched. So, for the first time, any measure computed from the notes can be tested on all 9,588 songs against "in Discogs-VI at all" and "taken up by another artist".

## Why these searches

Run 04's first principles said geometry on run 03's songs is spent and that fresh songs are needed; the notes above supply them. Run 04 also found that chords which loop go with more chance of being taken up and fewer coverers once taken up. So tonight's mathematics should be a construction that measures looping as *shape* rather than as counted repeats: does a song's sequence close into a circle (periodic), a torus (two cycles), or neither? That is the sliding-window / persistent-homology programme on Jason's "music as shapes" line, tier 1 item 5 of `math_reading_list.md`.

The second paper had to be counter-evidence (the rule: at least every third run; run 04 carried none, so run 05 at the latest). The search aimed at work that separates the content of songs from the artist's prior success.

## Consensus (free plan, page 0 only, no filters)

| # | Query | page_size | Results |
|---|---|---|---|
| 1 | sliding window embedding persistent homology periodicity quasiperiodicity time series theorem | 30 | 30 |
| 2 | song features fail to predict hit popularity; success determined by social influence or artist rather than musical content | 30 | 29 (first attempt hit a rate limit; retried after 32 s) |

Notable results, search 1: Perea & Harer 2015 (result 1, picked first); Perea 2016, toroidal sliding windows (3); Gakhar & Perea 2023, quasiperiodic sliding windows (5); Suarez Salas et al. 2026, three-gap theorem (2); Park et al. 2025, Topological Periodicity Test (10); Tralie & Perea 2018, (quasi)periodicity in video (21); Tralie 2017 thesis (15); Krishnamoorthy 2025, bi-conditional periodicity score (6).

Notable results, search 2: Askin & Mauskapf 2017, optimal differentiation (1); Interiano et al. 2018, success with and without a superstar flag (2, picked); Reisz et al. 2024, homophily and influencer networks (3); Oliveira et al. 2024, viral vs hit (4); Salganik et al. 2006 (11, already in the ledger); Adamska et al. 2025, Eurovision: intrinsic features explain a minimal share (15).

**Consensus research agent:** not used tonight. The construction (sliding windows and persistence) is well defined by the papers themselves, and an ordinary search was enough; Jason's allowance is saved.

## arXiv (WebSearch restricted to arxiv.org; WebFetch on arxiv.org/abs and /html)

| Query | Notable |
|---|---|
| sliding window persistence periodicity music melody topological data analysis | 1307.6188v2 (Perea & Harer), 2103.04540 (Gakhar & Perea), Tralie ISMIR 2017 rhythm, 1905.12118 |
| hit song prediction musical features little predictive power beyond artist popularity | 2403.12079 (Beyond Beats), 2211.15164 (homophily and influencer networks), 1812.00551, 2505.07280; Interiano et al. (PMC5990848) |

## What was read, and what could not be

- **Perea & Harer (2015), arXiv 1307.6188, Foundations of Computational Mathematics 15:799–838, doi:10.1007/s10208-014-9206-z.** First choice. arXiv lists only a PDF for it, and in this unattended run the PDF body did not come through the fetch tool (the abs page loaded; the PDF requests were blocked or returned only the abstract). The reader's first card, written from memory, was discarded unread. It is not paywalled: it is free on arXiv. Logged in `paywalled.md` as unreadable tonight, so that Jason can drop the PDF in the inbox if he wishes.
- **Gakhar & Perea (2023), arXiv 2103.04540.** Second choice; also PDF-only, and the HTML requests were blocked. Not read.
- **Card 1, read in full:** Park, An, Kim & Kim (2025, v4 2026), "Topological Periodicity Test (TopPT) via Confidence Bound of Time-Delay Embeddings", arXiv 2512.06324 (math.ST), from https://arxiv.org/html/2512.06324v4.
- **Card 2, read in full:** Interiano, Kazemi, Wang, Yang, Yu & Komarova (2018), "Musical trends and predictability of success in contemporary songs in and out of the top charts", Royal Society Open Science 5:171274, doi:10.1098/rsos.171274. PMC and the publisher page were blocked by unanswered permission prompts in this unattended run; the reader used the University of California eScholarship copy (escholarship.org, qt96b901t6). This is the counter-evidence paper.

**Note for the Skeptic rule:** run 05 carries counter-evidence (card 2). The next run that must carry some is run 08 at the latest.
