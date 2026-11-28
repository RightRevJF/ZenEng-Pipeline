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
