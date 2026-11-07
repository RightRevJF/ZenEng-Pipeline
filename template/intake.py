"""Song 27 intake (ZenEng v64 with the v65 fix list, songs 21-26, run as ports). The writer's own lyric (Module 29, lyric-first):
three four-line monorhyme stanzas against either/or thinking. Asked for: art rock."""
LOG = [{"q": "source", "writer": "Art rock song? [three stanzas, the writer's own: 'Where is the conflict, its with either or' / 'Theologians are cowards, hiding in words' / 'The mugwumps are hated by denizens of dread']"}]
TITLE = None
WRITER_TEXT = """Where is the conflict, its with either or
Birthed by a thinker, whose thought line was poor
Now there is anguish, everyone is made sore
All cause of Ari, should've realized he's a boor.

Theologians are cowards, hiding in words
Crowing their nonsense, syllables for the birds
Systematizing wind, they create nothing but turds
Which then are baptized, delighting the herds

The mugwumps are hated by denizens of dread
Who spin issues into inheritance, bones into bread
Telling you one thing, different from what's read
And its into perdition that you are being led"""
LOG.append({"q": "how to treat the words", "options": {"A": "set exactly as written, through-composed, no chorus", "B": "the stanzas as verses plus a refrain from his own words",
            "C": "raw material, shaped for singing"}, "recommended": "B", "answer": "B leaning towards C", "writer_adds": "what do you think the poem is about?"})
LOG.append({"q": "what the poem is about", "answer": "the run's reading given: an attack on either/or thinking (Aristotle's excluded middle) -> theologians systematizing the wind (spirit) -> the partisans of dread who hate the mugwumps"})
LOG.append({"q": "what the refrain carries", "options": {"A": "mockery of the binary, either/or thrown back", "B": "the answer, both/and", "C": "the wind: the spirit that won't be systematized"},
            "recommended": "B", "answer": "C"})
