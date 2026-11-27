# Run 09: searches

27 November 2026, the 10:17 ET pass.

- **Consensus:** skipped. Run 06 (26 November) was told the free allowance for the billing period is used up, and no later run (07, 08) notes a renewal.
- **Elicit:** skipped (api_access_denied in earlier runs).
- **Jason's inbox** ("Judging research inbox", Drive folder 1g3VCdZ216otpRPKGPUc2sDb1anIvVWi6): empty. No inbox papers this pass.

## arXiv (WebSearch restricted to arxiv.org)

| Query | Hits | Kept |
|---|---|---|
| path signature Lévy area time series theorem primer signature method | 10 | 1603.03788 (Chevyrev & Kormilitzin, A Primer on the Signature Method in Machine Learning; HTML v2) read as card 1. Also seen: 2006.00873 (generalised signature method; queued by the reader), 2005.12359, 2402.09532, 2505.05332. |
| discrete Fourier transform pitch class sets phase space voice leading theorem | 10 | none new (1208.4774, Amiot's torii of phases, already read in run 04). Seen: 2008.11529 (TIV.lib), 2512.04090, 1306.2859, 1602.04137 (graph-theoretic voice leading; queued). |
| jazz standards repertoire recordings network cultural evolution chord progressions corpus | 10 | 2610.15356 (Lee & Jeong, JSIR, jazz standard recordings with lead sheets) read as card 2. Also seen: 2208.00792 (jazz contrafact detection, PDF only; queued), 2307.09670 (JAZZVAR), 2609.34931 (JazzSAMBA), 2302.08632 (jazznet). |

**Why these two.**
- **Card 1 (mathematics, the focus; reading list tier 2, item 6).** Path signatures had not been read. The signature is a fixed, setting-free summary of a path (a chord sequence placed in a fixed space such as the circle of fifths or the Fourier phase plane), invariant to time-warping, and its second level is a signed area (the Lévy area). Run 06's chirality was a hand-made Lévy area; this paper gives the theory behind it, the lead-lag transform (quadratic variation as an area), and the uniqueness theorem up to tree-like back-and-forth, which suggests measures that a chart writer's inserted ii chords cannot move. arXiv lists it under stat.ML; the content is iterated-integral mathematics (Chen, shuffle product, rough paths).
- **Card 2 (another discipline, chosen for the obstacle).** Run 08's obstacle is that iReal Pro charts are written by the jazz players whose recordings make the outcome. JSIR gives, for 44 standards, a canonical lead sheet and what 4 to 9 recordings actually played, so it asks on the notes side alone whether performers add ii-V moves. Its quick check (card 2) found no excess (recordings 0.151 to 0.155 against lead sheets 0.155), with built-in reasons that bias towards no difference. The data were cloned from GitHub (MALerLab/JSIR at 1dd6b8b, CC BY-SA 4.0) to /home/claude/dl/jsir, outside the repo.
- **Counter-evidence:** due by run 10 or 11 at the latest (run 08 carried Evans & Giometto).

**Copies read.** Card 1: arXiv HTML v2 (17 January 2025), all sections and the bibliography. Card 2: arXiv HTML and PDF v1 (11 October 2026).

## Data searches and downloads (from the cloud machine)

| Source | What | Used |
|---|---|---|
| Zenodo 7706751 | ChoCo v1.0.0 (467 MB), re-downloaded (the machine was fresh) | run 08's parse re-run unchanged (42,002 charts, 41,206 with 8+ chords, as in run 08); NEW: the Band-in-a-Box internet corpus, the Real Book, Isophonics, uspop2002, rock corpus, Robbie Williams, JAAH and Weimar partitions (`experiments/parse09.py`) |
| Zenodo 13983028 | Discogs-VI 20240701 main.zip, reduced by the maintainer's `cliques_versions.py` unchanged (348,796 cliques, as before) | the outcome, after the predictions commit |
| GitHub MALerLab/JSIR | JSIR annotations (git clone; the GitHub API is not enabled for this repository in this session, raw and clone work) | card 2, notes side only |
