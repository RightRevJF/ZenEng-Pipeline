"""Song 64 (songs/p74): a lyric written to be banked unrun, as a fresh 4/4 hold-out for the engine. Words and music: Jason Bryant."""
LOG = []
LOG.append({"when": "2026-11-25", "q": "What should we do while we wait for the maintainer? A write a new lyric and bank it unrun as a fresh hold-out (Recommended); B finish the skill edit first; C the shorter-lines test", "answer": "A"})
LOG.append({"when": "2026-11-25", "q": "Which seed should song 64 be built on? A the last drive (Recommended); B the margins; C the phone call",
            "answer": "I don't like any of these, they seem cheesy. What about a woman, forced to turn off the life support for her son who was in an accident. She's talking to him like he's there but she's also saying goodbye without using those words"})
LOG.append({"when": "2026-11-25", "q": "What should song 64 sound like? A a slow piano ballad with strings, about 68 bpm (Recommended); B sparse indie folk, about 72; C slow soul with organ, about 66", "answer": "A"})
LOG.append({"when": "2026-11-25", "q": "How old is her son? A 19 (Recommended); B 16; C 30", "answer": "A"})
LOG.append({"when": "2026-11-25", "q": "How much should the song say about the accident? A never name it (Recommended); B one sideways detail; C name it plainly once", "answer": "A"})
LOG.append({"when": "2026-11-25", "q": "How should the song end? A in the moment, an ordinary line (Recommended); B a glimmer in what goes on; C a glimmer of faith, a prayer that doesn't sound like one",
            "answer": "C. BUT make sure it's bit an overtly Christian song. Unnamed hope if that's possible"})
LOG.append({"when": "2026-11-25", "q": "What should the title be? A 'Go On Ahead' (Recommended); B 'Somebody's Got You'; C 'Your Jacket's on the Chair'", "answer": "A"})
TITLE = "Go On Ahead"
GENRE, BPM, METRE, VOICE = "piano ballad with strings", 68, "4/4", "female (mezzo), the mother"
NEVER_SAY = ["god", "lord", "heaven", "angel", "angels", "jesus", "pray", "prayer", "goodbye", "bye", "die", "died", "dying", "death", "dead", "accident", "crash", "car", "wreck", "light", "heart", "soul", "tears"]
NOTES = "Never name the accident; no overt Christian words; hope unnamed; one plain feeling allowed late; a speaker with a stake and the son addressed throughout (the premise)."
LOG.append({"when": "2026-11-25", "q": "What do you think of draft 1? A I have notes; B lock it and run the mouth tests; C try a different angle", "answer": "B",
            "done": "lyric_locked.md and lyric64.json (banked, unrun: no room check, no build); mouth_p74.py -> mouth_readings.txt: 25 lines, median 9 syllables, 10 flagged (close vowels at line ends: do, you, street, nurse; weak ending 'good for it'; three 4-consonant clusters); hook 4 syllables; never-say none; lyric_people: I 7.0, you 9.5, named feelings 0.5."})
LOG.append({"when": "2026-11-25", "q": "Should I change verse 2's weak ending? A yes, to 'I wrote him back, you'll make it right' (Recommended); B keep as locked; C a different fix", "answer": "A",
            "done": "lyric_locked.md and lyric64.json changed; mouth tests rerun (mouth_readings.txt)."})
