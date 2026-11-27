# Run 08: searches

27 November 2026, the 02:17 ET pass.

- **Consensus:** skipped. Run 06 (26 November) was told the free allowance for the billing period is used up, and no later run (07) notes a renewal.
- **Elicit:** skipped (api_access_denied in earlier runs).
- **Jason's inbox** ("Judging research inbox", Drive folder 1g3VCdZ216otpRPKGPUc2sDb1anIvVWi6): empty. No inbox papers this pass.

## arXiv (WebSearch restricted to arxiv.org)

| Query | Hits | Kept |
|---|---|---|
| neutral model popularity charts turnover random copying theorem | 10 | 1105.4044 (Evans & Giometto, turnover of popularity charts in neutral models) read as card 2. Also seen: Bentley et al. 2007 (Evolution and Human Behavior; skimmed by the reader for context), 1703.10698 (neutral evolution of English word popularity), 0808.1655 (queued). |
| Wasserstein distance on the circle closed form transportation distances circular histograms | 10 | 0906.5499 (Rabin, Delon & Gousseau, transportation distances on the circle) read as card 1. Also seen: 2310.06002 (linear circular optimal transport, LCOT; queued), 2206.08780 (spherical sliced Wasserstein; queued). |

**Why these two.**
- **Card 1 (mathematics, the focus).** Run 03 learned to prefer geometry in a fixed space. A chord is a distribution of mass on the circle of twelve pitch classes, and this paper proves the exact, setting-free formula for the cheapest way to move one such distribution into another on a circle (a median of differences of running totals). It is the optimal-transport entry on the reading list's areas and had not been tried. For equal-weight triads it equals Tymoczko's smallest voice leading divided by three (checked by the reader), so it is a voice-leading distance that also works for chords of different sizes and for whole sections.
- **Card 2 (counter-evidence, due by run 08).** The rule asks for material cutting against Jason's stance at least every third run; runs 06 and 07 had none. Evans and Giometto show that content-free random copying (every song equally good) already produces heavy-tailed popularity and steady chart turnover. It is also mathematics (Wright-Fisher and Moran models), and it gives a test on the outcome itself: whether early covers alone predict late covers as a pure rich-get-richer urn would.

**Copies read.** Both ar5iv pages were refused in this unattended run (a permission prompt no one could answer). Card 1 was read from the arXiv PDF (v3, 2 June 2010); card 2 from the arXiv abstract page's full text (all sections, appendix, references). Both are noted on the cards.

## Data searches (Zenodo API, from the cloud machine)

Run 07's first principles named the way through as "chords rather than arrangements: a large chord corpus with artist and title".

| Query | What came back | Used |
|---|---|---|
| choco chord corpus | ChoCo: the Chord Corpus v1.0.0 (Zenodo 7706751, `smashub/choco-v1.0.0.zip`, 467 MB, JAMS); the ChoCo paper (Zenodo 11221563, CC BY 4.0) | yes: the iReal Pro (forum and playlists) and Wikifonia partitions |

The zip and both Discogs-VI and Hooktheory downloads were stored in /home/claude/dl, outside the repo. ChoCo's other partitions (Billboard = the McGill hold-out's source, Isophonics, RWC, Real Book, Band-in-a-Box, When in Rome, Weimar, JAAH, Nottingham, Schubert, Mozart, rock corpus, Chordify, uspop2002) were not used: Billboard must not be touched, and the rest are small, classical, without composers, or duplicates of the iReal charts.
