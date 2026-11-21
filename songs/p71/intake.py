"""Song 61 intake (the writer: Jason Bryant). Source: his essay 'The Problem of the Other Mind' (v4; read, used, not stored here). Song 44, 'Keeping Time' (songs/p48), came from the same essay.
Engine: Luthier v44 as merged at 3aa9cd2, plus the verse-closer form ruled for in Review 29 (LUTHIER_VERSE_CLOSER=apart), built both ways."""
LOG = []
LOG.append({"q": "(the writer) The maintainer is almost offline until Wednesday morning. Should we try to do another song before we turn over fixes?",
            "options": {"A": "Write song 61 now (Recommended)", "B": "Make song 49 the hold-out and run it both ways", "C": "Rest until Wednesday"},
            "answer": "(attached The_Problem_of_the_Other_Mind_v4.docx) We used this once before but I'm convinced there's another song to be gleaned from understanding it"})
LOG.append({"q": "1. Which angle of the essay? (song 44 took the coupling: two clocks on one wall)",
            "options": {"A": "'It is not good to be alone': isolation narrows the body, company brings it back (section 4.2) (Recommended)", "B": "'The lights are on': the old problem as a love song", "C": "'He let himself be touched': the Incarnation as an epistemic event (4.3, 1 John 1:1)"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "2. Who is singing to whom? (song 58 already has a lonely old man and a visitor)",
            "options": {"A": "The one at the door: the singer pleads with someone shut in (Recommended)", "B": "The one coming back from a long stretch alone", "C": "The one alone, up to the moment the door opens"},
            "recommended": "A", "answer": "A.  I like this.  Female voice. Tearjerker.  She's pleading to an addicted love one to let her in"})
LOG.append({"q": "3. The sound",
            "options": {"A": "Piano ballad, slow 4/4 near 70, strings in the last chorus (Recommended)", "B": "Country ballad: acoustic, pedal steel, light band", "C": "Americana, building from voice and guitar to full band"},
            "recommended": "A", "answer": "A.  Im thinking something akin to the Needle and the Damage Done."})
LOG.append({"q": "4. The setting, given 'The Needle and the Damage Done' (Neil Young, solo acoustic, short, live, observational)",
            "options": {"A": "Piano, as spare as Needle: voice and piano only, short, no swell (Recommended)", "B": "Fingerpicked acoustic guitar, like Needle itself", "C": "Piano that opens up: spare verses, strings only in the last chorus"},
            "recommended": "A", "answer": "Can we do acoustic guitar that opens up"})
LOG.append({"q": "5. How it ends (the music opens up; the door may not)",
            "options": {"A": "The door stays shut: still on the step, the last chorus quieter (Recommended)", "B": "It opens a crack in the last verse", "C": "Left hanging: the last line stops before we know"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "6. How the addiction shows in the words",
            "options": {"A": "Never name it: no drug, no 'addict', no demons, chains, rock bottom, broken, angel, fight, the high; only what she sees and hears (Recommended)", "B": "Name it once, plainly, the stock words still banned", "C": "No list; cut what rings false in the drafts"},
            "recommended": "A", "answer": "A"})
NEVER_SAY = ["demon", "demons", "chain", "chains", "rock bottom", "broken", "angel", "fight", "high", "addict", "addiction", "drug", "drugs", "needle", "pills", "bottle", "fix", "clean", "sober", "relapse"]
LOG.append({"q": "7. How much of the essay shows",
            "options": {"A": "One bodily image: her ear to the door, listening for the life in him going flat alone; no science words (Recommended)", "B": "The essay's words, lightly ('your heart forgets how to change')", "C": "The Genesis line as the hook"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "8. The title",
            "options": {"A": "Ear to the Door (Recommended)", "B": "This Side of the Door", "C": "Let Me In"},
            "recommended": "A", "answer": "B"})
TITLE = "This Side of the Door"
LOG.append({"q": "Draft 1 shown; asked who he is (A her brother (Recommended), B husband or partner, C son)",
            "answer": "What do you think of these notes? 1. Verse 3 is slightly less sharp than the first two. 'I've said every word I could think of / And a few that I shouldn't have said' is true but more general than the rest of the song. The childhood knock is the real payoff of the verse; the two lines before it could be tighter. 2. A couple of lines tip toward the explanatory. 'I've got a key that won't turn anymore' is good, but sits next to 'I'm not here to take anything from you,' which names the feeling a little more directly than necessary. In the bridge, 'Maybe that's so, but I know one thing' is functional but slightly rhetorical compared to the more observational writing around it. 3. Chorus second half 'Every day that you keep to yourself / It gets harder to hear' is accurate, but the last chorus's revision ('I'll be here, I'll be here') is stronger. The first two choruses still lean a little more on statement than image.",
            "done": "Draft 2: all three notes taken (V1 'I didn't bring anyone with me'; chorus 'And the TV is doing the talking'; bridge 'I've heard it in meetings and waiting rooms / But nobody gets well...'; V3 'My knees have gone stiff on the doormat / And my coffee went cold in the car', 'Somebody's walking a dog'). Relationship question still open."})
LOG.append({"q": "9. Who is he? (the childhood knock makes him her brother)",
            "options": {"A": "Her brother (Recommended)", "B": "Her husband or partner", "C": "Her son"},
            "recommended": "A", "answer": "A"})
LOG.append({"q": "10. Lock draft 2? (one fix offered: chorus 'And the TV' to 'While the TV')",
            "options": {"A": "Lock draft 2 with that one fix (Recommended)", "B": "Lock draft 2 exactly", "C": "Not yet; more notes"},
            "recommended": "A", "answer": "A"})
LOG.append({"run": "python3 mouth_p71.py lyric_locked.md (q = 72 provisional, six beats a line)", "result": "48 lines, median 8 syllables; densest 2.40/s (bridge 'nobody gets well'), none over the p95; no tongue-twisters; clusters of 4 at 'first frost', 'didn't bring', 'and drum'; rare: yellowed, doormat; held vowels close or reduced at many line ends (-ing endings, 'Tuesday', 'me', 'breathe', 'wood'); weak ending 'it' (bridge, 'want it'). No change proposed: the -ing endings are unstressed and short, 'want it' is spoken with the weight on 'want'. mouth_readings.txt."})
LOG.append({"q": "11. Settings",
            "options": {"A": "Folk, 4/4, about 72 bpm, alto (G3 to D5), major, the engine picks the key, fingerpicked guitar leads (Recommended)", "B": "The same, mezzo (A3 to F5)", "C": "The same, slower (about 63) and minor"},
            "recommended": "A", "answer": "A"})
LOG.append({"run": "python3 lib/luthier/lyric_room.py songs/p71/lyric61.json (40 quick tunes), and trials", "result": "As locked at 72: bars unsung 0.064 (kept 0.121-0.282), change in busyness 0.224 (kept 0.343-0.558), rhythm scaling 0.599 (kept 25th 0.605), all under the kept 25th; 413 s over 124 bars; verse lines 8.6 syllables, chorus 7.1. The verse-closer form changes nothing here (few verse lines of 6 to 8 syllables stand apart). Bridge cut to its first four lines: 387 s; at 80 bpm: 348 s."})
LOG.append({"q": "12. Length (room check: 6:53 at 72; little rest; one busyness)",
            "options": {"A": "Trim the bridge to its first four lines, tempo 80, about 5:50 (Recommended)", "B": "Every word, tempo 80, about 6:10", "C": "Every word at 72, 6:53"},
            "recommended": "A", "answer": "Its way too long. It needs to be devastating and right around 4 minutes.  How can we compress and not lose depth or emotion",
            "done": "Draft 3: 36 lines (from 56). Length is set by the line count, not the tempo (the engine gives each line the seconds kept lines of its length take). Second chorus dropped; verses 1 and 2 to six lines; bridge its first four; verse 3 four. Room check at 80: 246 s over 82 bars; at 72: 273 s."})
LOG.append({"q": "13. Lock draft 3 at 80? (A lock (Recommended), B a short second chorus, C notes)",
            "answer": "If time is the real constraint, the highest-value things to restore (even in shortened form) would be: 1. One strong past detail in Verse 2 2. A little more air in the bridge 3. One more physical detail of the wait in Verse 3",
            "done": "Draft 4: V2 'You sang the wrong words just to make me laugh / And drummed on the wheel at red lights' (the red light back, the verse still six lines); bridge adds two short lines 'I'm not asking for more / Than a sound I can carry home'; V3 adds 'And my coffee went cold in the car'. 39 lines; room check at 80: 264 s over 88 bars."})
LOG.append({"q": "14. Lock draft 4 at 80?", "options": {"A": "Lock draft 4 at 80 bpm, 4:24 (Recommended)", "B": "Lock it, trimmed toward 4:00", "C": "Not yet"}, "recommended": "A", "answer": "A"})
LOG.append({"run": "mouth_p71.py on the locked lyric (q = 80); lyric_room.py songs/p71/lyric61.json", "result": "New lines clean ('drummed' rare, a cluster of 4 at 'and drummed'). Room: bars unsung 0.06, change in busyness 0.25, rhythm scaling 0.583, all under the kept 25th; 264 s over 88 bars. Written to lyric61.room.json."})
LOG.append({"run": "python3 lib/luthier/song_from_lyric.py songs/p71/lyric61.json 1000 12, as built and with LUTHIER_VERSE_CLOSER=apart (Luthier v44, main 3b83673)", "result": "Both byte for byte the same (no verse line of 6 to 8 syllables stands apart). Key E (G3 to B4 as planned; F#3 to B4 as sung), pick 2573b5e71acf, 326 builds live, pool 25; the first build past the gates spans 15, under the floor 15.52 (asked 18.9), the pick spans 16; words' fit 0.363; commonest pitch 0.387 verse, 0.388 chorus; 88 bars, 264 s. Chant check: longest run 4."})
LOG.append({"inspect": "the pick by hand", "result": "Top B4 on 'wood' (stressed) in both choruses; 'And it's down to one note' sung on one note (F#4) but one. 'Three, and then two' (verse 3 and last chorus): 'three' a quarter beat, 'and' 2.25 beats, 'then' 3.25 beats, the length on the weak words (finding for the next list, 749.147). 'were kids': 'were' held 1.25 beats, 'kids' a half. Taken as drawn; a hand fix to be offered."})
LOG.append({"arrangement": "the writer's (intake 3-5): fingerpicked guitar from the engine's chord tones throughout; cello (the engine's chord roots) from verse 2; strings (its chord tones) and bass (the engine's bass line) in the bridge and the last chorus; the engine's harmony voice in the last chorus to its sixth line; all but the guitar out at 'Three, and then two' (bar 81) and in the outro; no drums.",
            "documents": "first edition: demo (MP3, General MIDI), lead sheet, full score, parts, number chart, MusicXML, songbook (Doc and Word), test report; consistency61: 56 of 56. References checked by search: Neil Young 'The Needle and the Damage Done' (Harvest, 1972); Brandi Carlile 'Sugartooth' (By the Way, I Forgive You, 2018); Lucinda Williams 'Sweet Old World' (Sweet Old World, 1992).",
            "docs": {"songbook (first edition)": "https://claude.ai/artifact/JdWVgGU7Nb2e8SwkBvpKZz"}})
LOG.append({"q": "15. The knock line: A fix it by hand (Recommended), B leave it, C let the engine choose again",
            "recommended": "A", "answer": "A.  And what about this? Two suggestions toward 9.5, if you want them: a diatonic variation of a non-title line in verse 3 (0 DU), and one borrowed chord, G major under \"But nobody gets well in a room with one chair\" (bar 53, 1 DU). The honest cost on the second is that it breaks the bridge's stillness, which is the design.",
            "done": "Second edition (hand61.py -> lyric61.hand.song.json; the engine's record untouched; first edition kept in out/first_edition_v44): 'Three, and then two' re-timed in verse 3 and the last chorus ('three' on the downbeat a beat and a half with its melisma, a half-beat breath, 'and then' quick on beat 3, 'two' on the next downbeat); suggestion 1 taken on the verse-3 line 'when we were kids': 'were' a half beat, 'kids' held two beats and lifted E4 to G#4. Words' fit 0.363 to 0.404. Suggestion 2 not taken yet: the bridge melody at bar 53 sits on C#4, B3 and G#3 (G#3 five times), and G major (G B D) puts G natural against G# and a tritone under C#. 56 of 56 checks.",
            "docs": {"songbook (second edition)": "https://claude.ai/artifact/BP85opYSZdXD21Cb3UCQ1q"}})
