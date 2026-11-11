"""The Water Used to Sing -- the locked lyric (11 Nov, Q14 A). From When the Bible Refuses to Behave, abstractly: mastery over a living
thing drains the joy and the sustenance out of it. A man dams the river he loved; the valley dies; his daughter asks what a river sounds
like; he opens the gate and the water comes back, singing and dangerous. No church word is said; one faint echo ('living water')."""
TITLE = "The Water Used to Sing"
V1 = [("verse", "It came off the ridge in a hurry,"), ("verse", "loud as a county fair,"), ("verse", "took the low field every April,"),
      ("verse", "gave it back black by June;"), ("verse", "we cursed it over supper"), ("verse", "and swam in it after dark.")]
PRE1 = [("pre", "I had a slide rule and a reason,"), ("pre", "and I knew what to do with stone:")]
CH = [("hook", "The water used to sing"), ("chorus", "the whole night under my window,"), ("hook", "the water used to sing."), ("chorus", "Now it only shines.")]
V2 = [("verse", "I poured the wall in August,"), ("verse", "forty feet of patient grey,"), ("verse", "and the river lay down like a sheepdog"),
      ("verse", "when it hears its name;"), ("verse", "they cut a ribbon, shook my hand,"), ("verse", "the lights came on in town.")]
PRE2 = [("pre", "The whole town called the quiet peace,"), ("pre", "and I slept like a stone:")]
BRIDGE = [("bridge", "Below the wall the willows went to paper,"), ("bridge", "the corn came up in matchsticks,"), ("bridge", "the mill wheel stopped like a dead man's watch,"),
          ("bridge", "the rope swing hung over dust,"), ("bridge", "and my girl said, \"Daddy, what's a river sound like?\""), ("bridge", "I didn't have an answer.")]
V3 = [("verse", "I took her up the wall that night and turned the wheel,"), ("verse", "it fought me like a mule,"), ("verse", "then the whole lake leaned against the gate"),
      ("verse", "and the gate let go;"), ("verse", "it went down the valley shouting,"), ("verse", "took my fence and the plaque with my name.")]
LAST = [("hook", "The water used to sing"), ("chorus", "the whole night under my window,"), ("chorus", "the water's singing now,"), ("chorus", "loud and crooked in the dark."),
        ("chorus", "It took the fence, it took the road,"), ("chorus", "it's in the cellar, at the door;"), ("chorus", "living water doesn't shine."), ("tag", "It sings.")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH), ("Bridge", BRIDGE),
            ("Verse 3", V3), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
NEVER_SAY = ["god", "lord", "holy", "faith", "grace", "gospel", "scripture", "bible", "church", "word", "verse", "pray", "prayer", "sin", "jesus", "christ",
             "heaven", "control", "mastery", "master", "joy", "meaning", "lesson", "soul"]
NEVER_PHRASES = ["go with the flow", "still waters run deep", "bridge over troubled water", "let it flow", "river runs deep", "let it be"]
ECHO = "living water"                                                                   # Q10 B: the one faint echo allowed
import re
_words = set(re.findall(r"[a-z']+", " ".join(SUNG).lower()))
assert not (_words & set(NEVER_SAY)), _words & set(NEVER_SAY)
assert not any(p in " ".join(SUNG).lower() for p in NEVER_PHRASES)
assert " ".join(SUNG).lower().count(ECHO) == 1
