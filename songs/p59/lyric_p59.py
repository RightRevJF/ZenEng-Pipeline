"""The World Is Asking -- the locked lyric (14 Nov, draft 4, 'A': lock it). From the writer's paper Beyond the Kantian Seal (src/, not
committed): the world is asking (A); one who believed the seal (A); answers the summons (A); never the paper's words, never 'God' (B)."""
TITLE = "The World Is Asking"
V1 = [("verse", "There's a door in my father's house"), ("verse", "Painted shut before I was born"), ("verse", "We hung our coats across the seam"),
      ("verse", "And never asked what it was for"), ("verse", "I grew up trusting what I could touch"), ("verse", "The nail, the bread, the roof of tin"),
      ("verse", "And if I heard a knock at night"), ("verse", "I told myself it was the wind")]
CH = [("hook", "But the world is asking"), ("chorus", "In the hum beneath the small"), ("chorus", "In the stutter of my heart"), ("chorus", "In the first light of it all"),
      ("chorus", "It's the knock behind the wall"), ("chorus", "I was taught to call the wind"), ("hook", "The world is asking"), ("chorus", "Will I let the question in")]
V2 = [("verse", "Three strangers working far apart"), ("verse", "Who never knew each other's names"), ("verse", "One counted beats inside a heart"),
      ("verse", "Another chased the oldest flame"), ("verse", "The third heard something like a hum"), ("verse", "Where nothing ought to make a sound"),
      ("verse", "And all of them found, every one"), ("verse", "The same small circle coming round")]
BR = [("bridge", "I don't have proof, I have a door"), ("bridge", "I'm leaving open just a crack"), ("bridge", "If you're the one who's asking"),
      ("bridge", "I won't send the question back"), ("bridge", "Here I am"), ("bridge", "Speak, I'm listening")]
LAST = [("hook", "And the world is asking"), ("chorus", "In the hum beneath the small"), ("chorus", "In the stutter of my heart"), ("chorus", "In the first light of it all"),
        ("chorus", "It's the knock behind the wall"), ("chorus", "And I won't call it the wind"), ("hook", "Here I am, here I am"), ("tag", "Speak, I'm listening")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH), ("Verse 2", V2), ("Chorus 2", CH), ("Bridge", BR), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p59/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
