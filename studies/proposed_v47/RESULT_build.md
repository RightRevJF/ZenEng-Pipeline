# Luthier v47, the kept patches built: result

25 November 2026. Checks in `PREDICTION_build.md`, written before the build; one amendment written before the second run. A thousand builds a song (`build_readings.json`, `studies/soundness/neighbour_v47.json`).

**Built: the octave gate (959) and varied returns (962) on; sections that loop less (960), the title gate (961) and blue notes off (963) as settings a lyric asks for. The region gate is not built.**

## The first build failed, and why

With 959, 961 and 962 all on, song 54's pool fell to 7 builds (the floor was 10) and a random pool pick failed the soundness rule 6.1 times in 100. The title gate was the cause. On the four songs it was tested on it passed over 2 to 53 tries in a thousand; on song 54 it passed over 194 and on song 49, 213, leaving 55 and 83 living builds where there had been 309 and 344. Song 49's title line is "The world is asking"; its last syllable is weak, a line's last note is usually its longest, and song 49's own intake asked for that syllable to be held. So the gate, right for song 62's "remembered", forbids a feminine ending in every title. It is now a setting (`"title_stress": true`). Before it could be a default, the kept songs must be read for where a title line's longest note falls.

## The second build

| Check | Result |
|---|---|
| 1. No chosen tune holds a leap past an octave in a line | Holds: none in songs 55, 54, 58, 60, 59, 49. |
| 1. Returning sections vary | Second choruses vary: 1 note lifted in song 58, 2 in song 60, 4 in song 59, 4 in song 49. **Not the tags:** songs 55's and 54's two-line tags still return note for note (no held note there could be lifted inside the rules). A tag is a repeat by design; I leave it. |
| 2. The three-song soundness rule | Holds: sound; one lean past the quartiles (rhythm scaling, low); 12 checks outside the middle half, as v46. |
| 3. The pool standard; pools of 10 | Holds, nearer the bar: pools 24, 23, 22 (v46: 39, 25, 39). The neighbour choice fails the rule 1.3 times in 100 (range 0.1 to 2.8); a random pool pick **6.5** (1.4 to 11.2), where v46's was 2.2 (0.1 to 5.4). Inside the bar of 10; the ranges overlap. |
| 4. Builds' middle words' fit within 0.02 of v46 | Holds: 0.263, 0.218, 0.296 against 0.265, 0.221, 0.306. |
| 5. Floor and ceiling | Hold. |
| 6. Songs 52 and 53 | Song 53 byte for byte. **Song 52 changes by one note:** its second chorus returned whole, and 962 lifts "wall" from G4 to B4 in its fifth line. Reported, as the check said. |
| 7. Hold-outs | Song 59 read: no leap; its two returning choruses vary (4 notes). Songs 50 and 63 not run. |

Builds that live: 223, 256, 294 (songs 55, 54, 58; v46: 342, 309, 419). The octave gate passes over 69, 66 and 111 tries in a thousand.

Chosen tunes (range; words' fit): song 55, 16; 0.383. Song 54, 17; 0.315. Song 58, 17; 0.344. Song 60, 19; 0.348. Song 59, 19; 0.363. Song 49, 17; 0.246.

**The settings**, read on seen songs: `"blue_notes": false` on song 61 leaves no lowered third (7 before). `"chords": "loop_less"` on song 61 gives a verse at 0.29 (0.55 before; kept median 0.333). `"title_stress": true` on song 62 puts its title line's longest note on a stressed syllable (it was not, with the gate off).

## Against what I expected

I expected checks 1, 2, 5 and 6 to hold and check 3's floor of 10 to be at risk in song 54. It was, but from the title gate, which I had expected to cost about 3 builds in 100 everywhere. Four songs were too few to see that its cost depends on the title's last syllable.

## What stands open

- The octave gate costs about 3 living builds in 10 and leaves the pools nearer the bar. If the next windows need the builds back, the kept-shaped form (at most one such leap a song, the kept 90th) is the place to look.
- Rhythm scaling still leans low, and nothing here touches it.
- 960 is a setting only. Song 63 is still sealed.
