"""Song 44 intake (the writer: Jason Bryant). Source: his essay 'The Problem of the Other Mind' (read, used, not stored here).
Words and music: Jason Bryant."""
LOG = []
LOG.append({"q": "0", "topic": "the method", "asked": "How can we solve a philosophical quandary in song the way the paper does?",
            "answer": "the writer's own question; the session's reading: the verses as failed answers, the pre-chorus names the hidden assumption, "
                      "the chorus re-asks rather than answers, a bridge one level up, an honest open ending; the music enacts the claim (coupling)"})
LOG.append({"q": "1", "topic": "how the song carries the other mind",
            "options": {"A": "a duet: two voices start apart and lock together", "B": "congregational: the room completes the last chorus",
                        "C": "pop: one voice; the band does the phasing"},
            "recommended": "A",
            "answer": "C. 'And everything must stay abstract. We don't need to say incarnation or resurrection or anything obvious.'"})
LOG.append({"q": "note", "topic": "the never-say question",
            "writer": "'What happened to that question by the way in the intake - the what words not to use. Doesn't seem like it's showed up the last couple of times'",
            "reply": "asked for songs 40, 41 and 42; skipped for song 43 (its list was set by the session, not asked); asked here as Q2"})
LOG.append({"q": "2", "topic": "never-say",
            "options": {"A": "fully hidden: no theology words, no philosophy or science words, no stock love-song phrases; pulse and heartbeat allowed",
                        "B": "as A, one faint echo allowed (an ordinary word a listener of faith might hear twice, e.g. 'touched' or 'heard')",
                        "C": "as A, science words allowed as images (static, frequency, signal), never as explanation"},
            "recommended": "A", "answer": "B"})
NEVER_SAY = ["god", "lord", "trinity", "word", "flesh", "incarnation", "incarnate", "resurrection", "risen", "heaven", "soul", "spirit", "holy",
             "faith", "believe", "mind", "minds", "conscious", "consciousness", "zombie", "proof", "prove", "brain", "neuron", "signal", "frequency", "critical"]
NEVER_PHRASES = ["two hearts beat as one", "soulmate", "meant to be", "you complete me", "never alone", "other half"]
ECHO = "one faint echo allowed (Q2 B): an ordinary word a listener of faith might hear twice, e.g. 'touched' or 'heard'"
LOG.append({"q": "3", "topic": "the scene",
            "options": {"A": "two people in the dark: he lies awake, his ear on her chest, her pulse", "B": "two strangers on a crowded dance floor; by the last chorus the beat moves them as one",
                        "C": "an open phone line between two cities, no one speaking"},
            "recommended": "A", "answer": "B"})
SCENE = "two strangers on a crowded dance floor; the beat moves them as one by the last chorus (Q3 B)"
LOG.append({"q": "4", "topic": "what the chorus does",
            "options": {"A": "re-asks: not 'is anyone in there' but 'were we ever apart' ('I can't see in, but I don't need to / we've been keeping time since the lights went down')",
                        "B": "never answers in words: the question alone; the band locks to the voice", "C": "invites: 'move like I move'; the proof is the joining"},
            "recommended": "A", "answer": "A"})
CHORUS_DESIGN = "the chorus re-asks the question rather than answering it (Q4 A)"
LOG.append({"q": "5", "topic": "the groove",
            "options": {"A": "mid-tempo dance-pop, about 112, four on the floor; hats and a synth pulse drift off the kick and lock by the chorus",
                        "B": "club house, about 124", "C": "slow burn, about 96, half-time R&B"},
            "recommended": "A", "answer": "A"})
FEEL = "mid-tempo dance-pop, q = 112, four on the floor, straight; the hats and a synth pulse drift off the kick in the verses and lock by the chorus (Q5 A)"
LOG.append({"q": "6", "topic": "who sings",
            "options": {"A": "a woman, mezzo (about G3-D5)", "B": "a man, light tenor (about C3-A4)", "C": "a man, baritone (about A2-E4)"},
            "recommended": "A", "answer": "A"})
VOICE = dict(kind="a woman, mezzo", lo=55, hi=74)
LOG.append({"q": "7", "topic": "the form",
            "options": {"A": "Intro 8, V 8, Pre 4, Ch 8, Post 4, V 8, Pre 4, Ch 8, Post 4, Bridge 8, LC 8, Post 4, Outro 4: 80 bars, about 2:51 at 112",
                        "B": "longer verses, no pre-chorus: 84 bars, about 3:00", "C": "as A, an instrumental break for the bridge: 80 bars, about 2:51"},
            "recommended": "A", "answer": "A. 'But is there any way we could pay it more to like 2:45?'"})
LOG.append({"q": "8", "topic": "paring to about 2:45",
            "options": {"A": "intro 4 bars: 76 bars, about 2:43", "B": "80 bars at 116, about 2:46", "C": "drop the first post-chorus: 76 bars, about 2:43"},
            "recommended": "A", "answer": "withdrawn: 'No. Disregard that last comment (it can stay 2:50) and ask the next query'"})
FORM = [("Intro", 8), ("Verse 1", 8), ("Pre 1", 4), ("Chorus 1", 8), ("Post 1", 4), ("Verse 2", 8), ("Pre 2", 4), ("Chorus 2", 8), ("Post 2", 4),
        ("Bridge", 8), ("Last Chorus", 8), ("Post 3", 4), ("Outro", 4)]                  # 80 bars, about 2:51 at q = 112 (Q7 A; Q8 withdrawn)
LOG.append({"q": "9", "topic": "the key",
            "options": {"A": "C minor verses opening to E-flat major in the chorus (same notes, a new home: the reframe in harmony)", "B": "A major throughout", "C": "D minor throughout"},
            "recommended": "A", "answer": "A"})
