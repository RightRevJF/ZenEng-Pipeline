"""Song 66 (songs/p76): from the writer's own older lyric ("They did the right thing"), revised by the session at his word. Words and music: Jason Bryant."""
LOG = []
LOG.append({"when": "2026-11-26", "q": "(the writer, pasting an older lyric from Chorus 1 on) Here's some old lyrics. What do you think?", "answer": "(the session's read) A make it song 66 (Recommended); B fix just the two chorus lines; C nothing for now"})
LOG.append({"when": "2026-11-26", "q": "(the writer pasted the full lyric, Verse 1 'The Borrowed Dark' through the Tag)", "answer": "Make all the changes you think work!"})
DESIGN_NOTES_FROM_THE_WRITER = ["Chorus ends: hold E4, at least 2 bars; the bass begins a chromatic descent", "Bridge: voice, guitar and bass only, the lowest level of the song", "After the bridge: all stop, 2 beats, every instrument, no fill", "Final chorus: full band back on the downbeat, no anticipation in the bar before; hold E4 3 bars; bass E, D#, D, C#, C", "Tag: voice and guitar, fading; hold E4, then decay; end on A minor, no resolution"]
LOG.append({"when": "2026-11-26", "q": "What do you think of the revision? A I have notes; B lock it and run the mouth tests; C restore something", "answer": "B"})
TITLE = "They Did the Right Thing"
NEVER_SAY = []
LOG.append({"when": "2026-11-26", "done": "lyric_locked.md; mouth_p76.py -> mouth_readings.txt (q = 76 provisional, six beats a line): 57 lines, median 8 syllables, nothing dense (max 2.53/s); weak endings 'been' (pre-chorus 1), 'should' (chorus), 'over' (verse 2), 'it' (bridge 'meant it'); close and reduced vowels at line ends; mild 4-consonant clusters; hook 5 syllables."})
LOG.append({"when": "2026-11-26", "q": "Keep the four weak endings? A keep all four as natural speech (Recommended); B rework only the chorus line; C rework all four", "answer": "A", "kept_knowingly": ["been", "should", "over", "meant it"]})
LOG.append({"when": "2026-11-26", "q": "What should song 66 sound like? A dark indie folk-rock, about 72 bpm, guitar-led, the falling bass, brushed drums, full band in the last chorus (Recommended); B slow minor-key soul, about 68; C slow-burning alt-rock, about 80", "answer": "A"})
GENRE, BPM, METRE, MODE = "rock", 72, "4/4", "minor"
LOG.append({"when": "2026-11-26", "q": "Who sings it? A a baritone (Recommended); B an alto; C a tenor", "answer": "C. We use baritones all the time. Let's use a renot [tenor]"})
VOICE = "tenor"
