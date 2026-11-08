"""Song 30 intake (ZenEng v64 + the v65 fix list, fixes 1-61). One question a turn, three options, logged.
The brief: a HIT. Genre open; the writer chose the hit lane after the catalog ranking (7 Nov 2026)."""
LOG = []
TITLE = None
LOG.append({"q": "goal", "answer": "I need a hit. Don't care what genre. What is our most likely path to that?",
            "reply": "country (2026's dominant lane), built for a 15-second clip, about 3 minutes, a real voice on the demo"})
LOG.append({"q": "path", "options": {"A": "song 30 from scratch, built for the lane", "B": "rework The Song You Sang Me as a hit cut", "C": "rank the catalog first"},
            "recommended": "A", "answer": "Ultimately A but I'd like to see how you rank what we've done so do C first"})
LOG.append({"q": "catalog ranking (C)", "top": ["Five-Oh-One", "Two Coffees, Black", "The Song You Sang Me", "Black 5000 (as country)", "All of It Was You (worship)"],
            "pattern": "one ordinary moment everyone has lived; the title on that moment; plain words"})
LOG.append({"q": "song 30 seed", "options": {"A": "fresh intake on the pattern: country, one universal moment, ~3:00, built for the clip",
            "B": "Black 5000's first-drive story as country", "C": "Five-Oh-One as country-pop"}, "recommended": "A", "answer": "A"})
BRIEF = {"lane": "country / country-pop", "length": "about 3:00, title inside the first 30 seconds", "clip": "one 15-second moment that stands alone as a video",
         "diction": "plain words that land on first hearing", "demo": "a real human vocal before anyone outside hears it"}
LOG.append({"q": 1, "topic": "the moment", "options": {"A": "the porch light: Mama left it on till you got home; now you leave it on for your own kid (clip: porch lights at night)",
            "B": "the truck-radio song that makes you seventeen again (clip: then/now photos)", "C": "small-town Friday night after the game (up-tempo; tailgates)"},
            "recommended": "A", "answer": "A"})
Q0 = ("porch light", "Mama left the porch light on till you got home; now you leave it on for your own kid")
LOG.append({"q": 2, "topic": "story shape", "options": {"A": "a lifetime in three verses: seventeen sneaking in under her light / the parent waiting up / she's gone and you still leave it on; the chorus deepens",
            "B": "one night as it happens: 1 a.m., waiting up, memories between looks at the driveway", "C": "the kid's side: grown, far away, realizing the light was her 'I love you'"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": 3, "topic": "feel and tempo", "options": {"A": "mid-tempo country, q~84: acoustic strum from bar 1, steel answering the lines, full band from chorus 1; ~3:10",
            "B": "slow piano-and-steel ballad, q~68", "C": "up-tempo heartland, q~110: sad words, driving beat"}, "recommended": "A", "answer": "A"})
FEEL = {"meter": "4/4", "qbpm": 84, "band": "acoustic strum, steel guitar, bass, drums, (piano/organ pad)", "target_len": "about 3:10"}
LOG.append({"q": 4, "topic": "voice (11.2)", "options": {"A": "male country voice B2-E4, F#4 once in the last chorus (the widest pool of country cuts)",
            "B": "female voice F3-C5", "C": "either: a narrow range, key set for the cut"}, "recommended": "A", "answer": "A"})
SINGERS = {"him": "male country voice, B2-E4, F#4 once (last chorus)"}
LOG.append({"q": 5, "topic": "title / hook line", "options": {"A": "She Left the Light On -- the last chorus turns to 'I leave the light on'",
            "B": "Porch Light", "C": "Till You're Home (flips: she's home now)"}, "recommended": "A", "answer": "A"})
TITLE = "She Left the Light On"
LOG.append({"q": 6, "topic": "form", "options": {"A": "V C V C B C: the bridge is the third chapter (she's gone, her porch dark); the last chorus flips; ~3:05",
            "B": "three full verses, a chorus after each; ~3:30", "C": "V C V C B V C; ~3:50"}, "recommended": "A", "answer": "A"})
FORM = ["Intro", "Verse 1", "Chorus 1", "Verse 2", "Chorus 2", "Bridge", "Chorus 3"]
LOG.append({"q": 7, "topic": "details", "options": {"A": "writer gives two or three real details", "B": "invented plain, universal details", "C": "one anchor detail from the writer"},
            "recommended": "A", "answer": "B because I don't have any ideas. But please, make them unique, memorable and not laughable nor cliche"})
DETAIL_RULE = "invented details: unique, memorable, never laughable, never cliche (writer)"
NEVER_SAY = ["moth", "moths", "angel", "angels", "heaven", "Jesus", "Lord", "pearly", "gates", "wings", "dirt road", "tailgate", "beer",
             "whiskey", "cold one", "Friday night", "small town", "country boy", "Chevy", "pickup", "truck bed", "rearview", "rear-view",
             "memory", "memories", "tears", "crying", "miss you", "beacon", "guiding light", "shining", "darkest night", "home sweet home"]
LOG.append({"q": 8, "topic": "how the bridge shows she's gone", "options": {"A": "never say it: the bulb burned out, nobody to change it, a stranger's light in her window",
            "B": "one plain line, no heaven imagery", "C": "name the day: the funeral and the drive home"}, "recommended": "A",
            "answer": "A. Before you draft, run a research on hit country music today, then on ways to make it judiciously more memorable -- music theory and contemporary hits -- the sweet spot of novelty AND success"})
