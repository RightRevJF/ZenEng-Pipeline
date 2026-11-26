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
LOG.append({"when": "2026-11-26", "q": "When should song 66 get its music? A (Recommended) keep it unrun until the drafting fix is built, then make it for real with the design notes; it could also be that fix's fresh test song. B make it now on the current engine and redo it after the fix. C keep it unrun purely as a hold-out", "answer": "A"})
STATUS = "banked, unrun; reserved for the drafting fix (749.208 form) as its fresh test song, then made for real with DESIGN_NOTES_FROM_THE_WRITER"
LOG.append({"when": "2026-11-26", "who": "maintainer (via coord thread)", "what": "Song 66 spent as the sealed test of the pair (749.217): six marks of seven held, pitch scaling failed (1.062 against v50 0.912); the pair not built. On v50 song 66 reads well (verses over the ceiling 17.0 in 100). The test records are in studies/borrow_kept and are not the writer's song."})
STATUS = "spent as the pair's sealed test (749.217, failed mark 7); unmade for the writer; can be made on v50"
LOG.append({"when": "2026-11-26", "q": "Make song 66 for real now? A (Recommended) yes, on the current engine with the design notes; B wait in case the maintainer's last try succeeds; C not today", "answer": "B",
            "plan": "Made once the direction line (749.218 on) closes: on the fixed engine if a form passes its seen-song marks and sealed song 64, otherwise on v50."})
