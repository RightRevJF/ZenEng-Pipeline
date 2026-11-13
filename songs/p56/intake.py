"""Song 46 intake (dir p56). Every choice logged (the writer's standing ask).
Engine: ZenEng v130 (Module 27.74). The next song (522): default path, 438 chart with 440's step
tested on the finished chart, bass by the routine (538 on four-kick songs), record built from both.
Form rule 524: a line of nine syllables or more gets a slot of three bars or more where the lyric allows."""
WRITER_BRIEF = None
LOG = [{"q": "where the song comes from",
        "options": {"A": "you give me the story or brief in your own words",
                    "B": "from one of your poems, sermons or book chapters (attach it)",
                    "C": "I offer three subjects and you pick"},
        "recommended": "A", "answer": "B"}]
SOURCE_MATERIAL = "the writer's sonnet \"Ark\" (src/ark.txt, not committed): three quatrains of \"Give me\" and a couplet; a car, a flood, a dove, a library aground, Noah"
LOG.append({"q": "how the song uses the poem", "options": {"A": "keep the poem's lines as the verses, cut to fit; write a new chorus from the couplet", "B": "keep its images and story, write new singable lines throughout", "C": "set the sonnet whole as written, verses only, no chorus"}, "recommended": "A", "answer": "B"})
LOG.append({"q": "whose voice", "options": {"A": "his voice alone, singing to her as the poem does", "B": "a duet: her verses answer his, the chorus shared", "C": "a narrator telling both, third person"}, "recommended": "A", "answer": "A", "writer": "The key will be bringing the ark imagery subtly to light.  The idea is that the affair was the flood and now, on set ground, Noah misses the water, so to speak.  Things are safer but far less exciting and enjoyable.  Did that come through in the sonnet?"})
LOG.append({"q": "sound", "options": {"A": "dark slow R&B: Rhodes, sub bass, soft programmed drums, rain in the room", "B": "Americana: acoustic guitar, pedal steel, low tremolo electric", "C": "atmospheric pop: pulsing synths, four-on-the-floor kick, the flood as a dance"}, "recommended": "A", "answer": "C", "note": "four kicks to the bar: 538 applies to the bass"})
LOG.append({"q": "voice (11.2)", "options": {"A": "tenor, about C3-A4, falsetto B4 once in the last chorus", "B": "baritone, about A2-E4", "C": "high tenor, E3-B4, chorus in falsetto"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "tempo and feel", "options": {"A": "4/4 q=118, steady four-on-the-floor, the verses sung long over a fast pulse", "B": "4/4 q=124, driving club pulse throughout", "C": "4/4 q=104, slower pulse, the kick drops out in the verses and lands in the chorus"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "form", "options": {"A": "Verse 1 (the flood: the car) / Pre / Chorus / Verse 2 (her, the dove) / Pre / Chorus / Bridge (the dry ground, the rainbow) / Last Chorus / Outro", "B": "Verse / Chorus x2, Bridge, Chorus; no pre-chorus", "C": "Verse 1 and Verse 2 in the flood, then one chorus on dry ground, repeated at the end"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "Ark", "B": "Dry Ground", "C": "Miss the Water"}, "recommended": "B", "answer": "B"})
TITLE = "Dry Ground"
LOG.append({"q": "how openly the ark is named", "options": {"A": "never name it: no Noah, ark, flood or dove, only images (rain, water rising, the bird, the leaf, the bow, dry ground)", "B": "plain words allowed (flood, dove, rainbow) but never Noah, ark or forty days", "C": "name Noah once, in the bridge, as the poem does"}, "recommended": "B", "answer": "B or C", "writer": "B or C.  I’ll look at the lyrics you write and choose"})
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "answer": "C chosen for the ark naming: the one Noah line in the bridge; notes to come", "writer": "I like the one Noah reference.  But I’ve got some notes for the lyrics."})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "change": "the bridge's last line is the C line (Noah)", "writer": "Okay.  Show me the full lyric with the noah line", "answer": None})
LOG[-1]["answer"] = "notes (verbatim in 'writer')"
LOG[-1]["writer_notes"] = """The first pre-chorus is solid but slightly softer than the rest of the writing. "The world could drown and we wouldn't know / Let it rise let it rise" is serviceable, but it doesn't quite match the precision of the verses or the bridge.
- The chorus is good but not yet inevitable. "Every board nailed safe and sound / There's a rainbow on the house, a promise" is clear, yet a touch more prosaic than the best lines around it. It does its job; it just doesn't yet have the same melodic or emotional lift that the verses and bridge suggest the song wants.
- The final chorus adds a third "I miss the water," which is understandable for emphasis, but the second one already does the work. The third can start to feel like it's pushing rather than landing.
- Outro is atmospheric and thematically right ("Roll the little window down / Let it in let it in"), but it risks feeling slightly abrupt or under-developed after the emotional peak of the bridge and last chorus."""
LOG.append({"q": "lyric draft 3", "file": "lyric_draft3.md", "changes": ["Pre 1 lines 3-4: The red brick swimming in the glass / Till the last dry thing went under (the brick foreshadows the library; the line answers Pre 2's 'So we went down again')", "Chorus lines 2-3: Every window painted shut / And the rainbow keeps its word (the shut windows against the quarter pane that gave; the rainbow's word is the vow)", "Last chorus: two 'I miss the water', not three", "Outro grows to four lines: he parks alone where they used to park, then rolls the window down"], "answer": None})
LOG[-1]["answer"] = "notes (verbatim in 'writer_notes')"
LOG[-1]["writer_notes"] = """The chorus is better, but still not quite at the level of the best writing in the song (the backbone/honey lines, the library image, "Noah stood there missing the rain"). It does its structural job cleanly; it just doesn't yet have the same inevitability or melodic magnetism those other sections suggest.
- "And the rainbow keeps its word" is good, but a hair abstract compared to the concrete images around it. It works, yet it doesn't quite sting the way the strongest lines do.
- The last chorus is identical to the first. That's fine for structure, but after the bridge's emotional peak, the final chorus could benefit from one small shift in the second half to keep it from feeling static."""
LOG.append({"q": "lyric draft 4", "file": "lyric_draft4.md", "changes": ["Chorus line 3: The sprinkler hangs a rainbow on the lawn (the only water left is tame; the rainbow made concrete)", "Last chorus line 4: I stand out in it till I'm soaked (he stands in the sprinkler)"], "answer": None})
LOG[-1]["answer"] = "five notes (summarised in 'writer_notes'; full text in the conversation)"
LOG[-1]["writer_notes"] = ["1. Sharpen the chorus button: keep the repetition with a dramatic melodic move on the second 'water', or vary it, e.g. 'And I miss the water / God, I miss the flood' or 'I was made to drown'",
 "2. Clarify 'Mesh on the glass': e.g. 'Foil on the glass to hide the day' or 'Cardboard in the glass to hide the day'",
 "3. Pre-Chorus 2's opening is understated after Verse 2: lean into sensory/breath imagery, e.g. 'A sigh slipped out into the dark / A dove sent out to look for land'",
 "4. Bridge: tighten 'Sitting on its hill like it ran aground', e.g. 'High upon the hill like it ran aground'",
 "5. Outro: land like a thesis, e.g. 'Some days I park where we used to park / Same cold hum and an empty seat / Roll the little window down / And let the grey come in'"]
