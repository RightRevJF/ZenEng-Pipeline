# World music research: posts

Three reading passes on world music for the metre work (3/4 and 6/8), on branch `world-music`: rhythm and metre; melody, pitch and psychoacoustics; form and repetition. Reports go in `reports/world_music/`. Research only: nothing under `lib/` or `tables/` changes. No TheSession data, and no figure from the withdrawn studies.

### 28 Nov 2026 10:23 ET, world music research (branch at the commit that carries this post)

**Started.** I've read the last posts on both coord files, `songs/p68/fixlist_v54.md` and `reports/Mathematics of fitting words to metre.md` (luthier-v8-stage1), so the passes build on that report and don't repeat it.

The 749 findings each pass is aimed at:
- **first-beat stress in triple metre:** 749.231, .236, .244, .252, and K3's borrowed first-beat line;
- **arriving one division early:** 749.253 (834's early entry);
- **bar rhythms sung again in a section:** 749.257, .259;
- **leaning on one pitch:** 749.226 (P6), .227, .255;
- **4/4 figures with no table of their metre:** 749.256.

This morning's "Grammar of great music" notes (outside the repo) are reused where they fit, with their sources checked again.

Ask: none.

### 28 Nov 2026 10:45 ET, world music research (branch at the commit that carries this post)

**Reading done; the three reports are being written.** The notes are outside the repo. The reports will cite them by link.

Three questions from the brief **have no published answer for triple metre**. Each will go in its report as a count to make, not a figure:
- beat one against beats two and three (only Essen 4/4 has a full onset profile);
- arriving one division early (every measured rate is 4/4 or 2/4);
- different bar rhythms per section (no count exists for any tradition).

One correction to the last report, for 749.253: Hayes & Kaun's 10.9% "headless" lines are lines whose first syllable comes in late. They don't show that 89% begin with a pickup.

Ask: none.

### 28 Nov 2026 10:52 ET, world music research (branch at the commit that carries this post)

**All three passes are done.** The reports are in `reports/world_music/`, each with a `.sources.json` beside it. `SUMMARY.md` ranks the ten findings that bear most on the metre work.

| Report | Sources | Testable ideas |
|---|---|---|
| 1, rhythm and metre | 70 | 29 |
| 2, melody, pitch and psychoacoustics | 65 | 19 |
| 3, form and repetition | 49 | 19 |

The counts to make first:
- notes on each beat and eighth in 3/4 and 6/8 (749.231, .252, K3);
- how often a strong beat is left empty because the note came early (749.253);
- different bar rhythms per 16 bars, against shuffled bars (749.259).

**Points for the maintainer:**
- Most papers were read through a summary tool, so their exact figures are flagged `figures_to_check`. Check them before anything is built in.
- The Hooktheory clips' licence depends on whether they come from the Sheet Sage release (CC BY-NC-SA 3.0); that isn't confirmed. Essen's licence is unconfirmed too.
- McBride et al. 2024's melody data may contain TheSession material. Don't open it until that's checked.
- The last report's sentence that 89% of lines begin with a pickup should go (749.253).

Nothing under `lib/` or `tables/` was changed.

Ask: the maintainer, the three counts above, rule first, when the metre work allows.

### 28 Nov 2026 12:49 ET, world music research (branch at the commit that carries this post)

**Passes 4 and 5 started, at the writer's word (12:30 ET): music as a language, and the world's traditions region by region.** Nine readers are done; the two reports are being written.

- **One deviation from "reading only":** the Africa reader downloaded the Global Jukebox Cantometrics code tables (Zenodo 4898406, 3.3 MB, outside the repo) and counted their call-and-response codes. They go in pass 5 as our own count, not a published figure. Redo them rule first before any use. The licence conflicts: Zenodo says CC BY-NC 4.0, the repo's own file CC BY 4.0. The stricter reading is taken.
- **Early signs across regions:** in a 3/4 waltz, a springar, the Arabic waltz cycle, Javanese and Thai cycles and the Indian tihai, the arrival that closes a group is strong and the slot before it leads in. Each is labelled as measured or theory in the report.

Ask: none.

### 28 Nov 2026 12:55 ET, world music research (branch at the commit that carries this post)

**This morning's report is now on the branch too:** `reports/Grammar of great music.md`, on what songs that lasted share across cultures. It ends with seven study designs for the judging research, each with its rule and pass mark written first. Passes 4 and 5 follow when written.

Ask: none.

### 28 Nov 2026 13:03 ET, world music research (branch at the commit that carries this post)

**Passes 4 and 5 are done**, and `SUMMARY.md` now ranks the ten findings from all five passes.

| Report | Sources | Testable ideas |
|---|---|---|
| 4, music as a language | 97 | 27 |
| 5, regional dialects | 114 | 36 |

**What's new for the maintainer:**
- **Beat 3 of 3/4 attracts notes as a lead-in** (waltz and springar timing, the Arabic waltz rhythm, the Indian run-up to the cadence). Stressed syllables on beat 2 against beat 3 stays open. Count notes and stresses separately (749.252, K3).
- **6/8:** the fourth eighth is a second landmark; the second and fifth are the weakest (749.231).
- **Early entry follows the lyric's language too** (common in English, rare in German, Italian and French) and needs a level setting (749.253).
- **Density in notes per second, not per bar;** 749.226's 2.09 a bar is about 1.16 a second at a 0.6 s beat (749.226, .243, .256).
- **Rhythm tables from sung songs of the style, not the lyric's language:** song and speech rhythm correlate about 0.09 (749.233).
- **The missing rhythm memory (749.259) is a gap in how the engine is built:** with no drum cycle, the melody must carry the repetition.
- **Commonest pitch:** count by duration, by third of the song and with syllable rate; the leaned-on note needn't be the home note (749.255).

**Licence changes:** the Weimar Jazz Database is ODbL; Cantometrics' licence conflict is stated, and the stricter reading taken. The Cantometrics counting scripts are in `reports/world_music/cantometrics_count/`; the data isn't in the repo.

Ask: the maintainer, the four counts in SUMMARY.md, rule first, when the metre work allows.
