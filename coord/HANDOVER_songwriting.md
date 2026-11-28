# Handover: the songwriting session (kept current overnight, 27 to 28 Nov 2026)

A fresh songwriting window should read this first, then `coord/THREAD.md`, then the bottom of `coord/maintainer.md` (on `luthier-v8-stage1`), `coord/judging_research.md` and this file's companion `coord/songwriting.md`.

## The writer's standing instructions (Jason)
- **Metres first.** "Prioritze these fixes" (15:42 ET). Nothing is built until 3/4 and 6/8 meet their marks (20:01 ET). The next edition goes to Claude Code for the app.
- **Check-ins every 15 minutes,** alternating with the maintainer, until 3/4 and 6/8 write properly.
- **Extrapolate mathematically,** test, try again on a miss (18:50 ET). Missing cells are deduced "like in algebra", proved first on a cell that can be counted. The notes alone are the test.
- **Metre apart from style** (15:52 ET): a lyric's genre chooses its style table. Folk is Essen, standard is the Wikifonia lead sheets, pop/rock/indie is Hooktheory, hymn is the hymns.
- **TheSession.org data is never touched** (its licence forbids LLM processing). Ideas from it are kept only as untested hypotheses, to be retested on allowed sources (20:33 ET).
- **Timbre on the arrangement side is parked** until the metres work (20:03 ET).
- **Overnight:** nothing goes to him unless it can't be undone (21:32 ET).
- **Working with him:** one question a turn, A/B/C with a recommendation; show content before asking; concise for a phone; full lyric drafts before music; mouth tests after lock.

## Where each metre stands (21:40 ET)
- **6/8 folk (22:05 ET):** the package is plan unpadded, copy join, title room, 749.232 (the line ahead ends early, a bar of rest), 749.237 (title drawn fresh), 749.234 (shared bars), 749.240 (again inside slot), the refit, 749.241 (split note inside limit), 749.243 two-sided (section density inside the table's middle half) and 749.244 (title line drawn among windows passing 840). **It meets every mark on songs 52 and 61's words, pick and median** (eb00414, `title_840.json`). Those lyrics are seen ground, so a held-out third spent lyric goes first: song 50's words, by rule (1d9e7d0). An added mark: the silence before a title line at or under 3 eighths (Essen's 90th); the package's silence is 5 eighths, from 749.232's bar of rest. Step A (749.232 off) missed: song 52's bridge title needs room for its pickup. 749.232's third reading (the line ahead ends an eighth earlier per light syllable the title opens on, no bar of rest; LUTHIER_TITLE_ENTRY=pickup) gives song 52 every mark with silence 2 eighths; song 61's words miss notes a bar by one note (3.596). Accepted (22:36 ET): 749.243 moves only the over-dense section's line. **Result (5e860bb): songs 52 and 61's words meet every mark, silence included. The held-out song 50's words, read once, meet ten of eleven and miss first-beat onsets (0.198 pick, 0.204 median, against 0.211).** 6/8 folk is not passed on a held-out lyric yet. The count (449bf61): our lines begin after the bar line 0.22 to 0.39 of the time against Essen's 0.081, from 870's wait (4/4's rests used in 6/8) and pickup-shaped windows sung a bar late; copies carry it on. Accepted (23:24 ET): 749.245 (870's wait from the table's own rests outside 4/4) and 749.246 (a pickup-only first bar read as a pickup before the bar line, or dropped). Then 52, 61's words and 50's words on every mark, then a new held-out lyric (49 or 58), read once. Song 69 is not ready to put to Jason yet. Next number 749.247. If it passes, put song 69 to Jason in the morning, one question A/B/C. The borrowed stress score is dropped; Lieder's counted 6/8 stress comes later.
- **3/4 pop** (song 55's words, genre rock, Hooktheory table): every figure mark met but K3 (words' stress on beat one: 0.278 pick, 0.305 median, against 0.45); the 712 count 1,023 against 846. Next: the pop rhythm equation (749.239's third: second order plus a repeat two bars back), then 749.236's weight (Billboard pop 4/4, checked across metre on the lead sheets and Lieder).
- **3/4 standard/waltz:** the earlier package (plan form, form B, 749.231) read; first-beat stress moves at the draw; the commonest pitch slightly over.
- **Rhythm grammar (749.239):** bars-as-words passes in Essen 6/8 two-bar cells 4 to 11 only (ruled: used only there). Not needed for the dead builds, which were 749.240.

## Songs banked (not to be run as trials)
- **67** "A Door in the Coral" (p77): held until the drafting fix.
- **68** "Save Me from My Muse" (p78): a 3/4 punk waltz, high tenor, Hooktheory pop table. The real 3/4 test once pop 3/4 passes. Ask Jason one question before running.
- **69** "Learned It from My Hands" (p79): a 6/8 folk protest ballad, baritone with the line's voices on the last chorus. The real 6/8 test once 6/8 passes on songs 52 and 61's words. Ask Jason one question before running.

## The lists
- **Fix list for v54:** `songs/p68/fixlist_v54.md` and Doc https://claude.ai/artifact/PeBRPVydu8R92mMJtPPd5V. Next number 749.247. The Doc is current to the held-out reading (5e860bb).
- **Research:** `research_notes/Music and the body/` (40 sources).
- **Asked of the judging research** (19:24 ET): surprise against a grammar (placement and level), once a grammar passes whole on a table.

## How the checks are done
- **Rule before run,** by commit times.
- **Figures from the json files,** never from posts.
- **Every moved figure** read on the living median and on the pick.
- **Missed is missed;** a miss now leads to the next form, rule first.
- **Commits** end with the Co-Authored-By and Claude-Session lines.