LOG.append({"q": "voice (11.2)", "options": {"A": "tenor D3-A4, Bb4 once", "B": "baritone B2-C4, D4 once", "C": "female A3-B4, C5 once"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "sound", "options": {"A": "angular art rock: two interlocking clean guitars, melodic bass, accented drums; the refrain opens into ringing chords over an organ drone",
            "B": "theatrical piano art rock: piano, strings, choir", "C": "atmospheric: reverb washes, drones, a huge climax"}, "recommended": "A", "answer": "A",
            "writer_adds": "I'm going to need an all parts pdf for production"})
DELIVER_PARTS = True
LOG.append({"q": "metre and tempo", "options": {"A": "verses 5/4, refrain 4/4, q=132", "B": "4/4 throughout q=120, displaced accents", "C": "7/8 throughout"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "form (lengths at q=132, 2 bars a line; fixes 13/31: the longest line 14 syllables in 20 eighths, no interludes needed)",
            "options": {"A": "classic, 72 bars, 2:27", "B": "extended: 8-bar intro, an 8-bar 5/4 build before the final refrains, 84 bars, 2:55", "C": "lean, 56 bars, 1:55"},
            "recommended": "B", "answer": "B"})
LOG.append({"q": "key", "options": {"A": "D Dorian verses (B natural), F major refrain (Bb): the either/or in one note; Bb4 once", "B": "E minor verses, G major refrain", "C": "A minor verses, C major refrain"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "Systematizing Wind", "B": "Either Or", "C": "Denizens of Dread"}, "recommended": "A", "answer": "B"})
TITLE = "Either Or"
LOG.append({"q": "lyric draft 1", "options": {"A": "lock", "B": "notes", "C": "refrain in another direction"}, "recommended": "B", "answer": "B",
            "writer": "So you think the words of the poem carry the tune without change. You've kept it my words primarily"})
LOG.append({"q": "three spots (thought line / Ari / turds)", "options": {"A": "keep all three", "B": "fix the first two for clarity, keep 'turds'", "C": "change all three"},
            "recommended": "B", "answer": "B", "result": "verse 1 line 2: 'birthed by Aristotle, whose line of thought was poor' (names him, so 'Ari' lands in line 4)"})
LOG.append({"q": "lyric draft 2", "options": {"A": "lock", "B": "notes", "C": "refrain elsewhere"}, "recommended": "A", "answer": "B",
            "writer": "I like the poem, don't like the lyrics other than the refrain"})
LOG.append({"q": "how to rework the verses", "options": {"A": "the poem exactly as written", "B": "new verses in the refrain's voice", "C": "new verses in the refrain's voice around his strongest phrases"},
            "recommended": "C", "answer": "C"})
LOG.append({"q": "lyric notes 3", "writer": "attached Either_Or_Lyric_Improvement_Suggestions.docx: a more dangerous opening line; a better verse 2 line 2 ('weighing the wind by the words that they heard'); the baptism image (the original may be best); verse 3 about being punished for refusing to choose, keep 'turning bones into bread'; space before the last line, delivered quietly"})
LOG.append({"q": "lyric notes 4", "writer": "1 'denizens of dread' -> 'from the high and heavy-fed' or 'from the keepers of the dead'; 2 refrain 'you can't fence it in, you can't keep score'; 3 'sprinkled holy water on the laws they wrote'; 4 'and we've bled across that line ever since'; 5 'handing down their fathers' wars by name'",
            "answer": "draft 5: all five taken; 'from the keepers of the dead' chosen (it sits with 'bones into bread')"})
LOG.append({"q": "lyric draft 5", "options": {"A": "lock and write the music", "B": "more notes", "C": "'the high and heavy-fed' instead"}, "recommended": "A", "answer": "A"})
# ---- derived (run's port, v64 + v65 fixes as ports) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 with the v65 fix list (songs 21-26) run as ports"
SOURCE_MATERIAL = "the writer's poem (three monorhyme stanzas), reworked over five drafts with his notes and two attached suggestion documents"
Q0 = ("either or", "Aristotle's line in the dust -- true or lie -- and the blood spilled across it ever since; theologians weighing the wind and blessing their laws; the ones who won't choose stoned by the keepers of the dead; and the wind, which blows where it wants and was never either or")
SINGERS = {"him": "male tenor (11.2, v65 fix 14 row), D3-A4, Bb4 once"}
INSTRUMENT = "angular art rock: two interlocking clean electric guitars, melodic bass, drums with sharp accents, an organ drone under the refrain"
OBJECTS = ["line", "dust", "blood", "side", "wind", "tower", "words", "water", "laws", "herd", "stones", "dead", "wars", "name", "bones", "bread", "score"]
WRITER_PHRASES = ["systematizing wind", "bones into bread", "turning bones into bread", "either or", "keepers of the dead", "weighing the wind by the words that they heard",
                  "sprinkled holy water on the laws they wrote"]
WRITER_WORDS = ["aristotle", "systematizing"]
LEXICON = {"systematizing": "S IH2 S T AH0 M AH0 T AY1 Z IH0 NG", "birthed": "B ER1 TH T", "mugwumps": "M AH1 G W AH2 M P S", "perdition": "P ER0 D IH1 SH AH0 N"}   # the writer's words
NEVER_SAY = []
NEVER_PHRASES = []
ROLES = {"verse", "chorus", "hook", "tag", "refrain"}
REQUIRED = {"story": Q0[1], "words": "B leaning C: the writer's stanzas as verses, reworked into new verses around his phrases (draft 5)",
            "refrain": "C the wind", "voice": "A tenor D3-A4, Bb4 once", "sound": "A angular art rock", "metre": "A verses 5/4, refrain 4/4, q=132",
            "form": "B extended, 84 bars, 2:55", "key": "A D Dorian verses (B natural), F major refrain (Bb); Bb4 once", "title": "B Either Or",
            "parts": "an all-parts PDF for production"}
ROUTING = "Argument (polemic) primary with a Paradox (P) refrain; art rock, one voice"
LOG.append({'q': 'blind pick (10.20)', 'options': {'A': "you can't fence it in, you can't keep score (Annotated top)", 'B': 'the wind was never either or (Remembered top)', 'C': 'and the wind blows where it wants to blow (middle: most-repeated hook line)'}, 'answer': 'B', 'slot': 'remembered'})
LOG.append({'q': 'fix list', 'options': {'A': 'add to the existing fix list Doc (songs 21-27, fixes 1-53)', 'B': 'a new Doc for song 27 only', 'C': 'hold off'}, 'recommended': 'A', 'answer': 'A'})
