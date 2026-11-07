"""Song 21 intake (ZenEng v64). One question a turn, three options, logged."""
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 (5 Nov 19:22); correction note sent (six example corrections)"
LOG = []
SOURCE = "the writer's poem 'Cattywumpus' (pasted 19:29)"
SOURCE_MATERIAL = "poem"     # v63/v64: a poem given as source does not add the detail row
LOG.append({"q": "source", "options": {"A": "another lived story", "B": "a real instrumental section", "C": "a poem/sonnet/older lyric"}, "answer": "C"})
LOG.append({"q": 1, "topic": "how close to the poem", "options": {"A": "keep its images and order, verses, the shade's crooked corner and 'cattywumpus' as the chorus",
            "B": "set nearly as written, through-composed", "C": "keep only the heart, write new"}, "recommended": "A", "answer": "A",
            "writer_adds": "doesn't like 'Cattywumpus' as the chorus unless the run is sure it can make it work"})
LOG.append({"q": 2, "topic": "the chorus's hook", "options": {"A": "the shade, 'cattywumpus' soft as the last word once a chorus",
            "B": "'the afternoon will have to make do' as the hook; 'cattywumpus' once in a verse; the title follows the chorus",
            "C": "'a black eyelid that will not quite close'"}, "recommended": "B", "answer": "B"})
