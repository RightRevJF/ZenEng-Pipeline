"""Swallowed Up -- the locked lyric (draft 2, locked 10 Nov: 'A'). The officiant buries his own father; death metal, the Christian overlay."""
TITLE = "Swallowed Up"
V1 = [("verse", "The straps creak out their slack into the clay."), ("verse", "The tent is drumming with November rain."),
      ("verse", "Hand over hand. Inch by inch."), ("verse", "My father in his Sunday suit."),
      ("verse", "I hold his Bible, margins rubbed to cloth,"), ("verse", "his pencil gouged through every psalm."),
      ("verse", "He drilled these words into my mouth."), ("verse", "Now I read them to the hole.")]
CHORUS = [("hook", "Swallowed up!"), ("chorus", "Clay jaw. Stone throat."), ("chorus", "Never says \"Enough!\""), ("hook", "Swallowed him up!")]
V2 = [("verse", "I stoop and fill my fist with the wet ground,"), ("verse", "cold as iron, heavy as a debt."),
      ("verse", "\"Earth to earth. Ashes. Dust.\""), ("verse", "I throw it. The lid booms back:"),
      ("verse", "a fist on the door at three a.m.,"), ("verse", "the sound since Abel's blood cried out."),
      ("verse", "My mother turns her face into my coat."), ("verse", "The backhoe idles by the hedge.")]
V3 = [("verse", "I step up to the edge and look you in the throat:"), ("verse", "clay walls cut clean, the roots stuck out like nerves,"),
      ("verse", "the rain pooled black and quiet on the vault,"), ("verse", "fake grass thrown over everything you spat."),
      ("verse", "So take him. Hold him. Lock your jaw."), ("verse", "Pack down the clay. Roll on the stone."),
      ("verse", "I read the end. The stone gets moved."), ("verse", "You don't get to keep this one.")]
SLOW = [("taunt", "O death, where is your sting?"), ("taunt", "O grave, where is your victory?"),
        ("taunt", "You'll split like a seed in the ground"), ("taunt", "and give him up at dawn.")]
LAST = [("hook", "Death is swallowed up!"), ("chorus", "Clay jaw. Stone throat."), ("chorus", "Now you've had \"Enough!\""), ("hook", "Swallowed up!")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CHORUS), ("Verse 2", V2), ("Chorus 2", CHORUS), ("Verse 3", V3), ("Chorus 3", CHORUS),
            ("Slowdown", SLOW), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
