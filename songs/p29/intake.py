"""Song 29 intake. Every choice logged (the writer's standing ask)."""
WRITER_BRIEF = """Now I want to write the best Christmas song ever. The idea would be to have a song with exceedingly memorable words about the
Incarnation and its having perfectly paired with the music. Imagine something that soloists would die for to sing, a real tour de force.
But it MUST avoid being saccharine or cliche"""
LOG = [{"q": "source", "writer": WRITER_BRIEF,
        "constraints": ["the Incarnation", "exceedingly memorable words", "words and music perfectly paired", "a soloist's tour de force", "never saccharine or cliché"]}]
TITLE = None
LOG.append({'q': 'which part of the Incarnation', 'options': {'A': "the Word that can't say a word (Andrewes 1618, Verbum infans): the voice that spoke the stars learning his mother's language", 'B': 'the hands: shaped the world, too small to hold a finger, nailed open', 'C': 'creation receiving its maker'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'what kind of song', 'options': {'A': "a concert carol in the 'O Holy Night' lineage: piano and strings (orchestra possible), a trained voice, a long climb to one great final note", 'B': 'contemporary ballad: piano, strings, a building band', 'C': 'gospel: piano, Hammond, a choir answering'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'voice (11.2; a concert row the table lacks)', 'options': {'A': 'high voice: written for soprano C4-A5, B-flat5 once at the climax; a tenor sings it an octave lower', 'B': 'low voice: mezzo or baritone A3-F5, G5 once', 'C': 'soprano only, C4-B-flat5, C6 possible'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'tempo and feel', 'options': {'A': '3/4 at q=66, a lullaby sway; the final section broadens to q=56', 'B': '12/8 at dotted-q=50', 'C': '4/4 at q=60, hymn-like'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'title', 'options': {'A': 'The Word Without a Word', 'B': 'Verbum Infans', 'C': 'First Word'}, 'recommended': 'A', 'answer': 'A',
            'writer_adds': "I want to see a lyric draft before the music comes and, like the last piece, I'll need a full score"})
TITLE = "The Breath That Made the World"
# ---- derived (provisional until the lyric) ----
OBJECTS = ["light", "call", "trough", "word", "chest", "breath", "world", "bread", "crumb", "tongue", "hand", "rain", "stars", "mount", "milk", "spit", "sound", "ear", "mother"]; WRITER_PHRASES = []; WRITER_WORDS = []; LEXICON = {}; ROLES = {"verse", "chorus", "bridge", "refrain", "hook", "tag"}
NEVER_SAY = ["silent", "precious", "lowly", "manger", "angel", "angels", "sweet", "tender", "miracle", "gift", "christmas", "jingle", "glory", "hallelujah"]   # the run's default list, shown with draft 1
NEVER_PHRASES = ["holy night", "little baby", "born to die", "baby boy", "on this night", "mary did you know", "joy to the world", "silent night"]
LOG.append({'q': 'form (lengths at q=66, the end at q=56; the longest line printed: 11 syllables in two bars, 13 at q=56; fixes 13/31/56)', 'options': {'A': '64 bars, about 3:00: intro, verse, refrain, verse, refrain, bridge, verse 3, final refrain broadened, coda', 'B': '80 bars, about 3:45: intro, V, R, V, R, 8-bar interlude, V3, bridge, V4, final refrain broadened to q=56, coda', 'C': '88 bars, about 4:10: through-composed, five stanzas, four bars a line'}, 'recommended': 'B', 'answer': 'B'})
LOG.append({'q': 'key', 'options': {'A': 'Db major, lifting a whole step to Eb for verse 4 and the final refrain; the Bb5 on the fifth of Eb', 'B': 'Eb throughout, no lift', 'C': 'Bb major lifting to C'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'lyric draft 1', 'options': {'A': 'lock', 'B': 'notes', 'C': 'a different refrain'}, 'recommended': 'B', 'answer': 'notes',
            'writer': "1 verse 2 more concrete and bodily: specific maternal actions, the baby's experience (bread's texture, rain on skin, held up to the night sky); 2 verse 3: the infant mouth struggling with consonants, the spit, failed attempts, the mother's patient repetition; 3 give the interlude a dramatic or musical job; 4 verse 4: stay longer in the cry before the summary; 5 test every line for hymn diction vs song diction ('the Speech that cannot speak', 'before the worlds', 'when all is said and done')"})
LOG.append({'q': 'lyric draft 2', 'options': {'A': 'lock', 'B': 'more notes', 'C': 'lock, flag weak lines first'}, 'recommended': 'A', 'answer': 'notes',
            'writer': "1 soften 'he's called his Father that forever' (trust 'Now: Abba'); 2 'works milk and spit into a sound' may crowd the melody; 3 one more sensory detail in verse 4 (the cry shaking his body, against her collarbone); 4 'breathes in, and out, and stays' may over-resolve; the earlier refrain's openness was useful; 5 'ma' and 'Abba' are structural anchors: tell the arranger"})
LOG.append({'q': 'lyric draft 3', 'options': {'A': 'lock and write the music', 'B': 'more notes', 'C': 'lock, flag weak lines first'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'music built', 'result': "pick f10477ea1784 (#3 of the frozen ranking: the floor 'verse 4 reaches Eb5' added after the run; no hand edits); 80 bars, 3:44; lead sheet, full score, Nashville chart, songbook + production notes, test report; consistency 30/30"})
LOG.append({'q': 'producer one-sheet (writer: "Is this something that would help a producer? ... add it to the songbook")', 'options': {'A': 'add it to this songbook now and make it standard (skill and fix list)', 'B': 'this songbook only, as a trial', 'C': 'let it replace the production brief'}, 'recommended': 'A', 'answer': 'A'})

LOG.append({"q": "blind pick (10.20), asked after song 31", "options": {"A": "The voice that said, Let there be light (Annotated top)", "B": "The Word without a word (Remembered top)", "C": "the breath that made the world (middle)"}, "answer": "B"})
BLIND_PICK = ("B", "The Word without a word -- the Remembered top (the title line)")
LOG.append({"q": "revision (8 Nov): the writer attached five notes (memorability and casting, measured against 'O Holy Night')",
            "options": {"A": "all five, then rebuild the full package with parts", "B": "move 1 first, shown before anything else", "C": "moves 2-5 only (the melody untouched)"},
            "recommended": "A", "answer": "A",
            "notes": ["1 plant the refrain's seed in the verses", "2 the cello answers the voice in verses 2-3", "3 the interlude varies one note",
                      "4 an A-flat5 ossia and a co-equal tenor edition", "5 the coda quotes the refrain; B-flat on top of the last chord"]})
REVISION = 1
LOG.append({"q": "retitle (8 Nov, after revision 1)", "writer": "I love the song, dislike the title. It needs to be stickier.",
            "his options": ["The Breath That Made the World", "And Joseph Turns", "The Word Without a Word", "Abba", "Bread", "Let There Be Light"],
            "run's five": ["What God Meant to Say", "Sleeping on Her Chest", "His Mother Hears", "First Word", "Half a Sound"],
            "options": {"A": "The Breath That Made the World", "B": "What God Meant to Say", "C": "something else / keep"}, "recommended": "A", "answer": "A"})
TITLE = "The Breath That Made the World"
