"""Song 12, Wood and Cloth: the second edition (from 21 Nov 2026). The first edition (4 Nov, ZenEng v55) is kept as the
writer's attached files in src/p12_ed1/ (never committed). Every choice logged (the writer's standing ask)."""
LOG = []
LOG.append({"when": "2026-11-21", "q": "which song is best", "answer": "Claude: best lyrics the Harold song, best music This Side of the Door, best overall Wood and Cloth"})
LOG.append({"q": "look at Wood and Cloth", "writer": "Here's what I have. If this is the best song I've got, then we need to rework some things. What do you think?",
            "attached": ["songbook (docx)", "hymnal page (pdf)", "lead sheet (pdf)"]})
LOG.append({"q": "concerns (writer adds an outside review)", "concerns": [
    "1 misplaced stresses: 1.3 'ON the hillside', 4.3 'A-bove'", "2 heavy 'stone rolled' lines on light beats (2.4, 5.2)",
    "3 1.2 'cattle tend' unclear", "4 5.2 'for all to find' padding", "5 stanza 4 weakest ('Once', 'shining day')",
    "6 one rhythm in every bar (also the review's trochee-in-3/4 point)", "7 line 3 doesn't echo line 1 in the tune",
    "8 low, flat tessitura", "9 weak final cadence (B falls to A)", "10 static harmony",
    "11 engraving: engine terms (PASS, Module 11.10), crowded lyrics bars 4-5, bar numbers against chord names, stanza 4 unmarked"],
    "declined": "review's 'would carry' change: kept, it is the hymn's look-ahead tense, as 'wood would hold him'"})
LOG.append({"q": "organist", "writer": "Also, I'd like a dedicated sheet of music for the organist, or a full score, whichever works best",
            "answer": "organ score (two manuals and pedal, introduction, registrations by stanza, stanza 4 tacet, broadening) from one record with the hymnal page and lead sheet: concern 12"})
LOG.append({"q": "where to start", "options": {"A": "words first", "B": "new tune on current words", "C": "both in one pass"}, "recommended": "A",
            "answer": "A. Rework the lyrics and print them here along with the first draft", "file": "lyric_draft2.md"})
LOG.append({"q": "lyric draft 2", "writer": "I think a hybrid of the two is best. Here are two versions. Which, if any, do you prefer?",
            "note": "the two pasted versions are identical: draft 2 with 2.4 back to 'one stone rolled against the light' and 5.2 back to 'stone rolled back for all to find'",
            "reply": "the hybrid works: the two stone lines are a pair (rolled against / rolled back); offered 5.2 'stone rolled back and none to find'"})
LOG.append({"q": "which hybrid", "options": {"A": "hybrid with 5.2 'stone rolled back and none to find'", "B": "hybrid as pasted", "C": "send the other version"},
            "recommended": "A", "answer": "A", "file": "lyric_draft3.md",
            "writer_adds": "Also, I'm worried about people confusing Joseph of Arimathea with Joseph Jesus stepfather"})
LOG.append({"q": "the two Josephs", "options": {"A": "keep Joseph; scripture refs under stanza 2 on the hymnal page (Luke 2:7; Matthew 27:57-60) and one sentence in songbook and bulletin naming Joseph of Arimathea",
            "B": "keep Joseph, no notes", "C": "'Rich men wrapped him close in linen' (John 19:40)"}, "recommended": "A", "answer": "A. And run the mouth tests",
            "locked": "lyric_locked.md (draft 3)"})
LOG.append({"step": "mouth tests on the locked lyric", "file": "mouth_p12.py -> mouth_readings.txt",
            "result": "no unstressed syllable on a strong position in any stanza (the two misstresses are gone); 87 87 exact; "
                      "heavy monosyllables on weak positions: 2.4 'one STONE', 5.2 'stone ROLLED', 4.2 'star LAID', 3.1 'wise MEN' (the tune gives them even notes); "
                      "close vowels on held 7th syllables: 'lin-en' (2.1, 2.3), 'Ju-dah' (4.1), 'sleep-ing' (5.3), all singable at a hymn's pace; "
                      "4-consonant joins (reported, none 5): 'and cloth', 'against the', 'friends would'; rare word: myrrh (kept, biblical); density about 1.1 syllables a second",
            "room_check": "not run: lyric_room.py lays a song out on the 4/4 engine; a strophic 3/4 hymn goes by the sketch path. The hymn's room is the hold at every line end and stanza 4 for choir alone"})
