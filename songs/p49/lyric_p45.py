"""Before It's Done -- the locked lyric (draft 4, Q12 A). From the writer's book 'You Will Wake', used and not copied: the verses are
the estrangement and the hospital room, the chorus the unfinished conversation held open (the next room, the hall light, the door), the
bridge the child the night before his birthday (the morning does not depend on him), the last chorus the morning come, the tag the
conversation picked up where it stopped."""
TITLE = "Before It's Done"
V1 = [("verse", "We kept it civil, kept it short, kept it far"), ("verse", "Two kids from the same house on different roads"),
      ("verse", "I was saving it for one kitchen when the folks got old"), ("verse", "Your number's still in my phone, and I don't know where it goes")]
CH = [("chorus", "Hold that thought, I'm still coming"), ("chorus", "You're only in the next room"),
      ("chorus", "Somebody left the hall light on and the door cracked open"), ("hook", "And this time no one calls lights out before it's done")]
V2 = [("verse", "I knew the room before they let us in"), ("verse", "The tissue box, the doctor sitting down and speaking slow"),
      ("verse", "I'd stood in that doorway for a hundred other families"), ("verse", "Never as the brother, walking in with nowhere left to go")]
BRIDGE = [("bridge", "Like a kid the night before his birthday"), ("bridge", "Everything's already waiting in the next room"),
          ("bridge", "The morning doesn't need him to believe it"), ("bridge", "It's coming anyway, it's never missed one yet")]
LAST = [("chorus", "It's morning, and I held the thought"), ("chorus", "You were only in the next room"),
        ("chorus", "And the hall light's on, and the door is open wide"), ("hook", "And no one calls lights out before it's done")]
TAG = [("tag", "Go on"), ("tag", "You were saying before")]
SECTIONS = [("Verse 1", V1), ("Chorus 1", CH), ("Verse 2", V2), ("Chorus 2", CH), ("Bridge", BRIDGE), ("Last Chorus", LAST), ("Tag", TAG)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
import re, importlib.util as _u
_s = _u.spec_from_file_location("intake45", "/home/claude/p49/intake.py"); _I = _u.module_from_spec(_s); _s.loader.exec_module(_I)
_t = " ".join(SUNG).lower()
assert not (set(re.findall(r"[a-z']+", _t)) & set(_I.NEVER_SAY))
assert not any(p in _t for p in _I.NEVER_PHRASES)
_lock = open("/home/claude/p49/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]               # every sung line is the locked lyric's
