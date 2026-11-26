# Run 06 searches (26 November 2026)

The Drive folder "Judging research inbox" (id 1g3VCdZ216otpRPKGPUc2sDb1anIvVWi6) was checked first: it is empty, so there are no inbox papers this run.

origin/main was read without checking it out (head 073efd6; main was force-updated since run 05's edbb6e0, and the diff from edbb6e0 was read). New since run 05: Luthier v48 to v50 (fix 964, the shared octave bin), `songs/p68/fixlist_v51.md` (the latest list, with addenda to 749.199), `lib/luthier/REVIEW_stage35.md`, `studies/the_peak_line/`, `studies/v48_trials/`, `studies/the_draw/`, and a hold-out ledger in `studies/judging_data/README.md` (749.169, now done). Nothing new under `studies/judging_checks` or `studies/fresh_songs`; the data pack's files are unchanged (only the README grew).

## Why these searches

Run 05's first principles said the useful mathematics may be dynamics rather than shape: not what figure the chords draw, but how they flow. Its arrow-of-time measure (detailed balance) was the first step; the next is the net flow of chord moves and how it splits into a downhill part (a ranking of chords from tension to rest) and a circulating part (loops), with entropy production as the graded measure of irreversibility. So tonight's search aimed at the Hodge (Helmholtz) decomposition of edge flows on graphs and the cycle decomposition of non-equilibrium Markov chains, preferring recent arXiv papers with HTML full text (run 05 learned that PDF-only papers do not come through the fetch tool in an unattended run).

No counter-evidence paper is due tonight (run 05 carried one; the next is due by run 08).

## Consensus

| # | Query | page_size | Result |
|---|---|---|---|
| 1 | entropy production Markov chain cycle affinities irreversibility estimation from finite trajectories | 30 | **Refused: "You've used all of this billing period's included usage."** |
| 2 | combinatorial Hodge decomposition edge flows graph gradient curl harmonic components ranking | 30 | Rate limit (sent at the same time); not retried, since the allowance is used up |

**Note for later nights: Consensus says the free allowance for this billing period is used up (26 November 2026).** Following the standing rule, later nights stop using Consensus (both search and the research agent) and scout on arXiv alone, unless Jason says the allowance has been renewed. The research agent was therefore not used.

Elicit: skipped (earlier runs found api_access_denied).

## arXiv (WebSearch restricted to arxiv.org)

| Query | Notable results |
|---|---|
| arxiv Hodge decomposition Markov chain edge flow entropy production cycle | 2409.07479v3 (Decomposing force fields as flows on graphs reconstructed from stochastic trajectories, HTML); 2303.05930 (Minimal entropy production under thermodynamic constraints: cycle decomposition for Markov chain design, HTML); 1206.2189 (Flow decomposition reveals dynamical structure of Markov process); 2610.05832 (Priority coordination games: Hodge decomposition); 2205.07214 (Entropy production for discrete-time Markov processes, PDF) |
| arxiv entropy production estimation finite data Markov chain plug-in bias irreversibility | 2009.11351 (Estimating entropy rate from censored symbolic time series: a test for time-irreversibility); 2305.04657 (Effective estimation of entropy production with lacking data); 2602.15663 (Entropy production reveals hidden dynamical constraints); 2107.02795 (matching-time irreversibility tests) |
| arxiv math.PR cycle decomposition Markov chain circulation net flow Hodge Laplacian graph theorem 2025 | **2412.09434 (Helmholtz-Hodge Decomposition on Graphs, HTML; picked)**; **2603.03634 (An approach to non-equilibrium Markov chains through cycle matrices, math.PR; picked)**; **2506.12546v1 (Circular Directional Flow Decomposition of Networks, HTML; fallback)**; 1105.2178 (cycle decompositions of non-equilibrium steady states); 2503.11222 (Betti number estimates for non-negatively curved graphs, math.CO) |

## What was read, and what could not be

- **Card 1, read in full:** March, P. (December 2024), "Helmholtz-Hodge Decomposition on Graphs", arXiv 2412.09434, from https://arxiv.org/html/2412.09434 (five passes). The abs page and the v2 HTML were blocked by unanswered permission prompts in this unattended run, so the category and version are not confirmed (probably math.CO). The reader checked the paper's dimension claims numerically and found that they fail beyond single-cycle graphs (card 1, section 4); the orthogonal three-way split itself holds.
- **2603.03634 (Cruz-de-la-Rosa & Guerrero-Poblete, math.PR, 4 March 2026): not read.** It has no HTML; the PDF, tried once, returned only the abstract. It is free on arXiv, not paywalled; logged in `paywalled.md` so Jason can drop the PDF in the inbox if he wishes.
- **Card 2, read in full instead:** Homs-Dones, MacKay, Sansom & Zhou (2025), "Circular Directional Flow Decomposition of Networks", arXiv 2506.12546v1, from https://arxiv.org/html/2506.12546v1 (seven passes; sections 1 to 7, appendices A to G, references). Its category could not be confirmed (the abs page was blocked).

Both are mathematics papers on the decomposition of flows on graphs, chosen because tonight's experiments test the gradient-versus-cycle split of a song's chord flow.