LOG.append({"q": 3, "topic": "Q0 -- who sings, when", "options": {"A": "as it happens: I to you, present tense, in the car in the minutes after",
            "B": "remembered years later", "C": "verses in the moment, chorus stepping back"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 4, "topic": "form", "options": {"A": "verse/chorus x2, short bridge, last chorus dropping away, ~3:30",
            "B": "verse/chorus x2, an instrumental break where the light comes in (tests v64's 27.21 instrumental line), last chorus",
            "C": "three verses, each ending on the hook as a refrain"}, "recommended": "A", "answer": "B"})
LOG.append({"q": 5, "topic": "sound", "options": {"A": "dream-pop haze: reverb guitars, slow drum machine, still bass; the break a clean guitar line",
            "B": "jazz-noir ballad: brushes, upright, piano; tenor sax break", "C": "trip-hop: heavy slow beat, dark keys, hiss; synth-lead break"},
            "recommended": "A", "answer": "A", "writer_asks": "so it's a rock song? -- answered: rock's quietest branch (guitar-based, from 80s-90s alt-rock), slow and soft, no drive"})
LOG.append({"q": 6, "topic": "voice", "options": {"A": "male, low and close, about A2-D4", "B": "female, low and breathy, G3-C5", "C": "male lead, female double an octave up in choruses"},
            "recommended": "A", "answer": "A"})
VOICE_ROW = "11.2 bass / baritone, B2-C4 (D4 in the final chorus) -- the nearest row to the option's 'about A2-D4' (A2 is under the row's floor; logged)"
LOG.append({"q": 7, "topic": "metre, tempo, feel", "options": {"A": "4/4 q=72, slow drum machine, air, ringing guitars", "B": "6/8 dotted-q=50 sway", "C": "4/4 q=88"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": 8, "topic": "key", "options": {"A": "G major (Gmaj7/Cmaj7 colours): 'make DO' peak B3 (the third), D4 once in the last chorus (the fifth)",
            "B": "D major: peak A3, D4 once (root)", "C": "E minor: peak B3, D4 once (the seventh)"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 9, "topic": "register", "options": {"A": "narrative", "B": "pop", "C": "folk"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 10, "topic": "title (locked)", "options": {"A": "Make Do", "B": "The Afternoon Will Have to Make Do", "C": "Cattywumpus"}, "recommended": "A", "answer": "A"})
TITLE = "Make Do"
LOG.append({"q": 11, "topic": "never-say (category expanded word by word, shown)",
            "options": {"A": "nothing explicit: naked, sex, sweat, breasts, thighs, lips, moan, climax, make love, inside you",
                        "B": "no dream-pop/afterglow cliches: haze, dreaming, floating, golden, glow, afterglow, heaven, baby, tonight, melt, burning, fire",
                        "C": "both"}, "recommended": "C", "answer": "C"})
NEVER_SAY = ["naked", "sex", "sweat", "breasts", "thighs", "lips", "moan", "climax", "haze", "dreaming", "floating", "golden", "glow",
             "afterglow", "heaven", "baby", "tonight", "melt", "burning", "fire"]
NEVER_PHRASES = ["make love", "inside you"]
LOG.append({"q": 12, "topic": "lexicon / reading (v54: an unknown word asked)", "options": {"A": "CAT-ee-WUM-pus", "B": "CAT-uh-WAM-pus (the 'catawampus' sound)", "C": "something else"}, "answer": "B"})
LEXICON = {"cattywumpus": "K AE2 T AH0 W AA1 M P AH0 S"}   # spelled as the poem spells it, said CAT-uh-WAM-pus (Q12 B)
# ---- derived (run's port, v64) ----
Q0 = ("as it happens", "I to you, present tense, in a car with the windows blacked out, in the minutes after")
OBJECTS_FROM = "Q1 A: the poem's images kept, in order"
OBJECTS = ["windows", "window", "leather", "air", "conditioner", "evidence", "body", "tremor", "skin", "dust", "clothes", "footwell", "light",
           "blade", "eyelid", "shade", "hands", "corner", "cattywumpus", "dark", "warmth", "afternoon", "black"]
WRITER_PHRASES = ["the afternoon will have to make do", "against the evidence", "a little loose in its dark", "will not quite close"]
WRITER_WORDS = ["cattywumpus"]
ROLES = {"verse", "chorus", "hook", "bridge"}
REQUIRED = {"story": "A as it happens (Q3)", "objects": "the poem's (Q1 A)", "never-say": "C (both lists, shown)", "voice": "A male low and close -> bass/baritone B2-C4, D4 final",
            "tempo-feel": "A 4/4 q=72, slow drum machine", "key": "A G major; peak B3, D4 once", "form": "B verse/chorus x2, instrumental break, last chorus",
            "register": "A narrative", "title": "Make Do", "unknown-words": "cattywumpus (Q12 B)", "readings": "CAT-uh-WAM-pus",
            "details": "not asked -- a poem given as source (v63 row)", "two-times": "not a frame form", "instrumental": "the break: clean guitar (Q5 A), Module 27.21"}
ROUTING = "Love song (V) primary -- the afterglow as it happens -- with Narrative (N) for the verses' pictures; dream-pop (alt-rock family), the break the light coming in"
SPAN = "q=72: two bars = 6.67 s x 2.1 = 14 syllables; a line takes two bars"
INSTRUMENT = "clean guitar (Q5 A: 'the break a clean guitar line')"
LOG.append({"q": "length", "writer": "too short -- maybe another verse?", "answer": "verse 3 after the instrumental break"})
LOG.append({"q": "verse 3 direction", "options": {"A": "time passing: the light crossing the seat and your shoulder, the dash clock, neither reaching for the door",
            "B": "the world outside", "C": "coming back: the footwell, the clothes back on, one more minute"}, "recommended": "A", "answer": "C",
            "writer_adds": "find an abstract way to capture the feeling of afterglow -- not quite turned to jelly, not quite what you were before"})
LOG.append({"q": "chorus line 2 trim", "options": {"A": "while the warmth is slow to leave", "B": "keep 'while the warmth is slow to leave me'", "C": "warmth still slow to leave me"},
            "recommended": "A", "answer": "A", "note": "the writer's premise (line 2 longer than line 1) was corrected: 8 syllables against 11"})
LOG.append({"q": "10.20", "topic": "blind pick: which line would you quote? (offered without scores)",
            "options": {"A": "one corner gone cattywumpus in the dark", "B": "the afternoon will have to make do", "C": "I watch a blade of daylight find its way in"},
            "slots": {"A": "Annotated top", "B": "middle (no line in both top quarters: the most-repeated hook line)", "C": "Remembered top"}, "recommended": None, "answer": "B"})
BLIND_PICK = ("B", "the afternoon will have to make do -- the middle slot (the most-repeated hook line; Remembered +5.01, second); the first middle-slot pick in nine")
WRITER_FIX_ITEM = ("20:26 -- for the next fix list: the songbook must be much less about the engine and how it did and much more about giving "
                   "musicians the data they need to bring the song alive; fine for testing, but the real engine's songbook is highly informational "
                   "and has no references to the engine or what it experienced")
