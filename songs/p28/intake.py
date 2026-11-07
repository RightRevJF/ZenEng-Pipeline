"""Song 28 intake. Every choice logged (the writer's standing ask)."""
WRITER_BRIEF = """We've touched the edges of it but now I wanna do a song about star-crossed lovers. Him, a pastor with a small congregation
and a stable but full life has a life-changing affair with a married teacher. Even though their middle aged, they have an incredible heat
between them and their affair is highly sexually charged. The two are caught by the woman's husband and they end bot the two are left
forever longing one another. Both however choose the comforts of what's known over the amazing possibility of getting together. Fear of
the unknown. The key will be to convey all that without giving away their occupations (let the words hint but stay ambiguous) or sounding
melodramatic. You've got to capture the high of the relationship against the incredible pull of inertia"""
LOG = [{"q": "source", "writer": WRITER_BRIEF,
        "constraints": ["occupations hinted, never named (pastor; teacher)", "not melodramatic", "the high of the affair against the pull of inertia",
                        "middle-aged, highly charged", "caught by her husband", "both choose the known; fear of the unknown; forever longing"]}]
TITLE = None
LOG.append({'q': 'whose voice', 'options': {'A': 'his voice alone', 'B': 'a duet, him and her: their own verses, the same chorus words, never together; the end sung apart', 'C': 'a narrator telling both'}, 'recommended': 'B', 'answer': 'B'})
LOG.append({'q': 'sound', 'options': {'A': 'slow-burn soul: electric piano, brushed drums, warm bass, a little organ', 'B': 'Americana duet: acoustic guitar, pedal steel, low tremolo electric', 'C': 'chamber pop: piano and string quartet'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'voices (11.2)', 'options': {'A': 'him baritone B2-C4 (D4 once); her female A3-B4 (C5 once); she sings his chorus tune an octave up', 'B': 'him male E3-F#4 (G4); her A3-B4 (C5)', 'C': 'him tenor D3-A4; her mezzo'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'tempo and feel', 'options': {'A': 'slow 6/8 sway, dotted-q = 54', 'B': '4/4 q=76 straight, half-time', 'C': '4/4 q=92 groove for the affair, half-time drop for the aftermath'}, 'recommended': 'A', 'answer': 'A',
            'writer_adds': "The two would meet and have sex in her car with all the windows shaded. They also would go to an adult bookstore and have sex in the theater. You've got to capture the heat AND the love of the affair in order to make their choice to remain apart heartbreaking"})
LOG.append({'q': 'form (lengths at dotted-q=54, 2 bars of 6/8 a line; fixes 13/31)', 'options': {'A': '104 bars, 3:51: intro; his verse, her verse (the car); chorus; his, her (the theater and the love); chorus; bridge (caught, trading lines); his, her (going home); last chorus twice, his then hers, never together; outro', 'B': '64 bars, 2:22: no bridge, no going-home verses', 'C': '112 bars, 4:09: A plus an 8-bar instrumental after chorus 2'}, 'recommended': 'A', 'answer': 'A',
            'writer_adds': "They were caught when her husband purloined her iWatch and read the many sonnets the lover had sent her"})
LOG.append({'q': 'key', 'options': {'A': 'Eb major, no key change anywhere: verses lean on C minor, the chorus opens in Eb; the last chorus refuses the lift', 'B': 'Db major with a half-step lift into the last chorus', 'C': 'his verses Bb, hers Db, the chorus shared'}, 'recommended': 'A', 'answer': 'A'})
LOG.append({'q': 'title', 'options': {'A': 'The Devil We Know', 'B': 'Tinted Glass', 'C': 'Fourteen Lines'}, 'recommended': 'A', 'answer': 'B'})
TITLE = "Tinted Glass"
LOG.append({'q': 'never say', 'options': {'A': 'both lists: the job words (church, pulpit, preacher, pastor, sermon, pew, congregation, school, class, teacher, students, chalk) and the affair cliches (forbidden, sin, cheating, affair, secret love, fire, burning, desire, soulmate)', 'B': 'job words only', 'C': 'no list'}, 'recommended': 'A', 'answer': 'A',
            'writer_adds': 'I want to see a working draft of the lyrics before you go to music'})
NEVER_SAY = ["church", "pulpit", "preacher", "pastor", "sermon", "pew", "pews", "congregation", "school", "class", "teacher", "teachers", "students", "chalk",
             "forbidden", "sin", "cheating", "affair", "fire", "burning", "desire", "soulmate"]
NEVER_PHRASES = ["secret love"]
LOG.append({'q': 'lyric draft 1', 'options': {'A': 'lock', 'B': 'notes', 'C': 'more heat in verses 1-4'}, 'recommended': 'B', 'answer': 'notes',
            'writer': "1 make the affair physically stranger (one image that belongs only to this affair; fingerprints, not evidence); 2 give her one line only she could say (a devastating behavioral detail); 3 a quieter, more frightening bridge; 4 the last chorus: replace 'I still know you by your breathing' with something observable the longing causes; 5 push the tinted glass further: protection, then distortion, then a barrier that remains or is gone"})
LOG.append({'q': 'lyric draft 2', 'options': {'A': 'lock', 'B': 'more notes', 'C': 'one chorus, same words'}, 'recommended': 'A', 'answer': 'notes',
            'writer': "Verse 1: it isn't cardboard shielding the sun, it was like vinyl, rings false. The parking lot was either a parking deck at a furniture company or a local library. Verse 2: she never wore a ring so that whole verse fails. Verse 3: swap quarters for dollars. Verse 4: humming a hymn isn't something anybody would do"})
LOG.append({'q': 'lyric draft 3', 'answer': 'notes', 'writer': "I don't like verse four's spread jacket. Didn't happen. Find some other way to display tenderness amid the raunchy setting. Make three suggestions before drafting the lyric"})
LOG.append({'q': 'verse 4 line 2 (tenderness)', 'options': {'A': 'you leaned in close and asked me if I was cold', 'B': 'we got the giggles like two kids in the back row', 'C': 'you watched my face and never once the screen'}, 'recommended': 'A', 'answer': 'B'})
LOG.append({'q': 'lyric draft 4', 'answer': 'notes', 'writer': "Verse two - why count to six hundred doesn't make sense"})
LOG.append({'q': 'verse 2 line 4', 'options': {'A': "I'd wait ten minutes so we'd leave apart", 'B': "I'd sit there till my face looked like my own", 'C': "then I'd peel the shades off one by one"}, 'recommended': 'B', 'answer': 'C', 'writer': "C. But we'd pull them down together"})
LOG.append({'q': 'lyric draft 5', 'options': {'A': 'lock and write the music', 'B': 'more notes', 'C': 'lock, but flag weak lines first (the room)'}, 'recommended': 'A', 'answer': 'C'})
# ---- derived (run's port, v64 + v65 fixes as ports) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 with the v65 fix list (songs 21-27) run as ports"
SOURCE_MATERIAL = "the writer's brief (star-crossed middle-aged lovers; occupations hinted, never named) and his notes over five drafts"
Q0 = ("tinted glass", "two married, middle-aged people: a life-changing, charged affair behind shaded car windows and in a highway theater; caught through the sonnets on her watch; both choose the known life over each other, and the longing stays")
SINGERS = {"him": "baritone B2-C4, D4 once", "her": "female A3-B4, C5 once (his chorus tune an octave up)"}
INSTRUMENT = "slow-burn soul: electric piano, brushed drums, warm bass, a little organ"
OBJECTS = ["deck", "vinyl", "window", "shades", "pens", "glasses", "hands", "dark", "noon", "door", "dollars", "lines", "laugh", "screen", "strangers",
           "kids", "row", "face", "glass", "watch", "bed", "hand", "words", "wife", "board", "road", "coffee", "sun", "car", "street", "call"]
WRITER_PHRASES = ["furniture company", "black vinyl", "pull the shades down together", "we got the giggles like two kids in the back row",
                  "paid in dollars for the dark", "tinted glass"]
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "chorus", "bridge"}
REQUIRED = {"story": Q0[1], "voice": "B duet: own verses, the same chorus tune, never together", "sound": "A slow-burn soul",
            "voices": "A him baritone B2-C4 (D4); her A3-B4 (C5), an octave up", "metre": "A 6/8, dotted-q = 54", "form": "A 104 bars, 3:51",
            "key": "A Eb major, no key change", "title": "B Tinted Glass", "never_say": "A both lists"}
ROUTING = "Narrative (two first persons, alternating) with a Turn in the last chorus; slow soul duet"
LOG.append({'q': 'the room: 12 locked lines too long for two bars of 6/8 at dotted-q=54 (the run had told him 8-11 syllables fit; the span holds 10 at most)', 'options': {'A': 'every verse and bridge line takes four bars (same words; space for the electric piano to answer); about 5:40', 'B': 'verses and bridge on a sixteenth grid, two bars a line; 3:51', 'C': 'cut the 12 lines to 9 syllables or fewer'}, 'recommended': 'B', 'answer': 'A'})
LOG.append({'q': 'the room at four bars a line (verses, bridge)', 'result': "33 of 37 locked lines live; 4 die and stand by the writer's lock: 'I said that I was out visiting the sick' (placement), 'you held my face like you were memorizing it' (weak ending 'it': v65 fix 9 case), 'Sundays I still say the words they pay me for' (weak ending 'for': fix 9 case), 'and for once in my life it was enough' (V1: fix 53 case, its couplet holds 'face')"})
FORM_BARS = 152
LOG.append({'q': 'music built', 'result': "pick dede2d3b460a (no hand edits); 152 bars, 5:38; lead sheet, full score (keyboard-led), Nashville chart, songbook + production notes, test report; consistency 30/30"})
LOG.append({'q': 'blind pick (10.20)', 'options': {'A': 'past the county line, a door with no name (middle: top quartile under both)', 'B': 'and I loved you, that was all (Annotated top)', 'C': 'behind the tinted glass (Remembered top)'}, 'answer': 'A', 'slot': 'middle'})
LOG.append({'q': 'fix list', 'options': {'A': 'add to the existing fix list Doc (songs 21-28, fixes 1-61)', 'B': 'a new Doc for song 28 only', 'C': 'hold off'}, 'recommended': 'A', 'answer': 'A'})
