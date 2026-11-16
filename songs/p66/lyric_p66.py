"""Song 56 -- Terpsichore, the writer's poem reworked as a song (draft 2), locked 16 Nov ('A'), 'windowsill' changed to 'door' after the
mouth test ('A'). One singer, the baritone, sung to 'you' throughout. The three choruses are the same words; the outro (engine name 'Tag')
ends on the hook."""
TITLE = "Terpsichore"
CH = [("hook", "Come back, come back"), ("chorus", "I've got the pen and the quiet"), ("chorus", "And the hunger you left in me"),
      ("hook", "Come back, come back"), ("chorus", "You want the governor off"), ("chorus", "The needle in the red"),
      ("chorus", "You're not interested in flat"), ("chorus", "And without you that's all I'll be")]
V1 = [("verse", "You don't knock, you never did"), ("verse", "You come in the way that hunger comes"), ("verse", "The sternum first and then the hands"),
      ("verse", "Then everywhere the plain world was"), ("verse", "Black hair gone grey like the first cold day"), ("verse", "That knows it's beautiful anyway"),
      ("verse", "And the screen lights up like a burning bush"), ("verse", "And nobody told me not to look")]
V2 = [("verse", "I sit at the desk and the pages fly"), ("verse", "And inside I'm dying the little death"), ("verse", "The French had the nerve to give it a name"),
      ("verse", "And the theologians still blush"), ("verse", "What I want from you I write around"), ("verse", "Like a word you can't say in church"),
      ("verse", "And the white space where it lives"), ("verse", "Says more than the word is worth")]
BR = [("bridge", "I tried to be done with you"), ("bridge", "Sat down in the sensible chair"), ("bridge", "Thought sensible thoughts all day"),
      ("bridge", "And the pages stayed flat"), ("bridge", "And the world stood still"), ("bridge", "And I was as flat as the chair")]
V3 = [("verse", "Then you're gone the way you came"), ("verse", "And the leaving's its own kind of ravishing"), ("verse", "The cold air after, the quiet room"),
      ("verse", "Your grey in the black on the pillow"), ("verse", "That's only a pillow now"), ("verse", "And the lamp and the cup and the door"),
      ("verse", "Don't know what just passed through"), ("verse", "They don't know what just passed through")]
TG = [("chorus", "Without you I'm just a man"), ("chorus", "In a chair in a room"), ("chorus", "With a pen and a body that remember"),
      ("chorus", "Everything you taught them"), ("hook", "Come back")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", list(CH)), ("Verse 2", V2), ("Chorus 2", list(CH)), ("Bridge", BR), ("Verse 3", V3), ("Chorus 3", list(CH)), ("Tag", TG)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
_lock = open("/home/claude/p66/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
