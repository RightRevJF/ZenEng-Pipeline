"""Song 43: intake. Every choice logged (question, options, recommendation, answer verbatim where the writer wrote words).
Words and music: Jason Bryant. The writer's sonnet is source material: read and used, never copied into the repo."""
SPEC = "ZenEng v113 (fixes 337-339 ported; findings from 340)"
LOG = []
LOG.append({"q": "1", "topic": "the idea", "options": {"A": "Ten and Two (a father teaching his kid to drive; heartland rock)", "B": "a congregational hymn of lament (SATB hymnal page)",
            "C": "Hold Music (wry up-tempo pop, a 1970s soft-rock era)"}, "recommended": "A",
            "answer": "his own: 'I want to turn this sonnet into a pop song. It's about a real incident that could be mined for further details' (the sonnet 'Blue Movie', not stored here)"})
SOURCE = "the writer's sonnet 'Blue Movie' (14 lines; a night in a cinema, then absence; the volta at 'Gone.'); a real incident"
TITLE = "Blue Movie (working)"
LOG.append({"q": "2", "topic": "how 'you' is gone", "options": {"A": "it ended between them (a breakup or drifting apart)", "B": "they died", "C": "something else"}, "recommended": None, "answer": "A"})
LOG.append({"q": "3", "topic": "the posted sign's rules", "options": {"A": "pandemic rules at a reopened cinema", "B": "a costume night or a theater's house rules", "C": "in his words"},
            "recommended": None, "answer": "C: 'I don't remember. She took a photograph of it though'"})
LOG.append({"q": "4", "topic": "where the photograph is now", "options": {"A": "still on his phone", "B": "she has it; he only knows it exists", "C": "in his words"}, "recommended": None, "answer": "B"})
LOG.append({"q": "5", "topic": "what was playing", "options": {"A": "neither watched it", "B": "he remembers the film", "C": "a scene, a colour, a sound"}, "recommended": None,
            "answer": "B: 'It was a porno, a lithe blonde and a swarthy man.'"})
LOG.append({"q": "6", "topic": "how it ended", "options": {"A": "she left", "B": "he left", "C": "it wore out, or his words"}, "recommended": None,
            "answer": "C: 'It was an affair and her husband figured it out. The song should be about the theater though.'"})
