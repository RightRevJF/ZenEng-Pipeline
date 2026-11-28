# Folk replication: plainer tunes, more artists? The rule, written before any outcome is joined

27 November 2026, branch `folk-replication`. Written and committed before any Discogs outcome is joined to any tune.
Nothing here is taken from the withdrawn studies (judging research run 10, `studies/session_lab`, `studies/gates_strengthened`,
`studies/transfer`, `studies/next_tests` t4) except how pitch-class entropy was defined, read from run 10's code. No TheSession data is used.

## Tunes (notes side, done before this file: `measures.py` -> `measures.json.gz`)

The four printed collections inside music21 10.5.2: O'Neill's 1850 (`oneills1850`), Ryan's Mammoth (`ryansMammoth`), Aird's Airs (`airdsAirs`), the Essen folk-song collection (`essenFolksong`). Every tune with a title and two notes or more. Pitches are the written notes (repeats not expanded; grace notes left out; ties joined; a chord read as its top note). An accidental carries to the end of its bar, as ABC says (music21 does not do this; `carry_accidentals` writes it out first). Each note's length is its time to the next note, in quarter notes.

## Outcome

The number of different performing-artist sets that have recorded the tune: the Discogs-VI 20240701 clique (`main.zip`, Zenodo 13983028) the tune's title is matched to, counted as `studies/judging_checks/within_artist/cliques_versions.py` counts `n_artist_sets` (each track's artist names, or else the release's, normalised and sorted, as one set). Only matched tunes are tested. Raw downloads stay outside the repository (`/home/claude/dl/discogsvi`).

## The match (fixed here, before it is run)

- **Key.** Lower case; ä ö ü ß written ae oe ue ss; other accents dropped; `&` as "and"; everything but a to z and 0 to 9 removed. The same on both sides.
- **The tune's titles:** every `T:` line. Before keying: text in brackets dropped, anything after ` -- ` dropped (Ryan's "Acacia -- Reel"), a final full stop dropped.
- **Exact key:** the key of that title. **Loose key:** the same after taking off a leading "the", "a" or "an" and any trailing tune-type words (reel, jig, double jig, single jig, slip jig, hop jig, hornpipe, strathspey, march, quick step, quickstep, air, set dance, polka, waltz, clog, schottische, slide, highland fling, fling, long dance, lament, song).
- **Two words or more:** a title is used only if it has two words or more once trailing tune-type words are taken off (articles count). One-word titles collide too easily.
- **Discogs side:** each clique's keys are the exact and loose keys of every distinct track title in it (`track_title_cleaned`, else `track_title`).
- **Order:** the cliques sharing any exact key with any usable title of the tune. One: matched (exact). More than one: the tie-break. None: the same with loose keys (loose). Still none: unmatched.
- **Tie-break:** of the candidate cliques, the ones with a traditional credit (any writer name matching `trad`, `traditional`, `anon`, `public domain` or `unknown`, as a word start, any case). Exactly one: matched, flagged as tie-broken. Otherwise unmatched.
- **One clique, several tunes:** the first tune is kept, in the order O'Neill's, Ryan's, Aird's, Essen, then file name, then X number. The others are dropped.
- **Exact-title matches** (for the check below) are those made at the exact step, tie-broken or not.

## Split

Each kept tune's half is `int(md5(exact key of its first usable title), 16) % 2`: 0 is the **test half**, 1 the **confirm half**.

## The tests (each its own test) and the predicted direction

Plain is the way `PLAIN` in `lib/luthier/page_gate.py` states; plainer is predicted to go with more artists.

| # | Measure | From | Predicted with more artists |
|---|---|---|---|
| 1 | Pitch-class entropy (bits, time-weighted) | `measures.pc_entropy` | lower |
| 2 | A next note easy to foresee (`surprise`, bits per interval under the gate's own kept table) | `page_gate.read` | lower |
| 3 | Few different pitches (`different_pitches`) | `page_gate.read` | lower |
| 4 | Time on the home note (`time_on_tonic`) | `page_gate.read` | higher |
| 5 | Five-note scale (`five_note_share`) | `page_gate.read` | higher |
| 6 | Six-note scale (`six_note_share`) | `page_gate.read` | higher |
| 7 | Few leaps (`leaps`) | `page_gate.read` | lower |
| 8 | Short figures sung again (`repeated_figures`) | `page_gate.read` | higher |
| 9 | The gate's whole plainness (`plainness`) | `page_gate.read` | higher |

Each measure in two forms:
- **A, nothing held:** Spearman's rank correlation of the measure with the number of artist sets.
- **B, held fixed:** least squares of log(artist sets) on the measure (standardised), log of the tune's number of notes, its range in semitones, its metre (one group per written metre class) and its collection; robust (HC3) standard error. In each half, a metre class with fewer than 5 tunes is joined to "other", and a collection with fewer than 5 tunes is joined to O'Neill's. This is question 3.

**K = 18 tests** (9 measures, two forms). **The pass level is .05 / 18 = .00278, one-sided** in the predicted direction.

## Pass mark (never rewritten after a result)

A test **holds** when all three are true:
1. its power (below) is one half or more;
2. on the test half, its one-sided p in the predicted direction is under .00278;
3. on the confirm half, the same form has the predicted sign and a one-sided p under .05.

A test with power one half or more that does not hold is **missed**; if its test-half p in the *other* direction is under .00278 it is recorded as **missed, the other way**. A test with power under one half is an **estimate**: its sign and size are reported, it passes nothing and kills nothing.

## Power (printed before the outcome is joined)

The size used: a correlation (form A) or a partial correlation (form B) of **0.15** in the predicted direction, a small effect by convention, chosen without any figure from the withdrawn studies. The test half's power at .00278 one-sided (Fisher z; for Spearman the standard error is sqrt(1.06 / (n − 3)); for form B, 1 / sqrt(n − k − 3), k the controls' columns), times the confirm half's power at .05. The smallest correlation with power one half is printed beside it. The number of matched tunes, by half, collection and match step, is printed in the same command, before any count of artists is read.

## The match check (printed before the outcome is joined)

A random hundred matched tunes (numpy seed 20261127). For each I see the tune's titles, collection and metre, and the clique's titles (up to four), writers (up to four) and three performing artists, alphabetical; never the number of artists. I mark each right (the same tune), wrong (another piece) or unsure, in `match_check.json`, before the join. The error rate is wrong / 100, with (wrong + unsure) / 100 as its upper bound.

## Reported, deciding nothing

- **Exact-title matches only:** all 18 tests again on those tunes, both halves, the same forms.
- Both halves together: the size of each, for scale only.
- If the match check's upper error is over 25 in 100, the summary says that a miss here is weak evidence against the idea, since a wrong match only blurs.

## What a result means

A test that holds supports that part of the gate on tunes and outcomes we may use. A miss with power is a miss and is recorded as one. An estimate is neither. None of this changes the engine: this is a study.
