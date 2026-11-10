"""Stay Tuned -- lyric draft 5 (locked 10 Nov: 'A'). The man behind the camera on a cable shouting show: both sides perform the
fight on air, share a car and an owner off it, and need the viewer angry. He is paid to light it, and it has split his own family.
The last chorus he cuts the cameras himself and tells you to turn it off. No party or name is said."""
TITLE = "Stay Tuned"
V1 = [("verse", "She powders both with the same brush,"), ("verse", "camera left, camera right;"),
      ("verse", "the script feeds them what to hate,"), ("verse", "and they hit their marks tonight.")]
PRE1 = [("pre", "The ad rate climbs with every shout,"), ("pre", "and my old man yells back at home —")]
CH = [("hook", "Stay tuned, stay mad,"), ("hook", "stay tuned, stay scared,"),
      ("chorus", "they're selling you the fight you're in,"), ("chorus", "and you're paying for the air."),
      ("hook", "Stay tuned, stay mad,"), ("hook", "stay right where you are;"),
      ("chorus", "we'll be right back after this,"), ("chorus", "so don't you touch that dial.")]
V2 = [("verse", "Red light off, and the shouting stops,"), ("verse", "they're laughing in the hall;"),
      ("verse", "one car downstairs for both of them,"), ("verse", "one billionaire who owns them all.")]
PRE2 = [("pre", "They pay my rent to light the fight,"), ("pre", "and Dad won't speak to Danny now —")]
BRIDGE = [("bridge", "They hug when the red light dies,"), ("bridge", "they toast the ratings, glass to glass;"),
          ("bridge", "they don't hate each other, friend,"), ("bridge", "they just need you to.")]
LAST = CH[:6] + [("chorus", "so I cut camera left,"), ("chorus", "and camera right goes dark."), ("tag", "Turn it off.")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH), ("Bridge", BRIDGE),
            ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
NEVER_PHRASES = ["wake up", "sheeple", "rigged", "the man", "power to the people", "fake news", "drain the swamp", "us versus them",
                 "us vs them", "democrat", "republican", "liberal", "conservative", "left wing", "right wing"]
