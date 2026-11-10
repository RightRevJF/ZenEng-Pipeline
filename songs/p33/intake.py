"""Song 33 intake (ZenEng v74: v64 + the fix list of songs 21-32 in v65-v71 + v72-v74's ranking and word norms). One question a turn,
three options, logged. The brief: a test of v74 by writing a song -- chosen to exercise what has never run as code."""
LOG = []
TITLE = None
LOG.append({"q": "goal", "answer": "Here's the latest engine. Way to test it by writing another song?"})
LOG.append({"q": 1, "topic": "what kind of song (a test of v74)",
            "options": {"A": "an up-tempo band song in 4/4 (pop-rock or country-rock): a riff built from the title, a designed drop before the last chorus, the senses dial set 'to hit' -- exercises 22, 23, 60, 78, 87, 88, the 27.22 gate and flags",
                        "B": "a 3/4 waltz duet (folk or Americana), two singers trading lines then together -- 16, the duet harmony rule, 74, 9 and 57",
                        "C": "the writer's own brief, the test fitted around it"},
            "recommended": "A", "answer": "A"})
TEMPLATE = "song 31 (a band song: drums, bass, guitars, keys; 4/4; cuts) with song 32's stress rules"
LOG.append({"q": 2, "topic": "what the song is about",
            "options": {"A": "Friday night lights: the whole town in the bleachers, cold air, stomping, everybody shouting one name; a country-rock anthem", "B": "the last shift: clocking out for good after thirty years", "C": "the kitchen floor: a couple dancing to the radio after the kids are asleep"},
            "recommended": "A", "answer": "A"})
PRIOR_ART = {"high school football, the town in the stands": "worn (fix 72): Kenny Chesney 'The Boys of Fall' (2010), Brantley Gilbert 'Friday Night', Billy Currington 'Drinkin' Town with a Football Problem' (2015), Jimmie Allen 'Big in a Small Town' -- a fresh angle required",
             "'Maddie Ray'": "no song found, but next to the duo Maddie & Tae; not used", "'Sadie'": "older songs by the name (the Spinners, the Beatles' 'Sexy Sadie'); no country football song"}
LOG.append({"q": 3, "topic": "the fresh angle (fix 72: the image is worn)",
            "options": {"A": "the kicker is a girl, the only one on the team; it comes down to her kick; her father sings from the stands (he never made the team); the name the town shouts is hers", "B": "the band drummer who never watches a down", "C": "the announcer calling his last game after forty years"},
            "recommended": "A", "answer": "A"})
Q0 = ("the kick", "a father in the stands while his daughter, the team's only girl, lines up the kick that decides the game, and the whole town shouts her name")
LOG.append({"q": 4, "topic": "the turn",
            "options": {"A": "she misses and the town shouts her name anyway", "B": "she makes it", "C": "the song never tells: the drop is the ball in the air, the band cut out; the last chorus is the town on its feet with her name -- the kick was never the point"},
            "recommended": "C", "answer": "C"})
TURN = "the song never tells whether the kick is good: the drop is the ball in the air; the last chorus is the town with her name"
LOG.append({"q": 5, "topic": "title (fix 94)",
            "options": {"A": "Sadie (her name: two syllables, stress first, a chant; shouted on the top note of every chorus)", "B": "Kick It Through", "C": "The Whole Town Knows Her Name"},
            "recommended": "A", "answer": "A"})
TITLE = "Sadie"
LOG.append({"q": 6, "topic": "who sings (11.2 rows, fix 25)",
            "options": {"A": "a male country-rock baritone lead (about A2-E4, one F#4), her father; a gang shouts 'Sadie' in every chorus; the whole crowd sings the last chorus in unison and the octave below", "B": "a male tenor lead (C3-A4) with the same gang", "C": "a male lead, no gang"},
            "recommended": "A", "answer": "A"})
SINGERS = {"him": "her father, male country-rock baritone, A2-E4 (one F#4)", "gang": "'Sadie' in every chorus; the whole last chorus in unison and the octave below"}
LOG.append({"q": 7, "topic": "tempo and feel",
            "options": {"A": "4/4 at q = 124, straight eighths, A major; palm-muted verses, four-on-the-floor choruses; the riff on the open A and E strings", "B": "a half-time stomp at q = 92 in E", "C": "a shuffle at q = 140 in G"},
            "recommended": "A", "answer": "A"})
FEEL = {"meter": "4/4", "qbpm": 124, "key": "A major", "feel": "straight eighths; palm-muted verses, four-on-the-floor choruses"}
LOG.append({"q": 8, "topic": "form (fix 13/31/56: two bars a line hold about 13 syllables at q = 124)",
            "options": {"A": "Intro 8 | V1 8 | Pre 4 | Ch 8 | Riff 4 | V2 8 | Pre 4 | Ch 8 | Bridge 8 | Drop 4 | Ch 8 | Last Ch 8 | Outro 4 = 88 bars, about 2:50", "B": "no pre-chorus, three verses, 68 bars, about 2:12", "C": "A plus a third verse and a post-chorus chant, about 104 bars, 3:20"},
            "recommended": "A", "answer": "A. Don't forget I want to see a draft of the lyrics before you go to music"})
FORM_PLAN = "Intro 8 | V1 8 | Pre 4 | Ch 8 | Riff 4 | V2 8 | Pre 4 | Ch 8 | Bridge 8 | Drop 4 | Ch 8 | Last Ch 8 | Outro 8 = 88 bars, about 2:50 (the option printed Outro 4 and 88 bars; the sum was 84, so the outro takes 8 to keep the length offered -- a finding)"
LOG.append({"q": 9, "topic": "never say",
            "options": {"A": "the football-song cliches: Friday night lights, small town, hometown, boys of fall, under the lights, glory days, legend, hero, touchdown, dirt road, tailgate, pickup, cold beer, in my blood, football and Jesus, the whole town came out", "B": "list A, but allow 'Friday night'", "C": "no list"},
            "recommended": "A", "answer": "B"})
