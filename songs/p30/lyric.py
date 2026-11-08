"""Song 30, 'She Left the Light On' -- the lyric, two drafts, locked by the writer (7 Nov 2026, 19:53). One male country voice, first
person. Draft 2 moved verse 2 into the past ('That was the year her knees gave out') so the bridge's 'still' and 'a year' read as now."""
TITLE = "She Left the Light On"
V1 = [("verse", "seventeen and an hour late, I'd cut the engine at the road"), ("verse", "coast the last of the gravel in like Mama wouldn't know"),
      ("verse", "never wondered who'd been oiling that screen door all along"), ("verse", "and every time I topped that hill, she left the light on")]
CHORUS = [("hook", "she left the light on"), ("chorus", "it never asked me where I'd been"), ("chorus", "it just showed me the way back in"),
          ("hook", "she left the light on")]
V2 = [("verse", "when my own boy got the keys and the clock went past two"), ("verse", "I stood at the window doing what she used to do"),
      ("verse", "that was the year her knees gave out, I hooked her porch light to my phone"), ("verse", "and lit hers too at sundown, three hundred miles from home")]
BRIDGE = [("bridge", "there's a button on my phone that still says Mama's Porch"), ("bridge", "every evening right at dark, it comes on by itself"),
          ("bridge", "I've had a year to shut it off, it'd only take my thumb")]
LAST = [("turn", "now you're the one out late"), ("hook", "so I leave the light on"), ("chorus", "I won't ask you where you've been"),
        ("chorus", "I'll just show you the way back in"), ("hook", "I leave the light on")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Chorus 2", CHORUS), ("Bridge", BRIDGE), ("Chorus 3", LAST)]
SINGER = {s: "him" for s, _ in SECTIONS}
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [("DRAFT 1 -> 2 (19:51)", "the writer's note", "timeline clarity: verse 2 in the past ('got', 'stood', 'That was the year her knees gave out', 'lit')"),
         ("LOCK (19:53)", "the writer's lock", "draft 2: 'Make this a country hit'")]
