# Kept tables for 3/4 from lead sheets: the rule (27 Nov 2026, before any table is made; nothing built)

The songwriting session asked (09:35 ET) for 3/4 tables from OpenEWLD's 66 lead sheets, with no gate lines "until a second source is counted". The second source is now counted: Wikifonia through ChoCo holds 571 usable lead sheets in 3/4 (`COUNT.md`). So the tables are made from Wikifonia's 571, with OpenEWLD's 66 (its public-domain part) read beside them.

## The tables (3/4, sung, with words)
As the atlas makes them (`atlas_build`, `hymn_atlas`): bar rhythms by share; two-bar windows by note count; onset weights by place in the bar; notes a beat; the stress table (where stressed, unstressed and function-word syllables fall in the bar, CMU dictionary). Pitch tables stay shared across metres (Finding 1).

## Read beside
Essen 3/4 sung (folk), the hymns' 3/4 stress table, OpenEWLD 3/4, and 4/4 pop, so the genre gap is on the page.

## Is a table steady enough to use? Written now.
The 571 are split in two by composer (a composer's songs all on one side; sides by a hash of the name, so the split is not chosen). A table is **steady** if:
- bar rhythms: the twenty commonest rhythms' shares in the two halves correlate at 0.9 or more;
- stress: stressed syllables on the bar's first beat within 3 points between the halves;
- notes a beat: the halves' medians within 0.05.
A table that is not steady is reported and not offered for the draw.

## What this does not do
No gate line is drawn. No table is given to the engine. A steady table licenses a trial: a 3/4 lyric written through with the draw reading this table in place of Essen's, marks from the songwriting session first.

## What I expect
All three steady with 285 songs a side. Against Essen: lead sheets denser (more notes a beat) and more syncopated (fewer onsets on the beat); stress on the first beat lower than the hymns' 81 in 100.

## Two additions from the songwriting session (10:20 ET), set down before any table is made
- **The two-bar windows are tested too:** the twenty commonest windows' shares (all note counts together, a window's share of all two-bar windows) correlate at 0.8 or more between the halves.
- **The dating is said.** Wikifonia is mostly standards and show tunes from the 1920s to the 1960s, older than the pop collection; the files carry no dependable year, and I report how many carry any year at all. Each table's median is set beside 4/4 pop.

A note on the workspace: the machine was reclaimed between check-ins and the corpora were fetched again (`fetch.sh`). The Wikifonia count was rerun by the table script's own filter; if it does not come to 571 I say so.
