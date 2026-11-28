# Folk replication: posts

One study, on branch `folk-replication`: do plainer tunes get recorded by more artists, tested again on sources we may use (the old printed collections in music21; Discogs-VI). Work in `studies/folk_replication/`. Nothing under `lib/` or `tables/` is changed. No TheSession data and no figure from the withdrawn studies.

### 27 Nov 2026 20:56 ET, folk replication (branch at the commit that carries this post)

**Set up, and the rule written first.** The rule and pass marks are in `studies/folk_replication/PREDICTION.md` (first commit c55de0f, 20:46 ET, before anything was matched). 18 tests: pitch-class entropy and eight parts of the page gate, each once as is and once with length, range, metre and collection held. Pass level .05 / 18.

- Tunes: O'Neill's 2,009, Ryan's 1,059, Aird's 1,180 read so far; Essen still reading.
- Discogs-VI downloaded outside the repo. Its artist names are stored as text, so I read them as lists (written in the rule's addendum before any join). The older counting script, `studies/judging_checks/within_artist/cliques_versions.py`, reads that text letter by letter. Its counts are close but not exact. I'm not touching it; flagging only.
- Also found: music21 doesn't carry a sharp or flat to the rest of its bar in ABC. Fixed in this study's reader only.

Ask: none.
