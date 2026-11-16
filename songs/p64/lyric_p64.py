"""Song 54 -- The Man Mama Prayed I'd Be, the writer's earlier lyric renovated (draft 3), locked 16 Nov ('A').
A narrator tells it; he sings his own refrains (choruses 2 and 3); she sings chorus 4 alone; the tag both. Every chorus keeps line 3
('One look and the porch light came on') and the title line's shape; the other lines change with the speaker."""
TITLE = "The Man Mama Prayed I'd Be"
V1 = [("verse", "He was sleepin' on a mildewed couch"), ("verse", "In a buddy's double wide"), ("verse", "With a wallet like a snack food aisle"),
      ("verse", "On a Super Bowl Sunday night"), ("verse", "Two a.m. at the Git 'n' Split"), ("verse", "Ten cents short on a honey bun"),
      ("verse", "She dug a dime out of her tip jar"), ("verse", "And smiled like he was the only one")]
C1 = [("chorus", "And he saw her"), ("chorus", "The girl workin' nights in his dreams"), ("chorus", "One look and the porch light came on"),
      ("chorus", "For a boy who'd been gone too long"), ("chorus", "And all at once he wanted to be"), ("hook", "The man Mama prayed he'd be")]
V2 = [("verse", "He dusted off some workin' boots"), ("verse", "He'd bought and never worn"), ("verse", "Called in the last favor he had"),
      ("verse", "For a ride at the crack of dawn"), ("verse", "Hat in hand on a dusty lot"), ("verse", "He said sir I'd like to try"),
      ("verse", "The boss never looked up from his clipboard"), ("verse", "Said son give me one good reason why")]
C2 = [("chorus", "'Cause I've seen her"), ("chorus", "The girl workin' nights in my dreams"), ("chorus", "One look and the porch light came on"),
      ("chorus", "For a boy who's been gone too long"), ("chorus", "And sir I'm finally fixin' to be"), ("hook", "The man Mama prayed I'd be")]
V3 = [("verse", "Workin' from the rooster's crow"), ("verse", "Till the sun had drowned in the hills"), ("verse", "Five a.m. at the Git 'n' Split"),
      ("verse", "A coffee and a dime in her tip jar still"), ("verse", "When his runnin' buddies saw"), ("verse", "A workin' man where a rebel had been"),
      ("verse", "They still saved him a stool at the bar"), ("verse", "And asked what in hell got into him")]
C3 = [("chorus", "Boys I've seen her"), ("chorus", "The girl workin' nights in my dreams"), ("chorus", "One look and the porch light came on"),
      ("chorus", "For a boy who's been gone too long"), ("chorus", "And that girl is why I've got to be"), ("hook", "The man Mama prayed I'd be")]
V4 = [("verse", "Twenties in a coffee can"), ("verse", "Under that mildewed couch"), ("verse", "Every mornin' just a thank you ma'am"),
      ("verse", "And a dime like a prayer he couldn't say out loud"), ("verse", "He was workin' up the nerve to walk in"),
      ("verse", "Some night on her graveyard shift"), ("verse", "But one noon in front of the whole crew"), ("verse", "She climbed out and planted a kiss")]
C4 = [("chorus", "'Cause I've seen you"), ("chorus", "The boy workin' days in my dreams"), ("chorus", "One look and the porch light came on"),
      ("chorus", "For a girl who's been gone too long"), ("chorus", "And every dime you left made me want to be"), ("hook", "The woman Daddy prayed I'd be")]
TG = [("tag", "The man Mama prayed I'd be"), ("tag", "The woman Daddy prayed I'd be")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", C1), ("Verse 2", V2), ("Chorus 2", C2), ("Verse 3", V3), ("Chorus 3", C3), ("Verse 4", V4),
            ("Chorus 4", C4), ("Tag", TG)]
SINGER = {"Chorus 4": "her", "Tag": ("him", "her")}      # who sings: the man everywhere else (the voice, A)
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p64/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
