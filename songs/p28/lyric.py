"""Tinted Glass -- the locked lyric (draft 5). Duet: him and her, never together."""
SECTIONS = [
 ("Verse 1", [("verse", "I said that I was out visiting the sick"), ("verse", "on the top deck at the furniture company"),
              ("verse", "you'd pressed black vinyl over every window"), ("verse", "and we were twenty in the dark at noon")]),
 ("Verse 2", [("verse", "I kept the shades rolled up with my red pens"), ("verse", "you laughed when your glasses fogged"),
              ("verse", "your hands were shaking worse than mine"), ("verse", "and we'd pull the shades down together")]),
 ("Chorus 1", [("hook", "behind the tinted glass"), ("chorus", "the world went dark and small"),
               ("chorus", "I knew you by your breathing"), ("chorus", "and I loved you, that was all")]),
 ("Verse 3", [("verse", "past the county line, a door with no name"), ("verse", "we paid in dollars for the dark"),
              ("verse", "then I drove home and couldn't sleep"), ("verse", "and wrote fourteen lines about your laugh")]),
 ("Verse 4", [("verse", "the screen was full of strangers, loud and bored"), ("verse", "we got the giggles like two kids in the back row"),
              ("verse", "you held my face like you were memorizing it"), ("verse", "and for once in my life it was enough")]),
 ("Chorus 2", [("hook", "behind the tinted glass"), ("chorus", "the world looked far away"),
               ("chorus", "I couldn't see the people"), ("chorus", "we'd have to face someday")]),
 ("Bridge", [("bridge", "he read them all and never made a sound"), ("bridge", "that Sunday he was waiting at the door"),
             ("bridge", "he plugged my watch in by my side of the bed"), ("bridge", "he shook my hand and said he liked the words")]),
 ("Verse 5", [("verse", "Sundays I still say the words they pay me for"), ("verse", "my wife still waves from the second row"),
              ("verse", "it's a good life, I built it board by board"), ("verse", "and I know where every road in it goes")]),
 ("Verse 6", [("verse", "he never brought the watch up again"), ("verse", "he still pours my coffee before the sun"),
              ("verse", "I traded the car for one with clear glass"), ("verse", "and I know how every day will run")]),
 ("Chorus 3", [("hook", "behind the tinted glass"), ("chorus", "the world is safe and small"),
               ("chorus", "I still fog the window on your street"), ("chorus", "and I never make the call")]),
 ("Chorus 4", [("hook", "behind the tinted glass"), ("chorus", "the world is safe and small"),
               ("chorus", "I still fog the window on your street"), ("chorus", "and I never make the call")]),
]
SINGER = {"Verse 1": "him", "Verse 2": "her", "Chorus 1": "him", "Verse 3": "him", "Verse 4": "her", "Chorus 2": "her",
          "Bridge": ["her", "him", "her", "him"], "Verse 5": "him", "Verse 6": "her", "Chorus 3": "him", "Chorus 4": "her"}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
LAST = SECTIONS[-1][1]
TITLE = "Tinted Glass"
