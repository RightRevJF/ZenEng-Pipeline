"""Song 27, 'Either Or' -- the lyric, from the writer's poem, reworked over five drafts and locked by him (12:56). One voice (tenor);
first person plural / second person. The refrain is the run's (draft 1), kept by the writer; the verses are draft 5."""
TITLE = "Either Or"
V1 = [("verse", "Aristotle drew a line across the dust"), ("verse", "said one thing's true and the other must be lies"),
      ("verse", "and we've bled across that line ever since"), ("verse", "calling our own blood the other side")]
REFRAIN = [("refrain", "and the wind blows where it wants to blow"), ("refrain", "it doesn't stop to ask you yes or no"),
           ("refrain", "you can't fence it in, you can't keep score"), ("hook", "the wind was never either or")]
V2 = [("verse", "they sat in the tower systematizing wind"), ("verse", "weighing the wind by the words that they heard"),
      ("verse", "sprinkled holy water on the laws they wrote"), ("verse", "and the herd said amen, word for word")]
V3 = [("verse", "the ones who won't choose catch the stones"), ("verse", "from the keepers of the dead"),
      ("verse", "handing down their fathers' wars by name"), ("verse", "turning bones into bread")]
LAST = REFRAIN[:3] + [("hook", "and you were never either or")]
SECTIONS = [("Verse 1", V1), ("Refrain 1", REFRAIN), ("Verse 2", V2), ("Refrain 2", REFRAIN), ("Verse 3", V3), ("Refrain 3", REFRAIN), ("Refrain 4", LAST)]
SINGER = {s: "him" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("DRAFT 1 (11:59)", "the run's", "the writer's three stanzas lightly shaped; the refrain new (the wind, John 3:8; the last line turned to 'you')"),
 ("DRAFT 2 (12:00)", "the writer's pick B", "'birthed by Aristotle, whose line of thought was poor' -- names him, so 'Ari' lands; 'turds' kept"),
 ("DRAFT 3 (12:46)", "the writer's note", "'I like the poem, don't like the lyrics other than the refrain' -> new verses in the refrain's voice around his phrases (C)"),
 ("DRAFT 4 (12:50)", "the writer's attached notes", "the line across the dust; 'weighing the wind by the words that they heard'; the ones who won't choose; the stop before the last line"),
 ("DRAFT 5 (12:55)", "the writer's notes", "'bled across'; 'fence it in'; 'sprinkled holy water on the laws they wrote'; 'keepers of the dead'; 'handing down'"),
 ("LOCK (12:56)", "the writer's lock", "draft 5"),
]
