## Summary

arXiv adds tools and data, not corrections. Across the 13 topics no paper reverses a rule in Parts 18 to 30, so a full redo of every research round is not warranted.

- **One real miss:** Chordonomicon, 666,000+ songs' chords with sections, genres and dates. It was skipped earlier as unavailable; it is public, but its file host is blocked from this workspace. It could retest harmony, chromatic chords and keys at about 900 times McGill's size.

- **Two small additions:** a long-note band for word setting (songs 54 and 56 fall short of it), and a floor on predictability (elevator music).

- **Outcome signals:** Spotify's skip curves (skips cluster at the start and at transitions) and YouTube's replay curves, both measuring listeners moment by moment.

- **Tools:** Python versions of the standard melodic features and of IDyOM, to check the studies' own measures.

Most music-psychology and music-theory work, which the earlier parts rest on, is published outside arXiv, so its absence there is expected.

## 1. How the pass was done

Each of the 13 research topics behind Parts 18 to 30 was searched on arXiv, with PsyArXiv and the ISMIR archive where arXiv was thin, for papers mostly from 2022 to 2026. A paper counts only if it changes a rule in Parts 18 to 30, adds data the engine could use, or gives a better way to measure an outcome. Papers on audio generation, voice cloning or model training alone are noted once and skipped.

The workspace cannot query arXiv's own search, so the pass uses web search restricted to arXiv and reads the papers it returns. That means a paper with unusual wording can be missed; each topic got at least two different searches to reduce that.

## 2. Topic by topic

No arXiv paper reverses a rule in Parts 18 to 30. Most of what arXiv holds on these topics is generation methods; the useful part is data, tools and outcome measures.

