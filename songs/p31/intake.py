"""Song 31 intake (ZenEng v64 + the v65 fix list, fixes 1-79). One question a turn, three options, logged.
The brief: the next hit; sex told through engaging euphemism (the 'Cake by the Ocean' vein) -- evocative and fun, never graphic or comical."""
LOG = []
TITLE = None
LOG.append({"q": "goal", "answer": "Let's write our next hit. An easy subject but hard to land - sex. It should be in the lyrical vein of 'Cake by the Ocean' and other songs that talk about sex by engaging euphemisms. The key is that the language must be evocative and fun without lapsing into being graphic or comical."})
TONE_RULE = "two levels: innocent on the surface, unmistakable underneath; evocative and fun; never graphic, never comical (writer)"
LOG.append({"q": 1, "topic": "sound", "options": {"A": "dance-pop / funk-pop ~118 BPM (the 'Cake by the Ocean' lane)", "B": "slow R&B ~70 BPM", "C": "up-tempo country-pop"},
            "recommended": "A", "answer": "A. But the music has got to be both memorable and innovative without being too novel"})
MUSIC_RULE = "memorable and innovative without being too novel (writer): familiar frame, one or two fresh moves (the research's sweet spot)"
PRIOR_ART = {"late checkout": "taken: Lil Durk 'Late Checkout' (2024, explicit, the same idea); Dent May album (2020)",
             "tan lines": "taken: Zach Top 'Good Times & Tan Lines' (2025 hit); kenzie 'tan lines' (2025, sexual)",
             "power outage": "open: no pop hit uses the outage as a sex euphemism (Arcade Fire 'Neighborhood #3 (Power Out)' is unrelated)"}
LOG.append({"q": 2, "topic": "the central euphemism", "options": {"A": "the power outage: the block goes dark, no Wi-Fi, nothing on but us", "B": "the snow day", "C": "late checkout (taken: Lil Durk 2024)"},
            "recommended": "A", "answer": "A. Seems pretty universal to me"})
Q0 = ("power outage", "the whole block goes dark, no Wi-Fi, nothing on but the two of us -- sex told through the outage")
LOG.append({"q": 3, "topic": "voice", "options": {"A": "female lead, sly and in control (the Sabrina Carpenter lane)", "B": "male lead", "C": "duet"}, "recommended": "A", "answer": "A"})
SINGERS = {"her": "female pop lead"}
LOG.append({"q": 4, "topic": "title / hook", "options": {"A": "Nothing On (no TV, no lights, no Wi-Fi... and nothing on)", "B": "Off the Grid", "C": "Power's Out"}, "recommended": "A", "answer": "A"})
TITLE = "Nothing On"
LOG.append({"q": 5, "topic": "the turn", "options": {"A": "the power comes back at 2 a.m. and she switches it off again (the outage was luck; now it's her choice)",
            "B": "morning after: the neighbors complain, she's never been happier", "C": "no turn"}, "recommended": "A", "answer": "A"})
NEVER_SAY = ["sex", "sexy", "naked", "nude", "body", "bodies", "bed", "sheets", "baby", "tonight", "electric", "spark", "sparks", "chemistry",
             "dance floor", "kiss", "lips", "hips", "skin", "heaven", "fire", "burn", "hot"]
