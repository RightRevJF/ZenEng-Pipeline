# Three trials for v48: result

25 November 2026. Checks in `PREDICTION.md` (commit 523d170, before any run). Numbers: `trial_readings.json`, `neighbour_octave_one.json`, `held_fit.json`, `title_lines.json`, `drafts.json`.

**All three fail their checks. Nothing is built. The engine of v48 writes the notes v47 wrote** (song 54 run again with every switch off: byte for byte).

## 1. One leap past an octave allowed (749.176): fails check 1

| | Song 55 | Song 54 | Song 58 |
|---|---|---|---|
| Living builds, the ban (v47) | 223 | 256 | 294 |
| Living builds, one leap allowed | 216 | 239 | 292 |
| Builds' middle words' fit, ban; one | 0.263; 0.261 | 0.218; 0.220 | 0.296; 0.310 |

Living builds were to rise in each song. They fell in each. Check 4 holds; the chosen tunes hold no such leap (check 3); a random pool pick fails the rule 5.1 times in 100 against 6.5. Check 1 decides: **the ban stands.**

**Why they fell (749.179).** The form was not run on the same engine. Before it builds, the engine fits its step and leap weights to the song on short trial runs (fix 930), and those runs pass through the gates. Change a gate and the fit lands elsewhere (song 55's leap weight 0.64 under the ban, 1.6 with one leap allowed), and every build after it is a different build. A gate cannot be tried as if it only removed builds.

**The reading that answers the question** (after the result; not a test). Each v47 record's own fitted spec run again, a thousand builds, under the three forms, so that only the gate differs (`held_fit.py`):

| Living builds | Song 55 | Song 54 | Song 58 |
|---|---|---|---|
| The ban | 223 | 256 | 294 |
| One leap allowed | 226 | 262 | 300 |
| No gate | 292 | 320 | 405 |

One leap allowed gives back 3, 6 and 6 builds of the 69, 64 and 111 the ban takes. A build that leaps past an octave nearly always does it twice or more: up, and back. So the kept-shaped form is the ban by another name, and there is nothing in it to build. If the builds are wanted back, the question is why the draw leaps past an octave twice as often as kept songs do, which is a question about the draw (the move weights, the register between lines), not the gate.

**Against what I expected.** I expected check 1 to hold and doubted check 2. Wrong about 1, and for a reason I had not seen: I thought of the form as a superset of the ban's builds.

## 2. The title line (749.177): the reading passes its rule; the gate fails its cost

**The kept reading.** 77 kept songs have a title line whose every word the lexicon holds; 387 lines (355 more left out for a word it does not hold).

| The title line's longest note falls on | Lines in 100 |
|---|---|
| a stressed syllable | 73 |
| a weak syllable, the line's last | 18 |
| a weak syllable inside the last word | 0 |
| a weak syllable before the last word | 9 |

Under 10 in 100, so the gate was tried. Two things the table also says: kept songs hold a weak last syllable long about one title line in six (961 as first written forbade that); and 18 kept songs in 100 have at least one title line with its longest note on a weak syllable before the last word. It is uncommon, not unknown.

**The gate** (a build passed over if a title line's longest note is on a weak syllable before the line's last word):

| | Song 54 | Song 49 | Song 62 | Song 55 | Song 58 |
|---|---|---|---|---|---|
| Passed over, of 100 builds that reached it and would live | 9.7 | 26.7 | 30.6 | 15.3 | 0 |
| Living builds (v47) | 243 (256) | 203 (287) | 77 | 216 (223) | 294 (294) |
| Chosen tune's title lines: stressed; weak last word; weak before | 2; 1; 0 | 2; 3; 0 | 1; 0; 0 | 7; 0; 0 | 6; 0; 0 |

Check 1 holds (song 62). Check 2 fails: 9.7 and 26.7 against 5. **Not built.** 961 stays the setting it was. The figure is an upper reading (a build passed over here might have died at a later gate), but 27 is not near 5.

What it shows about the engine: in song 49 a quarter of otherwise living builds put a title line's longest note on a weak word inside the line, where kept songs do it in 9 title lines of 100. The chosen tunes do not (the pick avoids it: none of 19 title lines here). So this is a fault of the draw that the judging already mostly screens. Song 49's v47 record has one such line of five; that is the size of the problem in what the writer hears.

**Against what I expected.** The kept share: right (5 to 10). The cost: wrong again, the second time for this gate.

## 3. The gentler loop gate (749.178): fails all three; song 63 not run

Major, a thousand drafted sections a kind:

| | Kept | No gate | 960 as built (median) | Gentle (over the 75th redrawn) |
|---|---|---|---|---|
| Verses at or under the kept median, in 100 | 50 | 45 | 99 | **65** (asked: 45 to 60) |
| Verses over the kept 75th, in 100 | 25 | 34 | 0.2 | 0.1 |
| Verses that are plain loops, in 100 | 30 | 32 | 17 | **21** (asked: 25 to 35) |
| Stage 4, verse bigrams (distance from held-out kept) | | 0.246 | 0.274 | **0.268** (+0.022; asked: +0.02 at most) |
| Stage 4, bridge last chord | | 0.310 | 0.397 | **0.345** (+0.035) |

Nearer than the median gate on every line, and outside every bar. The reason is in the second row: the unpatched writer puts 34 verses in 100 over the kept 75th, and the gate redraws every one of them until it is under, so none is left where kept songs keep a quarter. Any gate that redraws to a line empties the far side of the line. A form that would not: redraw a verse over the 75th with a chance (about one time in four), so the top is thinned and not cut off. That is a new form and needs its own rule first.

By the rule the seen-song checks failed, so **song 63 was not run** and is still sealed (the ledger says so). 960 stays the setting it was, in the median form.

**Against what I expected.** Check 1 to hold at 50 to 55: wrong (65). Check 2 the doubt: it failed. Check 3 even: failed narrowly.

## What v48 is

- The engine's notes: v47's. No rerun of any song is needed.
- New since v47 on the words' side: `lib/luthier/lyric_people.py` (advice), the line test (`studies/lyric_lines`), the check of Design B (`studies/covers_lines/CHECK_maintainer.md`).
- The three trial forms are in the code behind switches that are off (`LUTHIER_OCTAVE`, `LUTHIER_TITLE`, `LUTHIER_LOOP`), marked as trials that failed.

## Next, as I see it

1. **749.179 first.** Any trial of a gate should be read both ways from now on: the whole engine (fits and all), and the same fitted spec with only the gate changed. The second is the clean reading and costs minutes.
2. **The draw leaps too far, and holds weak title words too long.** Both trials found a fault of the draw behind a gate that screens it. The draw is where rhythm scaling's lean lives too. 749.171 (inside a one-bar line) belongs with them.
3. The loop gate with a chance, rule first, if the looping chords are still wanted before the covers question settles.
