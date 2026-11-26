# The melody under a chord that stays: result

25 November 2026. Rule in `PREDICTION.md` (committed before the runs). Numbers: `kept.json`, `builds_lyricNN.json`, `switches_lyricNN.json`; and three descriptions made after the result (`pull_level.json`, `by_how.json`, and the kept figure by song, below). Nothing in the engine is changed.

## A. Kept melodies do not loosen as a chord holds; the pull's steadiness is not the fault

The share of notes on a beat that are tones of the chord, by how long the chord has held:

| | Under 1 bar | 1 to 2 | 2 to 4 | 4 or more |
|---|---|---|---|---|
| Kept songs | 0.636 | 0.603 | 0.656 | 0.643 |
| Song 50's builds | 0.944 | 0.937 | 0.932 | |
| Song 58's builds | 0.912 | 0.953 | 0.892 | 0.923 |
| Song 49's builds | 0.909 | 0.928 | 0.939 | 0.934 |
| Song 55's builds | 0.869 | 0.916 | 0.879 | 0.966 |

Kept songs do not fall as the chord holds (the rule asked a fall of 0.05). **By the rule, nothing is named in part A.** I expected a small fall and there is none.

But the table says something I had not asked. **Kept melodies put a chord tone on the beat 64 times in 100. The engine puts one there 88 to 95 times in 100.** By song, the kept figure runs 0.44, 0.53, 0.64, 0.73, 0.83 at the 10th, 25th, 50th, 75th and 90th. Every one of the engine's songs is past the kept 90th. Off the beat it is the other way: kept 0.56, the engine 0.45 to 0.51.

Under a chord held four bars or more, the share of the stretch's notes on its commonest pitch: kept 0.36, 0.43, 0.52 at the quartiles; the builds 0.40 to 0.43, 0.53 to 0.55, 0.65.

## B. The road is found: three things, together

Living builds whose verses are over the ceiling, in 100 (the rule: 25 or under in two songs of three):

| Switch | Song 50 | Song 58 | Song 49 | |
|---|---|---|---|---|
| As it is | 65 | 56 | 56 | |
| 8. The figure memory off | 59 | 46 | 50 | |
| 9. Memory, the pull, the clash rule off | 25.3 | 35 | 24 | no |
| **10. Verse lines drawn fresh, the pull, the clash rule off** | **19** | **14** | **13** | **found** |
| 11. All four | 11 | 6 | 9 | |
| (song 55's verse chords, from before) | 20 | 17 | 23 | |

The least set that does it is 10: lines sung again, the pull, and the clash rule. The figure memory adds a little and is not needed.

## Why lines sung again are in it (749.198)

Reading the code for what a line sung again does to its notes: when an earlier line's tune is fitted to new words (fix 712), **every note that falls on a beat and is not a chord tone is moved to the nearest chord tone.** Every one. Then fresh lines are drawn with a chord tone on the beat favoured 2.6 to 0.3, and the clash rule (833) forbids long notes a semitone from a chord tone.

On-beat notes that are chord tones, by how the line was made: fresh lines 0.92 to 0.94; lines sung again 0.96 to 0.97. With the pull taken away and the clash rule off, the whole song still stands at 0.81 to 0.82, because the lines sung again are untouched by those.

So the engine's melodies are bound to the chord on the beat far more tightly than kept melodies are, by three rules that each make sure of it. Under six chords that binding moves the tune about. Under two chords that share a tone, it holds the tune on that tone. The one-pitch verses are a symptom. The thing itself is that the engine has never been checked against kept songs for how often the tune is on the chord, and it is past nine kept songs in ten.

(This is known of kept music: writers on rock and pop call it the melody's independence of the harmony. The tune keeps to the scale and the chords move under it.)

## What I would do, and why I stop here to ask

This is larger than the question I was sent with. Mending it changes how every tune sits on its chords, in every song, and what the writer hears: tunes less tied to each chord on the beat. By the kept songs that is right. But the three rules were put there on purpose (650, 712, 833), 833 after a fault heard by ear, and I do not want to loosen them on a figure alone without the writer and the session knowing what is being loosened.

What I would try, marks first, both ways, on the seen songs and then a sealed one:
1. A new soundness check: sung notes on a beat that are chord tones, against the kept quartiles (the record already reads this figure; it has no kept line beside it).
2. In lines sung again, move a beat's note to a chord tone only where the clash rule would (a long note a semitone from one), not every time.
3. The pull on the beat (2.6 to 0.3) set by a kept table, so that fresh lines land on chord tones about as often as kept melodies (the kept middle, 0.64), in place of a number set by hand.
The clash rule itself (833) I would leave: it was asked for by ear and kept songs' long notes do favour the chord (0.68).

The marks would be: the new check inside the kept 10th to 90th in every song; verses over the pitch ceiling in songs 50, 58 and 49 at or under 30 in 100; living builds, words' fit, floors and soundness as for 964; and song 50's pool at 10 or more.
