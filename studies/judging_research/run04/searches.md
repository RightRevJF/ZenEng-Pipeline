# Run 04 searches (24 November 2026)

The Drive folder "Judging research inbox" was checked first: it is empty, so there are no inbox papers this run.

origin/main was read without checking it out. Its head is still 1b46833, the same commit run 03 read. No new RESULT.md or PREDICTION.md has appeared under studies/judging_checks, studies/fresh_songs or studies/judging_data since run 03, and the latest fix list is still `songs/p68/fixlist_v46.md`.

## Why these searches
Run 03's first principles (section 6) said geometry should move out of chord maps built from the song and into a fixed space where every song is a path, so that a short song gives a noisier reading of the same shape. Its two candidates were the Fourier phases of each chord (the circle of fifths and the circle of thirds) and Tymoczko's voice-leading space. Run 03's late fifths-path test leaned the right way but was unsettled at power 0.06. Tonight's searches therefore looked for the founding construction of the Fourier phase torus, which can be computed exactly on every chord.

The second need came from the data. Run 03 counted 10,429 Hooktheory songs that have chord measures but were never matched to Discogs-VI. Whether a song is in Discogs-VI at all has never been used as an outcome, and it could give the fresh evidence run 03 lacked. To use it honestly we must know exactly how Discogs-VI decides which songs are in it. So the second paper is the dataset paper itself, a methods need rather than a counter-argument.

**Note for the Skeptic rule.** Tonight carries no counter-evidence paper. Run 05 must therefore include material that cuts against Jason's stance.

## Consensus (free plan, page 0 only, no filters)
| # | Query | page_size | Results |
|---|---|---|---|
| 1 | Fourier phase space of pitch-class sets and voice-leading geometry: torus of phases, chord distance | 30 | 29 |

Notable results:
- Amiot 2013, The Torii of Phases (result 3, picked)
- Yust 2015, Schubert and Fourier phase space (result 4)
- Yust 2020, Generalized Tonnetze and Zeitnetze (result 2)
- Tymoczko & Yust 2019, Fourier phase and pitch-class sum (result 7)
- Hoffman 2008, pc-set cartography (result 8)
- Tymoczko 2008, set-class similarity, voice leading and the Fourier transform (result 21)
- Callender 2007, continuous harmonic spaces (result 23)
- Bernardes et al. 2016, tonal interval space (result 24)
- Harasim et al. 2016, voice-leading duality (result 25)
- Genuys 2019, pseudo-distances between chords of different sizes (result 15)

## Consensus research agent
Not used tonight. An ordinary search was enough to find the construction, and the pitfalls (undefined phases, the wrap at ±π) are stated in the paper itself. This saves Jason's allowance.

## Elicit
Skipped: earlier runs recorded api_access_denied.

## arXiv (WebSearch restricted to arxiv.org; pages read through WebFetch)
| Query | Notable hits |
|---|---|
| discrete Fourier transform pitch-class sets phase space voice leading torus | 1208.4774 (Amiot, the paper); 2008.11529 (TIV.lib); 1306.2859 (chords to Fourier analysis, a survey) |
| voice-leading orbifold geometry chords minimal voice leading metric theorem | 2207.11035 (Himpel); 1307.1201 (topology of musical data, math.AT); 1602.04137 (graph approach to voice leading); 1508.05833 (Bergomi et al., a model of voice leading and its complexity) |
| Discogs-VI musical version identification dataset (Araz, Serra, Bogdanov) | 2410.17400 (the paper); 2608.04543 and 2501.01333 (version identification in the wild) |

## Other data searched
Hugging Face lists `m-a-p/HookTheory`, which holds the full Hooktheory.json.gz with the notes of every song. It is gated: a login and acceptance are needed. It was not downloaded, and no way around the gate was tried. Without it, the notes (and so any geometry) exist only for the 3,080 matched songs. The 10,429 unmatched songs have only the per-clip measures in `hooktheory_surprise.json.gz` and `hooktheory_rhythm.json.gz`.

## Picked this run
1. **Amiot (2013), The Torii of Phases**, arXiv 1208.4774 (math.HO; MCM 2013, LNCS 7937). This is the mathematics paper. It gives a fixed space (the torus of the phases of the third and fifth Fourier coefficients) where every chord is a point and every song is a path. Card 1.
2. **Araz, Serra & Bogdanov (2024), Discogs-VI**, arXiv 2410.17400 (ISMIR 2024). The methods paper behind the outcome. It shows how cliques are formed (exact title, plus shared writer credit) and that a song with only one version is never in a clique. Card 2.
