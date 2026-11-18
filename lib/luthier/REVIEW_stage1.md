# Review of Luthier v8 stage 1 (branch luthier-v8-stage1, c1ce8e2), by the songwriting session, 18 November 2026

Merged into main by fast-forward at the writer's instruction ("please review it and merge it into main").

## What was checked

| Check | Result |
|---|---|
| Every .py in the branch compiles | yes |
| No .pkl, src/ or out/ in the branch; no key | none |
| lib/luthier/gen_l8.py on song 57's v7 file gives the committed melody_l8_p67.py | byte for byte |
| Song 49 main, 1,000 builds, from the committed engine (songs/p59/runl8/review_main_v8.txt) | order 00ab881be2a7, 671 survivors, 752's pick a4e59c5f298c, 69 eligible: Table FS exactly |
| Song 57 on v8, 40-build smoke (songs/p67/runl8/review_smoke_v8.txt) | runs; 14 survivors; order 858e793a8e20 |
| 750 patch | keeps only rhythms whose onsets rise strictly inside the bar |
| 751 patch | evaluate's notes are in onset order, so the test of a doubled onset is sound |
| 753 (lib/carol/lyricsearch.py) | sleepin', callin', nothin', 'n', 'cause, a.m., p.m. read as meant |

## Findings (from 749.40)

**749.40. The committed stage-1 run logs predate 752.** *Problem:* songs/p59, p60, p61, p64 and p65's runl8/run_*.txt were made before the
pick was moved to luthier_judge6: song 49's records code 'e545ed727af5' where the committed engine reads '68e55733a5b0', and it prints
730's pick (3ef101ca2544) and 447 eligible where 752 gives a4e59c5f298c and 69. Songs 51 and 54 differ the same way; 50 and 55 happen to
agree. The orders are unaffected. *Evidence:* the review run above reproduces Table FS from the committed engine. *Fix:* make the five
runs again from the repository, or mark the logs as pre-752. *Check:* every log's code matches its engine.

**749.41. 753's a.m. rule catches a sentence's last 'a'.** *Problem:* words() rewrites any "a." followed by a word starting with m:
"it was plan a. make it work" reads "ayem", "ake". The same holds for "p." *Fix:* match "a.m." only when the m is followed by a full
stop or the word ends ("\ba\.\s?m(\.|\b)" with the next character not a letter). *Check:* "plan a. make" reads plan, a, make; "5 a.m." reads ayem.

Also noted, no finding: the branch commits the spec itself (reports/Luthier_v8.docx). 749.35 stays open with the session.
