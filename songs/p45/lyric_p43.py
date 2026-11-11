"""Blue Movie -- the locked lyric (11 Nov, Q13 A). From the writer's sonnet 'Blue Movie', used and not copied; the incident's
details from intake (the sign she photographed, the film, the pleather); present tense in the theater; the after only at the end."""
TITLE = "Blue Movie"
V1 = [("verse", "We paid cash, kept our heads down past the sign"), ("verse", "you read the rules out loud and laughed at each"),
      ("verse", "you snapped a picture, said it's mine"), ("verse", "like you'd need proof of every breach")]
PRE1 = [("pre", "You pulled my mask down, broke the first"), ("pre", "your mouth a red pen crossing out the rest")]
CH = [("chorus", "Let them have the screen, we've got the seats"), ("chorus", "let them fake it, we don't have to"),
      ("hook", "blue movie, blue movie"), ("chorus", "starring nobody but you")]
POST = [("tag", "Blue, blue, blue movie"), ("tag", "no one else in the blue movie")]
V2 = [("verse", "Black pleather sweating, cold to heat"), ("verse", "you climb me while the speakers moan"),
      ("verse", "the blue light licks you, beat by beat"), ("verse", "the blonde up there is on her own")]
PRE2 = [("pre", "Somebody shifts two rows behind"), ("pre", "you bite my shoulder, laugh, and climb")]
BRIDGE = [("bridge", "Don't let the house lights come up yet"), ("bridge", "don't let the credits start to roll"),
          ("bridge", "I'll know you like a tongue still knows"), ("bridge", "the empty socket of a tooth")]
LAST = CH[:3] + [("chorus", "starring only me and you")]
POST3 = [("chorus", "The film still loops, there isn't any screen"), ("chorus", "you climb me still, scene after scene")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH), ("Post 1", POST), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH),
            ("Post 2", POST), ("Bridge", BRIDGE), ("Last Chorus", LAST), ("Post 3", POST3)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
import re, importlib.util as _u
_s = _u.spec_from_file_location("intake43", "/home/claude/p45/intake.py"); _I = _u.module_from_spec(_s); _s.loader.exec_module(_I)
_t = " ".join(SUNG).lower()
assert not (set(re.findall(r"[a-z']+", _t)) & set(_I.NEVER_SAY))
_lock = open("/home/claude/p45/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]               # every sung line is the locked lyric's
