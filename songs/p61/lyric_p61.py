"""Song 51 -- A Wire Pulled Tight, the writer's v5 song revised (draft 3), locked 14 Nov ('A. What genre of song do you think it should be?').
Choruses 2, 3 and the final chorus change lines 5 and 6 (felt / lived / carried; the line after it); every other chorus line the same."""
TITLE = "A Wire Pulled Tight"
def CH(n5, n6):
    return [("chorus", "Every hour is a wire"), ("chorus", "run from the cradle to the stone"), ("chorus", "it hums in the dark of the house"),
            ("chorus", "it rings with every voice you've known"), ("chorus", n5), ("chorus", n6), ("chorus", "and somewhere in the stillness"),
            ("hook", "time is breaking through")]
V1 = [("verse", "There's a chair in the waiting room, white under the light"), ("verse", "where the clock on the wall forgets how to move"),
      ("verse", "a second stretched thin like a wire pulled tight"), ("verse", "the TV on mute with somebody's news")]
P1 = [("pre", "The coffee's gone cold in the paper cup"), ("pre", "and nobody's called my name")]
C1 = CH("I have felt every one", "the long ones in that white-walled room")
V2 = [("verse", "There's a laugh at a table on a warm afternoon"), ("verse", "where the hours slip by like water through hands"),
      ("verse", "you look up and the light's gone halfway round the room"), ("verse", "and nobody noticed and nobody planned")]
P2 = [("pre", "The ice is all water in the glasses"), ("pre", "and nobody wants to go")]
C2 = CH("I have lived every one", "the ones that went like afternoon")
V3 = [("verse", "There's a roar that hits before you know that it's real"), ("verse", "sixty thousand strangers and your feet leave the ground"),
      ("verse", "your hands find hands before your heart can feel"), ("verse", "and for one held breath the clock makes no sound")]
P3 = [("pre", "The bleachers shake under the stamping"), ("pre", "and the lights come up like day")]
C3 = CH("I have carried every one", "the ones where strangers sang in tune")
V4 = [("verse", "Then in a single second something gave way"), ("verse", "the way a fever breaks at three a.m."),
      ("verse", "the sheets gone cold and the window going gray"), ("verse", "and I could hear the birds again")]
BR = [("bridge", "The light came in all at once"), ("bridge", "and I put the clock down"), ("bridge", "every wall I'd built against the waiting"),
      ("bridge", "came apart and let me out"), ("bridge", "The clock still ticking in the dark"), ("bridge", "I can hear it and not count"),
      ("bridge", "none of it was ever lost"), ("bridge", "and none of it was wasted")]
LC = CH("I have carried every one", "and every one I thought I'd lose")
TG = [("tag", "There's a chair in the waiting room, white under the light"), ("tag", "and the weight inside it is a grace")]
SECTIONS = [("Verse 1", V1), ("Pre 1", P1), ("Chorus 1", C1), ("Verse 2", V2), ("Pre 2", P2), ("Chorus 2", C2), ("Verse 3", V3), ("Pre 3", P3),
            ("Chorus 3", C3), ("Verse 4", V4), ("Bridge", BR), ("Last Chorus", LC), ("Tag", TG)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p61/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
