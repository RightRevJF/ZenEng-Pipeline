"""Windows Down -- lyric draft 3 (locked 10 Nov: 'A'). A man walks out of his plant's last shift after twenty-six years and drives home
to his wife, windows down to air the cutting oil out of his clothes: the job ended, he didn't."""
TITLE = "Windows Down"
V1 = [("verse", "The clock still runs four minutes fast,"), ("verse", "we always said we'd fix it someday;"),
      ("verse", "I peeled your picture off my locker door"), ("verse", "and gave the rest of it away.")]
PRE1 = [("pre", "Noon, and my shadow's under my boots,"), ("pre", "like it doesn't know where to go —")]
CH = [("hook", "Windows down till the oil smell's gone,"), ("hook", "windows down with the heater on,"),
      ("chorus", "Number Four went quiet, but I'm not,"), ("chorus", "I'm hollering home with all I've got.")]
CHORUS = CH + CH                                   # sung twice (Q12: 16-bar choruses)
V2 = [("verse", "I shook Mike's hand and held it long,"), ("verse", "Sal's still got his hand on the gate;"),
      ("verse", "it gave the same old squeal it always gave,"), ("verse", "and I almost asked it to wait.")]
PRE2 = [("pre", "My thumb left oil on the phone,"), ("pre", "you didn't ask me what comes next —")]
BRIDGE = [("bridge", "I was nineteen when I walked in,"), ("bridge", "you packed my lunch that first cold day;"),
          ("bridge", "they had my hands for twenty-six years,"), ("bridge", "but you had me the whole damn way.")]
LAST = CH + [("hook", "Windows down till the oil smell's gone,"), ("hook", "windows down, but leave a little on;"),
             ("chorus", "Number Four can keep the quiet now,"), ("chorus", "I'm almost home. I'm almost home.")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CHORUS), ("Bridge", BRIDGE), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
NEVER_PHRASES = ["blue collar", "working man", "american dream", "the man upstairs", "bought and sold", "rust belt", "main street", "the open road", "glory days", "born to run", "stand tall"]
