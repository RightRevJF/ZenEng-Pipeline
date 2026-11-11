"""Song 42 intake (ZenEng v110; the default path in a straight feel). Words and music: Jason Bryant."""
SPEC = "ZenEng v110"
BRIEF = {"class": "pop or rock, 4/4", "feel": "straight eighths (no swing: 318 waits for a table)",
         "default path": "no era, character, summit or lift chosen; the song's range centred in the row unless chosen (314)",
         "runs": "1000 main, 1000 control (243 off), each twice; the table of 310-321 on this song's own runs (321); findings from 322"}
LOG = []
SOURCE = "Resurrection-Shaped Architecture (Jason Bryant; RSA_Zygon_Submission.docx, attached 11 Nov 2026): read, used abstractly (the part holds the whole; identity survives its substrate; known by voice), not copied into the repo"
LOG.append({"q": "1", "topic": "the idea", "options": {"A": "Second-Hand Piano", "B": "Porch Light", "C": "Two Towns, One Weather Report"}, "recommended": "A",
            "answer": "What about this. Is there a song in there? (RSA_Zygon_Submission.docx)"})
LOG.append({"q": "1 (revised)", "topic": "which way into the paper", "options": {"A": "The Voicemail: twelve seconds of his voice; all of him in it; the hope of hearing the rest",
            "B": "Not Too Steady: a heart monitor; a good life lives at the edge", "C": "Written to Be Read: the world written to be read"}, "recommended": "A",
            "answer": "I like A but I'm not sure that it won't be too explanatory and not deep enough."})
LOG.append({"q": "2", "topic": "which voicemail", "options": {"A": "the phone is dying: she lets it go; afterward she can still hear him (the pattern outlived what carried it), done as an act, never explained",
            "B": "recognition: memorizing him to know him again", "C": "his side: the throwaway message itself"}, "recommended": "A",
            "answer": "A. The difficulty will be explaining what's going on in such a way to allow the deeper meaning to shine through."})
LOG.append({"q": "3", "topic": "making the situation clear", "options": {"A": "the chorus is his message word for word, plain speech; verses in concrete scenes; the same words mean more each time",
            "B": "she speaks to him", "C": "a narrator at the repair counter"}, "recommended": "A",
            "answer": "A. But the chorus can't be cheesy or reduced to cliche or overworked images"})
CHORUS_RULE = "the chorus is his plain message; no cliche, no overworked images (the writer, Q3)"
LOG.append({"q": "4", "topic": "his message and the title", "options": {"A": "Nothing Important: 'Hey, it's me. Nothing important. Just wanted to hear you. Call me back.'",
            "B": "It's Me", "C": "When You Get This"}, "recommended": "A", "answer": "A"})
TITLE = "Nothing Important"
MESSAGE = "Hey, it's me. Nothing important. Just wanted to hear you. Call me back."
LOG.append({"q": "5", "topic": "sound and pace (straight feel)", "options": {"A": "piano ballad that opens up, q = 76: straight piano eighths; cello from verse 2; the band (bass, brushes into sticks, guitar) only at the last chorus",
            "B": "fingerpicked acoustic folk-pop, q = 92", "C": "mid-tempo pop-rock, q = 108"}, "recommended": "A", "answer": "A"})
FEEL = "straight eighths, q = 76"
LOG.append({"q": "6", "topic": "form", "options": {"A": "68 bars, 3:35: Intro 4, V1 8, Ch 8, V2 8, Ch 8, Bridge 8, V3 8, Last Ch 12, Outro 4",
            "B": "76 bars, 4:00: with 4-bar pre-choruses", "C": "56 bars, 3:00: no bridge"}, "recommended": "A", "answer": "A",
            "story": "V1 the message and what is in it; V2 the phone failing, the repair counter; bridge the last night, the last play; V3 after: the phone gone, she can still hear him; last chorus 12"})
FORM = [("Intro", 4), ("Verse 1", 8), ("Chorus 1", 8), ("Verse 2", 8), ("Chorus 2", 8), ("Bridge", 8), ("Verse 3", 8), ("Last Chorus", 12), ("Outro", 4)]
LOG.append({"q": "7", "topic": "voice and key", "options": {"A": "a woman, warm alto, B-flat major, row F3-D5", "B": "a woman, mezzo-soprano, D major, row A3-E5",
            "C": "a man, baritone, G major, row G2-E4, roles reversed"}, "recommended": "A",
            "answer": "A. And make sure the piano part is a full song so that a singular performer on a piano could play the thing without any further instrumentation"})
