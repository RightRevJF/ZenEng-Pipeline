# Round two: the songwriter

## 1. The two strongest ideas from the others

**(a) The sceptic's crossed hymn design (tune by text by hymnal), with the rival-tune contests.** This is the best experiment in the room: no record, no star, full range, and the words can be swapped out. The evolutionist's hymn idea is the same lab without the crossing.

What my trade adds and corrects:

- **Use "number of distinct texts carried", not "number of hymnals".** One beloved text can carry a tune into every hymnal on its own (NEW BRITAIN rides "Amazing Grace"). The sceptic's tune effect b_j handles this only if the crossing is dense enough.
- **A rival-tune "winner" is often a border, not a verdict.** "O Little Town of Bethlehem" is sung to ST. LOUIS in America and FOREST GREEN in Britain. Contests must be scored within one country and one denomination, or the sign test measures geography.
- **A hymn tune is selected for a congregation, not a soloist.** The filter rewards a range of about a ninth, stepwise motion and no hard entries. A positive result therefore means "tunes a room can carry", which is a real kind of greatness but not all of it; a pop song may be loved for the one note the crowd cannot reach.
- **The pairing term is where prosody lives.** The sceptic treats g_ij as a variance share. It should be modelled, which is my new idea in section 3.

**(b) The evolutionist's conserved core (his Idea 3), which is the physicist's stiff-and-sloppy spectrum measured note by note.** It is the first proposal that measures the song as musicians actually treat it: some notes are the song and the rest are yours.

What my trade adds and corrects:

- **I can say in advance what the core will be.** Every cover keeps the rhythm and contour of the title line, the pickup into the first phrase, the note each phrase lands on, and the chord under the hook. Verse passing notes, exact rhythmic placement, key, tempo and feel are free. That is a testable prior for his predictor in step (c).
- **His alignment will mistake phrasing for mutation.** Matching "pitch class within a quarter beat" fails the moment a singer lays back, and every good singer does. Sinatra is half a bar late and has changed nothing. Align at the phrase level and score order and arrival notes, not clock position.
- **The Lakh duplicates are not covers.** Several MIDI files of one hit are several fans transcribing the same record. Their disagreement measures what is hard to hear, not what performers feel free to change. This affects the evolutionist's Idea 3, the physicist's in-house proxy, the sceptic's wild idea and my own "three transcribers as three singers". Only true cover data (Da-TACOS, if it is what the physicist believes it is) or the Irish session settings test the claim.

## 2. The weakest idea in the room

**The mathematician's Idea 7: the song as a coordinate-free shape, compared by Gromov-Wasserstein distance.** He rates it at 7% himself; I rate it lower, for a specific reason. A set of bars with distances between them has no order. A song is the order: the chorus means what it means because the verse came first, and the last chorus means more because of the bridge. Remove order and nearly every hit has the same shape, two or three tight clusters of bars (verse, chorus, bridge) at similar distances, which is the "song form" test that already failed. The classifier will sit at chance, and that will not retire the shape hypothesis as he hopes, only the unordered version of it.

In fairness, the weakest of my own is Idea 7, the reframe (same tune over changed chords or arrangement). It will fail on our data whatever the truth is. Hooktheory entries are single sections, and fan sequencers build a MIDI file by copying and pasting the chorus block, so the changed last chorus is erased by the transcriber. The same fault threatens the mathematician's holonomy and part of the producer's build arc, and the producer's gate should include a check for bar-identical repeated blocks.

## 3. One new idea: the marriage score

It exists only because the sceptic's crossed hymn design is read beside my word-in-the-mouth and appointment ideas, with the neuroscientist's "few arrivals worth waiting for" behind them.

**Plain words.** My prosody idea was stuck for lack of note-aligned lyrics. Hymns need no alignment: they are syllabic, one syllable to one note, and the metre fixes which syllable meets which note. So for every text-and-tune pair in the same metre, including pairs nobody ever printed, we can compute how well the words sit on the tune. The sceptic's pairing effect then becomes a prediction: the marriages that lasted are the ones where the text's important syllables land on the tune's appointments.

**Mathematics.** For tune j, per note k: appointment weight w_jk = standardised sum of duration, metric weight, pitch height, and a cadence indicator (the last note of each line). For text i, per syllable k in each stanza: importance u_ik = lexical stress (0, 1, 2 from a pronouncing dictionary) plus 1 for a noun or verb, plus vowel openness on a fixed table. Then:

- Fit(i, j) = mean over stanzas of the correlation between u_i and w_j.
- Worst-stanza fit = the minimum over stanzas (a tune must work for every verse, which is the real constraint in hymn writing).
- Peak fit = the importance percentile of the syllable that lands on the tune's highest long note.

Tests: (1) does Fit predict the sceptic's pairing effect g_ij; (2) in rival-tune contests within one tradition, does the winner have the higher Fit with that text; (3) is a tune's greatness b_j predicted by its mean Fit over all texts of its metre, meaning a great tune is one whose appointments suit the way English stresses fall.

**Data.** Tunes: here. Texts: public domain, in Hymnary and in open hymnal collections on GitHub (to be checked). Pairing counts: Hymnary, the same need as the sceptic's design.

**Proved wrong if** real pairings have no higher Fit than random same-metre pairings. That is a cheap first check needing no hymnal counts at all, only a list of which pairs exist.

**Odds.** 45% that real pairings beat random ones clearly; 25% that Fit decides rival-tune contests.

## 4. My two votes

- **First test with data in hand: the sceptic's Idea 2, same work in different charting records.** It asks whether two hit recordings of one song share their later fate, and it needs no musical feature, so it cannot fail for want of the right one. It tells me whether my trade has anything to explain on this yardstick. The within-work regression also tests the producer's sparseness findings with the page held fixed.
- **First test needing new data: the sceptic's crossed hymn table from Hymnary**, scored on distinct texts per tune and on rival-tune contests within one tradition. The marriage score rides on the same download.

## 5. Where the room is converging, and whether I believe it

**The theory:** a great song is a small, rigid core with a great deal of room left around it, room in the record for the voice and room in the song for the next singer.

**Do I believe it?** Half. The room is real, and I would arrange by it tomorrow. But it explains why a song gets covered better than why it is loved, and a dull song with a sparse arrangement is also "unfinished". Room is necessary. What makes the core worth leaving room for is where it is placed and what lands on it, and the only measures of that in the room are my appointment and withheld-close ideas, neither yet tested.