NEVER_PHRASES = ["turn me on", "turn you on", "lights out", "power of love", "sparks fly", "rock my world", "all night long"]
FORM_PLAN = "Intro 4 | V1 8 | Pre 4 | Ch 8 | Post 4 | V2 8 | Pre 4 | Ch 8 | Post 4 | Bridge 8 (the turn) | Ch 8 (turned) | Post 4 + tag = about 2:35 at q = 118"
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "answer": None})
LOG[-1]["answer"] = ("A. Five notes: (1) pre-chorus 1 is coy ('lose a layer') -- make it about the room getting warm and let the chorus flirt; "
                     "(2) pre-chorus 2's second line does no job -- a physical direction in the dark that 'go by feel' answers; (3) the bridge's last line is a stage direction, "
                     "not a decision -- put the choice in the body (a hand, a hesitation) and leave the explanation to the final chorus; (4) give 'you' one more detail; "
                     "(5) trim the knocking line -- too many syllables for one breath; keep the outside world intruding and ignored")
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md", "answer": None})
LOG[-1]["answer"] = "Okay. Lock the lyrics. But before you write the music, do as deep a research dive as you can into contemporary hit music: see the trends, somewhat mimic them while leaving room for departure -- familiar enough not to be rejected, deviating enough to stand out. Use whatever corpora you can find."
LOCKED = "lyric_draft2.md (locked 8 Nov 04:47)"
RESEARCH = {  # 8 Nov 2026
 "optimal differentiation": "Askin & Mauskapf 2017 (ASR, ~27,000 Hot 100 songs): highly typical songs do worse; songs somewhat below average typicality do best",
 "2025 top 10": "pop back on top; retro influences in ~1/3 (the 1980s most popular for the sixth year); acoustic-sounding drums overtook electronic for the first time since 2014; synth use down four straight years; more guitar; major key 53% vs minor 45% (mid-2025); post-chorus hook center 63%",
 "exemplars": "Espresso (104 BPM, A minor, a two-bar iv-v loop that never lands on the tonic, phrases starting on weak beats, end-accented, melody loosely tied to chords, dense layered production); Cake by the Ocean (119 BPM, disco-pop); Manchild (123 BPM, G major, country-disco); I Just Might (Bruno Mars, 2026 #1 debut: funk guitar, bongos, handclaps, trumpets on the hook, P-bass); Man I Need (Olivia Dean, retro soul-pop, keyboard riff); Where Is My Husband! (RAYE, big-band brass, voice as percussion in breakdowns)",
 "harmony corpus": "Hooktheory: C-G-Am-F (I-V-vi-IV) and C-F-G-C the most common four-grams; IV and V appear in more progressions than I -- leaving out the tonic for effect is common",
 "local melody corpus (515 pop melodies)": "chorus range median 14 semitones (p25-p75 12-17); chorus above verse median +3 (p75 +5); chorus syncopation median 0.10 (p75 0.17, p95 0.32); leaps 13.5%, steps 45%; chorus ends on the tonic 53%",
}
MUSIC_PLAN = {"familiar": "112-120 BPM disco-funk pop; live-sounding kit, P-bass, funk guitar, handclaps, a horn stab hook; verse-pre-chorus-chorus-post-chorus; under 3:00; diatonic chords; melodic features inside the corpus's middle band",
              "departures (2-3 only)": ["the tonic withheld: a loop that never lands on I until the lights come back in the bridge; she turns them off and the loop returns",
                                       "the power cut: the band dies for a beat (tape-stop) at the top of each chorus on 'nothing on'; the bridge's return slams back in",
                                       "phrasing displaced: hooks start on weak beats, syncopation pushed to the corpus's 75th-90th percentile, every other feature in the middle band"]}
LOG.append({"q": "Q6 music direction (after the research)",
 "options": {"A": "Disco-funk at 116, minor-leaning; a two-chord loop that never lands home until the lights come back in the bridge; the band cuts out on 'nothing on'; hooks start off the beat (Recommended)",
             "B": "Brighter country-disco at 120 in a major key, Manchild-style; one departure only, the band cutting out",
             "C": "Slower, sultrier groove at 104, Espresso-style, with more space and a softer cut"},
 "rec": "A", "answer": "A. But we need to work on the lyrics more: (1) chorus reveals the relationship, not the outage; (2) promote 'the lights came back and I turned them off' -- plant in Chorus 2, pay off in the final chorus; (3) one instantly repeatable, quote-worthy line; (4) strengthen Verse 2, replace the neighbor knock with intimacy; (5) bigger final lift -- town comes back, phone comes back, she rejects it; tie to 'the only thing glowing is you'. The real song: 'The power came back, and I didn't want it.'"})
LOG.append({"q": "draft 3 (after notes on draft 2)", "file": "lyric_draft3.md",
 "changes": ["chorus line 2-3 now a choice that escalates: hope they stay off -> if they come back I'll turn them off -> they came back and I turned them off",
             "post-chorus: 'nothing on but the moon / nothing on but you'; final post adds 'the only thing glowing is you'",
             "V2: candle lit off a match, 'things you'd never say with the lights on', 'funny what you see when there's nothing to see' (the repeatable line); neighbor knock cut",
             "final chorus: 'my phone woke up and I let it ring' (V1 let it die)"], "answer": "C. (1) Pre-chorus 2 still the weakest section -- functional, restates the privacy instead of deepening the moment. (2) Bridge still mostly plot; only 'hold my breath' is charged; microwave and hall light ordinary. (3) Final post-chorus: 'the only thing glowing is you' right after 'nothing on but you' slightly repetitive on the page."})
