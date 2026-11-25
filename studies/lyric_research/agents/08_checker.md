# Agent 8: checker (round 2, 25 November 2026)

Method: each load-bearing claim checked against the paper, its abstract or a primary summary with WebFetch/WebSearch (no Consensus). Local numbers recomputed in the shell from feat.csv and our drafts via score_ours.py's pick and clean and measures.features. Hold-outs p69, p60 and p73 were not read. No lyric text stored.

## 1. Summary
Most of the load-bearing literature holds up, and agent 1's correction of reading.md is right: Kao & Jurafsky found **less** perfect rhyme and alliteration in professional poems. Corrections that matter: Johnson, Huron & Collister is **2014**, and its paired numbers are not a disagreement. Boyd 2020 measured **ratings**, not popularity. Rhyme-as-reason is weaker than agent 1 says (the slogan study found nothing). The high-pitch vowel claim is operatic and contested. Kolchinsky's genre exception is R&B/Soul. Wassiliwizky's address effect is small once position is controlled. Our I+you rate is **7.8**, not 7.2, so 22% of acclaimed hits sit at or below us. Round-1 covers matched title plus a loose performer check. The Grammy file lacks two nominees. Mori 2022 and the 2026 identifiable-victim meta-analysis are unverified.

## 2. Claim-by-claim verdicts

