"""Song 57 -- Jehovah's Band, from the writer's 'Acid Soaked Ramblings of Poetry' (the pilgrimage seam), lyric draft 4 locked 17 Nov ('B').
One singer, the baritone. The two choruses are the same words; the last chorus keeps lines 1 and 5 and turns the rest toward home, its
'Thank God' line sung twice; the outro (engine name 'Tag') is the title three times. Lines with the title are role 'hook' (232: the
title's stress on beat 1 or 3; H3)."""
TITLE = "Jehovah's Band"
CH = [("hook", "I been sitting in with Jehovah's band"), ("chorus", "Out across the sands of time"), ("chorus", "The moon was keeping the beat for us"),
      ("chorus", "And the angels sang glory in rhyme"), ("hook", "I been sitting in with Jehovah's band"), ("chorus", "Grinning like a dog that slipped out of the yard")]
V1 = [("verse", "Down in the basement of the attic of my mind"), ("verse", "A voice like gravel and honey came up the stair"),
      ("verse", "It called me by a name that wasn't mine and I said yes"), ("verse", "And I carried my spark like a match down there")]
V2 = [("verse", "My bare heels pounding the red dirt flat"), ("verse", "Sweat in my eyes and the moon running down my back"),
      ("verse", "Laughing I slipped through a seam to the world next door"), ("verse", "We were dancing there and the beast couldn't follow that")]
BR = [("bridge", "Then a county man in a sweat-stained cap"), ("bridge", "Leaned on his truck where the meadow turned to sand"),
      ("bridge", "Said son, that sand ain't supposed to sing"), ("bridge", "And he laughed till the drummer laid down his hands"),
      ("bridge", "He pinched out my spark with a licked finger and thumb"), ("bridge", "The angels closed their books and the moon went out"),
      ("bridge", "And I lost the sound of my daughter's name")]
V3 = [("verse", "I came to in a booth with a skin on my coffee"), ("verse", "Counted my fingers twice and didn't know the town"),
      ("verse", "A waitress with hair black as coal called me honey"), ("verse", "And the word just rolled off the table and down"),
      ("verse", "Then home, and my daughter came laughing down the hall"), ("verse", "Gold hair shining and she called me by my name"),
      ("verse", "The light above the stove came up like the moon"), ("verse", "And the icebox picked up where the drummer left off")]
LC = [("hook", "I been sitting in with Jehovah's band"), ("chorus", "Not out across the sands of time"), ("chorus", "Her bare feet drumming the linoleum floor"),
      ("chorus", "And she sings the angels' line over the frying pan"), ("hook", "I been sitting in with Jehovah's band"),
      ("chorus", "Thank God the band followed me home"), ("chorus", "Thank God the band followed me home")]
TG = [("hook", "Jehovah's band"), ("hook", "Jehovah's band"), ("hook", "Jehovah's band")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", list(CH)), ("Verse 2", V2), ("Chorus 2", list(CH)), ("Bridge", BR), ("Verse 3", V3), ("Chorus 3", LC), ("Tag", TG)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p67/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
