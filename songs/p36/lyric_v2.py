"""Dance Anyway -- version 2: lyric draft 5 (locked 10 Nov: 'A'); three lines changed from draft 4. Alone in the kitchen at 2 a.m.; joy chosen, not caused."""
TITLE = "Dance Anyway"
V1 = [("verse", "Two a.m., and the dishes are dry,"), ("verse", "the microwave's blinking twelve, been blinking since July;"),
      ("verse", "the radio finds an old song I know,"), ("verse", "and my socks hit the tile like they've got somewhere to go.")]
PRE1 = [("pre", "Every light in the house is off but one,"), ("pre", "and it's blinking like it's counting me in —")]
CHORUS = [("hook", "So I dance anyway,"), ("chorus", "by the green of a clock stuck on twelve,"), ("chorus", "in my socks with somewhere to go,"),
          ("chorus", "singing all the wrong words louder than the right;"), ("hook", "yeah, I dance anyway,"), ("chorus", "to a song I haven't heard since I was twelve,"),
          ("chorus", "and the only one watching"), ("chorus", "is a clock that's wrong, keeping time with me.")]
V2 = [("verse", "There's a bill on the counter, stamped in red,"), ("verse", "a call from this morning still loud in my head;"),
      ("verse", "it's the same red they sent me in July,"), ("verse", "when the lights went out and the clock forgot the time.")]
PRE2 = [("pre", "That light's been blinking since the dark in July,"), ("pre", "and this time I don't wait for the one —")]
BRIDGE = [("bridge", "Last July I sat here on the floor,"), ("bridge", "the freezer dripping in the dark, a puddle by the door;"),
          ("bridge", "I could hear the neighbors' radio through the wall,"), ("bridge", "and I didn't move at all.")]
LAST = [("hook", "Now I dance anyway,"), ("chorus", "by the green of a clock stuck on twelve,"), ("chorus", "with the bill turned face-down on the counter,"),
        ("chorus", "singing all the wrong words louder than the right;"), ("hook", "yeah, I dance anyway,"), ("chorus", "on the floor where I sat through July;"),
        ("chorus", "it can stay twelve o'clock forever —"), ("hook", "I'm still here, so I dance anyway.")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CHORUS), ("Bridge", BRIDGE), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
