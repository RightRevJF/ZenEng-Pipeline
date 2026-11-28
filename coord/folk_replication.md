# Folk replication: posts

One study, on branch `folk-replication`: do plainer tunes get recorded by more artists, tested again on sources we may use (the old printed collections in music21; Discogs-VI). Work in `studies/folk_replication/`. Nothing under `lib/` or `tables/` is changed. No TheSession data and no figure from the withdrawn studies.

### 27 Nov 2026 20:49 ET, folk replication (branch at the commit that carries this post)

**Set up, and the rule written first.** The rule and pass marks are in `studies/folk_replication/PREDICTION.md` (first commit c55de0f, 20:46 ET, before anything was matched). 18 tests: pitch-class entropy and eight parts of the page gate, each once as is and once with length, range, metre and collection held. Pass level .05 / 18.

- Tunes: O'Neill's 2,009, Ryan's 1,059, Aird's 1,180 read so far; Essen still reading.
- Discogs-VI downloaded outside the repo. Its artist names are stored as text, so I read them as lists (written in the rule's addendum before any join). The older counting script, `studies/judging_checks/within_artist/cliques_versions.py`, reads that text letter by letter. Its counts are close but not exact. I'm not touching it; flagging only.
- Also found: music21 doesn't carry a sharp or flat to the rest of its bar in ABC. Fixed in this study's reader only.

Ask: none.

### 27 Nov 2026 20:56 ET, folk replication (branch at the commit that carries this post)

**Done. Nothing held and nothing failed: too few tunes to tell.** One page: `studies/folk_replication/SUMMARY.md`. Full table: `RESULT.md`, printed with `result.json` by one command.

Rule first, by the commit clock:
- the rule c55de0f (20:46); the list-field addendum c289574 (20:49);
- the match, the eye check and addendum 2 at 21f0223 (20:54), all before the join;
- the join and the tests 2b6af3b (20:55).

| | |
|---|---|
| Tunes read | 12,761 |
| Matched (test / confirm) | 473 (231 / 242) |
| Power at a correlation of 0.15 | 0.21 and 0.22 |
| Eye check, wrong in 100 | 28 (37 at most) |
| Tests held / missed / estimates | 0 / 0 / 18 |
| Leaning the predicted way | 11 of 18 |

- Every test is an estimate, by the rule written before the join.
- Closest: short figures sung again, held fixed, test half p .0038 against .00278; the confirm half didn't follow.
- The German (Essen) matches were clean; about half the Irish and Scottish ones were later pop songs with the same title.
- The page gate's parts are neither supported nor ruled out without the withdrawn data.

Ask: the maintainer, please add the 473 matched tunes to the data pack's seen ledger (`matches.json`: the clique ids and halves), and look at the `cliques_versions.py` note in SUMMARY.md.
