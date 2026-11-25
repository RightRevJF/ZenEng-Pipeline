# The line test, within a writer: prediction

25 November 2026. Written and committed before any WASABI lyric is read. Seen before writing: the round-two lyric document and `studies/lyric_research/RESULT.md` (no word measure passes within a writer, on 4,612 Billboard hits without line breaks); one CoCoPops file's rhyme column, to learn its format. Nothing of WASABI but the name of its archive.

## Question

Within one artist's songs, do line-level traits of the words separate the songs on a Rolling Stone 500 list from the others?

## Data

- WASABI 2.0 (Zenodo 5603369, CC BY-NC 4.0): lyrics with line and stanza breaks. No lyric text is stored in the repository; numbers only.
- Kept: English lyrics of 50 words and 8 lines or more. One row per artist and normalised title (the longest lyric).
- **Outcome:** the song is on Rolling Stone's 500 Greatest Songs in any edition (2004, 2010, 2021; lists from github.com/HipsterVizNinja/random-data), matched by normalised title and artist. The round-two design also used Grammy Song of the Year; I do not have a checked list of it, so it is left out.
- **Artists:** at least one listed song and at least five songs in all.
- Songs 59, 50 and 63 and every song of ours: not read here.

## Measures and predicted signs (listed against the same artist's other songs)

| Measure | What it is | Predicted | From |
|---|---|---|---|
| `rhyme_rate` | Among lines not sung before in the song, the share whose last word rhymes (perfect or slant, a different word) with the last word of a line within four lines either side | higher | Menninghaus 2024 |
| `perfect_share` | Of the rhymed line ends, the share that are perfect rhymes | lower | "heavy, regular rhyme marks amateur verse" |
| `iyou_rate` | "I" words plus "you" words in 100 words | higher | the document's main claim |
| `you_lines` | Share of lines with a "you" word | higher | Wassiliwizky 2017; Packard and Berger 2020 |
| `end_weight` | Named feelings and "you" words per word in each stanza's last line, less the same in its other lines | higher | chills at stanza ends |
| `feel_late` | Named feelings per word in the song's second half less its first | higher | "one plain feeling, placed late" |

Described only, no prediction: `line_cv` (spread of syllables a line), `syl_line` (syllables a line), `repeat_share` (lines sung before), `emo_rate`, `i_rate`, `stanzas`.

Word lists are those of `studies/lyric_research/measures.py`, frozen there. Rhyme: CMU dictionary; perfect is the same sounds from the last stressed vowel on; slant is the same last stressed vowel, or the same sounds after it. A line end not in the dictionary is not counted.

## Tests

1. **Within artist:** conditional logistic regression grouped by artist; each measure alone, standardised, with log word count; and year where WASABI gives one for 80 rows in 100 or more (rows without it then dropped; otherwise year is left out).
2. **Two halves:** artists split in two by a hash of the name; the same model in each half.
3. **The rhyme detector first:** against CoCoPops's hand-marked rhymes (212 songs): a line counts as rhymed by hand if its last word carries a rhyme mark. If the detector's F1 on "this line is rhymed" is under 0.70, the two rhyme measures are reported as described only and leave the count below.

## Rule

A measure **passes** if its sign in test 1 is as predicted with p < 0.05 after Holm's correction over the predicted measures counted (six, or four), and the sign is the same in both halves. **Reversed:** the opposite sign at p < 0.05 uncorrected. Otherwise **unsettled**. Nothing that does not pass goes into the engine or the room as more than advice.

## What I expect

Nothing to pass. Round one found the words do not pick a writer's canonised song, and I see no strong reason for line traits to do better: within a writer, rhyme habits and pronouns are mostly the writer's. If one moves I would guess `iyou_rate`, and I would not bet on its sign: a list of critics may well favour the less personal song.

## Cautions

- One magazine's list, heavy with rock and soul of the 1960s and 1970s.
- WASABI's lyrics are fans' transcriptions; line breaks are theirs.
- The artist is not always the writer.