KEY = "C minor (verses), E-flat major (chorus): the relative pair (Q9 A)"
LOG.append({"q": "10", "topic": "the title",
            "options": {"A": "Keeping Time", "B": "Since the Lights Went Down", "C": "Lights On"}, "recommended": "A", "answer": "A"})
TITLE = "Keeping Time"
LOG.append({"q": "11", "topic": "what fails in the verses",
            "options": {"A": "verse 1 reads the face (a smile can be put on); verse 2 tries words (the bass breaks them apart)",
                        "B": "verse 1 fragments in the strobe; verse 2 only her own reflection", "C": "the session's choice in draft 1"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "12", "topic": "draft 1: lock or notes", "options": {"A": "lock", "B": "notes", "C": "a second full draft to compare"}, "recommended": None,
            "answer": "B", "notes": ["1 Verse 1 the least distinctive: lines 1-2 cinematic, 3-4 familiar; 'you smile the way that anyone can' generalized; "
                                     "the glass unclear (face, crowd, concealment?), less integrated than verse 2's wall; a concrete detail that makes the person "
                                     "simultaneously anonymous and compelling",
                                     "2 Pre-chorus 1: line 1 good; 'That's the only start I've known' sounds written to complete a rhyme; build anticipation musically and intellectually",
                                     "3 Bridge lines 3-4: the most ambitious passage; 'whoever keeps it' vague; 'heard and kept' a rhyme that hasn't found its meaning; "
                                     "preserve the idea (the beat was present before we arrived; its source came down among us so that we could hear it), not the words"]})
LOG.append({"q": "13", "topic": "draft 2: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "change one line"}, "recommended": None,
            "answer": "B", "notes": ["Chorus weak: the idea good, the language flat and abstract against the verses; 'Who ever said we started out apart' rhetorical "
                                     "rather than felt; the last-chorus 'Nobody ever started out apart' better; needs more melodic and rhythmic specificity on the page to be a true hook",
                                     "Post-chorus: 'Keeping time, keeping time / One beat under two' serviceable but thin, a placeholder chant, not a secondary hook; "
                                     "the final 'And the lights stay down' better (a small emotional close)",
                                     "Overall: a familiar lane (club communion, strangers connected by the beat); one or two more surprising images or turns of phrase, "
                                     "to feel owned rather than well-executed genre writing"]})
LOG.append({"q": "14", "topic": "draft 3: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "change one line"}, "recommended": None,
            "answer": "notes", "notes": ["Verse 1 still the strongest; verse 2 good but not as sharp",
                                         "the bridge the most ambitious and riskiest, in a different register: it lands if the production leans into atmosphere and space; "
                                         "a brief departure if the track stays high-energy and club-focused",
                                         "the final post-chorus 'And the lights stay down' effective as a quiet close, less rhythmically strong than 'Nobody's counting anymore'"]})
ARRANGEMENT_NOTES = ["the bridge: the production leans into atmosphere and space (the writer's note to draft 3); proposed: the kick drops out under the bridge and returns into the last chorus"]
LOG.append({"q": "15", "topic": "draft 4: lock or notes", "options": {"A": "lock", "B": "more notes", "C": "change one line"}, "recommended": None, "answer": "A"})
DENSITY_342 = "the locked lyric: 267 syllables over 68 sung bars, 3.93 a bar (Verse 1 3.88, Pre 2 4.50 the densest), inside the kept 3.6-4.1: no question needed (342)"
LOG.append({"q": "16", "topic": "the chorus design",
            "options": {"A": "design the hook: 'Two clocks on the same wall' rocks between two pitches a step apart, the band dropping out under it; 'keeping time, keeping time' "
                             "one rhythmic cell twice, the second a step higher; 'fall on the one' lands every phrase on the downbeat; a design gate (nine builds in ten)",
                        "B": "the melody acts out the coupling: the chorus's first half syncopated against the beat, the second half square on it",
                        "C": "no design: the engine draws the chorus as kept songs do"},
            "recommended": "A", "answer": "A"})
CHORUS_DESIGN = ("Q16 A: 'Two clocks on the same wall' rocks between two pitches a step apart (the band drops out under it); 'keeping time, keeping time' one rhythmic "
                 "cell twice, the second a step higher; 'fall on the one' lands every post-chorus phrase on a downbeat")
RUNS = dict(main=dict(survivors=732, order="077ff303e726", reproduced=True), ctl=dict(survivors=763, order="e3f1adf34008", reproduced=True),
            pick_362="6a61299cc70a", note="the pick's chorus register sits under the verse's (median 63.1 against 64.7; sung lift -3.5 at the median): "
                                          "the designed hook on E-flat 4 / D4 and the cell B-flat 3 - D4; the lift is the writer's at intake (298), not yet asked")
NOTE_358 = "358's passing notes read on the song's own sung extras (344: B natural, G-flat), not any pitch outside the scale (the first smoke pick sang E natural against C minor)"
LOG.append({"q": "17 (298)", "topic": "where the chorus sits against the verse",
            "options": {"A": "the chorus lifts: its median 3 or more over the verse's; the cell climbs to the chorus's top",
                        "B": "as drawn (a quarter of kept songs have the chorus under the verse)",
                        "C": "a narrow verse, then the chorus opens: the verses close and confined, the chorus over them and wider (the frame too small, then larger)"},
            "recommended": "C", "answer": "C"})
LIFT = "Q17 C: the verse's register seven semitones wide; the chorus's median 3 or more over the verse's, its top 3 or more over the verse's top, and its register 3 or more wider"