LOG.append({"q": "lyric draft 5", "file": "lyric_draft5.md", "changes": ["chorus button: God I miss the flood (his first example)", "Verse 1 line 2: Foil on the glass to hide the day (his example)", "Pre 2 line 1: The little coo you couldn't keep (from his sonnet; a dove's own sound, in place of 'A sigh slipped out into the dark', since the scene is an afternoon)", "Bridge line 2: High on the hill like it ran aground (his tightening, one word shorter)", "Outro: his four lines as written"], "answer": None})
LOG[-1]["answer"] = "Lock it!"
LYRIC_FILE = "lyric_locked.md"
LOG.append({"q": "key", "options": {"A": "A minor (tonic A3, verses low around C3-E4, chorus up to A4, falsetto B4 on the last 'flood')", "B": "F minor (darker, verses down to C3, chorus to Ab4)", "C": "C minor (brighter top, chorus sits around G4-Bb4)"}, "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
KEY = "A minor"
SYLLABLES = {"Verse 1": [8, 8, 9, 11], "Pre 1": [8, 8, 8, 8], "Chorus": [7, 7, 10, 8, 6, 5], "Verse 2": [8, 8, 9, 8], "Pre 2": [8, 8, 9, 6],
             "Bridge": [9, 9, 10, 9], "Last Chorus": [7, 7, 10, 8, 6, 5], "Outro": [9, 8, 7, 6]}   # the engine's syllable reading of the locked lyric
LOG.append({"q": "the form's bars (524: a line of nine syllables or more gets three bars or more)",
            "options": {"A": "three bars just where 524 asks, two elsewhere: Intro 8, Verse 2-2-3-3 (10), Pre 2-2-3-3 (10), Chorus 2-2-3-3-2-4 (16; 'flood' held four bars), Bridge 3-3-3-3 (12), Outro sung 3-3-2-4 (12); 120 bars, about 4:04",
                        "B": "everything in four-bar units, long lines four bars: Verse 2-2-4-4, Pre 2-2-4-4, Chorus 2-2-4-4-2-2, Bridge 4x4, Outro 4x4; 136 bars, about 4:37",
                        "C": "three bars for every line of the verses, pre-choruses and bridge (12 each), the chorus as A; 128 bars, about 4:20"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
SLOTS = {"Verse": [2, 2, 3, 3], "Pre": [2, 2, 3, 3], "Chorus": [2, 2, 3, 3, 2, 4], "Bridge": [3, 3, 3, 3], "Outro": [3, 3, 2, 4]}
FORM_BARS = 120
LOG.append({"q": "design: the chorus button ('And I miss the water / God I miss the flood')",
            "options": {"A": "choruses 1 and 2: 'water' on the chorus's high note, then 'flood' falls to the tonic A and holds (a sigh that lands); last chorus: 'flood' leaps to the falsetto B4 and holds",
                        "B": "every chorus: 'flood' leaps up to the top of the chorus and holds (a cry each time)",
                        "C": "the two lines one rhythmic figure sung twice, the second a step lower, 'flood' held on the tonic every time"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
LOG.append({"q": "arrangement",
            "options": {"A": "the flood sound: pulsing synth arpeggio and sidechained pads over the kick; the verses filtered as if underwater, opening wide at each chorus; rain in the intro; the bridge drops the kick (the dry ground); the last chorus full; the outro thins to a low hum and rain",
                        "B": "piano-house: stabbed piano chords, claps, a bright lead synth answering the voice, the same energy throughout with a breakdown before the last chorus",
                        "C": "minimal: kick, sub bass, one synth arpeggio and the voice, built a layer at a time to the last chorus"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
INSTRUMENT = "atmospheric pop: pulsing synth arpeggio, sidechained pads, four-on-the-floor kick, sub bass; verses filtered underwater, opening at each chorus; rain in the intro; the bridge drops the kick; the outro thins to a hum and rain"
NEVER_SAY = ["ark", "arks", "forty"]                     # Q9: plain words allowed (flood, dove, rainbow), Noah once (C), never the ark or forty days
NEVER_PHRASES = []
SINGERS = {"lead": "tenor C3-A4, falsetto B4 once (the last chorus's 'flood', Q12 A)"}
WRITER_NOTES = ["Words and music: Jason Bryant"]
