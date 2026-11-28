# Run 10: searches

27 November 2026, the 18:17 ET pass.

- **Consensus:** skipped. Run 06 (26 November) was told the free allowance for the billing period is used up, and no later run (07, 08, 09) notes a renewal.
- **Elicit:** skipped (api_access_denied in earlier runs).
- **Jason's inbox** ("Judging research inbox", Drive folder 1g3VCdZ216otpRPKGPUc2sDb1anIvVWi6): empty. No inbox papers this pass.

## Why these searches

Run 09's obstacle: every song with chords and names on this machine was spent, and the one lead (the ii-V share) lives only in jazz, where chart writers, players and the cover count are one community. Before searching papers, this pass looked for a corpus nobody in the project had joined to an outcome. It found one: the TheSession.org data dump on GitHub (adactio/TheSession-data, csv/, fetched 18:19 ET): 55,838 ABC transcriptions ("settings") of 23,199 Irish and related traditional tunes, with two outcomes of its own: the number of members who put each tune in their tunebook (musicians choosing to learn it; a love reading) and recordings by artist (covers by other artists). Run 02 read McBride & Leroi's paper on the same site (card 2 of run 02) but no experiment had used it. The data are melody only, with several transcriptions per tune by different people, which gives a stability test for free.

So the searches aimed at (1) a mathematics paper with a construction computable on single-line melodies (topology of a melody's transition graph), and (2) the counter-evidence due by run 10 or 11 (run 08 carried the last one), preferably on TheSession itself.

## arXiv (WebSearch restricted to arxiv.org)

| Query | Hits | Kept |
|---|---|---|
| arxiv persistent homology melody intervallic transition graph musical style | 10 | **2204.11139** (Mijangos, Bravetti & Padilla 2022, Musical Stylistic Analysis: intervallic transition graphs via persistent homology; HTML; math.AT cross-list; reading list tier 3 item 13) read as card 1. Also seen: 1602.00739 (topological fingerprint of music), 1307.1201 (Topology of Musical Data, math.AT), 2405.04796, 2611.00799 |
| arxiv folk tune transmission content bias weak popularity Irish traditional tunes social factors | 10 | **2607.12673** (McBride & Fitch, Contrasting statistical patterns in melodic and molecular evolution; uses TheSession directly) read as card 2. Also seen: 2609.09501 (McBride & Leroi, already in the ledger), 1906.11928 and 1810.11900 (Youngblood, conformity bias in sampling; fallback), 2301.02884 |

**Why these two.**
- **Card 1 (mathematics, the focus).** Persistent homology of a melody's transition graph is a fixed, setting-light topological summary that can be computed on every tune of the new corpus. The reader found no theorems in it (it applies Vietoris-Rips persistence and persistent entropy) and a corpus of 18 quartet movements, so its value is the construction, not the evidence.
- **Card 2 (counter-evidence, due).** McBride & Fitch align 51,680 pairs of TheSession versions and find that what survives transmission is what is typical: common pitches, strong beats, small steps. Tune identity is conserved by conformity as much as by anything in the notes. It cuts against "greatness is in the notes" and also hands this pass a "core of the tune" construction.

**Copies read.** Card 1: arXiv HTML v1, whole paper (6 sections, 19 references). Card 2: arXiv HTML v1, body, supplement sections 1 to 8, bibliography (figures as images not seen).

## Data searches and downloads (from the cloud machine)

| Source | What | Used |
|---|---|---|
| raw.githubusercontent.com/adactio/TheSession-data/main/csv/ | tunes.csv (18.3 MB), tune_popularity.csv (0.33 MB), recordings.csv (15.6 MB), aliases.csv | tunes.csv parsed notes side (`experiments/abcparse.py`); the two outcome files joined only after the predictions commit |

All raw downloads are in /home/claude/dl/thesession, outside the repo. The orchestrator printed the outcome files' row counts and the tunebook distribution (min 10, median 28) to size the design before any measure existed; no measure was ever compared with an outcome before the predictions commit.
