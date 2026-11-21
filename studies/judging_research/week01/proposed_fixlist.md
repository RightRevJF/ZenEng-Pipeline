# Proposed list from the judging research, week 01 (for the maintainer)

21 November 2026. Proposed by Jason Bryant from the judging research (studies/judging_research/week01 on the judging-research branch: report.md, card_1.md to card_4.md, debate.md, chair.md). Nothing here is in the engine. Numbers are proposal labels (J1 to J6); the maintainer assigns 749 numbers to whatever is taken up. Every item is rule first: read, then decide.

## In short

One finding on the written notes has held on two cover sources: songs whose chords move rather than loop within a section get covered more (J1). This week's papers add three leads for how a song spends its surprises (J2 to J4) and one for the hook (J5). None of the leads has been tested against the yardstick (still loved plus covered). They are proposed as readings of Luthier's builds against the kept songs, with a gate only if a build stands outside the kept range. J6 lists the studies that would turn the leads into evidence; they need data fetched and Jason's go-ahead.

Two cautions carry through. Luck and social history decide much of which songs win (Salganik et al. 2006), so a note measure can at best tell the strong from the weak at the ends, and effects will be small. And covers can feed a song's fame (dos Santos & Figueiredo 2024), so covers made in a song's first five years are the cleaner target.

## Items

### J1 Chords that move within a section (the one replicated finding)
**Status.** Replicated on two cover sources. Not yet checked on covers made before fame (J6a).
**Problem.** The chord writer takes a section's structure, which bars repeat which, from one kept section, whole (800). So Luthier's builds loop at the kept rate on average. The covered end of the kept songs loops less. The covers study proposed on 15 November to keep chord repetition within a section below the kept median, at least in the verse or the bridge. A search of lib/ on main found no rule for it; the chord writer reads `loops` and `distinct_bars` only in its held-out test.
**Evidence.** `studies/covers/covers_study_report.md`. Chord repetition within a section against covers, standardised: −0.124 (p .003) on 780 songs with SHS100K covers; −0.071 (p < .001) on 2,360 songs with Discogs-VI covers. Against views: −0.003 (p .88). Covers and views are unrelated once release year is held (r = 0.00), so this is the musicians' channel, not the audience's.
**Fix.** Rule first: read the covers study's within-section chord repetition on Luthier's chosen builds (songs 52 to 58, 60) and on the pool, against the kept distribution. If the chosen builds sit at or above the kept median, weight the structure draw (800) toward kept sections below the median in at least one of verse or bridge. Leave the chorus free; the audience channel rewards predictability there.
**Check.** Within-section repetition of chosen builds below the kept median in verse or bridge. The stage 4 held-out readings (first, last, chords, bigrams, bars) stay within their floors. Song 59 read only.

### J2 Plain chords, varied path
**Status.** Lead. A reframing of two existing results (chords that move; conventional chord choices helped a little on every channel in the covers study). The interaction is untested.
**Problem.** None in the engine yet: the writer draws bar content from kept bars given the two before, so single moves are already conventional. The question is whether the gain from J1 is larger when the chords themselves are plain. If so, J1 should be paired with no extra lean out of the key on the same sections.
**Evidence.** Card 2 (folk phrases built of expected, small-step material survive re-singing); card 1 (surprise mostly lowers pleasure); covers study (conventional chord choices: chord surprise −0.030, p .06 on Discogs-VI, −0.043, p .02 on views).
**Fix.** No engine change now. Add a reading: mean chord surprise (long-term model, trained on kept songs only) against within-section repetition, for chosen builds and kept songs, so the build's place in that plane is on record.
**Check.** The reading is reproduced byte for byte. Its test against covers is J6b.

### J3 Earn the surprise
**Status.** Lead from a lab study. The covers test of a Cheung-style term passed on SHS100K (+0.076, p .03) and failed on Discogs-VI (+0.009, p .54).
**Problem.** The chromatic setting (805, 823) sets how many bars leave the key, not where they fall. A surprising chord may land anywhere.
**Evidence.** Cheung et al. 2019 (card 1): 39 listeners, 30 chord progressions, first hearing. Surprise lowered pleasure overall (−0.33), uncertainty too (−0.14), and their interaction was −0.12, so surprise helps only after a predictable stretch, and that region is small. Brain-scan replication in 40 new listeners. The repo's earlier chord term differs from Cheung's in five ways (card 1), so the Discogs-VI failure does not settle it.
**Fix.** Rule first: read, for the kept songs and the chosen builds, the share of out-of-key (or high-surprise) chords that follow at least two bars inside the key. If builds stand under the kept 10th, place out-of-key bars after settled bars before anywhere else. No change if builds are inside the kept range.
**Check.** The chromatic share per song unchanged (823). Builds inside the kept 10th to 90th on the new reading.

