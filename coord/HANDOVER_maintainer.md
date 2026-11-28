# Handover for a fresh maintainer window (kept current; last written 28 November 2026, 03:30 ET)

Read this, then the last ten posts of `coord/maintainer.md` and `coord/songwriting.md`. Everything here is also in the thread; this is the short form.

## Who and what
- Jason Bryant's songwriting engine, Luthier: write and judge songs from the notes alone. He reads on a phone and is not technical: short, plain words, small tables, one question at a time, and only about his songs, unsettled disagreements, or things that cannot be undone.
- You are the maintainer. The songwriting session is the other window. You talk through the repository: you post in `coord/maintainer.md` on branch `luthier-v8-stage1` (append only; a dated heading with the time from `date "+%H:%M"`; each post ends with "Ask:"), and read `coord/songwriting.md` and `coord/judging_research.md` on main. Alternate about every 15 minutes.

## His standing instructions
- **Nothing is built into the engine until 3/4 and 6/8 work** (27 Nov, 20:01). The next edition goes to Claude Code for the app. Every switch below stays unset by default.
- The engine must write in every metre in the end; metre is kept apart from style (folk, standard, pop each have their own table).
- Missing knowledge is deduced from what is known, tested, and tried again on a miss. The test of a deduction is in the notes.
- Songs 67, 68 ("Save Me from My Muse", 3/4) and 69 ("Learned It from My Hands", 6/8) are banked: never run or used for trial until the songwriting session says.
- TheSession.org data is never touched (its licence forbids AI processing). Ideas from the withdrawn studies are kept as ideas and tested fresh on allowed sources. A separate window (branch `folk-replication`) is to rebuild that test.
- Raw corpora stay outside the repository. Wikifonia is in copyright; Hooktheory is non-commercial: licences to settle before any public app.

