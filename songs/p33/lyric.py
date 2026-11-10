"""Sadie -- the locked lyric (draft 4, locked 9 Nov: 'A'). Her father in the stands; a country-rock anthem; a gang on 'Sadie'."""
TITLE = "Sadie"
V1 = [("verse", "Four seconds left and it's tied at ten,"), ("verse", "the bleachers rumble under every boot;"),
      ("verse", "I've chewed my coffee cup down to the rim,"), ("verse", "and that's my daughter, eye black, number two.")]
PRE = [("pre", "I'm in the jacket that I never lettered in,"), ("pre", "and somebody behind me starts it up:")]
CHORUS = [("hook", "Sadie! Sadie! Feet pounding the aluminum,"), ("chorus", "two thousand hollering her name;"),
          ("chorus", "I used to say it soft so she would sleep,"), ("chorus", "and back then it was only mine to say.")]
V2 = [("verse", "She kicked a ball over the clothesline in the yard,"), ("verse", "I held it for her till my hands went raw;"),
      ("verse", "her first day out, the Miller boy laughed hard,"), ("verse", "now he's the one down on a knee to hold the ball.")]
BRIDGE = [("bridge", "The snap comes back and the band goes quiet,"), ("bridge", "the holder spins the laces round;"),
          ("bridge", "I don't pray much, but my lips are moving,"), ("bridge", "I'm on my feet and I can't hear a sound.")]
DROP = [("drop", "It's up.")]
LAST = CHORUS[:3] + [("chorus", "and it's never gonna sound the same.")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Pre 2", PRE), ("Chorus 2", CHORUS),
            ("Bridge", BRIDGE), ("Drop", DROP), ("Chorus 3", CHORUS), ("Chorus 4", LAST)]
SINGER = {s: "him" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
