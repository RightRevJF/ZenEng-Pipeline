# Agent 7: data scout (round 2, 25 November 2026)

Angle: find data that lets a rule-first test check line-level and structure traits (rhyme, line length, the turn, chorus reuse, text setting) against a lasting-value outcome, within writer where possible. No lyric text was stored in the repo; downloads sit in /home/claude/lyr_dl/scout/, scripts in /home/claude/scout_scripts/ (outside the repo).

## 1. Summary

The line-level test is feasible now, at scale, within writer. The key find is that the WASABI song corpus on Zenodo (CC BY-NC 4.0, record 5603369) holds full lyrics with line and stanza breaks inside its song.json. I pulled only that member (1.57 GB compressed, by byte range) and wrote a metadata table with no text: 2,079,510 songs, of which 1,197,486 are English with at least 8 lines (median 30 lines, 6 stanzas). In that set, 716 of the 780 Rolling Stone 500 songs (any edition) and 280 of 371 Grammy Song of the Year nominees can be found, and 540 artists have at least one acclaimed song plus at least 4 others (81,165 songs, 937 acclaimed). Choruses are mostly written out (section labels in 9.6% of songs, repeat shorthand in 7.5%; among acclaimed songs only 2.3% and 1.4%), so chorus reuse can be counted from repeated lines. For the musicians' outcome I reduced Discogs-VI to a writer table (348,796 version cliques with writer credits, number of versions, distinct recording artists, first year, genre). Matched to WASABI where the performer is a credited writer, it gives 982 artists with 10 or more self-written songs that have a cover count (37,407 songs). For text setting (words against beats), the only usable local sets are small: OpenEWLD standards (464 lead sheets with syllables on notes, 476 matched to cover counts, 21 lyricists or composers with 5+ works) and CoCoPops (214 Billboard songs with syllables on notes, hand-marked rhymes and phrase breaks, plus 80 Rolling Stone songs with syllable stress). Hymns would be an ideal within-writer, centuries-long outcome (Hymnary counts per text), but I found no reachable bulk source for the texts.

## 2. Findings table (data, not claims about lyrics)

