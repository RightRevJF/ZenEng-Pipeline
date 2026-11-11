"""Song 41 intake (ZenEng v109; a debugging song on the default path, in a different feel from song 40). Words and music: Jason Bryant."""
SPEC = "ZenEng v109"
BRIEF = {"class": "pop or rock, 4/4", "feel": "different from song 40's straight eighths", "form": "verse, pre-chorus, chorus, bridge",
         "default path": "era none; no character chosen; no designed summit; bridge register, chorus lift, countermelody, drum design not chosen; said twice asked as usual",
         "runs": "1000 main, 1000 control (243 off), each twice; findings from 310 (310-313 from the port test on song 40)"}
LOG = []
SOURCE = "When the Bible Refuses to Behave (Jason Bryant; WTBRB Amazon FINAL v1.docx, Drive, last modified 2026-05-01): read, used abstractly, not copied into the repo"
LOG.append({"q": "1", "topic": "the idea", "options": {"A": "Last Load (two strangers folding laundry at midnight)", "B": "The Long Way Home (after a funeral, past the childhood house)",
            "C": "Saturday Hands (father and grown daughter rebuild a fence)"}, "recommended": "A",
            "answer": "Use it as a basis for our next song. Abstractly, of course (When the Bible Refuses to Behave, the latest file from Drive)"})
LOG.append({"q": "2", "topic": "the song's center", "options": {"A": "the question (a child's question no one can answer; the song holds both halves)",
            "B": "Saturday people (the silent day between; grief and promise in one breath)", "C": "the wild text (something untamed every fence fails to hold; sung by one who tried to make it behave and lets it run)"},
            "recommended": "B", "answer": "C. But it can't be about the Bible directly otherwise people will tune it out. We've got to use language to open the idea that mastery over a thing often comes with the consequence of draining joy and sustenance out of a thing. Understand?"})
