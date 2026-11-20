# Where the repeating really goes wrong: results

Done without the songwriting session's list, at the writer's word. Each trial's rule was written before it was run. Song 59 is the hold-out: read, never fitted to.

## 1. The bar fit where the words allow (studies/bar_fit, PREDICTION3.md). Not built.

Keep a returning line's bars only where the new words sit as well as under the engine's refit.

- Strict form: taken in 40 to 50 lines in 100, words held, **bars did not rise** (rhythm sung again -0.016, -0.005, -0.003). Where the bar fit seats the words as well, it is nearly the same fit.
- One note's worth of give: taken in 97 in 100, bars rose, **the words' fit fell to 0.05 to 0.10.**

On the tune's side the bars and the words trade, and there is no free part of the trade.

## 2. Is it the lyric? (`match.py`) No.

I had inferred that kept songs keep both because later verses are written to the first verse's stresses. Measured, that is wrong.

| Verse 1 against later verses, bar by bar | Kept songs (25th, middle, 75th) | Songs 55, 54, 58, 59 |
|---|---|---|
| Bars with the same number of syllables | 0.38, 0.50, 0.68 | 0.52, 0.61, 0.62, 0.67 |
| Bars sung on the same rhythm | 0.13, 0.29, 0.57 | 0.52, 0.61, 0.62, 0.63 |

Luthier's later verses match their first verses as well as kept songs' do, and on rhythm better than seven kept songs in ten. The lyrics are not the fault.

## 3. Do the songs repeat too little at all? (`near.py`) No.

Bars whose rhythm has been sung before: kept quartiles 0.45, 0.59, 0.69; songs 55, 54, 58, 59 at 0.42, 0.56, 0.63, 0.48. By how far back the rhythm comes from, the songs stand in the kept middle half on nearly every row.

**So there was never a general fault of repetition.** The shortfall reported since v32 is against each song's own aimed kept song. Songs 54 and 58 aim at kept songs that repeat far more than most; the engine gave every song the same amount of repeating whatever it aimed at. This is the "too like the middle" fault (749.103) seen from one side: where the aim does not reach, every song lands at the kept middle.

## 4. The borrows fitted to the aimed song (PREDICTION.md, PREDICTION2.md). Passed its trial; built in; withdrawn.

One dial already in the engine moves these readings a long way (`reach.py`): how many fresh lines sing an earlier line of their section again, or take its rhythm. It is 0.8 and 0 for every song. Fitted to the aim instead:

| Second trial, new draws | Song 55 | Song 54 | Song 58 | Song 59 (hold-out) |
|---|---|---|---|---|
| Setting chosen (figure, rhythm) | 0.5, 0.5 | 1, 0 | 1, 0 | 0, 0 |
| Gap to the aim, kept widths: before, after | 0.88, 0.82 | 0.79, 0.54 | 1.72, 1.25 | 0.54, 0.28 |
| The words' fit, change | +0.003 | +0.012 | -0.021 | +0.055 |
| Builds passing the gates | 1.09 | 0.94 | 0.86 | 1.35 |

- First trial (`trial1.json`): every gap shrank and the hold-out's prediction held, but song 55's words' fit fell 0.046 (0.03 allowed). Not built on that.
- Amended so the fit may not buy bars with the words; second trial (`trial2.json`) on new draws: all checks hold, and the hold-out's prediction holds.
- **Built into the engine as 943, and withdrawn.** With it (`in_engine_943.json`, `neighbour_with_943.json`) the picks stayed sound, but a pick from the pools failed the soundness rule 10.2 times in 100 by the neighbour choice (90% range 4.0 to 18.5; v37: 1.5, 0.0 to 3.5) and 10.3 by a random pool pick (5.0 to 16.8; v37: 3.2, 1.2 to 6.1). Both under the standard's bar of ninety passes, both clear of v37's ranges.
- **Why.** More borrowing moves the bars toward the aim and rhythm scaling away. Nearly all the failures are one check: all three picks under the kept 10th on rhythm scaling (9.9 in 100; 1.8 before). The kept songs that repeat most have high rhythm scaling (Bird Dog 0.704); Luthier's songs, made to repeat by borrowing whole lines, get lower.
- `BORROW_FIT = None` in `lib/luthier/song_from_lyric.py`: the code is kept, off. With it off every record is v37's, byte for byte.

## What is left standing

1. There is no general fault of repetition, and the lyrics are not at fault.
2. The one fault under 749.104, 749.109 and 749.103 is that the aim reaches pitch moves and not rhythm.
3. The engine's way of repeating (borrowing whole lines) is not the kept songs' way: theirs keeps rhythm scaling high. That is the next thing to study, outside the engine, rule first.
