# Song 36 intake (ZenEng v91): a test of fixes 181 and 182 (and 178-180, 184, 191-193) in the pop, rock and country class.
TITLE = None
LOG = []
LOG.append({"q": "goal", "answer": "Read the spec (ZenEng_v91.docx, version row v125, ends at fix 193; song 35's 178-187 are 184-193). Read the tables (zeneng_v88_tables.json, zeneng_v91_hymn_supplement.json), don't refit; the paper decides at an edge. Port 181, 182, 178-180, 184, 191-193 before the search. Write a pop, rock or country song; intake one question per turn; the full lyric draft before any music. Report: 181's phrase-design labels and stock share; 182's surprise and spread against 2.39-3.97 (median 2.96, p25 2.76), back-test median 2.53, repeats/steps/leaps vs 28/43/3%; exact bar repetition vs 38% (back-test 20%); a control with 181 and 182 off; deaths per gate with 184 controls; which fixes ran. Findings from 194. Don't edit the paper.",
            "reading": "class pop/rock/country; v91 the single source; tables v88 + v91 hymn supplement (sha256 561355b1..., e74e7c30...); findings from 194 (v91's last fix is 193: checked)"})
LOG.append({"q": 1, "topic": "which class", "options": {"A": "pop: verse-chorus-bridge, the hook on the title", "B": "rock: heartland anthem", "C": "country: mid-tempo story"}, "recommended": "A", "answer": "A"})
CLASS = "pop"
LOG.append({"q": 2, "topic": "the one moment (10.10)", "options": {"A": "driving someone to the airport at 5 a.m.", "B": "a kitchen dance at 2 a.m.: the fridge light, socks on the tile, the song you both know", "C": "an old voicemail never deleted"},
            "recommended": "A", "answer": "B. Dancing for the sheer joy of life seems like a good pop subject",
            "reading": "joy for its own sake; objects: fridge light, socks on the tile, a song"})
OBJECTS = ["fridge light", "socks on the tile", "the song"]
LOG.append({"q": 3, "topic": "who is dancing", "options": {"A": "you, alone: nobody watching, dishes done, the radio finds the song", "B": "two of you, years married", "C": "the whole house"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 4, "topic": "the turn", "options": {"A": "anyway: the day was hard (a bill on the counter, a call that went wrong); nothing fixed; dance anyway; joy chosen, not caused", "B": "no turn", "C": "someone sees"},
            "recommended": "A", "answer": "A. Joy of the face of everyday life! Songs almost counter cultural",
            "reading": "joy in the face of everyday life, chosen; the song almost counter-cultural; objects added: the unpaid bill on the counter, the phone call"})
OBJECTS += ["the bill on the counter", "the phone call"]
LOG.append({"q": 5, "topic": "title", "options": {"A": "Dance Anyway", "B": "Kitchen Light", "C": "Socks on the Tile"}, "recommended": "A", "answer": "A"})
TITLE = "Dance Anyway"
LOG.append({"q": 6, "topic": "who sings (11.2)", "options": {"A": "female mezzo pop, about A3-D5", "B": "male high tenor", "C": "duet in unison"}, "recommended": "A", "answer": "A"})
VOICE = "female mezzo pop, A3-D5"
LOG.append({"q": 7, "topic": "tempo, feel, key", "options": {"A": "4/4 q = 118, E-flat major, four-on-the-floor disco-pop", "B": "q = 104, D, half-time R&B-pop", "C": "q = 128, F, synth-pop"}, "recommended": "A", "answer": "A"})
FEEL = {"meter": "4/4", "qbpm": 118, "key": "E-flat major", "feel": "four-on-the-floor disco-pop: octave bass, sixteenth hats, piano stabs"}
LOG.append({"q": 8, "topic": "form (fix 139: summed and timed)", "options": {"A": "Intro 4 | V1 8 | Pre 4 | Ch 16 | V2 8 | Pre 4 | Ch 16 | Bridge 8 | Last Ch 16 | Outro 4 = 88 bars, about 2:59", "B": "no pre-chorus, 8-bar choruses: 64 bars, about 2:10", "C": "108 bars, about 3:40"}, "recommended": "A", "answer": "A"})
FORM_PLAN = [("Intro", 4), ("Verse 1", 8), ("Pre 1", 4), ("Chorus 1", 16), ("Verse 2", 8), ("Pre 2", 4), ("Chorus 2", 16), ("Bridge", 8), ("Last Chorus", 16), ("Outro", 4)]
assert sum(b for _, b in FORM_PLAN) == 88 and round(88 * 240 / 118) == 179
LOG.append({"q": 9, "topic": "never say", "options": {"A": "dance-pop cliches (tonight's the night, on the dance floor, lose control, feel the beat, move your body, dance like nobody's watching, good vibes, let it go, shake it off) and self-help words (self-care, healing, toxic, manifest)", "B": "only the dance-floor cliches", "C": "no list"},
            "recommended": "A", "answer": "A"})
NEVER_SAY = ["self-care", "healing", "toxic", "manifest"]
NEVER_PHRASES = ["tonight's the night", "on the dance floor", "lose control", "feel the beat", "move your body", "dance like nobody's watching", "good vibes", "let it go", "shake it off"]
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md",
            "answer": "notes: (1) sharpen one physical detail into the song's signature (the fridge door's sound, a particular light: under the microwave, streetlight through blinds, phone flashlight; one object that refuses to be ignored), let it recur or evolve; (2) the pre-chorus the most generic: make it the last breath before the decision (how long, the body before the mind, a twist); (3) the bridge explains: show the cost of waiting (a concrete memory, an image of wearing thin, a defiant turn); (4) the last chorus heavier: change one more image, the title varied and earned, a different colour; (5) protect 'my socks hit the tile like they've got somewhere to go'; 'the words I never get right' too soft; 'the whole wide world' abstract; the bill heavier each time"})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md",
            "answer": "(1) chorus soft phrasing: 'and I mean every one' explanatory; 'like the night's got nowhere else to be' more poetic than lived-in; (2) bridge a bit safe: one sharper sensory detail from that July night (the sound through the wall, the floor's temperature, what the dark felt like); (3) one sock vs two: lean in or 'socks'; (4) title: one more unexpected placement or variation so the final 'I dance anyway' is more hard-won; priorities: tighten written-sounding chorus lines; a precise physical memory in the bridge; decide the sock; every final-chorus line advances the image or deepens the cost"})