|Topic (Part)|What arXiv adds|Changes a rule?|
|---|---|---|
|Harmony (18)|[Chordonomicon:](https://arxiv.org/abs/2410.22046)over 666,000 songs' chord progressions with section labels, genre, release date and Spotify IDs. [BeatlesFC](https://arxiv.org/html/2601.02099):harmonic-function labels for the Beatles (predominant 16.5%, dominant 13.2% of chords)|Not yet. Chordonomicon could retest Part 18 at about 900 times McGill's size (section 3)|
|The band (19)|Accompaniment and texture generators ( [AccoMontage,](https://arxiv.org/pdf/2108.11213v1) [METEOR,](https://arxiv.org/html/2409.11753) [whole-song hierarchical generation](https://arxiv.org/html/2405.09901v1)); no new corpus statistics|No|
|Tension (20)|A tension model on tonal interval vectors steered generation and passed a listening test ( 2511.19342); learned chord embeddings compared with human tension ratings ( 2609.36460)|No; a second tension reader to check Part 20's against|
|Metre above the bar (21)|Models that find 2-, 4-, 8- and 16-bar hypermeter in MIDI ( [2209.10259,](https://arxiv.org/pdf/2209.10259) [2210.17183](https://arxiv.org/pdf/2210.17183)); over half of POP909's phrases repeat at once( [2209.00182](https://arxiv.org/pdf/2209.00182))|No; confirms, and gives a check for our songs|
|Melody by genre (22)|Melodic diversity shaped by information and motor limits across cultures ( 2408.12635); melody and rhythm compared in 27,628 songs from 59 countries ( 2605.05982); a Python package of the standard melodic features ( [2608.19061)](https://arxiv.org/html/2608.19061)|No; the package could replace our own feature code|
|Setting words (23)|In human-written lyrics, syllable stress tracks metric strength, melodic peaks and note length; one version of the paper puts long notes on stressed syllables 73% of the time, another 82% ( [LOAF-M2L)](https://arxiv.org/html/2307.02146v1)|Adds a band (below)|
|Harmony voices (24)|Voice separation and an automatic four-part vocal harmonizer ( [2506.18143)](https://arxiv.org/pdf/2506.18143)|No|
|Song edges (25)|Spotify skips follow one shape: most skips come in the first seconds, with spikes at transitions such as a chorus starting or a voice entering, and a rise near the end that is not universal ( [Donier 2020)](https://arxiv.org/html/2005.06987)|No; supports Part 25's short intros and early voice|
|Ornament (26)|Singing-technique labels in 168 J-pop songs ( 2210.17367)and a nine-language technique corpus ( [GTSinger)](https://arxiv.org/html/2409.13832v8)|No|
|Key (27)|Little: keys skew major in high-valence clips ( 2407.20176)|No|
|Tempo and length (28)|Number-one songs have tripled their chart lifetime since the 1960s ( [2405.07574](https://arxiv.org/pdf/2405.07574v1)); Hot 100 songs' complexity sits closer to the mean than random songs' ( [1907.04292)](https://arxiv.org/pdf/1907.04292)|No|
|Solos (29)|Large guitar tablature sets ( [DadaGP,](https://ar5iv.labs.arxiv.org/html/2107.14653) [GOAT](https://arxiv.org/pdf/2509.22655))|No; DadaGP could give solo note statistics Part 29 lacked|
|The hook (30)|Covered in Part 30 (replay curves, memorability, hook labels)|Already in Part 30|
|Surprise (Part 8, for completeness)|A Python reimplementation of IDyOM ( GraphIDyOM); surprisal from a diffusion model shows the inverted U with liking ( [2310.03500)](https://arxiv.org/pdf/2310.03500)|No; a check on our own surprise model|

One PsyArXiv study is worth a line: elevator-music covers of popular songs were rated less pleasurable, surprising and arousing than the originals [(PsyArXiv xqs8b](https://osf.io/preprints/psyarxiv/xqs8b_v1)). Predictable wins (Parts 8 and 30), but there is a floor; Part 30's target of the 75th percentile for typical cells, not the 100th, keeps clear of it.

## 3. Datasets and outcome signals arXiv points to

The real miss is one dataset. Chordonomicon was set aside earlier because its local folder was empty; arXiv shows it is public, with section labels, genres and dates. Its file host is blocked from this workspace, so it needs another route.

|Resource|What it holds|Would retest|Reachable here?|
|---|---|---|---|
|Chordonomicon|666,000+ songs' chords (about 52 million chords), with verse, chorus, bridge and other parts, genre, release date and Spotify IDs; 1.3 GB, CC BY-NC|Part 18 (harmony by section), Part 14 (chromatic chords by genre), Part 27 (keys by genre and era), all at a scale McGill's 739 songs cannot reach|No: the Hugging Face file host refused the download (policy block)|
|SongFormDB|Song structure labels for over 14,000 songs|Part 25 (edges), Part 21 (section lengths)|Not tried|
|FaiSonic MMD|500 songs (250 English) with phrases, sections, chords and beats on the recordings|Part 21 (phrase lengths)|Not tried|
|DadaGP|Tokenised GuitarPro songs, solos included|Part 29 (solo melody)|Not tried|
|[J-pop singing techniques](https://arxiv.org/html/2210.17367v2)|168 songs with timed technique labels|Part 26 (ornament rates)|Not tried|
|YouTube "most replayed" (Rhapsody)|A 100-step replay curve per popular video|Parts 9 and 30 (moments and hooks)|No (YouTube pages)|
|Spotify skip curves (Donier 2020)|The shape of skipping through a song|Part 25|Published curves only|

The tools are smaller wins: a Python package of standard melodic features [(2608.19061](https://arxiv.org/html/2608.19061)) and a Python IDyOM ([2607.25787)](https://arxiv.org/html/2607.25787) would let the studies' homemade measures be checked against the field's standard ones.

## 4. What changes in Parts 18 to 30

Two small additions now, three retests later. Nothing already written needs correcting.

### Now

1. **Part 23, a long-note band.** Human lyrics put most long notes on stressed syllables (73% to 82% in the two versions of LOAF-M2L). Read the same way here (notes at least 1.5 times the song's median length): song 54 puts 65% of its long notes on stressed syllables, song 55 77%, song 56 68%. Two of three sit below the band. Check for v8: at least 75% of long notes on stressed syllables, reported per section. The paper's own definition of a long note may differ, so the band is approximate.

2. **Parts 8 and 30, a floor on predictability.** The elevator-music result supports keeping the typicality target at the 75th percentile rather than pushing it higher.

### Later, each needing data this workspace cannot fetch

|Retest|Data|What it would settle|
|---|---|---|
|Parts 18, 14 and 27 at scale|[Chordonomicon](https://arxiv.org/html/2410.22046)|Whether harmony by section, chromatic use and key choice hold by genre and decade across 666,000 songs|
|Part 29's solo melody|DadaGP|How solo lines move: range, speed, repetition, bends|
|Parts 9 and 30 on replays|YouTube's replay curves|Which moments and hooks listeners go back to, for thousands of songs|

### For the fix list (if added)

- **Long notes on stressed syllables:** Problem: songs 54 and 56 put a third of their long notes on unstressed syllables. Fix: a gate of at least 75% per section. Check: songs 52 to 56 rerun.

- **Chordonomicon retest:** a study, not a fix; logged so v8's harmony tables can be checked at scale once the data is reachable.

## 5. Sources

All papers are linked where they are used in sections 2 to 4. The main ones:

- [Chordonomicon (arXiv 2410.22046)](https://arxiv.org/abs/2410.22046) and its [Hugging Face page](https://huggingface.co/datasets/ailsntua/Chordonomicon)

- [Donier 2020, The universality of skipping behaviours on music streaming platforms (arXiv 2005.06987)](https://arxiv.org/html/2005.06987)

- [LOAF-M2L (arXiv 2307.02146)](https://arxiv.org/html/2307.02146v1)

- [Rhapsody (arXiv 2505.19429)](https://arxiv.org/abs/2505.19429v1)

- SongFormer and [SongFormDB](https://arxiv.org/abs/2510.02797) (arXiv 2510.02797)

- [FaiSonic MMD](https://arxiv.org/html/2611.13503) (arXiv 2611.13503)

- [DadaGP](https://ar5iv.labs.arxiv.org/html/2107.14653) (arXiv 2107.14653)

- [Computational features for symbolic melody analysis (arXiv 2608.19061);](https://arxiv.org/html/2608.19061) [GraphIDyOM (arXiv 2607.25787)](https://arxiv.org/html/2607.25787)

- [Elevator music as a tool for the quantitative characterization of reward (PsyArXiv)](https://osf.io/preprints/psyarxiv/xqs8b_v1)

- Songs 54 to 56's long notes: read from songs/p64 to p66 song_record.pkl
