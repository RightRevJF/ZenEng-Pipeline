# Checks on the judging research, nights one and two: result

22 November 2026. The document read: "Judging research: nights one and two" (week 01 and run 02 of `studies/judging_research` on the judging-research branch). Nothing here goes into the engine.

## 1. The sources

Eight papers carry the two nights. All eight exist, with the titles, authors, venues and identifiers the document gives. What I could confirm against the papers themselves:

| Paper | Checked against | Verdict |
|---|---|---|
| Janssen, Burgoyne & Honing 2017 (folk phrases) | full text (University of Amsterdam copy) | Every figure matches: 9,639 phrases, 147 families, 170,803 judgments; coefficients −0.30, −0.24, −0.10, +0.10, +0.09, +0.08, +0.05; R² 0.05 and 0.22; family SD 0.84; matcher misses 30%, adds 8%; no held-out test. |
| Madison & Schiölde 2017 (repeated listening) | full text (PMC) | Every figure matches: 15 listeners, 40 excerpts, 8 raters, hearings 1, 10, 19, 28; F(3,42) = 12.35, ω² 0.197; complexity F 0.81; interaction F 1.33; piece F 7.51; betas 0.551, 0.464, 0.226, R² 0.572; "dull" r −0.64, "odd" +0.41; no control group; vocals excluded. |
| dos Santos & Figueiredo 2024 (borrowings) | full text (arXiv HTML) | Matches, including the faults the card names: 884 pairs; 82 (9.3%) by regression discontinuity; 117 (64%) Granger with an unclear base; "182 cases (20%)" in the introduction; no split by type; no correction for many tests. |
| Salganik, Dodds & Watts 2006 (MusicLab) | article (author copy) | Matches: 14,341 participants, 48 songs, eight worlds, quality = share in the independent world. The per-experiment counts and the 2009 figures (16%, 38%) I did not re-read. |
| Di Marco et al. 2026 (note networks) | publisher's press release and Science News | Published details match: Scientific Reports 16, 11121, 23 April 2026; 21,480 pieces, six genres, 1600 to 2021. The preprint's popularity correlations (under 0.07 in pop and rock) I could not re-read. |
| McBride & Leroi 2026 (Irish tunes) | arXiv listing and a third-party review of the paper | Matches where checked: 11,791 tunes fitted, ΔAIC −57,700, conformity exponent 0.024 to 0.048, fitness −0.84 to 1.60, R² 0.29 in the text against 0.24 in the figure legend (the card flags this; so does the review), simpler tunes spread better. **Not confirmed by me: the split the night's argument leans on, 16 points for prestige against 3 for melody.** arXiv refused my fetches. |
| Ortega 2021 (who gets covered) | abstract and citation records | Matches at the level of the abstract: 106,000 artists, 855,000 covers, skewed counts, decline since the 1950s, genre first, Beatles, Ellington, Crosby. **Not confirmed by me: 22% of artists ever covered, top 100 take 41%, 73% of jazz covers stay in jazz.** The full text was behind a browser check. The card itself says its numbers came through a page-reading tool and were not copied by hand. |
| Cheung et al. 2019 (uncertainty and surprise) | citation and abstract records | Citation, 745 songs and about 80,000 chords match, and so does the finding. The participant counts (39 and 40) and Table 1's coefficients agree with what I know of the paper; I did not re-read them. |

I found no invented paper and no figure that contradicts its source. Three sets of figures remain unconfirmed by me, marked above. The forty or so "leads" were not checked.

**The repo claims** were checked against main and all hold: the covers study's −0.124, −0.071 and −0.003; covers and views unrelated with year held; `study_covers_discogs.py` sets `original=1.0` on every row (R02-3 is right); `discogs_cliques.py` reads each version's release id and year and keeps only counts and the earliest year (R02-2 is right); `ch_rep` is the share of chord 3-grams heard earlier in the clip.

## 2. The chair's own figures reproduce (A, prediction 1)

The chair's script for the spectral gap g was a scratch file. Built again from its written rules alone (`gap.py`, `gap.json`):

