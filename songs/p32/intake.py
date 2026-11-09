"""Song 32 intake (ZenEng v64 + the v65 fix list, fixes 1-94). One question a turn, three options, logged.
The brief: an Easter solo in the vein of song 29, 'The Breath That Made the World' -- a concert solo for one high voice, the theology told
through the body and one plain moment, plain words, never sweet."""
LOG = []
TITLE = None
LOG.append({"q": "goal", "answer": "Okay. I think we are hot. Ready to write an Easter solo in a similar vein to The Breath that Made the World?"})
TEMPLATE = "song 29 (concert carol: one high voice, piano, cello, strings; anchors; a summit note; an open ending)"
LOG.append({"q": 1, "topic": "the moment (song 29 told the Incarnation through one plain scene: the Word who cannot yet speak)",
            "options": {"A": "the garden: Mary Magdalene takes him for the gardener until he says one word, her name (John 20:16); song 29's first word was Abba, this one's is Mary",
                        "B": "the breath: he breathes on the disciples behind the locked door (John 20:22); a companion to song 29's 'breath that made the world'",
                        "C": "the beach: he cooks fish over charcoal at dawn and says 'come and have breakfast' (John 21:9-12); the risen body that is hungry"},
            "recommended": "A", "answer": "A"})
Q0 = ("the garden", "Mary Magdalene, weeping at the empty tomb, takes him for the gardener until he says one word: her name (John 20:16)")
LOG.append({"q": 2, "topic": "who sings",
            "options": {"A": "Mary herself, first person: 'I took him for the gardener'; she quotes him saying her name and answers 'Rabboni' (two anchors). A woman's song: soprano and mezzo editions, no tenor",
                        "B": "a narrator, third person, as in song 29: 'she took him for the gardener'; keeps the soprano and tenor editions",
                        "C": "Christ, second person, to her: 'you took me for the gardener'; the name is his to sing"},
            "recommended": "A", "answer": "A"})
SINGERS = {"her": "Mary Magdalene, first person; soprano and mezzo editions (fix 92)"}
LOG.append({"q": 3, "topic": "the turn (what the last refrain comes to mean)",
            "options": {"A": "'do not hold on to me' (John 20:17): she has to let go; the song ends with her sent, running to tell them",
                        "B": "the gardener was right: 'I took him for the gardener, and he was' -- the first garden made new; her mistake was the truth",
                        "C": "her name as the new creation: the voice that said 'Let there be light' (song 29's first line) says 'Mary', and the world begins again"},
            "recommended": "B", "answer": "B"})
TURN = "the gardener was right: 'I took him for the gardener, and he was' -- the first garden made new; her mistake was the truth"
PRIOR_ART = {"Christ the gardener; 'she was right'": "a common Easter sermon point (Zahnd 'The Gardener'; Episcopal 'First Fruits of a New Garden'; Christianity Today 2026 'Supposing Him to Be the Gardener'): the theology is familiar, so the freshness must come from the details and the first person",
             "'The Gardener'": "taken many times: Child ballad 219, Christy Moore (Paul Doran), Marilyn Manson, sermon titles",
             "'I Took Him for the Gardener'": "no song found (8 Nov search)"}
LOG.append({"q": 4, "topic": "title (fix 94: sung, on the peak, short, no clash)",
            "options": {"A": "I Took Him for the Gardener -- the refrain's line, sung every time, the turn's own words; no song found by that name; long (8 syllables)",
                        "B": "And He Was -- the turn's payoff, 3 syllables; a near-echo of Talking Heads' 'And She Was'",
                        "C": "Rabboni -- her one-word answer, an anchor; distinctive but unfamiliar to most listeners"},
            "recommended": "A", "answer": "A"})
TITLE = "I Took Him for the Gardener"
LOG.append({"q": 5, "topic": "the harmonic arc",
            "options": {"A": "dark to light: minor while she weeps ('while it was still dark'); the moment he says 'Mary', the music turns to its major -- the name is the sunrise",
                        "B": "major throughout, plain and warm, with one borrowed chord under the name (song 29's way)",
                        "C": "minor throughout, the major arriving only on the last line ('and he was'), held open"},
            "recommended": "A", "answer": "A"})
ARC = "minor while she weeps; the music turns to its major on MARY (the name is the sunrise)"
LOG.append({"q": 6, "topic": "metre and tempo",
            "options": {"A": "6/8 at a slow lilt (dotted quarter about 52): a walking pace in the garden at dawn, rocking, unhurried",
                        "B": "3/4 at about 66, the Christmas song's metre: the two read as a pair",
                        "C": "4/4 at about 60, plain and speech-like: the most room for the words"},
            "recommended": "A", "answer": "A"})
FEEL = {"meter": "6/8", "qbpm_dotted": 52, "feel": "a slow lilt, walking pace in a garden at dawn"}
LOG.append({"q": 7, "topic": "form (lengths at dotted quarter = 52, two bars of 6/8 a line; fix 13/56)",
            "options": {"A": "song 29's shape: Intro 4 | V1 8 | R1 8 | V2 8 | R2 8 | Interlude 4 | V3 8 | the Name (bridge) 8 | V4 8 | R3 8, broadening | Coda 4 = 84 bars, about 3:20. Told looking back, so the refrain 'I took him for the gardener' can come from the start; 'and he was' arrives in the last refrain",
                        "B": "three parts, through-composed (the dark; the name; the light), the refrain line closing each part: about 100 bars, 3:55",
                        "C": "lean: Intro 4 | V1 8 | R1 8 | V2 8 | the Name 8 | R2 8, turned | Coda 4 = 48 bars, about 2:00"},
            "recommended": "A", "answer": "A"})