### J4 Reach the surprise smoothly
**Status.** Speculative (the Geometer's round 2 proposal). Untested anywhere.
**Problem.** A surprising chord can be reached by small voice moves (C to A-flat: two half steps, one tone held) or by a leap in every voice. Nothing reads which.
**Evidence.** Debate round 2. Folk phrases built of small intervals survive (card 2). No data on songs yet.
**Fix.** No engine change. Add a reading: among each song's top quarter of chord changes by surprise, the mean smallest voice-leading distance (pitch-class sets, taxicab), for kept songs and builds. Settle the voice-leading rule before looking.
**Check.** The reading is reproduced. Its test against covers is part of J6b, with J1 and J2 held.

### J5 Keep the hook short, early, stepwise and predictable
**Status.** Lead from folk transmission. It measures what people remember and copy faithfully, not what musicians choose to cover.
**Problem.** The hook study (`studies/hooks`) measured chorus repetition, typical cells and surprise. It did not read phrase length or the hook's place in the chorus as predictors of memory.
**Evidence.** Janssen, Burgoyne & Honing 2017 (card 2): 9,639 phrases in 147 Dutch tune families. Log-odds of a phrase surviving, per SD: length −0.30, surprise −0.24, later position −0.10, small intervals +0.10, repetition +0.09. The notes explain about 5% (marginal R²); nothing was tested on held-out songs.
**Fix.** Rule first: read, for the hook phrase of each chosen build and the kept choruses, its length in notes, its place in the chorus, its mean interval and its surprise. If a build's hook stands outside the kept 10th to 90th on any, say which, and propose a gate on that one only.
**Check.** Readings reproduced; the words' fit does not fall; song 59 read only.

### J6 Studies that would turn the leads into evidence (need Jason's go-ahead and data)
**a. Early covers.** Rerun J1 counting only covers made within five years of release (Discogs-VI release years, cross-checked with SecondHandSongs dates). Prediction, written now: repetition beta −0.05 or stronger on early covers. Fails if weaker than −0.03 or p > .10 while it holds on later covers (the signal would then travel through fame). Needs Discogs-VI and the Hooktheory notes fetched again (not committed).
**b. Fresh songs.** McGill Billboard chord charts are already in the repo (`studies/harmony/billboard_sections.json`, 739 songs). Join them to Discogs-VI and SHS100K covers, drop songs already in the covers study, freeze J1, J2 and J4 before the join. Each needs a beta of 0.05 or more in its stated direction. Power is low (about 30% for 0.05 on about 700 songs), so a null is not a verdict; LargeSHS (arXiv 2511.15270), when downloadable, would be the better set.
**c. The ceiling.** The MusicLab public data (Salganik et al. 2006) shows how much of a song's success is luck. Prediction: appeal without social cues explains under half of a song's share in any one social world (strong condition). Ask the authors about terms first.

## Not proposed

Shape templates measured by distance on a plane, and reading S = 1 + g/π as an angle, were dropped in the debate (flexible, and an earlier flexible reader failed on fresh songs). The folk-phrase survival test is not proposed as a covers test, only as the hook reading in J5.

## Sources

1. Cheung, Harrison, Meyer, Pearce, Haynes & Koelsch (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. Current Biology 29(23). https://doi.org/10.1016/j.cub.2019.09.067
2. Janssen, Burgoyne & Honing (2017). Predicting variation of folk songs: a corpus analysis study on the memorability of melodies. Frontiers in Psychology 8, 621. https://doi.org/10.3389/fpsyg.2017.00621
3. Salganik, Dodds & Watts (2006). Experimental study of inequality and unpredictability in an artificial cultural market. Science 311, 854-856. https://doi.org/10.1126/science.1121066
4. dos Santos & Figueiredo (2024). Assessing the impact of sampling, remixes, and covers on original song popularity. LAMIR 2024. https://arxiv.org/abs/2411.01242
5. The repo's covers study: studies/covers/covers_study_report.md (main).
