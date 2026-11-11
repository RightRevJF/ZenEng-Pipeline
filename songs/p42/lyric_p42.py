"""Nothing Important -- the locked lyric (11 Nov, Q12 A). From Resurrection-Shaped Architecture, abstractly: the part holds the whole;
an identity outlives what carried it; he is known again by his marks; the promise of return comes from his side. Nothing is named."""
TITLE = "Nothing Important"
V1 = [("verse", "There's an old phone in the kitchen drawer,"), ("verse", "one saved message from March ninth;"),
      ("verse", "you can hear his blinker, his ring tapping the wheel,"), ("verse", "and he laughs like always before hello:")]
CH = [("hook", "Hey, it's me, nothing important,"), ("chorus", "I'm at the light on Seventh Street and thought of you;"),
      ("chorus", "hey, it's me, just wanted to hear you."), ("chorus", "Call me back.")]
V2 = [("verse", "In October the battery swelled"), ("verse", "and the screen came up off the case;"),
      ("verse", "the kid at the counter said, \"Nothing to save,\""), ("verse", "I said, \"There's one thing on it,\" and he looked away.")]
BRIDGE = [("bridge", "So I sat up with it one last night,"), ("bridge", "played it till the light went red,"),
          ("bridge", "the blinker and the laugh on Seventh Street,"), ("bridge", "and then it wouldn't turn back on.")]
V3 = [("verse", "Three days I kept the drawer shut,"), ("verse", "didn't play the radio;"),
      ("verse", "then the third morning at the sink I heard him,"), ("verse", "the laugh before he said hello:")]
LAST = [("hook", "Hey, it's me, nothing important,"), ("chorus", "I'm at the light on Seventh Street and thought of you;"),
        ("chorus", "hey, it's me, just wanted to hear you."), ("chorus", "Hey, it's me."), ("hook", "Nothing important."), ("chorus", "I'll call you back.")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH), ("Verse 2", V2), ("Chorus 2", CH), ("Bridge", BRIDGE), ("Verse 3", V3), ("Last Chorus", LAST)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
import re, importlib.util as _u
_s = _u.spec_from_file_location("intake42", "/home/claude/p42/intake.py"); _I = _u.module_from_spec(_s); _s.loader.exec_module(_I)
NEVER_SAY, NEVER_PHRASES = _I.NEVER_SAY, _I.NEVER_PHRASES
_t = " ".join(SUNG).lower()
assert not (set(re.findall(r"[a-z']+", _t)) & set(NEVER_SAY)) and not any(p in _t for p in NEVER_PHRASES)
assert _t.count("third morning") == 1                                                   # Q9 B: the one faint echo
