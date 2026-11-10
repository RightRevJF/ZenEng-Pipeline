# Song 34 intake (ZenEng v78): a test of Module 9-M, heavy metal.
TITLE = None
LOG = []
LOG.append({"q": "goal", "answer": "A. There's a new heavy metal section. Want to write in that genre to test it?"})
LOG.append({"q": 1, "topic": "which metal (9-M.2 preset)",
            "options": {"A": "Modern groove / metalcore", "B": "Thrash", "C": "Doom"}, "recommended": "A",
            "answer": "Which is the toughest to nail do you think, that's the one I want to do?",
            "reading": "the writer asks for the hardest preset of all six; the answer given: 5 Death, the preset that departs furthest from what the engine does (9-M.2's order): growl throughout so no melody search (9-M.10a), chromatic riff chains the engine's gates were built to reject, blasts and the slowdown, harsh syllables with no pitch in the demo"})
PRESET = "5 Death"
LOG.append({"q": 2, "topic": "the death setting (9-M.2; Table BX row 5)",
            "options": {"A": "straight death: chromatic riff chains, shifting centres, blasts, the slowdown, growl throughout", "B": "melodic death: diatonic minor, leads in thirds, verse and chorus, growled", "C": "death with one clean chorus (breaks the preset)"},
            "recommended": "A", "answer": "A",
            "reading": "SCENE aim by implication (9-M.2: riff and atmosphere before a singable chorus); MELODIC flag off; no melody search for the voice (9-M.10a)"})
SETTING = {"preset": "5 Death", "melodic": False, "aim": "SCENE", "voice": "growl throughout; low and mid one band"}
LOG.append({"q": 3, "topic": "what it is about (10.1 Q1; three pictures, v43 fix 5.2)",
            "options": {"A": "a graveside committal in the rain: the lowering straps, the dirt on the lid, 'ashes to ashes', the dead rising at the end (the Christian overlay, 9-M.8)", "B": "the war in heaven, Revelation 12", "C": "a mine collapse"},
            "recommended": "A", "answer": "A",
            "reading": "Christian overlay on: dark lexicon kept, enemy death, resolves toward hope; objects so far: the lowering straps, the dirt on the lid, the rain, 'ashes to ashes'"})
OVERLAY = "CHRISTIAN"
OBJECTS = ["lowering straps", "dirt on the lid", "rain", "ashes to ashes"]
LOG.append({"q": 4, "topic": "the speaker (9-M.8 overlay: combatant or penitent)",
            "options": {"A": "the one who says the words, the book in one hand and a fistful of dirt in the other, who throws it and turns the words on death: 'where is your sting?'", "B": "the dead man in the box", "C": "the son at the edge"},
            "recommended": "A", "answer": "A",
            "reading": "the speaker is the officiant, a combatant; objects added: the book, the fistful of dirt; 1 Cor 15:55 is the taunt"})
OBJECTS += ["the book", "fistful of dirt"]
SPEAKER = "the officiant at the grave, a combatant against death"
LOG.append({"q": 5, "topic": "stance (9-M.8: a dial apart from heaviness)",
            "options": {"A": "denunciation throughout: mocking death to its face", "B": "grim resolve", "C": "lament turning to defiance: the verses grieve in the rain; by the end he taunts death, 'where is your sting?'"},
            "recommended": "C", "answer": "C",
            "reading": "stance moves lament -> resolve -> denunciation of death, matching 9-M.1's arc (meet the dark, sustain, resolve to strength); hostility aimed only at death"})
STANCE = ["lament", "resolve", "denunciation (of death)"]
LOG.append({"q": 6, "topic": "title (9-M.8: Death titles lean to a participle or 'X of Y'; 9-M.7: the title goes to the intelligible voice)",
            "options": {"A": "Swallowed Up (the grave swallows him; 'death is swallowed up in victory', 1 Cor 15:54)", "B": "The Sting of Death", "C": "Committed"},
            "recommended": "A", "answer": "A"})
TITLE = "Swallowed Up"
LOG.append({"q": 7, "topic": "tempo, feel, tuning (9-M.5; Table BX row 5 DEFAULTS)",
            "options": {"A": "q = 200, blasts in the choruses, the slowdown to q = 100 at the turn (the taunt); tuned to B", "B": "q = 240, blasts most of the way", "C": "q = 170, mid-paced, more groove"},
            "recommended": "A", "answer": "A"})
