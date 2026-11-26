# The draw sits on its centre: result

26 November 2026. Rules in `PREDICTION.md` (the first committed before any run; the second written while the first ran, after its first figures, and before its own run). Numbers: `kept.json`, `builds.json`, `lines_kept.json`, `lines_builds.json`. Nothing in the engine is changed.

**No single weight is named, and the lines' heights are not named by the rule either. What the readings do show is the size and shape of the gap: the engine's verses are narrow in two ways at once, about equally.**

## A. A verse's notes over its pitches

| | Kept verses (quartiles) | The builds, v50 (middles; songs 55, 54, 58, 49, 50, 59) | With the tie at kept odds |
|---|---|---|---|
| Share on the commonest pitch | 0.26, 0.31, 0.36 | 0.34, 0.35, 0.46, 0.47, 0.50, 0.35 | 0.38, 0.41, 0.43, 0.44, 0.46, 0.40 |
| Spread about the mean, semitones | 2.5, 3.2, 3.8 | 2.5, 2.5, 2.2, 2.3, 2.1, 2.8 | 2.2, 2.2, 2.0, 2.1, 2.2, 2.4 |
| Different pitches | 7, 9, 11 | 8, 8, 6, 7, 6, 8 | |
| Span, semitones | 10, 14, 17 | | |

Kept verses: 0.54 of the notes on the two commonest pitches and 0.70 on the three. The commonest pitch sits in the middle third of the span 61 times in 100, so sitting mid-span is kept-like; it is the amount that is not.

## B. The weights, one at a time (the tie at kept odds)

The middle verse's share on its commonest pitch (0.34 or under asked, in four songs of six):

| | 55 | 54 | 58 | 49 | 50 | 59 |
|---|---|---|---|---|---|---|
| The tie at kept odds | 0.38 | 0.41 | 0.43 | 0.44 | 0.46 | 0.40 |
| 1. The register's pull halved | 0.37 | 0.40 | 0.43 | 0.40 | 0.41 | 0.37 |
| 2. The degrees levelled | 0.38 | 0.37 | 0.42 | 0.38 | 0.42 | 0.36 |
| 3. The figure memory off | 0.38 | 0.37 | 0.40 | 0.38 | 0.42 | 0.37 |
| 4. The pull halved and the degrees levelled | 0.37 | 0.35 | 0.39 | 0.37 | 0.39 | 0.36 |

None reaches 0.34 in any song. Each helps by 0.02 to 0.06. **Nothing is named.** I expected the register's pull to be named; halving it widens the verse's spread by about a tenth of a semitone.

## The second reading: between the lines and within them

A verse's spread split into the spread of its lines' middles and the spread of notes about their own line:

| | Kept (quartiles) | 55 | 54 | 58 | 49 | 50 | 59 |
|---|---|---|---|---|---|---|---|
| Between lines | 0.86, 1.54, 2.38 | 1.20 | 0.94 | 0.94 | 0.74 | 0.70 | 1.15 |
| Within lines | 1.91, 2.34, 2.76 | 2.08 | 2.06 | 1.95 | 2.02 | 1.91 | 2.32 |
| From a verse's lowest line to its highest, by their middles | 2.6, 4.6, 7.1 | 3.7 | 3.0 | 2.9 | 2.2 | 2.2 | 3.7 |

The rule asked the builds' between-line spread under the kept 25th in four songs of six. It is in two (songs 49 and 50); songs 54 and 58 are just over it. **By the rule the lines' heights are not named.**

But the table is plain enough about the lean, and I report it as a lean: in all six songs the lines of a verse sit closer together than in the middle kept verse (0.7 to 1.2 semitones against 1.5), and in all six the notes within a line are a little closer too (1.9 to 2.3 against 2.3). In song 50, a kept verse's variance is about 8.6 square semitones, 2.4 of it between lines; the engine's is about 4.1, 0.5 between lines. The shortfall is half from the lines all sitting at one height and half from each line being narrow.

## What this says about the chain

Five readings in two days have each looked for the one thing that holds the tune still, and each has found a thing that holds it a little: the chords' common tone, the pull to chord tones, the clash rule, lines sung again, the register's pull, the degrees, the memory. None is the cause, because there is no single cause. **The draw is built from many pulls toward the likely note, and each one narrows the tune a little; together they give verses with about half the kept variance.** The kept figures were each matched one at a time (intervals, degrees, repeats, chord tones on the beat), and matching each margin does not match what they make together.

That is why the octave bin could be mended with one fix and this cannot: that was one table read wrongly; this is the sum of a dozen rights.

## What I would do

Not another switch. A different kind of mend, which the engine already uses elsewhere: **fit the spread to the song, as fix 930 fits the step and leap weights.** Two things to set, each against a kept figure, on short trial runs before the build:
1. **Each line of a part given its own centre**, drawn about the part's centre with the kept spread between lines (the kept middle 1.5 semitones), so a verse's lines sit at different heights as kept verses' do.
2. **The register's width fitted** until the builds' spread within lines meets the kept middle (2.3).

Then the marks: a verse's share on its commonest pitch at the kept middle half; verses over the ceiling in songs 50, 58, 49 at or under 30 in 100; the tie to the chord (749.198) tried with it, since it can only be loosened once the tune moves by itself; and everything 964 was held to. It is a larger change than any since 944, and it should go to the session and the writer as a design before any of it is run.