FORM_PLAN = "Intro 4 | V1 8 | R1 8 | V2 8 | R2 8 | Interlude 4 | V3 8 | the Name (bridge) 8 | V4 8 | R3 8, broadening | Coda 4 = 84 bars, about 3:20; told looking back"
LOG.append({"q": 8, "topic": "never say",
            "options": {"A": "the Easter cliches: risen, alleluia, hallelujah, glory, triumph, victory, conquer, defeated, lilies, angels, heaven, salvation, sin, hope, new life, sunrise; and 'he is risen', 'rolled away', 'death, where is your sting', 'up from the grave', 'Easter morning'",
                        "B": "list A, but allow the gospel's own words where Mary says them ('they have taken my Lord', the angels in white)",
                        "C": "no list"},
            "recommended": "A", "answer": "A. The key as always is theological and emotional depth"})
NEVER_SAY = ["risen", "alleluia", "hallelujah", "glory", "triumph", "victory", "conquer", "conquered", "defeated", "lily", "lilies", "angel", "angels",
             "heaven", "salvation", "sin", "hope", "sunrise"]
NEVER_PHRASES = ["new life", "he is risen", "rolled away", "where is your sting", "up from the grave", "easter morning"]
DEPTH_RULE = "the key as always is theological and emotional depth (writer)"
OBJECTS = ["spices", "stone", "linen", "cloth", "head", "bed", "garden", "gardener", "dawn", "white", "name", "dead", "body", "feet", "hands", "dirt", "tomb", "myrrh"]
WRITER_PHRASES = ["i took him for the gardener", "and he was", "rabboni", "mary"]
WRITER_WORDS = ["rabboni"]
LEXICON = {}
ROLES = {"verse", "refrain", "hook", "bridge", "turn", "tag"}
INSTRUMENT = "piano, cello, strings (song 29's ensemble)"
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "room": "w1.py: every line scored; deaths fixed before showing (V2 line 3 -> 'folded in a place by itself'; the bridge's 'I begged him for the dead'; V4 rebuilt around Genesis 3:8-9 after 'where' read weak -- stress port, finding)",
 "answer": "C. (1) V3 last line: 'outside' lands vaguely -- keep 'someone' (the not-knowing is the point) but give him somewhere to stand. (2) 'I begged him for the dead' slightly compressed; plainness tips into terseness -- worth one look, though 'for the dead' has a bluntness 'for his body' would lose. (3) The angels are the least vivid part; the only passage that reports rather than shows; one concrete detail would carry it."})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "changes": ["V3: 'one at his head, one at his feet' (John 20:12: they frame the empty place); 'and someone stood among the trees' (Genesis 3:8, where Adam hid)", "The Name: 'I said, just give me back my dead' (blunt, but plain about what she wants)"],
 "answer": "notes received one at a time ('Don't do anything but receive these notes until I tell you what to do'): (1) V3 the angels still report, static; the two halves sit awkwardly; (2) The Name: pasted text repeated note 1; (3) V1 lacks the concrete weight of 'I knew how to wash the dead' -- stay in the body; (4) last refrain line 3 slightly explanatory. Then: 'Now what do you think of the notes?' and 'Show me what you've got for now'"})
LOG.append({"q": "lyric draft 3", "file": "lyric_draft3.md", "changes": ["V1: 'I'd tied my hair back for the work'", "V3: 'Two sat in white, a body's length / of empty stone between' (the gap as the image)", "last refrain: 'his hands in the earth again' (burial reversed)"],
 "answer": "notes: (1) 'just give me back my dead' a half-step outside the plain register -- 'the body' (his lean) or 'my Lord'; (2) V4 line 3 'asking where' soft -- 'still asking' or 'and called'; (3) V3 enjambment 'a body's length / of empty stone between' slightly literary (note cut off). Then: 'Revise the lyrics'"})
LOG.append({"q": "lyric draft 4", "file": "lyric_draft4.md", "changes": ["The Name: 'I said, just give me back the body' (his lean)", "V4: 'I walked this one in the dark and called' (God called the man; she called; he answered)", "V3: 'Two sat in white on either side, / the stone between them clean' (no enjambment; 'clean': she came to wash the dead and the place is already clean)"], "answer": "A"})
LOG.append({"q": "lock", "options": {"A": "lock draft 4 as it stands and write the music", "B": "take the micro-adjustments first ('clean' -> 'bare'; 'his hands still in the earth'; a period on the last line)", "C": "one more full pass"},
            "recommended": "A", "answer": "A",
            "note": "the writer's micro-notes offered after draft 4 ('clean' -> 'bare' or 'empty'; 'his hands still in the earth'; give the last line a period: 'the song should close, not trail') -- answered A: lock as is. Draft 4 already ends on a period."})
LOG.append({"q": "ports at the lock", "ports": ["song 32 stress port: line-final 'where/why/who/own/was' stressed; in-STEAD, it-SELF, SOME-one, rab-BO-ni (findings)"]})
LOG.append({"q": "blind pick (10.20)", "options": {"A": "and someone stood among the trees. (middle)", "B": "I said, sir, if you carried him, (Annotated top)",
            "C": "I took him for the gardener, (Remembered top)"}, "answer": "C", "slot": "Remembered top (the title line)"})
LOG.append({"q": "revision 1: verse 3 line 2", "note": "writer: 'One of the things I remain reluctant about is the clean line in the song. I know you like it but I don't think the lyric works because it confuses the listener.'",
            "options": {"A": "with no one in between (no one / someone two lines later; the same rhythm and long-e sound)", "B": "and nothing in between", "C": "keep 'the stone between them clean'"},
            "recommended": "A", "answer": "A"})
