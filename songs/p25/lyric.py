"""Song 25, 'Through Its Breaking' -- the lyric, drafted with the writer over two rounds (w1) and locked by him (15:10). From his parable
'The Cracked Bell'. One voice (female); third person. The tag is the parable's own last lines."""
TITLE = "Through Its Breaking"
V1 = [("verse", "high in the tower over the town"), ("verse", "a bell too big for a place this small"),
      ("verse", "green as moss, with a crack up the side"), ("verse", "wide enough to hold a thumbnail"),
      ("verse", "close to the note it was made to sing"), ("verse", "never quite the note at all")]
CHORUS = [("chorus", "close enough to know the tune"), ("chorus", "not close enough to call it true"),
          ("chorus", "like your name in a stranger's mouth"), ("hook", "and every hour she rings it through")]
V2 = [("verse", "she was never made for brilliance"), ("verse", "she was made for oil and rope"),
      ("verse", "she never meant to love the thing"), ("verse", "it found her, year by year, at the wheel"),
      ("verse", "some nights she couldn't find her sleep"), ("verse", "she'd climb up in the dark and sit"),
      ("verse", "her palm flat on the cold green bronze"), ("verse", "she thought: the note is still in it")]
BRIDGE = [("bridge", "one winter night the valley bell fell still"), ("bridge", "and the need came down like snow"),
          ("bridge", "the wrong bell was the only bell"), ("bridge", "she took the rope in both her hands"),
          ("bridge", "again, again, the split note went"), ("bridge", "out over roofs and frozen fields"),
          ("bridge", "and doors came open down the valley"), ("bridge", "farther out than it had ever reached")]
LAST = CHORUS[:2] + [("chorus", "it never rang in spite of the crack"), ("hook", "it rang through its breaking")]
TAG = [("tag", "the crack runs up the bronze"), ("tag", "the bell rings"), ("tag", "the sound carries")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Chorus 2", CHORUS), ("Bridge", BRIDGE), ("Chorus 3", LAST), ("Tag", TAG)]
SINGER = {s: "her" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("DRAFT 1 -> 2 (15:07)", "the writer's notes", "verse 1's last four lines listed the bell's functions -> cut to six lines ('it rings the hour, it rings the market' 0.824 and 'it calls the meeting to the hall' 0.642 dropped); the chorus's second couplet ('two almost-notes where one should be' died on a weak ending; 'and still she rings it anyway' 0.702) -> 'like your name in a stranger's mouth' (0.808) / 'and every hour she rings it through' (dies: weak ending 'through'); one more interior moment -> 'she never meant to love the thing' (0.580 under 'eleven years of every hour' 0.699) / 'it found her, year by year, at the wheel' (0.709)"),
 ("LOCK", "the writer's lock", "'and every hour she rings it through' (the particle 'through' read as a weak ending) and 'she thought: the note is still in it' (the pronoun ending; the writer's phrase from the parable) die in the room and are kept -- both findings (v65 fixes 24 and 9); 'it never rang in spite of the crack' (0.788) over 'it didn't ring' (0.856), the run's draft 2 wording, accepted with the lock"),
 ("TAG", "the writer's words", "the parable's last lines"),
]
