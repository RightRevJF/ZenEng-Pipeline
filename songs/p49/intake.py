"""Song 45 intake (the writer: Jason Bryant). Source: his book 'You Will Wake: What the Bible Actually Says About Death, Resurrection, and Seeing
the Ones You Love Again' (read, used, not stored here). Words and music: Jason Bryant."""
LOG = []
LOG.append({"q": "0", "topic": "the brief", "answer": "the writer's own: 'New song. Tearjerker all the way with a hopeful ending. I want to capture the theology of this book in song'"})
LOG.append({"q": "1", "topic": "whose story carries the song",
            "options": {"A": "the unfinished conversation: brother and sister never close, her sudden death, the dark year, the light after the storm, the conversation resumed in the morning",
                        "B": "the man who knew: a dying friend says 'This is goodbye' without fear; the comforter comforted",
                        "C": "no one story: the book's images (the night before waking, the room next door, the seed, a name called) sung to anyone grieving"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "2", "topic": "who sings to whom",
            "options": {"A": "he sings to her ('you'): the conversation he never had, said at last; in the last chorus the one they will have in the morning",
                        "B": "he tells it ('my sister')", "C": "she sings to him from the next room"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "3", "topic": "never-say",
            "options": {"A": "the book's images, not church words: no heaven, angel, Jesus, Lord, God, soul, resurrection, eternal; no grief cliches; no names; the theology in the night before waking, the room next door, the seed, a name called, the table",
                        "B": "as A, Scripture's scenes allowed (a name heard in a garden, bread broken, 'come out')", "C": "only the grief cliches banned"},
            "recommended": "A", "answer": "A"})
NEVER_SAY = ["heaven", "heavens", "angel", "angels", "jesus", "lord", "god", "soul", "souls", "resurrection", "eternal", "eternity", "amy", "leigh", "christ", "pray", "prayer", "holy"]
NEVER_PHRASES = ["gone too soon", "better place", "watching over me", "rest in peace", "in my heart", "other side", "see you again", "up above", "angel"]
CARRIERS = ["the night before waking", "the room next door, a wall with a door", "the seed", "a voice calling your name", "the table set for morning"]
LOG.append({"q": "4", "topic": "the sound",
            "options": {"A": "piano ballad in 6/8, about dotted-quarter 52; strings from the second chorus", "B": "fingerpicked acoustic guitar, about 72 in 4/4; a cello under the second verse",
                        "C": "country ballad, about 66, pedal steel"},
            "recommended": "A", "answer": "B. 'And could the output produce a guitar only whole score so a friend with a guitar could just play it?'"})
FEEL = "fingerpicked acoustic guitar, about 72, 4/4; a cello under the second verse (Q4 B)"
DELIVERABLES_EXTRA = ["a guitar-only whole score: voice, words, chords and the guitar part in notation and TAB, playable alone by a friend with a guitar (Q4 note)"]
LOG.append({"q": "5", "topic": "who sings", "options": {"A": "a man's middle voice, about B2-E4", "B": "a light tenor, about C3-A4", "C": "the friend's own range"},
            "recommended": "A", "answer": "A"})
VOICE = dict(kind="a man's middle voice", lo=47, hi=64)
LOG.append({"q": "6", "topic": "the key",
            "options": {"A": "G major, open chords; verses lean on E minor; the last chorus lifts a whole step to A", "B": "G major throughout", "C": "E minor verses opening to G major choruses"},
            "recommended": "A", "answer": "A. 'But please, don't dumb down the music just so it can be played. Allow your full musical brilliance to sparkle even with limited instrumentation'"})
KEY = "G major; the last chorus lifted a whole step to A (Q6 A)"
WRITER_NOTE_Q6 = "the music not simplified for playability: full harmonic and melodic invention within one guitar and a cello (borrowed chords, inner-voice motion, suspensions, open-string colour)"
LOG.append({"q": "7", "topic": "the form",
            "options": {"A": "Intro 4, V 8, Ch 8, V 8, Ch 8, Bridge 8, LC 8 (in A), Tag 4: 56 bars, about 3:07 at 72", "B": "as A with pre-choruses: 64 bars, about 3:33",
                        "C": "folk form, three verses with a refrain line, a bridge: 52 bars, about 2:53"},
            "recommended": "A", "answer": "A"})
FORM = [("Intro", 4), ("Verse 1", 8), ("Chorus 1", 8), ("Verse 2", 8), ("Chorus 2", 8), ("Bridge", 8), ("Last Chorus", 8), ("Tag", 4)]   # 56 bars, about 3:07 at 72
LOG.append({"q": "8", "topic": "the title", "options": {"A": "Before It's Done", "B": "The Room Next Door", "C": "You Will Wake"}, "recommended": "A", "answer": "A"})
TITLE = "Before It's Done"
LOG.append({"q": "9", "topic": "draft 1: lock or notes", "options": {"A": "lock", "B": "notes", "C": "a second full draft to compare"}, "recommended": None, "answer": "C"})
LOG.append({"q": "10", "topic": "which draft goes forward", "options": {"A": "draft 1", "B": "draft 2", "C": "a mix"}, "recommended": None,
            "answer": "B", "notes": ["1 make the death unmistakable earlier without naming it: one quiet pressure point in verse 1 or the first chorus that only makes sense if she is already gone ('I'm still coming', or a detail that implies absence rather than distance)",
                                     "2 strengthen verse 2's reveal: one more concrete, slightly clinical detail that belongs to the job, so the personal cost lands harder",
                                     "3 let the chorus carry more of the resurrection claim: the door already real, not merely possible, without becoming preachy",
                                     "4 tighten the bridge so the birthday image feels inevitable: a word or two linking the morning to the room in verse 2 or to the wall/door",
                                     "5 decide how much the tag should wound: leave it, or let it cut a fraction deeper (answering a conversation death interrupted mid-sentence)"]})
LOG.append({"q": "11", "topic": "draft 3: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "change one line"}, "recommended": None,
            "answer": "notes", "notes": ["the last chorus's 'I'm here, I held the thought': the tense change does a lot of work; is he reunited, speaking from the other side, or arrived at the hospital? make sure the delivery clarifies the emotional destination",
                                         "the chorus slightly less accomplished than the verses: 'Hold that thought, I'm still coming / Leave a light on in the next room' good; 'It's only a wall, and somebody's holding the door' more abstract than the phone, the kitchen, the tissue box and the doorway; maybe another way"]})
LOG.append({"q": "12", "topic": "draft 4: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "change one line"}, "recommended": None, "answer": "A"})
DENSITY_342 = "the locked lyric: 275 syllables over 52 sung bars, 5.29 a bar (Verse 2 6.75 the densest; the kept 3.6-4.1)"
LOG.append({"q": "13 (342)", "topic": "the lyric's density", "options": {"A": "keep every word: the verses talk in quick eighths and sixteenths, the choruses hold long notes",
            "B": "lengthen the lines (about 3:40)", "C": "trim the six longest lines"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "14 (298)", "topic": "where the chorus sits against the verse",
            "options": {"A": "the chorus lifts: verses lower, speaking; the chorus 3 or more over them with the long notes; the last chorus (in A) the top",
                        "B": "as drawn", "C": "a narrow verse, then the chorus opens wide"}, "recommended": "A", "answer": "A"})
LIFT = "Q14 A: the chorus's median 3 or more semitones over the verse's; the last chorus the song's top"
LOG.append({"q": "15", "topic": "the chorus design",
            "options": {"A": "the resolution withheld until morning: 'thought' held long over a suspension; 'before it's done' walks down by step toward home and stops one step short (the 2nd) in choruses 1-2; only the last chorus ('It's morning') lands home; the tag ends unresolved on 'before'; a design gate",
                        "B": "only the last chorus's last note home", "C": "no design"}, "recommended": "A", "answer": "A"})
CHORUS_DESIGN = "Q15 A: 'thought' held long over a sus chord; 'before it's done' steps down to the 2nd (choruses 1-2) and home (last chorus); the tag ends on the 2nd"
LOG.append({"q": "16", "topic": "after delivery: two weak lines in the pick of record (verse 2 opens on nine E3s; 'You're only in the next room' rushed in sixteenths, then a bar and a half of rest)",
            "options": {"A": "hand-edit both lines, log the edits and rebuild every document", "B": "keep the pick as it is", "C": "take the engine's next choice and rebuild"},
            "recommended": "A", "answer": "A"})
HAND_EDITS = "Q16 A: verse 2 line 1 re-pitched on its own rhythm; chorus line 2 re-set in eighths and quarters (chorus 2 the same), and the last chorus's return of it re-set to match"
