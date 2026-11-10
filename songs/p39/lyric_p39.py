"""Fixed by Fall -- lyric draft 3, retitled (locked 10 Nov: 'A'). An all-seeing narrator cuts between rooms where both sides of the
political class take the same money; the chorus is their campaign promise sung back as a sour jingle; the bridge follows them out of
office to the same cake, board, lake and firm; the last chorus is the two candidates, one singer on two tracks, ending in unison.
No party, colour, side or name is said."""
TITLE = "Fixed by Fall"
V1 = [("verse", "Tuesday night, a thousand a plate,"), ("verse", "Wednesday night, the other side;"), ("verse", "same shrimp, same band, same donor's hand"),
      ("verse", "on every shoulder, every time."), ("verse", "They get a minute each to rage,"), ("verse", "then pass the cough drops down the floor;"),
      ("verse", "the trade clears at nine-thirty-one:"), ("verse", "they knew the vote the night before.")]
CH1 = [("hook", "Vote for me, I'll fix it all,"), ("hook", "vote for me, I'll fix it all;"), ("chorus", "I'll shake his hand across the aisle,"), ("hook", "we've got it fixed by fall.")]
V2 = [("verse", "The bill was written down the street"), ("verse", "by a firm that pays them both;"), ("verse", "the bridge back home got studied twice,"),
      ("verse", "once by his kid, and once by hers."), ("verse", "They shut the government at dawn"), ("verse", "and keep their paychecks through the fight;"),
      ("verse", "the fundraiser's still on at eight,"), ("verse", "and both sides sleep just fine tonight.")]
CH2 = CH1[:3] + [("chorus", "he's paid, I'm paid, that's all.")]
BRIDGE = [("bridge", "One cake, both names in frosting script,"), ("bridge", "they take the same seat on the board;"), ("bridge", "one lake, two docks, one lobby firm,"),
          ("bridge", "both names in gold above the door.")]
LAST = CH1 + [("hook", "Vote for us, we'll fix it all,"), ("hook", "vote for us, we fixed it all;"), ("chorus", "we shook hands across the aisle,"),
              ("hook", "and you got fixed by fall."), ("tag", "Fixed by fall.")]
VOICES = {0: "one", 1: "two", 2: "both, apart", 3: "both, apart", 4: "unison", 5: "unison", 6: "unison", 7: "unison", 8: "unison"}     # the last chorus's duet
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH1), ("Verse 2", V2), ("Chorus 2", CH2), ("Bridge", BRIDGE), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
NEVER_PHRASES = ["wake up", "sheeple", "rigged", "the man", "power to the people", "fake news", "drain the swamp", "us versus them", "us vs them",
                 "democrat", "republican", "liberal", "conservative", "left wing", "right wing", "red", "blue", "left", "right", "swamp"]
