"""Song 47 intake (dir p57). Every choice logged (the writer's standing ask).
Engine: ZenEng v131 (Module 27.75): 540, 541, 542 ported; 525 (kept endings by the slot's bars, zeneng_v131_kept_slots.json);
527 (the form an aim: each line's slot set beside the kept slots for its syllables; a line flagged only where under a tenth of kept
lines of its count take its slot; 524 so amended); 526 (the judge that has not seen the song: the 37 measures, zeneng_v131_kept_windows.json).
The other AI's suggestion: a song with dense, wordy lines (534 still open)."""
WRITER_BRIEF = None
LOG = [{"q": "526's kept side", "options": {"A": "ask for the kept-window table with all 37 measures; start intake meanwhile", "B": "fit on the 29 measures both collections carry", "C": "CoCoPops alone, 33 measures"},
        "recommended": "A", "answer": "the table supplied: zeneng_v131_kept_windows.json (545 windows, 37 measures, 285 pieces), parsed from the writer's PDF"},
       {"q": "where the song comes from", "options": {"A": "you give me the story or brief in your own words", "B": "from one of your poems, sermons or book chapters (attach it)", "C": "I offer three subjects and you pick"},
        "recommended": "A", "answer": "B", "writer": "Any song in this?  I’m thinking Contemporary Christian"}]
