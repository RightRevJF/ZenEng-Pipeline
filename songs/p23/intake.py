"""Song 23 intake (ZenEng v64). Every choice logged."""
LOG = []
LOG.append({"q": "seed", "writer": "a song suggesting paradox is the center of our existence; worried it is too intellectual, not physical enough; wants help writing the lyrics"})
LOG.append({"q": "where the images come from", "options": {"A": "things held up by opposing forces", "B": "the body: heartbeat, breath, the fist that opens to hold", "C": "one real moment"}, "recommended": "A", "answer": "B"})
LOG[-1]["answer"] = "A (changed from B at 12:27)"
LOG.append({"q": "change", "writer": "I want to change my previous answer to A", "answer": "images: things held up by opposing forces"})
LOG.append({"q": "sound", "options": {"A": "driving rock built on tension (riff against the beat, coiled verses, chorus releases)", "B": "prog rock again", "C": "quiet and close, acoustic"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "who sings", "options": {"A": "one male voice, rock anthem E3-G4 (A4 last chorus)", "B": "one female voice, pop A3-B4 (C5)", "C": "duet as two opposing forces"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "form", "options": {"A": "V C V C Bridge C, ~4 min, bridge where pressure peaks and turns", "B": "same plus instrumental break, 5-6 min", "C": "one long build, chorus only at the end"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "tempo and feel", "options": {"A": "4/4 q=104, riff pushes ahead of the beat", "B": "q=132 straight eighths", "C": "q=76 half-time heavy"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "key", "options": {"A": "E minor verses, G major chorus", "B": "D minor throughout", "C": "A minor verses, C major chorus"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "point of view", "options": {"A": "first-person I in a physical world; chorus states it plainly once", "B": "you: the two forces are singer and another", "C": "no narrator, stacked images"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "Keystone", "B": "What Holds", "C": "Push Against"}, "recommended": "A", "answer": "B"})
TITLE = "What Holds"
LOG.append({"q": "writer's standing asks", "answer": "show the proposed lyrics before music generation; deliver the full producer package (parts PDF, lyric sheet, brief, session notes as Word) as for song 22"})
LOG.append({"q": "never say", "options": {"A": "thinking words", "B": "rock cliches", "C": "both"}, "recommended": "C", "answer": "C"})
NEVER_SAY = ["paradox", "contradiction", "irony", "ironic", "existence", "duality", "balance", "universe", "meaning", "truth",
             "fire", "burn", "chains", "tonight", "scream"]
NEVER_PHRASES = ["break free", "rise up", "stand tall", "the edge"]
LOG.append({"q": "bridge turn", "options": {"A": "the singer finds he is built the same way: the strain keeps him standing", "B": "goes huge then back to two hands", "C": "names something bigger (love or God)"}, "recommended": "A", "answer": "A"})
SPAN = "q=104: two bars = 4.6 s x 2.1 = ~10 syllables; a line takes two bars"
LOG.append({"q": "lyric notes 1", "writer": "V1 lines 3-4 explanatory, trust the picture; chorus plain, needs a line that sticks; tighter, percussive phrases for the groove", "answer": "draft 2"})
LOG.append({"q": "lyric notes 2", "writer": "chorus middle lines plain (palm to palm...); final variation abrupt, needs one more strong syllable or image", "answer": "draft 3: rafters at the ridge / I'm rubble / final 'push me, and I stand: that's what holds'"})
LOG.append({"q": "show full lyric", "answer": "shown (draft 3, full)"})
LOG.append({"q": "lyric", "answer": "A: locked (draft 3, after two rounds of the writer's notes)"})
# ---- derived (run's port, v64) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 (the v65 fix list written for song 22; v65 not yet received)"
DELIVERABLES_NOTE = "songbook for musicians only; the engine record in a separate test report; the full producer package (parts PDF; lyric sheet, brief, session notes as Doc and Word)"
Q0 = ("what holds", "paradox at the centre of existence, made physical: things held up by opposing forces -- an arch, a wire, two palms -- and, at the bridge, the singer's own body")
SINGERS = {"him": "rock anthem (male), E3-G4 (A4 in the final chorus)"}
INSTRUMENT = "riff guitar (overdriven) -- the run's reading: the intro, the riff between chorus 1 and verse 2, and the outro carry the riff (27.21); no instrumental section was asked"
OBJECTS = ["granite", "curve", "river", "block", "ground", "stone", "air", "trucks", "hand", "palm", "rafters", "ridge", "rubble", "weight",
           "wire", "towers", "pole", "wind", "kitchen", "floor", "bone", "bones", "muscle", "strain"]
WRITER_PHRASES = []
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "chorus", "hook", "bridge"}
REQUIRED = {"story": Q0[1], "images": "A: things held up by opposing forces (changed from B, the body, at 12:27)", "sound": "A driving rock built on tension",
            "voice": "A one male voice, rock anthem E3-G4 (A4)", "form": "A V C V C Bridge C", "tempo-feel": "A 4/4 q=104, the riff ahead of the beat",
            "key": "A E minor verses, G major chorus", "point of view": "A first person in a physical world", "title": "What Holds",
            "never-say": "C both lists", "bridge": "A the singer built the same way", "details": "not asked -- the writer asked for help writing; the lines were drafted with him over three rounds",
            "names": "none", "instrumental": "none asked; the riff carries the intro, the break after chorus 1 and the outro"}
ROUTING = "Paradox (P) primary with Narrative (N) images; rock, one voice"
LOG.append({"q": "music", "answer": "written: 800 built, 400 survived, pick fd5d96ca768f; 78 bars, 3:00"})
LOG.append({"q": "deliverables", "answer": "lead sheet, chart, demo, songbook (Doc https://claude.ai/artifact/4pVzaWrkwBjh8GfZmoUFZw + Word), test report, parts PDF, production doc (https://claude.ai/artifact/JSBbYKyczNPWHMH5KiaZh7 + Word)"})
LOG.append({"q": "10.20 blind pick", "options": {"A": "what holds is the hand against me (Remembered top)", "B": "locked like rafters at the ridge (middle: the most-repeated hook line)", "C": "one muscle bends, one straightens (Annotated top)"}, "recommended": None, "answer": "B (middle)"})
LOG.append({"q": "next", "answer": "A then B: song 23 findings added to the v65 fix list (fixes 9-13, fix 6 amended; https://claude.ai/artifact/22vP86jMUxjoUBdy7mqz3H); then song 24"})