LOG.append({"q": "7", "topic": "how much of the after", "options": {"A": "the whole song is that night, present tense; the after only as a shadow in the last line",
            "B": "verses in the theater, the chorus in the now", "C": "the theater as the photograph she kept"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "8", "topic": "sound and pace", "options": {"A": "slow-burning synth-pop, q = 96, straight", "B": "sultry R&B-pop, q = 72, straight (no swing table)", "C": "up-tempo dance-pop, q = 118, four on the floor"},
            "recommended": "A", "answer": "C: 'This is an uptempo pop song about two normal people engaging in some very naughty behavior and enjoying every minute of it. The longing can be in the background or eliminated if it muddles the pop song. I'd prefer to keep both though, the heat and the longing without lapsing into a story ... which pop doesn't do very well'"})
LOG.append({"q": "9", "topic": "form", "options": {"A": "88 bars, 3:00: Intro 8, V1 8, Pre 4, Ch 8, Post 4, V2 8, Pre 4, Ch 8, Post 4, Bridge 8, Last Ch 8, Post 4, Outro 4",
            "B": "the same without the post-chorus, 76 bars", "C": "chorus first"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "10", "topic": "voice and key", "options": {"A": "a man, light tenor, row C3-A4, A minor", "B": "a man, baritone, row G2-E4, F minor", "C": "a woman, row G3-E5, D minor"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "11", "topic": "what the chorus says", "options": {"A": "they become the film: the couple on screen is the dull one; they are the blue movie",
            "B": "the rules, broken one by one (the red pen)", "C": "the loop: the film still runs and there isn't any screen"}, "recommended": "A", "answer": "A"})
TITLE = "Blue Movie"
FEEL = "up-tempo dance-pop, q = 118, four on the floor, straight"
FORM = [("Intro", 8), ("Verse 1", 8), ("Pre 1", 4), ("Chorus 1", 8), ("Post 1", 4), ("Verse 2", 8), ("Pre 2", 4), ("Chorus 2", 8), ("Post 2", 4),
        ("Bridge", 8), ("Last Chorus", 8), ("Post 3", 4), ("Outro", 4)]
VOICE = dict(kind="a man, light tenor", lo=48, hi=69, key="A minor")
BRIEF = "heat in front, longing underneath; no story; present tense in the theater; the after only in the last post-chorus"
NEVER_SAY = ["baby", "tonight", "fire", "burn", "desire", "heaven", "sinner", "forbidden", "body", "touch"]
FORM_NOTE = "Q9 A was offered as '88 bars, about 3:00'; its sections sum to 80 bars, 2:43 at q = 118 (the session's arithmetic slip, told to the writer with draft 1)"
LOG.append({"q": "12", "topic": "draft 1: lock or notes", "options": {"A": "lock", "B": "notes", "C": "a second full draft to compare"}, "recommended": None,
            "answer": "notes (seven, numbered): 1 a more immediate, visual opening ('We slipped in late beneath the neon sign / you read the rules out loud and laughed at each' or 'We paid cash, kept our heads down past the sign / you read the rules and laughed at every breach'); 2 raise pre-chorus 2 ('Somebody shifts two rows behind / you bite my shoulder, laugh, and climb' or 'A lighter flicks two rows behind / you breathe a laugh against my neck and climb'); 3 a more singable bridge ('Don't let the house lights come up yet / don't let the credits start to roll / I'll know you like a tongue still knows / the empty socket of a tooth'); 4 the last chorus's last line 'starring only me and you'; 5 post-chorus 'Blue, blue, blue movie / no one else in the blue movie' (or 'just you and me in the blue movie'); 6 'Your mouth a red pen crossing out the rest' (or 'Your mouth the only rule that I would break'); 7 the last post-chorus 'The film still loops, there isn't any screen / you climb me still, scene after scene' (or 'Just you on me, scene after scene')"})
LOG.append({"q": "13", "topic": "draft 2: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "change one line"}, "recommended": None,
            "answer": "A, with a note for the music: 'The chorus needs to be extraordinarily melodic. The words are simple enough, but the title phrase needs to become an earworm. I'd imagine \"blue movie\" as a strong melodic descent or repeated rhythmic figure, with a contrasting lift on \"starring nobody but you.\" The post-chorus could then become almost chant-like. I would not make the lyric more conventional. Its unusual combination of humor, eroticism, and absence is precisely what distinguishes it'"})
CHORUS_DESIGN = "'blue movie' a strong melodic descent or a repeated rhythmic figure; a contrasting lift on 'starring nobody but you'; the post-chorus near-chant (Q13 note)"
DENSITY_342 = {"Verse 1": 4.50, "Pre 1": 4.50, "Chorus": 3.75, "Post": 3.25, "Verse 2": 4.00, "Pre 2": 4.00, "Bridge": 4.00, "Last post": 4.50, "song": 3.94, "kept notes a bar": (3.6, 4.1)}
LOG.append({"q": "14 (342)", "topic": "the lyric's density", "options": {"A": "keep as written, a named choice (song 3.94 syllables a bar; kept 3.6-4.1 notes a bar; verse 1, pre 1 and the last post 4.5)",
            "B": "verse 1 to 10 bars (its long lines three bars each)", "C": "cut the opening lines to 8 syllables"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "15", "topic": "the chorus design (Q13 note)", "options": {"A": "'blue movie, blue movie' one rhythmic figure twice, the second a step lower (a falling sequence from the chorus's high note); 'starring nobody but you' lifts back to it; the post-chorus chants the figure (design gate)",
            "B": "one continuous fall through a fifth, then the lift; the post-chorus on one note", "C": "the default path, printed against the note"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "16", "topic": "arrangement", "options": {"A": "four-on-the-floor kick, off-beat open hats, eighth-note synth bass, a plucked synth playing the 'blue movie' figure in the intro and post-choruses, a flickering pad; drums out for the bridge, all back for the last chorus",
            "B": "disco-leaning: octave bass guitar, string stabs, scratch guitar", "C": "minimal: kick, bass, one synth, the voice"}, "recommended": "A",
            "answer": "A: 'I'd especially like this one to be in the vein on similar known contemporary hits.'"})
LOG.append({"q": "17", "topic": "the lead reference", "options": {"A": "Dua Lipa, 'Houdini' (117 BPM, D minor)", "B": "Troye Sivan, 'Rush' (126 BPM, house-pop)", "C": "Ariana Grande, 'yes, and?' (119 BPM, pop-house)"},
            "recommended": "A", "answer": "A"})
PLACE = "centre (314/333 default; told to the writer)"
REFERENCES = ["Dua Lipa, 'Houdini' (lead)", "Troye Sivan, 'Rush'", "Ariana Grande, 'yes, and?'"]
LOG.append({"q": "18 (255)", "topic": "the pick", "options": {"A": "the judge's first, dc24946f27cb (judge 4.55, content 4.54; the figure from G4)",
            "B": "the pick of record by 255 as it stands, 840d7b4af214 (repeats 51%/48% of moves, kept 75th 40%)", "C": "the composite's first inside the kept repeats, 8c54529c4c9d (judge 1.76)"},
            "recommended": "A", "answer": "A"})