THESIS = "The power came back, and I didn't want it."
LOG.append({"q": "draft 4", "file": "lyric_draft4.md",
 "changes": ["Pre 2: 'the candle gave out and I heard you smile / say my name till I find where you are' (a direction that 'go by feel' answers)",
             "Bridge: the house wakes up and watches -- fridge clears its throat, windows open one eye, microwave blinking like it caught us; 'hold my breath' kept",
             "Final post: second line becomes 'nothing on but the moon' so 'and the only thing glowing is you' lands alone"], "answer": None})
LOG[-1]["answer"] = "A. And remember what you learned from your research"
LOCKED = "lyric_draft4.md (locked 8 Nov 05:03): lyric.py"
FEEL = {"meter": "4/4, sixteenth grid", "qbpm": 116, "band": "disco-funk: live-sounding kit, finger P-bass, two funk guitars (chank and single-note), Rhodes, horn stabs, handclaps, bongos", "target_len": "about 2:40"}
KEY = "F major / D minor signature; the loop (Gm7 - Am7, Bbmaj7 - C) never lands on F or Dm until the bridge; the song ends open on Bbmaj7"
SINGERS = {"her": "female pop lead, G3-C5, D5 once (OFF in the payoff line)"}
FORM_PLAN = "Intro 4 | V1 8 | Pre 4 | Ch 8 | Post 4 | V2 8 | Pre 4 | Ch 8 | Post 4 | Bridge 8 | Ch 8 | Post 6 | Outro 2 = 76 bars, 2:37 at q=116"
HIT_RULES = {  # the 8 Nov research, as rules for this song (sources in the reply)
 "length": "under 3:00 (staying-power hits ran shorter); intro under 11 s; the title inside the first 30 s of singing",
 "frame": "disco-funk pop 112-120 BPM, live-sounding drums, guitar forward, synths minor (the 2025 top-10 trends)",
 "post-chorus": "a post-chorus hook after every chorus (63% of 2025 top-10 hits)",
 "repetition": "the title sung at least 6 times in every chorus and post-chorus (more chorus repetition raised #1 odds)",
 "melody": "inside the 515-melody corpus's middle band: chorus range 12-17 semitones, chorus 3+ semitones above the verse, steps and leaps near the medians",
 "hook": "a common rise-fall contour with one distinctive leap (earworm research)",
 "departures": "two or three only (optimal differentiation): the withheld tonic, the power cut, the off-beat hooks with chorus syncopation at the corpus's 75th-95th percentile",
}
OBJECTS = ["street", "fridge", "fan", "phone", "air", "room", "lights", "candle", "birthday", "kitchen", "drawer", "match", "floor", "name",
           "window", "eye", "microwave", "hand", "switch", "breath", "moon", "throat", "nine"]
WRITER_PHRASES = ["nothing on", "the lights came back and i turned them off", "funny what you see when there's nothing to see",
                  "the only thing glowing is you", "go by feel", "heard you smile"]
WRITER_WORDS = []
LEXICON = {}
ROLES = {"verse", "pre", "chorus", "hook", "post", "bridge", "turn", "tag"}
REQUIRED = {"story": Q0[1], "sound": "A dance/funk-pop", "euphemism": "A the power outage", "voice": "A female lead", "title": "A Nothing On",
            "turn": "A the power comes back and she switches it off", "music": "A disco-funk 116, the withheld tonic, the power cut, off-beat hooks"}
WRITER_NOTES = ["Words and music: Jason Bryant"]
ENGINE = "ZenEng v64 with the v65 fix list (fixes 1-79, songs 21-30) run as ports, plus the 8 Nov hit research (HIT_RULES)"
SOURCE_MATERIAL = "pitched subject (A, the power outage); the writer's notes on four drafts; the 8 Nov research"
INSTRUMENT = FEEL["band"]
ROUTING = "Anthem (A) primary, Narrative secondary; up-tempo disco-funk pop, one female lead with a backing echo"
LOG.append({"q": "delivery (8 Nov)", "answer": "demo, lead sheet, Nashville chart, parts (16 pp), songbook Doc + Word with one-sheet, test report (findings 80-88); consistency 30/30"})
LOG.append({"q": "blind pick (10.20), shuffled", "options": {"A": "you struck a match and pulled me to the floor (Annotated top)", "B": "nothing on but the moon (middle: top quartile under both)",
            "C": "nothing on, nothing on (Remembered top)"}, "answer": "B"})
BLIND_PICK = ("B", "nothing on but the moon -- the middle slot (top quartile under both)")
