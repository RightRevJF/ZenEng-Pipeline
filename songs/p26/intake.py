"""Song 26 intake (ZenEng v64 with the v65 fix list run as ports). The test: up-tempo pop/R&B with sixteenth-note phrasing -- the first
song off the eighth-note grid."""
LOG = [{"q": "which untested song type", "options": {"A": "up-tempo pop/R&B with sixteenth-note phrasing", "B": "country story song with a punchline hook",
        "C": "responsorial psalm setting"}, "recommended": "A", "answer": "A"}]
TITLE = None
LOG.append({"q": "subject (source B: three pitched)", "options": {"A": "Left on Read: a text read, no reply, the spiral", "B": "the kitchen at midnight: a long-married couple dancing",
            "C": "Friday at 5:01: the week over, out the door, the first free hour"}, "recommended": "B", "answer": "C"})
LOG.append({"q": "sound", "options": {"A": "funk-pop: 16th-note rhythm guitar, busy bass, horn stabs, handclaps", "B": "modern R&B-pop: synths, 808, rapid hi-hats",
            "C": "disco-pop: four-on-the-floor, strings, octave bass"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "voice (11.2)", "options": {"A": "male tenor D3-A4, Bb4 once (v65 fix 14 row)", "B": "female A3-B4, C5 once", "C": "male E3-F#4, G4 once"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "tempo and feel", "options": {"A": "q=112, straight sixteenths", "B": "q=104, swung sixteenths", "C": "q=120, straight sixteenths"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "form (lengths at q=112, 2 bars a line; v65 fixes 13/31)", "options": {"A": "full funk-pop form, 80 bars, 2:51", "B": "lean V-C-V-C-B-C, 60 bars, 2:09",
            "C": "extended: A plus a whole-step key change into the final double chorus, 88 bars, 3:09"}, "recommended": "A", "answer": "C"})
LOG.append({"q": "key", "options": {"A": "Eb major, lifting to F for the final double chorus; chorus tops G4 then A4; Bb4 once in the last chorus",
            "B": "F major lifting to G; tops G4 then A4; no Bb4", "C": "G major lifting to A; peak A4; no Bb4"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "title", "options": {"A": "Five-Oh-One", "B": "Out the Door", "C": "Windows Down"}, "recommended": "A", "answer": "A"})
TITLE = "Five-Oh-One"
LOG.append({"q": "never say", "options": {"A": "the weekend cliches (TGIF, living for the weekend, let's get this party started, work hard play hard, turn up)",
            "B": "A plus the drinking and club words (drink, shots, bar, club, party)", "C": "no list"}, "recommended": "B", "answer": "A and B (= B: both lists)"})
NEVER_SAY = ["tgif", "drink", "drinks", "drinking", "shot", "shots", "bar", "bars", "club", "clubs", "party", "partying", "booze", "beer", "whiskey", "wine", "tequila", "buzz", "drunk", "wasted", "lit"]
NEVER_PHRASES = ["thank god it's friday", "living for the weekend", "let's get this party started", "work hard, play hard", "work hard play hard", "turn up", "turnt up", "weekend warrior"]
LOG.append({"q": "who the singer is", "options": {"A": "office worker (badge, elevator, laptop, parking deck)", "B": "shift worker (time clock stamps 5:01, boots, work truck)",
            "C": "no job named: only the leaving shown"}, "recommended": "B", "answer": "C"})
LOG.append({"q": "where he's headed", "options": {"A": "home to the one he loves", "B": "nowhere in particular", "C": "to his people (backyard, cookout, game)"},
            "recommended": "A", "answer": "other", "writer": "I want a party song. Can't he be headed off to a good time?"})
LOG.append({"q": "a party song vs the never-say lists", "options": {"A": "keep both lists: show the party without naming it", "B": "allow 'party', keep the drinking/club words banned",
            "C": "drop the second list"}, "recommended": "A", "answer": "A"})
DESTINATION = "headed out to a good time (a party), shown and never named"
FORM_PLAN = "Intro 4 | V1 8 | Pre 4 | Ch 8 | Post 4 | V2 8 | Pre 4 | Ch 8 | Post 4 | Breakdown 8 | Lift pre 4 | (Eb->F) Ch 8 | Ch 8 | Post 4 | Outro 4 = 88 bars, 3:09"
LOG.append({"q": "lyric draft 1", "answer": "shown (lyric_draft1.md)"})
LOG.append({"q": "lyric notes 1", "writer": "But he's not going home, is he? That part at the end doesn't make sense"})
LOG.append({"q": "the last line's turn", "options": {"A": "five-oh-one, and I'm here", "B": "five-oh-one, and it's on", "C": "five-oh-one, and we're all here"},
            "recommended": "A", "answer": "A", "writer_adds": "show the lyrics with that change"})
LOG.append({"q": "lyric notes 2", "writer": "attached Five-Oh-One_Improvement_Suggestions.docx: 5:01 as a jailbreak (your time is yours again); keep chorus lines 1-2 and 'sixty hours', find a more distinctive last line (liberation / communal / playful); Verse 2 a more cinematic arrival; more observed human details; the breakdown a crowd moment ending in a shouted FIVE-OH-ONE; protect 'owes me money', 'lets out its breath', the grandmother line"})
LOG.append({"q": "lyric draft 3", "options": {"A": "lock it and write the music", "B": "more notes", "C": "different direction"}, "recommended": "A", "answer": "A"})
# ---- derived (run's port, v64 + v65 fixes as ports) ----
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 with the v65 fix list (songs 21-25) run as ports"
SOURCE_MATERIAL = "pitched subject (C, Friday at 5:01); the writer's notes and an attached suggestion document"
Q0 = ("five-oh-one", "Friday at 5:01: five days somebody else had his hours; the minute flips, the week lets go, and he heads out to a good time -- a backyard full of people, shown and never named")
SINGERS = {"him": "male tenor (11.2, v65 fix 14 row), D3-A4, Bb4 once"}
INSTRUMENT = "funk-pop band: 16th-note rhythm guitar, busy bass, horn stabs, handclaps, drums, keys"
OBJECTS = ["clock", "wall", "feet", "second hand", "money", "coat", "chair", "keys", "fist", "hall", "minute", "breath", "speakers", "car", "address",
           "flames", "town", "tie", "light", "avenue", "hours", "radio", "song", "red light", "truck", "blocks", "bass", "glass", "driveway", "neighbor",
           "plate", "grandmother", "monday", "shovel", "wrist"]
WRITER_PHRASES = ["five-oh-one", "the whole place lets out its breath", "like it owes me money", "and she's winning", "you'll find me here", "good luck finding me now"]
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "pre", "chorus", "hook", "breakdown", "lift", "shout", "tag"}
REQUIRED = {"story": Q0[1], "subject": "C Friday at 5:01 (pitched)", "sound": "A funk-pop", "voice": "A male tenor D3-A4, Bb4 once",
            "feel": "A q=112, straight sixteenths", "form": "C extended, 88 bars, whole-step lift into the final double chorus",
            "key": "A Eb major, lifting to F", "title": "A Five-Oh-One", "never-say": "A and B (both lists)", "who": "C no job named",
            "destination": "a good time (writer's own); the party shown, never named"}
ROUTING = "Anthem (A) primary; up-tempo funk-pop, one voice with a gang shout"
LOG.append({"q": "deliverables (after delivery)", "writer": "Do a parts pdf for the whole band", "answer": "parts: horns, guitar, electric piano, bass, drums with claps, gang cue sheet (13 pages)"})
LOG.append({"q": "blind pick (10.20)", "options": {"A": "if your Tuesday held the shovel, clap (Annotated top)", "B": "five-oh, five-oh, five-oh-one (Remembered top)",
            "C": "five-oh-one, the whole town loosens its tie (middle: top quartile under both)"}, "answer": "A"})
