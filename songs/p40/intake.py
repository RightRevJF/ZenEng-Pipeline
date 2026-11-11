"""Song 40 intake (ZenEng v108; a debugging song on the default path). Words and music: Jason Bryant."""
SPEC = "ZenEng v108"
SOURCE = "Wild Fruit (Jason Bryant): 'The Garden That Grew by Itself' (read, used, not copied into the repo)"
BRIEF = {"class": "pop or rock, 4/4, straight eighths", "form": "verse, pre-chorus, chorus, bridge", "voice": "not an angry male baritone",
         "lines": "mixed lengths, not every line two bars with a pickup",
         "default path": "era none; no character chosen; no designed summit; bridge register, chorus lift, countermelody, drum design not chosen; said twice asked as usual (a plain repeat)",
         "runs": "1000 main, 1000 control (243 off), each twice; findings from 298"}
LOG = []
LOG.append({"q": "1", "topic": "the idea", "options": {"A": "First Light (dawn drive after a night shift)", "B": "The Last Box (emptying a childhood home)", "C": "Windows Down (road-trip duo)"},
            "recommended": "A", "answer": "What about something from the parable in Wild Fruit I shared with you called The Garden?"})
LOG.append({"q": "2", "topic": "whose song", "options": {"A": "Lark's song: warm mezzo; verses the clean coded food behind the wall; chorus Briar's line 'it used to taste like nothing else on earth'; bridge the girl at the crack",
            "B": "the girl at the crack, bright and wondering", "C": "Aster at the long table, 'never separate what grows together'"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "3", "topic": "who Lark sings to", "options": {"A": "to Briar ('You said it used to taste like nothing else on earth')", "B": "to the village", "C": "to no one, thinking aloud"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "4", "topic": "title", "options": {"A": "Nothing Else on Earth", "B": "Both Halves", "C": "The Garden Grew"}, "recommended": "A",
            "answer": "A.  The key will be to tell the story abstractly like Zeppelin's Misty Mountain Hop.  To being forward the world in oblique snippets",
            "reading": "title 'Nothing Else on Earth'; the lyric tells the story obliquely, the world brought forward in snippets (images, overheard lines), never explained"})
TITLE = "Nothing Else on Earth"
LOG.append({"q": "5", "topic": "sound and pace", "options": {"A": "riff-led rock, light touch, q = 116, electric piano or guitar riff, straight eighths", "B": "folk-rock q = 104", "C": "pop ballad q = 80"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "6", "topic": "form", "options": {"A": "86 bars, 2:57: Intro 8, V1 12, Pre 4, Ch 8, V2 12, Pre 4, Ch 8, Bridge 8, Riff break 8, Last Ch 10, Outro 4",
            "B": "110 bars, 3:47: as A with 16-bar choruses (last chorus 18)", "C": "74 bars, 2:33: no break, 4-bar intro"}, "recommended": "A",
            "answer": "B.  So make sure the hook is world class.  Be evocative and lush in your portrayal of this thought world",
            "reading": "form B: Intro 8, Verse 1 12, Pre 1 4, Chorus 1 16, Verse 2 12, Pre 2 4, Chorus 2 16, Bridge 8, Riff break 8, Last Chorus 18, Outro 4 = 110 bars at q = 116 (3:47); the chorus must carry a world-class hook; the imagery lush and evocative"})
FORM = [("Intro", 8), ("Verse 1", 12), ("Pre 1", 4), ("Chorus 1", 16), ("Verse 2", 12), ("Pre 2", 4), ("Chorus 2", 16), ("Bridge", 8), ("Riff break", 8), ("Last Chorus", 18), ("Outro", 4)]
LOG.append({"q": "7", "topic": "voice and key", "options": {"A": "warm mezzo A3-D5, D major", "B": "alto F3-C5, C major", "C": "mezzo-soprano C4-F5, F major"}, "recommended": "A", "answer": "A"})
VOICE = dict(kind="warm mezzo", lo=57, hi=74, key="D major")   # A3-D5
LOG.append({"q": "8 (242, 264)", "topic": "era", "options": {"A": "none (default path)", "B": "CLASSIC", "C": "MODERN"}, "recommended": "A", "answer": "A"})
ERA = None
LOG.append({"q": "9 (225)", "topic": "character on the axes", "options": {"A": "nothing in particular (default path)", "B": "off-beat verses", "C": "stepwise choruses"}, "recommended": "A", "answer": "A"})
CHARACTER = None
LOG.append({"q": "10", "topic": "never-say", "options": {"A": "oblique: no names from the book, no explaining words, no Eden/paradise/heaven/holy, no stock cliches", "B": "as A, Briar named once in the bridge", "C": "as A, explaining words allowed"}, "recommended": "A", "answer": "A"})
NEVER_SAY = ["Aster", "Briar", "Clement", "Flask", "Moss", "Lark", "Thresh", "Reed", "Stone", "Harmon", "Aldric", "Wren", "Finch", "Sable", "Petra", "Barrel"]
NEVER_PHRASES = ["classification", "faction", "dispensar", "the cities", "filter", "orientation", "eden", "paradise", "heaven", "holy",
                 "heart and soul", "set me free", "tears like rain", "broken wings", "fire inside", "against all odds", "meant to be", "light the way"]
LOG.append({"q": "11 (213)", "topic": "which section says it twice", "options": {"A": "the chorus: the hook line returns word for word, a plain repeat, no designed chant", "B": "the verse", "C": "the bridge"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "12", "topic": "draft 1: lock or notes", "options": {"A": "lock", "B": "notes", "C": "two other chorus first halves"}, "answer": "B",
            "notes": ["'Six letters on the peel': is it a fruit, a sign, a plaque? intriguing but may distract from a precise opening; test aloud, don't change automatically",
                      "Pre 2 weaker than Pre 1: more explanatory; 'like a song you've lost the words to' is familiar; find a more surprising way",
                      "Bridge risks explaining the metaphor ('Dark half, light half, both at once. Nobody there with a book.'); make it more imagistic without losing its meaning"]})
LOG.append({"q": "13", "topic": "draft 2: lock or notes", "answer": "Just read and react, don't fix until I say go",
            "notes": ["Mystery occasionally outruns meaning: 'ten questions and a pencil and a bench where you can wait' is not emotionally legible; several lines make atmosphere without advancing understanding",
                      "'Thank you for everything, says the note on the door' is so specific it generates theories (death, closure, abandonment, collapse, retirement) and pulls focus from the food/wholeness metaphor; scrutinize hardest",
                      "the refrain 'It used to taste like nothing else on earth' may be one repetition too long on the page; depends on the melody"]})
LOG.append({"q": "13 (cont.)", "answer": "If you agree with the notes, make the changes"})
LOG.append({"q": "14", "topic": "draft 3: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "lock, keep the third refrain in choruses 1-2"}, "answer": "A.  And I really like this song so do your absolute best musically!",
            "reading": "lyric locked as lyric_draft3.md (copied to lyric_locked.md)"})
LOG.append({"q": "15 (216, 244)", "topic": "designed summit", "options": {"A": "none: the engine places the peak (default path)", "B": "the top note on 'earth' in the hook", "C": "the top note on 'tastes' in the last line"}, "recommended": "A", "answer": "A"})
SUMMIT = None
LOG.append({"q": "16 (208)", "topic": "bridge register", "options": {"A": "not chosen: drawn from the kept distribution, an aim (default path)", "B": "above the verse, under the chorus top (design gate)", "C": "lowest and quietest (design gate)"}, "recommended": "A", "answer": "A"})
BRIDGE_REGISTER = None
LOG.append({"q": "17 (288)", "topic": "chorus lift", "options": {"A": "not chosen: drawn from the kept distribution (default path)", "B": "a large lift, 5+ semitones (design)", "C": "level (design)"}, "recommended": "A", "answer": "A"})
LIFT = None
LOG.append({"q": "18 (235)", "topic": "countermelody", "options": {"A": "off (default path)", "B": "last chorus only", "C": "every chorus, growing"}, "recommended": "A", "answer": "A"})
COUNTER = None
LOG.append({"q": "19 (236)", "topic": "drum design", "options": {"A": "not chosen: class defaults (default path)", "B": "Bonham-style half-time verse, full beat in the chorus (designed feel change)", "C": "four on the floor in the choruses"}, "recommended": "A", "answer": "B",
            "note": "off the default path: an arrangement design (236's feel change), not a melody gate; flagged to the writer"})
LOG.append({"q": "20", "topic": "keep the half-time verse (off the default path)", "options": {"A": "keep B: half-time verses, full beat at the chorus; an arrangement design, named in the report", "B": "switch to class defaults", "C": "half-time verses, full time from the pre"}, "recommended": "A", "answer": "A"})
DRUMS = "half-time verses (Bonham style), full beat in the choruses: an arrangement design (236), not a melody gate"
LOG.append({"q": "21 (230)", "topic": "lines of 9+ syllables in the chosen form", "finding": "230 gives no line of 9+ syllables two bars unless the design says so; the chorus passes (10,11,9,7 / 10,10,10,9 in 8 bars), pre-chorus 2 (11,10 in 4) and the bridge (10,8,7,10,8,6 in 8) cannot meet it in form B",
            "options": {"A": "the writer's form and lyric are the design: 9-11-syllable lines take two bars where the section requires, named; 230 failed by a named design choice", "B": "lengthen sections (about 140 bars)", "C": "trim words to 8 syllables or fewer"},
            "recommended": "A", "answer": "A",
            "readings_offered": ["232 over 289 for title lines", "288 kept rates of note lengths from the pop IOI shares (v88), eight lengths; chorus top/median/lowest drawn together from one quantile",
                                 "286 rhythm band and sequence legs read on the POP909 pairs at 5/95 soft and 1/99 hard", "'every' sung as two syllables", "last chorus 'and it tastes' a return of the hook; the tag repeats the hook's end"]})
SLOTS = {"Verse": [2, 1, 3, 3, 2, 1], "Pre": [2, 2], "Chorus": [2, 2, 2, 2, 2, 2, 2, 2], "Bridge": [2, 1, 1, 2, 1, 1], "Last Chorus": [2, 2, 2, 2, 2, 2, 2, 2, 2]}
# ---- after delivery: the song treated as a real song, not a test ----
LOG.append({"q": "22", "topic": "after delivery: the hook (the writer: 'stop thinking of it as a test and start thinking of it like a real song that we want to do great on')",
            "options": {"A": "design the chorus: where the hook peaks and how far the chorus lifts; rerun the search with that design, pick by ear, refine the hook by hand (logged)",
                        "B": "start from the old-fit pick 353742341ffc (chorus +4.5) and polish", "C": "hand-write the chorus melody; the engine fits the rest"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "23 (design)", "topic": "the hook's high point",
            "options": {"A": "climb through 'used to taste like', peak on 'NOTH-ing', land 'earth' on a held A4 over the A chord (open; only the tag comes home to D)",
                        "B": "'earth' on a held D5, the hook's top", "C": "peak early on 'taste', fall to 'earth' (lifted above the verse)"},
            "recommended": "A", "answer": "A. And I just realized, the Zeppelin song this should be patterned after is the Battle of Evermore!"})
LOG.append({"q": "24 (design)", "topic": "the sound, after The Battle of Evermore",
            "options": {"A": "all Evermore: mandolin riff, strummed and droning acoustic, frame drum or hand percussion, no kit",
                        "B": "Evermore, then the storm: verses and pre-choruses mandolin and acoustic only; the band (full beat, strings) arrives at the chorus",
                        "C": "keep the band; borrow only the duet and call and response"},
            "recommended": "A", "answer": "B"})
LOG.append({"q": "25 (design)", "topic": "the second voice",
            "options": {"A": "Briar sings the chorus: chorus 1 alone; Lark joins in harmony in chorus 2; the last chorus both, Lark on top for 'she sat down hungry'",
                        "B": "Lark sings all; a second female voice shadows every chorus", "C": "call and response inside the chorus: a second voice echoes 'nothing else on earth'"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "26 (design)", "topic": "Briar's voice",
            "options": {"A": "an older man, high and worn: the chorus at the written pitch, the climb and the A4 a cry; Lark's harmony above toward C#5",
                        "B": "an older man, low and gentle, an octave under", "C": "an older woman, alto, Lark's octave"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "27 (design)", "topic": "the mandolin riff",
            "options": {"A": "a new mandolin figure drawn by the engine: driving picked eighths over open D and A drones, the melody notes on top, moving over D-C-G-D (Evermore's spirit, not its notes)",
                        "B": "a hand-written D mixolydian figure", "C": "the current guitar riff an octave up on mandolin"},
            "recommended": "A", "answer": "A",
            "plan stated before it": "verses (Lark) low, top about F#4; the chorus (Briar) climbs to B4 on 'NOTH-ing', 'earth' a held A4; Lark's harmony above him later, up to C#5"})
