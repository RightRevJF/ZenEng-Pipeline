"""Song 22 intake (ZenEng v64): a prog-rock song from the writer's novel 'Coda' (Coda_Novel_Final_v7.docx, 64,472 words). One question a turn, three options, logged."""
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 (the song 21 fix list sent with the v64 corrections; v65 not yet received)"
SOURCE = "/home/claude/p22/coda.txt"
SOURCE_MATERIAL = "novel (the writer's own fiction) -- background, not lines to set"
DELIVERABLES_NOTE = "from this song: the songbook for musicians only (no engine references); the engine record in a separate test report (writer, 20:26 Nov 5)"
LOG = [{"q": 1, "topic": "scale", "options": {"A": "one 6-7 minute song on the heart of it, an instrumental where the city dissolves",
        "B": "a four-movement suite, 12-15 minutes", "C": "one character's song (Reed)"}, "recommended": "A", "answer": "A",
        "writer_adds": "we can't trace through the whole book; it can't be just musical recitation of the plotline"}]
LOG.append({"q": 2, "topic": "what it's about (under the plot)", "options": {"A": "the seam: two worlds touching along a line that won't close; love across a boundary you can see but can't cross; the seam in his sky and the crack in her floor the same wound",
            "B": "what you make becomes real", "C": "the record that outlasts the world"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 3, "topic": "who sings", "options": {"A": "her (I, the side that built the door)", "B": "him (from his window)",
            "C": "both, a duet: her verses from the lab side, his from the window, the voices meeting only in the chorus, at the seam"}, "recommended": "C", "answer": "C"})
LOG.append({"q": 4, "topic": "form", "options": {"A": "her verse, his verse, the chorus together; again; a long instrumental where the city comes apart; the last chorus; an ending sung by him alone, ~7 min",
            "B": "three linked movements, voices meet only after the instrumental", "C": "alternating lines, one chorus, instrumental, ~5 min"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 5, "topic": "voices (11.2)", "options": {"A": "her: pop female A3-B4 (C5 last chorus); him: rock anthem (male) E3-G4 (A4 last chorus); the chorus in harmony, a third or sixth apart",
            "B": "her higher A3-C5 (D5); him baritone B2-C4", "C": "one register, the chorus in unison"}, "recommended": "A", "answer": "A",
            "writer_adds": "do the songbook the way we talked about (musicians only, no engine) even though the fix isn't in the engine; show the lyrics before music generation"})
SINGERS = {"her": "pop female, A3-B4 (C5 in the final chorus)", "him": "rock anthem (male), E3-G4 (A4 in the final chorus)", "chorus": "both, in parts (harmony a third or sixth apart)"}
LOG.append({"q": 6, "topic": "metre, tempo, feel", "options": {"A": "4/4 q=80 verses and choruses, spacious, half-time drums under the verses; the instrumental in 7/8 at the same pulse",
            "B": "6/8 dotted-q=66 throughout", "C": "4/4 q=120 driving"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 7, "topic": "key", "options": {"A": "her verses E minor, his F minor (a half step apart); the chorus in C major (VI of E minor, V of F minor); on the title word her G4 over his E4",
            "B": "one key, D major / B minor", "C": "E minor verses, G major chorus"}, "recommended": "A", "answer": "A"})
LOG.append({"q": 8, "topic": "register", "options": {"A": "narrative, leaning abstract; the book's images carry the meaning; no plot told", "B": "pop", "C": "folk"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": 9, "topic": "title (locked)", "options": {"A": "The Seam", "B": "Not Through Your Door", "C": "Coda"}, "recommended": "A", "answer": "A"})
TITLE = "The Seam"
LOG.append({"q": 10, "topic": "never-say (category expanded word by word, shown)",
            "options": {"A": "no plot machinery / sci-fi jargon: Nexus, simulation, replica, signal, extraction, protocol, code, matrix, glitch, pixel, virtual, program, algorithm, upload",
                        "B": "no cosmic love-song cliches: soulmate, destiny, forever, meant to be, two hearts, other side, worlds apart, parallel, universe, stars align, eternity, heaven",
                        "C": "both"}, "recommended": "C", "answer": "C"})
NEVER_SAY = ["nexus", "simulation", "replica", "signal", "extraction", "protocol", "code", "matrix", "glitch", "pixel", "virtual", "program",
             "algorithm", "upload", "soulmate", "destiny", "forever", "parallel", "universe", "eternity", "heaven"]
NEVER_PHRASES = ["meant to be", "two hearts", "other side", "worlds apart", "stars align"]
LOG.append({"q": 11, "topic": "names sung?", "options": {"A": "no names: I and you", "B": "names once each", "C": "no names, the book's musical words as ordinary words"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": 12, "topic": "the instrumental's instrument (27.21)", "options": {"A": "synth lead -- her instrument, the world coming apart in its own voice",
            "B": "lead guitar (overdriven)", "C": "piano"}, "recommended": "A", "answer": "A"})
INSTRUMENT = "synth lead (Q12 A)"
# ---- derived (run's port, v64) ----
Q0 = ("the seam", "two worlds touching along a line that won't close; love across a boundary you can see but can't cross; the seam in his sky and the crack in her floor the same wound -- a duet, her verses from the lab, his from the window, meeting only in the chorus")
OBJECTS_FROM = "the novel's images (background), no plot told (Q1, Q2 A, Q8 A)"
OBJECTS = ["seam", "crack", "floor", "grey", "room", "stairs", "chord", "hands", "wood", "glass", "window", "door", "light", "sky", "blue", "blues",
           "horizon", "coffee", "notebook", "record", "morning", "east", "towers", "bakery", "lamp", "corridor", "line", "edge", "edges", "keys"]
WRITER_PHRASES = ["fear requires surprise", "i am not afraid", "trust the third layer", "not through your door"]
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "chorus", "hook", "bridge"}
REQUIRED = {"story": "the seam (Q2 A)", "objects": "the novel's images (background)", "never-say": "C both", "voice": "A duet: her pop female A3-B4 (C5), him rock anthem E3-G4 (A4), chorus in parts",
            "tempo-feel": "A 4/4 q=80, half-time verses; the instrumental 7/8", "key": "A her E minor, his F minor, the chorus C major", "form": "A",
            "register": "A narrative, leaning abstract", "title": "The Seam", "unknown-words": "none", "readings": "none",
            "details": "not asked -- a novel given as background (v63 row: lived experience only)", "two-times": "not a frame form",
            "instrumental": "the city coming apart, 7/8, synth lead (27.21)", "names": "none sung (Q11 A)"}
ROUTING = "Love song (V) primary with Narrative (N) images and Paradox (P) for the chorus (two blues, both real, not resolving); prog rock, a duet"
SPAN = "q=80: two bars = 6.0 s x 2.1 = 12 syllables; a line takes two bars"
LOG.append({"q": "lyric review", "writer": "verse 4 notes (06:47) -> pass 3; 'anything else?' -> the run's two: the last chorus's turn, her glass", "answer": "A, and show the final draft before the music"})
LOG.append({"q": "10.20", "topic": "blind pick (offered without scores)",
            "options": {"A": "I leave the notebook on the sill", "B": "a seam across the sky", "C": "the seam won't close, the seam won't heal"},
            "slots": {"A": "Annotated top", "B": "middle (no line in both top quarters: the most-repeated hook line)", "C": "Remembered top"}, "recommended": None, "answer": "C (Remembered top)"})
LOG.append({"q": "production pack", "answer": "A (all five: parts PDF + production doc)", "then": "producer notes as Word"})
LOG.append({"q": "next", "answer": "A (v65 fix list Doc: https://claude.ai/artifact/22vP86jMUxjoUBdy7mqz3H)"})