NEVER_SAY = ["legend", "hero", "touchdown", "tailgate", "pickup", "hometown"]
NEVER_PHRASES = ["friday night lights", "small town", "boys of fall", "under the lights", "glory days", "dirt road", "cold beer", "in my blood", "football and jesus", "the whole town came out"]
LOG.append({"q": 10, "topic": "commercial profile (fixes 71, 80)",
            "options": {"A": "country radio, 2020s: hold the norms (about 2:50-3:15, the title in the chorus's first line, the first chorus by about 0:40 -- this form reaches it at 0:39 -- a four-chord loop under the chorus); depart in two designed places: the drop (four near-silent bars) and the unresolved kick", "B": "arena rock", "C": "no commercial profile"},
            "recommended": "A", "answer": "A"})
COMMERCIAL = {"profile": "country radio, 2020s", "hold": ["2:50-3:15", "title in the chorus's first line", "first chorus by 0:40", "four-chord loop under the chorus"], "depart": ["the drop: four near-silent bars", "the unresolved kick"]}
SENSES = "to hit (fix 115): the body senses over the eye -- cold, breath, hands, feet, sound"
OBJECTS = ["bleachers", "boot", "coffee cup", "rim", "number", "clothesline", "yard", "ball", "laces", "holder", "snap", "band", "nurse", "feet", "hands"]
WRITER_PHRASES = ["sadie"]
WRITER_WORDS = ["sadie"]
LEXICON = {}
ROLES = {"verse", "pre", "chorus", "hook", "bridge", "drop", "tag"}
INSTRUMENT = "country-rock band: drums, bass, two electric guitars (the riff; palm-muted rhythm), acoustic guitar, keys (organ pad), gang vocals"
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "room": "every line 8-11 syllables (two bars at q = 124 hold about 13); the senses dial to hit: body over eye (boot, chewed cup, hands raw, lips moving, feet, can't hear); one-hearing check (fix 107) by hand: 'I spelled it for a nurse' kept with 'when she was born' so the naming needs no inference",
 "answer": "notes: (1) rewrite or cut the pre-chorus (fix the grammar and reduce the direct backstory explanation); (2) clarify the clothesline image in verse 2 so 'them' has a clear antecedent; (3) sharpen one or two generic lines in the chorus without losing the plain voice; (4) protect the bridge, the four-bar drop ('It's up.') and the final-chorus line change -- they are already strong"})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "changes": ["pre-chorus: 'I'm in the jacket that I never lettered in, / and somebody behind me starts it up:' (the backstory one image; the chant begins)", "verse 2: 'She kicked a ball over the clothesline in the yard, / I held it for her till my hands went raw'", "chorus line 1: 'Stomping on the aluminum'; line 4: 'and back then it was only mine to say' (the last chorus's change kept)", "bridge, drop and last-chorus line untouched"],
 "answer": "notes in five vectors (another reader): (1) show-don't-tell texture in verse 1 (replace the score readout); (2) the father's quiet against the crowd ('I used to say it quiet so she'd stay asleep / now two thousand strangers got a piece to keep'); (3) name the rival ('The Miller boy laughed when her helmet was too big'); (4) tighten 'two thousand people hollering one name'; (5) resolve the kick ('End-over-end right through the yellow posts')"})
LOG.append({"q": "lyric draft 3", "changes": ["verse 1 line 4: 'and that's my daughter, eye black, number two' (the score line kept: the stakes on one hearing)", "chorus line 2: 'two thousand hollering her name'; line 3: 'I used to say it soft so she would sleep'", "verse 2: 'her first day out, the Miller boy laughed hard, / now he's the one down on a knee to hold the ball'", "vector 5 declined: it reverses the turn (C) and the writer's note 4"],
 "answer": "the one issue: 'Stomping on the aluminum' -- who's stomping? It reads as Sadie. If it's the crowd: 'Feet pounding the aluminum' -- clearer, more visual, more singable; test it against the melody before changing it"})
LOG.append({"q": "lyric draft 4", "file": "lyric_draft4.md", "changes": ["chorus line 1: 'Sadie! Sadie! Feet pounding the aluminum' (12 syllables like the old line; stresses SA, SA, FEET, POUND, LU: the five downbeat candidates; set in the melody)"], "answer": "A"})
LOG.append({"q": "ports at the lock", "ports": ["song 33 stress port: SOME-bod-y (finding)", "v72-v74: 27.22's register plan as a gate (110, 117), the composite ranking the gate's survivors (112, 118), landing and dull-line flags (109, 111, 119, 120), the top twenty kept and the search's rerun record (113, 121)"]})
LOG.append({"q": "blind pick (10.20)", "options": {"A": "the holder spins the laces round; (Annotated top)", "B": "Sadie! Sadie! Feet pounding the aluminum, (Remembered top)", "C": "The snap comes back and the band goes quiet, (middle)"}, "recommended": None, "answer": "A"})
LOG.append({"q": "fix list", "options": {"A": "start a new fix list Doc after v74, from song 33 (fixes 122-128)", "B": "add to the songs 21-32 Doc", "C": "hold until more songs"}, "recommended": "A", "answer": "A", "doc": "https://claude.ai/artifact/HwA8HAhon1GJf5MgkwHUt4"})
