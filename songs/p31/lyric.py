"""Song 31, 'Nothing On' -- the lyric, four drafts, locked by the writer (8 Nov 2026, 05:03). One female pop lead with a backing echo,
first person. Draft 2 took the writer's five notes; draft 3 turned the chorus into a choice that grows (hope they stay off -> if they come
back I'll turn them off -> they came back and I turned them off); draft 4 rewrote pre-chorus 2, the bridge and the last post-chorus."""
TITLE = "Nothing On"
V1 = [("verse", "ten-fifteen and the whole street blinks"), ("verse", "the fridge goes quiet and the fan spins down"),
      ("verse", "my phone's on nine and I'm letting it die"), ("verse", "the only thing glowing is you")]
PRE1 = [("pre", "the air went off and the room got warm"), ("pre", "so quiet I can hear you breathe")]
CH1 = [("hook", "nothing on, nothing on"), ("chorus", "everybody's waiting on the lights"), ("chorus", "I hope they never come back on"),
       ("hook", "nothing on, nothing on")]
POST = [("post", "nothing on but the moon"), ("post", "nothing on but you")]
V2 = [("verse", "found a candle from your birthday in the kitchen drawer"), ("verse", "you struck a match and pulled me to the floor"),
      ("verse", "you told me things you'd never say with the lights on"), ("verse", "funny what you see when there's nothing to see")]
PRE2 = [("pre", "the candle gave out and I heard you smile"), ("pre", "say my name till I find where you are")]
CH2 = [("hook", "nothing on, nothing on"), ("chorus", "can't see a thing, so we'll go by feel"), ("chorus", "and if they come back, I'll turn them off"),
       ("hook", "nothing on, nothing on")]
BRIDGE = [("bridge", "two a.m. and the fridge clears its throat"), ("bridge", "every window on the street opens one eye"),
          ("bridge", "the microwave's blinking like it caught us"), ("bridge", "my hand finds the switch and I hold my breath")]
CH3 = [("hook", "nothing on, nothing on"), ("chorus", "my phone woke up and I let it ring"), ("turn", "the lights came back and I turned them off"),
       ("hook", "nothing on, nothing on")]
POST3 = [("post", "nothing on but the moon"), ("post", "nothing on but the moon"), ("tag", "and the only thing glowing is you")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH1), ("Post 1", POST), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH2),
            ("Post 2", POST), ("Bridge", BRIDGE), ("Chorus 3", CH3), ("Post 3", POST3)]
SINGER = {s: "her" for s, _ in SECTIONS}
ECHO = {("Post 1", 1): "nothing on", ("Post 2", 1): "nothing on", ("Post 3", 1): "nothing on"}   # the backing echo before the lead's line
SUNG = [l for _, ls in SECTIONS for _, l in ls]
PICKS = [("DRAFT 1 -> 2 (04:40)", "the writer's five notes", "the room getting warm; a direction that 'go by feel' answers; the bridge's choice in the body; one more detail of 'you'; the knock trimmed"),
         ("DRAFT 2 -> 3 (04:53)", "the writer's notes", "the chorus reveals the relationship; 'the lights came back and I turned them off' planted in chorus 2 and paid off last; a repeatable line; verse 2 intimate; a bigger final lift"),
         ("DRAFT 3 -> 4 (04:58)", "the writer's notes", "pre-chorus 2 deepened; the bridge's house wakes and watches; the last post-chorus without the doubled 'you'"),
         ("LOCK (05:03)", "the writer's lock", "draft 4: 'remember what you learned from your research'")]
