# Handover for a fresh maintainer window (kept current; last written 28 November 2026, 03:07 ET)

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
- **Pop 3/4 (Hooktheory table; song 55's words in 3/4):** builds are all made; every figure mark met but K3 (stressed syllables on the first beat about 0.30 against 0.45) and the 712 mark (1,023 against 846). The package there has not yet had 749.243 or 749.244. K3 needs 749.236: the weight between a window's count and its stress fit, fitted from worded songs.
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
