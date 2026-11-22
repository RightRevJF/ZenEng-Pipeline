# Judging research, run 02

22 November 2026. The first nightly run. Four papers read in full, a three-way debate, a chair's ranking and a first-principles review. Study only: nothing went into the Luthier engine.

## The run's best idea

A cover keeps a song's notes and changes everything else: the singer, the band, the sound. So far the project has only done the opposite comparison by accident, setting one artist's songs against another artist's, where fame, voice, era and genre all change along with the chords. The best idea this run is to hold the performer still and let the notes change: compare each artist's songs only with that same artist's other songs, and ask whether the ones whose chords move rather than loop still get more covers.

## Three ways forward, ranked by the chair

**1. Early covers, with fame and chart run held (builds on week 01's first idea and the covers study).** Test the one note finding that has held twice (chords that move within a section get more covers) on covers made in a song's first five years, while also holding how famous the original performer is (their covers on other songs) and how long and high the song charted. Prediction, written before any test: an effect of −0.05 or stronger, the same sign in both halves of the artists, then the same sign on fresh McGill Billboard songs. It fails if the effect is weaker than −0.03, the halves disagree, it shows only on later covers, or it vanishes once fame is held. Power is honest but modest: about a two-in-three chance of seeing a true effect of that size on 2,360 songs, and only 20 to 35% on the fresh songs. To decide: re-fetch Discogs-VI and the Hooktheory notes (neither is kept in the repo) and find a Hot 100 weekly archive.

**2. Covers across genres as the outcome (builds on week 01's first-principles note; this run adds the evidence).** Count how many different genres a song has been covered in, beyond its own. Card 1 shows that musicians mostly cover inside their own genre (73% of jazz artists' covers are jazz), so a cover that crosses a genre goes against the main pull and is a more selective vote for the song itself. Prediction: chords that move predict breadth at −0.05 or stronger, and more strongly than they predict the raw count. It fails if weaker than −0.03, if the halves split, or if breadth is no better than the count. First step, costing no test: the first-principles check found that the repo's Discogs script reads each version's release id but throws it away, and no committed file has genres. The free Discogs data dump can supply genres by release id. To decide: whether breadth may count toward the covers half of the yardstick. That changes the yardstick, so it is Jason's call.

**3. The spectral gap of the chord map, as a side term only (new this run).** Turn a song's chords into a map of moves from one chord to the next, and measure how quickly a walk on that map forgets where it started. A pure four-chord loop or a two-chord vamp scores zero; harmony with several roads out of a chord scores higher. This is the first geometric measure the project has found that a simple repeat count cannot see, and it is the nearest thing yet to Jason's non-Euclidean idea, though only by analogy. Prediction: +0.05 or more on early covers, at a stricter bar (p under .025) because it rides alongside idea 1. It fails if weaker than +0.03 or the halves split.

**The chair's one check.** Before letting the gap near any outcome, the chair asked whether it was just "chords that move" under a new name. On 721 McGill Billboard songs, with every outcome removed first, it is not: the two share only about 7% of their variation (rank correlation −0.26), and the gap does not follow how many chords or sections a song has. Three of four written predictions held; the fourth (that at least 10% of songs would score near zero) narrowly failed at 8.7%. Being different is not the same as meaning something: two thirds of the gap's variation is unexplained, and whether it is stable within a song is untested.

## First principles: the obstacle and the way through

**The obstacle.** No note finding that has held has ever been tested with the performer held fixed. Both replications of "chords that move" compare different artists' songs, so the performer's fame, voice, era and genre all travel with the harmony. The one earlier same-artist study (21 tune and chord measures against the yardstick) found nothing, but it never included chord repetition or covers alone.

**The way through.** Treat a cover as a natural experiment: notes held, performer changed. Then run its mirror: performer held, notes changed. Compare each artist's songs only with their own other songs (a fixed effect for each artist), with year and views held. Prediction, written first: chord repetition still predicts fewer covers at −0.04 or stronger, the same sign in both halves of the artists. If it falls weaker than −0.02, the finding belongs to performers, eras or genres, not to the notes. It has never been run. If it survives, move to covers across genres. If it dies (speculation), the next place to look is songs by the same writers that never charted, since every song tested so far was already a hit.

**What the review would delete or simplify.** It recommends retiring four of last week's proposals (J2 to J5): one already failed its test, two were never tested and only add chances of a lucky pass, and one rests on folk memory rather than musicians choosing songs. It would drop melodic entropy as a sixth try at the tune, after five runs on about 3,100 songs found nothing there. It disagrees with the chair on two points. Chart weeks and peak should not be held in the main model, because the notes may partly cause a long chart run. And "early covers only" may be backwards: the first covers of a hit are often quick budget cover albums, the most fame-driven covers of all, so both early and late covers should be reported. It found that the Discogs script's "first performer" control is set to 1 for every song, so it does nothing. The spectral gap is parked, not deleted. The simplest version left: one measure, one outcome, one control for the artist, plus year and views.

## The four papers

**Ortega (2021) [1].** A network of 106,000 artists joined by 855,000 covers from SecondHandSongs. Covering is very unequal: only 22% of artists have ever been covered, and the top 100 take 41% of all covers. Artists mostly cover inside their own genre, most strongly in jazz. Covers per artist peaked in the 1950s. It looks only at artists, not songs or notes, and runs no tests, so it is a warning: a raw cover count partly measures the original performer's fame and genre. That warning is why ideas 1 and 2 hold fame and count genres.

**McBride and Leroi (2026) [2].** The arXiv paper. On TheSession.org, players of Irish traditional music add tunes to their personal tunebooks, a close stand-in for musicians choosing what to learn. Across 820,752 adds of 22,216 tunes over 13 years, tunes have real, lasting differences in how readily they are taken up, and copying the crowd matters little. But in a test on held-out tunes, the prestige of a tune's recordings explained about 16 points of the differences and its melody only about 3. Simpler tunes, with fewer distinct pitches and fewer notes, spread a little better. No harmony was measured, the supplement was not available, and nothing has been replicated. It is the cleanest "musicians choose" data yet, and it says the notes are a small part of the choice.

**Madison and Schiölde (2017) [3].** The Skeptic's paper. Fifteen adults heard 40 unfamiliar instrumental excerpts daily for about four weeks. Liking rose with hearing at every level of complexity, with no turn-down and no difference between simple and complex music. Complexity was rated by trained musicians from recordings, not read from the notes. The simpler pieces were rated much more "dull" even as liking rose, which may be an early sign of wearing out that the study stopped too soon to see. Small, with no control group and no replication, but it supports the view that the love half of the yardstick partly records how often people heard a song.

**Di Marco and colleagues (2026) [4].** About 21,000 MIDI files across six genres, each turned into a network of note-to-note moves. Classical and jazz networks branch more and rock back and forth less than pop, rock or electronic, and genres have drifted toward simpler networks over time. The networks come from the notes, but from all instruments blended, from fan-made files. The only outcome, in the preprint, was current Spotify popularity, and in pop and rock the link was tiny (correlations under 0.07). The method, not the result, is what this run took: it gave the Geometer the chord map behind idea 3.

## The debate in brief

**Where they agreed.** By round 2 all three backed one frozen model built on early covers, with the original performer's fame held (card 1). All three accepted that card 3 weakens the love half for a notes-only judge, and that card 2's 3% sets an honest ceiling on how much the notes can explain even when only musicians choose. The Listener dropped the test of love against chart exposure, because a long chart run is partly caused by love, not handed out at random.

**Where they split.** The Geometer argues the chord map's gap sees something a repeat count cannot: whether a loop has any way out. The Skeptic will count it only if it adds to repetition with the song's form held, which the chair's check partly answered. The Listener kept one tune measure (how many distinct pitches the melody uses) as a test of memory; the Skeptic and the Geometer doubt the tune after five failures, and the first-principles review would drop it.

## Papers you could get for the inbox

Nothing new went behind a paywall this run; all four papers were read in full, though some supplements could not be reached. The earlier list still stands. If you can get any of these, drop the PDF in the Drive folder "Judging research inbox" and the next run will read it first:

- Jacoby and McDermott (2017), Integer ratio priors on musical rhythm revealed cross-culturally by iterated reproduction, Current Biology. doi:10.1016/j.cub.2016.12.031
- McDermott, Schultz, Undurraga and Godoy (2016), Indifference to dissonance in native Amazonians reveals cultural variation in music perception, Nature. doi:10.1038/nature18635
- Tymoczko (2006), The geometry of musical chords, Science. doi:10.1126/science.1126287
- Voss and Clarke (1975), 1/f noise in music and speech, Nature. doi:10.1038/258317a0
- Salimpoor and colleagues (2013), Interactions between the nucleus accumbens and auditory cortices predict music reward value, Science. doi:10.1126/science.1231059
- Plomp and Levelt (1965), Tonal consonance and critical bandwidth, JASA. doi:10.1121/1.1909741

## Leads for the next run

- Street, Eerola and Kendal (2022), population size and folk tune complexity [5]. Same TheSession data; reports an inverted U that card 2 contradicts.
- Anglada-Tort, Harrison, Lee and Jacoby (2023), large-scale iterated singing [6]. Which melodic shapes survive being passed on, with prestige removed by design.
- Leroi and colleagues (2020), neutral syndrome [7]. How to tell real selection from drift in popularity data: a guard for the yardstick.
- Youngblood (2019), conformity bias in music sampling traditions [8]. Do musicians reuse what is popular rather than what is good?
- Rosselló and colleagues (2025), network representations reveal structured uncertainty in music, arXiv 2509.14053 [9]. From a network-geometry group: a route to the non-Euclidean idea.
- Also queued: Orr and Ohlsson (2005) on whether musicians want more complexity than lay listeners; North and Hargreaves (1995), who did find an inverted U with real pop songs; Pessa and colleagues (2026) on the life of Billboard hits; Mas-Herrero and colleagues (2025) on predictive processes and individual preferences; Hamilton and Pearce (2024) on 70 years of chart melody.

## The proposed fix list

The proposed list for the maintainer from this run is the Doc "Proposed fix list: judging research, run 02": https://claude.ai/artifact/VR74RsLgCXDEzjPTZ13gDi (the same as proposed_fixlist.md in this folder).

## References

1. Ortega, J. L. (2021). Cover versions as an impact indicator in popular music: a quantitative network analysis. PLoS ONE 16(4), e0250212. https://doi.org/10.1371/journal.pone.0250212
2. McBride, J. M., & Leroi, A. M. (2026). Population ecology of tunes. arXiv:2609.09501. https://arxiv.org/abs/2609.09501
3. Madison, G., & Schiölde, G. (2017). Repeated listening increases the liking for music regardless of its complexity: implications for the appreciation and aesthetics of music. Frontiers in Neuroscience 11, 147. https://doi.org/10.3389/fnins.2017.00147
4. Di Marco, N., Loru, E., Galeazzi, A., Cinelli, M., & Quattrociocchi, W. (2026). Decoding the evolution of melodic and harmonic structure of Western music through the lens of network science. Scientific Reports 16, 11121. https://doi.org/10.1038/s41598-026-42872-7 (preprint arXiv:2501.07557)
5. Street, S. E., Eerola, T., & Kendal, J. R. (2022). The role of population size in folk tune complexity. Humanities and Social Sciences Communications. https://doi.org/10.1057/s41599-022-01139-y
6. Anglada-Tort, M., Harrison, P. M. C., Lee, H., & Jacoby, N. (2023). Large-scale iterated singing experiments reveal oral transmission mechanisms underlying music evolution. Current Biology. https://doi.org/10.1016/j.cub.2023.02.070
7. Leroi, A. M., Lambert, B., Rosindell, J., Zhang, X., & Kokkoris, G. D. (2020). Neutral syndrome. Nature Human Behaviour. https://doi.org/10.1038/s41562-020-0844-7
8. Youngblood, M. (2019). Conformity bias in the cultural transmission of music sampling traditions. Royal Society Open Science. https://doi.org/10.1098/rsos.191149
9. Rosselló, L. B., Jankowski, R., Bersini, H., Boguñá, M., & Serrano, M. A. (2025). Network representations reveal structured uncertainty in music. arXiv:2509.14053. https://arxiv.org/abs/2509.14053

Working files in this folder: searches.md, card_1.md to card_4.md, debate.md, chair.md, first_principles.md, proposed_fixlist.md. Published as the Doc "Judging research, run 02": https://claude.ai/artifact/GfyEnWfC6eiyGHe6gFsGng