LOG.append({"q": "lyric draft 3", "file": "lyric_draft3.md",
            "answer": "(1) 'with the dish towel over my shoulder' the weakest addition: arbitrary, no emotional information, written for a video; (2) 'in my socks on the cold kitchen tile' prosaic after the verse's socks line; the chorus's second half longer and more explanatory than the first; (3) pre-chorus 2 ('daring me again') only a small variation; (4) the dish towel appears once and vanishes"})
LOG.append({"q": "lyric draft 4", "file": "lyric_draft4.md", "answer": "A", "locked": "lyric_draft4.md"})
WRITER_PHRASES = ["dance anyway"]
WRITER_WORDS = ["anyway"]
LEXICON = {}
ROLES = {"verse", "pre", "chorus", "hook", "bridge"}
COMMERCIAL = {"profile": "chart pop, 2020s", "hold": ["2:50-3:15", "title in the chorus's first line", "first chorus by 0:40 (0:33)"], "depart": []}
SENSES = "the green blink, the hum, socks on tile, the drip in the dark, the radio through the wall"
INSTRUMENT = "pop band: drums (four on the floor), bass (octaves), electric piano stabs, rhythm guitar, synth pad; female lead"
OBJECTS += ["microwave clock blinking twelve", "dishes", "radio", "bill stamped in red", "freezer dripping", "puddle by the door", "neighbors' radio through the wall"]
LOG.append({"q": "delivery", "answer": "delivered 10 Nov: demo, MIDI x2, lead sheet, parts, chart, songbook (Doc https://claude.ai/artifact/WawhreHv92GQd6Cn3ZAN26 + Word), test report; pick 862839a1b813"})
LOG.append({"q": "blind pick (10.20), offered", "options": {"A": "by the green of a clock stuck on twelve, (middle: top quartile under both)", "B": "the microwave's blinking twelve, been blinking since July; (annotated top)", "C": "yeah, I dance anyway, (remembered top)"}})
LOG.append({"q": "blind pick (10.20)", "answer": "A", "slot": "middle (top quartile under both)", "line": "by the green of a clock stuck on twelve,"})
LOG.append({"q": "fix list", "answer": "Now generate the fix list and the test results the other ai requested", "reading": "a new fix list Doc after v91, findings 194-203, with the requested test results"})
