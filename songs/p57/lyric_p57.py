"""The Singer Doesn't Stop -- the locked lyric (13 Nov, 'Lock it!'). From the writer's paper 'Analytic Continuation Through Death'
(src/, not committed): the song and the singer (Q2 A); one believer singing to God (Q3 A); the science in everyday words (Q9 B)."""
TITLE = "The Singer Doesn't Stop"
V1 = [("verse", "The doctor says a healthy heart never keeps perfect time"), ("verse", "Mama swears I hummed before I talked, and I've been humming ever since"),
      ("verse", "I sing flat on the high part from the third pew on the left"), ("verse", "But one day I'll draw a breath to sing, and the next line won't come")]
CH = [("hook", "The song can stop"), ("hook", "But the singer doesn't stop"), ("chorus", "You remember every note I ever sang"),
      ("chorus", "Every heartbeat out of time"), ("chorus", "You will sing me again"), ("tag", "'Cause the singer doesn't stop")]
V2 = [("verse", "Lazarus walked out of the dark and back into the same old town"), ("verse", "Just a few more years of breathing till they laid him in the ground"),
      ("verse", "But You walked out into a morning where the walls can't keep You in"), ("verse", "With the nail holes in Your hands so Thomas knew You by Your scars")]
BR = [("bridge", "Not a copy, not a cover"), ("bridge", "Not a stranger with my face"), ("bridge", "Every scar and every stumble"),
      ("bridge", "Kept and carried into grace"), ("bridge", "No part of me remembers all of me"), ("bridge", "But You do, oh You do")]
BR2 = BR[:5] + [("bridge", "But You do"), ("bridge", "Yes You do"), ("bridge", "You remember all of me")]
LAST = CH[:3] + [("chorus", "Even the high part I sang flat"), ("chorus", "You will sing me again"), ("chorus", "And it will still be me")]
TAG = [("hook", "The song can stop"), ("tag", "'Cause the singer doesn't stop")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH), ("Verse 2", V2), ("Chorus 2", CH), ("Bridge", BR), ("Bridge 2", BR2), ("Last Chorus", LAST), ("Tag", TAG)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p57/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
