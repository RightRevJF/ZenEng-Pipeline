# Review 20: Luthier v33 (fixes 928–930)

Branch `luthier-v8-stage1` at 454799c, merged into main at a1e6d2f. Answers the list for v33 (749.105 to 749.109); 749.109 was tried and not adopted (`studies/v33_trials/`).

## Byte for byte

- The six makers write every kept table byte for byte.
- The four song records, `spec52.run.json`, `spec52.written_chords.json`, `stage4_results.json`, and song 53's `spec53.run.json` and `spec53.parts.json` reproduce.
- `soundness.py` reproduces `soundness.json`: sound; 4, 7, 9 checks outside the middle half; one lean past the middle half, rhythm scaling low.
- `neighbour.py` reproduces `neighbour_v33.json`.

## The fixes

- **928** is right: the cap is each engine's own, with no class state left, and the hymn engine takes three.
- **929** is right and does what was asked: one test on every path, a returning line's first note moved a step at a failing join, the melisma given the cap. The run gate removes no builds (342, 647, 278 before). The pools' figures sung again rose to 0.479, 0.593, 0.640.
- **930** works where the aim is reachable (song 55, two rounds). In songs 54 and 58 the weight ends at its limits (question 1).
- **One fault in 930's wiring (749.112).** The trial builds run on the engine before `run`, and `run` never resets `self.stats`, so every count in the record covers 160, 480 and 480 more builds than the thousand. The paper's counts of first notes moved (923, 1785, 3070) are over 1,160, 1,480 and 1,480 builds.

## Question 1: the step weight ends at its limit in songs 54 and 58

The limit is a symptom. The weight acts only on lines drawn fresh, and they hold about 13 notes in 100. Lines that return carry their source's moves. Traced at four weights, 120 builds each (`studies/review20/stepfit.py`):

| | 0.3 | 1.2 | 3.0 | 6.0 |
|---|---|---|---|---|
| Song 58 steps: as sung; before melismas; fresh lines | 0.430; 0.295; 0.113 | 0.485; 0.382; 0.312 | 0.519; 0.444; 0.512 | 0.553; 0.486; 0.659 |
| Song 54 steps: the same | 0.280; 0.218; 0.105 | 0.382; 0.332; 0.383 | 0.492; 0.459; 0.634 | 0.567; 0.547; 0.787 |

At the limits the fresh lines are pushed past any kept song (kept steps 10th to 90th: 0.265 to 0.558). Song 58's fresh lines step 11 times in 100, song 54's 79. The whole song moves about a third as far.

- **Song 58: the melismas.** 13.3 sung notes in 100 are melisma second notes, each a step below by rule. That adds 13 points of steps as sung (0.295 before, 0.430 after, at 0.3). The share was drawn from the kept quartiles (16.2 syllables in 100); Bird Dog has none. At the old weight, 1.2, song 58's steps before melismas are 0.382, at its aim of 0.398. The fit is undoing steps the aimed song never sings.
- **Song 54: an aim past the kept 90th.** Could I Have This Dance steps 0.595; the kept 90th is 0.558. At 6.0 the fresh lines already step 79 times in 100, and the returning lines lag (0.504). Only a change to how lines return (749.104) can carry the song further.
- The melisma shares miss their aims in all three songs: 3.8 against 10.7 (55), 8.6 against 3.6 (54), 16.2 against 0.0 (58).

**Answer.** Don't widen the limits. Draw the melisma share from the aimed song, as the lift and the run already are. Bound the fit by the fresh lines' share, kept inside the kept 10th to 90th, and record it. Accept song 54's shortfall until 749.104 (749.110).

## Question 2: song 55's builds span 15 against an aim of 19

The tune never reaches its top. Over the builds (`stepfit.py`, `ceiling.py`):

- **Where the notes sit.** The highest note is a median 74 against tops of 78 (verse), 76 (chorus) and 80 (bridge). The lowest note sits at the floor (60). A build reaches a part's top 15 times in 100.
- **Why spread can't fix it.** The spread acts on fresh lines only, and the returning lines copy what those reached. That is why widening it from 62 to 400 left the span at 15 to 17.
- **Song 58 shows the other face.** It is narrow and presses against its top: the pick spans 7 semitones before melismas (aim 9) and sits on its top note 32 times. That is 8 notes in 100, near the kept 90th (8.7), and its title is sung on one pitch. Bird Dog sits on its top twice. A quarter of song 58's builds are past the kept 90th.
- **All three picks span less than their aims:** 14, 12 and 8 against 19, 14 and 9.
- **How kept tunes do it.** They sing their top a median 4 times (quartiles 2, 4, 13) and reach it first at 0.37 of the song (0.15, 0.72): in a verse in 62 of 160 tunes, a chorus in 64, a bridge in 14. Don't Ask Me Why reaches its top first in a verse, at 0.04, and sings it 17 times.

**Answer.** Plant the peak where the aimed song first has its top. The first fresh line of that section draws its highest stressed note at the floor plus the aimed range, so the returns carry it. Set the tops a step or two above, so the peak is reached, not pressed against. Try it outside the engine first (749.111).

## The rest

- **749.107 reread:** 5 of 52 passed over in song 55 (7 of 44). Fewer, as expected once 929 stopped removing the repeats.
- **749.109:** the trial is clear and the reason given is right. A borrowed line refitted note by note to new words seldom gives back the same bars. 749.104 comes first.
- **Variety** (749.103): 1.46 against the kept 10.5 (1.18); not met.
- **Song 58's eleventh edition:** E major, D♯3 to B3, 337 seconds. The tenth is kept in `songs/p68/out/tenth_edition_v32/`. 44 of 44 document checks pass.

## Findings

749.110 to 749.112, in `songs/p68/fixlist_v34.md`. Next finding 749.113; next fix 931.
