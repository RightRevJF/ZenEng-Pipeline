"""Song 39 intake log (ZenEng v103)."""
LOG = []
LOG.append({"q": "goal", "answer": "C (after song 38): start a new song from the idea up; keep Stay Tuned as the media song it became",
            "writer": "I like the song but it's turned into more of an attack on media than the political class. I really want a song that shows them for the reckless profiteers they really are. Both sides.",
            "spec": "ZenEng v103 (row v137, last fix 256); findings from 269 (song 38's list ran 257-268)"})
LOG.append({"q": "idea 1: whose eyes", "options": {"A": "the bartender at the fundraisers", "B": "the driver", "C": "a retiring politician's confession"}, "recommended": "A",
            "answer": "Is there any way we can choose an omniscient narrator? I know it's harder to ground things physically but it's also easier to really bite.",
            "reading": "omniscient narrator; next: how the omniscient voice stays grounded"})
LOG.append({"q": "idea 2: how the omniscient voice stays grounded", "options": {"A": "the roving eye: each verse cuts between rooms, concrete scenes, both parties in every room", "B": "the ledger: receipts read out", "C": "the parable: two shepherds in two coats"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "idea 3: what the chorus does", "options": {"A": "says it straight", "B": "mocks their own voice: the campaign promise sung back as a sour jingle", "C": "turns on the listener"}, "recommended": "B", "answer": "B"})
LOG.append({"q": "idea 4: the turn", "options": {"A": "the receipts answer the jingle", "B": "two candidates, one voice: bridge follows both after office (same board seat, same lake, same firm); last chorus a duet that ends in unison", "C": "it starts over on election day"}, "recommended": "B", "answer": "B"})
LOG.append({"q": "idea 5: title", "options": {"A": "I'll Fix It All", "B": "Across the Aisle", "C": "Same Song"}, "recommended": "A", "answer": "B", "reading": "title: Across the Aisle"})
LOG.append({"q": "1", "topic": "class and sound", "options": {"A": "rock with a swagger: mid-tempo sneering shuffle (Stones-style groove), the chorus flipping into a bright mock campaign jingle", "B": "Who-style anthem again", "C": "country-rock, outlaw sneer"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "2", "topic": "who sings (11.2)", "options": {"A": "two male voices", "B": "male and female", "C": "one gritty baritone, double-tracked against himself in the duet, drifting into unison"}, "recommended": "C", "answer": "C"})
LOG.append({"q": "3", "topic": "tempo, feel, key", "options": {"A": "4/4 shuffle q = 108, E major, eighths written straight and played swung", "B": "12/8 at q. = 72 in A", "C": "straight eighths q = 116 in G"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "4", "topic": "form", "options": {"A": "Intro 4 | Verse 16 | Chorus 8 | Verse 16 | Chorus 8 | Bridge 8 | Solo 8 | Last Chorus 18 | Outro 4 = 90 bars, ~3:20", "B": "with pre-choruses, 82 bars", "C": "three short verses, 82 bars"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "5 (242)", "topic": "era setting", "options": {"A": "no era (bands as fitted; 258 not yet in)", "B": "CLASSIC", "C": "MODERN (needs a pre-chorus or a reason)"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "6 (225)", "topic": "character", "recommended": "11 off-beat in the verses, 3 chord-bound in the chorus (no kept window does both: 0 of 314; split by section)", "answer": "I'll take your recommendation",
            "reading": "Verse aimed at a kept window 1.4-2.1 on the off-beat axis (10 kept); Chorus at 1.4-2.1 on chord-bound (22 kept); the bridge free"})
LOG.append({"q": "7", "topic": "never say", "options": {"A": "song 38's list plus red, blue, left, right, swamp, no real names", "B": "song 38's list only", "C": "song 38's list plus the writer's"}, "recommended": "A", "answer": "A"})
NEVER_PHRASES = ["wake up", "sheeple", "rigged", "the man", "power to the people", "fake news", "drain the swamp", "us versus them", "us vs them",
                 "democrat", "republican", "liberal", "conservative", "left wing", "right wing", "red", "blue", "left", "right", "swamp"]
LOG.append({"q": "8 (213)", "topic": "which section opens by saying it twice", "options": {"A": "the chorus", "B": "the verse", "C": "the bridge"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "lyric draft 1", "file": "lyric_draft1.md", "note_230": "every line 4-8 syllables: two bars each; sections 16, 8, 16, 8, 8, 18 (228's +2: the tag 'Across the aisle')",
            "note_213": "chorus lines 1-2: 7 and 7 (the same words)", "note_232": "title sung 5 times (kept 2-10, median 5); first at bar 21 of 90 (23%)", "never_say": "none used"})
LOG.append({"q": "lyric draft 1 notes (writer)", "answer": "B. 1 some lines explain rather than show (hearing room, pound the desk, call it war); 2 the rusting bridge vs ribbon is familiar; 3 temperature: the unpaid guard is a moral note against the cold transactional details; 4 title 'Across the Aisle' serviceable but familiar; highest leverage: one or two more lines as specific and strange as the shrimp line; decide on the human cost or stay transactional; lean into the final duet, the 'us' moment is the punchline"})
LOG.append({"q": "lyric draft 2", "file": "lyric_draft2.md",
  "changes": {"verse 1 lines 5-6": "'They get a minute each to rage, / then pass the cough drops down the floor'",
              "verse 2 lines 3-4": "'the bridge back home got studied twice, / once by his kid, and once by hers' (both sides' families paid)",
              "verse 2 line 7": "'the fundraiser's still on at eight' for the unpaid guard: the song stays inside the transactional world",
              "last chorus": "unison pass turns past tense: 'vote for us, we fixed it all; / we shook hands across the aisle, / and you got fixed by fall'",
              "title": "kept; 'Fixed by Fall' offered (sung 5 times with the tag)"},
  "note_230": "every line 6-8 syllables, two bars", "note_232": "title 5 times, first bar 21 of 90"})
LOG.append({"q": "lyric draft 2 notes (writer)", "answer": "1 the chorus hasn't grown; by the second appearance it feels flat: one small internal variation or a colder delivery; 2 bridge not pushed as hard: 'one lake, two docks, one lobby firm' good, could be more specific or stranger; 3 title familiar; 'you got fixed by fall' is stronger than the title phrase"})
LOG.append({"q": "lyric draft 3", "file": "lyric_draft3.md",
  "changes": {"chorus 2": "line 4 'he's paid, I'm paid, that's all.'; sung flatter than chorus 1 (bright, a jingle)", "bridge line 1": "'One cake, both names in frosting script,' (names in frosting, then in gold)"}})
LOG.append({"q": "lyric draft 3: lock or notes", "options": {"A": "lock and retitle Fixed by Fall (tag 'Fixed by fall.')", "B": "lock, keep Across the Aisle", "C": "notes"}, "recommended": "A", "answer": "A",
            "reading": "locked as lyric_locked.md; title Fixed by Fall; sung 4 times (chorus 1 line 4, last chorus lines 4 and 8, the tag), first at bar 27 of 90 (30%)"})
LOG.append({"q": "9 (244, 216)", "topic": "summit placement", "options": {"A": "on 'Vote' at the top of each chorus (first quarter)", "B": "on 'aisle' mid-chorus", "C": "on 'fall' at the chorus end (last quarter)"}, "kept": "first quarter 52%, last quarter 16% of 8-bar chorus windows", "recommended": "A", "answer": "A"})
LOG.append({"q": "10 (208)", "topic": "bridge register", "options": {"A": "new tune above the verse, under the chorus top", "B": "highest section", "C": "lowest and quietest"}, "kept": "unrelated opening 94%, above verse 68%, highest 46%, lowest 14%", "recommended": "A", "answer": "A"})
LOG.append({"q": "11 (235)", "topic": "chorus countermelody", "options": {"A": "off (the duet is the feature)", "B": "barroom piano answering the jingle every chorus", "C": "guitar line under the last chorus only"}, "recommended": "A", "answer": "A"})
LOG.append({"q": "12 (236)", "topic": "drum design", "options": {"A": "shuffle throughout", "B": "shuffle in the verses; the choruses snap into a straight rally march (marching snare, kick on every beat)", "C": "half-time verses, shuffle choruses"}, "recommended": "B", "answer": "B",
            "reading": "verses, bridge, solo: shuffle (eighths swung), kick 1 and 3, snare 2 and 4; choruses: straight, kick on every beat, marching snare figure; a feel change at each chorus (named, 236)"})
SPEC = "ZenEng v103"
LOG.append({"q": "build", "reading": "main 500 builds, 58 survivors (order 07c5a8ad998f); control 500, 113; shortlist pick (255) f69bed50793e, composite 0.7873, combined 2.484; composite's first 03b97e94f12c was 54th of 58 by the judge; no hand edits",
            "design_choices": ["three target pools: verse off-beat (10 kept), chorus chord-bound (22), bridge all", "said twice: line 2 a whole step down over D, repaired for runs (finding 270)",
                               "the join into 'Vote': the line before re-walked toward E4", "swing in the demo only (finding 271)", "chorus 2 double-tracked (238: no verse fuller than its chorus)",
                               "bass waits for the verse (238: intro under half the fullest)"]})
