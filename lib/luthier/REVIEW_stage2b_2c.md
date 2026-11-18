# Review of stages 2b and 2c (Luthier v10 and v11, fixes 770 to 786), 18 November 2026

Branch `luthier-v8-stage1` at fe425dd, fast-forward from main. Merged.

## What was checked

| Check | Result | Held? |
|---|---|---|
| Every .py in lib/luthier, the l10 and l11 engines, lyricsearch.py compiles | all compile | yes |
| `gen_l11.py /home/claude/p67` reproduces the committed `melody_l11_p67.py` | byte for byte | yes |
| 781: a.m. and p.m. as whole tokens (749.41) | "plan a. make" keeps "a"; "5 a.m. and 6 p.m." gives ayem, peeem | yes |
| 782: `slots.py 112 13 10 7 -- 2 2 1` (749.45) | bars read as bars; the 7-syllable line in one bar flagged | yes |
| Song 55 (p65) main rerun, 1,000 builds | survivors 788, order 6a9fcf413211, pick 051fad3b89a8, as runl11/run_main.txt | yes |
| Song 54 (p64) main rerun, 1,000 builds | survivors 640, order 74942a1406ad, as runl11/run_main.txt | yes |
| 783: re-evaluate every clean survivor from the stored 8-field notes | p65 609 of 609 pass; p64 545 of 545; p67 732 of 732 | yes |
| 783 control: the same p67 builds with moved386 dropped | 546 pass, 186 die at 267 | the check is live |
| 784: runl11 logs are from the committed engines | code_sha differs on all five songs (749.46) | no |

Songs 54 and 55 have no build where 386 moves a note (0 of 545, 0 of 609), so on them the eighth field is never read. Song 57 (p67) has 396 of 732 clean survivors with a 386 move; that is the song 749.35 came from, and it is the real test of 783.

Song 57 on l11 (a check, not a new record): 1,000 main builds, survivors 851, order 66a278bb7f03, pick 830b39a046f9. Song 57's pick of record stays be9dba1f3d5c (v7).

## Finding 749.46: the runl11 logs' code_sha is not the committed engines'

**Problem.** 784 says the `runl11/` logs are from the committed engines. Their code_sha does not match what the committed engines compute.

**Evidence.** sha1(engine + lyric + p40/judges.py + p36/melody_p36.py)[:12], committed engine against the log:

| Song | Log | Committed engine (and my rerun's log) |
|---|---|---|
| p59 | de9980323711 | e2bd595ee676 |
| p60 | 6f6fcb2d5431 | 4f47c0f2fe7c |
| p61 | 95ad9f2570f1 | 769c20e82af5 |
| p64 | d0437ef8da41 | 53ad5c303c2e |
| p65 | e09301a20870 | 8a9b4858f763 |

The orders and survivors reproduce exactly on p64 and p65, so whatever differs does not change a build. Dropping the two unasserted `replace` calls of gen_l11 (the STATS list and the docstring) does not give the logged hash either.

**Fix.** Rerun the runl11 logs from the committed engines, or say which bytes differed (a judge or melody_p36 copy on the maintainer's box is the likeliest).

**Check.** Each log's code_sha equals the committed engine's.

## Note

784 also removed the session's review logs of stages 1 and 2a (p59 review_main_v8, p64 and p65 review_main_v9, p65 trace212_v9). They described superseded engines; their figures are in REVIEW_stage1.md and REVIEW_stage2a.md, so nothing is lost. The new review logs are `songs/p64`, `p65`, `p67` `runl11/review_main_v11.txt`.
