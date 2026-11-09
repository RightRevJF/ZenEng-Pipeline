"""I Took Him for the Gardener -- the locked lyric (draft 4, locked 8 Nov: 'A'). Mary Magdalene, first person (John 20:1-18).
Soprano and mezzo editions."""
TITLE = "I Took Him for the Gardener"
V1 = [("verse", "It was still dark. I brought the spices;"), ("verse", "I knew how to wash the dead."),
      ("verse", "I'd tied my hair back for the work,"), ("verse", "and the stone was moved instead.")]
REFRAIN = [("hook", "I took him for the gardener,"), ("refrain", "the first one out at dawn;"),
           ("refrain", "I said, sir, if you carried him,"), ("refrain", "just tell me where he's gone.")]
V2 = [("verse", "I found his linen lying flat,"), ("verse", "the cloth that wrapped his head"),
      ("verse", "folded in a place by itself,"), ("verse", "as if he'd made the bed.")]
V3 = [("verse", "Two sat in white on either side,"), ("verse", "with no one in between;"),
      ("verse", "they asked me why I cried. I turned,"), ("verse", "and someone stood among the trees.")]
NAME = [("bridge", "He asked me who I came to find;"), ("bridge", "I said, just give me back the body."),
        ("bridge", "And then he only said my name."), ("bridge", "Mary. And I said, Rabboni.")]
V4 = [("verse", "God walked the first garden in the evening"), ("verse", "and called the man he'd made by name;"),
      ("verse", "I walked this one in the dark and called,"), ("verse", "and he answered with my name.")]
LAST = [("hook", "I took him for the gardener,"), ("refrain", "the first one out at dawn,"),
        ("refrain", "his hands in the earth again,"), ("refrain", "come back to tend his own."),
        ("hook", "I took him for the gardener, and he was.")]
SECTIONS = [("Verse 1", V1), ("Refrain 1", REFRAIN), ("Verse 2", V2), ("Refrain 2", REFRAIN), ("Verse 3", V3), ("The Name", NAME),
            ("Verse 4", V4), ("Refrain 3", LAST)]
SINGER = {s: "her" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
