"""Song 25 intake (ZenEng v64; v65 not yet received). Source: the writer's 'Wild Fruit: Parables for Your Soul' (34,257 words):
The Garden That Grew by Itself (8 chapters) and seven parables -- The Room Next Door, The Woman Who Wore the Ground, The Luthier Who
Could Not Hear, The Woman Who Kept the Time, The Young Man Who Held Still, The Woman Who Dropped Stones, The Cracked Bell."""
LOG = [{"q": "source", "writer": "here is some material to read to consider for the next song (Wild_Fruit_KDP_v4.docx)"}]
TITLE = None
LOG.append({"q": "which parable", "options": {"A": "The Cracked Bell", "B": "The Woman Who Kept the Time", "C": "The Room Next Door"}, "recommended": "A", "answer": "A"})
SOURCE = "/home/claude/p25/src/wild_fruit.txt (The Cracked Bell, lines 1271-1500; epigraph 2 Corinthians 4:7)"
LOG.append({"q": "who tells it", "options": {"A": "third-person story ballad", "B": "the keeper, first person", "C": "congregational, we are the cracked bells"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "sound", "options": {"A": "folk: guitar, cello, a real bell on the night", "B": "piano ballad: piano as the bell (low ringing octaves; the crack a half-step struck together), strings build to the night", "C": "cinematic indie-folk"}, "recommended": "B", "answer": "B"})
LOG.append({"q": "voice (11.2)", "options": {"A": "female A3-B4 (C5)", "B": "male E3-F#4 (G4)", "C": "bass/baritone B2-C4 (D4)"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "tempo and feel", "options": {"A": "slow 4/4 q=66 tolling", "B": "6/8 in two, dotted-q=54, the bell swinging", "C": "3/4 waltz q=84"}, "recommended": "B", "answer": "B"})
LOG.append({"q": "form", "options": {"A": "two long verses each into the chorus; the winter night as bridge; last chorus turned ~3:10", "B": "four short verses, chorus after 2 and 4 and turned ~2:20", "C": "five long verses, no chorus ~3:15"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "key", "options": {"A": "A minor verses, C major chorus; C5 on the tonic at the turn", "B": "Eb major", "C": "D minor throughout"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "The Cracked Bell", "B": "Through Its Breaking", "C": "The Note Is Still in It"}, "recommended": "B", "answer": "B"})
TITLE = "Through Its Breaking"
LOG.append({"q": "never say", "options": {"A": "the sermon words", "B": "the cliches (and clear of Cohen's crack/light)", "C": "both"}, "recommended": "C", "answer": "C"})
NEVER_SAY = ["grace", "god", "lord", "faith", "redemption", "purpose", "blessing", "miracle", "healing", "scars", "scar", "shine", "shining"]
NEVER_PHRASES = ["light gets in", "let the light in", "beautiful mess", "perfectly imperfect", "gold in the cracks", "rise up", "everything happens for a reason"]
LOG.append({"q": "the winter night's need", "options": {"A": "unnamed, as the parable", "B": "a fire", "C": "a child lost in the snow"}, "recommended": "A", "answer": "A", "writer_adds": "show the lyrics before drafting the music"})
LOG.append({"q": "lyric notes 1", "writer": "V1 lines 5-8 list functions -- trim; chorus second couplet lacks weight/originality; her interior life sketched -- one more precise interior moment", "answer": "draft 2: V1 six lines; chorus 'like your name in a stranger's mouth / and every hour she rings it through'; V2 'she never meant to love the thing / it found her, year by year, at the wheel'"})
LOG.append({"q": "lyric draft 2", "answer": "B: locked"})
# ---- derived (run's port, v64) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 (the v65 fix list for songs 21-24 written; v65 not yet received)"
SOURCE_MATERIAL = "the writer's parable 'The Cracked Bell' (Wild Fruit) -- background; its last lines and the keeper's thought used as the writer's words"
Q0 = ("through its breaking", "a cracked bell that cannot sound its true note, tended for eleven years by a keeper built for maintenance; on a winter night it is the only bell, and its split note carries further than a true one -- it rang not despite its breaking but through it")
SINGERS = {"her": "female (11.2), A3-B4 (C5 once at the turn)"}
INSTRUMENT = "piano (the bell: low ringing octaves and the crack as a half-step struck together) with strings building to the night; no instrumental melody asked (27.21 not run)"
OBJECTS = ["tower", "town", "bell", "moss", "crack", "side", "thumbnail", "note", "tune", "name", "mouth", "hour", "oil", "rope", "wheel",
           "palm", "bronze", "dark", "night", "snow", "valley", "hands", "roofs", "fields", "doors", "sound"]
WRITER_PHRASES = ["the note is still in it", "the crack runs up the bronze", "the bell rings", "the sound carries", "through its breaking"]
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "chorus", "hook", "bridge", "tag"}
REQUIRED = {"story": Q0[1], "who tells it": "A third-person story ballad", "sound": "B piano ballad; the piano as the bell; strings build",
            "voice": "A female A3-B4 (C5)", "feel": "B 6/8 in two, dotted quarter = 54", "form": "A two long verses into the chorus; the night as bridge; the last chorus turned; tag",
            "key": "A A minor verses, C major chorus; C5 on the tonic at the turn", "title": "B Through Its Breaking", "never-say": "C both lists (clear of Cohen)",
            "the need": "A unnamed", "details": "not asked -- the writer's own parable as background"}
ROUTING = "Narrative (N) primary with a Paradox (P) turn; piano ballad, one voice"
LOG.append({"q": "deliverables (after delivery)", "writer": "since it's a piano piece, engrave the whole song; merge the songbook with the producer notes",
            "answer": "full score (voice, piano with the bell, cello, strings); one document: songbook + lyric sheet, production brief, session notes, score and parts"})
LOG.append({"q": "blind pick (10.20)", "options": {"A": "it rang through its breaking (middle: top quartile under both)", "B": "and every hour she rings it through (Remembered top)", "C": "the bell rings (Annotated top)"}, "answer": "A"})