## Working rules (each learned the hard way)
1. A rule file (PREDICTION_*.md) with the form, the marks and what you expect is committed and pushed **before** any code or run. Marks are never rewritten after a result; a miss is recorded as a miss.
2. **Count the cause before proposing a fix.** Five guessed causes were wrong on 27 Nov; every count was right.
3. No figure goes into a result or a post unless printed from its file by the command that writes the result.
4. Marks are read on the living builds' median **and** the pick.
5. After any change under lib/ or tables/: byte check (songs 54, 55, 52 written through with every switch unset must equal the repository's records; lyric53 unset must equal the Essen-arm reference), then reread room files (`lyric_room.py --check`) and wait until none is running, then commit.
6. Read the record after a run: check it carries the switches you meant and that the judge ran ("pass_the_gate" present).
7. Commit trailers and the push command are in the thread's first posts; the Stop hook wants everything committed and pushed.

## Where the metres stand
- **4/4:** works (engine v53).
- **6/8 folk (Essen table): with the package below all five seen lyrics (song 52; the words of songs 61, 50, 49, 58 set in 6/8) meet every mark** (`studies/other_metres/RESULT_247_248.md`, 28 Nov 01:30 ET). Three held-out lyrics were each read once overnight: the first missed one mark, the second two others, **the third (song 58's words) none** (`RESULT_held_out_3_6_8.md`); each miss was counted, mended and re-read. Not proof 6/8 works: all five lyrics were written for 4/4; no unseen spent folk lyric is left. 749.249 (the title line's stress pull) was tried in two arms and neither passed by its rule, so the title keeps its doubled pull (`RESULT_249.md`); 749.250 (pickup room across the section's edge, `LUTHIER_TITLE_EDGE=1`) is IN song 69's package by the songwriting session's ruling of 28 Nov 02:50 ET (`studies/other_metres/RESULT_250.md`). Known soft spot, watched not marked: a short title line takes one rhythm in 86 to 93 builds of 100 on three lyrics. **The test that counts is song 69 (banked, written for 6/8). Its package is the one below, settled by the songwriting session's rule. Do not run it until the songwriting session says Jason has answered.**
  - Package: `LUTHIER_TABLE_6_8=../../studies/other_metres/trial_tables/6-8_folk_sung LUTHIER_PLAN_6_8=folk LUTHIER_TITLE_ROOM=0.001 LUTHIER_COPY_JOIN=1 LUTHIER_TITLE_ENTRY=pickup LUTHIER_TITLE_NOWAIT=1 LUTHIER_TITLE_FRESH=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_SHARED_BARS=1 LUTHIER_SECTION_DENSITY=3 LUTHIER_TITLE_840=2 LUTHIER_REST_TABLE=1 LUTHIER_PICKUP_WINDOWS=0 LUTHIER_AGAIN_RUNS=2 LUTHIER_TITLE_EDGE=1` (the named table is Essen 6/8's own counts and rows with a rests file beside it; its borrowed stress file is not read). Reader: `studies/other_metres/read_package.py LYRIC RECORD LIMIT_712`.
  - Marks: living 30, pool 10; notes a bar 3.60 to 4.33; onsets on the beat 0.389; on the first beat 0.211; 731 at 0.40; deaths on 780 and 840 under one in ten; in the voice, no leap past an octave in a line; title lines on time 75 in 100; the share of tries to sing a marked line again that are drawn fresh (`why_again_fresh.py`, 300 builds) at most the higher of 0.076 and 1.5 times the lyric's own share before 749.240; silence before a title line 3 eighths or under. Reader: `studies/other_metres/read_6_8_lyric.py`.
  - Open: on song 61's words 749.243 (first-beat onsets in dense verses) and notes a bar pull against each other; no stress table counted on worded 6/8 song yet (OpenScore Lieder, CC0); pop-style 6/8.
- **Pop 3/4 (Hooktheory table; song 55's words in 3/4):** with the overnight's metre-level forms added, **every mark is met but K3** (stressed syllables on the first beat about 0.33 against 0.45; off the beat about 0.34 against 0.26): studies/other_metres/RESULT_pop_3_4_b.md. Nothing never made, 840 none, repeats kept. **K3 is not the draw's ordering (a count on 28 Nov, studies/other_metres/RESULT_count_k3.md): lines drawn fresh, title lines and copies meet K3; lines sung again to NEW WORDS do not (0.27 and 0.23 on the first beat) and carry seven tenths of the song's stresses, because outside 4/4 the refit of new words to an old rhythm is blind to stress (4/4 has fix 882 for this).** The form proposed: a line sung again chooses its splits and drops by the table's stress score. Read the songwriting session's last post for its word and number. 749.236 (the weight from data) and the OpenScore Lieder count are still worth doing for stress outside 4/4 but are not K3's road; the worded pop 4/4 set for 749.236 is CoCoPops (corpora/cocopops_notes.csv.gz). Package: LUTHIER_TABLE_3_4=../../studies/other_metres/trial_tables/3-4_pop_sung LUTHIER_PLAN_3_4=1 LUTHIER_RANGE_3_4=centres LUTHIER_COPY_JOIN=1 LUTHIER_STRESS_3_4=1 LUTHIER_SHARED_BARS=1 LUTHIER_AGAIN_INSIDE=1 LUTHIER_AGAIN_REFIT=2 LUTHIER_TITLE_ROOM=0.001 LUTHIER_TITLE_840=2 LUTHIER_TITLE_ENTRY=pickup LUTHIER_TITLE_EDGE=1 LUTHIER_TITLE_FRESH=1 LUTHIER_TITLE_NOWAIT=1 LUTHIER_SECTION_DENSITY=3 LUTHIER_AGAIN_RUNS=2 LUTHIER_REST_TABLE=1 LUTHIER_PICKUP_WINDOWS=0; reader studies/other_metres/pop_read.py.
- **Standard 3/4 (lead-sheet table, song 53):** met most marks earlier in the day; not reread under tonight's forms.
- **Other metres (12/8, 2/2, ...):** not begun.

## Forms by number (all behind switches, unset)
749.226 bars from density · .227 3/4 range · .228 copy join · .229 title room · .231 stress score by table (helps 3/4; a borrowed table hurt 6/8 folk) · .232 the line ahead of a title line leaves room for the title's pickup (third reading; earlier: a bar more, then a bar of rest) · .234 shared bars · .235 title line skips 870's wait · .236 the weight from data (not yet written) · .237 title line drawn fresh · .239 rhythm grammar (two equations fitted; Essen passes cell by cell in two-bar cells 4 to 11 only; not used; a third equation for pop accepted) · .240 a line sung again ends inside its slot · .241 the split-off note stays inside the limit · .242 the page gate's evidence restated without TheSession · .243 no section denser than the table's 75th · .244 a title line drawn among windows that pass 840's test · .245 outside 4/4, 870's wait draws from the table's own rests · .246 a kept window whose first bar holds only a pickup is not offered · .247 a line sung again mends its own run of one pitch, keeping the chord (AGAIN_RUNS=2) · .248 749.244 on every path (TITLE_840=2) · the title's room (.229) retired where .244 draws the title line (TITLE_ROOM=0.001).

## Queue
1. Whatever the songwriting session answers to the last post.
2. Pop 3/4 with the 6/8 package's metre-level forms added (749.243, .244, .245 where a rests file exists, the pickup reading of .232, the run mend, the title's room retired); then 749.236 (fit on Billboard pop 4/4; check across metre with lead sheets and Lieder).
3. Count OpenScore Lieder (fetch outside the repository): a worded stress table for 6/8 and 3/4.
4. The grammar's third equation (pop).
5. After the metres: the v54 paper; 749.221 (arrangement design file); the Claude Code hand-off brief.

## Machine notes
- Repository at `/home/claude/zeneng-pipeline`; if gone: clone, check out the branch, `bash setup.sh`, `bash studies/other_metres/fetch.sh`.
- The scratchpad does not survive a new container; trial lyrics are rebuilt from `songs/p62/lyric52.json`, `songs/p71/lyric61.json` (metre 6/8, bpm 54, genre folk) and `songs/p65/lyric55.json` (metre 3/4, bpm 133, genre rock).
- A whole-engine song takes one and a half to five minutes; run in the background and wait on the record file, not on a flag left from an earlier run.

## Update 04:05 ET 28 Nov: 749.251 tried, not passed
- Pop 3/4 with `LUTHIER_AGAIN_WORDS=1`: K3 first beat 0.337 pick, 0.412 median (0.45 wanted); the pick also misses K5 (0.317) and K6 rhythm again (0.3). The five 6/8 lyrics byte for byte. See `studies/other_metres/RESULT_251.md`. The switch stays unset; it is in no package.
- "Again" lines 0.272 to 0.362, 818's 0.227 to 0.35, fresh 0.465: half the gap closed.
- Proposed next (awaiting the songwriting session): count stresses in one-for-one "again" lines; count why the pick is worse than the median.

## Update 04:24 ET 28 Nov: the two counts after 749.251
- See `studies/other_metres/RESULT_counts_251.md`. Same-count "again" lines carry 0.304 of those lines' stresses (0.312 on the first beat); split-fitted lines 0.373 (0.359). Mending same-count lines alone would not reach 0.45.
- The judge does not rank in the pool: the pick is the first build past the gates in the order built. About one build in nine meets every pop mark; the pick being worse than the median is chance. Mend what reaches the pool.
- Awaiting the songwriting session: whether to write the rule file for "a line that will be sung again is drawn by the summed stress score of every set of words it will carry".

## Update 04:56 ET 28 Nov: 749.252 tried, not passed
- `LUTHIER_SOURCE_WORDS=1` (a line that will be sung again is drawn for every set of words it will carry; twelve draws, one taken by the later sets' stress score). Pop 3/4 K3 median 0.412 to 0.422; same-count "again" lines did not move. See `studies/other_metres/RESULT_252.md`. Unset; in no package. The pick met every mark by chance only.
- Proposed next (awaiting the songwriting session): a count of whether the twelve draws differ, what the stress score's best gives on the first beat, and which lines carry the same-count stresses.
- Pop 3/4 package is still the one in this file (749.251 and 749.252 NOT in it). 3/4 is not working yet: K3 misses.

## Update 05:16 ET 28 Nov: three counts after 749.252
- `studies/other_metres/RESULT_counts_252.md`. The stress score is not the wall (its best rhythm: 0.668 on the first beat; the unlimited draw expects 0.606; built fresh lines get 0.465). The twelve draws differ and choose firmly. The form acts on few lines: 818 chains most lines of a section to the line two above, so one rhythm carries up to 31 sets of words.
- Proposed next (awaiting the songwriting session): count (A) what the draw's limits remove; count (B) the best one rhythm can do for all the words it carries.

## Update 05:35 ET 28 Nov: counts (A) and (B)
- `studies/other_metres/RESULT_counts_AB.md`. Drawn lines: the unlimited draw expects 0.591 on the first beat, 0.472 is built. The largest taker is 834's early entry (0.072): a 4/4 chance (0.2) used in 3/4 because the pop 3/4 table has no entry shares, and the early rhythm is scored as if unmoved. The earliest start takes 0.043.
- One rhythm can serve all its words (0.538 for the two always-drawn lines), but 749.252's summed score picks one reaching 0.459.
- Proposed (awaiting the songwriting session): a form "outside 4/4, 834's early entry only at the table's own share; none where the table gives none"; and 749.252's sum over first-beat stresses only.

## Update 06:07 ET 28 Nov: pop 3/4 meets every mark for the first time (arm 2), narrowly
- `studies/other_metres/RESULT_253_254.md`. 749.253 (`LUTHIER_EARLY_TABLE=1`: outside 4/4 no early entry, since no table outside 4/4 gives its share) alone: K3 0.449; 0.444, missed by a hair. With 749.252 (`LUTHIER_SOURCE_WORDS=1`) and 749.254 (`LUTHIER_SOURCE_STRESSED=1`): K3 0.455; 0.46, every mark met on pick and median. By the choice written beforehand, arm 2 is taken.
- **Pop 3/4 package now:** the package in this file plus `LUTHIER_AGAIN_WORDS=1 LUTHIER_EARLY_TABLE=1 LUTHIER_SOURCE_WORDS=1 LUTHIER_SOURCE_STRESSED=1`. All unset by default. One seen lyric, one seed, a margin of 0.01: not proof.
- 749.253 changes 6/8 notes too; the five 6/8 lyrics still meet every mark with it. Song 69's package is NOT changed; that is the songwriting session's decision.
- Awaiting the songwriting session: more seeds on the seen lyric or straight to song 68; 749.253 in 6/8.

## Update 06:26 ET 28 Nov: seeds 2 and 3; pop 3/4 NOT ready for song 68
- `studies/other_metres/RESULT_seeds_3_4.md`. K3's median holds at all three seeds (0.46, 0.46, 0.46). Seed 2's pick misses K3 (0.439). Seed 3 misses K5 on pick and median (0.335; 0.331 against 0.303): narrower tunes, cause not counted, may predate tonight's forms.
- The pick is the first build past the gates and only 24 to 40 in 100 of the pool meet every mark, so "pick and median at every seed" fails most times.
- Awaiting the songwriting session: K5-at-seed-3 count or the earliest-start count first; and what "ready" should ask of the pick.

## Update 07:00 ET 28 Nov: K5 at seed 3 is old; 4/4 picks the same way
- `studies/other_metres/RESULT_counts_K5_pool.md`. The K5 miss at seed 3 is in the pre-tonight package too. It goes with the plan's lift drawn once per seed (lift 1 at seed 3: verse and chorus on one centre; lifts 4 and 6 at seeds 1 and 2). Three points only.
- 4/4's pick is also the first build past the gates (then range floor, then voice). 4/4's pool meets its own six band marks in 63.6 to 81.8 in 100 (songs 54, 55, 59, 61, 66); 3/4's pool on the same six 76.9 to 91.1; on all nine 36.5, 40.1, 23.9.
- New tool: `studies/other_metres/pool_count.py LYRIC [SEED]` runs the planner's own routine under the shell's switches and reads the pool from inside the run.
- Awaiting the songwriting session: K5-by-lift over more seeds; how the "ready" bar reads the pool.

## Update 07:32 ET 28 Nov: 749.255 tried (956's ceiling outside 4/4), and the open question
- `studies/other_metres/RESULT_255.md`. `LUTHIER_CEILING_TABLE=1` reads `trial_tables/3-4_pop_sung.commonest.json` (ceiling 0.396 every part; Hooktheory has no section labels). It moves the POOL (seed 3: pool median commonest 0.318 to 0.29; pool meeting K5 41.0 to 66.1 in 100) but cannot move the LIVING median, which is read before the gates. So by the marks as written it does not pass (K5 at seed 3 on the living median, 0.331).
- Open with the songwriting session: is the median read on living builds or on the pool? Then either the K5-by-lift count over twenty seeds, or 749.255 re-read on the pool.
- The list of 4/4-only settings is in `PREDICTION_255.md`: still acting outside 4/4 at 4/4's figures are 771's entry weights, 876's 0.09, 818's 0.8, and the lift (838).
- Judging research run 11 checked by the four steps (in the maintainer thread). Jason asked at 07:09 whether the research branch helps: answer given: not directly for 3/4.
- Pop 3/4 is NOT ready for song 68. 6/8: song 69's package unchanged and waiting on Jason's answer via the songwriting session.

## Update 07:52 ET 28 Nov: fresh seeds 4 to 6 on the pool's median; pop 3/4 misses the bar on ONE mark
- From now on every mark is read on the POOL's median (songwriting session's ruling 07:45); living median printed beside it.
- `studies/other_metres/RESULT_seeds_456.md`: with 749.255 on, all nine figure marks are met on the pool's median at seeds 4, 5, 6 (K3 0.46, 0.465, 0.465; K5 0.262, 0.197, 0.263). The one miss: the pool's share meeting the six like marks is 63.3, 76.7, 74.2 against 4/4's 76.2; the shortfall is K6 rhythm again within sections at its lower line 0.349.
- **Current pop 3/4 package:** RESULT_pop_3_4_b's switches plus `LUTHIER_AGAIN_WORDS=1 LUTHIER_EARLY_TABLE=1 LUTHIER_SOURCE_WORDS=1 LUTHIER_SOURCE_STRESSED=1 LUTHIER_CEILING_TABLE=1`. All unset by default; nothing built into the engine.
- Proposed next (awaiting the songwriting session): count K6 rhythm-again on the pool at seeds 4 to 6 on the older packages, to say whether the shortfall is old, 749.253's, or the source forms'.

## Update 08:12 ET 28 Nov: counts on rhythm sung again (K6)
- `studies/other_metres/RESULT_counts_K6.md`. The shortfall on the six like marks is K6 rhythm again. (1) The old charge (the judge's first cut, its least half) removes the builds that repeat more: at seeds 4 to 6 the removed half meets K6's line more often than the kept half. (2) It is old, and tonight's source forms raised it (pool on the six: about 42 before tonight, 46 to 52 with arm 1, 63 to 77 now). (3) Pop clips repeat a two-bar rhythm exactly 0.231 of the time (unit two back); the engine's pool about 0.012: 818's 0.8 gives refitted notes, rarely the same rhythm.
- Proposed (awaiting the songwriting session): read what the old charge charges outside 4/4; or a form where a line sung again keeps its source's rhythm exactly where counts allow.
- Tool: `pool_count.py` now prints the judge's steps in turn ("stages") and the two-bar-unit repeat; `pop_units_again.py` counts the clips.

## Update 08:31 ET 28 Nov: the old charge read; 749.257 held; the writer's research pass
- The old charge (874) outside 4/4 charges against the metre's OWN table (not 4/4's), but the pop table is of sections and the charge reads the whole song, so repetition is charged. Most of the charge is melodic. (`read_old_charge.py`)
- A line sung again ALREADY keeps its source's rhythm where counts allow (same count: 0.935 exact). 749.257 as ordered would do almost nothing; rule file NOT written; awaiting the songwriting session. Only 0.294 of lines sung again have the source's syllable count: the low exact repetition is on the lyric's side (song 55's words were written for 4/4). Proposed: a lyric-side count of matching line lengths, incl. song 68's lyric read without running it. (`count_again_rhythm.py`)
- Jason (08:20 to 08:25): we are not writing waltzes; K3's first-beat line is borrowed from 3/4 lead sheets (another style); that is before the songwriting session. He ordered a thorough research pass on the math; five researchers running; notes in `research_notes/Mathematics of fitting words to metre/`, report to `reports/Mathematics of fitting words to metre.md`; then a plain summary to him.

## Update 08:39 ET 28 Nov: the research report is in
- `reports/Mathematics of fitting words to metre.md`, delivered to Jason. Headline: no one has measured pop outside 4/4; style acts as a SHIFT (pop anticipates the beat) on top of a metre's placement rule written by level; cheapest next counts: CoCoPops-Billboard by metre (row 1), anticipation in the wordless pop 3/4 and 6/8 tunes (row 6). Note the tension with 749.253 (which removes early entries outside 4/4): pop may want early arrivals at its own rate, not none.

## Update 08:50 ET 28 Nov: the lyric-side count
- `studies/other_metres/RESULT_count_lyric_side.md`. A line has the syllable count of the line two above: song 55 0.238, song 68 0.658 (pop clips' units 0.356); of the line it is marked to sing again: song 55 0.538, song 68 0.968. So part of the K6 / six-mark shortfall belongs to the trial lyric (song 55, written for 4/4). Song 49's words are nearest to song 68's.
- Rulings 08:38: 749.257 withdrawn (not needed); 749.258 on the list (old charge by section); K3's first-beat line is WATCHED, labelled "borrowed (lead sheets)", for pop 3/4; K3 off the beat stays a mark. The bar: every mark on the pool's median and the pool on the six like marks at least 76.2, on fresh seeds.
- Proposed next: song 49's words in pop 3/4 at seeds 7 to 9 on the unchanged package; then 749.258; then the report's rows 6 and 1.

## Update 09:11 ET 28 Nov: song 49's words at seeds 7 to 9: the bar missed; the lyric is NOT the cause
- `studies/other_metres/RESULT_song49_seeds_789.md`. Every mark on the pool's median met at all three seeds, but the pool on the six like marks is 59.8, 52.8, 70.2 against 76.2 (K6 rhythm again within sections: pool median about 0.35 against a line of 0.349; the pop table's median is 0.625). By the rule: no other lyric is tried; 749.258 (the old charge reads each section against the section table) is next.
- My deduction (matching line lengths would lift it) was wrong. Proposed first: a bar-by-bar count of which bars are on a rhythm already sung, by how the line was made.
- Order awaiting the songwriting session: that count, 749.258, the report's row 6 (early arrivals in pop clips; bears on 749.253), CoCoPops-Billboard by metre (row 1).

## Update 09:23 ET 28 Nov: the cause of the last 3/4 shortfall, counted
- `studies/other_metres/RESULT_count_bars_again.md`. In a section's first 16 sung bars the engine uses 10 different bar rhythms (either lyric); a pop 3/4 clip uses 6. Bars on a rhythm already sung: 0.375 against 0.625. K6 is read WITHIN a section, so lines sung again across sections do not count; inside a section every line drawn takes a new window. The engine has a memory for pitch figures (923) and none for bar rhythms.
- Proposed form (awaiting the songwriting session's number and marks): a section remembers its bars: windows made of bars already sung in the section are favoured, the weight fitted so the builds' different bar rhythms in 16 bars meet the pop clips' median.
- Jason (09:20) wants results; this count was made at his word before the songwriting session ruled on its order.

## Update 10:08 ET 28 Nov: 749.259 (a section remembers its bars) tried: song 55's words pass, song 49's do not
- `studies/other_metres/RESULT_259.md`. `LUTHIER_BAR_MEMORY=64` (fitted on seen seeds; FIT_259.md). Fresh seeds 10 to 12: song 55's words meet every mark and the six-mark share (76.8, 79.5, 89.1); song 49's words miss at seed 10 (60.1) and their pick has a leap past an octave at seeds 10 and 12 (959 is off outside 4/4). Not passed; pop 3/4 not ready.
- The form barely moves the figure it was fitted to (different bar rhythms in 16 bars stay 9 to 10 against pop's 6): it reaches too few lines.
- Awaiting the songwriting session: act where the bars are made (818's choice, or the section's first rhythms); 959 outside 4/4; a count of K6 against what the seed fixes.
- Switches now in the tree, all unset by default: AGAIN_WORDS, EARLY_TABLE, SOURCE_WORDS, SOURCE_STRESSED, CEILING_TABLE, BAR_MEMORY (plus the earlier ones). Nothing is built into the engine.

## Update 10:46 ET 28 Nov: counts with 749.260
- `studies/other_metres/RESULT_260_counts.md` (seen seeds 1 to 12, both lyrics). 749.259 (BAR_MEMORY=64) raises the six-mark share at all 12 seeds on both lyrics: song 55's words 5 to 12 seeds of 12 at or over 76.2; song 49's 2 to 9 (under at seeds 6, 8, 10). It reaches only about one line in ten (lines drawn from windows).
- 749.260 (`LUTHIER_OCTAVE_OUTSIDE=1`: 959's octave gate outside 4/4) coded behind an unset switch; on seen seeds it passes over up to 220 builds in 1,000 on song 49's words and starves no pool. To be tested with the test for ready at fresh seeds 13 to 15 (both lyrics; every mark on the pool's median; six-mark share at least 76.2; no pick with a leap).
- Next (awaiting the songwriting session): the memory where the bars are made (818's choice, or the first sections' first rhythms), weight fitted on seen seeds; then seeds 13 to 15.
- Current pop 3/4 package: RESULT_seeds_456's switches + `LUTHIER_BAR_MEMORY=64` (+ `LUTHIER_OCTAVE_OUTSIDE=1` once ruled). All unset by default.

## Update 11:21 ET 28 Nov: THE CAUSE of the 3/4 six-mark (K6) shortfall and of the seed spread: melismas
- `studies/other_metres/RESULT_count_first_rhythms.md` + `RESULT_count_melisma_share.json`. The song's melisma share (848) is drawn once per seed and title among 3.8, 8.6, 16.2 syllables in 100 (4/4's kept quartiles). On the notes AS MADE, rhythm again within sections is about 0.5 and K6's line is met in 98 to 100 builds in 100; AS SUNG (second notes placed, each line on its own) it falls to 0.35 at 16.2. Rank correlation of the share drawn with the six-mark share over seeds 1 to 12: -0.93 (song 49's words), -0.65 (song 55's).
- Proposed form (awaiting the songwriting session's number and marks): a line that sings an earlier line again takes its second notes where its source has them. And count the melisma share for 3/4 and 6/8 from the lead sheets (848's figures are 4/4's).
- 749.260 (`LUTHIER_OCTAVE_OUTSIDE=1`) is coded behind an unset switch, to be tested with the ready test at fresh seeds 13 to 15. 749.259 (`LUTHIER_BAR_MEMORY=64`) stays in the package.
- Research read today: `reports/Mathematics of fitting words to metre.md`, the world-music branch's three reports, `reports/Beat strength in threes from the physics of entrainment.md`. Jason was advised against a separate physics branch for now.

## Update 12:12 ET 28 Nov: POP 3/4 MEETS THE BAR FOR READY (both seen lyrics, fresh seeds 13 to 15)
- `studies/other_metres/RESULT_261.md`. With 749.261 (`LUTHIER_MELISMA_FOLLOW=1`: a line that sings an earlier line again takes its second notes where its source has them) and 749.260 (`LUTHIER_OCTAVE_OUTSIDE=1`), both lyrics pass at seeds 13, 14, 15: every mark on the pool's median, six-mark share 91.2, 91.2, 96.8, 94.4, 99.6, 94.4, no pick with a leap. By the songwriting session's rule, songs 68 and 69 are ready to run together WHEN THE SONGWRITING SESSION SAYS SO. Do not run them before.
- **Pop 3/4 package:** RESULT_seeds_456's switches + `LUTHIER_BAR_MEMORY=64 LUTHIER_MELISMA_FOLLOW=1 LUTHIER_OCTAVE_OUTSIDE=1` (full line in the maintainer thread's post of 12:12 ET). All unset by default; nothing built into the engine (Jason: wait until 3/4 and 6/8 both work).
- Standing gaps, said with the pass: sections use 8 to 9.5 different bar rhythms as sung against pop's 6; K3's first-beat line is borrowed and only watched; the melisma share is 4/4's; 838 ran to 493 deaths at one seed.
- Song 69 (6/8): package unchanged; whether it takes 749.253, 749.260, 749.261 is the songwriting session's to rule before it runs.
