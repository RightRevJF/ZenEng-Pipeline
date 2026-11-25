# Luthier list for v50 (since v49)

25 November 2026. Luthier v49 (the draw read; two forms of a mend, failed by marks written first; nothing built; the engine writes v47's notes) is reviewed (`lib/luthier/REVIEW_stage34.md`) and merged into main. Song 54 and the reading of the draw on song 55 reproduce; the check passes. Next finding 749.191; next fix 964.

## In short

You found the cause: the planted peak makes the octave leaps, a dozen at a time, because the line that carries it is copied (749.186). And the title-line "fault" was no fault (749.187). Both readings stand.

Neither mend passed, and you were right not to build against your own marks. The third form, with the way back inside the line, is approved, with its marks set so the test can fail on what matters (749.189).

The writer has ruled that song 50 is the third form's hold-out, run once and only if the seen-song checks hold (749.190).

## Items

### 749.189 The third form: the way back inside the line
**Problem.** The first two forms planted the peak less often than v47 (5 to 20 in 100 fewer). The second form's way back fired in 2 to 16 builds in 1,000, because it sat at the last chorus line, where the peak is usually out of reach (749.188).
**Fix.** Of the carrying line's 60 draws, take the first that reaches the peak with no leap past an octave; if none does, take the first that reached the peak (v47's own draw). Behind a switch until it passes.
**Check (written before any run).** In every 4/4 song (55, 54, 58, 49, 60, 59, 61, 62):
- living builds above v47's;
- builds' middle words' fit within 0.02 of v47's;
- the chosen tune at or over its floor;
- the clean reading (v47's fitted spec, only the form changed, gate off): builds holding a leap past an octave at or under the kept 17.5 in 100.

On songs 55, 54, 58: the three-song soundness rule; pools of 10 or more; a random pool pick failing the rule no more often than v47's 6.5 in 100.
A check of the code, not of the idea: the peak planted within 3 in 100 of v47's count in each song (by construction it should match).
Then, if the writer agrees (749.190), song 50 once, by the same marks, its ledger line first.

### 749.190 A hold-out for 749.182 (for the writer)
**Problem.** Every 4/4 song we have has now been run under a form of 749.182, song 59 included. The third form can only meet a song it has never touched by spending a sealed one.
**Options.** Song 50 (folk, 4/4, 88), run once if the seen-song checks pass; or no hold-out, the third form judged on seen songs only. Song 63 stays reserved for the loop gate (749.185).
**Ruled (the writer, 25 November): spend song 50.** Run once, only if every seen-song check of 749.189 holds, by the same marks. The ruling is in the ledger (`studies/judging_data/README.md`); the run writes its own line there first.

## Addendum: the third form, run and failed (luthier-v8-stage1 at 27f257d)

The third form ran before this list reached the maintainer, by its own marks, and fails by both its marks and this list's (living builds under v47's in songs 55, 49, 61; the clean reading over 17.5 in five songs of six). Not built. Song 50 not run; still sealed. The maintainer's finding stands: the plant and the leaps trade one for one, because 950 raises the carrying line's top and leaves its centre.

### 749.191 The carrying line's centre (reading first)
**Problem.** About one planted build in six reaches the peak only by leaping; no choice among draws avoids it (the three forms of 749.182).
**Fix.** A reading first, rule committed before it: where kept songs' highest lines sit their centre against their top. Then a form that lets the carrying line's centre rise toward the peak, as 927 lets a part's centre follow its top.
**Check (for the form, written before any run).** In every 4/4 song: living builds above v47's; the clean reading, gate off, builds holding a leap past an octave at or under the kept 17.5 in 100; the peak planted within 5 in 100 of v47's; the chorus's height over the verse within the kept middle half; 956's ceiling and 954's floor held; builds' middle words' fit within 0.02. Read both ways (749.179).
**Hold-out (the writer's ruling, 25 November).** Song 64, "Go On Ahead" (`songs/p74/lyric64.json`; piano ballad, 4/4, 68, mezzo), locked tonight and never run: run once, only if every seen-song check holds, the ledger line first. Song 50 stays sealed for later.

**Numbering.** 749.190 is the writer's hold-out ruling above. Next finding 749.192; next fix 964.

## Carried, open

- 749.185 the loop gate with a chance (waits; song 63 reserved).
- 749.171 what the engine does inside a line it gives one bar; rhythm scaling leans low.
- 749.144 song 58's bars of rest; 749.147 a short line in a long slot; 749.148 to 749.152 the hymn items; 749.163.
- 749.165, 749.170: the region, as a change to the draw.

## Closed

- 749.177, 749.183 (749.187: no fault of the draw; 961 stays a setting).
- 749.182's first two forms (not built), 749.184 (mended; the session's second nit was its own misreading), 749.186, 749.188.
