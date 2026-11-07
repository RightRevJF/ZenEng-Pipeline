"""The Word Without a Word -- the locked lyric (draft 3). One high voice (soprano; a tenor an octave lower)."""
TITLE = "The Word Without a Word"
V1 = [("verse", "The voice that said, Let there be light,"), ("verse", "and light came running at the call,"),
      ("verse", "is lying in a feeding trough"), ("verse", "with not a single word at all.")]
REFRAIN = [("hook", "The Word without a word"), ("refrain", "is sleeping on her chest;"),
           ("refrain", "the breath that made the world"), ("refrain", "goes in and out, and rests.")]
V2 = [("verse", "She'll soften bread and say it, bread,"), ("verse", "and set a crumb against his tongue;"),
      ("verse", "she'll cup his hand to catch the rain,"), ("verse", "then lift him up where stars are hung.")]
V3 = [("verse", "The tongue that thundered on the mount"), ("verse", "is milk and spit and half a sound;"),
      ("verse", "he loses it and tries again,"), ("verse", "and she says ma until it's found.")]
BRIDGE = [("bridge", "And when he gets a whole word out,"), ("bridge", "it's not a word he had to learn;"),
          ("bridge", "he reaches up past both of them."), ("bridge", "Now: Abba. And Joseph turns.")]
V4 = [("verse", "He cries, red-faced, and shakes with it,"), ("verse", "a thin cry, hoarse against her ear;"),
      ("verse", "now all that God has left to say"), ("verse", "is crying, and his mother hears.")]
LAST = [("hook", "The Word without a word"), ("refrain", "is what God meant to say:"),
        ("refrain", "the breath that made the world"), ("refrain", "goes in, and out, and in.")]
SECTIONS = [("Verse 1", V1), ("Refrain 1", REFRAIN), ("Verse 2", V2), ("Refrain 2", REFRAIN), ("Verse 3", V3), ("Bridge", BRIDGE),
            ("Verse 4", V4), ("Refrain 3", LAST)]
SINGER = {s: "her" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