FEEL = {"meter": "4/4", "qbpm": 200, "slowdown_qbpm": 100, "tuning": "B standard (low B)", "home_feel": "double time", "chorus_feel": "blast", "turn": "the slowdown, a true halving of tempo"}
LOG.append({"q": 8, "topic": "form (9-M.6; fix 139: lengths summed and computed)",
            "options": {"A": "Intro 16 | Riff 8 | V1 16 | Ch1 8 | V2 16 | Ch2 8 | Solo 16 | Slowdown 16 (q = 100) | Riff 8 | Last Ch 8 | Outro 8 = 128 bars, about 2:53", "B": "no return, 88 bars, about 2:05", "C": "A plus a third verse and chorus before the solo: 152 bars, about 3:22"},
            "recommended": "A", "answer": "C"})
FORM_PLAN = [("Intro",16,200),("Riff",8,200),("Verse 1",16,200),("Chorus 1",8,200),("Verse 2",16,200),("Chorus 2",8,200),("Verse 3",16,200),("Chorus 3",8,200),("Solo",16,200),("Slowdown",16,100),("Riff 2",8,200),("Last Chorus",8,200),("Outro",8,200)]
_b = sum(b for _,b,_ in FORM_PLAN); _s = sum(b*4*60/q for _,b,q in FORM_PLAN)
assert _b == 152 and round(_s) == 202, (_b, _s)
LOG.append({"q": 9, "topic": "never say (v77: a death)",
            "options": {"A": "metal and funeral cliches: rot, maggots, gore, the reaper, eternal darkness, six feet under, darkness falls; rest in peace, gone too soon, a better place, angels, heaven's gates ('ashes to ashes' and scripture allowed)", "B": "only the metal cliches", "C": "no list"},
            "recommended": "A", "answer": "A"})
NEVER_SAY = ["rot", "maggots", "gore", "reaper", "angels"]
NEVER_PHRASES = ["eternal darkness", "six feet under", "darkness falls", "rest in peace", "gone too soon", "a better place", "heaven's gates"]
LOG.append({"q": 10, "topic": "who is in the box (10.10: the object question)",
            "options": {"A": "an old farmer from the church; his feed-store cap on the lid", "B": "the speaker's own father; the book in his hand was his father's, the margins worn soft", "C": "a young man killed on the highway; his truck keys on the lid"},
            "recommended": "B", "answer": "B",
            "reading": "the officiant buries his own father with his father's Bible; the words he says are the words his father taught him"})
OBJECTS += ["father's Bible, margins worn soft"]
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md",
            "answer": "B. notes: (1) verse 3 is the weakest: rhetorical, less physical ('Eden's gate', 'kings and beggars' is sermon not scene); keep the confrontation with the grave but pull it back into the body and the moment; (2) some lines too smooth for death metal: shorter, harder, percussive ('he taught me every word I have to say / and now I say them, standing at his head'; 'but what you've got down there is not your own'); (3) chorus lines 2-3 explanatory: more abrupt and physical. Priority: verse 3 in the dirt; tighten literary lines; test the chorus under a harsh vocal, every syllable wants to be spat"})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "changes": ["verse 3 rewritten at the edge of the hole: the cut walls, the roots like nerves, rain on the vault, fake grass over the spoil; ends 'I read the end. The stone gets moved. / You don't get to keep this one.'", "smooth lines cut short: 'Hand over hand. Inch by inch.', 'My father in his Sunday suit.', 'He drilled these words into my mouth. / Now I read them to the hole.', 'I throw it. The lid booms back:'", "chorus: 'Swallowed up! / Clay jaw. Stone throat. / Never says \"Enough!\" / Swallowed him up!'; last chorus: 'Death is swallowed up! / Clay jaw. Stone throat. / Now you've had \"Enough!\" / Swallowed up!'"], "answer": "A"})
WRITER_PHRASES = ["swallowed up", "ashes to ashes", "earth to earth", "where is your sting"]
WRITER_WORDS = ["swallowed"]
LEXICON = {}
ROLES = {"verse", "chorus", "hook", "taunt"}
COMMERCIAL = {"profile": "SCENE (9-M.2)", "hold": [], "depart": []}
SENSES = "to hit: the body (hands, fist, mouth, jaw, throat), cold, wet, sound (creak, drumming, booms)"
INSTRUMENT = "death metal band: two rhythm guitars (left and right, the same riff), a lead guitar, five-string bass, drums; a harsh voice (growl low, shout mid, one high scream)"
TITLE = "Swallowed Up"
LOG.append({"q": "delivery", "songbook_doc": "https://claude.ai/artifact/K1q3mBa6731VeiXDCGB5UA", "riffs_frozen": "7f7d89c5e09d", "solo_order": "b644ed162840 (reproduced)", "consistency": "41/41"})