| | The chair | Here |
|---|---|---|
| g against within-section repetition | −0.26 (721 songs) | −0.263 (721 songs) |
| g against distinct chords | +0.02 | +0.031 |
| g against branching (E) | +0.47 | +0.461 |
| Median g; middle half | 0.19; 0.09 to 0.30 | 0.188; 0.092 to 0.302 |
| Songs with g under 0.01 | 8.7% | 9.4% |
| Songs kept | 721 | 734 with g; 721 with g and repetition |

By my rule the count of songs kept is 13 off, not within 10; every other figure is inside the bands I wrote. The 721 is exactly the songs that have both measures, so the difference is which songs are dropped for having no section of 4 chords. The chair's figures are real.

## 3. g is steadier within a song than I expected (A, prediction 2)

| First half of the song against the second | Spearman | Songs |
|---|---|---|
| g | **0.58** | 729 |
| Distinct chords | 0.80 | 734 |
| Repetition (chord 3-grams heard earlier) | 0.77 | 731 |

I predicted 0.15 to 0.45 for g and was wrong: it is 0.58, over the 0.5 I set as "stable enough to test". It is less steady than the plain measures, and less steady the more chords a song has (0.70 with 2 to 5 distinct chords, 0.58 with 6 to 9, 0.39 with 10 or more). One caution on all three figures: a song's verse and chorus come round in both halves, so part of the agreement is the same section played twice. The chair's check that it did not run is now run: g may go near an outcome, as a secondary term, as the chair proposed.

## 4. Luthier's sections do not loop more than kept sections as a body (B)

Within-section chord repetition, first verse, first chorus and bridge (`loops.py`, `loops.json`). Kept sections (McGill): verse 0.00, 0.00, 0.33, 0.50, 0.71 at the 10th, 25th, middle, 75th, 90th (755 sections); chorus 0.00, 0.00, 0.33, 0.50, 0.70 (696); bridge 0.00, 0.00, 0.14, 0.38, 0.58 (254).

| | Song 55 | Song 54 | Song 58 | Song 60 | Song 59 (read only) |
|---|---|---|---|---|---|
| Verse | 0.10 | 0.10 | **0.86** | **0.73** | 0.25 |
| Chorus | **0.75** | 0.50 | 0.14 | 0.40 | 0.36 |
| Bridge | none | none | 0.45 | 0.00 | 0.33 |

Bold: over the kept 90th. I predicted that at least three of the four verses would stand at or over the kept middle: two do, so that prediction failed. I predicted at least one over the kept 75th: two stand over the kept 90th. Luthier's sections spread from 0 to 0.86, about as widely as kept sections do. With four songs nothing can be said about a lean.

**What follows for J1.** The premise (Luthier's builds loop at the kept rate on average) is not contradicted. But the reading shows single sections at both ends, and song 58's verse is a plain loop (I V, four times, twice over). Whether looping less is better is not known from this; it rests on the between-artist result that night two rightly says must first be tested within artists (R02-1).

## 5. What I think of the two nights' ideas

- **R02-1 (the within-artist test) is the right next test, and I agree it should come before any change to the structure draw.** It needs Discogs-VI and the Hooktheory notes, which are not on this machine and which this machine's network cannot fetch.
- **Night two's review of night one is sound.** Retiring J2 to J5 is right: each is a lead from a setting unlike ours, and each added reading is another chance of a lucky pass.
- **Early covers only** should not be adopted as the target on the argument given; night two's objection (budget cover albums) is as plausible as night one's case. Report both periods.
- **The 16-to-3 split** (prestige against melody) is being used as a ceiling on what notes can explain. Until someone reads the paper's figure and supplement it should be quoted as "about", and it is a ceiling for melody in instrumental dance tunes, with no harmony measured, so it does not bound the one finding that has held (harmony).
- **Breadth across genres** changes the yardstick and is Jason's to decide.

## 6. What this could not do

Confirm the three sets of figures marked above. Check the leads. Run R02-1, or any test against covers: no outcome data is on this machine. The split-half reading of g cannot separate real steadiness from sections that repeat in both halves; a reading on sections that occur once would.
