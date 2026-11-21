# Judging research, week 01

21 November 2026. Four papers read in full, a three-way debate, and a chair's ranking. Study only: nothing went into the Luthier engine.

## The week's best idea

Covers can feed a song's fame, and fame draws more covers, so a cover count partly measures fame. The cleanest test is to count only the covers a song gets in its first five years, before that loop has time to run. If "chords that move" (the one note finding that has already held up twice) still predicts those early covers, it is a mark of the song itself and not of its fame.

## Three ways forward, ranked

**1. Early covers (builds on the covers study).** Count only covers made within five years of release. Prediction, written before any test: songs whose chords repeat less within a section get more early covers, by a standardised effect of 0.05 or more. The test uses Discogs-VI release years on the 2,360 Hooktheory songs from the covers study, cross-checked with SecondHandSongs dates. It fails if the effect on early covers is weaker than 0.03 (or not significant) while it still holds on later covers. That would mean the signal travels through fame. One weakness: these are the same songs the finding came from, so this asks when the effect appears, not whether it is real. To decide: re-fetch the data (it is not kept in the repo), and accept early covers as the cleaner target for the covers half of the yardstick.

**2. Plain words, varied sentences: fresh songs (partly new).** Musicians may cover songs whose single chord moves are common but whose path does not loop, like plain words put into varied sentences. Where a song does surprise, the surprise may only pay off when the voices reach it by small steps (the Geometer's "parsimonious surprise"). Prediction: on songs never used before, less chord repetition goes with more covers; the benefit is larger when the chord vocabulary is plain; and the most surprising chord changes are reached by smaller voice movements in more-covered songs. Each needs an effect of 0.05 or more in the stated direction. The test uses the McGill Billboard corpus (about 740 songs with chord charts) joined to Discogs-VI and SHS100K, dropping any song already studied, with every measure frozen before the join. Each part fails if its confidence interval crosses zero or its sign flips. To decide: about 700 songs gives only about a 30% chance of detecting an effect that small, so either run it now as a lead or wait for the larger LargeSHS release.

**3. Measure the ceiling (new).** If chance and social history decide much of who wins, no note measure can explain much, and some earlier failures would be due to that limit. The MusicLab experiment ran eight parallel worlds with the same 48 songs, so the limit can be measured rather than guessed. Prediction: in its stronger social condition, a song's appeal without social cues explains less than half of its market share in any one world. It fails if it explains half or more; then luck is small and the "ceiling" excuse for weak note results is withdrawn. To decide: fetch the public data and ask the authors about terms. The number caps early download success, not decades of love, so it is a guide, not a hard bound.

**The chair's one check.** Before running it, the chair predicted that the love half and the covers half of the yardstick respond differently to the notes in past results. They did not: across 61 earlier measures, the two halves moved together (rank correlation 0.44). The chair notes the check was weak, since both come from the same songs. So the reason to split covers by time rests on time order, not on the halves disagreeing.

## The four papers

**Cheung and colleagues (2019) [1].** Thirty-nine listeners rated how pleasant chords felt in 30 chord progressions taken from pop songs, stripped of melody and words. Pleasure depended on two things together: how uncertain the listener was before a chord, and how surprising it was. Over most of the range, surprise lowered pleasure; surprise helped only after a very predictable stretch, and that region is small. A brain scan study of 40 new listeners found the same pattern in reward and memory areas. This is first-hearing pleasure on strangers' music, so it says little directly about lasting love or covers. The repo's earlier chord-surprise term differs from Cheung's in five ways, so its failure on Discogs-VI is not a strike against this paper. The supplement could not be reached this week.

**Janssen, Burgoyne and Honing (2017) [2].** In Dutch folk songs passed on by ear, which phrases survive re-singing? Across 9,639 phrases in 147 tune families, phrases survived better when short, early in the song, low in surprise and built from small steps. The notes explained only about 5% of survival on their own, and nothing was tested on held-out songs. Faithful copying favours plain material, which is not the same as musicians choosing to perform a song. The supplement could not be reached this week.

**Salganik, Dodds and Watts (2006) [3].** The week's skeptic paper. 14,341 people downloaded 48 unknown songs in parallel "worlds". When people could see what others had chosen, success became more unequal and less predictable. The best songs rarely did badly and the worst rarely did well, but anything could happen in the middle. Quality here is a listener measure, not a measure of the notes. It suggests that even a perfect note judge would only reliably sort the very top from the very bottom.

**dos Santos and Figueiredo (2024) [4].** A short workshop paper on arXiv. Using WhoSampled and Google search interest, it asks whether a cover, sample or remix lifts interest in the original song. Sometimes it seems to, mostly for samples. But the study had no controls, tested 884 pairs one by one without correcting for chance, and its counts do not add up. It hints that covers feed back into lasting love, which is why idea 1 splits covers by time.

## The debate in brief

**Where they agreed.** All three moved to early covers and to the extreme ends (the most and least covered songs) as the target, because of the luck in [3] and the feedback loop in [4]. All three agreed that the Geometer's flexible "shape templates" risk the same fate as an earlier reader that passed once and then failed on fresh songs, so those templates were dropped. Reading S = 1 + g/π as an angle on a chart was also shelved until a plainer measure passes.

**Where they split.** The Geometer held that geometry still adds something: an unexpected chord reached by tiny voice movements differs from one reached clumsily, and a count of chords cannot see that. The Skeptic thinks voice-leading distance may just be "chords that move" under another name, and wants it to count only if it adds to that finding. The Listener argued that lasting love also needs songs that resist wearing out on repeat, measurable from public listening logs (ListenBrainz); the Skeptic estimated that notes alone may explain at most about a tenth of the yardstick, and the Listener asked that the limit be measured, not guessed (idea 3).

## Papers you could get for the inbox

Nothing new went behind a paywall this week; all four papers were read in full. The earlier list still stands. If you can get any of these, drop the PDF in the Drive folder "Judging research inbox" (created this week in your My Drive) and the next run will read it first:

- Jacoby and McDermott (2017), Integer ratio priors on musical rhythm revealed cross-culturally by iterated reproduction, Current Biology. doi:10.1016/j.cub.2016.12.031
- McDermott, Schultz, Undurraga and Godoy (2016), Indifference to dissonance in native Amazonians reveals cultural variation in music perception, Nature. doi:10.1038/nature18635
- Tymoczko (2006), The geometry of musical chords, Science. doi:10.1126/science.1126287
- Voss and Clarke (1975), 1/f noise in music and speech, Nature. doi:10.1038/258317a0
- Salimpoor and colleagues (2013), Interactions between the nucleus accumbens and auditory cortices predict music reward value, Science. doi:10.1126/science.1231059
- Plomp and Levelt (1965), Tonal consonance and critical bandwidth, JASA. doi:10.1121/1.1909741

## Next week's leads

- Ortega (2021), cover versions as a measure of impact, from 855,000 SecondHandSongs covers [5]. Tests the covers yardstick itself.
- van de Rijt (2019), self-correcting dynamics in social influence [6]. The strongest answer to [3]: given time, better options may regain the lead.
- Müllensiefen and Halpern (2014), features that make new melodies memorable [7]. The counter-claim to [2].
- Whyatt and colleagues (2026), computational features for symbolic melody analysis, arXiv 2608.19061 [8]. Ready-made note measures.
- Gold and colleagues (2019), musical reward prediction errors and learning [9]. Ties expectation to the motivation to learn a song.
- Also queued: Askin and Mauskapf (2017) on optimal differentiation; Hamilton and colleagues (2024) on 70 years of chart melodies; Salganik and Watts (2008, 2009); Krumme and colleagues (2012); the McGill Billboard corpus paper (Burgoyne, Wild and Fujinaga 2011); Van Balen and colleagues (2015) on hooks.

## References

1. Cheung, V. K. M., Harrison, P. M. C., Meyer, L., Pearce, M. T., Haynes, J.-D., & Koelsch, S. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. Current Biology 29(23), 4084-4092. https://doi.org/10.1016/j.cub.2019.09.067
2. Janssen, B., Burgoyne, J. A., & Honing, H. (2017). Predicting variation of folk songs: a corpus analysis study on the memorability of melodies. Frontiers in Psychology 8, 621. https://doi.org/10.3389/fpsyg.2017.00621
3. Salganik, M. J., Dodds, P. S., & Watts, D. J. (2006). Experimental study of inequality and unpredictability in an artificial cultural market. Science 311(5762), 854-856. https://doi.org/10.1126/science.1121066
4. dos Santos, G. S. S., & Figueiredo, F. (2024). Assessing the impact of sampling, remixes, and covers on original song popularity. LAMIR 2024. https://arxiv.org/abs/2411.01242
5. Ortega, J. L. (2021). Cover versions as an impact indicator in popular music: a quantitative network analysis. PLoS ONE. https://doi.org/10.1371/journal.pone.0250212
6. van de Rijt, A. (2019). Self-correcting dynamics in social influence processes. American Journal of Sociology. https://doi.org/10.1086/702899
7. Müllensiefen, D., & Halpern, A. R. (2014). The role of features and context in recognition of novel melodies. Music Perception 31(5). https://doi.org/10.1525/mp.2014.31.5.418
8. Whyatt, D., and colleagues (2026). Computational features for symbolic melody analysis. arXiv. https://arxiv.org/abs/2608.19061
9. Gold, B. P., Mas-Herrero, E., Zeighami, Y., Benovoy, M., Dagher, A., & Zatorre, R. J. (2019). Musical reward prediction errors engage the nucleus accumbens and motivate learning. PNAS. https://doi.org/10.1073/pnas.1809855116

Working files in this folder: searches.md, card_1.md to card_4.md, debate.md, chair.md. Published as the Doc "Judging research, week 01": https://claude.ai/artifact/51hN6BSgCaeXsryR8ujTtY