VOICE = dict(lo=53, hi=74, key="B-flat major", kind="female alto, warm and plain")
PIANO = "a complete solo piano part: one player at the piano can perform the whole song with the voice and nothing else; the band is added on top (the writer, Q7)"
LOG.append({"q": "8 (314)", "topic": "where the song sits in her row", "options": {"A": "centred (default): about 2 semitones spare above and below", "B": "low: F3 to about B-flat 4", "C": "high: about A3 to D5"},
            "recommended": "A", "answer": "A"})
PLACE = "centre"
LOG.append({"q": "9", "topic": "never-say", "options": {"A": "fully hidden: no church or afterlife words, no grief cliches, no science words; never named as dead",
            "B": "hidden, with one faint echo allowed (an ordinary word a listener of faith might hear twice)", "C": "lighter: only grief cliches banned"},
            "recommended": "A", "answer": "B. Again, the absolute goal is to have a song that teaches the resurrection without ever mentioning it. Do you think you can do that?"})
GOAL = "a song that teaches the resurrection without ever mentioning it (the writer, Q9)"
NEVER_SAY = ["heaven", "angel", "angels", "soul", "pray", "prayer", "god", "lord", "jesus", "christ", "rise", "risen", "resurrection", "eternal", "forever", "beyond",
             "grave", "tomb", "funeral", "died", "dead", "death", "pattern", "signal", "frequency", "wave", "spirit", "ghost", "miracle", "faith", "believe"]
NEVER_PHRASES = ["gone too soon", "in my heart", "watching over me", "never really gone", "i can still hear your voice", "better place", "rest in peace",
                 "see you again", "until we meet", "up above", "one day we'll"]
ECHO_ALLOWED = "one faint echo (for example 'the third morning'), never explained"
LOG.append({"q": "10 (213)", "topic": "which section says it twice", "options": {"A": "the chorus: 'Hey, it's me' returns word for word; sets up the last chorus's one changed line",
            "B": "the verse", "C": "the bridge"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "11", "topic": "draft 1: lock or notes", "options": {"A": "lock", "B": "notes", "C": "a second full draft to compare"}, "recommended": None, "answer": "B",
            "notes": "1 V1 L2 'one saved message from March ninth'. 2 Bridge L3 'the blinker and the laugh on Seventh Street' (or 'his laugh and that light on Seventh Street'). 3 V3 give the turn more air: 'then the third morning at the sink I heard him - the laugh before he said hello'. 4 Last chorus: keep the words; hold 'Nothing important' longer and let 'I'll call you back' fall more quietly (delivery, re-breaking). 5 One quiet marker of who he is, in V1 or the bridge (e.g. 'and he laughs the way he always did before he says hello')."})
DELIVERY = "last chorus: 'Nothing important' held longer; 'I'll call you back' falls quietly (the writer, Q11 note 4)"
LOG.append({"q": "12", "topic": "draft 2: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "a different relationship marker"}, "recommended": None, "answer": "A"})
LOG.append({"q": "13 (230)", "topic": "room for the long lines", "options": {"A": "two bars a line as the form is (68 bars, 3:35); 230 failed by named design; the last three short lines two bars each",
            "B": "230's default: 104 bars, about 5:30", "C": "split the long lines (about 4:30)"}, "recommended": "A", "answer": "A"})
SLOTS_DESIGN = "230 failed by a named design choice (Q13 A): every line two bars; 9-12-syllable lines two bars"
LOG.append({"q": "14 (235)", "topic": "the cello", "options": {"A": "holds in verse 2 and the choruses; a quiet countermelody answering the voice in its gaps in the bridge and the last chorus (design)",
            "B": "holds only (default path)", "C": "countermelody from verse 2 on"}, "recommended": "A", "answer": "A"})
COUNTER = "cello: holds in verse 2 and choruses 1-2; countermelody in the voice's gaps in the bridge and the last chorus (design, 235)"
LOG.append({"q": "15 (208)", "topic": "bridge register", "options": {"A": "drawn as kept songs do (default path)", "B": "below the verse (design)", "C": "above the verse (design)"},
            "recommended": "A", "answer": "A"})