HIT_RULES = {  # from the 7 Nov 2026 research (sources in the reply)
 "length": "under ~3:20; staying-power top-10 hits of 2025 averaged 3:17 vs 3:29 and were more often under 3:00",
 "intro": "short: staying-power hits averaged an 11-second intro; an instrumental guitar hook that returns in the vocal (Choosin' Texas)",
 "outro": "short (~0:19), may end unresolved/abrupt",
 "post-chorus": "a post-chorus 'hook center' was in 63% of 2025 top-10 hits",
 "repetition": "each extra chorus repetition raised odds of #1 by 14.5% (Nunes 2015); too much single-word repetition hurts",
 "melody": "earworms: common contour (rise then fall) + one distinctive leap or repeated-note cell (Jakubowski 2016); simple melodies (pop melodic complexity down ~30% since 1950)",
 "harmony": "pleasure = predictable then one surprise, or uncertain then resolved (Cheung 2019): diatonic I-IV-V-vi world with ONE borrowed chord at the turn",
 "rhythm": "rolling, conversational: held notes against quick syllable bursts; break the pattern before the chorus and at the closing hook",
 "delivery": "space and restraint; even-keeled delivery; let key lines breathe",
 "novelty": "a fresh take on a familiar theme (Texas vs Tennessee = a love triangle between places)",
 "turn": "country's twist: the final chorus means something new; title flip",
 "arrangement": "acoustic guitar (country #1s), drums present; strategic subtractions/additions at section joins (S.I.A.s)",
 "warning": "the porch-light image is well worn (Every Light in the House; Meanwhile Back at Mama's; many AI-generated porch-light songs): the song needs one detail nobody has used",
}
LOG.append({"q": 9, "topic": "the fresh angle", "options": {"A": "the electric bill on her empty house", "B": "the worn switch plate", "C": "the timer: he runs her porch light from a phone app, 300 miles away, at dusk"},
            "recommended": "A", "answer": "C"})
ANGLE = "her porch light runs from his phone (set up when her knees gave out); a year after, the button still says Mama's Porch and comes on at dark"
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "answer": None})
LOG[-1]["answer"] = ("A. Timeline clarity between Verse 2 and the bridge: verse 2 is present tense ('I light hers too at sundown'), the bridge reveals she's been gone a year; "
                     "a first-time listener may wonder whether he's lighting an empty house or the timeline jumped. A very light anchor in verse 2 (or one clarifying beat in the bridge).")
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "change": "verse 2 moved to the past ('got', 'stood', 'That was the year her knees gave out', 'lit'); the bridge's 'still' and 'a year' now read as now", "answer": None})
LOG.append({"q": "lyric lock", "options": {"A": "lock it and write the music", "B": "more notes", "C": "an alternate chorus"}, "recommended": "A",
            "answer": "A. Remember what you've learned on top of the engine. Make this a country hit"})
# ---- derived (run's port, v64 + v65 fixes 1-61 as ports) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 with the v65 fix list (fixes 1-61, songs 21-28) run as ports, plus the 7 Nov hit research (HIT_RULES)"
SOURCE_MATERIAL = "pitched subject (A, the porch light); invented details by the writer's rule; the 7 Nov research"
NEVER_PHRASES = ["leave a light on", "every light in the house", "porch light's on", "coming home", "welcome home", "home sweet home"]
INSTRUMENT = "country band: strummed acoustic, clean electric (the lick), pedal steel, bass, drums"
OBJECTS = ["engine", "road", "gravel", "screen door", "hill", "light", "keys", "clock", "window", "knees", "porch light", "phone", "sundown",
           "miles", "button", "porch", "evening", "dark", "thumb", "hinge"]
WRITER_PHRASES = ["she left the light on", "i leave the light on", "mama's porch"]
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "chorus", "hook", "bridge", "turn", "tag"}
REQUIRED = {"story": Q0[1], "shape": "A a lifetime in three chapters", "feel": "A mid-tempo country, q=84", "voice": "A male, B2-E4, F#4 once",
            "title": "A She Left the Light On (flip: I leave the light on)", "form": "A V C V C B C", "details": "B invented (unique, never cliche)",
            "bridge": "A never say it", "angle": "C the phone app, 300 miles away"}
ROUTING = "Narrative (N) primary, Lament secondary; radio country, one male voice"
FORM_PLAN = "Intro 4 | V1 8 | Ch 8 | Post 2 | V2 8 | Ch 8 | Post 2 | Bridge 6 | Ch3 10 (the turn line over the drop, then the flip) | Outro 4 = 60 bars, about 2:51 at q = 84"
KEY = "D major; one borrowed chord, G minor (iv), under 'thumb' at the end of the bridge"
LOG.append({"q": "deliverables", "answer": "demo MP3 + GM/GarageBand MIDI, lead sheet, Nashville chart, songbook (Doc https://claude.ai/artifact/6oiZAeJi5DoBKmeeDCMTnV + Word) with the producer one-sheet, test report (findings 71-79)"})
LOG.append({"q": "10.20 blind pick (offered without scores, shuffled)", "options": {"A": "I've had a year to shut it off, it'd only take my thumb", "B": "and lit hers too at sundown, three hundred miles from home", "C": "she left the light on"},
            "slots": {"A": "middle (top quartile under both)", "B": "Annotated top", "C": "Remembered top"}, "recommended": None, "answer": "A"})
BLIND_PICK = ("A", "I've had a year to shut it off, it'd only take my thumb -- the middle slot (top quartile under both)")
