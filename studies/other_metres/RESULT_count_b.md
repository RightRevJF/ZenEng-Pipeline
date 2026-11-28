# Count (b): 840 and first-beat onsets on song 61's words (27 Nov 2026). A count; nothing predicted, nothing built.

20:56 ET. count_b.py, 400 builds from each record's fitted spec (749.241's trial). Figures printed from count_b_61.json and count_b_52.json by the command that wrote this file.

## Which gate takes builds
- Song 61's words (400 made): {"838": 69, "living": 262, "840": 67, "731": 2}.
- Song 52 (400 made): {"838": 78, "living": 322}.

## The title lines
Song 61's words:

| Title line | Syllables | Sung bars | How made | Stressed on a beat, builds dying on 840 | builds that do not |
|---|---|---|---|---|---|
| Chorus 1:7 | 7 (3 stressed) | 4 | {"fresh": 400} | 0.333 | 1.0 |
| Last Chorus:7 | 6 (2 stressed) | 4 | {"again": 372, "fresh": 28} | 0.5 | 1.0 |

Song 52:

| Title line | Syllables | Sung bars | How made | Stressed on a beat, builds dying on 840 | builds that do not |
|---|---|---|---|---|---|
| Chorus 1:2 | 7 (5 stressed) | 4 | {"fresh": 400} | None | 1.0 |
| Chorus 2:2 | 7 (5 stressed) | 4 | {"copy": 400} | None | 1.0 |
| Bridge:2 | 10 (6 stressed) | 4 | {"fresh": 400} | None | 1.0 |

## First-beat onsets by section (median), and syllables a sung bar
- Song 61's words: first-beat onsets {"Bridge": 0.176, "Chorus 1": 0.207, "Last Chorus": 0.241, "Verse 1": 0.2, "Verse 2": 0.231, "Verse 3": 0.225}; syllables a bar {"Verse 1": 4.58, "Chorus 1": 3.05, "Verse 2": 4.33, "Bridge": 3.64, "Verse 3": 4.0, "Last Chorus": 2.84}.
- Song 52: first-beat onsets {"Bridge": 0.238, "Chorus 1": 0.245, "Chorus 2": 0.245, "Last Chorus": 0.241, "Verse 1": 0.24, "Verse 2": 0.244, "Verse 3": 0.234, "Verse 4": 0.244}; syllables a bar {"Verse 1": 4.17, "Chorus 1": 3.27, "Verse 2": 3.75, "Chorus 2": 3.27, "Verse 3": 3.92, "Bridge": 3.23, "Verse 4": 3.75, "Last Chorus": 3.41}.

## What it says, and what it does not
- 840's deaths on song 61's words are builds where the first chorus's title line, drawn fresh over four bars, puts a third of its stresses on a beat (the median). In the builds that do not die on 840 the median is all of them. The last chorus's title line is that line sung again, so it follows.
- The draw is letting poor windows through for that line. In these trials the stress score of 749.231 is **not on** for 6/8 (stress scored by the table: False): the draw weighs a window's count and the old stress score, not where kept songs sing a stressed syllable.
- First-beat onsets on song 61's words are under song 52's in every section but the last chorus, and lowest in the bridge and the first verse. More notes a bar means a smaller share of them can be on the bar's first beat: a bar has one first beat, so at Verse 1's 4.58 syllables a bar the most is 1 in 4.58, or 0.218. **So in the dense verses the mark of 0.211 sits just under the ceiling.** That is arithmetic about the lyric and the plan, not a fault of the draw.
- Not counted here: whether 749.231's stress score would stop the title line's poor windows. That is a trial, and its rule comes first.
