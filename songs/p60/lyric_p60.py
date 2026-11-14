"""Song 50 -- the writer's lyric, locked (14 Nov): 'Nice.' / 'Do it!'. Every chorus the same words; the last chorus slows on its last line."""
TITLE = "The Small Things"
V1 = [("verse", "Late afternoon comes rolling in"), ("verse", "and lays itself across the floor"), ("verse", "Sammie takes his post again"),
      ("verse", "just left of the sliding glass door"), ("verse", "A bumblebee goes bouncing by"), ("verse", "fat and gold and full of sound"),
      ("verse", "Maggie hits the glass with both paws"), ("verse", "and doesn't even slow down")]
CH = [("chorus", "And I think somebody's watching this"), ("chorus", "the same way I do from the couch"), ("chorus", "I think somebody's laughing too"),
      ("chorus", "at old Sammie in his crouch"), ("chorus", "that the bees keep flying and the cats keep trying"), ("chorus", "and the afternoon holds still"),
      ("hook", "I think God likes the small things"), ("hook", "I think He always will")]
V2 = [("verse", "There's no moral to the story here"), ("verse", "no lesson I can name"), ("verse", "just Sammie and Maggie doing their work"),
      ("verse", "and the glass doing the same"), ("verse", "The light comes sideways through the door"), ("verse", "and turns the whole room gold"),
      ("verse", "and I think I'll remember this"), ("verse", "long after I am old")]
BR = [("bridge", "Nobody wrote this down"), ("bridge", "nobody sent me here"), ("bridge", "I just sat down on a Tuesday"), ("bridge", "and the holy showed up clear")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH), ("Verse 2", V2), ("Chorus 2", CH), ("Bridge", BR), ("Last Chorus", CH)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p60/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