| Claim | Evidence | Strength | Outcome type | Travels? | What it means for our process |
|---|---|---|---|---|---|
| WASABI song.json carries line-broken lyrics for about 1.2M English songs, plus artist, title, year, Deezer rank, a Wikipedia-page flag, MusicBrainz id | Buffa et al. 2021, ESWC; Zenodo 5603369; my pass: songs_meta.csv | STRONG (as data) | none built in; matched to critics, awards, covers | many genres, mostly pop/rock | The main test bed for rhyme, line length, stanza form, chorus reuse and the turn |
| RS500 and Grammy SOTY can be matched inside WASABI within artist | my matching: 716/780 RS, 280/371 SOTY; 540 artists, 937 acclaimed songs | STRONG (n) | critics/canon; peer award | rock/soul heavy (RS), pop/MOR (SOTY) | Two different acclaim panels; a trait that passes both is less likely to be one magazine's taste |
| Discogs-VI gives a writer-credited cover count for 348,796 songs | Araz et al. 2024 (Discogs-VI); my reduction cliques.csv | STRONG (n); matching is title + writer name | covers (musicians' choice to re-record) | all genres incl. jazz, country, folk, Latin | Lasting value judged by other musicians, within writer; Dylan, for one, has 566 credited cliques (median 4 covering artists, max 305) |
| Wide spread of cover counts inside each writer's catalogue | e.g. Irving Berlin 471 cliques (median 4, max 1,179), Carole King 180 (median 3, max 730), Joni Mitchell 96 (median 4, max 281) | STRONG | covers | yes | A within-writer outcome with real variance |
| OpenEWLD lead sheets have syllables on notes; 476 of 509 English works match a cover count (median 104 covering artists, 90th pct 360) | local OpenEWLD.db + MusicXML; my match | SUGGESTIVE (n under 500, all already standards) | covers | standards only | The only within-writer text-setting set we have (Hart 42 works, Gershwin 34, Kern 27, Kahn 21); lines must be inferred from phrases |
| CoCoPops Billboard: 214 songs with hand-marked rhyme pairs, phrase breaks, form labels and syllables on notes; 32 on an RS list | Condit-Schultz & Arthur, CoCoPops (local) | STRONG as gold labels, small as a test | charts sample; RS for 32 | 1958-1991 pop | Use to validate an automatic rhyme detector before running it on WASABI |
| BiMMuDa: 367 full sung transcriptions with stanza breaks and repeats (median 47 lines), 1,153 section-labelled melodies, but no word-to-note alignment | local; 62 RS matches, about 70 SOTY title matches, 17 artists with both kinds | SUGGESTIVE | critics, award | 1950-2022 top 5 | Cross-check WASABI's transcriptions against sung ones; too few for within-writer |
| Hymnary.org lists every text by an author with its number of printings | Watts: 1,289 English texts, median 18 hymnals, 90th pct 141, max 2,110 (person page fetched once) | STRONG outcome; texts not reachable | lasting congregational use (centuries) | hymns only | Best possible within-writer outcome for Jason's hymn work, blocked by texts: Hymnary text pages refuse the shell after one request; Gutenberg and CCEL are not reachable |
| Not usable: Genius 5M on HF (9 GB, CDN refused), Song Interpretation Dataset (lyrics but no artist or title; Music4All metadata on request), DALI (Zenodo access restricted), WASABI line-similarity matrices (mega.nz only), jazzstandards.com (WebFetch only, titles only) | checked by API/listing | n/a | n/a | n/a | Do not plan on these |

Round-1 caution found on the way: /home/claude/lyr_dl/covers.csv matched by title key only, so same-title songs share counts (for example two different songs titled "One" both carry 37). The new writer table allows writer-checked matching.

## 3. Testable next: ranked test designs

**Design A (rank 1): WASABI within artist, critics and awards.** Data: WASABI English songs with lyrics, artists with 1 or more acclaimed songs (RS500 or SOTY) and 5 or more songs; n = 540 artists, 81,165 songs, 937 acclaimed. Outcome: acclaimed or not, conditional logit by artist; controls year, length, Deezer rank, Hot 100 peak where matched. Within writer: yes (restrict to self-written via Discogs-VI credits as a sensitivity run). Traits: end-rhyme rate and scheme regularity (CMU dict, `pronouncing` installed), slant versus perfect rhyme, mean and spread of line length (syllables), stanza count and size regularity, chorus share (repeated-line share), title placement (first or last line of the repeated block), the turn (shift in pronoun, tense or image family between first and final stanza; a late unrepeated stanza as a bridge). Effort: medium, about a day (metadata pass done; one feature pass of about 4 minutes per run). Prediction: within writer, acclaimed songs have a lower exact-repeat share and more slant rhyme; the turn measure is the most open bet.

**Design B (rank 2): WASABI within writer, covers.** Data: WASABI matched to Discogs-VI where the performer is a credited writer; 982 artists with 10 or more matched songs, 37,407 songs. Outcome: distinct covering artists (negative binomial or rank within writer, artist fixed effects, controls year and popularity). Within writer: yes. Traits: same as A. Effort: medium (the join needs care with titles; clique selection means every song has at least 2 versions). Prediction: covered songs are more singable: more regular line length, clearer chorus, rhyme at line ends. If A and B disagree, that is the critics-versus-musicians split again.

**Design C (rank 3): rhyme detector validation on CoCoPops.** Data: 212 songs with hand-marked rhymes. Outcome: none; agreement of the automatic detector with the gold labels (precision and recall at line ends). Effort: low (half a day, Humdrum spines parse easily). Required before A and B report any rhyme result.

**Design D (rank 4): text setting in standards, within lyricist.** Data: OpenEWLD 464 note-aligned lead sheets, 476 with cover counts; 21 authors with 5+ works (273 works). Outcome: covering artists, within author. Traits: stressed syllables on strong beats (CMU stress against MusicXML metre via music21), rhyme on the phrase-final note, syllables per note (melisma), title on the downbeat of the A section. Effort: medium to high (2 days; lines inferred from rests and phrase lengths; the author table mixes composers and lyricists). Prediction: within author, more covered songs have fewer stressed syllables on weak beats.

**Design E (rank 5): across-writer checks on BiMMuDa and CoCoPops Rolling Stone.** Data: BiMMuDa 367 songs (62 RS); CoCoPops RS 80 with stress. Outcome: RS membership (across writer only). Use: a sanity check that WASABI's text gives the same feature values as sung transcriptions for the songs in both. Effort: low.

**Held in reserve: hymns within author.** Outcome ready from Hymnary person pages (instance counts); needs a public-domain text source the shell can reach, or texts Jason supplies. If found, this is the closest match to his hymn writing and spans 300 years of use.

## 4. Sources

- WASABI dataset, Zenodo 5603369: https://zenodo.org/records/5603369 ; https://github.com/micbuffa/WasabiDataset ; Buffa et al. 2021, ESWC, https://hal.science/hal-03282619
- Discogs-VI (local copy; Araz et al. 2024, ISMIR)
- CoCoPops (local; Condit-Schultz & Arthur), McGill Billboard (Burgoyne et al. 2011), RS200 (de Clercq & Temperley 2011)
- OpenEWLD (local; Wikifonia lead sheets)
- BiMMuDa (local)
- iRealPro corpus of jazz standards, Zenodo 3546040: https://zenodo.org/records/3546040
- Grammy Song of the Year nominees: https://en.wikipedia.org/wiki/Grammy_Award_for_Song_of_the_Year (via WebFetch summary; spot-check before use)
- Songwriters Hall of Fame list (461 through 2019): https://en.wikipedia.org/wiki/List_of_Songwriters_Hall_of_Fame_inductees
- Hymnary.org person pages: https://hymnary.org/person/Watts_Isaac
- Jazz standards ranking (1,000 titles, basis not stated): https://www.jazzstandards.com/compositions/index.htm
- Song Interpretation Dataset, Zenodo 7429711; DALI, Zenodo 3576083 (restricted); Genius lyrics on HF: sebastiandizon/genius-song-lyrics

Files written (no lyric text): /home/claude/lyr_dl/scout/wasabi/songs_meta.csv, song_flags.csv, acclaim_ids.txt, song_json.deflate (raw source, 1.57 GB); /home/claude/lyr_dl/scout/dvi_writers/cliques.csv; /home/claude/lyr_dl/scout/grammy/soty.psv; /home/claude/lyr_dl/scout/ireal/ireal_titles.tsv; /home/claude/lyr_dl/scout/hymnary/w2.html.
