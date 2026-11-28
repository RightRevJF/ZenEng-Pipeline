# Folk replication: the one-page reading

27 November 2026, branch `folk-replication`. Written by `summary.py` from `result.json`, `match_check.json` and `matches.json`. The rule came first: `PREDICTION.md`.

**The question:** are plainer tunes recorded by more artists? Tested again from scratch, without TheSession and without any withdrawn figure.

## In short

- **What held:** nothing. 0 of 18 tests held.
- **What failed:** nothing either. There were too few tunes to tell, so every test is an estimate (18 of 18).
- **How sure:** not sure. If the link is small but real (a correlation of 0.15), this study had about a 21 in 100 chance of showing it.
- **The page gate without the withdrawn data:** neither supported nor ruled out. Its parts still rest on the hymn tunes and the within-artist readings alone.

## Why so thin

| | Count |
|---|---|
| Tunes read from the four collections | 12,761 |
| Found in Discogs, one tune per song | 473 |
| Test half / confirm half | 231 / 242 |
| Matches checked by eye: right / wrong / unsure | 63 / 28 / 9 |
| Wrong among the German (Essen) matches checked | 0 of 40 |
| Wrong among the Irish and Scottish matches checked | 28 of 60 |

Most old tunes aren't in Discogs under their printed names. Many Irish and Scottish titles land on a later pop song with the same name ("Hang Fire", "Christmas Eve"). A wrong match only blurs a result, but it blurs it a lot. Since the check's wrong share (28 in 100) is over 25, a miss here would count only weakly against the idea anyway.

## Which way the tests leaned (estimates, deciding nothing)

| Test | As is | Held fixed* |
|---|---|---|
| Fewer pitch classes (entropy) | as predicted (-0.06) | the other way (+0.09) |
| Next note easy to foresee | as predicted (-0.02) | the other way (+0.03) |
| Few different pitches | as predicted (-0.10) | the other way (+0.07) |
| Time on the home note | as predicted (+0.01) | the other way (-0.00) |
| Five-note scale | the other way (-0.01) | the other way (-0.02) |
| Six-note scale | as predicted (+0.04) | as predicted (+0.01) |
| Few leaps | as predicted (-0.02) | as predicted (-0.03) |
| Short figures sung again | as predicted (+0.02) | as predicted (+0.11) |
| The gate's whole plainness | as predicted (+0.06) | the other way (-0.03) |

*Held fixed: tune length, range, metre and collection. Sizes are both halves together, for scale only. "As is" is a rank correlation; "held fixed" is the change per step of the measure.

- 11 of 18 lean the predicted way. Coin flips would give about 9.
- Closest to passing: short figures sung again, held fixed, test half p 0.0038 against a bar of 0.00278; the confirm half didn't follow (p 0.54).
- Spread of pitches leans the predicted way as is, but the other way once length and range are held. So the small edge seen as is may come from those, not from the pitches themselves.
- Exact-title matches only: 10 of 18 lean the predicted way. Essen only (the clean matches, 185 tunes): 10 of 18. No test passes either way.

## What it would take

About 800 correctly matched tunes (400 a half) for an even chance at a correlation of 0.15, and more again for the matching errors. That's roughly double what was found, all of it matched right. Old printed collections plus Discogs titles won't give that. A source with recordings already tied to each tune would.

## Notes for the maintainer

- `studies/judging_checks/within_artist/cliques_versions.py` reads Discogs-VI's artist fields, stored as the text of a list, letter by letter. A track with no track artist counts `"[]"` as an artist and never falls back to the release's artists. The pack's cover counts are close but not exact. Here the lists were parsed properly (`PREDICTION.md`, addendum).
- music21 10.5's ABC reader doesn't carry a sharp or flat to the rest of its bar. This study writes it out first (`measures.py`). Anything else reading ABC through music21 has the same gap.
- Nothing under `lib/` or `tables/` was changed. Raw downloads are outside the repository.
