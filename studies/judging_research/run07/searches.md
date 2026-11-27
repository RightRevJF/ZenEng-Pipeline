# Run 07: searches

26 November 2026, the 18:17 ET pass.

- **Consensus:** skipped. Run 06 (this morning) was told the free allowance for the billing period is used up, and no later run notes a renewal.
- **Elicit:** skipped (api_access_denied in earlier runs).
- **Jason's inbox** ("Judging research inbox", Drive folder 1g3VCdZ216otpRPKGPUc2sDb1anIvVWi6): empty. No inbox papers this pass.

## arXiv (WebSearch restricted to arxiv.org)

| Query | Hits | Kept |
|---|---|---|
| Gromov hyperbolicity finite metric space computing four-point condition algorithm | 10 | 2412.05746 (Gilbert & Yim, average hyperbolicity; math.MG, HTML) read as card 1. Also seen: 1210.3323 (Fournier, Ismail & Vigneron, computing hyperbolicity; PDF only), 2505.21073, 2607.24096, 2610.16932 (queued). |
| self-similarity matrix music structure persistent homology sliding window periodicity theorem | 10 | 1307.6188 (Perea & Harer, sliding windows and persistence; FoCM 2015; ar5iv HTML) read as card 2. Also seen: 1602.00739 (topological fingerprint of music), 1507.05143 (Tralie, cover song shape sequences), 2303.13881. |

**Why these two.** Both papers are mathematics (the focus asks for at least one), and both are chosen for what the pass's data can now do. This pass found a corpus of **whole songs** with names: the Lakh Pianoroll Dataset's 21,425 cleansed songs (Zenodo 5646574), named through the Gold-Caps metadata (Zenodo 10178563), which repeats the Million Song Dataset's artist and title for every track. Run 03 learned that Hooktheory clips are too short for form-level geometry. Whole songs are not, so the two form-level constructions on the reading list come first. Card 1 gives a tree-likeness invariant (average four-point hyperbolicity) for how a song's bars nest, which is Jason's non-Euclidean idea made computable. Card 2 gives a proved periodicity score (sliding-window persistence) for how loop-like a whole song's harmony is. Both are math.MG / math.AT in substance.

**Counter-evidence for the Skeptic:** not this pass. The rule asks for it at least every third run; the next is due by run 08.

## Data searches (Zenodo API, from the cloud machine)

The way through that run 06's first principles named was a larger corpus with chords and names. Chordonomicon is blocked (Hugging Face storage host; no names). Zenodo queries:

| Query | What came back | Used |
|---|---|---|
| lakh midi | Lakh Pianoroll Dataset (5646574: LPD-5 cleansed 555 MB, metadata.zip with the cleansed MSD ids); Gold-Caps LMD-matched (10178563: 31,034 MSD tracks with artist, title, year, hotttnesss) | yes, both |
| million song dataset metadata | Hit Song Prediction (3258042: `msd_bb_matches.csv`, 5,832 MSD tracks on the Billboard Hot 100 with peak and weeks; `msd_bb_non_matches.csv`) | yes, as a fame control |
| clean_midi; lmd_matched; msd unique tracks | nothing usable | no |

`millionsongdataset.com` is not reachable from here. All 21,425 LPD cleansed ids have a name in Gold-Caps; 15,893 are by artists with two or more songs in the set.
