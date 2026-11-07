"""Song 22, 'The Seam' -- the lyric, from the writing room (w1, w2). A duet: HER verses (E minor), HIS verses (F minor), BOTH in the
chorus (C major), HIM alone at the end. Every line is the top of its slot unless PICKS says why."""
TITLE = "The Seam"
V1 = [("verse", "six inches of crack in a grey that never breaks"), ("verse", "one warm room at the bottom of the stairs"),
      ("verse", "my hands on the worn place in the wood"), ("verse", "your window, lit, beyond my glass")]
V2 = [("verse", "the coffee's right, the light is right"), ("verse", "the sky is wrong by a degree"),
      ("verse", "one blue stops where another starts"), ("verse", "I write it down and nobody looks up")]
CHORUS = [("hook", "a seam across the sky"), ("chorus", "two blues, and neither one is wrong"),
          ("chorus", "a line we both can see and neither cross"), ("hook", "the seam won't close, the seam won't heal")]
V3 = [("verse", "I made a door; it only opens one way"), ("verse", "the light in your window never goes out"),
      ("verse", "there's a note on the keys: trust the third layer"), ("verse", "every day I stay, the edges thin")]
V4 = [("verse", "I kept the record against the day"), ("verse", "the seam has moved a hand's width east"),
      ("verse", "this morning I put the pencil down"), ("verse", "the smell of bread came through the open door")]
ENDING = [("bridge", "I leave the notebook on the sill"), ("bridge", "fear requires surprise"), ("bridge", "and I am not afraid")]
LAST = CHORUS[:3] + [("hook", "the seam won't close, and neither will we")]
SECTIONS = [("Verse 1", V1), ("Verse 2", V2), ("Chorus 1", CHORUS), ("Verse 3", V3), ("Verse 4", V4), ("Chorus 2", CHORUS),
            ("Chorus 3", LAST), ("Ending", ENDING)]
SINGER = {"Verse 1": "her", "Verse 3": "her", "Verse 2": "him", "Verse 4": "him", "Chorus 1": "both", "Chorus 2": "both", "Chorus 3": "both", "Ending": "him"}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("V2.4", "plain (#2, 0.574)", "over 'it's in my notebook, every morning, same hour' (0.619, 0.045): 'nobody looks up' answers the sky he is watching"),
 ("VERSE 4 (06:47)", "", "the writer's notes: a progression (preservation -> expansion -> discovery -> the ordinary); the record given weight; the seam moving, anchored; the bread kept, plain; and the verse beginning the ending's movement from observing to living -- pass 3 (w3), every line the top of its slot: 'I kept the record against the day' (0.707), 'the seam has moved a hand's width east' (0.689), 'this morning I put the pencil down' (0.783), 'the smell of bread came through the open door' (0.721)"),
 ("REVIEW (06:49-06:51)", "", "the run's review, the writer's A: V1.4 'your window, lit, beyond my glass' (0.753; her glass, his window); the last chorus's line 4 'the seam won't close, and neither will we' (0.747; the turn after the instrumental, sung by both)"),
 ("END.2-3", "the writer's words", "the novel's last line, 'Fear requires surprise. I am not afraid.'"),
]