| Claim (agent) | Verdict | What the source says |
|---|---|---|
| Wassiliwizky et al. 2017, SCAN: chills at line, stanza and poem ends; social address adds chills beyond position (1, 3, 4) | **VERIFIED, with strength note** | n=27 physiology, 17 fMRI, 30 behavioural; 1,593 chill periods. End effects all p<.001 (poem end largest: b=1.28 experimenter poems, 2.26 self-chosen). Social address with position controlled: b=0.05 (p<.05) in experimenter poems, 0.39 (p<.001) in self-chosen ones. The authors offer rhyme and metre at closure as an explanation but did not test it. One lab, one language: SUGGESTIVE. |
| Kao & Jurafsky 2012: professional poems had less perfect end rhyme (OR 0.12) and less alliteration (OR 0.53) (1) vs reading.md "richer sound devices" | **Agent 1 VERIFIED; reading.md CORRECTED** | Perfect rhyme OR 0.12, p=5e-7; alliteration OR 0.53, p=.019; slant rhyme, assonance and consonance not significant. Concrete objects OR 3.72; abstract words 0.28; negative emotion 0.46. 100 vs 100 poems. |
| Menninghaus et al., parallelism +0.52, deviation −0.38 on liking; comprehensibility +0.31 / −0.31 (1 says 2023, 3 says 2024) | **VERIFIED; same paper** | Phil Trans R Soc B 379(1895), 20220424; online 18 Dec 2023, issue Jan 2024. 96 texts × 4 versions, n=282. The rating was beauty/liking. Deviation was not varied independently of rhyme and metre (authors' own caveat). Cite as 2023 (online) or 2024 (issue), but give one year. |
| Johnson, Huron & Collister: 85% vs 75% aligned; archaic 41% vs 81% sung (55% vs 94% spoken, φ=.35); melisma 77% vs 84%; rhyme 65% vs 74%; diphthong errors 16% vs 25% (1, 2, 5, 6, reading.md) | **VERIFIED numbers; year CORRECTED to 2014** | EMR 9(1), 2014; n=27 listeners. Each pair is one comparison (aligned vs not, etc.), not a disagreement. Caveat: stimuli sung by operatic and music-theatre singers. Each effect is φ≈.09–.11 except archaic words (.35). |
| Packard & Berger 2020: "you" raises liking and purchase; object "you" strongest; mechanism = thinking of someone in one's life (5, reading.md) | **VERIFIED** | Abstract: 4,200 Billboard songs, experiments N=2,921, outcomes liking and purchase; the mechanism as stated. That object "you" is strongest comes from press summaries (Discover); no effect sizes public. One field sample was 1,736 download-chart songs, 2014–16. Popularity, not acclaim. |
| Bamman et al. 2025: narrativity; country nominees 3.61 vs album-mates 3.40 (3) | **VERIFIED** | Country 3.61 vs 3.40, p=.002 (n=259); R&B 3.03/2.98; rock 3.13/3.08; rap 4.25/4.18 (all n.s.); Song of the Year 3.15 vs 3.02, p=.050 uncorrected, n.s. after Bonferroni. Hot 100: 2.58 (1960) to 3.72 (2024), 5,745 songs. No pop analysis. |
| Boyd, Blackburn & Pennebaker 2020: arc does not predict popularity (3) | **CORRECTED (outcome)** | Outcome was audience **ratings** (639 romance novels by star group, 18,074 films by IMDb rating), not sales or popularity. No meaningful effect of rating group. The authors flag the skewed ratings as a limit. Outcome type: liking. |
| Vuoskoski & Eerola 2017: sad-music liking works through being moved (4) | **VERIFIED** | Exp 1 n=308: indirect effect .30 [.25, .34]; direct effect n.s. (fully mediated). Exp 2 n=19: beauty also mediated; direct effect turned negative. |
| Mori 2022, Cognition: farewell lyrics predict tears (4) | **UNVERIFIABLE** | Title and venue confirmed; abstract and full text paywalled (PhilArchive record has no abstract). The 54 listeners, 186 pieces and the farewell finding are unchecked. Treat as SUGGESTIVE at most until read. |
| Ali & Peynircioglu 2006 replication failed: Ma et al. 2023 (4) vs 2024 (2) | **VERIFIED; same paper** | Ma, Baker, Vukovics, Davis & Elliott, Musicae Scientiae 28(1), 174–186 (2024 issue; DOI from 2022/23 OnlineFirst). n=104; results "contradicted" the original on several variables. Cite 2024. |
| Identifiable-victim effect small, r≈.05 (Lee & Feeley 2016); r=.04 n.s. in a 2026 meta-analysis of 266 effects (4) | **Lee & Feeley VERIFIED; Smith et al. 2026 UNVERIFIABLE** | Lee & Feeley: 41 studies, r=.05, significant but modest, strongest for one child photographed in poverty with a money request. I could not find the 2026 PsyArXiv paper. |
| Orvell, Kross & Gelman 2017, Science: generic "you" (5) | **VERIFIED** | 9 experiments, N=2,489. When making meaning of a negative event, 46% used generic "you" (vs 10% reliving, 3% neutral). Outcome: language use and distancing, not song. |
| Tan, Lustig & Temperley 2019: early stressed syllables (2) | **VERIFIED, wording CORRECTED** | 80 songs, 10,433 stressed syllables; 8th-level SQ .228 (.333 with 16th level); 19th-century songs 0. 77% of 8th-level syncopations were anticipations. Correction: 66 of 76 songs had **more than half** of their syncopations as anticipations. The share of anticipations did not change over time, though syncopation itself rose. |
| Nichols et al. 2009: stress on strong beats, long notes, peaks; 55% vs 45% (2) | **VERIFIED** | 679 lead sheets (229 private, 450 Wikifonia, so many standards, not only pop); all p<.0001. 55% of primary-stressed notes are long; 55% of unstressed are short. The effects are real but modest. |
| Kolchinsky et al. 2017: 86,627 songs; minor 6.16 vs major 6.28; flips in alt-folk, indie, punk; none in 1980s (2) | **CORRECTED (genres)** | Count and means verified (LabMT 0–9). The only genre without major > minor overall is **Contemporary R&B/Soul**. Alt-folk, indie and punk invert only within the 1980s (data not shown). No major–minor difference in the 1980s or in Asia. |
| Simonton equal-odds; quantity–quality r .5 to .7 (6) | **VERIFIED, scope note** | The rule holds across creators' careers (hits are a stable share of output). "Draft many and select" is an inference from it, not a test. |
| Berg 2016, ASQ: creators misjudge their own ideas (6) | **VERIFIED** | 339 circus professionals; checked against 13,000+ viewers. Creators overrated their own acts, judged peers better than managers did, and were best on novel hits. Lab replication with product ideas. |
| High pitch: vowels converge above about A4 to E5; only /i a u/ survive (2) | **CORRECTED (scope and strength)** | Agent 2 is inconsistent with itself (summary: /i a u/; table: /i a/ to E5, none above). Scotto di Carlo and Joliveau describe **operatic** formant tuning. Friedrichs et al. 2017, JASA: /i a u/ are identified up to almost 1 kHz (about C6); /e ø o/ fall to chance. Rank SUGGESTIVE for pop singing. A4–E5 is rarely reached in congregational or male pop ranges. |
| Rhyme-as-reason replicated across languages (1) | **CORRECTED (strength)** | Filkuková & Klempe 2013 found **no** difference in the credibility of rhymed vs plain slogans when readers judged content (agent 6 is right). In McGlone the effect shrank when readers were told to separate form from meaning. Downgrade STRONG to SUGGESTIVE. |

## 3. Local numbers recomputed

**Agent 5, pronouns** (37 songs, not 38: ours.json and my run both give 37). Medians per 100 words:

| | "I" | "you" | I + you (per-song sum) |
|---|---|---|---|
| Ours | 5.17 | 1.98 | **7.78** |
| Acclaimed (245) | 7.60 | 4.50 | 12.86 |
| All hits (4,617) | 8.43 | 5.41 | 14.15 |

- Acclaimed hits with "you" ≤ 2.0: **26.1%** (all 20.1%). VERIFIED.
- I + you: agent 5's 7.2 is the sum of two medians. The median of per-song sums is 7.78. At or below 7.78: **22.0%** of acclaimed hits, 17.4% of all. At 7.2: 18.0% and 14.5%, which matches agent 5's arithmetic. CORRECTED: report 7.8 and 22%.
- Third person: median 2.3 per 100 words in my count (agent 5 said 2.1; the word list differs). Close enough.
- So our pronoun layer is thin but not off the distribution: about one acclaimed hit in five is as impersonal.

**Agent 7, data files.** All exist. songs_meta.csv has 2,079,510 rows (VERIFIED). English songs with at least 8 lines: 1,197,483 (agent: 1,197,486; trivial), median 30 lines and 6 stanzas. acclaim_ids.txt has 947 ids, song_flags.csv 1,714,211 rows, cliques.csv 348,796 (VERIFIED). soty.psv has 371 rows.

**Covers matching (round 1).** CORRECTED in wording: covers_reduce.py matches on normalised title **and** a loose check that the hit's artist key shares a 6-character prefix with any artist in the clique. It never checks the writer. So a same-title clique that merely contains the artist can be taken. Agent 7's example is real: Elton John's and U2's songs titled "One" both carry 37. Scale: 17 of the 1,172 matched titles share one count across different artists. That is small, but the writer-checked table should replace it.

**Grammy Song of the Year spot-check** (10 ceremonies against the Wikipedia table: 1966, 1972, 1984, 1993, 2001, 2010, 2017, 2020, 2023, 2025). Winners and nominees match in 9 of 10. In 1972 the file lists only Carole King for a song credited to James Taylor / Carole King, which is harmless. **2023 lacks one nominee** (The Heart Part 5, confirmed on its own Wikipedia page). A follow-up check found **2022 also lacks one** (Right on Time; the article's own text names it). Both gaps come from Wikipedia's table. True total is at least 373. The 2026 entries match.

## 4. Cross-agent consistency
- **Year mismatches, same paper:** Johnson et al. (use 2014), Menninghaus (2023 online, 2024 issue: pick one), Ma et al. (use 2024).
- **Real disagreement:** rhyme-as-reason. Agent 1 counts the slogan study as support, agent 6 says it found nothing; agent 6 is right.
- **Strength labels differ:** Wassiliwizky is SUGGESTIVE (1, 4) vs STRONG-ish (3); use SUGGESTIVE. Text-setting alignment is STRONG (2) vs SUGGESTIVE–STRONG (6): STRONG as corpus practice, SUGGESTIVE for listener comprehension (two small studies, φ≈.1).
- **Internal inconsistency:** agent 2's high-pitch vowels (the summary and the table disagree).
- **Apparent conflicts that are compatible:** the image-density ceiling (3, 6) vs "imagery not our gap" (4), since no agent says more imagery helps. Low "you" as a chill cost (3, 4) vs no acclaim penalty (5), since the outcomes differ. Chaudhuri 2025 PACA (reading.md) vs 2024 PLoS ONE (3) are two real papers.

## 5. Rule compliance
I found no reproduced lyric or poem line in 01–07, and no quote of 15 words or more. The long "quotes" my scan flagged come from unpaired quotation marks around the pronoun "I", not from quoted text. Short quotes from masters' interviews (06_masters.md lines 12, 14, 16, 18, 23) are each under 15 words. One borderline case: 06_masters.md attributes two short phrases to Sondheim (line 12 and line 6). Paraphrasing one of them would satisfy "one phrase per source" strictly. Nothing needs removing.

## 6. Synthesis: cross-cutting conclusions, ranked after checks

| # | Conclusion (agents) | Rank | Outcome type | Basis after checks |
|---|---|---|---|---|
| 1 | Rhyme and patterned form help; twisting syntax to reach a rhyme costs (1, 3, 6) | **STRONG** for the rhyme and parallelism gain; **SUGGESTIVE** for the forcing cost | liking, comprehension, memory | Menninghaus n=282; Obermeier; Rubin & Wallace. Deviation was confounded with removing rhyme. |
| 2 | Pathos comes from people and bonds at a turning point, not from images (4, 5, 6) | **STRONG** in general; **SUGGESTIVE** for lyrics | felt emotion | Kama muta across 19 nations and Menninghaus 2015 are strong. The lyric-specific evidence (Mori) is unverified. |
| 3 | Our songs lack a speaker with a stake and a present addressee (3, 4, 5) | **SUGGESTIVE** | felt emotion (address chills); popularity (Packard) | Our gap is verified (I+you 7.8 vs 12.9; 22nd percentile of acclaimed). The chill effect of address is small once position is controlled. Round 1 found no acclaim penalty for low "you". |
| 4 | Endings carry weight, but the average carries more (1, 3, 4) | **SUGGESTIVE** | felt emotion, remembered intensity | Wassiliwizky (end effects robust within one study); Schäfer and Rozin: the whole-song average dominates. |
| 5 | Text-setting floor: stress on the beat, few archaic words, melisma on known words (2, 5, 6) | **STRONG** as practice; **SUGGESTIVE** for comprehension; **no evidence** for acclaim | comprehension, memory | Nichols, Tan et al. corpora; Johnson 2014 (n=27). |
| 6 | Heavy, regular rhyme serves the audience and marks the amateur or the machine, not acclaim (1, 6) | **SUGGESTIVE** | liking (lay) vs acclaim (page poetry) | Lay preference for AI poems is strong. The acclaim side rests on 200 page poems (Kao & Jurafsky). |
| 7 | Story is a genre's style, not a quality lever (3, 6) | **STRONG** (null except country) | acclaim (awards), liking | Bamman within-album; Boyd (ratings). |
| 8 | Repetition helps up to an inverted U; recolour the refrain (3) | **STRONG** for the inverted U; **FOLKLORE** for recolouring | liking | Chmiel & Schubert review. |
| 9 | Process: draft many, let a separate judge choose (6) | **SUGGESTIVE** | eminence (careers), audience forecasting | Simonton's rule is across careers, an inference for drafts; Berg is one field study plus a lab study. |
| 10 | Mixed feeling and contrast beat one tone; one image family flattens (4) | **SUGGESTIVE** | felt emotion | Vuoskoski & Eerola; Ullrich 2017. |
| 11 | One named feeling is not a fault (4) | **SUGGESTIVE** (absence of harm evidence) | none direct | Round-1 acclaimed median 1.2 named emotions per 100 words; no study shows harm. |
| 12 | Detail density has a ceiling, and we may be past it (3, 6) | **FOLKLORE** until tested | acclaim (claimed) | Masters' advice only. Testable now on feat.csv (quadratic in image_noun_rate). |
| 13 | "Specific equals moving" as a law (4, masters) | **Weak**: the effect is real but small | prosocial behaviour | Lee & Feeley r=.05. |

## 7. Sources checked
- Wassiliwizky et al. 2017: https://refubium.fu-berlin.de/bitstream/fub188/20311/1/nsx069.pdf
- Kao & Jurafsky 2012: https://aclanthology.org/W12-2502.pdf
- Menninghaus et al. 2023/24: https://pmc.ncbi.nlm.nih.gov/articles/PMC10725771/
- Johnson, Huron & Collister 2014: https://core.ac.uk/download/20329824.pdf
- Packard & Berger 2020: https://www.psychologicalscience.org/journals/psychological-science/0956797620902380/ ; https://www.discovermagazine.com/mind/people-like-songs-about-you
- Bamman et al. 2025: https://anthology.ach.org/volumes/vol0003/measuring-stories-in-contemporary-songs/10.63744@w9C0wDxmZTVt.pdf
- Boyd et al. 2020: https://pmc.ncbi.nlm.nih.gov/articles/PMC7413736
- Vuoskoski & Eerola 2017: https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.00439/full
- Mori 2022 (record only): https://dc2.philarchive.org/rec/MORDPE-4
- Ma et al. 2024: https://repository.lsu.edu/psychology_pubs/2339
- Lee & Feeley 2016: https://pure.skku.edu/en/publications/the-identifiable-victim-effect-a-meta-analytic-review/
- Orvell et al. 2017: https://www.eurekalert.org/news-releases/581183
- Tan, Lustig & Temperley 2019: https://www.jurispro.com/files/articles/anticipatorysyncopationinrockacorpusstudymusicperception364353370_8745.pdf
- Nichols et al. 2009: https://archives.ismir.net/ismir2009/paper/000084.pdf
- Kolchinsky et al. 2017: https://arxiv.org/pdf/1706.08609v2
- Simonton 1997 summary: https://www.jimdavies.org/summaries/simonton1997.html
- Berg 2016: https://www.gsb.stanford.edu/insights/managers-are-not-best-judge-creative-ideas
- Friedrichs et al. 2017: https://discovery-pp.ucl.ac.uk/id/eprint/1571133/1/Friedrichs2017JASA_AcceptedManuscript.pdf
- Rhyme-as-reason (Filkuková & Klempe null): https://en.wikipedia.org/wiki/Rhyme-as-reason_effect
- Chaudhuri (two papers): https://research.gold.ac.uk/id/eprint/34000 ; https://research.gold.ac.uk/id/eprint/37418
- Grammy Song of the Year: https://en.wikipedia.org/wiki/Grammy_Award_for_Song_of_the_Year ; https://en.wikipedia.org/wiki/The_Heart_Part_5
