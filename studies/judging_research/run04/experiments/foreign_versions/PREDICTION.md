# Is the loop effect on "versioned at all" real uptake by other artists? Frozen after seeing results, before this outcome is built

Run 04, 24 November 2026. This rule comes from `run04/first_principles.md` section 5 (the first-principles reviewer). It is written **after seeing the five results of tonight**, in particular move_extensive H1: chord repetition +1.19 pp per SD of P(in Discogs-VI), p .018, which was a kill of the predicted negative sign. **Label: after seeing results.** A pass is a lead that needs fresh songs, never a finding. It is the sixth test of tonight. Its outcome (the split of each matched song's versions into own and foreign performer sets) has not been built or looked at by anyone before this file was committed. Run 04 does not touch the McGill hold-out.

## Question
A Discogs-VI group needs only two distinct performer sets. "Artist" on one release and "Artist, Guest" on another count as two (card 2; `cliques_versions.py`). So a song can be "in Discogs-VI" without any other artist ever recording it. Two stories fit tonight's +1.19:
- **Two-part story.** Loops are taken up by someone else more often, but, once taken up, by fewer distinct artists (the replicated −0.042 within matched songs).
- **Artefact story.** Loops (dance and pop singles) collect the original artist's own credit variants, remixes with guests and so on. The plus sign lives in those, not in other artists.

## Code
Reuse `run04/experiments/move_extensive/test.py`, changing only the outcome. Rows, columns, model, controls, halves and conditional logit stay exactly the same:
- **Rows:** the same 9,588 songs (artists with 2+ songs).
- **Columns:** z `ch_rep` and z `ch_ic_mean` (n_mel-weighted song values), plus these controls:
  - the chord-count bins [5, 7, 9, 11, 13, 16, 20, 25, 32]
  - clips-per-song dummies (2, 3, 4+)
  - ln beats
  - title flags (word-count dummies 1 to 4, parentheses, shared title)
- **Model:** artist demeaning; LPM with y in points (0 or 100); CR1 SE clustered by artist; normal two-sided p.
- **Halves:** md5 of the artist slug.
- **Conditional logit:** grouped by artist, statsmodels `ConditionalLogit` or the exact likelihood. Print the artists and songs dropped, and whether it converged (judge by the score if the flag is not returned).

## Outcome
For a song whose `vid` is a key of `hooktheory_covers_discogs.json` (origin/main):
- **Its sets:** the first element (the list of performing artists) of every entry of `discogs_versions_matched.json["cliques"][clique]["versions"]`, where `clique` is the song's `clique` field.
- **Artist key:** a = `re.sub(r"[^a-z0-9]", "", slug.lower().replace("&", "and"))` on the first clip's `artist` slug, the matching rule of `covers_match_discogs.py`, with no unquoting. Each name n in a set is normalised the same way, norm(n) = `re.sub(r"[^a-z0-9]", "", n.lower().replace("&", "and"))`.
- **Own set:** any set in which some name normalises to a. **O** = the set of normalised names appearing in any own set.
- **Foreign set:** a non-empty set none of whose normalised names is in O.
- **y_foreign** = 100 if the song has at least one foreign set, else 0. It is 0 for every song not in Discogs-VI.
- **y_self** = y − y_foreign, where y is move_extensive's outcome (100 if in Discogs-VI).
- **Drops:** a matched song with no own set, or whose clique is missing from the versions file, is printed and dropped from every model below. Its rows are dropped for y, y_foreign and y_self alike, so the split stays exact. If more than 25 songs are dropped, stop and record "not run".
- **Print order:** the counts of y_foreign = 100 and y_self = 100, and the dropped count, then the SE and power, all before any β.

## Prediction
β(`ch_rep`) on y_foreign = **+0.9 points per SD** (two-part story). This is most of +1.19, shrunk for a first look. The artefact story predicts under +0.3, with the rest on y_self.

## Rules
Tonight now counts six hypotheses, so this test needs **p < .05/6 = .0083, two-sided (z 2.638)**. The five earlier tests were all killed or below .01 regardless, so no earlier verdict changes under the stricter threshold.
- **Pass (a lead needing fresh songs):** β > 0, p < .0083, β > 0 in both artist halves, and the conditional-logit coefficient > 0 with convergence. The artefact story dies.
- **Kill:** β < +0.3. The sign was the original artist's own credit variants. Drop "loops get versioned more", and later tests on being versioned use y_foreign.
- **Unsettled:** anything else.

## Power
Expected SE ≤ 0.50 points (move_extensive's realised clustered SE for `ch_rep` was 0.50 on y; y_foreign has lower variance or the same). Power at +0.9 and p < .0083 is about 0.20. The kill line is what decides: it fires about 12% of the time if +0.9 is true, and 73% if the true effect is zero. The script prints its own SE and power before β.

## Reported, deciding nothing
- β on y_self, with β_foreign + β_self = β(y) checked to 1e−9 on the same rows.
- Foreign defined as "a not in the set" (looser).
- Sets whose names contain "karaoke" or "tribute" removed before deciding y_foreign.
- `ch_ic_mean` on y_foreign.

## What it cannot say
- It is not love, and not a cover count. "A foreign set exists" is the closest this data has to "another artist recorded it".
- Name matching misses aliases, so some own variants under another name will count as foreign. That bias favours the two-part story, so a pass is weaker than it looks.
- It uses the same 9,588 songs as move_extensive. It is not fresh.
