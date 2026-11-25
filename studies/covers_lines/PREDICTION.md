# Design B: the line test against covers, within a writer: prediction

25 November 2026, the songwriting session. Written and committed before any lyric feature is joined to any cover count. The maintainer checks.

**Seen before writing:** the round-two report; the maintainer's line test against the Rolling Stone 500 (`studies/lyric_lines` on luthier-v8-stage1 at add5ae8: nothing passes; `you_lines` reversed; leads: shorter lines, more returning lines, more stanzas); my check of it; the data scout's notes (the size of the join below, from titles and credits only). No feature of any song has been set beside its cover count.

## Question
Within one songwriter's own songs, do line-level traits of the words go with how many other artists recorded the song? Critics answered "no" (the line test). This asks the musicians.

## Data
- **Lyrics:** WASABI 2.0 (Zenodo 5603369, CC BY-NC 4.0), English, 50 words and 8 lines or more; one row per normalised artist and title (the longest lyric). Numbers only are kept; no lyric text in the repository.
- **Covers:** Discogs-VI (Zenodo 13983028), one row per version clique (`cliques.csv`, the data scout's reduction): its credited writers, its number of distinct recording artists, its first year.
- **The join (the data scout's rule, unchanged):** a WASABI song is matched to a clique with the same normalised title in which the performing artist is a credited writer (a six-character match of the artist's name with a writer's). Where several cliques match, the one with the most artists. So the performer wrote (or co-wrote) every song in the test.
- **Writers kept:** 10 matched songs or more.
- **Outcome:** log of the clique's number of distinct recording artists.
- **Controls:** log word count; the clique's first year (centred, per decade).
- Songs 59, 50, 63 and every song of ours: not read.

## Measures and predicted signs
The maintainer's `linefeat.py`, copied unchanged.

| Measure | Predicted | Why |
|---|---|---|
| `rhyme_rate` | higher | rhyme raises liking and memory (Menninghaus 2024); covers are a singer's choice |
| `iyou_rate` | higher | listeners picture a person with "I" and "you" (Packard and Berger 2020); another singer can wear the song |
| `you_lines` | higher | as above; critics went the other way, musicians may not |
| `end_weight` | higher | chills at stanza ends (Wassiliwizky 2017) |
| `feel_late` | higher | the round-two advice |
| `syl_line` | lower | the line test's lead (shorter lines in the listed song), now tested on a new outcome |
| `line_cv` | lower | regular lines are easier to sing (the data scout's prediction) |

Described only: `perfect_share`, `repeat_share`, `stanzas`, `emo_rate`, `i_rate` (`repeat_share` and `stanzas` may be fans' typing habits, as the line test said).

## Tests
1. **Within writer (primary):** OLS of the outcome on each measure alone (standardised), log word count and first year, with the writer's mean taken out of every variable; errors clustered by writer.
2. **Two halves:** writers split by a hash of the name (md5 mod 2); the same model in each.
3. **With zeros (secondary):** all of the kept writers' songs, an unmatched song counted as one recording artist (the writer alone), year from WASABI where the clique gives none; the same model.

## Rule
A measure **passes** if in test 1 its sign is as predicted with p < 0.05 after Holm's correction over the seven, and the sign is the same in both halves and in test 3. **Reversed:** the opposite sign at p < 0.05 uncorrected in test 1. Otherwise **unsettled**. Nothing that does not pass goes into the engine or the room as more than advice.

## What I expect
Little. Covers follow a song's fame, and fame within a writer follows the record more than the words. If anything moves I would guess `repeat_share` (described only) and `you_lines` upward: musicians, like listeners, may take the song they can sing to someone. A pass for `syl_line` would make shorter lines the one trait two outcomes agree on.

## Cautions
- Every song in the test has at least two versions in Discogs (a clique exists): the test is among songs that were versioned at all. Test 3 is there for that.
- Discogs credits and titles are editorial; the join can miss or mismatch.
- The performer-writer rule leaves out bands whose name is not a writer's, and songs a writer gave to others.
