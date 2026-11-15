"""Song 52 -- The Room Next Door, from the writer's parable in Wild Fruit; draft 2 locked 14 Nov. Nora sings to Bernard. The final chorus
sings 'there's a door in the wall' twice (the form, A)."""
TITLE = "The Room Next Door"
CH = [("chorus", "It's the north wall, love, but it's warm to my hand"), ("chorus", "like the sun's coming in where the sunlight never falls"),
      ("chorus", "you're just in the room next door"), ("chorus", "and I can't come yet, but I'm not shut out at all"), ("hook", "there's a door in the wall")]
V1 = [("verse", "Forty years I could walk this whole house in the dark"), ("verse", "I could find every door, I could feel every stair"),
      ("verse", "then I heard you get up with that little tired sigh"), ("verse", "and I came with the tea and you weren't in your chair")]
V2 = [("verse", "I have kept your cup and your book on the stand"), ("verse", "lying open face down at the page you were on"),
      ("verse", "and I moved my own chair to the cold north wall"), ("verse", "and I sit there at night when the day is gone")]
V3 = [("verse", "Margaret came in the spring with her bags and her worry"), ("verse", "and she watched me the way that daughters do"),
      ("verse", "and I said hello through the plaster that night"), ("verse", "and I slept the whole night through, the first time since you")]
BR = [("bridge", "One morning early, the light coming in"), ("bridge", "my hand on the wall and the kettle not on"),
      ("bridge", "the room next door came as close as a breath"), ("bridge", "and you were there, and the wall was all but gone")]
V4 = [("verse", "I made us two cups and we sat on the stair"), ("verse", "and she said Mama, you look more than slept"),
      ("verse", "and I said there's a door, and it's going to open"), ("verse", "and I know who'll be there when I take the step")]
FC = [("chorus", "It's the north wall, love, and it's warm to my hand"), ("chorus", "like the sun's coming in where the sunlight never falls"),
      ("chorus", "and some morning it opens and I'll walk through"), ("chorus", "and the first thing I'll know is you, after all"),
      ("hook", "there's a door in the wall"), ("hook", "there's a door in the wall")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH), ("Verse 2", V2), ("Chorus 2", CH), ("Verse 3", V3), ("Bridge", BR), ("Verse 4", V4), ("Last Chorus", FC)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p62/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