SOURCE_MATERIAL = "the writer's paper \"Analytic Continuation Through Death\" (v2, July 2026; src/, not committed)"
GENRE_WISH = "Contemporary Christian (the writer, Q1)"
LOG.append({"q": "which song in the paper", "options": {"A": "the singer and the song: 'The song can stop. The singer does not.' The resurrection as the Word singing a stopped life again on a wider stage", "B": "the wounds remain: Thomas touches them; what rises is this life, scars and history, not a copy", "C": "the kitchen table: the widow in Charlotte, six months on, crying, feeding the cat, the nights less terrible; grief finding its way back"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "whose voice", "options": {"A": "one believer singing to God: I am the song, You are the singer", "B": "congregational: 'we', for a church to sing together", "C": "God's voice to the one whose song is ending: 'I will sing you again'"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "sound", "options": {"A": "piano-led CCM ballad: piano and pads, building to full band with big drums in the last chorus", "B": "acoustic-driven modern CCM: strummed acoustic in driving eighths, bass and drums, electric guitar swells, a lift into each chorus", "C": "pop CCM: synths and programmed drums, up-tempo and bright"}, "recommended": "B", "answer": "B"})
LOG.append({"q": "voice (11.2)", "options": {"A": "tenor, about C3-A4", "B": "baritone, about A2-E4", "C": "female alto/mezzo, about G3-D5"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "tempo and feel", "options": {"A": "4/4 q=84, sixteenth-note strum; the verses wordy and quick (sixteenths), the chorus opening into longer notes", "B": "4/4 q=72, half-time ballad feel throughout", "C": "4/4 q=126, straight eighths, up-tempo"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "form", "options": {"A": "Verse 1 / Chorus / Verse 2 / Chorus / Bridge (sung twice, building) / Last Chorus / Tag", "B": "Verse / Pre-chorus / Chorus, twice; Bridge; Last Chorus", "C": "three verses, each ending on a refrain line (hymn-like), no bridge"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "The Singer Doesn't Stop", "B": "Sing Me Again", "C": "A Wider Stage"}, "recommended": "A", "answer": "A"})
TITLE = "The Singer Doesn't Stop"
LOG.append({"q": "how much of the paper's science the words carry", "options": {"A": "none: only the song-and-singer image and plain faith language", "B": "a touch, in everyday words: the heartbeat's rhythm, every part carrying the whole, the wounds kept, Lazarus against the risen Christ; no jargon", "C": "lean in: name the science (patterns, scaling, the edge of chaos) in a few lines"}, "recommended": "B", "answer": "B"})
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "answer": "notes", "writer_notes": ["Verse 1 needs more individuality: one or two lines with the distinctiveness of the Lazarus passage", "The last chorus needs a better payoff: 'on a wider stage' makes the ending bigger, not more meaningful; deliver the emotional consequence of God knowing and remembering the individual person", "MUSIC (to apply at the melody): a hook almost impossible to forget; an intimate, conversational first verse; a chorus that opens up melodically without becoming bombastic; a second verse with increasing emotional weight; a bridge that builds progressively, particularly through 'But You do'; a final chorus expansive without becoming stadium-worship generic; resist a huge production: the emotional power is in the intimacy"]})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "changes": ["Verse 1 lines 1 and 3: the doctor's healthy heart that never keeps perfect time; singing flat on the high part from the third pew on the left", "Last chorus: 'Even the high part I sang flat / You will sing me again / And it will still be me' (the flat note kept, as the wounds were)", "Tag ends on the chorus's own close"], "answer": None})
LOG[-1]["answer"] = "notes"; LOG[-1]["writer_notes"] = ["Verse 2: smooth 'He'd get sick again and die again and they'd lay him in the ground' (repeating syllables trip; more lyric, less prose)", "Chorus: let some of the last chorus's localized storytelling bleed back into the main chorus so it punches on first listen; check how 'When the last bar fades to silence / You will sing me again' connects musically", "Bridge: the second pass must accelerate or open up so it is not repetitive; 'But You do, oh You do' needs a strong melodic lift before the final chorus"]
LOG.append({"q": "lyric draft 3", "file": "lyric_draft3.md", "changes": ["Verse 2 line 2: Just a few more years of breathing till they laid him in the ground", "Chorus line 4: Every heartbeat out of time (calls back the doctor in verse 1; the last chorus goes further: the high part I sang flat)", "Bridge written out twice: the second pass opens up: But You do / Yes You do / You remember all of me (to be sung higher, the lift into the last chorus)"], "answer": None})
LOG[-1]["answer"] = "notes on verse 1: line 2 is explained, not experienced (needs decoding; CCM gives one pass); line 4's idea is excellent, its phrasing clinical"
LOG.append({"q": "verse 1, lines 2 and 4", "options": {"A": "Mama swears I hummed before I talked, and I've been humming ever since / But one day I'll take a breath for the next line and the line won't come", "B": "I hum at red lights and in the shower and when I can't fall asleep / But someday the last note's coming and I won't hear how it ends", "C": "Every little piece of me sounds a little like the rest of me / But I know a rest is coming, and that rest won't ever end"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "lyric draft 4", "file": "lyric_draft4.md", "answer": None})
LOG[-1]["answer"] = "note: verse 1 line 4 repeats 'line ... line' in one phrase; the ear stops there"
LOG.append({"q": "verse 1, last line", "options": {"A": "But one day I'll draw a breath to sing, and the next line won't come", "B": "But one day I'll take a breath for the next line and there won't be one", "C": "But one day I'll take a breath for the next verse and nothing comes"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "lyric draft 5", "file": "lyric_draft5.md", "answer": None})
LOG[-1]["answer"] = "Lock it!"
LYRIC_FILE = "lyric_locked.md"
LOG.append({"q": "key", "options": {"A": "G major: verses low and close around D3-B3, the chorus opening to E4-G4, 'But You do' peaking at A4 in the second bridge", "B": "A major: brighter; chorus around F#4-A4, the bridge's peak at A4 (the row's top, often)", "C": "F major: warmer and lower; chorus to F4, bridge peak G4"}, "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
KEY = "G major"
SYLLABLES = {"Verse 1": [14, 18, 14, 15], "Chorus": [4, 7, 11, 7, 6, 7], "Verse 2": [16, 15, 16, 15], "Bridge": [8, 7, 8, 7, 10, 6],
             "Bridge 2": [8, 7, 8, 7, 10, 3, 3, 7], "Last Chorus": [4, 7, 11, 8, 6, 6], "Tag": [4, 7]}   # the engine's syllable reading of the locked lyric
LOG.append({"q": "the form's slots (527: each line's slot beside the kept slots for its syllables; flagged under a tenth)",
            "options": {"A": "every line two bars: the verses dense (14-18 syllables in two bars: kept 37%, 27%, 10% at 14, 15, 16+); Intro 4, Verse 8, Chorus 12, Verse 8, Chorus 12, Bridge 12, Bridge 16, Last Chorus 12, Tag 4: 88 bars, about 4:11; no line flagged",
                        "B": "the verses' lines four bars (the kept slot most taken, 47-56%), everything else two: 104 bars, about 4:57",
                        "C": "as A, with each verse's last line given four bars to land (the breath; the scars): 92 bars, about 4:23"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
SLOTS = "every line two bars (Q A); Intro 4, Verse 8, Chorus 12, Verse 8, Chorus 12, Bridge 12, Bridge 2 16, Last Chorus 12, Tag 4"
FORM_BARS = 88
LOG.append({"q": "design: the hook ('The song can stop / But the singer doesn't stop')",
            "options": {"A": "'The song can stop': a short falling figure landing on the tonic, then a full beat of silence; 'But the singer doesn't stop': the same figure a step higher, running straight on into the next line with no breath (the music does what the words say)",
                        "B": "both lines one figure on one rhythm, the second a step higher, each followed by a breath",
                        "C": "no design: the engine draws the chorus"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
LOG.append({"q": "design: the bridge's build (the writer: progressive, particularly through 'But You do')",
            "options": {"A": "the second bridge sung a step higher than the first, note for note; its 'But You do / Yes You do' rising by step to the song's top, A4, on the last 'do', held, then 'You remember all of me' falling home into the last chorus",
                        "B": "both bridges at one pitch; the second gets denser rhythm and the band builds under it; 'But You do' held on the same note each time",
                        "C": "no design: the engine draws the bridges, the build left to the arrangement"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
LOG.append({"q": "arrangement (the writer: resist a huge production; the power is in the intimacy)",
            "options": {"A": "small band, built slowly: verse 1 the acoustic guitar alone (soft sixteenths) and the voice; bass and a brushed kit at chorus 1; verse 2 adds a low electric guitar swell; bridge 1 back down to guitar and voice; bridge 2 builds with the band; the last chorus full but plain (no gang vocals, no big pads); the tag the guitar alone",
                        "B": "piano and acoustic guitar together throughout, a string quartet entering at the bridges",
                        "C": "the full band from chorus 1 on, the bridge dropping out and the last chorus the biggest"},
            "recommended": "A", "answer": None})
LOG[-1]["answer"] = "A"
INSTRUMENT = "small band built slowly: acoustic guitar (soft sixteenths), voice; bass and brushed kit from chorus 1; a low electric guitar swell in verse 2; bridge 1 guitar and voice; bridge 2 builds; last chorus full but plain; tag guitar alone"
NEVER_SAY = []
NEVER_PHRASES = []
SINGERS = {"lead": "tenor, search row C3-G4; the lifted second bridge reaches A4 (Q: the bridge's build, A)"}
WRITER_NOTES = ["Words and music: Jason Bryant"]
LOG.append({"q": "blind pick (10.20): which line stays with you most (shuffled)",
            "options": {"A": "Not a copy, not a cover", "B": "'Cause the singer doesn't stop", "C": "Every scar and every stumble"},
            "slots": {"A": "Annotated", "B": "Remembered", "C": "Middle"}, "recommended": None, "answer": "A", "slot_picked": "Annotated"})