LOG.append({"q": "3", "topic": "the image", "options": {"A": "the river: he dams it; power, order, a calm lake; the valley dries, the sound goes quiet; he opens the gate",
            "B": "the tune played until perfect, no longer moving anyone", "C": "the horse broken to the saddle"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "4", "topic": "title and hook", "options": {"A": "The Water Used to Sing (the water used to sing; now it only shines)", "B": "Open the Gate", "C": "Everything Downstream"},
            "recommended": "A", "answer": "A"})
TITLE = "The Water Used to Sing"
LOG.append({"q": "5", "topic": "sound and pace (a different feel from song 40)", "options": {"A": "swung shuffle, q = 96: Americana rock, rolling swung eighths; acoustic and electric guitars, organ, brushes to sticks",
            "B": "sixteenth-note soul groove, q = 92", "C": "slow triplet ballad, q = 66"}, "recommended": "A", "answer": "A"})
FEEL = "swung eighths (shuffle), q = 96"
LOG.append({"q": "6", "topic": "form", "options": {"A": "80 bars, 3:20: Intro 4, V1 8, Pre 4, Ch 8, V2 8, Pre 4, Ch 8, Bridge 8, Break 8, Last Ch 12, Outro 8",
            "B": "96 bars, 4:00: Intro 8, V1 8, Pre 4, Ch 8, V2 8, Pre 4, Ch 8, Bridge 8, Break 8, V3 8, Last Ch 16, Outro 8", "C": "64 bars, 2:40: no break, no third verse"},
            "recommended": "B", "answer": "B",
            "story": "V1 the wild river he loved; V2 the dam and the victory; bridge the dry valley and the silence; break the gate opening; V3 the water coming back; last chorus 16"})
FORM = [("Intro", 8), ("Verse 1", 8), ("Pre 1", 4), ("Chorus 1", 8), ("Verse 2", 8), ("Pre 2", 4), ("Chorus 2", 8), ("Bridge", 12), ("Break", 8), ("Verse 3", 12), ("Last Chorus", 16), ("Outro", 8)]   # Q20 A: 104 bars
LOG.append({"q": "7", "topic": "voice and key", "options": {"A": "male baritone, warm and weathered, G major, G2-E4", "B": "male tenor, A major, A2-A4", "C": "female alto, E major, E3-C#5"},
            "recommended": "A", "answer": "A"})
VOICE = dict(lo=43, hi=64, key="G major", kind="male baritone, warm and weathered (written an octave up)")
LOG.append({"q": "8", "topic": "era", "options": {"A": "no era (default path)", "B": "classic era (to 1979)", "C": "modern era (1990 on)"}, "recommended": "A", "answer": "A"})
ERA = None
LOG.append({"q": "9", "topic": "character", "options": {"A": "not chosen (default path)", "B": "reciting", "C": "singing"}, "recommended": "A", "answer": "A"})
CHARACTER = None
LOG.append({"q": "10", "topic": "never-say", "options": {"A": "fully hidden: no church words, no explaining words, no river cliches",
            "B": "as A, one faint echo allowed (e.g. 'living water')", "C": "only the obvious church words"}, "recommended": "A", "answer": "B"})
NEVER_SAY = ["god", "lord", "holy", "faith", "grace", "gospel", "scripture", "bible", "church", "word", "verse", "pray", "prayer", "sin", "jesus", "christ", "heaven",
             "control", "mastery", "master", "joy", "meaning", "lesson", "soul"]
NEVER_PHRASES = ["go with the flow", "still waters run deep", "bridge over troubled water", "let it flow", "river runs deep", "let it be"]
ECHO_ALLOWED = "one faint echo (e.g. 'living water')"
LOG.append({"q": "11 (213)", "topic": "which section says it twice", "options": {"A": "the chorus: the hook line returns word for word, a plain repeat", "B": "the verse", "C": "the bridge"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "12", "topic": "draft 1: lock or notes", "options": {"A": "lock", "B": "notes", "C": "two other choruses"}, "recommended": None, "answer": "notes",
            "notes": "V1: 'took the low field every April, left it black by June' (drop the 'and'). Pre 1 keep. Chorus works; in the final chorus vary the second pass of the hook. V2 excellent, keep. Pre 2 keep. Bridge: make the girl's question a little more natural in speech. V3: optionally one more personal or lasting loss than the mailbox (understatement works). Last chorus: test 'whatever I build next'; the song could end on 'It sings.' with a hold."})
LOG.append({"q": "13", "topic": "draft 2: lock or notes", "answer": "These might be redundant. Check them and tell me if you want to make more changes (The_Water_Used_to_Sing_Revision_Suggestions.docx, on draft 1)",
            "suggestions": "rewrite both pre-choruses (youthful certainty; satisfaction with the still lake, silence mistaken for peace); test the sheepdog (too affectionate?); one restrained clue for why he opens the gate (and the irony that restoring is control too); make the final chorus's 'it will take whatever I build' less explanatory; the swimming hole is familiar; 'fought me like a mule' conventional; keep the moral ambiguity"})
LOG.append({"q": "14", "topic": "the writer's edit of draft 3 (verse 3: 'it fought me like a mule' restored)", "options": {"A": "lock as the writer has it", "B": "more notes"},
            "recommended": "A", "answer": "A", "locked": "lyric_locked.md"})
LOG.append({"q": "15 (216, 244)", "topic": "designed summit", "options": {"A": "not chosen: the search places the peak (default path; song 40 under v109: the top note sounded ~11 times, mostly in the chorus; kept songs ~4)",
            "B": "the top note E4 held on 'sings', once, at the end", "C": "the top note on 'shines' in each chorus"}, "recommended": "B", "answer": "A"})
SUMMIT = None
LOG.append({"q": "16 (208)", "topic": "bridge register", "options": {"A": "not chosen: drawn from the kept distribution, bridge median 2 over the verse's at the median, 0 to 5 in the middle half (default path)",
            "B": "lower than the verse: the dry valley at the floor of the voice (design)", "C": "higher than the verse, under the chorus top (design)"},
            "recommended": "B", "answer": "B"})
BRIDGE_REGISTER = "below the verse (design): bridge median under the verse's median"
LOG.append({"q": "17 (288)", "topic": "chorus lift", "options": {"A": "not chosen: drawn from the kept distribution, chorus median 1 over the verse's at the median (0 to 3); the chorus top at or under the verse's in about half the builds (default path)",
            "B": "a clear lift, 4+ semitones (design)", "C": "level (design)"}, "recommended": "B", "answer": "A"})
LIFT = None
LOG.append({"q": "18 (235)", "topic": "countermelody", "options": {"A": "off (default path)", "B": "last chorus only: an organ line above the voice", "C": "every chorus, growing (slide guitar)"},
            "recommended": "A", "answer": "B"})
COUNTER = "last chorus only: organ above the voice (design, 235)"
LOG.append({"q": "19 (236)", "topic": "drum design", "options": {"A": "not chosen: the kit follows the chosen sound (brushes in the verses, sticks from the first chorus, the shuffle throughout, a fill at each section's end) (default path)",
            "B": "the groove stiffens from verse 2 through the bridge, swing back at the gate (design)", "C": "drums out in the bridge (design)"}, "recommended": "A", "answer": "A"})
DRUMS = None
LOG.append({"q": "20 (230, 308)", "topic": "lines of 9+ syllables in the chosen form", "finding": "230's default gives a line of 9+ syllables four bars; 308 caps a long line at int(0.57n) syllables in any bar, so it needs two bars at least. The bridge (11,7,9,7,12,7) and verse 3 (12,6,9,5,8,9) need 9 bars each and cannot fit 8; the other sections fit with one-bar slots for short lines",
            "options": {"A": "bridge and verse 3 grow to 12 bars (every line two bars there); the rest stays; long lines in verses 1-2 and pre 1 take two bars by named design; 104 bars, about 4:20",
                        "B": "230's default throughout: 140 bars, about 5:50", "C": "keep 96 bars by cutting words in the bridge and verse 3 (unlocks the lyric)"},
            "recommended": "A", "answer": "A"})
SLOTS_DESIGN = "230 failed by a named design choice (Q20 A): 9-12-syllable lines take two bars; 6-8-syllable lines take one bar in verses 1-2"
