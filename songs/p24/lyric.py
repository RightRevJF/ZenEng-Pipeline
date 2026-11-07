"""Song 24, 'The Song You Sang Me' -- the lyric, drafted with the writer over three rounds (w1) and locked by him (13:35). One tenor
and one guitar. Four visits, each verse closing on the refrain line; the parent's lullaby is the chorus, after verse 2 and at the end
(sung by both). The refrain turns once: 'son' becomes 'song'."""
TITLE = "The Song You Sang Me"
V1 = [("verse", "you're folding the same napkin by the window"), ("verse", "you ask me if I've come to fix the heat"),
      ("verse", "I pull my chair in close like I've always done"), ("refrain", "it's me. I'm your son.")]
V2 = [("verse", "I brought the pictures from the lake in August"), ("verse", "you touch a face and say, \"she used to swim\""),
      ("verse", "you hold my hand the way you'd hold anyone"), ("refrain", "it's me. I'm your son.")]
CHORUS = [("chorus", "go to sleep, I've got the dark"), ("chorus", "I'll keep it folded, keep it near"),
          ("chorus", "and if you wake and don't know where you are"), ("hook", "I'll say your name till you know you're here")]
V3 = [("verse", "you called me by your brother's name on Tuesday"), ("verse", "now you watch the birds come to the feeder"),
      ("verse", "I write my name in marker underneath the date"), ("refrain", "it's me. I'm your son.")]
V4 = [("verse", "I sang it soft, and somewhere in the second line"), ("verse", "your hand came up and kept the time"),
      ("verse", "you didn't know my face, but you sang along"), ("refrain", "it's me. I'm your song.")]
SECTIONS = [("Verse 1", V1), ("Verse 2", V2), ("Chorus 1", CHORUS), ("Verse 3", V3), ("Verse 4", V4), ("Chorus 2", CHORUS)]
SINGER = {s: "him" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [
 ("DRAFT 1 -> 2 (13:28)", "the writer's question ('Where's the chorus?')", "form A had a one-line refrain and the lullaby as a bridge; his choice C made the lullaby the chorus, after verse 2 and at the end, sung by both; no words changed"),
 ("DRAFT 2 -> 3 (13:32)", "the writer's notes", "verse 3's third line explained ('I tell you anyway, the way you'd leave a light on', 0.632) -> 'I write my name in marker underneath the date' (0.695); the chorus's imagery familiar ('lay your head, the lamp is low' ...) -> 'go to sleep, I've got the dark' (0.806), 'I'll keep it folded, keep it near' (0.702), 'and if you wake and don't know where you are' (0.530 under draft 2's 0.575), 'I'll say your name till you know you're here' (0.697); one harder image -> 'you called me by your brother's name on Tuesday' (0.674)"),
 ("V1.1", "the writer's lock", "'you're folding the same napkin by the window' dies in the room on strong-beat agreement (0.00) -- the room's walk in 3/4 lands its downbeats on weak syllables; kept in every draft, a finding"),
]
