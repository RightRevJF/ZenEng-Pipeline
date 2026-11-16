"""Song 55 -- Your Yard Man, the writer's earlier lyric renovated (draft 2), locked 16 Nov ('A'). One singer, the baritone, first person.
Every chorus keeps lines 1, 2, 9 and 10 (the call and its answer, 'That's all I aim to be'); lines 5-8 change each time (Holland; the gold
watch his daddy never got to; Paris); chorus 3 changes lines 3 and 4 as well ('I make my own livin' / Ain't nobody summons me')."""
TITLE = "Your Yard Man"
def CH(l3, l4, a, b, c, d):
    return [("hook", "I'm your yard man"), ("chorus", "That's all I aim to be"), ("chorus", l3), ("chorus", l4), ("chorus", a), ("chorus", b),
            ("chorus", c), ("chorus", d), ("hook", "I'm your yard man"), ("hook", "But I'm my own man")]
V1 = [("verse", "Up at a quarter past pitch black"), ("verse", "Coffee by the jug"), ("verse", "Half-ton, trailer, mower on the back"),
      ("verse", "Pray the reflux don't come up"), ("verse", "I go yard to yard across your town"), ("verse", "And I'm finished up by three"),
      ("verse", "It beats a time clock forty hours"), ("verse", "And a boss with a stopwatch on me")]
C1 = CH("And a long day's work", "Never frightened me", "I may never see Holland", "And I don't mind a bit", "I've weeded enough tulip beds", "To be plumb sick of it")
V2 = [("verse", "My daddy punched the mill clock"), ("verse", "Thirty-one years straight"), ("verse", "They gave him a watch and a sheet cake"),
      ("verse", "And a heart that wouldn't wait"), ("verse", "He spent his last two summers"), ("verse", "In a chair by the kitchen door"),
      ("verse", "Watchin' me cut his grass"), ("verse", "Like he never had time before")]
C2 = CH("And a long day's work", "Never frightened me", "I may never get a gold watch", "Or a party when I'm through", "I'll take the summers Daddy", "Never got to")
V3 = [("verse", "Come Sunday I'm still up at dawn"), ("verse", "But the mower gets a rest"), ("verse", "Second pew in a pressed white shirt"),
      ("verse", "Preacher gives us hell, God bless"), ("verse", "Then I'm out on the lake by noon"), ("verse", "Old Glory on my hat"),
      ("verse", "My phone's back in the half-ton"), ("verse", "And I ain't callin' back")]
C3 = CH("I make my own livin'", "Ain't nobody summons me", "I may never see Paris", "And I can live with that", "Couldn't park the trailer anywhere", "And they'd laugh at my hat")
TG = [("tag", "I'm your yard man"), ("tag", "But I'm my own man")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", C1), ("Verse 2", V2), ("Chorus 2", C2), ("Verse 3", V3), ("Chorus 3", C3), ("Tag", TG)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p65/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
