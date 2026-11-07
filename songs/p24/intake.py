"""Song 24 intake (ZenEng v64; v65 not yet received). One question a turn, three options, logged."""
LOG = []
TITLE = None
LOG.append({"q": "source", "options": {"A": "a lived story", "B": "something he has written", "C": "an idea"}, "recommended": "A", "answer": "C",
            "writer_adds": "a tear jerker written for a male tenor and a guitar"})
SINGERS = {"him": "male tenor (writer)"}
INSTRUMENT = "guitar (the only accompaniment)"
LOG.append({"q": "kind of heartbreak", "options": {"A": "someone gone, through one object", "B": "a goodbye still happening (a parent fading, a child leaving)", "C": "something never said"}, "recommended": "A", "answer": "B", "writer_adds": "losing a parent to dementia"})
LOG.append({"q": "point of view", "options": {"A": "the grown child at visits; a repeated scene (telling them his name)", "B": "the parent, from inside the fog", "C": "both; the parent surfaces once in the bridge"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "which parent", "options": {"A": "mother", "B": "father", "C": "unsaid, so every listener puts their own there"}, "recommended": None, "answer": "C"})
LOG.append({"q": "voice (11.2)", "options": {"A": "tenor D3-A4, one Bb4 at the peak", "B": "tenor C3-G4, one A4", "C": "low and spoken D3-E4, peak F#4"}, "recommended": "A", "answer": "A", "note": "v64 11.2 has no tenor row -- a finding"})
LOG.append({"q": "guitar and feel", "options": {"A": "fingerpicked 3/4 waltz q=76, a lullaby rock", "B": "fingerpicked folk 4/4 q=66", "C": "strummed 4/4, full at the bridge"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "form", "options": {"A": "four verses (four visits), each closing on the same refrain line; a bridge after the third where he sings their old lullaby back; the last refrain changes; ~3:45", "B": "V C V C B C ~4:25", "C": "five verses, no refrain ~3:45"}, "recommended": "A", "answer": "A", "writer_adds": "show the proposed lyrics before drafting the music"})
LOG.append({"q": "key", "options": {"A": "F major, guitar capo 3 in D shapes; Bb4 peak over Bb (IV)", "B": "D minor, peak over Bb (bVI)", "C": "G major, Bb4 borrowed"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "never say", "options": {"A": "clinical words", "B": "sentimental cliches", "C": "both"}, "recommended": "C", "answer": "C"})
NEVER_SAY = ["dementia", "alzheimer's", "alzheimers", "disease", "diagnosis", "memory", "patient", "hospital",
             "angel", "angels", "heaven", "tears", "tear", "cry", "crying"]
NEVER_PHRASES = ["nursing home", "broken heart", "fade away", "in my heart", "gone too soon", "always with me"]
LOG.append({"q": "refrain", "options": {"A": "It is me. I am your son. (turns the last time)", "B": "Have we met?", "C": "I will be back on Sunday"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "It's Me", "B": "I'm Your Son", "C": "The Song You Sang Me"}, "recommended": "A", "answer": "C"})
TITLE = "The Song You Sang Me"
LOG.append({"q": "the lullaby", "options": {"A": "an original lullaby written for the song, heard first in the bridge", "B": "a traditional lullaby", "C": "an old hymn"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "lyric draft 1", "writer": "Where is the chorus?", "answer": "explained: form A has a one-line refrain, no chorus; options offered"})
LOG.append({"q": "chorus", "options": {"A": "keep the refrain form ~3:45", "B": "a new chorus after verses 2 and 4, the lullaby as bridge ~5:00", "C": "the lullaby becomes the chorus: after verse 2 and at the end (sung by both), no bridge ~4:25"}, "recommended": "C", "answer": "C"})
FORM_NOTE = "V1 V2 Chorus(lullaby) V3 V4 Final chorus(both); one-line refrain closes each verse; 4 bars a line, 3/4 q=76; ~4:25"
LOG.append({"q": "lyric notes 1", "writer": "V3 line 3 abstract/explanatory; the chorus imagery familiar (lamp low, river, hall light), no memorable turn; tone all gentle -- one harder, more specific image", "answer": "draft 3: V3 'You called me by your brother's name on Tuesday' / 'now you watch the birds come to the feeder' / 'I write my name in marker underneath the date'; chorus 'Go to sleep, I've got the dark / I'll keep it folded, keep it near / and if you wake and don't know where you are / I'll say your name till you know you're here'"})
LOG.append({"q": "lyric notes 2 -> draft 3", "answer": "B: locked (draft 3)"})
# ---- derived (run's port, v64) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 (the v65 fix list for songs 22-23 written; v65 not yet received)"
Q0 = ("the song you sang me", "losing a parent to dementia, seen by the grown son at his visits: he tells them his name every time; they know the lullaby they sang him when they no longer know him")
SINGERS = {"him": "tenor, D3-A4 (Bb4 once at the peak) -- the run's row: v64 11.2 has no tenor row"}
INSTRUMENT = "steel-string acoustic guitar, fingerpicked, capo 3 (D shapes) -- the only accompaniment; it plays the lullaby's tune alone in the intro and the outro"
OBJECTS = ["napkin", "window", "heat", "chair", "pictures", "lake", "august", "face", "hand", "brother", "tuesday", "birds", "feeder",
           "name", "marker", "date", "line", "time", "dark", "light", "sleep"]
WRITER_PHRASES = []
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "chorus", "hook", "refrain"}
REQUIRED = {"story": Q0[1], "source": "C an idea", "heartbreak": "B a goodbye still happening: losing a parent to dementia", "point of view": "A the grown child at visits",
            "parent": "C unsaid", "voice": "A tenor D3-A4, Bb4 once", "feel": "A fingerpicked 3/4 waltz q=76, a lullaby rock", "form": "A then C: four visits with a one-line refrain; the lullaby as the chorus (after verse 2 and at the end, sung by both)",
            "key": "A F major, capo 3 D shapes", "never-say": "C both lists", "refrain": "A It's me. I'm your son.", "title": "C The Song You Sang Me",
            "lullaby": "A an original lullaby", "details": "not asked -- an idea, not a lived story (v63 row: lived experience only)"}
ROUTING = "Narrative (N) primary with a Love song (V) refrain; folk ballad, one voice and one guitar"
LOG.append({"q": "music", "answer": "written: 800 built, 510 survived, pick 629622b1f9dc; 112 bars, 4:25; 27/27"})
LOG.append({"q": "10.20 blind pick", "options": {"A": "it is me. I am your song. (Remembered top)", "B": "you hold my hand the way you would hold anyone (middle: top quarter of both)", "C": "you touch a face and say, she used to swim (Annotated top)"}, "recommended": None, "answer": "A (Remembered top)"})
LOG.append({"q": "next", "answer": "A: the v65 fix list made complete for songs 21-24 (fixes 1-28, corrections C1-C6, blind-pick record 13-24; https://claude.ai/artifact/22vP86jMUxjoUBdy7mqz3H)"})
LOG.append({"q": "producer package", "answer": "A: built -- guitar part (capo 3, D shapes, notation + TAB, 4 pp), production doc (https://claude.ai/artifact/R4MKnC6wNoGz9hkUz1HKuK) + Word; refs verified: Campbell 2014, Isbell 2017, Clapton Unplugged 1992; the guitar re-voiced to true D shapes (demo, lead sheet rebuilt)"})
